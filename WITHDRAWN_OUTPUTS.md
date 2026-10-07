# Withdrawn outputs — retained for the record, not for citation

Everything in this directory was produced by the pre-audit implementation and is
invalid. It is kept unmodified because it is the evidence for why the rebuild was
necessary.

**Do not cite, reuse, or report any number or figure from this directory.**

## Why

1. **Degenerate transition matrices.** NaN-valued next-period states reached
   `np.percentile`, which returns NaN; the NaN propagated through `np.clip` and
   `np.searchsorted` and collapsed every next-period cell index to a single
   value. The continuation value was therefore constant across states, so the
   estimator was not solving a dynamic problem. This invalidates every Monte
   Carlo number, every SEC estimate, the WLS coefficients, and the computed
   D(x). Reproduced and fixed in `rebuild/tests.py::test_nan_discretisation_defect_regression`.

2. **Separate bin edges for t and t+1.** The two periods were binned against
   different percentile grids, so T_a[k,k'] mapped between two different
   partitions of the state space.

3. **A mis-specified DGP.** The simulation set v(x,0) = V*(x) - exit_gap +
   delta(x) while the estimator assumed v(x,0) = W_tilde(x). The Monte Carlo
   therefore measured specification bias, not sampling error, which is why RMSE
   did not fall with N and rose with panel length.

4. **fig4_sec_utilities.pdf contains no SEC data.** The figure script looked for
   `sec_estimates.pkl`; the file on disk was `sec_estimation.pkl`, so the
   fallback branch loaded the synthetic DGP's assumed parameters and plotted them
   under the title "Recovered Utility Coefficients".

5. **Unreproducible results.** Eight of fifteen result files had no generating
   script in the repository, and two of the five that did had key names
   incompatible with the analysis scripts that read them.

6. **The SEC exit variable.** No code in the repository produces the panel's
   schema. 487 exit rows span only 423 firms, so some firms exit more than once
   from a state that is supposed to be absorbing. 1,178 firms are last observed
   in 2025 with none coded as exits. 432 of 625 cells contain no observed exit,
   making the estimated value function a deterministic function of cell sample
   size there.

See `../PROJECT_X_AUDIT.md` for the full defect register and the arithmetic.
