> ## SUPERSEDED. Do not cite the novelty verdicts in this document.
>
> Compiled 18 May 2026. At that date the project had not examined Kang (2026),
> *A Lecture Note on Offline RL and IRL, Part II: Foundations of Inverse
> Reinforcement Learning and Dynamic Discrete Choice Models*, arXiv:2605.30843.
> That note already contains the results rated novel below. Its Remark 2.9 gives
> the Gumbel location normalisation and the equality of the two Bellman
> equations. Its Section 3.2 states the anchor-action assumption and names an
> exit action as the example.
>
> Every NOVEL verdict in this document is withdrawn. The project's surviving
> contribution is computational, not theoretical. See `docs/PROJECT_X_AUDIT.md`
> Section 4 for the comparison, and `REPORT.md` for what is now claimed.
>
> "Ghost in the Machine" below was the project's working title in May 2026.
>
> The text below is preserved unedited. It records what the project believed in
> May 2026.

---

# Literature Gap Analysis — Ghost in the Machine vs. 19-paper reference set

**Compiled:** 18 May 2026
**Method:** Deep read (pages 1–5 first, then pages 12–18) of the 7 highest-overlap-risk papers (refs [01], [02], [04], [05], [06], [11], [16], [17]); abstract + page 1 read of the remaining 12 papers. **Phase 2 verification (18 May 2026):** also downloaded and deep-read Arcidiacono-Miller (2011) `[00a]` and (2019) `[00b]` foundational papers, plus deeper sections of [01] §6–7, [07] §1–4, [11] §3–4. Every claim below is verifiable by opening the cited PDF in the `references/` folder.
**Standard applied:** A paper "overlaps" with a contribution only if it proves the *same mathematical claim about the same mathematical objects*. Topical similarity without theorem-level overlap is not overlap.

---

## The project's 6 contributions, as stated in `mathematical modelling.pdf`

| # | Claim | Located in V10 |
|---|---|---|
| **C1** | Under absorbing exit + Gumbel shocks, no constant `c` satisfies `V(x) = V^soft(x) + c` for all `x ∈ 𝒳`. | Theorem 7.1 |
| **C2** | The discrepancy `D(x) := V(x) − V^soft(x)` satisfies the nonlinear functional equation `D(x) = ln[σ_0^soft + Σ_{a≥1} σ_a^soft · exp(β·E_a[D])] + γ`. | Proposition 7.2 |
| **C3** | `D*(x)` is bounded: `γ ≤ D*(x) ≤ γ/(1−β)` for every `x`, via monotone-operator argument. | Remark 7.3 |
| **C4** | For the continuation-only subproblem (`𝒜' = {1, 2}`, no absorbing state), `V' = V'^soft + γ/(1−β)` exactly and policies coincide. | Proposition 7.4 |
| **C5** | The iterative CCP estimation scheme is algebraically equivalent to a single-step closed-form procedure (no fixed-point iteration). | Theorem 6.3 |
| **C6** | Empirical demonstration on SEC EDGAR firm panel: N = 2,906 firms, 146,985 obs, 2009–2025, with corporate exit/maintain/growth actions. | §7, §8 of V10 |

---

## Per-paper overlap check

### Ref [01] — Zeng, Hong & Garcia (2024) *Structural Estimation of MDPs in High-Dim State Space with Finite-Time Guarantees*

**What they actually prove (verified pp. 2–5):**
- Single-loop ML-IRL algorithm with finite-time guarantee: O(ε⁻²) steps for ε-stationary solution.
- Their value function (their Eq 5b, p. 5): `V_θ(s) = log(Σ_ã exp Q_θ(s,ã))` — this is the **soft** value, no +γ_Euler.
- They cite [26] (a separate paper) for the **policy-level** equivalence of Gumbel-shock DDC and entropy-regularized RL (their Proposition 1 reference).
- They absorb the scale into r_θ; the +γ_Euler never appears explicitly.

**Overlap with project contributions:**
| Claim | Verdict | Reasoning |
|---|---|---|
| C1 (no constant shift, absorbing exit) | **NO OVERLAP** | They never compute `V − V^soft`; they work entirely in soft regime; no absorbing-exit analysis. |
| C2 (functional equation for D) | **NO OVERLAP** | They never define D(x). |
| C3 (bounds γ ≤ D ≤ γ/(1−β)) | **NO OVERLAP** | They never bound D. |
| C4 (continuation-subproblem equivalence) | **NO OVERLAP** | They don't decompose into continuation vs. exit subproblems. |
| C5 (one-step ≡ iterative CCP) | **NO OVERLAP** | Their single-loop algorithm is a *different* simplification (iterative one-step ML updates), not the iterative-CCP-≡-closed-form equivalence. |
| C6 (SEC empirical) | **NO OVERLAP** | They use MuJoCo robotics, not finance. |

**Verdict:** No theorem overlap. **Closest precedent that must be cited and positioned against in §1 and §6.** Position as: "Zeng et al. (2024) provide finite-time guarantees for a single-loop ML-IRL algorithm in the soft regime; we instead retain the full Gumbel-CCP value function and characterise its discrepancy from V^soft under absorbing exit."

---

### Ref [02] — Skalse & Abate (Nov 2024) *Partial Identifiability and Misspecification in IRL*

**What they actually prove (verified TOC + skim, 170-page paper):**
- Comprehensive framework characterising reward partial identifiability and misspecification robustness for **all** standard IRL behavioural models.
- §3.4 Reward Transformations: covers potential shaping, equivalence classes.
- §5 Partial Identifiability: invariances of policies, ambiguity tolerance.
- §6–§7 Misspecification With Equivalence Relations / Metrics.

**Overlap check:**
- C1–C4: Skalse-Abate's framework includes MaxEnt as one behavioural model among many. They characterise reward equivalence classes generically; they do **not** specifically compute the value-function discrepancy between Gumbel-CCP V and MaxEnt V^soft under absorbing exit.
- C5–C6: Out of scope (they don't do CCP estimation algorithms or SEC empirics).

**Verdict:** No theorem overlap. Cite as the modern foundational framework for IRL identifiability discussion; your §4 (identification) can position the Magnac-Thesmar normalisation result as a specific instance of their general partial-identifiability theory.

---

### Ref [03] — Skalse & Abate (Dec 2024, AAAI-25) *Partial Identifiability in IRL For Agents With Non-Exponential Discounting*

**Topic:** Hyperbolic/non-exponential discounting behavioural model. **Orthogonal** — your project uses exponential β = 0.976 discounting.

**Verdict:** **No overlap on any contribution.** Useful only as evidence that AAAI accepts identifiability-theory papers in IRL.

---

### Ref [04] — Schlaginhaufen & Kamgarpour (June 2023, ICML 2023) *Identifiability and Generalizability in Constrained IRL*

**What they actually prove (verified pp. 2–5):**
- Their Theorem 4.5 characterises rewards optimising for a given expert occupancy measure.
- Their Eq (13): `IRL_M(μ^E) = r^E + U = β log π^{μ^E} + U`, where `U = span(E − γP)` is the subspace of **potential shaping transformations**.
- Identifiability up to potential shaping `r̄(s,a,s') ↦ r̄(s,a,s') + η(s) − γη(s')`.

**Overlap check:**
- This is **reward** identifiability up to a **state-dependent** function η(s), not value-function discrepancy.
- They prove this for the **unconstrained MCE-IRL** case (citing Cao et al. 2021 + Skalse et al. 2022); their novel result is the **constrained** extension and showing it breaks for non-entropy regularizations.

**Verdict:** **No theorem overlap with C1–C5.** This is a *parallel* identification result for rewards, not value functions. Cite in your §4 as the modern ML-side re-derivation of Magnac-Thesmar identification (which your project uses for u₀-normalisation).

---

### Ref [05] — Cao, Cohen & Szpruch (Nov 2021) *Identifiability in Inverse Reinforcement Learning*

**What they actually prove (verified pp. 2–5):**
- Eq (4), p. 3: `V_λ^*(s) = λ log Σ_a exp((1/λ) Q_λ^*(s,a))` — soft value function, no +γ_Euler.
- Page 5, comparison with MaxEntIRL: explicit statement that "many IRL methods make the tacit assumption that the demonstrator agent is **myopic**", noting that MaxEntIRL (Ziebart et al.) assumes the value function is constant.
- Abstract: "given knowledge of the optimal policy under two different discount rates, or sufficiently different transition laws, we can uniquely identify the rewards (up to a constant shift)."

**Overlap check:**
- Their "constant shift" is a **reward**-level result (`r` ↔ `r + const`), not the **value-function** comparison between two different Bellman operators.
- They work entirely in the entropy-regularized regime; they do not compute `V_DDC − V^soft`.
- They do not address absorbing exit.

**Verdict:** **No theorem overlap with C1–C5.** Foundational citation for the IRL reward-identifiability literature; cite in §4.

---

### Ref [06] — Hao & Kasahara (May 2024) *CCP Estimation of DDC Models with 2-period Finite Dependence*

**What they actually prove (verified pp. 2–5):**
- Extends Arcidiacono-Miller (2011, 2019) on **finite dependence**.
- Shows many DDC models exhibit 2-period finite dependence under their generalised definition.
- Builds CCP estimator that exploits Kronecker product structure in state transitions.

**Overlap check:**
- They use the Hotz-Miller framework (your foundation) but their contribution is **computational efficiency** via finite dependence, not the **algebraic equivalence of iterative vs one-step CCP** (your C5).
- They do reference absorbing/terminal states (p. 2): "finite dependence... arises when there is a terminal or absorbing state." This is a *property they exploit*, not the *value-function discrepancy* you analyse.

**Verdict:** **No theorem overlap with C5.** Direct contemporary extension of Hotz-Miller — cite in §6 (estimation) and in your §1 related-work discussion of modern CCP advances.

---

### Ref [07] — Renard, Schlaginhaufen, Ni & Kamgarpour (March 2025) *Convergence of a Model-Free Entropy-Regularized IRL Algorithm*

**Topic:** Sample complexity guarantees O(1/ε²) and O(1/ε⁴) for model-free entropy-reg IRL.

**Overlap check:** Algorithmic / sample-complexity paper. They prove a different kind of theorem (convergence rates), not the value-function discrepancy. **No overlap with C1–C5.**

**Verdict:** Cite in §8.2 (statistical properties) for modern sample-complexity context.

---

### Refs [08]–[15] — Surveys, extensions, applications

| Ref | Brief description | Overlap verdict |
|---|---|---|
| [08] Liu et al. 2024 — TMLR survey on inverse constrained RL | **No overlap.** Survey of constrained-IRL literature. Cite as related-work survey. |
| [09] Zhang et al. 2025 — IRL under overparameterization | **No overlap.** Neural-net extension of ML-IRL. |
| [10] Wu et al. 2026 — Distributional IRL | **No overlap.** Different framework (return distributions). |
| [11] Jhaveri et al. 2025 (NeurIPS 2025) — Entropy-reg + distributional RL convergence | **No overlap.** Temperature-decoupling gambit; no absorbing-exit analysis. |
| [12] Norets & Shimizu 2023 — Semiparametric Bayesian DDC | **No overlap.** Relaxes the Gumbel-shock assumption (uses location-scale mixtures); your project assumes Gumbel. Cite as alternative-distribution work. |
| [13] Gui & Doshi 2025 (ICLR 2026 UR) — Transferable rewards via abstracted states | **No overlap.** State-abstraction direction. |
| [14] Blevins 2025 — Continuous-time DDC games | **No overlap.** Continuous-time framework; yours is discrete-time. |
| [15] Ghanem et al. 2025 — Recursive deep IRL | **No overlap.** Online/recursive algorithm; yours is one-step closed-form. |

---

### Ref [16] — Krishnamurthy (July 2025) *IRL using Revealed Preferences and Passive Stochastic Optimization*

**What it actually is (verified pp. 2–5):**
- Cornell PhD-course monograph drawn from his Cambridge book *Partially Observed MDPs*, 2nd ed. (2025).
- Chapter 1 uses **classical static Afriat's theorem** for single-period utility maximization (cognitive radar, sensors).
- Chapter 2 covers Bayesian IRL and inverse stopping-time problems.
- Chapter 3 covers adaptive IRL via Langevin dynamics.

**Overlap check:**
- Krishnamurthy works in the **static** revealed-preference framework (Afriat); your project works in **dynamic** discrete-choice MDP with Gumbel shocks.
- Different mathematical objects entirely. He doesn't prove anything about Gumbel-CCP vs MaxEnt or absorbing exit in the dynamic sense.

**Verdict:** **No theorem overlap.** Useful framing citation: "revealed-preferences" terminology has academic precedent in IRL literature.

---

### Ref [17] — van der Laan, Kallus & Bibaut (May 2026) *IRL with Just Classification and a Few Regressions*

**What they actually prove (verified pp. 2–5):**
- They explicitly bridge DDC and MaxEnt IRL: "**dynamic discrete choice and MaxEnt IRL reduce to the same mathematical object: a soft Bellman system with a softmax policy**" (p. 4).
- Their Eq for Q^†: `Q^† = r^† + γPV^†`; their Ξ operator: `V^†(s) = ΞQ^†(s) = log Σ_a e^{Q^†(s,a)}` — soft Bellman, no +γ_Euler explicit.
- "Without loss of generality, we set τ = 1 and absorb the scale into r^†." — they **absorb the +γ_Euler-scale** into the reward.
- Main contribution: characterise reward identifiability via **statewise affine normalisations**, reduce IRL to classification + regression (GenPQR algorithm).

**OVERLAP CHECK — THIS IS THE HIGHEST-RISK PAPER:**

| Claim | Verdict | Reasoning |
|---|---|---|
| C1 (no constant shift, absorbing exit) | **NO OVERLAP — but folk wisdom present** | They state the equivalence "DDC ≡ MaxEnt IRL as soft Bellman" without proof and without addressing absorbing exit. Your Thm 7.1 refines exactly this: the equivalence holds at the policy level but the value functions differ by a state-dependent function under absorbing exit. |
| C2 (functional equation for D) | **NO OVERLAP** | They never compute the discrepancy; they absorb it into the reward. |
| C3 (bounds γ ≤ D ≤ γ/(1−β)) | **NO OVERLAP** | They don't bound the discrepancy. |
| C4 (continuation-subproblem γ/(1−β) equivalence) | **NO OVERLAP** | They don't decompose. |
| C5 (one-step ≡ iterative CCP) | **NO OVERLAP** | Their algorithm is fitted-Q + classification, not Hotz-Miller iteration. |

**Verdict:** **No theorem overlap, but their framing claim "DDC ≡ MaxEnt" is the exact piece of folk wisdom your Theorem 7.1 corrects under absorbing exit.** This paper is the most important citation in your §1: "Recent work (van der Laan, Kallus & Bibaut, 2026) explicitly identifies DDC and MaxEnt IRL as the same mathematical object via the soft Bellman equation, by absorbing the Euler-Mascheroni scale γ into the reward parametrisation. We instead retain the explicit Gumbel-CCP value function with +γ and show that under absorbing exit this scale cannot be absorbed into a constant — Theorem 7.1."

This is a *strengthening* of your novelty claim, not a threat. They make the loose equivalence claim; you refine it.

---

### Refs [18]–[19] — Finance & healthcare applications

| Ref | Description | Overlap verdict |
|---|---|---|
| [18] Leukam et al. 2025 — Portfolio with GIRL | **No overlap.** Application paper using GIRL on portfolio data. Cite as finance IRL precedent. |
| [19] Fang et al. 2024 — Offline ICRL in healthcare | **No overlap.** Healthcare application of inverse constrained RL. Cite as offline-IRL precedent. |

---

## Final novelty verdict

| Claim | Novelty status | Confidence |
|---|---|---|
| **C1** No constant shift V = V^soft + c under absorbing exit (Thm 7.1) | **NOVEL** | High — no paper computes the discrepancy as a function of x under absorbing exit. The closest, [17], makes the opposite (folk-equivalence) claim that you refute. |
| **C2** Functional equation for D(x) (Prop 7.2) | **NOVEL** | High — D(x) is never written down in the reference set. |
| **C3** Bounds γ ≤ D*(x) ≤ γ/(1−β) (Rmk 7.3) | **NOVEL** | High — no paper produces these specific bounds with a monotone-operator proof. |
| **C4** Exact γ/(1−β) equivalence in continuation subproblem (Prop 7.4) | **NOVEL** | High — this is a precise structural result that nobody else states. [04] proves *reward* identifiability up to potential shaping in continuous-action MDPs but not this specific value-function equivalence in the continuation subproblem. |
| **C5** Iterative-CCP ≡ one-step closed-form (Thm 6.3) | **NOVEL** | Medium-high — Arcidiacono-Miller (2011, 2019) and Hao-Kasahara (2024) develop CCP estimation techniques but do not prove this specific algebraic equivalence between iterative-CCP and the direct closed-form procedure. Recommend double-checking against Arcidiacono-Miller 2011/2019 (not in folder, pre-2021) before final submission. |
| **C6** SEC firm exit/maintain/growth application | **NOVEL setting** | High — no prior IRL or DDC paper found applying this exact framework to SEC EDGAR corporate exit. The closest, [18], is portfolio choice, not firm exit. |

## Threat assessment

**Highest-risk citation to position against:** Ref [17] van der Laan/Kallus/Bibaut (2026). They state "DDC and MaxEnt IRL reduce to the same mathematical object" — this is the folk wisdom your Thm 7.1 corrects under absorbing exit. **You MUST cite them in §1 and explicitly state the refinement.**

**Second-highest-risk:** Ref [01] Zeng/Hong/Garcia (2024). The "DDC↔IRL bridge with finite-time guarantees" framing is widely cited and your paper should clarify how your contribution differs (you provide a structural decomposition result; they provide an algorithm with rate guarantees).

**Other papers requiring explicit positioning in your related work:**
- [00a] Arcidiacono-Miller 2011 — **for §6 (CCP estimation); your Thm 6.3 is derivative of their representation theorem** (added Phase 2)
- [00b] Arcidiacono-Miller 2019 — for §6 (finite dependence framework)
- [04] Schlaginhaufen/Kamgarpour 2023 — for §4 (identification)
- [05] Cao/Cohen/Szpruch 2021 — for §4 (identification)
- [06] Hao/Kasahara 2024 — for §6 (CCP estimation)
- [11] Jhaveri et al. 2025 — for §2 (Bellman contraction theory)
- [16] Krishnamurthy 2025 — for §1 (revealed-preference framing precedent)

**No papers in the references folder pose a direct threat to your novelty claim.** The risk is *framing*, not *priority* — you must clearly distinguish your value-function discrepancy result from existing reward-identifiability results, and clearly distinguish your structural theorem (Thm 7.1) from existing folk-equivalence claims.

## Action items

1. ~~**Read Arcidiacono-Miller (2011, *Econometrica*) and Arcidiacono-Miller (2019)** in full.~~ ✅ **DONE in Phase 2 verification (18 May 2026).** Both PDFs added as `00a_ArcidiaconoMiller2011_CCP_Heterogeneity.pdf` and `00b_ArcidiaconoMiller2019_NonstatFiniteDependence.pdf`. See `VERIFICATION_REPORT.md` Item #1.
2. **Verify the AAAI bibliography format requirement** for citing arXiv preprints vs. journal versions. Ref [01] is published in *Operations Research* 73(2); refs [02], [10], [13] are arXiv-only.
3. **Write the §1 positioning paragraph** that explicitly cites [17] and states your Thm 7.1 as the refinement.

---

## Phase 2 verification results (18 May 2026)

### Arcidiacono-Miller 2011 [00a] — IMPACT ON THM 6.3 NOVELTY

**What AM 2011 actually proves (verified pp. 1–9):**

- **Main theorem:** The expected value of future utilities from optimal decision making can be expressed as a function of flow payoffs and conditional choice probabilities for **any sequence of future choices**, optimal or not. This is the "representation theorem" foundation of CCP estimation.
- **Their Eq (2.4), p. 7:** `v_2(x,s) = θ_1·x + θ_2·s + β·ln[exp(v_1(x+1,s)) + exp(v_2(x+1,s))] + β·γ` — explicit `+β·γ` Euler term in the conditional value function recursion.
- **Their Eq (2.6), p. 7:** `v_1(x,s) = β·v_1(0,s) − β·ln(p_1(0,s)) + β·γ` — direct recovery of conditional value from CCPs.

**Verdict on your Thm 6.3:**

Your V10 §C one-step procedure is **a specialisation of AM 2011's representation theorem** to the absorbing-exit three-action case. AM 2011 already establishes that V can be expressed as a function of CCPs and flow payoffs WITHOUT iteration. Therefore:

- **Your Thm 6.3 is NOT a fundamentally novel contribution.** It is an algebraic consequence of AM 2011's representation theorem applied to the V10 framework.
- **Honest positioning:** "We make explicit the one-step reduction of the V10 iterative scheme of editions 2–5, applying the representation theorem of Arcidiacono-Miller (2011) to the absorbing-exit three-action case. The resulting closed-form recovery procedure (Eqs 28a, 28b, 28c) requires no fixed-point iteration."
- **Demote Thm 6.3 to a methodological clarification.** Your headline novelty load is carried by Thm 7.1, Prop 7.2, Rmk 7.3, Prop 7.4.

### Arcidiacono-Miller 2019 [00b] — IMPACT ON FINITE DEPENDENCE FRAMING

**What AM 2019 proves (verified pp. 1–6):**

- Generalises the finite-dependence definition of AM 2011 by allowing **negative weights** on conditional value functions: "the ex-ante value function can be expressed as a weighted average of the conditional value functions of all the alternatives plus a function of the conditional choice probabilities, where all the weights sum to one but some may be negative or greater than one."
- Provides a systematic algorithm to determine whether finite dependence holds in a model with a large finite state space.

**Verdict:** No overlap with your contributions. AM 2019 is a methodological extension of AM 2011 in a direction orthogonal to your work (finite dependence is *about computational efficiency*, not about the Gumbel-CCP/MaxEnt discrepancy). Cite [00b] in §6 (estimation) when discussing the modern finite-dependence literature.

### [01] Zeng et al. §6–7 deep read — REFINED INVOCATION

**Cor 1(ii) of Zeng et al. (verified p. 13):** Uses a **reference-action normalisation** — "the ground-truth reward value `r(s,ā;θ*)` for a reference action `ā ∈ 𝒜` and `s ∈ 𝒮` are known" — to uniquely pin down the optimal solution. **This is the ML-side parallel to your Magnac-Thesmar normalisation `u(x,0) = W̃(x)`.**

**Refined verdict:** Cite Cor 1(ii) of [01] alongside [04], [05] in §4 (identification) as a modern ML convergence point on reference-action normalisation. No overlap with Thm 6.3.

### [11] Jhaveri et al. §3–4 deep read — REFINED INVOCATION

**Their results (verified pp. 3–8):**
- "Temperature decoupling gambit" — they study τ → 0 limit of entropy-regularised RL with a decoupled temperature schedule σ(τ) such that σ/τ → 0.
- Theorem 3.9: policies converge to "optimality-filtered reference-optimal" policy in vanishing-temperature limit.
- Theorem 4.2: Soft distributional Bellman operator is γ-contraction in `d̄_p`.

**Refined verdict:** **No overlap with your Prop 7.4.** Their work studies the VANISHING-temperature limit (τ → 0), yours is at FIXED temperature (β = 0.976, γ = γ_Euler). Different mathematical objects. Cite Theorem 4.2 in §2 (Bellman contraction). Cite the τ → 0 work in a §7 footnote as orthogonal to your fixed-temperature discrepancy result.

### [07] Renard et al. deep read — IMPACT ON ITEM #5 (bootstrap)

**Their results (verified pp. 2–7):**
- Theorem 4.3: O(γ^H) + O(1/√T) reward sub-optimality bound for their iterative stochastic gradient algorithm.
- Cor 4.7: O(1/ε²) sample complexity for ε-approximate reward recovery.

**Refined verdict:** Their bounds are for a **different algorithm** (iterative gradient descent on a stochastic objective), not directly applicable to your one-step closed-form estimator. Cite [07] as the modern context for sample-complexity bounds in entropy-regularised IRL, but acknowledge that the **cluster bootstrap is the correct inference method for your two-step semiparametric estimator** (V10 §8.2; Murphy-Topel 1985).

**Code action item:** Extend `src/bootstrap.py` to also bootstrap `ω̂` (the WLS coefficients) — see `VERIFICATION_REPORT.md` Item #5 for the ~20 LOC fix.

## Final refined novelty table (post Phase 2)

| Claim | Novelty status | Confidence |
|---|---|---|
| **C1** No constant shift V = V^soft + c under absorbing exit (Thm 7.1) | **NOVEL** | High — confirmed by [17] absorbing-into-r reading |
| **C2** Functional equation for D(x) (Prop 7.2) | **NOVEL** | High |
| **C3** Bounds γ ≤ D*(x) ≤ γ/(1−β) (Rmk 7.3) | **NOVEL** | High |
| **C4** Exact γ/(1−β) equivalence in continuation subproblem (Prop 7.4) | **NOVEL** | High — confirmed by [11] τ → 0 reading (different question) |
| **C5** Iterative-CCP ≡ one-step closed-form (Thm 6.3) | **DERIVATIVE** — algebraic consequence of [00a] AM 2011 representation theorem | High confidence in this verdict |
| **C6** SEC firm exit/maintain/growth application | **NOVEL setting** | High |
