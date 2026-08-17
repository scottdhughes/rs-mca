#!/usr/bin/env python3
"""Independent selected-cell audit for the rank-twelve locator floor."""
from fractions import Fraction
from math import comb,prod
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];X=ROOT/'experimental/data/certificates/kb-mca-rank12-common-locator-floor-v1/result.json'
R=1048576;D=67472;L=5170912;K0=262710
def fall(x,r):return prod(x-i for i in range(r))
def rise(x,r):return prod(x+i for i in range(r))
def ceilq(a,b):return -(-a//b)
def theta(K):return max(fall(R+K,3)//((D+K)*rise(D+1,1)),fall(R+2,3)//rise(D+1,2))
def inc(K):return ceilq(L*(D+K)-theta(K),R+K)
def direct_uniform(k):
 n=R+k;m=D+k;q=m//2;a=m-q-1;low=comb(n,2)//(q*(m-q));best=Fraction(-1)
 for h in range(1,n//(q+1)+1):
  for p in range(h+1):
   W=n-h*m+p+(h-p)*a
   if W>=0:best=max(best,Fraction(h*(h-1))+W*(Fraction(p)+Fraction(h-p,a)))
 return low+best.numerator//best.denominator
def stable(k):return max(2*(R-2*D-k+2)+2,981136)
def C(k):return stable(k) if k>=K0 else direct_uniform(k)
def invert(K):
 target=inc(K);lo=1;hi=K-1;ans=0
 while lo<=hi:
  mid=(lo+hi)//2
  if C(mid)>=target:ans=mid;lo=mid+1
  else:hi=mid-1
 return ans

def controls():
 checked=0
 for n in range(9,31):
  for m in range(3,n):
   q=m//2;a=m-q-1
   if a<1:continue
   for h in range(1,n//(q+1)+1):
    brute=Fraction(-1)
    for p in range(h+1):
     W=n-h*m+p+(h-p)*a
     if W>=0:brute=max(brute,Fraction(comb(h,2))+W*(Fraction(p)+Fraction(hw-p,a))
    assert brute>=0;checked+=1
 return checked

def main():
 x=json.loads(X.read_text())
 expected={262711:(262710,1),262712:(262710,2),262713:(262709,4),262731:(262697,34),264388:(260256,4132),300000:(209241,90759),500000:(107312,392688),1048576:(40231,1008345)}
 for K,(k,c) in expected.items():
  z=invert(K);assert (z,K-z)==(k,c);assert C(z)>=inc(K);assert z==K-1 or C(z+1)<inc(K)
 assert x['full_row']['common_locator_floor']==1008345
 print(f'KB_MCA_RANK12_LOCATOR_FLOOR_AUDIT_PASS selected={len(expected)} finite_controls={controls()}')
if __name__=='__main__':main()
