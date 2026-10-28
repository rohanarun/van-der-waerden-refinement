# Notice

Pinned sources: this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`,
through `pr/door-one` (`00375ff`, PR #20): `exact-door-one-condition`
(radar-d9: Propositions 1, 4 and 5, the slow-word counts) and
`ap-free-frozen-sets` (the hitting bound (H), the template model, the digit
sets); through them, `source-only-1-16` (radar-3a, Lemma 3: a key occupies
at most two positions) and the OpenAI manuscript pinned in
`source-manifest.json`.

External results, cited and not reproved (read on 27/10/2026): Fox–Hunter,
*Three-color van der Waerden numbers grow super-exponentially*,
arXiv:2606.02541 (Lemma 2.9); Korsky, *Hitting Arithmetic Progressions at the
Square-Root Scale*, arXiv:2606.01780 (and, as cited there, Brown–Freedman and
Truss); Behrend (1946).

Credits: the question is S6 of sprint 4 ("contre-pied"), asked by Erwan.
radar-89 asked that the class be stated as key-measurable colorings, and
that the role of the iid flips be said explicitly; both are done in
Theorem 1. A complementary angle (counting, entropy, discrepancy on (I′) +
(II′)) is radar-d9's.

Review history: radar-cc refereed the first draft ("publishable after (s1),
(s2)"): (s1) the reading of `b` as a parameter of the law holds for
existence, and closures of classes of certificates exist without a vdW
bound; (s2) the Brown–Freedman and Korsky attributions are separated. Both
applied. After radar-dd's S7, the referee's (z): digit sets give hitting
only (they contain whole progressions, so they are not proper); the
sharpness of (D) at `k^{−a}` now rests on a random key set (C1). Applied. The referee's precision (s3) on paying the color word of `c₀` in
that union bound is added.

AI assistance: the reduction, verifier and text were prepared with Claude
Opus 5.5 (Anthropic), in cooperating sessions. Not independently reviewed
by a human. Standard library only; no upstream file is modified.
