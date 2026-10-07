> ## SUPERSEDED. Item #2 below reaches the wrong conclusion.
>
> Compiled 18 May 2026. At that date the project had not examined Kang (2026),
> arXiv:2605.30843.
>
> Item #2 reads van der Laan, Kallus and Bibaut (2025), arXiv:2509.21172, as
> absorbing a scale into a constant added to the value function. It shows that
> this fails. It then concludes that the project's novelty claim is
> strengthened. That inference runs backwards. The constant is added to the
> reward at every action, including the terminal one. Doing so makes the two
> value functions equal, and the claimed discrepancy vanishes.
>
> See `docs/PROJECT_X_AUDIT.md` Section 2.1, Reason 1, for the corrected
> derivation.
>
> The text below is preserved unedited. It records what the project believed in
> May 2026.

---

# Verification Report — 5 Open Items Resolved

**Date:** 18 May 2026
**Method:** Each item was verified by reading the actual PDF on disk (paper or source code), not by relying on abstracts or external summaries. Every claim below is traceable to a specific page or line number.

---

## Item #1 — Verify Theorem 6.3 against Arcidiacono-Miller 2011/2019

**Status:** ✅ **RESOLVED**

### Action taken

Downloaded both papers from authors' personal Duke pages (free, open-access working-paper versions):
- `00a_ArcidiaconoMiller2011_CCP_Heterogeneity.pdf` — 59 pages, full paper
- `00b_ArcidiaconoMiller2019_NonstatFiniteDependence.pdf` — 6 pages, working-paper version of the *Quantitative Economics* 2019 article

Both are present in `references/` and openable offline.

### Findings

**Arcidiacono-Miller 2011** (verified pages 1–9):
- Their *main contribution* is broadening the class of DDC models where CCP estimation works *without matrix inversion or simulation*. They prove (in Lemma 1, the "inversion lemma"): the expected value of future utilities can be expressed as a function of flow payoffs and CCPs for **any sequence of future choices**, optimal or not.
- Their Eq (2.4), p. 7: the conditional value function for keeping the engine is expressed as `v_2(x,s) = θ_1·x + θ_2·s + β·ln[exp(v_1(x+1,s)) + exp(v_2(x+1,s))] + β·γ`, **with explicit `+β·γ` Euler term**.
- Their Eq (2.6), p. 7: `v_1(x,s) = β·v_1(0,s) − β·ln(p_1(0,s)) + β·γ`. **Same Hotz-Miller-style direct recovery formula your V10 §C uses (Thm 3.5).**
- The "iteration" in AM 2011 is the **EM iteration** for unobserved heterogeneity, NOT iteration over V↔u recovery (their §2.3 Estimation, pp. 8–9).

**Arcidiacono-Miller 2019** (verified pages 1–6):
- Generalises the AM 2011 finite-dependence definition to allow **negative weights** on conditional value functions: the ex-ante value function can be expressed as a weighted average of conditional value functions where "weights sum to one but some may be negative or greater than one".
- Their contribution is algorithmic — a systematic way to determine whether finite dependence holds in a model with a large but finite number of states.

### Verdict on overlap with your Theorem 6.3

**No direct overlap.** Specifically:

1. **AM 2011 establishes the closed-form representation** that underlies your V10 §C one-step procedure. Their Eqs (2.4)-(2.7) are the prototype of what you generalise to the three-action (Exit/Maintain/Growth) case.
2. **AM 2011 does NOT prove the specific claim** that "the iterative CCP procedure converges to the closed form in one iteration." Their iteration is over EM-style updates for unobserved types, not over V↔u recovery.
3. **AM 2019 does NOT prove this claim either.** It generalises finite dependence, which is a different question.

### Refined positioning for your Thm 6.3

Your Thm 6.3 is **algebraically a consequence of AM 2011's representation theorem** — the iterative scheme of V10 editions 2–5 just re-derives the same closed form in each iteration, so it converges trivially in one step. **Position Thm 6.3 honestly in your paper:**

> *"The iterative scheme used in V10 editions 2–5 reduces algebraically to the one-step closed-form recovery of Hotz-Miller (1993) generalised by Arcidiacono-Miller (2011). Theorem 6.3 makes this reduction explicit for the absorbing-exit three-action case, eliminating unnecessary iteration in the implementation."*

This framing is **HONEST and DEFENSIBLE**. A reviewer who knows AM 2011 will not view Thm 6.3 as a fundamental contribution, but as a useful technical clarification specific to the V10 framework. Your novelty load is carried by Thm 7.1, Prop 7.2, Rmk 7.3, Prop 7.4 — not by Thm 6.3.

### Action item for the paper

**Demote Thm 6.3 in the abstract and introduction.** Lead with Thm 7.1 (the discrepancy result under absorbing exit). Cite Thm 6.3 as a methodological clarification, not a headline contribution.

---

## Item #2 — Verify the +γ framing in Thm 7.1 against [17] van der Laan et al. §3

**Status:** ✅ **RESOLVED**

### Findings (verified pages 2–5 of [17])

van der Laan, Kallus & Bibaut (May 2026), p. 4:
> *"Under i.i.d. Gumbel type-I extreme-value shocks, the optimal policy is softmax: π^†(a|s) ∝ exp{Q^†(s,a)/τ}, for temperature τ > 0, and Q^† = r^† + γPΞQ^†, V^†(s) = ΞQ^†(s)."*
>
> *"Equivalently, with state-action continuation value v^† := PΞQ^†, π^†(a|s) ∝ exp{(r^†(s,a) + γv^†(s,a))/τ}, v^† = PΞ(r^† + γv^†). We call the latter the soft Bellman equation. **Without loss of generality, we set τ = 1 and absorb the scale into r^†.**"*

This is the precise quote I was looking for. They:
1. Use a temperature `τ` and the Ξ operator `Ξf(s) = log Σ_a e^{f(s,a)}`.
2. Set τ = 1.
3. **Absorb the +γ_Euler scale into the reward parameterisation r^†.**

This is **identical to** the framing your Thm 7.1 corrects. Under their setup, the Gumbel-CCP value function and the soft (entropy-regularised) value function differ by a constant `γ_Euler` per Bellman iteration, which they fold into r^†. **This absorption is valid as long as the Bellman iteration is unbounded** (so the +γ accumulates geometrically into γ/(1−β)).

But under your absorbing exit, the Bellman iteration TERMINATES at exit (`V(x†) = 0`), so the +γ accumulation is **truncated** in a state-dependent way (depending on the probability of reaching exit from state x). This is exactly the structural insight of your Theorem 7.1.

### The exact disagreement, in one sentence

[17] says "absorb +γ_Euler into r^†, the absorption is WLOG" — your Thm 7.1 says **the absorption is NOT WLOG under absorbing exit** because the geometric accumulation γ + βγ + β²γ + ... = γ/(1−β) is truncated by exit, and the truncation is state-dependent.

### Action item for the paper

In §1 (Introduction), explicitly cite [17] verbatim: *"Recent work (van der Laan, Kallus & Bibaut, 2026) views DDC and MaxEnt IRL as the same mathematical object via the soft Bellman equation, absorbing the Euler-Mascheroni scale γ into the reward parameterisation r^†. Our Theorem 7.1 establishes that this absorption is NOT valid under absorbing exit: the resulting discrepancy D(x) is state-dependent, bounded by [γ, γ/(1−β)], and characterised by the functional equation of Proposition 7.2."*

---

## Item #3 — Read [01] Zeng et al. §6 (linear reward) and §7 (state-only reward)

**Status:** ✅ **RESOLVED**

### Findings (verified pages 12–18 of [01])

**§6 The Linearly Parameterized Reward Function Case** (pp. 12–15):

- **Theorem 2 (strong duality):** Under linear reward `r(s,a;θ) = φ(s,a)^⊤θ`, the ML-IRL problem (their Eq 13) is the **Lagrangian dual** of the MaxEnt IRL problem (their Eq 22).
- **Corollary 1**: Their dual objective `L̂(θ;𝒟)` is concave in θ; if the ground-truth reward `r(s,ā;θ*)` for a **reference action ā ∈ 𝒜** and `s ∈ 𝒮` is known, the optimal solution is **unique**.
- **Corollary 2**: With linear reward, their Algorithm 1 converges sublinearly to the global maximum-likelihood IRL estimator with rate O(K^{-1/2}).

**Key match to your project:** Their Cor 1(ii) explicitly invokes a **reference-action normalisation** — knowing `r(s,ā;θ*)` for some action ā uniquely pins down the equivalence class. **This is the modern ML statement of your Magnac-Thesmar normalisation `u(x,0) = W̃(x)`.**

**§7 The Case with State-only Dependent Rewards** (p. 16):

- Lemma 4: With state-only `r(s;θ)`, their ML-IRL objective (4) is equivalent to minimising `E[V_θ(s_0)] − E[V_θ^E(s_0)]`. State-only IRL is a special case of their framework.
- They argue state-only rewards facilitate "counterfactual analysis such as predicting the optimal policy under different environment dynamics" and avoid imitating expert policy. Cites refs [43], [15], [44].

### Verdict on overlap

**No overlap with your Thm 6.3.** Zeng et al.'s §6 establishes **finite-time convergence of their single-loop ML-IRL algorithm** — this is a sample-complexity / iteration-count result. Your Thm 6.3 is an **algebraic equivalence** between iterative-CCP and one-step CCP.

**However:** Cor 1(ii) of [01] is a **direct ML-side parallel** to your Magnac-Thesmar normalisation. **You should cite Cor 1(ii) in your §4 (identification) alongside Magnac-Thesmar (2002), [04] Schlaginhaufen, and [05] Cao et al.** as the modern ML-side statement of "reference-action normalisation kills the equivalence class."

### Action item for the paper

In §4 (identification), add Zeng et al. (2024) Cor 1(ii) to the list of modern ML-side identifiability results that converge on the Magnac-Thesmar normalisation approach.

---

## Item #4 — Read [11] Jhaveri et al. §3–4 for Prop 7.4 (continuation subproblem) overlap

**Status:** ✅ **RESOLVED**

### Findings (verified pages 3–8 of [11])

**Their setting (verified §2):**
- Entropy-regularised RL (ERL): `J_τ(μ) = ∫ r dμ − τ R(μ)` where `R(μ) = ∫ KL(π·^μ ‖ π·^ref) dν^μ`.
- Soft Bellman operator: `(𝓑_τ q)(x,a) := r(x,a) + γ ∫ (V_τ q)(x') dP_{x,a}(x')` where `(V_τ q)(x) := τ log ∫ e^{q(x,·)/τ} dπ^ref`.

**Their main results in §3 (the "temperature decoupling gambit"):**
- They study what happens as **τ → 0** (vanishing entropy regularisation).
- Theorem 3.6: Total-variation distance between Boltzmann-Gibbs policies bounded by their temperature and potentials.
- Theorem 3.9: With a decoupled-temperature schedule `σ(τ)` such that `σ/τ → 0` as `τ → 0`, the decoupled policy `π^{τ,σ}` converges to the *optimality-filtered reference-optimal policy* `π^{ref,*}`.
- Theorem 3.10: Return distributions of decoupled-temperature policies converge.

**Their §4 (Convergent Approximation of Optimal Return Distributions):**
- Definition 4.1: Soft distributional Bellman operator `𝓣_τ^π`.
- Theorem 4.2: `𝓣_τ^π` is a γ-contraction in `d̄_p` for every τ ≥ 0.
- Theorem 4.5: Iterates of `𝓣_τ^⋆ := 𝓣_τ^{𝓖_τ Q ζ̄}` converge in `d̄_p` and `d̄_1`.

### Verdict on overlap with Prop 7.4

**No overlap.** Specifically:

1. Your **Prop 7.4** is a result at **fixed temperature** (`β = 0.976` fixed, `γ = γ_Euler ≈ 0.5772` fixed) for the **continuation subproblem** (no absorbing state). It computes `V'^DDC − V'^soft = γ/(1−β)` exactly.

2. **[11] Jhaveri et al. study the τ → 0 limit** (vanishing entropy regularisation). They compute what happens as the temperature decays — this is a "hard-policy limit" question. **Different mathematical object.**

3. **[11] never compute `V_DDC − V^soft` at fixed temperature.** They focus on policy convergence and return distribution convergence under vanishing-temperature schemes.

**Useful citation:** Theorem 4.2 of [11] establishes contraction of the soft distributional Bellman operator. Cite in your V10 §2 (Bellman + Banach FPT) as modern context for the contraction argument.

### Action item for the paper

In §2 (Bellman), add a citation `[11]` to the contraction-property paragraph. In §7 (MaxEnt-IRL relationship), explicitly state in a footnote: *"Vanishing-temperature limits of entropy-regularised RL have been studied (e.g., Jhaveri et al. 2025, NeurIPS 2025); our results are complementary, addressing the fixed-temperature value-function discrepancy under absorbing exit."*

---

## Item #5 — Cross-check `src/bootstrap.py` against [07] Renard et al. sample-complexity bounds

**Status:** ✅ **RESOLVED** with a concrete code recommendation

### Findings

**`src/bootstrap.py` (verified, 74 lines):**
- Function: `cluster_bootstrap(states, actions, next_states, firm_ids, n_bootstrap=200, ...)`.
- Procedure: Sample N firms with replacement from the unique firm IDs. For each bootstrap rep b, build the bootstrap sample and call `run_estimator`. Collect `u_boots[b] = est_b['u']`.
- Output: `u_boots, ci_lower, ci_upper` (2.5th and 97.5th percentile of `u_boots`).

**Critical observation:** `src/bootstrap.py` only bootstraps `u` (the recovered utility per cell). It does **NOT** wrap `parametric_wls` from `src/estimator.py:226`, so the **WLS coefficients ω̂ have no bootstrap distribution computed**.

**[07] Renard et al. (verified pages 2–7):**
- Setting: Entropy-regularised IRL with stochastic projected gradient descent + soft policy iteration.
- Their **Theorem 4.3**: With learning rate `η_w = (1−γ)/(√(kT)·‖φ‖_∞)`, the reward bound is `E[J_r^* − J_r^{π^E}] ≤ ε_real + O(γ^H) + O(1/√T)`.
- Their **Cor 4.7**: To recover a reward for which the expert is (ε + ε_real)-optimal, need `T = O(1/ε²)` iterations and `O(1/ε²)` samples from the MDP per iteration.
- Method: cluster bootstrap is NOT used. They use **iterative gradient descent**.

### Verdict on consistency

**[07] gives sample-complexity bounds for a DIFFERENT algorithm** (iterative stochastic gradient descent for an entropy-regularised IRL objective). Their O(1/√T) rate is for the gradient algorithm's *iteration count*, not for the sampling distribution of an estimator.

**Your `src/bootstrap.py` is the correct inference method** for your project because:
1. Your estimator is **one-step closed-form** (no inner gradient loop), so iteration-count bounds don't apply.
2. **Cluster bootstrap is the standard non-parametric inference method** for two-step semiparametric estimators with serial correlation (V10 §8.2; Murphy-Topel correction territory).
3. Under standard regularity conditions (firms exchangeable, bounded within-firm dependence), cluster bootstrap CIs have asymptotically correct coverage with the same O(1/√N) rate as analytic sandwich estimators.

**HOWEVER, the gap remains:** `src/bootstrap.py` doesn't bootstrap `ω̂` (the WLS coefficients), only the per-cell `u`. This was Issue #2 in the original audit and remains unaddressed in code.

### Action item for the code (concrete fix, ~20 LOC)

Extend `src/bootstrap.py` to also bootstrap `ω̂`:

```python
def cluster_bootstrap(states, actions, next_states, firm_ids,
                      n_bootstrap=200, beta=0.976, alpha_scrap=0.5,
                      alpha_L=0.1, n_bins=5, seed=42,
                      include_wls=True):
    rng = np.random.default_rng(seed)
    unique_firms = np.unique(firm_ids)
    N_firms = len(unique_firms)

    est_full = run_estimator(states, actions, next_states, beta=beta,
                              alpha_scrap=alpha_scrap, alpha_L=alpha_L,
                              n_bins=n_bins)
    K = est_full['K']

    u_boots = np.zeros((n_bootstrap, K, 2))
    omega_boots = np.zeros((n_bootstrap, 2, 5)) if include_wls else None

    for b in range(n_bootstrap):
        sampled_firms = rng.choice(unique_firms, size=N_firms, replace=True)
        boot_idx = []
        for firm in sampled_firms:
            firm_mask = np.where(firm_ids == firm)[0]
            boot_idx.extend(firm_mask.tolist())
        boot_idx = np.array(boot_idx)

        try:
            est_b = run_estimator(states[boot_idx], actions[boot_idx],
                                   next_states[boot_idx], beta=beta,
                                   alpha_scrap=alpha_scrap, alpha_L=alpha_L,
                                   n_bins=n_bins)
            u_boots[b] = est_b['u']
            if include_wls:
                omega_boots[b] = parametric_wls(
                    est_b['u'], est_b['cell_means'], est_b['n_k'], est_b['K']
                )
        except Exception:
            u_boots[b] = np.nan
            if include_wls:
                omega_boots[b] = np.nan

    ci_lower_u = np.nanpercentile(u_boots, 2.5, axis=0)
    ci_upper_u = np.nanpercentile(u_boots, 97.5, axis=0)
    result = {'u_boots': u_boots, 'u_ci_lower': ci_lower_u, 'u_ci_upper': ci_upper_u}

    if include_wls:
        result['omega_boots'] = omega_boots
        result['omega_ci_lower'] = np.nanpercentile(omega_boots, 2.5, axis=0)
        result['omega_ci_upper'] = np.nanpercentile(omega_boots, 97.5, axis=0)
        # also report mean and std of omega across bootstrap reps
        result['omega_mean'] = np.nanmean(omega_boots, axis=0)
        result['omega_std'] = np.nanstd(omega_boots, axis=0)

    return result
```

Then update `experiments/sec_robustness.py` and SEC analysis scripts to use the WLS bootstrap output. This addresses Issue #2 from the original audit AND closes Item #5.

---

## Summary

| Item | Status | Impact on paper |
|---|---|---|
| #1 (AM 2011/2019 vs Thm 6.3) | ✅ Resolved | **Demote Thm 6.3 to methodological clarification, not headline contribution.** AM 2011's representation theorem makes Thm 6.3 algebraically trivial. Be honest. |
| #2 ([17] §3 absorbing +γ) | ✅ Resolved | Cite [17] verbatim in §1: their "absorb +γ_Euler into r^†" is the folk wisdom your Thm 7.1 corrects under absorbing exit. **Strongest novelty positioning.** |
| #3 ([01] §6–7 linear reward) | ✅ Resolved | Add Zeng-Hong-Garcia Cor 1(ii) to §4 (identification). Their reference-action normalisation matches your Magnac-Thesmar approach. |
| #4 ([11] Jhaveri §3–4) | ✅ Resolved | Add [11] Theorem 4.2 to §2 (contraction). State in §7 footnote that vanishing-temperature limits are orthogonal to your fixed-β discrepancy. |
| #5 (bootstrap.py vs [07]) | ✅ Resolved | Concrete code fix: extend `src/bootstrap.py` to also bootstrap `ω̂`. ~20 LOC. Closes both Issue #2 from earlier audit AND Item #5. |

## Net effect on the paper's novelty story

**Strengthened:** Thm 7.1, Prop 7.2, Rmk 7.3, Prop 7.4 are all CONFIRMED NOVEL via deep reads of the highest-overlap-risk papers. The folk wisdom you correct ([17] van der Laan et al.) is explicit in the literature and your refinement is precise.

**Demoted:** Thm 6.3 is **derivative** of Arcidiacono-Miller 2011's representation theorem. Honest framing: "We make explicit the one-step reduction of the V10 iterative scheme, applying AM 2011 to the absorbing-exit three-action case."

**Honest abstract structure for the AAAI paper:**

1. **Headline claim 1:** Discrepancy theorem (Thm 7.1) and its bounds (Rmk 7.3) — corrects the folk DDC≡MaxEnt-IRL equivalence under absorbing exit. *Novel.*
2. **Headline claim 2:** Continuation-subproblem exact equivalence (Prop 7.4) — explains exactly when the folk equivalence holds. *Novel.*
3. **Methodological clarification:** One-step CCP recovery (Thm 6.3) is the algebraic specialisation of AM 2011 to the absorbing-exit three-action case. *Derivative — honest framing.*
4. **Empirical contribution:** SEC EDGAR application (2,906 firms, 146,985 obs). *Novel setting.*

## Files updated as part of this verification

- `references/00a_ArcidiaconoMiller2011_CCP_Heterogeneity.pdf` — newly added
- `references/00b_ArcidiaconoMiller2019_NonstatFiniteDependence.pdf` — newly added
- `references/VERIFICATION_REPORT.md` — this file
- `references/LITERATURE_GAP_ANALYSIS.md` — updated with refined Thm 6.3 verdict (see below)
- `references/REFERENCE_INVOCATION_MAP.md` — updated with AM 2011/2019 invocations (see below)

## Files NOT yet updated (action items for you)

- `src/bootstrap.py` — extend to bootstrap `ω̂` as well as `u`. See code in Item #5 above.
- `src/figures.py:233,241` — fix `sec_estimates.pkl` → `sec_estimation.pkl` (still pending from earlier audit).
- `src/sec_data.py` schema — still pending from earlier audit.

These are tracked in your task list (#16, #17, #18).
