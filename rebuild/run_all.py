"""
Single entry point: regenerates EVERY number and figure, and reports the two
decision gates from PROJECT_X_DECISION.md.

    python rebuild/run_all.py

Writes
------
rebuild/out/results.json   all numbers, machine-readable
rebuild/out/RESULTS.md     the same numbers formatted for the manuscript
rebuild/out/fig1_consistency.pdf
rebuild/out/fig2_convention_wedge.pdf
rebuild/out/fig3_sparse_exit.pdf

Gates
-----
GATE 1  Does the corrected estimator recover known utilities, with RMSE
        falling about as N^{-1/2} in a correctly-specified DGP?
        -> test suite T6.  If this fails, STOP: the estimator is wrong beyond
           the NaN path, and the project ships as the audit alone.

GATE 2  Is the convention wedge materially large?
        -> measured two ways: in utils (beta*kappa) and as a multiplicative
           error in exit ODDS (exp(beta*kappa)), plus the ratio of the wedge
           to the cross-state spread of recovered exit margins.
"""

import sys, os, json, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ccp
from ccp import EULER
import tests as T

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------------------
# Experiment 1 -- the convention wedge across beta  (Gate 2)
# ---------------------------------------------------------------------------

def exp_convention_wedge(betas=(0.90, 0.95, 0.976, 0.99), K=48,
                         N=4000, T_max=25, target_exit_rate=0.05):
    """
    THEORY_V12 Prop 3 predicts the wedge on continuation utilities is exactly
    -beta*kappa, independent of the data.  Verify numerically at each beta,
    and express the magnitude in units a practitioner cares about:

      * exit-margin bias, in utils          = beta*kappa
      * multiplicative error in exit odds   = exp(beta*kappa)
      * wedge relative to the cross-state spread of exit margins
    """
    rows = []
    for beta in betas:
        m = ccp.make_mdp(K=K, seed=11, beta=beta,
                         target_exit_rate=target_exit_rate)
        panel = ccp.simulate(m, N=N, T_max=T_max, seed=1100)
        e_g = ccp.run_estimator_finite(panel, m["u_exit"], K, beta, kappa=EULER)
        e_0 = ccp.run_estimator_finite(panel, m["u_exit"], K, beta, kappa=0.0)

        predicted = beta * EULER
        observed = float(np.mean(e_0["u"] - e_g["u"]))
        max_dev = float(np.max(np.abs((e_0["u"] - e_g["u"]) - predicted)))

        # Exit margins under the standard convention, u(x,a) - u(x,0)
        margins = e_g["u"] - m["u_exit"][:, None]
        spread = float(margins.std())

        rows.append({
            "beta": beta,
            "exit_margin_bias_utils": predicted,
            "exit_odds_error_factor": float(np.exp(predicted)),
            "exit_odds_error_pct": float(100.0 * (np.exp(predicted) - 1.0)),
            "observed_wedge": observed,
            "max_abs_deviation_from_prediction": max_dev,
            "exit_margin_cross_state_sd": spread,
            "wedge_over_spread": predicted / spread if spread > 0 else float("nan"),
        })
    return rows


# ---------------------------------------------------------------------------
# Experiment 2 -- Laplace sensitivity under sparse exits
# ---------------------------------------------------------------------------

def exp_laplace_sensitivity(alphas=(0.01, 0.1, 0.5, 1.0), K=32, N=8000,
                            T_max=25, target_exit_rate=0.001):
    """
    With rare exits, V_hat(k) = W_tilde(k) - ln sigma_hat(0|k) + kappa becomes
    a function of cell SAMPLE SIZE in cells with no observed exits, because
    sigma_tilde(0|k) = alpha_L / (n_k + A*alpha_L) there.  This is the
    mechanism the audit verified exactly on the SEC results (432/625 cells).
    """
    m = ccp.make_mdp(K=K, seed=12, target_exit_rate=target_exit_rate)
    panel = ccp.simulate(m, N=N, T_max=T_max, seed=1200)
    rows = []
    for aL in alphas:
        est = ccp.run_estimator_finite(panel, m["u_exit"], K, m["beta"],
                                       kappa=EULER, alpha_L=aL)
        w = est["n_k"]
        pdom = est["n_ka"][:, 0] == 0
        # Correlation between V_hat and ln(n_k) among prior-dominated cells:
        # a value near 1 means V_hat there is driven by cell size, not data.
        if pdom.sum() >= 3:
            corr = float(np.corrcoef(est["V"][pdom],
                                     np.log(w[pdom] + 1e-12))[0, 1])
        else:
            corr = float("nan")
        rows.append({
            "alpha_L": aL,
            "n_prior_dominated": est["n_prior_dominated"],
            "frac_prior_dominated": est["n_prior_dominated"] / K,
            "corr_Vhat_log_nk_prior_dominated": corr,
            "rmse_u1": ccp.weighted_rmse(est["u"][:, 0] - m["u_cont"][:, 0], w),
            "rmse_diff": ccp.weighted_rmse(
                (est["u"][:, 0] - est["u"][:, 1])
                - (m["u_cont"][:, 0] - m["u_cont"][:, 1]), w),
        })
    return {"realised_exit_rate": m["realised_exit_rate"], "rows": rows}


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def make_figures(consistency, wedge, laplace):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Fig 1 -- Gate 1 consistency
    rows = consistency["rows"]
    Ns = np.array([r["N"] for r in rows], dtype=float)
    r1 = np.array([r["rmse_u1"] for r in rows])
    r2 = np.array([r["rmse_u2"] for r in rows])
    rd = np.array([r["rmse_diff"] for r in rows])

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(Ns, r1, "o-", label=r"$\hat u(x,1)$ (maintain)")
    ax.plot(Ns, r2, "s--", label=r"$\hat u(x,2)$ (growth)")
    ax.plot(Ns, rd, "^:", label=r"$\hat u(x,1)-\hat u(x,2)$")
    ref = r1[0] * np.sqrt(Ns[0]) / np.sqrt(Ns)
    ax.plot(Ns, ref, color="grey", lw=1.0, ls="-", label=r"$N^{-1/2}$ reference")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of agents $N$")
    ax.set_ylabel("Weighted RMSE of recovered utility")
    ax.set_title("Recovery in a correctly-specified DGP\n"
                 f"log-log slope = {consistency['loglog_slope_rmse_u1']:.3f}")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1_consistency.pdf"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)

    # Fig 2 -- the convention wedge
    b = np.array([r["beta"] for r in wedge])
    bias = np.array([r["exit_margin_bias_utils"] for r in wedge])
    odds = np.array([r["exit_odds_error_factor"] for r in wedge])

    fig, (axa, axb) = plt.subplots(1, 2, figsize=(9.2, 3.8))
    axa.plot(b, bias, "o-")
    axa.axhline(EULER, color="grey", lw=1.0, ls=":")
    axa.annotate(r"$\gamma$", xy=(b[0], EULER), xytext=(4, 4),
                 textcoords="offset points", fontsize=9, color="grey")
    axa.set_xlabel(r"Discount factor $\beta$")
    axa.set_ylabel(r"Exit-margin bias $\beta\kappa$ (utils)")
    axa.set_title("Wedge in utility units")

    axb.plot(b, odds, "s-", color="C1")
    axb.axhline(1.0, color="grey", lw=1.0, ls="-")
    axb.set_xlabel(r"Discount factor $\beta$")
    axb.set_ylabel(r"Exit-odds error factor $e^{\beta\kappa}$")
    axb.set_title("Wedge in exit odds")
    for f in (fig,):
        f.suptitle("Choosing the standard Gumbel convention over mean-zero shocks",
                   y=1.04, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_convention_wedge.pdf"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)

    # Fig 3 -- sparse-exit honesty figure
    lr = laplace["rows"]
    aL = np.array([r["alpha_L"] for r in lr])
    frac = np.array([r["frac_prior_dominated"] for r in lr])
    corr = np.array([r["corr_Vhat_log_nk_prior_dominated"] for r in lr])

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(aL, frac, "o-", label="fraction of cells with no observed exit")
    ax.plot(aL, np.abs(corr), "s--",
            label=r"$|{\rm corr}(\hat V,\ \ln n_k)|$ in those cells")
    ax.set_xscale("log")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel(r"Laplace smoothing $\alpha_L$")
    ax.set_ylabel("Share / correlation")
    ax.set_title("When exits are rare, $\\hat V$ tracks cell sample size\n"
                 f"(realised exit rate {laplace['realised_exit_rate']:.4f})")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3_sparse_exit.pdf"), dpi=300,
                bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_results_md(payload):
    g1 = payload["gate_1"]
    g2 = payload["gate_2"]
    w = payload["convention_wedge"]
    base = next((r for r in w if abs(r["beta"] - 0.976) < 1e-9), w[0])
    L = []
    A = L.append
    A("# Generated results\n")
    A(f"Produced by `rebuild/run_all.py` on {payload['generated_utc']}.\n")
    A(f"numpy {payload['numpy_version']}; seeds fixed in source.\n")

    A("\n## Gate 1 — does the corrected estimator work?\n")
    A(f"**{'PASS' if g1['GATE_1_PASS'] else 'FAIL'}** — "
      f"log-log slope of RMSE on N = `{g1['loglog_slope_rmse_u1']:.4f}` "
      "(target: near −0.5).\n")
    A("\n| N | observations | RMSE u1 | RMSE u2 | RMSE (u1−u2) | cells w/o exits |")
    A("|---|---|---|---|---|---|")
    for r in g1["rows"]:
        A(f"| {r['N']} | {r['n_obs']} | {r['rmse_u1']:.4f} | {r['rmse_u2']:.4f} "
          f"| {r['rmse_diff']:.4f} | {r['n_prior_dominated']} |")

    A("\n## Gate 2 — is the convention wedge material?\n")
    A(f"**{'PASS' if g2['GATE_2_PASS'] else 'FAIL'}** at the "
      f"{g2['materiality_threshold_pct']:.0f}% exit-odds threshold.\n")
    A(f"\nAt β = {base['beta']}: exit-margin bias **{base['exit_margin_bias_utils']:.4f} utils**, "
      f"exit-odds error factor **{base['exit_odds_error_factor']:.4f}** "
      f"(**{base['exit_odds_error_pct']:.1f}%**).\n")
    A("\n| β | βκ (utils) | exit-odds factor | error % | max dev from Prop 3 | wedge / margin SD |")
    A("|---|---|---|---|---|---|")
    for r in w:
        A(f"| {r['beta']} | {r['exit_margin_bias_utils']:.4f} "
          f"| {r['exit_odds_error_factor']:.4f} | {r['exit_odds_error_pct']:.1f}% "
          f"| {r['max_abs_deviation_from_prediction']:.2e} "
          f"| {r['wedge_over_spread']:.3f} |")
    A("\nThe `max dev from Prop 3` column is the numerical check of "
      "THEORY_V12 Proposition 3: the wedge equals −βκ exactly, so these "
      "should be at machine precision.\n")

    A("\n## Laplace smoothing under sparse exits\n")
    lp = payload["laplace_sensitivity"]
    A(f"Realised exit rate {lp['realised_exit_rate']:.5f}.\n")
    A("\n| α_L | cells w/o exits | share | corr(V̂, ln n_k) there | RMSE u1 | RMSE (u1−u2) |")
    A("|---|---|---|---|---|---|")
    for r in lp["rows"]:
        A(f"| {r['alpha_L']} | {r['n_prior_dominated']} "
          f"| {r['frac_prior_dominated']:.3f} "
          f"| {r['corr_Vhat_log_nk_prior_dominated']:.3f} "
          f"| {r['rmse_u1']:.4f} | {r['rmse_diff']:.4f} |")

    A("\n## Test suite\n")
    for name, res in payload["test_suite"].items():
        A(f"- `{res['status'].upper()}` — {name}")

    with open(os.path.join(OUT, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    print("=" * 68)
    print("PROJECT X rebuild — full regeneration")
    print("=" * 68)

    print("\n--- test suite -------------------------------------------------")
    test_results, n_fail = T.main()

    print("\n--- GATE 1: recovery + consistency -----------------------------")
    gate1 = T.test_recovery_consistency(verbose=True)
    print(f"  log-log slope = {gate1['loglog_slope_rmse_u1']:.4f}  "
          f"-> GATE 1 {'PASS' if gate1['GATE_1_PASS'] else 'FAIL'}")

    print("\n--- GATE 2: convention wedge -----------------------------------")
    wedge = exp_convention_wedge()
    base = next((r for r in wedge if abs(r["beta"] - 0.976) < 1e-9), wedge[0])
    THRESH = 10.0  # an exit-odds error above 10% is treated as material
    gate2 = {
        "materiality_threshold_pct": THRESH,
        "exit_odds_error_pct_at_baseline": base["exit_odds_error_pct"],
        "GATE_2_PASS": bool(base["exit_odds_error_pct"] > THRESH),
    }
    for r in wedge:
        print(f"  beta={r['beta']:<6} bias={r['exit_margin_bias_utils']:.4f} utils  "
              f"odds x{r['exit_odds_error_factor']:.4f} "
              f"({r['exit_odds_error_pct']:.1f}%)  "
              f"max|dev|={r['max_abs_deviation_from_prediction']:.2e}")
    print(f"  -> GATE 2 {'PASS' if gate2['GATE_2_PASS'] else 'FAIL'}")

    print("\n--- Laplace sensitivity ----------------------------------------")
    laplace = exp_laplace_sensitivity()
    for r in laplace["rows"]:
        print(f"  alpha_L={r['alpha_L']:<5} no-exit cells={r['n_prior_dominated']:<4} "
              f"corr(V,ln n_k)={r['corr_Vhat_log_nk_prior_dominated']:.3f}  "
              f"rmse_u1={r['rmse_u1']:.4f}")

    payload = {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "numpy_version": np.__version__,
        "euler_gamma": float(EULER),
        "gate_1": gate1,
        "gate_2": gate2,
        "convention_wedge": wedge,
        "laplace_sensitivity": laplace,
        "test_suite": test_results,
    }
    with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=float)
    write_results_md(payload)

    print("\n--- figures ----------------------------------------------------")
    try:
        make_figures(gate1, wedge, laplace)
        print("  wrote fig1_consistency.pdf, fig2_convention_wedge.pdf, "
              "fig3_sparse_exit.pdf")
    except Exception as e:
        print(f"  figures skipped: {type(e).__name__}: {e}")

    print("\n" + "=" * 68)
    print(f"GATE 1: {'PASS' if gate1['GATE_1_PASS'] else 'FAIL'}   "
          f"GATE 2: {'PASS' if gate2['GATE_2_PASS'] else 'FAIL'}   "
          f"tests: {n_fail} failed")
    print(f"outputs in {OUT}")
    print("=" * 68)
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
