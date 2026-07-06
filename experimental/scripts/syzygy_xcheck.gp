/* syzygy_xcheck.gp -- independent PARI/GP cross-check of dim(sum V_k)=E_3 (<=> dim Syz=K)
   at the E_3=ell-2 saturators. Rebuilds cosets/fibers/co-fiber-locators/M from scratch with
   PARI's own primitive root and polynomial arithmetic (independent of the Sage computation).
   Spectrum + E_3 + excess fibers are generator-independent, so a different primroot is fine. */

crosscheck(p, ell, gam) =
{
  my(g, n, zeta, rows, Ecnt, K, pts, lv, uniq, mult, mu, midx, modal, cof, cofpts, hk, poly, M, r, dimV, dimSyz);
  g = znprimroot(p);            \\ Mod(_,p), a primitive root (PARI's own choice)
  n = (p-1)/ell;
  zeta = g^n;                   \\ order-ell element
  rows = List(); Ecnt = 0; K = 0;
  for(i = 0, n-1,
    my(b = g^i);
    pts = vector(ell, j, b*zeta^(j-1));
    lv  = vector(ell, j, lift( sum(r = 1, ell-1, gam[r]*pts[j]^r) ));
    uniq = Set(lv);
    mult = vector(#uniq, t, sum(j = 1, ell, lv[j] == uniq[t]));
    mu = vecmax(mult);
    if(mu >= 3,
      midx = 0; for(t = 1, #uniq, if(mult[t] == mu && midx == 0, midx = t));
      modal = uniq[midx];
      cof = select(j -> lv[j] != modal, vector(ell, j, j));  \\ indices with non-modal value
      cofpts = vector(#cof, t, pts[cof[t]]);
      hk = prod(t = 1, #cofpts, (x - cofpts[t]));            \\ co-fiber locator, Mod coeffs
      for(d = 0, mu-2,
        poly = hk * x^d;
        listput(rows, vector(ell-1, jj, polcoef(poly, jj-1)));
      );
      Ecnt += mu-2; K += 1;
    );
  );
  M = matconcat(vector(#rows, t, rows[t])~)~;   \\ (#rows) x (ell-1) matrix over F_p
  r = matrank(M);                                \\ rank over F_p (entries are Mod(_,p))
  dimV = r; dimSyz = #rows - r;
  printf("  ell=%2d p=%3d : K=%d  E_3=%d  #rows=%d  rank=dim(sumV)=%d  dim Syz=%d  ->  %s\n",
         ell, p, K, Ecnt, #rows, dimV, dimSyz,
         if(dimV == Ecnt && dimSyz == K, "MATCHES Sage (dimV=E_3, dimSyz=K)", "MISMATCH!"));
}

print("PARI/GP independent cross-check of dim(sum V_k)=E_3 and dim Syz=K:");
crosscheck(331, 11, [97,29,97,239,171,92,143,155,270,1]);
crosscheck(313, 13, [254,289,29,276,242,219,201,261,79,232,133,1]);
crosscheck(103, 17, [30,82,52,3,7,90,70,30,27,71,85,33,12,85,66,0]);
quit;
