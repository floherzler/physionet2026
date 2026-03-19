# Q-0008: SleepFM LSTM Baseline Under Submission-Safe Challenge Constraints

## Quest Metadata

- Quest ID: `Q-0008`
- Status:
  - [ ] Draft
  - [x] In Progress
  - [ ] In Review
  - [ ] Completed
- Created date (YYYY-MM-DD): `2026-03-19`
- Completed date (YYYY-MM-DD): `<date>`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `<timestamp>`
- Owner (GitHub): `@floherzler`

## Objective

Implement the first real SleepFM-based challenge baseline while preserving the official root entrypoint contracts and keeping the submitted repository self-contained for training and inference.

## Scope

- Add a submission-safe SleepFM runtime path behind `team_code.py`.
- Build a canonical sequence representation `[6480, 128]` with a matching `[6480]` valid mask from raw EDF input.
- Implement configurable downstream baselines `B0`, `B1`, and `B2`.
- Cache training-time sequence features for repeatable experiments without making inference depend on external precomputed holdout caches.
- Keep completed Q-0004 unchanged and mark draft Q-0005 as superseded.

## Acceptance Criteria

- [x] Root entrypoints remain present and keep their required signatures.
- [x] New package code exists for channel mapping, SleepFM extraction, pooled-sequence construction, downstream modeling, and serialization.
- [x] `team_code.train_model(...)` trains from SleepFM sequence features and saves a self-describing model artifact.
- [x] `team_code.run_model(...)` can derive features from raw PSG through repo-contained code and emit binary label plus probability.
- [x] Training cache artifacts use a canonical sequence representation with embeddings and valid mask.
- [x] Baseline variants `B0`, `B1`, and `B2` are selectable through configuration.
- [ ] End-to-end local validation is recorded for train, run, and evaluate flows.

## Implementation Tasks

- [x] Add `src/physionet2026/` package scaffolding.
- [x] Vendor the minimal SleepFM runtime architecture into package code and use a repo-local checkpoint path.
- [x] Implement deterministic channel mapping using `channel_table.csv`.
- [x] Implement 128 Hz resampling, 5 s tokenization, 9 h crop/pad, modality pooling, and sequence cache writing.
- [x] Implement downstream baseline heads and training loop.
- [x] Replace the previous random-forest `team_code.py` wiring with the SleepFM baseline pipeline.
- [x] Add quest documentation for the new baseline.
- [ ] Run and record concrete validation commands.

## Validation

Planned commands:

```bash
.venv-sleepfm/bin/python train_model.py -d data/challenge2026_training10/training_set -m model_q0008 -v
.venv-sleepfm/bin/python run_model.py -d data/challenge2026_training10/training_set -m model_q0008 -o outputs_q0008 -v
.venv-sleepfm/bin/python evaluate_model.py -d data/challenge2026_training10/training_set/demographics.csv -o outputs_q0008/demographics.csv -s outputs_q0008/scores.txt
```

Current evidence:

- Syntax and import smoke checks passed:
  - `.venv-sleepfm/bin/python -m py_compile team_code.py src/physionet2026/*.py`
  - `.venv-sleepfm/bin/python - <<'PY' import team_code; print('team_code import ok') PY`
- End-to-end train smoke test passed on a one-session local subset:
  - `PHYSIONET2026_BASELINE_VARIANT=B0 PHYSIONET2026_EPOCHS=1 PHYSIONET2026_PATIENCE=1 PHYSIONET2026_BATCH_SIZE=1 PHYSIONET2026_DEVICE=cpu .venv-sleepfm/bin/python train_model.py -d /tmp/physionet2026_q0008_smoke -m /tmp/physionet2026_q0008_model -v`
  - observed output included: `trained_records=1 skipped_records=0 variant=B0`
- End-to-end inference smoke test passed on the same subset:
  - `.venv-sleepfm/bin/python run_model.py -d /tmp/physionet2026_q0008_smoke -m /tmp/physionet2026_q0008_model -o /tmp/physionet2026_q0008_outputs -v`
  - observed output included:
    - `Loaded SleepFM baseline variant=B0`
    - `Predicted sub-I0002150001401 ses-2: p=0.6216`
    - `Results saved to: /tmp/physionet2026_q0008_outputs/demographics.csv`
- Evaluation script was invoked but local metric evidence is still incomplete because the checked-in one-session smoke subset had only one label class:
  - `.venv-sleepfm/bin/python evaluate_model.py -d /tmp/physionet2026_q0008_smoke/demographics.csv -o /tmp/physionet2026_q0008_outputs/demographics.csv -s /tmp/physionet2026_q0008_outputs/scores.txt`
  - failure: `ValueError: Only one class present in y_true. ROC AUC score is not defined in that case.`

## Risks / Open Questions

- Full-night bidirectional LSTM over 6480 tokens may be slow on CPU-only environments.
- Submission safety depends on keeping the required SleepFM checkpoint inside the parent repository rather than only in a Git submodule.
- Multi-session output overwrites remain limited by the unchanged upstream `run_model.py` result-aggregation behavior.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0004-sleepfm-embedding-adapter-and-metric-eval.md`
  - `docs/quests/Q-0005-embedding-consumer-and-challenge-wrapper-integration.md`
  - `docs/quests/Q-0006-challenge-metric-evaluation-and-threshold-policy.md`
