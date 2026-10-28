# Attribution and review status

Prepared for GitHub user `ChaloupeMusic` with substantial AI assistance
(Claude, Anthropic), on October 20, 2026, during a coordinated sprint of
several Claude sessions. An adversarial review by a separate session of the
same sprint is pending. No independent human review has taken place.

The construction, event families, finite interfaces and variable-scale
transfer are those of PR #12 by `1337isnot1337`, which this package
reuses and cites. Behind PR #12:

- the cyclic construction, meshes, drift lemmas and digit product come
  from the pinned OpenAI manuscript;
- Rohan Arun's repository supplies the two-point band lemma and the
  sharpened outer argument;
- Artus Krohn-Grimberghe's repeated-key work supplies the certificate
  precursor;
- DaysSky's contributions supply the rank split, matched digit rank and
  short-period runs;
- PR #9 supplies the explicit finite encoding factors, whose displayed
  products Lemma D re-bounds.

The source disclosures attribute substantial AI assistance to their
contributors and models.

New here: the five lemmas and the retuned constants. Erdős's bound
`theta(x) < x log 4` is classical and is not claimed. The audit of PR #12 by
the same sprint (PR #13) measured the slack in PR #12's entropy bounds that
motivated this retuning.

There is no literature-priority claim, end-to-end formal verification or
theorem-sized colouring. The mathematical status is a conditional proof draft
with explicit inherited assumptions.
