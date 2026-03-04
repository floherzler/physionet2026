# Q-0003: Kaggle Data Access and Local Sampling for PhysioNet 2026

## Quest Metadata

- Quest ID: `Q-0003`
- Status:
  - [x] Draft
  - [ ] In Progress
  - [ ] In Review
  - [x] Completed
- Created date (YYYY-MM-DD): `2026-03-04`
- Completed date (YYYY-MM-DD): `2026-03-04`
- Completed timestamp UTC (YYYY-MM-DDTHH:MM:SSZ): `2026-03-04T22:27:11Z`
- Owner (GitHub): `@floherzler`

## Objective

Establish a reproducible Kaggle CLI workflow to discover, partially download, and locally inspect PhysioNet Challenge 2026 data without requiring a full dataset download.

## Scope

- Use Kaggle CLI against `physionet/physionetchallenge2026data`.
- Document authentication expectations for `kaggle` CLI v2.
- Record exact commands used to list files and download a small local sample.
- Keep this quest focused on data access and format understanding (not model training).

## Acceptance Criteria

- [x] Kaggle CLI is installed and callable locally (`kaggle --version`).
- [x] Dataset file listing is validated for `physionet/physionetchallenge2026data`.
- [x] At least one metadata CSV and one EDF file are downloaded as a local sample.
- [x] Follow-up notes identify whether full download is needed for next quest.

## Implementation Tasks

- [x] Verify CLI availability and authentication path.
- [x] Enumerate Kaggle dataset files.
- [x] Download minimal sample for format inspection.
- [x] Add short data-profiling notes (schema/channels/session structure) for handoff.

## Validation

Commands used (retroactive record):

```bash
# Verify CLI
kaggle --version

# Enumerate dataset files
kaggle datasets files physionet/physionetchallenge2026data

# Download sample metadata and one EDF
mkdir -p data/challenge2026_sample
kaggle datasets download -d physionet/physionetchallenge2026data \
  -f supplementary_set/demographics.csv \
  -p data/challenge2026_sample
kaggle datasets download -d physionet/physionetchallenge2026data \
  -f supplementary_set/physiological_data/I0004/sub-I0004177500794_ses-4.edf \
  -p data/challenge2026_sample

# Corrected path for true training samples
kaggle datasets download -d physionet/physionetchallenge2026data \
  -f training_set/demographics.csv \
  -p data/challenge2026_training10

# Build first-10 training EDF paths from demographics and download
tail -n +2 data/challenge2026_training10/demographics.csv \
| head -n 10 \
| awk -F, '{printf "training_set/physiological_data/%s/%s_ses-%s.edf\n",$1,$4,$5}' \
> /tmp/training10_edf_paths.txt

while read -r f; do
  kaggle datasets download \
    -d physionet/physionetchallenge2026data \
    -f "$f" \
    -p data/challenge2026_training10
done < /tmp/training10_edf_paths.txt

# Build annotation paths from demographics and download
# demographics columns:
#   $1=SiteID, $4=BidsFolder (sub-...), $5=SessionID
# resolved filenames on Kaggle:
#   human:       <BidsFolder>_ses-<SessionID>_expert_annotations.edf
#   algorithmic: <BidsFolder>_ses-<SessionID>_caisr_annotations.edf
tail -n +2 data/challenge2026_training10/demographics.csv \
| head -n 10 \
| awk -F, '{
  base=$4"_ses-"$5
  print "training_set/human_annotations/"$1"/"base"_expert_annotations.edf"
  print "training_set/algorithmic_annotations/"$1"/"base"_caisr_annotations.edf"
}' \
| while read -r f; do
  outdir="data/challenge2026_training10/$(dirname "$f")"
  mkdir -p "$outdir"
  kaggle datasets download -d physionet/physionetchallenge2026data -f "$f" -p "$outdir"
done
```

Observed evidence:

- `kaggle datasets files` returned paginated file listing including `supplementary_set/demographics.csv` and multiple EDFs under `supplementary_set/physiological_data/...`.
- Sample EDF file sizes in listing are on the order of ~90 MB to ~536 MB, supporting incremental download strategy.
- `data/challenge2026_training10/` contains `training_set/demographics.csv` and downloaded training EDFs (e.g., `sub-I0002150001401_ses-2.edf`, `sub-I0002150005420_ses-1.edf`).
- Annotation filename conventions were confirmed and used for successful downloads, e.g.:
  - `training_set/human_annotations/I0002/sub-I0002150001401_ses-2_expert_annotations.edf`
  - `training_set/algorithmic_annotations/I0002/sub-I0002150001401_ses-2_caisr_annotations.edf`

## Risks / Open Questions

- Full dataset extraction may exceed practical local storage headroom once unzipped artifacts and derived intermediates are added.
- Confirm whether next active quest should prioritize data profiling/loader hardening before full SleepFM baseline runs.
- Decision for next step: continue with incremental downloads and sample-based loader checks before any full data pull.

## Links

- Requirements: `docs/requirements-overview.md`
- Workflow: `docs/best-practices/ai-agent-task-workflow.md`
- Planning guide: `docs/best-practices/quest-creation-best-practices.md`
- Related quests:
  - `docs/quests/Q-0001-integrate-sleepfm-submodule.md`
  - `docs/quests/Q-0002-refine-handbook-structure.md`
  - `docs/quests/side-quests/Q-0103-time-aware-multimodal-module.md`
