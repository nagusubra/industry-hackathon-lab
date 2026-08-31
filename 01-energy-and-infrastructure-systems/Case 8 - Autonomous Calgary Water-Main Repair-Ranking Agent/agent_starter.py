"""Water-main ranking: count-only vs count x consequence; then heavier consequence."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "calgary_water_main_breaks_2016_2026.csv"
WEIGHT = {"high": 3.0, "medium": 1.5, "low": 1.0}
WEIGHT_REVISE = {"high": 6.0, "medium": 1.5, "low": 1.0}


def top25(g, score, label):
    ranked = g.assign(score=score).sort_values("score", ascending=False).head(25)
    high_n = int((ranked["consequence"] == "high").sum())
    print(
        f"{label:40s}  high_in_top25={high_n}  "
        f"breaks_in_list={int(ranked['n'].sum())}  "
        f"mean_count={ranked['n'].mean():.1f}"
    )
    return set(ranked.index), ranked


def main():
    df = pd.read_csv(DATA, parse_dates=["break_date"])
    df["lat_r"] = df["latitude"].round(3)
    df["lon_r"] = df["longitude"].round(3)
    df["location_key"] = df["lat_r"].astype(str) + "," + df["lon_r"].astype(str)

    g = df.groupby("location_key").agg(
        n=("break_date", "size"),
        community_name=("community_name", lambda s: s.value_counts().index[0]),
        consequence=("consequence", lambda s: s.value_counts().index[0]),
    )
    g["w"] = g["consequence"].map(WEIGHT)
    g["w2"] = g["consequence"].map(WEIGHT_REVISE)

    a, _ = top25(g, g["n"], "Baseline: count only")
    b, ranked = top25(g, g["n"] * g["w"], "v1: count x consequence")
    c, _ = top25(g, g["n"] * g["w2"], "revise: heavier high consequence")
    print(f"Overlap baseline vs v1: {len(a & b)}/25")
    print(f"Overlap v1 vs revise:   {len(b & c)}/25")
    print("\nTop of v1:")
    print(ranked[["community_name", "consequence", "n", "score"]].head(8).to_string())


if __name__ == "__main__":
    main()
