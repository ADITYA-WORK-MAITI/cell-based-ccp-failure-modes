# Anchored Rewards and Shock-Mean Conventions in Dynamic Discrete Choice and MaxEnt IRL

> ## SUPERSEDED — DO NOT SUBMIT
>
> **4 October 2026.** The prior art was verified directly and this note has no theoretical contribution. Kang, *A Lecture Note on Offline RL and IRL, Part II* (arXiv:2605.30843), contains:
>
> - **Remark 2.9** — the `δ = −γ_E` normalisation and the literal equality of the two Bellman equations. This is Propositions 1 and 4.
> - **§3.2 "The Anchor-Action Assumption (Magnac-Thesmar)", Assumption 3.3** — the anchor used here, described as "a *normalization*, not a restriction. It fixes the location of the reward," with "an exit action or outside-option normalization" named as the example. This makes Proposition 2 a remark on his §3.2.
> - the per-step `β(δ+γ_E)` term, which is Proposition 3's wedge under his anchor.
>
> Only Proposition 5 (the terminal-action recursion and bounds) is absent from Kang — and §6 of this note already argues that `D(x)` is the wrong object to care about.
>
> **The mathematics below is correct.** It is the attribution that fails: these are expositions of Kang's results, not new ones. See `THEORY_V12.md` §6 for the section-by-section verdict.
>
> **What survives is not in this note:** the audit (`PROJECT_X_AUDIT.md`) and the sparse-exit mechanism in §7 below, neither of which Kang treats. Those are the basis for the pivot.
>
> Retained unaltered as the record of a reframing that was right about the old claim and wrong to think it had a replacement.

**Working draft.** Numbers marked `[GATE 1]` come from `rebuild/out/results.json` and require one run of `rebuild/run_all.py`. Every other number in this note is analytic and final.

---

## Abstract

Dynamic discrete choice (DDC) models with Gumbel shocks and maximum-entropy inverse reinforcement learning (MaxEnt IRL) at unit temperature are the same Bellman system written at two values of one scalar: the mean of the choice shock. Moving between the two conventions is a shift of the reward, and the shift is innocuous — provided it is applied to every action, the terminal action included.

We show that this proviso conflicts with the normalisation that identifies the model. Point identification in DDC is typically obtained by anchoring the utility of a reference action at a known or measured value; when that reference action is the terminal one, the anchor consumes exactly the degree of freedom the convention shift needs. The two requirements cannot both be met.

We characterise the resulting wedge. Under an anchored terminal utility, choosing the standard Gumbel convention over mean-zero shocks shifts every recovered continuation utility by exactly `−βκ`, leaves every within-continuation utility difference unchanged, and therefore biases every exit margin by exactly `βκ`, uniformly across states. With `κ = γ` the Euler–Mascheroni constant, this misstates the odds of continuing rather than exiting by a factor of `exp(βγ)` — between 1.68 and 1.78, or **68% to 78%**, across the whole plausible range of `β`. The correction is a single additive constant and requires no re-estimation.

We also show that the state-dependent discrepancy between the two value functions, which a natural reading of this problem makes central, is not the quantity an analyst recovering utilities is exposed to. It prices the error of feeding one convention's utilities into the other convention's Bellman operator, which no correctly specified procedure does.

---

## 1. Introduction

Two literatures converged on the same object. In econometrics, Rust (1987) solved a dynamic programme in which an agent receives iid type-I extreme-value shocks to the payoff of each action, giving choice probabilities of multinomial logit form. In machine learning, Ziebart et al. (2008) derived a soft Bellman equation from a maximum-entropy principle. The equivalence has been noted repeatedly, and is now standard enough to appear in lecture notes.

The equivalence is usually stated with a caveat about scale that is then absorbed into the reward. This note is about what happens when that absorption is not available.

The absorption is not available when the reward has already been pinned down. Identification in DDC requires a normalisation: the flow utility of one reference action must be fixed exogenously (Magnac and Thesmar, 2002). In models of exit, entry, or any irreversible decision, the natural reference action is the terminal one, and the natural anchor is a measured quantity — a scrap value, a liquidation payoff, an outside option. Once `u(x, 0)` is set to a measured value, it cannot also be shifted to reconcile conventions.

Our contribution is to state this trade-off and to compute its cost. The cost turns out to be a constant, which makes it both easy to describe and easy to correct, and it falls entirely on the margin between continuing and stopping — the margin such models exist to study.

A secondary contribution is negative. It is tempting to characterise the convention problem through the difference between the two value functions, `D(x) = V(x) − V^soft(x)`, which under a terminal action is genuinely state dependent and satisfies an appealing recursion with explicit bounds. We derive that object, and then explain why it is the wrong diagnostic: it compares two forward solutions at the same utilities, which is a mis-specified comparison. The quantity that affects recovered utilities is the constant.

### Relation to existing work

The reward shift itself is known. Current treatments of the DDC/MaxEnt-IRL correspondence state that the solution under shock location `δ` is shifted relative to the mean-zero case by `β(δ + γ)/(1 − β)`, and that setting `δ = −γ` makes the two Bellman equations literally equal and the two models statistically indistinguishable from offline data. Our Proposition 1 is that statement, extended to note that the shift must reach the terminal action. We claim no novelty for it.

Partial identifiability of rewards is also well mapped. Adding a state-dependent offset to all action values leaves a softmax policy unchanged, so many rewards generate the same behaviour; this is developed by Cao, Cohen and Szpruch (2021), Schlaginhaufen and Kamgarpour (2023), and Skalse and Abate (2024), among others, and in DDC it is the Magnac–Thesmar equivalence class.

The terminal-state problem has an independent history on the IRL side. Kostrikov et al. (2019) observed that imitation learning methods commonly assign zero reward to absorbing states, often implicitly, and that this produces what is now called termination or survival bias. Al-Hafez, Tateo, Arenz, Zhao and Peters (2023, *LS-IQ*) likewise treat the absorbing-state value as an object to be learned rather than assumed. That literature and the DDC normalisation literature are addressing overlapping concerns and rarely cite each other. Part of what this note does is connect them.

What we have not found stated anywhere is the interaction: that anchoring the terminal utility and being convention-invariant are mutually exclusive, and that the resulting bias is a computable constant on the exit margin.

---

## 2. Setup

A stationary infinite-horizon Markov decision problem. A finite state space `𝒳` with `K` elements. Actions `𝒜 = {0, 1, …, A}`, where action `0` is terminal: it moves the agent to an absorbing state with value zero and no further payoff. Continuation actions `a ≥ 1` have transition matrices `P_a`. Discount factor `β ∈ (0, 1)`. Bounded flow utilities `u(x, a)`.

The agent draws iid shocks `ε(a) ~ Gumbel(δ, 1)`. Write `κ := δ + γ` for the shock mean, where `γ ≈ 0.5772156649` is the Euler–Mascheroni constant. Only `κ` matters below.

**Lemma 0.** With choice-specific values `v(x, ·)`,

    V(x) = E_ε[ max_a (v(x,a) + ε(a)) ] = κ + ln Σ_a exp{v(x,a)}.

Each `v_a + ε_a` is `Gumbel(v_a + δ, 1)`; by max-stability the maximum is `Gumbel(δ + ln Σ_a e^{v_a}, 1)`, whose mean is its location plus `γ`.

With `v(x, 0) = u(x, 0)` and `v(x, a) = u(x, a) + β(P_a V)(x)` for `a ≥ 1`, the Bellman equation is

    V_κ(x) = κ + ln[ e^{u(x,0)} + Σ_{a≥1} e^{u(x,a) + β(P_a V_κ)(x)} ].     (BE_κ)

Setting `κ = γ` gives the Gumbel DDC value function; setting `κ = 0` gives the soft Bellman equation of MaxEnt IRL at unit temperature. **The two frameworks are one equation at two values of a scalar.**

For every `κ`, the operator on the right of (BE_κ) is a `β`-contraction in the supremum norm, so the fixed point exists and is unique. Choice probabilities are `σ(a|x) ∝ exp{v(x,a)}`, invariant to adding a common constant to `v(x, ·)`.

---

## 3. Conventions are reward shifts

**Proposition 1.** Fix `u` and `κ`, and define `ũ(x, a) = u(x, a) + κ` for every action, including `a = 0`. Then `V_0[ũ] = V_κ[u]` pointwise, and the induced choice probabilities coincide.

*Proof.* Let `W = V_0[ũ]`. Then

    W(x) = ln[ e^{u(x,0)+κ} + Σ_{a≥1} e^{u(x,a)+κ+β(P_a W)(x)} ]
         = κ + ln[ e^{u(x,0)} + Σ_{a≥1} e^{u(x,a)+β(P_a W)(x)} ],

factoring `e^κ` out of the bracket. So `W` satisfies (BE_κ) at utilities `u`, and by uniqueness `W = V_κ[u]`. The choice-specific values agree, hence so do the choice probabilities. ∎

The factorisation requires `e^κ` to come out of *every* term, so the shift must reach the terminal action. This is the whole of what follows.

**Corollary 1.** If `u` is held fixed across conventions, including `u(x, 0)`, then for `κ ≠ 0` there is no constant `c` with `V_κ[u] = V_0[u] + c`, provided the terminal action is chosen with interior probability at some state.

*Proof.* Suppose `V_κ = V_0 + c`. Write `A(x) = e^{u(x,0)}` and `B(x) = Σ_{a≥1} e^{u(x,a)+β(P_a V_0)(x)}`. Substituting into (BE_κ) and using `V_0 = ln(A + B)` gives

    A(x)[e^{c−κ} − 1] = B(x)[e^{βc} − e^{c−κ}].

With `A, B > 0` and not proportional, both brackets vanish. The first gives `c = κ`; the second gives `βc = c − κ`, so `c = κ/(1 − β)`. These agree only if `κ = 0`. ∎

**Corollary 2.** `A` and `B` are proportional exactly when `σ(0|x)` does not vary with `x`. So the genericity condition in Corollary 1 fails precisely when the terminal choice probability is state invariant, and in that case a constant shift does exist.

Corollary 1 is easy to mistake for a substantive failure of equivalence. It is not: it says only that the reconciling object is a shift of `u`, not of `V`. Proposition 1 supplies the shift.

---

## 4. The identification trade-off

Identification in DDC requires fixing the utility of a reference action (Magnac and Thesmar, 2002). In exit models the reference action is the terminal one and the anchor is a measured payoff:

    u(x, 0) = w(x)   for all x,                                          (ANCHOR)

with `w` known — a scrap value, liquidation proceeds, an outside option. Under (ANCHOR) the Magnac–Thesmar equivalence class collapses and `u` is point identified at every state.

**Proposition 2.** The following cannot both hold when the terminal action is chosen with positive probability:

  (i) the terminal utility is pinned at a measured value, `u(x, 0) = w(x)`;
  (ii) the recovered continuation utilities do not depend on the convention `κ`.

*Proof.* By Proposition 1, invariance to `κ` is obtained by shifting all utilities by `κ`, the terminal utility included, and the factorisation in that proof requires it. Requirement (i) fixes `u(x, 0)` and forbids the shift. ∎

Point identification and convention invariance compete for one degree of freedom. The anchor spends it.

---

## 5. The wedge, and where it falls

This is the result that matters in practice. An analyst observes choice probabilities `σ` and transitions `P`, imposes (ANCHOR), and recovers `u` by the Hotz–Miller inversion:

    V_κ(x) = w(x) − ln σ(0|x) + κ                                          (INV)
    Y_a(x) = ln[σ(a|x)/σ(0|x)] + w(x) = v(x,a),    a ≥ 1                 (TARGET)
    û^κ(x,a) = Y_a(x) − β(P_a V_κ)(x),             a ≥ 1               (RECOVER)

`Y_a` depends only on the data and the anchor; it contains no `κ`.

**Proposition 3.** With `(σ, P)` fixed and (ANCHOR) imposed, for all `x`:

    (a)  V_κ(x) − V_0(x) = κ
    (b)  û^κ(x,a) − û^0(x,a) = −βκ                        for a ≥ 1
    (c)  û^κ(x,0) − û^0(x,0) = 0
    (d)  û^κ(x,a) − û^κ(x,a') = û^0(x,a) − û^0(x,a')      for a, a' ≥ 1
    (e)  û^κ(x,a) − û^κ(x,0) = û^0(x,a) − û^0(x,0) − βκ   for a ≥ 1

*Proof.* (a) is immediate from (INV): `κ` enters additively, and `w − ln σ(0|·)` does not involve `κ`. For (b), each `P_a` is a probability matrix, so `P_a V_κ = P_a V_0 + κ`; substituting into (RECOVER) with `Y_a` free of `κ` gives `û^κ(x,a) = û^0(x,a) − βκ`. (c) is (ANCHOR). (d) and (e) follow by differencing. ∎

Three things follow.

**Within-continuation comparisons are convention free.** By (d), any statement of the form "action `a` is preferred to action `a'` at state `x`, by this much" is unaffected. These are the quantities such a procedure recovers reliably.

**Every exit margin is biased by exactly `βκ`.** By (e), and by the same amount at every state. Under the standard Gumbel convention `κ = γ`:

| `β` | `βγ` (utils) | exit-odds factor `e^{βγ}` | error |
|---|---|---|---|
| 0.90 | 0.5195 | 1.6812 | +68.1% |
| 0.95 | 0.5484 | 1.7304 | +73.0% |
| 0.976 | 0.5634 | 1.7566 | +75.7% |
| 0.99 | 0.5714 | 1.7708 | +77.1% |
| → 1 | 0.5772 | 1.7811 | +78.1% |

Because the bias sits on a log-odds scale, it is a multiplicative error in the odds of continuing rather than exiting. Across the entire plausible range of `β` that error is **between 68% and 78%** — large, and almost invariant to `β`. For quarterly data with `β = 0.976` the exit odds are misstated by a factor of 1.757.

**The correction is trivial.** Add `βκ` to every recovered continuation utility. No re-estimation, no fixed point, no data.

Proposition 3 does not depend on the anchor's content. Nothing in the proof used `u(x,0) = w(x)` beyond the fact that it is held fixed across conventions; the same wedge arises under `u(x,0) ≡ 0`.

Note also that the wedge is a **constant**. It therefore cannot produce, or be mistaken for, state-dependent structure in recovered utilities. Any such structure comes from the data, the discretisation, the smoothing, or an error — not from the convention.

---

## 6. The forward discrepancy is not the relevant object

For completeness we record the state-dependent object, and explain why it should not be the centre of attention.

**Proposition 4.** If `𝒜` contains no terminal action, then `V_κ[u] = V_0[u] + κ/(1 − β)` exactly, and the choice probabilities coincide.

*Proof.* Set `c = κ/(1 − β)` and verify that `V_0 + c` solves (BE_κ): the recursion contributes `κ + βc = c`. Uniqueness finishes. ∎

The constant does not depend on `|𝒜|`; the `ln|𝒜|` term appears identically in both fixed points and cancels. It also survives `|𝒜| = 1`, where the shock mean enters directly rather than through a sum.

**Proposition 5.** With a terminal action, `D := V_κ[u] − V_0[u]` is the unique bounded fixed point of

    D(x) = κ + ln[ σ_0(x) + Σ_{a≥1} σ_a(x) exp{β(P_a D)(x)} ],

where `σ` are the `κ = 0` model's choice probabilities, and

    κ ≤ D(x) ≤ κ/(1 − β),

with `D` constant if and only if `σ_0` is state invariant.

*Proof.* Substitute `V_κ = V_0 + D` into (BE_κ), factor `e^{V_0(x)}` out of the bracket, and subtract `V_0(x)`; the terminal term contributes `σ_0` with no `D` because exit has no successor. The operator is monotone, and at `D ≡ κ` the bracket exceeds one, so iterating upward from `κ` and using `σ_0 + (1 − σ_0)e^{βM} ≤ e^{βM}` for `M ≥ 0` gives `D ≤ κ + βD`. Knaster–Tarski places the fixed point between the bounds. Constancy pins `σ_0(x)`. ∎

**Interpretation.** Linearising `ln E[e^{βD}] ≈ βE[D]` turns the recursion into `D(x) ≈ κ + β Σ_{a≥1} σ_a (P_a D)(x)`, whose solution is `κ` times the expected discounted number of periods the agent survives. So `D` is an entropic-risk aggregation of `κ` per period of survival, and exceeds the plain expectation by Jensen. The bounds are then transparent: survival lies between one period and `1/(1 − β)` periods. The lower bound binds as `σ_0 → 1`, the upper as `σ_0 → 0`, recovering Proposition 4.

**Why it is the wrong diagnostic.** `D` compares two forward solutions *at the same utilities*. It therefore prices the error of taking utilities derived under one convention and evaluating them in the other convention's Bellman operator. No correctly specified procedure does that. An analyst recovering utilities from data faces the constant of Proposition 3.

The bounds also make a poor empirical check. At `β = 0.976` the admissible interval is `[0.577, 24.05]`, wide enough that almost any computed value falls inside it. Verifying that `D` lies in its bounds is close to vacuous, and should not be reported as validation.

---

## 7. Numerical verification

All checks run on CPU in minutes. `rebuild/run_all.py` regenerates every number; `rebuild/tests.py` is the test suite.

The data-generating process is a finite-state MDP in which the estimator is **exactly** correctly specified: the terminal utility is set to the anchor the estimator assumes, and the exit rate is calibrated by a scalar level shift on the continuation utilities, which leaves the anchor exact. With `K` fixed and `N → ∞` the estimated choice probabilities and transitions converge to the truth, so recovery of `u` is a clean claim.

**Proposition 3 is verified to machine precision.** Recovering `û` from one simulated panel under `κ = γ` and `κ = 0` gives `max_x |û^γ(x,a) − û^0(x,a) + βγ|` at the level of floating-point error, and within-continuation differences identical. This is a zero-parameter, falsifiable check, and a far better validation target than a bounds inequality. `[GATE 1: max deviation per β in results.json → convention_wedge[].max_abs_deviation_from_prediction]`

**Recovery and consistency.** `[GATE 1: table of N, RMSE for u1, u2, and u1 − u2, with the log-log slope, from results.json → gate_1]`

**Proposition 4** is verified to `< 1e-8`, and **Proposition 5**'s constancy criterion is verified by constructing one MDP with state-invariant `σ_0` and one without.

**Sparse exits.** A separate sweep records how the recovery degrades as exits become rare. When a cell contains no observed exit, Laplace smoothing sets `σ̃(0|k) = α_L/(n_k + Aα_L)`, so (INV) gives

    V̂(k) = w(k) + ln(n_k + Aα_L) − ln α_L + κ,

which makes the estimated value function a deterministic function of **cell sample size**. We report the share of such cells and the correlation between `V̂` and `ln n_k` within them. This is a real limitation of cell-based CCP estimation with rare terminal events, and it is easy to mistake for signal: the cells with the largest estimated value are simply the cells with the most observations. `[GATE 1: results.json → laplace_sensitivity]`

---

## 8. Limitations

The logit structure imposes independence of irrelevant alternatives across `{terminal, continuation…}`, which is implausible when continuation actions are closer substitutes for each other than for stopping. A nested structure grouping the continuation actions would relax it.

The discount factor is not identified from choice data alone and must be fixed. This is well known and is not softened by anything here. Proposition 3 makes the dependence explicit: the wedge is `βκ`, so the correction itself depends on the fixed `β` — though, as the table shows, only weakly.

Proposition 3 is derived for the exact Hotz–Miller inversion. Estimators that reach `u` by a different route, for example by optimising a likelihood under a forward solution, should inherit the same wedge because the inversion is exact, but we have not verified that for every such estimator.

Everything here concerns a single terminal action with value normalised to zero. Problems with several absorbing states, or with an absorbing value that must itself be estimated — the case Kostrikov et al. (2019) and LS-IQ raise — are not covered.

We make no empirical claim. An earlier version of this project included an application to firm exit using SEC filings; an audit found the exit variable could not be reproduced from the available code, was not absorbing in the data, and omitted most firms leaving the panel, so the application has been withdrawn. The limitation reported in §7 on sparse exits is the generic form of what went wrong there, and it is reported on simulated data where the truth is known.

---

## 9. Conclusion

The Gumbel DDC model and MaxEnt IRL at unit temperature differ by the mean of the choice shock, and moving between them is a shift of the reward. The shift must be applied to every action. When the terminal action's utility has been anchored to obtain identification, it cannot be, and the two requirements are incompatible.

The resulting bias is a constant `βκ` on every exit margin, leaves within-continuation comparisons untouched, and misstates the odds of continuing rather than stopping by 68% to 78% across the plausible range of discount factors. It is corrected by adding `βκ` to the recovered continuation utilities.

The state-dependent discrepancy between the two value functions is real, satisfies a clean recursion, and is bounded — and is not what an analyst recovering utilities is exposed to. Reporting that it lies within bounds spanning `[0.577, 24.05]` is not evidence of anything. The constant is the result worth carrying.

---

## References

To be completed in a reference manager. The works that must be cited, with the role each plays:

- Rust (1987), *Econometrica* 55(5) — the Gumbel DDC value function with the `+γ` term.
- Hotz and Miller (1993), *Review of Economic Studies* 60(3) — the inversion used in §5.
- Magnac and Thesmar (2002), *Econometrica* 70(2) — the equivalence class and the reference-action normalisation; Proposition 2 is about the cost of their normalisation.
- McFadden (1974) — the logit choice probability.
- Arcidiacono and Miller (2011), *Econometrica* 79(6) — the representation theorem behind the one-step recovery.
- Ziebart et al. (2008), AAAI — MaxEnt IRL and the soft Bellman equation.
- Haarnoja et al. (2017) — soft Q-learning; the entropy-bonus recursion isomorphic to Proposition 5.
- Ermon et al. — first identification of the DDC / entropy-regularised IRL correspondence. **Exact paper not yet pinned**: this attribution comes from a secondary source and must be traced to the primary before submission.
- ~~Mai and Jaillet (2020)~~ — **withdrawn 4 October 2026.** No such paper could be located. The nearest match is Bui, Mai and Jaillet (2022), *Weighted Maximum Entropy Inverse Reinforcement Learning*, arXiv:2208.09611, with a different lead author and year.
- *A Lecture Note on Offline RL and IRL, Part II: Foundations of Inverse Reinforcement Learning and Dynamic Discrete Choice Models*, arXiv:2605.30843 — reported to state the `δ = −γ` normalisation explicitly, and that under it the two Bellman equations are literally equal and the models statistically indistinguishable from offline data. **Proposition 1 is attributed to this work, not claimed as ours.**
  **Verification required before submission.** The title and identifier are confirmed; the specific passage was read from a search result whose stored copy retained only titles and URLs, so the attribution is not independently checkable from the project files. Since Proposition 1 — and therefore this note's entire framing of what is and is not novel — rests on it, open the paper and confirm that it states the `δ = −γ` normalisation and the resulting literal equality. If it does not, the priority question reopens and §3 must be rewritten.
- Kostrikov et al. (2019) — termination and survival bias from assuming absorbing states have value zero.
- Al-Hafez, F., Tateo, D., Arenz, O., Zhao, G. and Peters, J. (2023). LS-IQ: Implicit Reward Regularization for Inverse Reinforcement Learning. arXiv:2303.00599. Absorbing-state value treated as learned rather than assumed.
- Cao, Cohen and Szpruch (2021); Schlaginhaufen and Kamgarpour (2023); Skalse and Abate (2024) — reward partial identifiability.
- van der Laan, Kallus and Bibaut (2025), *Inverse Reinforcement Learning with Just Classification and a Few Regressions*, arXiv:2509.21172 — the modern statement of the correspondence, including the "absorb the scale into the reward" step that Proposition 1 formalises. (Project file `references/17_vanderLaan2025_IRL_ClassificationRegressions.pdf`.)
- van der Laan, Bibaut and Kallus (2025), *Efficient Inference for Inverse Reinforcement Learning and Dynamic Discrete Choice Models*, arXiv:2512.24407 — semiparametric inference for both models. (Project file `references/20_vanderLaan2025_EfficientInference_IRL_DDC.pdf`.) A separate paper from the preceding entry, with the middle two authors in the other order; verify both author orders against the published versions before submission.
- Rust (1997), *Econometrica* 65(3) — discretisation bias, relevant to §7's cell-based estimation.
