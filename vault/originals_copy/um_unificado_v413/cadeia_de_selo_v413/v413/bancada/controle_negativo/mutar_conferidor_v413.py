# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bancada_B3_servico/controle_negativo/mutar_conferidor_v412.py (M1-M6), reapontado ao conferir_exigencias_servico_v413.py e
# acrescido das mutacoes da pendencia 2.8: M7 (o ja_fora_do_ar aceita PID parado), M8 (a conferencia A sem o sha256), M9 (aceita o ultimo PID VIVO com um_bancada), M10a/b/c (uma chave do recibo sai ou e' renomeada:
# porta_fechada, religar, versao_servida) e M11 (o livro do quadro volta a pular linha ilegivel, com o 2.2).
"""mutar_conferidor_v413.py -- CONTROLE NEGATIVO do conferidor (conferir_exigencias_servico_v413.py). NADA do servico e' executado e nenhum script real e' alterado.
Cada mutacao roda SOZINHA numa pasta TEMPORARIA nova: copias dos tres scripts do servico, do util e do delta_bn (o delta_bn da copia aponta HERE para a pasta real dos scripts e SERVICO_DIR para a pasta temporaria,
para que a conferencia do conferidor copiado seja gravada so' ali), a mutacao e uma copia do conferidor. Antes, o controle SEM mutacao tem de dar rc 0; depois, o conferidor tem de FALHAR (rc 1) em cada mutacao, e a
condicao que falha tem de ser a que aquela mutacao fere:
  M1  recibo_parada      : o `assert AUT` passa para DEPOIS da sonda da porta (E/S antes da exigencia da autorizacao);
  M2  recibo_religamento : a variavel de ambiente volta a V412_AUTORIZACAO_OPERADOR;
  M3  evento_c1_b3       : o `assert os.path.isfile(ESP)` passa para o FIM, depois do subprocess que anota no quadro;
  M4  recibo_parada      : sai o assert do CONTEUDO do AUT (os hash16 dos eventos 1687 e 1689, os sha16, a fala de 20/11): qualquer texto passaria;
  M5  recibo_religamento : volta como texto a data de uma ordem anterior (dd/mm/aaaa);
  M6  delta_bn           : o caminho da fala de 20/11 vira um nome que NAO existe (um rotulo enfiado no nome);
  M7  recibo_parada      : no ja_fora_do_ar sai a recusa de V413_PID_PARADO / V413_PID_PARADO_CRIADO no ambiente;
  M8  recibo_parada      : no ja_fora_do_ar sai a conferencia da conferencia A pelo sha256 que a gerencia passa;
  M9  recibo_parada      : no ja_fora_do_ar o ultimo PID conhecido passa a ser aceito VIVO como um_bancada;
  M10a recibo_parada     : a chave porta_fechada e' renomeada; M10b: a chave religar sai; M10c recibo_religamento: a chave versao_servida e' renomeada;
  M11 util               : o livro_conferido volta a pular a linha ilegivel (`continue` no lugar do raise).
Grava RESULTADO_CONTROLE_NEGATIVO_v413.json (em V413_MUTAR_SAIDA, padrao: DBN.SERVICO_DIR\\controle_negativo; nao sobrescreve) com os diffs e as condicoes que falharam. As pastas temporarias somem.
uso: V413_AUTORIZACAO_OPERADOR=<o texto que a gerencia passa aos recibos> python -I -B -X utf8 mutar_conferidor_v413.py   (V413_MUTAR_TEMP muda a pasta temporaria; padrao: %TEMP%\\mutar_conferidor_v413;
NUNCA o sandbox curto do pre-selo, C:\\t\\vb24, que o limpar apaga inteiro: o script recusa)"""
import ast
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)                          # ...\v413\bancada (os scripts reais)
sys.path.insert(0, SRC)
import delta_bn_v413 as DBN  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
NOMES = ("evento_c1_b3_v413.py", "recibo_parada_v413.py", "recibo_religamento_v413.py", "util_bn_v413.py", "delta_bn_v413.py")
TEMP_DIR = os.path.abspath(os.environ.get("V413_MUTAR_TEMP") or os.path.join(tempfile.gettempdir(), "mutar_conferidor_v413"))   # (revisao M1) nunca o sandbox curto do pre-selo
_sb = os.path.normcase(os.path.abspath(DBN.SANDBOX_CURTO))
assert not (os.path.normcase(TEMP_DIR) == _sb or os.path.normcase(TEMP_DIR).startswith(_sb + os.sep)), "M1: C:\\t\\vb24 e' exclusivo do pre-selo real; o controle negativo usa outra pasta (V413_MUTAR_TEMP)"
OUT_DIR = os.environ.get("V413_MUTAR_SAIDA") or os.path.join(DBN.SERVICO_DIR, "controle_negativo")
assert os.environ.get("V413_AUTORIZACAO_OPERADOR", "").strip(), "defina V413_AUTORIZACAO_OPERADOR com o MESMO texto que a gerencia passa aos recibos: sem ele o controle sem mutacao reprova no AUT e nada se prova"


def ler(p):
    return open(p, encoding="utf-8").read()


def gravar(p, t):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)


def so_uma_linha(t, prefixo):
    linha = [x for x in t.splitlines(True) if x.startswith(prefixo)]
    assert len(linha) == 1, (prefixo, len(linha))
    return linha[0]


def troca_uma(t, a, b):
    assert t.count(a) == 1, (a[:80], t.count(a))
    return t.replace(a, b, 1)


def m1(t):
    linha = so_uma_linha(t, "assert AUT,")
    assert t.count("s.close()\n") == 1
    return t.replace(linha, "").replace("s.close()\n", "s.close()\n" + linha, 1)


def m2(t):
    return troca_uma(t, 'os.environ.get("V413_AUTORIZACAO_OPERADOR"', 'os.environ.get("V412_AUTORIZACAO_OPERADOR"')


def m3(t):
    linha = so_uma_linha(t, "assert os.path.isfile(ESP)")
    return t.replace(linha, "") + linha


def m4(t):
    alvo = [n for n in ast.parse(t).body if isinstance(n, ast.Assert) and "FALA_20NOV_SHA16 in AUT" in ast.unparse(n.test)]
    assert len(alvo) == 1, len(alvo)
    linhas = t.splitlines(True)
    return "".join(linhas[:alvo[0].lineno - 1] + linhas[alvo[0].end_lineno:])


def m5(t):
    return troca_uma(t, '"""10-ter da v413', '"""10-ter da v413 (autorizacao de 12/11/2026)')


def m6(t):
    return troca_uma(t, '"OPERADOR_20nov_colei_no_codex', '"OPERADOR_20nov_v413_colei_no_codex')


def m7(t):
    return t.replace(so_uma_linha(t, '    assert not os.environ.get("V413_PID_PARADO"'), "")


def m8(t):
    return t.replace(so_uma_linha(t, "    assert hashlib.sha256(SA_BYTES).hexdigest() == SA_PINO"), "")


def m9(t):
    return troca_uma(t, '(ULT.startswith("VIVO|") and "um_bancada" not in ULT)', 'ULT.startswith("VIVO|")')


def m10a(t):
    return troca_uma(t, '"porta_fechada": True', '"porta_fechada_v413": True')


def m10b(t):
    return t.replace(so_uma_linha(t, '       "religar": '), "")


def m10c(t):
    return troca_uma(t, '"versao_servida": c.get("canonical_version")', '"versao": c.get("canonical_version")')


def m11(t):
    return t.replace(so_uma_linha(t, '            raise ValueError("EVENTOS_JSONL_ILEGIVEL'), "            continue\n")


MUTACOES = [("M1_assert_AUT_depois_da_sonda_da_porta", "recibo_parada_v413.py", m1, "recibo_parada_v413.py: nenhuma chamada de E/S antes do assert AUT"),
            ("M2_nome_da_v412_na_variavel", "recibo_religamento_v413.py", m2, "recibo_religamento_v413.py: ha a atribuicao AUT"),
            ("M3_assert_do_ESPERADOS_depois_do_subprocess", "evento_c1_b3_v413.py", m3, "evento (2.6): assert do stdout do ENSAIO"),
            ("M4_sem_o_conteudo_do_AUT", "recibo_parada_v413.py", m4, "recibo_parada_v413.py: N4:"),
            ("M5_data_de_ordem_anterior_no_script", "recibo_religamento_v413.py", m5, "recibo_religamento_v413.py: nenhuma data dd/mm/aaaa"),
            ("M6_fala_de_20nov_inexistente_no_delta_bn", "delta_bn_v413.py", m6, "delta_bn: a fala de 20/11"),
            ("M7_ja_fora_do_ar_aceita_pid_parado", "recibo_parada_v413.py", m7, "recibo_parada_v413.py: no ja_fora_do_ar nao finge parada"),
            ("M8_conferencia_A_sem_o_sha256", "recibo_parada_v413.py", m8, "recibo_parada_v413.py: no ja_fora_do_ar a conferencia A"),
            ("M9_ultimo_pid_vivo_com_um_bancada_aceito", "recibo_parada_v413.py", m9, "recibo_parada_v413.py: no ja_fora_do_ar o ultimo PID conhecido"),
            ("M10a_chave_porta_fechada_renomeada", "recibo_parada_v413.py", m10a, "recibo_parada_v413.py: chaves do dict rec"),
            ("M10b_chave_religar_retirada", "recibo_parada_v413.py", m10b, "recibo_parada_v413.py: chaves do dict rec"),
            ("M10c_chave_versao_servida_renomeada", "recibo_religamento_v413.py", m10c, "recibo_religamento_v413.py: chaves do dict rec"),
            ("M11_livro_pula_linha_ilegivel", "util_bn_v413.py", m11, "util (M11): livro_conferido")]
CONF = ler(os.path.join(SRC, "conferir_exigencias_servico_v413.py"))


def patch_delta(t, tmp):
    """o delta_bn da copia: HERE = a pasta real dos scripts (os lugares derivados continuam os reais, so' leitura) e SERVICO_DIR = a pasta temporaria (onde o conferidor copiado grava e onde nao ha' recibo)."""
    h = so_uma_linha(t, "HERE = os.path.dirname(os.path.abspath(__file__))")
    s = so_uma_linha(t, 'SERVICO_DIR = os.path.join(V413, "bancada_B3_servico")')
    return t.replace(h, "HERE = %r\n" % SRC).replace(s, "SERVICO_DIR = %r\n" % tmp)


def rodar(tmp, nome_do_script=None, novo=None):
    for n in NOMES:
        t = novo if n == nome_do_script else ler(os.path.join(SRC, n))
        gravar(os.path.join(tmp, n), patch_delta(t, tmp) if n == "delta_bn_v413.py" else t)
    gravar(os.path.join(tmp, "conferir_mut.py"), CONF)
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(tmp, "conferir_mut.py")], capture_output=True, text=True, encoding="utf-8", env=dict(os.environ), cwd=tmp, stdin=subprocess.DEVNULL)
    saida_p = os.path.join(tmp, "CONFERENCIA_EXIGENCIAS_SERVICO_v413.json")
    if not os.path.isfile(saida_p):
        raise SystemExit("a copia do conferidor terminou sem gravar a saida (rc %r) em %s; stderr: %s" % (r.returncode, tmp, (r.stderr or "")[-1500:]))
    saida = json.load(open(saida_p, encoding="utf-8"))
    return r.returncode, [{"nome": x["nome"], "observado": x["observado"]} for x in saida["condicoes"] if not x["ok"]], saida["n_condicoes"], saida["n_condicoes_ok"]


CRIOU_SANDBOX = not os.path.exists(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)
with tempfile.TemporaryDirectory(dir=TEMP_DIR) as tmp:
    rc0, falhas0, n0, nok0 = rodar(tmp)
resultados, diffs = {}, {}
for k, n, fn, esperada in MUTACOES:
    with tempfile.TemporaryDirectory(dir=TEMP_DIR) as tmp:
        original = ler(os.path.join(SRC, n))
        novo = fn(original)
        assert novo != original, ("a mutacao nao mudou nada", k)
        diffs[k] = "".join(difflib.unified_diff(original.splitlines(True), novo.splitlines(True), fromfile="real/" + n, tofile="mutado/" + n))
        rc, falhas, nn, nok = rodar(tmp, n, novo)
    pegou_esp = any(f["nome"].startswith(esperada) for f in falhas)
    resultados[k] = {"script": n, "rc": rc, "n_condicoes": nn, "n_condicoes_ok": nok, "condicoes_que_falharam": falhas, "condicao_esperada": esperada, "pegou_a_condicao_esperada": pegou_esp, "pegou": rc == 1 and pegou_esp}
SANDBOX = {"caminho": TEMP_DIR, "existia_antes": not CRIOU_SANDBOX, "criado_aqui": CRIOU_SANDBOX, "vazio_no_fim": None, "removido_no_fim": False}
if CRIOU_SANDBOX:   # so' o que ESTA corrida criou, e so' se ficou vazio
    SANDBOX["vazio_no_fim"] = not os.listdir(TEMP_DIR)
    if SANDBOX["vazio_no_fim"]:
        os.rmdir(TEMP_DIR)
        SANDBOX["removido_no_fim"] = True
res = {"contrato": "RESULTADO_CONTROLE_NEGATIVO_v413", "sandbox": SANDBOX, "script": {"path": os.path.abspath(__file__), "sha256": sha(open(os.path.abspath(__file__), "rb").read())},
       "conferidor": {"path": os.path.join(SRC, "conferir_exigencias_servico_v413.py"), "sha256": sha(open(os.path.join(SRC, "conferir_exigencias_servico_v413.py"), "rb").read())},
       "controle_sem_mutacao": {"rc": rc0, "esperado_rc": 0, "n_condicoes": n0, "n_condicoes_ok": nok0, "condicoes_que_falharam": falhas0},
       "mutacoes": list(resultados), "esperado_rc": 1, "resultados": resultados, "rc_do_conferidor_por_mutacao": {k: v["rc"] for k, v in resultados.items()},
       "falhas_por_mutacao": {k: [f["nome"][:120] for f in v["condicoes_que_falharam"]] for k, v in resultados.items()},
       "toda_mutacao_foi_pega": rc0 == 0 and all(v["pegou"] for v in resultados.values()),
       "diffs_das_mutacoes": diffs, "escopo": "nada do servico foi executado; nenhum script real foi alterado; as pastas temporarias foram apagadas; NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
os.makedirs(OUT_DIR, exist_ok=True)
dest = os.path.join(OUT_DIR, "RESULTADO_CONTROLE_NEGATIVO_v413.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("controle sem mutacao: rc", rc0, "(%d/%d condicoes ok)" % (nok0, n0), "| toda mutacao pega:", res["toda_mutacao_foi_pega"])
for k, v in resultados.items():
    print(" ", k, "-> rc", v["rc"], "|", len(v["condicoes_que_falharam"]), "condicao(oes) falhou(aram) | pegou a esperada:", v["pegou_a_condicao_esperada"])
print(dest, sha(open(dest, "rb").read())[:16])
sys.exit(0 if res["toda_mutacao_foi_pega"] else 1)
