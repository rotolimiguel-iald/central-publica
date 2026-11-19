# Revisor K05/T1: confere DOIs/metadados das citacoes via API Crossref (consulta externa, somente leitura).
import json, sys, urllib.request, urllib.parse

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "revisor-k05-t1/1.0 (mailto:noreply@example.org)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))

dois = {
 "Takesaki1972_JFA9": "10.1016/0022-1236(72)90004-3",
 "Takesaki1973_Acta131": "10.1007/BF02392041",
 "ConnesTakesaki1977_Tohoku29": "10.2748/tmj/1178240493",
 "BW1975_JMP16": "10.1063/1.522605",
 "BW1976_JMP17": "10.1063/1.522898",
 "Choi1974_IJM18": "10.1215/ijm/1256051007",
 "Longo1979_CMP69": "10.1007/bf01197443",
 "TakesakiVolII_2003": "10.1007/978-3-662-10451-4",
}
out = {}
for k, d in dois.items():
    try:
        j = get("https://api.crossref.org/works/" + urllib.parse.quote(d))["message"]
        out[k] = {
            "doi": d,
            "titulo": (j.get("title") or [""])[0],
            "autores": [(a.get("family", "") + ", " + a.get("given", "")) for a in j.get("author", [])],
            "revista": (j.get("container-title") or [""])[0],
            "volume": j.get("volume"), "numero": j.get("issue"), "paginas": j.get("page"),
            "ano": (j.get("issued", {}).get("date-parts") or [[None]])[0][0],
        }
    except Exception as e:
        out[k] = {"doi": d, "erro": repr(e)}
# Driessler: busca por titulo
try:
    q = urllib.parse.urlencode({"query.bibliographic": "Driessler Comments on lightlike translations and applications in relativistic quantum field theory", "rows": 3})
    j = get("https://api.crossref.org/works?" + q)["message"]["items"]
    out["Driessler_busca"] = [{"doi": x.get("DOI"), "titulo": (x.get("title") or [""])[0],
        "autores": [(a.get("family", "") + ", " + a.get("given", "")) for a in x.get("author", [])],
        "revista": (x.get("container-title") or [""])[0], "volume": x.get("volume"), "paginas": x.get("page"),
        "ano": (x.get("issued", {}).get("date-parts") or [[None]])[0][0]} for x in j]
except Exception as e:
    out["Driessler_busca"] = repr(e)
json.dump(out, open("conferir_doi_crossref_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
