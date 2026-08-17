#!/usr/bin/env python3
"""Independent selected-cell and direct endpoint audit."""
from fractions import Fraction
from math import comb,prod
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];X=ROOT/'experimental/data/certificates/kb-mca-rank12-three-slope-wall-v1/result.json'
R=1048576;D=67472;L=5170912
def fall(x,r):return prod(x-i for i in range(r))
def rise(x,r):return prod(x+i for i in range(r))
def ceilq(a,b):return -(-a//b)
def res(k):return max(fall(R+k,3)//((D+k)*rise(D+1,1)),fall(R+2,3)//rise(D+1,2))
def inc(K):return ceilq(L*(D+K)-res(K),R+K)
def direct(k):
 n=R+k;m=D+k;q=m//2;A=m-q-1;best=Fraction(-1);st=None;non=Fraction(-1)
 for h in range(n//(q+1)+1):
  for p in range(h+1):
   V=n-h*m+p+(h-p)*A
   if V<0:continue
   v=Fraction(comb(h,2))+V*(Fraction(p)+Fraction(h-p,A))
   if v>best:best,st=v,(h,p,V)
   if (h,p)!=(2,2):non=max(non,v)
 V=n-2*(m-1);low=comb(n,2)//(q*(m-q));two=-1 if V<0 else 4*V-4*m+3+comb(V,2)//(q*(m-q))
 return best.numerator//best.denominator,non.numerator//non.denominator,low,two,max(best.numerator//best.denominator+1,non.numerator//non.denominator+low,two),st
def main():
 x=json.loads(X.read_text())
 for k in (262710,262711,262712,300000,500000,1048576):
  b,n,l,t,c,st=direct(k);assert st[:2]==(2,2) or b<=981105;assert n+l<=981136;assert t<=max(2*(R-2*D-k+2)+2,981136);assert c<=max(2*(R-2*D-k+2)+2,981136)
 assert [(K,inc(K),max(2*(R-2*D-(K-1)+2)+2,981136)) for K in range(262710,262715)]==[(262710,1301844,1301852),(262711,1301847,1301850),(262712,1301850,1301848),(262713,1301853,1301846),(262714,1301856,1301844)]
 assert x['boundary']['shortfall']==3 and x['next_cell']['slack']==2
 print('KB_MCA_RANK12_THREE_SLOPE_AUDIT_PASS boundary=3 next_slack=2')
if __name__=='__main__':main()
