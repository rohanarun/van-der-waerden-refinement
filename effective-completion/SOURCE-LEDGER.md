# Attribution and exact source ledger

The coefficient and method claims in PR6/PR7 predate this completion. Credit OpenAI for the upstream construction, Rohan Arun and the base refinement for the two-point norm-band lemma and sharpened outer construction, Artus Krohn-Grimberghe for PR4's repeated-key precursor, and DaysSky (with Claude assistance) for PR6's carry split and PR7's matched digit rank and short-period method. OpenAI Pro produced the completed draft; Codex independently reconstructed it and prepared this proposal for Artus Krohn-Grimberghe. Do not attribute the coefficient range or methods as an independent discovery by this submission.

The exact public proposals are [PR4](https://github.com/rohanarun/van-der-waerden-refinement/pull/4), [PR6](https://github.com/rohanarun/van-der-waerden-refinement/pull/6), and [PR7](https://github.com/rohanarun/van-der-waerden-refinement/pull/7). Current public head status and novelty observations are version-bound preparation evidence; these immutable file URLs remain the proof's source references.

# Source ledger and proof dependencies

This ledger refers only to the supplied public snapshot and the two exact-pin P6 blob reads and the base sharpened-note read. The original source archive is retained in the immutable reviewed local packet. The public patch contains links and hashes, rather than redistributing that archive.

Original ZIP SHA-256: `6c15b2d207144ecb8be4c52ec8c4d622b2c749657ae9d45f7ece50e47487cee1`.

The original 46-entry `source_inventory` in `DEPENDENCIES.json` is retained from the manifest inside that ZIP; the additional authenticated base sharpened-region note is listed separately. All 46 listed entries were recomputed and passed byte-size, SHA-256, and Git-blob checks; the twelve selected current/historical pairs are byte-identical. The preparation evidence independently matches all 46 retained exact-pin API responses and the manifest; the proof depends on the analytic arguments, not these checks. These are consistency checks against the supplied manifest, not a claim to have independently re-fetched every remote repository path.

## Proof-to-source map

Paths in this table are relative to the `vdw-public-source/` directory in the preserved source snapshot. Exact repository/commit/blob/URL information for each path follows in the inventory. Each mathematical ingredient marked proved is proved in `PROOF.md`, not assumed because a repository contains it.

| Definition or theorem | Completion | Source files | Treatment |
|---|---|---|---|
| Definitions, scope, headline not used as a black box | PROOF 1–3 | upstream/README.md; upstream/build/sections/01-introduction.tex; base/README.md | Scope/attribution only; report proves stronger coefficient independently |
| Exact prime, prime-power, coordinate, dilation, mesh, label and key definitions | PROOF 3–4,14 | upstream/build/sections/02-setup.tex; base/research-note.tex §4; base/sharpened-region-proof.md (origin); pr7/sharpened-region-proof.md (fork-inherited copy) | Literal conventions retained; explicit small-primary, prime and algebraic-decision proofs supplied |
| Affinity and separation | PROOF 5.1,7.1 | upstream/build/sections/02-setup.tex; upstream/build/sections/05-dichotomy.tex | Proved from integer torus relations and base-q divisibility |
| Sign arrangements and global/anchored words | PROOF 4.2–4.3 | upstream/build/sections/03-counting.tex; base/research-note.tex §4; base/sharpened-region-proof.md; pr7/sharpened-region-proof.md (inherited copy) | All faces counted, explicit constants; exact feasibility specified in PROOF 14 |
| First and second global outer families | PROOF 6 | upstream/build/sections/04-outer.tex; base/research-note.tex §4; base/sharpened-region-proof.md; pr7/sharpened-region-proof.md (inherited copy) | Proved with deterministic rows, actual word choices, supports and cross-family weights |
| Heavy-return path, regular long blocks, short affine path | PROOF 5,6.3 | upstream/build/sections/05-dichotomy.tex; base/research-note.tex §4; base/sharpened-region-proof.md; pr7/sharpened-region-proof.md (inherited copy) | Cut equalities and changed scales proved explicitly |
| Two-point norm-band improvement | PROOF 7.1 | base/research-note.tex; pr6/research-note.tex; pr7/research-note.tex | Proved for literal half-open bands; closed-band negative control separated |
| Repeated boxes, common return, collision classes, carries, anchored identity | PROOF 7,10 | pr4/repeated-key-certificate-proof.md; pr7/rank-certificate-proof.md | P4 attribution retained; deterministic repeated-pair data explicitly encoded |
| PR6 projection certificate A, anchored B, progression count C and carry-rank split | PROOF 10 | pr7/rank-certificate-proof.md; pr6/parameters.json | Included blob independently checked at P6 exact pin; finite bounds proved |
| Balanced start digits, return digits, matched rank R and dual counts | PROOF 8–9 | pr7/digit-rank-proof.md; pr7/rank-certificate-proof.md | Certificate entropy R log q and progression entropy (2D-R) log q proved with finite multiplicities |
| Single-run property and third outer family | PROOF 5.4,6 | pr7/short-period-runs-proof.md | Small-interval lift repair; abstract indexing vs actual-run quantifiers kept distinct |
| Many-light-key cover and heavy-run prescription code | PROOF 11 | pr7/short-period-runs-proof.md | No hidden full-label-word entropy; repeated-key consistency checked |
| Original shared-key perturbation and affine signature framework | PROOF 9–11 | upstream/build/sections/06-perturbation.tex; pr6/research-note.tex | Source probability claims re-proved; no source headline theorem assumed |
| Literal explicit parameters and margin audit context | PROOF 3,12 | pr6/parameters.json; pr7/parameters.json; pr6/audit_math.py; pr7/audit_math.py | Data/claims inspected; repository code NOT run and its logs not accepted as proof |
| Digit product, exact interval length, nonzero cyclic digit step | PROOF 13 | upstream/build/sections/07-transfers.tex | Full carry-safe proof supplied; finite primitive products independently validated |
| Explicit effective threshold, exact event enumeration, the DIRECT search bound, and supplementary structured cost estimates | PROOF 12,14–16 | All preceding definitions; no new external source | New completion here: exact rational acceptance checklist, algebraic decisions, finite exhaustive algorithms |
| Reference notation and bibliographic attribution | PROOF 2 and this ledger | upstream/build/preamble.tex; upstream/build/paper.tex; upstream/build/references.bib | No extra theorem imported from the bibliography |
| Material outside the requested proof | Not a dependency | upstream/build/sections/08-upper.tex; unrelated matrix sections in research-note/README/audit files | Integrity checked as included bytes; not used to prove the lower-bound construction |

## Two additional exact-pin reads

The snapshot contains the rank and sharpened proofs under the PR7 directory. To check their membership at PR6 without changing revisions, the following files were read using the public GitHub connector, with the explicitly specified PR6 commit. Both returned the same blob as the already included PR7 copy. No new mathematical source bytes or later revisions were introduced.

### `rank-certificate-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`. Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`. Git blob: `33acb0fec1f3c64a27ec60eb60e1be24b7876f89`. SHA-256 of the matching included bytes: `de3c52b38914cfafd37943626382583d55983737e1dd5c921d568154ece182d0`. Byte size: 19154.

Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/rank-certificate-proof.md

### `sharpened-region-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`. Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`. Git blob: `7bf21638c2d8ca50e3cd47a6289931f0d45bd80f`. SHA-256 of the matching included bytes: `daf7302d0a5c1efc0334c6c908a57356863ccf8b18bd1ffcf92b1ac55c321640`. Byte size: 9052.

Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/sharpened-region-proof.md

## Full supplied inventory

The manifest's exact public URL is reproduced for each file. The file hashes below were independently recomputed from the accepted frozen bytes and matched to all 46 retained exact-pin API responses by a newly authored read-only provenance capture. Source programs and stored source audit results were not executed or trusted as proofs.

### 1. `base/README.md`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `54ac9715fceab938ca77d5980c36ab691765a04d`  
Git blob: `fb05b554e8ff4cc7cd62995c7c6fef29e7ee55e2`  
SHA-256: `cd41154d35978d0d9f5a428750547f0919870e72e35086eb44d5680d825cde14`  
Bytes: 12795  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/54ac9715fceab938ca77d5980c36ab691765a04d/README.md

### 2. `base/audit_math.py`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `54ac9715fceab938ca77d5980c36ab691765a04d`  
Git blob: `f90c85cfd6c0216c25001a713ab32cec577f78c7`  
SHA-256: `5cc95e010e54a75e92ae1715694a624436b413c70febbb8f08a1f4b7c3a21aeb`  
Bytes: 5645  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/54ac9715fceab938ca77d5980c36ab691765a04d/audit_math.py

### 3. `base/experiments/exact-audit.json`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `54ac9715fceab938ca77d5980c36ab691765a04d`  
Git blob: `91e57965df8eedcc764856cb0503b892a73c2a59`  
SHA-256: `917ac588397e9ca1098c8fbccc18d01f16f2ca4ffab6a7a68dfbfdb7b9f9b075`  
Bytes: 3434  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/54ac9715fceab938ca77d5980c36ab691765a04d/experiments/exact-audit.json

### 4. `base/parameters.json`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `54ac9715fceab938ca77d5980c36ab691765a04d`  
Git blob: `67619d9092e0d0b620b588b09d6a87b12876eda3`  
SHA-256: `5d7cc3391820ed4d9ef7b608d0ab574197f2f35b5069b5eba68b645d97f449a2`  
Bytes: 990  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/54ac9715fceab938ca77d5980c36ab691765a04d/parameters.json

### 5. `base/research-note.tex`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `54ac9715fceab938ca77d5980c36ab691765a04d`  
Git blob: `f6ac989e0318fa4d2608ffa724b3bb9df91b2951`  
SHA-256: `700a23a04b9ac5845fd961366c02fcf781c57334bd1af28a99b41130d28172c2`  
Bytes: 17623  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/54ac9715fceab938ca77d5980c36ab691765a04d/research-note.tex

### 6. `historical/README.md`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `32689475d88dc169e0a28c90532cbe84caa164da`  
SHA-256: `d34c41dfe21e93e2ad5c5c802e2dd809e8d65eec849c9858c81a960258546620`  
Bytes: 680  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/README.md

### 7. `historical/build/paper.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `b9197f584551b7458ffc72fe00a610a2a8113569`  
SHA-256: `da801dbc42e8f2812da79dd74674ec5a343848a8d65c3481dc1f9644650b7154`  
Bytes: 867  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/paper.tex

### 8. `historical/build/preamble.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `6bd53f90835bf2f79ecbb639758c4df75a6e4e8b`  
SHA-256: `10b77be7b67b3de4cb4f0576645082fd7c7b074026465339303f282c060bd3e9`  
Bytes: 3640  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/preamble.tex

### 9. `historical/build/references.bib`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `2f7931297905abfd0a56ba7df608349df100c12e`  
SHA-256: `54e3f84edfa2b73177731d818d6fa596a9b0143dae79bd6eb99e82563bbd8a98`  
Bytes: 8939  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/references.bib

### 10. `historical/build/sections/01-introduction.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `af53ecac8dfaf2fa0870f25010400f9ed8c22a91`  
SHA-256: `d9df34764dab48d839cd4e8bdf612d167a9fd92e2a243e08c4e50016ffee1f80`  
Bytes: 9296  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/01-introduction.tex

### 11. `historical/build/sections/02-setup.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `e70440abe7732dcd97e47c3fa4cadc1a5b936783`  
SHA-256: `9ba2817eda5b94221c4f05ba59835bef53760fbffe7eda896228b323b7cb3beb`  
Bytes: 10472  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/02-setup.tex

### 12. `historical/build/sections/03-counting.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `45e527fa7f77423d0f3f64903009d204ff69ea3b`  
SHA-256: `ca84ac51bf6c8539f2458bdc462c98ef465ea70afaa15496d0e6fcaec453c243`  
Bytes: 10130  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/03-counting.tex

### 13. `historical/build/sections/04-outer.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `8570fab8f40fb1c77dd06d3b4b83b00f711d3378`  
SHA-256: `e602972f1194c81ec780c4e17b8c5d3f94874db59f42dbfbc3008f9cec0d5ae8`  
Bytes: 7803  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/04-outer.tex

### 14. `historical/build/sections/05-dichotomy.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `a9617cbdf685aab18b3da5d08906bfd26b9c2e7f`  
SHA-256: `ef0ff02ce80fe4351eb84b1f5db0ea2fce0085030f0ee30eea64f6dbec1f26ae`  
Bytes: 12609  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/05-dichotomy.tex

### 15. `historical/build/sections/06-perturbation.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `9ca1771c317eef2f3e91b424da1c5052b6dc9a87`  
SHA-256: `863d06426a7f4b24386e39172c1b5b243ff7587179895befd68aa8ff11c38774`  
Bytes: 12112  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/06-perturbation.tex

### 16. `historical/build/sections/07-transfers.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `d6aa7b73f047b64a3ca53381801072a25627ae76`  
SHA-256: `4d54ebb5b4605ad42c2111b5d4d723ac010cacd76da1bc04c581c5a04b04502d`  
Bytes: 7486  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/07-transfers.tex

### 17. `historical/build/sections/08-upper.tex`

Repository: `openai/math`  
Commit: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`  
Git blob: `b162622f671a27eadaec38ef03bc03a107f1470f`  
SHA-256: `76d46da40c1d8cdef2b2f2b0efda291e8d9f2b73a401d3fb408828a40509cda3`  
Bytes: 5206  
Source: https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/08-upper.tex

### 18. `pr4/repeated-key-certificate-proof.md`

Repository: `rohanarun/van-der-waerden-refinement`  
Commit: `4b4e80ea5e0ffec956577004905f22659af0bff5`  
Git blob: `a9f40fafc1093347ae13bd94ef287a2788de9798`  
SHA-256: `6d07b2642b45c59d18fdcb35f53c612267979c74981ee56c59b452ef80033826`  
Bytes: 29762  
Source: https://github.com/rohanarun/van-der-waerden-refinement/blob/4b4e80ea5e0ffec956577004905f22659af0bff5/repeated-key-certificate-proof.md

### 19. `pr6/README.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`  
Git blob: `f04506c661a1798fc07b238a3f0b109339165851`  
SHA-256: `01064b9f43a92d5af08198705380617aef8884bd79c7a778861e0455323df39d`  
Bytes: 15858  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/README.md

### 20. `pr6/audit_math.py`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`  
Git blob: `caf908b886423379fb8a78b6dbbaa97e4aab3580`  
SHA-256: `8689461e1002d39a9a76f5b1d4463c021bcde5f9f34c38734a9bad68a73ad421`  
Bytes: 10150  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/audit_math.py

### 21. `pr6/experiments/exact-audit.json`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`  
Git blob: `bb3359398724864a71bc2907674723aab1da0986`  
SHA-256: `875b8c2b59bddaa56845bac5e1fdb3e52605856ae52495293466ce2fa8fd4e44`  
Bytes: 4477  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/experiments/exact-audit.json

### 22. `pr6/parameters.json`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`  
Git blob: `38e5075e57bc9fce714965eadcd3c3f4acc01e1c`  
SHA-256: `991754e403f84a3218efc714d6365e61aed6e05bb243d74f94a7c78848b2ad18`  
Bytes: 1254  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/parameters.json

### 23. `pr6/research-note.tex`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `fc5738bfda508566e7b4ce706c22bbb2b9194226`  
Git blob: `16dd8a5811aa9151469c5aecd5b5ac4f3108c3be`  
SHA-256: `dac64545bbf04dd19d3dd771c6e9ab2c88fdc8b3c900b616fba5e2a893101fbe`  
Bytes: 21519  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/fc5738bfda508566e7b4ce706c22bbb2b9194226/research-note.tex

### 24. `pr7/README.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `12509ef46f8ba63f0e375db7cef23caf6b947a6b`  
SHA-256: `96a3b42e1aa3e83d240fc4430a7fd8c4ee05d8404ef8074e130eff98dcf3b665`  
Bytes: 20962  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/README.md

### 25. `pr7/audit_math.py`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `b30cad23f70933c1e9a1d663c1b574762fb083b6`  
SHA-256: `11cb61afb8a5b5f1fd444f509d222edd2edc7ba230dcfc524f09d67cc3d9b1e6`  
Bytes: 16557  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/audit_math.py

### 26. `pr7/digit-rank-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `e490d7d160e05c5566d77ff3f1480e807046a449`  
SHA-256: `34be273ca19eafaa7546754714d67d29d3a1bd00797321bac81ceb42ad2fe42b`  
Bytes: 11394  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/digit-rank-proof.md

### 27. `pr7/experiments/exact-audit.json`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `37391157915c91bd2ab3b5a52dd102b79e13cf57`  
SHA-256: `9189b31b83b26a4add0b8fafdb1694642a5fd133c621a61f428d6c9d0f8d7b99`  
Bytes: 6588  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/experiments/exact-audit.json

### 28. `pr7/fetch_sources.py`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `6c332919516e6f3f7d1c1bf2fb6179322b25cd83`  
SHA-256: `498491054e8219050d5ce6cfc65c32920c4dc92d9da7253ec21a9be9401a2353`  
Bytes: 1960  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/fetch_sources.py

### 29. `pr7/parameters.json`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `a24e441a8b40e24f2826b7a7689b4c76664630b4`  
SHA-256: `c8dba118db2d9ead9bff3690c7d353c7c989c931a017146a6af8ddc5dbf97455`  
Bytes: 1802  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/parameters.json

### 30. `pr7/rank-certificate-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `33acb0fec1f3c64a27ec60eb60e1be24b7876f89`  
SHA-256: `de3c52b38914cfafd37943626382583d55983737e1dd5c921d568154ece182d0`  
Bytes: 19154  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/rank-certificate-proof.md

### 31. `pr7/research-note.tex`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `376a64647da3b1c90e605f4f413ab3a1788bb474`  
SHA-256: `611e53399c8d531bce63d6e4ec3841e3a6950193dcf3290712c4f45183a6f48c`  
Bytes: 27327  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/research-note.tex

### 32. `pr7/sharpened-region-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `7bf21638c2d8ca50e3cd47a6289931f0d45bd80f`  
SHA-256: `daf7302d0a5c1efc0334c6c908a57356863ccf8b18bd1ffcf92b1ac55c321640`  
Bytes: 9052  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/sharpened-region-proof.md

### 33. `pr7/short-period-runs-proof.md`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `84bfedb474b0095dbdf7d79ac8b07de3c48274bd`  
SHA-256: `dce39359d0fb1957d25c555871218a1f43414b12db325563644d8e07e345bdff`  
Bytes: 12223  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/short-period-runs-proof.md

### 34. `pr7/source-manifest.json`

Repository: `DaysSky/van-der-waerden-refinement`  
Commit: `987c96cfda59b65728ae4dcd5adc8a64ff95bab2`  
Git blob: `c336140d2c3407d1a231ee1949684cf827f53130`  
SHA-256: `e6dd98f5338eb7c981ed68afaca2b998c66f5c68397acccdb682c8d70a75e98c`  
Bytes: 8074  
Source: https://github.com/DaysSky/van-der-waerden-refinement/blob/987c96cfda59b65728ae4dcd5adc8a64ff95bab2/source-manifest.json

### 35. `upstream/README.md`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `32689475d88dc169e0a28c90532cbe84caa164da`  
SHA-256: `d34c41dfe21e93e2ad5c5c802e2dd809e8d65eec849c9858c81a960258546620`  
Bytes: 680  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/README.md

### 36. `upstream/build/paper.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `b9197f584551b7458ffc72fe00a610a2a8113569`  
SHA-256: `da801dbc42e8f2812da79dd74674ec5a343848a8d65c3481dc1f9644650b7154`  
Bytes: 867  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/paper.tex

### 37. `upstream/build/preamble.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `6bd53f90835bf2f79ecbb639758c4df75a6e4e8b`  
SHA-256: `10b77be7b67b3de4cb4f0576645082fd7c7b074026465339303f282c060bd3e9`  
Bytes: 3640  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/preamble.tex

### 38. `upstream/build/references.bib`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `2f7931297905abfd0a56ba7df608349df100c12e`  
SHA-256: `54e3f84edfa2b73177731d818d6fa596a9b0143dae79bd6eb99e82563bbd8a98`  
Bytes: 8939  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/references.bib

### 39. `upstream/build/sections/01-introduction.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `af53ecac8dfaf2fa0870f25010400f9ed8c22a91`  
SHA-256: `d9df34764dab48d839cd4e8bdf612d167a9fd92e2a243e08c4e50016ffee1f80`  
Bytes: 9296  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/01-introduction.tex

### 40. `upstream/build/sections/02-setup.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `e70440abe7732dcd97e47c3fa4cadc1a5b936783`  
SHA-256: `9ba2817eda5b94221c4f05ba59835bef53760fbffe7eda896228b323b7cb3beb`  
Bytes: 10472  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/02-setup.tex

### 41. `upstream/build/sections/03-counting.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `45e527fa7f77423d0f3f64903009d204ff69ea3b`  
SHA-256: `ca84ac51bf6c8539f2458bdc462c98ef465ea70afaa15496d0e6fcaec453c243`  
Bytes: 10130  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/03-counting.tex

### 42. `upstream/build/sections/04-outer.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `8570fab8f40fb1c77dd06d3b4b83b00f711d3378`  
SHA-256: `e602972f1194c81ec780c4e17b8c5d3f94874db59f42dbfbc3008f9cec0d5ae8`  
Bytes: 7803  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/04-outer.tex

### 43. `upstream/build/sections/05-dichotomy.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `a9617cbdf685aab18b3da5d08906bfd26b9c2e7f`  
SHA-256: `ef0ff02ce80fe4351eb84b1f5db0ea2fce0085030f0ee30eea64f6dbec1f26ae`  
Bytes: 12609  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/05-dichotomy.tex

### 44. `upstream/build/sections/06-perturbation.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `9ca1771c317eef2f3e91b424da1c5052b6dc9a87`  
SHA-256: `863d06426a7f4b24386e39172c1b5b243ff7587179895befd68aa8ff11c38774`  
Bytes: 12112  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/06-perturbation.tex

### 45. `upstream/build/sections/07-transfers.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `d6aa7b73f047b64a3ca53381801072a25627ae76`  
SHA-256: `4d54ebb5b4605ad42c2111b5d4d723ac010cacd76da1bc04c581c5a04b04502d`  
Bytes: 7486  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/07-transfers.tex

### 46. `upstream/build/sections/08-upper.tex`

Repository: `openai/math`  
Commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`  
Git blob: `b162622f671a27eadaec38ef03bc03a107f1470f`  
SHA-256: `76d46da40c1d8cdef2b2f2b0efda291e8d9f2b73a401d3fb408828a40509cda3`  
Bytes: 5206  
Source: https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Quantitative-Superexponential-Bounds-for-van-der-Waerden-Numbers-September-23-2026/build/sections/08-upper.tex

## Attribution and status

The upstream manuscript supplies the basic van der Waerden construction. The public P4 precursor supplies the repeated-key and anchored-certificate structure; its attribution to Artus Krohn-Grimberghe and the initial GPT-6 Pro argument is retained as stated in the public source. B supplies the two-point lemma and the sharpened outer construction. P6 supplies the carry-rank split; P7 supplies the matched digit rank and short-period-run refinement. This report supplies the explicit completion, boundary arguments, exact enumeration and threshold accounting presented in its proofs. It does not infer correctness from a pull request's publication, merge status, audit script, or numerical log.

No private review, earlier chat answer, unpublished material, matrix-multiplication argument, or source at a later revision is a dependency. The written all-size proof remains a mathematical proof rather than a formal proof-assistant certificate; finite replay results have their explicitly limited scope.

## Additional attribution authentication after Opus review

The base `sharpened-region-proof.md` at `54ac9715fceab938ca77d5980c36ab691765a04d` was fetched through the supported read-only GitHub API. Its 9,052 bytes hash to Git blob `7bf21638c2d8ca50e3cd47a6289931f0d45bd80f`, SHA-256 `daf7302d0a5c1efc0334c6c908a57356863ccf8b18bd1ffcf92b1ac55c321640`, identical to the inherited P6/P7 note. This confirms base-source credit; it does not identify an unsupported individual author. Structured resource envelopes remain supplementary estimates; the accepted exact DIRECT bound is distinguished.
