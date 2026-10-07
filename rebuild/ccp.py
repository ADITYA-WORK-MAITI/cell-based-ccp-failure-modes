"""
CCP inversion for discrete-choice MDPs with a terminal action — repaired implementation.

Every equation reference is to THEORY_V12.md.

Repairs relative to the original src/ (see PROJECT_X_AUDIT.md for the defect register):

  R1  Bin edges are computed ONCE from the time-t states and REUSED for the
      time-(t+1) states.  The original binned the two against separate
      percentile grids, so T_a[k,k'] mapped between two different partitions.
  R2  NaN rows are detected and excluded explicitly.  The original passed
      NaN-bearing arrays to np.percentile, which returns NaN, propagating
      through np.clip and np.searchsorted and collapsing EVERY next-period
      cell index to a single value -- leaving the continuation value constant
      across states.  (Defect "Reason 2" of the audit.)
  R3  estimate_transitions reports how many (cell, action) pairs fell back to
      the uniform kernel instead of injecting 1/K silently.
  R4  The shock-mean convention is an explicit parameter `kappa`, defaulting to
      the Euler-Mascheroni constant (standard Gumbel).  kappa=0 is the
      mean-zero / soft-Bellman convention.  See THEORY_V12 Lemma 0.
  R5  The data-generating process places the exit utility at exactly the
      anchor the estimator assumes, u(x,0) = W_tilde(x).  The original DGP set
      v(x,0) = V*(x) - exit_gap + delta(x), violating the estimator's
      identifying normalisation, so the Monte Carlo measured specification
      bias rather than sampling error.
"""

import numpy as np

EULER = np.euler_gamma  # 0.5772156649015329


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

def logsumexp_rows(M):
    """Numerically stable log-sum-exp along axis 1."""
    m = M.max(axis=1, keepdims=True)
    return m[:, 0] + np.log(np.exp(M - m).sum(axis=1))


def scrap_value(lev, size, alpha=0.5):
    """
    Raw scrap value.  W(x) = alpha * e^SIZE / (LEV + 1) * 1{LEV > -1}.

    Exact under the accounting identity Assets = Liabilities + Equity, giving
    W = alpha*Equity when Equity > 0 and 0 otherwise.
    """
    lev = np.asarray(lev, dtype=float)
    size = np.asarray(size, dtype=float)
    ok = lev > -1.0
    denom = np.where(ok, lev + 1.0, 1.0)
    return np.maximum(alpha * np.exp(size) / denom * ok, 0.0)


def ztransform(w):
    """W_tilde = z-score of ln(1+W).  Falls back to centring if sd == 0."""
    lw = np.log1p(np.asarray(w, dtype=float))
    sd = lw.std(ddof=0)
    if sd < 1e-15:
        return lw - lw.mean()
    return (lw - lw.mean()) / sd


# ---------------------------------------------------------------------------
# R1 + R2: discretisation with shared edges and explicit NaN handling
# ---------------------------------------------------------------------------

def make_edges(x, n_bins):
    """
    Quantile bin edges per dimension, computed from the time-t states only.

    Uses nanpercentile so NaN rows (exits, right-truncated final periods) do
    not poison the edges.  Returns a list of d arrays of n_bins+1 edges.
    """
    x = np.asarray(x, dtype=float)
    qs = np.linspace(0.0, 100.0, n_bins + 1)
    return [np.nanpercentile(x[:, j], qs) for j in range(x.shape[1])]


def bin_with_edges(x, edges, n_bins):
    """
    Assign each row of x to a cell using PRE-COMPUTED edges (R1).

    Rows containing any non-finite entry return -1 (R2) rather than silently
    collapsing to a single index.  Cell id is the mixed-radix encoding
    cell = sum_j b_j * n_bins**(d-1-j), matching the original layout.
    """
    x = np.asarray(x, dtype=float)
    n, d = x.shape
    bad = ~np.isfinite(x).all(axis=1)

    bins = np.zeros((n, d), dtype=np.int64)
    for j in range(d):
        interior = edges[j][1:-1]
        col = np.where(bad, edges[j][0], x[:, j])  # placeholder for bad rows
        idx = np.searchsorted(interior, col, side="right")
        bins[:, j] = np.clip(idx, 0, n_bins - 1)

    mult = np.array([n_bins ** (d - 1 - j) for j in range(d)], dtype=np.int64)
    cells = bins @ mult
    cells[bad] = -1
    return cells


# ---------------------------------------------------------------------------
# Estimation
# ---------------------------------------------------------------------------

def estimate_ccps(cell_ids, actions, K, n_actions=3, alpha_L=0.1):
    """
    Laplace-smoothed CCPs, sigma_tilde(a|k) = (n_ka + aL) / (n_k + A*aL).

    Returns n_ka and n_k so prior-dominated cells (n_k0 == 0) can be reported.
    The audit found 432 of 625 SEC cells had n_k0 == 0, making V_hat a
    deterministic function of cell sample size there.
    """
    cell_ids = np.asarray(cell_ids)
    actions = np.asarray(actions)
    keep = cell_ids >= 0
    n_ka = np.zeros((K, n_actions), dtype=float)
    np.add.at(n_ka, (cell_ids[keep], actions[keep]), 1.0)
    n_k = n_ka.sum(axis=1)
    sigma = (n_ka + alpha_L) / (n_k[:, None] + n_actions * alpha_L)
    return sigma, n_ka, n_k


def estimate_transitions(cell_ids, actions, next_cell_ids, K, n_actions=3):
    """
    Action-specific transition matrices for continuation actions.

    info['n_fallback'][a] counts cells with no observed (cell, action)
    transitions, which receive the uniform kernel 1/K (R3).  A large count
    means the continuation value there is the global average and carries no
    local information.
    """
    cell_ids = np.asarray(cell_ids)
    actions = np.asarray(actions)
    next_cell_ids = np.asarray(next_cell_ids)

    T, n_fallback = {}, {}
    for a in range(1, n_actions):
        M = np.zeros((K, K), dtype=float)
        sel = (actions == a) & (cell_ids >= 0) & (next_cell_ids >= 0)
        np.add.at(M, (cell_ids[sel], next_cell_ids[sel]), 1.0)
        rs = M.sum(axis=1)
        empty = rs == 0
        M[~empty] /= rs[~empty, None]
        M[empty] = 1.0 / K
        T[a] = M
        n_fallback[a] = int(empty.sum())
    return T, {"n_fallback": n_fallback}


def invert(sigma, T, u_exit_anchor, beta, kappa=EULER):
    """
    Hotz-Miller inversion under shock-mean convention kappa.

    THEORY_V12 (INV), (TARGET), (RECOVER):
        V(k)   = W_tilde(k) - ln sigma(0|k) + kappa
        Y_a(k) = ln[sigma(a|k)/sigma(0|k)] + W_tilde(k)
        u_a(k) = Y_a(k) - beta (T_a V)(k)

    Proposition 3: changing kappa shifts V by exactly kappa and every
    continuation utility by exactly -beta*kappa, leaving within-continuation
    differences untouched.
    """
    sigma = np.asarray(sigma, dtype=float)
    w = np.asarray(u_exit_anchor, dtype=float)
    n_actions = sigma.shape[1]

    V = w - np.log(sigma[:, 0]) + kappa
    Y = np.empty((len(w), n_actions - 1))
    u = np.empty_like(Y)
    for i, a in enumerate(range(1, n_actions)):
        Y[:, i] = np.log(sigma[:, a]) - np.log(sigma[:, 0]) + w
        u[:, i] = Y[:, i] - beta * (T[a] @ V)
    return u, V, Y


def spectral_radius_betaM(sigma, T, beta):
    """
    rho(beta*M) with M = sum_a diag(sigma_a) T_a.  Should be < 1.

    NOTE: the audit found this check PASSES (rho ~= beta) even when every T_a
    is degenerate, so it must not be treated as evidence that the transition
    matrices are informative.  Use transition_diagnostics for that.
    """
    n_actions = sigma.shape[1]
    M = sum(np.diag(sigma[:, a]) @ T[a] for a in range(1, n_actions))
    return float(np.max(np.abs(np.linalg.eigvals(beta * M))))


def transition_diagnostics(T):
    """
    The check that was missing.  A degenerate transition matrix -- all mass in
    one column, as produced by the original NaN defect -- gives
    n_reachable_columns == 1 and continuation values constant across states.
    """
    out = {}
    for a, M in T.items():
        col_mass = M.sum(axis=0)
        out[a] = {
            "n_reachable_columns": int((col_mass > 1e-12).sum()),
            "max_column_mass_share": float(col_mass.max() / col_mass.sum()),
            "row_sums_ok": bool(np.allclose(M.sum(axis=1), 1.0)),
        }
    return out


# ---------------------------------------------------------------------------
# Forward solution
# ---------------------------------------------------------------------------

def solve_bellman(u_exit, u_cont, T, beta, kappa=EULER, tol=1e-12, max_iter=20000):
    """
    Fixed point of THEORY_V12 (BE_kappa):
        V(k) = kappa + ln[ e^{u_exit(k)} + sum_a e^{u_cont(k,a) + beta (T_a V)(k)} ]

    kappa = EULER -> standard Gumbel DDC;  kappa = 0 -> soft Bellman.
    """
    u_exit = np.asarray(u_exit, dtype=float)
    u_cont = np.asarray(u_cont, dtype=float)
    K, nc = u_cont.shape
    V = np.zeros(K)
    for it in range(max_iter):
        cols = [u_exit] + [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
        V_new = kappa + logsumexp_rows(np.column_stack(cols))
        if np.max(np.abs(V_new - V)) < tol:
            return V_new, it + 1
        V = V_new
    return V, max_iter


def solve_bellman_continuation(u_cont, T, beta, kappa=EULER, tol=1e-12, max_iter=20000):
    """Same recursion with the terminal action removed (THEORY_V12 Prop 4)."""
    u_cont = np.asarray(u_cont, dtype=float)
    K, nc = u_cont.shape
    V = np.zeros(K)
    for it in range(max_iter):
        cols = [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
        V_new = kappa + logsumexp_rows(np.column_stack(cols))
        if np.max(np.abs(V_new - V)) < tol:
            return V_new, it + 1
        V = V_new
    return V, max_iter


def ccps_from_values(u_exit, u_cont, T, V, beta):
    """sigma(a|k) from choice-specific values.  Invariant to kappa."""
    u_exit = np.asarray(u_exit, dtype=float)
    u_cont = np.asarray(u_cont, dtype=float)
    nc = u_cont.shape[1]
    cols = [u_exit] + [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
    Vmat = np.column_stack(cols)
    Z = np.exp(Vmat - Vmat.max(axis=1, keepdims=True))
    return Z / Z.sum(axis=1, keepdims=True)


def discrepancy(u_exit, u_cont, T, beta, kappa=EULER):
    """
    D = V_kappa - V_0 (THEORY_V12 Prop 5), with bounds check.

    This is the FORWARD discrepancy: the same u fed to two different
    operators.  It is NOT what an analyst recovering utilities is exposed to
    (that is Prop 3's constant -beta*kappa).
    """
    V_k, _ = solve_bellman(u_exit, u_cont, T, beta, kappa=kappa)
    V_0, _ = solve_bellman(u_exit, u_cont, T, beta, kappa=0.0)
    D = V_k - V_0
    lo, hi = kappa, kappa / (1.0 - beta)
    return D, {
        "D_min": float(D.min()), "D_max": float(D.max()),
        "lower": float(lo), "upper": float(hi),
        "bounds_ok": bool(D.min() >= lo - 1e-8 and D.max() <= hi + 1e-8),
        "is_constant": bool(D.std() < 1e-8),
        "D_std": float(D.std()),
    }


# ---------------------------------------------------------------------------
# R5: finite-state DGP in which the estimator is EXACTLY correctly specified
# ---------------------------------------------------------------------------

def make_mdp(K=64, seed=0, beta=0.976, kappa=EULER, alpha_scrap=0.5,
             target_exit_rate=0.01, mix=0.35, omega=None):
    """
    Build a finite-state MDP whose exit utility is EXACTLY the anchor the
    estimator assumes: u(k,0) = W_tilde(k).

    The exit rate is calibrated by a scalar level shift xi on the CONTINUATION
    utilities, which leaves the anchor exact.  As N -> infinity with K fixed,
    sigma_hat -> sigma and T_hat -> T, so u_hat -> u: consistency is a clean
    claim and the Gate-1 test is unambiguous.

    `mix` controls transition mixing (0 = near-identity, 1 = near-uniform).
    """
    rng = np.random.default_rng(seed)
    if omega is None:
        omega = np.array([[1.0, 0.5, -0.5, 2.0, 0.1],
                          [0.5, 0.2, -0.3, 1.0, 0.3]])
    omega = np.asarray(omega, dtype=float)
    n_cont = omega.shape[0]
    n_actions = n_cont + 1

    phi = np.column_stack([
        rng.uniform(0.0, 0.8, K),    # LIQ
        rng.uniform(-0.5, 6.0, K),   # LEV
        rng.uniform(-0.3, 0.3, K),   # ROA
        rng.uniform(3.0, 12.0, K),   # SIZE
    ])
    Phi = np.column_stack([np.ones(K), phi])

    u_exit = ztransform(scrap_value(phi[:, 1], phi[:, 3], alpha_scrap))

    T = {}
    for a in range(1, n_actions):
        base = np.exp(rng.normal(0.0, 1.0, size=(K, K)))
        base /= base.sum(axis=1, keepdims=True)
        M = (1.0 - mix) * np.eye(K) + mix * base
        T[a] = M / M.sum(axis=1, keepdims=True)

    u_base = Phi @ omega.T  # (K, n_cont)

    def mean_exit(xi):
        uc = u_base + xi
        V, _ = solve_bellman(u_exit, uc, T, beta, kappa=kappa)
        return float(ccps_from_values(u_exit, uc, T, V, beta)[:, 0].mean())

    lo, hi = -60.0, 80.0  # mean_exit is decreasing in xi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mean_exit(mid) > target_exit_rate:
            lo = mid
        else:
            hi = mid
    xi = 0.5 * (lo + hi)

    u_cont = u_base + xi
    V, n_it = solve_bellman(u_exit, u_cont, T, beta, kappa=kappa)
    sigma = ccps_from_values(u_exit, u_cont, T, V, beta)

    return {
        "K": K, "n_actions": n_actions, "beta": beta, "kappa": float(kappa),
        "phi": phi, "u_exit": u_exit, "u_cont": u_cont, "T": T,
        "V": V, "sigma": sigma, "omega": omega, "xi": float(xi),
        "n_iter": int(n_it), "realised_exit_rate": float(sigma[:, 0].mean()),
    }


def simulate(mdp, N, T_max, seed=0):
    """
    Simulate N agents for up to T_max periods.  Exit is absorbing.

    next_cell is -1 for exit rows AND for the final period of surviving
    agents (right-truncation) -- the realistic pattern that triggered the
    original NaN defect downstream.
    """
    rng = np.random.default_rng(seed)
    K, sigma, Tm = mdp["K"], mdp["sigma"], mdp["T"]
    n_actions = mdp["n_actions"]
    cum = sigma.cumsum(axis=1)
    # Precomputed row CDFs: searchsorted is far faster than rng.choice(p=...)
    tcum = {a: Tm[a].cumsum(axis=1) for a in Tm}

    cells, acts, nxt, fids = [], [], [], []
    start = rng.integers(0, K, size=N)
    for i in range(N):
        k = int(start[i])
        for t in range(T_max):
            a = min(int(np.searchsorted(cum[k], rng.random())), n_actions - 1)
            cells.append(k); acts.append(a); fids.append(i)
            if a == 0:
                nxt.append(-1)
                break
            k2 = min(int(np.searchsorted(tcum[a][k], rng.random())), K - 1)
            nxt.append(-1 if t == T_max - 1 else k2)
            k = k2
    return {
        "cell_ids": np.array(cells), "actions": np.array(acts),
        "next_cell_ids": np.array(nxt), "firm_ids": np.array(fids),
    }


def run_estimator_finite(panel, u_exit_anchor, K, beta, kappa=EULER,
                         alpha_L=0.1, n_actions=3):
    """Full pipeline on an already-discrete panel."""
    sigma, n_ka, n_k = estimate_ccps(panel["cell_ids"], panel["actions"], K,
                                     n_actions=n_actions, alpha_L=alpha_L)
    T, tinfo = estimate_transitions(panel["cell_ids"], panel["actions"],
                                    panel["next_cell_ids"], K,
                                    n_actions=n_actions)
    u, V, Y = invert(sigma, T, u_exit_anchor, beta, kappa=kappa)
    return {
        "u": u, "V": V, "Y": Y, "sigma": sigma, "T": T,
        "n_ka": n_ka, "n_k": n_k, "K": K,
        "n_fallback": tinfo["n_fallback"],
        "n_prior_dominated": int((n_ka[:, 0] == 0).sum()),
        "rho_betaM": spectral_radius_betaM(sigma, T, beta),
        "transition_diagnostics": transition_diagnostics(T),
    }


def weighted_rmse(err, w):
    err = np.asarray(err, dtype=float)
    w = np.asarray(w, dtype=float)
    w = w / w.sum() if w.sum() > 0 else np.full(len(err), 1.0 / len(err))
    return float(np.sqrt(np.sum(w * err ** 2)))
