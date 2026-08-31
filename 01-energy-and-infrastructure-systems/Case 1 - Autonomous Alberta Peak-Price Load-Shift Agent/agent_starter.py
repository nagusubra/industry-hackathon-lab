"""Peak-price load shift: always-on vs a threshold rule, then one revise."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "aeso_hourly_2024.csv"
KW = 1.0  # 1 kW flexible load; scale as you like


def bill(price, on_mask):
    return float((price * on_mask * KW).sum() / 1000.0)  # CAD for 1 kW over those hours


def main():
    df = pd.read_csv(DATA, parse_dates=["timestamp"]).dropna(subset=["pool_price_cad_per_mwh"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    peak = df.loc[df["pool_price_cad_per_mwh"].idxmax(), "timestamp"]
    start = (peak.normalize() - pd.Timedelta(days=3))
    hold = df[(df["timestamp"] >= start) & (df["timestamp"] < start + pd.Timedelta(days=7))].copy()
    train = df.loc[~df.index.isin(hold.index)]
    p = hold["pool_price_cad_per_mwh"]

    always_on = bill(p, 1)
    q90 = float(train["pool_price_cad_per_mwh"].quantile(0.90))
    v1 = bill(p, p < q90)
    q80 = float(train["pool_price_cad_per_mwh"].quantile(0.80))
    v2 = bill(p, p < q80)

    print(f"Hold-out (week around peak {peak.date()}): {len(hold)} hours  train p90={q90:.1f}  p80={q80:.1f} CAD/MWh")
    print(f"Always-on bill:     ${always_on:.2f}")
    print(f"Idle if price>=p90: ${v1:.2f}  save ${always_on - v1:.2f}")
    print(f"Revise idle>=p80:   ${v2:.2f}  save ${always_on - v2:.2f}")
    print("Next: add a battery SoC constraint, or never-run 17:00-20:00, and re-score.")


if __name__ == "__main__":
    main()
