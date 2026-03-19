from __future__ import annotations

import csv
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from helper_code import HEADERS, load_age, load_demographics, load_label, load_sex

from .downstream import DemographicStats, SleepFMClassifier
from .sleepfm_pipeline import (
    PREPROCESS_VERSION,
    MissingSignalError,
    extract_sequence_embeddings,
    load_sequence_cache,
    load_sleepfm_bundle,
    save_sequence_cache,
    sequence_cache_path,
)


@dataclass
class BaselineConfig:
    variant: str = "B1"
    epochs: int = 3
    patience: int = 2
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    batch_size: int = 1
    seed: int = 420
    threshold: float = 0.5
    device: str = "cpu"
    cache_dirname: str = "sequence_cache"
    sleepfm_batch_windows: int = 128


def build_config() -> BaselineConfig:
    variant = os.getenv("PHYSIONET2026_BASELINE_VARIANT", "B1").upper()
    return BaselineConfig(
        variant=variant,
        epochs=int(os.getenv("PHYSIONET2026_EPOCHS", "3")),
        patience=int(os.getenv("PHYSIONET2026_PATIENCE", "2")),
        learning_rate=float(os.getenv("PHYSIONET2026_LR", "1e-3")),
        weight_decay=float(os.getenv("PHYSIONET2026_WEIGHT_DECAY", "1e-4")),
        batch_size=int(os.getenv("PHYSIONET2026_BATCH_SIZE", "1")),
        seed=int(os.getenv("PHYSIONET2026_SEED", "420")),
        threshold=float(os.getenv("PHYSIONET2026_THRESHOLD", "0.5")),
        device=os.getenv("PHYSIONET2026_DEVICE", "cpu"),
        sleepfm_batch_windows=int(os.getenv("PHYSIONET2026_SLEEPFM_BATCH_WINDOWS", "128")),
    )


def set_seed(seed: int) -> None:
    import torch

    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def encode_sex_value(value: str) -> float:
    value = str(value).strip().lower()
    if value.startswith("m"):
        return 1.0
    if value.startswith("f"):
        return 0.0
    return 0.5


def labeled_session_rows(data_folder: Path) -> list[dict[str, object]]:
    df = pd.read_csv(resolve_demographics_path(data_folder))
    rows = []
    for _, row in df.iterrows():
        label_value = row.get(HEADERS["label"])
        if pd.isna(label_value):
            continue
        rows.append(row.to_dict())
    return rows


def resolve_demographics_path(data_folder: Path) -> Path:
    candidates = [data_folder / "demographics.csv", data_folder.parent / "demographics.csv"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Could not find demographics.csv under {data_folder} or its parent.")


def resolve_physiological_root(data_folder: Path) -> Path:
    candidates = [data_folder / "physiological_data", data_folder / "training_set" / "physiological_data"]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Could not find physiological_data under {data_folder}.")


def build_edf_path(data_folder: Path, row: dict[str, object]) -> Path:
    site_id = str(row[HEADERS["site_id"]]).strip()
    bids_folder = str(row[HEADERS["bids_folder"]]).strip()
    session_id = str(row[HEADERS["session_id"]]).strip()
    if session_id.endswith(".0"):
        session_id = session_id[:-2]
    return resolve_physiological_root(data_folder) / site_id / f"{bids_folder}_ses-{session_id}.edf"


def normalize_session_id(value: object) -> str:
    text = str(value).strip()
    return text[:-2] if text.endswith(".0") else text


def ensure_sequence_cache(
    repo_root: Path,
    data_folder: Path,
    cache_root: Path,
    row: dict[str, object],
    bundle,
    config: BaselineConfig,
) -> tuple[Path, dict[str, object]]:
    site_id = str(row[HEADERS["site_id"]]).strip()
    bids_folder = str(row[HEADERS["bids_folder"]]).strip()
    session_id = normalize_session_id(row[HEADERS["session_id"]])
    cache_path = sequence_cache_path(cache_root, site_id, bids_folder, session_id)
    label = float(load_label(row))
    age = float(load_age(row))
    sex_code = encode_sex_value(load_sex(row))

    if not cache_path.is_file():
        embeddings, valid_mask, metadata = extract_sequence_embeddings(
            build_edf_path(data_folder, row),
            repo_root=repo_root,
            bundle=bundle,
            batch_windows=config.sleepfm_batch_windows,
        )
        metadata.update(
            {
                "site_id": site_id,
                "bids_folder": bids_folder,
                "session_id": session_id,
            }
        )
        save_sequence_cache(
            cache_path,
            embeddings=embeddings,
            valid_mask=valid_mask,
            age=age,
            sex_code=sex_code,
            label=label,
            patient_id=bids_folder,
            metadata=metadata,
        )

    record = {
        "cache_path": str(cache_path),
        "site_id": site_id,
        "bids_folder": bids_folder,
        "session_id": session_id,
        "age": age,
        "sex_code": sex_code,
        "label": label,
    }
    return cache_path, record


def write_cache_manifest(cache_root: Path, records: list[dict[str, object]]) -> None:
    manifest_path = cache_root / "manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["site_id", "bids_folder", "session_id", "cache_path", "age", "sex_code", "label"]
    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record[key] for key in fieldnames})


class SequenceDataset:
    def __init__(self, records: list[dict[str, object]]):
        self.records = records

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, object]:
        record = self.records[index]
        cached = load_sequence_cache(Path(record["cache_path"]))
        return {
            "embeddings": cached["embeddings"],
            "mask": cached["valid_mask"],
            "age": float(record["age"]),
            "sex_code": float(record["sex_code"]),
            "label": float(record["label"]),
        }


def collate_batch(batch: list[dict[str, object]]) -> dict[str, object]:
    import torch

    return {
        "embeddings": torch.tensor(np.stack([item["embeddings"] for item in batch]), dtype=torch.float32),
        "mask": torch.tensor(np.stack([item["mask"] for item in batch]), dtype=torch.bool),
        "age": torch.tensor([item["age"] for item in batch], dtype=torch.float32),
        "sex_code": torch.tensor([item["sex_code"] for item in batch], dtype=torch.float32),
        "label": torch.tensor([item["label"] for item in batch], dtype=torch.float32),
    }


def split_records(records: list[dict[str, object]], seed: int) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    if len(records) < 4:
        return records, []
    rng = np.random.default_rng(seed)
    labels = np.array([record["label"] for record in records], dtype=np.int64)
    indices = np.arange(len(records))
    train_indices = []
    val_indices = []
    for label in sorted(set(labels.tolist())):
        label_indices = indices[labels == label]
        rng.shuffle(label_indices)
        cutoff = max(1, int(round(0.85 * len(label_indices))))
        if cutoff >= len(label_indices):
            cutoff = len(label_indices) - 1
        if cutoff <= 0:
            train_indices.extend(label_indices.tolist())
            continue
        train_indices.extend(label_indices[:cutoff].tolist())
        val_indices.extend(label_indices[cutoff:].tolist())
    if not val_indices:
        return records, []
    return [records[i] for i in train_indices], [records[i] for i in val_indices]


def demographic_stats(records: list[dict[str, object]]) -> DemographicStats:
    ages = np.array([record["age"] for record in records], dtype=np.float32)
    return DemographicStats(age_mean=float(np.mean(ages)), age_std=float(np.std(ages)))


def evaluate_model(model, loader, demo_stats: DemographicStats | None, device) -> float:
    import torch

    model.eval()
    losses = []
    criterion = torch.nn.BCEWithLogitsLoss()
    with torch.no_grad():
        for batch in loader:
            embeddings = batch["embeddings"].to(device)
            mask = batch["mask"].to(device)
            labels = batch["label"].to(device)
            demographics = None
            if demo_stats is not None:
                demographics = demo_stats.encode(batch["age"].to(device), batch["sex_code"].to(device))
            logits = model(embeddings, mask, demographics)
            losses.append(float(criterion(logits, labels).item()))
    return float(np.mean(losses)) if losses else 0.0


def train_downstream_model(records: list[dict[str, object]], config: BaselineConfig):
    import torch
    from torch.utils.data import DataLoader

    set_seed(config.seed)
    device = torch.device(config.device if config.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    train_records, val_records = split_records(records, config.seed)
    train_loader = DataLoader(
        SequenceDataset(train_records),
        batch_size=config.batch_size,
        shuffle=True,
        collate_fn=collate_batch,
    )
    val_loader = DataLoader(
        SequenceDataset(val_records),
        batch_size=config.batch_size,
        shuffle=False,
        collate_fn=collate_batch,
    ) if val_records else None

    demo_stats = demographic_stats(train_records) if config.variant == "B2" else None
    model = SleepFMClassifier(variant=config.variant).to(device)
    labels = np.array([record["label"] for record in train_records], dtype=np.float32)
    pos = float(labels.sum())
    neg = float(len(labels) - pos)
    pos_weight = torch.tensor([neg / max(pos, 1.0)], dtype=torch.float32, device=device)
    criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)

    best_state = None
    best_loss = float("inf")
    patience_left = config.patience
    for _ in range(config.epochs):
        model.train()
        for batch in train_loader:
            embeddings = batch["embeddings"].to(device)
            mask = batch["mask"].to(device)
            labels = batch["label"].to(device)
            demographics = None
            if demo_stats is not None:
                demographics = demo_stats.encode(batch["age"].to(device), batch["sex_code"].to(device))
            logits = model(embeddings, mask, demographics)
            loss = criterion(logits, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        current_loss = evaluate_model(model, val_loader, demo_stats, device) if val_loader is not None else 0.0
        if current_loss <= best_loss:
            best_loss = current_loss
            best_state = {key: value.detach().cpu() for key, value in model.state_dict().items()}
            patience_left = config.patience
        else:
            patience_left -= 1
            if patience_left <= 0:
                break

    if best_state is None:
        best_state = {key: value.detach().cpu() for key, value in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.to("cpu")
    return model, demo_stats


def save_training_artifacts(model_folder: Path, model, demo_stats: DemographicStats | None, config: BaselineConfig) -> None:
    import torch

    model_folder.mkdir(parents=True, exist_ok=True)
    artifact = {
        "variant": config.variant,
        "threshold": config.threshold,
        "preprocess_version": PREPROCESS_VERSION,
        "state_dict": model.state_dict(),
        "demographic_stats": asdict(demo_stats) if demo_stats is not None else None,
        "config": asdict(config),
    }
    torch.save(artifact, model_folder / "model.pt")


def train_challenge_model(data_folder: str, model_folder: str, verbose: bool) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    data_root = Path(data_folder)
    model_root = Path(model_folder)
    config = build_config()
    cache_root = model_root / config.cache_dirname
    bundle = load_sleepfm_bundle(repo_root, device_name=config.device)

    records = []
    skipped = 0
    for row in labeled_session_rows(data_root):
        try:
            _, record = ensure_sequence_cache(repo_root, data_root, cache_root, row, bundle, config)
            records.append(record)
        except (FileNotFoundError, MissingSignalError) as exc:
            skipped += 1
            if verbose:
                print(f"Skipping {row.get(HEADERS['bids_folder'])}: {exc}")

    if not records:
        raise RuntimeError("No training sessions with usable SleepFM-compatible channels were found.")

    write_cache_manifest(cache_root, records)
    model, demo_stats = train_downstream_model(records, config)
    save_training_artifacts(model_root, model, demo_stats, config)
    if verbose:
        print(f"trained_records={len(records)} skipped_records={skipped} variant={config.variant}")


def load_challenge_model(model_folder: str, verbose: bool):
    import torch

    repo_root = Path(__file__).resolve().parents[2]
    artifact = torch.load(Path(model_folder) / "model.pt", map_location="cpu")
    config = BaselineConfig(**artifact["config"])
    model = SleepFMClassifier(variant=artifact["variant"])
    model.load_state_dict(artifact["state_dict"])
    model.eval()
    stats = artifact.get("demographic_stats")
    demo_stats = DemographicStats(**stats) if stats else None
    bundle = load_sleepfm_bundle(repo_root, device_name=config.device)
    if verbose:
        print(f"Loaded SleepFM baseline variant={artifact['variant']}")
    return {
        "repo_root": repo_root,
        "threshold": float(artifact["threshold"]),
        "variant": artifact["variant"],
        "model": model,
        "demo_stats": demo_stats,
        "sleepfm_bundle": bundle,
        "config": config,
    }


def predict_record(loaded_model, record: dict[str, object], data_folder: str, verbose: bool) -> tuple[int, float]:
    import torch

    data_root = Path(data_folder)
    site_id = str(record[HEADERS["site_id"]]).strip()
    bids_folder = str(record[HEADERS["bids_folder"]]).strip()
    session_id = normalize_session_id(record[HEADERS["session_id"]])
    edf_path = data_root / "physiological_data" / site_id / f"{bids_folder}_ses-{session_id}.edf"
    if not edf_path.is_file():
        raise FileNotFoundError(f"Missing EDF for inference: {edf_path}")

    embeddings, valid_mask, _ = extract_sequence_embeddings(
        edf_path,
        repo_root=loaded_model["repo_root"],
        bundle=loaded_model["sleepfm_bundle"],
        batch_windows=loaded_model["config"].sleepfm_batch_windows,
    )

    patient_data = load_demographics(resolve_demographics_path(data_root), bids_folder, record[HEADERS["session_id"]])
    age = torch.tensor([float(load_age(patient_data))], dtype=torch.float32)
    sex_code = torch.tensor([encode_sex_value(load_sex(patient_data))], dtype=torch.float32)
    x = torch.tensor(embeddings[None, ...], dtype=torch.float32)
    mask = torch.tensor(valid_mask[None, ...], dtype=torch.bool)
    demographics = None
    if loaded_model["demo_stats"] is not None:
        demographics = loaded_model["demo_stats"].encode(age, sex_code)

    with torch.no_grad():
        logit = loaded_model["model"](x, mask, demographics)
        probability = float(torch.sigmoid(logit).item())
    label = int(probability >= loaded_model["threshold"])
    if verbose:
        print(f"Predicted {bids_folder} ses-{session_id}: p={probability:.4f}")
    return label, probability
