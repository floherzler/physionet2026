# Local Dev Bootstrap (Clone -> UV -> Kaggle 10-file Sample -> Embeddings)

This guide is the reproducible local path used for offline SleepFM embedding extraction tests.

## 1) Prerequisites

- Linux/macOS shell with `bash`
- `git`
- `uv` (https://docs.astral.sh/uv/)
- Kaggle CLI (`kaggle`) with API access

Verify tools:

```bash
uv --version
kaggle --version
```

## 2) Clone and enter repo

```bash
git clone git@github.com:floherzler/physionet2026.git
cd physionet2026
```

## 3) Configure Kaggle auth

Kaggle CLI expects credentials in `~/.kaggle/kaggle.json`.

```bash
mkdir -p ~/.kaggle
chmod 700 ~/.kaggle
# place kaggle.json in ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

Quick access check:

```bash
kaggle datasets files physionet/physionetchallenge2026data | head -n 20
```

## 4) Download the 10-file training sample

This creates `data/challenge2026_training10/` with:

- `demographics.csv`
- 10 physiological EDF files under `training_set/physiological_data/...`
- matching annotation files under `training_set/human_annotations/...` and `training_set/algorithmic_annotations/...`

```bash
mkdir -p data/challenge2026_training10

# 4.1 Download training demographics
kaggle datasets download -d physionet/physionetchallenge2026data \
  -f training_set/demographics.csv \
  -p data/challenge2026_training10

# 4.2 Build first-10 physiological EDF paths from demographics
tail -n +2 data/challenge2026_training10/demographics.csv \
| head -n 10 \
| awk -F, '{printf "training_set/physiological_data/%s/%s_ses-%s.edf\n",$1,$4,$5}' \
> /tmp/training10_edf_paths.txt

# 4.3 Download 10 physiological EDF files
while read -r f; do
  kaggle datasets download \
    -d physionet/physionetchallenge2026data \
    -f "$f" \
    -p data/challenge2026_training10
done < /tmp/training10_edf_paths.txt

# 4.4 Download matching human + algorithmic annotation EDF files
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

## 5) Create UV environment and install dependencies

Use a dedicated environment for offline SleepFM extraction.

```bash
uv venv .venv-sleepfm --python 3.10
source .venv-sleepfm/bin/activate

# Main repo dependency surface
uv pip install -r requirements.txt

# SleepFM extraction stack
uv pip install -r external/sleepfm-clinical/requirements.txt
```

If torch resolution needs explicit index:

```bash
uv pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu
```

Optional cache warning cleanup:

```bash
export TRANSFORMERS_CACHE="$PWD/.cache/huggingface"
```

## 6) Run embedding extraction for the 10-file sample

```bash
.venv-sleepfm/bin/python scripts/extract_sleepfm_embeddings.py \
  --data-folder data/challenge2026_training10/training_set \
  --output-folder artifacts/sleepfm_cache \
  --sleepfm-root external/sleepfm-clinical \
  --manifest artifacts/sleepfm_cache/manifest.csv \
  --seed 420 \
  --limit 10
```

## 7) Validate outputs

```bash
.venv-sleepfm/bin/python - <<'PY'
import pandas as pd
df = pd.read_csv("artifacts/sleepfm_cache/manifest.csv")
print(df[["cache_key", "status", "num_windows", "embedding_dim"]].head(20))
print("rows=", len(df), "unique_keys=", df["cache_key"].nunique())
print("status_counts=", df["status"].value_counts(dropna=False).to_dict())
PY
```

Expected for a healthy run:

- `status_counts` should include `ok` rows (ideally all 10 for this sample).
- For each `ok` row:
  - `artifacts/sleepfm_cache/<SiteID>/<BidsFolder>/ses-<SessionID>/embeddings.h5` exists
  - `artifacts/sleepfm_cache/<SiteID>/<BidsFolder>/ses-<SessionID>/meta.json` exists
