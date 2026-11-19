# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R10)] copia de conferir_decima_lista_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_02_derivar_kernel_v412.py). O original fica intacto.
"""conferir_undecima_lista_v412.py -- (contrato R10) confere a DECIMA PRIMEIRA lista de pedras, so' por leitura: (1) o sha256 e os bytes de cada um dos 156 arquivos de insumos\\pedras_r11 contra insumos\\MANIFESTO_PEDRAS_v412_R11.json;
(2) nenhum arquivo em pedras_r11 fora do manifesto; (3) os 42 modulos da setima lista sao identicos BYTE A BYTE aos de insumos\\pedras_r7 (e ao sha256 do manifesto R7); (4) as duas pedras da oitava lista
(OPassoEOFim, OPsibitEACompressao) sao identicas BYTE A BYTE as de insumos\\pedras_r8; (5) os 112 restantes sao exatamente o campo novas_em_relacao_a_oitava_lista e tem frente C; frentes A=17, B=27, C=112;
(6) os espacos de nome da frente C sao os que o contrato diz (Codex 70, IALD 27, TGLExt 11, PsiNetworks 3, SondaCadeiaCaminho 1, SondaN0 1), lidos da PRIMEIRA linha `namespace` de cada fonte; (7) os dois arquivos de nome em
minusculas estao la' com o nome que tem; (8) nenhum modulo colide com um arquivo de TGLExt/ do Nos (nem por caixa); (9) todo import de irmao resolve na lista e todo import TGLExt/TGL resolve no kernel do Nos ou na lista;
(10) nenhuma fonte tem CR; (11) o campo tudo_junto do manifesto diz rc 0 e o recibo pedras_novas\\build\\TUDO_JUNTO.json existe. Grava kernel\\UNDECIMA_LISTA_CONFERIDA_v412.json. Cada checagem diz quantos itens examinou; zero e' falha."""
import collections, hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e7_lib_v412 import Exame, salvar_json, sha16_arq
NOS_K = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
R7, R8, R10 = HERE / "insumos" / "pedras_r7", HERE / "insumos" / "pedras_r8", HERE / "insumos" / "pedras_r11"
M7 = json.loads((HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json").read_bytes().decode("utf-8"))
M10 = json.loads((HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R11.json").read_bytes().decode("utf-8"))
sh = lambda b: hashlib.sha256(b).hexdigest()
e = Exame("decima_lista")
ent10 = {x["modulo"]: x for x in M10["modulos"]}
ent7 = {x["modulo"]: x for x in M7["modulos"]}
bad = [m for m, x in ent10.items() if not (R10 / (m + ".lean")).exists() or sh((R10 / (m + ".lean")).read_bytes()) != x["sha256"] or (R10 / (m + ".lean")).stat().st_size != int(x["bytes"])]
e.chk("os %d arquivos de pedras_r11 tem o sha256 e os bytes do manifesto R10" % len(ent10), not bad and len(ent10) == int(M10["n_modulos"]) == 156, len(ent10), bad[:5])
nomes_disco = sorted(p.name[:-5] for p in R10.iterdir() if p.name.endswith(".lean"))
sobra = [n for n in nomes_disco if n not in ent10]
e.chk("nenhum arquivo em pedras_r11 fora do manifesto (nomes comparados com a caixa exata)", not sobra and sorted(ent10) == nomes_disco, len(nomes_disco), sobra)
ig7 = [m for m in ent7 if m in ent10 and (R7 / (m + ".lean")).read_bytes() == (R10 / (m + ".lean")).read_bytes() and ent7[m]["sha256"] == ent10[m]["sha256"]]
e.chk("os 42 da setima lista sao identicos byte a byte (pedras_r7 x pedras_r11) e nos dois manifestos", len(ig7) == 42 == len(ent7), len(ent7), sorted(set(ent7) - set(ig7))[:5])
oit = ["OPassoEOFim", "OPsibitEACompressao"]
ig8 = [m for m in oit if m in ent10 and (R8 / (m + ".lean")).exists() and (R8 / (m + ".lean")).read_bytes() == (R10 / (m + ".lean")).read_bytes()]
e.chk("as duas pedras da oitava lista sao identicas byte a byte (pedras_r8 x pedras_r11) e estao na frente A", ig8 == oit and all(ent10[m]["frente"] == "A" for m in oit), len(oit), ig8)
novas = sorted(set(ent10) - set(ent7) - set(oit))
e.chk("os 112 restantes sao o campo novas_em_relacao_a_oitava_lista e tem todos frente C", novas == sorted(M10["novas_em_relacao_a_oitava_lista"]) and len(novas) == 112 and all(ent10[m]["frente"] == "C" for m in novas), len(novas), novas[:3])
fr = collections.Counter(x["frente"] for x in M10["modulos"])
e.chk("frentes: A=17, B=27, C=112", (fr["A"], fr["B"], fr["C"]) == (17, 27, 112), 156, dict(fr))
prim = collections.Counter(); sem_ns = []; dois = []
for m in novas:
    t = (R10 / (m + ".lean")).read_text(encoding="utf-8")
    g = sorted({x.split(".")[0] for x in re.findall(r"(?m)^namespace\s+(\S+)", t)})
    if not g:
        sem_ns.append(m); continue
    for raiz_ns in g:
        prim[raiz_ns] += 1
    if len(g) > 1:
        dois.append([m, g])
esperado = {"Codex": 70, "IALD": 27, "TGLExt": 11, "PsiNetworks": 3, "SondaCadeiaCaminho": 1, "SondaN0": 1}
e.chk("os espacos de nome da frente C (raiz de cada linha `namespace` de cada fonte; o modulo que abre dois conta nos dois) sao os do contrato", dict(prim) == esperado and not sem_ns and len(dois) == sum(esperado.values()) - 112, len(novas), [dict(prim), sem_ns, dois])
minus = sorted(m for m in ent10 if m[0].islower())
e.chk("os dois arquivos de nome em minusculas entram com o nome que tem", minus == ["sonda_cadeia_caminho", "sonda_n0_contraexemplo"] and all((R10 / (m + ".lean")).name == m + ".lean" for m in minus), len(minus), minus)
nos_nomes = {p.name[:-5] for p in (NOS_K / "TGLExt").iterdir() if p.name.endswith(".lean")}
nos_low = {n.lower() for n in nos_nomes}
colide = [m for m in ent10 if m in nos_nomes]; colide_caixa = [m for m in ent10 if m.lower() in nos_low and m not in nos_nomes]
entre_si = [k for k, v in collections.Counter(m.lower() for m in ent10).items() if v > 1]
e.chk("nenhum modulo colide com um arquivo de TGLExt/ do Nos (nem so' pela caixa), nem dois modulos da lista entre si pela caixa", not colide and not colide_caixa and not entre_si, len(ent10), [colide, colide_caixa, entre_si])
nao_res = []; n_imp = 0; n_irmaos = 0
for m in ent10:
    for imp in re.findall(r"(?m)^import\s+(\S+)", (R10 / (m + ".lean")).read_text(encoding="utf-8")):
        n_imp += 1
        if imp.startswith("Mathlib") or imp in ("Init", "Lean") or imp.startswith(("Init.", "Lean.")):
            continue
        if imp in ent10:
            n_irmaos += 1; continue
        if (NOS_K / (imp.replace(".", "/") + ".lean")).exists():
            continue
        nao_res.append((m, imp))
e.chk("todo import de irmao resolve na lista; todo import TGLExt/TGL resolve no kernel do Nos (%d imports de irmaos)" % n_irmaos, not nao_res and n_irmaos == sum(len(x["imports_de_candidatas"]) for x in M10["modulos"]), n_imp, nao_res[:5])
cr = [m for m in ent10 if b"\r" in (R10 / (m + ".lean")).read_bytes()]
e.chk("nenhuma fonte tem CR (fim de linha LF)", not cr, len(ent10), cr[:5])

def _sem_comentarios(t):
    """tira os comentarios de linha (--) e os blocos /- ... -/ (aninhados; inclui /-- docstring e /-! cabecalho) e normaliza os espacos; o que sobra e' o codigo"""
    out = []; i = 0; n = len(t); prof = 0; instr = False
    while i < n:
        c = t[i]
        if prof == 0 and instr:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(t[i + 1]); i += 2; continue
            if c == '"':
                instr = False
            i += 1; continue
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof > 0:
            if t.startswith("-/", i):
                prof -= 1; i += 2; continue
            i += 1; continue
        if t.startswith("--", i):
            j = t.find("\n", i)
            i = n if j < 0 else j; continue
        if c == '"':
            instr = True
        out.append(c); i += 1
    return " ".join("".join(out).split())


R10_ANT = HERE / "insumos" / ("pedras_" + "r10")
mud = list(M10.get("mudaram_da_decima_lista") or [])
dif_cod = [m for m in mud if _sem_comentarios((R10_ANT / (m + ".lean")).read_text(encoding="utf-8")) != _sem_comentarios((R10 / (m + ".lean")).read_text(encoding="utf-8"))]
dif_bytes = [m for m in mud if (R10_ANT / (m + ".lean")).read_bytes() != (R10 / (m + ".lean")).read_bytes()]
e.chk("as tres fontes que mudaram da decima lista (campo mudaram_da_decima_lista) mudaram so' em comentario: o codigo sem comentarios e' identico; os bytes diferem (a emenda existe)", mud == ["AClausulaExemplificativa", "AFitaEOIndice", "OPsiBitDaFormula"] and not dif_cod and sorted(dif_bytes) == sorted(mud), len(mud), {"codigo_diferente": dif_cod, "bytes_diferentes": dif_bytes})
resto_igual = [m for m in ent10 if m not in mud and m not in (M10.get("novas_em_relacao_a_decima_lista") or []) and (R10_ANT / (m + ".lean")).read_bytes() != (R10 / (m + ".lean")).read_bytes()]
e.chk("as outras 150 fontes sao identicas byte a byte as da decima lista; as tres novas (novas_em_relacao_a_decima_lista) nao existem na decima", not resto_igual and all(not (R10_ANT / (m + ".lean")).exists() for m in M10["novas_em_relacao_a_decima_lista"]) and len(M10["novas_em_relacao_a_decima_lista"]) == 3, len(ent10) - 3, resto_igual[:5])

tj = HERE / "pedras_novas" / "build" / "TUDO_JUNTO.json"
tjd = json.loads(tj.read_bytes().decode("utf-8")) if tj.exists() else None
e.chk("o manifesto diz que a raiz que importa o kernel e os 156 compilou com saida zero, e o recibo pedras_novas\\build\\TUDO_JUNTO.json existe", (M10.get("tudo_junto") or {}).get("rc") == 0 and tjd is not None, 1,
      {"manifesto": M10.get("tudo_junto"), "recibo_sha16": sha16_arq(tj) if tj.exists() else None, "recibo_rc": (tjd or {}).get("rc")})
out = {"ok": e.ok, "resumo": e.resumo(), "checagens": e.linhas, "manifesto_R10_sha16": sha16_arq(HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R11.json"), "manifesto_R7_sha16": sha16_arq(HERE / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"),
       "mudaram_da_nona_lista": M10.get("mudaram_da_nona_lista"), "por_autor": dict(collections.Counter(x["de_quem"] for x in M10["modulos"])), "por_autor_nas_novas": M10.get("por_autor_nas_novas")}
salvar_json(HERE / "kernel" / "UNDECIMA_LISTA_CONFERIDA_v412.json", out)
print(e.resumo())
for l in e.linhas:
    print(("ok    " if l["ok"] else "FALHOU"), l["checagem"][:150], l["n_itens_examinados"], "" if l["ok"] else str(l["detalhe"])[:400])
sys.exit(0 if e.ok else 1)
