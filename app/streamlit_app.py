"""Interactive model tuning demo for CFPB monetary-relief prediction.

This app is presentation-oriented: it retrains selected models on sampled data
and shows how hyperparameters + decision threshold shift precision/recall tradeoffs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "processed" / "train_features.csv"
TEST_PATH = ROOT / "data" / "processed" / "test_features.csv"


@dataclass
class ExperimentResult:
    metrics: dict
    sweep_df: pd.DataFrame
    y_test: np.ndarray
    y_proba: np.ndarray
    threshold: float
    train_rows: int
    test_rows: int
    positive_rate: float
    runtime_sec: float


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not TRAIN_PATH.exists() or not TEST_PATH.exists():
        raise FileNotFoundError(
            "Processed feature files are missing. Run notebooks/02_preprocessing.ipynb first."
        )
    return pd.read_csv(TRAIN_PATH), pd.read_csv(TEST_PATH)


def stratified_sample(df: pd.DataFrame, frac: float, random_state: int) -> pd.DataFrame:
    if frac >= 1.0:
        return df.copy()
    sampled, _ = train_test_split(
        df,
        train_size=frac,
        random_state=random_state,
        stratify=df["target"],
    )
    return sampled.reset_index(drop=True)


def evaluate_probs(y_true: np.ndarray, y_proba: np.ndarray, threshold: float) -> dict:
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    return {
        "Threshold": float(threshold),
        "Accuracy": accuracy_score(y_true, y_pred),
        "Balanced Accuracy": balanced_accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "Kappa": cohen_kappa_score(y_true, y_pred),
        "ROC-AUC": roc_auc_score(y_true, y_proba),
        "PR-AUC": average_precision_score(y_true, y_proba),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp),
    }


@st.cache_data(show_spinner=False)
def run_experiment(
    model_name: str,
    sample_frac: float,
    random_state: int,
    threshold: float,
    tfidf_max_features: int,
    lr_c: float,
    lr_class_weight: str,
    rf_n_estimators: int,
    rf_max_depth: int,
    rf_min_samples_leaf: int,
    rf_class_weight: str,
    rf_text_feature_cap: int,
    nb_alpha: float,
    knn_neighbors: int,
    knn_weights: str,
    svd_components: int,
    ann_h1: int,
    ann_h2: int,
    ann_h3: int,
    ann_max_iter: int,
    ann_learning_rate_init: float,
) -> ExperimentResult:
    start = time.time()
    train_df, test_df = load_data()
    train_df = stratified_sample(train_df, sample_frac, random_state)
    test_df = stratified_sample(test_df, sample_frac, random_state)

    y_train = train_df["target"].to_numpy()
    y_test = test_df["target"].to_numpy()

    x_train = train_df.drop(columns=["target"])
    x_test = test_df.drop(columns=["target"])

    narratives_train = x_train["narrative_clean"].fillna("")
    narratives_test = x_test["narrative_clean"].fillna("")

    tfidf = TfidfVectorizer(max_features=tfidf_max_features, max_df=0.8, min_df=2, ngram_range=(1, 2))
    x_train_tfidf = tfidf.fit_transform(narratives_train)
    x_test_tfidf = tfidf.transform(narratives_test)

    x_train_struct = x_train.drop(columns=["narrative_clean"])
    x_test_struct = x_test.drop(columns=["narrative_clean"])
    scaler = StandardScaler()
    x_train_struct_scaled = scaler.fit_transform(x_train_struct)
    x_test_struct_scaled = scaler.transform(x_test_struct)

    class_weight_lr = None if lr_class_weight == "None" else "balanced"
    class_weight_rf = None if rf_class_weight == "None" else "balanced"

    text_cap = max(10, min(rf_text_feature_cap, tfidf_max_features))
    x_train_combined = None
    x_test_combined = None

    def get_combined_features():
        nonlocal x_train_combined, x_test_combined
        if x_train_combined is None or x_test_combined is None:
            x_train_combined = np.hstack([x_train_struct_scaled, x_train_tfidf.toarray()[:, :text_cap]])
            x_test_combined = np.hstack([x_test_struct_scaled, x_test_tfidf.toarray()[:, :text_cap]])
        return x_train_combined, x_test_combined

    if model_name == "Logistic Regression":
        model = LogisticRegression(C=lr_c, class_weight=class_weight_lr, max_iter=1000, random_state=42)
        model.fit(x_train_tfidf, y_train)
        y_proba = model.predict_proba(x_test_tfidf)[:, 1]

    elif model_name == "Naive Bayes":
        model = MultinomialNB(alpha=nb_alpha)
        model.fit(x_train_tfidf, y_train)
        y_proba = model.predict_proba(x_test_tfidf)[:, 1]

    elif model_name == "KNN":
        max_svd = max(2, min(svd_components, x_train_tfidf.shape[1] - 1))
        svd = TruncatedSVD(n_components=max_svd, random_state=42)
        x_train_svd = svd.fit_transform(x_train_tfidf)
        x_test_svd = svd.transform(x_test_tfidf)
        model = KNeighborsClassifier(n_neighbors=knn_neighbors, weights=knn_weights, n_jobs=-1)
        model.fit(x_train_svd, y_train)
        y_proba = model.predict_proba(x_test_svd)[:, 1]

    elif model_name == "Random Forest":
        x_train_combined, x_test_combined = get_combined_features()

        model = RandomForestClassifier(
            n_estimators=rf_n_estimators,
            max_depth=rf_max_depth if rf_max_depth > 0 else None,
            min_samples_leaf=rf_min_samples_leaf,
            class_weight=class_weight_rf,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(x_train_combined, y_train)
        y_proba = model.predict_proba(x_test_combined)[:, 1]

    elif model_name == "Neural Network (ANN)":
        x_train_combined, x_test_combined = get_combined_features()
        model = MLPClassifier(
            hidden_layer_sizes=(ann_h1, ann_h2, ann_h3),
            activation="relu",
            solver="adam",
            max_iter=ann_max_iter,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            learning_rate_init=ann_learning_rate_init,
        )
        model.fit(x_train_combined, y_train)
        y_proba = model.predict_proba(x_test_combined)[:, 1]

    else:
        # Voting Ensemble (5-model avg) to match notebook setup.
        x_train_combined, x_test_combined = get_combined_features()
        max_svd = max(2, min(svd_components, x_train_tfidf.shape[1] - 1))
        svd = TruncatedSVD(n_components=max_svd, random_state=42)
        x_train_svd = svd.fit_transform(x_train_tfidf)
        x_test_svd = svd.transform(x_test_tfidf)

        lr = LogisticRegression(C=lr_c, class_weight=class_weight_lr, max_iter=1000, random_state=42)
        nb = MultinomialNB(alpha=nb_alpha)
        knn = KNeighborsClassifier(n_neighbors=knn_neighbors, weights=knn_weights, n_jobs=-1)
        rf = RandomForestClassifier(
            n_estimators=rf_n_estimators,
            max_depth=rf_max_depth if rf_max_depth > 0 else None,
            min_samples_leaf=rf_min_samples_leaf,
            class_weight=class_weight_rf,
            random_state=42,
            n_jobs=-1,
        )
        ann = MLPClassifier(
            hidden_layer_sizes=(ann_h1, ann_h2, ann_h3),
            activation="relu",
            solver="adam",
            max_iter=ann_max_iter,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            learning_rate_init=ann_learning_rate_init,
        )

        lr.fit(x_train_tfidf, y_train)
        nb.fit(x_train_tfidf, y_train)
        knn.fit(x_train_svd, y_train)
        rf.fit(x_train_combined, y_train)
        ann.fit(x_train_combined, y_train)

        y_proba = (
            lr.predict_proba(x_test_tfidf)[:, 1]
            + nb.predict_proba(x_test_tfidf)[:, 1]
            + knn.predict_proba(x_test_svd)[:, 1]
            + rf.predict_proba(x_test_combined)[:, 1]
            + ann.predict_proba(x_test_combined)[:, 1]
        ) / 5.0

    metrics = evaluate_probs(y_test, y_proba, threshold)

    thresholds = np.round(np.arange(0.10, 0.91, 0.05), 2)
    sweep_rows = []
    for thr in thresholds:
        row = evaluate_probs(y_test, y_proba, float(thr))
        row["Model"] = model_name
        sweep_rows.append(row)

    sweep_df = pd.DataFrame(sweep_rows)

    return ExperimentResult(
        metrics=metrics,
        sweep_df=sweep_df,
        y_test=y_test,
        y_proba=y_proba,
        threshold=threshold,
        train_rows=len(train_df),
        test_rows=len(test_df),
        positive_rate=float(np.mean(y_test)),
        runtime_sec=time.time() - start,
    )


def plot_confusion(y_true: np.ndarray, y_proba: np.ndarray, threshold: float):
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    cm = np.array([[tn, fp], [fn, tp]])
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Pred 0", "Pred 1"],
        yticklabels=["Actual 0", "Actual 1"],
        ax=ax,
    )
    ax.set_title(f"Confusion Matrix (thr={threshold:.2f})")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    return fig


def plot_threshold_sweep(sweep_df: pd.DataFrame, selected_threshold: float):
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(sweep_df["Threshold"], sweep_df["F1"], marker="o", label="F1")
    ax.plot(sweep_df["Threshold"], sweep_df["Precision"], marker="o", label="Precision")
    ax.plot(sweep_df["Threshold"], sweep_df["Recall"], marker="o", label="Recall")
    ax.axvline(selected_threshold, color="black", linestyle="--", linewidth=1, label=f"Selected={selected_threshold:.2f}")
    ax.set_title("Threshold Sweep")
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.25)
    ax.legend()
    return fig


def main() -> None:
    st.set_page_config(page_title="CFPB Model Tuning Demo", layout="wide")
    st.title("CFPB Monetary Relief: Interactive Model Tuning")
    st.caption(
        "Class demo app: retrain quickly on sampled data, tune hyperparameters, and inspect threshold tradeoffs."
    )

    with st.sidebar:
        st.header("Controls")
        model_name = st.selectbox(
            "Model",
            [
                "Logistic Regression",
                "Naive Bayes",
                "KNN",
                "Random Forest",
                "Neural Network (ANN)",
                "Voting Ensemble (5-model avg)",
            ],
            index=3,
        )
        sample_frac = st.slider("Train/Test sample fraction", 0.10, 1.00, 0.40, 0.05)
        threshold = st.slider("Decision threshold", 0.10, 0.90, 0.10, 0.05)
        random_state = st.number_input("Random state", min_value=1, max_value=9999, value=42, step=1)

        st.markdown("---")
        st.subheader("Shared Text Features")
        tfidf_max_features = st.slider("TF-IDF max features", 100, 1000, 300, 50)

        # Default values keep run_experiment signature stable for caching.
        lr_c = 1.0
        lr_class_weight = "balanced"
        nb_alpha = 0.1
        knn_neighbors = 5
        knn_weights = "uniform"
        svd_components = 50
        rf_n_estimators = 150
        rf_max_depth = 15
        rf_min_samples_leaf = 1
        rf_class_weight = "balanced"
        rf_text_feature_cap = 100
        ann_h1 = 128
        ann_h2 = 64
        ann_h3 = 32
        ann_max_iter = 400
        ann_learning_rate_init = 0.001

        if model_name in ["Logistic Regression", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("Logistic Regression")
            lr_c = st.select_slider("C (inverse regularization)", options=[0.1, 0.3, 1.0, 3.0, 10.0], value=1.0)
            lr_class_weight = st.selectbox("LR class_weight", ["None", "balanced"], index=1)

        if model_name in ["Naive Bayes", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("Naive Bayes")
            nb_alpha = st.select_slider("alpha (smoothing)", options=[0.01, 0.05, 0.1, 0.5, 1.0], value=0.1)

        if model_name in ["KNN", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("KNN")
            knn_neighbors = st.slider("n_neighbors", 3, 21, 5, 2)
            knn_weights = st.selectbox("weights", ["uniform", "distance"], index=0)
            svd_components = st.slider("SVD components", 10, 120, 50, 5)

        if model_name in ["Random Forest", "Neural Network (ANN)", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("Structured + Text Mix")
            rf_text_feature_cap = st.slider("Text features added to combined models", 20, 300, 100, 10)

        if model_name in ["Random Forest", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("Random Forest")
            rf_n_estimators = st.slider("n_estimators", 50, 400, 150, 25)
            rf_max_depth = st.slider("max_depth (0=None)", 0, 30, 15, 1)
            rf_min_samples_leaf = st.slider("min_samples_leaf", 1, 10, 1, 1)
            rf_class_weight = st.selectbox("RF class_weight", ["None", "balanced"], index=1)

        if model_name in ["Neural Network (ANN)", "Voting Ensemble (5-model avg)"]:
            st.markdown("---")
            st.subheader("Neural Network (ANN)")
            ann_h1 = st.slider("hidden layer 1", 32, 256, 128, 16)
            ann_h2 = st.slider("hidden layer 2", 16, 128, 64, 8)
            ann_h3 = st.slider("hidden layer 3", 8, 64, 32, 8)
            ann_max_iter = st.slider("max_iter", 100, 600, 400, 50)
            ann_learning_rate_init = st.select_slider(
                "learning_rate_init",
                options=[0.0005, 0.001, 0.002, 0.005],
                value=0.001,
            )

    run = st.button("Train / Refresh", type="primary")

    if "auto_ran" not in st.session_state:
        st.session_state.auto_ran = True
        run = True

    if not run:
        st.info("Change controls and click 'Train / Refresh'.")
        return

    with st.spinner("Training model and computing metrics..."):
        result = run_experiment(
            model_name=model_name,
            sample_frac=sample_frac,
            random_state=int(random_state),
            threshold=threshold,
            tfidf_max_features=tfidf_max_features,
            lr_c=lr_c,
            lr_class_weight=lr_class_weight,
            rf_n_estimators=rf_n_estimators,
            rf_max_depth=rf_max_depth,
            rf_min_samples_leaf=rf_min_samples_leaf,
            rf_class_weight=rf_class_weight,
            rf_text_feature_cap=rf_text_feature_cap,
            nb_alpha=nb_alpha,
            knn_neighbors=knn_neighbors,
            knn_weights=knn_weights,
            svd_components=svd_components,
            ann_h1=ann_h1,
            ann_h2=ann_h2,
            ann_h3=ann_h3,
            ann_max_iter=ann_max_iter,
            ann_learning_rate_init=ann_learning_rate_init,
        )

    st.success(f"Completed in {result.runtime_sec:.2f}s")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("F1", f"{result.metrics['F1']:.4f}")
    c2.metric("Precision", f"{result.metrics['Precision']:.4f}")
    c3.metric("Recall", f"{result.metrics['Recall']:.4f}")
    c4.metric("PR-AUC", f"{result.metrics['PR-AUC']:.4f}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Kappa", f"{result.metrics['Kappa']:.4f}")
    c6.metric("ROC-AUC", f"{result.metrics['ROC-AUC']:.4f}")
    c7.metric("Test Positive Rate", f"{result.positive_rate:.2%}")
    c8.metric("No-skill Precision", f"{result.positive_rate:.4f}")

    st.write(
        f"Rows used: train={result.train_rows:,}, test={result.test_rows:,} | model={model_name} | threshold={result.threshold:.2f}"
    )

    left, right = st.columns([1, 1.2])
    with left:
        st.pyplot(plot_confusion(result.y_test, result.y_proba, result.threshold), clear_figure=True)
    with right:
        st.pyplot(plot_threshold_sweep(result.sweep_df, result.threshold), clear_figure=True)

    st.subheader("Threshold Sweep Table")
    view_cols = [
        "Threshold",
        "F1",
        "Precision",
        "Recall",
        "Kappa",
        "PR-AUC",
        "ROC-AUC",
        "TN",
        "FP",
        "FN",
        "TP",
    ]
    st.dataframe(result.sweep_df[view_cols].round(4), width="stretch")


if __name__ == "__main__":
    main()
