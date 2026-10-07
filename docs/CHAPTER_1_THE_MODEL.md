# Chapter 1. The Model, From Scratch

**Aditya Maiti.** Companion to *Two failure modes in cell-based CCP estimation of dynamic discrete choice models*.

This chapter assumes you know what a probability distribution is, what an expectation is, and what a logarithm does. Everything else is built here. Every number in the worked examples was computed, not recalled.

---

## 1.1 The question

Somebody makes choices. You watch. You never see why.

A bus depot manager decides each month whether to replace an engine. A firm decides each quarter whether to invest heavily, invest lightly, or shut down. You observe the decision and the circumstances. You do not observe the manager's reasoning, the firm's internal forecast, or the value either of them places on the outcomes.

The question of this field is simple to state. **From the choices alone, what can you learn about the preferences behind them?**

Two research communities asked this question independently. Economists call their version *dynamic discrete choice*, or DDC. Machine learning researchers call theirs *inverse reinforcement learning*, or IRL. They built different notation, cited different papers, and for a long time did not read each other. They were solving the same problem.

This chapter builds both, shows they are the same, and shows exactly where that sameness breaks.

---

## 1.2 Choosing once

### 1.2.1 Utility with a random part

Start with one decision, no future.

An agent picks one action `a` from a finite set `𝒜`. Each action delivers utility. Split that utility into two pieces:

```
U(a) = u(a) + ε(a)
```

`u(a)` is the **systematic** part. It depends on things you can measure. `ε(a)` is the **shock**, everything you cannot measure: the manager's mood, a private signal, an unrecorded constraint.

The agent sees both. You see neither directly. You see only which action was taken.

The agent picks the largest total:

```
a* = argmax_a [ u(a) + ε(a) ]
```

Because `ε` is random, `a*` is random. You cannot predict the choice. You can only state a probability for it. That probability is the object connecting your model to your data.

### 1.2.2 Why Gumbel

To get a probability you must assume a distribution for `ε`. The field almost always picks the **Gumbel** distribution, also called Type I extreme value. Its cumulative distribution function is

```
F(z) = exp( −exp( −(z − δ) ) )
```

`δ` is a **location parameter**. It slides the whole distribution left or right. The distribution's mean is not `δ`. It is

```
E[ε] = δ + γ,    γ = 0.5772156649015329
```

`γ` is the **Euler-Mascheroni constant**. It is not a modelling choice. It is a fixed mathematical constant that falls out of the Gumbel integral, the same way `π` falls out of a circle.

Hold on to that sentence. The entire original error of this project was forgetting it.

Why Gumbel and not the normal distribution? Because of one property, **max-stability**. If `ε(a)` are independent Gumbel with the same scale, then the *maximum* over actions is itself Gumbel. The normal distribution has no such property, and the resulting choice probabilities have no closed form.

Concretely, if `ε(a) ~ Gumbel(δ, 1)` independently, then `u(a) + ε(a) ~ Gumbel(u(a) + δ, 1)`, and

```
max_a [ u(a) + ε(a) ]  ~  Gumbel( δ + ln Σ_a e^{u(a)} ,  1 )
```

The maximum of several Gumbels is one Gumbel, with its location shifted by the log-sum-exp of the systematic parts. That is the whole reason this distribution is used.

### 1.2.3 The logit formula

From max-stability you get the choice probability in one line:

```
P(a) = e^{u(a)} / Σ_b e^{u(b)}
```

This is the **multinomial logit**. It is the workhorse of discrete choice. Train (2009), Chapter 3, which is in the project's `references/` folder, records the history and the derivation. The result that an extreme value distribution leads to the logit formula is the older one. McFadden (1974) proved the converse, that the logit formula necessarily implies extreme value unobserved utility.

Notice something crucial. **`δ` does not appear.** Shifting every action's shock by the same amount changes nothing about which action wins. The choice probabilities are blind to `δ`.

That blindness is the seed of the whole problem. Hold it.

**Worked example.** Three actions with `u = (0, 1, 2)`.

```
Σ_b e^{u(b)} = 1 + 2.718282 + 7.389056 = 11.107338
P(0) = 1/11.107338        = 0.090031
P(1) = 2.718282/11.107338 = 0.244728
P(2) = 7.389056/11.107338 = 0.665241
```

Now run it backwards, which is the trick the whole field rests on:

```
ln P(1) − ln P(0) = ln(0.244728) − ln(0.090031) = 1.000000 = u(1) − u(0)
```

**The log-ratio of two choice probabilities equals the utility difference.** You just recovered a preference from a frequency. That is inverse reinforcement learning in one line.

### 1.2.4 The value of having a choice

How good is it to face this menu, before the shocks are drawn? Take the expectation of the maximum. Using max-stability, the maximum is `Gumbel(δ + ln Σ e^{u(a)}, 1)`, and a Gumbel's mean is its location plus `γ`:

```
E[ max_a (u(a) + ε(a)) ] = δ + γ + ln Σ_a e^{u(a)}
```

Define

```
κ := δ + γ
```

`κ` is the **mean of the shock**. One symbol for one quantity. Then

```
V = κ + ln Σ_a e^{u(a)}        ... (Lemma 0)
```

The `ln Σ e^{·}` piece is the **log-sum-exp**, written `LSE`. Economists call it the *inclusive value*. It is a soft maximum: close to the largest `u(a)` when one action dominates, larger than all of them when several are close, because having options is worth something.

**Worked example continued.** `LSE(0,1,2) = ln(11.107338) = 2.407606`. With `δ = 0`, so `κ = γ`:

```
V = 0.577216 + 2.407606 = 2.984822
```

The best action alone is worth `2`. The menu is worth `2.98`. The extra `0.98` is the value of having choices and of the shocks sometimes making a nominally worse action turn out better.

**Two conventions are in common use.**

- Set `δ = 0`. Then `κ = γ ≈ 0.5772`. The shock has mean `γ`. This is the economics default.
- Set `δ = −γ`. Then `κ = 0`. The shock has mean zero. This is the machine learning default.

Both are legitimate. Neither changes any choice probability. **But they change `V` by `κ`, and this chapter is about what that does.**

---

## 1.3 Choosing again and again

### 1.3.1 The state

Now the agent chooses repeatedly and today's choice affects tomorrow's circumstances.

Write `x` for the **state**, everything relevant and observable. In this project `x` was four numbers about a firm: cash over assets, liabilities over equity, operating income over assets, and log assets.

Write `p(x′ | x, a)` for the **transition probability**, the chance of landing in state `x′` tomorrow after taking action `a` in state `x` today.

Write `β ∈ (0,1)` for the **discount factor**, how much tomorrow is worth relative to today. This project used `β = 0.976` per quarter, roughly a 10% annual rate.

### 1.3.2 The Bellman equation

Define the **conditional value** `v(x,a)`: the total expected discounted payoff from taking `a` today in state `x` and behaving optimally afterwards.

```
v(x,a) = u(x,a) + β Σ_{x′} p(x′ | x, a) V(x′)
```

Today's utility, plus the discounted expected value of tomorrow.

And `V(x)` is the **ex-ante value**: how good state `x` is before the shocks are drawn. By Lemma 0 applied at each state,

```
V(x) = κ + ln Σ_a exp{ v(x,a) }
```

Substituting gives the **Bellman equation**:

```
V(x) = κ + ln [ Σ_a exp{ u(x,a) + β Σ_{x′} p(x′|x,a) V(x′) } ]        ... (BE)
```

`V` appears on both sides. This is not circular. The right-hand side defines an operator on functions, and that operator is a **contraction** with modulus `β`. Apply it to any two starting guesses and they move closer together by a factor of `β`. Banach's fixed point theorem then gives exactly one solution, reachable by iterating from any starting point. That is Lemma 1, and it is what makes `solve_bellman` in the code terminate.

### 1.3.3 Where the constant comes from

Look at (BE) again. The `κ` sits outside the log, added once per period.

Set `κ = γ` and you get the economists' Bellman equation. Set `κ = 0` and you get the machine learners'. Same utilities, same transitions, same discount factor, one term different.

**The choice probabilities are identical in both.** The `κ` is a constant inside the state, so it cancels in every ratio.

**The value functions are not identical.** That gap is the subject of this project.

---

## 1.4 Working backwards: from behaviour to utility

### 1.4.1 The inversion

You do not observe `u`. You observe choices. From choices you estimate the **conditional choice probabilities**, written `σ(a|x)`: the fraction of times action `a` was taken in state `x`.

Hotz and Miller (1993) showed you can go backwards. Their observation is the one from Section 1.2.3, now with time in it:

```
ln σ(a|x) − ln σ(0|x) = v(x,a) − v(x,0)
```

Pick action `0` as a **reference action**. Every other conditional value is now known *relative to it*, straight from the data.

And the ex-ante value comes along free. Since `σ(0|x) = e^{v(x,0)} / Σ_b e^{v(x,b)}`, take logs and rearrange:

```
ln Σ_b e^{v(x,b)} = v(x,0) − ln σ(0|x)
```

so

```
V(x) = κ + v(x,0) − ln σ(0|x)        ... (INV)
```

**Read that equation slowly, because Failure Two in the report lives entirely inside it.** The value of a state equals the reference action's value, minus the log probability of taking the reference action, plus `κ`. If the reference action is rare, `ln σ(0|x)` is very negative, and `V(x)` is large. The model says: if you almost never leave, staying must be worth a lot.

That inference is correct when `σ(0|x)` is measured correctly. When it is an artefact of a smoothing rule, the inference is garbage, and Section 1.9 shows exactly how.

### 1.4.2 Only differences are visible

Add a constant `c` to every `u(x,a)` at a given state. Every `v(x,a)` rises by `c`. Every exponential is multiplied by `e^c`. Every ratio is unchanged.

**The data cannot see level shifts in utility.** Only differences are identified. This is not a weakness of a particular estimator. It is a property of the information in choices. No amount of data fixes it.

### 1.4.3 The anchor

Since levels are invisible, you must *choose* one. This is the **anchor** or **normalisation**: pin one action's utility to a known value and measure everything else from there.

Magnac and Thesmar (2002) formalised this. They name three things that must be set before the model is point identified: the distribution of the unobserved shocks, the discount rate, and current and future preferences in one reference alternative. The usual choice is a reference action with a natural zero, and the usual candidate is an exit or outside option. Kang (2026) calls this the Anchor-Action Assumption and is explicit that it is "a normalization, not a restriction. It fixes the location of the reward."

This project set the exit action's utility to a measured scrap value, `u(x,0) = W̃(x)`, where `W̃` is a standardised liquidation value.

**This is a modelling decision, not a discovery.** Any other anchor gives a different but equally valid set of recovered utilities.

### 1.4.4 What cannot be recovered

Three things, worth naming because papers sometimes forget them.

1. **Utility levels.** Only differences from the anchor.
2. **The discount factor `β`**, from choice data alone with a flexible utility function. Magnac and Thesmar show these models are not identified and determine the exact degree of underidentification. This project fixed `β = 0.976` rather than estimating it. That is standard and honest, as long as it is stated.
3. **The shock scale.** Set to `1` by convention. Rescaling it rescales all utilities together.

---

## 1.5 The other tradition: maximum entropy IRL

Ziebart and colleagues (2008) came at this from driver route modelling. They wanted to learn reward functions from demonstrated behaviour, and applied the method to 100,000 miles of taxi GPS data. Their principle: among all behaviours matching the observed feature counts, pick the one of maximum entropy, that is, the least committed one.

Out of that principle falls a recursion. Their Algorithm 1 states it in exponentiated form, as a backward pass over partition functions `Z`, with the action probability given by `Z_a / Z_s`. Taking logarithms turns that into the **soft Bellman equation**:

```
V^soft(x) = ln [ Σ_a exp{ r(x,a) + β Σ_{x′} p(x′|x,a) V^soft(x′) } ]
```

And the induced policy is

```
π(a|x) = exp{ r(x,a) + β E V^soft } / Σ_b exp{ ... }
```

Compare with (BE). Write them side by side:

```
DDC   :  V(x)      = κ + ln Σ_a exp{ u(x,a) + β E V }
MaxEnt:  V^soft(x) =     ln Σ_a exp{ r(x,a) + β E V^soft }
```

**The only difference is the `κ`.**

The same equation also arises as the solution to an **entropy-regularised MDP**, where the agent maximises reward plus the entropy of its own policy. Haarnoja and colleagues (2017) use this in soft Q-learning. Three literatures, one equation.

---

## 1.6 The two models are the same model

### 1.6.1 The shift

Here is the result, and it is three lines.

> **Proposition 1 (shock-mean conventions are reward shifts).** Fix `u` and `κ`. Define
> ```
> ũ(x,a) := u(x,a) + κ    for every action a, the terminal action included.
> ```
> Then `V_0[ũ] = V_κ[u]` pointwise, and the two models induce identical choice probabilities.

*Proof.* Let `W` be the soft value function at utilities `ũ`:

```
W(x) = ln [ Σ_a exp{ u(x,a) + κ + β E W } ]
     = κ + ln [ Σ_a exp{ u(x,a) + β E W } ]
```

because `e^κ` factors out of every term in the sum. That is exactly (BE) with `W` in place of `V_κ`. Both are fixed points of the same contraction, so by uniqueness they are equal. ∎

**Read what that says.** The difference between the two traditions is not deep. It is a constant added to the reward. Shift every reward by `κ` and the soft value function becomes the Gumbel value function, exactly, everywhere.

### 1.6.2 What this project originally got wrong

The original manuscript claimed the following. When one action leads to an **absorbing exit state**, the `+γ` cannot be absorbed, the two value functions genuinely differ, and the difference is state dependent. It presented this as Theorem 7.1 and built a paper on it.

The algebra in that theorem is correct. Its premise is not.

The theorem holds `u(x,0)`, the exit utility, **fixed** while varying `κ`. Under that constraint, no constant reconciles the two. True.

But Proposition 1 shifts `u(x,0)` too. The words "for every action, the terminal action included" are doing all the work. Shift the exit utility as well and the two coincide exactly, absorbing state and all. The discrepancy is zero.

So the original theorem is not about absorbing states. It is about whether you let the anchor move. That is a different and much smaller claim, and Kang (2026) states the underlying normalisation result explicitly in his Remark 2.9.

**This is the honest summary: there was no theoretical contribution.** Finding that out is what the audit was for.

---

## 1.7 Exit, and why it still matters

### 1.7.1 Absorbing states

An **absorbing state** is one you never leave. A firm that exits does not come back. Formally, exit is an action whose conditional value has no continuation term:

```
v(x,0) = u(x,0)        no β E V term
```

Every other action carries the discounted future. Exit does not.

This asymmetry is why exit is the natural anchor. Its value involves no forecast, so if you can measure something like a liquidation value, you can pin it directly.

### 1.7.2 The incompatibility

Now put the two pieces together and something real appears.

> **Proposition 2 (incompatibility).** These two requirements cannot both hold when the terminal action is taken with positive probability:
> - **(i)** the terminal utility is pinned at a measured value, `u(x,0) = W̃(x)`
> - **(ii)** the recovered continuation utilities do not depend on the convention `κ`.

*Why.* By Proposition 1, invariance to `κ` is achieved by, and only by, shifting all utilities by `κ`, the terminal one included. Requirement (i) forbids moving the terminal utility. So you may have a fixed, interpretable anchor, or convention-invariant answers. Not both. ∎

This is a genuine tension, and it is practical rather than exotic. An applied researcher who anchors on a measured scrap value has, without noticing, made their recovered utilities depend on a convention they probably never thought about.

### 1.7.3 How big is it?

Precisely this big.

> **Proposition 3 (the convention wedge).** With the anchor held fixed and the data `(σ, p)` held fixed:
> ```
> (a)  V_κ(x) − V_0(x)          = κ            constant, not state dependent
> (b)  û^κ(x,a) − û^0(x,a)      = −βκ          for every non-terminal a
> (c)  û^κ(x,0) − û^0(x,0)      = 0            pinned by the anchor
> (d)  differences among non-terminal actions are unaffected
> (e)  every action's gap to exit shifts by exactly −βκ
> ```

The derivation is short. By (INV), `V(x) = κ + v(x,0) − ln σ(0|x)`. The anchor fixes `v(x,0)`, and `σ(0|x)` is data, so `V` shifts by exactly `κ`. Then recovery of utility is `u(x,a) = v(x,a) − β E V`, and `v(x,a)` is pinned by the anchor and the observed probability ratios, so the recovered `u` shifts by `−βκ`.

**The numbers, computed not recalled.** With `δ = 0`, so `κ = γ`:

| `β` | wedge `βκ` in utils | effect on exit odds | error |
|---|---|---|---|
| 0.90 | 0.5195 | ×1.6812 | 68.1% |
| 0.95 | 0.5484 | ×1.7304 | 73.0% |
| 0.976 | 0.5634 | ×1.7566 | 75.7% |
| 0.99 | 0.5714 | ×1.7708 | 77.1% |

At the project's `β = 0.976`, switching convention moves every continuation utility by `0.563` utils and multiplies the odds of exit by `1.757`. **A 76% error in the quantity the model exists to measure, produced by a notational choice.**

The numerical check that the wedge equals `−βκ` exactly agrees to within `3.00e-15`, which is machine precision.

**Note what this is and is not.** It is not a new theorem. Kang derives the same per-step term under his anchor. It is a clean statement of a trap that applied work can fall into.

### 1.7.4 The forward discrepancy

For completeness, the object the original project chased.

> **Proposition 4 (no terminal action).** With no terminal action, `V_γ[u] = V_0[u] + γ/(1−β)` exactly.

*Proof.* Set `c = γ/(1−β)` and check `V_0 + c` solves the `κ = γ` equation. Each period adds `γ` and discounts the rest by `β`, so `γ + βc = c`. Uniqueness finishes it. ∎

At `β = 0.976` that constant is `24.050653`.

> **Proposition 5 (with a terminal action).** `D(x) := V_γ(x) − V_0(x)` is the unique bounded solution of
> ```
> D(x) = γ + ln [ σ_0(x) + Σ_{a≥1} σ_a(x) · exp{ β E D } ]
> ```
> with `γ ≤ D(x) ≤ γ/(1−β)`, and `D` constant exactly when the exit probability does not vary across states.

The intuition is clean once you see it. `D` accumulates one `γ` per period survived. A state that always exits immediately collects one `γ`. A state that never exits collects `γ/(1−β)`. **`D(x)` is `γ` times the expected discounted survival time.** The bracket is not a mystery. It is a lifetime.

This is correct and mildly pretty. It is also not the quantity anyone estimating a structural model actually needs, which is why the report leads with Proposition 3 instead.

---

## 1.8 Where the failures live

Everything above is theory. The report is about estimation, and the bridge is (INV):

```
V(x) = W̃(x) − ln σ(0|x) + κ
```

Two quantities on the right come from counting data in cells: `σ(0|x)` and the transition probabilities behind the recovery step. Both counting procedures failed.

**Failure One.** The transition matrices collapsed. Every next-period state was assigned to one cell out of 625, because missing values propagated through the discretiser. With a single reachable next state, the continuation value `E V` is the same number everywhere. In this project it was `7.701230708570058` at every one of the 625 cells. The model still ran. It still produced utilities. It had no dynamics left.

**Failure Two.** 432 of 625 cells contained no observed exit at all. Additive smoothing with parameter `α_L` fills the gap with `σ(0|x) = α_L / (n_x + A α_L)`, where `n_x` is the number of observations in the cell and `A` the number of actions. Substituting into (INV):

```
V(x) = W̃(x) + ln(n_x + A α_L) − ln α_L + κ
```

**The value function is now a function of cell sample size.** Not of economics. Of how many rows landed in the bin.

Two cells, both with zero exits, both with identical true economics. One holds 6 observations, the other 2090. With `α_L = 0.1` and `A = 3`:

```
n = 6    :  −ln σ(0|x) = 4.1431
n = 2090 :  −ln σ(0|x) = 9.9476
difference = 5.8045 utils
```

**5.80 utils of pure artefact.** For scale, the entire convention wedge of Section 1.7.3, the thing worth writing a report about, is `0.56` utils. The bug is ten times the size of the phenomenon.

Chapter 2 shows the code that did this, line by line, and why twenty one unit tests and two robustness checks all passed anyway.

---

## 1.9 Notation

| Symbol | Meaning |
|---|---|
| `x` | state, observable circumstances |
| `a` | action, with `a = 0` the terminal or reference action |
| `u(x,a)` | flow utility, the object to be recovered |
| `ε(a)` | unobserved shock, Gumbel distributed |
| `δ` | Gumbel location parameter, a convention |
| `γ` | Euler-Mascheroni constant, `0.5772156649015329`, not a convention |
| `κ = δ + γ` | mean of the shock |
| `β` | discount factor, `0.976` per quarter here |
| `v(x,a)` | conditional value: act `a` now, behave optimally after |
| `V(x)` | ex-ante value, before shocks are drawn |
| `V^soft(x)` | the same object with `κ = 0` |
| `D(x)` | `V_γ(x) − V_0(x)`, the forward discrepancy |
| `σ(a\|x)` | conditional choice probability, estimated from data |
| `W̃(x)` | standardised scrap value, used as the anchor |
| `α_L` | additive smoothing parameter |
| `n_x` | number of observations in cell `x` |
| `LSE` | log-sum-exp, `ln Σ e^{·}` |

---

## 1.10 What to read next

In order of how much they will repay you.

1. **Rust (1987)**, the bus engine paper. The founding application.
2. **Hotz and Miller (1993)**, the inversion. Read the first ten pages.
3. **Magnac and Thesmar (2002)**, identification. Short and decisive on what you cannot recover.
4. **Ziebart et al. (2008)**, maximum entropy IRL. Four pages, and the other half of the story.
5. **Kang (2026)**, the lecture note that connects them. Remark 2.9 and Section 3.2 are the relevant parts, and they are the reason this project has no theoretical contribution.

Full details are in the reference list of `REPORT.md`, each one checked against the PDF or the publisher record.
