# Project Operating Plan (Fork + Quest Docs Workflow)

This repo now uses a **fork-first** GitHub setup and a local **document-driven development** flow.

- Use **quests** as the actionable feature work units.
- Keep docs Markdown-first (`.md`) except explicit assets/resources.

## Confirmed GitHub Setup

- `origin` points to your fork: `git@github.com:floherzler/physionet2026.git`
- `main` tracks `origin/main`

Optional:
- Add `upstream` to `physionetchallenges/python-example-2026` for syncs.

## Docs Structure

```text
docs/
├── project-operating-plan.md
├── requirements-overview.md
├── templates/
│   └── quest-template.md
├── best-practices/
│   ├── ai-agent-task-workflow.md
│   └── quest-creation-best-practices.md
├── quests/
│   ├── README.md
│   ├── Q-0001-baseline-training.md
│   └── Q-0002-data-ingestion.md
└── assets/                         # optional non-markdown files
```

## Quest Model

- **Quest**: one implementation slice scoped to one small PR or a tightly related PR batch.

Recommended naming:
- Quest id: `Q-0001`, `Q-0002`, ...
- Quest slug: kebab-case, e.g. `baseline-training`.
- Recommended quest filename: `Q-0001-baseline-training.md`

## Basic Workflow Steps

1. Define scope and constraints in [requirements-overview.md](./requirements-overview.md).
2. Create one or more quests using [quest-template.md](./templates/quest-template.md).
3. Before coding, ensure each quest links to:
   - [AI Agent Task Workflow](./best-practices/ai-agent-task-workflow.md)
   - [Quest Creation Best Practices](./best-practices/quest-creation-best-practices.md)
   - [Requirements Overview](./requirements-overview.md)
4. Implement via short-lived branches and small PRs.
5. Record validation evidence in the quest doc before merge.
6. Set completion fields (date and timestamp) when done.

## Challenge-Safe Architecture

- Keep these files as challenge-facing wrappers:
  - `train_model.py`
  - `run_model.py`
  - `evaluate_model.py`
  - `helper_code.py`
- Keep required function signatures in `team_code.py` unchanged.
- Implement most logic in `src/physionet2026/` and call it from `team_code.py`.

## `uv` + Submission Compromise

Use dual dependency surfaces:

- Local development source of truth:
  - `pyproject.toml`
  - `uv.lock`
- Submission/runtime source of truth:
  - `requirements.txt` (installed by Docker build)

Rules:

1. Add or update dependencies in `pyproject.toml`.
2. Lock locally with `uv`.
3. Export/refresh `requirements.txt` from the locked environment before submission.
4. Ensure Docker install succeeds with only `requirements.txt`.

Suggested command sequence:

```bash
uv sync
uv lock
uv export --format requirements-txt --no-hashes --output-file requirements.txt
python train_model.py -d <data> -m <model> -v
python run_model.py -d <data> -m <model> -o <outputs> -v
```

This gives fast local iteration with `uv` while preserving challenge compatibility.

## Lightning-First With Challenge Compatibility

- Use PyTorch Lightning + Lightning CLI for training orchestration.
- Keep challenge entrypoints minimal:
  - `team_code.train_model(...)` calls package training adapter.
  - `team_code.load_model(...)` loads serialized inference bundle.
  - `team_code.run_model(...)` performs record-level inference.
- Avoid invoking Lightning CLI directly from challenge wrappers in a way that breaks required arguments.
- Keep a CPU-safe default training path for challenge runtime constraints.

## Team Collaboration Rules (3 people)

- Each quest has one primary implementer and at least one reviewer.
- PR title should contain the quest id, e.g. `Q-0003: add baseline datamodule`.
- If scope changes, update docs first, then code.

## Agent Guardrails

- Do not start implementation before quest acceptance criteria exist.
- Do not break official challenge entrypoint contracts at repo root.
- Keep decisions explicit and linkable for future human and AI contributors.
