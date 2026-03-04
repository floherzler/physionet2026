# Quest Creation Best Practices

Use this guide to keep quest docs lightweight, actionable, and traceable in Git.

## Definition

- **Quest**: a small implementation slice with clear acceptance criteria.

## Naming and Numbering

- Use filename format: `Q-0001-<slug>.md`
- Use four-digit sequential numbering (`0001`, `0002`, ...).
- Slug should be short, kebab-case, and outcome-oriented.

## Authoring Rules

- Keep one quest small enough for one focused PR where possible.
- Use concrete acceptance criteria that can be validated.
- Include checkbox task lists so agents can mark progress.
- Record assumptions and risks explicitly.

## Completion and History Rules

- Keep quest files in Git history; do not delete completed quests.
- Mark completion in the file itself.
- Fill both:
  - completion date (`YYYY-MM-DD`)
  - completion timestamp in UTC (`YYYY-MM-DDTHH:MM:SSZ`)

## Minimal Required Sections

- Quest Metadata
- Objective
- Scope / Out of Scope
- Acceptance Criteria (checkboxes)
- Implementation Tasks (checkboxes)
- Validation
- Risks / Open Questions
- Links

## Cross-References

- [Project Operating Plan](../project-operating-plan.md)
- [Requirements Overview](../requirements-overview.md)
- [AI Agent Task Workflow](./ai-agent-task-workflow.md)
