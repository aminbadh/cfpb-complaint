---
lang: en
numbersections: true
fontsize: 11pt
linestretch: 1.2
geometry: a4paper,margin=2.2cm
header-includes:
  - |
    \usepackage{setspace}
  - |
    \usepackage{titlesec}
  - |
    \setlength{\parskip}{6pt}
    \setlength{\parindent}{0pt}
---

\pagenumbering{gobble}
\pagestyle{empty}

\begin{center}
\vspace*{\fill}
{\huge \textbf{Data Mining Project Report}}\\

\vspace*{\fill}
{\LARGE \textbf{Title}}\\[0.25cm]
{\Large CFPB Consumer Complaints: Predicting Monetary Relief Outcomes from Complaint-Time Information}\\

\vspace*{\fill}
{\LARGE \textbf{Names}}\\[0.25cm]
{\large Amin Ben Abdelhafidh}\\
{\large Koussay Hidouri}\\
{\large Louay Ilahi}\\

\vspace*{\fill}
{\LARGE \textbf{Course Title}}\\[0.25cm]
{\Large BA 360: Business Data Mining}\\
\vspace*{\fill}
\end{center}

\newpage
\tableofcontents
\newpage
\pagenumbering{arabic}
\pagestyle{plain}

# Dataset Description

## General Context
The dataset comes from the U.S. Consumer Financial Protection Bureau (CFPB). It contains real consumer complaints about financial products and services (for example credit cards, loans, credit reporting, and debt collection). In business terms, this dataset helps identify where customer harm occurs and where monetary relief is more likely, which supports better risk monitoring and faster case prioritization.

## Data Source

- Source: CFPB Consumer Complaint Database.
- Official page: https://www.consumerfinance.gov/data-research/consumer-complaints/
- Direct file used as full raw input in this project: data/raw/complaints.csv.
- Because the full file is very large, we created and used a memory-safe working sample for modeling: data/processed/complaints_sample.csv.

Local snapshot (as documented in the project README on 2026-04-20):

- Full raw dataset size: 14,636,145 rows and 18 columns.
- Uncompressed CSV size: about 8.0 GB.
- Compressed download size (complaints.csv.zip): about 1.7 GB.

## Unit of Observation
One observation (one row) represents one consumer complaint submitted to the CFPB complaint system. Each row includes complaint metadata available at intake time (for example product, issue, submission channel, state, and dates), and in many cases a free-text complaint narrative.

For this project, we defined a binary target from resolution information:

- 1: complaint ended with monetary relief.
- 0: complaint ended without monetary relief.

To avoid leakage, post-resolution fields are not used as predictors at inference time.

## Main Variables
Main variables used in EDA and modeling include:

- Text variable: consumer_complaint_narrative.
- Product taxonomy: product and sub_product.
- Problem taxonomy: issue and sub_issue.
- Submission and geography: submitted_via and state.
- Time variables: date_received (and derived temporal features).
- Target construction fields: company_response_to_consumer (used to derive the label, then excluded from predictor set for leakage-safe modeling).

Data handling note: because the full dataset in data/raw/complaints.csv is too large for efficient iterative experimentation on a local machine, we generated a representative sample (data/processed/complaints_sample.csv) and used that sample throughout preprocessing and model development.

# Problem Statement

## Problem to Study
Financial institutions and regulators receive a very large volume of consumer complaints, but only a subset of cases ends with monetary relief for the consumer. The core problem is to identify, as early as possible, which complaints are more likely to lead to monetary relief using only information available at complaint time.

This is a pressing business problem for companies because slow or inaccurate complaint triage increases regulatory exposure, operational costs, customer dissatisfaction, and reputational risk. In practice, firms must quickly decide which complaints need urgent escalation versus standard handling. A reliable predictive signal can improve response prioritization, shorten time-to-resolution for high-risk cases, and support more consistent consumer-outcome management.

## Objective
The objective of this analysis is to build and evaluate a leakage-safe binary classification model that predicts whether a CFPB complaint will end with monetary relief. We aim to compare multiple modeling approaches, assess class-imbalance-aware performance metrics, and identify a practical decision threshold for operational use.

## Research Questions
The main research questions are:

- Can complaint-time features (text narrative, product/issue categories, channel, geography, and time features) predict monetary relief outcomes with useful accuracy?
- Which model family provides the best trade-off between precision, recall, and overall robustness for this imbalanced classification task?
- How should the decision threshold be adjusted to match operational priorities, such as capturing more potential monetary-relief cases versus reducing false alarms?
- Which complaint attributes appear most informative for distinguishing likely monetary-relief outcomes?

## Target Variable
The target variable is a binary label derived from the complaint resolution outcome:

- 1: complaint ended with monetary relief.
- 0: complaint ended without monetary relief.

To preserve real-world validity, predictors are restricted to complaint-time information only. Fields that reveal or are strongly tied to post-resolution outcomes are excluded from the feature set used at inference time.

# Data Preparation

## Missing Values
Missing values were handled according to variable type and modeling role. For text, missing complaint narratives were converted to empty strings so every observation could be processed consistently by text cleaning and vectorization steps. For numeric fields, missing values were imputed conservatively (for example with zeros for engineered count-like features where zero has a meaningful baseline). For categorical fields, missing values were retained as explicit categories where appropriate during encoding so missingness information was not silently discarded. This strategy avoids unnecessary row loss, keeps preprocessing deterministic, and is computationally safe on large samples.

## Outliers and Quality Checks
Quality checks focused on label validity, missingness patterns, and basic distribution sanity checks rather than aggressive outlier deletion. We first reviewed the response-status distribution and identified that several statuses were unresolved or ambiguous from a monetary-relief perspective. Because the project objective is supervised prediction of monetary relief, label clarity was prioritized over maximizing row count. We also checked narrative availability and feature completeness to confirm that model inputs remained usable after filtering.

## Label Definition and Eligibility Policy
The target is intentionally strict to reduce label noise:

- Positive class (1): Closed with monetary relief.
- Negative class (0): Closed with explanation, Closed with non-monetary relief, Closed without relief, and Closed.
- Excluded from supervised labeling: unresolved or ambiguous statuses such as In progress, Untimely response, missing response, and other unclear variants (for example Closed with relief).

This rule ensures that class 0 means a clearly closed non-monetary outcome, rather than a mixture of unresolved and resolved cases. The trade-off is fewer training rows, but substantially cleaner supervision, which is more important in an already imbalanced task.

## Feature Transformations
Narrative text was cleaned with a reproducible pipeline: lowercasing, URL removal, email removal, repeated redaction token cleanup, and whitespace normalization. We engineered narrative-length and narrative-presence indicators to capture useful signal even when text quality varies. Date fields were parsed into temporal features (year, month, quarter, and processing-delay proxies) to capture seasonality and operational timing effects.

## Encoding and Scaling
Structured categorical fields were one-hot encoded to support linear and tree-based learners without imposing ordinal assumptions. Text features were represented with TF-IDF for sparse high-dimensional signal extraction. For distance-sensitive models (for example KNN), dimensionality reduction and compatible scaling were used in the modeling notebook to keep computation stable and reduce noise from sparse text spaces.

## Feature Selection and Leakage Control
Leakage prevention was a hard constraint. Any post-resolution field, especially Company response to consumer, was used only to construct the target and then excluded from predictors. Models were trained only on complaint-time information (narrative, product/issue taxonomy, channel, geography, and intake-time-derived temporal features). This preserves real-world deployability because the same information is available at prediction time.

# Methods and Analysis

## Modeling Strategy
Explain train/test setup and model comparison approach.

## Models Implemented
- Logistic Regression (TF-IDF)
- Naive Bayes (TF-IDF)
- KNN (SVD-reduced text)
- Random Forest (structured + text)
- MLP Neural Network
- Voting Classifier Ensemble

## Why These Methods
Justify method choices for this problem.

# Results and Interpretation

## Model Comparison
Insert summary table from reports outputs.

![Model comparison table figure](assets/model_comparison.png)

## Threshold Analysis
Discuss trade-offs and operational threshold recommendation.

![Threshold analysis](assets/threshold_analysis.png)

## Confusion Matrix Insights
Interpret false positives and false negatives in business terms.

![Confusion matrix](assets/confusion_matrix.png)

## Key Findings
Provide clear, practical conclusions.

# Conclusion

## Objective Recap
Summarize initial objective.

## Methods Recap
Summarize methods used.

## Main Results
Summarize strongest findings and selected model.

## Business Insights
Summarize actionable recommendations.

# Appendix (Optional)

## Evolution and Corrections
Reference the mistakes-to-improvements timeline.

## Additional Tables
Add detailed model metrics if needed.
