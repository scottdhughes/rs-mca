import copy
from kb_rank_descent import descend,scan
from kb_pair_core_endpoint import best_endpoint,coupled

R12=descend(11,1)
R13=descend(12,1)
R14=descend(13,1,True)

__checked12,__rows12=scan(R12,3)
__checked13,__rows13=scan(R13,4)

# Local decreases exist in the rank-13 profile; only the global minimum is used.
assert __rows12[11][1]==0 and __rows13[12][1]>0
for s,item in __rows12.items():
    assert item[0]==R12[s-1] and item[1]==0
for s,item in __rows13.items():
    assert item[0]==R13[s-1]

#__best12,__first12=best_endpoint(3,R12[3])
#__best13,__first13=best_endpoint(4,R13[4])
assert __best12==(5761,16_380_678) and __first12==(59,80_307_161)
assert __best13==(12_233,22_658_813) and __first13==(1_037,73_634_528)

assert coupled(3)[0]==14_778_066
assert coupled(4)[0]==15_649_594
assert R14[8]==39_342_841_453
assert coupled(8)[0]==55_071_795_746

RESULT={
    "parent":"d01c546f4dca70e256c18c142873821b3bb48ab5",
    "rank12":{"forced":R12[3],"best_T":__best12[0],"cap":__best12[1],"coupled":14_778_066},
    "rank13":{"forced":R13[4],"best_T":__best13[0],"cap":__best13[1],"coupled":15_649_594},
    "rank14_wall":{"forced_rank8":R14[8],"coupled_cap":55_071_795_746,"shortfall":55_071_795_746-R14[8]},
    "cells_checked":__checked12+__checked13,
    "claims":{"rank12_paid":True,"rank13_paid":True,"rank14_paid":False,"active_v4_ledger_movement":0,"koalabear_closed":False},
}

def tamper():
    mutations=[
        ("rank12","forced"), ("rank12","cap"),
        ("rank13","forced"), ("rank13","cap"),
        ("rank14_wall","coupled_cap"),
        ("claims","rank12_paid"), ("claims","rank14_paid"),
        ("parent",None),
    ]
    caught=0
    for a,b in mutations:
        x=copy.deepcopy(RESULT)
        if b==None:
            x[a]="WRONG"
        elif isinstance(x[a][b],bool):
            x[a][b]=not x[a][b]
        else:
            x[a][b]+=1
        if x!=RESULT:
            caught+=1
    assert caught==len(mutations)
    return caught

if __name__=="__main__":
    print("KB_MCA_RANK12_13_PAIR_CORE_PASS",RESULT)
    print(f"KB_MCA_RANK12_13_PAIR_CORE_TAMPER_PASS mutations={tamper()}/8")
