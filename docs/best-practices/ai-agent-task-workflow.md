# AI Agent Task Workflow

Use this workflow for any AI-assisted coding task in this repository.

## Modes

- Planning Mode: define and finalize quest scope before coding.
- Implementation Mode: execute an approved quest with minimal extra context.

## Planning Mode

1. Read [requirements-overview.md](../requirements-overview.md) and [project-operating-plan.md](../project-operating-plan.md).
2. Create or update a quest file in `docs/quests/` using `docs/templates/quest-template.md`.
3. Fill objective, scope, acceptance criteria, implementation tasks, validation, and risks.
4. Keep quest status as Draft until plan is approved.
5. Finalize the quest and mark status as In Progress when ready for execution.

## Implementation Mode

1. Read the approved quest file first.
2. Restate the task in concrete terms (inputs, outputs, constraints).
3. Implement the smallest viable change aligned to quest acceptance criteria.
4. Run local validation (tests/lint/type checks or targeted script runs).
5. Update the quest doc with:
   - completed checkboxes,
   - what changed,
   - validation evidence,
   - remaining risks.
6. Open/finish PR with the quest reference.
7. When merged, set quest status to Completed and fill completion date + UTC timestamp.

## Chat Handoff Protocol (Plan -> Build)

Use separate chats to keep context clean:

1. Planning chat finalizes quest file only.
2. Start a new implementation chat and pass only the handoff prompt below.
3. Implementation chat must not redefine quest scope unless requested.

## Copy/Paste Implementation Prompt

```text
Implement quest: docs/quests/Q-XXXX-<slug>.md

Follow these files in this order:
1) docs/quests/Q-XXXX-<slug>.md
2) docs/requirements-overview.md
3) docs/project-operating-plan.md
4) docs/best-practices/ai-agent-task-workflow.md
5) docs/best-practices/quest-creation-best-practices.md

Rules:
- Do not change scope outside the quest acceptance criteria.
- Keep challenge root contracts intact (train_model.py, run_model.py, evaluate_model.py, helper_code.py, team_code.py signatures).
- If dependencies change, keep pyproject.toml/uv.lock and requirements.txt in sync.
- Update the quest file with completed checkboxes, validation evidence, and residual risks.

Deliverables:
- Code changes required by the quest
- Updated quest markdown with status and evidence
- Short summary of what was done and what remains
```

## Mandatory Rules

- Do not implement code without a linked quest.
- Before implementing, verify quest completion state:
  - if `Completed` is checked and completion date/timestamp are filled, do not re-implement;
  - only proceed if the user explicitly requests reopening that completed quest.
- Do not change challenge root contracts unless quest explicitly allows it.
- Keep edits scoped to quest acceptance criteria.
- Prefer incremental commits and reviewable diffs.
- If dependencies change, update both `pyproject.toml`/`uv.lock` and `requirements.txt`.
- Keep Lightning-heavy logic in package code, not in challenge wrapper scripts.

## PR Linking Convention

- Include quest path in PR description, for example:
  - `docs/quests/Q-0003-datamodule.md`

## Cross-References

- [Project Operating Plan](../project-operating-plan.md)
- [Requirements Overview](../requirements-overview.md)
- [Quest Creation Best Practices](./quest-creation-best-practices.md)
