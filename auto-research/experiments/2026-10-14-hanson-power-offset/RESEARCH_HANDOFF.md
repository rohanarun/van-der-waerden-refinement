# Research handoff — seed 46

The completed mathematical deliverable is a characterization of
`P_{lambda,s}(a,b)=((1+lambda)u-lambda)^s(v+lambda(u-1))`, `u=min(a,b)`,
`v=max(a,b)`, within `lambda,s>=0`. Separate discrete concavity and shifted
tripling hold exactly when `0<=lambda<=1/2` and
`s=(1-lambda)/(1+lambda)`. These profiles also satisfy the scalar rank envelope
with diagonal exponent `2/(1+lambda)`. Its unique minimum is the predecessor
profile's `4/3`; this two-parameter deformation gives no improvement.

The written argument proves a family-wide statement using two asymptotic
integer second-difference stencils for necessity and real derivatives for
sufficiency. The finite replay is supplementary evidence. Human mathematical
review, formal proof checking, tensor realizability, and literature priority
remain unestablished. No van der Waerden coefficient or main result is edited.

## Identity and instructions

- Base and fetched upstream main: `63bef9ca996786a41169de4a0c3d6b3b47b0fe96`.
- Branch: `research/seed46-profile-family` in the isolated local clone
  `/Volumes/Auto Research Workspace/Runtime/tmp/vdw-seed46-profile`.
- Assignment seed: `46`, drawn once with `secrets.randbelow(100)`; structural
  research. `CLAIM.json` records the three candidates and the selection.
- Exact entry point: the requested repository `auto-research.md`. The supplied
  Hanson operating defaults also apply. No additional on-disk AGENTS.md or
  contribution guide was found in the checked checkout/ancestor paths.
- Existing track: `auto-research/experiments/`; its README was absent, so an
  index is added. Existing top-level files and historical experiments are
  unchanged. No upstream source tree is written.
- The current conditional vdW proposal in the base is `1/9`, not the historical
  launch figure `1/25`. Its source chain and conditional status were inspected;
  they are not premises of the new matrix-family proposition.

## Reproduce and expected results

From the isolated clone or a checkout containing the contribution:

```sh
python3 -B auto-research/experiments/2026-10-14-hanson-power-offset/verify.py
```

Expect exit 0 and JSON equal to `RESULT.json`, with `status: "passed"`.
The command authenticates package and pinned base files, performs 2,160
concavity checks (960 certified by rational radical intervals, 1,200 exact
equalities), 2,304 tripling and 2,304 envelope checks across nine parameter
choices, and reconstructs 10,000 base-profile tripling and envelope pairs.
Four actual invalid profiles must fail their respective mathematical
constraints. The finite centers, additional evaluation points, seed-derived
offsets and stopping rule are fully recorded in `RESULT.json`.

Optional symbolic cross-check (SymPy 1.14.0):

```sh
python3 -B auto-research/experiments/2026-10-14-hanson-power-offset/check_identities.py
```

Expect six derivative/Taylor identities checked and `status: "passed"`.
This is algebra checking, not a formal proof of the inequalities or limits.

Repository baseline checks reproduced:

```sh
python3 -B audit_math.py
python3 -B check_complex.py experiments/complex-contractions/baseline.json --output experiments/baseline-independent-check.json
git diff --exit-code -- experiments/exact-audit.json experiments/baseline-independent-check.json
```

Both Python commands exited 0; saved baseline outputs remained byte-identical
to the base. The finite combinatorial baseline has 35 vertices, 66 edges and
three cuts. `VALIDATION.json` records command exit status and output hashes.
The supplied environment is Python 3.14.6, SymPy 1.14.0, NumPy 2.5.4 and
SciPy 1.18.1. The latter two versions differ from `requirements.txt`; this
local run is not a claim to have used the repository's exact dependency pins.
The contribution's primary verifier needs only the standard library.

The harness interpreter is
`/Volumes/Auto Research Workspace/venv/bin/python`; substitute that quoted
absolute path for `python3` to use the same local environment.

## Failures, recovery and lessons

1. The initial environment rejected `.git/FETCH_HEAD` writes, could not resolve
   GitHub, and lacked SymPy. No remote state or passing full audit was inferred.
   Work continued in an isolated local clone with a locally recorded claim.
2. Cloning on the original volume produced AppleDouble sidecars, including an
   invalid `._pack-*.idx` that Git tried to parse. Only generated sidecars in
   this run's own clone were removed. The original checkout was preserved.
3. The launcher switch interrupted the tool session. Its identifier was no
   longer active on resume. Saved work was inspected before proceeding; the
   mathematical scope and single OS assignment seed were retained.
4. The user migrated the preserved workspace to the current internal-storage
   mount, enabled network/Git writes, and supplied the Python environment.
   The volume and available space were checked, fetch succeeded, the base was
   unchanged, and the previously blocked baseline audit was reproduced.
5. `ps` remains denied, so a general inventory of concurrent processes is
   unavailable. No unrelated process was stopped or changed. Browser-based
   access was considered but not used; the restored GitHub CLI was sufficient.
6. The initial improvement hypothesis fails for a mathematical reason:
   tripling caps the offset, while the seam and interior discrete stencils
   force the power onto one curve. Enlarging the finite grid would not change
   this family-wide conclusion. A stronger result needs a different family or
   additional justified constraints, not another numerical scan of this one.

The two-parameter proof is the one completed research result. No speculative
coefficient, failed-search impossibility claim, or external acceptance record
is manufactured.

## Coordination and submission

After network restoration, the all-state GitHub issue list was empty, so no
coordination issue was available. Open PR #9 (`89660352...`) and PR #10
(`a46ef517...`) and the latter's conditional-review ledger were read; full
pins are in `SOURCES.json`. Their listed files concern the vdW construction
and selected formal reviews, with no overlap found with this matrix-family
work. These reviews are credited but are not mathematical dependencies.

Package validation is complete: a fresh copied package reproduces the saved
report normally and under `python3 -O`. Four package controls reject a changed
proof, an unlisted nested file, a false result with a recomputed manifest, and
a changed source pin. Receipts are in `VALIDATION.json`.

Submitted exactly one focused research-note PR: [#11](https://github.com/rohanarun/van-der-waerden-refinement/pull/11),
through `bbMisk:research/seed46-profile-family`. The local claim and track
index link the result. Local checks pass; remote checks and maintainer review
are separate. GitHub reported `action_required` with no job results for
[workflow run 38591677550](https://github.com/rohanarun/van-der-waerden-refinement/actions/runs/38591677550)
on submitted head `ee7a7cd22cbb56294ff635f17078abed02a0bc6b`. A remote CI pass
is not claimed; the workflow action and maintainer review remain external
obligations. No merge or maintainer acceptance is claimed.

For a mathematical reviewer, the principal obligations are the two scaled
integer-stencil limits and the `h<a` tripling reduction. The proof states its
parameter domain explicitly. Beyond review of this contribution, no additional
experiment is justified within the selected family.
