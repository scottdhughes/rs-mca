import json, urllib.request
def search(q, n=6, tags=None):
    body={"query":q,"n_results":n}
    if tags: body["tags"]=tags
    req=urllib.request.Request("https://api.theoremsearch.com/search",
        data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r: return json.loads(r.read())
def show(q, tags):
    print("\n"+"="*74); print("Q:",q)
    try: res=search(q,6,tags)
    except Exception as e: print("  ERR",e); return
    for t in res.get("theorems",[])[:6]:
        pap=t.get("paper") or {}
        print(f"  [{t.get('score',0):.3f}] {pap.get('paper_id','')} ({pap.get('year','')}) [{pap.get('primary_category','')}] {pap.get('title','')[:52]}")
        print(f"      {t.get('name','')}: {(t.get('body') or '').replace(chr(10),' ')[:190]}")
NT=["math.NT","math.CA","math.CO"]
show("Vinogradov mean value theorem over a multiplicative subgroup of a finite field", NT)
show("decoupling inequality for the moment curve over finite fields, mean value estimate", NT)
show("number of solutions equal power sums variables restricted to roots of unity subgroup", NT)
show("efficient congruencing mean value power sums finite field subgroup uniform in degree", NT)
show("additive energy of the moment curve image restricted to a subgroup, mean value", NT)
