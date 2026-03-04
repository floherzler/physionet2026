# Q-0002: Refine Handbook Structure and Fill-In Prompts

## Quest Metadata

- Quest ID: `Q-0002`
- Status:
  - [x] Draft
  - [ ] In Progress
  - [ ] In Review
  - [x] Completed
- Created date (YYYY-MM-DD): `2026-03-04`
- Completed date (YYYY-MM-DD): `2026-03-04`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `2026-03-04T21:23:09Z`
- Owner (GitHub): `@floherzler`

## Objective

Create an "adventurous" handbook scaffold that complements quests, with practical templates and questions for progressive content fill-in.

## Scope

- Refine `handbook/README.md` to define structure and usage.
- Add starter files for:
  - `handbook/lorebook/README.md`
  - `handbook/guild-charter.md`
  - `handbook/map.md`
- Add explicit fill-in questions in handbook files to guide collaborator input.

## Acceptance Criteria

- [x] Handbook root README clearly explains purpose and folder layout.
- [x] `lorebook`, `guild-charter`, and `map` files exist with concise templates.
- [x] Each new handbook file includes actionable questions/placeholders for user-provided content.
- [x] Quest doc is updated with validation evidence and status for review handoff.

## Implementation Tasks

- [x] Update `handbook/README.md` with structure, conventions, and write-in prompts.
- [x] Create `handbook/lorebook/README.md`.
- [x] Create `handbook/guild-charter.md`.
- [x] Create `handbook/map.md`.
- [x] Run quick validation (`find`, `rg`) and record evidence.

## Validation

- Commands:
  - `find handbook -maxdepth 3 -type f | sort`
  - `rg -n "Questions to answer|Adventurer prompts|Fill this in" handbook`
- Evidence:
  - `find` output shows:
    - `handbook/README.md`
    - `handbook/guild-charter.md`
    - `handbook/lorebook/README.md`
    - `handbook/map.md`
  - `rg` output shows prompt sections in all handbook files:
    - `Questions to answer` present in 4 files.
    - `Fill this in` present in content template files.

## Risks / Open Questions

- "Adventurous" tone may drift into low-signal fluff if not anchored by concrete operating decisions.
- Team may prefer different naming for sections after first usage.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
