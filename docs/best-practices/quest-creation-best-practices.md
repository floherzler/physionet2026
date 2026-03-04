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
- Prefer minimal quests: include only what is necessary for handoff.

## Completion and History Rules

- Keep quest files in Git history; do not delete completed quests.
- Mark completion in the file itself.
- Fill both:
  - completion date (`YYYY-MM-DD`)
  - completion timestamp in UTC (`YYYY-MM-DDTHH:MM:SSZ`)
- Completed quests are immutable by default:
  - do not implement them again unless explicitly reopened.

## Minimal Required Sections

- Quest Metadata
- Objective
- Scope
- Acceptance Criteria (checkboxes)
- Implementation Tasks (checkboxes)
- Validation
- Risks / Open Questions
- Links

Optional sections:
- Add extra detail only when ambiguity would otherwise block implementation.

## Iteration Policy

- Use incrementing quest numbers for new work, even if related to prior quests.
- If additional work is needed after completion, create a new quest (e.g. `Q-0012-followup-...`) instead of silently extending old scope.

## Cross-References

- [Project Operating Plan](../project-operating-plan.md)
- [Requirements Overview](../requirements-overview.md)
- [AI Agent Task Workflow](./ai-agent-task-workflow.md)
