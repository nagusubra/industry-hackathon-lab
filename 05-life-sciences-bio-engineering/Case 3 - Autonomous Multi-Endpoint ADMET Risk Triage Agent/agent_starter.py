#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 5 Starter Agent
Case: Autonomous Multi-Endpoint ADMET Risk Triage Agent
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ENDPOINTS = ("clintox", "sider", "herg")


def synthesize_admet_table(path: Path, n: int = 300) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(33)
    rows = []
    for i in range(n):
        fps = rng.integers(0, 2, size=24)
        compound_id = f"CMPD_{i:04d}"
        for ep_idx, endpoint in enumerate(ENDPOINTS):
            # Endpoint-specific latent rules on shared fingerprint
            logits = fps[ep_idx * 4 : (ep_idx + 1) * 4].sum() + rng.normal(0, 0.4)
            activity = int(logits > 1.2)
            rows.append(
                {
                    "compound_id": compound_id,
                    "smiles": "CCO",
                    "endpoint": endpoint,
                    "activity": activity,
                    **{f"fp_{j}": int(fps[j]) for j in range(24)},
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote toy multi-endpoint ADMET table to {path}")
    return df


def perceive(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return synthesize_admet_table(path)


def featurize(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    fp_cols = [c for c in df.columns if c.startswith("fp_")]
    if not fp_cols:
        raise ValueError("Expected fp_* columns (toy fingerprints) or extend with RDKit.")
    return df[fp_cols].to_numpy(), fp_cols


def reason_train_per_endpoint(df: pd.DataFrame, labeled_mask: pd.Series) -> dict[str, tuple]:
    X_all, fp_cols = featurize(df)
    models: dict[str, tuple] = {}
    for endpoint in ENDPOINTS:
        mask = (df["endpoint"] == endpoint) & labeled_mask
        sub = df.loc[mask]
        if len(sub) < 10 or sub["activity"].nunique() < 2:
            continue
        X = sub[fp_cols].to_numpy()
        y = sub["activity"].to_numpy()
        stratify = y if len(y) >= 8 and np.min(np.bincount(y)) >= 2 else None
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=stratify)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(Xtr, ytr)
        proba = model.predict_proba(Xte)[:, 1]
        auroc = float(roc_auc_score(yte, proba)) if len(np.unique(yte)) > 1 else float("nan")
        models[endpoint] = (model, {"auroc": auroc, "n_train": len(Xtr)})
    return models


def act_endpoint_acquisition(
    df: pd.DataFrame,
    models: dict[str, tuple],
    labeled_mask: pd.Series,
    batch: int = 9,
) -> list[tuple[str, str]]:
    """Pick compound–endpoint pairs with highest prediction uncertainty."""
    X_all, fp_cols = featurize(df)
    candidates: list[tuple[float, str, str]] = []
    for idx, row in df.loc[~labeled_mask].iterrows():
        endpoint = str(row["endpoint"])
        if endpoint not in models:
            continue
        model, _ = models[endpoint]
        x = row[fp_cols].to_numpy().reshape(1, -1)
        proba = model.predict_proba(x)[0, 1]
        uncertainty = abs(proba - 0.5)
        candidates.append((uncertainty, str(row["compound_id"]), endpoint))
    candidates.sort(key=lambda t: t[0])
    return [(cid, ep) for _, cid, ep in candidates[:batch]]


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    labeled = pd.Series(False, index=df.index)
    # Seed: first 60 rows (20 compounds × 3 endpoints)
    labeled.iloc[:60] = True
    for i in range(1, iters + 1):
        models = reason_train_per_endpoint(df, labeled)
        metrics = {ep: m[1] for ep, m in models.items()}
        pairs = act_endpoint_acquisition(df, models, labeled)
        for compound_id, endpoint in pairs:
            hit = (df["compound_id"] == compound_id) & (df["endpoint"] == endpoint)
            labeled.loc[hit] = True
        print(
            f"=== iteration {i} === endpoint_metrics={metrics} "
            f"acquired={pairs[:5]} ... labeled={int(labeled.sum())}"
        )
    print("TODO: load ClinTox / SIDER / hERG via PyTDC or HuggingFace (see data/README.md).")
    print("TODO: replace toy fingerprints with RDKit Morgan FPs on real SMILES.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 5 multi-endpoint ADMET triage starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "toy_admet_multiendpoint.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)


if __name__ == "__main__":
    main()
