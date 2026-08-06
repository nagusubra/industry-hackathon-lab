#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 2 Starter Agent
Case: Autonomous Battery Health and RUL Agent

Minimal capacity-fade RUL baseline + iterative derate policy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io as sio
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

RATED_CAPACITY_AH = 2.0
EOL_FRACTION = 0.70


def find_nasa_mats(data_dir: Path) -> list[Path]:
    if not data_dir.exists():
        return []
    return sorted(data_dir.glob("B*.mat"))


def synthesize_battery_like(data_dir: Path, cell_id: str = "B0005", n_cycles: int = 150) -> Path:
    """Create a synthetic NASA-style capacity fade .mat file."""
    data_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(5)
    eol_cycle = int(rng.integers(80, n_cycles))
    capacities = []
    for c in range(1, n_cycles + 1):
        fade = min(1.0, c / eol_cycle)
        cap = RATED_CAPACITY_AH * (1.0 - 0.35 * fade) + rng.normal(0, 0.01)
        capacities.append(max(0.5, cap))

    cycles = []
    for i, cap in enumerate(capacities, start=1):
        n_pts = 200
        voltage = 3.0 + 1.2 * (1.0 - i / n_cycles) + 0.3 * np.linspace(1, 0, n_pts)
        current = np.full(n_pts, -1.5)
        temp = 25.0 + 5.0 * (i / n_cycles) + rng.normal(0, 0.2, n_pts)
        cycles.append(
            {
                "type": "discharge",
                "data": {
                    "Voltage_measured": voltage.astype(np.float64),
                    "Current_measured": current.astype(np.float64),
                    "Temperature_measured": temp.astype(np.float64),
                    "Capacity": np.float64(cap),
                },
            }
        )

    out = data_dir / f"{cell_id}.mat"
    sio.savemat(out, {"cycle": np.array(cycles, dtype=object)}, do_compression=True)
    print(
        f"[warn] Wrote synthetic demo data to {out} — this is NOT real NASA PCoE data. "
        "Download the official zip per data/README.md for actual battery aging records."
    )
    return out


def extract_capacity_series(mat_path: Path) -> pd.DataFrame:
    """Extract per-cycle capacity from a NASA-style .mat file."""
    mat = sio.loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    cycles = mat["cycle"]
    if not isinstance(cycles, np.ndarray):
        cycles = np.array([cycles])
    rows = []
    discharge_idx = 0
    for c in cycles:
        ctype = str(getattr(c, "type", "")).lower()
        if "discharge" not in ctype:
            continue
        discharge_idx += 1
        data = c.data
        cap = float(np.asarray(data.Capacity).ravel()[0])
        voltage = np.asarray(data.Voltage_measured, dtype=np.float64).ravel()
        current = np.asarray(data.Current_measured, dtype=np.float64).ravel()
        temp = np.asarray(data.Temperature_measured, dtype=np.float64).ravel()
        rows.append(
            {
                "cycle": discharge_idx,
                "capacity_ah": cap,
                "voltage_mean": float(voltage.mean()),
                "voltage_min": float(voltage.min()),
                "current_mean": float(current.mean()),
                "temp_mean": float(temp.mean()),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        raise ValueError(f"No discharge cycles found in {mat_path}")
    eol_capacity = RATED_CAPACITY_AH * EOL_FRACTION
    below = df.index[df["capacity_ah"] <= eol_capacity]
    eol_idx = int(below[0]) if len(below) else len(df) - 1
    df["rul_cycles"] = np.maximum(0, eol_idx - df.index)
    df["soh"] = df["capacity_ah"] / RATED_CAPACITY_AH
    return df


def perceive(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    feature_cols = ["cycle", "voltage_mean", "voltage_min", "current_mean", "temp_mean", "soh"]
    X = df[feature_cols].to_numpy()
    y = df["rul_cycles"].to_numpy()
    return X, y


def reason_train(X: np.ndarray, y: np.ndarray):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    metrics = {
        "rul_mae": float(mean_absolute_error(yte, pred)),
        "rul_rmse": float(mean_squared_error(yte, pred) ** 0.5),
    }
    return model, metrics, pred, yte


def act(predicted_rul: np.ndarray, derate_threshold: float, c_rate_limit: float) -> dict:
    """Policy: derate charge rate when predicted RUL falls below threshold."""
    needs_derate = predicted_rul < derate_threshold
    new_c_rate = np.where(needs_derate, c_rate_limit * 0.7, c_rate_limit)
    return {
        "derate_threshold_cycles": derate_threshold,
        "c_rate_limit": c_rate_limit,
        "derate_rate": float(np.mean(needs_derate)),
        "n_derated": int(np.sum(needs_derate)),
        "mean_c_rate": float(np.mean(new_c_rate)),
    }


def evaluate(decision: dict, y_true: np.ndarray, predicted_rul: np.ndarray) -> dict:
    """Score derate policy: cycles where early derate would have helped."""
    early_warning = predicted_rul < decision["derate_threshold_cycles"]
    still_healthy = y_true > decision["derate_threshold_cycles"]
    timely = int(np.sum(early_warning & still_healthy))
    late = int(np.sum((~early_warning) & (y_true <= decision["derate_threshold_cycles"])))
    return {
        "timely_warnings": timely,
        "late_warnings": late,
        "warning_precision": timely / max(int(np.sum(early_warning)), 1),
    }


def run_loop(df: pd.DataFrame, iters: int = 3) -> None:
    X, y = perceive(df)
    model, metrics, pred, y_hold = reason_train(X, y)
    print("baseline_metrics:", metrics)
    full_pred = model.predict(X)
    threshold = max(5.0, float(np.percentile(y, 25)))
    c_rate = 1.0
    for i in range(1, iters + 1):
        decision = act(full_pred, threshold, c_rate)
        scores = evaluate(decision, y, full_pred)
        print(f"=== iteration {i} ===", decision, scores)
        if decision["derate_rate"] < 0.05:
            threshold *= 1.1
        elif decision["derate_rate"] > 0.40:
            threshold *= 0.9
            c_rate = max(0.5, c_rate - 0.05)
        print(f"  next_threshold={threshold:.1f}, c_rate={c_rate:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 2 Battery health / RUL starter agent")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "nasa-battery",
    )
    parser.add_argument("--cell", type=str, default="B0005")
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    mat_path = args.data_dir / f"{args.cell}.mat"
    if not mat_path.exists():
        synthesize_battery_like(args.data_dir, cell_id=args.cell)

    df = extract_capacity_series(mat_path)
    run_loop(df, iters=args.iters)
    print("TODO: replace synthetic/local .mat with NASA PCoE Li-ion Battery Aging zip.")
    print("TODO: optional — Randomized Battery Usage on Zenodo for extra cycling diversity.")


if __name__ == "__main__":
    main()
