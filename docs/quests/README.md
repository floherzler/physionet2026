# Quests Directory

This folder stores quest planning docs for implementation work.

## Suggested Layout

```text
docs/quests/
├── Q-0001-project-setup.md
├── Q-0002-data-ingestion.md
└── Q-0003-training-baseline.md
```

## Rules

- Create quests from `docs/templates/quest-template.md`.
- Use sequential numbering in filenames (`Q-0001`, `Q-0002`, ...).
- Quest files stay in Git history; do not delete completed quests.
- Every quest must link to:
  - `docs/requirements-overview.md`
  - `docs/best-practices/ai-agent-task-workflow.md`
  - `docs/best-practices/quest-creation-best-practices.md`
- Keep docs in Markdown; put non-markdown artifacts in `docs/assets/` or a local `assets/` folder.
