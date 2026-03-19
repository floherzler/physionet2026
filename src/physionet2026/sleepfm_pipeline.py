from __future__ import annotations

import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import resample_poly

from .vendor_sleepfm import SetTransformer

TARGET_SAMPLE_RATE = 128
TOKEN_SECONDS = 5
TOKEN_SAMPLES = TARGET_SAMPLE_RATE * TOKEN_SECONDS
NIGHT_HOURS = 9
TOTAL_SAMPLES = TARGET_SAMPLE_RATE * 60 * 60 * NIGHT_HOURS
TOTAL_TOKENS = TOTAL_SAMPLES // TOKEN_SAMPLES
EMBED_DIM = 128
MODALITY_ORDER = ("BAS", "RESP", "EKG", "EMG")
PREPROCESS_VERSION = "q0008-v1"

CATEGORY_TO_MODALITY = {
    "eeg": "BAS",
    "eog": "BAS",
    "ecg": "EKG",
    "resp": "RESP",
    "chin emg": "EMG",
    "leg emg": "EMG",
}


class MissingSignalError(RuntimeError):
    pass


def normalize_label(label: str) -> str:
    return "".join(ch.lower() for ch in label if ch.isalnum())


def load_runtime_channel_map(repo_root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    table = pd.read_csv(repo_root / "channel_table.csv")
    for _, row in table.iterrows():
        modality = CATEGORY_TO_MODALITY.get(str(row["Category"]).strip().lower())
        if modality is None:
            continue
        for alias in str(row["Channel_Names"]).split(";"):
            norm = normalize_label(alias)
            if norm:
                mapping[norm] = modality
    return mapping


def load_edf_signals(edf_path: Path) -> tuple[dict[str, np.ndarray], dict[str, float]]:
    import edfio

    edf = edfio.read_edf(str(edf_path), lazy_load_data=False)
    signals: dict[str, np.ndarray] = {}
    sample_rates: dict[str, float] = {}
    for sig in edf.signals:
        label = str(sig.label).strip()
        signals[label] = np.asarray(sig.data, dtype=np.float32)
        sample_rates[label] = float(sig.sampling_frequency)
    return signals, sample_rates


def resample_to_rate(signal: np.ndarray, source_rate: float, target_rate: int = TARGET_SAMPLE_RATE) -> np.ndarray:
    if int(round(source_rate)) == target_rate:
        return signal.astype(np.float32, copy=False)
    ratio = Fraction(target_rate / source_rate).limit_denominator(1000)
    out = resample_poly(signal, ratio.numerator, ratio.denominator)
    return out.astype(np.float32, copy=False)


def zscore(signal: np.ndarray) -> np.ndarray:
    mean = float(np.mean(signal))
    std = float(np.std(signal))
    if std <= 0:
        return signal - mean
    return (signal - mean) / std


@dataclass
class SleepFMBundle:
    model: object
    device: object


def get_sleepfm_checkpoint(repo_root: Path) -> Path:
    vendored = repo_root / "vendor" / "sleepfm" / "checkpoints" / "model_base" / "best.pt"
    if vendored.is_file():
        return vendored
    external = repo_root / "external" / "sleepfm-clinical" / "sleepfm" / "checkpoints" / "model_base" / "best.pt"
    if external.is_file():
        return external
    raise FileNotFoundError("SleepFM base checkpoint not found in vendor/ or external/ paths.")


def load_sleepfm_bundle(repo_root: Path, device_name: str = "cpu") -> SleepFMBundle:
    import torch

    device = torch.device(device_name if device_name != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    model = SetTransformer(
        in_channels=1,
        patch_size=TOKEN_SAMPLES,
        embed_dim=EMBED_DIM,
        num_heads=8,
        num_layers=6,
        pooling_head=8,
        dropout=0.0,
    ).to(device)
    checkpoint = torch.load(str(get_sleepfm_checkpoint(repo_root)), map_location=device)
    state = checkpoint["state_dict"] if isinstance(checkpoint, dict) and "state_dict" in checkpoint else checkpoint
    cleaned = {k.replace("module.", "", 1): v for k, v in state.items()}
    model.load_state_dict(cleaned, strict=False)
    model.eval()
    return SleepFMBundle(model=model, device=device)


def map_signals_to_modalities(
    signals: dict[str, np.ndarray],
    sample_rates: dict[str, float],
    channel_map: dict[str, str],
) -> tuple[dict[str, list[np.ndarray]], int, dict[str, list[str]]]:
    modality_signals: dict[str, list[np.ndarray]] = {modality: [] for modality in MODALITY_ORDER}
    modality_labels: dict[str, list[str]] = {modality: [] for modality in MODALITY_ORDER}
    max_len = 0
    ordered_labels = sorted(signals.keys(), key=lambda item: normalize_label(item))
    for label in ordered_labels:
        modality = channel_map.get(normalize_label(label))
        if modality is None:
            continue
        resampled = zscore(resample_to_rate(signals[label], sample_rates[label]))
        modality_signals[modality].append(resampled)
        modality_labels[modality].append(label)
        max_len = max(max_len, len(resampled))
    modality_signals = {k: v for k, v in modality_signals.items() if v}
    modality_labels = {k: v for k, v in modality_labels.items() if v}
    return modality_signals, max_len, modality_labels


def crop_or_pad(signal: np.ndarray, total_samples: int = TOTAL_SAMPLES) -> np.ndarray:
    if len(signal) >= total_samples:
        return signal[:total_samples].astype(np.float32, copy=False)
    out = np.zeros(total_samples, dtype=np.float32)
    out[: len(signal)] = signal
    return out


def extract_sequence_embeddings(
    edf_path: Path,
    repo_root: Path,
    bundle: SleepFMBundle,
    batch_windows: int = 128,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    import torch

    signals, sample_rates = load_edf_signals(edf_path)
    channel_map = load_runtime_channel_map(repo_root)
    modality_signals, max_len, modality_labels = map_signals_to_modalities(signals, sample_rates, channel_map)
    if not modality_signals:
        raise MissingSignalError(f"No supported SleepFM channels found in {edf_path}.")

    valid_tokens = min(TOTAL_TOKENS, int(math.ceil(max_len / TOKEN_SAMPLES))) if max_len > 0 else 0
    modality_embeddings = []
    modality_presence = []
    with torch.no_grad():
        for modality in MODALITY_ORDER:
            channels = modality_signals.get(modality)
            if not channels:
                continue
            standardized = np.stack([crop_or_pad(channel) for channel in channels], axis=0)
            windows = standardized.reshape(standardized.shape[0], TOTAL_TOKENS, TOKEN_SAMPLES)
            windows = np.transpose(windows, (1, 0, 2))
            outputs = []
            for start in range(0, TOTAL_TOKENS, batch_windows):
                batch = windows[start : start + batch_windows]
                x = torch.from_numpy(batch).float().to(bundle.device)
                mask = torch.zeros((x.shape[0], x.shape[1]), dtype=torch.bool, device=bundle.device)
                pooled, _ = bundle.model(x, mask)
                outputs.append(pooled.detach().cpu().numpy().astype(np.float32, copy=False))
            modality_embeddings.append(np.concatenate(outputs, axis=0))
            modality_presence.append(modality)

    stacked = np.stack(modality_embeddings, axis=0)
    pooled = stacked.mean(axis=0).astype(np.float32, copy=False)
    valid_mask = np.zeros(TOTAL_TOKENS, dtype=bool)
    valid_mask[:valid_tokens] = True
    pooled[~valid_mask] = 0.0
    metadata = {
        "valid_tokens": valid_tokens,
        "present_modalities": modality_presence,
        "channel_labels": modality_labels,
        "preprocess_version": PREPROCESS_VERSION,
    }
    return pooled, valid_mask, metadata


def sequence_cache_path(cache_root: Path, site_id: str, bids_folder: str, session_id: str) -> Path:
    return cache_root / site_id / bids_folder / f"ses-{session_id}" / "sequence_cache.npz"


def save_sequence_cache(
    cache_path: Path,
    embeddings: np.ndarray,
    valid_mask: np.ndarray,
    age: float,
    sex_code: float,
    label: float,
    patient_id: str,
    metadata: dict[str, object],
) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        cache_path,
        embeddings=embeddings.astype(np.float32, copy=False),
        valid_mask=valid_mask.astype(bool, copy=False),
        age=np.array(age, dtype=np.float32),
        sex_code=np.array(sex_code, dtype=np.float32),
        label=np.array(label, dtype=np.float32),
        patient_id=np.array(patient_id),
        metadata=np.array(json.dumps(metadata)),
    )


def load_sequence_cache(cache_path: Path) -> dict[str, np.ndarray]:
    with np.load(cache_path, allow_pickle=False) as npz:
        return {key: npz[key] for key in npz.files}
