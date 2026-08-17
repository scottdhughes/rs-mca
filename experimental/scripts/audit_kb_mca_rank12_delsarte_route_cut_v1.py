#!/usr/bin/env python3
"""Independent reverse-order audit for the rank-12 Delsarte route cut."""
from fractions import Fraction
from math import comb,prod,lcm
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
DUALS=ROOT/'experimental/data/certificates/kb-mca-rank12-delsarte-route-cut-v1/duals.json'
R=1_048_576;D=67_472;P=2_130_706_433;FIELD=P**6
B=274_980_728_111_395_087;NEAR=134_944;LOAD=B-NEAR+1
EXPECTED={5000:8_585_236_439_425_575,5040:10_093_625_108_064_998,5051:18_762_982_391_634_723}

def fall(x,r):return prod(x-j for j in range(r))
def rise(x,r):return prod(x+j for j in range(r))
def resource(s,K):
 vals=[Fraction(R+K)]
 for j in range(1,s+1):vals.extend((Fraction(fall(R+K,j+1),(D+K)*rise(D+1,j-1)),Fraction(fall(R+j,j+1),rise(D+1,j))))
 x=max(vals);return x.numerator//x.denominator

def q_falling(n,w,r,i):
 j=w-r;den=fall(w,i)*fall(n-w,i);num=sum((-1)**t*comb(i,t)*fall(j,t)**2*fall(r,i-t)*fall(n-2*w+r,i-t) for t in range(i+1));return Fraction(num,den)

def q_binomial(n,w,r,i):
 j=w-r;den=comb(w,j)*comb(n-w,j);num=0
 for t in range(i+1):
  a=j-t
  if 0<=a<=w-i and 0<=a<=n-w-i:num+=(-1)**t*comb(i,t)*comb(w-i,a)*comb(n-w-i,a)
 return Fraction(num,den)

def reverse_solve(A,b):
 n=len(A);M=[row[:]+[b[i]] for i,row in enumerate(A)]
 for c in range(n-1,-1,-1):
  p=next(j for j in range(c,-1,-1) if M[j][c]);M[c],M[p]=M[p],M[c];z=M[c][c];M[c]=[x/z for x in M[c]]
  for j in range(n):
   if j==c:continue
   z=M[j][c]
   if z:M[j]=[M[j][k]-z*M[c][k] for k in range(n+1)]
 return [M[i][-1] for i in range(n)]

def verify_record(K,rec,boundary=False):
 delta=int(rec['delta']);degrees=list(map(int,rec['degrees']));active=list(map(int,rec['active']));n=R+K;w=D+K-delta;lam=K-1
 y=reverse_solve([[-q_falling(n,w,r,i) for i in degrees] for r in active],[Fraction(1)]*len(degrees));assert all(x>=0 for x in y)
 value=Fraction(1)+sum(y);assert str(value.numerator)==rec['numerator'] and str(value.denominator)==rec['denominator'] and value.numerator//value.denominator==rec['floor']
 probes=sorted(set([0,lam,*active,lam//2]))
 for r in probes:
  assert sum(-y[j]*q_falling(n,w,r,degrees[j]) for j in range(len(degrees)))>=1
 if boundary:
  for r in probes:
   for i in degrees:assert q_falling(n,w,r,i)==q_binomial(n,w,r,i)
  dens=[fall(w,i)*fall(n-w,i) for i in degrees];L=1
  for x,z in zip(y,dens):L=lcm(L,x.denominator*z)
  coeff=[-x.numerator*(L//(x.denominator*z)) for x,z in zip(y,dens)]
  minimum=None
  for r in range(lam,-1,-1):
   total=-L
   for c,i in zip(coeff,degrees):
    j=w-r;num=sum((-1)**t*comb(i,t)*fall(j,t)**2*fall(r,i-t)*fall(n-2*w+r,i-t) for t in range(i+1));total+=c*num
   assert total>=0
   minimum=total if minimum is None or total<minimum else minimum
  assert minimum==0

def ordinary(delta):
 if delta>=D:return None
 q=comb(R+10,10)//comb(D-delta+10,10);return q if q*q<FIELD else None

def cap(K,records):
 cert={int(x['delta']):int(x['floor']) for x in records};INF=10**300;raw=[]
 for delta in range(1,D+2):
  vals=[];o=ordinary(delta)
  if o is not None:vals.append(o)
  if delta in cert:vals.append(cert[delta])
  raw.append(min(vals) if vals else INF)
 current=INF
 for i in range(len(raw)-1,-1,-1):current=min(current,raw[i]);raw[i]=current
 rem=resource(10,K);total=0;prev=0
 for delta,prefix in enumerate(raw,1):
  if prefix>=INF:take=rem//delta;total+=take;rem-=take*delta;break
  new=prefix-prev;per=(R-D+delta)//delta;slots=new*per;take=min(slots,rem//delta);total+=take;rem-=take*delta;prev=prefix
  if take<slots or rem<delta+1:break
 return total

def incident(K):
 c=min(resource(11,K),LOAD*(D+1));return -(-(LOAD*(D+K)-c)//(R+K))

def main():
 data=json.loads(DUALS.read_text());count=0
 for key in ('5051','5040','5000'):
  K=int(key);records=data[key];count+=len(records)
  verify_record(K,records[0],boundary=False)
  if len(records)>1:verify_record(K,records[-1],boundary=False)
  assert cap(K,records)==EXPECTED[K]
 intervals=((11,5001,17_683_935_531_825_185),(5002,5041,18_902_799_528_381_643),(5042,5052,18_912_521_379_321_277))
 for lo,hi,expected in reversed(intervals):assert min(incident(K) for K in range(hi,lo-1,-1))==expected
 assert incident(5053)==18_915_194_758_920_786
 assert 8*67_472+508_801==1_048_577 and 8*508_801+1==4_070_409
 print(f'KB_MCA_RANK12_DELSARTE_ROUTE_CUT_AUDIT_PASS certificates={count} first_open_K=5053')
if __name__=='__main__':main()
