import urllib.request, json, time
dois = ["10.1063/1.5010424","10.1007/BF02392041","10.2748/tmj/1178240493","10.1007/3-540-28517-2","10.1007/978-1-4612-0005-5","10.1007/s11005-022-01514-5","10.1090/memo/0796","10.1007/s00220-020-03825-x","10.1142/S021988781100597X","10.1007/s11040-016-9207-z","10.1007/s11040-023-09451-y","10.1016/j.aim.2024.109496"]
res = {}
for d in dois:
    url = "https://api.crossref.org/works/" + d
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "revisao-k05 (mailto:none@example.org)"})
        j = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))["message"]
        res[d] = {"title": (j.get("title") or [None])[0], "container": (j.get("container-title") or [None])[0], "volume": j.get("volume"), "issue": j.get("issue"), "page": j.get("page"), "article-number": j.get("article-number"), "year": (j.get("issued", {}).get("date-parts") or [[None]])[0][0], "authors": [ (a.get("family") or a.get("name")) for a in j.get("author", [])][:6]}
    except Exception as e:
        res[d] = "ERRO " + repr(e)
    time.sleep(1)
json.dump(res, open("crossref_meta_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, json.dumps(v, ensure_ascii=False))
