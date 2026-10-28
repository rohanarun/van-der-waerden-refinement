# Conditional review using the pinned OpenAI construction

Review date: 13 October 2026. This changes the review boundary: the imported
OpenAI construction is assumed, while the refinements are checked against its
actual hypotheses. It does not change the mathematical statements in the PRs.

**Verdict:** no blocking mathematical error was found in the stated conditional
claims of #3, #4, #6, or #7 at the revisions below. This is a mathematical source
review supported by exact checks and selected Lean proofs, not a complete formal
verification of the new arguments. The additional effective-construction claim
in #9 is not certified by this narrower review.

## Assumptions and dependency boundary

The assumed source is `openai/math` at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, specifically Sections 02–07 of
*Quantitative Superexponential Bounds for van der Waerden Numbers*.
Eight retained source sections, including the introduction and upper-bound
section, were authenticated against the original SHA-256 manifest during this
review. See [evidence/conditional-source-check.json](evidence/conditional-source-check.json).

We assume the source coordinate/separation and adaptive-mesh lemmas, finite
equality-inclusive arrangement counts, finite asymmetric local lemma, eligible
pattern and short-path/dichotomy tools, perturbation framework, and digit-product
transfer with their stated hypotheses. Assuming only the source's numerical
headline bound would not justify any of these refinements.

The following changes are reviewed additions, not automatically imported facts:

1. The two-point norm-band improvement and the merged #2 sharpened outer input.
   The shorter cutoff gives `log T_glob = O(k^(2a) log^3 k)`; the incident weights
   still decay with `2a<m`, and balancing the light positions outside eligible
   heavy blocks avoids double counting. The no-heavy-label case is handled
   directly. The outer coloring remains one global full-label coloring.
2. #4's common return, affine collision classes, nested matching, and literal
   certificate encoding. Its repeated-pair identity removes directional step
   data. The factorial gap bound controls the rounding cost by `exp(O(k))`.
   Events assigned to the same certificate are covered by one all-flips event;
   they are not identified with each other and independence between events
   is not assumed.
3. #6's projection and anchored certificates and its complementary progression
   count. Integer digit forms and a nonsingular pivot minor determine the
   remaining step digits. Uniformity in rank keeps the total error subleading.
4. #7's matched start/step digit forms, common digit rank, and added outer-event
   family. The finite family is fixed before sampling label bits. The weighted
   tail estimate uses independent label bits and the multiplicity bound, not
   independent positions. Heavy-run encoding records only the prescriptions
   needed by the cover, so it does not need to reconstruct the full color word.

Thus the reviewed chain is OpenAI → the merged sharpened refinement → #4 → #6
→ #7. The latter PRs have genuine new dependencies on earlier contributions;
those are checked in this chain rather than silently included in the OpenAI
assumption. #3 describes an older, more restrictive union-bound template and
does not contradict improvements using a different cover.

## Verdicts at exact revisions

| PR | Revision | Conditional review result |
|---|---|---|
| #3 | `6caa55cb9d6ed24e6f50ad54d0760b9853faca4e` | Pass for the ceiling proposition with its explicit template/entropy hypotheses. `b<a` and `2a+b≤1` still imply `b<1/3`; the corrected weighted floor-sum bound has the right direction. The subsequent rigidity discussion remains explanatory, not a universal impossibility theorem. |
| #4 | `4b4e80ea5e0ffec956577004905f22659af0bff5` | Pass for the conditional coefficient `1/19`, and the stated region `c<1/18`, using the reviewed sharpened outer input. Rich inequalities are `2c<b(gamma-tau)` and `c<b*tau`, with `tau=gamma/3`. |
| #6 | `fc5738bfda508566e7b4ce706c22bbb2b9194226` | Pass for the conditional coefficient `1/16`, and the stated region `c<1/15`, using the preceding chain. The uniform cover cost is at most `5/2`; the exact rich margin is positive. |
| #7 | `987c96cfda59b65728ae4dcd5adc8a64ff95bab2` | Pass for the conditional coefficient `1/9`, and every fixed `c<1/8`, using the preceding chain and the run justification below. Matching digit costs sum to `2D`; the new non-rich estimate needs `b<a` and `a+b<1`. |
| #9 | `89660352f5dfcf1180a47b224610d444b2ce8701` | Its coefficient route is supported by the preceding chain and its 42 recorded threshold comparisons pass Lean. The stronger claim of an effective, terminating construction valid for all inputs above the displayed threshold is outside this conditional verdict. Assuming the original proof does not establish the new explicit constants and algorithm. |
| #10 | Proof package accompanying this report | Verified as a package of selected obligations: 84 named Lean theorems, standard-axiom audit, source association checks, and four rejection controls pass locally. This is not an additional lower-bound theorem. |

The exact parameter regions for these claims are in
[Parameters.lean](Vdw/Parameters.lean). Supremum endpoints are not attained.
For #7 the total coefficient gain over the source is `100000/9`, approximately
11,111.11. Relative to the merged `1/25` coefficient it is `25/9`, approximately
2.78. These are coefficient ratios within an exponent, not runtime improvements
or finite coloring records.

## The circular-run step in #7

The terse statement that a monotone circular path enters an interval only once
needs the small-width hypotheses in the surrounding construction. Here is the
explicit justification used in this review:

- A first-coordinate mesh cell is a half-open interval of width `H_x<1/2`.
  Points in two distinct integer translates of that cell are separated by more
  than `1/2` in the direction of increasing translates.
- Within a residue class, the lifted first-coordinate path has total motion
  at most `2M H_x<1/2`. It therefore cannot hit two different translates of the
  same cell.
- Inside its one possible translate, the preimage under an affine path is an
  interval. Its integer sample indices are consecutive. The centered second
  coordinates are already real affine paths, so the same interval argument
  applies directly. Intersection over all coordinates preserves consecutiveness.
- The source's separated-residue path lemma puts occurrences of the same full
  label in one residue class. Together these facts give the claimed single run.

The first three scalar implications are now kernel-checked in
[Runs.lean](Vdw/Runs.lean). Association with the actual progression and the
separated-residue premise still uses the reviewed/assumed geometric inputs.

## Evidence and merge boundary

The previous reviews are reused only for unchanged exact heads. Retained review
and independent-check receipts are in [evidence/conditional/](evidence/conditional/). Their independent
checks included #4's pair identity, nested pairs, event covers and prime-power
separation; #6/#7's nonzero digit tails through dimension 32 and pivot recovery;
and #9's independently reconstructed threshold arithmetic. Their finite checks
corroborate the proof review rather than serving as universal proof premises.

The submitted random digit tests in #6 and #7 accept only dimension 2. That
coverage defect remains in those PRs; it does not supply evidence about higher
digit tails. The independent higher-dimensional tests and the universal Lean
recurrence/span lemmas supply separate evidence. They do not by themselves
prove all geometric realizability and counting claims.

At review time, GitHub checks had not passed on these current revisions. The
conditional mathematical verdict and remote CI status are separate. No merge
or combined-branch validation is recorded here; overlapping branches must still
be integrated and checked before their aggregate result is described as merged.

Attribution remains as recorded in the source PRs: OpenAI; Rohan Arun; Artus
Krohn-Grimberghe (`artuskg`); and `DaysSky`, with their disclosed AI assistance.
