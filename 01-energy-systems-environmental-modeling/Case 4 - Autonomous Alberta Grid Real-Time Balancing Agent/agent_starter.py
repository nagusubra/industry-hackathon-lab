#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Alberta Grid Real-Time Balancing Agent
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Minimal perceive -> reason -> act -> evaluate loop for AESO Alberta grid balancing.
Replace TODOs with live AESO API ingestion, forecasts, and optimization.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class AesoObservation:
    timestamps: pd.DatetimeIndex
    ail_mw: np.ndarray
    wind_mw: np.ndarray
    solar_mw: np.ndarray
    storage_mw: np.ndarray
    gas_mw: np.ndarray
    pool_price: np.ndarray | None = None

    @property
    def renewable_mw(self) -> np.ndarray:
        return self.wind_mw + self.solar_mw

    @property
    def dispatchable_mw(self) -> np.ndarray:
        return self.gas_mw + self.storage_mw


@dataclass
class BalancingAction:
    storage_adjust_mw: np.ndarray
    dr_curtail_mw: np.ndarray
    reserve_hold_mw: np.ndarray
    notes: str


def _synthesize_aeso_demo(csd_path: Path, price_path: Path, periods: int = 168) -> None:
    """Write synthetic AIL + wind/storage + pool price series when no AESO CSV exists."""
    csd_path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    t = pd.date_range("2025-01-06", periods=periods, freq="h")
    hour = np.array([ts.hour for ts in t])
    ail = 9500 + 800 * np.sin((hour - 8) * np.pi / 12) + rng.normal(0, 150, periods)
    wind = np.clip(1800 + 600 * np.sin(hour * np.pi / 12) + rng.normal(0, 200, periods), 0, None)
    solar = np.clip(400 * np.sin(np.pi * (hour - 6) / 12), 0, None)
    solar = np.where((hour < 6) | (hour > 20), 0, solar)
    storage = rng.normal(0, 50, periods)
    gas = np.clip(ail - wind - solar - storage + rng.normal(0, 120, periods), 2000, None)

    csd = pd.DataFrame(
        {
            "timestamp": t,
            "ail_mw": ail,
            "wind_mw": wind,
            "solar_mw": solar,
            "storage_mw": storage,
            "gas_mw": gas,
        }
    )
    csd.to_csv(csd_path, index=False)

    pool_price = 45 + 25 * np.sin((hour - 17) * np.pi / 8) + rng.normal(0, 8, periods)
    pool_price = np.clip(pool_price, 10, None)
    prices = pd.DataFrame({"timestamp": t, "pool_price": pool_price})
    prices.to_csv(price_path, index=False)

    print(f"[info] Wrote synthetic AESO demo to {csd_path} and {price_path}")


def perceive(csd_csv: Path, price_csv: Path | None = None) -> AesoObservation:
    """Load AESO CSD and optional pool-price CSVs. See data/README.md."""
    price_default = csd_csv.parent / "pool_price.csv"
    if price_csv is None:
        price_csv = price_default

    if not csd_csv.exists():
        _synthesize_aeso_demo(csd_csv, price_csv)

    df = pd.read_csv(csd_csv)
    col = {c.lower(): c for c in df.columns}
    time_col = col.get("timestamp", df.columns[0])

    def _get(name: str, default: float = 0.0) -> np.ndarray:
        key = col.get(name)
        if key and key in df.columns:
            return df[key].to_numpy(dtype=float)
        return np.full(len(df), default)

    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col)

    pool_price = None
    if price_csv.exists():
        p_df = pd.read_csv(price_csv)
        p_col = {c.lower(): c for c in p_df.columns}
        p_time = p_col.get("timestamp", p_df.columns[0])
        p_val = p_col.get("pool_price", p_col.get("smp", p_df.select_dtypes(include="number").columns[0]))
        p_df[p_time] = pd.to_datetime(p_df[p_time])
        p_df = p_df.sort_values(p_time)
        n = min(len(df), len(p_df))
        pool_price = p_df[p_val].iloc[:n].to_numpy(dtype=float)
        timestamps = pd.DatetimeIndex(df[time_col].iloc[:n])
    else:
        timestamps = pd.DatetimeIndex(df[time_col])
        print("[warn] No pool price CSV — imbalance cost uses proxy.")

    n = len(timestamps)
    return AesoObservation(
        timestamps=timestamps,
        ail_mw=_get("ail_mw")[:n] if len(_get("ail_mw")) >= n else _get("ail_mw"),
        wind_mw=_get("wind_mw")[:n],
        solar_mw=_get("solar_mw")[:n],
        storage_mw=_get("storage_mw")[:n],
        gas_mw=_get("gas_mw")[:n],
        pool_price=pool_price,
    )


def reason(obs: AesoObservation) -> dict[str, Any]:
    """Compute imbalance and pool-price risk indicators."""
    supply = obs.renewable_mw + obs.dispatchable_mw
    imbalance = obs.ail_mw - supply
    renewable_share = obs.renewable_mw / (obs.ail_mw + 1e-9)

    price_vol = 0.0
    if obs.pool_price is not None:
        price_vol = float(np.nanstd(obs.pool_price))

    return {
        "mean_ail_mw": float(np.nanmean(obs.ail_mw)),
        "mean_renewable_share": float(np.nanmean(renewable_share)),
        "mean_imbalance_mw": float(np.nanmean(imbalance)),
        "peak_imbalance_mw": float(np.nanmax(np.abs(imbalance))),
        "pool_price_volatility": price_vol,
        "imbalance_risk_score": float(np.nanmean(np.abs(imbalance)) * (1 + price_vol / 50)),
    }


def act(obs: AesoObservation, plan: dict[str, Any], aggressiveness: float = 0.5) -> BalancingAction:
    """
    Recommend storage adjustment, DR curtailment, and reserve holds.
    TODO: replace with stochastic optimization / learned policy.
    """
    supply = obs.renewable_mw + obs.dispatchable_mw
    imbalance = obs.ail_mw - supply

    storage_adj = np.clip(-imbalance * aggressiveness, -200, 200)
    dr_curtail = np.clip(imbalance * aggressiveness * 0.3, 0, 150)
    reserve_hold = np.where(plan["imbalance_risk_score"] > 500, 100.0, 0.0)

    note = (
        f"balancing policy | aggressiveness={aggressiveness:.2f} | "
        f"risk_score={plan['imbalance_risk_score']:.1f}"
    )
    return BalancingAction(
        storage_adjust_mw=storage_adj,
        dr_curtail_mw=dr_curtail,
        reserve_hold_mw=reserve_hold,
        notes=note,
    )


def evaluate(obs: AesoObservation, action: BalancingAction) -> dict[str, float]:
    """Evaluate post-action imbalance and estimated cost exposure."""
    supply = obs.renewable_mw + obs.dispatchable_mw
    pre_imbalance = obs.ail_mw - supply
    post_imbalance = pre_imbalance - action.storage_adjust_mw - action.dr_curtail_mw

    if obs.pool_price is not None:
        cost_proxy = np.nansum(np.abs(post_imbalance) * obs.pool_price) / len(obs.pool_price)
        pre_cost = np.nansum(np.abs(pre_imbalance) * obs.pool_price) / len(obs.pool_price)
    else:
        cost_proxy = float(np.nanmean(np.abs(post_imbalance)))
        pre_cost = float(np.nanmean(np.abs(pre_imbalance)))

    return {
        "mean_abs_imbalance_mw": float(np.nanmean(np.abs(post_imbalance))),
        "peak_abs_imbalance_mw": float(np.nanmax(np.abs(post_imbalance))),
        "imbalance_reduction_mw": float(np.nanmean(np.abs(pre_imbalance)) - np.nanmean(np.abs(post_imbalance))),
        "cost_proxy": float(cost_proxy),
        "cost_reduction_proxy": float(pre_cost - cost_proxy),
        "total_storage_action_mwh": float(np.nansum(action.storage_adjust_mw)),
        "total_dr_mwh": float(np.nansum(action.dr_curtail_mw)),
    }


def run_agent_loop(obs: AesoObservation, max_iters: int = 3) -> None:
    aggressiveness = 0.5
    best = None
    for i in range(1, max_iters + 1):
        plan = reason(obs)
        action = act(obs, plan, aggressiveness=aggressiveness)
        metrics = evaluate(obs, action)
        print(f"=== iteration {i} ===")
        print("plan:", plan)
        print("action:", action.notes)
        print("metrics:", metrics)
        best = metrics
        if metrics["imbalance_reduction_mw"] < 0:
            aggressiveness = max(0.2, aggressiveness - 0.1)
        else:
            aggressiveness = min(0.9, aggressiveness + 0.1)
        print(f"[revise] next aggressiveness={aggressiveness:.2f}")
    print("final:", best)


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 4 Alberta grid balancing starter agent")
    parser.add_argument(
        "--csd-csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "aeso" / "csd_current.csv",
        help="Path to AESO Current Supply/Demand CSV",
    )
    parser.add_argument(
        "--price-csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "aeso" / "pool_price.csv",
        help="Optional pool price / SMP CSV",
    )
    parser.add_argument("--iters", type=int, default=3, help="Agent loop iterations")
    args = parser.parse_args()

    obs = perceive(args.csd_csv, args.price_csv)
    run_agent_loop(obs, max_iters=args.iters)


if __name__ == "__main__":
    main()
