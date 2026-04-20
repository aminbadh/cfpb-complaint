# Business Data Mining Project: CFPB Consumer Complaints

This folder is the working area for our NLP + multi-model business data mining project.

## Python Setup
Create and activate the project virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Project Goal
Build and compare multiple models to predict complaint outcomes and generate business insights from complaint narratives.

## Official Data Sources
Primary source page:
- https://www.consumerfinance.gov/data-research/consumer-complaints/

Direct full dataset downloads:
- CSV ZIP: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
- JSON ZIP: https://files.consumerfinance.gov/ccdb/complaints.json.zip

Documentation:
- Field reference: https://cfpb.github.io/api/ccdb/fields.html
- API docs: https://cfpb.github.io/api/ccdb/api.html
- Current API base: https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/

## Why This Dataset
- Public and high-volume real-world complaint data.
- Includes text narratives for NLP.
- Includes structured fields for tree-based and tabular modeling.
- Supports a strong final ensemble setup (for example Voting Classifier).

## Target Variable
**Predict Monetary Relief Outcome** (binary classification):
- **1**: Complaint receives monetary relief (e.g., refund, credit, restitution)
- **0**: Complaint resolved without monetary relief (explanation only)

Why this target:
- Direct business impact (predicts cost)
- Realistic class balance (~30-40% positive)
- Allows early warning and resource allocation
- Perfect for multi-model comparison

Features:
- **Text**: Consumer complaint narrative (cleaned, vectorized)
- **Structured**: Product, Issue, State, Submission channel, Temporal features

Leakage prevention:
- Exclude company response fields created after resolution
- Use only complaint intake and metadata available at receipt time

## Quick Start: Fetch Data (Choose One)

### Option 1: Full Dataset Download (1.8 GB, slower)
If you need the complete dataset:

```bash
mkdir -p data/raw
curl -L "https://files.consumerfinance.gov/ccdb/complaints.csv.zip" -o data/raw/complaints.csv.zip
unzip -o data/raw/complaints.csv.zip -d data/raw
```

Or use the helper script:

```bash
python src/download_cfpb_data.py --download
```

### Option 2: Lightweight API Sample (fallback)
If downloading the full archive is unstable on your machine, pull a smaller JSON sample:

```bash
python src/fetch_cfpb_api.py --records 10000
```

## Minimal Working Structure

```text
cfpb-complaint/
  README.md
  data/
    raw/
    processed/
  notebooks/
  src/
  reports/
   # Planned (future):
   # app/
   #   streamlit_app.py
```

## Planned Next Step (GUI)

A **Streamlit GUI** is planned for a later phase to test trained models live (single complaint prediction + batch testing), compare outputs, and present key metrics interactively.

Implementation is intentionally deferred until preprocessing/modeling are finalized.

## Project Status

| Phase | File(s) | Status | Notes |
|---|---|---|---|
| Data Acquisition | `data/raw/complaints.csv` | ✓ Complete | Full 1.8GB dataset available; sampled 5K rows for efficiency |
| Sampling | `src/sample_cfpb_data.py` | ✓ Complete | Chunked reading prevents memory overload |
| EDA | `01_data_loading_and_eda.ipynb` | ✓ Complete | Target validated, narratives available (25%), class distribution analyzed |
| Preprocessing | `02_preprocessing.ipynb` | → Ready | Text cleaning, feature engineering, train/test split (80/20) |
| Modeling | `03_modeling.ipynb` | → Ready | 5 model families: Logistic Regression, Naive Bayes, KNN, Random Forest, ANN |
| Ensemble | `03_modeling.ipynb` | → Ready | Soft voting classifier combines 5 models |
| Report | `reports/` | → Template | Model comparison tables, metrics, visualizations |

## Models Included

1. **Baseline (Text-only)**
   - Logistic Regression on TF-IDF
   - Naive Bayes on TF-IDF

2. **Nearest Neighbors**
   - KNN (k=5) on SVD-reduced TF-IDF

3. **Tree Ensemble (Structured + Text)**
   - Random Forest (100 trees, depth=15)

4. **Neural Network**
   - MLP: 128 → 64 → 32 → 1 (with early stopping)

5. **Meta-Learner**
   - Voting Classifier (soft vote average of 5 models)

## Quick Start

### Run the Full Pipeline

```bash
# Activate environment
source .venv/bin/activate

# Already done: data loaded and sampled
# Already done: EDA completed

# Preprocess
jupyter notebook notebooks/02_preprocessing.ipynb
# Output: train_features.csv, test_features.csv

# Train & Compare Models
jupyter notebook notebooks/03_modeling.ipynb
# Output: model_comparison.csv, model_comparison_with_ensemble.csv
```

## Key Metrics

All models evaluated on:
- **Accuracy**: Overall correctness
- **Precision**: Avoiding false positives (costs)
- **Recall**: Catching true monetary-relief cases
- **F1**: Harmonic mean (primary metric)
- **ROC-AUC**: Ranking ability
- **PR-AUC**: Precision-recall trade-off (handles imbalance well)
