# Evaluation Guide For This Project

## Purpose
This file summarizes how model evaluation should be handled in this repository. The project predicts whether a CFPB complaint will result in monetary relief, so evaluation should focus on class imbalance, business usefulness, and clear comparison across models.

## What To Report
For every serious model candidate, report at least:
- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- PR-AUC
- Confusion matrix

Accuracy alone is not enough for this project.

## Recommended Primary View
Use a combination of:
- `F1` as the main single-number comparison,
- `PR-AUC` for imbalanced classification quality,
- `Recall` when we want to avoid missing monetary-relief cases,
- `Precision` when we want to reduce false positives.

The final model choice should be justified in business terms, not only by the highest accuracy.

## Threshold Analysis
Do not stop at the default threshold of `0.50`.

For the main shortlisted models:
- compare several probability thresholds,
- show how precision and recall move together,
- explain which threshold is best for the presentation/demo,
- save threshold analysis outputs in `reports/`.

Useful threshold outputs include:
- precision/recall/F1 by threshold,
- confusion matrices at selected thresholds,
- short notes on the tradeoff.

## Confusion Matrix Checklist
Every final comparison should make it easy to answer:
- How many positive cases were caught?
- How many were missed?
- How many false alarms were created?
- Is the error profile acceptable for the project goal?

If the model has high accuracy but poor recall on the positive class, call that out clearly.

## Validation Rules
- Keep preprocessing and target definition leakage-safe.
- Evaluate on held-out data or clean cross-validation splits.
- Use the same evaluation setup across models when comparing them.
- Do not compare models trained on different targets or inconsistent feature sets without explaining it.

## Model Comparison Expectations
The final report or artifacts should make it easy to compare:
- baseline text models,
- structured-feature models,
- combined/ensemble approaches,
- threshold-adjusted versions of the strongest models.

At minimum, keep one clean comparison table with the same metrics for all major candidates.

## What Good Evaluation Looks Like Here
A strong evaluation section in this repo should:
- compare multiple models fairly,
- include imbalance-aware metrics,
- discuss threshold tradeoffs,
- interpret the confusion matrix,
- explain why the final model was selected.

## Suggested `reports/` Outputs
When modeling changes are made, try to keep these artifacts current:
- model comparison table,
- threshold analysis table,
- confusion matrix summary,
- precision-recall or ROC plots if available,
- short experiment notes describing what improved and what did not.
