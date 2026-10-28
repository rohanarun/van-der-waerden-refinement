"""Checks for 'Lean: the finite core of the key-measurable reduction'.

Standard library only.  Run:  python3 -B verify.py   (exit 0 = all checks pass;
the JSON summary must equal RESULT.json; --write regenerates it).

Only `lake build` proves anything.  This script does not run Lean: it checks
that the recorded evidence belongs to the sources in the package, and that the
definitions say what the note means.  To rebuild and re-record the evidence:
lean/record-evidence.sh (lake build, then #print axioms, then the source
fingerprints, in one pass).

  1. evidence/sources.sha256, written by record-evidence.sh with the build and
     the audit, matches every Lean source in the package: evidence whose
     recorded fingerprints differ from the sources is refused.  The
     fingerprints are a declaration: recomputed by hand, they pass, so this
     catches a stale record, not a forged one.  Then a lint,
     not a proof: the sources contain no sorry, admit, axiom declaration,
     native_decide, implemented_by or extern outside comments (a regex,
     which nested comments or strings can fool; #print axioms is the check
     that counts), and pin Lean 4.21.0 and Mathlib v4.21.0.
  2. evidence/axioms.txt (#print axioms on every constant of the namespace)
     lists exactly the announced count, every constant depends only on
     propext, Classical.choice and Quot.sound, and the named statements are
     among them, including the kernel-checked counts |kAPs 6 3| = 8 and
     |kAPs 7 3| = 21 and the degenerate lengths.
  3. evidence/build.txt records a build of KeyMeasurable.
  4. A hand transcription of the Lean definitions (member, final, weight,
     probGood, Good), replayed by exhaustive enumeration in exact rationals on
     random toys, including an empty family, an empty set and one-point sets:
     weight_sum, probGood_pos_iff, fixed_iff (p in {1/5, 1/2}),
     method_iff_class (both outcomes must occur), mono_iff.  It tests the
     transcription, not the Lean terms, which are noncomputable.
  5. Proposition 2 on the same kind of toys (same transcription): rich_alone;
     mono_iff_presc; card_bad_le (at most T * 2^(|K| - m) failing Y, T the
     number of distinct prescriptions, m the least number of keys on a slow
     set), including families with an empty set (m = 0); slow_alone whenever
     T < 2^m, with cases where it applies.
"""
import hashlib
import json
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE / 'lean'
OUT = {}
FAIL = []


def check(ok, msg):
    if not ok:
        FAIL.append(msg)
        print('FAIL:', msg)


# 1. Sources: the recorded fingerprints must match them (a declaration, not a proof)
recorded = {}
for line in (LEAN / 'evidence' / 'sources.sha256').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    recorded[name] = digest
LEAN_FILES = ['KeyMeasurable.lean', 'KeyMeasurable/Basic.lean', 'Axioms.lean', 'lakefile.toml',
              'lean-toolchain', 'lake-manifest.json']
check(sorted(recorded) == sorted(LEAN_FILES), 'sources.sha256 lists other files')
for name in LEAN_FILES:
    check(hashlib.sha256((LEAN / name).read_bytes()).hexdigest() == recorded.get(name),
          f'{name} differs from the sources that produced evidence/: rerun record-evidence.sh')
check('"name": "key_measurable"' in (LEAN / 'lake-manifest.json').read_text(), 'manifest name')
SOURCES = ['KeyMeasurable.lean', 'KeyMeasurable/Basic.lean', 'Axioms.lean']
FORBIDDEN = ['sorry', 'admit', 'native_decide', 'implemented_by', 'extern']
for name in SOURCES:
    text = (LEAN / name).read_text()
    code = re.sub(r'/-.*?-/', '', text, flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    for w in FORBIDDEN:
        check(re.search(r'\b' + w + r'\b', code) is None, f'{name} contains {w}')
    check(re.search(r'^\s*axiom\b', code, flags=re.M) is None, f'{name} declares an axiom')
check((LEAN / 'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.21.0', 'toolchain')
check('rev = "v4.21.0"' in (LEAN / 'lakefile.toml').read_text(), 'mathlib pin')
print(f'1. sources: evidence recorded from these {len(LEAN_FILES)} files; lint clean '
      '(no sorry/admit/axiom/native_decide/implemented_by/extern)')

# 2. Axioms
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
lines = (LEAN / 'evidence' / 'axioms.txt').read_text()
announced = int(re.match(r'(\d+) constants', lines).group(1))
entries = re.findall(r"'([^']+)' (depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", lines)
check(len(entries) == announced, 'axioms.txt count')
used = set()
for name, _, axs in entries:
    check(name.startswith('KeyMeasurable.'), f'foreign constant {name}')
    ax = {a.strip() for a in axs.replace('\n', ' ').split(',') if a.strip()}
    check(ax <= STANDARD, f'{name} uses {ax - STANDARD}')
    used |= ax
MAIN = ['weight_sum', 'probGood_pos_iff', 'fixed_iff', 'method_iff_class', 'mono_iff',
        'method_iff_class_kAPs', 'rich_alone', 'mono_iff_presc', 'presc_union',
        'card_prescribed_le', 'card_bad_le', 'slow_alone', 'card_kAPs_6_3', 'card_kAPs_7_3',
        'kAPs_eq_empty_of_lt', 'kAPs_zero']
names = {n for n, _, _ in entries}
for m in MAIN:
    check('KeyMeasurable.' + m in names, f'{m} missing from the audit')
OUT['axioms'] = {'constants': announced, 'axioms_used': sorted(used), 'statements': MAIN}
print(f'2. axioms: {announced} constants, axioms used {sorted(used)}')

# 3. Build
build = (LEAN / 'evidence' / 'build.txt').read_text()
check('Built KeyMeasurable' in build and build.rstrip().endswith('Build completed successfully.'),
      'build.txt')
print('3. build: recorded (the proof is lake build itself, not this record)')


# 4. A hand transcription of the definitions of KeyMeasurable/Basic.lean:
#    member Y n = c0(L n) xor [kappa n in Y]
#    final X F n = c0(L n) xor ([kappa n in X] xor [kappa n in F])
#    weight X p F = p^|F| (1-p)^|X^c \ F|,  probGood = sum over F subset X^c.
def subsets(s):
    s = sorted(s)
    for mask in range(1 << len(s)):
        yield frozenset(x for i, x in enumerate(s) if mask >> i & 1)


def good(fam, f):
    return all(any(f[x] != beta for x in P) for P in fam for beta in (0, 1))


def toy(rng, nv, nk, nl, nfam, size):
    V = range(nv)
    L = [rng.randrange(nl) for _ in V]
    kap = [rng.randrange(nk) for _ in V]
    c0 = [rng.randrange(2) for _ in range(nl)]
    fam = [frozenset(rng.sample(V, size)) for _ in range(nfam)]
    return V, L, kap, c0, fam, range(nk)


def member(V, L, kap, c0, Y):
    return [c0[L[n]] ^ (kap[n] in Y) for n in V]


def final(V, L, kap, c0, X, F):
    return [c0[L[n]] ^ ((kap[n] in X) ^ (kap[n] in F)) for n in V]


def weight(K, X, p, F):
    free = set(K) - X
    return p ** len(F) * (1 - p) ** len(free - F)


rng = random.Random(20261027)
count = {'toys': 0, 'empty_family': 0, 'with_empty_set': 0, 'with_one_point_set': 0,
         'fixed_cases': 0, 'mono_cases': 0, 'class_good': 0, 'class_bad': 0}
for t in range(60):
    V, L, kap, c0, fam, K = toy(rng, nv=9, nk=5, nl=3, nfam=rng.randrange(4, 14), size=3)
    if t % 10 == 0:
        fam = []
        count['empty_family'] += 1
    elif t % 10 == 1:
        fam = fam + [frozenset()]
        count['with_empty_set'] += 1
    elif t % 10 == 2:
        fam = fam + [frozenset([rng.randrange(9)])]
        count['with_one_point_set'] += 1
    count['toys'] += 1
    class_good = any(good(fam, member(V, L, kap, c0, Y)) for Y in subsets(K))
    count['class_good' if class_good else 'class_bad'] += 1
    some_success = False
    for X in subsets(K):
        free = set(K) - X
        for p in (Fraction(1, 5), Fraction(1, 2)):
            ws = {F: weight(K, X, p, F) for F in subsets(free)}
            check(sum(ws.values()) == 1, 'weight_sum')
            prob = sum(w for F, w in ws.items() if good(fam, final(V, L, kap, c0, X, F)))
            some_F = any(good(fam, final(V, L, kap, c0, X, F)) for F in ws)
            some_Y = any(X <= Y and good(fam, member(V, L, kap, c0, Y)) for Y in subsets(K))
            check((prob > 0) == some_F, 'probGood_pos_iff')
            check((prob > 0) == some_Y, 'fixed_iff')
            some_success |= prob > 0
            count['fixed_cases'] += 1
    check(some_success == class_good, 'method_iff_class')
    for Y in subsets(K):
        f = member(V, L, kap, c0, Y)
        for P in fam:
            for beta in (0, 1):
                mono = all(f[x] == beta for x in P)
                inY = {x for x in P if kap[x] in Y}
                cls = {x for x in P if c0[L[x]] != beta}
                check(mono == (inY == cls), 'mono_iff')
                count['mono_cases'] += 1
check(count['class_good'] > 0 and count['class_bad'] > 0, 'both outcomes must occur')
OUT['toys'] = count
print(f"4. toys: {count['toys']} toys ({count['class_good']} with a good member, "
      f"{count['class_bad']} without), {count['fixed_cases']} (X, p) cases, "
      f"{count['mono_cases']} mono_iff cases")


# 5. Proposition 2.  presc P beta = (kappa(P ∩ {c0 != beta}), kappa(P ∩ {c0 = beta})).
def presc(L, kap, c0, P, beta):
    return (frozenset(kap[x] for x in P if c0[L[x]] != beta),
            frozenset(kap[x] for x in P if c0[L[x]] == beta))


rng = random.Random(271027)
p2 = {'toys': 0, 'rich_hypothesis_holds': 0, 'empty_family': 0, 'with_empty_set': 0, 'with_one_point_set': 0, 'bound_cases': 0, 'slow_alone_applies': 0, 'tight': 0}
for t in range(200):
    nk = rng.randrange(3, 8)
    V, L, kap, c0, fam, K = toy(rng, nv=10, nk=nk, nl=3, nfam=rng.randrange(1, 6),
                                size=rng.randrange(2, 6))
    if t % 7 == 0:
        fam = fam + [frozenset()]
        p2['with_empty_set'] += 1
    elif t % 7 == 1:
        fam = fam + [frozenset([t % 10])]
        p2['with_one_point_set'] += 1
    elif t % 7 == 2 and t % 3 == 0:
        fam = []
        p2['empty_family'] += 1
    p2['toys'] += 1
    # rich_alone
    if good(fam, [c0[L[n]] for n in V]):
        p2['rich_hypothesis_holds'] += 1
        check(good(fam, member(V, L, kap, c0, frozenset())), 'rich_alone')
    # mono_iff_presc
    for Y in subsets(K):
        f = member(V, L, kap, c0, Y)
        for P in fam:
            for beta in (0, 1):
                a, b = presc(L, kap, c0, P, beta)
                check(all(f[x] == beta for x in P) == (a <= Y and not (b & Y)), 'mono_iff_presc')
                check(a | b == {kap[x] for x in P}, 'presc_union')
    # hm is vacuous on an empty family: any m is allowed, take 3.
    m = min((len({kap[x] for x in P}) for P in fam), default=3)
    T = len({presc(L, kap, c0, P, beta) for P in fam for beta in (0, 1)})
    bad = sum(1 for Y in subsets(K) if not good(fam, member(V, L, kap, c0, Y)))
    check(bad <= T * 2 ** (len(K) - m), 'card_bad_le')
    p2['bound_cases'] += 1
    p2['tight'] += bad == T * 2 ** (len(K) - m)
    if T < 2 ** m:
        p2['slow_alone_applies'] += 1
        check(bad < 2 ** len(K), 'slow_alone')
check(p2['slow_alone_applies'] > 0, 'slow_alone never applies on the toys')
OUT['proposition_2'] = p2
print(f"5. Proposition 2: {p2['toys']} toys ({p2['with_empty_set']} with an empty set, m = 0; "
      f"{p2['with_one_point_set']} with a one-point set; {p2['empty_family']} empty families), "
      f"card_bad_le on all, slow_alone applies on {p2['slow_alone_applies']}, "
      f"bound attained on {p2['tight']}")

out = json.dumps(OUT, indent=2, sort_keys=True) + '\n'
res = HERE / 'RESULT.json'
if '--write' in sys.argv:
    if not FAIL:
        res.write_text(out)
elif not res.exists() or res.read_text() != out:
    check(False, 'RESULT.json differs from the computed summary')
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    raise SystemExit(1)
print('Test passé : all checks pass')
