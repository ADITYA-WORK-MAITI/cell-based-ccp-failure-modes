"""
Test suite for the repaired CCP estimator.

These are the checks the original project lacked.  Its 21 tests all passed and
none of them called run_estimator, so the integration path where the defects
lived was never exercised.

Run:  python rebuild/tests.py
Needs only numpy.

Test map
--------
T1  reward-shift equivalence                      THEORY_V12 Prop 1
T2  no-constant-shift corollary                   THEORY_V12 Cor 1 (= old Thm 7.1)
T3  continuation subproblem = kappa/(1-beta)      THEORY_V12 Prop 4
T4  forward discrepancy: bounds + constancy       THEORY_V12 Prop 5
T5  convention wedge is exactly -beta*kappa       THEORY_V12 Prop 3   <- the new result
T6  end-to-end recovery + consistency in N        GATE 1
T7  NaN discretisation defect: regression         audit "Reason 2"
T8  transition diagnostics catch degeneracy       the guard that was missing
T9  sparse-exit degradation is reported honestly  audit Reason 3
"""

import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ccp
from ccp import EULER


# ---------------------------------------------------------------------------
# T1 -- Proposition 1: shock-mean conventions are reward shifts
# ---------------------------------------------------------------------------

def test_reward_shift_equivalence():
    m = ccp.make_mdp(K=40, seed=1, target_exit_rate=0.02)
    beta, kappa = m["beta"], EULER

    V_kappa, _ = ccp.solve_bellman(m["u_exit"], m["u_cont"], m["T"], beta, kappa=kappa)
    # Shift EVERY utility by kappa, terminal action included
    V_shift, _ = ccp.solve_bellman(m["u_exit"] + kappa, m["u_cont"] + kappa,
                                   m["T"], beta, kappa=0.0)
    err = np.max(np.abs(V_kappa - V_shift))
    assert err < 1e-9, f"Prop 1 failed: max|V_kappa - V_0[u+kappa]| = {err:.3e}"

    # And the CCPs coincide
    s1 = ccp.ccps_from_values(m["u_exit"], m["u_cont"], m["T"], V_kappa, beta)
    s2 = ccp.ccps_from_values(m["u_exit"] + kappa, m["u_cont"] + kappa,
                              m["T"], V_shift, beta)
    assert np.max(np.abs(s1 - s2)) < 1e-12
    return {"max_abs_V_error": float(err)}


# ---------------------------------------------------------------------------
# T2 -- Corollary 1: shifting only the CONTINUATION actions cannot work
# ---------------------------------------------------------------------------

def test_no_constant_shift_when_anchor_held_fixed():
    m = ccp.make_mdp(K=40, seed=2, target_exit_rate=0.02)
    beta, kappa = m["beta"], EULER
    D, info = ccp.discrepancy(m["u_exit"], m["u_cont"], m["T"], beta, kappa=kappa)
    # D must be non-constant (exit probability varies across cells here)
    assert not info["is_constant"], "D unexpectedly constant; check sigma_0 variation"
    assert info["bounds_ok"], f"bounds violated: {info}"
    # Neither candidate constant from Cor 1 reconciles the two
    for c in (kappa, kappa / (1 - beta)):
        assert np.max(np.abs(D - c)) > 1e-6
    return {"D_min": info["D_min"], "D_max": info["D_max"],
            "D_std": info["D_std"], "sigma0_std": float(m["sigma"][:, 0].std())}


# ---------------------------------------------------------------------------
# T3 -- Proposition 4: continuation subproblem shifts by exactly kappa/(1-beta)
# ---------------------------------------------------------------------------

def test_continuation_subproblem_exact():
    m = ccp.make_mdp(K=40, seed=3, target_exit_rate=0.02)
    beta, kappa = m["beta"], EULER
    Vc, _ = ccp.solve_bellman_continuation(m["u_cont"], m["T"], beta, kappa=kappa)
    Vs, _ = ccp.solve_bellman_continuation(m["u_cont"], m["T"], beta, kappa=0.0)
    expected = kappa / (1.0 - beta)
    err = float(np.max(np.abs((Vc - Vs) - expected)))
    assert err < 1e-8, f"Prop 4 failed: max dev from kappa/(1-beta) = {err:.3e}"
    return {"expected": expected, "max_abs_error": err}


# ---------------------------------------------------------------------------
# T4 -- Proposition 5: D constant IFF sigma_0 state-invariant
# ---------------------------------------------------------------------------

def _mean_exit_prob(u_exit, u_cont, T, beta, kappa):
    V, _ = ccp.solve_bellman(u_exit, u_cont, T, beta, kappa=kappa)
    return float(ccp.ccps_from_values(u_exit, u_cont, T, V, beta)[:, 0].mean())


def test_discrepancy_constant_iff_exit_prob_invariant():
    """
    D is constant iff sigma_0 is state-invariant (THEORY_V12 Prop 5).

    NOTE ON AN EARLIER VERSION OF THIS TEST.  It fixed u_exit = 0.3 against
    continuation utilities of 1.0/0.8 at beta = 0.95, giving V ~ 43.5 and hence
    sigma_0 ~ 1e-19 in every state.  With exit effectively impossible, D sits
    pinned at its ceiling kappa/(1-beta) everywhere and the "varying" case was
    numerically constant (std ~ 8e-14), so the test failed for a reason that had
    nothing to do with the claim.  The exit utility is now CALIBRATED to put
    sigma_0 in the interior, and the test ASSERTS that it got there -- so this
    design error cannot recur silently.
    """
    beta, kappa, K = 0.95, EULER, 30
    rng = np.random.default_rng(4)
    T = {}
    for a in (1, 2):
        M = np.exp(rng.normal(size=(K, K))); M /= M.sum(axis=1, keepdims=True)
        T[a] = M

    u_cont_c = np.column_stack([np.full(K, 1.0), np.full(K, 0.8)])

    # Calibrate a scalar exit-utility level so that mean sigma_0 ~ 0.1.
    # mean_exit is increasing in the exit level, so bisect on it.
    lo, hi = -5.0, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _mean_exit_prob(np.full(K, mid), u_cont_c, T, beta, kappa) < 0.10:
            lo = mid
        else:
            hi = mid
    level = 0.5 * (lo + hi)

    # Constant exit utility + constant continuation utilities => V constant
    # (row-stochastic T leaves a constant vector fixed) => sigma_0 constant.
    u_exit_c = np.full(K, level)
    _, info_c = ccp.discrepancy(u_exit_c, u_cont_c, T, beta, kappa=kappa)
    s0_c = _mean_exit_prob(u_exit_c, u_cont_c, T, beta, kappa)

    # Perturb the exit utility => sigma_0 varies => D varies.
    u_exit_v = level + rng.normal(0.0, 1.2, size=K)
    _, info_v = ccp.discrepancy(u_exit_v, u_cont_c, T, beta, kappa=kappa)
    s0_v = _mean_exit_prob(u_exit_v, u_cont_c, T, beta, kappa)

    # Guard: the construction must actually put exit in the interior, or the
    # constant/non-constant comparison below is vacuous.
    assert 1e-4 < s0_c < 0.6, f"constant case sigma_0 not interior: {s0_c:.3e}"
    assert 1e-4 < s0_v < 0.6, f"varying case sigma_0 not interior: {s0_v:.3e}"

    assert info_c["is_constant"], f"expected constant D, got std={info_c['D_std']:.3e}"
    assert not info_v["is_constant"], (
        f"expected non-constant D, got std={info_v['D_std']:.3e} "
        f"(mean sigma_0 = {s0_v:.4f})")
    assert info_c["bounds_ok"] and info_v["bounds_ok"]
    return {"calibrated_exit_level": level,
            "mean_sigma0_constant_case": s0_c,
            "mean_sigma0_varying_case": s0_v,
            "D_std_constant_case": info_c["D_std"],
            "D_std_varying_case": info_v["D_std"],
            "D_range_varying": (info_v["D_min"], info_v["D_max"]),
            "ceiling_kappa_over_1mb": kappa / (1 - beta)}


# ---------------------------------------------------------------------------
# T5 -- Proposition 3: the convention wedge is exactly -beta*kappa
#       This is the paper's new result, and the sharpest available check.
# ---------------------------------------------------------------------------

def test_convention_wedge_is_minus_beta_kappa():
    m = ccp.make_mdp(K=48, seed=5, target_exit_rate=0.05)
    beta, kappa, K = m["beta"], EULER, m["K"]
    panel = ccp.simulate(m, N=3000, T_max=25, seed=50)

    # SAME panel, hence same sigma_hat and T_hat; only the convention differs
    e_g = ccp.run_estimator_finite(panel, m["u_exit"], K, beta, kappa=kappa)
    e_0 = ccp.run_estimator_finite(panel, m["u_exit"], K, beta, kappa=0.0)

    # (b) continuation utilities shift by exactly -beta*kappa
    wedge = e_g["u"] - e_0["u"]
    err_wedge = float(np.max(np.abs(wedge + beta * kappa)))
    # (a) value function shifts by exactly kappa
    err_V = float(np.max(np.abs((e_g["V"] - e_0["V"]) - kappa)))
    # (d) within-continuation differences are convention-free
    d_g = e_g["u"][:, 0] - e_g["u"][:, 1]
    d_0 = e_0["u"][:, 0] - e_0["u"][:, 1]
    err_diff = float(np.max(np.abs(d_g - d_0)))

    assert err_wedge < 1e-10, f"Prop 3(b) failed: {err_wedge:.3e}"
    assert err_V < 1e-10, f"Prop 3(a) failed: {err_V:.3e}"
    assert err_diff < 1e-10, f"Prop 3(d) failed: {err_diff:.3e}"
    return {"beta_kappa": float(beta * kappa),
            "max_abs_err_wedge": err_wedge,
            "max_abs_err_V_shift": err_V,
            "max_abs_err_within_continuation": err_diff}


# ---------------------------------------------------------------------------
# T6 -- GATE 1: end-to-end recovery, and RMSE falling like N^{-1/2}
# ---------------------------------------------------------------------------

def test_recovery_consistency(Ns=(500, 2000, 8000, 32000), T_max=25,
                              K=32, target_exit_rate=0.05, verbose=True):
    m = ccp.make_mdp(K=K, seed=6, target_exit_rate=target_exit_rate)
    beta = m["beta"]
    rows = []
    for N in Ns:
        panel = ccp.simulate(m, N=N, T_max=T_max, seed=600 + N)
        est = ccp.run_estimator_finite(panel, m["u_exit"], K, beta, kappa=EULER)
        w = est["n_k"]
        r1 = ccp.weighted_rmse(est["u"][:, 0] - m["u_cont"][:, 0], w)
        r2 = ccp.weighted_rmse(est["u"][:, 1] - m["u_cont"][:, 1], w)
        rd = ccp.weighted_rmse(
            (est["u"][:, 0] - est["u"][:, 1]) - (m["u_cont"][:, 0] - m["u_cont"][:, 1]), w)
        rows.append({"N": N, "n_obs": int(len(panel["actions"])),
                     "rmse_u1": r1, "rmse_u2": r2, "rmse_diff": rd,
                     "n_prior_dominated": est["n_prior_dominated"],
                     "n_fallback": est["n_fallback"]})
        if verbose:
            print(f"    N={N:>6}  obs={rows[-1]['n_obs']:>8}  "
                  f"rmse_u1={r1:.4f}  rmse_u2={r2:.4f}  rmse_diff={rd:.4f}  "
                  f"prior_dom={est['n_prior_dominated']}")

    logN = np.log(np.array([r["N"] for r in rows], dtype=float))
    logE = np.log(np.array([r["rmse_u1"] for r in rows], dtype=float))
    slope = float(np.polyfit(logN, logE, 1)[0])

    assert rows[-1]["rmse_u1"] < rows[0]["rmse_u1"], (
        "RMSE did not fall with N -- estimator is not consistent here")
    assert slope < -0.30, f"log-log slope {slope:.3f} not close to -0.5"
    return {"rows": rows, "loglog_slope_rmse_u1": slope,
            "GATE_1_PASS": bool(slope < -0.30)}


# ---------------------------------------------------------------------------
# T7 -- Regression test for the original NaN discretisation defect
# ---------------------------------------------------------------------------

def _original_discretise(x, n_bins=5):
    """
    Faithful reproduction of the ORIGINAL src/utils.py path:
    winsorise with np.percentile, then quantile-bin with np.percentile.
    Kept here only so the defect stays covered by a test.
    """
    x = np.asarray(x, dtype=float)
    n, d = x.shape
    xw = x.copy()
    for j in range(d):
        lo = np.percentile(x[:, j], 1.0)    # NaN-propagating
        hi = np.percentile(x[:, j], 99.0)
        xw[:, j] = np.clip(x[:, j], lo, hi)
    bins = np.zeros((n, d), dtype=np.int64)
    for j in range(d):
        edges = np.percentile(xw[:, j], np.linspace(0, 100, n_bins + 1))
        idx = np.searchsorted(edges[1:-1], xw[:, j], side="right")
        bins[:, j] = np.clip(idx, 0, n_bins - 1)
    mult = np.array([n_bins ** (d - 1 - j) for j in range(d)], dtype=np.int64)
    return bins @ mult


def test_nan_discretisation_defect_regression(n_bins=5):
    rng = np.random.default_rng(7)
    n = 4000
    states = rng.normal(size=(n, 4))
    nxt = states + rng.normal(scale=0.3, size=(n, 4))
    nxt[rng.random(n) < 0.05] = np.nan          # exits / truncated final rows

    with np.errstate(invalid="ignore"):
        orig = _original_discretise(nxt, n_bins)
    n_unique_orig = len(np.unique(orig))

    edges = ccp.make_edges(states, n_bins)      # R1: edges from time-t states
    fixed = ccp.bin_with_edges(nxt, edges, n_bins)
    n_unique_fixed = len(np.unique(fixed[fixed >= 0]))
    n_flagged = int((fixed < 0).sum())

    # The defect: every row collapses to ONE cell index
    assert n_unique_orig == 1, (
        f"expected the original path to collapse to 1 cell, got {n_unique_orig}")
    # The fix: many distinct cells, and NaN rows flagged rather than absorbed
    assert n_unique_fixed > 50, f"fix produced only {n_unique_fixed} cells"
    assert n_flagged == int(np.isnan(nxt).any(axis=1).sum())
    return {"original_unique_cells": n_unique_orig,
            "original_collapsed_index": int(np.unique(orig)[0]),
            "fixed_unique_cells": n_unique_fixed,
            "nan_rows_flagged": n_flagged}


# ---------------------------------------------------------------------------
# T8 -- the guard that was missing: catch a degenerate transition matrix
# ---------------------------------------------------------------------------

def test_transition_diagnostics_catch_degeneracy():
    K, beta = 60, 0.976
    rng = np.random.default_rng(8)
    sigma = np.column_stack([np.full(K, 0.01), np.full(K, 0.6), np.full(K, 0.39)])

    degenerate = {a: np.zeros((K, K)) for a in (1, 2)}
    for a in (1, 2):
        degenerate[a][:, K - 1] = 1.0           # all mass in one column
    healthy = {}
    for a in (1, 2):
        M = np.exp(rng.normal(size=(K, K))); M /= M.sum(axis=1, keepdims=True)
        healthy[a] = M

    d_deg = ccp.transition_diagnostics(degenerate)
    d_ok = ccp.transition_diagnostics(healthy)
    rho_deg = ccp.spectral_radius_betaM(sigma, degenerate, beta)
    rho_ok = ccp.spectral_radius_betaM(sigma, healthy, beta)

    assert d_deg[1]["n_reachable_columns"] == 1
    assert d_ok[1]["n_reachable_columns"] == K
    # The original guard passes in BOTH cases -- that is why it masked the bug
    assert rho_deg < 1.0 and rho_ok < 1.0
    return {"degenerate_reachable_columns": d_deg[1]["n_reachable_columns"],
            "healthy_reachable_columns": d_ok[1]["n_reachable_columns"],
            "rho_betaM_degenerate": rho_deg, "rho_betaM_healthy": rho_ok,
            "note": "rho(beta*M) < 1 in both cases: the original check could not detect this"}


# ---------------------------------------------------------------------------
# T9 -- sparse exits: report the degradation instead of hiding it
# ---------------------------------------------------------------------------

def test_sparse_exit_degradation(K=32, N=8000, T_max=25):
    out = []
    for rate in (0.05, 0.01, 0.001):
        m = ccp.make_mdp(K=K, seed=9, target_exit_rate=rate)
        panel = ccp.simulate(m, N=N, T_max=T_max, seed=900)
        est = ccp.run_estimator_finite(panel, m["u_exit"], K, m["beta"], kappa=EULER)
        w = est["n_k"]
        out.append({
            "target_exit_rate": rate,
            "realised_exit_rate": m["realised_exit_rate"],
            "n_prior_dominated_cells": est["n_prior_dominated"],
            "frac_prior_dominated": est["n_prior_dominated"] / K,
            "rmse_u1": ccp.weighted_rmse(est["u"][:, 0] - m["u_cont"][:, 0], w),
            "rmse_diff": ccp.weighted_rmse(
                (est["u"][:, 0] - est["u"][:, 1])
                - (m["u_cont"][:, 0] - m["u_cont"][:, 1]), w),
        })
    # Levels degrade as exits get rarer; within-continuation differences hold up
    assert out[-1]["rmse_u1"] > out[0]["rmse_u1"], "expected level RMSE to worsen"
    return {"rows": out}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

TESTS = [
    ("T1 reward-shift equivalence (Prop 1)", test_reward_shift_equivalence),
    ("T2 no constant shift under fixed anchor (Cor 1)", test_no_constant_shift_when_anchor_held_fixed),
    ("T3 continuation subproblem exact (Prop 4)", test_continuation_subproblem_exact),
    ("T4 D constant iff exit prob invariant (Prop 5)", test_discrepancy_constant_iff_exit_prob_invariant),
    ("T5 convention wedge = -beta*kappa (Prop 3)", test_convention_wedge_is_minus_beta_kappa),
    ("T6 GATE 1: recovery + consistency in N", test_recovery_consistency),
    ("T7 NaN discretisation defect regression", test_nan_discretisation_defect_regression),
    ("T8 transition diagnostics catch degeneracy", test_transition_diagnostics_catch_degeneracy),
    ("T9 sparse-exit degradation reported", test_sparse_exit_degradation),
]


def main():
    results, passed, failed = {}, 0, 0
    for name, fn in TESTS:
        print(f"\n[ RUN ] {name}")
        try:
            res = fn()
            results[name] = {"status": "pass", "detail": res}
            passed += 1
            print(f"[ PASS] {name}")
        except AssertionError as e:
            results[name] = {"status": "fail", "error": str(e)}
            failed += 1
            print(f"[ FAIL] {name}\n        {e}")
        except Exception as e:
            results[name] = {"status": "error", "error": f"{type(e).__name__}: {e}"}
            failed += 1
            print(f"[ERROR] {name}\n        {type(e).__name__}: {e}")

    print(f"\n{'='*68}\n{passed} passed, {failed} failed, of {len(TESTS)}\n{'='*68}")
    return results, failed


if __name__ == "__main__":
    _, nfail = main()
    sys.exit(1 if nfail else 0)
