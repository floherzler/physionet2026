# Requirements Overview

This file is the top-level contract for project scope, constraints, and done criteria.

## Project Goal

Build a strong, reproducible PhysioNet 2026 challenge entry while preserving official submission compatibility.

## Hard Constraints

- Keep root challenge contract intact (`team_code.py` interface and official scripts behavior).
- Submission must run in official-style Docker flow.
- Work in Python with reproducible local environment.
- Keep documentation Markdown-first in `docs/`.
- Keep `requirements.txt` valid for Docker install in submission.
- Allow `uv` as local package manager without making challenge runtime depend on `uv`.

## Team Operating Constraints

- 3 collaborators working in parallel.
- Document-first workflow: quest docs before implementation.
- Small, reviewable pull requests linked to quest docs.

## Done Criteria (Project-Level)

- At least one end-to-end train + inference path works through challenge entrypoints.
- Reproducible setup instructions are documented.
- Core modeling/inference quests have validation evidence.
- Major technical decisions are captured in docs.
- Lightning CLI-based training path is integrated behind `team_code.py` wrappers.
- Docker build succeeds using only `requirements.txt`.

## Dependency Policy

- Local/dev dependency workflow: `pyproject.toml` + `uv.lock`.
- Submission dependency workflow: `requirements.txt`.
- Dependency changes are not complete until both surfaces are synchronized.

## Training Pipeline Policy

- Use Lightning CLI as the primary local training orchestrator.
- Keep challenge-called scripts as stable wrappers.
- Place training/inference implementation in package code (`src/physionet2026/`).

## Required Cross-References

- [Project Operating Plan](./project-operating-plan.md)
- [AI Agent Task Workflow](./best-practices/ai-agent-task-workflow.md)
- [Quest Creation Best Practices](./best-practices/quest-creation-best-practices.md)
