# AI Agent Task Workflow

Use this workflow for any AI-assisted coding task in this repository.

## Workflow

1. Read [requirements-overview.md](../requirements-overview.md) and the relevant quest docs.
2. Restate the task in concrete terms (inputs, outputs, constraints).
3. Implement the smallest viable change.
4. Run local validation (tests/lint/type checks or targeted script runs).
5. Update the quest doc with:
   - what changed,
   - validation evidence,
   - remaining risks.
6. Open/finish PR with the quest reference.

## Mandatory Rules

- Do not implement code without a linked quest.
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
