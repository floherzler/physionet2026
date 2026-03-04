# Q-0001: Integrate SleepFM as a Git Submodule

## Quest Metadata

- Quest ID: `Q-0001`
- Status:
  - [x] Draft
  - [ ] In Progress
  - [ ] In Review
  - [ ] Completed
- Created date (YYYY-MM-DD): `2026-03-04`
- Completed date (YYYY-MM-DD): `<date>`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `<timestamp>`
- Owner (GitHub): `@floherzler`

## Objective

Add SleepFM as an external Git submodule and document a challenge-safe integration path so this repo can use SleepFM embeddings without breaking official PhysioNet entrypoint contracts.

## Integration Mode Decision

- Decision for this quest: **offline-only embeddings preparation**.
- Meaning:
  - SleepFM is integrated as a submodule and documented for local embedding extraction workflows.
  - Challenge runtime entrypoints do **not** call SleepFM directly in this quest.
  - Runtime adapter wiring is not part of this quest.

## SleepFM Reference Pin

- Repository: `https://github.com/zou-group/sleepfm-clinical`
- Latest observed `main` commit (UTC check date 2026-03-04): `70ce04e6f6c656f46a4857fff74ce04a0a00e5da`
- This quest should pin the submodule to that commit unless explicitly changed during implementation.

## Scope

- Add SleepFM repository as a submodule under `external/sleepfm-clinical`.
- Document why and how it is integrated for local experimentation and challenge-safe usage.
- Define boundaries: offline embedding extraction only; no direct challenge-runtime invocation.

## Acceptance Criteria

- [ ] SleepFM submodule exists at `external/sleepfm-clinical` and is pinned to commit `70ce04e6f6c656f46a4857fff74ce04a0a00e5da`.
- [ ] `.gitmodules` contains the SleepFM source URL and path.
- [ ] `docs/project-operating-plan.md` includes explicit offline-only integration boundary for this quest.
- [ ] `docs/requirements-overview.md` remains compliant with dependency policy (`uv` local workflow, `requirements.txt` challenge runtime).
- [ ] Quest metadata and status are updated for handoff (`In Review` or `Completed`) with evidence.

## Implementation Tasks

- [ ] Add submodule: `external/sleepfm-clinical` from `https://github.com/zou-group/sleepfm-clinical`.
- [ ] Pin submodule to commit `70ce04e6f6c656f46a4857fff74ce04a0a00e5da`.
- [ ] Add documentation note to `docs/project-operating-plan.md` clarifying offline-only mode in this quest.
- [ ] Link this quest from PR description and keep updates in this file.

## Validation

- Commands:
  - `git submodule status`
  - `git config -f .gitmodules --get-regexp "submodule\\..*\\.(path|url)"`
  - `rg -n "sleepfm|submodule|external/sleepfm-clinical" docs README.md`
- Evidence:
  - Submodule appears in `.gitmodules` and under `external/sleepfm-clinical` at pinned hash.
  - Docs clearly describe offline-only approach for this quest.
  - Quest file reflects status and completion metadata when done.

## Risks / Open Questions

- SleepFM dependency set may be heavy for challenge container runtime; keep runtime path optional and controlled.
- License and compatibility constraints should be confirmed before submission packaging.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
