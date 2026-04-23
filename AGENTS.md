# AGENTS Guide

## Purpose
This repository builds a binary classifier for CFPB complaints to predict monetary relief outcomes from complaint-time information.

## Read First
- Project overview and setup: [README.md](README.md)
- Course requirements context: [docs/project_desc.md](docs/project_desc.md)
- Evaluation rubric notes: [docs/evaluate.md](docs/evaluate.md)
- Improvement notes: [docs/improve.md](docs/improve.md)

## Repository Map
- Data loading and EDA only: [notebooks/01_data_loading_and_eda.ipynb](notebooks/01_data_loading_and_eda.ipynb)
- Authoritative preprocessing and target construction: [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)
- Model training, comparison, and ensembles: [notebooks/03_modeling.ipynb](notebooks/03_modeling.ipynb)
- Shared target-label policy helpers: [src/label_policy.py](src/label_policy.py)
- Raw data download helper: [src/download_cfpb_data.py](src/download_cfpb_data.py)
- Memory-safe sampling helper: [src/sample_cfpb_data.py](src/sample_cfpb_data.py)
- Interactive demo for threshold/model exploration: [app/streamlit_app.py](app/streamlit_app.py)
- Model outputs and report artifacts: [reports](reports)
- Final written report workspace: [reports/final_report](reports/final_report)

## Working Conventions
- Respect notebook boundaries:
  - Label/feature definition changes belong in [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)
  - Descriptive analysis belongs in [notebooks/01_data_loading_and_eda.ipynb](notebooks/01_data_loading_and_eda.ipynb)
  - Modeling and metrics changes belong in [notebooks/03_modeling.ipynb](notebooks/03_modeling.ipynb)
- Keep shared policy logic centralized:
  - If the monetary-relief response mapping changes, update [src/label_policy.py](src/label_policy.py) and keep notebook usage aligned with it.
- Treat the Streamlit app as presentation/demo code:
  - Changes to interactive tuning, threshold exploration, or classroom demo behavior belong in [app/streamlit_app.py](app/streamlit_app.py)
- Keep leakage-safe modeling: do not use post-resolution fields as predictors at inference time.
- Prioritize functionality changes over style-only edits.
- Prefer minimal, targeted edits; do not reformat unrelated cells/files.

## Environment And Commands
- Setup environment:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`
- Data download (optional full dataset):
  - `python src/download_cfpb_data.py --download`
- Memory-safe sample creation:
  - `python src/sample_cfpb_data.py --sample-size 20000`
- Execute pipeline notebooks in order:
  1. [notebooks/01_data_loading_and_eda.ipynb](notebooks/01_data_loading_and_eda.ipynb)
  2. [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb)
  3. [notebooks/03_modeling.ipynb](notebooks/03_modeling.ipynb)

## Output Expectations
When working on modeling updates, ensure key artifacts are produced in [reports](reports), including detailed model comparison, threshold analysis, confusion-matrix summaries, and evolution tracking.

When working on the final written deliverable, keep source/report assets under [reports/final_report](reports/final_report), where:
- `final_report.md` is the report source
- `assets/` contains figures used by the report
- `final_report.pdf` is the exported deliverable when regenerated

## Common Pitfalls
- Running full raw CSV operations can exceed local memory; use chunking/sampling first.
- Accuracy alone is insufficient; include class-imbalance-aware metrics and threshold analysis.
- Keep an explicit mistakes-to-improvements timeline for presentation readiness.
