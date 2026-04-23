# Improvement Playbook For This Repo

## Purpose
This file tracks the most useful directions for improving the CFPB monetary-relief classifier without breaking the project boundaries or introducing leakage.

## First Priorities
Before adding more complex models, make sure the basics are solid:
- target definition is stable and leakage-safe,
- train/test split is consistent,
- preprocessing is reproducible,
- metrics are tracked consistently across experiments.

## High-Value Improvement Areas

### 1. Better Text Signal
- improve text cleaning without removing important complaint meaning,
- test stronger TF-IDF settings,
- try n-gram ranges,
- reduce noisy rare terms,
- compare text-only versus text-plus-structured inputs.

### 2. Better Structured Features
- review categorical encoding choices,
- group rare categories when helpful,
- add complaint-time temporal features,
- test interaction-friendly models on structured fields.

### 3. Class Imbalance Handling
- compare class weights,
- test threshold tuning,
- monitor precision/recall tradeoffs instead of accuracy only.

### 4. Model Tuning
- tune the strongest baseline models first,
- keep search spaces realistic,
- document what changed and whether it helped,
- avoid adding complexity that does not materially improve evaluation metrics.

### 5. Ensemble Strategy
- only keep ensembles if they outperform simpler models on held-out data,
- verify that ensembles improve more than one metric,
- include threshold analysis for the final ensemble too.

## Safe Improvement Rules
- Do not use post-resolution fields as predictors.
- Do not change the target inside the modeling notebook; target logic belongs in `notebooks/02_preprocessing.ipynb`.
- Keep descriptive exploration in `notebooks/01_data_loading_and_eda.ipynb`.
- Keep final training and comparisons in `notebooks/03_modeling.ipynb`.

## Good Experiment Habits
For each notable experiment, record:
- what changed,
- why it was tested,
- the main metric changes,
- whether the result is worth keeping.

Short experiment tracking is better than rerunning models without notes.

## Improvement Ideas Worth Trying
- stronger logistic regression tuning for TF-IDF features,
- Naive Bayes smoothing comparison,
- KNN dimension reduction tuning,
- Random Forest depth/tree tuning,
- better probability threshold selection,
- calibrated probabilities if threshold behavior is unstable,
- a cleaner soft-voting ensemble built from the best complementary models.

## What To Avoid
- optimizing only for accuracy,
- mixing exploratory edits with authoritative preprocessing logic,
- adding features that are unavailable at complaint time,
- keeping many similar models with no clear comparison,
- large undocumented changes right before presentation.

## Presentation Readiness
The final story should show a visible improvement path:
1. baseline model,
2. key weakness discovered,
3. targeted improvement,
4. metric change,
5. final selected model and threshold.

That improvement timeline is often as important as the final score.
