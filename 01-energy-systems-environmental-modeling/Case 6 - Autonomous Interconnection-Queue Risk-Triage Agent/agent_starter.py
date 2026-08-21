#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Interconnection-Queue Risk-Triage Agent
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Score withdrawal risk, rank a limited study-slot portfolio, evaluate
against historical outcomes, revise ranking weights.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.preprocessing import OneHotEncoder


LOGICAL_COLS = [
    "iso",
    "state",
    "resource",
    "capacity_mw",
    "queue_year",
    "outcome",  # operational | withdrawn | active
]


def _synthesize_queue_demo(path: Path, n: int = 1200, seed: int = 7) -> pd.DataFrame:
    """Labeled synthetic queue — not the LBNL workbook."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    isos = np.array(["PJM", "MISO", "CAISO", "ERCOT", "SPP", "NYISO", "ISONE"])
    resources = np.array(["Solar", "Wind", "Storage", "Gas", "Hybrid"])
    states = np.array(["PA", "IL", "CA", "TX", "KS", "NY", "MA", "OH"])
    iso = rng.choice(isos, n)
    resource = rng.choice(resources, n)
    state = rng.choice(states, n)
    queue_year = rng.integers(2012, 2025, n)
    capacity_mw = np.clip(rng.lognormal(mean=3.8, sigma=1.1, size=n), 5, 2000)

    # Hidden outcome process (agent must infer, not copy this function).
    withdraw_logit = (
        -0.4
        + 0.08 * (2024 - queue_year)
        + 0.35 * (resource == "Solar")
        + 0.25 * (resource == "Storage")
        - 0.9 * (resource == "Gas")
        + 0.0004 * capacity_mw
        + 0.4 * np.isin(iso, ["CAISO", "PJM", "NYISO"])
        + rng.normal(0, 0.5, n)
    )
    p_w = 1 / (1 + np.exp(-withdraw_logit))
    withdrawn = rng.random(n) < p_w
    still_active = (~withdrawn) & (queue_year >= 2022) & (rng.random(n) < 0.35)
    outcome = np.where(withdrawn, "withdrawn", np.where(still_active, "active", "operational"))

    df = pd.DataFrame(
        {
            "iso": iso,
            "state": state,
            "resource": resource,
            "capacity_mw": capacity_mw,
            "queue_year": queue_year,
            "outcome": outcome,
        }
    )
    df.to_csv(path, index=False)
    print(f"[warn] Synthetic demo written to {path} — not LBNL Queued Up. Download the xlsx for scoring.")
    return df


def _normalize_workbook(df: pd.DataFrame) -> pd.DataFrame:
    """Best-effort map of common Queued Up column names → logical fields."""
    lower = {c.lower().strip(): c for c in df.columns}

    def pick(*cands: str) -> str | None:
        for cand in cands:
            if cand in lower:
                return lower[cand]
        for key, orig in lower.items():
            if any(cand in key for cand in cands):
                return orig
        return None

    iso_c = pick("iso", "ba", "entity", "balancing area", "region")
    state_c = pick("state")
    res_c = pick("resource", "type1", "fuel", "technology", "type")
    mw_c = pick("capacity_mw", "mw_1", "mw1", "q_mw", "capacity")
    year_c = pick("queue_year", "ir_year", "year_entered", "q_year")
    date_c = pick("queue_date", "ir_date", "date_proposed", "received")
    status_c = pick("status", "outcome", "q_status")

    out = pd.DataFrame()
    out["iso"] = df[iso_c].astype(str) if iso_c else "unknown"
    out["state"] = df[state_c].astype(str) if state_c else "NA"
    out["resource"] = df[res_c].astype(str) if res_c else "Unknown"
    out["capacity_mw"] = pd.to_numeric(df[mw_c], errors="coerce") if mw_c else 50.0
    if year_c:
        out["queue_year"] = pd.to_numeric(df[year_c], errors="coerce")
    elif date_c:
        out["queue_year"] = pd.to_datetime(df[date_c], errors="coerce").dt.year
    else:
        out["queue_year"] = np.nan

    status = df[status_c].astype(str).str.lower() if status_c else pd.Series(["active"] * len(df))
    outcome = np.full(len(df), "active", dtype=object)
    outcome = np.where(status.str.contains("withdraw|cancel|termin", regex=True), "withdrawn", outcome)
    outcome = np.where(
        status.str.contains("operat|cod|complete|in service|built", regex=True),
        "operational",
        outcome,
    )
    out["outcome"] = outcome
    return out.dropna(subset=["capacity_mw", "queue_year"])


def perceive(xlsx_path: Path, demo_csv: Path) -> pd.DataFrame:
    if xlsx_path.exists():
        raw = pd.read_excel(xlsx_path, sheet_name=0)
        df = _normalize_workbook(raw)
        print(f"[info] Loaded {len(df)} rows from {xlsx_path}")
        return df
    if demo_csv.exists():
        print(f"[warn] No workbook at {xlsx_path}; using existing {demo_csv}")
        return pd.read_csv(demo_csv)
    return _synthesize_queue_demo(demo_csv)


def _design_matrix(df: pd.DataFrame, encoder: OneHotEncoder | None = None) -> tuple[np.ndarray, OneHotEncoder]:
    cats = df[["iso", "resource"]].astype(str)
    if encoder is None:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        cat_x = encoder.fit_transform(cats)
    else:
        cat_x = encoder.transform(cats)
    num = np.column_stack(
        [
            np.log1p(df["capacity_mw"].to_numpy(dtype=float)),
            df["queue_year"].to_numpy(dtype=float),
        ]
    )
    return np.hstack([num, cat_x]), encoder


def reason(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> dict[str, Any]:
    """Fit P(withdrawn | features known at entry). Active rows excluded from training labels."""
    labeled = train[train["outcome"].isin(["withdrawn", "operational"])].copy()
    y = (labeled["outcome"] == "withdrawn").to_numpy(dtype=int)
    x_train, enc = _design_matrix(labeled)
    model = LogisticRegression(max_iter=400, class_weight="balanced")
    model.fit(x_train, y)
    x_test, _ = _design_matrix(test, encoder=enc)
    p_withdraw = model.predict_proba(x_test)[:, 1]
    return {"model": model, "encoder": enc, "p_withdraw": p_withdraw}


def act(
    test: pd.DataFrame,
    p_withdraw: np.ndarray,
    k_slots: int,
    size_weight: float,
) -> np.ndarray:
    """
    Rank study slots by expected completed MW:
    (1 - P_withdraw) * capacity_mw ** size_weight
    """
    score = (1.0 - p_withdraw) * np.power(np.clip(test["capacity_mw"].to_numpy(dtype=float), 1.0, None), size_weight)
    order = np.argsort(-score)
    return order[:k_slots]


def evaluate(test: pd.DataFrame, p_withdraw: np.ndarray, selected: np.ndarray, k_slots: int) -> dict[str, float]:
    settled = test["outcome"].isin(["withdrawn", "operational"]).to_numpy()
    y = (test["outcome"] == "withdrawn").to_numpy(dtype=int)
    metrics: dict[str, float] = {}
    if settled.sum() >= 20 and len(np.unique(y[settled])) == 2:
        metrics["auroc"] = float(roc_auc_score(y[settled], p_withdraw[settled]))
        metrics["pr_auc"] = float(average_precision_score(y[settled], p_withdraw[settled]))
    else:
        metrics["auroc"] = float("nan")
        metrics["pr_auc"] = float("nan")

    sel = test.iloc[list(selected)]
    completed_mw = float(sel.loc[sel["outcome"] == "operational", "capacity_mw"].sum())
    rng = np.random.default_rng(0)
    rand_idx = rng.choice(len(test), size=min(k_slots, len(test)), replace=False)
    rand_sel = test.iloc[list(rand_idx)]
    random_mw = float(rand_sel.loc[rand_sel["outcome"] == "operational", "capacity_mw"].sum())
    largest = test.sort_values("capacity_mw", ascending=False).head(k_slots)
    largest_mw = float(largest[largest["outcome"] == "operational"]["capacity_mw"].sum())
    metrics["completed_mw_topk"] = completed_mw
    metrics["completed_mw_random"] = random_mw
    metrics["completed_mw_largest"] = largest_mw
    metrics["lift_vs_random"] = completed_mw - random_mw
    return metrics


def run_agent_loop(df: pd.DataFrame, k_slots: int, max_iters: int = 3) -> None:
    df = df.dropna(subset=["queue_year", "capacity_mw"]).copy()
    df["queue_year"] = df["queue_year"].astype(int)
    cutoff = int(df["queue_year"].quantile(0.70))
    train = df[df["queue_year"] <= cutoff]
    test = df[df["queue_year"] > cutoff]
    if len(train) < 50 or len(test) < 20:
        raise ValueError("Not enough rows for a year-based split; download the LBNL workbook.")

    size_weight = 1.0
    for i in range(1, max_iters + 1):
        bundle = reason(train, test)
        selected = act(test, bundle["p_withdraw"], k_slots=k_slots, size_weight=size_weight)
        metrics = evaluate(test, bundle["p_withdraw"], selected, k_slots=k_slots)
        print(f"=== iteration {i} (size_weight={size_weight:.2f}, cutoff_year={cutoff}) ===")
        print("train_n:", len(train), "test_n:", len(test))
        print("metrics:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in metrics.items()})
        if metrics["completed_mw_topk"] + 1e-6 < metrics["completed_mw_largest"]:
            size_weight = min(1.4, size_weight + 0.15)
            print("[revise] trailing largest-MW-first — raising size weight")
        else:
            size_weight = max(0.6, size_weight - 0.1)
            print("[revise] beating largest-MW-first — slightly more risk-aware")
    print("TODO: survival model for months-to-COD; ISO-specific calibrations; ECE plot.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 6 interconnection-queue risk-triage starter agent")
    root = Path(__file__).parent
    parser.add_argument(
        "--xlsx",
        type=Path,
        default=root / "data" / "raw" / "lbnl-queues" / "queued_up_2026.xlsx",
        help="Path to LBNL Queued Up workbook",
    )
    parser.add_argument(
        "--demo-csv",
        type=Path,
        default=root / "data" / "raw" / "lbnl-queues" / "demo_queue.csv",
        help="Synthetic fallback path (written only if xlsx is missing)",
    )
    parser.add_argument("--k-slots", type=int, default=40, help="Study slots in the planner portfolio")
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    df = perceive(args.xlsx, args.demo_csv)
    missing = [c for c in LOGICAL_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns {missing}; see data/README.md codebook mapping.")
    run_agent_loop(df, k_slots=args.k_slots, max_iters=args.iters)


if __name__ == "__main__":
    main()
