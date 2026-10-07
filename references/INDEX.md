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
> Two notes, since the text below is unedited. "Ghost in the Machine" was the
> project's working title in May 2026; the work is now titled *Two failure modes
> in cell-based CCP estimation of dynamic discrete choice models*. And the
> commands in the Reproducibility section at the end use absolute paths from the
> author's May 2026 machine, which will not run anywhere else; from a clone of
> this repository the equivalents are `python references/_download.py` and
> `python references/_download_phase2.py`.
>
> The text below is preserved unedited.

---

# References Index — Ghost in the Machine

**Purpose:** 19 recent arXiv papers (2021–2026, last 5 years) directly relevant to the Ghost in the Machine project. Every entry below is verified by reading page 1 of the actual PDF on this machine. arXiv IDs, titles, authors, and venues are pulled from the PDF text itself, not from search-result summaries.

**Last verified:** 18 May 2026. All 19 PDFs are present in this folder.

**Phase 2 update (refs 16-19, added 18 May 2026):** 4 papers added to close the "finance / applied IRL" gap noted in the original §"What this set does NOT cover".

**Phase 3 update (refs 00a, 00b, added 18 May 2026):** 2 *foundational pre-5-year* papers added because they are essential for verifying the novelty of Theorem 6.3 (V10 §C one-step recovery). These are Arcidiacono-Miller (2011, *Econometrica*) and Arcidiacono-Miller (2019, *Quantitative Economics*) — both downloaded as free working-paper versions from the authors' Duke pages.

**Phase 4 update (refs F01–F13, added 18 May 2026):** **13 additional foundational PDFs** downloaded so that EVERY citation in `MATHEMATICAL_MODELLING_V11.md` corresponds to a physically-present PDF in this folder. These are the older (>5 year) foundational papers invoked throughout V11 §A–§F. All downloaded from author webpages, AAAI open access, university hosts, or arXiv. Marked with `F` prefix to distinguish from the modern set.

**After Phase 4: this folder is the COMPLETE evidence base for V11.** Every claim in V11 that cites a paper can be verified by opening the corresponding PDF locally without internet.

**Phase 5 update (ref [20], added 18 May 2026 after Research Mode audit):** Added van der Laan, Bibaut & Kallus (Dec 30, 2025) *"Efficient Inference for Inverse Reinforcement Learning and Dynamic Discrete Choice Models"* (arXiv:2512.24407). This is the natural follow-up to ref [17] and is the canonical 2026 reference for semiparametric efficient-influence-function inference applied directly to MaxEnt-IRL and Gumbel-shock DDC. Cited in V11 §F (Statistical Inference) as the modern theoretical backing for the cluster-bootstrap inference procedure.

---

## Tier 0F — Foundational citations invoked throughout V11 (Phase 4, added 18 May 2026)

These 13 PDFs are the older (>5 year) papers cited in `MATHEMATICAL_MODELLING_V11.md`. All have been verified by reading page 1 of the actual PDF on disk.

### [F01] Rust (1987) — *Optimal Replacement of GMC Bus Engines: An Empirical Model of Harold Zurcher*
- **File:** `F01_Rust1987_OptimalReplacement_BusEngines.pdf` (567 KB)
- **Venue:** Econometrica 55(5), 999–1033, Sep 1987 (JSTOR 1911259)
- **Source:** Caltech hosted PDF `http://www.its.caltech.edu/~mshum/stats/rust.pdf`
- **Invoked at:** V11 §A.1 (state vector framework), §A.2 (compactness via winsorisation), §B.1 (choice-specific value), §C (CCP inversion historical context)

### [F02] Hotz & Miller (1993) — *Conditional Choice Probabilities and the Estimation of Dynamic Models*
- **File:** `F02_HotzMiller1993_CCP_DynamicModels.pdf` (887 KB)
- **Venue:** Review of Economic Studies 60(3), 497–529, Jul 1993
- **Source:** Caltech hosted PDF `http://www.its.caltech.edu/~mshum/gradio/papers/condChoiceProbEstDynModel1993.pdf`
- **Invoked at:** V11 §C.2 (Theorem 3.5 direct value recovery — origin of the inversion lemma), §C (CCP inversion procedure)

### [F03] Ziebart, Maas, Bagnell & Dey (2008) — *Maximum Entropy Inverse Reinforcement Learning*
- **File:** `F03_Ziebart2008_MaxEntIRL_AAAI.pdf` (391 KB)
- **Venue:** AAAI 2008 Proceedings, pp. 1433–1438
- **Source:** AAAI open access `https://cdn.aaai.org/AAAI/2008/AAAI08-227.pdf`
- **Invoked at:** V11 §E.1 (MaxEnt soft Bellman definition), §E.2 (folk-equivalence framing), §E.3 (Theorem 7.1 — the result that refines Ziebart's framework under absorbing exit)
- **AAAI relevance:** This is THE foundational MaxEnt IRL paper. Your AAAI-27 submission positions itself as a correction to its absorbing-exit case.

### [F04] Magnac & Thesmar (2002) — *Identifying Dynamic Discrete Decision Processes*
- **File:** `F04_MagnacThesmar2002_IdentifyingDDC.pdf` (336 KB)
- **Venue:** Econometrica 70(2), 801–816, Mar 2002 (JSTOR 2692293)
- **Source:** Caltech hosted PDF `https://www.its.caltech.edu/~mshum/gradio/papers/IDDDP.pdf`
- **Invoked at:** V11 §A.6 (Magnac-Thesmar normalisation foundation), §A.8 (β non-identification, Theorem 6 of MT), §D.1 (equivalence class Theorem 4.5), §D.2 (Corollary 4.6 normalisation kills the class), §D.3 (kernel condition Proposition 4.7), §D.4 (Theorem 4.4 β non-identification)

### [F05] Pulvino (1998) — *Do Asset Fire Sales Exist? An Empirical Investigation of Commercial Aircraft Transactions*
- **File:** `F05_Pulvino1998_AssetFireSales_Aircraft.pdf` (455 KB)
- **Venue:** Journal of Finance 53(3), 939–978
- **Source:** Stanford hosted PDF `https://web.stanford.edu/~piazzesi/Reading/Pulvino%201998.pdf`
- **Invoked at:** V11 §A.4 (empirical justification for scrap-value recovery rate α ∈ [0.3, 0.7])

### [F06] Ramey & Shapiro (2001) — *Displaced Capital: A Study of Aerospace Plant Closings*
- **File:** `F06_RameyShapiro2001_DisplacedCapital_Aerospace.pdf` (198 KB)
- **Venue:** Journal of Political Economy 109(5), 958–992, Oct 2001
- **Source:** UMich hosted PDF `https://public.websites.umich.edu/~shapiro/papers/jpe2001-jpe.pdf`
- **Invoked at:** V11 §A.4 (empirical justification for scrap-value recovery rate α and its asset-specificity)

### [F07] Rust (1997) — *Using Randomization to Break the Curse of Dimensionality*
- **File:** `F07_Rust1997_RandomizationCurseDimensionality.pdf` (622 KB)
- **Venue:** Econometrica 65(3), 487–516, May 1997
- **Source:** Editorial Express `https://editorialexpress.com/jrust/crest_lectures/randomization.pdf`
- **Invoked at:** V11 §F.3 (consistency target = cell-average utility; O(h²) discretisation bias)

### [F08] McFadden (1974) — *Conditional Logit Analysis of Qualitative Choice Behavior*
- **File:** `F08_McFadden1974_ConditionalLogit.pdf` (1.8 MB)
- **Venue:** P. Zarembka (ed.), *Frontiers in Econometrics*, Academic Press, pp. 105–142
- **Source:** Berkeley hosted PDF `https://eml.berkeley.edu/reprints/mcfadden/zarembka.pdf`
- **Invoked at:** V11 §C.1 (logit CCP derivation Theorem 3.1)

### [F09] Arcidiacono & Ellickson (2011) — *Practical Methods for Estimation of Dynamic Discrete Choice Models*
- **File:** `F09_ArcidiaconoEllickson2011_PracticalMethods_DDC.pdf` (302 KB)
- **Venue:** Annual Review of Economics 3, 363–394
- **Source:** Duke hosted PDF `https://public.econ.duke.edu/~psarcidi/annualreview5revision.pdf`
- **Invoked at:** V11 §1.1 (DDC estimation literature survey), §C.5 (modern context for CCP methods)

### [F10] Haarnoja, Tang, Abbeel & Levine (2017) — *Reinforcement Learning with Deep Energy-Based Policies* (Soft Q-Learning)
- **File:** `F10_Haarnoja2017_SoftQLearning_DeepEnergyPolicies.pdf` (3.5 MB)
- **Venue:** ICML 2017 (PMLR 70)
- **Source:** arXiv 1702.08165
- **Invoked at:** V11 §E.1 (cited by [17] as the connection between soft Bellman and entropy-regularised RL)

### [F11] Aguirregabiria & Mira (2002) — *Swapping the Nested Fixed Point Algorithm: A Class of Estimators for Discrete Markov Decision Models*
- **File:** `F11_AguirregabiriaMira2002_NPL_SwappingNFXP.pdf` (780 KB)
- **Venue:** Econometrica 70(4), 1519–1543 (CEMFI working paper version, 1999, 7 pp.)
- **Source:** CEMFI hosted PDF `https://www.cemfi.es/ftp/wp/9904.pdf`
- **Invoked at:** V11 §C.5 (NPL scheme distinction from Theorem 6.3)
- **Note:** This is the 1999 CEMFI working paper (7 pp.), not the full 25-page Econometrica 2002 version. The core NPL algorithm contribution is present.

### [F12] Newey & McFadden (1994) — *Large Sample Estimation and Hypothesis Testing*
- **File:** `F12_NeweyMcFadden1994_LargeSampleEstimation.pdf` (7.6 MB)
- **Venue:** Handbook of Econometrics, Vol. 4, Chapter 36, Elsevier
- **Source:** UW-Madison hosted PDF `https://www.ssc.wisc.edu/~xshi/econ715/chap36neweymacfadden.pdf`
- **Invoked at:** V11 §F.2 (asymptotic theory for two-step estimators; cluster bootstrap context)

### [F13] Train (2009) — *Discrete Choice Methods with Simulation*, 2nd edition, Chapter 3: Logit
- **File:** `F13_Train2009_Ch03_Logit.pdf` (194 KB)
- **Venue:** Cambridge University Press, Chapter 3, pp. 34–75
- **Source:** Author's Berkeley page `http://eml.berkeley.edu/books/choice2nd/Ch03_p34-75.pdf`
- **Invoked at:** V11 §A.7 (Gumbel shocks reference), §C.1 (logit derivation context)
- **Note:** Chapter 3 only (the Logit chapter — the only chapter directly cited). Full book is available at `https://eml.berkeley.edu/books/choice2.html` for additional chapters.

---

## Citation coverage statement (Phase 4 complete, 18 May 2026)

**`references/` is now a strict superset of the bibliography invoked in `MATHEMATICAL_MODELLING_V11.md`.** Every paper cited in V11 corresponds to a physical PDF in this folder.

V11 was edited on 18 May 2026 to replace three previously-cited references whose free PDFs are unobtainable:
- **Murphy & Topel (1985)** was replaced with **[F12] Newey & McFadden (1994) §6.1 "Generated Regressors"** which covers the same theoretical ground in a far more general framework.
- **Johnson, Kotz & Balakrishnan (1995)** was replaced with **[F13] Train (2009) Chapter 3** which derives the Gumbel max-stability property explicitly on p. 34.
- **Bertsekas & Shreve / Puterman** were never substantively cited in V11; the contraction proof of Proposition 2.4 is self-contained.

Result: zero honest-disclosure exceptions. Every reference in V11 can be opened offline by pointing to the corresponding PDF in this folder.

## Tier 0 — Foundational pre-5-year predecessors (Phase 3, added for Thm 6.3 novelty verification)

### [00a] Arcidiacono & Miller (Econometrica 2011) — *CCP Estimation of Dynamic Discrete Choice Models with Unobserved Heterogeneity*
- **File:** `00a_ArcidiaconoMiller2011_CCP_Heterogeneity.pdf`
- **Year:** 2011 (Econometrica 79(6), 1823–1867) — **older than 5 years**, included for novelty verification only
- **Source:** Author Duke page `https://public.econ.duke.edu/~psarcidi/ccpnoid.pdf` (free open-access working-paper version, 59 pp.)
- **Why it matters:** The foundational *representation theorem* for CCP estimation in DDC with unobserved heterogeneity. Their Lemma 1 (the "inversion lemma") and their Eqs (2.4)–(2.7) provide the closed-form V↔u recovery formula that your V10 §C one-step procedure specialises to the absorbing-exit three-action case. **Your Theorem 6.3 is an algebraic consequence of AM 2011's representation theorem.** See `VERIFICATION_REPORT.md` Item #1 for the honest-positioning implication.

### [00b] Arcidiacono & Miller (Quantitative Economics 2019) — *Nonstationary Dynamic Models with Finite Dependence*
- **File:** `00b_ArcidiaconoMiller2019_NonstatFiniteDependence.pdf`
- **Year:** 2019 (Quantitative Economics 10(3), 853–890) — **older than 5 years**, included for novelty verification only
- **Source:** Author Duke page `https://public.econ.duke.edu/~psarcidi/finitedependence.pdf` (working-paper version, 6 pp. — short summary, not the full 38-page published version)
- **Why it matters:** Generalises the AM 2011 finite-dependence definition to allow *negative* weights on conditional value functions. Cited by [06] Hao-Kasahara (2024) as direct predecessor. Useful context for §6 of your paper but **no overlap with your contributions**.

---

## Tier 1 — Core fit (directly addresses the project's headline questions)

### [01] Zeng, Hong & Garcia (2024) — *Structural Estimation of Markov Decision Processes in High-Dimensional State Space with Finite-Time Guarantees*
- **File:** `01_Zeng2024_StructEstMDP_HighDim.pdf`
- **arXiv:** [2210.01282v3](https://arxiv.org/abs/2210.01282) (last revised 1 March 2024)
- **Affiliations:** University of Minnesota (ECE), Texas A&M (ISE)
- **Venue:** Journal version (Operations Research)
- **Why it matters:** *This is the closest existing precedent for the project's central bridge.* They formulate structural MDP estimation as a single-loop ML-IRL algorithm with finite-time guarantees, framing the estimation task as one that has been studied both as DDC (econometrics) AND as IRL (ML). **You MUST cite this and position your contribution against it explicitly.** Their algorithm targets policy estimation; your paper instead delivers a closed-form one-step utility recovery via CCP inversion (Thm 6.3) plus a separate theoretical result on the MaxEnt–CCP discrepancy under absorbing exit (Thm 7.1). Different questions, related framework.

### [02] Skalse & Abate (Nov 2024) — *Partial Identifiability and Misspecification in Inverse Reinforcement Learning*
- **File:** `02_Skalse2024_PartialIdentifiability_IRL.pdf`
- **arXiv:** [2411.15951v1](https://arxiv.org/abs/2411.15951) (26 November 2024)
- **Affiliation:** University of Oxford, Department of Computer Science
- **Why it matters:** Comprehensive mathematical analysis of partial identifiability and misspecification in IRL. Provides a framework characterising the ambiguity of the reward function across all common behavioural models. **Anchor citation for your normalisation discussion** (V10 §4 Magnac–Thesmar equivalence class) — they make the same equivalence-class-up-to-shaping argument from an ML angle.

### [03] Skalse & Abate (Dec 2024, AAAI-25 proceedings) — *Partial Identifiability in Inverse Reinforcement Learning For Agents With Non-Exponential Discounting*
- **File:** `03_Skalse2024_NonExponentialDiscounting_IRL.pdf`
- **arXiv:** [2412.11155v1](https://arxiv.org/abs/2412.11155) (15 December 2024)
- **Affiliation:** University of Oxford
- **Venue:** AAAI 2025 (Association for the Advancement of Artificial Intelligence — copyright notice on first page)
- **Why it matters:** **Direct precedent for an AAAI publication on IRL identifiability theory.** Demonstrates that AAAI's reviewer pool accepts and values this style of result. Use this paper's structure as a template for how AAAI expects identifiability theorems to be stated and proved.

### [04] Schlaginhaufen & Kamgarpour (June 2023, ICML 2023) — *Identifiability and Generalizability in Constrained Inverse Reinforcement Learning*
- **File:** `04_Schlaginhaufen2023_Identifiability_ConstrainedIRL.pdf`
- **arXiv:** [2306.00629v1](https://arxiv.org/abs/2306.00629) (1 June 2023)
- **Affiliation:** EPFL, SYCAMORE Lab
- **Venue:** PMLR 202, *Proceedings of the 40th International Conference on Machine Learning*, Honolulu 2023
- **Why it matters:** Establishes identifiability-up-to-potential-shaping as a consequence of entropy regularisation. Directly maps to your V10 §7 result that the MaxEnt-IRL value function differs from the Gumbel-CCP value function by `γ/(1−β)` in the continuation subproblem (Prop 7.4). They develop the constrained-MDP version; you have the absorbing-exit version.

### [05] Cao, Cohen & Szpruch (Nov 2021) — *Identifiability in inverse reinforcement learning*
- **File:** `05_Cao2021_Identifiability_IRL.pdf`
- **arXiv:** [2106.03498v3](https://arxiv.org/abs/2106.03498) (8 November 2021)
- **Affiliations:** Alan Turing Institute; University of Oxford (Mathematical Institute); University of Edinburgh / Alan Turing Institute
- **Why it matters:** *Foundational identifiability theorem* — under entropy regularisation, the reward can be recovered up to a constant given demonstrations under two distinct discount factors or sufficiently different environments. Cites Lucas (1976) explicitly, which is exactly the structural-econometrics framing your paper uses. Cite as the modern ML re-derivation of Magnac–Thesmar identification.

### [06] Hao & Kasahara (May 2024) — *Conditional Choice Probability Estimation of Dynamic Discrete Choice Models with 2-period Finite Dependence*
- **File:** `06_HaoKasahara2024_CCP_FiniteDependence.pdf`
- **arXiv:** [2405.12467v1](https://arxiv.org/abs/2405.12467) (21 May 2024, econ.EM)
- **Affiliations:** University of Hong Kong (Business and Economics); University of British Columbia (Vancouver School of Economics)
- **JEL codes:** C15, C25, C57, C61, C63 (econometrics + computational)
- **Why it matters:** **Direct contemporary extension of Hotz-Miller / Arcidiacono-Miller (2011) CCP estimation** — the methodological lineage of your one-step procedure (Thm 6.3). They characterise finite dependence and produce a computationally attractive CCP estimator. Cite alongside Arcidiacono-Miller (2011) as the modern CCP literature.

### [07] Renard, Schlaginhaufen, Ni & Kamgarpour (March 2025) — *Convergence of a model-free entropy-regularized inverse reinforcement learning algorithm*
- **File:** `07_Renard2025_EntropyReg_IRL_Convergence.pdf`
- **arXiv:** [2403.16829v3](https://arxiv.org/abs/2403.16829) (3 March 2025; first version March 2024)
- **Affiliation:** EPFL, SYCAMORE Lab
- **Why it matters:** Provides sample-complexity guarantees ε-optimal reward recovery with O(1/ε²) samples for entropy-regularised IRL. **Modern statistical-learning counterpart to your asymptotic-normality claim (V10 Claim 8.3).** Cite when discussing inference; their finite-sample bounds complement your cluster-bootstrap practical strategy.

---

## Tier 2 — Strong supporting context

### [08] Liu, Xu, Liu, Gaurav, Subramanian & Poupart (Jan/Feb 2025, TMLR) — *A Comprehensive Survey on Inverse Constrained Reinforcement Learning: Definitions, Progress and Challenges*
- **File:** `08_Liu2024_ConstrainedIRL_Survey.pdf`
- **arXiv:** [2409.07569v3](https://arxiv.org/abs/2409.07569) (1 February 2025)
- **Affiliations:** CUHK Shenzhen; University of Waterloo; Penn State; Vector Institute
- **Venue:** **Transactions on Machine Learning Research, January 2025** (peer-reviewed)
- **Why it matters:** Authoritative recent survey covering ICRL but with extensive treatment of MaxEnt IRL framing, causal entropy, and entropy-regularised RL — exactly your background section. Cite as the up-to-date IRL survey alongside Ziebart et al. 2008.

### [09] Zhang, Zeng, Li, Garcia & Hong (March 2025) — *Understanding Inverse Reinforcement Learning under Overparameterization: Non-Asymptotic Analysis and Global Optimality*
- **File:** `09_Zhang2025_Understanding_IRL_Overparam.pdf`
- **arXiv:** [2503.17865v1](https://arxiv.org/abs/2503.17865) (22 March 2025, stat.ML)
- **Affiliations:** Johns Hopkins; University of Minnesota; Texas A&M
- **Why it matters:** Direct follow-up by the Zeng/Hong/Garcia group to paper [01]. Extends ML-IRL guarantees from linear rewards to neural-network parameterisations. Cite when discussing why your linear-parametric WLS step (V10 Step 4) is a feature, not a limitation — you get interpretability and small-sample guarantees that the overparameterised setting can't match.

### [10] Wu, Zhao & Wu (April 2026) — *Distributional Inverse Reinforcement Learning*
- **File:** `10_Wu2026_Distributional_IRL.pdf`
- **arXiv:** [2510.03013v3](https://arxiv.org/abs/2510.03013) (21 April 2026)
- **Affiliation:** Georgia Institute of Technology (Computational Science & Engineering; Woodruff School of Mech. Eng.)
- **Why it matters:** Recent (Apr 2026) IRL contribution: jointly model uncertainty over reward functions AND full return distributions, capturing variability that point-estimate IRL misses. Cite in your discussion (V10 §11.2) when noting that your scalar utility-recovery does not capture distributional reward structure — proper limitation framing.

---

## Tier 3 — Methodologically adjacent context

### [11] Jhaveri, Wiltzer, Shafto, Bellemare & Meger (Oct 2025, NeurIPS 2025) — *Convergence Theorems for Entropy-Regularized and Distributional Reinforcement Learning*
- **File:** `11_Bellemare2025_EntropyReg_DistRL_Convergence.pdf`
- **arXiv:** [2510.08526v1](https://arxiv.org/abs/2510.08526) (9 October 2025)
- **Affiliations:** Rutgers University–Newark; Mila–Québec AI Institute / McGill University
- **Venue:** **NeurIPS 2025** (39th Conference on Neural Information Processing Systems)
- **Why it matters:** Convergence theory for vanishing-temperature limits in entropy-regularised RL — addresses exactly the τ → 0 question that connects your Gumbel-shock (econometric) and MaxEnt (IRL) Bellman operators. Cite for theoretical-foundations grounding.

### [12] Norets & Shimizu (Feb 2022 / Aug 2023, v3) — *Semiparametric Bayesian Estimation of Dynamic Discrete Choice Models*
- **File:** `12_NoretsShimizu2023_SemiparBayes_DDC.pdf`
- **arXiv:** [2202.04339v3](https://arxiv.org/abs/2202.04339) (3 August 2023, econ.EM)
- **Affiliations:** Brown University (Economics); University of Alberta (Economics)
- **Why it matters:** Relaxes the Gumbel-shock assumption in DDC estimation using location-scale extreme-value mixtures. Shows the standard dynamic logit can deliver misleading counterfactuals when shocks are non-Gumbel. **Cite as motivation for stating Assumption 1.14 (Gumbel) explicitly in your paper** and acknowledging Norets-Shimizu-style robustness as a future direction.

### [13] Gui & Doshi (Dec 2025, under review ICLR 2026) — *Inversely Learning Transferable Rewards via Abstracted States*
- **File:** `13_GuiDoshi2025_TransferableRewards.pdf`
- **arXiv:** [2501.01669v3](https://arxiv.org/abs/2501.01669) (7 December 2025)
- **Affiliation:** University of Georgia, School of Computing
- **Venue:** Under review as a conference paper at ICLR 2026
- **Why it matters:** Demonstrates current (Dec 2025) reviewer interest in IRL with abstracted state representations — your project's quintile-grid discretisation `K = 5⁴ = 625` is a form of state abstraction. Cite when discussing the discretisation choice; their VAE-based abstraction is a complementary direction.

### [14] Blevins (Nov 2025) — *Identification and Estimation of Continuous-Time Dynamic Discrete Choice Games*
- **File:** `14_Blevins2025_ContinuousTime_DDCGames.pdf`
- **arXiv:** [2511.02701v1](https://arxiv.org/abs/2511.02701) (4 November 2025, econ.EM)
- **Affiliation:** The Ohio State University
- **JEL codes:** C13, C35, C62, C73
- **Why it matters:** Current (Nov 2025) DDC identification paper using Rust (1987) as the empirical example — single-agent renewal model, entry-and-exit model. **Direct contemporary work in your econometric lineage.** Use as evidence that DDC identification work is active in 2025 and AAAI's ML reviewers will be exposed to it indirectly via citations.

### [15] Ghanem, Howell, Potter, Closas, Ramezani, Erdogmus & Imbiriba (Oct 2025) — *Recursive Deep Inverse Reinforcement Learning*
- **File:** `15_Ghanem2025_Recursive_DeepIRL.pdf`
- **arXiv:** [2504.13241v5](https://arxiv.org/abs/2504.13241) (4 October 2025)
- **Affiliations:** Northeastern University; Boston Dynamics AI Institute; UMass Boston
- **Why it matters:** Online/recursive deep IRL with Extended-Kalman-Filter-style updates. Cite as an example of "MaxEnt IRL methods rely on first-order updates which limits real-time applicability" — your one-step closed-form Hotz-Miller recovery is the *opposite extreme* of this online/recursive approach, with the trade-off being stationary vs. online operation.

---

---

## Tier 4 — Finance & applied IRL (closes the gap from phase 1)

### [16] Krishnamurthy (July 2025) — *Inverse Reinforcement Learning using Revealed Preferences and Passive Stochastic Optimization*
- **File:** `16_Krishnamurthy2025_IRL_RevealedPreferences.pdf`
- **arXiv:** [2507.04396v1](https://arxiv.org/abs/2507.04396) (8 July 2025)
- **Affiliation:** Cornell University (vikramk@cornell.edu)
- **Venue:** Excerpted from monograph *"Partially Observed Markov Decision Processes: Filtering, Learning and Controlled Sensing"*, 2nd ed., Cambridge University Press, 2025
- **Why it matters:** *The single strongest framing match for your project.* Views IRL through the lens of **revealed preferences from microeconomics** — exactly the language in your `Problem Statement.pdf` ("revealed objective function"). Uses Afriat's theorem and extensions to identify constrained utility maximisers from observed actions. **You must cite this when introducing the revealed-preference framing.** Monograph form means it's both rigorous and recent.

### [17] van der Laan, Kallus & Bibaut (May 2026, v2) — *Inverse Reinforcement Learning with Just Classification and a Few Regressions*
- **File:** `17_vanderLaan2025_IRL_ClassificationRegressions.pdf`
- **arXiv:** [2509.21172v2](https://arxiv.org/abs/2509.21172) (7 May 2026; first version 25 September 2025)
- **Affiliations:** University of Washington (Statistics); Cornell University (Nathan Kallus); Netflix
- **Why it matters:** **This paper explicitly bridges the two frameworks your project bridges.** Page 1 of the abstract reads: *"In maximum-entropy (MaxEnt) IRL... closely related to dynamic discrete-choice (DDC) models with i.i.d. Gumbel shocks (Rust, 1987), the observed policy has a softmax form induced by an unknown reward and continuation value."* They develop GenPQR (Generalized Policy-to-Q-to-Reward), reducing IRL to "off-the-shelf classification and regression methods" — the same lineage as your one-step CCP procedure (Thm 6.3), from the ML side. Cite alongside Hotz-Miller as the modern ML-side translation of your econometric approach. Nathan Kallus is a major name in this area.

### [18] Leukam, Koffi & Djagba (Nov 2025) — *Reinforcement Learning for Portfolio Optimization with a Financial Goal and Defined Time Horizons*
- **File:** `18_Leukam2025_GIRL_Portfolio.pdf`
- **arXiv:** [2511.18076v1](https://arxiv.org/abs/2511.18076) (22 November 2025)
- **Affiliations:** AIMS South Africa / Stellenbosch University; University of South Africa; Michigan State University
- **arXiv category:** q-fin.PM (quantitative finance / portfolio management)
- **Why it matters:** **A 2025 IRL-in-finance application paper.** Uses GIRL (Gradient Inverse Reinforcement Learning, a G-learning approach to IRL) to estimate investor reward functions from portfolio decisions. Sharpe ratio improvement from 0.42 to 0.483 over baselines. Closest published example of "apply IRL to recover the objective function of a financial agent" — exactly your paper's empirical posture, but with portfolio agents instead of corporate exit/maintain/growth decisions. Cite in §1 (Introduction) when motivating IRL in finance, and in §6 (related empirical work).

### [20] van der Laan, Bibaut & Kallus (Dec 2025) — *Efficient Inference for Inverse Reinforcement Learning and Dynamic Discrete Choice Models*
- **File:** `20_vanderLaan2025_EfficientInference_IRL_DDC.pdf`
- **arXiv:** [2512.24407v1](https://arxiv.org/abs/2512.24407) (30 Dec 2025; dated 1 Jan 2026)
- **Affiliations:** University of Washington (Statistics); Netflix Research; Cornell Tech, Cornell University (Kallus)
- **Why it matters:** **Canonical 2026 inference reference for V11 §F.** Develops semiparametric debiased IRL/DDC inference: efficient influence functions, √n-consistency, asymptotic normality for reward-dependent functionals in BOTH MaxEnt-IRL AND Gumbel-shock DDC. Key insight verbatim from abstract: *"the log-behaviour policy acts as a pseudo-reward that point-identifies policy value differences and, under a simple normalization, the reward itself."* This is the modern theoretical backbone for V11's cluster-bootstrap inference approach. Cited as Phase 5 addition after Research Mode audit (18 May 2026).

### [19] Fang, Liu & Gong (Oct 2024, v2) — *Offline Inverse Constrained Reinforcement Learning for Safe-Critical Decision Making in Healthcare*
- **File:** `19_Fang2024_OfflineICRL_Healthcare.pdf`
- **arXiv:** [2410.07525v2](https://arxiv.org/abs/2410.07525) (14 October 2024)
- **Affiliations:** University of Science and Technology of China; CUHK Shenzhen (Guiliang Liu — same author as ref [08])
- **Why it matters:** **High-stakes applied-IRL precedent in a non-finance domain.** Sepsis treatment example, offline data, exactly the offline-from-historical-records setup you have with SEC. Cite as "IRL has been deployed in high-stakes safety-critical applied domains [19]; we extend this lineage to corporate finance." Useful when an AAAI reviewer asks "is offline IRL on observational data feasible?" — yes, here is a precedent.

---

## NOT in the offline folder but worth knowing about (manual retrieval required)

### Zelman, Stefanik, Weiss & Teichmann (Nov 2024) — *Adversarial Inverse Reinforcement Learning for Market Making*
- **Venue:** ACM ICAIF '24 (5th ACM International Conference on AI in Finance), Brooklyn NY, 14-17 Nov 2024, pp. 81-89
- **DOI:** [10.1145/3677052.3698641](https://dl.acm.org/doi/10.1145/3677052.3698641)
- **Code:** https://github.com/JurajZelman/airl-market-making (official, public)
- **Affiliations:** Richfox Capital & ETH Zürich (Zelman, Stefanik); ETH Zürich Department of Mathematics (Weiss); ETH Zürich (Teichmann)
- **Why noted:** *Best-fit finance IRL application paper, but ACM-paywalled.* I attempted direct PDF download from the ACM DOI and was blocked by Cloudflare (HTTP 403). The paper applies AIRL (Adversarial IRL, combining GANs and IRL) to limit-order-book market making.
- **How to get it:**
  1. Use your USAR / GGSIPU library institutional access to ACM Digital Library.
  2. Or check ResearchGate at https://www.researchgate.net/publication/385819526 — authors sometimes upload free-access copies.
  3. Or email the authors directly (zelman@richfoxcapital.com, juraj.zelman@math.ethz.ch).
  4. The GitHub repository contains code and likely cites the paper in its README — useful even without the PDF.

**If you cannot obtain the PDF, do NOT cite it as a primary reference** — you said no abstracted evidence. Either retrieve a real copy or cite refs [17] and [18] as the finance-IRL examples instead.

---

## Coverage check (against the AAAI reviewer demands identified in Research Mode report)

| Reviewer concern | References that address it |
|---|---|
| Modern IRL identifiability framing | [02], [03], [04], [05], [13] |
| MaxEnt IRL theoretical foundations (2021–2025) | [04], [05], [07], [11] |
| Recent CCP / DDC literature in econometrics | [06], [12], [14] |
| ML-IRL bridge precedents (must position against) | [01], [09], **[17]** |
| Revealed-preferences framing (matches your problem statement) | **[16]** |
| Survey-level coverage for related-work section | [08] |
| Online / distributional / extension IRL methods | [10], [15] |
| Convergence theory in entropy-regularised RL | [07], [11] |
| Continuous-time / game-theoretic DDC extensions | [14] |
| Finance IRL applications (closest precedents) | **[17], [18]**, *[Zelman et al. ICAIF '24, paywalled]* |
| Applied IRL in high-stakes offline settings (analogue to SEC) | **[19]** |

## What this set does NOT cover (updated after phase 2)

Honest gaps you should still be aware of:

1. ~~**Application-specific IRL in finance.**~~ **PARTIALLY CLOSED in phase 2.** Refs [17] (van der Laan/Kallus/Bibaut — DDC-IRL bridge) and [18] (Leukam et al. — portfolio with GIRL) now in folder. Best-fit paper (Zelman et al. ICAIF '24 on adversarial IRL for market-making) is ACM-paywalled; if you have institutional access, retrieve manually. Your *corporate-exit* application remains novel — there is no prior IRL paper on firm exit/maintain/growth that I could find.
2. **Recent Murphy-Topel / two-step inference advances.** The Murphy-Topel two-step variance correction is older theory (1985), and recent advances are scattered across econometrics journals not always on arXiv. You may need to supplement with a journal search (e.g., Journal of Econometrics, Journal of Business & Economic Statistics) for any 2021–2026 paper that has tightened these results.
3. **Recent MaxEnt IRL applications to firm exit, entry, or industrial dynamics specifically.** Refs [17], [18] are the closest. Your SEC corporate-exit application would still be among the first specifically on firm dynamics; that's a feature, not a bug. Answer the "where is the prior work?" question honestly: "There is no prior IRL work on the firm exit/maintain/growth setting. The closest analogues are limit-order-book IRL (Roa-Vicens 2019, predates 5-year window; Zelman et al. 2024 at ICAIF), portfolio-objective IRL [18], and the DDC-IRL methodological bridge [17]."
4. **Older but still-cited foundational papers.** Rust (1987), Hotz-Miller (1993), Magnac-Thesmar (2002), Ziebart et al. (2008), McFadden (1974), and Train (2009) are NOT in this folder because they're all older than 5 years. They remain essential citations in your paper — they just don't count toward the "last 5 years" requirement. Keep notes/*.md as your record of those.

## Reproducibility

This catalog and all 19 PDFs were generated by running:
```
python C:/Users/admin/Desktop/neurips_project/references/_download.py          # refs 01-15
python C:/Users/admin/Desktop/neurips_project/references/_download_phase2.py   # refs 16-19
```
on 18 May 2026. Both scripts download from `https://arxiv.org/pdf/{arxiv_id}` with a polite User-Agent and 3-second sleeps between requests. Re-run if arXiv versions update. The Zelman et al. ICAIF '24 paper is NOT in this folder — it is ACM-paywalled; see the "NOT in the offline folder" section above for manual retrieval options.
