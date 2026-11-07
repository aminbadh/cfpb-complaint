# Retrieval extension: CFPB complaint search

Individual extension to the group project, by Louay Ilahi. It adds a retrieval and evaluation experiment on the CFPB complaint narratives and does not change any existing project code.

## Goal
Compare three ways of finding similar complaints: a TF-IDF baseline, sentence embeddings, and a hybrid of both.

## Data
5,000 narratives randomly sampled (seed 42) from `data/processed/complaints_sample.csv` in this repo. Rows without a narrative are dropped.

## Method
- **Embeddings:** `all-MiniLM-L6-v2` (sentence-transformers), normalized vectors, FAISS inner-product index.
- **Baseline:** TF-IDF (English stop words, sublinear TF) with cosine similarity.
- **Hybrid:** weighted average of z-scored embedding and TF-IDF similarities, `a * emb + (1 - a) * tfidf`.

## Evaluation
- A retrieved complaint counts as relevant if it has the same `Issue` label as the query complaint. This is an automatic proxy, not a human judgement.
- Metrics: Hit@k, Precision@k and MRR, with the query excluded from its own results.
- The hybrid weight `a` was tuned on one half of the test queries and scored on the other half.
- Differences were assessed with a 5,000-sample bootstrap on the held-out half.

## Results (1,500 held-out queries)
| Method | MRR |
|---|---|
| TF-IDF | 0.556 |
| Embeddings (MiniLM) | 0.586 |
| Hybrid (a = 0.7) | 0.586 |

- Embeddings vs TF-IDF: +0.031 MRR, 95% bootstrap CI [0.013, 0.048].
- Hybrid vs embeddings: no measurable difference, 95% CI [-0.015, 0.014].

Conclusion: on this dataset, embeddings outperform TF-IDF, and combining the two does not add a gain. A first run with 250 held-out queries gave an interval that included zero, so the larger run was used.

## Limitations
- Relevance labels are the `Issue` categories, which are coarse and partly keyword-driven.
- One dataset and one sample of 5,000 narratives.
- MiniLM reads only the first ~256 tokens of long narratives.

## How to run
`pip install -r requirements.txt`, then open the notebook and run all cells (encoding takes about 10 minutes on a CPU).
