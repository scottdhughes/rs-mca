#!/usr/bin/env python3
"""Independent direct-enumeration audit for the rank-eleven uniform-line repair."""
from fractions import Fraction
from math import comb,prod
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'experimental/data/certificates/kb-mca-rank11-uniform-line-repair-v1/result.json'
R=1_048_576;D=67_472;KMAX=1_048_576;START=274_980_728_111_395_087-134_944+1
def fall(x,r):return prod(x-i for i in range(r))
def rise(x,r):return prod(x+i for i in range(r))
def ceilq(a,b):return -(-a//b)
def res(s,k):return max(fall(R+k,s+1)//((D+k)*rise(D+1,s-1)),fall(R+s,s+1)//rise(D+1,s))
def loads(s):
 o={s:START}
 for j in range(s,1,-1):o[j-1]=ceilq(o[j]*(D+j)-res(j,j),R+j)
 return o
def direct(k):
 n=R+k;m=D+k;q=m//2;a=m-q-1;low=comb(n,2)//(q*(m-q));best=Fraction(-1);st=None
 for h in range(1,n//(q+1)+1):
  for p in range(h+1):
   W=n-h*m+p+(h-p)*a
   if W<0:continue
   v=Fraction(h*(h-1))+W*(Fraction(p)+Fraction(h-p,a))
   if v>best:best=v;st=(h,p,h-p,a,W)
 return low+best.numerator//best.denominator,st
def vertex(k):
 n=R+k;m=D+k;q=m//2;a=m-q-1;low=comb(n,2)//(q*(m-q));bn=-1;bd=1
 for h in range(1,n//(q+1)+1):
  b=a-1;C=n-h*m+h*a;c={0,h}
  if b:
   v=(C-h)//(2*b);c|={v-1,v,v+1,v+2,C//b,C//b+1}
  for p in c:
   if not 0<=p<=h:continue
   W=n-h*m+p+(h-p)*a
   if W<0:continue
   num=h*(h-1)*a+W*(p*a+h-p)
   if num*bd>bn*a:bn,bd=num,a
 return low+bn//bd
def controls():
 z=0
 for n in range(9,31):
  for m in range(3,n):
   q=m//2;a=m-q-1
   if a<1:continue
   for h in range(1,n//(q+1)+1):
    brute=Fraction(-1)
    for p in range(h+1):
     W=n-h*m+p+(h-p)*a
     if W>=0:brute=max(brute,Fraction(h*(h-1))+W*(Fraction(p)+Fraction(h-p,a)))
    b=a-1;C=n-h*m+h*a;c={0,h}
    if b:
     v=(C-h)//(2*b);c|={v-1,v,v+1,v+2,C//b,C//b+1}
    red=Fraction(-1)
    for p in c:
     if 0<=p<=h:
      W=n-h*m+p+(h-p)*a
      if W>=0:red=max(red,Fraction(h*(h-1))+W*(Fraction(p)+Fraction(h-p,a)))
    assert brute==red;z+=1
 return z
def main():
 x=json.loads(RESULT.read_text());mx=-1;arg=0;prev=None;inc=0
 for k in range(1,KMAX+1):
  v=vertex(k)
  if v>mx:mx,arg=v,k
  if prev is not None and v>prev:inc+=1
  prev=v
 assert (mx,arg,inc)==(4_070_947,1,0)
 for k in (1,2,3,1000,100000,KMAX):assert direct(k)[0]==vertex(k)
 l11=loads(10);l12=loads(11);assert l11[1]-mx==1_130_918
 vals=[ceilq(l12[2]*(D+k)-res(2,k),R+k) for k in range(2,KMAX+1)]
 assert (min(vals),max(vals))==(332_497,2_751_700)
 assert x['uniform_line']['maximum']==mx
 print(f'KB_MCA_RANK11_UNIFORM_LINE_AUDIT_PASS max={mx} argmax={arg} finite_controls={controls()} rank12_max_incident={max(vals)}')
if __name__=='__main__':main()
