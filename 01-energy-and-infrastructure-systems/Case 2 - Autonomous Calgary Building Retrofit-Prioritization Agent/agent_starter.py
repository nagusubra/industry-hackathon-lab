"""Retrofit ranker: biggest-building-first vs energy-per-dollar, then a tighter budget."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "calgary_city_buildings_latest_year.csv"
COST_PER_M2 = 50.0  # stated assumption — the City file has no retrofit cost
BUDGET = 2_000_000.0


def pick(df, score_col, budget):
    ranked = df.sort_values(score_col, ascending=False)
    chosen, spent = [], 0.0
    for row in ranked.itertuples(index=False):
        cost = float(row.cost)
        if spent + cost <= budget:
            chosen.append(row.property_name)
            spent += cost
    return chosen, spent


def savings(df, names):
    return float(df.loc[df["property_name"].isin(names), "site_energy_gj"].sum())


def main():
    df = pd.read_csv(DATA).dropna(subset=["property_name", "floor_area_m2", "site_energy_gj"])
    df["cost"] = df["floor_area_m2"] * COST_PER_M2
    df["energy_per_dollar"] = df["site_energy_gj"] / df["cost"]
    df["size_score"] = df["floor_area_m2"]

    base_names, base_spent = pick(df, "size_score", BUDGET)
    v1_names, v1_spent = pick(df, "energy_per_dollar", BUDGET)
    v2_names, v2_spent = pick(df, "energy_per_dollar", BUDGET * 0.8)

    print(f"Assumption: retrofit costs ${COST_PER_M2:.0f}/m2. Budget ${BUDGET:,.0f}")
    print(f"Baseline biggest-first: {len(base_names)} buildings, ${base_spent:,.0f}, {savings(df, base_names):.0f} GJ")
    print(f"Energy per $:           {len(v1_names)} buildings, ${v1_spent:,.0f}, {savings(df, v1_names):.0f} GJ")
    print(f"Revise 80% budget:      {len(v2_names)} buildings, ${v2_spent:,.0f}, {savings(df, v2_names):.0f} GJ")
    print("Funded (energy per $):", ", ".join(v1_names[:8]), "...")


if __name__ == "__main__":
    main()
