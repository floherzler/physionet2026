# Expedition Map

Updated on: `2026-03-04`

A lightweight roadmap that complements quests by showing direction and sequencing.

## Current Expedition Stage

- Stage name: `SleepFM Basecamp`
- Time window: `2026-03 to <next checkpoint>`
- Success definition: SleepFM integration works with PhysioNet Challenge 2026 data path.

## Milestones

1. SleepFM integration works on challenge data
   - Outcome: one stable, reproducible baseline pipeline using SleepFM with PhysioNet challenge modalities/data flow.
   - Dependency: submodule integration and data compatibility checks.
2. Improve task-specific performance
   - Outcome: targeted modeling/training improvements once baseline path is stable.
   - Dependency: milestone 1 complete with validated baseline.
3. Add time-aware multimodal modeling
   - Outcome: prototype module for temporal reasoning over modality snippets across the night.
   - Dependency: working baseline plus clear temporal slicing strategy.

## Risk Terrain

- High-risk area: reliance on methods with limited public implementation details (e.g., by-time cross-net).
  - Early warning signal: inability to reproduce core behavior from paper description.
  - Mitigation path: first ship a simpler time-aware baseline, then incrementally approximate paper mechanisms.

## Link to Active Quests

- `docs/quests/Q-0001-integrate-sleepfm-submodule.md`
- `docs/quests/Q-0002-refine-handbook-structure.md`
- `docs/quests/Q-0003-kaggle-data-access-and-sampling.md` (In Progress)
- `docs/quests/side-quests/Q-0103-time-aware-multimodal-module.md` (Draft, parked)

## Questions to answer

- Do you want date-based checkpoints per milestone, or sequence-only tracking for now?
- Should by-time cross-net exploration become its own dedicated quest once baseline is stable?
