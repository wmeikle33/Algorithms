import numpy as np

def sample_lead_time(rng, size):
    """Lead time in days ~ Normal(μ=5, σ=1), rounded to ≥1 day."""
    L = np.maximum(1, np.round(rng.normal(5, 1, size)).astype(int))
    return L

def sample_daily_demand(rng, size):
    return rng.poisson(20, size)

def stockout_probability(R, n_sims=200_000, seed=0):
    rng = np.random.default_rng(seed)
    L = sample_lead_time(rng, n_sims)      # vector of lead times per trial
    max_L = int(L.max())

    # Simulate a demand matrix (n_sims x max_L), then zero out days beyond each L
    D = sample_daily_demand(rng, (n_sims, max_L)).astype(float)
    D[np.arange(n_sims)[:, None], np.arange(max_L)[None, :] >= L[:, None]] = 0.0
    DL = D.sum(axis=1)              

    hits = (DL > R)                        
    p_hat = hits.mean()
    se = np.sqrt(p_hat * (1 - p_hat) / n_sims)
    ci = (p_hat - 1.96 * se, p_hat + 1.96 * se)

    stats = {
        "mean_leadtime_demand": float(DL.mean()),
        "p90_leadtime_demand":  float(np.percentile(DL, 90)),
        "p95_leadtime_demand":  float(np.percentile(DL, 95)),
        "p99_leadtime_demand":  float(np.percentile(DL, 99)),
    }
    return p_hat, ci, stats

if __name__ == "__main__":
    R = 120  # reorder point (units)
    p, ci, s = stockout_probability(R)
    print(f"P(stockout | R={R}) ≈ {p:.3f} (95% CI: [{ci[0]:.3f}, {ci[1]:.3f}])")
    print(s)
