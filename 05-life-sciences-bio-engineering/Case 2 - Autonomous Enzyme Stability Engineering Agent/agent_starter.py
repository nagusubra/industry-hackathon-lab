#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 5 Starter Agent
Case: Autonomous Enzyme Stability Engineering Agent
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

AMINO_ACIDS = list("ACDEFGHIKLMNPQRSTVWY")
WILDTYPE_STUB = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSHSPGEKIKVNQ"


def synthesize_stability_table(path: Path, n: int = 400) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(22)
    rows = []
    for i in range(n):
        n_mut = int(rng.integers(1, 6))
        seq = list(WILDTYPE_STUB[:80])
        for _ in range(n_mut):
            pos = int(rng.integers(0, len(seq)))
            seq[pos] = rng.choice([aa for aa in AMINO_ACIDS if aa != seq[pos]])
        fp = np.zeros(20, dtype=int)
        for aa in seq:
            if aa in AMINO_ACIDS:
                fp[AMINO_ACIDS.index(aa)] += 1
        ph = float(rng.uniform(5.5, 8.5))
        # Latent rule: hydrophobic-rich mutants + low pH depress Tm
        hydrophobic = fp[AMINO_ACIDS.index("A")] + fp[AMINO_ACIDS.index("V")] + fp[AMINO_ACIDS.index("I")]
        tm = 62.0 + 0.04 * hydrophobic - 1.2 * n_mut - 0.8 * (ph - 7.0) + rng.normal(0, 1.5)
        rows.append(
            {
                "mutant_id": f"MUT_{i:04d}",
                "sequence": "".join(seq),
                "pH": round(ph, 2),
                "tm": round(tm, 2),
                "n_mutations": n_mut,
                **{f"aa_{aa}": int(fp[j]) for j, aa in enumerate(AMINO_ACIDS)},
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote toy enzyme-stability table to {path}")
    return df


def perceive(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return synthesize_stability_table(path)


def fetch_structure_context_stub(novozymes_dir: Path | None = None) -> str:
    """Load competition wildtype PDB from data/raw/novozymes if present; otherwise skip."""
    search_dir = novozymes_dir or Path(__file__).parent / "data" / "raw" / "novozymes"
    if not search_dir.is_dir():
        return "[warn] No data/raw/novozymes/ — structure context skipped (download competition bundle)"

    pdb_files = sorted(search_dir.glob("*.pdb"))
    if not pdb_files:
        return "[warn] No *.pdb in data/raw/novozymes/ — structure context skipped"

    pdb_path = pdb_files[0]
    header = " | ".join(pdb_path.read_text(encoding="utf-8", errors="replace").splitlines()[:3])
    return f"{pdb_path.name}: local competition PDB — {header}"


def featurize(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    aa_cols = [c for c in df.columns if c.startswith("aa_")]
    if not aa_cols:
        raise ValueError("Expected aa_* composition columns or extend with ESM embeddings.")
    X = df[aa_cols].to_numpy()
    if "pH" in df.columns:
        X = np.column_stack([X, df["pH"].to_numpy()])
    y = df["tm"].to_numpy()
    ids = df["mutant_id"].astype(str).tolist()
    return X, y, ids


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    model = RandomForestRegressor(n_estimators=120, random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    mae = float(mean_absolute_error(yte, pred))
    return model, {"mae": mae, "n_train": len(Xtr), "n_test": len(Xte)}


def act_active_learning(model, X: np.ndarray, ids: list[str], batch: int = 10) -> list[str]:
    """Acquire mutants with highest predicted Tm gain potential (explore/exploit stub)."""
    pred = model.predict(X)
    # Prefer high predicted Tm with spread (proxy for exploration)
    score = pred + 0.15 * np.std(pred) * (np.arange(len(pred)) % 7 - 3)
    pick = np.argsort(score)[-batch:]
    return [ids[i] for i in pick]


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    print("structure_context:", fetch_structure_context_stub())
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
        top = sorted(zip(ids, model.predict(X)), key=lambda t: t[1], reverse=True)[:3]
        print(
            f"=== iteration {i} === metrics={metrics} "
            f"queried={query_ids[:5]} ... labeled={int(labeled.sum())} top_pred={top}"
        )
    print("TODO: replace toy composition features with ESM / ProtBERT embeddings on real Novozymes sequences.")
    print("TODO: load competition AlphaFold wildtype PDB for residue-level mutation proposals.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 5 enzyme stability starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "toy_enzyme_stability.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)


if __name__ == "__main__":
    main()
