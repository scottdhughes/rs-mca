load "/tmp/l1_syz_data.m2"
<< "=== ENGINE 3: Macaulay2 independent dim Syz (truncated kernel) ===" << endl;
scan(SATDATA, row -> (
  label := row#0; p := row#1; ell := row#2; mus := row#3; hcoeffs := row#4;
  kk := ZZ/p; R := kk[x];
  H := apply(hcoeffs, hc -> sum apply(#hc, i -> (hc#i * 1_kk) * x^i));
  K := #H;
  E3 := sum apply(mus, mu -> mu-2);
  -- rows = coeff vectors of h_k * x^d (d=0..mu_k-2) in F_p[X]_{<=ell-2} (dim ell-1)
  rows := flatten apply(K, k -> apply(mus#k-1, d -> (
    poly := H#k * x^d;
    apply(ell-1, j -> lift(coefficient(x^j, poly), kk))
  )));
  M := matrix rows;              -- (E3+K) x (ell-1)
  r := rank M;                   -- = dim(sum V_k)
  dimSyz := (E3+K) - r;
  << label << ": K=" << K << " E3=" << E3 << " rank(=dim sumV)=" << r
     << " dimSyz=" << dimSyz << "  [need dimSyz<=K, =K expected]: "
     << (if dimSyz == K then "= K (MATCH)" else if dimSyz <= K then "<= K" else "VIOLATION") << endl;
));

