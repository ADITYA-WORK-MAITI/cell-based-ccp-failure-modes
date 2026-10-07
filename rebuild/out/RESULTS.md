# Generated results

Produced by `rebuild/run_all.py` on 2026-10-04T13:07:48.157946+00:00.

numpy 2.5.3; seeds fixed in source.


## Gate 1 — does the corrected estimator work?

**PASS** — log-log slope of RMSE on N = `-0.4890` (target: near −0.5).


| N | observations | RMSE u1 | RMSE u2 | RMSE (u1−u2) | cells w/o exits |
|---|---|---|---|---|---|
| 500 | 7841 | 0.4598 | 0.3600 | 0.4744 | 10 |
| 2000 | 30210 | 0.2385 | 0.1218 | 0.2099 | 0 |
| 8000 | 121420 | 0.1603 | 0.1011 | 0.1107 | 0 |
| 32000 | 482592 | 0.0548 | 0.0505 | 0.0396 | 0 |

## Gate 2 — is the convention wedge material?

**PASS** at the 10% exit-odds threshold.


At β = 0.976: exit-margin bias **0.5634 utils**, exit-odds error factor **1.7566** (**75.7%**).


| β | βκ (utils) | exit-odds factor | error % | max dev from Prop 3 | wedge / margin SD |
|---|---|---|---|---|---|
| 0.9 | 0.5195 | 1.6812 | 68.1% | 2.00e-15 | 0.514 |
| 0.95 | 0.5484 | 1.7304 | 73.0% | 1.89e-15 | 0.513 |
| 0.976 | 0.5634 | 1.7566 | 75.7% | 3.00e-15 | 0.551 |
| 0.99 | 0.5714 | 1.7708 | 77.1% | 5.55e-15 | 0.535 |

The `max dev from Prop 3` column is the numerical check of THEORY_V12 Proposition 3: the wedge equals −βκ exactly, so these should be at machine precision.


## Laplace smoothing under sparse exits

Realised exit rate 0.00100.


| α_L | cells w/o exits | share | corr(V̂, ln n_k) there | RMSE u1 | RMSE (u1−u2) |
|---|---|---|---|---|---|
| 0.01 | 14 | 0.438 | 0.505 | 0.6400 | 0.1994 |
| 0.1 | 14 | 0.438 | 0.505 | 0.3717 | 0.1290 |
| 0.5 | 14 | 0.438 | 0.505 | 0.3910 | 0.1321 |
| 1.0 | 14 | 0.438 | 0.505 | 0.4451 | 0.1442 |

## Test suite

- `PASS` — T1 reward-shift equivalence (Prop 1)
- `PASS` — T2 no constant shift under fixed anchor (Cor 1)
- `PASS` — T3 continuation subproblem exact (Prop 4)
- `PASS` — T4 D constant iff exit prob invariant (Prop 5)
- `PASS` — T5 convention wedge = -beta*kappa (Prop 3)
- `PASS` — T6 GATE 1: recovery + consistency in N
- `PASS` — T7 NaN discretisation defect regression
- `PASS` — T8 transition diagnostics catch degeneracy
- `PASS` — T9 sparse-exit degradation reported
