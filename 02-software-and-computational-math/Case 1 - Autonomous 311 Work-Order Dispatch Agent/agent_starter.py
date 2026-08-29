"""311 dispatch: FIFO vs priority mix; then one crew is sick and we replan."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "311_dispatch_sample.csv"
CREWS = 8
JOBS_PER_CREW = 5


def priority(name: str) -> int:
    n = name.lower()
    if "pothole" in n or "ice" in n or "snow" in n:
        return 3
    if "streetlight" in n or "sign" in n:
        return 2
    return 1


def assign(df, n_slots):
    return df.head(n_slots).copy()


def main():
    df = pd.read_csv(DATA, parse_dates=["requested_date"])
    df["priority"] = df["service_name"].map(priority)
    slots = CREWS * JOBS_PER_CREW

    ranked = df.sort_values(["priority", "requested_date"], ascending=[False, True])

    def assign_capped(frame, n_slots, max_per_type=12):
        picked, counts = [], {}
        for row in frame.itertuples(index=False):
            t = row.service_name
            if counts.get(t, 0) >= max_per_type:
                continue
            picked.append(row)
            counts[t] = counts.get(t, 0) + 1
            if len(picked) >= n_slots:
                break
        return pd.DataFrame(picked)

    fifo = assign(df.sort_values("requested_date"), slots)
    scored = assign_capped(ranked, slots)
    scored2 = assign_capped(ranked, int(slots * 0.8))

    def report(name, part):
        print(f"{name:28s} jobs={len(part)}  priority_sum={int(part['priority'].sum())}  types={part['service_name'].nunique()}")

    report("FIFO", fifo)
    report("priority then oldest", scored)
    report("revise: 80% capacity", scored2)
    moved = set(scored["service_request_id"]) - set(scored2["service_request_id"])
    print(f"Jobs dropped after disruption: {len(moved)}")


if __name__ == "__main__":
    main()
