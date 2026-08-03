#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 5 Starter Agent
Case: Autonomous Protein-Structure-to-Toxicity Screening Agent
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def synthesize_tox_table(path: Path, n: int = 400) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    # Toy fingerprints: 32 random bits as stand-in for Morgan FP
    fps = rng.integers(0, 2, size=(n, 32))
    # Latent toxicity rule: first 5 bits correlated with label
    logits = fps[:, :5].sum(axis=1) + rng.normal(0, 0.5, size=n)
    y = (logits > np.median(logits)).astype(int)
    df = pd.DataFrame(fps, columns=[f"fp_{i}" for i in range(32)])
    df.insert(0, "compound_id", [f"CMPD_{i:04d}" for i in range(n)])
    df["smiles"] = ["CCO"] * n  # placeholder
    df["assay_id"] = "TOY_NR_ASSAY"
    df["activity"] = y
    df.to_csv(path, index=False)
    print(f"[info] Wrote toy Tox21-like table to {path}")
    return df


def perceive(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return synthesize_tox_table(path)


def fetch_pdb_header(pdb_id: str = "1A3N") -> str:
    """Lightweight structure-context fetch (PDB header via RCSB)."""
    url = f"https://files.rcsb.org/header/{pdb_id}.pdb"
    try:
        r = requests.get(url, timeout=20)
        if r.ok:
            lines = r.text.splitlines()[:5]
            return " | ".join(lines)
    except requests.RequestException as exc:
        return f"PDB fetch failed: {exc}"
    return "PDB fetch failed"


def featurize(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    fp_cols = [c for c in df.columns if c.startswith("fp_")]
    if not fp_cols:
        raise ValueError("Expected fp_* columns (toy fingerprints) or extend with RDKit.")
    X = df[fp_cols].to_numpy()
    y = df["activity"].to_numpy()
    ids = df["compound_id"].astype(str).tolist()
    return X, y, ids


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(Xtr, ytr)
    proba = model.predict_proba(Xte)[:, 1]
    auroc = float(roc_auc_score(yte, proba)) if len(np.unique(yte)) > 1 else float("nan")
    return model, {"auroc": auroc, "n_train": len(Xtr), "n_test": len(Xte)}


def act_active_learning(model, X: np.ndarray, ids: list[str], batch: int = 10) -> list[str]:
    proba = model.predict_proba(X)[:, 1]
    uncertainty = np.abs(proba - 0.5)  # lower = more uncertain
    pick = np.argsort(uncertainty)[:batch]
    return [ids[i] for i in pick]


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    print("structure_context:", fetch_pdb_header("1A3N"))
    X, y, ids = featurize(df)
    labeled = np.zeros(len(y), dtype=bool)
    # seed labels
    labeled[:40] = True
    for i in range(1, iters + 1):
        model, metrics = reason_train(X[labeled], y[labeled])
        query_ids = act_active_learning(model, X[~labeled], [ids[j] for j in range(len(ids)) if not labeled[j]])
        # Virtual wet-lab: reveal labels for queried IDs
        id_to_idx = {cid: k for k, cid in enumerate(ids)}
        for cid in query_ids:
            labeled[id_to_idx[cid]] = True
        print(f"=== iteration {i} === metrics={metrics} queried={query_ids[:5]} ... labeled={int(labeled.sum())}")
    print("TODO: replace toy fingerprints with RDKit Morgan FPs on real Tox21 SMILES.")
    print("TODO: link AlphaFold accessions for the biological target under study.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 5 toxicity screening starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "toy_tox21.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)


if __name__ == "__main__":
    main()
