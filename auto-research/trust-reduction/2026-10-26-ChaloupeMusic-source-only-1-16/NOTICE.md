# Notice

Pinned sources:

- this repository at `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`
  (`sharpened-region-proof.md`, `short-period-runs-proof.md`,
  `repeated-key-certificate-proof.md`, `README.md`);
- PR #10 at `a46ef51768724334affb3af77e4b04d7f60ae322`
  (`formal/CONDITIONAL-REVIEW.md`, `formal/Vdw/Geometry.lean`);
- OpenAI, *Quantitative Superexponential Bounds for van der Waerden Numbers*,
  `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, `build/sections/`,
  SHA-256 of the sections used:
  - `02-setup.tex` `9ba2817eda5b94221c4f05ba59835bef53760fbffe7eda896228b323b7cb3beb`
  - `03-counting.tex` `ca84ac51bf6c8539f2458bdc462c98ef465ea70afaa15496d0e6fcaec453c243`
  - `04-outer.tex` `e602972f1194c81ec780c4e17b8c5d3f94874db59f42dbfbc3008f9cec0d5ae8`
  - `05-dichotomy.tex` `ef0ff02ce80fe4351eb84b1f5db0ea2fce0085030f0ee30eea64f6dbec1f26ae`
  - `06-perturbation.tex` `863d06426a7f4b24386e39172c1b5b243ff7587179895befd68aa8ff11c38774`
  - `07-transfers.tex` `4d54ebb5b4605ad42c2111b5d4d723ac010cacd76da1bc04c581c5a04b04502d`

Credits: the construction and every lemma quoted from it are OpenAI's. The
three changes of §4–5 (shorter dilation, `(1/2−ε)` balance, light positions
outside heavy blocks) are Rohan Arun's (`sharpened-region-proof.md`, merged
PR #2), as is the two-point lemma. Lemmas 4 and 7, the third local-lemma
family and the two-case non-rich estimate are `DaysSky`'s
(`short-period-runs-proof.md`, PR #7). Repairs M1 and M2 come from the
2026-10-20 independent audit of that note. What is new here is the complete
write-up of these arguments as one proof from the source alone, and the
observation that the source's own rich estimate, with multiplicity two, is
enough below `1/16`, so that the rich-event chain of PRs #4, #6 and #7 is not
needed there.

AI assistance: the proof write-up, the verifier and this text were prepared
with Claude (Anthropic), one session among several Claude sessions working on
this repository. Not reviewed by a human.
