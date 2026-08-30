"""Housing DP triage: oldest-first vs days-over-target + housing type; then 20% fewer slots."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "calgary_housing_development_permits.csv"
N = 50
# Stated targets (days): developing 100, established/complete 186 — matching public wait-time range.
TARGET = {"DEVELOPING": 100, "ESTABLISHED": 186, "COMPLETE": 186}
AS_OF = pd.Timestamp("2026-08-29")


def housing_weight(category: str) -> int:
    c = str(category).lower()
    if "multi-family" in c:
        return 3
    if "new single" in c or "contextual" in c:
        return 2
    if "secondary suite" in c or "additions" in c:
        return 2
    return 1


def main():
    df = pd.read_csv(DATA, parse_dates=["applieddate", "decisiondate"])
    open_status = ~df["statuscurrent"].str.lower().isin(["released", "cancelled", "approved"])
    df = df.loc[open_status].copy()
    df["applieddate"] = pd.to_datetime(df["applieddate"], errors="coerce")
    df = df.dropna(subset=["applieddate", "permitnum"])
    df["age_days"] = (AS_OF - df["applieddate"]).dt.days.clip(lower=0)
    df["target"] = df["srg"].map(TARGET).fillna(100)
    df["days_over"] = (df["age_days"] - df["target"]).clip(lower=0)
    df["type_w"] = df["category"].map(housing_weight)
    df["score"] = df["days_over"] * df["type_w"] + 0.1 * df["age_days"]

    fifo = df.sort_values("applieddate").head(N)
    scored = df.sort_values("score", ascending=False).head(N)
    cut = df.sort_values("score", ascending=False).head(int(N * 0.8))

    def report(name, part):
        mf = int(part["category"].str.contains("Multi-Family", case=False, na=False).sum())
        print(
            f"{name:28s}  n={len(part)}  mean_age={part['age_days'].mean():.0f}  "
            f"days_over_sum={int(part['days_over'].sum())}  multi_family={mf}  "
            f"established={int((part['srg']=='ESTABLISHED').sum())}"
        )

    report("FIFO oldest-first", fifo)
    report("over-target x housing", scored)
    report("revise 80% capacity", cut)
    dropped = set(scored["permitnum"]) - set(cut["permitnum"])
    print(f"Files dropped after the cut: {len(dropped)}")


if __name__ == "__main__":
    main()
