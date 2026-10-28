# Adversarial audit: PR #9, the effective completion and its thresholds

**Status:** independent audit, AI-assisted. No counterexample, no failed test
and no blocking gap were found in PR #9. Three non-blocking points are recorded
below. This is not a formal proof, and not a human review.

**Pins.** Repository base `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`. PR #9 head
`89660352f5dfcf1180a47b224610d444b2ce8701` on base
`54ac9715fceab938ca77d5980c36ab691765a04d`, directory `effective-completion/`.
`THRESHOLDS.json` sha256
`a1820e5e6655746248171fc3cd23b2e1e24b99be52a75da80625581e7c900093`.

## Why this audit

PR #9 claims, for every rational `0 < c < 1/8`, a computable `K(c)` such that
`W_r(k) > k^{ck floor(log2 r)}` for every `k >= K(c)` and `r >= 2`, and
`K = 2^33554432` for the literal PR7 tuple (`c = 1/9`) and the literal PR6
tuple (`c = 1/16`). It has no review on GitHub. Its README cites a local review
and an Opus review whose checker is not part of the PR, and its
`THRESHOLDS.json` records `checks_not_executed_again_during_submission_preparation: true`.
PR #12 imports PR #9's factor formulas (Sections 7.3, 7.12, 8.2, 8.3) as
interfaces, and the `independent-audit` track lists them as having "one
re-proof and no independent check of their geometric realizability claims".

## What was checked, and how

1. **Sources.** All 47 records of `DEPENDENCIES.json` were re-hashed: size,
   sha256 and Git blob id. 23 come from the pinned commits of this repository
   and its forks, 24 from the pinned OpenAI manuscript. All match.
2. **The proof, read line by line** (Sections 3 to 13) against the claims it
   imports. Every inequality used in Sections 4 to 11 was traced to a row of
   the Section 12 checklist (table below).
3. **Part A of `verify.py` (exact).** The 21 tests of Section 12, recomputed
   from the parameter tuples alone, for six tuples: literal PR7, literal PR6,
   and the four general-rule tuples PR #9 records (`c = 1/100, 1/9,
   1249/10000, 0.124999999999`). The monomial certificate (12.8) is decided
   by exact integer comparison without allocating `2^{floor(dt)}`. Every
   recomputed field matches PR #9's records (`--thresholds PATH` compares the
   whole file, 126 tests). The returned `t` is minimal among the doubled
   values: at `t/2`, the anchored-entropy test `log k >= 4C_L/eps^2` fails
   for all six tuples, and for PR6 the inverse-log term of (12.1) fails too.
4. **Part B (exact symbolic identities).** (7.8), (7.9), (7.10), (7.11), the
   band decomposition (8.9), the digit expansion (8.2)/(8.3), the rich-split
   identity (9.2) for every rank, and the gap identities of rule (13.1).
5. **Part C (finite exact replays).** Separation (7.1) and the balanced-digit
   expansion (8.1) on every nonzero element of six small groups, including the
   composite base `q = 9`; equality in (7.1) is attained, so its constant is
   sharp. The digit product (13.3) on every ordinary 4-term progression of
   `[0, 7^s)`, `s <= 3`. And the whole chain of Sections 7 and 8 on actual
   progressions of `Z/q^D` in the literal small regime `k = 192 >= 64D`,
   `D = 3`, `q = 1031^2`, with a half-open geometric V-mesh obeying (4.1):
   common return vector, two-point key lemma (7.2), single-class affinity
   (7.4), carries (7.5), vertex identities (7.8)–(7.11), the cell estimate
   `|X_a - q^2<v_a, beta>| < 3`, digit forms (8.3)–(8.5), the C* decoding
   (the step `d` is recovered from the start, the discrete data and the
   digit forms) and the A* band decomposition.
   157 progressions: 87 with collision classes, 7 of them with two or more
   collision classes and nonzero carry differences (digit rank `R` up to 3),
   all decoded.
6. **Part D (mutations).** One mutation per decisive constant or step; each
   makes the corresponding check fail (list in `RESULT.json`).

## Findings

**Counterexample:** none. **Failed test:** none. **Blocking gap:** none.

**Hidden-condition ledger.** Each condition used in Sections 4 to 11, and the
checklist row of Section 12 that implies it for every `k >= K`:

| Condition | Used in | Implied by |
|---|---|---|
| `D <= k/64`, `k^{1-a} >= 128` | (4.9), (8.4), (4.10) | dimension `128 k^{a-1} <= 1` with `D <= 2k^a` |
| `h_0 < 2M` | dilation, (5.3), long blocks | short-period cutoff `8 k^{a-m} log^2 k <= 1` |
| `2M/k <= 1/16`, `4MH < 1` | (5.1), (5.3), (5.4), dichotomy | small blocks `64 k^{m-1} <= 1` |
| `4MH/k <= eta` | (5.6), rotating coordinates | rotating drift `128 k^{a+m-3} <= eps_reg` |
| `D(4 eta + 1/h_0) <= eps_reg` | (5.6) | regular fraction `2/log^2 k <= eps_reg` |
| `A_0(k-h-delta k) >= gamma k` | (6.3) | dichotomy remainder `4A_0 k^{m-1} <= g` |
| `p <= 1/2` | (9.1), (10.6), (11.5) | flip bias |
| `eps^2 l(E) >= 4`, `z_E < 1/2` | (6.2) | first-row, second and third sizes |
| `I_1, I_2, I_3 <= eps^2/(48k)` | (6.4) | first and second incidence; anchored and third-family entropy |
| (9.3) `<= 1/4`, (11.3) `<= 1/4` | Sections 9, 11 | (12.1) through (12.4)–(12.5) |
| (11.6) run term `<= 1/4` | Section 11.2 | (12.2) through (12.6) |
| (10.6) `<= 1/4` | Section 10 | (12.3) through (12.7) |

The derivations in Section 4.3 ((4.9), (4.10)), Section 8.3's factor table,
(11.1), (11.4) and (12.4)–(12.7) were redone by hand; every displayed constant
holds, most with a wide margin.

**Non-blocking points.**

- **P1. No executable certificate is shipped.** Section 12.2 says an
  independent checker "passed all 21 tests for each literal tuple", but the
  checker is not in the PR, and `THRESHOLDS.json` records that the checks
  were not executed again for the submitted revision. The certificates are
  nevertheless correct: Part A recomputes all of them from the parameters and
  matches every recorded field. (Classification: missing test, now supplied.)
- **P2. The PR6 fallback (Section 10) is sketched.** The anchored certificate B
  (10.2)–(10.3) and the projection certificate (10.1) say that "the same
  integer-threshold and crossing-order argument" applies, without the
  explicit factor table that Section 8.3 gives for A*. The statement is
  plausible and its error budget `E_k` has a margin of two orders of
  magnitude, but it is not written out. Theorem 1 (`c = 1/9` and every
  `c < 1/8`) does not use Section 10. (Classification: missing proof, detail
  only, non-blocking for Theorem 1.)
- **P3. The literal threshold is driven by one test.** For both literal
  tuples, `K = 2^33554432` is forced only by the anchored-entropy row
  `log k >= 4C_L/eps^2 = 14,720,000`, that is by the constant `C_L = 92` of
  (4.10) with `eps = 1/200`; every other row passes at `t = 2^24` except, for
  PR6, the inverse-log term of (12.1). A sharper (4.10), as PR #12 later did
  with explicit scales, lowers `K` directly. This is an observation, not a
  defect: PR #9 says the value was not optimized.

## Scope

Parts A and B are exact. Part C is a finite replay: it shows that the encodings
of Sections 7 and 8 hold on actual progressions with collision classes and
nonzero carry differences, at small parameters where all of PR #9's
side conditions hold; it is not a proof of the universal statements. The local
lemma (Section 6.2), the arrangement count (4.3) and the realization procedures
of Section 14 were read, not executed. Resource estimates (Section 16) were not
audited; PR #9 itself marks them as supplementary.

## Reproduce

From the repository root, Python 3 standard library only:

```sh
python3 -B auto-research/independent-audit/2026-10-20-ChaloupeMusic-effective-thresholds-pr9/verify.py
```

It prints `RESULT.json` on stdout and `Test passé` on stderr, in about a
minute. With PR #9 fetched (`git fetch origin pull/9/head`), the field-by-field
comparison with its certificates is

```sh
git show 89660352f5dfcf1180a47b224610d444b2ce8701:effective-completion/THRESHOLDS.json > /tmp/THRESHOLDS.json
python3 -B auto-research/independent-audit/2026-10-20-ChaloupeMusic-effective-thresholds-pr9/verify.py --thresholds /tmp/THRESHOLDS.json
```

`MANIFEST.json` lists the sha256 of the other files of this directory.
