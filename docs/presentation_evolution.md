# Presentation Evolution Storyline

Use this to present the project as a rigorous iteration process.

## Slide flow (8 minutes total)

1. Problem and business objective (1-2 min)
2. Data and preprocessing boundary (2 min)
3. What we got wrong and how we fixed it (1 min)
4. Model improvements and final comparison (2 min)
5. Live model run and conclusion (1-2 min)

## Core slide: What we got wrong and how we fixed it

Show one concise table with 3 rows:

| Stage | What was wrong | How we detected it | What we changed | Evidence of improvement |
|---|---|---|---|---|
| Target framing v1 | Initial target framing was inconsistent with deployment-time prediction needs | Metric behavior looked unstable and interpretation was weak | Re-defined target and enforced leakage-safe feature boundary in preprocessing | F1, PR-AUC, and Kappa improved and became more interpretable |
| Evaluation v1 | Relied too much on default threshold and limited metric set | Accuracy looked acceptable but minority-class behavior was poor | Added PR-AUC, Kappa, confusion matrix, and threshold search | Better recall/precision balance at chosen threshold |
| Ensemble v1 | Simple equal-weight average only | Ensemble gains were limited | Added weighted voting and stacking | Higher validation performance and more stable results |

## Evidence slide (before vs after)

Prepare a small table with these columns:
- model_version
- threshold
- f1
- pr_auc
- kappa
- recall
- precision

Keep only 2-4 key rows:
- one early baseline
- one corrected baseline
- final champion

## Speaking script (short)

"We intentionally kept an audit trail of mistakes and corrections. Early in the project, our framing around target and evaluation was not fully aligned with deployment-time prediction quality. We detected this through weak minority-class behavior and unstable interpretation. We corrected the target boundary, expanded evaluation beyond accuracy, and tuned thresholds with cross-validation. This produced a more reliable model and a clearer business decision signal."

## Do and do not

Do:
- Be transparent and specific.
- Quantify improvement with at least 3 metrics.
- Tie every correction to a concrete notebook or report artifact.

Do not:
- Hide early mistakes.
- Claim improvements without numeric evidence.
- Spend too much time on implementation details during the 8-minute talk.

## Files to reference during presentation

- notebooks/02_preprocessing.ipynb
- notebooks/03_modeling.ipynb
- reports/model_comparison_with_ensemble.csv
- reports/model_comparison_detailed.csv
- reports/threshold_analysis.csv
- reports/confusion_matrices.csv
- reports/evolution_log.md
