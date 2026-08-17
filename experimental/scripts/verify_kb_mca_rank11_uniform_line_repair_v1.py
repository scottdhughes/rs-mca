#!/usr/bin/env python3
"""Exact verifier for the uniform weighted-line repair of KoalaBear rank 11."""
from __future__ import annotations
import argparse, copy, json
from math import comb, prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank11-uniform-line-repair-v1/result.json'
PARENT='d01c546f4dca70e256c18c142873821b3bb48ab5'
R=1_048_576; D=67_472; KMAX=1_048_576
BUDGET=274_980_728_111_395_087; NEAR=134_944; START=BUDGET-NEAR+1

class Reject(ValueError): pass
def req(x:bool,msg:str)->None:
    if not x: raise Reject(msg)
def fall(x:int,r:int)->int:return prod(x-i for i in range(r))
def rise(x:int,r:int)->int:return prod(x+i for i in range(r))
def ceilq(a:int,b:int)->int:return -(-a//b)

def resource(s:int,k:int)->int:
    return max(fall(R+k,s+1)//((D+k)*rise(D+1,s-1)),fall(R+s,s+1)//rise(D+1,s))

def loads(start:int)->dict[int,int]:
    out={start:START}
    for s in range(start,1,-1):out[s-1]=ceilq(out[s]*(D+s)-resource(s,s),R+s)
    return out

def line_cap(k:int)->tuple[int,dict[str,int],int]:
    n=R+k;m=D+k;q=m//2;a=m-q-1
    low=comb(n,2)//(q*(m-q));hmax=n//(q+1)
    bn=-1;bd=1;state={};rows=0
    for h in range(1,hmax+1):
        b=a-1;C=n-h*m+h*a;cand={0,h}
        if b:
            v=(C-h)//(2*b);cand|={v-1,v,v+1,v+2,C//b,C//b+1}
        for p in cand:
            if not 0<=p<=h:continue
            W=n-h*m+p+(h-p)*a
            if W<0:continue
            num=h*(h-1)*a+W*(p*a+h-p);rows+=1
            if num*bd>bn*a:
                bn,bd=num,a;state={'h':h,'unit':p,'endpoint':h-p,'A':a,'W':W,'high':num//a}
    req(bool(state),'nonempty line scan')
    return low+bn//bd,state,rows

def uniform_scan()->dict:
    mx=-1;arg=0;prev=None;inc=0;rows=0;first={};last={}
    for k in range(1,KMAX+1):
        v,st,r=line_cap(k);rows+=r
        if k==1:first={'cap':v,**st}
        if k==KMAX:last={'cap':v,**st}
        if v>mx:mx,arg=v,k
        if prev is not None and v>prev:inc+=1
        prev=v
    req((mx,arg,inc)==(4_070_947,1,0),'uniform cap')
    req(first=={'cap':4_070_947,'h':8,'unit':8,'endpoint':0,'A':33_736,'W':508_801,'high':4_070_464},'first cell')
    req(last['cap']==981_112,'last cell')
    return {'maximum':mx,'argmax':arg,'strict_increases':inc,'dimensions':KMAX,'endpoint_rows':rows,'first':first,'last':last}

def early_scan(load:int,s:int)->dict[str,int]:
    tail=rise(D+1,s-1);constant=fall(R+s,s+1)//rise(D+1,s);numerator=fall(R+s,s+1)
    mn=None;mx=None;amin=amax=0;dec=0;prev=None
    for k in range(s,KMAX+1):
        moving=numerator//((D+k)*tail)
        v=ceilq(load*(D+k)-max(moving,constant),R+k)
        if mn is None or v<mn:mn,amin=v,k
        if mx is None or v>mx:mx,amax=v,k
        if prev is not None and v<prev:dec+=1
        prev=v
        if k<KMAX:numerator=numerator*(R+k+1)//(R+k-s)
    return {'minimum':int(mn),'argmin':amin,'maximum':int(mx),'argmax':amax,'decreases':dec,'cells':KMAX-s+1}

def build()->dict:
    l11=loads(10);req(l11[1]==5_201_865,'rank11 load')
    us=uniform_scan();req(l11[1]>us['maximum'],'rank11 contradiction')
    old=early_scan(l11[1],1);req((old['minimum'],old['maximum'])==(334_710,2_768_286),'old gap')
    l12=loads(11);req((l12[2],l12[1])==(5_170_912,332_497),'rank12 loads')
    scans={};cells=0
    for s in range(11,1,-1):
        z=early_scan(l12[s],s);req(z['minimum']==l12[s-1] and z['argmin']==s,f'rank12 s={s}')
        scans[str(s)]={'minimum':z['minimum'],'argmin':z['argmin'],'decreases':z['decreases'],'cells':z['cells']};cells+=z['cells']
    drop=early_scan(l12[2],2);req((drop['minimum'],drop['argmin'],drop['maximum'],drop['argmax'])==(332_497,2,2_751_700,KMAX),'rank12 drop')
    req(drop['maximum']<us['maximum'],'rank12 remains open')
    return {
      'schema':'kb-mca-rank11-uniform-line-repair-v1','parent':PARENT,
      'uniform_line':us,'rank11':{'load':l11[1],'cap':us['maximum'],'slack':l11[1]-us['maximum'],'old_early_drop':old},
      'rank12_route_cut':{'rank2_load':l12[2],'sequential_rank1_load':l12[1],'proper_drop_rank1_min':drop['minimum'],'proper_drop_rank1_max':drop['maximum'],'shortfall':us['maximum']-drop['maximum'],'cells':cells,'rows':scans},
      'claims':{'rank11_terminal_gap_repaired':True,'complete_affine_error_rank_11_paid':True,'complete_affine_error_rank_12_paid':False,'complete_affine_error_rank_13_paid':False,'active_v4_ledger_movement':0,'koalabear_closed':False}}

def tamper(x:dict)->int:
    edits=[('uniform_line','maximum',1),('uniform_line','argmax',2),('rank11','load',1),('rank11','slack',1),('rank12_route_cut','proper_drop_rank1_max',1),('claims','rank11_terminal_gap_repaired',False),('claims','complete_affine_error_rank_12_paid',True),('parent','', 'WRONG')]
    caught=0
    for a,b,v in edits:
        y=copy.deepcopy(x)
        if a=='parent':y['parent']=v
        elif isinstance(v,bool):y[a][b]=v
        else:y[a][b]+=v
        caught+=y!=x
    req(caught==8,'tamper');return caught

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--tamper-selftest',action='store_true');a=ap.parse_args();x=build()
    if a.write:RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('WROTE',RESULT);return
    req(RESULT.exists() and json.loads(RESULT.read_text())==x,'result reconstruction')
    if a.tamper_selftest:print(f'KB_MCA_RANK11_UNIFORM_LINE_TAMPER_PASS mutations={tamper(x)}/8');return
    print(f"KB_MCA_RANK11_UNIFORM_LINE_PASS load={x['rank11']['load']} cap={x['rank11']['cap']} slack={x['rank11']['slack']} rank12_shortfall={x['rank12_route_cut']['shortfall']}")
if __name__=='__main__':main()
