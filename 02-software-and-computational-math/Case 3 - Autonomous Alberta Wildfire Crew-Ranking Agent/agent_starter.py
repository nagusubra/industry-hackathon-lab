"""Wildfire crews: biggest-first vs size+weather; then a 20% crew cut."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "alberta_wildfires_2023_2025.csv"
N = 40


def main():
    df = pd.read_csv(DATA)
    df["CURRENT_SIZE"] = pd.to_numeric(df["CURRENT_SIZE"], errors="coerce")
    df["WIND_SPEED"] = pd.to_numeric(df["WIND_SPEED"], errors="coerce").fillna(0)
    df["RELATIVE_HUMIDITY"] = pd.to_numeric(df["RELATIVE_HUMIDITY"], errors="coerce").fillna(50)
    df["FIRE_SPREAD_RATE"] = pd.to_numeric(df["FIRE_SPREAD_RATE"], errors="coerce").fillna(0)
    df = df.dropna(subset=["FIRE_NUMBER", "CURRENT_SIZE"])

    dryness = (100 - df["RELATIVE_HUMIDITY"]).clip(lower=0) / 100
    df["score"] = df["CURRENT_SIZE"] * (1 + df["WIND_SPEED"] / 20) * (1 + dryness) + 5 * df["FIRE_SPREAD_RATE"]

    biggest = df.sort_values("CURRENT_SIZE", ascending=False).head(N)
    scored = df.sort_values("score", ascending=False).head(N)
    cut = df.sort_values("score", ascending=False).head(int(N * 0.8))

    def report(name, part):
        print(
            f"{name:28s}  n={len(part)}  ha={part['CURRENT_SIZE'].sum():.0f}  "
            f"mean_wind={part['WIND_SPEED'].mean():.1f}  mean_spread={part['FIRE_SPREAD_RATE'].mean():.2f}"
        )

    report("biggest-first", biggest)
    report("size + wind + dryness", scored)
    report("revise 80% crews", cut)
    dropped = set(scored["FIRE_NUMBER"]) - set(cut["FIRE_NUMBER"])
    print(f"Fires that lost a crew: {len(dropped)}")
    print("Dropped:", ", ".join(sorted(dropped)[:12]), "...")


if __name__ == "__main__":
    main()
