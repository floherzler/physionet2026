# Lorebook

Updated on: `2026-03-04`

Domain and project lore that helps contributors reason faster.

Use this section for:

- Clinical context that affects modeling choices.
- Definitions and shorthand used in this repo.
- Data caveats and assumptions that are easy to forget.

## Fill this in

### 1) Problem Framing

- Build robust models for the PhysioNet Challenge 2026 sleep-study setting across multiple modalities.
- Most harmful early failure mode: brittle integration that works on toy paths but fails on challenge data contracts.

### 2) Vocabulary

- Canonical terms:
  - `Modality`: one signal source from the overnight sleep study (not ECG-only).
  - `Snippet`: a local time slice/chunk from one or more modalities.
  - `Time-aware module`: model component that explicitly uses temporal order across the night.

### 3) Data Realities

- This challenge context is multimodal sleep-study data; scope should always be checked against available modality channels.
- Initial lore focus is minimal and modality-oriented, not deep clinical interpretation.

### 4) Modeling Heuristics

- Prioritize getting one end-to-end working integration (SleepFM + challenge data path) before optimizing architecture.
- Avoid premature complexity in early quests; add temporal fusion after baseline compatibility is stable.

## Questions to answer

- Which exact modality names should be listed explicitly from the challenge dataset once finalized?
- When we add deeper lore, should we cite papers inline here or in a separate bibliography file?
