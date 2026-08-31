"""Fleet remaining life: fit a straight line on a few sensors, then move the inspect line.

RUL = remaining useful life (cycles left). MAE = average how far off we are.
Raising the inspect cutoff catches more tired engines and also inspects extra healthy ones.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

DATA = Path(__file__).parent / "data"
COLS = ["unit_nr", "time_cycles", "setting_1", "setting_2", "setting_3"] + [f"s_{i}" for i in range(1, 22)]
FEATS = ["s_4", "s_7", "s_11", "s_12", "s_15"]


def last_rows(df):
    idx = df.groupby("unit_nr")["time_cycles"].idxmax()
    return df.loc[idx].sort_values("unit_nr")


def main():
    train = pd.read_csv(DATA / "train_FD001.txt", sep=r"\s+", header=None, names=COLS)
    test = pd.read_csv(DATA / "test_FD001.txt", sep=r"\s+", header=None, names=COLS)
    true_rul = pd.read_csv(DATA / "RUL_FD001.txt", sep=r"\s+", header=None, names=["RUL"])["RUL"].to_numpy()

    max_cycle = train.groupby("unit_nr")["time_cycles"].transform("max")
    train["rul"] = max_cycle - train["time_cycles"]
    model = LinearRegression().fit(train[FEATS], train["rul"])

    last_test = last_rows(test)
    pred = model.predict(last_test[FEATS])
    mae = float(np.mean(np.abs(pred - true_rul)))
    print(f"Test MAE (last-cycle linear on {FEATS}): {mae:.1f} cycles")

    for name, thresh in [("inspect if pred RUL < 30", 30), ("revise: pred RUL < 50", 50)]:
        flag = pred < thresh
        missed = int(((true_rul < thresh) & ~flag).sum())
        extra = int((flag & (true_rul >= thresh)).sum())
        caught = int((flag & (true_rul < thresh)).sum())
        print(f"{name}: inspect {int(flag.sum())} engines  caught={caught} missed={missed} extra={extra}")


if __name__ == "__main__":
    main()
