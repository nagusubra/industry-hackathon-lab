#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 4 Starter Agent
Case: Autonomous Sustainable Polymer Design Agent

Synthetic polymer SMILES-like features + Tg labels;
multi-objective rank; propose next candidates; iterate.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


SMILES_FRAGMENTS = ["c1ccccc1", "CCO", "C(=O)O", "C#N", "C(F)(F)F", "COC", "CC(=O)N", "c1ncccn1"]
TARGET_TG = 150.0  # °C — heat-resistance target


def synthetic_polymer_table(path: Path, n_rows: int = 150) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(13)
    rows = []
    for i in range(n_rows):
        n_frag = int(rng.integers(2, 5))
        frags = rng.choice(SMILES_FRAGMENTS, size=n_frag, replace=True)
        smiles = ".".join(frags)
        # Hidden structure: aromatic + nitrile fragments raise Tg
        aromatic = sum(f.count("c1") for f in frags)
        nitrile = sum(f.count("#N") for f in frags)
        ffv = float(rng.uniform(0.08, 0.22))
        density = float(rng.uniform(0.95, 1.35))
        thermal_k = float(rng.uniform(0.15, 0.45))
        rg = float(rng.uniform(8, 25))
        tg = float(60 + 25 * aromatic + 18 * nitrile - 80 * ffv + rng.normal(0, 8))
        rows.append(
            {
                "polymer_id": f"poly-{i:04d}",
                "smiles": smiles,
                "Tg": tg,
                "thermal_conductivity": thermal_k,
                "Rg": rg,
                "density": density,
                "FFV": ffv,
                "n_aromatic": aromatic,
                "n_nitrile": nitrile,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote synthetic polymer table to {path}")
    return df


def perceive(csv_path: Path) -> pd.DataFrame:
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return synthetic_polymer_table(csv_path)


def featurize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "smiles" in out.columns:
        out["smiles_len"] = out["smiles"].astype(str).str.len()
        out["n_dots"] = out["smiles"].astype(str).str.count(r"\.")
    for col in ["n_aromatic", "n_nitrile", "FFV", "density", "thermal_conductivity", "Rg"]:
        if col not in out.columns:
            out[col] = 0.0
    return out


def multi_objective_score(df: pd.DataFrame, target_tg: float = TARGET_TG) -> pd.DataFrame:
    out = df.copy()
    tg_err = np.abs(out["Tg"].astype(float) - target_tg)
    out["tg_score"] = -tg_err
    out["thermal_score"] = out["thermal_conductivity"].astype(float)
    out["process_score"] = -out["FFV"].astype(float)  # lower free volume often better barrier
    out["agent_score"] = out["tg_score"] + 0.5 * out["thermal_score"] + 0.3 * out["process_score"]
    return out.sort_values("agent_score", ascending=False)


def propose_candidates(
    df: pd.DataFrame,
    model: RandomForestRegressor,
    feature_cols: list[str],
    n_proposals: int,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Mutate top polymers by swapping SMILES fragments; score with surrogate model."""
    top = df.nlargest(10, "agent_score") if "agent_score" in df.columns else df.head(10)
    proposals = []
    for i in range(n_proposals):
        parent = top.sample(1, random_state=int(rng.integers(1e9))).iloc[0]
        frags = str(parent["smiles"]).split(".")
        if len(frags) > 1 and rng.random() < 0.5:
            idx = int(rng.integers(0, len(frags)))
            frags[idx] = rng.choice(SMILES_FRAGMENTS)
        else:
            frags.append(rng.choice(SMILES_FRAGMENTS))
        new_smiles = ".".join(frags)
        aromatic = sum(f.count("c1") for f in frags)
        nitrile = sum(f.count("#N") for f in frags)
        ffv = float(rng.uniform(0.08, 0.22))
        feat = {
            "smiles_len": len(new_smiles),
            "n_dots": new_smiles.count("."),
            "n_aromatic": aromatic,
            "n_nitrile": nitrile,
            "FFV": ffv,
            "density": float(parent.get("density", 1.1)),
            "thermal_conductivity": float(parent.get("thermal_conductivity", 0.3)),
            "Rg": float(parent.get("Rg", 15)),
        }
        pred_tg = float(model.predict(pd.DataFrame([feat])[feature_cols])[0])
        proposals.append(
            {
                "polymer_id": f"proposal-{i:03d}",
                "smiles": new_smiles,
                "Tg": pred_tg,
                "thermal_conductivity": feat["thermal_conductivity"],
                "Rg": feat["Rg"],
                "density": feat["density"],
                "FFV": feat["FFV"],
                "n_aromatic": aromatic,
                "n_nitrile": nitrile,
                "smiles_len": feat["smiles_len"],
                "n_dots": feat["n_dots"],
            }
        )
    return pd.DataFrame(proposals)


def run_loop(df: pd.DataFrame, iters: int = 3, target_tg: float = TARGET_TG, seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    feature_cols = [
        "smiles_len",
        "n_dots",
        "n_aromatic",
        "n_nitrile",
        "FFV",
        "density",
        "thermal_conductivity",
        "Rg",
    ]

    working = featurize(df)
    for i in range(1, iters + 1):
        ranked = multi_objective_score(working, target_tg=target_tg)
        print(f"=== iteration {i} === top candidates (target Tg={target_tg:.0f} °C)")
        print(ranked.head(3)[["polymer_id", "smiles", "Tg", "agent_score"]].to_string(index=False))

        X = ranked[feature_cols]
        y = ranked["Tg"].astype(float)
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=seed + i)
        model = RandomForestRegressor(n_estimators=50, random_state=seed + i)
        model.fit(X_train, y_train)

        proposals = propose_candidates(ranked, model, feature_cols, n_proposals=8, rng=rng)
        proposals = multi_objective_score(proposals, target_tg=target_tg)
        print(f"[propose] {len(proposals)} new candidates; best predicted Tg={proposals['Tg'].max():.1f} °C")

        # Merge proposals into working set for next iteration
        working = pd.concat([ranked, proposals], ignore_index=True).drop_duplicates(subset=["smiles"])
        hit_rate = (ranked.head(10)["Tg"].sub(target_tg).abs() <= 20).mean()
        print(f"[metric] top-10 Tg within ±20 °C: {hit_rate:.0%}")

        if hit_rate >= 0.5:
            print("[done] target hit rate reached.")
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 4 sustainable polymer design starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "polymer" / "train.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    parser.add_argument("--target-tg", type=float, default=TARGET_TG)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    df = perceive(args.csv)
    # Map NeurIPS columns if present
    col_map = {"Tg": "Tg", "tg": "Tg", "glass_transition_temperature": "Tg"}
    for src, dst in col_map.items():
        if src in df.columns and dst not in df.columns:
            df = df.rename(columns={src: dst})
    if "Tg" not in df.columns:
        print("[warn] No Tg column found — using synthetic table.")
        df = synthetic_polymer_table(args.csv.parent / "synthetic_polymers.csv")

    run_loop(df, iters=args.iters, target_tg=args.target_tg, seed=args.seed)
    print("TODO: add RDKit fingerprints and NeurIPS competition property models.")


if __name__ == "__main__":
    main()
