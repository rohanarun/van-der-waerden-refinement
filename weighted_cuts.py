"""Model proposal: replace three equal cuts by a rational cut distribution.

LP proposes weights; Fractions independently certify edge coverage >= 1/3.
Hits satisfy generalized finite hypotheses only, not the full theorem.
"""
import argparse,json,time,random
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from search_complex import structure,refinement,cuts,contractions,flips

parser=argparse.ArgumentParser();parser.add_argument('--baseline',required=True);parser.add_argument('--output',required=True);parser.add_argument('--seconds',type=float,required=True);parser.add_argument('--seed',type=int,required=True);args=parser.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
base=tuple(map(tuple,json.loads(Path(args.baseline).read_text())['faces']))
queue=list(contractions(base));seen=set(queue);rng=random.Random(args.seed);start=time.monotonic();counts={'tested':0,'discrete':0,'lp_feasible':0,'exact_hits':0};best=len(base)+structure(base)[0]
while queue and time.monotonic()-start<args.seconds:
    faces=queue.pop(0);st=structure(faces);n,edges,adj,dual=st;counts['tested']+=1
    discrete,hist=refinement(faces,n)
    if discrete and max(map(len,adj))<=6:
        counts['discrete']+=1;cs=cuts(faces,st)
        if cs:
            cover=np.array([[int(c['mask']>>i&1) for c in cs] for i in range(len(edges))])
            # Maximize uniform excess; degree-six vertices force zero there.
            r=linprog(np.zeros(len(cs)),A_ub=-cover,b_ub=-np.ones(len(edges))/3,A_eq=np.ones((1,len(cs))),b_eq=[1],bounds=(0,None),method='highs')
            if r.success:
                counts['lp_feasible']+=1
                support=[(j,Q(float(x)).limit_denominator(1000000)) for j,x in enumerate(r.x) if x>1e-8]
                total=sum(w for _,w in support);weights=[(j,w/total) for j,w in support]
                margins=[sum(w for j,w in weights if cs[j]['mask']>>i&1)-Q(1,3) for i in range(len(edges))]
                if min(margins)>=0 and max(margins)>0:
                    counts['exact_hits']+=1
                    result={'status':'generalized finite hypotheses only; analytic transfer pending','points':n,'faces':faces,'incidence_vertices':n+len(faces),'incidence_edges':3*len(faces),'refinement':hist,'cuts':[dict(cs[j],weight=str(w)) for j,w in weights],'pair_coverage_margins':list(zip(map(list,edges),map(str,margins)))}
                    if n+len(faces)<best:
                        best=n+len(faces);(out/f'candidate-{best}.json').write_text(json.dumps(result,indent=2));print(json.dumps({'hit':best,'support':len(weights),'counts':counts}),flush=True)
    neighbors=list(flips(faces))+list(contractions(faces));rng.shuffle(neighbors)
    for f in neighbors:
        if f not in seen:
            seen.add(f);queue.append(f)
(out/'summary.json').write_text(json.dumps(dict(counts,best=best,elapsed=time.monotonic()-start,seen=len(seen)),indent=2))
print(json.dumps(dict(counts,best=best)),flush=True)
