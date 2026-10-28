#!/usr/bin/env python3
"""Checks for the dangerous-traces scoping note (README.md). Not a formal proof.

Standard library only, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0, last line "Test passé : all checks pass", and a JSON summary equal to RESULT.json.
"""
import hashlib
import json
import math
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
RNG = random.Random(20261027)
AP_FREE = HERE.parent / "2026-10-26-ChaloupeMusic-ap-free-frozen-sets" / "RESULT.json"


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def check_proposition1(trials=4000):
    """Positions 0..k-1 dealt into rows of size M (the light part) and blocks of size h (the heavy part).
    Dangerous: some row with >= eps M/4 points of X_P, or some block with >= eps h/8. Row-sparse means
    no dangerous row or block; then |X_P| < eps k."""
    eps = Fr(1, 2)
    seen_dangerous = seen_sparse = 0
    for _ in range(trials):
        M = RNG.randrange(4, 12)
        h = RNG.randrange(4, 12)
        nrows = RNG.randrange(1, 5)
        nblocks = RNG.randrange(0, 4)
        k = nrows * M + nblocks * h
        dens = RNG.choice([Fr(1, 20), Fr(1, 8), Fr(1, 4), Fr(1, 2)])
        X = [RNG.random() < dens for _ in range(k)]
        rows = [X[i * M:(i + 1) * M] for i in range(nrows)]
        blocks = [X[nrows * M + i * h: nrows * M + (i + 1) * h] for i in range(nblocks)]
        dangerous = any(sum(r) >= eps * M / 4 for r in rows) or any(sum(b) >= eps * h / 8 for b in blocks)
        row_sparse = all(sum(r) < eps * M / 4 for r in rows) and all(sum(b) < eps * h / 8 for b in blocks)
        require(dangerous == (not row_sparse), "dangerous iff not row-sparse")
        if row_sparse:
            require(sum(X) < eps * k, "row-sparse traces have |X_P| < eps k")
            seen_sparse += 1
        else:
            seen_dangerous += 1
    require(seen_sparse > 100 and seen_dangerous > 100, "both cases exercised")
    return {"trials": trials, "row_sparse": seen_sparse, "dangerous": seen_dangerous}


def check_scales():
    pts = json.loads(AP_FREE.read_text())["numerics"]
    rows, control_fails = {}, False
    for name in sorted(pts):
        if "a=" not in name:
            continue
        kexp = int(name.split("k=2^")[1].split(",")[0])
        a = float(name.split("a=")[1].split(",")[0])
        c = float(Fr(name.split("c=")[1]))
        log2k = kexp
        log2lnk = math.log2(kexp * math.log(2))
        log2D = a * log2k
        m = (2 * a + 1) / 2                                   # midway between 2a and 1
        log2M = m * log2k
        log2_lnq = math.log2(c) + log2k + log2lnk - log2D     # ln q = c k ln k / D
        log2_Dlnq = log2D + log2_lnq                          # = log2(c k ln k)
        require(log2D < log2M < log2k < log2_Dlnq, f"scale order at {name}")
        require(log2D + log2lnk < log2M, f"D log k << M at {name}")
        rows[name] = {"log2_D": round(log2D, 1), "log2_M": round(log2M, 1), "log2_k": log2k,
                      "log2_D_ln_q": round(log2_Dlnq, 1)}
        if not (log2D + log2lnk < a * log2k):                 # control: with m = a, M = D, and D log k << M fails
            control_fails = True
    require(len(rows) >= 15, "too few template points")
    require(control_fails, "control: m = a does not break D log k << M")
    return rows


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {"proposition1": check_proposition1(), "scales": check_scales(), "integrity_files": integrity()}
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(text)
    stored = HERE / "RESULT.json"
    if "--write" in sys.argv:
        stored.write_text(text)
    else:
        require(stored.read_text() == text, "output differs from RESULT.json")
    print("Test passé : all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
