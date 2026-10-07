# PROJECT X — Independent Audit and Direction Recommendation

**Auditor role:** skeptical referee / mathematical auditor
**Material audited:** `PROJECT X.zip`, 168 files, unpacked and read
**Date:** 4 October 2026

---

## 0. Verdict up front

**The project is currently a technical/passion project (option 4), not a paper.**

Two independent findings drive this, and each is sufficient on its own:

1. **The headline theorem answers a question the field has already dissolved.** Theorem 7.1's proof is valid, but the "discrepancy" it characterises exists only because the Gumbel shocks are given location 0 (mean γ) in one model and the soft Bellman is written without `+γ` in the other. The published convention `δ = −γ_E` (mean-zero Gumbel) makes the two Bellman equations *literally identical*, absorbing exit included. This is in the current literature as a remark, not a research gap.

2. **Every computed number in the repository is produced by an estimator whose continuation value is constant across states.** A NaN-propagation defect collapses all next-period cell assignments to a single index, so the transition matrices carry no information. This invalidates the Monte Carlo, the SEC estimates, the WLS coefficients, the `D(x)` values, and both figures.

Separately: `figures/fig4_sec_utilities.pdf`, labelled "Recovered Utility Coefficients," plots the synthetic DGP's *assumed* parameters, not any estimate from any data.

**Nothing in `results/` or `figures/` should be posted, submitted, or cited.** Both stated venues have in any case closed (AAAI-27 full papers were due 28 July 2026).

**There is a real, narrow, defensible contribution in here** — see §4 — but it is a short methodological note, and reaching it requires reframing the central claim and rebuilding the computational layer. That is 4–8 weeks of focused work, not a rescue of the existing manuscript.

---

## 1. What the project actually contains

| Component | State |
|---|---|
| `MATHEMATICAL_MODELLING_V11.md` (68 KB, 663 lines) | Complete, carefully written, eight self-audit passes. Theory frozen 18 May 2026. |
| `src/` (8 modules, ~67 KB) | Complete and readable. Contains the defects in §2.2. |
| `experiments/` (7 scripts) | Incomplete — generates 5 of the 15 result files; 2 of those 5 have key mismatches with the analysis scripts. |
| `results/` (15 files) | Present, but **8 of 15 have no generating script in the repo**. |
| `figures/` | 2 of 4 planned figures. Both are invalid (§2.3). |
| `data/sec_panel.csv` | 146,985 rows. **Schema does not match `src/sec_data.py`** — the generating code is absent. |
| `references/` | 36 PDFs + 4 analysis documents. Genuinely well organised. |
| `paper/` | `outline.md` only. No manuscript exists. |
| `tests/` | 21 tests, all passing, but **none call `run_estimator`** — the integration path where the defects live is untested. |
| `.git` | **One commit** ("phase 1-2 code for kaggle"). Phases 3–4 are uncommitted. |

The theory document is the strongest artifact by a wide margin. Its self-assessment is unusually honest: it already labels Remark 7.3 "NOT novel," Theorem 6.3 "derivative," and Proposition 7.4 "mechanically straightforward." The README has not been updated to match and still advertises inflated NeurIPS-2026 framing.

**Target drift:** README says NeurIPS 2026; V11 says AAAI-27; `outline.md` is built to an 8-page NeurIPS budget. V11's header named a third party as project owner, which sits oddly against the brief's "independent research, no supervisor" framing. **Resolved 4 October 2026:** the author confirms sole authorship and no involvement by that person. **Redacted 5 October 2026** from every file in the repository. It is worth resolving before any author list is written.

---

## 2. Hostile referee audit

### 2.1 The three strongest reasons I would reject this

#### Reason 1 — The central theorem is about a normalisation choice, not about absorbing states. *(Fatal as framed; the claim must be rebuilt.)*

V11 compares

```
Gumbel-CCP :  V(x)      = γ + ln[ e^{W̃(x)} + Σ_{a≠0} e^{u(x,a) + β E[V(x')|x,a]} ]
MaxEnt soft:  V^soft(x) =     ln[ e^{W̃(x)} + Σ_{a≠0} e^{u(x,a) + β E[V^soft(x')|x,a]} ]
```

and proves no constant `c` gives `V = V^soft + c`. The algebra is correct. The framing is not.

The `+γ` appears because §A.7 assumes `ε ~ Gumbel(0,1)`, which has **mean γ**, so the agent collects an expected bonus of γ in every period it remains alive. The soft Bellman corresponds to `ε ~ Gumbel(−γ,1)` — mean zero. The two models are not two theories of the same agent; they are one theory under two shock-location conventions.

**The absorption the cited literature performs is into the reward, and it works.** Set `ũ(x,a) := u(x,a) + γ` for *every* action including exit (`ũ(x,0) = W̃(x) + γ`). Then

```
V^soft[ũ](x) = ln[ e^{W̃+γ} + Σ_{a≠0} e^{u_a + γ + β E V^soft} ]
             = γ + ln[ e^{W̃} + Σ_{a≠0} e^{u_a + β E V^soft} ]
```

which is the *same fixed-point equation* as `V`. By uniqueness of the contraction's fixed point, `V^soft[ũ] ≡ V[u]` exactly — with absorbing exit, state by state, D ≡ 0.

`VERIFICATION_REPORT.md` Item #2 reads van der Laan et al.'s "absorb the scale into `r†`" as absorption into a constant added to `V`, shows that constant does not exist, and concludes the novelty is "strengthened." That inference is backwards: `r†` is the reward, and absorption into the reward succeeds. The theorem refutes a claim nobody makes.

**This is also already published.** A current lecture note on exactly this intersection states that relative to the mean-zero equation the solution <cite index="5-1,5-2">"is shifted by the constant β(δ + γ_E)/(1 − β), so the induced softmax policy is unchanged. The clean literal equality of the DDC and unit-entropy MaxEnt-IRL Bellman equations is obtained under the paper's normalization δ = −γ_E."</cite> It goes on: <cite index="5-6">"Under λ = 1 and δ = −γ_E, the choice-specific Bellman equation and the induced policy are identical, so the two formulations are statistically indistinguishable from offline observations of (s, a, s')."</cite>

The absorbing-state angle is also occupied from the IRL side, under the name *termination/survival bias*: <cite index="11-1,11-3,11-4,11-5">the inverse Bellman operator obtained "under the assumption that the value of absorbing states is zero… may introduce termination or survival bias; the value of absorbing states also needs to be learned."</cite>

Neither source is in the project's 36-PDF reference set. Nor are Mai & Jaillet (2020), who <cite index="4-5">established that entropy-regularized MDPs and Gumbel-shock logit DDC "are equivalent in both forward-control and inverse-learning perspectives"</cite>, nor Ermon et al., credited with <cite index="7-8">first identifying the DDC/entropy-regularized-IRL equivalence</cite>.

**Fixable?** Not as stated. The *reframed* version in §4 is defensible but much smaller.

#### Reason 2 — The estimator's continuation value is constant across states, so no reported number measures what it claims. *(Fatal; mechanically fixable.)*

In `src/estimator.py::run_estimator`:

```python
next_states_w, _ = winsorise(next_states, winsor_pcts[0], winsor_pcts[1])
next_cell_ids, _, _ = discretise(next_states_w, n_bins)
```

`next_states` contains all-NaN rows by construction — `simulate_panel` writes `np.full(4, np.nan)` on exit, and `sec_robustness.py::load_sec_panel` leaves NaN for every firm's final row. `winsorise` calls `np.percentile` (not `nanpercentile`), which returns NaN when any element is NaN. The bounds become NaN, `np.clip(x, nan, nan)` makes the entire array NaN, and `discretise`'s `np.searchsorted` on an all-NaN edge array drives every bin index to its maximum. With `n_bins=5` every observation lands in cell `4·125 + 4·25 + 4·5 + 4 = 624`.

Consequence: `T_a[k, 624] = 1` for every supported cell, and `T_a[k,:] = 1/K` for the rest. So

```
Z_a(k) = β (T_a V)_k  ∈  { β·V[624],  β·mean(V) }
```

— at most two distinct values across all 625 cells. The dynamic programme is inert; `û_a(k) = Y_a(k) − const`.

Three independent signatures corroborate this, each computed from the committed results:

- **RMSE does not fall with sample size.** `N=500 → 3.5156`, `N=5000 → 3.1852`. A tenfold increase in firms buys a 9% RMSE reduction. It *rises* with panel length: `T=10 → 3.4365`, `T=80 → 4.1989`. This is specification bias, not sampling error.
- **Bootstrap coverage splits exactly as the defect predicts.** Levels: `cov_u1 = 0.2612`, `cov_u2 = 0.2319` against nominal 95%. Difference: `cov_diff = 0.9946`, with `rmse_diff ≈ 0.39` versus `≈3.4` for levels. A continuation-value error common to actions 1 and 2 cancels in `û₁ − û₂` and contaminates both levels — which is precisely what is observed.
- **`fig3` shows two razor-thin arcs, not a cloud.** Two clusters over 625 cells is the visual signature of a continuation value taking two values. The same figure puts the implied soft exit probability at **0.25–0.97 per quarter** against a DGP target exit rate of 0.001 — three orders of magnitude off.

**Epistemic status:** derived from code reading plus numpy semantics and corroborated by the three signatures above; **not yet executed**, because both compute kernels are blocked on this machine (§6). This is the first thing to run.

**Fixable?** Yes — `nanpercentile`, or mask NaN rows before binning, plus a shared bin-edge set for `states` and `next_states` (currently the two are binned against *different* percentile grids, so `T_a[k,k']` maps between two different partitions even once NaN is handled). Then every experiment must be re-run.

#### Reason 3 — The empirical application's dependent variable is unreproducible and internally inconsistent with the model. *(Fatal for the empirical claim; expensive to fix.)*

`data/sec_panel.csv` has columns `adsh, cik, date, year_quarter, Assets_Val, LIQ, LEV, ROA, SIZE, CapEx_Intensity, ACTION, SCRAP_VALUE, cik_padded`. `src/sec_data.py` writes `cik, name, period, LIQ, LEV, ROA, SIZE, action`. **The code that built the panel is not in the repository**, so the central variable cannot be audited or regenerated.

What the panel itself shows (computed directly from the CSV):

- **Exit is not absorbing in the data.** 487 rows have `ACTION=0`, spread across only **423 distinct firms** — 64 firm-quarters are coded as exits that are followed by further observations of the same firm. An absorbing state cannot be entered twice.
- **Attrition is not exit.** 1,178 firms (40.5%) are last observed in 2025, yet **zero** firms are exit-coded in 2025 and only 12 in 2024. The overwhelming majority of disappearances — right-censoring at the panel edge, delisting, acquisition, filing-status changes — are not captured, while 487 rows of unknown provenance are.
- **The date range is wrong in every document.** Actual span is **2008-12-31 to 2026-06-30**. README, V11 §G, and `outline.md` all claim "2009–2025, 68 quarters."
- **State variables violate their own definitions.** §A.1 defines `LIQ = Cash/Assets ∈ [0,1]`. The panel has 5,758 rows with `LIQ > 1` and 145 with `LIQ < 0`; 11,707 rows with `|ROA| > 1`; and **19,615 rows (13.3%) with `|LEV| > 100`**. Winsorising at the 1st/99th percentile removes 2% and cannot repair a 13% tail — which is why `sec_analysis.txt` reports cell-mean leverage of **6768.059** and **6297.490**.
- **Two-thirds of the utility estimates are the prior, not the data.** 432 of 625 cells have zero observed exits. For those cells `σ̃(0|k) = α_L/(n_k + 3α_L)`, so `V̂(k) = W̃(k) + ln(n_k + 0.3) − ln(0.1) + γ` — a deterministic function of **cell sample size**.

I verified that last point exactly. Solving `(n_k0 + α_L)/(n_k + 3α_L) = σ̂₀` for the integer exit count in all ten cells `sec_analysis.txt` highlights reproduces every printed `σ₀` to <5×10⁻⁷:

| cell | D | σ₀ reported | n_k | implied n_k0 |
|---|---|---|---|---|
| 525 | 6.7865 | 0.000048 | 2090 | **0** |
| 526 | 6.7748 | 0.000071 | 1400 | **0** |
| 531 | 6.7718 | 0.000078 | 1289 | **0** |
| 532 | 6.7660 | 0.000090 | 1117 | **0** |
| 344 | 6.7528 | 0.000117 | 855 | **0** |
| 179 | 2.3132 | 0.174603 | 6 | 1 |
| 229 | 2.5854 | 0.132530 | 8 | 1 |
| 78 | 3.1539 | 0.074205 | 28 | 2 |
| 109 | 3.4795 | 0.053040 | 77 | 4 |
| 84 | 3.5410 | 0.049759 | 62 | 3 |

The five cells with the **largest** `D` contain **no exits at all**; the five with the smallest contain one to four. The entire reported range `D ∈ [2.31, 6.79]` is spanned by cells that are either pure prior or driven by ≤4 events. The project's own output already warns that "Laplace smoothing MAY distort results for prior-dominated cells" — the distortion is total, not partial.

**Fixable?** Only by rebuilding the panel with a real exit definition (SEC Form 25/15 filings, or CRSP delisting codes), explicit right-censoring, and state variables that satisfy their definitions. That is a multi-month data project, and it would still face sparse exits, fixed β, and IIA.

### 2.2 Additional defects (not among the top three, all real)

| # | Defect | Location | Effect |
|---|---|---|---|
| D1 | DGP sets `v0 = V*(x) − exit_gap + δ(x)`, where `δ = 0.5 × z(log scrap)`. The estimator assumes `v(x,0) = W̃(x) = z(log(1+W))`. | `dgp.py:simulate_panel` | The simulation **violates the estimator's identifying normalisation**. Even with the transition defect fixed, the MC measures specification bias, not consistency. |
| D2 | `_approx_continuation_value` uses bandwidth 0.15 against grid spacing 3.0 (LEV) and 2.25 (SIZE) → `exp(−200)` weights. | `dgp.py` | The DGP has **no dynamics in LEV or SIZE** — the two variables that drive the scrap value. |
| D3 | `analyse_mc.py` reads `bl['results']`; `mc_baseline.py` writes `{'summary', 'all_results'}`. Reads `irl['all_bounds_ok']`; `mc_irl.py` writes `'bound_checks'`. | `experiments/` | The committed scripts **cannot have produced** the committed results. `mc_summary.csv` records 30 reps where `mc_irl.py` specifies 100. |
| D4 | No generator exists for `mc_bootstrap`, `mc_laplace`, `mc_nonlinear`, `mc_vary_beta`, `mc_vary_exit`, `mc_vary_T`, `sec_estimation`, `sec_irl`. | `experiments/` | **8 of 15 result files are unreproducible.** |
| D5 | Unsupported `(cell, action)` pairs get `T_a[k,:] = 1/K` silently; the count is never reported. | `utils.py:estimate_transitions` | Uniform-over-625-cells transitions injected without disclosure. |
| D6 | `check_substochastic` returns `ρ(βM) ≈ 0.976 < 1` even when `T` is degenerate. | `estimator.py` | The only numerical guard **passes under the defect**, masking it. |
| D7 | 21 tests never call `run_estimator`; `test_transitions_row_stochastic` passes NaN-free inputs. | `tests/` | "All tests pass" is true and uninformative. |
| D8 | Bounds `[γ, γ/(1−β)] = [0.577, 24.05]` vs observed `D ∈ [2.31, 6.79]`. | V11 §E.5, §G | "Bounds satisfied: True" is near-vacuous; the bracket is 4× wider than the data. Correctly flagged in V11 §G as a "loose safety net." |
| D9 | `bootstrap.py` bootstraps `u` but never `parametric_wls`. | `bootstrap.py` | The reported WLS coefficients have **no standard errors at all**. Known since the May audit; unfixed. |
| D10 | Remark 7.3's lower-bound proof assumes `D* ≥ 0`, then "bootstraps" it mid-proof. | V11 §E.5 | Conclusion holds (`T(γ) > γ`, operator monotone, Tarski applies) but as written it is circular. Presentational. |
| D11 | Thm 7.1 derives `K₁ = 0 ⟹ βc = 0` only by chaining the already-derived `e^{c−γ}=1`. Cleanly, `K₀=0 ⟹ c=γ` and `K₁=0 ⟹ c=γ/(1−β)`. | V11 §E.3 | Same conclusion, muddled derivation. Presentational. |

### 2.5 Corrections and additions after opening the pickles (4 October 2026)

Executing the code corrected two of my own findings and produced two new ones. Recorded here rather than silently patched.

**CORRECTION to D3 — I had the mismatch backwards.** I wrote that `experiments/analyse_mc.py` reads keys the pickles do not have. The opposite is true: `mc_baseline.pkl` does contain `results`, and `mc_irl.pkl` does contain `all_bounds_ok`, `all_cont_error` and `all_D`, all of which `analyse_mc.py` reads successfully. The mismatch is with the committed **generators**: `experiments/mc_baseline.py` writes `{'summary', 'all_results'}`, while the pickle on disk holds `{'K','N','T','beta','results'}`. So `analyse_mc.py` was written against the uncommitted Kaggle scripts that actually produced the results. D3's conclusion stands — the committed generators cannot have produced the committed results — but my stated mechanism was wrong.

**CORRECTION to the fig3 circularity claim.** I argued the x-axis was `sigmoid(γ − D)`, a deterministic function of the y-axis. The code would do that today, because `mc_irl.pkl` contains `all_D` and so the proxy branch triggers. But the rendered figure matches neither candidate: the saved `last_sigma_0_soft` spans [0.038, 0.641], the proxy spans [0.009, 0.021], and the figure's x-axis spans roughly [0.25, 0.97]. **The rendered figure is not reproducible from any committed artifact** — which is a different and arguably worse problem than circularity, but it is not the problem I named. Note also that the saved data does contain the genuine `last_sigma_0_soft`, so a correct version of this figure was always available; `corr(last_sigma_0_soft, last_D) = −0.993`.

**NEW — undisclosed configuration change in the headline IRL experiment.** `mc_irl.pkl` holds `all_D` with shape **(30, 81)**: 30 replications over **81 cells**. The committed `experiments/mc_irl.py` specifies `n_reps=100` and `n_bins=5`, i.e. 100 replications over 625 cells. So the paper's reported `D` range of [3.0586, 6.8653] comes from an 81-cell, 30-replication run, while the SEC application uses 625 cells. Neither `mc_summary.csv` nor `sec_analysis.txt` records the difference.

**NEW — the Laplace artefact is invariant to the smoothing parameter.** On a correctly specified simulation with a 0.1% exit rate, the correlation between `V̂` and `ln n_k` among cells with no observed exit is **0.505 at every** `α_L ∈ {0.01, 0.1, 0.5, 1.0}`. Sweeping the smoothing hyperparameter does not mitigate the cell-size dependence, because `V̂` picks up `ln(n_k + Aα_L)` whatever `α_L` is. Level RMSE is non-monotone in `α_L` (0.6400, 0.3717, 0.3910, 0.4451), so there is an interior optimum near 0.1 — but the structural dependence is untouched. The original robustness sweep over `α_L` could therefore never have detected this, which is worth saying plainly: that sweep was the project's main defence on this point and it was incapable of firing.

### 2.3 The figures

- **`fig4_sec_utilities.pdf` contains no SEC data.** `figures.py` looks for `sec_estimates.pkl`; the file on disk is `sec_estimation.pkl`. The `else` branch loads `default_true_omega()`. The rendered bars are exactly `[1.0, 0.5, −0.5, 2.0, 0.1]` and `[0.5, 0.2, −0.3, 1.0, 0.3]` — the synthetic DGP's assumed truth. The actual SEC WLS coefficients (`−5.4446 / −5.7901` intercepts, `LEV ≈ −0.0003`) appear nowhere in it. The figure is titled "Recovered Utility Coefficients." **Had this reached a referee it would read as fabricated empirical results.** It was flagged in the May 2026 session log and never fixed.
- **`fig3_D_vs_sigma0.pdf`** is sound in construction only because it took the recompute branch; had `mc_irl.pkl` been loaded, the x-axis would have been `sigmoid(γ − D)` — a deterministic function of the y-axis, explicitly commented "not exact, but illustrative." As rendered it is still invalid, for the reasons in Reason 2.

### 2.4 What is mathematically correct

To be fair to the work: Theorem 2.1, Proposition 2.4, Theorem 3.1, Theorem 3.5, Lemma 3.6, Proposition 5.2, Theorem 6.3, Theorem 4.4/4.5, Corollary 4.6 and Proposition 4.7 are all correct. I re-derived Proposition 7.2's functional equation and it is right. Proposition 7.4 is right, and its `|𝒜'|`-independence note is a genuinely careful piece of work. The numerical check `cont_err = 8.23e-07` confirms Prop 7.4 in code — the one result in `results/` that is both correct and meaningful, because it doesn't depend on the estimated transitions.

All of these are standard or derivative, and V11 says so.

---

## 3. Evidence ledger

| Claim | Status |
|---|---|
| Laplace identity reproduces all 10 reported `σ₀` to <5×10⁻⁷ | **Verified** (arithmetic, this session) |
| Panel counts, date range, LIQ/LEV/ROA violations, 487 exits / 423 firms | **Verified** (computed from `sec_panel.csv`) |
| `fig4` bars equal `default_true_omega()` | **Verified** (visual inspection vs source constant) |
| MC RMSE flat in N, rising in T; coverage 0.26/0.23/0.99 | **Verified** (read from `mc_summary.csv`) |
| `γ`-shift into the reward makes `V^soft ≡ V` under absorbing exit | **Verified** (algebra, re-derived twice) |
| Prop 7.2 derivation, Prop 7.4, Rmk 7.3 bounds | **Verified** (re-derived) |
| NaN → all `next_cell_ids = 624` → degenerate `T_a` | **VERIFIED by execution, 4 Oct 2026, on the real SEC panel.** 2,970 all-NaN next-state rows → winsorise bounds `(nan, nan)` → every winsorised next-state entry NaN → `unique next-cell indices: [624]`. A single cell, exactly the index predicted from numpy's `searchsorted` semantics before any code was run. Read directly from `results/sec_estimation.pkl`: `T[1]` has **1 reachable column** (624, 100% of mass), `T[2]` has column 624 holding **99.52%**, and `Z[:,0]` — the continuation value for Maintain — takes **exactly one distinct value, 7.701230708570058, across all 625 cells**. The published SEC estimates were produced by an estimator whose dynamic programme contributed a constant. |
| Prior art: `δ = −γ_E` normalisation (arXiv:2605.30843) | **Identifier and title confirmed; quoted passage NOT re-checkable** — the stored search result kept only titles and URLs. Reason 1 below depends on this; open the paper before relying on it. |
| Prior art: termination bias (Kostrikov 2019, LS-IQ); van der Laan et al. ×2 | **Literature-sourced** (live search; arXiv IDs 2509.21172, 2512.24407 confirmed, PDFs also in `references/`) |
| Prior art: Mai & Jaillet (2020); Ermon et al. | **Secondary attribution only** — neither primary read; trace before citing |
| Contents of the 11 `.pkl` files | **Inspected 4 Oct 2026.** See the two corrections and two new findings in §2.5. |
| Corrected estimator recovers known utilities (Gate 1) | **VERIFIED.** RMSE 0.4598 → 0.2385 → 0.1603 → 0.0548 for N = 500 → 32,000; log-log slope **−0.4890** against a target near −0.5. 9 of 9 tests pass. |
| Convention wedge equals `−βκ` (Prop 3) | **VERIFIED to machine precision** at four discount factors: max deviation 1.9×10⁻¹⁵ to 5.6×10⁻¹⁵. |

---

## 4. Three directions, compared

### Direction A — Normalisation incompatibility in absorbing-exit IRL/DDC *(research note)*

**Claim.** In an MDP with an absorbing terminal action, the anchor-action normalisation that point-identifies the DDC model and the uniform reward shift `u ↦ u + γ` that reconciles Gumbel-DDC with unit-temperature MaxEnt IRL **cannot be imposed simultaneously**. Fixing the exit utility at a measured scrap value `u(x,0) = W̃(x)` consumes the degree of freedom that the shift needs. The residual discrepancy solves the Prop 7.2 recursion, is bracketed by `[γ, γ/(1−β)]`, and — because `E[D(x')|x, exit] = 0` while `E[D(x')|x, continue] > 0` — **loads entirely on the exit margin**, the one quantity an exit application cares about.

This is the honest, survivable core of Theorem 7.1. It is a statement about an identification trade-off, not about a failure of equivalence.

- *Contribution:* names a normalisation trap and gives the closed form of the induced bias in recovered exit utilities.
- *Novelty:* modest but real. Must be positioned against the `δ = −γ_E` lecture note (arXiv:2605.30843), Kostrikov's termination bias, LS-IQ, and the two van der Laan et al. papers (arXiv:2509.21172, arXiv:2512.24407). The Mai & Jaillet (2020) and Ermon et al. attributions came via a secondary source and need tracing to the primaries.
- *Difficulty:* low. Algebra plus a small, correct synthetic illustration.
- *Compute:* seconds on CPU.
- *Empirical requirement:* none.
- *Likely objection:* "a corollary of known partial-identifiability results." Partly true; the defence is the explicit closed form and the exit-margin concentration.
- *Weakness:* thin on its own.

### Direction B — What the absorbing-state convention costs you *(methods paper)*

**Claim.** Published conventions for terminal states in soft-Bellman IRL — zero terminal value, learned terminal value, Gumbel-location normalisation, anchor-action normalisation — imply materially different recovered rewards. Quantify the divergence systematically across exit rate, horizon, discount factor, and state-space coarseness.

- *Contribution:* a clean reproducible benchmark, plus the first careful bridge between the econometrics-side normalisation question and the IRL-side termination-bias literature. Those two communities have named the same problem twice and not cited each other.
- *Novelty:* moderate. The bridge and the systematic quantification are new even though each component is known.
- *Difficulty:* moderate. Requires a correct simulator (fix D1, D2) and a correct estimator (fix Reason 2, D5).
- *Compute:* CPU-feasible; 625-cell problems solve in seconds.
- *Empirical requirement:* none — simulation only.
- *Likely objection:* "benchmark paper, limited insight." Mitigated by pairing with A's analytical result.

### Direction C — SEC firm exit as structural DDC *(empirical paper)*

- Requires: a real exit definition (Form 25/15, or CRSP delisting codes), explicit right-censoring, a rebuilt and validated state construction, and a defensible identification argument for utility *levels*.
- *Difficulty:* high — months of data work before any estimation is credible.
- *Weaknesses:* β unidentified and fixed; 0.33% exit rate; IIA across {Exit, Maintain, Growth} is implausible; and the original brief's framing ("what corporations actually optimise") is not supported by any identification strategy available here.
- **Not achievable on the current footing.** Shelve it.

### Recommendation — REVISED 4 October 2026, after verifying the prior art

**Directions A and B are both dead.** Kang (arXiv:2605.30843) was retrieved and read. His §3.2 is titled "The Anchor-Action Assumption (Magnac-Thesmar)"; his Assumption 3.3 is the anchor normalisation; he states it "fixes the location of the reward"; he names "an exit action or outside-option normalization" as the example; and his Remark 2.9 gives the `δ = −γ_E` convention and the literal equality of the two Bellman equations. Direction A's claim is a remark on his §3.2, and the `βκ` wedge is his per-step term. See `THEORY_V12.md` §6.

**Revised recommendation: Direction D — a reproducibility case study, shipped as a technical report with code (original option 4).**

The two findings Kang does not touch, and which are this project's only verified original content:

1. **Silent degeneration of cell-based CCP estimators.** NaN-valued next-period states reaching a percentile-based discretiser collapse every next-period cell index to one value, leaving the continuation value constant across states — while `ρ(βM) < 1` still passes and 21 unit tests still pass. A dynamic estimator silently becomes a static one.
2. **Laplace smoothing under rare terminal events.** In cells with no observed exit, `σ̃(0|k) = α_L/(n_k + Aα_L)`, so `V̂(k) = w(k) + ln(n_k + Aα_L) − ln α_L + κ`: the estimated value function becomes a deterministic function of cell sample size. Verified exactly on the SEC output — the five largest-`D` cells contain zero exits, and all ten reported `σ₀` reproduce from the formula to <5×10⁻⁷.

Both are concrete, both are verified, both would mislead a practitioner, and neither is in the literature as far as this audit established. That is a legitimate technical report and an honest portfolio artifact. It is not a journal paper, and it should not be dressed as one.

**Superseded recommendation, retained for the record:** pursue A and B as a single short methodological working paper (~10–12 pages), simulation-only, dropping the SEC application.

Rationale: A supplies the analytical point and B supplies the evidence that it matters, and together they are defensible without any empirical data. The SEC panel cannot support a claim right now, and attaching it would import three fatal problems into an otherwise clean note. If the panel is ever rebuilt, it becomes a *second* paper, not a section of this one.

This is a **research note / working paper (option 3)** — not a conference paper, and not a dead project.

---

## 5. Minimum work to get there

**Stage 1 — Confirm the defect (1 day, blocked on compute).** Execute the NaN path; print `np.unique(next_cell_ids)` and `T[1].sum(axis=0).nonzero()`. If it returns a single index, Reason 2 is confirmed and every result file is formally void.

**Stage 2 — Repair the computational layer (1 week).** `nanpercentile` or pre-masking; shared bin edges for `states` and `next_states`; report the count of uniform-fallback cells; make the DGP satisfy `v(x,0) = W̃(x)` exactly; widen the DGP transition bandwidth so LEV and SIZE actually move; add one end-to-end test that recovers known `u` to a stated tolerance in a correctly-specified DGP. **That test is the one that should have existed from the start.**

**Stage 3 — Re-derive the claim (1 week).** Restate Theorem 7.1 as the normalisation-incompatibility proposition of Direction A. State the converse sharply: `D` is constant **iff** the soft exit probability is state-invariant. Add the interpretation the current draft misses — `D(x)` is the entropic-risk aggregation of `γ × (discounted survival time)`, which is what makes the `[γ, γ/(1−β)]` bracket intuitive. Retire the "folk equivalence fails" framing.

**Stage 4 — Rebuild the literature position (3–5 days).** Add the `δ = −γ_E` lecture note (arXiv:2605.30843), Kostrikov et al. (2019), and LS-IQ (2023); correct the two van der Laan et al. papers to 2025 (arXiv:2509.21172, arXiv:2512.24407), which V11 dated 2026. Trace the Ermon et al. and Mai & Jaillet (2020) attributions to the primary papers — both reached this audit through a secondary source and neither has been read here. Rewrite `LITERATURE_GAP_ANALYSIS.md`'s novelty table — its six "NOVEL / High confidence" verdicts do not survive contact with these sources.

**Stage 5 — Run Direction B's sweeps (1 week).** Only after Stage 2.

**Stage 6 — Write (2 weeks).** ~10–12 pages, simulation-only.

**Total: 5–7 weeks.** No GPU, no cluster, no neural networks.

**Do not** fix `figures.py`'s filename and regenerate `fig4` from `sec_estimation.pkl`. Those SEC estimates are themselves produced by the broken estimator; a "corrected" fig4 would be just as invalid and far less obviously so.

---

## 6. Blocker (resolved)

The first pass of this audit ran without a working Python interpreter, because the
machine's application-control policy blocked the one available. The transition defect was
therefore marked *derived* rather than *verified* at that stage.

**Resolved 4 October 2026.** A signed interpreter was installed, the defect was executed
against the real 146,985-row panel, and the binary result files were opened and inspected.
Every finding in this document is now marked according to what was actually run. See
`docs/TRACEABILITY.md`.

---

## 7. CV and publication strategy

### What is truthful today

> **Independent research project** — structural estimation and inverse reinforcement learning; dynamic discrete choice with absorbing exit. *(2026)*

That is accurate and you may use it now. **"Working paper," "preprint," "manuscript in preparation," and "under review" are all currently false.**

### Earliest truthful upgrades

| Milestone | Requires | Realistic timing |
|---|---|---|
| **Manuscript in preparation** | Stages 1–4 done, draft started | ~4 weeks |
| **Working paper / preprint** | Stages 1–6, posted to arXiv (econ.EM or stat.ML) | ~7 weeks |
| **Under review** | Submitted somewhere | ~8 weeks |

arXiv listing is the right first target: it is a real, citable, honestly-labelled artifact, it timestamps the contribution, and it costs nothing but correctness.

### Venues, by realism

- **Near-term, realistic:** arXiv preprint (econ.EM / stat.ML). Then a workshop with archival proceedings at a 2027 ML conference — the normalisation-trap result is exactly workshop-shaped.
- **Ambitious but defensible if B is strong:** a methods-oriented ML venue in the 2027 cycle. **AAAI-27 closed on 28 July 2026**; AAAI-28 opens around summer 2027.
- **Longer-term journal:** if the note grows a genuine econometric contribution, *Journal of Applied Econometrics* or *Econometric Reviews* would fit better than a general-interest econ journal. Not yet.

Do not aim at NeurIPS/ICML main tracks with this. The contribution is a clarification, and those venues reject clarifications.

---

## 8. Challenges to your framing

1. **"Is the discrepancy genuinely state dependent?"** — Yes, conditional on refusing the standard normalisation. The right question is not whether `D` varies with `x` but whether the convention that generates `D` is one anyone should adopt. Once asked that way, the theorem becomes a cautionary note.

2. **Eight audit passes verified citations to the page number and never checked whether the code computed the mathematics.** `VERIFICATION_REPORT.md` confirms AM 2011's Eq (3.5) is at the bottom of p. 1834. No pass asked whether `Z_a(k)` varied across `k`. Rigour was spent on the most checkable surface rather than the load-bearing one — worth noticing as a process lesson, not just a one-off.

3. **"No prior IRL paper on this exact setting" is true and weak.** Absence of a prior paper on SEC firm exit is not evidence of a contribution; it is more often evidence that the identification problem is hard. Treat novelty-of-setting as near-zero credit.

4. **The brief asked what capitalism optimises. The project cannot answer that, and should stop implying it can.** Recovering `u(x,a)` up to a fixed `β`, a fixed shock distribution, an assumed scrap value, and an anchor normalisation, from a 625-cell discretisation with 487 exit events of unknown provenance, does not identify corporate objectives. Narrowing to the methodological question was the right call; the narrowing should now be made explicit in the writing.

5. **Preserve, don't overwrite.** Keep the current `results/` and `figures/` as a dated `v0_invalid/` the original project rather than deleting them. They are the evidence for why the rebuild was necessary, and that record is worth keeping.
