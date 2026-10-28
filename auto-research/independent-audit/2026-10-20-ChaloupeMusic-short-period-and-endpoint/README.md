# Adversarial audit: the short-period note (c = 1/9) and PR #12's endpoint transfer

**Status:** independent audit, AI-assisted. No counterexample and no blocking gap
were found in either object. Four non-blocking imprecisions are recorded below.
This is not a formal proof, and not a human review.

**Pins.** Base `63bef9ca996786a41169de4a0c3d6b3b47b0fe96` (contains
`short-period-runs-proof.md` from PR #7, revision `987c96c`). PR #12 head
`029431bb29f2bc64bf3f6dd150ddd15bbdf7c7d5`. PR #9 head
`89660352f5dfcf1180a47b224610d444b2ce8701`. PR #10 head
`a46ef51768724334affb3af77e4b04d7f60ae322`. OpenAI source at `fd4aeeb`,
Sections 02 to 07, hash-checked against `source-manifest.json`.

## What was audited, and how this differs from earlier reviews

1. `short-period-runs-proof.md`, read step by step against the pinned source
   lemmas it calls: the drift, path, heavy-width and short-period paragraphs
   of Section 05, the counting lemmas of Section 03, and the local lemma of
   Section 04. The digit-rank, rank-certificate and repeated-key notes were
   read for the facts the 1/9 chain imports from them.
2. PR #12 (`auto-research/quantitative-endpoint/`), Sections 3 to 10 and
   Appendix A. This is the only open claim at the 1/8 endpoint. Its track
   README lists independent review as pending.

PR #10's conditional review gives a verdict on the chain and kernel-checks the
scalar part of Lemma 1. PR #9 re-proves the chain with effective thresholds.
This audit adds three things they do not contain:

- a ledger of every hidden "for sufficiently large k" condition of the 1/9
  chain, written in exponent form and checked exactly over the whole open
  region (Part A of `verify.py`);
- the first review of PR #12;
- an independent numeric replay of PR #12's explicit inequalities, and of
  its Appendix A against PR #9's factor formulas (Parts B and C).

## Findings on the short-period note

**Counterexample:** none. **Failed test:** none.

**Non-blocking imprecisions** (each one is a missing detail with an obvious repair,
not a false step):

- **M1. Lemma 2, y-coordinates.** The note allows abstract paths `A + jw` to
  leave the representative cube, so each V-endpoint needs up to three real
  lifts. The count is then `3k(|V|+1)` lines, not `k(|V|+1)`. This changes a
  constant only. PR #9 (4.8) already counts `2k(J+1)`.
- **M2. Origin of `a + b < 1`.** In case (ii), the V-box part of the key word
  (`exp(O(D log k))`) needs the same inequality as the run code
  (`exp(O(D log^3 k))`). The note names only the run code. The inequality
  is unchanged.
- **M3. Parameter transfer is not stated.** The note uses Lemmas A\*, C\* and
  facts (R1) to (R5) at `a = 49/100`, `m = 99/100`, but they were written with
  `a = 333/1000`, `m = 4/5`. Their hidden conditions are listed in the table
  below: `4kH < 1`, `D = o(k)`, `4D(k+2)q/k^2 < q/8`, `3|v|_1/k^2 < 1`, and an
  error `O(log q + D log k + k) = o(k log k)`. All of them hold for every
  `0 < a < 1`, independently of `m`. The transfer is therefore valid. Part A
  checks this exactly.
- **M4. Lemma 1, circle step.** "A monotone path enters a box once" needs the
  small total motion `2MH_x < 1/2` against the interval width. This step is
  already supplied by PR #10 (`Runs.lean`) and PR #9 (Section 5); it is
  credited, not new here.

**Side-condition ledger** (Part A). Each condition is a strict linear
inequality in `(a, m, b)`. The margin is taken at the explicit 1/9 tuple. The
supremum is taken over the closed region `0 <= b <= a`, `2a <= m <= 1`; a
supremum at most the bound gives the strict inequality on the open region.

| Condition | Where it is used | Margin at 1/9 | Sup over region |
|---|---|---:|---:|
| `a < m` | `h_0 < 2M` | 1/2 | 0 |
| `2a < m` | first local-lemma family, `log T_glob = o(M)` | 1/100 | 0 |
| `m < 1` | drift lemma, `2M/k <= 1/16`, block coverage | 1/100 | 1 |
| `m < 2` | path, heavy-width, short-period motion, Lemma 1 | 101/100 | 1 |
| `m < 3` | `|v - λu| <= 6MH/k < 1` | 201/100 | 1 |
| `a + m < 3` | rotating drift `4MH/k < η` | 38/25 | 3/2 |
| `a < 1` | Lemma C/C\* digit windows, `O(D log k)` errors | 51/100 | 1/2 |
| `a > 0` | `O(log q)` errors; case (i) key words | 49/100 | – |
| `b < a` | case (ii): `6 log q = o(pk)` | 1/200 | 0 |
| `a + b < 1` | case (ii): V-box word and run code `= o(pk)` | 1/40 | 1 |
| `b > 0` | `p <= 1/2` eventually | 97/200 | – |

**Where the region binds.** Only case (ii) of the non-rich estimate uses `b`
(few s-light positions, long heavy runs, heavy keys unflipped). Case (i) costs
`exp(-Ω(k log k))` against key words of entropy `o(k log k)`, so it has a wide
margin.

## Findings on PR #12

**Counterexample:** none. **Failed test:** none. **Blocking gap:** none found in
the new arguments (Sections 3 to 10).

Checked step by step:

- **(9) and (11).** The Chebyshev-type bound `π(x) <= 10x/log x` is proved
  correctly: `θ(2^j) < 2^{j+1} log 2 <= 4x`, then the primes above `√x` are
  counted. `log λ <= 60 h_0` follows from `log h_0 >= t/3` and `log(2M) <= 2t`.
- **Family 1.** The additive tolerance `k/t` is valid. Weighted Hoeffding
  with `Σ w_β² <= (k/M)|S| <= k²/M` gives `2 exp(-2M/t²)`. There is one event per
  actual word, so the total weight is at most `T_glob e^{-M/t²}`.
- **Families 2 and 3, criterion (24).** The bounds `15Dt <= h/(16t²)` (for
  `h > h_0`), `M_s/32 >= 128Dt` and `w >= 1` give `e^{-w-1/8} >= 2e^{-2w}`.
- **Dichotomy (25).** `A_0(k-h) - k/t >= (1/2 - 3.5/t)k` uses `h <= 2M <= 2k/t`
  and `A_0 <= 1/2`. It also holds when the contribution of `S` is negative.
- **Rich split (27).** The identity `T_R L - R log q = (γk - T_R)L - (2D-R)log q
  = Γ` is exact, and `T_R <= γk/2 < γk`.
- **Section 9.** Many s-light positions give `k/8` opposite positions and
  `k/16` flips. Few give at most `M_s` runs, `k/4` prescribed keys and
  `exp(-pk/4)`.
- **Appendix A.** Its factor table is PR #9's (Sections 7.3, 7.12, 8.2 and
  8.3), with the same sums `6 log q + 81Dt + 9k` and `4 log q + 26Dt + 2k`.
  PR #9 derives these factors under `k >= 64D` and `q > k`, both true here.
  Part C re-evaluates every factor formula at PR #12's own scales.
- **Numeric replay** (Part B). All 35 explicit inequalities of Sections 4 to
  9 were recomputed from the definitions, ceilings and floors included, with
  the worst source prime `P = 2k²`. They hold at every integer `t` in
  `[512, 4096]` and at `t = 5000, 10^4, 3·10^4, 10^5, 10^6`.
- PR #12's own `verify.py` was rerun: `PASS: 14 exact certificates valid for
  every real t >= 512`, 9 negative controls rejected, 8 integrity files
  checked.

**Not checked:** PR #9's encodings themselves, which PR #12 imports as its
Section 2 interfaces; the local lemma and Hoeffding's inequality as formal
statements; and PR #12's all-larger-t monomial certificates beyond rerunning
its verifier.

**On the rate.** The `k log log k` loss comes from `p ∝ t⁴/√k`, that is
`D ∝ √k/t³`. Two Hoeffding tolerances `1/t` (outer families 1 and 2) contribute
`t²`, the cap `M <= k/t` on the closest-return block lost in `γ` contributes
`t`, and `log q = F/D ∝ t` contributes `t`. In a heuristic accounting (not a
theorem), retuning `ε`, `ε_reg` and `M = μk/t` changes only the `O(k)` term. A
smaller coefficient in front of `k log log k` would need a different mechanism.

## Reproduce

```sh
python3 -B auto-research/independent-audit/2026-10-20-ChaloupeMusic-short-period-and-endpoint/verify.py
```

Expected result: exit code 0, and standard output byte-identical to `RESULT.json`
(about 5 s, standard library only). Part A runs in exact fractions; Parts B and C use
90-digit `decimal` arithmetic in log space, with terms in `log q` cancelled exactly
before comparison.

Negative controls run by `verify.py`:

- four points just outside the region violate `b < a`, `2a < m`, `a + b < 1`
  and `a < 1` respectively;
- with `D = √k/(64t³)` instead of `√k/(4096t³)`, (18) fails at `t = 512`;
- the `6 log q` term of `E` is load-bearing, since the first arrangement
  factor alone exceeds `100Dt`.

Mutation tests, run by hand and not part of `verify.py`:

| Change | Result |
|---|---|
| `4096 -> 512` in `u` | caught by (14) and (18) |
| `65536 -> 4096` in `p` | caught by (31) |
| `20 -> 15` in `F` | caught by (26) |
| `7k -> 6k` budget in Appendix A | caught |
| `M_s = 4096Dt -> 1024Dt` | still passes: the actual `log A_s` is about `19Dt`, not the `40Dt` bound, so (23) keeps slack |

## Scope

This audit makes no claim of a new bound or a new coefficient. "No error found"
is a failed search for errors, not a proof of correctness. Parts B and C are
finite replays at the listed `t`; they corroborate and do not replace PR #12's
all-`t` certificates.
