# -*- coding: utf-8 -*-
"""derivar_scripts_etapa1_v413.py -- (claude-construtor-v413, 20/11/2026, a servico da gerencia c1) Etapa 1 da v413, item 4: DERIVACAO MECANICA dos scripts da Etapa 1 da v412
para a pasta da v413. Cada destino nasce do seu molde (pasta da v412 ou C:\\t\\k412c, SO' LEITURA) por:
  (1) trocas de texto EXATO, cada uma com o numero EXATO de ocorrencias exigido (a contagem achada fica registrada; se diferir, aborta e nada e' gravado);
  (2) a subida simultanea dos rotulos de versao, so' como token inteiro: v412->v413, v411->v412, v410->v411, V412->V413, V411->V412, k412c->k413c, k411c->k412c, k410c->k411c,
      K412C->K413C, K411C->K412C e _412_->_413_ (o prefixo das bandeiras); numero solto NAO sobe;
  (3) uma linha de cabecalho `# [DERIVADO v413 ...]` logo depois da linha de codificacao (ou do #!).
Depois: compile() (.py) ou `sh -n` (.sh); o diff unificado vai para bump\\<destino>.diff; as linhas que ainda tem 412/411/410 sao LISTADAS para revisao (nada e' trocado as cegas).
Registro: DERIVACAO_ETAPA1_v413.json (molde e destino com sha256, cada troca com a contagem, os tokens subidos, o risco restante). O molde fica intacto; destino existente que difere
ganha backup de BYTES (.bak_<data>) antes; escrita por temporario conferido. Nunca executa o que deriva.
uso: C:\\Python314\\python.exe -B -X utf8 derivar_scripts_etapa1_v413.py [--seco] [--so <destino> ...]"""
import datetime, difflib, hashlib, json, os, re, subprocess, sys, warnings

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V412 = os.path.join(os.path.dirname(HERE), "v412")
T12 = os.path.join("C:" + os.sep, "t", "k412c")
T13 = os.path.join("C:" + os.sep, "t", "k413c")
BUMPDIR = os.path.join(HERE, "bump")
LOGP = os.path.join(HERE, "DERIVACAO_ETAPA1_v413.json")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ESTE = "derivar_scripts_etapa1_v413.py"
SECO = "--seco" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
CAB = ("# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de %s; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json "
       "(derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.")
VMAP = {"v412": "v413", "v411": "v412", "v410": "v411", "V412": "V413", "V411": "V412", "V410": "V411",
        "k412c": "k413c", "k411c": "k412c", "k410c": "k411c", "K412C": "K413C", "K411C": "K412C", "_412_": "_413_"}
RX_V = re.compile(r"(?<![0-9A-Za-z])(?<!construtor-)(v41[012]|V41[012]|k41[012]c|K41[12]C)(?![0-9])|_412_")
RISCO = re.compile(r"(?<![0-9a-f])41[0-3](?![0-9a-f])")
# as MARCAS HISTORICAS de cabecalho (quem derivou ou adaptou, quando, de que molde) sao registro: NAO sobem (molde: v412\_bump_copia_v412.py); nem a autoria `claude-construtor-v41x`
RX_MARCA = re.compile(r"^\s*#\s*\[(?:ADAPTADO|AUTORAL|ADAPTADA|DERIVADO)\s+v4\d\d\b")


def subir_rotulos(t):
    cont = {"marcas_historicas_preservadas": 0}

    def f(m):
        k = m.group(0)
        cont[k] = cont.get(k, 0) + 1
        return VMAP[k]
    out = []
    for ln in t.split("\n"):
        if RX_MARCA.match(ln):
            out.append(ln)
            if RX_V.search(ln):
                cont["marcas_historicas_preservadas"] += 1
            continue
        out.append(RX_V.sub(f, ln))
    return "\n".join(out), cont


def insere_cabecalho(t, linha):
    ls = t.split("\n"); i = 0
    if ls and ls[0].startswith("#!"):
        i = 1
    if i < len(ls) and re.match(r"#.*coding[:=]", ls[i]):
        i += 1
    ls.insert(i, linha)
    return "\n".join(ls)


def grava(dst, novo_b):
    if os.path.exists(dst):
        atual = open(dst, "rb").read()
        if atual == novo_b:
            return "igual"
        bk = dst + ".bak_" + TS
        open(bk, "wb").write(atual); assert open(bk, "rb").read() == atual
        estado = "regravado_com_backup"
    else:
        estado = "gravado"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".tmp"
    open(tmp, "wb").write(novo_b); assert os.path.getsize(tmp) == len(novo_b); os.replace(tmp, dst)
    assert open(dst, "rb").read() == novo_b
    return estado


BLOCOS = os.path.join(HERE, "derivacao_blocos")


def _novo(novo):
    """o texto novo: literal, ou '@arquivo:<nome>' (o texto EXATO de derivacao_blocos\\<nome>, lido em bytes; o sha256 do arquivo fica no registro)."""
    if novo.startswith("@arquivo:"):
        p = os.path.join(BLOCOS, novo[len("@arquivo:"):])
        b = open(p, "rb").read(); assert b"\r" not in b, ("bloco com CR", p)
        return b.decode("utf-8"), {"arquivo": os.path.relpath(p, HERE), "sha256": sha(b)}
    return novo, None


def aplicar_trocas(t, trocas, reg):
    """cada troca: (velho, novo, n_exato[, motivo]) -- substituicao exata com contagem; ou ("@@BLOCO", inicio, fim, novo[, motivo]) -- o trecho que vai do UNICO `inicio` ate' o primeiro
    `fim` depois dele (inclusive) e' trocado por `novo` (o sha256 do trecho retirado fica no registro)."""
    for tr in trocas:
        if tr[0] == "@@BLOCO":
            _, ini, fim, novo, *mot = tr
            novo, arq = _novo(novo)
            assert t.count(ini) == 1, ("o inicio do bloco nao e' unico: NADA gravado", ini[:120], t.count(ini))
            i0 = t.index(ini); i1 = t.find(fim, i0)
            assert i1 >= 0, ("o fim do bloco nao aparece depois do inicio: NADA gravado", fim[:120])
            i1 += len(fim); velho = t[i0:i1]
            t = t[:i0] + novo + t[i1:]
            reg["trocas"].append({"tipo": "bloco", "inicio": ini[:160], "fim": fim[:160], "velho_sha16": sha(velho.encode())[:16], "velho_linhas": velho.count("\n") + 1,
                                  "novo": arq or novo[:200], "novo_sha16": sha(novo.encode())[:16], "novo_linhas": novo.count("\n") + 1, "ocorrencias": 1, "motivo": mot[0] if mot else None})
        else:
            velho, novo, n, *mot = tr
            novo, arq = _novo(novo)
            c = t.count(velho)
            assert c == n, ("contagem da troca diferente da exigida: NADA gravado", velho[:140], c, n)
            t = t.replace(velho, novo)
            reg["trocas"].append({"velho": velho[:200], "novo": arq or novo[:200], "ocorrencias": c, "velho_sha16": sha(velho.encode())[:16], "novo_sha16": sha(novo.encode())[:16], "motivo": mot[0] if mot else None})
    return t


def derivar(molde, destino, trocas, cabecalho=True, subir=True, modo="antes"):
    """molde/destino: caminhos absolutos; trocas: ver aplicar_trocas. modo 'antes': as trocas valem sobre o texto do MOLDE e a subida dos rotulos vem depois (os textos novos escritos nos
    termos do molde); modo 'depois': primeiro a subida dos rotulos, depois as trocas sobre o texto JA SUBIDO (os textos novos sao os finais, nada sobe neles)."""
    raw = open(molde, "rb").read(); t = raw.decode("utf-8")
    assert "\r" not in t, ("o molde tem CR: a derivacao respeita LF e PARA", molde)
    reg = {"molde": molde, "molde_sha256": sha(raw), "destino": destino, "derivador": ESTE, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "modo": modo, "trocas": [], "rotulos_subidos": {}}
    if modo == "antes":
        t = aplicar_trocas(t, trocas, reg)
        if subir:
            t, reg["rotulos_subidos"] = subir_rotulos(t)
    else:
        assert modo == "depois", modo
        if subir:
            t, reg["rotulos_subidos"] = subir_rotulos(t)
        t = aplicar_trocas(t, trocas, reg)
    if cabecalho:
        t = insere_cabecalho(t, CAB % molde.replace(os.sep, "\\"))
    if destino.endswith(".py"):
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)   # (escape invalido em cadeia nova reprova a derivacao)
            compile(t, destino, "exec")
    elif destino.endswith(".sh"):
        r = subprocess.run(["sh", "-n"], input=t.encode("utf-8"), capture_output=True)
        assert r.returncode == 0, (destino, r.stderr[:300])
    out = t.encode("utf-8")
    reg["destino_sha256"] = sha(out); reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    reg["linhas_com_41x_restantes"] = [[i + 1, l.strip()[:200]] for i, l in enumerate(t.split("\n")) if RISCO.search(l)][:80]
    d = "".join(difflib.unified_diff(raw.decode("utf-8").splitlines(True), t.splitlines(True), fromfile=molde.replace(os.sep, "/"), tofile=destino.replace(os.sep, "/"), n=1))
    reg["diff"] = os.path.join("bump", os.path.basename(destino) + ".diff")
    reg["linhas_alteradas"] = sum(1 for l in d.splitlines() if l.startswith("+") and not l.startswith("+++"))
    if SECO:
        reg["estado"] = "seco"
    else:
        reg["estado"] = grava(destino, out)
        os.makedirs(BUMPDIR, exist_ok=True)
        grava(os.path.join(BUMPDIR, os.path.basename(destino) + ".diff"), d.encode("utf-8"))
    print("derivado: %-44s <- %-40s %6d bytes sha16 %s | trocas %d | rotulos %s | %s" % (os.path.basename(destino), os.path.basename(molde), len(out), reg["destino_sha16"],
                                                                                   len(reg["trocas"]), sum(reg["rotulos_subidos"].values()), reg["estado"]))
    return reg


# ======================================================================================================================================================
# AS DERIVACOES (cada uma: molde, destino, trocas). Os textos novos dizem o que a v413 muda; nenhum hash nem contagem de modulos e' digitado (tudo lido em tempo de execucao).
# ======================================================================================================================================================
D = []


def _grava_com_backup(var):
    """[v413] a troca que poe BACKUP DE BYTES antes de regravar a saida JSON dos scripts de conferencia (o molde gravava por cima, em modo texto, sem backup: a segunda rodada da
    conferencia das fontes sobrescreveu a primeira assim). Texto exato do molde e o novo, para a variavel `var` do arquivo de saida."""
    velho = 'open(%s + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(%s + ".tmp", %s)' % (var, var, var)
    novo = ('_b = json.dumps(rep, ensure_ascii=False, indent=1).encode("utf-8")\n'
            'if os.path.exists(%s):   # [v413] backup de BYTES antes de regravar a saida (o molde gravava por cima)\n'
            '    _bk = %s + ".bak_" + __import__("datetime").datetime.now().strftime("%%Y%%m%%d_%%H%%M%%S"); open(_bk, "wb").write(open(%s, "rb").read()); assert open(_bk, "rb").read() == open(%s, "rb").read()\n'
            'open(%s + ".tmp", "wb").write(_b); assert os.path.getsize(%s + ".tmp") == len(_b); os.replace(%s + ".tmp", %s)') % ((var,) * 8)
    return (velho, novo, 1, "backup de bytes antes de regravar a saida (causa: a segunda rodada da conferencia sobrescreveu a primeira sem backup)")

# ---------------------------------------------------------------- 1. conferencia das fontes do sandbox de origem contra o Nos (item 1)
D.append((os.path.join(V412, "conferir_fontes_k411c_vs_nos_v412.py"), os.path.join(HERE, "conferir_fontes_k412c_vs_nos_v413.py"), [
    ('"""conferir_fontes_k411c_vs_nos_v412.py -- (claude-construtor-v412, 17/11/2026) ANTES de copiar o sandbox:',
     '"""conferir_fontes_k411c_vs_nos_v412.py -- (claude-construtor-v412; derivado para a v413 em 20/11/2026) ANTES de copiar o sandbox:', 1),
    ("(3) confere que NENHUM dos 34 modulos do manifesto da v412 existe no Nos nem na origem",
     "(3) confere que NENHUM dos modulos novos do manifesto da v412 existe no Nos nem na origem", 1),
    ("(so' os rotulos sobem; a medicao do tamanho e a conferencia dos 34 nomes sao novas)",
     "(so' os rotulos sobem e o manifesto da v412 e' lido no formato dele: modulos_novos, chaves TGLExt.<Nome>; mais: o modulo que a v412 corrige so' no texto, kernel_corrigido, tem de ser igual no Nos e na origem)", 1),
    ('nomes = [m["modulo"] for m in man["modulos"]]',
     'nomes = [k_.split(".", 1)[1] for k_ in man["modulos_novos"]]\n'
     'assert len(nomes) == len(set(nomes)) == int(man["n_modulos_novos"]), ("o manifesto nao tem n_modulos_novos nomes distintos", len(nomes), man.get("n_modulos_novos"))\n'
     '# o modulo que a v412 corrige so\' no texto: a fonte de origem (sha256_origem do manifesto) tem de ser a do Nos e a da origem do sandbox\n'
     'corr = {}\n'
     'for k_, v_ in (man.get("kernel_corrigido") or {}).items():\n'
     '    rel_ = k_.replace(".", "/") + ".lean"\n'
     '    corr[rel_] = {"sha256_origem_do_manifesto": v_["sha256_origem"], "nos": a.get(rel_), "sandbox_origem": b.get(rel_), "igual": a.get(rel_) == b.get(rel_) == v_["sha256_origem"]}', 1),
    ('"modulos_v412": len(nomes), "colisoes_de_nome_de_modulo_sem_caixa": colide, "sem_colisao_de_nome_de_modulo": not colide}',
     '"modulos_v412": len(nomes), "colisoes_de_nome_de_modulo_sem_caixa": colide, "sem_colisao_de_nome_de_modulo": not colide,\n'
     '       "kernel_corrigido": corr, "kernel_corrigido_origem_igual_no_nos_e_no_sandbox": all(v_["igual"] for v_ in corr.values()) and len(corr) > 0}', 1),
    ('and not colide and rep["folga_depois_da_copia_gb"] > 20',
     'and not colide and rep["folga_depois_da_copia_gb"] > 20 and rep["kernel_corrigido_origem_igual_no_nos_e_no_sandbox"]', 1),
    _grava_com_backup("SAIDA"),
]))

# ---------------------------------------------------------------- 2. a copia do sandbox (item 1)
D.append((os.path.join(V412, "copiar_k412c.sh"), os.path.join(HERE, "copiar_k413c.sh"), [
    ("# v412 (17/11/2026, claude-construtor-v412): o sandbox do kernel da v412 = COPIA do sandbox C:\\t\\k411c\\final (DESENHO_v412 secao 1: sandbox k412c, nascido do k411c; ordem da Etapa 1, item 1:",
     "# v412 (claude-construtor-v412; derivado para a v413 em 20/11/2026): o sandbox do kernel da v412 = COPIA do sandbox C:\\t\\k411c\\final (ordem da Etapa 1 da v412, item 1: sandbox k412c, nascido do k411c;", 1),
    ("# CONFERENCIA_FONTES_K411C_v412.json: 1764 fontes comuns, todas iguais, nada so' num dos lados; nenhum dos 34 nomes da v412 existe la', sem caixa). A origem k411c\\final e' SO' LIDA.",
     "# CONFERENCIA_FONTES_K411C_v412.json: as fontes comuns todas iguais; nenhum dos nomes novos da v412 existe la', sem caixa; o modulo corrigido igual nos dois). A origem k411c\\final e' SO' LIDA.", 1),
    ("# Os 34 modulos da v412 NAO entram aqui: e' o passo seguinte (preparar_bundle_v412.py). Molde: copiar_k411c.sh (so' os rotulos e a origem sobem).",
     "# Os modulos novos da v412 e o modulo corrigido NAO entram aqui: e' o passo seguinte (preparar_bundle_v412.py). Molde: copiar_k411c.sh (so' os rotulos e a origem sobem).", 1),
]))

# ---------------------------------------------------------------- 3. a base (a v412 selada, copia de bytes do Nos) para o pos_build e o portao do pilar
D.append((os.path.join(V412, "copiar_base_v412.py"), os.path.join(HERE, "copiar_base_v413.py"), [
    ("# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v411\\copiar_base_v411.py: copia de bytes do Nos v411 SELADO para base_v411 (so' os rotulos sobem; o sha16 da base e' LIDO do DESENHO_v412 da gerencia, sem delta)",
     "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v411\\copiar_base_v411.py: copia de bytes do Nos v411 SELADO para base_v411 (so' os rotulos sobem; o sha16 da base e' LIDO do DESENHO_v412 da gerencia, sem delta)\n"
     "# [v413] a v413 ainda nao tem desenho nem contrato (sao da gerencia): o sha16 da base e' LIDO de dois arquivos da cadeia da v411 (ESPERADOS_v411.json e CANDIDATO_v411.json) e tem de bater com o pino do selo", 1),
    ("(as funcoes de leitura do Audit, a escada E411, o axiom_report da v411)", "(as funcoes de leitura do Audit, a escada E412, o axiom_report da v411)", 1),
    ("Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v411; o sha16 == o candidato_sha16 de v411\\\\ESPERADOS_v411.json == o que o DESENHO_v412 da gerencia\ndeu (lido do arquivo; o arquivo manda);",
     "Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v411; o sha16 == o candidato_sha16 de v411\\\\ESPERADOS_v411.json == o sha256 do\nCANDIDATO_v411.json (lidos dos arquivos; o arquivo manda);", 1),
    ('_des = open(os.path.join(HERE, "DESENHO_v412.md"), "rb").read().decode("utf-8")\n_m = re.search(r"Base: a v411 selada \\(`um\\.py` do N[oó]s, sha16 `([0-9a-f]{16})`", _des)\nassert _m, "o DESENHO_v412 nao traz a base"\nBASE_SHA16_DA_ORDEM = _m.group(1)',
     '_cand = json.load(open(os.path.join(V411, "CANDIDATO_v411.json"), encoding="utf-8"))\nassert _cand.get("sha256") and _cand["sha256"][:16] == _cand.get("sha16"), "o CANDIDATO_v411.json nao traz sha256/sha16 coerentes"\nBASE_SHA16_DA_ORDEM = _cand["sha16"]', 1),
    ('assert sha(raw)[:16] == BASE_SHA16_DA_ORDEM, ("o um.py do Nos NAO e\' o que o DESENHO_v412 deu", sha(raw)[:16], BASE_SHA16_DA_ORDEM)',
     'assert sha(raw) == _cand["sha256"], ("o um.py do Nos NAO e\' o candidato da v411 (CANDIDATO_v411.json)", sha(raw)[:16], BASE_SHA16_DA_ORDEM)', 1),
    ('rep = {"base_sha16": sha(raw)[:16], "base_sha16_do_desenho": BASE_SHA16_DA_ORDEM,',
     'rep = {"base_sha16": sha(raw)[:16], "base_sha16_do_candidato_v411": BASE_SHA16_DA_ORDEM, "base_sha16_dos_esperados_v411": esp["candidato_sha16"],', 1),
    _grava_com_backup("p_"),
]))

# ---------------------------------------------------------------- 4. a pre-conferencia de colisao de nomes de declaracao (item 2: PARE se colidir)
D.append((os.path.join(V412, "pre_colisao_declaracoes_v412_r7.py"), os.path.join(HERE, "pre_colisao_declaracoes_v413.py"), [
    ('MAN = json.load(open(os.path.join(PK, "insumos", "MANIFESTO_PEDRAS_v412_R12.json"), encoding="utf-8"))\nPED = os.path.join(PK, "insumos", "pedras_r12")',
     'MAN = json.load(open(os.path.join(PK, "insumos", "MANIFESTO_PEDRAS_v412.json"), encoding="utf-8"))\nPED = os.path.join(PK, "insumos", "pedras_limpas", "TGLExt")\n'
     'KC = {k_: v_ for k_, v_ in (MAN.get("kernel_corrigido") or {}).items()}', 1),
    ('OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v412_R7.json")', 'OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v412.json")', 1),
    ('por_mod = {}; sha_ruim = []\nfor m in MAN["modulos"]:\n    b = open(os.path.join(PED, m["modulo"] + ".lean"), "rb").read()\n    if hashlib.sha256(b).hexdigest() != m["sha256"]:\n        sha_ruim.append(m["modulo"])\n    por_mod[m["modulo"]] = nomes_da_fonte(b.decode("utf-8"))',
     'por_mod = {}; sha_ruim = []\nfor k_, m in MAN["modulos_novos"].items():\n    nome_ = k_.split(".", 1)[1]\n    b = open(os.path.join(PED, nome_ + ".lean"), "rb").read()\n    if hashlib.sha256(b).hexdigest() != m["sha256_pedra_limpa"]:\n        sha_ruim.append(nome_)\n    por_mod[nome_] = nomes_da_fonte(b.decode("utf-8"))\n'
     '# o modulo corrigido so\' no texto: os nomes que ele declara tem de ser EXATAMENTE os que o kernel ja tem dele (nada novo, nada some)\ncorr_rep = {}\nfor k_, v_ in KC.items():\n'
     '    b = open(v_["saida"], "rb").read()\n    if hashlib.sha256(b).hexdigest() != v_["sha256_saida"]:\n        sha_ruim.append(k_)\n    ns_ = sorted({q for q, kw in nomes_da_fonte(b.decode("utf-8"))})\n'
     '    ausentes_ = [q for q in ns_ if q not in existentes]\n    corr_rep[k_] = {"n_nomes_lidos": len(ns_), "nomes_que_o_kernel_nao_tem": ausentes_, "ok": not ausentes_}', 1),
    ('       "colisao_com_o_kernel_nome_exato": col_kernel,',
     '       "kernel_corrigido": corr_rep, "kernel_corrigido_ok": all(v_["ok"] for v_ in corr_rep.values()) and len(corr_rep) == len(KC),\n       "colisao_com_o_kernel_nome_exato": col_kernel,', 1),
    ("Le, por expressao regular sobre as fontes congeladas (insumos\\\\pedras, sha256 conferido contra o manifesto)",
     "Le, por expressao regular sobre as fontes congeladas (insumos\\\\pedras_limpas\\\\TGLExt, sha256 conferido contra o manifesto)", 1),
    (" (a) com os 34300 nomes do kernel atual (as linhas TGL_DECL_SOURCE do log do Audit da v411,", " (a) com os nomes do kernel atual (as linhas TGL_DECL_SOURCE do log do Audit da v411,", 1),
    (" (b) entre os proprios 34 modulos (dois modulos", " (b) entre os proprios modulos novos (dois modulos", 1),
    ("sys.exit(1 if (col_kernel or col_prefixo or col_entre or sha_ruim) else 0)",
     "sys.exit(1 if (col_kernel or col_prefixo or col_entre or sha_ruim or not rep[\"kernel_corrigido_ok\"]) else 0)", 1),
    _grava_com_backup("OUT"),
    ('"""pre_colisao_declaracoes_v412.py -- (claude-construtor-v412, 17/11/2026) PRE-CONFERENCIA de colisao de NOMES DE DECLARACAO, antes de instalar os 34 modulos no sandbox.',
     '"""pre_colisao_declaracoes_v412.py -- (claude-construtor-v412, 17/11/2026) PRE-CONFERENCIA de colisao de NOMES DE DECLARACAO, antes de instalar os modulos novos no sandbox.\n'
     '[v413] le o manifesto da v413 (modulos_novos; as pedras limpas em insumos\\\\pedras_limpas\\\\TGLExt) e confere tambem o modulo que a v413 corrige so\' no texto (kernel_corrigido):\n'
     'os nomes que ele declara tem de estar todos no kernel atual (a correcao nao cria nem tira declaracao).', 1),
]))

# ---------------------------------------------------------------- 5. a leitura de texto Lean (dependencia do preparo): copia com rotulo
D.append((os.path.join(V412, "lean_texto_v412.py"), os.path.join(HERE, "lean_texto_v413.py"), []))

# ---------------------------------------------------------------- 6. O PREPARADOR DO BUNDLE (item 2). Modo 'depois': os textos velhos sao os do molde JA com os rotulos subidos.
#   O que muda de fato: o formato do manifesto da v413 (modulos_novos com chaves TGLExt.<Nome>; sha256_pedra_limpa; imports_tglext; ordem_topologica_sugerida), as fontes ja na forma do kernel
#   (nenhum import se troca; import solto de irmao PARA), e o modulo que a v413 corrige so' no texto (kernel_corrigido: conferido contra o recibo e o Nos, codigo identico, antigo na quarentena).
PB = "preparar_bundle_v413__"
D.append((os.path.join(V412, "preparar_bundle_v412.py"), os.path.join(HERE, "preparar_bundle_v413.py"), [
    ("K12", "K13", 10, "o nome da variavel do sandbox acompanha o rotulo (k413c)"),
    ("@@BLOCO", '"""preparar_bundle_v413.py -- v413, Etapa 1, item 2 (claude-construtor-v412', '[--manifesto <json>] [--pedras <pasta>]"""', "@arquivo:" + PB + "01_docstring.txt", "a docstring diz o que a v413 faz"),
    ('PED = arg("--pedras", PK / "insumos" / "pedras")\n', 'PED = arg("--pedras", PK / "insumos" / "pedras_limpas" / "TGLExt")\nKED = arg("--kernel-edits", None)   # (padrao: a pasta do campo saida de cada modulo corrigido no manifesto)\n', 1,
     "as pedras limpas da v413 e a pasta da fonte corrigida"),
    ("@@BLOCO", 'MODS = MAN["modulos"]', "\"import solto do manifesto que nao e' modulo do conjunto\"", "@arquivo:" + PB + "02_manifesto.txt", "o formato do manifesto da v413"),
    ("@@BLOCO", 'for m in MODS:\n    p = PED / (m["modulo"] + ".lean")', 'copia congelada com sha256/bytes diferente do manifesto: NADA foi gravado", ruins)', "@arquivo:" + PB + "03_sha.txt",
     "sha256_pedra_limpa; e a fonte corrigida contra o manifesto, o recibo da correcao e o Nos"),
    ('    assert len(i_print) == int(m["linhas_print_axioms"]), ("numero de #print axioms != manifesto", n, len(i_print), m["linhas_print_axioms"])\n',
     "    # (v413: o manifesto nao traz a contagem das linhas #print axioms; ela e' MEDIDA aqui e registrada no BUNDLE)\n", 1, "o manifesto da v413 nao tem linhas_print_axioms"),
    ("@@BLOCO", '    assert [x for _, x in imp_txt] == list(m["imports"])', "    deps[n] = sorted(set(trocar.values()))", "@arquivo:" + PB + "04_imports.txt",
     "os imports ja vem como TGLExt.<Nome>: nenhum se troca; import solto PARA; os irmaos conferidos contra imports_tglext"),
    ("    # RECONSTRUCAO independente: o RX do molde da v411 sobre o texto inteiro + a troca por expressao regular so' das linhas de import de candidata",
     "    # RECONSTRUCAO independente: o RX das linhas #print axioms (o do molde da IALD2, v410, e o da v412) sobre o texto inteiro; a troca de import por expressao regular fica (na v413 nao troca nada)", 1,
     "o rotulo v410->v411 da subida nao vale aqui: o molde do RX e' o da IALD2 (v410)"),
    ('fromfile="insumos/pedras/%s.lean" % n,', 'fromfile="insumos/pedras_limpas/TGLExt/%s.lean" % n,', 1, "o caminho do insumo no diff"),
    ("@@BLOCO", '    entradas[n] = {"modulo": n, "rel": "TGLExt/%s.lean" % n, "frente": m["frente"]', '"diff": "kernel/bundle/%s.diff" % n, "diff_texto": "".join(dif)}', "@arquivo:" + PB + "05_entradas.txt",
     "os campos do manifesto da v413 no registro de cada modulo; os namespaces medidos da fonte"),
    ("ordem = []; feitos = set(); resto = list(NOMES)", "ordem = []; feitos = set(); resto = list(SUG_NOMES)   # (v413: o desempate e' a ordem_topologica_sugerida do manifesto)", 1,
     "o desempate da ordem topologica"),
    ("dependentes = {x: sorted({y for y in NOMES if x in deps[y]}) for x in NOMES}", "@arquivo:" + PB + "06_corrigido.txt", 1, "o modulo corrigido: conferencias e quem depende dele no kernel"),
    ("@@BLOCO", "if SECO:\n    mud = [x for x in ordem", "    sys.exit(0)", "@arquivo:" + PB + "07_seco.txt", "o modo seco diz tambem o corrigido"),
    ('raiz_mudou = troca_com_backup(K13 / "TGLExt.lean", raiz_nova, no_lugar=False)', "@arquivo:" + PB + "08_grava_corrigido.txt", 1, "grava o corrigido (o antigo vai para a quarentena)"),
    ("@@BLOCO", "if not mudados and not raiz_mudou and bd_prev", 'ficam como estao" % len(ordem))', "@arquivo:" + PB + "09_nada_mudou.txt", "o atalho NADA MUDOU considera o corrigido"),
    ("@@BLOCO", 'rels = ["TGLExt/%s.lean" % x for x in ordem]', '"retirados": retirados}, ensure_ascii=False, indent=1))', "@arquivo:" + PB + "10_json.txt",
     "os registros da instalacao com o corrigido (BUNDLE, kernel_modulos_novos, SHA256_POR_MODULO, ULTIMA_INSTALACAO)"),
    ("@@BLOCO", 'lista = " ".join("TGLExt.%s" % x for x in ordem)', '""" % {"ts": TS, "n": len(ordem), "lista": lista}', "@arquivo:" + PB + "11_sh.txt",
     "o construir_kernel_v413.sh: o corrigido primeiro, depois os novos"),
    ("@@BLOCO", 'print("bundle:", len(ordem), "modulos | mudados no sandbox nesta rodada:"', '    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])', "@arquivo:" + PB + "12_prints.txt",
     "o resumo impresso"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 7. O RUN_BUILD (item 3) e o lancador do orquestrador, em C:\t\k413c (so' rotulos)
D.append((os.path.join(T12, "run_build.py"), os.path.join(T13, "run_build.py"), []))
D.append((os.path.join(T12, "run_pos_treino.py"), os.path.join(T13, "run_pos_treino.py"), [
    ("claude-construtor-v412, a servico da gerencia c1, 17/11/2026.", "claude-construtor-v413, a servico da gerencia c1, 20/11/2026 (molde de claude-construtor-v412, 17/11/2026).", 1, "autoria"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 8. O POS-BUILD (item 3). Modo 'depois'.
PP = "pos_build_kernel_v413__"
D.append((os.path.join(V412, "pos_build_kernel_v412_r7.py"), os.path.join(HERE, "pos_build_kernel_v413.py"), [
    ('-I -B -X utf8 pos_build_kernel_v413.py"""', "@arquivo:" + PP + "01_doc.txt", 1, "a docstring diz o que muda na v413"),
    ('BASE = os.path.join(HERE, "base_v412")', 'BASE = os.path.join(HERE, "base_v412")\nMAN_P = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413.json")\nV412 = os.path.join(os.path.dirname(HERE), "v412")', 1,
     "o manifesto da v413 e a pasta da cadeia da v412 (ESPERADOS)"),
    ('    MAN = json.load(open(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413_R12.json"), encoding="utf-8"))', '    MAN = json.load(open(MAN_P, encoding="utf-8"))', 1, "o manifesto da v413"),
    ("@@BLOCO", '    chk("a lista dos modulos novos (kernel_modulos_novos_v413.json) == a do BUNDLE_v413.json == n_modulos do manifesto', '        [N_NOVOS, BDL["n"], MAN["n_modulos"]])',
     "@arquivo:" + PP + "04_manifesto.txt", "n_modulos_novos; o modulo corrigido do BUNDLE contra o manifesto"),
    ("@@BLOCO", '    _des = open(os.path.join(HERE, "DESENHO_v413.md"), "rb").read().decode("utf-8")', "[sha(um_b)[:16], _mb.group(1) if _mb else None])", "@arquivo:" + PP + "05_base.txt",
     "a base conferida pelo selo e pelos ESPERADOS da v412 (a v413 nao tem desenho)"),
    ('    chk("as marcas trazem UMA linha por modulo novo, todas com rc 0, na ordem do bundle", [m for m in por_mod_marcas] == NEWMODS and all(v["rc"] == 0 for v in por_mod_marcas.values()), [len(por_mod_marcas), N_NOVOS])',
     '    chk("as marcas trazem UMA linha por modulo (o corrigido primeiro, depois os novos na ordem do bundle), todas com rc 0", [m for m in por_mod_marcas] == KCMODS + NEWMODS and all(v["rc"] == 0 for v in por_mod_marcas.values()), [len(por_mod_marcas), len(KCMODS) + N_NOVOS])', 1,
     "o corrigido tem a sua linha nas marcas"),
    ("""    chk("'Build completed successfully' em CADA invocacao do lake (%d por modulo + 1 do build inteiro)" % N_NOVOS, n_inv == N_NOVOS + 1 and n_ok == n_inv, [n_inv, n_ok])""",
     """    chk("'Build completed successfully' em CADA invocacao do lake (%d por modulo + 1 do build inteiro)" % (len(KCMODS) + N_NOVOS), n_inv == len(KCMODS) + N_NOVOS + 1 and n_ok == n_inv, [n_inv, n_ok])""", 1,
     "uma invocacao a mais (o corrigido)"),
    ("BUILT_CHECAGEM_CORRIGIDA_R7_v413.json", "BUILT_CHECAGEM_CORRIGIDA_v413.json", 1, "o recibo dos modos de conferencia sem o rotulo da rodada da v412"),
    ("(build da decima segunda lista)", "(build da v413)", 1, "texto"),
    ('    chk("(informativo) TODOS os %d modulos novos foram compilados neste build (a frio, como o do rito)" % N_NOVOS, todos_a_frio, {k: v for k, v in modo.items() if v != "Built"}, informativo=True)',
     "@arquivo:" + PP + "09_corrigido_built.txt", 1, "o corrigido tem linha Built; os antigos que dependem dele (informativo)"),
    ("@@BLOCO", "    avisos = {}\n    for st, md, s_, L in blocos:", '{"TowerWedgeIndex": av_conhecido.get("linhas", [])[:3], "outros": outros}, informativo=True)', "@arquivo:" + PP + "10_avisos.txt",
     "avisos: novos e corrigido; a TowerWedgeIndex agora e' modulo antigo; os antigos a parte"),
    ('    for m in NEWMODS + ["TGLExt", "TGL.Audit"]:', '    for m in KCMODS + NEWMODS + ["TGLExt", "TGL.Audit"]:', 1, "o cabecalho do .olean do corrigido"),
    ('"cabecalho de TODO .olean (%d novos + raiz + Audit)', '"cabecalho de TODO .olean (%d novos + o corrigido + raiz + Audit)', 1, "texto"),
    ('    chk("o axiom_report de agora tem exatamente os nomes da v412 mais as declaracoes dos modulos novos", set(axm) == set(axr0) | set(novas_todas), [len(axm), len(axr0), len(novas_todas)])',
     "@arquivo:" + PP + "12_corrigido_decl.txt", 1, "o corrigido emite as mesmas declaracoes da v412, com os mesmos axiomas"),
    ('for r in ("TGLExt.lean", "TGL/Audit.lean")) and all(os.path.exists(os.path.join(ARV, *r.split("/"))) for r in nov)',
     'for r in ["TGLExt.lean", "TGL/Audit.lean"] + KCRELS) and all(os.path.exists(os.path.join(ARV, *r.split("/"))) for r in nov)', 1, "o corrigido na arvore == o do sandbox"),
    ('"a arvore tem os %d modulos novos e a raiz e o Audit identicos aos do sandbox"', '"a arvore tem os %d modulos novos, e o modulo corrigido, a raiz e o Audit identicos aos do sandbox"', 1, "texto"),
    ("    # ------------------------------------------------------------------ os modulos (pedras) do recibo: declaracoes que o B(n) aceita (N1k)", "@arquivo:" + PP + "14_corrigido_antes.txt", 1,
     "o ANTES do corrigido == o manifesto v412 pinado; o DEPOIS == o instalado"),
    ("pos_build_kernel_v413_r7.py", "pos_build_kernel_v413.py", 2, "o nome do script sem o rotulo da rodada da v412"),
    ('              "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),',
     '              "pedras": pedras + pedras_kc, "kernel_corrigido": [{"path": r, "sha256_antes": kc_antes[r]["formal_files_v412"], "sha256_depois": kc_antes[r]["depois_na_arvore"], "declaracoes": kc_decl[r]["nomes"]} for r in KCRELS],\n'
     '              "formal_files_antes": ff, "axiomas": sorted(TRIO),', 1, "o recibo do kernel traz o corrigido: nas pedras (o B(n), N1l: novos ou mudados) e no campo kernel_corrigido (antes e depois)"),
    ("(Etapa 2 pelo contrato R11, decima segunda lista de pedras, 18/11/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v413 e do manifesto novo);",
     "(Etapa 1 da v413, 20/11/2026: os modulos novos da v413 e o modulo que ela corrige so' no texto); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v413 e do manifesto novo); o modulo corrigido esta' nas pedras (N1l do B(n): novos ou mudados) e, com o antes e o depois, no campo kernel_corrigido, que a ferramenta nao confere;", 1,
     "a nota do recibo"),
    ('"E411": E0,', '"E412": E0,', 1, "a escada de antes e' a da v412"),
    ('           "chaves_antigas": {"n": len(base_flags), "mudam": chaves_mudam},',
     '           "chaves_antigas": {"n": len(base_flags), "mudam": chaves_mudam},\n'
     '           "kernel_corrigido": {"modulos": KCMODS, "modo_no_build": modo_kc, "declaracoes": {k: {kk: vv for kk, vv in v.items() if kk != "nomes"} for k, v in kc_decl.items()}, "antes_depois": kc_antes,\n'
     '                                "dependentes_antigos_sem_linha_Built": dep_sem_built, "n_dependentes_antigos": len(dep_ant_mod)},\n'
     '           "avisos_modulos_antigos": {"n_modulos": len(antigos_com_aviso), "n_avisos": sum(antigos_com_aviso.values()), "por_modulo": antigos_com_aviso},', 1, "o POS_BUILD registra o corrigido e os avisos dos antigos"),
    ("proposta do construtor (claude-construtor-v412)", "proposta do construtor (claude-construtor-v413, como a v412 fez com _412_)", 1, "quem propoe os prefixos"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 9. A COPIA DOS LOGS (conferidor idempotente). Modo 'depois'.
D.append((os.path.join(V412, "copiar_logs_do_kernel_v412.py"), os.path.join(HERE, "copiar_logs_do_kernel_v413.py"), [
    ("# o da v412 era o do caso SEM modulo novo (nao lia LOGS_COPIADOS) e por isso nao e' o molde aqui (ordem da Etapa 1, item 4: para o que depende de bundle nao vazio, o molde e' a v411)",
     "# [v413] o molde e' o da v412 (bundle NAO vazio: le KH_N1 e LOGS_COPIADOS, que o pos_build grava); so' os rotulos sobem (v412->v413)", 1, "a subida v410->v411 nao vale nesta linha"),
    ('(molde: copiar_logs_do_kernel_v411.py)"""', '(molde: v412\\\\copiar_logs_do_kernel_v412.py)"""', 1, "o molde e' o da v412"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 10. O COMANDO UNICO DE RECONSTRUCAO. Modo 'depois'.
D.append((os.path.join(V412, "reconstruir_kernel_v412_r7.py"), os.path.join(HERE, "reconstruir_kernel_v413.py"), [
    ("(ordem da Etapa 1: a ordem 023 pode mudar texto de\nsete fontes e a gerencia regera o manifesto)",
     "(ordem da Etapa 1 da v413: a leitura de terceiro pode mudar docstrings;\na gerencia regera o manifesto e roda este comando)", 1, "o porque da v413"),
    ("(confere o sha256 de toda copia congelada contra o manifesto;", "(confere o sha256 de toda pedra limpa e da fonte corrigida contra o manifesto;", 1, "texto"),
    ("[--pedras <pasta>] [--so-preparar]", "[--pedras <pasta>] [--kernel-edits <pasta>] [--so-preparar]", 1, "a pasta da fonte corrigida pode ser trocada"),
    ('PADRAO = {"--manifesto": os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413_R12.json"), "--pedras": os.path.join(HERE, "insumos", "pedras_r12")}   # (r3: a quinta lista e\' o padrao)',
     'PADRAO = {"--manifesto": os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413.json"), "--pedras": os.path.join(HERE, "insumos", "pedras_limpas", "TGLExt")}   # (v413: o manifesto e as pedras limpas da gerencia)', 1,
     "o padrao da v413"),
    ("    extra += [k, sys.argv[sys.argv.index(k) + 1] if k in sys.argv else PADRAO[k]]",
     "    extra += [k, sys.argv[sys.argv.index(k) + 1] if k in sys.argv else PADRAO[k]]\n"
     "if \"--kernel-edits\" in sys.argv:   # (padrao: a pasta do campo saida do manifesto)\n"
     "    extra += [\"--kernel-edits\", sys.argv[sys.argv.index(\"--kernel-edits\") + 1]]", 1, "passa --kernel-edits ao preparo"),
    ('passo("3 pos_build_kernel_v413_r7", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "pos_build_kernel_v413_r7.py")])',
     'passo("3 pos_build_kernel_v413", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "pos_build_kernel_v413.py")])', 1, "o pos_build da v413"),
    ('print("RECONSTRUCAO DO KERNEL v413 (r7, decima segunda lista): TUDO PASSOU")', 'print("RECONSTRUCAO DO KERNEL v413 (os modulos novos e o corrigido): TUDO PASSOU")', 1, "texto"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 11. O PORTAO DO PILAR por leitura de codigo (item 5). Modo 'depois'. Nada roda na placa: so' ast sobre o um.py v412 selado.
D.append((os.path.join(V412, "portao_do_pilar_v412.py"), os.path.join(HERE, "portao_do_pilar_v413.py"), [
    ('"""portao_do_pilar_v413.py -- (claude-construtor-v412, 17/11/2026) Etapa 1, item 5:',
     '"""portao_do_pilar_v413.py -- (claude-construtor-v413, 20/11/2026; derivado de v412\\\\portao_do_pilar_v412.py, de claude-construtor-v412) Etapa 1, item 5:', 1, "autoria"),
    ("(3) se algo do que a v413 muda (modulos Lean novos -> _EMBEDDED_KERNEL_FILES e _LEAN_THEOREM_FLAGS; registros por especificacao; texto do artigo)",
     "(3) se algo do que a v413 muda (modulos Lean novos e a correcao de texto de um modulo do kernel -> _EMBEDDED_KERNEL_FILES e _LEAN_THEOREM_FLAGS; registros por especificacao; texto do artigo)", 1,
     "a correcao de texto do modulo do kernel"),
    ('"o_que_a_v413_muda": {"nomes": MUDA_V413 + ["registros por especificacao (texto do core)", "texto do artigo"],',
     '"o_que_a_v413_muda": {"nomes": MUDA_V413 + ["registros por especificacao (texto do core)", "texto do artigo"],\n'
     '                             "a_correcao_de_texto": "a docstring de TGLExt.OResumoEPsiBit (kernel_corrigido do manifesto) muda o texto embutido em _EMBEDDED_KERNEL_FILES; nao muda declaracao, bandeira, registro nem artigo",', 1,
     "a correcao de texto no relatorio"),
    ("logo os modulos Lean novos, os registros por especificacao e o texto da v413 NAO ",
     "logo os modulos Lean novos, a correcao de texto do modulo do kernel (que so' muda _EMBEDDED_KERNEL_FILES), os registros por especificacao e o texto da v413 NAO ", 1, "a resposta inclui a correcao"),
    ('"(foi assim na v411 e na v412, com o treino junto). Se o ambiente da placa mudar (o treino da Nativa pode ter "',
     '"(o que o rito da v412 fez esta\' nas linhas do pilar do stdout dele, em estado_lido). Se o ambiente da placa mudar (o treino da Nativa pode ter "', 1,
     "a frase de historia vira leitura do stdout da v412"),
    _grava_com_backup("out"),
], {"modo": "depois"}))

# ---------------------------------------------------------------- 12. O FECHO (item 6). Modo 'depois'. Molde: o fecho da Etapa 1 da v412; checagens no molde do gerar_pronto_kernel_r7_v412.py.
PG = "gerar_pronto_etapa1_v413__"
D.append((os.path.join(V412, "gerar_pronto_etapa1_v412.py"), os.path.join(HERE, "gerar_pronto_etapa1_v413.py"), [
    ("T12", "T13", 11, "o nome da variavel acompanha o rotulo (k413c)"),
    ("@@BLOCO", '"""gerar_pronto_etapa1_v413.py -- (claude-construtor-v412, 17/11/2026) FECHA', '-B -X utf8 gerar_pronto_etapa1_v413.py"""', "@arquivo:" + PG + "01_doc.txt", "a docstring da v413"),
    ("import datetime, hashlib, json, os, sys", "import datetime, hashlib, json, os, re, subprocess, sys", 1, "re e subprocess para as checagens e o conferidor dos logs"),
    ('bump = lj(os.path.join(HERE, "BUMP_v413_RESULTADO.json")) or {}',
     'der = lj(os.path.join(HERE, "DERIVACAO_ETAPA1_v413.json")) or {}\ninv = lj(os.path.join(HERE, "INVENTARIO_CADEIA_v413.json")) or {}\nult = lj(os.path.join(KD, "ULTIMA_INSTALACAO_v413.json")) or {}', 1,
     "a v413 tem derivacao e inventario no lugar do bump"),
    ('kernel_ok = bool(pos.get("ok"))', "@arquivo:" + PG + "04_desvios.txt", 1, "os desvios desta ordem"),
    ("@@BLOCO", "SCRIPTS = [", 'criados["(scripts bumpados na pasta da v413)"] = {"bytes": b_bump, "arquivos": len(bumpados)}', "@arquivo:" + PG + "05_scripts.txt",
     "os scripts da Etapa 1 da v413, a derivacao e o que a etapa criou"),
    ("@@BLOCO", "out = {", "nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move\",\n}", "@arquivo:" + PG + "06_out.txt",
     "as checagens e o conteudo do fecho da v413"),
    ("@@BLOCO", 'print(json.dumps({"etapa_1_fechou": kernel_ok,', '"pronto_sha16": sh16(p)}, ensure_ascii=False))', "@arquivo:" + PG + "07_print.txt", "o resumo e o codigo de saida"),
], {"modo": "depois"}))


def main():
    so = sys.argv[sys.argv.index("--so") + 1:] if "--so" in sys.argv else None
    log = json.load(open(LOGP, encoding="utf-8")) if os.path.exists(LOGP) else {"contrato": "DERIVACAO_ETAPA1_v413", "derivacoes": {}}
    feitos = 0
    for item in D:
        molde, destino, trocas = item[:3]
        opts = item[3] if len(item) > 3 else {}
        nome = os.path.basename(destino)
        if so and nome not in so:
            continue
        reg = derivar(molde, destino, trocas, **opts)
        log["derivacoes"][nome] = reg; feitos += 1
    if not SECO and feitos:
        log["gerado"] = TS; log["derivador_sha256"] = sha(open(os.path.abspath(__file__), "rb").read())
        log["vmap"] = VMAP
        b = json.dumps(log, ensure_ascii=False, indent=1).encode("utf-8")
        grava(LOGP, b)
    print("DERIVADOS:", feitos, "| registro:", LOGP if not SECO else "(seco)")


if __name__ == "__main__":
    main()
