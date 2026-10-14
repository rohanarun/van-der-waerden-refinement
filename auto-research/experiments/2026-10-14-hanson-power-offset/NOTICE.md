# Sources, attribution, and assistance

Prepared for Hanson Sun by OpenAI Codex during the Auto Research sprint on
2026-10-14. Substantial AI assistance includes the mathematical derivation,
proof prose, verifier implementation, and packaging. The run began on the
previous launcher model and continued after the user switched to Astra Max.
No independent human mathematical review or kernel checking is claimed.
The authenticated GitHub submission account is `bbMisk`.

The direct predecessor is Rohan Arun's abstract profile in the section
"An obstruction for the matrix profile inequalities" of `research-note.tex`,
repository `rohanarun/van-der-waerden-refinement`, pinned at
`63bef9ca996786a41169de4a0c3d6b3b47b0fe96`. The endpoint here is exactly that
profile; no discovery or novelty claim is made for it. The base source
already discloses Codex assistance. `audit_math.py` and
`experiments/matrix-profile.json` provide predecessor finite checks and LP
experiments; this verifier does not import their implementations.

The repository attributes the scalar constraints to OpenAI's *An Upper Bound
of 9/4 for the Matrix Multiplication Exponent*, in `openai/math` at
`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Its pinned paper path is
`preprints/Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex`,
with SHA-256
`c396f2580a711b8b9e51ecf1265cb0e691acd745943f81bfc14ec0df209e1028`.
This contribution proves a statement about the selected scalar constraints
as explicitly transcribed in the base repository; it does not re-audit their
association with tensor characters or the upstream manuscript's theorem.
No upstream tree or manuscript is modified or bundled.

The van der Waerden context retains the credit to OpenAI, Rohan Arun,
Artus Krohn-Grimberghe (`artuskg`, repeated-key cover), and `DaysSky`
(rank-split, digit-rank, and short-period work, with disclosed Claude assistance).
The current open PRs #9 and #10 were inspected for overlap. Their effective
construction and selected formal/source review results are not premises of
this matrix-profile proof. The reviewed heads are recorded in `SOURCES.json`.

`SOURCES.json` pins every consumed local base file by SHA-256. No license file
was found in the base checkout. Existing notices and attribution are retained;
this addition does not relicense predecessor material. No literature-priority,
maintainer-acceptance, or independent-review claim is made.
