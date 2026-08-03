#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Grid-Balancing Agent for Renewable Wind Integration

This skeleton implements a minimal perceive -> reason -> act loop.
Replace TODOs with your forecast models, PyPSA optimization, and policies.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class GridObservation:
    timestamps: pd.DatetimeIndex
    load_mw: np.ndarray
    wind_mw: np.ndarray

    @property
    def net_load_mw(self) -> np.ndarray:
        return self.load_mw - self.wind_mw


@dataclass
class AgentAction:
    storage_charge_mw: np.ndarray
    curtail_wind_mw: np.ndarray
    notes: str


def perceive(load_csv: Path, wind_csv: Path | None = None) -> GridObservation:
    """Load local CSV time series. See data/README.md for download instructions."""
    if not load_csv.exists():
        raise FileNotFoundError(
            f"Missing {load_csv}. Download a load series per data/README.md "
            "(e.g., Kaggle PJM hourly or PERFORM ISO load)."
        )

    load_df = pd.read_csv(load_csv)
    # Heuristic: first datetime-like column + first numeric MW column
    time_col = load_df.columns[0]
    value_col = load_df.select_dtypes(include="number").columns[0]
    load_df[time_col] = pd.to_datetime(load_df[time_col])
    load_df = load_df.sort_values(time_col)

    load_mw = load_df[value_col].to_numpy(dtype=float)

    if wind_csv and wind_csv.exists():
        wind_df = pd.read_csv(wind_csv)
        w_time = wind_df.columns[0]
        w_val = wind_df.select_dtypes(include="number").columns[0]
        wind_df[w_time] = pd.to_datetime(wind_df[w_time])
        wind_df = wind_df.sort_values(w_time)
        wind_mw = wind_df[w_val].to_numpy(dtype=float)
        n = min(len(load_mw), len(wind_mw))
        load_mw, wind_mw = load_mw[:n], wind_mw[:n]
        timestamps = pd.DatetimeIndex(load_df[time_col].iloc[:n])
    else:
        # Synthetic wind placeholder so the loop runs before real WTK data arrives
        rng = np.random.default_rng(42)
        wind_mw = np.clip(0.35 * load_mw + rng.normal(0, 0.05 * np.nanmean(load_mw), size=len(load_mw)), 0, None)
        timestamps = pd.DatetimeIndex(load_df[time_col])
        print("[warn] No wind CSV provided — using synthetic wind. Replace with NREL WTK/PERFORM data.")

    return GridObservation(timestamps=timestamps, load_mw=load_mw, wind_mw=wind_mw)


def reason(obs: GridObservation) -> dict[str, Any]:
    """TODO: replace with ML forecast + uncertainty / risk scoring."""
    net = obs.net_load_mw
    return {
        "mean_net_load_mw": float(np.nanmean(net)),
        "peak_net_load_mw": float(np.nanmax(net)),
        "wind_capacity_factor": float(np.nanmean(obs.wind_mw) / (np.nanmax(obs.wind_mw) + 1e-9)),
        "imbalance_proxy_mwh": float(np.nansum(np.abs(net - np.nanmean(net)))),
    }


def act(obs: GridObservation, plan: dict[str, Any]) -> AgentAction:
    """
    Naive policy: charge storage when wind > load, curtail excess beyond storage rate.
    TODO: replace with PyPSA LOPF / multi-period storage optimization.
    """
    # Optional PyPSA import for teams ready to wire a real network model
    try:
        import pypsa  # noqa: F401

        pypsa_available = True
    except ImportError:
        pypsa_available = False

    surplus = obs.wind_mw - obs.load_mw
    charge = np.clip(surplus, 0, None) * 0.5
    curtail = np.clip(surplus - charge, 0, None)
    note = (
        f"naive storage policy | peak_net={plan['peak_net_load_mw']:.1f} MW | "
        f"pypsa_installed={pypsa_available}"
    )
    return AgentAction(storage_charge_mw=charge, curtail_wind_mw=curtail, notes=note)


def evaluate(obs: GridObservation, action: AgentAction) -> dict[str, float]:
    # Convention: positive residual = unmet demand after usable wind and storage charge.
    # usable_wind = wind - curtail; charging increases residual (draws from surplus).
    usable_wind = obs.wind_mw - action.curtail_wind_mw
    residual = obs.load_mw - usable_wind + action.storage_charge_mw
    return {
        "mean_abs_residual_mw": float(np.nanmean(np.abs(residual))),
        "total_curtail_mwh": float(np.nansum(action.curtail_wind_mw)),
        "total_charge_mwh": float(np.nansum(action.storage_charge_mw)),
    }


def run_agent_loop(obs: GridObservation, max_iters: int = 2) -> None:
    best = None
    for i in range(1, max_iters + 1):
        plan = reason(obs)
        action = act(obs, plan)
        metrics = evaluate(obs, action)
        print(f"=== iteration {i} ===")
        print("plan:", plan)
        print("action:", action.notes)
        print("metrics:", metrics)
        best = metrics
        # TODO: revise policy parameters from metrics (true autonomy)
    print("final:", best)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 1 grid-balancing starter agent")
    parser.add_argument(
        "--load-csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "load.csv",
        help="Path to load time-series CSV",
    )
    parser.add_argument("--wind-csv", type=Path, default=None, help="Optional wind power CSV")
    parser.add_argument("--iters", type=int, default=2)
    args = parser.parse_args()

    # If no user data yet, synthesize a tiny demo series so `python agent_starter.py` runs
    if not args.load_csv.exists():
        args.load_csv.parent.mkdir(parents=True, exist_ok=True)
        demo = pd.DataFrame(
            {
                "Datetime": pd.date_range("2018-01-01", periods=168, freq="h"),
                "Load_MW": 800 + 120 * np.sin(np.linspace(0, 6 * np.pi, 168)) + np.random.default_rng(0).normal(0, 20, 168),
            }
        )
        demo.to_csv(args.load_csv, index=False)
        print(f"[info] Wrote demo load CSV to {args.load_csv}")

    obs = perceive(args.load_csv, args.wind_csv)
    run_agent_loop(obs, max_iters=args.iters)


if __name__ == "__main__":
    main()
