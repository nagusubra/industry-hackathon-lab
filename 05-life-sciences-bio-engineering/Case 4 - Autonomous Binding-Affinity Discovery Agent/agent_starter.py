#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 5 Starter Agent
Case: Autonomous Binding-Affinity Discovery Agent
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def synthesize_binding_table(path: Path, n: int = 400) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(44)
    fps = rng.integers(0, 2, size=(n, 28))
    # Latent affinity rule on first 6 bits -> paffinity
    logits = fps[:, :6].sum(axis=1) + rng.normal(0, 0.35, size=n)
    affinity_nM = np.clip(10 ** (6.0 - logits), 0.5, 50000.0)
    paffinity = -np.log10(affinity_nM * 1e-9)
    df = pd.DataFrame(fps, columns=[f"fp_{i}" for i in range(28)])
    df.insert(0, "ligand_id", [f"LIG_{i:04d}" for i in range(n)])
    df["smiles"] = ["CCO"] * n
    df["target_uniprot"] = "P00533"
    df["affinity_type"] = "Ki"
    df["affinity_nM"] = np.round(affinity_nM, 2)
    df["paffinity"] = np.round(paffinity, 3)
    df.to_csv(path, index=False)
    print(f"[info] Wrote toy binding-affinity table to {path}")
    return df


def perceive(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return synthesize_binding_table(path)


def featurize(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    fp_cols = [c for c in df.columns if c.startswith("fp_")]
    if not fp_cols:
        raise ValueError("Expected fp_* columns (toy fingerprints) or extend with RDKit.")
    X = df[fp_cols].to_numpy()
    y = df["paffinity"].to_numpy()
    ids = df["ligand_id"].astype(str).tolist()
    return X, y, ids


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    model = RandomForestRegressor(n_estimators=120, random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    mae = float(mean_absolute_error(yte, pred))
    return model, {"mae": mae, "n_train": len(Xtr), "n_test": len(Xte)}


def act_active_learning(model, X: np.ndarray, ids: list[str], batch: int = 10) -> list[str]:
    """Acquire ligands with highest predicted paffinity among unlabeled pool."""
    pred = model.predict(X)
    # Blend exploit (high pred) with explore (mid-range uncertainty proxy)
    uncertainty = np.abs(pred - np.median(pred))
    score = pred + 0.2 * uncertainty
    pick = np.argsort(score)[-batch:]
    return [ids[i] for i in pick]


def rank_ligands(model, X: np.ndarray, ids: list[str], top_k: int = 5) -> list[tuple[str, float]]:
    pred = model.predict(X)
    order = np.argsort(pred)[::-1][:top_k]
    return [(ids[i], float(pred[i])) for i in order]


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    target = df["target_uniprot"].iloc[0] if "target_uniprot" in df.columns else "UNKNOWN"
    print(f"target_context: UniProt={target} (filter BindingDB articles TSV to one target family)")
    X, y, ids = featurize(df)
    labeled = np.zeros(len(y), dtype=bool)
    labeled[:40] = True
    for i in range(1, iters + 1):
        model, metrics = reason_train(X[labeled], y[labeled])
        unlabeled_idx = np.where(~labeled)[0]
        query_ids = act_active_learning(
            model,
            X[unlabeled_idx],
            [ids[j] for j in unlabeled_idx],
        )
        id_to_idx = {cid: k for k, cid in enumerate(ids)}
        for cid in query_ids:
            labeled[id_to_idx[cid]] = True
        top = rank_ligands(model, X, ids)
        print(
            f"=== iteration {i} === metrics={metrics} "
            f"queried={query_ids[:5]} ... labeled={int(labeled.sum())} top_ranked={top}"
        )
    print("TODO: replace toy fingerprints with RDKit Morgan FPs on BindingDB SMILES.")
    print("TODO: load BindingDB_BindingDB_Articles_*_tsv.zip and filter by UniProt (see data/README.md).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 5 binding-affinity discovery starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "toy_binding_affinity.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)


if __name__ == "__main__":
    main()
