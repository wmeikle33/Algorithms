import math, random
from math import hypot
from typing import List, Tuple

# ----- Problem: TSP on 2D points -----
def route_length(route: List[int], pts: List[Tuple[float,float]]) -> float:
    d = 0.0
    for i in range(len(route)):
        x1,y1 = pts[route[i]]
        x2,y2 = pts[route[(i+1) % len(route)]]  # wrap to make a cycle
        d += hypot(x1 - x2, y1 - y2)
    return d

def two_opt(route: List[int]) -> List[int]:
    """Reverse a random subpath (classic 2-opt move)."""
    n = len(route)
    i, j = sorted(random.sample(range(n), 2))
    if i == j: 
        return route
    # Avoid reversing the entire route (no-op when j-i == n-1)
    if (j - i) % n <= 1:
        return route
    new = route[:]
    new[i:j] = reversed(new[i:j])
    return new

# ----- Simulated Annealing -----
def simulated_annealing_tsp(pts: List[Tuple[float,float]],
                            steps=30_000, T0=1.0, alpha=0.9992, seed=0):
    random.seed(seed)
    n = len(pts)
    cur = list(range(n))
    random.shuffle(cur)
    cur_len = route_length(cur, pts)
    best, best_len = cur[:], cur_len

    T = T0
    for k in range(steps):
        cand = two_opt(cur)
        # quick delta compute (simple but recalculates total; fine for small n)
        cand_len = route_length(cand, pts)
        delta = cand_len - cur_len

        # accept if better, else with Boltzmann probability
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-12)):
            cur, cur_len = cand, cand_len
            if cur_len < best_len:
                best, best_len = cur[:], cur_len

        T *= alpha  # geometric cooling

    return best, best_len

# ----- Demo -----
if __name__ == "__main__":
    # 20 random cities in a unit square
    pts = [(random.random(), random.random()) for _ in range(20)]
    best_route, best_len = simulated_annealing_tsp(pts, steps=40_000, T0=0.5, alpha=0.9993, seed=42)
    print("Best length:", round(best_len, 4))
    print("Best route:", best_route)
