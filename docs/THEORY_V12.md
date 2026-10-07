# Shock-Mean Conventions and Terminal Actions in Gumbel Discrete Choice and MaxEnt IRL

**Theory document V12** — supersedes `MATHEMATICAL_MODELLING_V11.md`
**Status:** mathematics complete and self-contained. No result here depends on unexecuted code.
**Date:** 4 October 2026

---

## What changed from V11, and why

V11's headline (Theorem 7.1) claimed that the equivalence between Gumbel dynamic discrete choice (DDC) and maximum-entropy IRL "fails generically" under absorbing exit. That claim does not survive audit, for a reason V11 never considered: the `+γ` term it treats as structural is a **shock-mean convention**, and the reconciling shift is a shift of the *reward*, which the literature performs explicitly and which works perfectly well with a terminal action — provided the shift is applied to the terminal action too.

Reframing it produced a cleaner result than the original, and one that reverses the paper's emphasis:

> The convention wedge that matters in practice is **a constant, not a state-dependent function**. Under an anchored terminal utility, choosing the standard Gumbel convention over the mean-zero convention biases every recovered *exit margin* by exactly `βκ`, leaves every *within-continuation* utility difference untouched, and does so uniformly across states.

The state-dependent object `D(x)` that V11 built its paper around is an artifact of a mis-specified comparison — feeding one model's utilities into the other model's operator. It is mathematically real (Proposition 5 below) but it is not the quantity an analyst recovering utilities is exposed to.

**Numerically, for the project's calibration** (`β = 0.976`, standard Gumbel `κ = γ`): the exit margin is biased by `βγ ≈ 0.5634` utils. That is the paper's practical takeaway, and it is a number, not a bracket.

---

## 1. Setup

A stationary infinite-horizon MDP. State space `𝒳` finite with `K` elements (the discretised cells; everything below holds verbatim for compact `𝒳` with `C(𝒳)`). Actions `𝒜 = {0, 1, …, A}`. Action `0` is **terminal**: choosing it moves the agent to an absorbing state `x†` with `V(x†) = 0` and all subsequent flow utility zero. Actions `a ≥ 1` are **continuation** actions with transition kernels `P_a`. Discount `β ∈ (0,1)`. Flow utilities `u : 𝒳 × 𝒜 → ℝ`, bounded.

**Shocks.** The agent draws iid `ε(a) ~ Gumbel(δ, 1)`, CDF `F(e) = exp(−e^{−(e−δ)})`. Write

```
κ := δ + γ = 𝔼[ε(a)],        γ = Euler–Mascheroni ≈ 0.5772156649
```

`κ` is the **shock mean**, and it is the only way `δ` enters anything below.

Two conventions appear in the literature:

| Convention | `δ` | `κ` | Used by |
|---|---|---|---|
| Standard Gumbel | `0` | `γ` | Rust (1987) and the DDC tradition |
| Mean-zero Gumbel | `−γ` | `0` | soft-Bellman / MaxEnt IRL at unit temperature |

**Lemma 0 (ex-ante value).** With `ε(a) ~ Gumbel(δ,1)` iid and choice-specific values `v(x,·)`,

```
V(x) := 𝔼_ε[ max_a (v(x,a) + ε(a)) ] = κ + ln Σ_a exp{v(x,a)}.
```

*Proof.* `v_a + ε_a ~ Gumbel(v_a + δ, 1)`. By max-stability the maximum is `Gumbel(δ + ln Σ_a e^{v_a}, 1)`, whose mean is its location plus `γ`. ∎

So the Bellman equation, with `v(x,0) = u(x,0)` and `v(x,a) = u(x,a) + β (P_a V)(x)` for `a ≥ 1`, is

```
V_κ(x) = κ + ln[ e^{u(x,0)} + Σ_{a≥1} e^{u(x,a) + β(P_a V_κ)(x)} ].        (BE_κ)
```

`κ = γ` gives V11's Eq B.4; `κ = 0` gives V11's Eq E.1, the soft Bellman. **The two "competing frameworks" are one equation at two values of a single scalar.**

**Lemma 1 (contraction).** For every `κ`, the operator `(T_κ V)(x) :=` RHS of (BE_κ) is a `β`-contraction in `‖·‖_∞`, with a unique bounded fixed point.

*Proof.* The terminal term `e^{u(x,0)}` does not involve `V` and cancels in differences. `ln Σ_i e^{y_i}` is 1-Lipschitz in `‖·‖_∞` (its gradient is a softmax, of `ℓ¹`-norm 1). Each `P_a` is non-expansive. Composing, `‖T_κ V_1 − T_κ V_2‖_∞ ≤ β‖V_1 − V_2‖_∞`. Banach applies. ∎

**CCPs.** `σ(a|x) = exp{v(x,a)} / Σ_{a'} exp{v(x,a')}`, invariant to adding any constant to all of `v(x,·)`.

---

## 2. The reward shift, and the role of the terminal action

**Proposition 1 (shock-mean conventions are reward shifts).** Fix `u` and `κ`. Define the shifted utility

```
ũ(x,a) := u(x,a) + κ        for every a ∈ 𝒜, the terminal action a = 0 included.
```

Then `V_0[ũ] = V_κ[u]` pointwise, and the two models induce identical CCPs and identical choice behaviour.

*Proof.* Let `W := V_0[ũ]`, the fixed point of (BE_0) at utilities `ũ`:

```
W(x) = ln[ e^{u(x,0)+κ} + Σ_{a≥1} e^{u(x,a)+κ+β(P_a W)(x)} ]
     = κ + ln[ e^{u(x,0)} + Σ_{a≥1} e^{u(x,a)+β(P_a W)(x)} ],
```

where the second line factors `e^κ` out of the bracket. So `W` satisfies (BE_κ) at utilities `u`. By Lemma 1 that fixed point is unique, hence `W = V_κ[u]`. The choice-specific values coincide, so the CCPs coincide. ∎

**This is the result V11's Theorem 7.1 missed.** The shift has to be applied to the terminal action as well as the continuation actions. V11 held `u(x,0) = W̃(x)` fixed, shifted nothing, and then asked whether a constant added to `V` could reconcile the two fixed points. It cannot — that is V11's Theorem 7.1, and its algebra is correct — but the question is the wrong one, because the reconciling object is a shift of `u`, not of `V`.

**Corollary 1 (restatement of V11 Theorem 7.1).** If `u` is held fixed across conventions — including `u(x,0)` — then for `κ ≠ 0` there is no constant `c` with `V_κ[u] = V_0[u] + c`, provided the terminal action is chosen with interior probability at some state.

*Proof.* Suppose `V_κ = V_0 + c`. Substituting into (BE_κ) and writing `A(x) := e^{u(x,0)}`, `B(x) := Σ_{a≥1} e^{u(x,a)+β(P_a V_0)(x)}`:

```
V_0(x) + c = κ + ln[ A(x) + e^{βc} B(x) ],      and      V_0(x) = ln[A(x) + B(x)],
```

so `e^{c−κ}[A + B] = A + e^{βc}B`, i.e. `A(x)[e^{c−κ} − 1] = B(x)[e^{βc} − e^{c−κ}]`. With `A, B > 0` and not proportional, both brackets vanish: the first gives `c = κ`, the second `βc = c − κ`, i.e. `c = κ/(1−β)`. These agree only if `κ = 0`. ∎

Note the sharpened conclusion: the two candidate constants are `κ` and `κ/(1−β)`. V11's proof chained the second condition through the first and reported `c = 0`, reaching the same contradiction by a muddier route.

**Corollary 2 (when the constant does exist).** `A` and `B` are proportional exactly when the terminal-action odds `e^{u(x,0)}/B(x)` — equivalently `σ(0|x)` — do not vary with `x`. In that case a constant shift does exist. So Corollary 1's "genericity hypothesis" has a clean interpretation: **it fails precisely when the terminal choice probability is state-invariant.**

---

## 3. The identification trade-off

The anchor that delivers point identification is the Magnac–Thesmar reference-action normalisation, here fixing the terminal utility at an externally measured scrap value:

```
u(x,0) = W̃(x)     for all x ∈ 𝒳.        (ANCHOR)
```

Under (ANCHOR) the Magnac–Thesmar equivalence class collapses to `{0}` and `u` is point-identified at every state (V11 Corollary 4.6, which is correct).

**Proposition 2 (incompatibility).** The following two requirements cannot both be met when the terminal action is chosen with positive probability:

- **(i)** the terminal utility is pinned at a measured value, `u(x,0) = W̃(x)`;
- **(ii)** the recovered continuation utilities are invariant to the shock-mean convention `κ`.

*Proof.* By Proposition 1, invariance to `κ` is achieved by, and only by, shifting all utilities by `κ` — the terminal utility included, since the factorisation in Proposition 1's proof requires `e^κ` to come out of *every* term in the bracket. Requirement (i) fixes `u(x,0)` and so forbids that shift. Hence under (i) the recovered utilities depend on `κ`. ∎

Informally: **point identification and convention-invariance compete for the same degree of freedom.** The anchor spends it; the shift needs it. This is the honest content of what V11 was reaching for, and it is an identification statement, not a failure-of-equivalence statement.

---

## 4. The wedge is a constant, and it sits on the exit margin

This is the practically relevant result. The exercise is the inverse one: an analyst observes CCPs `σ` and transitions `P`, imposes (ANCHOR), and recovers `u` by Hotz–Miller inversion. What does the convention cost?

**Inversion under convention `κ`.** From `σ(0|x) = e^{v(x,0)}/\exp(V_κ(x) − κ)` and `v(x,0) = W̃(x)`:

```
V_κ(x) = W̃(x) − ln σ(0|x) + κ.                        (INV)
Y_a(x) := ln[σ(a|x)/σ(0|x)] + W̃(x) = v(x,a),   a ≥ 1.  (TARGET)
û^κ(x,a) = Y_a(x) − β (P_a V_κ)(x),            a ≥ 1.  (RECOVER)
```

`Y_a` depends only on the data and the anchor — it carries no `κ`.

**Proposition 3 (the convention wedge).** Let `û^κ` be recovered by (INV)–(RECOVER) from fixed `(σ, P)` under (ANCHOR). Then for all `x ∈ 𝒳`:

```
(a)  V_κ(x) − V_0(x)  =  κ                           (constant, not state-dependent)
(b)  û^κ(x,a) − û^0(x,a)  =  −βκ        for a ≥ 1
(c)  û^κ(x,0) − û^0(x,0)  =  0                       (pinned by the anchor)
(d)  [û^κ(x,a) − û^κ(x,a')]  =  [û^0(x,a) − û^0(x,a')]        for a, a' ≥ 1
(e)  [û^κ(x,a) − û^κ(x,0)]  =  [û^0(x,a) − û^0(x,0)] − βκ     for a ≥ 1
```

*Proof.* (a) is immediate from (INV): `κ` enters additively and `W̃ − ln σ(0|·)` is `κ`-free. For (b), `P_a` is a probability kernel so `(P_a V_κ) = (P_a V_0) + κ`; substituting into (RECOVER) and using that `Y_a` is `κ`-free gives `û^κ(x,a) = û^0(x,a) − βκ`. (c) is (ANCHOR). (d) and (e) follow by differencing (b) and (c). ∎

**Reading of Proposition 3.**

- **Within-continuation comparisons are convention-free** (d). Any statement of the form "maintain is preferred to growth at this state, by this much" is invariant. These are the quantities the Monte Carlo should and does recover.
- **Every exit margin is biased by exactly `βκ`** (e), the same amount at every state. Under the standard Gumbel convention with `κ = γ` and quarterly `β = 0.976`:

```
βγ = 0.976 × 0.5772156649 = 0.5633624889…  ≈ 0.5634 utils
```

- The bias is **uniform**, **exactly computable**, and **does not require solving anything**. An analyst who has recovered utilities under one convention converts to the other by adding `βκ` to every continuation utility. No re-estimation.
- Consequently the convention affects every statement about *whether to continue or exit*, and no statement about *how to continue*. In an application whose entire object is the exit decision, this is the margin that matters.

**Proposition 3 is robust to the anchor's content.** Nothing in the proof used `u(x,0) = W̃(x)` beyond the fact that it is held fixed across conventions. The same wedge `−βκ` arises under `u(x,0) ≡ 0` or any other fixed anchor.

---

## 5. The forward discrepancy, and why it is not the relevant object

For completeness, the state-dependent object V11 built its paper around. Fix `u` (including `u(x,0)`) and compare the two forward solutions: `D := V_γ[u] − V_0[u]`.

**Proposition 4 (no terminal action).** If `𝒜` contains no terminal action, then `V_γ[u] = V_0[u] + γ/(1−β)` exactly, and the CCPs coincide.

*Proof.* Set `c := γ/(1−β)` and verify `V_0 + c` solves (BE_γ): `γ + ln Σ_{a} e^{u_a + β(P_a V_0) + βc} = γ + βc + V_0 = V_0 + c` since `γ + βc = c`. Uniqueness (Lemma 1) finishes. CCPs are invariant to a common constant. ∎

The constant is independent of `|𝒜|`: the `ln|𝒜|` term appears identically in both fixed points and cancels. It also survives `|𝒜| = 1`, where the `+γ` comes from `𝔼[ε]` rather than from the sum.

**Proposition 5 (with a terminal action).** `D` is the unique bounded fixed point of

```
D(x) = γ + ln[ σ_0^{(0)}(x) + Σ_{a≥1} σ_a^{(0)}(x) · exp{β (P_a D)(x)} ],
```

where `σ^{(0)}` are the CCPs of the `κ = 0` model, and

```
γ ≤ D(x) ≤ γ/(1−β)    for all x,
```

with `D` constant iff `σ_0^{(0)}` is state-invariant.

*Proof.* Substitute `V_γ = V_0 + D` into (BE_γ), factor `e^{V_0(x)}` out of the bracket, and subtract `V_0(x)`; the terminal term contributes `σ_0^{(0)}` with no `D` because exit has no successor. For the bounds: the operator is monotone, and at `D ≡ γ` the bracket exceeds 1 (since `e^{βγ} > 1`), so `T(γ) > γ`; iterating upward from `γ` and using `σ_0 + (1−σ_0)e^{βM} ≤ e^{βM}` for `M ≥ 0` gives `D ≤ γ + βD`, i.e. `D ≤ γ/(1−β)`. Knaster–Tarski gives the fixed point between them. Constancy: a constant `d` requires `d = γ + ln[σ_0 + (1−σ_0)e^{βd}]` to hold at every `x`, which pins `σ_0(x)`. ∎

**Interpretation (missing from V11).** Linearising `ln 𝔼[e^{βD}] ≈ β𝔼[D]` turns the recursion into `D(x) ≈ γ + β Σ_{a≥1} σ_a (P_a D)(x)`, whose solution is `γ ×` the expected discounted number of periods the agent remains alive. So `D` is the entropic-risk aggregation of **`γ` per period of survival**, and by Jensen it exceeds the plain expectation. The bracket `[γ, γ/(1−β)]` is then transparent: survival is between one period and `1/(1−β)` periods. The lower bound binds as `σ_0 → 1` (certain immediate exit), the upper as `σ_0 → 0` (never exits, recovering Proposition 4).

**Why this is not the relevant object.** `D` compares two forward solutions *at the same `u`* — that is, it prices the error of feeding one convention's utilities into the other convention's Bellman operator. No correctly-specified analysis does that. An analyst recovering utilities from data faces Proposition 3's constant `−βκ`, not `D`. V11 made `D` the centrepiece and `D` is where its empirical figure pointed; the audit found that figure invalid on independent grounds, but even a valid version would have been measuring the wrong thing.

---

## 6. Novelty — VERIFIED AGAINST THE PRIOR ART, 4 October 2026

**Verdict: there is no theoretical contribution left. Every proposition below is either stated in, or one line from, Kang (arXiv:2605.30843).**

The paper was retrieved and read directly (`arxiv.org/html/2605.30843v1`, 189k characters of text). It is *A Lecture Note on Offline RL and IRL, Part II: Foundations of Inverse Reinforcement Learning and Dynamic Discrete Choice Models*, by **Enoch Hyunwook Kang**. What it contains:

- **§2.7 and Remark 2.9 ("Two views, one model")** — verbatim: the solution "is shifted by the constant `β(δ+γ_E)/(1−β)`, so the induced softmax policy is unchanged. The clean literal equality of the DDC and unit-entropy MaxEnt-IRL Bellman equations is obtained under the paper's normalization `δ = −γ_E`." And: "Under `λ = 1` and `δ = −γ_E`, the choice-specific Bellman equation and the induced policy are identical, so the two formulations are statistically indistinguishable from offline observations of `(s,a,s')`." → **This is Proposition 1 and Proposition 4.**
- **§3.2, titled "The Anchor-Action Assumption (Magnac-Thesmar)"**, with **Assumption 3.3 (Anchor action)**: "For every `s ∈ 𝒮` there exists a known, distinguished action `a_s` … `r(s, a_s) = 0`." → **This is our (ANCHOR).** He adds: "the anchor-action assumption is a *normalization*, not a restriction. It fixes the location of the reward," and explicitly names the example: "anchor actions, e.g., **an exit action or outside-option normalization**."
- The note also develops Magnac–Thesmar identification (21 mentions), Rust's NFXP, Hotz–Miller CCP, the Adusumilli–Eckardt TD methods, AIRL, IQ-Learn and offline ML-IRL.

**Consequence for each result here.**

| Result | Verdict |
|---|---|
| Proposition 1 (conventions are reward shifts) | **Kang's §2.7 / Remark 2.9.** Not ours. |
| Proposition 4 (`κ/(1−β)` with no terminal action) | **Kang's `β(δ+γ_E)/(1−β)`,** at the `Q` level rather than the `V` level — see the reconciliation note below. Not ours. |
| Proposition 2 (anchor / convention-invariance incompatible) | **A remark on Kang §3.2, not a contribution.** He imposes the anchor, states that it fixes the location of the reward, states the `δ` convention, and names the exit action as his example. That the two cannot be imposed independently is immediate in his framework. |
| Proposition 3 (the wedge is `−βκ` on continuation rewards) | **This is Kang's per-step `β(δ+γ_E)` term,** viewed as a reward bias under his anchor. One line from his `Q` recursion. Not ours. |
| Proposition 5 (terminal-action recursion, bounds, constancy criterion, survival reading) | **Not in Kang** — the note contains zero occurrences of "absorbing", "terminal", "scrap", "stopping". But §6 of this document already judged `D(x)` the wrong object to care about, so what survives is algebra about a quantity we argued is not decision-relevant. |

**Reconciliation of `β(δ+γ_E)/(1−β)` with `κ/(1−β)`.** These are not in conflict; they describe different objects. Kang's soft recursion is at the choice-specific value, `Q(s,a) = r(s,a) + β·LSE(Q(s',·))`, which picks up `+β(δ+γ_E)` per step and so shifts by `β(δ+γ_E)/(1−β)`. The ex-ante value adds one more shock mean on top: `V = LSE(Q) + (δ+γ_E)`, so its shift is `β(δ+γ_E)/(1−β) + (δ+γ_E) = κ/(1−β)`, which is Proposition 4. Anyone comparing the two statements should be told this explicitly, because the discrepancy reads like an error.

**What this means for the project.** The reframing in §1 of this document was correct — V11's Theorem 7.1 does not survive — but the replacement does not constitute a contribution either. The honest position is that this intersection has been thoroughly worked out by Kang, and the project's theoretical ambitions should be retired. What remains of value is the audit and the reproducibility findings: see `PROJECT_X_AUDIT.md` §2.2 and the sparse-exit mechanism in `MANUSCRIPT.md` §7, neither of which Kang addresses and both of which are concrete, verified, and useful to practitioners of cell-based CCP estimation.

---

## 6b. Earlier, pre-verification novelty assessment (retained for the record)

| Result | Status |
|---|---|
| Lemma 0, Lemma 1, CCP formula, Hotz–Miller inversion (INV)–(RECOVER) | **Standard.** McFadden (1974); Rust (1987); Hotz & Miller (1993); Arcidiacono & Miller (2011). |
| Proposition 1 (conventions are reward shifts; `κ = 0` is the canonical choice) | **Known.** Stated for the non-terminal case in the current DDC/IRL literature as the `δ = −γ_E` normalisation. The observation that the shift must include the terminal action is the part V11 got wrong and is, at best, a clarifying remark. |
| Proposition 4 (`γ/(1−β)` with no terminal action) | **Known / folklore.** Appears as the shift `β(δ+γ_E)/(1−β)` in the literature. |
| Corollary 1 (= V11 Thm 7.1) | **Correct but answers a mis-posed question.** Demote to a remark motivating Proposition 2. |
| Proposition 5 (recursion, bounds, constancy criterion, survival interpretation) | **Correct; low novelty.** Recursion is isomorphic to the soft-Q entropy-bonus recursion; bounds are an immediate monotone-operator consequence. The constancy criterion and the survival-time reading are new *as statements* but are remarks, not theorems. |
| **Proposition 2 (anchor / convention-invariance incompatibility)** | **The contribution.** Modest and narrow, but not in the literature as far as I can establish. |
| **Proposition 3 (the wedge is `−βκ`, uniform, concentrated on the exit margin)** | **The contribution, and the practically useful half.** Gives a correction factor rather than a bracket. |

**Adjacent literature that must be cited and positioned against:** Ermon et al. (first identification of the DDC/entropy-regularised-IRL equivalence); Mai & Jaillet (2020) (equivalence in both forward and inverse directions) — **this citation could not be confirmed on 4 October 2026 and is withdrawn**; the nearest locatable work is Bui, Mai and Jaillet (2022), arXiv:2208.09611; *A Lecture Note on Offline RL and IRL, Part II: Foundations of Inverse Reinforcement Learning and Dynamic Discrete Choice Models*, arXiv:2605.30843, reported to give the `δ = −γ_E` normalisation explicitly (see the verification note below); Kostrikov et al. (2019, arXiv:1809.02925) and Al-Hafez, Tateo, Arenz, Zhao and Peters (2023, *LS-IQ*, arXiv:2303.00599) on *termination/survival bias*, which is the same problem named from the IRL side; Magnac & Thesmar (2002); Cao, Cohen & Szpruch (2021); Schlaginhaufen & Kamgarpour (2023); van der Laan, Kallus & Bibaut (2025, arXiv:2509.21172) and van der Laan, Bibaut & Kallus (2025, arXiv:2512.24407) — two distinct papers, both present as PDFs in the project's `references/`.

**Load-bearing verification — do this first.** Proposition 1 is attributed to arXiv:2605.30843, and the whole novelty assessment in the table above depends on that attribution: if the `δ = −γ_E` normalisation and the resulting literal equality of the two Bellman equations are *not* in that paper, then Proposition 1 may be novel after all and this document's framing is too conservative rather than too strong. The paper's title and identifier are confirmed from a search result; the specific passage was read from search-result content whose stored copy retained only titles and URLs, so it cannot be re-checked from the project files. **Open the paper and confirm the passage before relying on this section either way.** The same applies to the equivalent statement quoted in `PROJECT_X_AUDIT.md` §2.1, which is what retired V11's Theorem 7.1.

**Citation hygiene.** Years for the two van der Laan et al. papers are 2025 (arXiv 2509 and 2512), not 2026 as V11 recorded them; V11's "2026" appears to track a later revision. The Ermon et al. and Mai & Jaillet (2020) attributions reached this document through a secondary source and are **not yet traced to the primary papers** — do that before any submission. An earlier draft of this section also listed "Geng et al. (2020)", which could not be sourced and has been removed.

**A referee's strongest remaining objection,** which should be met in the text rather than hidden: *Proposition 3 is elementary once Proposition 1 is stated, and Proposition 1 is known.* The defence is that the composition is what practitioners get wrong — V11 itself is the worked example of getting it wrong, across eight self-audit passes — and that the resulting correction (`add βκ to continuation utilities`) is actionable and previously unstated. That is a research-note-sized defence. It is not a conference-paper-sized one.

---

## 7. What this means for the empirical claim

Proposition 3 says the convention wedge is a constant. It therefore **cannot** be detected by, or confused with, a state-dependent pattern in recovered utilities. Any state-dependent structure in `û` comes from the data, the discretisation, the smoothing, or a defect — not from the convention.

In the project's SEC results, the audit established that the state-dependent structure came from the last three: a degenerate transition matrix, and Laplace smoothing making `V̂` a function of cell sample size in 432 of 625 cells. V12 does not rehabilitate those results. It does make the correct prediction sharp enough to be testable on simulated data, which is what the rebuilt experiments should test:

> **Testable prediction.** Recover `û` from the same simulated CCPs under `κ = γ` and `κ = 0`. Then `max_x |û^γ(x,a) − û^0(x,a) + βγ|` should be at machine precision for every continuation action `a`, and within-continuation differences should agree to machine precision.

That is a sharp, falsifiable, zero-parameter check — and it is a far better validation target than "bounds satisfied: True."
