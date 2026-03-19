# Vendored SleepFM Runtime Assets

This folder stores the minimum runtime asset needed for the submission-safe SleepFM baseline in `Q-0008`.

- Source integration quest: `docs/quests/Q-0001-integrate-sleepfm-submodule.md`
- Upstream pinned commit: `70ce04e6f6c656f46a4857fff74ce04a0a00e5da`
- Vendored asset: `checkpoints/model_base/best.pt`

The runtime architecture is reimplemented in `src/physionet2026/vendor_sleepfm.py` so challenge training and inference do not depend on Git submodule checkout behavior.
