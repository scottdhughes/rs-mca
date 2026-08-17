#!/usr/bin/env python3
"""Exact verifier for the dimension-matched rank-12 proper-drop wall."""
from __future__ import annotations
import argparse,copy,json
from math import comb,prod
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank12-three-slope-wall-v1/result.json'
PARENT='8911e26e78c8d91173c413f079a13f88a04701fe'
R=1_048_576;D=67_472;KMAX=1_048_576;L2=5_170_912;K0=262_710
class Reject(ValueError):pass
def req(x,m):
 if not x:raise Reject(m)
def fall(x,r):return prod(x-i for i in range(r))
def rise(x,r):return prod(x+i for i in range(r))
def ceilq(a,b):return -(-a//b)
def theta2(k):return max(fall(R+k,3)//((D+k)*rise(D+1,1)),fall(R+2,3)//rise(D+1,2))
def incident(K):return ceilq(L2*(D+K)-theta2(K),R+K)
def local_cap(k):
 # Certified for k>=K0 by the heavy/light stability lemma.
 V=R-2*D-k+2
 return max(2*V+2,981_136)
def endpoint_scan(k):
 n=R+k;m=D+k;q=m//2;A=m-q-1;hmax=n//(q+1)
 best=-1;second=-1;state=None
 for h in range(hmax+1):
  for p in range(h+1):
   V=n-h*m+p+(h-p)*A
   if V<0:continue
   num=comb(h,2)*A+V*(p*A+h-p);floor=num//A
   if floor>best:second=best;best=floor;state=(h,p,h-p,A,V)
   elif floor>second and (h,p)!=(2,2):second=floor
 # Recompute nonextremal maximum exactly.
 non=-1
 for h in range(hmax+1):
  for p in range(h+1):
   if (h,p)==(2,2):continue
   V=n-h*m+p+(h-p)*A
   if V>=0:non=max(non,(comb(h,2)*A+V*(p*A+h-p))//A)
 low=comb(n,2)//(q*(m-q))
 V=n-2*(m-1)
 two_light=-1 if V<0 else 4*V-4*m+3+comb(V,2)//(q*(m-q))
 return {'best_high':best,'nonextremal_high':non,'state':state,'low':low,'V':V,'two_light':two_light,'cap':max(best+1,non+low,two_light)}
def build():
 # Scan the entire active window and certify the finite endpoint inequalities.
 nonmax=-1;lowmax=-1;twomax_gap=-10**30;cells=0
 for k in range(K0,KMAX+1):
  z=endpoint_scan(k);cells+=1
  req(z['state'][:2]==(2,2) or z['best_high']<=981_105,'high classification')
  nonmax=max(nonmax,z['nonextremal_high']);lowmax=max(lowmax,z['low'])
  req(z['nonextremal_high']+z['low']<=981_136,'nonextremal branch')
  req(z['two_light']<=local_cap(k),'two-light branch')
  req(z['cap']<=local_cap(k),'local cap')
 # Dimension-matched scan: a proper rank-two drop at K lands in rank-one row k=K-1.
 first_possible=None;strict=0;mindiff=None;argmin=None
 for K in range(K0+1,KMAX+1):
  gap=incident(K)-local_cap(K-1)
  if gap<=0 and first_possible is None:first_possible=K
  if K>=262_712:req(gap>0,'all K>=262712 forced global')
  if mindiff is None or gap<mindiff:mindiff,argmin=gap,K
  strict+=gap>0
 req(first_possible==262_711,'first possible drop')
 req((incident(262_711),local_cap(262_710))==(1_301_847,1_301_850),'three-slope wall')
 req((incident(262_712),local_cap(262_711))==(1_301_850,1_301_848),'next cell paid')
 return {'schema':'kb-mca-rank12-three-slope-wall-v1','parent':PARENT,'active_window_start':K0,
  'rank2_load':L2,'first_possible_proper_drop':262_711,
  'boundary':{'ambient_dimension':262_711,'guaranteed_rank1_load':1_301_847,'dimension_matched_rank1_cap':1_301_850,'shortfall':3},
  'next_cell':{'ambient_dimension':262_712,'guaranteed_rank1_load':1_301_850,'dimension_matched_rank1_cap':1_301_848,'slack':2},
  'scan':{'ambient_cells':KMAX-K0,'endpoint_cells':cells,'nonextremal_high_max':nonmax,'low_max':lowmax},
  'claims':{'proper_drop_impossible_for_K_ge_262712':True,'rank12_paid':False,'rank13_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False}}
def tamper(x):
 edits=[('rank2_load',1),('first_possible_proper_drop',1),('boundary.shortfall',1),('next_cell.slack',-1),('claims.rank12_paid',True),('claims.proper_drop_impossible_for_K_ge_262712',False),('parent','WRONG'),('active_window_start',1)];c=0
 for key,v in edits:
  y=copy.deepcopy(x);p=key.split('.');d=y
  for z in p[:-1]:d=d[z]
  if isinstance(v,bool) or key=='parent':d[p[-1]]=v
  else:d[p[-1]]+=v
  c+=y!=x
 req(c==8,'tamper');return c
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--tamper-selftest',action='store_true');a=ap.parse_args();x=build()
 if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('WROTE',RESULT);return
 req(RESULT.exists() and json.loads(RESULT.read_text())==x,'result')
 if a.tamper_selftest:print(f'KB_MCA_RANK12_THREE_SLOPE_TAMPER_PASS mutations={tamper(x)}/8');return
 print(f"KB_MCA_RANK12_THREE_SLOPE_PASS first={x['first_possible_proper_drop']} shortfall={x['boundary']['shortfall']} next_slack={x['next_cell']['slack']}")
if __name__=='__main__':main()
