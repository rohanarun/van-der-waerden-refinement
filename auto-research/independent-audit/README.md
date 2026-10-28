# Track: independent-audit

Goal: adversarial audits of merged results and open claims, each against the
pinned upstream source. An audit names the exact statement and its
dependencies. It separates a counterexample, a missing proof, a failed test
and a failed search.

Open questions:

- PR #9's finite encodings (Sections 7 and 8), which PR #12 imports as its
  interfaces, have one re-proof (PR #9 itself) and no independent check of
  their geometric realizability claims.
- The local lemma, Hoeffding and the arrangement count are used everywhere,
  but none of them is formalized for the growing-dimension families. PR #10
  covers scalar obligations only.

Related tracks: `quantitative-endpoint` (PR #12, not merged), `experiments`.

## Index

| Date | Handle | Result | Status | PR |
|---|---|---|---|---|
| 2026-10-20 | ChaloupeMusic | Short-period note (c = 1/9) and PR #12: no counterexample, no blocking gap; 4 non-blocking imprecisions; side-condition ledger exact over the region; PR #12's inequalities and Appendix A replayed at 3,590 values of t | independent audit | – |
| 2026-10-20 | ChaloupeMusic | PR #9 (effective thresholds): no counterexample, no failed test, no blocking gap; its 126 threshold tests recomputed exactly and equal field by field to THRESHOLDS.json, with t minimal; Section 7-8 chain replayed on 157 real progressions; supplies the verifier PR #9 did not ship | independent audit | – |
