"""Neighbourhood flags: downtown-only vs nearest-station AQHI + hail track."""
from pathlib import Path

import numpy as np
import pandas as pd

AQ = Path(__file__).parent / "data" / "calgary_air_quality_seed.csv"
NEIGH = Path(__file__).parent / "data" / "neighbourhoods_hail_scenario.csv"

HAIL_W = {"high": 3.0, "medium": 1.5, "low": 0.0}
DOWNTOWN = {
    "DOWNTOWN COMMERCIAL CORE",
    "DOWNTOWN EAST VILLAGE",
    "DOWNTOWN WEST END",
    "EAU CLAIRE",
    "CHINATOWN",
    "BELTLINE",
}


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlmb = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def main():
    aq = pd.read_csv(AQ, parse_dates=["readingdate"])
    aqhi = aq[aq["parameter"] == "Air Quality Health Index"].copy()
    latest = (
        aqhi.sort_values("readingdate")
        .groupby("station_name", as_index=False)
        .tail(1)
        [["station_name", "value", "latitude", "longitude"]]
        .rename(columns={"value": "aqhi", "latitude": "st_lat", "longitude": "st_lon"})
    )
    neigh = pd.read_csv(NEIGH)

    rows = []
    for row in neigh.itertuples(index=False):
        dist = haversine_km(row.latitude, row.longitude, latest["st_lat"].to_numpy(), latest["st_lon"].to_numpy())
        j = int(np.argmin(dist))
        st = latest.iloc[j]
        rows.append(
            {
                "community_name": row.community_name,
                "hail_track": row.hail_track,
                "station": st["station_name"],
                "aqhi": float(st["aqhi"]),
            }
        )
    df = pd.DataFrame(rows)
    city_mean = df["aqhi"].mean()

    df["hail_w"] = df["hail_track"].map(HAIL_W)
    df["score"] = df["aqhi"] + df["hail_w"]
    df["baseline_downtown"] = df["community_name"].str.upper().isin(DOWNTOWN)
    # Naive ops rule: if the city mean looks smoky, flag every neighbourhood.
    df["baseline_citywide"] = city_mean >= 4
    # Local air + hail path — not the same list as "flag everyone".
    df["flag_v1"] = (df["aqhi"] >= 5) | (df["hail_track"] == "high")
    df["flag_v2"] = (df["score"] >= 6.5) | (df["hail_track"] == "high")

    print(f"Citywide mean AQHI (assigned): {city_mean:.2f}")
    print(f"Baseline downtown-only flags:      {int(df['baseline_downtown'].sum())}")
    print(f"Baseline citywide (mean>=4) flags: {int(df['baseline_citywide'].sum())}")
    print(f"v1 AQHI>=5 or hail high:           {int(df['flag_v1'].sum())}")
    print(f"Revise score>=6.5 or hail high:    {int(df['flag_v2'].sum())}")
    flipped = int((df["flag_v1"] != df["flag_v2"]).sum())
    print(f"Communities that flipped:          {flipped}")
    both = df[df["flag_v1"] & (df["hail_track"] == "high")]
    print(f"v1 hail-high (also in v1):         {len(both)}")
    show = df.loc[df["flag_v1"], ["community_name", "station", "aqhi", "hail_track", "score"]]
    print(show.sort_values(["hail_track", "score"], ascending=[True, False]).head(12).to_string(index=False))


if __name__ == "__main__":
    main()
