# Wolfram exact replay

A separate Wolfram Language calculation reconstructed the full endpoint
recurrence and weighted-line extremizer using exact integers and rationals.

```wl
Module[{rr=1048576,dd=67472,bb=274980728111395087,near0=134944,
  theta,loads,nend,mend,half,rows,best,low,total},
 theta[s_,k_]:=Floor[Max[
   Product[rr+k-i,{i,0,s}]/((dd+k) Product[dd+i,{i,1,s-1}]),
   Product[rr+s-i,{i,0,s}]/Product[dd+i,{i,1,s}]]];
 loads=Association[10->bb-near0+1];
 Do[AssociateTo[loads,s-1->Ceiling[
   (loads[s](dd+s)-theta[s,s])/(rr+s)]],{s,10,2,-1}];
 nend=rr+1; mend=dd+1; half=(mend-1)/2;
 rows=Flatten[Table[With[{q=h-p,
   out=nend-h mend+p+(h-p) half},
   If[out>=0,{h,p,h-p,out,
     h(h-1)+out(p+(h-p)/half)},Nothing]],
   {h,1,Floor[nend/(half+1)]},{p,0,h}],1];
 best=First[MaximalBy[rows,Last]];
 low=Floor[Binomial[nend,2]/(half(half+1))];
 total=Floor[Last[best]]+low;
 <|"loads"->loads,"highExtremizer"->best,
   "lowCap"->low,"totalCap"->total,
   "forced"->loads[1],"slack"->loads[1]-total|>]
```

Output:

```text
loads = {10->274980728111260144, 9->17695628624859819,
 8->1138737729126327, 7->73278302796469, 6->4715427489703,
 5->303431536894, 4->19525148223, 3->1256382675,
 2->80843204, 1->5201865}
highExtremizer = {8,8,0,508801,4070464}
lowCap = 483
totalCap = 4070947
forced = 5201865
slack = 1130918
```

The replay imports no Python output.
