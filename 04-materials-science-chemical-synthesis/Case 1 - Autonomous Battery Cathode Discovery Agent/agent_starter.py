#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 4 Starter Agent
Case: Autonomous Battery Cathode Discovery Agent
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd


def synthetic_electrodes(path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(3)
    chem = ["NMC811", "NCA", "LFP", "LMO", "NMC622", "LNMO", "NaFePO4", "Li2MnO3"]
    rows = []
    for i, name in enumerate(chem * 5):
        rows.append(
            {
                "battery_id": f"synth-{i}-{name}",
                "formula": name,
                "working_ion": "Li" if "Na" not in name else "Na",
                "average_voltage": float(rng.uniform(2.8, 4.6)),
                "capacity_grav": float(rng.uniform(100, 220)),
                "energy_grav": float(rng.uniform(300, 800)),
                "stability_proxy": float(rng.uniform(0.0, 0.12)),
                "contains_co": int("NMC" in name or "NCA" in name),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote synthetic electrode table to {path}")
    return df


def try_fetch_mp(limit: int = 50) -> pd.DataFrame | None:
    key = os.environ.get("MP_API_KEY")
    if not key:
        print("[warn] MP_API_KEY not set — using local/synthetic data.")
        return None
    try:
        from mp_api.client import MPRester
    except ImportError:
        print("[warn] mp-api not installed.")
        return None

    with MPRester(key, use_document_model=False) as mpr:
        docs = mpr.materials.insertion_electrodes.search(working_ion="Li", num_chunks=1, chunk_size=limit)
    return pd.DataFrame(docs)


def perceive(csv_path: Path) -> pd.DataFrame:
    mp_df = try_fetch_mp()
    if mp_df is not None and len(mp_df) > 0:
        return mp_df
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return synthetic_electrodes(csv_path)


def score(df: pd.DataFrame, co_penalty: float = 50.0) -> pd.DataFrame:
    out = df.copy()
    # Flexible column picking for MP vs synthetic
    energy = None
    for c in ["energy_grav", "energy_density", "specific_energy"]:
        if c in out.columns:
            energy = out[c].astype(float)
            break
    if energy is None and {"average_voltage", "capacity_grav"}.issubset(out.columns):
        energy = out["average_voltage"].astype(float) * out["capacity_grav"].astype(float)
    if energy is None:
        raise ValueError("Could not find energy-related columns to score.")

    stab = out["stability_proxy"] if "stability_proxy" in out.columns else 0.0
    co = out["contains_co"] if "contains_co" in out.columns else 0.0
    out["agent_score"] = energy - 500.0 * pd.Series(stab).astype(float) - co_penalty * pd.Series(co).astype(float)
    return out.sort_values("agent_score", ascending=False)


def act(shortlist: pd.DataFrame, voltage_min: float) -> dict:
    if "average_voltage" in shortlist.columns:
        filtered = shortlist[shortlist["average_voltage"] >= voltage_min]
    else:
        filtered = shortlist
    return {
        "voltage_min": voltage_min,
        "n_candidates": int(len(filtered)),
        "top_ids": filtered.head(5).get("battery_id", filtered.head(5).iloc[:, 0]).astype(str).tolist(),
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    voltage_min = 3.2
    for i in range(1, iters + 1):
        ranked = score(df)
        decision = act(ranked, voltage_min)
        print(f"=== iteration {i} ===", decision)
        print(ranked.head(3)[["battery_id", "agent_score"]].to_string(index=False) if "battery_id" in ranked.columns else ranked.head(3))
        # Autonomous revise: if too many candidates, raise voltage floor
        if decision["n_candidates"] > 20:
            voltage_min += 0.1
            print(f"[revise] voltage_min -> {voltage_min:.2f}")
        elif decision["n_candidates"] < 3:
            voltage_min = max(2.5, voltage_min - 0.1)
            print(f"[revise] voltage_min -> {voltage_min:.2f}")
        else:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 4 cathode discovery starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "sample_electrodes.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()
    df = perceive(args.csv)
    run_loop(df, iters=args.iters)
    print("TODO: add pymatgen composition featurization and MatGL surrogates.")


if __name__ == "__main__":
    main()
