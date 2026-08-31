"""Cathode shortlist: energy-only top 10 vs energy + cycle/abundance; then drop Co."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "demo_insertion_electrodes.csv"


def show(title, df):
    cols = ["formula", "working_ion", "energy_grav_wh_kg", "cycle_life_proxy", "abundance_score"]
    print(f"\n{title}")
    print(df[cols].head(10).to_string(index=False))
    return set(df.head(10)["formula"])


def main():
    df = pd.read_csv(DATA)
    # This file is literature-typical, not a Materials Project dump.
    a = show("Baseline: energy only", df.sort_values("energy_grav_wh_kg", ascending=False))
    df["grid_score"] = (
        0.35 * df["energy_grav_wh_kg"] / df["energy_grav_wh_kg"].max()
        + 0.40 * df["cycle_life_proxy"] / 100
        + 0.25 * df["abundance_score"] / 100
        - 0.15 * df["volume_change_pct"] / 100
    )
    b = show("v1: grid_score (cycle + abundance)", df.sort_values("grid_score", ascending=False))
    no_co = df[~df["formula"].str.contains("Co", regex=False)]
    c = show("revise: drop Co-containing formulas", no_co.sort_values("grid_score", ascending=False))
    print(f"\nOverlap energy vs grid_score: {len(a & b)}/10")
    print(f"Overlap grid_score vs no-Co:  {len(b & c)}/10")


if __name__ == "__main__":
    main()
