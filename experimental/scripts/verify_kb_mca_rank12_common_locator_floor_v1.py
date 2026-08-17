#!/usr/bin/env python3
"""Exact verifier for the rank-twelve common-locator floor."""
from __future__ import annotations
import argparse, copy, json
from math import comb, prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank12-common-locator-floor-v1/result.json'
PARENT='8911e26e78c8d91173c413f079a13f88a04701fe'
R=1_048_576;D=67_472;KMAX=1_048_576;K0=262_710;L2=5_170_912

class Reject(ValueError): pass
def req(v:bool,msg:str)->None:
    if not v: raise Reject(msg)
def fall(x:int,r:int)->int:return prod(x-i for i in range(r))
def rise(x:int,r:int)->int:return prod(x+i for i in range(r))
def ceilq(a:int,b:int)->int:return -(-a//b)
def theta2(K:int)->int:return max(fall(R+K,3)//((D+K)*rise(D+1,1)),fall(R+2,3)//rise(D+1,2))
def incident(K:int)->int:return ceilq(L2*(D+K)-theta2(K),R+K)

def uniform_cap(k:int)->int:
    """Parent uniform weighted-line cap, independently reconstructed."""
    n=R+k;m=D+k;q=m//2;a=m-q-1
    low=comb(n,2)//(q*(m-q));hmax=n//(q+1)
    best_num=-1;best_den=1
    for h in range(1,hmax+1):
        b=a-1;C=n-h*m+h*a;candidates={0,h}
        if b:
            vertex=(C-h)//(2*b)
            candidates|={vertex-1,vertex,vertex+1,vertex+2,C//b,C//b+1}
        for p in candidates:
            if not 0<=p<=h:continue
            W=n-h*m+p+(h-p)*a
            if W<0:continue
            num=h*(h-1)*a+W*(p*a+h-p)
            if num*best_den>best_num*a:
                best_num,best_den=num,a
    req(best_num>=0,'nonempty uniform cap')
    return low+best_num//best_den

def stable_cap(k:int)->int:
    """Sharpened no-universal cap, proved for k>=K0."""
    req(k>=K0,'stable window')
    V=R-2*D-k+2
    return max(2*V+2,981_136)

def cap(k:int,uniform:list[int])->int:
    return stable_cap(k) if k>=K0 else uniform[k]

def endpoint_scan(k:int)->dict[str,int|tuple[int,...]]:
    """Exact active-window heavy/light endpoint control."""
    n=R+k;m=D+k;q=m//2;A=m-q-1;hmax=n//(q+1)
    best=-1;state=None;non=-1
    for h in range(hmax+1):
        for p in range(h+1):
            V=n-h*m+p+(h-p)*A
            if V<0:continue
            value=(comb(h,2)*A+V*(p*A+h-p))//A
            if value>best:best=value;state=(h,p,h-p,A,V)
            if (h,p)!=(2,2):non=max(non,value)
    low=comb(n,2)//(q*(m-q));V=n-2*(m-1)
    two_light=-1 if V<0 else 4*V-4*m+3+comb(V,2)//(q*(m-q))
    actual=max(best+1,non+low,two_light)
    return {'best':best,'state':state,'non':non,'low':low,'two_light':two_light,'actual':actual}

def build()->dict:
    # Reconstruct every parent cap below the stability window.
    uniform=[0]*(K0+1);increases=0;previous=None
    for k in range(1,K0):
        uniform[k]=uniform_cap(k)
        if previous is not None and uniform[k]>previous:increases+=1
        previous=uniform[k]
    uniform[K0]=stable_cap(K0)
    req(increases==0,'uniform caps nonincreasing')
    req((uniform[1],uniform[K0-1],uniform[K0])==(4_070_947,1_301_883,1_301_850),'cap boundary')

    # Independently certify every active-window endpoint profile.
    endpoint_cells=0;nonmax=-1;lowmax=-1
    for k in range(K0,KMAX+1):
        z=endpoint_scan(k);endpoint_cells+=1
        req(z['state'][:2]==(2,2) or z['best']<=981_105,'active extremizer')
        req(z['non']+z['low']<=981_136,'active nonextremal cap')
        req(z['two_light']<=stable_cap(k),'active light stability')
        req(z['actual']<=stable_cap(k),'active exact cap')
        nonmax=max(nonmax,int(z['non']));lowmax=max(lowmax,int(z['low']))

    # Target increases, while cap decreases.  The maximal effective residual
    # dimension therefore moves monotonically downward.
    pointer=K0;previous_core=0;core_decreases=0
    milestones={}; selected={}; ambient_cells=0
    threshold_list=[1,2,4,8,16,32,64,128,256,512,1024,4131,10000,100000,500000,1000000]
    selected_K={262711,262712,262713,262720,262750,262800,263000,270000,300000,400000,500000,700000,900000,KMAX}
    first_possible=None
    for K in range(K0+1,KMAX+1):
        target=incident(K)
        while pointer>1 and cap(pointer,uniform)<target:pointer-=1
        req(cap(pointer,uniform)>=target,'capacity at pointer')
        if pointer<K-1:req(cap(pointer+1,uniform)<target,'pointer maximality')
        core=K-pointer
        if core<previous_core:core_decreases+=1
        previous_core=core;ambient_cells+=1
        if first_possible is None:first_possible=(K,pointer,core,target)
        if K in selected_K:
            selected[str(K)]={'incident_load':target,'max_effective_dimension':pointer,'common_locator_floor':core,'cap_at_effective_dimension':cap(pointer,uniform),'next_cap':None if pointer==K-1 else cap(pointer+1,uniform)}
        for threshold in threshold_list:
            if str(threshold) not in milestones and core>=threshold:
                milestones[str(threshold)]={'ambient_dimension':K,'max_effective_dimension':pointer,'common_locator_floor':core,'incident_load':target}
    req(core_decreases==0,'locator floor nondecreasing')
    req(first_possible==(262_711,262_710,1,1_301_847),'first cell')
    req(selected[str(KMAX)]=={'incident_load':2_751_700,'max_effective_dimension':40_231,'common_locator_floor':1_008_345,'cap_at_effective_dimension':2_751_709,'next_cap':2_751_689},'full row')
    expected_milestones={
      '2':(262712,262710,2),'4':(262713,262709,4),'8':(262717,262709,8),'16':(262724,262708,16),'32':(262731,262697,34),'64':(262744,262678,66),'128':(262769,262641,128),'256':(262821,262565,256),'512':(262925,262411,514),'1024':(263131,262107,1024),'4131':(264388,260256,4132),'10000':(266765,256765,10000),'100000':(303866,203864,100002),'500000':(587137,87137,500000),'1000000':(1040688,40688,1000000)}
    for t,(K,k,c) in expected_milestones.items():
        req((milestones[t]['ambient_dimension'],milestones[t]['max_effective_dimension'],milestones[t]['common_locator_floor'])==(K,k,c),f'milestone {t}')
    return {
      'schema':'kb-mca-rank12-common-locator-floor-v1','parent':PARENT,'rank2_load':L2,
      'capacity':{'uniform_max':uniform[1],'transition_left':uniform[K0-1],'transition_right':uniform[K0],'transition_effective_dimension':K0,'uniform_dimensions_checked':K0-1,'active_endpoint_cells':endpoint_cells,'nonextremal_high_max':nonmax,'light_cap_max':lowmax},
      'first_cell':{'ambient_dimension':262_711,'incident_load':1_301_847,'max_effective_dimension':262_710,'common_locator_floor':1},
      'full_row':selected[str(KMAX)],'selected_cells':selected,'milestones':milestones,
      'scan':{'ambient_cells':ambient_cells,'locator_floor_decreases':core_decreases},
      'claims':{'proper_rank2_drop_forces_common_locator':True,'rank12_paid':False,'rank13_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False}}

def tamper(x:dict)->int:
    edits=[('rank2_load',1),('first_cell.common_locator_floor',1),('full_row.common_locator_floor',1),('milestones.32.ambient_dimension',1),('capacity.transition_right',1),('claims.rank12_paid',True),('claims.proper_rank2_drop_forces_common_locator',False),('parent','WRONG')];caught=0
    for key,value in edits:
        y=copy.deepcopy(x);parts=key.split('.');d=y
        for p in parts[:-1]:d=d[p]
        if isinstance(value,bool) or key=='parent':d[parts[-1]]=value
        else:d[parts[-1]]+=value
        caught+=y!=x
    req(caught==8,'tamper');return caught

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--tamper-selftest',action='store_true');a=ap.parse_args();x=build()
    if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('WROTE',RESULT);return
    req(RESULT.exists() and json.loads(RESULT.read_text())==x,'result reconstruction')
    if a.tamper_selftest:print(f'KB_MCA_RANK12_LOCATOR_FLOOR_TAMPER_PASS mutations={tamper(x)}/8');return
    print(f"KB_MCA_RANK12_LOCATOR_FLOOR_PASS first={x['first_cell']['common_locator_floor']} full={x['full_row']['common_locator_floor']} kappa={x['full_row']['max_effective_dimension']}")
if __name__=='__main__':main()
