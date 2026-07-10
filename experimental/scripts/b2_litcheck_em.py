import json, urllib.request
def search(q, n=6, tags=None):
    body={"query":q,"n_results":n}
    if tags: body["tags"]=tags
    req=urllib.request.Request("https://api.theoremsearch.com/search",
        data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r: return json.loads(r.read())
def show(q, tags):
    print("\n"+"="*76); print("Q:",q, tags)
    try: res=search(q,6,tags)
    except Exception as e: print("  ERR",e); return
    for t in res.get("theorems",[])[:6]:
        pap=t.get("paper") or {}
        print(f"  [{t.get('score',0):.3f}] {pap.get('paper_id','')} ({pap.get('year','')}) [{pap.get('primary_category','')}] {pap.get('title','')[:56]}")
        print(f"      {t.get('name','')}: {(t.get('body') or '').replace(chr(10),' ')[:200]}")

NT=["math.NT","math.CO"]; CA=["math.CA","math.CV","math.NT"]; IT=["cs.IT","math.NT","math.CO"]
show("bound on elementary symmetric function of complex numbers on the unit circle via power sums", CA)
show("coefficients of a polynomial with all roots on the unit circle, upper bound", CA)
show("elementary symmetric polynomial of values of an exponential sum over a multiplicative subgroup", NT)
show("weight enumerator of a subfield subcode or cyclic Reed-Solomon code via exponential sums", IT)
show("number of subsets of a multiplicative subgroup with prescribed power sums, Fourier coefficient bound", NT)
show("bound elementary symmetric e_m of roots of unity phases cancellation Bourgain Chang subgroup", NT)
