"""Independent finite-certificate verifier (does not import search code)."""
import argparse,json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

def check(data):
    faces=[set(f) for f in data['faces']];n=data['points'];F=len(faces)
    assert all(len(f)==3 for f in faces)
    assert len({tuple(sorted(f)) for f in faces})==F
    assert set().union(*faces)==set(range(n)) and F>n
    pairs=defaultdict(list)
    for j,f in enumerate(faces):
        for e in combinations(sorted(f),2):pairs[e].append(j)
    assert all(len(js)==2 for js in pairs.values())
    dual=[set() for _ in faces]
    for js in pairs.values():
        a,b=js;dual[a].add(b);dual[b].add(a)
    seen={0};todo=[0]
    while todo:
        j=todo.pop()
        for k in dual[j]-seen:seen.add(k);todo.append(k)
    assert len(seen)==F
    weights=[Q(c.get('weight',str(Q(1,len(data['cuts']))))) for c in data['cuts']]
    assert all(w>0 for w in weights) and sum(weights)==1
    coverage=Counter()
    for w,cut in zip(weights,data['cuts']):
        sides=cut['orders'];assert len(sides)==2
        assert set(sides[0]).isdisjoint(sides[1])
        assert set(sides[0])|set(sides[1])==set(range(F))
        for order in sides:
            assert len(order)==len(set(order))==n-2
            seen=set(faces[order[0]]);old=[order[0]]
            for j in order[1:]:
                assert len(faces[j]-seen)==1
                assert any(len(faces[j]&faces[k])==2 for k in old)
                seen|=faces[j];old.append(j)
            assert seen==set(range(n))
        left=set(sides[0])
        for e,(j,k) in pairs.items():
            if (j in left)!=(k in left):coverage[e]+=w
    assert all(coverage[e]>=Q(1,3) for e in pairs)
    assert any(coverage[e]>Q(1,3) for e in pairs)
    adj=[[] for _ in range(n+F)]
    for j,f in enumerate(faces):
        for v in f:adj[v].append(n+j);adj[n+j].append(v)
    labels=[0]*n+[1]*F
    for _ in range(n+F):
        sig=[(labels[v],tuple(sorted(labels[w] for w in adj[v]))) for v in range(n+F)]
        uniq={x:i for i,x in enumerate(sorted(set(sig)))};new=[uniq[x] for x in sig]
        if len(set(new))==len(set(labels)):break
        labels=new
    assert len(set(labels))==n+F
    # Independently verify the identity-type support intersection used by
    # the generic kernel argument, beyond the search's four properties.
    corners={(i,j) for j,f in enumerate(faces) for i in f}
    U={e:{(i,j) for i in e for j in js} for e,js in pairs.items()}
    M={corner:set().union(*(u for u in U.values() if corner in u)) for corner in corners}
    for e,u in U.items():
        assert set.intersection(*(M[c] for c in u))==u
    for i,j in corners:
        incident=[U[e] for e in pairs if i in e and set(e)<=faces[j]]
        assert len(incident)==2 and incident[0]&incident[1]=={(i,j)}
        assert len(M[i,j])==7
    return {'vertices':n+F,'edges':3*F,'cuts':len(weights),'min_pair_coverage':str(min(coverage.values())),'support_intersections':'passed','discrete_refinement':'passed'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificates',nargs='+');p.add_argument('--output',required=True);a=p.parse_args()
    results=[]
    for name in a.certificates:
        d=json.loads(Path(name).read_text());results.append(dict(file=name,certificate=check(d)))
        broken=json.loads(json.dumps(d));broken['faces'][0]=broken['faces'][1]
        try:check(broken)
        except AssertionError:pass
        else:raise AssertionError('Duplicate-face mutation was accepted')
        broken=json.loads(json.dumps(d));broken['cuts'][0]['orders'][0].pop()
        try:check(broken)
        except AssertionError:pass
        else:raise AssertionError('Incomplete-exposure mutation was accepted')
    Path(a.output).write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
