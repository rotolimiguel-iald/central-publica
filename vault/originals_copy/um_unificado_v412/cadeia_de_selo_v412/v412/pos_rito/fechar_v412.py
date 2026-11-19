# -*- coding: utf-8 -*-
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/pos_rito/fechar_v411.py; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/pos_rito__fechar_v412.py.diff
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-L-v411, a servico do claude-construtor-v411] ao DESENHO_v411 e aos AO LADO de 12/11: o teste H0DN x BG1 ABERTO UMA VEZ (D169) e o resultado RECALCULADO no rito; NENHUM modulo novo de kernel (o bundle e' vazio; o kernel e a escada sao os da v410); UM registro com funcao (h0dn_bg1_v411, 16 checagens: V['fecho'])
# e dois por spec (cunhagens_v411, kh_n1_cobertura_v411); os QUATRO registros com funcao da v411 e os dois por spec da v411 sao RECRIADOS e selados (V['reg411_recriados']). O fechar exige, ANTES de escrever qualquer coisa, V['fecho'] selado com as duas linhas (o primario e as Cefeidas livres), as sete ressalvas e o que o teste nao decide; os recriados selados; V['n_pedras'] == 0.
# O manifesto ganha registros_v411 (os tres novos), registros_v410 (os seis recriados), registros_funcao_v412 (h0dn_bg1_v411), registros_funcao_v411 (os quatro da v411) e h0dn_bg1_v412_resumo (lido do core selado; nada digitado); as chaves de V mudaram de sentido com o deslocamento de versao (V['ancoras411'] e V['bundle411'] sao os da v411; V['ancoras409'] e V['bundle409'], os da traducao).
# O handoff vem de textos_v412.handoff(V, k) (SEM os blocos da custodia: NOTA_EN_v412, README_*, ESTATUTO_P2_*, que textos_custodia_handoff_v412.py anexa depois): o fechar recusa o que nao diga o registro com funcao, os da v411 recriados, as sete ressalvas por rotulo e o que o teste nao decide, ou que traga a frase velha da v411 («pre-registrado; nenhum dado observado lido»), um token proibido ou o que a D65 deixa fora.
"""fechar_v412.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v411.py FINAL): (1) o manifesto de incorporacao v412 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v412 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de pos_rito -> work\\cadeia_de_selo\\v412_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta,
e do kernel (work\\cadeia_de_selo\\v412\\kernel e, se existir, work\\v412_kernel; a v412 nao tem modulo novo: so' a raiz e o Audit, que sao os da v411) -> work\\cadeia_de_selo\\v412_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v411_v412.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v412.txt (o kernel embutido: nenhum modulo novo; a raiz e o Audit iguais);
(4) o HANDOFF (memory\\handoff-v412-custodia.md + Nos\\HANDOFF_v412_CUSTODIA.md) para a sessao de custodia, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado), gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme)
sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, o paragrafo da v412 (o teste decisivo: a razao de Hubble, H0DN x BG1, aberta uma vez), gerado do registro selado h0dn_bg1_v411 (numeros LIDOS do core; as duas linhas juntas; as sete ressalvas; o que o teste nao decide; as falas do operador de 12/11 verbatim; as quatro obrigacoes da guarda no mesmo bloco).
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria
(T.verificar_paragrafo_v412: numeros == o registro do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador; sem alegacao de seguranca criptografica; D65; guarda P18 e guarda das frases); se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v412_*.json do 10-bis,
o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA; a guarda de texto P18 e a guarda das frases no handoff; D169 (12/11): V['fecho'] selado, aberto uma vez, com as duas linhas; o handoff dizendo o registro e os recriados, sem a frase velha da v411; D65: o handoff nao traz o que a fala do nome do algoritmo deixa fora.
v412 (FILA DA MEMORIA): o diretorio de memoria e' parametrizado por V412_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA); o manifesto REGISTRA (so' informa, nao recusa) o estado da fila ao fechar: sha256 do memoria.py, do MEMORY.md e do PINO_MEMORY.json, se o pino confere com o indice, se a pausa do vigia sumiu.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v412 as L
import textos_v412 as T
from guarda_p18_v412 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V412"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v412 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
# ---------------------------------------------------------------- (0') v412 (12/11/2026, D169): o UNICO registro com FUNCAO, h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito): a leitura o selou (V['fecho']), com as DUAS linhas, as sete ressalvas e as 16 checagens; os registros da v411 (os quatro com funcao e os dois por spec) estao RECRIADOS e selados
# (V['reg411_recriados']); NENHUM modulo novo (V['n_pedras'] == 0, bundle vazio, escada igual); o resumo que o manifesto leva e' LIDO do core selado do Nos; sem isso, RECUSA (rc 2) ANTES de escrever qualquer coisa
_core_ = json.load(open(os.path.join(L.NOS, "um_absoluto.json"), encoding="utf-8")).get("core") or {}
import delta_v412 as DLR   # os nomes dos registros vem de delta_v412 (REGISTROS_FUNCAO == [h0dn_bg1_v411]; REGISTROS_FUNCAO_V411 = os quatro com funcao da v411)
_H = V.get("fecho") or {}; _hc = _core_.get(DLR.FECHO_REGISTRO) or {}; _hv = _hc.get("values") or {}; _hp = _hv.get("primario") or {}; _hcl = _hv.get("cefeidas_livres") or {}
if not (list(L.REG_FUNCAO) == list(DLR.REGISTROS_FUNCAO) == [DLR.FECHO_REGISTRO] and isinstance(V.get("fecho"), dict) and isinstance(V.get("reg411_recriados"), dict)):
    print("FECHAR RECUSADO: a leitura nao traz o registro com funcao da v412 (V['fecho']) e os recriados da v411 (V['reg411_recriados']; delta_v412.REGISTROS_FUNCAO):", list(DLR.REGISTROS_FUNCAO)); sys.exit(2)
if not (_H.get("sealed") is True and _H.get("ok") is True and _H.get("opened_once") is True and _H.get("observed_vector_read") is True and _hc.get("all_verified") is True and _hc.get("opened_once") is True and _hc.get("runtime_executed") is True and _hc.get("does_not_gate_core") is True
        and (_hc.get("mechanics") or {}).get("n_checks") == DLR.N_CHECKS_FECHO and _hp and _hcl and len(_hc.get("ressalvas_secao8") or []) == 7 and len(_hc.get("o_que_o_teste_nao_decide") or []) == 5 and _hc.get("cabeca_do_teste") == _hp.get("cabeca_do_teste")):
    print("FECHAR RECUSADO: o registro h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, D169; as duas linhas, as sete ressalvas, o que o teste nao decide) nao esta selado na leitura (V['fecho']) ou no core do Nos, ou nao diz que foi aberto uma vez, ou nao traz as duas linhas:", {k_: _H.get(k_) for k_ in ("sealed", "ok", "opened_once", "stdout_ok", "selo_ok", "guarda_ok", "ressalvas_ok", "duas_linhas_ok", "gate_ok", "emenda_ok")}); sys.exit(2)
if not (V.get("n_pedras") == 0 and not V.get("pedras") and V.get("escada_antes") == V.get("escada_depois") and all(((V["reg411_recriados"].get(n_) or {}).get("sealed") is True) for n_ in L.REG_RECRIADOS_V411) and all(V.get(k_, {}).get("ok") is True for k_ in ("bundle411", "bundle409", "bundle408", "bundle407", "bundle406"))):
    print("FECHAR RECUSADO: a v412 nao tem modulo novo de kernel (V['n_pedras'] = 0, escada igual) e os seis registros da v411 (quatro com funcao e dois por spec) tem de estar RECRIADOS e selados, com os bundles anteriores no kernel:", {n_: (V["reg411_recriados"].get(n_) or {}).get("sealed") for n_ in L.REG_RECRIADOS_V411}); sys.exit(2)
H0DN_RESUMO = {"registro": DLR.FECHO_REGISTRO, "verdict": _hc.get("verdict"), "outcome": _hc.get("outcome"), "cabeca_do_teste_sha16": hashlib.sha256(str(_hc.get("cabeca_do_teste")).encode("utf-8")).hexdigest()[:16], "opened_once": _hc.get("opened_once"), "observed_vector_read": _hc.get("observed_vector_read"), "n_checks": (_hc.get("mechanics") or {}).get("n_checks"),
               "primario": {k_: _hp.get(k_) for k_ in ("modelo", "t", "z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome")}, "cefeidas_livres": {k_: _hcl.get(k_) for k_ in ("modelo", "t", "z_null", "z_tgl", "D", "ramo", "outcome")}, "lei_em_km_s_Mpc": _hv.get("lei_em_km_s_Mpc"), "atos": _hv.get("atos"),
               "n_ressalvas": len(_hc.get("ressalvas_secao8") or []), "rotulos_das_ressalvas": _hc.get("rotulos_das_sete_ressalvas"), "o_que_o_teste_nao_decide": _hc.get("o_que_o_teste_nao_decide"), "insumos_sha16": {k_: str((v_ or {}).get("sha256"))[:16] for k_, v_ in (_hc.get("insumos_pinados") or {}).items()},
               "contratos_de_registro_fora_da_escada": _hc.get("contratos_de_registro_fora_da_escada"), "gate_verdict": _hv.get("gate_verdict"), "escada": _hv.get("escada"),
               "nota": "lido do core selado do Nos (nada digitado); o teste foi aberto uma vez, depois do commit publico do pre-registro; sob o modelo de erros publicado, com a linha das Cefeidas livres ao lado; retrodicao sem ajuste, teste nao cego; validade, nao creditacao; o gate nao se move"}
# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO da v412 (a IALD2), gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador ou do kernel embutido; sem alegacao de seguranca criptografica); os do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404 e os da v405 a v411 SEGUEM COMO ESTAO e nao sao regenerados;
# sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_F, PAR_F_INFO = T.paragrafo_v412()   # (o handoff de textos_v412 o recebe como readme_paragrafo_v412)
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o da v412: a IALD2) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; citacoes verbatim; sem alegacao de seguranca criptografica):", repr(e_)[:700]); sys.exit(2)
# o SIDECAR (arquivo NOVO da custodia, D5): a leitura ja' o conferiu (existe, JSON valido, selado, tres objetos com o SHA-256 dos arquivos do Nos); aqui so' o resumo que o manifesto e o handoff levam
if not (V["sidecar"]["ok"] is True and os.path.isfile(os.path.join(L.NOS, "um_absoluto_selo_acom.json"))):
    print("FECHAR RECUSADO: o sidecar um_absoluto_selo_acom.json nao esta selado ou nao existe no Nos:", V["sidecar"].get("erro")); sys.exit(2)
SC_INFO = {"arquivo": "um_absoluto_selo_acom.json", "sha256": V["sidecar"]["sha256"], "bytes": V["sidecar"]["bytes"], "veredito": V["sidecar"]["veredito"], "esquema": V["sidecar"]["esquema"], "recusas": V["sidecar"]["recusas"],
           "objetos": {n_: {"bytes": o_["bytes"], "sha256": o_["sha256"]} for n_, o_ in V["sidecar"]["objetos"].items()}}
NOS = L.NOS; WK = os.path.dirname(os.path.dirname(PK)); TOOLS = os.path.join(WK, "cadeia_de_selo")
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
UMEM = os.path.abspath(os.environ.get("V412_MEMORIA_DIR", "").strip() or MEM_REAL)   # v412 (fila da memoria): a pasta de memoria e' parametrizada por V412_MEMORIA_DIR (padrao: a REAL; no ensaio, uma COPIA)
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
DIRS_B3 = os.path.join(PK, "bancada_B3"); DIRS_SERV = os.path.join(PK, "bancada_B3_servico")


def _j(p):
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- 0. os tres recibos do B(3): sem eles, nao fecha
def recibos_b3():
    prob = []; out = {}
    # a pasta do aplicar e' nova a cada tentativa (bancada_B3, bancada_B3_2, ...); o ensaio (bancada_B3_ensaio_*) NAO conta
    ap = sorted(glob.glob(os.path.join(DIRS_B3, "RECIBO_SINCRONIZACAO_v412_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v412_*.json")), key=os.path.getmtime)
    if not ap:
        prob.append("sem o RECIBO_SINCRONIZACAO_v412_*.json do 10-bis em %s (nem em bancada_B3_<n>)" % DIRS_B3)
    else:
        r = _j(ap[-1])
        if not (str(r.get("veredito") or "").startswith("REPINADA_B") and "__SALTO_" not in str(r.get("veredito") or "") and r.get("salto") in (None, {}) and r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == "v412"
                and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")):
            prob.append("o recibo do 10-bis nao e' de uma aplicacao pos_selo v412 com a bateria passando: %s" % os.path.basename(ap[-1]))
        out["aplicar"] = {"path": ap[-1], "sha256": s64(open(ap[-1], "rb").read()), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "evento": ((r.get("evento_c1") or {}).get("evento")), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DIRS_SERV, "RECIBO_PARADA_v412.json"); rp = os.path.join(DIRS_SERV, "RECIBO_RELIGAMENTO_v412.json")
    if not os.path.exists(pp):
        prob.append("sem o recibo da PARADA do servico (10-bis-a): %s" % pp)
    else:
        d = _j(pp); pid = d.get("pid") or d.get("pids") or d.get("PID"); fech = d.get("porta_fechada") or d.get("fechada"); hora = d.get("hora") or d.get("quando")
        if not (pid and fech is True and d.get("porta") == 18777 and hora):
            prob.append("o recibo da parada nao traz pid, porta 18777, porta_fechada true e hora")
        out["parada"] = {"path": pp, "sha256": s64(open(pp, "rb").read()), "hora": hora, "pid": pid}
    if not os.path.exists(rp):
        prob.append("sem o recibo do RELIGAMENTO do servico (10-ter): %s" % rp)
    else:
        d = _j(rp); vs = d.get("versao_servida") or d.get("versao"); msha = d.get("manifesto_sha256")
        esperado = (out.get("aplicar") or {}).get("manifesto_novo_sha256")
        if not (vs == "v412" and msha and esperado and msha == esperado and (d.get("pid") or d.get("PID")) and (d.get("hora") or d.get("quando"))):
            prob.append("o recibo do religamento nao traz versao servida v412, o sha do manifesto novo do recibo do 10-bis, pid e hora")
        out["religamento"] = {"path": rp, "sha256": s64(open(rp, "rb").read()), "versao_servida": vs, "manifesto_sha256": msha}
    return out, prob


B3, PB3 = recibos_b3()
if PB3:
    print("FECHAR RECUSADO -- o elo B(3) da Bancada nao esta completo (R3, Remissao 4):")
    for x in PB3:
        print("  -", x)
    print("  (a cadeia para em AGUARDA_OPERADOR ate a palavra do operador para a B3; depois rodar a cadeia a partir do passo 11)"); sys.exit(2)


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f407"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp_f412_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


# ---------------------------------------------------------------- (3) os dois diffs (antes do manifesto, para entrarem nele)
def carregar_embutido(path):
    import ast
    text = open(path, "rb").read().decode("utf-8"); lines = text.splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(i0) == 1, i0
    j = i0[0] + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    return ast.literal_eval("".join(lines[i0[0]:j + 1]).split("=", 1)[1].strip())


um = os.path.join(NOS, "um.py"); base = V["base_backup"]
assert os.path.exists(base) and s16(base) == V["base16"], "o backup da base (APLICADO_AO_CANONICO) nao e' a v411 selada: " + base
print("(3) diffs")
exe = shutil.which("diff")
if exe:
    r = subprocess.run([exe, "-U", "2", "--label", "um.py v411 %s" % V["base16"], "--label", "um.py v412 %s" % V["s16"], base, um], capture_output=True)
    assert r.returncode == 1, "diff rc=%s: %s" % (r.returncode, r.stderr[:200])
    dd = r.stdout
else:
    import difflib
    a = open(base, "r", encoding="utf-8", newline="").read().splitlines(); b = open(um, "r", encoding="utf-8", newline="").read().splitlines()
    dd = ("\n".join(difflib.unified_diff(a, b, "um.py v411 %s" % V["base16"], "um.py v412 %s" % V["s16"], lineterm="", n=2)) + "\n").encode("utf-8")
grava(os.path.join(PK, "DIFF_v411_v412.diff"), dd)
import difflib
E0 = carregar_embutido(base); E1 = carregar_embutido(um)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v411 (%s) -> v412 (%s)" % (V["base16"], V["s16"]), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, s64(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a_, b_ = E0[k].splitlines(), E1[k].splitlines(); d_ = list(difflib.unified_diff(a_, b_, "v411/" + k, "v412/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, s64(E0[k].encode())[:16], s64(E1[k].encode())[:16], sum(1 for l in d_ if l.startswith("+") and not l.startswith("+++")),
                                                         sum(1 for l in d_ if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d_]
    else:
        out += ["      " + l[:200] for l in d_[:6]] + ["      ... (%d linhas de diff no total)" % len(d_)]
grava(os.path.join(PK, "DIFF_KERNEL_v412.txt"), ("\n".join(out) + "\n").encode("utf-8"))
assert len(novos) == V["n_pedras"] and not removidos, ("o kernel embutido: novos != pedras do registro ou arquivo removido", len(novos), V["n_pedras"], removidos)

# ---------------------------------------------------------------- (1) o manifesto de incorporacao
def fila_info():
    """O estado da FILA DA MEMORIA ao fechar (v412; SO' INFORMA, nao recusa): o memoria.py (sha16 e se e' o do PINO_MEMORIA_PY_v412.json), o MEMORY.md (sha256, bytes, linhas), o PINO_MEMORY.json (sha256 do indice, quem e quando pinou), se o pino CONFERE com o indice agora
    e se a fila\\PAUSA_VIGIA.json esta ausente. Tudo LIDO dos arquivos por script."""
    try:
        f_ = os.path.join(UMEM, "fila"); mp_ = os.path.join(f_, "memoria.py"); ix_ = os.path.join(UMEM, "MEMORY.md"); pn_ = os.path.join(f_, "PINO_MEMORY.json"); pp_ = os.path.join(PK, "PINO_MEMORIA_PY_v412.json")
        pino_ = _j(pn_) if os.path.isfile(pn_) else {}
        ixb_ = open(ix_, "rb").read() if os.path.isfile(ix_) else b""
        d_ = {"dir": UMEM, "memoria_py_sha16": s16(mp_) if os.path.isfile(mp_) else None, "memoria_py_igual_ao_pino_v412": (s16(mp_) == _j(pp_)["sha16"]) if (os.path.isfile(mp_) and os.path.isfile(pp_)) else None,
              "memory_md_sha256": s64(ixb_) if ixb_ else None, "memory_md_bytes": len(ixb_), "memory_md_linhas": ixb_.count(b"\n"), "pino_sha256": pino_.get("sha256"), "pino_por": pino_.get("por"), "pino_em": pino_.get("pinado_em"), "pino_via": pino_.get("via"),
              "pino_confere_com_o_indice": bool(ixb_) and pino_.get("sha256") == s64(ixb_), "pausa_do_vigia_ausente": not os.path.exists(os.path.join(f_, "PAUSA_VIGIA.json"))}
    except Exception as e_:   # noqa: BLE001
        d_ = {"erro": repr(e_)[:200]}
    return d_


FILA_INFO = fila_info()
print("(0) fila da memoria ao fechar:", json.dumps({k_: FILA_INFO.get(k_) for k_ in ("memory_md_linhas", "pino_confere_com_o_indice", "pausa_do_vigia_ausente", "memoria_py_igual_ao_pino_v412")}, ensure_ascii=False))
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff", ".md")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
ESP = _j(os.path.join(PK, "ESPERADOS_v412.json"))
pedras_nos = {rel: s16(os.path.join(NOS, "tgl_kernel", *rel.split("/"))) for rel in ESP["bundle_sha256"]}
# v412: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata e o recibo de compilacao, a saida do lean, o bundle e a medida KH-N1; o desenho fica so' por sha16, D65); as falas ficam em insumos/cunhagens (indexadas no arquivo)
m = {"stamp": ST, "versao": "v412", "instalacao": os.path.basename(app), "base_v411": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"pedras_no_nos_sha16": pedras_nos, "escada": [V["escada_antes"], V["teor"]], "axiom_report_n": V["axiom_report_n"], "build_full_log_sha16": s16(os.path.join(PK, "kernel", "build_full.log")) if os.path.exists(os.path.join(PK, "kernel", "build_full.log")) else None,
                "kernel_recibo_sha16": s16(os.path.join(PK, "kernel", "KERNEL_RECIBO_v412.json")) if os.path.exists(os.path.join(PK, "kernel", "KERNEL_RECIBO_v412.json")) else None},
     "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v411": V["reg412"], "registros_v410": V["reg411_recriados"], "registros_v409": V["reg411t"], "registros_v408": V["reg408d"], "registros_v407": V["reg407d"], "registros_v406": V.get("reg406d"), "registros_v405": V["reg411c"], "registros_v404": V.get("reg411b"), "registros_v403": V["reg411_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "registros_funcao_v412": {"h0dn_bg1_v411": V["fecho"]}, "registros_funcao_v411": {n_: V["reg411_recriados"][n_] for n_ in L.REG_RECRIADOS_V411F}, "registros_funcao_v409": {"traducao_turing_v409": V["fecho411"]}, "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho408"]}, "registros_funcao_v407": {"psion_canto_v407": V["fecho407"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v412": V["ancoras"], "ancoras_v411": V["ancoras411"], "ancoras_v409": V["ancoras409"], "ancoras_v408": V["ancoras408"], "ancoras_v407": V["ancoras407"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v412": V["bandeiras"], "bandeiras_ate_v411": V["bandeiras411"], "chaves_v407": V["chaves407"], "chaves_v406": V.get("chaves406"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v411_recriadas": {n_: V["reg411_recriados"][n_] for n_ in L.REG_RECRIADOS_V411F}, "funcoes_v409_recriadas": {"traducao_turing_v409": V["fecho411"]}, "funcoes_v408_recriadas": {"tetelestai_terminal_v408": V["fecho408"]}, "funcoes_v407_recriadas": {"psion_canto_v407": V["fecho407"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")}, "funcoes_v405_recriadas": V["fun411c"], "funcoes_v404_recriadas": V.get("fun411b"), "funcoes_v403_recriadas": V["fun411"], "funcoes_v402_recriadas": V["fun402"], "pedras_v411_como_registro": V["bundle411"], "pedras_v409_como_registro": V["bundle409"], "pedras_v408_como_registro": V["bundle408"], "pedras_v407_como_registro": V["bundle407"], "pedras_v406_como_registro": V.get("bundle406"), "pedras_v405_como_registro": V["pedras_v408"], "falsidade_v401": V["fal401"],
     "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_v412": {"sha16": hashlib.sha256(PAR_F.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_F_INFO}, "paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v404", "massa_derivada_e_identidade_v405", "o_fechamento_v406", "o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v408", "a_traducao_as_classes_de_turing_v409", "iald_ao_quadrado_v411"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": False, "fila_da_memoria": FILA_INFO, "sidecar_acom": SC_INFO, "h0dn_bg1_v412_resumo": H0DN_RESUMO, "troca_dita": V["troca_dita"], "pedras": V["pedras"], "varredura": V["varr"], "verbatins": V["verbatins"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "insumos_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,
     "diffs": {"DIFF_v411_v412.diff": s16(os.path.join(PK, "DIFF_v411_v412.diff")), "DIFF_KERNEL_v412.txt": s16(os.path.join(PK, "DIFF_KERNEL_v412.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v412_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v412_incorporacao_manifesto.json"), mb)
# ---------------------------------------------------------------- (2) o arquivo
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "pacote": PK, "arquivos": {}, "copias": {}, "nao_copiado": {}}


def indexa(p):
    b = open(p, "rb").read(); arq["arquivos"][p] = {"bytes": len(b), "sha256": s64(b)}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f412"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["copias"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pyc",)
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__", "pilar_anterior", "memoria_copia"))]   # (memoria_copia: a COPIA da memoria do ensaio da fila, descartavel; so' o JSON de evidencia entra)
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f:
            continue
        indexa(p)
# pos_rito (e o conferidor) -> v412_selo
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f in ("v412_incorporacao_manifesto.json", "DERIVACAO_v412.json", "HARNESS_TEXTOS_ENSAIO_v412.json", "HARNESS_FECHAR_SANDBOX_v412.json", "FILA_MEMORIA_ENSAIO_v412.json", "registro_mapa_v412.json", "NOTAS_DERIVACAO_v412.md", "NOTA_ESPERADOS_H0DN_v412.md", "ADAPTACAO_09nov_SONNET.json")):
            continue
        copia(p, os.path.join(TOOLS, "v412_selo", os.path.relpath(p, HERE)))
# v412: o SIDECAR (arquivo NOVO da custodia, D5) e o SELO PRIMARIO, ao lado: copias de bytes em v412_selo (a segunda testemunha so' se confere com o selo; o selo nao pode conter o selo ACOM de si mesmo)
for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json"):
    copia(os.path.join(NOS, nm_), os.path.join(TOOLS, "v412_selo", nm_))
# kernel: a pasta kernel da cadeia (+ work\v412_kernel, se existir) e as pedras do Nos -> v412_kernel
for src in (os.path.join(PK, "kernel"), os.path.join(WK, "v412_kernel")):
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if os.path.isfile(p):
                if os.path.getsize(p) > 5 * 1024 * 1024:
                    arq["nao_copiado"][p] = "%d B (> 5 MB; indexado por sha256)" % os.path.getsize(p); continue
                copia(p, os.path.join(TOOLS, "v412_kernel", ("" if src.startswith(PK) else "work_v412_kernel"), f))
for rel in ESP["bundle_sha256"]:
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v412_kernel", "pedras", rel.replace("/", "_")))
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v412_kernel", "depois", rel.replace("/", "_")))
for f in ("DIFF_v411_v412.diff", "DIFF_KERNEL_v412.txt"):
    copia(os.path.join(PK, f), os.path.join(TOOLS, "v412_kernel", f))
grava(os.path.join(PK, "MANIFESTO_ARQUIVO_v412.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  indexados: %d; copiados: %d; nao copiados (ditos): %d" % (len(arq["arquivos"]), len(arq["copias"]), len(arq["nao_copiado"])))
# ---------------------------------------------------------------- (4) o handoff
ap_ = B3.get("aplicar") or {}
# o handoff da v412: o texto vive em textos_v412.handoff(V, k) (testavel pelo harness); aqui so' entram os campos dos recibos do B(n), lidos dos arquivos (nenhum numero digitado)
_k = {"readme_paragrafo": PAR, "readme_paragrafo_v412": PAR_F, "ap_nome": os.path.basename(ap_.get("path", "?")), "ap_sha": str(ap_.get("sha256"))[:16], "ap_ver": ap_.get("veredito"), "ap_evento": ap_.get("evento"), "ap_bat": ap_.get("bateria"),
      "par_sha": str((B3.get("parada") or {}).get("sha256"))[:16], "rel_sha": str((B3.get("religamento") or {}).get("sha256"))[:16], "rel_man": str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16]}
doc = T.handoff(V, _k)
vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
import guarda_frases_v412 as GF
vf = GF.violacoes(doc)
assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)
import delta_v412 as DLF   # (v412) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff (recusa ANTES de gravar)
vd65 = [x_ for x_ in DLF.FORA_D65 if x_.lower() in doc.lower()]
assert not vd65, "D65: o handoff traz o que fica fora dos textos: %r" % (vd65[:3],)
# v412 (12/11, D169): o handoff DIZ o registro com funcao (h0dn_bg1_v411), os registros da v411 recriados, as sete ressalvas por rotulo e o que o teste nao decide; NAO traz a frase velha da v411 («pre-registrado; nenhum dado observado lido»), nem token proibido; as quatro obrigacoes do primario (F67) ja' foram conferidas por GF.violacoes(doc) acima; recusa ANTES de gravar
assert DLF.FECHO_REGISTRO in doc, "D169: o handoff nao diz o registro %s (o registro com funcao da v412)" % DLF.FECHO_REGISTRO
_faltam_rf = [n_ for n_ in tuple(DLF.REGISTROS_FUNCAO) + tuple(DLF.REGISTROS_FUNCAO_V411) + (DLF.CUNHAGENS_REGISTRO, DLF.KH_REGISTRO, "cunhagens_v410", "kh_n1_cobertura_v410") if n_ not in doc]   # o handoff diz, pelo nome, o registro novo, os tres por spec e os quatro com funcao da v411 recriados
assert not _faltam_rf, "o handoff nao diz os registros da v412 e os da v411 recriados: %r" % (_faltam_rf,)
_faltam_rs = [r_ for r_ in DLF.RESSALVAS_ROTULOS_PT if r_ not in doc]
assert not _faltam_rs, "o handoff nao traz as sete ressalvas por rotulo: %r" % (_faltam_rs[:3],)
_faltam_nd = [x_ for x_ in (_hc.get("o_que_o_teste_nao_decide") or []) if " ".join(str(x_).split()) not in " ".join(doc.split())]
assert not _faltam_nd, "o handoff nao traz o que o teste NAO decide (secao 6 do pre-registro): %r" % (_faltam_nd[:2],)
assert DLF.FRASE_H0DN_OBRIGATORIA_PT not in doc and DLF.FRASE_H0DN_OBRIGATORIA_EN not in doc, "D169: o handoff traz a frase velha da v411 (pre-registrado; nenhum dado observado lido): o teste foi aberto uma vez"
assert "RECRIADOS" in doc and "nenhum módulo novo" in doc, "o handoff nao diz que os registros da v411 sao recriados e que nao ha modulo novo"
_proib_fecho = [t_ for t_ in ("Clay resolvido", "CONF" + "IRMED", "PRO" + "VED_BY") if t_ in doc]   # (montadas por concatenacao: a guarda P18 varre ESTE arquivo)
assert not _proib_fecho, "o handoff traz forma vedada: %r" % (_proib_fecho,)
_vt412 = [t_ for t_ in DLF.TOKENS_PROIBIDOS_V412 if t_ in doc]
assert not _vt412, "D169: o handoff traz token proibido: %r" % (_vt412[:3],)
print("(4) handoff")
grava(os.path.join(UMEM, "handoff-v412-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v412_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v412:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v412-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v412_CUSTODIA.md")))
