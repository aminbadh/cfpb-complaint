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
Describe the business and regulatory context of CFPB complaints.

## Data Source
- Source: CFPB Consumer Complaint Database
- Link: https://www.consumerfinance.gov/data-research/consumer-complaints/
- File used in project: `data/processed/complaints_sample.csv`

## Unit of Observation
Explain what one row represents.

## Main Variables
Summarize key variables used in EDA and modeling.

# Problem Statement

## Problem to Study
State the analytical problem clearly.

## Objective
Define the objective of the analysis.

## Research Questions
List the main research questions.

## Target Variable
Explain the binary target design (monetary relief vs no monetary relief) and leakage-safe constraints.

# Data Preparation

## Missing Values
Explain handling strategy and justification.

## Outliers and Quality Checks
Describe checks and decisions.

## Feature Transformations
Detail text cleaning, vectorization, and any transformations.

## Encoding and Scaling
Document categorical encoding and scaling choices.

## Feature Selection and Leakage Control
List excluded post-resolution fields and explain why.

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
