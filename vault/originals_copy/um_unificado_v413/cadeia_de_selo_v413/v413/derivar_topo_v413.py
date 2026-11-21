# -*- coding: utf-8 -*-
"""derivar_topo_v413.py -- gerencia c1, 21/11/2026: deriva, POR SCRIPT, o TOPO_RATIFICADO_v413_DERIVADO.json que o instalador exige.
Regra do contrato R2 (secao 6): «O resumo do artigo nao muda, salvo o que a pagina disser.» A pagina R2 nao fala do resumo. Logo o topo
da v413 e' o topo da v412 SEM troca nenhuma. Antes de gravar, o script CONFERE (fail-closed):
  (1) o contrato vigente traz a frase acima e a pagina vigente nao traz a palavra «resumo»;
  (2) o candidato nao define _V413_TOPO (a v413 nao escreve topo novo);
  (3) os literais _V412_TOPO e _V411_TOPO e as funcoes _v412_topo_texto e _v411_topo_texto do candidato sao IDENTICOS aos do um.py v412 do Nos;
  (4) o texto pt/en do TOPO_RATIFICADO_v412_DERIVADO.json e' o do _V412_TOPO do programa (se o literal tiver as chaves pt/en).
Grava por temporario (conferindo os bytes) com a proveniencia; nada digitado. Script da cadeia; nada daqui entra no programa."""
import ast, hashlib, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
BASE = V.parent / "v412" / "TOPO_RATIFICADO_v412_DERIVADO.json"
SAIDA = V / "TOPO_RATIFICADO_v413_DERIVADO.json"
CONTRATO = V / "CONTRATO_v413_R2.md"
PAGINA = V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R2.md"
ESP = json.loads((V / "ESPERADOS_v413.json").read_text(encoding="utf-8"))
CAND = Path(ESP["candidato"]["caminho"])
NOS_UM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731

c_raw, n_raw = CAND.read_bytes(), NOS_UM.read_bytes()
assert sha(c_raw)[:16] == ESP["candidato_sha16"], "o candidato nao e' o do ESPERADOS"
assert sha(n_raw)[:16] == ESP["origem_sha16"], "o um.py do Nos nao e' a v412 selada do ESPERADOS"
ct = CONTRATO.read_bytes().decode("utf-8")
frase = "O resumo do artigo não muda, salvo o que a página disser."
assert ct.count(frase) == 1, "o contrato vigente nao traz a regra do resumo"
pg = PAGINA.read_bytes().decode("utf-8")
assert "resumo" not in pg.lower(), "a pagina vigente fala do resumo: o topo precisa de derivacao com troca, nao de copia"
c_lin = c_raw.decode("utf-8").split("\n")
n_lin = n_raw.decode("utf-8").split("\n")
assert not any(x.startswith("_V413_TOPO") for x in c_lin), "o candidato define _V413_TOPO: este script nao serve"


def literal(lin, nome):
    ini = [i for i, x in enumerate(lin) if x.startswith(nome + " = ")]
    assert len(ini) == 1, (nome, len(ini))
    i = ini[0]
    for j in range(i + 1, min(i + 4000, len(lin)) + 1):
        trecho = "\n".join(lin[i:j])
        try:
            arv = ast.parse(trecho)
        except SyntaxError:
            continue
        assert len(arv.body) == 1 and isinstance(arv.body[0], ast.Assign)
        return trecho, ast.literal_eval(arv.body[0].value)
    raise AssertionError("literal nao fechou: " + nome)


def funcao(lin, nome):
    ini = [i for i, x in enumerate(lin) if x.startswith("def " + nome + "(")]
    assert len(ini) == 1, (nome, len(ini))
    i = ini[0]
    j = i + 1
    while j < len(lin) and (lin[j] == "" or lin[j][:1] in (" ", "\t", "#") or lin[j].startswith(")")):
        j += 1
    return "\n".join(lin[i:j]).rstrip("\n")


conf = {}
for nome in ("_V412_TOPO", "_V411_TOPO"):
    tc, vc = literal(c_lin, nome)
    tn, vn = literal(n_lin, nome)
    assert tc == tn and vc == vn, "o literal %s do candidato difere do da v412" % nome
    conf[nome] = {"identico": True, "sha256_do_trecho": sha(tc.encode("utf-8"))}
for nome in ("_v412_topo_texto", "_v411_topo_texto"):
    fc, fn = funcao(c_lin, nome), funcao(n_lin, nome)
    assert fc == fn, "a funcao %s do candidato difere da da v412" % nome
    conf[nome] = {"identico": True, "sha256_do_trecho": sha(fc.encode("utf-8"))}
braw = BASE.read_bytes()
base = json.loads(braw.decode("utf-8"))
_, v412 = literal(n_lin, "_V412_TOPO")
pt_en = "sem chaves pt/en no literal"
if isinstance(v412, dict) and "pt" in v412 and "en" in v412:
    assert base["pt"] == v412["pt"] and base["en"] == v412["en"], "o TOPO_RATIFICADO_v412_DERIVADO.json nao e' o _V412_TOPO do programa"
    pt_en = "pt e en do arquivo da v412 iguais aos do _V412_TOPO do programa"
saida = json.loads(braw.decode("utf-8"))
assert "derivacao_v413" not in saida
saida["derivacao_v413"] = {
    "o_que_e": "o topo ratificado da v412 SEM troca nenhuma: a v413 nao muda o resumo (contrato R2, secao 6) e o candidato nao escreve topo novo",
    "quem": "gerencia c1 (derivar_topo_v413.py)",
    "base": {"arquivo": "v412\\TOPO_RATIFICADO_v412_DERIVADO.json", "sha256": sha(braw)},
    "regra": {"contrato": CONTRATO.name, "sha256": sha(CONTRATO.read_bytes()), "frase": frase,
              "pagina": PAGINA.name, "pagina_sha256": sha(PAGINA.read_bytes()), "pagina_fala_do_resumo": False},
    "conferencia_no_programa": {"candidato_sha16": sha(c_raw)[:16], "um_py_v412_sha16": sha(n_raw)[:16], "trechos": conf,
                                "candidato_define_V413_TOPO": False, "texto_do_arquivo_v412": pt_en},
}
b = json.dumps(saida, ensure_ascii=False, indent=1).encode("utf-8")
if SAIDA.exists():
    if SAIDA.read_bytes() == b:
        print("ja' igual:", SAIDA)
        raise SystemExit(0)
    raise SystemExit("RECUSO: %s ja existe com outro conteudo" % SAIDA)
tmp = SAIDA.with_name(SAIDA.name + ".tmp")
tmp.write_bytes(b)
assert tmp.read_bytes() == b
tmp.replace(SAIDA)
print("gravado %s | sha16 %s | %d B | base v412 %s | %s" % (SAIDA.name, sha(b)[:16], len(b), sha(braw)[:16], pt_en))
for k, v in conf.items():
    print("  %-18s identico ao da v412 (trecho %s)" % (k, v["sha256_do_trecho"][:16]))
