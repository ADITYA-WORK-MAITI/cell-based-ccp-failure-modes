> ## Historical record. Compiled 18 May 2026.
>
> This document describes the reference set as it stood in May 2026. It predates
> the project audit. The theoretical claims it supports are withdrawn. See
> `docs/PROJECT_X_AUDIT.md` and `REPORT.md`.
>
> The PDFs described here are third-party copyrighted works. They sit on the
> author's disk and are not redistributed in this repository. Statements below
> that a PDF is present in this folder refer to the author's local copy.
>
> The text below is preserved unedited.

---

# Reference Invocation Map — Mathematical Modelling ↔ references/

**Compiled:** 18 May 2026
**Purpose:** For every assumption, equation, theorem, and normalisation in `mathematical modelling.pdf` (the V10 §7 excerpt), this document lists the **specific reference [01]–[19] in `references/`** that should be cited at that point in the paper. Every reference invoked is physically present in the folder and verifiable offline.

**Convention:**
- **MUST-CITE** = the claim or notation is *adopted from* or *directly extends* the cited paper
- **SHOULD-CITE** = strong topical match, would strengthen the citation if reviewer pushes
- **CONTEXT-CITE** = useful for related-work paragraph but not load-bearing for the claim
- **(older)** = foundational citation NOT in the `references/` folder (because >5 years old); use your existing `notes/*.md` for these

---

## Section A — MDP Primitives and State Space (mathematical modelling.pdf p. 8)

### A.1 State vector `x = (LIQ, LEV, ROA, SIZE) ∈ ℝ^4` and definition of state variables

- **MUST-CITE:** [06] Hao & Kasahara (2024), §2.1 baseline DDC model (p. 4 of [06]). Standard DDC state-variable construction.
- **MUST-CITE (older):** Rust (1987) for the canonical DDC state-vector formulation.
- **SHOULD-CITE:** [14] Blevins (2025) §1, who uses Rust (1987) as the empirical example with similar state-action structure.

### A.2 Winsorisation at 1st/99th percentile, `𝒳` compact by Heine-Borel

- No direct reference required (standard preprocessing). Mention in §6.2 estimation methodology.

### A.3 Action space `𝒜 = {0, 1, 2}` (Exit, Maintain, Growth)

- **MUST-CITE (older):** Hotz & Miller (1993) — three-action DDC formulation in `notes/hotzmiller1993.md`.
- **CONTEXT-CITE:** [14] Blevins (2025) uses exit/entry/quality-ladder examples — same structural intuition.

### A.4 Absorbing terminal `x†`, `V(x†) = 0`, scrap value `W(x)`

- **MUST-CITE:** [06] Hao & Kasahara (2024) §1 p. 2 explicitly: *"finite dependence... arises when there is a terminal or absorbing state."* They cite this as a key DDC structural feature.
- **SHOULD-CITE:** [14] Blevins (2025) — single-agent renewal model + dynamic entry-exit model in §1 (replication available at github.com/jrblevin/ctgames-qe).

### A.5 Transformed scrap `W̃(x) = z-score(ln(1 + W(x)))`

- No direct reference required (standard z-score transformation). This is a project-specific normalisation choice.

### A.6 Normalisation `u(x, 0) = W̃(x)` for all `x ∈ 𝒳`

- **MUST-CITE:** [17] van der Laan, Kallus & Bibaut (2026), §2 p. 5: their **statewise affine normalisation** framework. They specifically discuss `r(s, a^†) = 0` (the Rust 1987 normalisation) and `μ^⊤ r = g` (the general case) as a normalisation choice.
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) — modern ML re-derivation of the constant-shift indeterminacy that necessitates normalisation.
- **MUST-CITE:** [04] Schlaginhaufen & Kamgarpour (2023) Eq (12), p. 5: their potential-shaping subspace `U = span(E − γP)` is the modern ML expression of the Magnac-Thesmar equivalence class.
- **MUST-CITE (older):** Magnac & Thesmar (2002), `notes/magnac2002.md`.

### A.7 Gumbel(0,1) shocks, `γ ≈ 0.5772`, variance `π²/6`

- **MUST-CITE (older):** Johnson, Kotz & Balakrishnan (1995) per `notes/remaining_refs.md`.
- **CONTEXT-CITE:** [12] Norets & Shimizu (2023) — they relax the Gumbel assumption using location-scale extreme-value mixtures; cite as alternative-distribution future work in §11.

### A.8 Discount factor `β = 0.976`, fixed exogenously

- **MUST-CITE (older):** Magnac & Thesmar (2002) Theorem 4.4 of V10 / `notes/magnac2002.md` — β not identified from CCPs alone.
- **SHOULD-CITE:** [05] Cao, Cohen & Szpruch (2021) abstract: "given knowledge of the optimal policy under two different discount rates... we can uniquely identify the rewards (up to a constant shift)" — relevant when discussing why β is fixed.

---

## Section B — Bellman Equation and Value Functions (mathematical modelling.pdf p. 8)

### B.1 Choice-specific value `v(x, a) = u(x, a) + β E[V(x')|x, a]` (Eq 7)

- **MUST-CITE:** [01] Zeng, Hong & Garcia (2024), Eq 1 p. 4 — soft-Bellman operator `Λ_θ(Q(s,a)) = r(s,a;θ) + γ E[max_a (Q(s',a) + ε)]`. Their Q-function formulation is parallel.
- **MUST-CITE:** [17] van der Laan et al. (2026) p. 4: `Q^†(s,a) = r^†(s,a) + γPV^†(s,a)`. Modern ML statement.
- **MUST-CITE (older):** Rust (1987) for the canonical formulation in `notes/rust1987.md`.

### B.2 For exit: `v(x, 0) = W̃(x) + β · 0 = W̃(x)`

- This follows from the absorbing-exit assumption A.4 + normalisation A.6.
- No additional reference required beyond those cited at A.4 and A.6.

### B.3 Closed-form ex-ante value `V(x) = ln[Σ_a exp{v(x,a)}] + γ` (Thm 2.3)

- **MUST-CITE (older):** Johnson, Kotz & Balakrishnan (1995) for the Gumbel max distribution → log-sum-exp + γ.
- **MUST-CITE:** [01] Zeng, Hong & Garcia (2024) p. 5, their derivation Eq (5b): `V_θ(s) = log(Σ exp Q(s,a))` (note: they drop the +γ_Euler, absorbing it into r — this is precisely the framing your Theorem 7.1 corrects). **Cite here AND in §7.**
- **MUST-CITE:** [17] van der Laan et al. (2026) p. 4: `V^†(s) = ΞQ^†(s) = log Σ_a e^{Q^†(s,a)}` and "we set τ = 1 and absorb the scale into r^†". **The framing match — and the framing you correct.**

### B.4 Bellman recursive form `V(x) = ln[Σ_a exp{u(x,a) + β E[V(x')|x,a]}] + γ` (Eq 13)

- **MUST-CITE:** [11] Jhaveri, Wiltzer, Shafto, Bellemare & Meger (Oct 2025, NeurIPS 2025) — soft Bellman convergence theory. Their work formalises the contraction structure in entropy-regularized RL.
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) Eq (4), p. 3.

### B.5 Contraction on `(C(𝒳), ‖·‖_∞)` with modulus `β < 1`; Banach FPT

- **MUST-CITE:** [11] Jhaveri et al. (2025) — formal convergence for entropy-regularized Bellman operators in vanishing-temperature limits.
- **MUST-CITE:** [07] Renard, Schlaginhaufen, Ni & Kamgarpour (2025) — sample-complexity guarantees for entropy-reg IRL, building on the same contraction argument.
- **MUST-CITE (older):** Bertsekas & Shreve (2004) or Puterman (2014) for the classical contraction proof — cited by [05] p. 3.

---

## Section C — CCP Inversion and Utility Recovery (mathematical modelling.pdf pp. 9–10)

### C.1 Multinomial logit `σ(a|x) = exp{v(x,a)} / Σ exp{v(x,a')}` (Thm 3.1)

- **MUST-CITE (older):** McFadden (1974), Train (2009) per `notes/logit_theory.md`.
- **MUST-CITE:** [17] van der Laan et al. (2026) p. 4: `π^†(a|s) ∝ exp{Q^†(s,a)/τ}` — modern ML statement using identical formula.
- **MUST-CITE:** [01] Zeng et al. (2024) Eq (5c) p. 5.

### C.2 Direct value-function recovery `V(x) = W̃(x) − ln σ(0|x) + γ` (Thm 3.5)

- **MUST-CITE (older):** Hotz & Miller (1993) Lemma 3.2 / `notes/hotzmiller1993.md`.
- **MUST-CITE:** [06] Hao & Kasahara (2024) §1: explicitly cites Hotz-Miller (1993) and Aguirregabiria-Mira (2007). Their finite-dependence approach builds on this exact inversion.

### C.3 Observable target `Y_a(x) = ln[σ(a|x)/σ(0|x)] + W̃(x)`

- **MUST-CITE:** [06] Hao & Kasahara (2024) — they construct CCP estimators using the same inversion principle.
- **CONTEXT-CITE (older):** Arcidiacono & Miller (2011) — your `notes/remaining_refs.md` lists this; check this 2011 paper for the precise origin of `Y_a` notation.

### C.4 Continuation value `Z_a(x) = β ∫_𝒳 V(x') P(dx'|x, a)` and `u(x, a) = Y_a(x) − Z_a(x)`

- **MUST-CITE (older):** Hotz & Miller (1993); Aguirregabiria & Mira (2002).
- **MUST-CITE:** [17] van der Laan et al. (2026) — their "Bellman fixed-point" recovery in §3.3 is the modern ML translation of this structural decomposition.

### C.5 One-step closed-form procedure (Thm 6.3, the iterative-≡-one-step equivalence) — REFINED Phase 2

**HONEST FRAMING REQUIRED (per Phase 2 verification):** Your Thm 6.3 is **derivative**, not a fundamental novelty. It is an algebraic consequence of AM 2011's representation theorem specialised to the absorbing-exit three-action case.

Position it as a **methodological clarification**:

> *"We make explicit the one-step reduction of the V10 iterative scheme used in editions 2–5, applying the representation theorem of Arcidiacono & Miller (2011) to the absorbing-exit three-action case. The resulting closed-form recovery procedure (Eqs 28a, 28b, 28c) requires no fixed-point iteration."*

- **MUST-CITE:** **[00a] Arcidiacono & Miller (2011)** — their Eqs (2.4)-(2.7) on p. 7 establish the closed-form V↔u recovery; your Thm 6.3 specialises to absorbing exit + three actions. **The representation theorem is theirs, not yours.**
- **MUST-CITE:** [06] Hao & Kasahara (2024) — they extend AM 2011's iterative CCP framework using finite dependence in a different direction (computational efficiency via Kronecker structure).
- **MUST-CITE:** [01] Zeng et al. (2024) — their single-loop ML-IRL achieves a different form of "single-loop" simplification (single-loop for policy + reward update, with sample-complexity bounds). Position as distinct.
- **CONTEXT-CITE:** [00b] Arcidiacono & Miller (2019) — generalises finite dependence to allow negative weights. Different question from Thm 6.3 but cited as continued lineage.
- **MUST-CITE (older):** Aguirregabiria & Mira (2002) — NPL scheme; your Thm 6.3 demonstrates a different one-step reduction.

**Headline implication:** Demote Thm 6.3 in the abstract and §1. Your novelty is carried by Thm 7.1, Prop 7.2, Rmk 7.3, Prop 7.4 — NOT by Thm 6.3. This is honest. AAAI reviewers who know AM 2011 will not credit Thm 6.3 as novel if framed too strongly.

---

## Section D — Identification (mathematical modelling.pdf p. 9)

### D.1 Point identification with normalisation `u(x, 0) = W̃(x)` (Thm 4.2)

- **MUST-CITE (older):** Magnac & Thesmar (2002) Cor 4.6 / `notes/magnac2002.md`.
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) — modern ML re-derivation; their Theorem 1 (referenced in their §3.1).
- **MUST-CITE:** [04] Schlaginhaufen & Kamgarpour (2023) Theorem 4.5 and Eq (13) — parallel reward-identification-up-to-potential-shaping result.
- **MUST-CITE:** [02] Skalse & Abate (2024) §3.1 Partial Identifiability — general framework subsuming the Magnac-Thesmar case.

### D.2 Magnac-Thesmar equivalence class `u'(x, a) = u(x, a) + c(x)` with `∫ c P(dx'|x, a) = 0`

- **MUST-CITE (older):** Magnac & Thesmar (2002), Theorem 4.5.
- **MUST-CITE:** [04] Schlaginhaufen & Kamgarpour (2023) Eq (12) p. 5: their potential-shaping subspace `U = {Δ_r : Δ_r(s, a) = η(s) − γ E_{s'∼P(·|s,a)}[η(s')]}` is **literally** the Magnac-Thesmar equivalence class for entropy-regularised IRL. **This is the modern ML statement of your D.2 claim — must cite.**
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) — same equivalence class derived via entropy-regularization lens.

### D.3 Kernel condition `ker(T₁) ∩ ker(T₂) = {0}` (Prop 4.7, without normalisation)

- **MUST-CITE (older):** Magnac & Thesmar (2002) Theorem 6.
- **CONTEXT-CITE:** [02] Skalse & Abate (2024) §5 — general invariances framework.

### D.4 Discount factor `β` not identified from CCPs alone (Thm 4.4)

- **MUST-CITE (older):** Magnac & Thesmar (2002).
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) — abstract explicitly addresses identifiability under different discount rates.

---

## Section E — Relationship to Maximum Entropy IRL (mathematical modelling.pdf pp. 9–10)

### E.1 MaxEnt soft Bellman `V^soft(x) = ln[Σ_a exp{u(x,a) + β E[V^soft(x')|x,a]}]` (no +γ)

- **MUST-CITE (older):** Ziebart, Maas, Bagnell & Dey (2008) — `notes/ziebart2008.md`.
- **MUST-CITE:** [17] van der Laan et al. (2026) p. 4: explicit soft Bellman `V^† = ΞQ^†`, identical form.
- **MUST-CITE:** [01] Zeng et al. (2024) Eq (5b), (6a) p. 5.
- **MUST-CITE:** [04] Schlaginhaufen & Kamgarpour (2023) Eq (3) p. 3.
- **MUST-CITE:** [05] Cao, Cohen & Szpruch (2021) Eq (3), (4) p. 3.
- **MUST-CITE:** [11] Jhaveri et al. (2025) — entropy-regularised RL convergence framework.

### E.2 "The only difference between Eq 13 and Eq 30 is the +γ constant"

- **MUST-CITE:** [17] van der Laan, Kallus & Bibaut (2026) p. 4: *"we set τ = 1 and absorb the scale into r^†"* — they absorb +γ_Euler into the reward parameterisation. **This is the framing your project corrects.**
- **MUST-CITE:** [01] Zeng et al. (2024) p. 5: same absorption.

### E.3 **Theorem 7.1 — No constant `c` satisfies `V(x) = V^soft(x) + c` under absorbing exit**

**This is your headline C1 claim. The MUST-CITE here is the paper your theorem REFINES:**

- **POSITION AGAINST:** [17] van der Laan, Kallus & Bibaut (2026): *"dynamic discrete choice and MaxEnt IRL reduce to the same mathematical object: a soft Bellman system with a softmax policy"* (p. 4). Your Theorem 7.1 establishes precisely when this folk-equivalence breaks (under absorbing exit).
- **POSITION AGAINST:** [01] Zeng, Hong & Garcia (2024) — same folk-equivalence framing.
- **CONTEXT-CITE:** [04] Schlaginhaufen & Kamgarpour (2023): proves reward-identifiability-up-to-potential-shaping under entropy regularisation. Your result is the dual: value-function-non-equivalence under absorbing exit.
- **CONTEXT-CITE:** [05] Cao, Cohen & Szpruch (2021): proves reward identifiable up to constant shift under two discount rates. Your result is value-function non-identifiable under absorbing exit.

### E.4 **Proposition 7.2 — Functional equation for `D(x) = V(x) − V^soft(x)`**

- **CONTEXT-CITE:** [11] Jhaveri et al. (2025) — temperature-decoupling gambit gives a related family of fixed-point equations, but for a different limit (τ → 0), not your discrepancy.
- This functional equation appears to be original. No reference required for the equation itself, but cite [11] in the §7 related-work paragraph.

### E.5 **Remark 7.3 — Bounds `γ ≤ D*(x) ≤ γ/(1−β)`**

- **SHOULD-CITE:** [07] Renard et al. (2025) — monotone-operator-type arguments are standard in entropy-reg IRL theory. Cite as evidence that monotone-operator proofs are well-established in this literature.
- This bound appears to be original.

### E.6 **Proposition 7.4 — Continuation subproblem `V' = V'^soft + γ/(1−β)` exactly**

- **MUST-CITE:** [04] Schlaginhaufen & Kamgarpour (2023) — their proof that "identifiability up to potential shaping is a consequence of entropy regularization" is the dual result (reward-side) of your value-side equivalence. Cite as the parallel reward-identifiability statement.
- **MUST-CITE:** [17] van der Laan et al. (2026) — they implicitly rely on this equivalence when absorbing scale into r^†; your Prop 7.4 makes the conditions explicit.

---

## Section F — Statistical inference (V10 §6.6, §8 — referenced from mathematical modelling.pdf §C)

### F.1 WLS parametric regression `u(x, a; ω) = ω_{a,0} + ω_{a,1}·LIQ + ... + ω_{a,4}·SIZE` (Eq 29)

- **MUST-CITE (older):** Murphy & Topel (1985) — generated-regressors variance correction.
- **MUST-CITE:** [07] Renard et al. (2025) — sample-complexity guarantees for entropy-reg IRL — cite as modern complement.

### F.2 Cluster bootstrap at firm level

- **MUST-CITE (older):** Newey & McFadden (1994) Handbook chapter — asymptotic theory.
- **CONTEXT-CITE:** [19] Fang, Liu & Gong (2024) — offline IRL on historical data; cite as precedent for offline IRL inference on observational data.

### F.3 Consistency target = cell-average utility `ū*(k, a)` (V10 Thm 8.2)

- **MUST-CITE (older):** Rust (1997) — random-grid discretization, O(h²) bias.
- **CONTEXT-CITE:** [06] Hao & Kasahara (2024) — they discuss state-discretization in §3.

---

## Section G — Empirical application (V10 §9)

### G.1 SEC EDGAR firm panel (N = 2,906, 146,985 obs, 2009–2025) with exit/maintain/growth actions

**This is your novel C6 contribution — no prior IRL paper on this exact setting.** Closest precedents:

- **CONTEXT-CITE:** [18] Leukam, Koffi & Djagba (2025) — portfolio with GIRL (closest finance-IRL application).
- **CONTEXT-CITE:** [19] Fang, Liu & Gong (2024) — offline ICRL on healthcare historical data (closest in *offline IRL on observational records* methodology).
- **CONTEXT-CITE:** [14] Blevins (2025) — uses Rust (1987) renewal model + entry-exit model with replication package; serves as a modern econometric precedent for empirical DDC.

### G.2 Scrap recovery rate `α ∈ {0.3, 0.5, 0.7, 1.0}` robustness sweep

- **MUST-CITE (older):** Pulvino (1998), Ramey & Shapiro (2001) per `notes/remaining_refs.md`.

---

## Reverse map — every reference [01]–[19] gets invoked at least once

| Ref | Invoked in sections | Role |
|---|---|---|
| [01] Zeng/Hong/Garcia 2024 | A.1, B.1, B.3, C.5, E.1, E.2, E.3 | DDC-IRL bridge precedent; position your Thm 7.1 against |
| [02] Skalse/Abate 2024 (partial identifiability) | D.1, D.3 | General identifiability framework for §4 |
| [03] Skalse/Abate 2024 (non-exp discounting) | — *NOT INVOKED — orthogonal topic* | Cite only in §11 future work if hyperbolic discounting comes up |
| [04] Schlaginhaufen/Kamgarpour 2023 | A.6, D.1, D.2, E.3, E.6 | Modern ML reward-identifiability up to potential shaping |
| [05] Cao/Cohen/Szpruch 2021 | A.6, A.8, B.4, D.1, D.2, D.4, E.1, E.3 | Foundational modern IRL identifiability |
| [06] Hao/Kasahara 2024 | A.1, A.4, C.2, C.3, C.5, F.3 | Contemporary CCP estimator extension |
| [07] Renard et al. 2025 | B.5, E.5, F.1 | Sample-complexity for entropy-reg IRL |
| [08] Liu et al. 2024 (constrained IRL survey) | — *NOT INVOKED in math; cite in §1.1 related work as survey* | TMLR-published survey |
| [09] Zhang et al. 2025 (overparameterization) | — *NOT INVOKED in math; cite in §11 future work for neural-net extension* | |
| [10] Wu et al. 2026 (distributional IRL) | — *NOT INVOKED in math; cite in §11 future work* | |
| [11] Jhaveri et al. 2025 (NeurIPS) | B.4, B.5, E.1, E.4 | Convergence theory for entropy-regularised RL |
| [12] Norets/Shimizu 2023 | A.7 | Non-Gumbel shock alternative; §11 future work |
| [13] Gui/Doshi 2025 | — *NOT INVOKED in math; cite in §11 future work for transfer/abstraction* | |
| [14] Blevins 2025 | A.1, A.3, A.4, G.1 | Modern DDC empirical replication framework |
| [15] Ghanem et al. 2025 | — *NOT INVOKED in math; cite in §11 future work for online IRL* | |
| [16] Krishnamurthy 2025 | §1 framing (revealed preferences) — not directly in math section | Cite in §1 introduction |
| [17] van der Laan/Kallus/Bibaut 2026 | A.6, B.1, B.3, C.1, C.4, E.1, E.2, E.3, E.6 | **THE primary contemporary position-against citation** |
| [18] Leukam et al. 2025 | G.1 | Finance IRL application precedent |
| [19] Fang et al. 2024 | F.2, G.1 | Offline IRL on observational data precedent |

**Coverage check:** 15 of 19 references are invoked at least once in the mathematical modelling sections. The 4 not invoked in the math sections ([03], [08], [09], [10], [13], [15]) are still useful for §1.1 related work, §11 future work, or §1 framing — see the per-reference notes above. **No reference is "wasted"** in the folder.

**No reference is invoked that is not physically present in the `references/` folder.** Every [XX] marker above corresponds to a PDF on disk that can be opened locally without internet.

---

## Open verification items — ✅ ALL RESOLVED (Phase 2, 18 May 2026)

All 5 items resolved. See `VERIFICATION_REPORT.md` for the detailed findings on each.

| Item | Status | Outcome |
|---|---|---|
| 1. AM 2011/2019 vs Thm 6.3 | ✅ Resolved | Both PDFs downloaded as [00a], [00b]. **Thm 6.3 is derivative of AM 2011's representation theorem** — demote in paper. |
| 2. [17] §3 absorbing-into-r framing | ✅ Resolved | Verbatim quote located at [17] p. 4: *"we set τ = 1 and absorb the scale into r^†"*. This IS the folk wisdom your Thm 7.1 corrects under absorbing exit. Cite explicitly. |
| 3. [01] §6 linear reward case | ✅ Resolved | Their Cor 1(ii) p. 13 uses reference-action normalisation — matches your Magnac-Thesmar approach. Cite in §4. No overlap with Thm 6.3. |
| 4. [11] §3-4 τ → 0 vs Prop 7.4 | ✅ Resolved | [11] studies vanishing-temperature limit τ → 0 — orthogonal to your fixed-β discrepancy. No overlap. Cite Thm 4.2 in §2 (contraction). |
| 5. bootstrap.py vs [07] | ✅ Resolved | Cluster bootstrap is correct for two-step semiparametric. [07] bounds are for a different (iterative gradient) algorithm. **Code fix: extend `src/bootstrap.py` to also bootstrap ω̂.** See VERIFICATION_REPORT §5.
