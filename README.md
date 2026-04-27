# Business Data Mining Project: CFPB Consumer Complaints

This folder is the working area for our NLP + multi-model business data mining project.

Read the final report: [reports/final_report/final_report.pdf](reports/final_report/final_report.pdf)

## Development Note
AI coding agents were used during development to help draft, revise, and organize parts of this project. In particular, the repository's `AGENTS.md` file was used to provide project-specific context and task instructions so updates could be made with clearer constraints and expectations. All generated or assisted changes were reviewed after creation before being kept in the project.

## Python Setup
Create and activate the project virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Project Goal
Build a binary classifier that predicts whether a complaint will result in monetary relief, using complaint-time information (narrative + structured intake fields).

Specific deliverables:
- A clean, leakage-safe training dataset and reproducible preprocessing pipeline
- Multiple baseline and advanced models with comparable evaluation
- A final champion or ensemble model selected by business-relevant metrics (F1, PR-AUC, recall)
- Actionable business insights: where monetary relief risk is concentrated by product/issue/channel/time

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

## Full Dataset Profile (Local Snapshot)

The full dataset currently loaded in this repo is:
- Rows: 14,636,145
- Columns: 18
- Compressed file size (`complaints.csv.zip`): ~1.7 GB
- Uncompressed CSV size (`complaints.csv`): ~8.0 GB
- Raw data directory size (`data/raw/`): ~9.7 GB

These numbers were measured from the local files in this project on 2026-04-20.

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

## Quick Start: Fetch Data

### Full Dataset Download (~1.7 GB zip, ~8.0 GB extracted)
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

## Minimal Working Structure

```text
cfpb-complaint/
  README.md
  app/
    streamlit_app.py
  data/
    raw/
    processed/
  docs/
  notebooks/
  reports/
  src/
```

## File Responsibilities (Single Source of Truth)

- `notebooks/01_data_loading_and_eda.ipynb`: Data loading, quality checks, schema review, and exploratory visuals only.
- `notebooks/02_preprocessing.ipynb`: Authoritative target construction and leakage-safe feature engineering.
- `notebooks/03_modeling.ipynb`: Model training, comparison, and ensemble evaluation using preprocessed outputs.
- `src/download_cfpb_data.py`: Download and extract official CFPB data into `data/raw/`.
- `src/sample_cfpb_data.py`: Create memory-safe working samples from large raw CSV files.

Boundary rule:
- If a step changes labels/features used for training, it belongs in `02_preprocessing.ipynb`.
- If a step is only descriptive/exploratory, it belongs in `01_data_loading_and_eda.ipynb`.

## Interactive Streamlit Demo

A lightweight Streamlit app is included to support in-class demonstration of model tuning and decision-threshold tradeoffs.

Run from the project root:

```bash
source .venv/bin/activate
streamlit run app/streamlit_app.py
```

The app retrains quickly on sampled data and lets you adjust:
- model choice (Logistic Regression, Naive Bayes, KNN, Random Forest, Neural Network, Voting Ensemble),
- model-specific hyperparameters (only shown for the selected model),
- decision threshold with live confusion-matrix/metric updates.

This is presentation-oriented and intentionally focused on model behavior exploration rather than production inference serving.

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

## Reports Tracking

The `reports/` folder can contain many generated intermediate artifacts (tables, curves, confusion matrix exports) that are useful during iteration but noisy for version control.

This project now keeps the final deliverables in version control under:

- `reports/final_report/`

and ignores other generated report files in `reports/` by default via `.gitignore`.

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
