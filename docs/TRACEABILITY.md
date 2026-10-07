# Traceability

**Aditya Maiti.** Companion to *Two failure modes in cell-based CCP estimation of dynamic discrete choice models*.

Every quantitative claim and every reference attribution in `REPORT.md`, `docs/CHAPTER_1_THE_MODEL.md` and `docs/CHAPTER_2_THE_CODE.md` is listed here with the file that produces or supports it. Compiled 5 October 2026.

An automated check backs this up. Every multi-digit numeral in the three documents was extracted and matched against `rebuild/out/results.json`, `rebuild/verify_math.py`, and the shipped evidence files below. The numerals not matched are DOI prefixes, arXiv identifiers, and intermediate arithmetic shown inside worked examples.

---

## 1. Mathematical statements

Run `python rebuild/verify_math.py`. It exits non-zero if any check fails. **49 checks, all passing.**

The full console output of the run behind this table is committed as
`rebuild/out/verify_math_output.txt`, so the per-check deviations and the diagnostic ranges
quoted anywhere in this repository can be read off a file rather than taken on trust. The run
reports `sigma_0` spanning `[0.0354, 0.3894]` at check B0 and the discrepancy spanning
`[6.5635, 7.0231]` with standard deviation `0.123932` at checks B4 and B5b, inside the bracket
`[0.5772, 11.5443]`.

| Statement | Where it is used | Check |
|---|---|---|
| Gumbel mean is `δ + γ` | CH1 1.2.2 | A1, Monte Carlo |
| Max-stability of the Gumbel | CH1 1.2.2 | A2, sup-norm on the CDF |
| Lemma 0, `E[max] = κ + LSE` | CH1 1.2.4, THEORY | A3, B2 |
| Logit choice probability | CH1 1.2.3 | A4, simulated argmax |
| CH1 worked example, all four figures | CH1 1.2.3, 1.2.4 | A5 |
| Lemma 1, the Bellman operator is a `β`-contraction | CH1 1.3.2 | B1 |
| Proposition 1, conventions are reward shifts | CH1 1.6.1, REPORT | B3, B3b |
| Corollary 1, no constant shift under a fixed anchor | CH1 1.6.2 | B4, with a B0 guard that exit probability varies |
| Corollary 2, the constant exists iff exit probability is state invariant | CH1 1.7.4 | B7a, B7b |
| Proposition 5, recursion and the `[γ, γ/(1−β)]` bracket | CH1 1.7.4 | B5, B5b |
| Proposition 4, `γ/(1−β)` with no terminal action | CH1 1.7.4 | B6 |
| (INV) | CH1 1.4.1, CH2 2.5 | C1 |
| Arcidiacono-Miller Lemma 1 form | CH1 1.4.3 | C2 |
| (TARGET) and (RECOVER) recover the truth exactly | CH2 2.5 | C3, C3b |
| Proposition 3 (a) through (e) | CH1 1.7.3, REPORT | C4a to C4e |
| Proposition 2, incompatibility, both arms | CH1 1.7.2 | C5 |
| The `βκ` table, all four rows | CH1 1.7.3 | C6 |
| `γ/(1−0.976) = 24.050653` | CH1 1.7.4 | C6b |
| The Laplace identity | CH1 1.9, CH2 2.3.3 | D1 at four cell sizes |
| `4.1431`, `9.9476`, `5.8045` | CH1 1.9, CH2 2.3.4 | D1b, D1c, D1d |
| `estimate_ccps` matches its documented formula | CH2 2.3.1 | D2, D2b |
| `np.percentile` returns NaN edges | CH2 2.2.3 | D3a |
| The repaired path flags rather than collapses | CH2 2.2.6 | D3b, D3c |
| The spectral radius cannot separate the two cases | CH2 2.7.2 | D4 |
| `transition_diagnostics` can | CH2 2.7.4 | D4b |
| One reachable column makes continuation values constant | CH2 2.2.4 | D5 |

**A note on how this suite was built.** Its first run failed one check, B4, which asserted that the discrepancy is not constant under a fixed anchor. The random test MDP had drawn exit utilities so far below the continuation values that exit was never chosen, which made the exit probability state invariant and so, by Corollary 2, forced the discrepancy to be constant. The mathematics was right and the test was vacuous. Check B0 now guards against this by asserting the exit probability spans a real range before the constancy tests run.

---

## 2. Reported numbers from the corrected estimator

All produced by `python rebuild/run_all.py`, which writes `rebuild/out/results.json` and `rebuild/out/RESULTS.md`. Seeds are fixed in source.

| Number | Key in `results.json` |
|---|---|
| Gate 1 log-log slope `−0.4890` | `gate_1.loglog_slope_rmse_u1` |
| RMSE table, all 16 entries | `gate_1.rows[*].rmse_u1`, `.rmse_u2`, `.rmse_diff` |
| Observation counts, cells without exits | `gate_1.rows[*].n_obs`, `.n_prior_dominated` |
| Gate 2 exit-odds error `75.7%` | `gate_2.exit_odds_error_pct_at_baseline` |
| Wedge table, deviations from Proposition 3 | `convention_wedge[*].max_abs_deviation_from_prediction` |
| Laplace sensitivity table | `laplace_sensitivity[*]` |
| Test statuses T1 to T9 | `test_suite.*` |

**Reproduction check.** On 4 October 2026 the published code was re-run from a clean copy of `rebuild/` and the output compared key by key against the committed `results.json`. Of 186 values, 185 were identical. The only difference was the generation timestamp.

---

## 3. Numbers from the withdrawn original work

These appear in the report as evidence of the defects. The binary results are declared invalid in `WITHDRAWN_OUTPUTS.md` and are not version controlled, so the readable extracts below are tracked instead.

| Number | Source file in the repository |
|---|---|
| `7.701230708570058`, the constant continuation value | `evidence/degenerate_transitions_evidence.txt` |
| `T[1]` has 1 reachable column, index 624, 100% of mass | same |
| `T[2]` has column 624 at `0.995208` of mass | same |
| `Z[:,0]` has exactly 1 distinct value across 625 cells | same |
| The ten reported `σ₀` values, `0.000048` to `0.174603` | `evidence/sec_analysis.txt` |
| Original Monte Carlo RMSE, `3.5156` at `N=500` to `3.1852` at `N=5000` | `evidence/mc_summary.csv` |
| Original bootstrap coverage `0.2612`, `0.2319`, `0.9946` | same |
| 432 of 625 cells with no observed exit | `evidence/sec_analysis.txt` |
| Panel counts: 146,985 rows, 2,970 all-NaN, 2,906 firms, 487 exit rows | `data/sec_panel.csv`, not version controlled, 24 MB. Counts were executed against it on 4 October 2026 and are not independently reproducible from this repository. |

The last row is an honest gap. The panel is too large to ship and the code that built it is absent, which is itself one of the audit findings.

---

## 4. Reference attributions

Each claim was checked on 4 and 5 October 2026 against the source named in the right column.

Short codes such as `F02` and `00a` identify PDFs in the author's local reading library, which
is catalogued in `references/INDEX.md`. Those are third-party copyrighted works and are not
redistributed here, so the codes will not resolve to files in this repository. The full title,
authors and DOI of every one of them is in the reference list of `REPORT.md`, which is where a
reader should go to obtain them.

| Claim as stated | Verified against |
|---|---|
| Rust (1987) gives the value function with extreme value shocks | **Secondary.** The copy in `references/` is a scan with no text layer. Arcidiacono and Miller (2011) Section 2.2 states the log-sum-exp conditional value function and attributes it to Rust (1987). |
| Hotz and Miller (1993) give the inversion | `references/F02`, their Proposition 1 and the surrounding text on invertibility |
| Magnac and Thesmar (2002) show these models are not identified, determine the exact degree of underidentification, and name three parameters that must be set including preferences in one reference alternative | `references/F04`, abstract and introduction |
| Arcidiacono and Miller (2011) Lemma 1 gives a function of the choice probabilities equal to `V − v_k`, and Theorem 1 uses it | `references/00a`, Lemma 1 and Theorem 1 |
| Rust (1997) proves randomised algorithms break the curse of dimensionality for discrete decision processes | `references/F07`, abstract and keywords |
| McFadden (1974) proved the converse, that the logit formula implies extreme value unobserved utility | `references/F13`, Train (2009) Chapter 3, which states this history |
| Ziebart et al. (2008) derived the recursion from a maximum entropy principle, in partition-function form, applied to driver route modelling | `references/F03`, abstract and Algorithm 1 |
| Haarnoja et al. (2017) use this in soft Q-learning | `references/F10`, abstract and Section 3 |
| Cao, Cohen and Szpruch (2021) resolve non-identifiability under entropy regularisation | `references/05`, abstract |
| Kostrikov et al. (2019) show imitation learning methods assign zero reward to absorbing states, often implicitly, that this biases the policy, and that their remedy is to learn that reward | arXiv:1809.02925 full text, Sections 4.1 and 4.2 |
| Kang (2026) states the normalisation result and the Anchor-Action Assumption, and names an exit action as the example | arXiv:2605.30843 full text, Remark 2.9 and Section 3.2 |

### Corrections made on 5 October 2026

Five attributions were wrong or imprecise and have been fixed.

1. **Kostrikov.** The report said "treating the **value** of absorbing states as zero" and credited the remedy to "**later work**". The paper says zero **reward**, assigned implicitly, and it is that same paper that learns it.
2. **Ziebart.** Chapter 1 said they "came at this from **robotics**". The word robot does not appear in the paper. It is driver route modelling, applied to 100,000 miles of taxi GPS data.
3. **McFadden.** Chapter 1 said he "derived" the logit formula in 1974. Train's own account is that the extreme value to logit direction is older and McFadden proved the converse.
4. **Rust (1997).** The report said it "covers discretisation bias". It proves randomised algorithms break the curse of dimensionality for discrete decision processes.
5. **Ziebart's recursion.** Chapter 1 said the soft Bellman equation "falls out" of the maximum entropy principle. The paper states it in exponentiated partition-function form. Taking logarithms gives the soft recursion.

### Withdrawn citations

| Citation | Status |
|---|---|
| Geng et al. (2020) | **Withdrawn.** No locatable paper. |
| Mai & Jaillet (2020) | **Withdrawn.** No locatable paper. The nearest match is Bui, Mai and Jaillet (2022), arXiv:2208.09611, with a different lead author and year. |
| Ermon et al. | **Untraced.** Reached the project through a secondary source and never pinned to a paper. Not relied on in `REPORT.md`. |
| LS-IQ (2023) | **Corrected**, not withdrawn. Now cited as Al-Hafez, Tateo, Arenz, Zhao and Peters (2023), arXiv:2303.00599. |

### Known limits of this check

- **McFadden (1974)** itself is a scan with no text layer. The attribution rests on Train (2009) Chapter 3, which is machine-readable and states it.
- **Rust (1987)** is likewise a scan. The attribution rests on Arcidiacono and Miller (2011) Section 2.2.
- The six documents in `references/` dated 18 May 2026 carry superseded novelty verdicts. Each has a notice at the top saying so. They are retained as a record of what the project believed before the prior art was checked, not as current findings.

---

## 5. What is not traceable

Stated plainly, because the point of this file is to be complete rather than reassuring.

1. **The SEC panel itself.** 24 MB, not version controlled, and the script that built it is absent. Every count taken from it was executed on 4 October 2026 but cannot be regenerated from this repository. No claim in `REPORT.md` depends on the panel being correct, because the empirical application is withdrawn.
2. **The original project's binary results and development record.** Declared invalid in `WITHDRAWN_OUTPUTS.md` and retained privately by the author rather than published. The three readable extracts above are the parts the report relies on.
3. **Figure 3 of the original project.** Its rendered x-axis matches no saved array. It is not reproducible from any committed artifact. This is recorded in `PROJECT_X_AUDIT.md`. The figure is retained privately and is not published.
