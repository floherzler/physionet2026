# Q-0006: Challenge-Metric Evaluation and Threshold Policy

## Quest Metadata

- Quest ID: `Q-0006`
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

Define and validate a challenge-aligned local evaluation protocol that prioritizes `evaluate_model.py` compatibility and uses a fixed seed-420 split policy.

## Scope

- Document exact invocation and file expectations for `evaluate_model.py`.
- Define reproducible train/validation/test split policy with fixed random seed `420`.
- Define threshold-selection policy for `Cognitive_Impairment` from `Cognitive_Impairment_Probability`.
- Document relationship and gap between local metrics and challenge-score utility.

## Acceptance Criteria

- [ ] Validation commands pass with explicit CSV file paths (not folder placeholders) for `evaluate_model.py`.
- [ ] Protocol defines split strategy and uses fixed seed `420`.
- [ ] Binary threshold is selected on validation split only and then frozen for test reporting.
- [ ] Reporting template includes AUROC, AUPRC, Accuracy, and F-measure from `evaluate_model.py`.
- [ ] Quest notes include optional cross-check with `helper_code.compute_challenge_score` and residual gap to official challenge scoring.

## Implementation Tasks

- [ ] Add a short protocol document block in this quest with split, seed, and threshold rules.
- [ ] Add concrete command examples for train, run, and evaluate with explicit paths.
- [ ] Record one evidence run on local sample data with generated `scores.txt`.
- [ ] Document failure modes (label leakage, split leakage, missing predictions).

## Validation

Planned commands:

```bash
# 1) Train
python train_model.py -d data/challenge2026_training10/training_set -m model -v

# 2) Run inference
python run_model.py \
  -d data/challenge2026_training10/training_set \
  -m model \
  -o outputs/challenge2026_training10 \
  -v

# 3) Evaluate (explicit CSV paths required by evaluate_model.py)
python evaluate_model.py \
  -d data/challenge2026_training10/training_set/demographics.csv \
  -o outputs/challenge2026_training10/demographics.csv \
  -s outputs/challenge2026_training10/scores.txt
```

Expected evidence:

- `scores.txt` contains AUROC, AUPRC, Accuracy, and F-measure.
- Evaluation protocol records seed `420`, split definition, and threshold-selection rule.

## Protocol (Draft)

- Split policy: use a fixed random seed of `420`.
- Split policy: build patient/session-level splits once and persist split IDs to a file for reuse.
- Split policy: recommended local ratio is `70% train`, `15% validation`, `15% test` using session-safe keys.
- Threshold policy: fit on train only.
- Threshold policy: select threshold on validation only (maximize F-measure or a challenge-prioritized objective).
- Threshold policy: freeze threshold and report test metrics without re-tuning.

## Risks / Open Questions

- Small local sample sizes can make AUROC/AUPRC unstable.
- If prediction CSV misses rows, current evaluation behavior defaults to zeros for missing outputs, which can hide pipeline failures.
- Official challenge scoring pipeline may differ; this quest only establishes local guardrails.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0004-sleepfm-embedding-adapter-and-metric-eval.md`
  - `docs/quests/Q-0005-embedding-consumer-and-challenge-wrapper-integration.md`
