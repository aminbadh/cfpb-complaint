# Project Alignment Plan (Spring 2026 Data Mining Requirements)

This plan translates the new reference documents into concrete repo updates.

## 1) What must change now

1. Expand evaluation beyond accuracy and F1.
2. Add model tuning with cross-validation.
3. Add at least one stronger ensemble strategy beyond simple averaging.
4. Add interpretation artifacts and business insight outputs.
5. Add a short live-run script for presentation day.
6. Restructure report content to match the required course sections.

## 2) Gap analysis against current project

Current strengths:
- Clear business objective and target variable.
- Reproducible preprocessing split.
- Multiple baseline and advanced models.
- Existing comparison reports with core metrics.

Current gaps:
- No Cohen's kappa in model comparison outputs.
- No confusion matrix summary per model.
- No threshold tuning (default 0.5 only).
- No cross-validated tuning process (GridSearchCV or RandomizedSearchCV).
- Ensemble is manual soft average only; no weighted voting or stacking experiment.
- No dedicated model interpretation output (top features, error slices).
- No presentation-ready live inference script.

## 3) Required repository updates

### A. Modeling notebook updates
File: notebooks/03_modeling.ipynb

Add:
1. Metrics block with:
   - Cohen's kappa
   - Balanced accuracy
   - Confusion matrix counts (TP, FP, TN, FN)
2. Threshold search per model:
   - Sweep thresholds from 0.10 to 0.90
   - Pick threshold maximizing F1 or business-weighted utility
3. Calibration and curve diagnostics:
   - ROC curve and PR curve plots for top models
4. Cross-validated tuning:
   - Logistic Regression: C, class_weight
   - Random Forest: n_estimators, max_depth, min_samples_leaf
   - KNN: n_neighbors, weights
5. Stronger ensemble experiments:
   - Weighted soft voting
   - StackingClassifier (meta learner: logistic regression)

Outputs to save:
- reports/model_comparison_detailed.csv
- reports/threshold_analysis.csv
- reports/confusion_matrices.csv

### B. Preprocessing notebook checks
File: notebooks/02_preprocessing.ipynb

Add a short validation cell that confirms:
1. Leakage columns are not present in modeling input.
2. Missing-value handling summary by feature.
3. Final feature dictionary table for the report.

Outputs to save:
- reports/preprocessing_summary.csv
- reports/feature_dictionary.csv

### C. New live demo script
New file to create:
- src/live_demo.py

Behavior:
1. Load saved champion model and preprocessing artifacts.
2. Accept one complaint text plus structured fields (CLI args).
3. Print:
   - predicted class
   - probability of monetary relief
   - decision threshold used
4. Optional batch mode for CSV input.

This satisfies the in-class live model run requirement.

### D. Report structure alignment
Add/update a final report document (markdown is fine) with required sections:
1. Title page + presentation link
2. Dataset description
3. Problem statement and research questions
4. Data preparation decisions (justified)
5. Methods and why each is appropriate
6. Results and interpretation (with curves and confusion matrices)
7. Conclusion and business recommendations

Suggested file:
- reports/final_report.md

## 4) Priority execution order

1. Update evaluation function in modeling notebook.
2. Add tuning + threshold optimization.
3. Add weighted voting + stacking.
4. Export detailed reports.
5. Build live demo script.
6. Finalize final report markdown and slide storyboard.

## 5) Show the project evolution (required in presentation)

Treat project evolution as evidence of scientific rigor. Explicitly show what was wrong,
how it was detected, and what changed.

Include one slide titled: "What we got wrong and how we fixed it"

Minimum items to show:
1. Initial framing or target mismatch:
   - Document the initial target/feature framing that was weak or inconsistent.
   - Explain why it was problematic (for example, post-outcome signal leakage, unclear business objective, or unstable label logic).
2. Correction applied:
   - Show the corrected target definition and leakage-safe feature boundary.
   - Mention where the fix was implemented in preprocessing.
3. Measurable impact:
   - Before/after table with at least F1, PR-AUC, and Kappa.
   - Brief interpretation of what improved and what tradeoff remained.
4. Process lesson:
   - One sentence on what this changed in your modeling strategy.

Suggested artifact to prepare:
- `reports/evolution_log.md` with columns:
  - phase
  - issue_detected
  - decision_made
  - evidence_metric_before
  - evidence_metric_after
  - impact_on_business_use

## 6) Minimum acceptance checklist (ready for grading)

- At least 3 models tuned with cross-validation.
- Final table includes Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Kappa.
- Confusion matrix for champion model included in report.
- Threshold choice explicitly justified.
- Ensemble comparison includes at least one method better than untuned baseline.
- Live run command works in front of class.
- Presentation includes a transparent mistakes-to-improvements timeline.

## 7) Suggested commands for reproducible run

1. python src/sample_cfpb_data.py --sample-size 20000
2. Run notebooks/02_preprocessing.ipynb
3. Run notebooks/03_modeling.ipynb
4. python src/live_demo.py --help
