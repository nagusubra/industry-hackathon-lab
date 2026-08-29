"""Collision hotspots: count-only top 20 vs count + recent-share; re-weight once."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "calgary_traffic_incidents_2025.csv"


def top20(df, score, label):
    g = df.groupby("location_key").agg(
        n=("incident_count", "sum"),
        recent=("is_recent", "mean"),
        sample=("incident_info", "first"),
    )
    g["score"] = score(g)
    ranked = g.sort_values("score", ascending=False).head(20)
    print(f"\n{label}")
    print(ranked[["n", "recent", "score"]].head(8).to_string())
    return set(ranked.index)


def main():
    df = pd.read_csv(DATA, parse_dates=["start_dt"])
    df["lat_r"] = df["latitude"].round(3)
    df["lon_r"] = df["longitude"].round(3)
    df["location_key"] = df["lat_r"].astype(str) + "," + df["lon_r"].astype(str)
    cutoff = df["start_dt"].max() - pd.Timedelta(days=90)
    df["is_recent"] = df["start_dt"] >= cutoff

    a = top20(df, lambda g: g["n"], "Baseline: count only")
    b = top20(df, lambda g: g["n"] * (1 + g["recent"]), "v1: count * (1 + recent share)")
    c = top20(df, lambda g: g["n"] * (1 + 2 * g["recent"]), "revise: heavier recent weight")
    print(f"\nOverlap baseline vs v1: {len(a & b)}/20")
    print(f"Overlap v1 vs revise:   {len(b & c)}/20")


if __name__ == "__main__":
    main()
