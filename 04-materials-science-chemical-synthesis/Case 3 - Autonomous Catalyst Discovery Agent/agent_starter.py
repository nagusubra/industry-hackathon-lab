#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 4 Starter Agent
Case: Autonomous Catalyst Discovery Agent

Query Catalysis-Hub (or synthetic fallback) for adsorption energies;
score vs Sabatier-volcano target; iteratively revise filters.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd


HER_OPTIMAL_DG_H = 0.0  # eV — Sabatier optimum for hydrogen evolution


def synthetic_adsorption_table(path: Path, n_rows: int = 120) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    metals = ["Pt", "Pd", "Ni", "Co", "Fe", "Cu", "Mo", "W", "Ru", "Rh", "Ir", "Au", "Ag", "Zn"]
    rows = []
    for i, metal in enumerate(metals * 8):
        # Volcano-shaped hidden landscape centered near Pt-group metals
        center_shift = {"Pt": 0.05, "Pd": -0.08, "Ni": -0.25, "Co": -0.35, "Fe": -0.45}.get(metal, 0.2)
        dg_h = float(rng.normal(center_shift, 0.18))
        rows.append(
            {
                "surface_id": f"synth-{i:03d}-{metal}",
                "chemical_composition": f"{metal}(111)",
                "metal": metal,
                "facet": "(111)",
                "adsorbate": "H",
                "dg_h_ev": dg_h,
                "pub_id": "synthetic",
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote synthetic adsorption table to {path}")
    return df


def try_fetch_catalysis_hub(limit: int = 80, cache_path: Path | None = None) -> pd.DataFrame | None:
    try:
        import requests
    except ImportError:
        print("[warn] requests not installed.")
        return None

    query = """
    {
      reactions(first: %d, reactants: "H") {
        edges {
          node {
            chemicalComposition
            reactionEnergy
            facet
            pubId
          }
        }
      }
    }
    """ % (
        limit,
    )

    try:
        resp = requests.post(
            "http://api.catalysis-hub.org/graphql",
            json={"query": query},
            timeout=20,
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:  # noqa: BLE001 — starter demo
        print(f"[warn] Catalysis-Hub query failed: {exc}")
        return None

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"[info] Cached Catalysis-Hub response to {cache_path}")

    edges = payload.get("data", {}).get("reactions", {}).get("edges", [])
    if not edges:
        print("[warn] Catalysis-Hub returned no edges.")
        return None

    rows = []
    for i, edge in enumerate(edges):
        node = edge.get("node", {})
        rows.append(
            {
                "surface_id": f"ch-{i:04d}",
                "chemical_composition": node.get("chemicalComposition", ""),
                "facet": node.get("facet", ""),
                "adsorbate": "H",
                "dg_h_ev": float(node.get("reactionEnergy", 0.0)),
                "pub_id": node.get("pubId", ""),
            }
        )
    print(f"[info] Fetched {len(rows)} reactions from Catalysis-Hub.")
    return pd.DataFrame(rows)


def perceive(csv_path: Path, use_api: bool, cache_path: Path | None = None) -> pd.DataFrame:
    if use_api:
        api_df = try_fetch_catalysis_hub(cache_path=cache_path)
        if api_df is not None and len(api_df) > 0:
            return api_df
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return synthetic_adsorption_table(csv_path)


def volcano_score(dg_h: pd.Series, optimal: float = HER_OPTIMAL_DG_H) -> pd.Series:
    """Higher is better — peaks at optimal binding energy."""
    return -np.abs(dg_h.astype(float) - optimal)


def score(df: pd.DataFrame, dg_col: str = "dg_h_ev", complexity_penalty: float = 0.05) -> pd.DataFrame:
    out = df.copy()
    if dg_col not in out.columns:
        for alt in ["reactionEnergy", "adsorption_energy"]:
            if alt in out.columns:
                dg_col = alt
                break
    if dg_col not in out.columns:
        raise ValueError("No adsorption-energy column found.")

    out["volcano_score"] = volcano_score(out[dg_col])
    # Penalize complex compositions (proxy: string length)
    if "chemical_composition" in out.columns:
        out["complexity"] = out["chemical_composition"].astype(str).str.len()
    else:
        out["complexity"] = 10
    out["agent_score"] = out["volcano_score"] - complexity_penalty * out["complexity"]
    return out.sort_values("agent_score", ascending=False)


def act(shortlist: pd.DataFrame, dg_window: tuple[float, float]) -> dict:
    col = "dg_h_ev" if "dg_h_ev" in shortlist.columns else "reactionEnergy"
    lo, hi = dg_window
    if col in shortlist.columns:
        filtered = shortlist[(shortlist[col] >= lo) & (shortlist[col] <= hi)]
    else:
        filtered = shortlist
    id_col = "surface_id" if "surface_id" in filtered.columns else filtered.columns[0]
    return {
        "dg_window": dg_window,
        "n_candidates": int(len(filtered)),
        "top_ids": filtered.head(5)[id_col].astype(str).tolist(),
        "mean_volcano": float(filtered["volcano_score"].mean()) if len(filtered) else 0.0,
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    dg_lo, dg_hi = -0.8, 0.5
    for i in range(1, iters + 1):
        ranked = score(df)
        decision = act(ranked, (dg_lo, dg_hi))
        print(f"=== iteration {i} ===", decision)
        cols = [c for c in ["surface_id", "chemical_composition", "dg_h_ev", "agent_score"] if c in ranked.columns]
        print(ranked.head(3)[cols].to_string(index=False))

        # Autonomous revise: tighten window around best observed binding energies
        if decision["n_candidates"] > 25:
            dg_lo += 0.05
            dg_hi -= 0.05
            print(f"[revise] dg_window -> ({dg_lo:.2f}, {dg_hi:.2f})")
        elif decision["n_candidates"] < 5:
            dg_lo = max(-1.2, dg_lo - 0.1)
            dg_hi = min(0.8, dg_hi + 0.1)
            print(f"[revise] dg_window -> ({dg_lo:.2f}, {dg_hi:.2f})")
        else:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 4 catalyst discovery starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "catalyst_adsorption.csv",
    )
    parser.add_argument("--iters", type=int, default=3)
    parser.add_argument("--no-api", action="store_true", help="Skip Catalysis-Hub API attempt")
    parser.add_argument(
        "--cache-api",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "catalysis-hub" / "her_h_adsorption.json",
    )
    args = parser.parse_args()

    use_api = not args.no_api and not os.environ.get("SKIP_CATALYSIS_HUB")
    df = perceive(args.csv, use_api=use_api, cache_path=args.cache_api if use_api else None)
    run_loop(df, iters=args.iters)
    print("TODO: add OER/CO2RR scaling descriptors and multi-objective Pareto reporting.")


if __name__ == "__main__":
    main()
