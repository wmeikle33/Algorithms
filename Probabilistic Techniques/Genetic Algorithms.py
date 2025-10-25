import numpy as np
from typing import Callable, Tuple

def rastrigin(x: np.ndarray) -> float:
    A = 10.0
    return A * x.size + np.sum(x**2 - A * np.cos(2 * np.pi * x))

def genetic_algorithm(
    f: Callable[[np.ndarray], float],
    bounds: Tuple[np.ndarray, np.ndarray],
    dim: int,
    pop_size: int = 120,
    generations: int = 300,
    tournament_k: int = 3,
    crossover_rate: float = 0.9,
    blx_alpha: float = 0.5,
    mutation_rate: float = 0.15,       # per-gene probability
    mutation_sigma: float = 0.1,       # as fraction of (ub-lb)
    elite: int = 2,
    seed: int = 0
):
    rng = np.random.default_rng(seed)
    lb, ub = (np.broadcast_to(np.array(bounds[0], float), (dim,)),
              np.broadcast_to(np.array(bounds[1], float), (dim,)))
    span = ub - lb

    pop = lb + rng.random((pop_size, dim)) * span
    fitness = np.array([f(ind) for ind in pop])  # lower is better (minimization)

    def tournament_select():
        idx = rng.integers(0, pop_size, size=tournament_k)
        return idx[np.argmin(fitness[idx])]

    history = []
    for g in range(generations):
        elite_idx = np.argsort(fitness)[:elite]
        next_pop = [pop[i].copy() for i in elite_idx]

        while len(next_pop) < pop_size:
            p1 = pop[tournament_select()]
            p2 = pop[tournament_select()]
            c1, c2 = p1.copy(), p2.copy()

            if rng.random() < crossover_rate:
                lo = np.minimum(p1, p2)
                hi = np.maximum(p1, p2)
                r = hi - lo
                lo_exp = lo - blx_alpha * r
                hi_exp = hi + blx_alpha * r
                c1 = rng.uniform(lo_exp, hi_exp)
                c2 = rng.uniform(lo_exp, hi_exp)

            for c in (c1, c2):
                mask = rng.random(dim) < mutation_rate
                if mask.any():
                    c[mask] += rng.normal(0.0, mutation_sigma, size=mask.sum()) * span[mask]
                np.clip(c, lb, ub, out=c)

            next_pop.extend([c1, c2])

        pop = np.array(next_pop[:pop_size])
        fitness = np.array([f(ind) for ind in pop])
        best_idx = np.argmin(fitness)
        history.append(float(fitness[best_idx]))

        if (g+1) % 20 == 0 or g == 0:
            print(f"Gen {g+1:3d}: best f = {fitness[best_idx]:.6f}")

    best_idx = np.argmin(fitness)
    return pop[best_idx], float(fitness[best_idx]), history

