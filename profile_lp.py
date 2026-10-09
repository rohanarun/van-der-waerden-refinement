"""Explore ALL finite concavity/tripling constraints, not only diagonal ones.

Floating LP values are conjecture guidance, not a certified exponent.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

p=argparse.ArgumentParser();p.add_argument('--size',type=int,required=True);p.add_argument('--targets',type=int,nargs='+',required=True);p.add_argument('--output',required=True);args=p.parse_args()
N=args.size;pairs=[(a,b) for a in range(1,N+1) for b in range(a,N+1)];ids={x:i for i,x in enumerate(pairs)}
def ix(a,b):return ids[tuple(sorted((a,b)))]
rr=[];cc=[];vv=[];rows=[]
def row(terms,label):
    j=len(rows);rows.append(label)
    for a,b,v in terms:rr.append(j);cc.append(ix(a,b));vv.append(v)
for a in range(1,N+1):
    for b in range(2,N):row([(a,b-1,1),(a,b,-2),(a,b+1,1)],['concavity',a,b])
    for h in range(1,(N-a+1)//3+1):row([(a,h,3),(a,3*h+a-1,-1)],['tripling',a,h])
    # Positivity on the infinite concave sequence forces nonnegative increments.
    for b in range(1,N):row([(a,b,1),(a,b+1,-1)],['monotonicity',a,b])
A=coo_matrix((vv,(rr,cc)),shape=(len(rows),len(pairs))).tocsr()
bounds=[(b,b) if a==1 else (0,None) for a,b in pairs];out=[]
for k in args.targets:
    objective=np.zeros(len(pairs));objective[ix(k,k)]=1
    r=linprog(objective,A_ub=A,b_ub=np.zeros(len(rows)),bounds=bounds,method='highs')
    item={'N':N,'target':k,'success':r.success,'message':r.message}
    if r.success:
        item.update(diagonal=r.fun,finite_log_slope=math.log(r.fun)/math.log(k),baseline_power=k**(4/3),max_constraint_error=float(max(A@r.x)))
    out.append(item);print(json.dumps(item),flush=True)
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2))
