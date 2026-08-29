"""Snow/delivery routing: nearest-neighbour, then 2-opt, then one stop closed."""
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).parent / "data" / "stops.csv"


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dl = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def dist_matrix(stops):
    n = len(stops)
    d = np.zeros((n, n))
    lat, lon = stops["lat"].to_numpy(), stops["lon"].to_numpy()
    for i in range(n):
        for j in range(n):
            d[i, j] = haversine_km(lat[i], lon[i], lat[j], lon[j])
    return d


def tour_len(tour, d):
    return float(sum(d[tour[i], tour[i + 1]] for i in range(len(tour) - 1)))


def nearest_neighbour(d):
    n = d.shape[0]
    unvisited = set(range(1, n))
    tour = [0]
    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda j: d[last, j])
        unvisited.remove(nxt)
        tour.append(nxt)
    tour.append(0)
    return tour


def two_opt(tour, d):
    best = tour[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                if j - i == 1:
                    continue
                cand = best[:i] + best[i:j][::-1] + best[j:]
                if tour_len(cand, d) + 1e-9 < tour_len(best, d):
                    best = cand
                    improved = True
    return best


def main():
    stops = pd.read_csv(DATA)
    d = dist_matrix(stops)
    nn = nearest_neighbour(d)
    opt = two_opt(nn, d)
    print(f"NN tour km:    {tour_len(nn, d):.2f}")
    print(f"2-opt tour km: {tour_len(opt, d):.2f}")

    # Disruption: close stop_id 10 (drop that node, keep depot).
    closed = 10
    keep = [i for i in range(len(stops)) if i != closed]
    sub = stops.iloc[keep].reset_index(drop=True)
    d2 = dist_matrix(sub)
    nn2 = nearest_neighbour(d2)
    opt2 = two_opt(nn2, d2)
    print(f"After closing stop_id={closed} ({stops.loc[stops.stop_id==closed, 'name'].iloc[0]}): {tour_len(opt2, d2):.2f} km")


if __name__ == "__main__":
    main()
