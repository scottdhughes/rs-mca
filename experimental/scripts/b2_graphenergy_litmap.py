import json, urllib.request, urllib.error

def search(q, n=6):
    req=urllib.request.Request("https://api.theoremsearch.com/search",
        data=json.dumps({"query":q,"n_results":n}).encode(),
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return json.loads(r.read())

queries=[
 "additive energy of multiplicative subgroup twisted by a polynomial phase uniform in the number of monomials",
 "second moment sum over s of squared incomplete character sum over multiplicative subgroup intersection",
 "square-root cancellation on average for character sums over multiplicative subgroups sparse Weil sum",
 "energy of graph (x, g(x)) multiplicative subgroup finite field polynomial exponential sum bound",
 "Weil sum over small multiplicative subgroup incomplete sum bound uniform in degree Bourgain Chang",
 "L2 average of exponential sums additive energy subgroup fourth moment bound independent of degree",
]
seen=set()
for q in queries:
    print("\n"+"="*74)
    print("Q:",q)
    try: res=search(q,6)
    except Exception as e:
        print("  ERR",e); continue
    for i,t in enumerate(res.get("theorems",[])[:6]):
        pap=t.get("paper") or {}
        title=pap.get("title","")
        arx=pap.get("paper_id") or pap.get("link","")
        yr=pap.get("year","")
        name=t.get("name","")
        body=(t.get("body") or "").replace("\n"," ")
        sc=t.get("score",0)
        key=(arx,name)
        star=" *NEW*" if key not in seen else ""
        seen.add(key)
        print(f"  [{sc:.3f}] {arx} ({yr}) — {title[:60]}{star}")
        print(f"        {name}: {body[:230]}")
