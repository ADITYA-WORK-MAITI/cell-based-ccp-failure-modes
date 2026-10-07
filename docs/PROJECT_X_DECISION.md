> **Status note, 5 October 2026.** This memo records the decision made on 4 October and the
> three-week plan written that day. The plan was executed and compressed into two days. Where
> the forward-looking steps below differ from what was actually done, `REPORT.md`,
> `docs/TRACEABILITY.md` and `rebuild/out/RESULTS.md` are authoritative. The memo is kept for
> the reasoning, not for its schedule.

---

# PROJECT X — Decision Memo

**Date:** 4 October 2026
**Companion to:** `PROJECT_X_AUDIT.md` (full audit; read that for the evidence behind these calls)

---

## The decision

**Stop treating it as a paper. Finish it as a public technical artifact — three weeks. Let the paper earn its way out of that, on evidence, or not at all.**

Three constraints force this:

1. **The theoretical core is pre-empted.** The `δ = −γ_E` normalisation that dissolves the headline "discrepancy" is already published, as is the absorbing-state problem under the name *termination/survival bias*.
2. **The empirical application is unsalvageable on a reasonable horizon.** The panel's exit variable has no generating code, is not absorbing (487 exit rows / 423 firms), and misses the 1,178 firms that vanish in 2025.
3. **arXiv is effectively closed to you.** Since 21 January 2026 the automatic path needs *both* an institutional email *and* prior authorship in that endorsement domain. You have neither. Personal endorsement is the only route, and arXiv staff cannot provide it.

**You do not owe the paper/project fork an answer yet.** Stages 1–2 below are required on both paths. The reason the direction feels inconclusive is that the numbers which would settle it do not yet exist. Repair first; the fork then answers itself.

**Opportunity cost is the binding constraint.** If your other paper is closer to done, it is the better CV investment. Spend three weeks here, not seven.

---

## Three-week plan, with gates

### Week 1 (6–10 Oct) — Confirm and repair
- Unblock compute by installing a signed Python interpreter. **Done 4 October 2026.**
- Execute the degenerate-transition check: print `np.unique(next_cell_ids)` and `T[1].sum(axis=0).nonzero()`. A single index confirms the defect and formally voids all 15 result files.
- Fix: `nanpercentile` (or pre-mask NaN rows); **shared bin edges** for `states` and `next_states`; report the count of uniform-fallback cells instead of silently injecting `1/K`.
- Fix the DGP: make `v(x,0) = W̃(x)` exactly (currently `V*(x) − exit_gap + δ(x)`); widen the transition bandwidth so LEV and SIZE actually move.
- Add the test that should always have existed: **recover known `u` to a stated tolerance in a correctly-specified DGP.**

> **GATE 1 — end of Week 1.** Does the end-to-end test pass, with RMSE falling approximately as `N^{-1/2}`?
> **No →** the estimator is wrong beyond the NaN path. Stop, and ship the audit alone as the artifact. Do not spend Week 2.
> **Yes →** continue.

### Week 2 (13–17 Oct) — Re-derive and re-measure
- Restate Theorem 7.1 as the **normalisation-incompatibility** proposition: anchoring exit utility at a *measured* scrap value consumes the degree of freedom that the `u ↦ u + γ` shift needs, so point identification and MaxEnt/Gumbel value equivalence cannot both be imposed. Retire the "folk equivalence fails" framing.
- Add the sharp converse: `D` is constant **iff** the soft exit probability is state-invariant.
- Add the interpretation the draft misses: `D(x)` is the entropic-risk aggregation of `γ × (discounted survival time)` — this is what makes `[γ, γ/(1−β)]` intuitive.
- Re-run the sweeps on corrected code. Measure the bias induced in recovered utilities across exit rate, `β`, and grid coarseness.
- Rewrite `LITERATURE_GAP_ANALYSIS.md`'s novelty table. Add Kang (2026, arXiv:2605.30843), Kostrikov et al. (2019, arXiv:1809.02925), and Al-Hafez et al. (2023, arXiv:2303.00599). Two attributions carried from a secondary source were checked on 4 October 2026 and could not be confirmed: "Geng et al. (2020)" matches no locatable paper and is withdrawn, and "Mai & Jaillet (2020)" matches no locatable paper either. The nearest real work is Bui, Mai and Jaillet (2022), *Weighted Maximum Entropy Inverse Reinforcement Learning*, arXiv:2208.09611, which has a different lead author and year. Its six "NOVEL / High confidence" verdicts do not survive these.

> **GATE 2 — end of Week 2.** Is the induced bias in recovered exit utilities **materially large** across a realistic range of exit rates — large enough that a practitioner would change what they do?
> **No →** there is no paper. Ship the artifact. This is a legitimate, honest outcome, not a failure.
> **Yes →** the optional note in Week 4–5 is justified.

### Week 3 (20–24 Oct) — Ship the artifact
- Write a 8–12 page technical report: the framework, the corrected result, the quantified convention effect, and an explicit **reproducibility section** on the failure modes found (NaN-propagating percentile discretisation silently degenerating transition matrices; Laplace smoothing making `V̂` a function of cell sample size).
- Retain the old outputs as evidence for the rebuild rather than deleting them. **As executed: retained privately and not published. The three extracts the report relies on are in `evidence/`.**
- Clean public GitHub repo: corrected `src/`, working tests, `run_experiments` that actually regenerates every committed result.
- Get an **ORCID**. Deposit report + code on **Zenodo** → permanent DOI, citable, indexed by Google Scholar and Semantic Scholar.
- **Drop the SEC application from this artifact entirely.** If the panel is ever rebuilt with a real exit definition (SEC Form 25/15, or CRSP delisting codes) it becomes a second project, not a section of this one.

### Optional, Weeks 4–5 (27 Oct – 7 Nov) — only if Gate 2 passed
Cut the note to length for one venue below and submit. One venue, one submission. Do not serialise through the ladder.

---

## CV wording, by stage

| When | Exact wording | Truthful after |
|---|---|---|
| **Today** | **Independent Research Project** — Structural estimation and inverse reinforcement learning: dynamic discrete choice with absorbing exit. *(2026)* | now |
| After Week 3 | **Independent Research Project** — … *Technical report and reproducible implementation, Zenodo, DOI: the project DOI (2026).* | Zenodo deposit live |
| If Gate 2 passed, drafting | add: **Manuscript in preparation** | a draft actually exists |
| On submission | add: **Under review**, *[venue]* | submitted |
| On acceptance | **Accepted**, *[venue]* | acceptance email |

Do not use "working paper," "preprint," "in preparation," or "under review" before its gate. A DOI'd Zenodo technical report is a real, citable research output — you do not need to inflate it.

---

## Venue ladder, with honest odds

| Venue | Fit | Odds for an unaffiliated first-time author | Cost |
|---|---|---|---|
| **Zenodo** (technical report + code, DOI) | Exact | Certain — no gatekeeping | Free |
| **Economics Bulletin** | Good — short methodological notes, RePEc-indexed | Realistic | Free, open access |
| **ML workshop** (reward learning / IRL, at a 2027 ML conference) | Good — the normalisation trap is workshop-shaped; no affiliation requirement | Realistic; useful referee feedback | Often non-archival |
| **Economics Letters** | Good in scope (~2000 words) | **Reach.** High desk-rejection rate; a clarification result is a hard sell | No submission fee |
| **arXiv** (econ.EM / stat.ML) | Good | **Blocked** until someone with endorsement privileges in that domain endorses you | Free |
| AAAI / NeurIPS / ICML main tracks | Poor | Near zero — these venues reject clarifications | — |
| General-interest economics journals | Poor | Near zero | — |

**Sequencing:** Zenodo first, unconditionally. It makes the work citable immediately and removes all time pressure from the endorsement problem. If Gate 2 passes, pick **one** of Economics Bulletin or an ML workshop. Treat arXiv as something that becomes available later, via a personal endorser met through workshop feedback — not as a dependency in this plan.

---

## Constraints, corrected

- **GPU: a non-issue.** A 625-cell tabular MDP solves by value iteration in milliseconds. Your 4-core laptop is far more than sufficient. Delete this worry.
- **No institution: three real costs.** (a) arXiv endorsement — route around via Zenodo. (b) No co-author to catch errors — which is precisely what the audit just supplied; keep that function in the loop. (c) Higher desk-rejection risk — mitigated by choosing note-length venues.
- ~~**Open item:** V11 names a supervisor.~~ **Closed 4 October 2026: sole author, Aditya Maiti. No supervisor. The third-party name was redacted from the whole repository on 5 October 2026.**
