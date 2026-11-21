# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\portao_do_pilar_candidato_v412.py (que fica intacto).
"""portao_do_pilar_candidato_v413.py -- o PORTAO DO PILAR NO CANDIDATO, por LEITURA DE CODIGO (nada roda; nada importa torch; nada toca a placa): confere, por sha256 do texto de cada nome de topo, que o gerador NAO tocou nenhuma
das tres entradas da chave do cache do pilar (o trabalhador embutido _QP_WORKER_SRC, a especificacao canonica _QP_SPEC_JSON e beta pelo motor _qp_beta) nem nada do fecho de dependencias da funcao da chave (_qp_key e o que ela e
as tres entradas leem); que os nomes do fecho sao os de PORTAO_DO_PILAR_v413.json (Etapa 1, lidos por script); que _EMBEDDED_KERNEL_FILES (onde muda, NOVO na v413, o texto do modulo corrigido), _LEAN_THEOREM_FLAGS, os
registros e o texto da v413 continuam FORA desse fecho; e que a correcao de texto do modulo do kernel so' muda _EMBEDDED_KERNEL_FILES. So' leitura. Grava PORTAO_DO_PILAR_CANDIDATO_v413.json (no modo proposta, com o sufixo).
O passo seguinte ao rito (conferir, antes dele, que o ambiente da placa e' o do cache; se nao for, PARAR) NAO e' deste script: ele nao toca a placa.
uso: C:\\Python314\\python.exe -B -X utf8 portao_do_pilar_candidato_v413.py [<candidato.py>]"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import e7_lib_v413 as L
sha = lambda b: hashlib.sha256(b).hexdigest()
CAND = sys.argv[1] if len(sys.argv) > 1 else str(L.CAND_DIR / "um_v413_candidato.py")
BASE = os.path.join(HERE, "base_v412", "um.py")
PJ = L.ler_json(L.D / "PORTAO_DO_PILAR_v413.json")


def carregar(p):
    src = open(p, "rb").read().decode("utf-8")
    tree = ast.parse(src)
    top = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            top[n.name] = n
        elif isinstance(n, ast.Assign):
            for tg in n.targets:
                if isinstance(tg, ast.Name):
                    top[tg.id] = n
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            top[n.target.id] = n
    return src, top


def fecho(top, raizes):
    vis, fila = set(), list(raizes)
    while fila:
        a = fila.pop()
        if a in vis or a not in top:
            continue
        vis.add(a)
        fila.extend(sorted({x.id for x in ast.walk(top[a]) if isinstance(x, ast.Name) and x.id in top and x.id != getattr(top[a], "name", None)}))
    return vis


bsrc, btop = carregar(BASE)
csrc, ctop = carregar(CAND)
ENTRADAS = {"worker_sha256": ["_qp_materialize", "_QP_WORKER_SRC", "_qp_dir"], "spec_canonica": ["_QP_SPEC_JSON", "_qp_canon", "_QP_SPEC_SHA256"], "beta_hex": ["_qp_beta"]}
raizes = ["_qp_key"] + sum(ENTRADAS.values(), [])
fb, fc = fecho(btop, raizes), fecho(ctop, raizes)
_LINHAS = {}


def seg(src, top, n):
    """o MESMO texto que ast.get_source_segment(src, top[n]) devolve (padded=False), com as linhas cortadas UMA vez por arquivo (ast._splitlines_no_ff, a funcao que o ast usa): o get_source_segment corta o
    arquivo inteiro a cada chamada, e com 50 MB e milhares de nomes de topo o portao levava perto de meia hora; o resultado nao muda (conferido abaixo contra o proprio ast em nomes de topo dos dois arquivos)"""
    k_ = id(src)
    if k_ not in _LINHAS:
        _LINHAS[k_] = ast._splitlines_no_ff(src)
    lines, node = _LINHAS[k_], top[n]
    a_, b_ = node.lineno - 1, node.end_lineno - 1
    if a_ == b_:
        return lines[a_].encode()[node.col_offset:node.end_col_offset].decode()
    return lines[a_].encode()[node.col_offset:].decode() + "".join(lines[a_ + 1:b_]) + lines[b_].encode()[:node.end_col_offset].decode()


for _src, _top in ((bsrc, btop), (csrc, ctop)):   # o atalho devolve o mesmo que o ast: conferido em nomes do inicio, do meio e do fim de cada arquivo (inclusive o maior)
    _ns = sorted(_top, key=lambda n_: _top[n_].lineno)
    _amostra = set(_ns[:3] + _ns[len(_ns) // 2:len(_ns) // 2 + 2] + _ns[-3:] + ["_EMBEDDED_KERNEL_FILES", "_qp_key"])
    for _n in _amostra:
        assert seg(_src, _top, _n) == ast.get_source_segment(_src, _top[_n]), ("o atalho do segmento difere do ast", _n)
e = L.Exame("portao_do_pilar_no_candidato_v413")
e.chk("o fecho de dependencias da chave e' o mesmo na base e no candidato (%d nomes)" % len(fb), fb == fc and len(fb) > 0, len(fb), sorted(fb ^ fc)[:6])
e.chk("o fecho da chave e' o mesmo que a Etapa 1 mediu (PORTAO_DO_PILAR_v413.json, campo fecho_dos_nomes_de_topo_da_chave)", sorted(fb) == sorted(PJ["fecho_dos_nomes_de_topo_da_chave"]), len(fb),
      sorted(set(fb) ^ set(PJ["fecho_dos_nomes_de_topo_da_chave"]))[:6])
_sha_e1 = PJ.get("sha256_do_texto_de_cada_nome_no_um_py_selado") or {}
_sha_c = {n: sha(seg(csrc, ctop, n).encode()) for n in fb if n in ctop}
e.chk("o sha256 do texto de cada nome do fecho no candidato e' o que a Etapa 1 leu no um.py selado", bool(_sha_e1) and all(_sha_c.get(n) == (v if len(v) == 64 else _sha_c.get(n)) and _sha_c.get(n, "")[:len(v)] == v for n, v in _sha_e1.items()), len(_sha_e1),
      {n: [v[:16], _sha_c.get(n, "")[:16]] for n, v in _sha_e1.items() if _sha_c.get(n, "")[:len(v)] != v})
dif = [n for n in sorted(fb) if n in ctop and sha(seg(bsrc, btop, n).encode()) != sha(seg(csrc, ctop, n).encode())]
e.chk("o texto de CADA nome do fecho tem o mesmo sha256 na base e no candidato", not dif and len(fb) > 0, len(fb), dif[:6])
por_entrada = {}
for k, nomes in ENTRADAS.items():
    hs = {n: (sha(seg(bsrc, btop, n).encode())[:16], sha(seg(csrc, ctop, n).encode())[:16]) for n in nomes if n in btop and n in ctop}
    por_entrada[k] = {n: {"base": a, "candidato": b, "igual": a == b} for n, (a, b) in hs.items()}
    e.chk("a entrada %s (%s): cada nome tem o mesmo sha256 na base e no candidato" % (k, ", ".join(nomes)), set(hs) == set(nomes) and all(a == b for a, b in hs.values()), len(nomes), por_entrada[k])
PROIBIDOS = ["_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "_V413_SPECS", "_V413_SECAO", "_V413_NOMES_REGISTROS", "_v413_secao_tex", "_v413_rodar_specs", "_V412_SPECS", "_V412_SECAO", "_V412_TOPO", "_v412_travessia",
             "_v412_guarda_frases", "_V411_SPECS", "_V411_H0DN_CONTRACT", "_ESQUELETO_STONES", "prove_external_ladder"]
dentro = [n for n in PROIBIDOS if n in fc]
e.chk("nenhum nome do que a v413 muda (kernel embutido com o modulo corrigido, bandeiras, escada, ledger, registros, texto do artigo) esta' no fecho da chave do candidato", not dentro, len(PROIBIDOS), dentro)
e.chk("as tres entradas da chave sao as de PORTAO_DO_PILAR_v413.json", set(PJ["entradas_da_chave"]) == set(ENTRADAS), len(ENTRADAS), sorted(PJ["entradas_da_chave"]))
# a correcao de texto do modulo do kernel so' muda _EMBEDDED_KERNEL_FILES: os nomes de topo que diferem entre a base e o candidato
dif_top = sorted(n for n in set(btop) & set(ctop) if sha(seg(bsrc, btop, n).encode()) != sha(seg(csrc, ctop, n).encode()))
novos_top = sorted(set(ctop) - set(btop))
ESPERADOS_DIF = {"_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder", "_ESQUELETO_STONES", "UM_VERSION", "_V411_SPECS", "_V411_H0DN_CONTRACT", "main"}
e.chk("os nomes de topo que mudam da base ao candidato sao so' os do delta (kernel embutido, bandeiras, escada, ledger, versao, pinos herdados, main, literais da escada); nenhum do fecho", not (set(dif_top) & fb), len(dif_top),
      {"mudam": dif_top[:60], "fora_do_esperado": sorted(set(dif_top) - ESPERADOS_DIF)[:30]})
e.chk("os nomes de topo novos sao os do runtime da v413", set(novos_top) == {"_v413_secao_tex", "_v413_rodar_specs", "_V413_SECAO", "_V413_SPECS", "_V413_NOMES_REGISTROS", "_V413_FONTES", "_V413_VERBATINS2"}, len(novos_top), novos_top)
e.chk("o candidato difere da base (nao e' copia: o gerador rodou)", sha(csrc.encode()) != sha(bsrc.encode()), 2)
out = {"ok": e.ok, "modo": L.MODO, "resumo": e.resumo(), "checagens": e.linhas, "candidato": {"arquivo": CAND, "sha16": sha(csrc.encode())[:16], "bytes": len(csrc.encode())}, "base_v412_sha16": sha(bsrc.encode())[:16],
       "entradas": por_entrada, "n_nomes_do_fecho": len(fb), "fecho": sorted(fb), "nomes_de_topo_que_mudam": dif_top, "nomes_de_topo_novos": novos_top, "portao_json_sha16": L.sha16_arq(L.D / "PORTAO_DO_PILAR_v413.json"),
       "falta_antes_do_rito": "conferir que o ambiente da placa (torch, cuda, numpy, scipy, python, gpu) e' o do cache; se nao for, PARAR e avisar (ha' treino em curso na placa): ato da gerencia, nao deste script"}
L.salvar_json(L.saida("PORTAO_DO_PILAR_CANDIDATO_v413.json"), out)
print(e.resumo())
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:400])
print("nomes de topo que mudam:", dif_top[:40], "| novos:", novos_top)
sys.exit(0 if e.ok else 1)
