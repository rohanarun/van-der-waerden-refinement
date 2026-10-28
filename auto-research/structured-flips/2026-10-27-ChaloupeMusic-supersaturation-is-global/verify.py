#!/usr/bin/env python3
"""Checks for 'supersaturation is global' (README.md). Not a formal proof.

Standard library only, exact rationals, no network. Run from anywhere:

    python3 -B verify.py

Exit code 0, last line "Test passé : all checks pass", and a JSON summary equal to RESULT.json.
"""
import hashlib
import itertools
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


# 1. per-progression bound under a uniform Y
def check_per_progression():
    cases = 0
    for _ in range(300):
        k = RNG.randrange(3, 9)
        nkeys = RNG.randrange(max(1, (k + 1) // 2), 7)
        keys = []
        while len(keys) < k:
            x = RNG.randrange(nkeys)
            if keys.count(x) < 2:
                keys.append(x)
        cols = [RNG.randrange(2) for _ in range(k)]
        used = sorted(set(keys))
        require(len(used) * 2 >= k, "at least k/2 distinct keys")
        for beta in (0, 1):
            target = {i for i in range(k) if cols[i] != beta}            # Y_P must equal this set
            hits = 0
            for bits in itertools.product((0, 1), repeat=len(used)):
                Y = {used[i] for i in range(len(used)) if bits[i]}
                if {i for i in range(k) if keys[i] in Y} == target:
                    hits += 1
            p = Fr(hits, 2 ** len(used))
            consistent = all(len({cols[i] for i in range(k) if keys[i] == x}) == 1 for x in used)
            require(p == (Fr(1, 2 ** len(used)) if consistent else 0), "exact induced-class probability")
            require(p <= Fr(1, 2) ** Fr(k, 2) if p else True, "bound 2^{-k/2}")
            cases += 1
    return cases


# 2. progressions inside a line of Z/N, N = q^D
def check_line_count():
    out = {}
    for q, D in ((3, 2), (5, 2), (3, 3), (7, 2)):
        N = q ** D
        step = q ** (D - 1)
        for r in range(min(N, 6)):
            line = {(r + step * m) % N for m in range(q)}
            count = 0
            for n0 in line:
                for d in range(N):
                    if all((n0 + j * d) % N in line for j in range(q)):
                        count += 1
            require(count == q * q, "q^2 progressions of length q inside a line")
        out[f"q={q},D={D}"] = q * q
    return out


# 3. scale comparison at the template points of ap-free-frozen-sets
def check_scales():
    pts = json.loads(AP_FREE.read_text())["numerics"]
    rows, n = {}, 0
    for name in sorted(pts):
        if "a=" not in name:
            continue
        kexp = int(name.split("k=2^")[1].split(",")[0])
        a = float(name.split("a=")[1].split(",")[0])
        c = Fr(name.split("c=")[1])
        lnk = kexp * math.log(2)
        k_log2 = kexp
        D_log2 = a * kexp                                                 # D = ceil(k^a), log2 up to 2^-300
        ln_q_log2 = math.log2(float(c)) + k_log2 + math.log2(lnk) - D_log2   # ln q = c k ln k / D
        lhs_log2 = 1 + ln_q_log2                                          # log2(2 ln q)
        rhs_log2 = k_log2 - 1 + math.log2(math.log(2))                    # log2((k/2) ln 2); the -3 is negligible
        margin = rhs_log2 - lhs_log2
        require(margin > 50, f"2 ln q not far below (k/2 - 3) ln 2 at {name}")
        require(abs(ln_q_log2 - pts[name]["ln_q_log2"]) < 1.0, f"ln q model disagrees with ap-free at {name}")
        rows[name] = round(margin, 1)
        n += 1
    require(n >= 15, "too few template points")
    return rows


# 4. a toy line: uniform colouring of Z/q without monochromatic k-AP
def check_toy_line(q=37, k=13):
    aps = set()
    for n0 in range(q):
        for d in range(1, q):
            aps.add(frozenset((n0 + j * d) % q for j in range(k)))
    expected = Fr(2 * len(aps), 2 ** k)
    require(expected < 1, "toy line: expected monochromatic APs below 1")
    for _ in range(200):
        col = [RNG.randrange(2) for _ in range(q)]
        if all(len({col[x] for x in ap}) == 2 for ap in aps):
            return {"q": q, "k": k, "aps": len(aps), "expected_mono": str(expected), "good_colouring_found": True}
    raise AssertionError("no good colouring found on the toy line")


# 5. negative controls
def negative_controls():
    rej = {}
    # bound in positions (2^{-k}) fails: k = 4 positions on 2 keys, induced class has probability 1/4 > 1/16
    keys, cols = [0, 0, 1, 1], [0, 0, 1, 1]
    target = {i for i in range(4) if cols[i] != 0}
    hits = sum(1 for bits in itertools.product((0, 1), repeat=2)
               if {i for i in range(4) if keys[i] in {j for j in range(2) if bits[j]}} == target)
    rej["bound_in_positions"] = Fr(hits, 4) > Fr(1, 2 ** 4)
    # forgetting d = 0 mod q^{D-1}: progressions that merely start on the line number q N, not q^2,
    # and most of them leave it
    q, D = 5, 2
    N, step = q ** D, q
    line = {(step * m) % N for m in range(q)}
    starts = sum(1 for n0 in line for d in range(N))
    leave = sum(1 for n0 in line for d in range(N) if any((n0 + j * d) % N not in line for j in range(q)))
    rej["line_count_without_step_condition"] = starts == q * N and leave == q * N - q * q and starts > q * q
    require(all(rej.values()), f"negative control not rejected: {rej}")
    return rej


def integrity():
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, digest in sorted(manifest.items()):
        if name == "RESULT.json":
            continue
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, f"hash mismatch: {name}")
    return sorted(name for name in manifest if name != "RESULT.json")


def main():
    report = {
        "per_progression_cases": check_per_progression(),
        "line_counts": check_line_count(),
        "scale_margin_log2": check_scales(),
        "toy_line": check_toy_line(),
        "negative_controls_rejected": negative_controls(),
        "integrity_files": integrity(),
    }
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
