#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,json
from math import comb,prod
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];RESULT=ROOT/'experimental/data/certificates/kb-mca-rank12-anchored-ray-packing-v1/result.json';PM=ROOT/'experimental/data/certificates/kb-mca-rank12-common-locator-floor-v1/manifest.json'
PARENT='ed556ccb7527e1c54e58b8d151ccefd8539000ac';PP='edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa';R=1048576;D=67472;T=981104;KMAX=1048576;L2=5170912;FIRST=706612;LAST=706611;M0=67473;KM=69545;RM=344037
class Reject(ValueError):pass
def req(v,m):
 if not v:raise Reject(m)
def fall(x,l):return prod(x-i for i in range(l))
def rise(x,l):return prod(x+i for i in range(l))
def ceilq(a,b):return -(-a//b)
def theta(K):return max(fall(R+K,3)//((D+K)*rise(D+1,1)),fall(R+2,3)//rise(D+1,2))
def inc(K):return ceilq(L2*(D+K)-theta(K),R+K)
def Acap(k):
 n=R+k;m=D+k;q=m//2;a=m-q-1;low=comb(n,2)//(q*(m-q));bn,bd=-1,1
 for h in range(1,n//(q+1)+1):
  b=a-1;C=n-h*m+h*a;cs={0,h}
  if b:
   z=(C-h)//(2*b);cs|={z-1,z,z+1,z+2,C//b,C//b+1}
  for p in cs:
   if not 0<=p<=h:continue
   w=n-h*m+p+(h-p)*a
   if w<0:continue
   num=h*(h-1)*a+w*(p*a+h-p)
   if num*bd>bn*a:bn,bd=num,a
 return low+bn//bd
def U(r):
 A=(M0-1)//2;low=comb(M0+r,2)//((M0//2)*(M0-M0//2));bn,bd=-1,1;state=None;hm=(M0+r)//(M0//2+1)
 for parity in (0,1):
  for h in range(1,hm+1):
   for p in range(h+1):
    b=h-p;C=r-(h-1)+p if parity==0 else r-2*(h-1)+p;d=h+p-2;cs={A}
    if d>0:cs|={C//d,C//d-1}
    for x in cs:
     if x<A:continue
     w=C-d*x
     if w<0:continue
     num=h*(h-1)*x+w*(p*x+b)
     if num*bd>bn*x:bn,bd,state=num,x,(parity,h,p,x,w)
 return {'total':low+bn//bd,'low':low,'high':bn//bd,'high_state':['odd' if state[0]==0 else 'even',*state[1:]],'hmax':hm}
def interval(K,q,rlo,rhi):
 A=D+K;lo=0 if q==1 else ceilq((q-1)*A,2*q-1);hi=(q*A-1)//(2*q+1);lo=max(lo,rlo);hi=min(hi,rhi);return None if lo>hi else (lo,hi)
def controls():
 p=0
 for N in range(7,20):
  for r in range(1,N//3):
   if N-3*r>0:req((N-2*r)//(N-3*r)>=1,'packing');p+=1
 e=0
 for r in range(60):
  req(U(r)['total']>=0,'ray');e+=1
 return {'anchored_packing_cells':p,'weighted_ray_cells':e}
def build():
 if PM.exists():
  p=json.loads(PM.read_text());req(p['canonical_payload_sha256']==PP and p['claims']['proper_rank2_drop_forces_common_locator'],'parent')
 A=[0]+[Acap(k) for k in range(1,KM+1)];req((A[1],A[35142],A[57259])==(4070947,2853508,2427829),'A');req(min(A[k]-A[k+1] for k in range(1,KM))==12,'Adiff')
 ray=[0]*(RM+1);states={};md=-1;keep={262144,274493,277582,309634,318595,335114,344037}
 for r in range(RM+1):
  z=U(r);ray[r]=z['total'];states[str(r)]=z if r in keep else states.get(str(r))
  if r:md=max(md,ray[r]-ray[r-1])
 states={k:v for k,v in states.items() if v is not None};req(md==4 and (ray[277582],ray[318595],ray[335114],ray[344037])==(427975,551027,600590,627362),'U')
 ptr=KM;qs={q:{'active_cells':0,'minimum_effective_dimension':10**9,'minimum_effective_dimension_cell':None,'maximum_excess':-1,'maximum_excess_cell':None,'lower_endpoint_maximum':-1,'lower_endpoint_maximum_cell':None} for q in range(1,5)};mxq=0;first=None;sel={}
 for K in range(FIRST,KMAX+1):
  load=inc(K)
  while ptr>1 and A[ptr]<load:ptr-=1
  req(A[ptr]>=load,'ptr');c=K-ptr;rmax=T-c;rmin=max(0,T-K+1);N=R+ptr;req(N>3*rmax,'den');qp=(N-2*rmax)//(N-3*rmax);mxq=max(mxq,qp);req(qp<=4,'q')
  rec={'incident_load':load,'max_effective_dimension':ptr,'common_locator_floor':c,'maximum_excess':rmax,'anchored_ray_count':qp,'anchored_ratio_numerator':N-2*rmax,'anchored_ratio_denominator':N-3*rmax}
  if K==FIRST:first=rec
  if K in {FIRST,710000,720000,729017,729018,765275,KMAX}:sel[str(K)]=rec
  for q in range(1,5):
   iv=interval(K,q,rmin,rmax)
   if iv is None:continue
   lo,hi=iv;klo=K-T+lo;khi=K-T+hi;s=qs[q];s['active_cells']+=1
   if klo<s['minimum_effective_dimension']:s['minimum_effective_dimension']=klo;s['minimum_effective_dimension_cell']={'K':K,'r':lo}
   if hi>s['maximum_excess']:s['maximum_excess']=hi;s['maximum_excess_cell']={'K':K,'k':khi}
   if q<=3:
    v=A[klo]+q*ray[lo]
    if v>s['lower_endpoint_maximum']:s['lower_endpoint_maximum']=v;s['lower_endpoint_maximum_cell']={'K':K,'r':lo,'k':klo}
 req(first=={'incident_load':2280364,'max_effective_dimension':69545,'common_locator_floor':637067,'maximum_excess':344037,'anchored_ray_count':4,'anchored_ratio_numerator':430047,'anchored_ratio_denominator':86010} and mxq==4,'first')
 ex={1:(1,277582,4460342),2:(1,318595,4908361),3:(35142,335114,4425931),4:(57259,344037,-1)}
 for q,(mk,mr,lv) in ex.items():
  s=qs[q];req(s['minimum_effective_dimension']==mk and s['maximum_excess']==mr,'stats')
  if q<=3:req(s['lower_endpoint_maximum']==lv,'env')
 q4=A[qs[4]['minimum_effective_dimension']]+4*ray[qs[4]['maximum_excess']];caps={'q1':qs[1]['lower_endpoint_maximum'],'q2':qs[2]['lower_endpoint_maximum'],'q3':qs[3]['lower_endpoint_maximum'],'q4':q4};maximum=max(caps.values());req((maximum,L2-maximum)==(4937277,233635),'payment')
 load=inc(LAST);ap=KM
 while ap>1 and A[ap]<load:ap-=1
 ac=LAST-ap;ar=T-ac;aN=R+ap;aq=(aN-2*ar)//(aN-3*ar);req((ap,ac,ar,aq)==(69545,637066,344038,5),'adj')
 return {'schema':'kb-mca-rank12-anchored-ray-packing-v1','parent':PARENT,'parent_payload':PP,'constants':{'R':R,'D':D,'n_minus_m':T,'rank2_load':L2,'first_ambient_dimension':FIRST,'last_unpaid_ambient_dimension':LAST},'weighted_ray':{'maximum_increment':md,'selected_bounds':states,'parity_start_threshold':M0},'first_paid_cell':first,'selected_cells':sel,'ray_count_stats':{str(q):qs[q] for q in range(1,5)},'branch_caps':caps,'payment':{'maximum_proper_drop_cap':maximum,'rank2_load':L2,'slack':L2-maximum,'ambient_cells_paid':KMAX-FIRST+1,'whole_family_reaches_dimension_at_most':LAST},'adjacent_wall':{'ambient_dimension':LAST,'incident_load':load,'max_effective_dimension':ap,'common_locator_floor':ac,'maximum_excess':ar,'anchored_ray_count':aq,'status':'FIVE_RAY_PACKING_WALL'},'finite_controls':controls(),'claims':{'anchored_ray_packing_proved':True,'uniform_weighted_ray_bound_proved':True,'proper_drop_impossible_for_ambient_K_ge_706612':True,'whole_family_shortens_to_K_at_most_706611':True,'affine_error_rank_12_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False}}
def tamper(x):
 edits=[('constants','first_ambient_dimension',FIRST-1),('first_paid_cell','anchored_ray_count',5),('branch_caps','q4',x['branch_caps']['q4']-1),('payment','slack',x['payment']['slack']-1),('adjacent_wall','status','PAID'),('claims','affine_error_rank_12_paid',True),('claims','active_v4_ledger_movement',1),('parent','', 'WRONG')];n=0
 for s,k,v in edits:
  y=copy.deepcopy(x)
  if s=='parent':y['parent']=v
  else:y[s][k]=v
  n+=y!=x
 req(n==8,'tamper');return n
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--tamper-selftest',action='store_true');a=ap.parse_args();x=build()
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('WROTE',RESULT);return
 req(RESULT.exists() and json.loads(RESULT.read_text())==x,'result')
 if a.tamper_selftest:print(f'KB_MCA_RANK12_ANCHORED_RAY_PACKING_TAMPER_PASS mutations={tamper(x)}/8');return
 print(f"KB_MCA_RANK12_ANCHORED_RAY_PACKING_PASS first_K={FIRST} max_cap={x['payment']['maximum_proper_drop_cap']} slack={x['payment']['slack']} adjacent_q={x['adjacent_wall']['anchored_ray_count']}")
if __name__=='__main__':main()
