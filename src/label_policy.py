"""Shared label policy for CFPB monetary-relief classification.

This module centralizes how company response values are normalized and mapped
into policy groups so notebooks can stay DRY and consistent.
"""

from __future__ import annotations

import pandas as pd

POSITIVE_RESPONSE = "closed with monetary relief"
NEGATIVE_RESPONSES = {
    "closed with explanation",
    "closed with non-monetary relief",
    "closed without relief",
    "closed",
}


def normalize_response_series(response_series: pd.Series) -> pd.Series:
    """Return normalized response text used by labeling policy."""
    return response_series.fillna("").astype(str).str.strip().str.lower()


def classify_response_policy(response_series: pd.Series) -> pd.DataFrame:
    """Classify each response into positive, negative, or excluded policy groups."""
    normalized = normalize_response_series(response_series)

    policy_group = pd.Series(
        "excluded_ambiguous_or_unresolved",
        index=normalized.index,
        dtype="object",
    )
    policy_group.loc[normalized == POSITIVE_RESPONSE] = "positive_monetary"
    policy_group.loc[normalized.isin(NEGATIVE_RESPONSES)] = "negative_non_monetary"

    eligible_for_supervised_label = policy_group != "excluded_ambiguous_or_unresolved"
    target_if_eligible = (policy_group == "positive_monetary").astype(int)

    return pd.DataFrame(
        {
            "response_normalized": normalized,
            "policy_group": policy_group,
            "eligible_for_supervised_label": eligible_for_supervised_label,
            "target_if_eligible": target_if_eligible,
        }
    )


def build_supervised_target(response_series: pd.Series) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """Return eligible mask, target labels for eligible rows, and policy table."""
    policy_df = classify_response_policy(response_series)
    eligible_mask = policy_df["eligible_for_supervised_label"]
    target = policy_df.loc[eligible_mask, "target_if_eligible"].astype(int)
    return eligible_mask, target, policy_df
