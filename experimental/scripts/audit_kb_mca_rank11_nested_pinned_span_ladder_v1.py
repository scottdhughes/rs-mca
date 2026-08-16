#!/usr/bin/env python3
"""Independent product/Fraction audit for the nested pinned-span ladder."""

from fractions import Fraction
from math import prod

n=2_097_152
K=1_048_576
m=1_116_048
w=67_472
B=274_980_728_111_395_087
C10=106_618_568_137_036_225_644
near=134_944
R1=8_147_918
p=2_130_706_433
tau=1_937
h=36_775

def falling(x,r):
    return prod(range(x-r+1,x+1))

def ratio_floor(top,bot,r):
    value=Fraction(1,1)
    for j in range(1,r+1):
        value*=Fraction(top+j,bot+j)
    return value.numerator//value.denominator

A=m-tau
c=2*A-n
mult=n-A
d=A-K
M=[ratio_floor(n-K,d,r) for r in range(1,11)]
M2=M[1]
N1=falling(m,9)//(c-h)**9
N2=falling(m,8)//(c-h)**8
total=near+C10//(tau+1)+mult+R1*N1+mult*M2*N2
L=B+1-total
q=h+1

loads=[]
value=L
for j in range(10):
    value=(value*(q-j)+(m-j)-1)//(m-j)
    loads.append(value)

caps=[mult*x for x in M]
dims=[]
for load in loads:
    dim=2
    for r,cap in enumerate(caps,1):
        if load>cap:
            dim=max(dim,r+1)
    dims.append(dim)

assert total==188_677_776_072_813_437
assert L==86_302_952_038_581_651
assert M==[16,255,4095,65530,1048431,16773712,268356622,4293280145,68684687551,1098814582063]
assert loads==[2843853816476423,93708171878891,3087708134499,101738094101,3352119806,110444488,3638792,119884,3950,131]
assert dims==[8,7,6,5,3,2,2,2,2,2]
assert all(x*x<p**6 for x in M)

print("KB_MCA_RANK11_NESTED_PIN_AUDIT_PASS")
print(f"total={total}")
print(f"residual={L}")
print("loads="+",".join(map(str,loads)))
print("dims="+",".join(map(str,dims)))
