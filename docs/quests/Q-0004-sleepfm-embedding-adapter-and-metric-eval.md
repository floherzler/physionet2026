# Q-0004: SleepFM Offline Embedding Cache Contract and Extraction Adapter

## Quest Metadata

- Quest ID: `Q-0004`
- Status:
  - [ ] Draft
  - [x] In Progress
  - [ ] In Review
  - [ ] Completed
- Created date (YYYY-MM-DD): `2026-03-04`
- Completed date (YYYY-MM-DD): `<date>`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `<timestamp>`
- Owner (GitHub): `@floherzler`

## Objective

Define and implement a reproducible offline embedding pipeline that converts PhysioNet 2026 EDF inputs into a versioned, session-safe SleepFM embedding cache for downstream challenge wrappers.

## Scope

- Define and document the canonical embedding cache contract (key schema, file format, metadata manifest).
- Implement an offline extraction adapter from challenge EDF layout to SleepFM-compatible input and cache outputs.
- Persist cache artifacts with stable IDs derived from (`SiteID`, `BidsFolder`, `SessionID`).
- Keep challenge root contracts intact and prevent direct SleepFM runtime calls from challenge entrypoints.

## Cache Contract (Locked)

- Extraction entrypoint script path: `scripts/extract_sleepfm_embeddings.py`
- Cache root: `artifacts/sleepfm_cache/`
- Session-safe cache key format: `<SiteID>/<BidsFolder>/ses-<SessionID>`
- Per-session artifact path: `artifacts/sleepfm_cache/<SiteID>/<BidsFolder>/ses-<SessionID>/embeddings.h5`
- Per-session metadata sidecar: `artifacts/sleepfm_cache/<SiteID>/<BidsFolder>/ses-<SessionID>/meta.json`
- Manifest path: `artifacts/sleepfm_cache/manifest.csv`
- HDF5 dataset names (if present): `BAS`, `RESP`, `EKG`, `EMG`
- HDF5 dataset dtype: `float32`
- HDF5 dataset shape convention: `[num_windows, embedding_dim]` (2D)
- Adapter behavior for missing modalities: missing modality dataset is omitted; manifest still records session status.
- `meta.json` minimum fields:
  - `site_id` (string)
  - `bids_folder` (string)
  - `session_id` (string)
  - `cache_key` (string)
  - `sleepfm_commit` (string)
  - `adapter_version` (string)
  - `created_utc` (ISO-8601 UTC timestamp)
  - `num_windows` (integer)
  - `embedding_dim` (integer)

Manifest schema (locked):

- `site_id` (string, required)
- `bids_folder` (string, required)
- `session_id` (string, required)
- `cache_key` (string, required, unique)
- `cache_path` (string, required)
- `meta_path` (string, required)
- `sleepfm_commit` (string, required)
- `adapter_version` (string, required)
- `status` (string enum: `ok`, `missing_input`, `preprocess_error`, `inference_error`, `write_error`)
- `error_message` (string, nullable)
- `num_windows` (integer, nullable when status != `ok`)
- `embedding_dim` (integer, nullable when status != `ok`)
- `created_utc` (ISO-8601 UTC timestamp, required)

## Acceptance Criteria

- [ ] Cache key format is fixed and documented as session-safe: `<SiteID>/<BidsFolder>/ses-<SessionID>`.
- [ ] Cache artifact format is fixed and documented as HDF5 (`embeddings.h5`) + JSON sidecar (`meta.json`) + manifest row.
- [ ] A scriptable adapter extracts embeddings for sampled EDF files and writes deterministic cache artifacts.
- [ ] `scripts/extract_sleepfm_embeddings.py` is implemented and callable from repository root.
- [ ] A manifest file is produced that matches the locked schema in this quest.
- [ ] Documentation explicitly states offline-only mode: SleepFM runs only in precompute step, never inside challenge runtime entrypoints (`train_model.py`, `run_model.py`, `team_code.py` runtime path).

## Implementation Tasks

- [ ] Define canonical cache contract in this quest doc (ID mapping, on-disk layout, file suffixes, manifest schema).
- [ ] Implement `scripts/extract_sleepfm_embeddings.py` for sampled EDF extraction.
- [ ] Persist extraction metadata, including SleepFM commit pin and adapter version.
- [ ] Add failure status handling in manifest for records that cannot be embedded.
- [ ] Run extraction validation and record concrete command evidence.

## Validation

Planned commands:

```bash
# 1) Extract embeddings from local sample
python scripts/extract_sleepfm_embeddings.py \
  --data-folder data/challenge2026_training10/training_set \
  --output-folder artifacts/sleepfm_cache \
  --sleepfm-root external/sleepfm-clinical \
  --manifest artifacts/sleepfm_cache/manifest.csv \
  --seed 420

# 2) Validate manifest coverage
python -c "import pandas as pd; df=pd.read_csv('artifacts/sleepfm_cache/manifest.csv'); print(df[['cache_key','status']].head()); print('rows=', len(df)); print('unique_keys=', df['cache_key'].nunique())"
```

Expected evidence:

- Embedding cache files created under the session-safe directory layout.
- Manifest present with locked schema columns and non-empty rows.
- Failed extraction records are present in manifest with explicit status and reason.
- At least one successful (`status=ok`) record has both `embeddings.h5` and `meta.json` on disk.

## Risks / Open Questions

- SleepFM preprocessing assumptions may not fully match challenge EDF channel availability without adapter logic.
- Embedding extraction cost may be substantial even for medium subsets; batching and resumability are required.
- Cache contract drift could block downstream integration unless treated as a fixed interface.

## Implementation Readiness

- This quest is now fully specified for implementation and marked `In Progress`.
- Any scope beyond cache extraction/contract (model consumption or evaluation protocol) belongs to Q-0005 and Q-0006.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0001-integrate-sleepfm-submodule.md`
  - `docs/quests/Q-0003-kaggle-data-access-and-sampling.md`
  - `docs/quests/Q-0005-embedding-consumer-and-challenge-wrapper-integration.md`
  - `docs/quests/Q-0006-challenge-metric-evaluation-and-threshold-policy.md`
  - `docs/quests/side-quests/Q-0103-time-aware-multimodal-module.md`
