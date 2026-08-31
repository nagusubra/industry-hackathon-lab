"""Street-light 311: oldest-first vs age+repeats; then a 20% crew cut."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "street_lights_311.csv"
N = 40


def main():
    df = pd.read_csv(DATA, parse_dates=["requested_date"])
    now = df["requested_date"].max() + pd.Timedelta(days=1)
    df["age_days"] = (now - df["requested_date"]).dt.days
    repeats = df.groupby("comm_name")["service_request_id"].transform("count")
    df["repeat_n"] = repeats
    df["score"] = df["age_days"] + 3 * df["repeat_n"]

    fifo = df.sort_values("requested_date").head(N)
    scored = df.sort_values("score", ascending=False).head(N)
    cut = df.sort_values("score", ascending=False).head(int(N * 0.8))

    def report(name, part):
        print(
            f"{name:22s}  n={len(part)}  mean_age={part['age_days'].mean():.1f}  "
            f"communities={part['comm_name'].nunique()}"
        )

    report("FIFO oldest-first", fifo)
    report("age + 3*repeats", scored)
    report("revise 80% crew", cut)


if __name__ == "__main__":
    main()
