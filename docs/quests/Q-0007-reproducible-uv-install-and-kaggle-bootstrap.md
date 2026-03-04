# Q-0007: Reproducible UV Install and Kaggle Bootstrap Documentation

## Quest Metadata

- Quest ID: `Q-0007`
- Status:
  - [ ] Draft
  - [x] In Progress
  - [ ] In Review
  - [ ] Completed
- Created date (YYYY-MM-DD): `2026-03-05`
- Completed date (YYYY-MM-DD): `<date>`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `<timestamp>`
- Owner (GitHub): `@floherzler`

## Objective

Provide a fresh-clone reproducible guide for:

- `uv` dependency installation (main repo + SleepFM extraction stack), and
- Kaggle download of the 10-file local sample used for embedding extraction tests.

## Scope

- Add one canonical bootstrap document with copy/paste commands.
- Link the bootstrap doc from `README.md`.
- Keep challenge runtime contracts unchanged.

## Acceptance Criteria

- [x] A new doc explains end-to-end setup from clone to local extraction test.
- [x] Commands include Kaggle auth precheck and deterministic 10-file download path generation.
- [x] Commands include `uv` install steps for both dependency surfaces.
- [x] README links to the new bootstrap doc.

## Implementation Tasks

- [x] Create `docs/local-dev-bootstrap.md` with reproducible commands.
- [x] Add README cross-link for discoverability.
- [x] Record short validation evidence in this quest.

## Validation

- `docs/local-dev-bootstrap.md` created with copy/paste shell blocks.
- `README.md` includes a dedicated link to the bootstrap guide.

## Risks / Open Questions

- Kaggle CLI auth is machine/user-specific (`~/.kaggle/kaggle.json`) and cannot be fully automated in repo docs.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0003-kaggle-data-access-and-sampling.md`
  - `docs/quests/Q-0004-sleepfm-embedding-adapter-and-metric-eval.md`
