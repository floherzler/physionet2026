#!/usr/bin/env python3
"""Extract offline SleepFM embeddings into the locked Q-0004 cache contract."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.signal import resample_poly

ADAPTER_VERSION = "q0004-v1"
MODALITY_ORDER = ("BAS", "RESP", "EKG", "EMG")
MANIFEST_COLUMNS = [
    "site_id",
    "bids_folder",
    "session_id",
    "cache_key",
    "cache_path",
    "meta_path",
    "sleepfm_commit",
    "adapter_version",
    "status",
    "error_message",
    "num_windows",
    "embedding_dim",
    "created_utc",
]
STATUS_VALUES = {"ok", "missing_input", "preprocess_error", "inference_error", "write_error"}


class PreprocessError(RuntimeError):
    pass


class InferenceError(RuntimeError):
    pass


class WriteError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_session_id(raw_value: object) -> str:
    raw = str(raw_value).strip()
    if raw.endswith(".0"):
        raw = raw[:-2]
    return raw


def read_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def zscore_1d(signal: np.ndarray) -> np.ndarray:
    mean = float(np.mean(signal))
    std = float(np.std(signal))
    if std <= 0.0:
        return signal - mean
    return (signal - mean) / std


def resample_to_rate(signal: np.ndarray, source_rate: float, target_rate: int) -> np.ndarray:
    if source_rate <= 0:
        raise PreprocessError(f"invalid sampling rate: {source_rate}")
    if int(round(source_rate)) == target_rate:
        return signal.astype(np.float32, copy=False)

    ratio = Fraction(target_rate / source_rate).limit_denominator(1000)
    out = resample_poly(signal, ratio.numerator, ratio.denominator)
    return out.astype(np.float32, copy=False)


def get_sleepfm_commit(sleepfm_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(sleepfm_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except Exception:
        return "unknown"


def resolve_demographics_path(data_folder: Path) -> Path:
    candidates = [data_folder / "demographics.csv", data_folder.parent / "demographics.csv"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find demographics.csv. Checked: {', '.join(str(c) for c in candidates)}"
    )


def resolve_physiological_root(data_folder: Path) -> Path:
    candidates = [data_folder / "physiological_data", data_folder / "training_set" / "physiological_data"]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"Could not find physiological_data folder. Checked: {', '.join(str(c) for c in candidates)}"
    )


def maybe_import_torch():
    try:
        import torch  # type: ignore

        return torch, None
    except Exception as exc:  # pragma: no cover - environment dependent
        return None, str(exc)


def maybe_import_h5py():
    try:
        import h5py  # type: ignore

        return h5py, None
    except Exception as exc:  # pragma: no cover - environment dependent
        return None, str(exc)


def read_edf_signals(edf_path: Path) -> Dict[str, List[Tuple[np.ndarray, float]]]:
    """Return mapping: channel_label -> list[(signal, sample_rate)]."""
    signals: Dict[str, List[Tuple[np.ndarray, float]]] = {}

    try:
        import pyedflib  # type: ignore

        with pyedflib.EdfReader(str(edf_path)) as reader:
            n = reader.signals_in_file
            labels = [reader.getLabel(i).strip() for i in range(n)]
            sample_rates = [float(reader.getSampleFrequency(i)) for i in range(n)]
            for i, (label, rate) in enumerate(zip(labels, sample_rates)):
                arr = np.asarray(reader.readSignal(i), dtype=np.float32)
                signals.setdefault(label, []).append((arr, rate))
        return signals
    except ModuleNotFoundError:
        pass
    except Exception as exc:
        raise PreprocessError(f"pyedflib failed reading {edf_path}: {exc}") from exc

    try:
        from edfio import read_edf  # type: ignore

        rec = read_edf(str(edf_path))
        for sig in rec.signals:  # edfio API
            label = str(sig.label).strip()
            arr = np.asarray(sig.samples, dtype=np.float32)
            rate = float(sig.sampling_frequency)
            signals.setdefault(label, []).append((arr, rate))
        if not signals:
            raise PreprocessError(f"No channels read from EDF: {edf_path}")
        return signals
    except ModuleNotFoundError as exc:
        raise PreprocessError(
            f"No EDF reader available for {edf_path}; install pyedflib or edfio ({exc})"
        ) from exc
    except Exception as exc:
        raise PreprocessError(f"edfio failed reading {edf_path}: {exc}") from exc


def pick_modality_arrays(
    signals_by_label: Dict[str, List[Tuple[np.ndarray, float]]],
    channel_groups: Dict[str, List[str]],
    target_rate: int,
) -> Dict[str, np.ndarray]:
    modality_arrays: Dict[str, np.ndarray] = {}
    for modality in MODALITY_ORDER:
        channels = channel_groups.get(modality, [])
        selected: List[np.ndarray] = []
        for channel_name in channels:
            if channel_name not in signals_by_label:
                continue
            signal, source_rate = signals_by_label[channel_name][0]
            resampled = resample_to_rate(signal, source_rate=source_rate, target_rate=target_rate)
            selected.append(zscore_1d(resampled))

        if not selected:
            continue
        min_len = min(len(x) for x in selected)
        if min_len <= 0:
            continue
        trimmed = np.stack([x[:min_len] for x in selected]).astype(np.float32, copy=False)
        modality_arrays[modality] = trimmed
    return modality_arrays


@dataclass
class SleepFMModelBundle:
    torch: object
    model: object
    device: object
    channel_groups: Dict[str, List[str]]
    sampling_freq: int
    sampling_duration_min: int


def load_sleepfm_bundle(sleepfm_root: Path, device: str, seed: int) -> SleepFMModelBundle:
    torch, torch_import_error = maybe_import_torch()
    if torch is None:
        raise InferenceError(f"torch import failed: {torch_import_error}")

    sleepfm_pkg_root = sleepfm_root / "sleepfm"
    model_config_path = sleepfm_pkg_root / "checkpoints" / "model_base" / "config.json"
    checkpoint_path = sleepfm_pkg_root / "checkpoints" / "model_base" / "best.pt"
    channel_groups_path = sleepfm_pkg_root / "configs" / "channel_groups.json"

    for required in (model_config_path, checkpoint_path, channel_groups_path):
        if not required.exists():
            raise InferenceError(f"Missing SleepFM artifact: {required}")

    if str(sleepfm_pkg_root) not in sys.path:
        sys.path.insert(0, str(sleepfm_pkg_root))
    try:
        from models.models import SetTransformer  # type: ignore
    except Exception as exc:
        raise InferenceError(f"Failed importing SleepFM model code: {exc}") from exc

    cfg = read_json(model_config_path)
    channel_groups = read_json(channel_groups_path)
    runtime_device = torch.device(device if device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if runtime_device.type == "cuda":
        torch.cuda.manual_seed_all(seed)

    model = SetTransformer(
        in_channels=cfg["in_channels"],
        patch_size=cfg["patch_size"],
        embed_dim=cfg["embed_dim"],
        num_heads=cfg["num_heads"],
        num_layers=cfg["num_layers"],
        pooling_head=cfg["pooling_head"],
        dropout=0.0,
    )
    model = model.to(runtime_device)
    checkpoint = torch.load(str(checkpoint_path), map_location=runtime_device)
    state = checkpoint["state_dict"] if isinstance(checkpoint, dict) and "state_dict" in checkpoint else checkpoint
    cleaned_state = {k.replace("module.", "", 1): v for k, v in state.items()}
    model.load_state_dict(cleaned_state, strict=False)
    model.eval()

    return SleepFMModelBundle(
        torch=torch,
        model=model,
        device=runtime_device,
        channel_groups=channel_groups,
        sampling_freq=int(cfg["sampling_freq"]),
        sampling_duration_min=int(cfg["sampling_duration"]),
    )


def extract_session_embeddings(edf_path: Path, bundle: SleepFMModelBundle) -> Dict[str, np.ndarray]:
    signals_by_label = read_edf_signals(edf_path)
    modality_arrays = pick_modality_arrays(
        signals_by_label=signals_by_label,
        channel_groups=bundle.channel_groups,
        target_rate=bundle.sampling_freq,
    )
    if not modality_arrays:
        raise PreprocessError("No overlapping channels found between EDF and SleepFM channel groups")

    chunk_len = bundle.sampling_duration_min * 60 * bundle.sampling_freq
    if chunk_len <= 0:
        raise InferenceError(f"Invalid chunk length derived from SleepFM config: {chunk_len}")

    torch = bundle.torch
    out: Dict[str, np.ndarray] = {}
    with torch.no_grad():
        for modality in MODALITY_ORDER:
            if modality not in modality_arrays:
                continue
            arr = modality_arrays[modality]
            n_chunks = arr.shape[1] // chunk_len
            if n_chunks <= 0:
                continue

            chunks = arr[:, : n_chunks * chunk_len].reshape(arr.shape[0], n_chunks, chunk_len)
            chunks = np.transpose(chunks, (1, 0, 2))  # [num_windows, channels, samples]
            x = torch.from_numpy(chunks).float().to(bundle.device)
            mask = torch.zeros((x.shape[0], x.shape[1]), dtype=torch.bool, device=bundle.device)
            pooled, _ = bundle.model(x, mask)  # [num_windows, embed_dim]
            out[modality] = pooled.detach().cpu().numpy().astype(np.float32, copy=False)

    if not out:
        raise InferenceError("No embeddings produced; channels exist but no valid windows after chunking")
    return out


def write_cache_artifacts(
    cache_path: Path,
    meta_path: Path,
    meta_payload: Dict,
    embeddings_by_modality: Dict[str, np.ndarray],
) -> None:
    h5py, h5py_import_error = maybe_import_h5py()
    if h5py is None:
        raise WriteError(f"h5py import failed: {h5py_import_error}")

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with h5py.File(str(cache_path), "w") as h5f:
            for modality in MODALITY_ORDER:
                if modality not in embeddings_by_modality:
                    continue
                data = embeddings_by_modality[modality].astype(np.float32, copy=False)
                if data.ndim != 2:
                    raise WriteError(f"Expected 2D embeddings for {modality}, got shape {data.shape}")
                h5f.create_dataset(modality, data=data, dtype="float32")
    except Exception as exc:
        raise WriteError(f"Failed writing HDF5 cache {cache_path}: {exc}") from exc

    try:
        write_json(meta_path, meta_payload)
    except Exception as exc:
        raise WriteError(f"Failed writing metadata sidecar {meta_path}: {exc}") from exc


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract offline SleepFM embeddings for PhysioNet challenge sessions.")
    parser.add_argument("--data-folder", type=Path, required=True, help="Folder containing physiological_data/ and demographics.")
    parser.add_argument("--output-folder", type=Path, default=Path("artifacts/sleepfm_cache"))
    parser.add_argument("--sleepfm-root", type=Path, default=Path("external/sleepfm-clinical"))
    parser.add_argument("--manifest", type=Path, default=None, help="Manifest CSV path; defaults to <output-folder>/manifest.csv.")
    parser.add_argument("--seed", type=int, default=420)
    parser.add_argument("--limit", type=int, default=None, help="Optional max number of demographics rows to process.")
    parser.add_argument("--overwrite", action="store_true", help="Recompute sessions that already have cache artifacts.")
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--adapter-version", type=str, default=ADAPTER_VERSION)
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    output_folder = args.output_folder
    manifest_path = args.manifest or (output_folder / "manifest.csv")
    output_folder.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    demographics_path = resolve_demographics_path(args.data_folder)
    physiological_root = resolve_physiological_root(args.data_folder)
    sleepfm_commit = get_sleepfm_commit(args.sleepfm_root)

    demographics = pd.read_csv(demographics_path)
    required_cols = {"SiteID", "BidsFolder", "SessionID"}
    missing_cols = required_cols - set(demographics.columns)
    if missing_cols:
        raise ValueError(f"demographics.csv missing required columns: {sorted(missing_cols)}")
    if args.limit is not None:
        demographics = demographics.head(args.limit)

    load_error: Optional[str] = None
    model_bundle: Optional[SleepFMModelBundle] = None
    try:
        model_bundle = load_sleepfm_bundle(args.sleepfm_root, device=args.device, seed=args.seed)
    except InferenceError as exc:
        load_error = str(exc)

    rows: List[Dict] = []
    seen_cache_keys = set()

    for _, rec in demographics.iterrows():
        site_id = str(rec["SiteID"]).strip()
        bids_folder = str(rec["BidsFolder"]).strip()
        session_id = normalize_session_id(rec["SessionID"])
        cache_key = f"{site_id}/{bids_folder}/ses-{session_id}"

        if cache_key in seen_cache_keys:
            continue
        seen_cache_keys.add(cache_key)

        session_dir = output_folder / site_id / bids_folder / f"ses-{session_id}"
        cache_path = session_dir / "embeddings.h5"
        meta_path = session_dir / "meta.json"
        edf_path = physiological_root / site_id / f"{bids_folder}_ses-{session_id}.edf"

        created_utc = utc_now_iso()
        row = {
            "site_id": site_id,
            "bids_folder": bids_folder,
            "session_id": session_id,
            "cache_key": cache_key,
            "cache_path": str(cache_path),
            "meta_path": str(meta_path),
            "sleepfm_commit": sleepfm_commit,
            "adapter_version": args.adapter_version,
            "status": "missing_input",
            "error_message": None,
            "num_windows": None,
            "embedding_dim": None,
            "created_utc": created_utc,
        }

        if not edf_path.is_file():
            row["status"] = "missing_input"
            row["error_message"] = f"Missing EDF: {edf_path}"
            rows.append(row)
            continue

        if load_error is not None:
            row["status"] = "inference_error"
            row["error_message"] = load_error
            rows.append(row)
            continue

        assert model_bundle is not None

        if cache_path.exists() and meta_path.exists() and not args.overwrite:
            try:
                prev_meta = read_json(meta_path)
                row["status"] = "ok"
                row["num_windows"] = int(prev_meta["num_windows"])
                row["embedding_dim"] = int(prev_meta["embedding_dim"])
                row["created_utc"] = str(prev_meta.get("created_utc", created_utc))
                rows.append(row)
                continue
            except Exception:
                pass

        try:
            embeddings = extract_session_embeddings(edf_path=edf_path, bundle=model_bundle)
        except PreprocessError as exc:
            row["status"] = "preprocess_error"
            row["error_message"] = str(exc)
            rows.append(row)
            continue
        except InferenceError as exc:
            row["status"] = "inference_error"
            row["error_message"] = str(exc)
            rows.append(row)
            continue
        except Exception as exc:
            row["status"] = "inference_error"
            row["error_message"] = f"Unexpected inference failure: {exc}"
            rows.append(row)
            continue

        n_windows = max(arr.shape[0] for arr in embeddings.values())
        emb_dim = next(iter(embeddings.values())).shape[1]
        meta_payload = {
            "site_id": site_id,
            "bids_folder": bids_folder,
            "session_id": session_id,
            "cache_key": cache_key,
            "sleepfm_commit": sleepfm_commit,
            "adapter_version": args.adapter_version,
            "created_utc": created_utc,
            "num_windows": int(n_windows),
            "embedding_dim": int(emb_dim),
        }

        try:
            write_cache_artifacts(
                cache_path=cache_path,
                meta_path=meta_path,
                meta_payload=meta_payload,
                embeddings_by_modality=embeddings,
            )
            row["status"] = "ok"
            row["num_windows"] = int(n_windows)
            row["embedding_dim"] = int(emb_dim)
            row["error_message"] = None
        except WriteError as exc:
            row["status"] = "write_error"
            row["error_message"] = str(exc)
        except Exception as exc:
            row["status"] = "write_error"
            row["error_message"] = f"Unexpected write failure: {exc}"
        rows.append(row)

    df = pd.DataFrame(rows, columns=MANIFEST_COLUMNS)
    if not set(df["status"].dropna().unique()).issubset(STATUS_VALUES):
        raise ValueError("Manifest contains invalid status values.")
    df.to_csv(manifest_path, index=False)

    counts = df["status"].value_counts(dropna=False).to_dict()
    print(f"demographics_path={demographics_path}")
    print(f"physiological_root={physiological_root}")
    print(f"manifest_path={manifest_path}")
    print(f"rows={len(df)} unique_cache_keys={df['cache_key'].nunique()}")
    print(f"status_counts={counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
