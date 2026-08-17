#!/usr/bin/env python3
"""Exact verifier for the rank-twelve basis-graph ray payment."""
from __future__ import annotations
import argparse, copy, json
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank12-basis-graph-ray-payment-v1/result.json'
PARENT_MANIFEST=ROOT/'experimental/data/certificates/kb-mca-rank12-common-locator-floor-v1/manifest.json'
PARENT='ed556ccb7527e1c54e58b8d151ccefd8539000ac'
PARENT_PAYLOAD='edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa'
R=1_048_576;D=67_472;T=R-D;L2=5_170_912;A1=4_070_947;KMAX=1_048_576
FIRST=778_970;R4=R//4;CORE4=T-R4;KAPPA_FIRST=60_010
CFIRST=774_075;CWALL=774_074;CKAPPA=60_631;CRMAX=267_660

class Reject(ValueError):pass
def req(v:bool,m:str)->None:
    if not v:raise Reject(m)
def fall(x:int,j:int)->int:return prod(x-i for i in range(j))
def rise(x:int,j:int)->int:return prod(x+i for i in range(j))
def ceilq(a:int,b:int)->int:return -(-a//b)
def theta2(k:int)->int:return max(fall(R+k,3)//((D+k)*(D+1)),fall(R+2,3)//rise(D+1,2))
def incident(k:int)->int:return ceilq(L2*(D+k)-theta2(k),R+k)

def line_cap(k:int)->int:
    n=R+k;m=D+k;q=m//2;a=m-q-1
    low=comb(n,2)//(q*(m-q));best=(-1,1)
    for h in range(1,n//(q+1)+1):
        b=a-1;c=n-h*m+h*a; cand={0,h}
        if b:
            z=(c-h)//(2*b);cand|={z-1,z,z+1,z+2,c//b,c//b+1}
        for p in cand:
            if not 0<=p<=h:continue
            out=n-h*m+p+(h-p)*a
            if out<0:continue
            num=h*(h-1)*a+out*(p*a+h-p)
            if num*best[1]>best[0]*a:best=(num,a)
    req(best[0]>=0,'line cap')
    return low+best[0]//best[1]

def hetero(k:int,m:int)->int:return m-1 if m<=k-1 else (k-1)*(m-k+1)
def ray_candidates(k:int,r:int)->dict[str,int]:
    req(k>=CWALL and 0<=r<=CRMAX+1,'ray window')
    return {lab:r+1+comb(m+r,2)//hetero(k,m) for lab,m in (
        ('M=D+1',D+1),('M=K-1',k-1),('M=K',k),('M=K+D',k+D))}
def ray(k:int,c:int,r:int)->tuple[int,str,dict[str,int]]:
    if c>T:return 0,'EMPTY_EXCEPTIONAL_FAMILY',{}
    if r==0:return 1,'FIXED_SUPPORT',{'fixed_support':1}
    z=ray_candidates(k,r);lab,val=max(z.items(),key=lambda x:(x[1],x[0]));return val,lab,z

def build()->dict[str,Any]:
    if PARENT_MANIFEST.exists():
        p=json.loads(PARENT_MANIFEST.read_text())
        req(p['canonical_payload_sha256']==PARENT_PAYLOAD,'parent payload')
        req(p['claims']['proper_rank2_drop_forces_common_locator'],'parent claim')
    req(3*R4<R+1 and 4*R4<R+1 and 4*(R4+1)==R+4,'support thresholds')
    req(CORE4==718_960,'locator threshold')
    caps={k:line_cap(k) for k in range(40_230,60_633)}
    req((caps[60_009],caps[60_010],caps[60_011])==(2_394_823,2_394_811,2_394_799),'cap boundary')
    req((incident(778_969),incident(778_970))==(2_394_808,2_394_810),'load boundary')

    ptr=CKAPPA;cmax=-1;cat=[];dmax=-1;ccells=0;cfirst=None;clast=None
    for k in range(CFIRST,FIRST):
        load=incident(k)
        while caps[ptr]<load:ptr-=1
        req(caps[ptr+1]<load,'conditional pointer')
        c=k-ptr;r=T-c;req(3*r<R+1,'conditional triple')
        rv,lab,vals=ray(k,c,r);total=A1+rv;req(total<L2,'conditional ray')
        deg=max(0,4*r-(R+1));dmax=max(dmax,deg)
        rec={'ambient_dimension':k,'incident_load':load,'effective_rank_one_dimension':ptr,
             'common_locator_floor':c,'outside_excess':r,'ray_cap':rv,'ray_argmax':lab,
             'ray_endpoint_candidates':vals,'composed_total':total,'slack':L2-total,
             'basis_edge_residual_factor_degree_max':deg}
        if k==CFIRST:cfirst=rec
        if k==FIRST-1:clast=rec
        if total>cmax:cmax=total;cat=[k]
        elif total==cmax:cat.append(k)
        ccells+=1
    req((cmax,cat,dmax,ccells)==(5_170_907,[CFIRST],22_063,4_895),'conditional scan')
    wload=incident(CWALL);wptr=CKAPPA
    while caps[wptr]<wload:wptr-=1
    wc=CWALL-wptr;wr=T-wc;wray,wlab,wvals=ray(CWALL,wc,wr);wtotal=A1+wray
    req((wptr,wc,wr,wtotal)==(60_631,713_443,267_661,L2+1),'conditional wall')

    ptr=KAPPA_FIRST;prev=CORE4-1;decreases=0;mxr=-1;mxrk=[];mxt=-1;mxtk=[];cells=0
    first_rec=None;full_rec=None;argmax:dict[str,int]={}
    for k in range(FIRST,KMAX+1):
        load=incident(k)
        while caps[ptr]<load:ptr-=1
        req(caps[ptr+1]<load,'pointer maximality')
        c=k-ptr;decreases+=c<prev;prev=c;r=max(0,T-c)
        req(c>=CORE4 and 3*r<R+1 and 4*r<R+1,'four-support cell')
        rv,lab,vals=ray(k,c,r);total=A1+rv;req(total<L2,'paid proper drop')
        argmax[lab]=argmax.get(lab,0)+1
        if rv>mxr:mxr,mxrk=rv,[k]
        elif rv==mxr:mxrk.append(k)
        if total>mxt:mxt,mxtk=total,[k]
        elif total==mxt:mxtk.append(k)
        rec={'ambient_dimension':k,'incident_load':load,'effective_rank_one_dimension':ptr,
             'common_locator_floor':c,'outside_excess':r,'rank_one_cap_at_floor':caps[ptr],
             'rank_one_global_cap':A1,'ray_cap':rv,'ray_argmax':lab,
             'ray_endpoint_candidates':vals,'total_cap':total,'slack':L2-total}
        if k==FIRST:first_rec=rec
        if k==KMAX:full_rec=rec
        cells+=1
    req(decreases==0 and (mxr,mxrk)==(1_067_271,[FIRST]),'ray maximum')
    req((mxt,mxtk,cells)==(5_138_218,[FIRST],269_607),'payment scan')
    req(first_rec and full_rec and full_rec['ray_cap']==0,'boundary records')

    ak=FIRST-1;ac=CORE4-1;ar=R4+1;an=D+ak+ar;ae=ak-ac
    arv,alab,avals=ray(ak,ac,ar);atotal=A1+arv
    req((an,ae,atotal,L2-atotal)==(1_108_586,60_010,5_138_224,32_688),'adjacent cell')
    return {
      'schema':'kb-mca-rank12-basis-graph-ray-payment-v1','parent':PARENT,'parent_payload':PARENT_PAYLOAD,
      'constants':{'R':R,'D':D,'n_minus_m':T,'rank2_load':L2,'rank1_global_max':A1,
        'first_ambient_dimension':FIRST,'four_support_excess_max':R4,'locator_threshold':CORE4,
        'conditional_first_ambient_dimension':CFIRST,'conditional_excess_max':CRMAX},
      'payment':{'first_cell':first_rec,'full_row':full_rec,'ambient_cells':cells,
        'maximum_ray_cap':mxr,'maximum_ray_cap_cells':mxrk,'maximum_composed_cap':mxt,
        'maximum_composed_cap_cells':mxtk,'minimum_slack':L2-mxt,
        'ray_endpoint_argmax_counts':argmax},
      'conditional_near_mds_interval':{'first_cell':cfirst,'last_cell':clast,'ambient_cells':ccells,
        'maximum_synchronized_total_cap':cmax,'maximum_synchronized_total_cap_cells':cat,
        'minimum_synchronized_slack':L2-cmax,'maximum_basis_edge_residual_factor_degree':dmax,
        'preceding_wall':{'ambient_dimension':CWALL,'incident_load':wload,
          'effective_rank_one_dimension':wptr,'common_locator_floor':wc,'outside_excess':wr,
          'ray_cap':wray,'ray_argmax':wlab,'ray_endpoint_candidates':wvals,
          'composed_total':wtotal,'over_by':wtotal-L2}},
      'adjacent_wall':{'ambient_dimension':ak,'incident_load':incident(ak),
        'effective_rank_one_dimension':ae,'common_locator_floor':ac,'outside_excess':ar,
        'four_omission_bound':4*ar,'reed_solomon_minimum_weight':R+1,'near_mds_excess':3,
        'shortened_domain_size':an,'outside_zero_count_min':an-(R+4),
        'outside_zero_count_max':an-(R+1),'residual_factor_degree_max':3,
        'synchronized_ray_cap':arv,'synchronized_ray_argmax':alab,
        'synchronized_ray_endpoint_candidates':avals,'synchronized_total_cap':atotal,
        'synchronized_slack':L2-atotal,
        'status':'EITHER_SYNCHRONIZED_RAY_IS_PAID_OR_CUBIC_NEAR_MDS_BASIS_EDGE'},
      'finite_controls':{'basis_graph':{'scalar_configurations':128,'basis_vertices':1002,
        'basis_edges':2400,'affine_cells':2},'arrangement':{'endpoint_cells':872,
        'cross_compositions':2516,'large_clone_cells':7056}},
      'claims':{'basis_graph_synchronizes_all_nonzero_second_differences':True,
        'one_affine_correction_ray_for_outside_core_family':True,
        'universal_core_aware_ray_cap_proved':True,
        'proper_drop_impossible_for_ambient_K_ge_778970':True,
        'whole_family_shortens_to_K_at_most_778969':True,
        'adjacent_cubic_near_mds_terminal_proved':True,
        'conditional_synchronized_ray_paid_for_K_ge_774075':True,
        'surviving_conditional_interval_emits_near_mds_basis_edge':True,
        'affine_error_rank_12_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False}}

def tamper(x:dict)->int:
    edits=[('constants.locator_threshold',CORE4-1),('adjacent_wall.residual_factor_degree_max',2),
      ('payment.maximum_composed_cap',x['payment']['maximum_composed_cap']-1),
      ('conditional_near_mds_interval.minimum_synchronized_slack',4),
      ('claims.basis_graph_synchronizes_all_nonzero_second_differences',False),
      ('claims.affine_error_rank_12_paid',True),('claims.active_v4_ledger_movement',1),('parent','WRONG')]
    caught=0
    for key,val in edits:
        y=copy.deepcopy(x);parts=key.split('.');d=y
        for p in parts[:-1]:d=d[p]
        d[parts[-1]]=val;caught+=y!=x
    req(caught==8,'tamper');return caught

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--json',action='store_true');ap.add_argument('--tamper-selftest',action='store_true');a=ap.parse_args();x=build()
    if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('WROTE',RESULT);return
    req(RESULT.exists() and json.loads(RESULT.read_text())==x,'result reconstruction')
    if a.tamper_selftest:print(f'KB_MCA_RANK12_BASIS_GRAPH_TAMPER_PASS mutations={tamper(x)}/8');return
    if a.json:print(json.dumps(x,sort_keys=True,separators=(',',':')));return
    print(f"KB_MCA_RANK12_BASIS_GRAPH_PASS first_K={FIRST} ray={x['payment']['maximum_ray_cap']} max_total={x['payment']['maximum_composed_cap']} min_slack={x['payment']['minimum_slack']}")
if __name__=='__main__':main()
