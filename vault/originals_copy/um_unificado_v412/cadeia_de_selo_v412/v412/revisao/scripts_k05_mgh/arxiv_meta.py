import urllib.request, re, sys, json, time
ids = ["math/0011063","2004.14115","2005.08544","2302.07877","2111.13865","2212.10874","2205.06043","0706.3463","math/0609703","hep-th/9603053","1011.4456","1505.01939","1611.07062"]
out = {}
for i in ids:
    url = "http://export.arxiv.org/api/query?id_list=" + i
    try:
        data = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    except Exception as e:
        out[i] = "ERRO " + repr(e); continue
    ent = data.split("<entry>")[-1]
    def g(tag):
        m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), ent, re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else None
    out[i] = {"title": g("title"), "journal_ref": g("arxiv:journal_ref"), "doi": g("arxiv:doi"), "published": g("published"), "updated": g("updated")}
    time.sleep(3)
json.dump(out, open("arxiv_meta_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, json.dumps(v, ensure_ascii=False))
