# Q-0005: Embedding Consumer and Challenge Wrapper Integration

## Quest Metadata

- Quest ID: `Q-0005`
- Status:
  - [x] Draft
  - [ ] In Progress
  - [ ] In Review
  - [ ] Completed
- Created date (YYYY-MM-DD): `2026-03-05`
- Completed date (YYYY-MM-DD): `<date>`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `<timestamp>`
- Owner (GitHub): `@floherzler`

## Objective

Integrate precomputed SleepFM embeddings into challenge-compatible `train_model.py` and `run_model.py` flows via `team_code.py`, without invoking SleepFM during runtime.

## Scope

- Consume embedding cache artifacts produced by Q-0004.
- Add a baseline classifier that uses embeddings (optionally concatenated with demographics features).
- Keep challenge root contracts intact (`train_model.py`, `run_model.py`, `team_code.py` required signatures).
- Implement a safe missing-embedding policy for train and inference.

## Acceptance Criteria

- [ ] `train_model.py` trains successfully using precomputed embeddings and saves model artifacts.
- [ ] `run_model.py` writes challenge-format `demographics.csv` with `Cognitive_Impairment` and `Cognitive_Impairment_Probability`.
- [ ] Runtime path does not call SleepFM directly; it only reads cache files.
- [ ] Missing embeddings in training are handled deterministically: affected record is skipped and counted in an explicit warning summary.
- [ ] Missing embeddings in inference are handled deterministically: `team_code.run_model(...)` raises a clear missing-cache exception so `run_model.py --allow_failures` can decide fallback behavior.
- [ ] Multi-session outputs are session-safe (no silent overwrite between sessions).

## Implementation Tasks

- [ ] Add cache reader utilities keyed by (`SiteID`, `BidsFolder`, `SessionID`).
- [ ] Add a small cache-fixture test path so this quest can progress in parallel with Q-0004 extraction work.
- [ ] Wire embedding feature construction into `team_code.train_model(...)`.
- [ ] Wire embedding inference path into `team_code.run_model(...)`.
- [ ] Update output-writing logic to prevent multi-session overwrite.
- [ ] Add logging/reporting counters for missing embeddings during train and run.
- [ ] Validate end-to-end on local sample data.

## Validation

Planned commands:

```bash
# 1) Train from cached embeddings
python train_model.py -d data/challenge2026_training10/training_set -m model -v

# 2) Run inference
python run_model.py \
  -d data/challenge2026_training10/training_set \
  -m model \
  -o outputs/challenge2026_training10 \
  -v
```

Expected evidence:

- Model artifacts exist in `model/`.
- Output CSV exists at `outputs/challenge2026_training10/demographics.csv`.
- Output CSV contains both required prediction columns.
- Logs include a deterministic count of missing-embedding records (if any).

## Risks / Open Questions

- If many embeddings are missing, training sample size may collapse and destabilize metrics.
- Session-safe output updates may require helper-path changes while preserving challenge interfaces.
- Baseline model choice should remain simple to keep this quest reviewable.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0004-sleepfm-embedding-adapter-and-metric-eval.md`
  - `docs/quests/Q-0006-challenge-metric-evaluation-and-threshold-policy.md`
