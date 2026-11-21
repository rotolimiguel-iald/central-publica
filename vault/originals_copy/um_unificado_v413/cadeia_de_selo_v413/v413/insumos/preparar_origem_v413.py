# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a ORIGEM das pedras novas da v413, na forma do kernel. Copia os 21 modulos novos (3 da
gerencia, 4 do Kimi, 12 do Codex, a sonda da contagem e o enunciado da fronteira) para insumos\\origem\\TGLExt\\X.lean,
com os imports dos modulos novos reescritos para TGLExt.X (os dos modulos da v412 ja' vem com TGLExt.). So' muda a
linha de import; nada mais. Fail-closed: o sha256 de cada fonte e' conferido contra o recibo que a conferiu ou
revisou (lido do recibo, nunca digitado). Recibo: insumos\\ORIGEM_v413.json."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
V413 = AQUI.parent
CAND = V413 / "candidatas_c1"
K412C = V413 / "conferencia_c1_codex" / "k412c" / "CONFERENCIA_K412C.json"
CONSOL = V413 / "revisao_codex" / "CODEX_CONSOLIDADO_R3" / "RESULTADO.json"
OUT = AQUI / "origem" / "TGLExt"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def le(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


k412c = {m["modulo"]: (Path(m["fonte"]), m["sha256_fonte"]) for m in le(K412C)["modulos"]}
consol = {it["module"]: (Path(it["source"]["path"]), it["source"]["sha256"]) for it in le(CONSOL)["items"]
          if isinstance(it.get("source"), dict) and "path" in it["source"]}


def da_conferencia_da_gerencia(pasta, nome):
    c = le(CAND / pasta / "build" / "CONFERENCIA.json")
    if "modulos" in c:
        m = [x for x in c["modulos"] if x["modulo"] == nome]
        assert len(m) == 1 and c.get("todos_bons") is True, (pasta, nome)
        return CAND / pasta / (nome + ".lean"), m[0]["sha256"], "CONFERENCIA.json de " + pasta
    assert c["bom"] is True, pasta
    return Path(c["fonte"]), c["sha256"], "CONFERENCIA.json de " + pasta


FONTES = {}
for nome in ["Operador"]:
    FONTES[nome] = da_conferencia_da_gerencia("R2_operador", nome) + ("gerencia",)
FONTES["Trinity"] = da_conferencia_da_gerencia("R8_trinity", "Trinity") + ("gerencia",)
FONTES["PonteCookLevin"] = da_conferencia_da_gerencia("R1_ponte_cook_levin", "PonteCookLevin") + ("gerencia",)
for nome in ["AIdentidadePreservada", "APropostaDaTensao", "ONomeEBeta", "APonteDeCookLevin"]:
    FONTES[nome] = k412c[nome] + ("CONFERENCIA_K412C.json", "Kimi")
for nome in ["APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral", "SimExterior", "SimCompleta",
             "RelogioBeta", "LeituraBeta", "QuantizacaoBeta", "Reconstrucao", "PonteLeituraBeta", "EntregaBeta"]:
    FONTES[nome] = k412c[nome] + ("CONFERENCIA_K412C.json", "Codex")
FONTES["SondaContagem"] = k412c["SondaContagem"] + ("CONFERENCIA_K412C.json", "gerencia")
FONTES["AFronteiraNaLinguaClassica"] = consol["AFronteiraNaLinguaClassica"] + ("CODEX_CONSOLIDADO_R3\\RESULTADO.json",
                                                                            "gerencia")
NOVOS = set(FONTES)
assert len(NOVOS) == 21

IMP = re.compile(r"^import (\S+)\s*$", re.M)
OUT.mkdir(parents=True, exist_ok=True)
itens = {}
for nome, (fonte, esperado, recibo, autor) in sorted(FONTES.items()):
    fonte = Path(fonte)
    medido = sha(fonte)
    assert medido == esperado, "FONTE MUDOU: %s %s != %s (%s)" % (nome, medido[:16], esperado[:16], recibo)
    t = fonte.read_bytes().decode("utf-8")
    n_crlf = t.count("\r\n")
    t = t.replace("\r\n", "\n")
    assert "\r" not in t, nome
    trocas = []

    def troca(m):
        alvo = m.group(1)
        if alvo in NOVOS:
            trocas.append([alvo, "TGLExt." + alvo])
            return "import TGLExt." + alvo
        assert alvo.startswith("TGLExt.") or alvo.startswith("Mathlib."), (nome, alvo)
        return m.group(0)

    novo = IMP.sub(troca, t)
    dados = novo.encode("utf-8")
    dest = OUT / (nome + ".lean")
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)
    imports = IMP.findall(novo)
    itens[nome] = {"autor_da_construcao": autor, "fonte": str(fonte), "sha256_fonte": medido, "recibo_do_hash": recibo,
                   "origem": str(dest), "sha256_origem": sha(dest), "trocas_de_import": trocas, "imports": imports,
                   "crlf_normalizados_para_lf": n_crlf}
    print("%-27s %-9s fonte %s -> origem %s | trocas %d | crlf->lf %d" % (
        nome, autor, medido[:16], itens[nome]["sha256_origem"][:16], len(trocas), n_crlf))

rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "o_que_e": "origem das pedras novas da v413 na forma do kernel; "
       "so' as linhas de import dos modulos novos mudam, e o fim de linha CRLF vira LF, como no kernel", "modulos": itens}
dados = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = AQUI / "ORIGEM_v413.json.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(AQUI / "ORIGEM_v413.json")
print("21 modulos | recibo ORIGEM_v413.json sha16 %s" % sha(AQUI / "ORIGEM_v413.json")[:16])
