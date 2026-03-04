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

## Policy Source of Truth

For mandatory constraints and technical policy, use [requirements-overview.md](./requirements-overview.md) as the canonical source. This includes:

- Challenge-safe wrapper boundaries.
- `uv` local workflow + `requirements.txt` runtime policy.
- Lightning-first training policy.

Quick operational reminder:
- Implement in package code and keep challenge entrypoints stable.
- Sync dependency surfaces before submission-related changes.

## Team Collaboration Rules (3 people)

- Each quest has one primary implementer and at least one reviewer.
- PR title should contain the quest id, e.g. `Q-0003: add baseline datamodule`.
- If scope changes, update docs first, then code.

## Agent Guardrails

- Do not start implementation before quest acceptance criteria exist.
- Do not break official challenge entrypoint contracts at repo root.
- Keep decisions explicit and linkable for future human and AI contributors.
