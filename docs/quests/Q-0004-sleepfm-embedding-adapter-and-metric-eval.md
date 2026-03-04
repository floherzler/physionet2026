# Q-0004: SleepFM Offline Embedding Cache Contract and Extraction Adapter

## Quest Metadata

- Quest ID: `Q-0004`
- Status:
  - [ ] Draft
  - [ ] In Progress
  - [ ] In Review
  - [x] Completed
- Created date (YYYY-MM-DD): `2026-03-04`
- Completed date (YYYY-MM-DD): `2026-03-04`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `2026-03-04T23:57:42Z`
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

- [x] Cache key format is fixed and documented as session-safe: `<SiteID>/<BidsFolder>/ses-<SessionID>`.
- [x] Cache artifact format is fixed and documented as HDF5 (`embeddings.h5`) + JSON sidecar (`meta.json`) + manifest row.
- [x] A scriptable adapter extracts embeddings for sampled EDF files and writes deterministic cache artifacts.
- [x] `scripts/extract_sleepfm_embeddings.py` is implemented and callable from repository root.
- [x] A manifest file is produced that matches the locked schema in this quest.
- [x] Documentation explicitly states offline-only mode: SleepFM runs only in precompute step, never inside challenge runtime entrypoints (`train_model.py`, `run_model.py`, `team_code.py` runtime path).

## Implementation Tasks

- [x] Define canonical cache contract in this quest doc (ID mapping, on-disk layout, file suffixes, manifest schema).
- [x] Implement `scripts/extract_sleepfm_embeddings.py` for sampled EDF extraction.
- [x] Persist extraction metadata, including SleepFM commit pin and adapter version.
- [x] Add failure status handling in manifest for records that cannot be embedded.
- [x] Run extraction validation and record concrete command evidence.

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

Observed evidence (2026-03-05):

- Extraction command run:
  - `python scripts/extract_sleepfm_embeddings.py --data-folder data/challenge2026_training10/training_set --output-folder artifacts/sleepfm_cache --sleepfm-root external/sleepfm-clinical --manifest artifacts/sleepfm_cache/manifest.csv --seed 420`
- Script output:
  - `rows=622 unique_cache_keys=622`
  - `status_counts={'missing_input': 612, 'inference_error': 10}`
- Manifest validation run:
  - `python -c "import pandas as pd; df=pd.read_csv('artifacts/sleepfm_cache/manifest.csv'); print(df[['cache_key','status']].head()); print('rows=', len(df)); print('unique_keys=', df['cache_key'].nunique())"`
- Manifest schema columns match locked contract:
  - `site_id,bids_folder,session_id,cache_key,cache_path,meta_path,sleepfm_commit,adapter_version,status,error_message,num_windows,embedding_dim,created_utc`
- Failure status handling verified:
  - `missing_input` rows present for demographics entries without downloaded EDF files.
  - `inference_error` rows present for local EDFs due missing local `torch` dependency in current environment.
- Post-install extraction validation on downloaded 10-file sample:
  - `.venv-sleepfm/bin/python scripts/extract_sleepfm_embeddings.py --data-folder data/challenge2026_training10/training_set --output-folder artifacts/sleepfm_cache --sleepfm-root external/sleepfm-clinical --manifest artifacts/sleepfm_cache/manifest.csv --seed 420 --limit 10`
  - `rows=10 unique_cache_keys=10`
  - `status_counts={'ok': 10}`
  - Per-session artifacts confirmed for `ok` rows: `embeddings.h5` + `meta.json`.

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

- Quest implementation is complete.
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
