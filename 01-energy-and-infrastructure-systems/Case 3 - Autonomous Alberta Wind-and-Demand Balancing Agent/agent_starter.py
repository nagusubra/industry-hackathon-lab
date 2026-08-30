"""Wind vs demand: flag tight hours; beat last-week-same-hour; retune once.

Tight = expensive hour (top 10% price). Persistence = was it tight 168 hours ago?
v1/v2 = low wind share. Change the quantile if you want a different rule.
"""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "aeso_hourly_2024.csv"


def metrics(y_true, y_pred):
    y_true = y_true.astype(bool)
    y_pred = y_pred.astype(bool)
    tp = int((y_true & y_pred).sum())
    fp = int((~y_true & y_pred).sum())
    fn = int((y_true & ~y_pred).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    return tp, fp, fn, prec, rec


def main():
    df = pd.read_csv(DATA, parse_dates=["timestamp"]).dropna()
    df = df.sort_values("timestamp")
    df["wind_share"] = df["wind_mw"] / df["ail_mw"]
    # Ground truth for scoring: expensive hour (you can replace this definition).
    df["tight"] = df["pool_price_cad_per_mwh"] >= df["pool_price_cad_per_mwh"].quantile(0.90)
    df["persist"] = df["tight"].shift(24 * 7)  # 168 hours earlier (same clock hour last week)
    # First rule: low wind share.
    t1 = df["wind_share"].quantile(0.20)
    df["flag_v1"] = df["wind_share"] <= t1
    t2 = df["wind_share"].quantile(0.30)
    df["flag_v2"] = df["wind_share"] <= t2

    hold = df.dropna(subset=["persist"])
    print("Hold-out hours", len(hold), "true tight (p90 price)", int(hold["tight"].sum()))
    for name, col in [
        ("persistence (last week, same hour)", hold["persist"]),
        (f"wind_share <= {t1:.3f}", hold["flag_v1"]),
        (f"revise wind_share <= {t2:.3f}", hold["flag_v2"]),
    ]:
        tp, fp, fn, prec, rec = metrics(hold["tight"], col)
        print(f"{name:40s}  prec={prec:.2f} rec={rec:.2f}  tp={tp} fp={fp} fn={fn}")


if __name__ == "__main__":
    main()
