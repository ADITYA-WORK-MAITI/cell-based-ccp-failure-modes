# Two failure modes in cell-based CCP estimation of dynamic discrete choice models

Aditya Maiti. Independent research, 2026.
ORCID [0009-0004-2501-1459](https://orcid.org/0009-0004-2501-1459).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23208936.svg)](https://doi.org/10.5281/zenodo.23208936)

Conditional choice probability inversion is a standard way to estimate dynamic discrete choice models. One common implementation discretises the state space into cells and estimates choice probabilities and transitions by counting. This repository documents two failure modes of that implementation, both found in a working research codebase, and both of which passed every check the codebase contained.

Read `REPORT.md` first.

## What is valid and what is not

This repository holds two bodies of work. They must not be confused.

**Valid.** `REPORT.md`, everything in `rebuild/`, and the audit in `docs/`. The numbers in the report were produced by `rebuild/run_all.py` and can be regenerated.

**Withdrawn.** The original version of this project, in full. Its theoretical claim does not survive comparison with the prior art, and its empirical results were produced by a defective estimator. `WITHDRAWN_OUTPUTS.md` explains why, file by file. Do not cite or reuse any number or figure from it.

The withdrawn material is retained privately by the author rather than published. The three readable extracts the report relies on as evidence are in `evidence/`.

## Layout

```
REPORT.md              the report
CITATION.cff           how to cite this
WITHDRAWN_OUTPUTS.md   why the original results are invalid

rebuild/               the corrected implementation
  ccp.py               estimator, forward solver, simulation
  tests.py             9 tests, including one that reproduces the defect
  run_all.py           regenerates every number and figure
  out/                 generated results and figures

docs/
  PROJECT_X_AUDIT.md     full audit of the original version
  THEORY_V12.md          the theory, and why its novelty claim was retired
  PROJECT_X_DECISION.md  scope and direction decisions
  MANUSCRIPT.md          superseded draft, kept as a record

evidence/              three extracts the report cites
data/                  the SEC panel, not version controlled
references/            reading library, not version controlled
```

## Learning the material

Two companion chapters build the subject from scratch. They assume no background beyond
basic probability and expectations.

- `docs/CHAPTER_1_THE_MODEL.md` builds the Gumbel choice model, the Bellman equation, the
  Hotz-Miller inversion, maximum-entropy IRL, and the exact sense in which the two
  traditions are one model. Every worked number was computed, not recalled.
- `docs/CHAPTER_2_THE_CODE.md` walks the estimator line by line, shows the two defects in
  the original implementation, and explains why twenty one unit tests and two robustness
  checks all passed over them.

- `docs/TRACEABILITY.md` maps every number and every reference attribution in the three
  documents to the file that produces or supports it, and states plainly what is not
  traceable.

## Reproduce

Needs Python, `numpy` and `matplotlib`.

```
python rebuild/tests.py        # 9 tests of the estimator
python rebuild/verify_math.py  # 49 checks of every equation in docs/
python rebuild/run_all.py      # all numbers and figures
```

`verify_math.py` writes nothing. Its committed console output is
`rebuild/out/verify_math_output.txt`, kept so the per-check deviations are auditable.

Output lands in `rebuild/out/`. Runtime is a few minutes on a laptop. No GPU is used or needed.

## What is not in version control

`data/sec_panel.csv` is 24 MB and is not validated. The code that built it is not in this repository, so it cannot be regenerated or audited. The report makes no empirical claim from it.

`references/` holds 36 published papers as PDFs. They are other people's copyrighted work and are not redistributed here. The four analysis documents in that folder are part of this project and are tracked.

`.venv/` is a local virtual environment.

## Method and tooling

This work was done with AI assistance, under the author's direction, with the author
responsible for every claim in it.

The reason for stating that plainly is the subject of this report. It is about results that
passed their own checks and were wrong anyway. A reader is entitled to know how the work was
produced before deciding what weight to give it.

Nothing here rests on trusting that record. Every mathematical statement has a check in
`rebuild/verify_math.py`, every reported number has a named source in `docs/TRACEABILITY.md`,
and the estimator has nine tests in `rebuild/tests.py`. Run them.

## Licence

Code under MIT. See `LICENSE`.

Text and figures under Creative Commons Attribution 4.0 International. This
covers `REPORT.md`, the documents in `docs/` and `references/`, and the
generated figures in `rebuild/out/`. See `LICENSE-CC-BY-4.0.txt`.

The PDFs described in `references/INDEX.md` are other people's copyrighted
work. They are not in this repository and are not covered by either licence.

## Cite

Maiti, A. (2026). *Two failure modes in cell-based CCP estimation of dynamic discrete
choice models* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23208936

`10.5281/zenodo.23208936` always resolves to the most recent version. The snapshot archived as
v1.0.0 has its own DOI, `10.5281/zenodo.23208937`; cite that one if you need to pin a
specific version.
