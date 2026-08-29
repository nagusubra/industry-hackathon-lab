"""Water flags: mean-of-parameter vs cited limits; then tighten one limit."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"


def flag_mean(samples):
    means = samples.groupby("parameter")["numeric_result"].transform("mean")
    out = samples.copy()
    out["flag"] = out["numeric_result"] > means
    return out


def flag_limits(samples, limits, tp_override=None):
    lim = limits.copy()
    if tp_override is not None:
        lim.loc[lim["parameter"] == "Total Phosphorus (TP)", "limit_value"] = tp_override
    rows = []
    for _, s in samples.iterrows():
        hit = lim[lim["parameter"] == s["parameter"]]
        if hit.empty:
            continue
        row = hit.iloc[0]
        val = s["numeric_result"]
        if row["comparator"] == "<=":
            bad = val > float(row["limit_value"])
        elif row["comparator"] == ">=":
            bad = val < float(row["limit_value"])
        elif row["comparator"] == "range":
            bad = val < float(row["limit_value_low"]) or val > float(row["limit_value_high"])
        else:
            continue
        if bad:
            rows.append(s)
    return pd.DataFrame(rows)


def main():
    samples = pd.read_csv(DATA / "watershed_samples.csv", parse_dates=["sample_date"])
    limits = pd.read_csv(DATA / "limits.csv")
    # Keep parameters that have a one-sided or range limit.
    use = samples[samples["parameter"].isin(limits["parameter"])]

    mean_flags = flag_mean(use)
    lim_flags = flag_limits(use, limits)
    tight = flag_limits(use, limits, tp_override=0.03)

    print(f"Rows scored: {len(use)}")
    print(f"Baseline flag > mean:           {int(mean_flags['flag'].sum())}  (weak rule — many false alarms)")
    print(f"Cited limits:                   {len(lim_flags)}")
    print(f"Revise TP limit 0.05 -> 0.03:   {len(tight)}")
    if len(lim_flags):
        print("\nLimit exceedances by site (top):")
        print(lim_flags.groupby("sample_site").size().sort_values(ascending=False).head(8).to_string())


if __name__ == "__main__":
    main()
