# Chapter 2. The Code, From Scratch

**Aditya Maiti.** Companion to *Two failure modes in cell-based CCP estimation of dynamic discrete choice models*.

Chapter 1 built the model. This chapter builds the program that estimates it, shows the two places the original program broke, and shows why every test it had still passed. All code shown is the real code from `rebuild/ccp.py`, not a simplification.

---

## 2.1 What the program has to do

You have a panel. Rows are firm-quarters. Each row has four numbers describing the firm, one action taken, and the firm's numbers next quarter.

You want `u(x,a)`, the flow utility of each action in each state.

Chapter 1 gave the recipe. Three equations, applied in order:

```
V(k)   = W̃(k) − ln σ(0|k) + κ                      (INV)
Y_a(k) = ln[ σ(a|k) / σ(0|k) ] + W̃(k)              (TARGET)
u_a(k) = Y_a(k) − β (T_a V)(k)                     (RECOVER)
```

To use them you need three estimated objects:

- `σ(a|k)`, the probability of each action in each cell
- `T_a`, the transition matrix for each continuation action
- `W̃(k)`, the anchor value

So the program is six steps.

```
1. discretise    continuous states  ->  cell ids
2. count         cell ids, actions  ->  σ
3. count         cell ids, actions, next cell ids  ->  T_a
4. invert        σ, W̃  ->  V
5. recover       V, T_a  ->  u
6. check         diagnostics
```

Steps 1, 2 and 3 are counting. Steps 4 and 5 are three lines of algebra. **Both failures were in the counting.** This is worth internalising. The mathematics was never the fragile part.

---

## 2.2 Step 1: continuous states into discrete cells

### 2.2.1 Why discretise at all

`T_a` is a matrix. A matrix needs a finite index set. But `LIQ`, `LEV`, `ROA` and `SIZE` are continuous. So you chop each into bins and treat the combination as one cell.

With 4 variables and 5 bins each you get `5⁴ = 625` cells. That number matters later.

The natural binning is by **quantiles**, so each bin holds roughly the same number of observations. Equal-width bins would be useless here, because `LEV` had values above 100 in 13.3% of rows.

### 2.2.2 How binning works

```python
def make_edges(x, n_bins):
    x = np.asarray(x, dtype=float)
    qs = np.linspace(0.0, 100.0, n_bins + 1)
    return [np.nanpercentile(x[:, j], qs) for j in range(x.shape[1])]
```

For 5 bins this asks for the 0th, 20th, 40th, 60th, 80th and 100th percentiles. Six numbers define five intervals.

Then each row is placed:

```python
interior = edges[j][1:-1]                        # drop the outer two
idx = np.searchsorted(interior, col, side="right")
bins[:, j] = np.clip(idx, 0, n_bins - 1)
```

`np.searchsorted` answers "where would this value be inserted to keep the array sorted?". That index *is* the bin number.

Finally the four bin numbers collapse to one cell id by mixed-radix encoding, exactly like reading a 4-digit number in base 5:

```python
mult = np.array([n_bins ** (d - 1 - j) for j in range(d)])
cells = bins @ mult
```

Bins `(3,1,4,0)` become `3·125 + 1·25 + 4·5 + 0·1 = 420`.

### 2.2.3 Failure One, in three lines of numpy

The original code called `np.percentile`, not `np.nanpercentile`, on the **next-period** state array.

That array had missing values. Of 146,985 rows, **2,970 were entirely NaN**: the firm's last observed quarter has no next quarter.

Now follow the consequences.

**One.** `np.percentile` with any NaN present returns `nan` for every percentile. Not an error. Not a warning. Just `nan`. So the bin edges became `(nan, nan, nan, nan, nan, nan)`.

**Two.** The code then winsorised the data to those bounds using `np.clip(x, nan, nan)`, which makes **every** value NaN. One firm's missing final quarter destroyed the entire next-period array, all 146,985 rows.

**Three.** `np.searchsorted` does not raise on NaN. NaN compares false against everything, and searchsorted's ordering convention places it at the **end**. So every row got the top bin in every dimension: `(4,4,4,4)`.

```
4·125 + 4·25 + 4·5 + 4·1 = 624
```

**Every next-period observation was assigned to cell 624.** One cell out of 625.

This was verified by executing the original code path on the real panel. The output is `unique next-cell indices: [624]`.

### 2.2.4 What that did to the economics

A transition matrix with one reachable column says: whatever you do, wherever you are, you end up in the same place.

Pull that through `(RECOVER)`. The continuation term `(T_a V)(k)` becomes `V(624)` for every `k`. A constant. From the saved results:

```
T[1]: 1 reachable column (624, 100% of mass)
T[2]: column 624 holds 99.52% of mass
Z[:,0]: exactly one distinct value, 7.701230708570058, across all 625 cells
```

**The model had no dynamics.** `u_a(k) = Y_a(k) − β·constant`. The recovered utilities were just the static target `Y` shifted by a fixed number. Every dynamic claim the project made rested on a constant.

### 2.2.5 The second, independent discretisation bug

There was a separate error in the same place. Time-`t` states and time-`t+1` states were binned against **two different percentile grids**, each computed from its own array.

So `T_a[k, k′]` mapped a cell in one partition to a cell in a different partition. Row `k` and column `k` were not the same region of state space. Even with no NaN at all, that matrix would have been meaningless.

### 2.2.6 The fix

Two repairs, labelled R1 and R2 in the code.

**R1.** Compute the edges once, from the time-`t` states only, and reuse them for both arrays. Now row `k` and column `k` denote the same region.

**R2.** Flag bad rows instead of silently binning them.

```python
bad = ~np.isfinite(x).all(axis=1)
...
cells[bad] = -1
```

A row with any non-finite entry returns `-1`. Downstream every counting routine filters on `cell_ids >= 0`. The NaN rows are excluded, counted, and reported. They can no longer quietly become cell 624.

`nanpercentile` in `make_edges` is the belt to R2's braces.

---

## 2.3 Step 2: counting choices

### 2.3.1 The counting

```python
n_ka = np.zeros((K, n_actions), dtype=float)
np.add.at(n_ka, (cell_ids[keep], actions[keep]), 1.0)
n_k = n_ka.sum(axis=1)
sigma = (n_ka + alpha_L) / (n_k[:, None] + n_actions * alpha_L)
```

`np.add.at` is an in-place scatter-add. It increments `n_ka[cell, action]` once per row, handling repeats correctly, which plain fancy indexing does not.

The last line is **additive smoothing**, often called Laplace smoothing. Instead of the raw frequency `n_ka / n_k`, add a small pseudo-count `α_L` to every cell-action pair.

### 2.3.2 Why smooth at all

Without smoothing, a cell with zero observed exits gives `σ(0|k) = 0`. Then `(INV)` computes `ln 0 = −∞` and `V(k) = +∞`. The program dies, or worse, propagates infinities.

Smoothing is the standard fix and is not in itself wrong. It is the right tool. The problem is what it quietly does when the zeros are not rare.

### 2.3.3 Failure Two, in one substitution

Set `n_{k,0} = 0`, meaning no exits observed in cell `k`. Then

```
σ(0|k) = α_L / (n_k + A·α_L)
```

Substitute into `(INV)`:

```
V(k) = W̃(k) − ln σ(0|k) + κ
     = W̃(k) − ln α_L + ln(n_k + A·α_L) + κ
```

**Read the result.** In any cell with no observed exit, the estimated value function is the anchor plus `ln(n_k)` plus constants. It is a deterministic, increasing function of **how many rows landed in the bin**.

Not of profitability. Not of leverage. Of sample size.

In the SEC application, **432 of 625 cells had no observed exit**. Over two thirds of the state space had a value function determined by binning density.

### 2.3.4 The arithmetic, concretely

`α_L = 0.1`, `A = 3` actions. Two cells, both with zero exits.

```
n_k = 6     ->  −ln σ(0|k) = 4.1431
n_k = 2090  ->  −ln σ(0|k) = 9.9476
                 difference = 5.8045 utils
```

Identical economics. **5.80 utils apart.**

Put that next to the real phenomenon from Chapter 1. The convention wedge, the thing worth writing about, is `0.563` utils at `β = 0.976`. The artefact is **ten times larger than the effect**.

The five cells with the largest reported discrepancy in the original results were cells 525, 526, 531, 532 and 344, holding 2090, 1400, 1289, 1117 and 855 observations. The implied exit count in every one of them is **zero**. The headline finding was a ranking of bin sizes.

Solving the smoothing identity backwards for the integer exit count reproduced all ten reported `σ₀` values to better than `5e-7`, which is how this was confirmed rather than merely suspected.

### 2.3.5 The fix

There is no clever repair. Smoothing cannot invent an exit that was never observed. The honest fix is to make the problem **visible**:

```python
return sigma, n_ka, n_k
```

The function now returns the raw counts alongside the smoothed probabilities. The caller reports how many cells have `n_{k,0} = 0`. In the corrected simulations that count goes `10 → 0 → 0 → 0` as the sample grows, which is what a healthy estimator looks like.

If the count is large, the answer is not a better `α_L`. It is coarser cells, more data, or a different estimator.

---

## 2.4 Step 3: counting transitions

```python
for a in range(1, n_actions):
    M = np.zeros((K, K))
    sel = (actions == a) & (cell_ids >= 0) & (next_cell_ids >= 0)
    np.add.at(M, (cell_ids[sel], next_cell_ids[sel]), 1.0)
    rs = M.sum(axis=1)
    empty = rs == 0
    M[~empty] /= rs[~empty, None]
    M[empty] = 1.0 / K
    T[a] = M
    n_fallback[a] = int(empty.sum())
```

Count every observed `(cell, action) → next cell` move, then normalise each row to sum to one.

The loop starts at `a = 1`. **Exit has no transition matrix**, because exit is absorbing. There is no next state. This is Chapter 1 Section 1.7.1 expressed in a loop bound.

### 2.4.1 The fallback and why it must be counted

Some `(cell, action)` pairs are never observed. The row is all zeros and cannot be normalised. The code fills it with the uniform distribution `1/K`.

That is a defensible default. It is also an admission that you know nothing about that row. Repair R3 is the single line

```python
n_fallback[a] = int(empty.sum())
```

If a quarter of your rows are uniform fallbacks, your continuation values are mostly the global average of `V` and carry almost no local information. The original code did this substitution silently. Now it reports.

**The general lesson is larger than this bug.** A fallback that is never counted is indistinguishable from a result.

---

## 2.5 Steps 4 and 5: inversion and recovery

```python
V = w - np.log(sigma[:, 0]) + kappa
for i, a in enumerate(range(1, n_actions)):
    Y[:, i] = np.log(sigma[:, a]) - np.log(sigma[:, 0]) + w
    u[:, i] = Y[:, i] - beta * (T[a] @ V)
```

Three lines, and they are exactly `(INV)`, `(TARGET)` and `(RECOVER)` from Chapter 1. No iteration. No optimiser. No convergence criterion. **This is the part that always worked.**

Repair R4 made `kappa` an explicit argument with no hidden default behaviour. Pass `kappa=np.euler_gamma` for the economists' convention, `kappa=0.0` for the machine learners'. Proposition 3 is then directly testable: run both, subtract, and check the gap is `−βκ`. Test T5 does exactly that and it holds to `3.00e-15`.

Note how short this is relative to the counting. Roughly 8 lines of algebra against 60 lines of counting. The failure rate was the reverse.

---

## 2.6 Solving the model forward

For simulation you need the other direction: given utilities, find `V`.

```python
V = np.zeros(K)
for it in range(max_iter):
    cols = [u_exit] + [u_cont[:, i] + beta * (T[i + 1] @ V) for i in range(nc)]
    V_new = kappa + logsumexp_rows(np.column_stack(cols))
    if np.max(np.abs(V_new - V)) < tol:
        return V_new, it + 1
    V = V_new
```

This is value iteration, and it is `(BE)` from Chapter 1 typed out. Start anywhere, apply the operator, repeat. Lemma 1 guarantees it converges, because the operator is a `β`-contraction. With `β = 0.976` the error shrinks by 2.4% per sweep, so `tol = 1e-12` is reached in a few thousand iterations.

`logsumexp_rows` subtracts the row maximum before exponentiating. Without that, `exp(800)` overflows to infinity and the result is `nan`. This is standard and the code does it.

---

## 2.7 Why twenty one tests passed over two fatal bugs

This is the most useful section of the chapter, because the failure of the checks is more instructive than the bugs.

### 2.7.1 The tests never called the estimator

The original project had 21 unit tests. **Not one of them called `run_estimator`.** They tested helper functions in isolation: the log-sum-exp, the scrap value transform, the z-score. Every one of those helpers was correct.

A test suite that never runs the pipeline end to end tests the pieces, not the thing.

### 2.7.2 The spectral radius check cannot see the bug

The code computed `ρ(βM)` with `M = Σ_a diag(σ_a) T_a` and checked it was below 1. A sensible stability condition.

It was `0.96624` with the degenerate matrices, and `0.96624` with healthy ones.

**Identical to five decimal places.** The reason is structural: `ρ(βM) ≈ β` whenever the rows of `M` sum to something close to the survival probability, and that holds whether the mass sits in one column or spreads over 625. The check is blind to the thing it looks like it should catch.

The comment left in the code says so plainly, so nobody repeats the mistake:

```python
# NOTE: the audit found this check PASSES (rho ~= beta) even when every T_a
# is degenerate, so it must not be treated as evidence that the transition
# matrices are informative.  Use transition_diagnostics for that.
```

### 2.7.3 The robustness sweep could not fire

The project swept `α_L` over `{0.01, 0.1, 0.5, 1.0}` and found the results stable. It read that as reassurance.

Look again at the identity:

```
V(k) = W̃(k) + ln(n_k + A·α_L) − ln α_L + κ
```

`α_L` enters almost entirely through the constant `−ln α_L`, which is **the same for every cell**. Changing it shifts the whole value function up or down. It cannot change the *pattern*, and the pattern is the bug.

Measured directly:

| `α_L` | cells with no exits | corr(`V̂`, `ln n_k`) |
|---|---|---|
| 0.01 | 14 of 32 | 0.505 |
| 0.1 | 14 of 32 | 0.505 |
| 0.5 | 14 of 32 | 0.505 |
| 1.0 | 14 of 32 | 0.505 |

**`0.505` at every value.** The sweep was structurally incapable of detecting the defect. It was not a weak check. It was the wrong check, and it provided false comfort.

### 2.7.4 The three checks that do work

```python
def transition_diagnostics(T):
    out = {}
    for a, M in T.items():
        col_mass = M.sum(axis=0)
        out[a] = {
            "n_reachable_columns": int((col_mass > 1e-12).sum()),
            "max_column_mass_share": float(col_mass.max() / col_mass.sum()),
            "row_sums_ok": bool(np.allclose(M.sum(axis=1), 1.0)),
        }
    return out
```

1. **Count reachable columns.** Degenerate gives `1`. Healthy gives hundreds. This is a one-line check that would have caught Failure One on day one.
2. **Count cells with zero reference-action observations.** Catches Failure Two.
3. **Count fallback rows.** Catches silent uniform substitution.

None of them is sophisticated. All three are counts. That is the point: **the diagnostics that would have saved this project are simpler than the ones that did not.**

---

## 2.8 The test suite now

Nine tests in `rebuild/tests.py`. Five check the mathematics, four check the failures.

| Test | Checks |
|---|---|
| T1 | Reward-shift equivalence, Proposition 1 |
| T2 | No constant shift under a fixed anchor, Corollary 1 |
| T3 | Continuation subproblem exact, Proposition 4 |
| T4 | `D` constant exactly when exit probability is state invariant, Proposition 5 |
| T5 | Convention wedge equals `−βκ`, Proposition 3 |
| T6 | Recovery works and improves with sample size |
| T7 | **Regression on Failure One** |
| T8 | Transition diagnostics detect degeneracy |
| T9 | Sparse-exit degradation is reported, not hidden |

T7 deserves a note. It contains `_original_discretise`, a faithful reimplementation of the broken code path, and asserts that it collapses to **exactly one** cell while the fixed path yields 624 and flags 199 NaN rows. The bug is pinned in place by a test that fails if anyone reintroduces it.

T4 also deserves a note, as a lesson in test design. Its first version was wrong, not in its assertion but in its setup: the exit utilities were so far below the continuation values that the exit probability was around `1e-20`, which pins `D` at its ceiling in both arms and makes the test pass for the wrong reason. It now bisects a scalar exit-utility level until the mean exit probability is near `0.10`, and asserts `1e-4 < σ₀ < 0.6` in both arms. **A test that cannot fail is not a test**, and the guard makes that failure mode impossible to reintroduce silently.

---

## 2.9 Does the corrected estimator work?

Yes, and the criterion is stated in advance rather than after seeing the answer.

For a consistent estimator, root mean squared error should fall as `N^(−1/2)`, so a log-log plot against sample size should have slope near `−0.5`.

| `N` firms | observations | RMSE `u1` | RMSE `u2` | RMSE `u1 − u2` | cells with no exits |
|---|---|---|---|---|---|
| 500 | 7,841 | 0.4598 | 0.3600 | 0.4744 | 10 |
| 2,000 | 30,210 | 0.2385 | 0.1218 | 0.2099 | 0 |
| 8,000 | 121,420 | 0.1603 | 0.1011 | 0.1107 | 0 |
| 32,000 | 482,592 | 0.0548 | 0.0505 | 0.0396 | 0 |

**Fitted slope `−0.4890`.** Target `−0.5`. The estimator is consistent.

Compare with the original, where RMSE was flat in `N` (`3.5156` at `N = 500`, `3.1852` at `N = 5000`) and **rose** with panel length. Error that does not fall with data is not sampling error. It is bias, and in that case it came from a data generating process that did not match the estimator's own assumption about the anchor.

---

## 2.10 Running it

```
python rebuild/tests.py     # 9 tests, about a minute
python rebuild/run_all.py   # every number and figure, a few minutes
```

Needs Python, `numpy` and `matplotlib`. No GPU. No cluster. Runs on a laptop.

Output lands in `rebuild/out/`: `results.json`, `RESULTS.md`, and three figures.

**On reproducibility.** On 4 October 2026 the published code was re-run from a clean copy and the output compared against the committed `results.json`, key by key. Of **186 values, 185 were identical** and the only difference was the generation timestamp. Seeds are fixed in source. That is the standard the report holds itself to, and it is the standard the original code could not meet, since 8 of its 15 result files had no generating script at all.

---

## 2.11 Five things worth taking away

1. **The arithmetic was never the problem.** Three lines of inversion worked perfectly. Sixty lines of counting destroyed the study.
2. **`np.percentile` propagates NaN silently.** So do `np.clip` and `np.searchsorted`, each in its own way. None of them raises. Three quiet behaviours composed into one fatal one.
3. **Smoothing a zero does not create information.** It replaces an honest `−∞` with a confident number that encodes your bin sizes. If most cells have no reference-action observations, the estimator is reporting your histogram back to you.
4. **A check that passes in both the broken and healthy case is not a check.** The spectral radius gave `0.96624` either way. Before trusting a diagnostic, verify it fails on a case you know is broken.
5. **Test the pipeline, not only the pieces.** Twenty one green tests over two fatal bugs, because no test ever called the estimator.
