kk = ZZ/331;
R = kk[x];
cof = {{85,111,274,167,74,293},{58,103,296,149,179,4,320},{161,114,328,91,76,122},{10,52,117,145,92,15,78,207}};
ell = 11;
h  = apply(cof, S -> product(S, a -> (x - a)));      -- co-fiber locators h_k
mu = apply(cof, S -> ell - #S);                      -- mu_k = ell - |cofiber|
E3 = sum apply(mu, m -> m-2);
K  = #h;
-- the E3+K polynomials { h_k * x^d : 0<=d<=mu_k-2 }
kd = flatten for k from 0 to K-1 list for d from 0 to (mu#k - 2) list (h#k * x^d);
-- scalar matrix: rows = degrees 0..ell-2, cols = the E3+K polys ; rank = dim(sum V_k)
Mrows = for j from 0 to ell-2 list (for f in kd list coefficient(x^j, f));
M = matrix Mrows;
r = rank M;
<< "K = " << K << ", E_3 = " << E3 << ", #polys = " << #kd << endl;
<< "rank M  = dim(sum V_k) = " << r << "   (expect E_3 = " << E3 << " ; <= ell-2 = " << ell-2 << ")" << endl;
<< "nullity = dim Syz      = " << (#kd - r) << "   (expect K = " << K << ")" << endl;
<< "MACAULAY2 CROSS-CHECK: " << (if r == E3 and (#kd - r) == K then "PASS" else "FAIL") << endl;
