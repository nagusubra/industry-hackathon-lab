#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 2 Starter Agent
Case: Autonomous Structural-Health and Aerodynamic-Design Agent

Minimal RUL baseline on NASA C-MAPSS-style tables + iterative threshold policy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


COLS = ["unit", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]


def synthesize_cmapss_like(path: Path, n_units: int = 20, max_cycles: int = 200) -> Path:
    """Create a tiny synthetic FD001-like table so the starter runs without NASA zip."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    rows = []
    for u in range(1, n_units + 1):
        life = int(rng.integers(120, max_cycles))
        for c in range(1, life + 1):
            health = 1.0 - c / life
            sensors = 500 + 50 * health + rng.normal(0, 3, size=21)
            ops = rng.normal(0, 1, size=3)
            rows.append([u, c, *ops, *sensors])
    df = pd.DataFrame(rows, columns=COLS)
    df.to_csv(path, sep=" ", header=False, index=False)
    print(f"[info] Wrote synthetic C-MAPSS-like training data to {path}")
    return path


def load_train(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=r"\s+", header=None, names=COLS)
    max_cycle = df.groupby("unit")["cycle"].transform("max")
    df["rul"] = max_cycle - df["cycle"]
    return df


def perceive(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    feature_cols = [c for c in df.columns if c.startswith("op") or c.startswith("s")]
    X = df[feature_cols].to_numpy()
    y = df["rul"].to_numpy()
    return X, y


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    metrics = {
        "mae": float(mean_absolute_error(yte, pred)),
        "rmse": float(mean_squared_error(yte, pred) ** 0.5),
    }
    return model, metrics


def act(predicted_rul: np.ndarray, inspect_threshold: float) -> dict:
    """Policy: flag engines/cycles below RUL threshold for inspection."""
    alerts = predicted_rul < inspect_threshold
    return {
        "threshold_cycles": inspect_threshold,
        "alert_rate": float(np.mean(alerts)),
        "n_alerts": int(np.sum(alerts)),
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    X, y = perceive(df)
    model, metrics = reason_train(X, y)
    print("baseline_metrics:", metrics)
    pred = model.predict(X)
    threshold = float(np.percentile(y, 20))
    for i in range(1, iters + 1):
        decision = act(pred, threshold)
        # Autonomous revision: tighten threshold if alert rate too low / high
        if decision["alert_rate"] < 0.05:
            threshold *= 1.1
        elif decision["alert_rate"] > 0.35:
            threshold *= 0.9
        print(f"=== iteration {i} ===", decision, f"next_threshold={threshold:.1f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 2 SHM / RUL starter agent")
    parser.add_argument(
        "--train-file",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "cmapss" / "train_FD001.txt",
    )
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    if not args.train_file.exists():
        synthesize_cmapss_like(args.train_file)

    df = load_train(args.train_file)
    run_loop(df, iters=args.iters)
    print("TODO: swap synthetic/local file for official NASA C-MAPSS FD001–FD004.")
    print("TODO: stretch — consume HiLiftAeroML force_mom CSVs for aero surrogates.")


if __name__ == "__main__":
    main()
