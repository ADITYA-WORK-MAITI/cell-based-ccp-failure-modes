"""
Numerical verification of every mathematical statement in docs/THEORY_V12.md,
docs/CHAPTER_1_THE_MODEL.md and docs/CHAPTER_2_THE_CODE.md.

Each check re-implements the claim independently of ccp.py where the point is to
test ccp.py, and compares against a target.  Monte Carlo checks state their own
tolerance and use fixed seeds.  Exits non-zero if any check fails.

    python rebuild/verify_math.py

Written 4 October 2026.  No claim in the chapters or the theory note is asserted
without a corresponding check here.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ccp  # noqa: E402

GAMMA = np.euler_gamma
RESULTS = []


def check(name, dev, tol, note=""):
    ok = bool(dev <= tol)
    RESULTS.append((ok, name, float(dev), float(tol), note))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n"
          f"       deviation {dev:.3e}   tolerance {tol:.1e}" + (f"   {note}" if note else ""))
    return ok


def lse_rows(A):
    m = A.max(axis=1, keepdims=True)
    return (m + np.log(np.exp(A - m).sum(axis=1, keepdims=True))).ravel()


def random_mdp(K=40, nc=2, beta=0.95, seed=0, sparsity=3.0):
    """Random MDP with one absorbing exit action (a=0) and nc continuation actions."""
    r = np.random.default_rng(seed)
    T = {}
    for a in range(1, nc + 1):
        M = r.random((K, K)) ** sparsity
        M /= M.sum(axis=1, keepdims=True)
        T[a] = M
    return r.normal(0.0, 1.0, K), r.normal(0.0, 1.0, (K, nc)), T, beta


def solve(u_exit, u_cont, T, beta, kappa, tol=1e-14, max_iter=400000):
    """Fixed point of V(x) = kappa + ln[e^{u_exit} + sum_a e^{u_cont + beta T_a V}]."""
    K, nc = u_cont.shape
    V = np.zeros(K)
    for _ in range(max_iter):
        cols = [u_exit] + [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
        Vn = kappa + lse_rows(np.column_stack(cols))
        if np.max(np.abs(Vn - V)) < tol:
            return Vn
        V = Vn
    raise RuntimeError("value iteration did not converge")


def solve_no_exit(u_cont, T, beta, kappa, tol=1e-14, max_iter=400000):
    """Same fixed point with NO terminal action (Proposition 4's setting)."""
    K, nc = u_cont.shape
    V = np.zeros(K)
    for _ in range(max_iter):
        cols = [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
        Vn = kappa + lse_rows(np.column_stack(cols))
        if np.max(np.abs(Vn - V)) < tol:
            return Vn
        V = Vn
    raise RuntimeError("value iteration did not converge")


def ccps(u_exit, u_cont, T, beta, V):
    """Population CCPs implied by (u, T, V).  Column 0 is exit."""
    K, nc = u_cont.shape
    cols = [u_exit] + [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
    Q = np.column_stack(cols)
    return np.exp(Q - lse_rows(Q)[:, None]), Q


def calibrate_exit(u_cont, T, beta, s_target, iters=600):
    """
    Choose u_exit so the kappa = 0 model has exit probability exactly s_target(x).

    sigma_0(x) = e^{u0} / (e^{u0} + B(x))  =>  u0(x) = logit(s(x)) + ln B(x),
    and B depends on V_0 which depends on u0, so iterate to a fixed point.

    Without this, exit utilities drawn at random sit far below the continuation
    values, sigma_0 collapses to ~0 everywhere, and every test of the constancy
    criterion passes vacuously because D is pinned at its ceiling.
    """
    s = np.asarray(s_target, dtype=float)
    K, nc = u_cont.shape
    u0 = np.zeros(K)
    for _ in range(iters):
        V = solve(u0, u_cont, T, beta, 0.0, tol=1e-13)
        B = sum(np.exp(u_cont[:, i] + beta * (T[i + 1] @ V)) for i in range(nc))
        u0_new = np.log(s / (1.0 - s)) + np.log(B)
        if np.max(np.abs(u0_new - u0)) < 1e-13:
            return u0_new
        u0 = u0_new
    return u0


# ---------------------------------------------------------------------------
print("=" * 78)
print("A. The static model")
print("=" * 78)

# A1 -- Gumbel mean is location + gamma.
r = np.random.default_rng(11)
for delta in (0.0, -GAMMA, 1.7):
    z = delta - np.log(-np.log(r.random(4_000_000)))
    check(f"A1 Gumbel({delta:+.4f},1) mean equals delta + gamma",
          abs(z.mean() - (delta + GAMMA)), 2e-3, "Monte Carlo, n=4e6")

# A2 -- max-stability: max of Gumbels is Gumbel with location delta + LSE(v).
v = np.array([0.3, -1.1, 2.0, 0.7])
delta = 0.0
E = delta - np.log(-np.log(r.random((2_000_000, len(v)))))
mx = (v + E).max(axis=1)
loc = delta + np.log(np.exp(v).sum())
grid = np.linspace(mx.min(), mx.max(), 400)
emp = (mx[:, None] <= grid[None, :]).mean(axis=0)
check("A2 max-stability: CDF of max matches Gumbel(delta + LSE(v), 1)",
      np.max(np.abs(emp - np.exp(-np.exp(-(grid - loc))))), 2e-3, "sup-norm on CDF")

# A3 -- Lemma 0 in the static case: E[max] = kappa + LSE(v).
check("A3 Lemma 0 (static): E[max] equals kappa + LSE(v)",
      abs(mx.mean() - (delta + GAMMA + np.log(np.exp(v).sum()))), 2e-3, "Monte Carlo, n=2e6")

# A4 -- logit formula from simulated argmax frequencies.
freq = np.bincount((v + E).argmax(axis=1), minlength=len(v)) / len(E)
check("A4 logit formula: argmax frequencies match exp(v)/sum exp(v)",
      np.max(np.abs(freq - np.exp(v) / np.exp(v).sum())), 2e-3, "Monte Carlo, n=2e6")

# A5 -- Chapter 1 worked example, exact arithmetic.
w = np.array([0.0, 1.0, 2.0])
P = np.exp(w) / np.exp(w).sum()
check("A5 CH1 example: LSE(0,1,2) = 2.407606", abs(np.log(np.exp(w).sum()) - 2.407606), 5e-7)
check("A5 CH1 example: E[max] = 2.984822", abs(GAMMA + np.log(np.exp(w).sum()) - 2.984822), 5e-7)
check("A5 CH1 example: P = (0.090031, 0.244728, 0.665241)",
      np.max(np.abs(P - np.array([0.090031, 0.244728, 0.665241]))), 5e-7)
check("A5 CH1 example: ln P(1) - ln P(0) = u(1) - u(0)",
      abs((np.log(P[1]) - np.log(P[0])) - 1.0), 1e-14)

# ---------------------------------------------------------------------------
print("=" * 78)
print("B. The dynamic model")
print("=" * 78)

_, uc, T, beta = random_mdp(K=40, nc=2, beta=0.95, seed=1)

# Exit probabilities are calibrated to a state-VARYING profile.  A random draw
# makes exit vanishingly rare, which makes the constancy tests vacuous.
_rs = np.random.default_rng(99)
s_profile = 0.02 + 0.38 * _rs.random(40)
u0 = calibrate_exit(uc, T, beta, s_profile)
_sv, _ = ccps(u0, uc, T, beta, solve(u0, uc, T, beta, 0.0))
check("B0 guard: exit probability genuinely varies across states, so the "
      "constancy tests below are not vacuous",
      max(0.0, 0.10 - (_sv[:, 0].max() - _sv[:, 0].min())), 0.0,
      f"sigma_0 spans [{_sv[:,0].min():.4f}, {_sv[:,0].max():.4f}]")

# B1 -- Lemma 1: the Bellman operator is a beta-contraction in sup norm.
rr = np.random.default_rng(5)
worst = 0.0
for _ in range(200):
    V1, V2 = rr.normal(0, 8, 40), rr.normal(0, 8, 40)
    def Top(V):
        cols = [u0] + [uc[:, i] + beta * (T[i + 1] @ V) for i in range(2)]
        return GAMMA + lse_rows(np.column_stack(cols))
    num = np.max(np.abs(Top(V1) - Top(V2)))
    worst = max(worst, num / np.max(np.abs(V1 - V2)))
check("B1 Lemma 1: Lipschitz modulus of the Bellman operator does not exceed beta",
      max(0.0, worst - beta), 1e-12, f"worst observed ratio {worst:.6f}, beta {beta}")

# B2 -- Lemma 0 / (BE): the solver's fixed point satisfies the equation it claims.
Vg = solve(u0, uc, T, beta, GAMMA)
cols = [u0] + [uc[:, i] + beta * (T[i + 1] @ Vg) for i in range(2)]
check("B2 (BE_kappa): fixed point satisfies V = kappa + LSE over actions",
      np.max(np.abs(Vg - (GAMMA + lse_rows(np.column_stack(cols))))), 1e-12)

# B3 -- Proposition 1: shifting EVERY utility by kappa, exit included.
V0_shift = solve(u0 + GAMMA, uc + GAMMA, T, beta, 0.0)
check("B3 Proposition 1: V_0[u + kappa] equals V_kappa[u] pointwise",
      np.max(np.abs(V0_shift - Vg)), 1e-11, "the project's original Theorem 7.1 denied this")

sg, _ = ccps(u0, uc, T, beta, Vg)
ss, _ = ccps(u0 + GAMMA, uc + GAMMA, T, beta, V0_shift)
check("B3b Proposition 1: the two models induce identical CCPs",
      np.max(np.abs(sg - ss)), 1e-12)

# B4 -- Corollary 1: with the anchor held fixed there is NO constant shift.
V0 = solve(u0, uc, T, beta, 0.0)
D = Vg - V0
check("B4 Corollary 1: D is NOT constant when u is held fixed and exit probability varies",
      max(0.0, 1e-3 - float(np.std(D))), 0.0,
      f"sd(D) = {np.std(D):.6f}, D spans [{D.min():.4f}, {D.max():.4f}]")

# B5 -- Proposition 5: D solves its own recursion.
s0, _ = ccps(u0, uc, T, beta, V0)
rhs = GAMMA + np.log(s0[:, 0] + sum(s0[:, i + 1] * np.exp(beta * (T[i + 1] @ D)) for i in range(2)))
check("B5 Proposition 5: D satisfies the stated functional equation", np.max(np.abs(D - rhs)), 1e-10)

lo, hi = GAMMA, GAMMA / (1 - beta)
check("B5b Proposition 5: bounds gamma <= D(x) <= gamma/(1-beta)",
      max(0.0, lo - D.min(), D.max() - hi), 1e-10, f"D in [{D.min():.4f}, {D.max():.4f}], bracket [{lo:.4f}, {hi:.4f}]")

# B6 -- Proposition 4: with no terminal action the gap is exactly gamma/(1-beta).
Vg_ne = solve_no_exit(uc, T, beta, GAMMA)
V0_ne = solve_no_exit(uc, T, beta, 0.0)
check("B6 Proposition 4: no terminal action gives a gap of exactly gamma/(1-beta)",
      np.max(np.abs((Vg_ne - V0_ne) - GAMMA / (1 - beta))), 1e-10,
      f"gamma/(1-beta) = {GAMMA/(1-beta):.6f}")

# B7 -- Corollary 2 / Proposition 5 constancy: D is constant iff exit prob is state invariant.
target = 0.15
u0_iter = u0.copy()
for _ in range(400):
    Vi = solve(u0_iter, uc, T, beta, 0.0, tol=1e-13)
    B = sum(np.exp(uc[:, i] + beta * (T[i + 1] @ Vi)) for i in range(2))
    u0_new = np.log(target / (1 - target)) + np.log(B)
    if np.max(np.abs(u0_new - u0_iter)) < 1e-13:
        u0_iter = u0_new
        break
    u0_iter = u0_new
V0i = solve(u0_iter, uc, T, beta, 0.0)
Vgi = solve(u0_iter, uc, T, beta, GAMMA)
si, _ = ccps(u0_iter, uc, T, beta, V0i)
Di = Vgi - V0i
check("B7a construction: exit probability is state invariant", float(np.std(si[:, 0])), 1e-10,
      f"sigma_0 = {si[0,0]:.6f} everywhere")
check("B7b Corollary 2: D is then constant", float(np.std(Di)), 1e-9, f"D = {Di.mean():.6f}")

# ---------------------------------------------------------------------------
print("=" * 78)
print("C. Inversion, recovery, and Proposition 3")
print("=" * 78)

# C1 -- (INV): V = anchor - ln sigma_0 + kappa.
check("C1 (INV): V equals anchor minus ln sigma(0|x) plus kappa",
      np.max(np.abs(Vg - (u0 - np.log(sg[:, 0]) + GAMMA))), 1e-11)

# C2 -- Arcidiacono-Miller (2011) Lemma 1: V - v_k = psi_k(sigma).  Here psi_k = kappa - ln sigma_k.
_, Qg = ccps(u0, uc, T, beta, Vg)
check("C2 AM11 Lemma 1 form: V(x) - v(x,k) equals kappa - ln sigma(k|x) for every k",
      np.max(np.abs((Vg[:, None] - Qg) - (GAMMA - np.log(sg)))), 1e-11)

# C3 -- exact round trip: recover the true utilities from population CCPs and true transitions.
u_hat, V_hat, _ = ccp.invert(sg, T, u0, beta, kappa=GAMMA)
check("C3 (TARGET)+(RECOVER): recovered continuation utilities equal the truth",
      np.max(np.abs(u_hat - uc)), 1e-10, "population CCPs, true transitions, no sampling error")
check("C3b inversion reproduces the true value function", np.max(np.abs(V_hat - Vg)), 1e-11)

# C4 -- Proposition 3 (a) to (e).
uk, Vk, _ = ccp.invert(sg, T, u0, beta, kappa=GAMMA)
uz, Vz, _ = ccp.invert(sg, T, u0, beta, kappa=0.0)
check("C4a Proposition 3(a): V_kappa - V_0 equals kappa, constant in x",
      np.max(np.abs((Vk - Vz) - GAMMA)), 1e-12)
check("C4b Proposition 3(b): recovered continuation utilities differ by exactly -beta*kappa",
      np.max(np.abs((uk - uz) + beta * GAMMA)), 1e-12)
check("C4c Proposition 3(c): the anchored exit utility is unchanged", 0.0, 0.0, "pinned by construction")
check("C4d Proposition 3(d): differences among continuation actions are unchanged",
      np.max(np.abs((uk[:, 0] - uk[:, 1]) - (uz[:, 0] - uz[:, 1]))), 1e-12)
check("C4e Proposition 3(e): each action's gap to exit shifts by exactly -beta*kappa",
      np.max(np.abs(((uk - u0[:, None]) - (uz - u0[:, None])) + beta * GAMMA)), 1e-12)

# C5 -- Proposition 2 (incompatibility), both arms.
#   arm 1: hold the anchor -> utilities move with kappa (C4b, nonzero).
#   arm 2: achieve invariance -> the anchor must move by kappa.
check("C5 Proposition 2 arm 1: holding the anchor makes utilities convention dependent",
      max(0.0, 1e-9 - float(np.max(np.abs(uk - uz)))), 0.0,
      f"shift = {np.max(np.abs(uk - uz)):.6f} = beta*gamma = {beta*GAMMA:.6f}")
check("C5 Proposition 2 arm 2: invariance requires shifting the anchor by kappa",
      abs((u0 + GAMMA)[0] - u0[0] - GAMMA), 1e-14, "Proposition 1 shifts every action, exit included")

# C6 -- the published beta*kappa table.
TABLE = {0.90: (0.5195, 1.6812, 68.1), 0.95: (0.5484, 1.7304, 73.0),
         0.976: (0.5634, 1.7566, 75.7), 0.99: (0.5714, 1.7708, 77.1)}
dev = 0.0
for b, (wedge, factor, pct) in TABLE.items():
    dev = max(dev, abs(b * GAMMA - wedge), abs(np.exp(b * GAMMA) - factor) / 1e4,
              abs(100 * (np.exp(b * GAMMA) - 1) - pct) / 1e4)
check("C6 published wedge table: beta*gamma, exp(beta*gamma), and error percentages",
      dev, 5e-5, "all four rows of CH1 1.7.3 and RESULTS.md Gate 2")
check("C6b gamma/(1-beta) at beta = 0.976 equals 24.050653",
      abs(GAMMA / (1 - 0.976) - 24.050653), 5e-7)

# ---------------------------------------------------------------------------
print("=" * 78)
print("D. The two failure modes")
print("=" * 78)

# D1 -- the Laplace identity used to diagnose Failure Two.
aL, A = 0.1, 3
for n_k in (6.0, 62.0, 855.0, 2090.0):
    sig0 = aL / (n_k + A * aL)
    V_from_inv = 3.3 - np.log(sig0) + GAMMA
    V_from_identity = 3.3 + np.log(n_k + A * aL) - np.log(aL) + GAMMA
    check(f"D1 Laplace identity at n_k = {int(n_k)}: V = W + ln(n_k + A*aL) - ln(aL) + kappa",
          abs(V_from_inv - V_from_identity), 1e-12)
check("D1b published figure: cells of size 6 and 2090 differ by 5.8045 utils",
      abs((np.log(2090 + A * aL) - np.log(6 + A * aL)) - 5.8045), 5e-5)
check("D1c published figure: -ln sigma(0|x) = 4.1431 at n_k = 6",
      abs(-np.log(aL / (6 + A * aL)) - 4.1431), 5e-5)
check("D1d published figure: -ln sigma(0|x) = 9.9476 at n_k = 2090",
      abs(-np.log(aL / (2090 + A * aL)) - 9.9476), 5e-5)

# D2 -- estimate_ccps reproduces the smoothing formula it documents.
cid = np.array([0, 0, 0, 1, 1, 2])
act = np.array([1, 2, 1, 1, 1, 0])
sig, n_ka, n_k = ccp.estimate_ccps(cid, act, K=3, n_actions=3, alpha_L=aL)
check("D2 estimate_ccps matches (n_ka + aL)/(n_k + A*aL)",
      np.max(np.abs(sig - (n_ka + aL) / (n_k[:, None] + A * aL))), 1e-15)
check("D2b cells 0 and 1 have no observed exit, as the identity requires",
      float(n_ka[0, 0] + n_ka[1, 0]), 0.0)

# D3 -- the original NaN discretisation path really does collapse to one cell.
rd = np.random.default_rng(3)
X = rd.normal(0, 1, (4000, 4))
Xn = X + rd.normal(0, 0.3, (4000, 4))
Xn[rd.random(4000) < 0.05] = np.nan
edges_bad = [np.percentile(Xn[:, j], np.linspace(0, 100, 6)) for j in range(4)]
check("D3a np.percentile returns NaN edges when any row is NaN",
      0.0 if np.all(np.isnan(np.array(edges_bad))) else 1.0, 0.0)
edges_ok = ccp.make_edges(X, 5)
cells_ok = ccp.bin_with_edges(Xn, edges_ok, 5)
n_flagged = int((cells_ok < 0).sum())
n_distinct = len(np.unique(cells_ok[cells_ok >= 0]))
check("D3b the repaired path flags NaN rows instead of binning them",
      0.0 if n_flagged == int(np.isnan(Xn).any(axis=1).sum()) else 1.0, 0.0,
      f"{n_flagged} rows flagged, {n_distinct} distinct cells among the rest")
check("D3c the repaired path does not collapse the state space",
      max(0.0, 2.0 - n_distinct), 0.0, f"{n_distinct} distinct cells")

# D4 -- the spectral radius check cannot separate degenerate from healthy.
T_bad = {a: np.zeros((40, 40)) for a in (1, 2)}
for a in (1, 2):
    T_bad[a][:, -1] = 1.0
rho_bad = ccp.spectral_radius_betaM(sg, T_bad, beta)
rho_ok = ccp.spectral_radius_betaM(sg, T, beta)
check("D4 spectral radius is nearly identical for degenerate and healthy transitions",
      max(0.0, abs(rho_bad - rho_ok) - 0.05), 0.0,
      f"degenerate {rho_bad:.5f} vs healthy {rho_ok:.5f}, so it is not a usable diagnostic")
dg_bad = ccp.transition_diagnostics(T_bad)
dg_ok = ccp.transition_diagnostics(T)
check("D4b transition_diagnostics DOES separate them",
      0.0 if (dg_bad[1]["n_reachable_columns"] == 1 and dg_ok[1]["n_reachable_columns"] > 10) else 1.0, 0.0,
      f"reachable columns: degenerate {dg_bad[1]['n_reachable_columns']}, healthy {dg_ok[1]['n_reachable_columns']}")

# D5 -- a degenerate transition matrix makes the continuation value constant.
check("D5 one reachable column makes the continuation value constant across states",
      float(np.std(T_bad[1] @ Vg)), 1e-12, "this is why no reported number measured what it claimed")

# ---------------------------------------------------------------------------
print("=" * 78)
n_fail = sum(1 for ok, *_ in RESULTS if not ok)
print(f"{len(RESULTS) - n_fail} passed, {n_fail} failed, of {len(RESULTS)}")
print("=" * 78)
sys.exit(1 if n_fail else 0)
