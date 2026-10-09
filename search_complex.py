"""Model-proposed search: contract/flip triangulations, then certify three cuts.

This checks finite hypotheses only. A hit is NOT a Sidorenko counterexample
until the analytic construction has been transferred and verified.
"""
import argparse
from collections import Counter, defaultdict, deque
from itertools import combinations
import json
from pathlib import Path
import random
import re
import time

def normalize(faces):
    verts = sorted(set().union(*map(set, faces)))
    relabel = {v:i for i,v in enumerate(verts)}
    return tuple(sorted(tuple(sorted(relabel[v] for v in f)) for f in faces))

def structure(faces):
    edges=defaultdict(list)
    for j,f in enumerate(faces):
        for e in combinations(f,2):edges[e].append(j)
    n=len(set().union(*map(set,faces)))
    if len(faces)!=2*n-4 or len(set(faces))!=len(faces):return None
    if any(len(v)!=2 for v in edges.values()):return None
    adj=[set() for _ in range(n)]
    dual=[set() for _ in faces]
    for (a,b),(j,k) in edges.items():
        adj[a].add(b);adj[b].add(a);dual[j].add(k);dual[k].add(j)
    return n,edges,adj,dual

def refinement(faces,n):
    adj=[set() for _ in range(n+len(faces))]
    for j,f in enumerate(faces):
        for v in f:adj[v].add(n+j);adj[n+j].add(v)
    colors=[0]*n+[1]*len(faces);history=[colors]
    while True:
        signatures=[(colors[v],tuple(sorted(Counter(colors[w] for w in adj[v]).items()))) for v in range(len(adj))]
        ids={s:i for i,s in enumerate(sorted(set(signatures)))}
        nxt=[ids[s] for s in signatures]
        history.append(nxt)
        if len(set(nxt))==len(set(colors)):return len(set(nxt))==len(adj),history
        colors=nxt

def exposure(faces,subset,n):
    todo=set(subset);order=[min(todo)];todo.remove(order[0]);seen=set(faces[order[0]])
    while todo:
        for j in sorted(todo):
            f=set(faces[j])
            if len(f-seen)==1 and any(len(f&set(faces[k]))==2 for k in order):break
        else:return None
        order.append(j);todo.remove(j);seen.update(f)
    return order if len(seen)==n else None

def cuts(faces,st):
    n,edges,adj,dual=st;edgeids={e:i for i,e in enumerate(edges)};out=[]
    path=[0]
    def visit(mask):
        a=path[-1]
        if len(path)==n:
            if 0 not in adj[a] or path[1]>a:return
            cycle=path+[0]
            es={tuple(sorted((cycle[i],cycle[i+1]))) for i in range(n)}
            seen={0};q=[0]
            while q:
                j=q.pop()
                for k in dual[j]:
                    if k not in seen and tuple(sorted(set(faces[j])&set(faces[k]))) not in es:
                        seen.add(k);q.append(k)
            if len(seen)!=n-2:return
            other=set(range(len(faces)))-seen
            orders=[exposure(faces,seen,n),exposure(faces,other,n)]
            if not all(orders):return
            out.append({'mask':sum(1<<edgeids[e] for e in es),'cycle':path[:],'orders':orders})
            return
        for b in sorted(adj[a]):
            if not (mask>>b)&1:
                path.append(b);visit(mask|(1<<b));path.pop()
    visit(1)
    return out

def certify(faces):
    st=structure(faces)
    if st is None:return None
    n,edges,adj,dual=st
    discrete,hist=refinement(faces,n)
    if not discrete:return None
    cs=cuts(faces,st);allmask=(1<<len(edges))-1
    covers=[sum(1<<i for i,c in enumerate(cs) if c['mask']>>e&1) for e in range(len(edges))]
    for i,c in enumerate(cs):
        for j in range(i,len(cs)):
            need=allmask^(c['mask']|cs[j]['mask']);possible=(1<<len(cs))-1
            while need and possible:
                b=need&-need;possible&=covers[b.bit_length()-1];need-=b
            if possible:
                k=(possible&-possible).bit_length()-1;chosen=[cs[i],cs[j],cs[k]]
                bits=[''.join('0' if f in x['orders'][0] else '1' for x in chosen) for f in range(len(faces))]
                separation=[sum(a!=b for a,b in zip(bits[v[0]],bits[v[1]])) for v in edges.values()]
                assert min(separation)>=1 and max(separation)>1
                return {'points':n,'faces':faces,'incidence_vertices':n+len(faces),'incidence_edges':3*len(faces),'bits':bits,'cuts':chosen,'refinement':hist,'pair_separations':list(zip(map(list,edges),separation))}
    return None

def contractions(faces):
    st=structure(faces)
    for a,b in st[1]:
        new=[]
        for f in faces:
            g=set(a if v==b else v for v in f)
            if len(g)==3:new.append(tuple(sorted(g)))
        new=normalize(new)
        if structure(new):yield new

def flips(faces):
    st=structure(faces)
    for e,(j,k) in st[1].items():
        a=next(v for v in faces[j] if v not in e);b=next(v for v in faces[k] if v not in e)
        if tuple(sorted((a,b))) in st[1]:continue
        new=[f for i,f in enumerate(faces) if i not in (j,k)]
        new.extend(tuple(sorted((a,b,v))) for v in e)
        yield normalize(new)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--seconds',type=float,required=True);args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    text=Path(args.source).read_text().split('\\midrule',1)[1].split('\\bottomrule',1)[0]
    rows=re.findall(r'^\s*(\d+)\s*&\s*(\d+)&(\d+)&(\d+)\s*&',text,re.M)
    initial=normalize([tuple(map(int,row[1:])) for row in rows]);assert len(initial)==22
    baseline=certify(initial);assert baseline is not None
    (out/'baseline.json').write_text(json.dumps(baseline,indent=2))
    rng=random.Random(args.seed);start=time.monotonic();queue=deque([initial]);seen={initial};best=len(initial)+len(set().union(*map(set,initial)));stats=Counter();hits=[]
    while queue and time.monotonic()-start<args.seconds:
        faces=queue.popleft();st=structure(faces);n=st[0];stats[str(n)]+=1
        candidate=certify(faces)
        if candidate and candidate['incidence_vertices']<best:
            best=candidate['incidence_vertices'];hits.append(candidate)
            (out/f'candidate-{best}.json').write_text(json.dumps(candidate,indent=2))
            print(json.dumps({'hit':best,'points':n,'faces':len(faces),'tested':sum(stats.values())}),flush=True)
        neighbors=list(contractions(faces))+list(flips(faces));rng.shuffle(neighbors)
        # Model hypothesis favors contractions; flips explore new triangulations.
        for nxt in neighbors:
            if nxt not in seen:
                seen.add(nxt)
                if len(nxt)<len(faces):queue.appendleft(nxt)
                else:queue.append(nxt)
        if sum(stats.values())%100==0:print(json.dumps({'tested':dict(stats),'best':best,'queue':len(queue)}),flush=True)
    (out/'summary.json').write_text(json.dumps({'seed':args.seed,'elapsed':time.monotonic()-start,'tested':dict(stats),'seen':len(seen),'best_finite_hypotheses':best,'hit_count':len(hits),'status':'finite hypotheses only; analytic transfer not certified'},indent=2))

if __name__=='__main__':main()
