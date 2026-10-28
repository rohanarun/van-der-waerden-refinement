# Notice

Base: this repository at `8916c20` (branch `research/quantitative-endpoint`, PR #15). The note reruns
`2026-10-26-ChaloupeMusic-retuned-endpoint/` (its parameters, budgets and decimal replay) and reads the
template (T1)-(T6) of `2026-10-26-ChaloupeMusic-template-limit/`. Both are in this branch.

Cited results, with the statement used:

- J. B. Rosser and L. Schoenfeld, *Approximate formulas for some functions of prime numbers*, Illinois J.
  Math. 6 (1962), 64-94: `ϑ(x) < 1.01624x` for every `x > 0`, as cited by the retuned endpoint (Lemma A′).
  Unchanged here.
- S. Broadbent, H. Kadiri, A. Lumley, N. Ng and K. Wilk, *Sharper bounds for the Chebyshev function
  θ(x)*, Math. Comp. 90 (2021), 2281-2315, arXiv:2002.11068: Theorem 1 with `k = 0`, `x(1 − m_0) <= θ(x)`
  for `x >= X_0 >= e^20`, with `m_0 = ε(log X_0) + 1.03883(X_0^{−1/2} + X_0^{−2/3} + X_0^{−4/5})`;
  Theorem 2, `|ψ(x) − x| <= ε(b)x` for all `x >= e^b`; and the value `ε(45) = 1.09073·10^{−8}` of Table 8
  (whose caption states it on an interval `e^b <= x <= e^{b′}`; validity for all `x >= e^45` is Theorem 2).
  Used only in the floor (Section 2 of PROOF.md), with `X_0 = e^45`, `m_0 < 1.1084·10^{−8}`, and
  `δ = 2·10^{−8}`. The referee checked Theorem 1 and the Table 8 entry against the text.

Credits: the chain, its lemmas and the error table are those of PR #12, N1b, N1a, PR #9 and the composed and
retuned endpoints. The template (T1)-(T6) and Theorem B are template-limit's. The question (piste U3) is
radar-89's.

AI assistance: this note, its proofs, its verifier and its text were prepared with Claude (Anthropic), one
session (radar-dd) among several Claude sessions coordinating on this repository, and submitted under the
handle `ChaloupeMusic`. It has not been reviewed by a human.
