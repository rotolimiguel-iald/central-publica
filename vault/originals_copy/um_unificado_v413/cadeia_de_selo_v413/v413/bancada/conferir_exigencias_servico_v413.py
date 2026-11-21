# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bancada_B3_servico/conferir_exigencias_servico_v412.py (so' leitura: ast + texto), reescrito para os scripts do servico da v413
# (recibo_parada_v413.py, recibo_religamento_v413.py, evento_c1_b3_v413.py), a biblioteca que eles usam (util_bn_v413.py: o livro do quadro conferido inteiro, 2.2) e as constantes (delta_bn_v413.py: N4, N6).
"""conferir_exigencias_servico_v413.py -- SO LEITURA (ast + texto; o livro do quadro, os recibos de entrada e os arquivos das falas sao LIDOS): NADA e' executado (nem parada, nem religamento, nem evento).
Confere:
  (a) parada e religamento EXIGEM V413_AUTORIZACAO_OPERADOR: a atribuicao e o `assert AUT` seguinte sao as UNICAS coisas executaveis antes de qualquer E/S; nenhum nome da v412 sobrou;
  (b) N4 (decisao da gerencia): o livro do quadro e' conferido INTEIRO (U.livro_conferido, 2.2) ANTES dos eventos; o 1687 pelo sha256 do recibo que ele nomeia, o 1689 pelo sha16 da fala que ele nomeia, a fala de 20/11 por
      bytes; e o assert do conteudo do AUT (os dois hash16 dos eventos, os sha16, a resposta, a decisao, a fala de 20/11 inteira) vem DEPOIS dessas conferencias; o AUT do ambiente deste conferidor traz tudo isso;
  (c) as chaves e a ordem do dict `rec` dos dois recibos = as dos recibos REAIS da v411 + os acrescimos da v413 (declarados aqui);
  (d) a parada: os dois modos escolhidos por V413_PARADA, nunca presumidos (o assert do modo DEPOIS da autorizacao e ANTES da sonda da porta); no ja_fora_do_ar: recusa PID parado no ambiente (M7), confere a
      conferencia A pelo sha256 que a gerencia passa (M8), exige o ultimo PID conhecido AUSENTE ou outro programa (M9) e diz que nada foi parado; N6: le o religamento da v411;
  (e) o religamento: o recibo do APLICAR tambem numa repeticao (2.3), so' o veredito do APLICAR do salto e exatamente 1 com o manifesto do disco; o deployment B21-v413 e o anterior B20 (N6); o modo da placa e a fala
      dele ANTES do lancamento (sem ela, AGUARDA rc 20); no cpu, CUDA_VISIBLE_DEVICES=-1; N9: o stdout e o stderr anexados aos logs de estado\\; a identidade SO' de /api/contratos; o recibo existente bloqueia antes;
  (f) o evento (2.6): o ENSAIO e o b3_recibo dele com rc 0 ANTES de anotar; o ESPERADOS e o candidato antes do subprocess que anota; o rc do iald.py exigido; o retorno lido e o elo conferido no livro;
  (g) o util: livro_conferido recusa linha ilegivel (o except LEVANTA, nunca `continue`), confere anterior e hash e recusa seq repetida (M11);
  (h) o delta_bn: a fala de 20/11 existe (M6), as seqs da autorizacao, o sandbox curto novo;
  (i) nenhuma data dd/mm/aaaa nem hash de 16+ hex digitado nos tres scripts; os recibos da v413 ainda NAO existem; os insumos existem.
Grava CONFERENCIA_EXIGENCIAS_SERVICO_v413.json em DBN.SERVICO_DIR (nao sobrescreve). uso: V413_AUTORIZACAO_OPERADOR=<o texto que a gerencia passara aos recibos> python -I -B -X utf8 conferir_exigencias_servico_v413.py"""
import ast
import glob
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
IO = {"socket", "subprocess", "open", "urlopen", "load", "loads", "dump", "dumps", "replace", "run", "connect_ex", "write", "read", "glob", "isfile", "exists", "Popen",
      "livro_conferido", "processos_um_bancada", "porta_aberta", "get_json", "processo", "pid_da_porta", "ultimo_boot", "sha256_arquivo", "ler_json"}
ACRESCIMOS = {"recibo_parada_v413.py": ["modo", "autorizacao_conferida", "evidencia_fora_do_ar", "ultimo_boot"],
              "recibo_religamento_v413.py": ["modo_da_placa", "fala_do_modo_da_placa", "ambiente_do_processo", "log", "autorizacao_conferida", "processo"]}
REAIS = {"recibo_parada_v413.py": DBN.RECIBO_PARADA_V411, "recibo_religamento_v413.py": DBN.RECIBO_RELIGAMENTO_V411}
SAIDAS = {"recibo_parada_v413.py": "RECIBO_PARADA_v413.json", "recibo_religamento_v413.py": "RECIBO_RELIGAMENTO_v413.json"}
checks = []


def chk(nome, ok, observado, esperado=True):
    checks.append({"nome": nome, "ok": bool(ok), "observado": observado, "esperado": esperado})


def chamadas(no):
    out = []
    for n in ast.walk(no):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.append(f.id)
            elif isinstance(f, ast.Attribute):
                out.append(f.attr)
    return out


def corpo(nome):
    p = os.path.join(HERE, nome)
    txt = open(p, encoding="utf-8").read()
    return p, txt, ast.parse(txt)


def un(n):
    return ast.unparse(n).replace("'", '"')


def idx(mod, pred):
    return next((i for i, n in enumerate(mod) if pred(n)), None)


def e_assert_aut(n):
    return isinstance(n, ast.Assert) and isinstance(n.test, ast.Name) and n.test.id == "AUT"


def e_atrib_aut(n):
    return (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AUT" for t in n.targets) and un(n.value) == 'os.environ.get("V413_AUTORIZACAO_OPERADOR", "").strip()')


def chaves_do_rec(arv):
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and any(isinstance(t, ast.Name) and t.id == "rec" for t in n.targets):
            return [k.value for k in n.value.keys if isinstance(k, ast.Constant)]
    return None


def asserts_em(no):
    return [n for n in ast.walk(no) if isinstance(n, ast.Assert)]


# ---- o livro do quadro e a autorizacao (N4): lidos aqui para conferir o AUT do ambiente
try:
    LIVRO = U.livro_conferido(DBN.QUADRO)
    livro_ok = True
except Exception as e_:   # noqa: BLE001
    LIVRO, livro_ok = {"eventos": {}, "n_elos": 0}, False
E87, E89 = LIVRO["eventos"].get(DBN.SEQ_AUTORIZACAO) or {}, LIVRO["eventos"].get(DBN.SEQ_DECISAO) or {}
D87, D89 = E87.get("dados") or {}, E89.get("dados") or {}
ev_ok = (livro_ok and E87.get("tipo") == "AVISO_AUTORIZACAO_RECEBIDA" and D87.get("versao") == "v412" and D87.get("unidade") == "F0.6" and os.path.isfile(str(D87.get("recibo"))) and sha(D87["recibo"]) == D87.get("sha256")
         and E89.get("tipo") == "AVISO_DECISAO_DO_OPERADOR_B21" and E89.get("quem") == "claude-c1" and D89.get("em_resposta_ao_evento") == DBN.SEQ_AUTORIZACAO and os.path.isfile(str(D89.get("fala")))
         and sha(D89["fala"])[:16] == D89.get("fala_sha16") and DBN.UM_VERSION_BN in str(D89.get("decisao_do_operador")))
chk("o livro do quadro confere INTEIRO (2.2) e os eventos %d e %d sao o aviso da autorizacao do ciclo da Bancada (recibo pelo sha256 do evento) e a decisao do operador do salto na v413 (fala pelo sha16 do evento)"
    % (DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO), ev_ok, {"n_elos": LIVRO["n_elos"], "hash16": [str(E87.get("hash"))[:16], str(E89.get("hash"))[:16]]})
ORD16 = sha(D87["recibo"])[:16] if ev_ok else None
FRASE = str(json.loads(open(D87["recibo"], "rb").read().decode("utf-8"))["bench"]["answer"]).strip() if ev_ok else None
FALA_DEC16 = sha(D89["fala"])[:16] if ev_ok else None
DECISAO = str(D89.get("decisao_do_operador") or "").strip()
F20_OK = os.path.isfile(DBN.FALA_AUTORIZACAO_20NOV) and os.path.basename(DBN.FALA_AUTORIZACAO_20NOV).startswith("OPERADOR_20nov_")
F20 = open(DBN.FALA_AUTORIZACAO_20NOV, "rb").read().decode("utf-8").strip() if F20_OK else None
F20_16 = sha(DBN.FALA_AUTORIZACAO_20NOV)[:16] if F20_OK else None
chk("delta_bn: a fala de 20/11 (FALA_AUTORIZACAO_20NOV) existe em cunhagens_13out, e' de 20/11 pelo nome e fala da Bancada", F20_OK and F20 is not None and "bancada" in U.texto_normalizado(F20), DBN.FALA_AUTORIZACAO_20NOV)
AUT_AMB = os.environ.get("V413_AUTORIZACAO_OPERADOR", "").strip()
chk("o AUT que a gerencia passa (V413_AUTORIZACAO_OPERADOR no ambiente deste conferidor) traz: 'evento %d' e o hash16 dele, o sha16 e a resposta do recibo; 'evento %d' e o hash16 dele, o sha16 da fala e a decisao; a fala de 20/11 inteira e o sha16 dela"
    % (DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO),
    bool(AUT_AMB) and ev_ok and F20_OK and ("evento %d" % DBN.SEQ_AUTORIZACAO) in AUT_AMB and str(E87.get("hash"))[:16] in AUT_AMB and ORD16 in AUT_AMB and FRASE in AUT_AMB
    and ("evento %d" % DBN.SEQ_DECISAO) in AUT_AMB and str(E89.get("hash"))[:16] in AUT_AMB and FALA_DEC16 in AUT_AMB and DECISAO in AUT_AMB and F20 in AUT_AMB and F20_16 in AUT_AMB,
    {"tem_AUT": bool(AUT_AMB), "ordem_sha16": ORD16, "fala_decisao_sha16": FALA_DEC16, "fala_20nov_sha16": F20_16})
chk("delta_bn: as seqs da autorizacao sao 1687 e 1689 (ORDEM_BN_v413.md, N4) e o sandbox curto e' C:\\t\\vb24 (pasta nova, N8)", DBN.SEQ_AUTORIZACAO == 1687 and DBN.SEQ_DECISAO == 1689
    and os.path.normcase(DBN.SANDBOX_CURTO) == os.path.normcase(os.path.join("C:" + os.sep, "t", "vb24")), [DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO, DBN.SANDBOX_CURTO])

arquivos = {}
for nome in ("recibo_parada_v413.py", "recibo_religamento_v413.py"):
    p, txt, arv = corpo(nome)
    arquivos[nome] = {"path": p, "sha256": sha(p), "bytes": os.path.getsize(p)}
    mod = arv.body
    i_atrib, i_assert = idx(mod, e_atrib_aut), idx(mod, e_assert_aut)
    chk(nome + ": ha a atribuicao AUT = os.environ.get(V413_AUTORIZACAO_OPERADOR).strip()", i_atrib is not None, i_atrib)
    chk(nome + ": o assert AUT vem logo depois da atribuicao (sem nada entre)", i_atrib is not None and i_assert == i_atrib + 1, [i_atrib, i_assert])
    antes = mod[:i_assert] if i_assert is not None else mod
    io_antes = sorted({c for n in antes for c in chamadas(n) if c in IO})
    chk(nome + ": nenhuma chamada de E/S antes do assert AUT (so imports, D e AUT)", i_assert is not None and not io_antes, io_antes, [])
    chk(nome + ": V413_AUTORIZACAO_OPERADOR aparece 2 vezes (leitura e mensagem do assert)", txt.count("V413_AUTORIZACAO_OPERADOR") == 2, txt.count("V413_AUTORIZACAO_OPERADOR"), 2)
    chk(nome + ": nenhum nome da v412 sobrou (V412_AUTORIZACAO_OPERADOR, V412_PARADA, V412_PID_PARADO, RECIBO_*_v412.json, bancada_B3_servico da v412)",
        not any(x_ in txt for x_ in ("V412_AUTORIZACAO_OPERADOR", "V412_PARADA", "V412_PID_PARADO", "RECIBO_PARADA_v412.json", "RECIBO_RELIGAMENTO_v412.json", "RECIBO_SINCRONIZACAO_v412_")), True)
    chk(nome + ": grava so' em %s (em DBN.SERVICO_DIR) e recusa sobrescrever (assert not os.path.exists(P_REC))" % SAIDAS[nome],
        ('P_REC = os.path.join(DBN.SERVICO_DIR, "%s")' % SAIDAS[nome]) in txt and "assert not os.path.exists(P_REC)" in txt, True)
    k_novo, k_real = chaves_do_rec(arv), list(json.load(open(REAIS[nome], encoding="utf-8")).keys()) + ACRESCIMOS[nome]
    chk(nome + ": chaves do dict rec (ordem) = as do recibo REAL da v411 + os acrescimos da v413", k_novo == k_real, [k_novo, k_real], "listas iguais")
    i_livro = idx(mod, lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "LIVRO" for t in n.targets) and un(n.value) == "U.livro_conferido(DBN.QUADRO)")
    sem_leitor_proprio = not any(isinstance(n, ast.FunctionDef) and n.name in ("evento", "livro", "eventos") for n in ast.walk(arv)) and "eventos.jsonl" not in txt and "QUADRO =" not in txt
    chk(nome + ": 2.2: o livro do quadro e' conferido INTEIRO por U.livro_conferido(DBN.QUADRO), depois do assert AUT, e o script nao tem leitor proprio de eventos (que pularia linha ilegivel)",
        i_livro is not None and i_assert is not None and i_assert < i_livro and sem_leitor_proprio, [i_assert, i_livro, sem_leitor_proprio])
    i_s87 = idx(mod, lambda n: isinstance(n, ast.Assert) and 'hashlib.sha256(ORDEM_BYTES).hexdigest() == D87["sha256"]' in un(n.test))
    i_s89 = idx(mod, lambda n: isinstance(n, ast.Assert) and 'FALA_DECISAO_SHA16 == D89.get("fala_sha16")' in un(n.test))
    i_cont = idx(mod, lambda n: isinstance(n, ast.Assert) and all(x_ in un(n.test) for x_ in ("H87 in AUT", "H89 in AUT", "ORDEM_SHA16 in AUT", "FRASE_DA_ORDEM in AUT", "FALA_DECISAO_SHA16 in AUT", "DECISAO in AUT", "FALA_20NOV in AUT", "FALA_20NOV_SHA16 in AUT")))
    chk(nome + ": N4: o recibo do evento %d pelo sha256 que o evento registra, a fala do %d pelo fala_sha16, a fala de 20/11 lida por bytes; o assert do CONTEUDO do AUT (hash16 dos dois eventos, sha16, resposta, decisao, fala de 20/11) vem DEPOIS"
        % (DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO), None not in (i_livro, i_s87, i_s89, i_cont) and i_livro < i_s87 < i_s89 < i_cont and "open(DBN.FALA_AUTORIZACAO_20NOV, \"rb\")" in txt
        and "H87, H89 = E87[\"hash\"][:16], E89[\"hash\"][:16]" in txt, [i_livro, i_s87, i_s89, i_cont])
    chk(nome + ": nenhuma data dd/mm/aaaa nem hash de 16+ hex digitado no script", U.RX_DATA_BR.search(txt) is None and re.search(r"[0-9a-f]{16}", txt) is None,
        [U.RX_DATA_BR.findall(txt), re.findall(r"[0-9a-f]{16,}", txt)], [[], []])
    chk(nome + ": o recibo da v413 ainda nao existe (nada foi executado)", not os.path.exists(os.path.join(DBN.SERVICO_DIR, SAIDAS[nome])), os.path.exists(os.path.join(DBN.SERVICO_DIR, SAIDAS[nome])), False)
    if nome == "recibo_parada_v413.py":
        chk(nome + ": N6: le o religamento da v411 (DBN.RECIBO_RELIGAMENTO_V411: pid e no_ar_desde); no pelo_pid o PID vem de V413_PID_PARADO e V413_PID_PARADO_CRIADO",
            "json.load(open(DBN.RECIBO_RELIGAMENTO_V411" in txt and 'rel411["no_ar_desde"]' in txt and 'os.environ.get("V413_PID_PARADO", "")' in txt and 'os.environ.get("V413_PID_PARADO_CRIADO", "")' in txt, True)
        i_modo = idx(mod, lambda n: isinstance(n, ast.Assert) and un(n.test) == 'MODO in ("pelo_pid", "ja_fora_do_ar")')
        i_sock = idx(mod, lambda n: isinstance(n, ast.Assign) and "socket.socket()" in un(n.value))
        chk(nome + ": o modo da parada e' escolhido por V413_PARADA (pelo_pid | ja_fora_do_ar) e nunca presumido: o assert do modo vem DEPOIS do conteudo do AUT e ANTES da sonda da porta",
            'os.environ.get("V413_PARADA", "").strip()' in txt and None not in (i_cont, i_modo, i_sock) and i_cont < i_modo < i_sock, [i_cont, i_modo, i_sock])
        ramo = next((n for n in mod if isinstance(n, ast.If) and un(n.test) == 'MODO == "pelo_pid"'), None)
        senao = ast.Module(body=(ramo.orelse if ramo else []), type_ignores=[])
        a_senao = [un(a_.test) for a_ in asserts_em(senao)]
        chk(nome + ": no ja_fora_do_ar nao finge parada: recusa V413_PID_PARADO e V413_PID_PARADO_CRIADO no ambiente (M7)",
            any('not os.environ.get("V413_PID_PARADO", "").strip()' in t_ and 'not os.environ.get("V413_PID_PARADO_CRIADO", "").strip()' in t_ for t_ in a_senao), a_senao[:2])
        chk(nome + ": no ja_fora_do_ar a conferencia A (V413_SAUDE_RECIBO) e' conferida pelo sha256 que a gerencia passa (V413_SAUDE_SHA256) (M8)",
            any(t_ == "hashlib.sha256(SA_BYTES).hexdigest() == SA_PINO" for t_ in a_senao) and 'os.environ.get("V413_SAUDE_SHA256", "")' in txt, [t_ for t_ in a_senao if "SA_" in t_][:3])
        chk(nome + ": no ja_fora_do_ar o ultimo PID conhecido tem de estar AUSENTE ou ser outro programa, nunca VIVO com um_bancada (M9)",
            any(t_ == 'ULT == "AUSENTE" or (ULT.startswith("VIVO|") and "um_bancada" not in ULT)' for t_ in a_senao), [t_ for t_ in a_senao if "ULT" in t_])
        chk(nome + ": o recibo diz que nada foi parado no ja_fora_do_ar", "NADA foi parado por esta cadeia" in txt and "nenhum PID foi parado" in txt, True)
    else:
        chk(nome + ": 2.3: o recibo do APLICAR e' achado tambem numa repeticao (bancada_B3 e bancada_B3_[0-9]*), so' com o veredito do APLICAR do salto e exatamente 1 com o manifesto novo == o do disco",
            '"bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json"' in txt and '"bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_%s_*.json"' in txt and 'j_.get("veredito") == DBN.VEREDITO_APLICAR' in txt
            and 'get("sha256") == MAN_DISCO' in txt and "assert len(APLICADOS) == 1" in txt, True)
        chk(nome + ": confere o deployment servido contra o do APLICAR (DBN.RE_DEPLOYMENT_NOVO), a versao servida (DBN.UM_VERSION_BN) e o anterior da Bancada (o B20, N6)",
            "DBN.RE_DEPLOYMENT_NOVO.match(dep_esp)" in txt and '("deployment_id", dep_esp)' in txt and '("canonical_version", DBN.UM_VERSION_BN)' in txt and 'ma["deployment_id"] == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"]' in txt, True)
        i_aguarda = idx(mod, lambda n: isinstance(n, ast.If) and "FALA_MODO_NOME" in un(n.test) and "sys.exit(20)" in un(n))
        i_fala = idx(mod, lambda n: isinstance(n, ast.Assert) and "FALA_MODO in AUT" in un(n.test) and 'modo da placa: %s' in un(n.test))
        i_prec = idx(mod, lambda n: isinstance(n, ast.Assert) and un(n.test) == "not os.path.exists(P_REC)")
        i_popen = idx(mod, lambda n: "subprocess.Popen" in un(n))   # o primeiro comando de modulo que lanca (o try do breakaway, B9)
        chk(nome + ": o modo da placa (V413_MODO_PLACA em DBN.MODOS_DA_PLACA) e a fala dele (V413_FALA_MODO_PLACA; sem ela, sys.exit(20), AGUARDA), conferida no AUT com o modo, e o recibo existente vem ANTES do lancamento",
            None not in (i_aguarda, i_fala, i_prec, i_popen) and i_cont < i_aguarda < i_fala < i_prec < i_popen and 'os.environ.get("V413_MODO_PLACA", "")' in txt and 'os.environ.get("V413_FALA_MODO_PLACA", "")' in txt,
            [i_cont, i_aguarda, i_fala, i_prec, i_popen])
        chk(nome + ": no modo cpu o processo lancado recebe CUDA_VISIBLE_DEVICES=-1; no normal a variavel sai do ambiente dele", 'AMB["CUDA_VISIBLE_DEVICES"] = "-1"' in txt and 'AMB.pop("CUDA_VISIBLE_DEVICES", None)' in txt
            and "env=AMB" in txt, True)
        chk(nome + ": o processo lancado nao herda variaveis PYTHON* (retiradas e registradas, B7) e o lancamento tenta sair do Job da sessao (CREATE_BREAKAWAY_FROM_JOB, com o resultado no recibo, B9)",
            "AMB.pop(v_, None)" in txt and '"PYTHONPATH"' in txt and "CREATE_BREAKAWAY_FROM_JOB" in txt and '"breakaway": BREAKAWAY' in txt, True)
        chk(nome + ": N9: o lancamento anexa o stdout e o stderr a DBN.LOG_SERVIDOR e DBN.LOG_SERVIDOR_ERROS (open 'ab'), destacado, e o recibo registra o log",
            'open(DBN.LOG_SERVIDOR, "ab")' in txt and 'open(DBN.LOG_SERVIDOR_ERROS, "ab")' in txt and "DETACHED_PROCESS" in txt and '"log": LOG' in txt, True)
        chk(nome + ": a identidade vem SO' de /api/contratos (nenhuma leitura de /api/estado, que cria contexto CUDA)", "/api/contratos" in txt and "/api/estado\"" not in txt.replace("'", '"') and "api/estado\"" not in txt, True)
        chk(nome + ": o PID da porta tem de ser o lancado e o um_bancada.py", "PID_PORTA != PID_LANCADO" in txt and '"um_bancada.py" not in PROC_INFO.get("linha_de_comando", "")' in txt, True)

# ---- o evento (2.6)
pe, te, ae = corpo("evento_c1_b3_v413.py")
arquivos["evento_c1_b3_v413.py"] = {"path": pe, "sha256": sha(pe), "bytes": os.path.getsize(pe)}
me = ae.body
i_ens = idx(me, lambda n: isinstance(n, ast.Assert) and "os.path.isfile(ENSAIO_OUT)" in un(n.test))
i_b3 = idx(me, lambda n: isinstance(n, ast.Assign) and "subprocess.run" in un(n.value) and "b3_recibo_v413.py" in un(n.value))
i_b3ok = idx(me, lambda n: isinstance(n, ast.Assert) and un(n.test) == "RR.returncode == 0")
i_esp = idx(me, lambda n: isinstance(n, ast.Assert) and "os.path.isfile(ESP)" in un(n.test))
i_cand = idx(me, lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAND16" for t in n.targets))
i_conf = idx(me, lambda n: isinstance(n, ast.Assert) and "startswith(CAND16)" in un(n.test))
i_run = idx(me, lambda n: isinstance(n, ast.Assign) and "subprocess.run" in un(n.value) and "anotar" in un(n.value))
i_rc = idx(me, lambda n: isinstance(n, ast.Assert) and un(n.test) == "r.returncode == 0")
i_print = idx(me, lambda n: isinstance(n, ast.Expr) and "EVENTO=%d EVENTO_HASH=%s" in un(n))
chk("evento (2.6): assert do stdout do ENSAIO < b3_recibo do ensaio < assert rc 0 dele < assert os.path.isfile(ESP) < CAND16 < assert startswith(CAND16) < subprocess.run (anotar) < assert rc 0 do iald.py < print EVENTO=",
    None not in (i_ens, i_b3, i_b3ok, i_esp, i_cand, i_conf, i_run, i_rc, i_print) and i_ens < i_b3 < i_b3ok < i_esp < i_cand < i_conf < i_run < i_rc < i_print,
    [i_ens, i_b3, i_b3ok, i_esp, i_cand, i_conf, i_run, i_rc, i_print], "ordem crescente")
i_ja = idx(me, lambda n: isinstance(n, ast.If) and un(n.test) == "JA" and "sys.exit(0)" in un(n))
chk("evento (B6): nunca anota duas vezes: antes do subprocess que anota, procura no livro conferido o elo da claude-c1 com os mesmos dados depois do fim do ensaio e, se ha', devolve EVENTO= dele e sai sem anotar",
    None not in (i_conf, i_ja, i_run) and i_conf < i_ja < i_run and 'e_.get("dados") == dados and U.instante(e_["quando"]) > FIM_ENSAIO' in te, [i_conf, i_ja, i_run])
dados_ = next((n.value for n in me if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "dados" for t in n.targets) and isinstance(n.value, ast.Dict)), None)
chaves_dados = [k.value for k in dados_.keys] if dados_ is not None else None
chk("evento: dados com versao DBN.UM_VERSION_BN, acao sincronizacao, unidade F0.6, tipo SINCRONIZACAO_BANCADA, e chaves no conjunto fechado do esboco",
    chaves_dados is not None and set(chaves_dados) <= {"versao", "bancada", "acao", "um_py", "selo", "reparo", "gravacoes", "unidade", "nota"} and '"versao": DBN.UM_VERSION_BN' in te
    and '"acao": "sincronizacao"' in te and '"unidade": "F0.6"' in te and '"SINCRONIZACAO_BANCADA"' in te, chaves_dados)
chk("evento: le o retorno {ok, evento, hash} do iald.py, confere o elo no livro conferido INTEIRO e exige o evento POSTERIOR ao fim do recibo do ensaio",
    "U.livro_conferido(DBN.QUADRO)" in te and 'E.get("dados") == dados' in te and 'U.instante(E["quando"]) > U.instante(U.ler_json(REC_ENSAIO)["fim_utc"])' in te, True)
chk("evento: nenhum hash literal (16 a 64 hex entre aspas) e nenhuma data dd/mm/aaaa", re.search(r'"[0-9a-f]{16,64}"', te) is None and U.RX_DATA_BR.search(te) is None, re.findall(r'"[0-9a-f]{16,64}"', te), [])
chk("evento: V413_AUTORIZACAO_OPERADOR nao e' usada (o evento nao exige a variavel; so' parada e religamento)", "V413_AUTORIZACAO_OPERADOR" not in te, "V413_AUTORIZACAO_OPERADOR" in te, False)

# ---- o util (M11): o livro conferido inteiro
pu, tu, au = corpo("util_bn_v413.py")
arquivos["util_bn_v413.py"] = {"path": pu, "sha256": sha(pu), "bytes": os.path.getsize(pu)}
fl = next((n for n in au.body if isinstance(n, ast.FunctionDef) and n.name == "livro_conferido"), None)
tries = [n for n in ast.walk(fl)] if fl else []
try_json = [n for n in tries if isinstance(n, ast.Try) and any("json.loads" in un(b_) for b_ in n.body)]
handler_levanta = bool(try_json) and all(any(isinstance(x_, ast.Raise) for x_ in ast.walk(h_)) and not any(isinstance(x_, (ast.Continue, ast.Pass)) for x_ in ast.walk(h_)) for t_ in try_json for h_ in t_.handlers)
chk("util (M11): livro_conferido: o json.loads de cada linha fica num try cujo except LEVANTA (nunca continue/pass); confere anterior == o hash anterior e hash == o recalculado; recusa seq repetida",
    fl is not None and handler_levanta and 'e.get("anterior") != ant' in un(fl) and 'e.get("hash") != hash_evento(e)' in un(fl) and "EVENTO_SEQ_DUPLICADO" in un(fl), {"tem_funcao": fl is not None, "except_levanta": handler_levanta})
fh_ = next((n for n in au.body if isinstance(n, ast.FunctionDef) and n.name == "hash_evento"), None)
_regra_hash = un(ast.parse('json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True)').body[0].value)   # a forma canonica pelo mesmo unparse (independe da versao do Python)
chk("util: hash_evento = sha256 do JSON (sort_keys, ensure_ascii False) do elo sem o campo hash (a regra do iald.py e do esboco)", fh_ is not None and _regra_hash in un(fh_), True)

# ---- insumos
rel = DBN.RECIBO_RELIGAMENTO_V411
chk("insumo da parada (N6): RECIBO_RELIGAMENTO_v411.json existe, e' da porta do delta e traz pid, no_ar_desde e hora_recibo", os.path.isfile(rel) and (lambda d_: d_.get("porta") == DBN.PORTA and str(d_.get("pid", "")).isdigit()
    and bool(d_.get("no_ar_desde")) and bool(d_.get("hora_recibo")))(json.load(open(rel, encoding="utf-8"))), rel)
bn13 = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)) + glob.glob(os.path.join(DBN.V413, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)))
chk("o recibo do APLICAR da v413 ainda nao existe (v413\\bancada_B3 e bancada_B3_<k> sem RECIBO_SINCRONIZACAO_v413_*; a pasta do ENSAIO, bancada_B3_ensaio_*, nao conta)", len(bn13) == 0, [os.path.basename(x) for x in bn13], [])
res = {"contrato": "CONFERENCIA_EXIGENCIAS_SERVICO_v413", "como": "so leitura (ast + texto; o livro do quadro, os recibos de entrada e as falas lidos); nada foi executado; a producao nao foi tocada",
       "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))}, "arquivos": arquivos,
       "autorizacao": {"eventos": [DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO], "hash16": [str(E87.get("hash"))[:16], str(E89.get("hash"))[:16]], "recibo_sha16": ORD16, "resposta": FRASE, "fala_decisao_sha16": FALA_DEC16,
                       "decisao": DECISAO, "fala_20nov": {"arquivo": DBN.FALA_AUTORIZACAO_20NOV, "sha16": F20_16, "fala": F20}},
       "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]), "escopo": "NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
os.makedirs(DBN.SERVICO_DIR, exist_ok=True)
dest = os.path.join(DBN.SERVICO_DIR, "CONFERENCIA_EXIGENCIAS_SERVICO_v413.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("%d/%d condicoes ok" % (res["n_condicoes_ok"], res["n_condicoes"]))
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["nome"][:160], str(c["observado"])[:300])
print(dest, sha(dest)[:16])
sys.exit(0 if res["n_condicoes_ok"] == res["n_condicoes"] else 1)
