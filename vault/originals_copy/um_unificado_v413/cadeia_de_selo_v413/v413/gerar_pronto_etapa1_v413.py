# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\gerar_pronto_etapa1_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
"""gerar_pronto_etapa1_v413.py -- (claude-construtor-v413, 20/11/2026; derivado de v412\\gerar_pronto_etapa1_v412.py, com checagens no molde de v412\\gerar_pronto_kernel_r7_v412.py) FECHA a
Etapa 1 da preparacao da v413 em PRONTO_PARA_CANDIDATO_v413.json (ordem da Etapa 1 da v413, item 6): o estado MEDIDO (o recibo do kernel, a escada, as declaracoes, os avisos por modulo, o modulo
corrigido, os scripts derivados com sha16, a resposta do portao do pilar, o inventario do item 4) e o que falta para a Etapa 2. Tudo LIDO dos artefatos (nada digitado); o que nao existir aparece
como ausente; cada checagem diz quantos itens examinou. Roda o conferidor dos logs (copiar_logs_do_kernel_v413.py, que so' le) e registra o codigo de saida. Grava tambem TAMANHOS_CRIADOS_v413.json
(o que a etapa criou e quanto ocupa). uso: C:\\Python314\\python.exe -B -X utf8 gerar_pronto_etapa1_v413.py"""
import datetime, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel")
T13 = os.path.join("C:" + os.sep, "t", "k413c")
sha = lambda b: hashlib.sha256(b).hexdigest()


def sh16(p):
    return sha(open(p, "rb").read())[:16] if os.path.exists(p) else None


def lj(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def tamanho(raiz, seguir=False):
    tot = n = 0
    if os.path.isfile(raiz):
        return os.path.getsize(raiz), 1
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        try:
            it = list(os.scandir(d))
        except FileNotFoundError:
            continue
        for e in it:
            if (e.is_junction() or e.is_symlink()) and not seguir:
                continue
            if e.is_dir(follow_symlinks=False):
                pilha.append(e.path)
            elif e.is_file(follow_symlinks=False):
                tot += e.stat(follow_symlinks=False).st_size; n += 1
    return tot, n


pos = lj(os.path.join(KD, "POS_BUILD_v413.json")) or {}
rec = lj(os.path.join(KD, "KERNEL_RECIBO_v413.json")) or {}
flg = lj(os.path.join(KD, "FLAGS_v413.json")) or {}
kh = lj(os.path.join(KD, "KH_N1_v413.json")) or {}
bd = lj(os.path.join(HERE, "BUNDLE_v413.json")) or {}
conf = lj(os.path.join(HERE, "CONFERENCIA_FONTES_K412C_v413.json")) or {}
prec = lj(os.path.join(KD, "PRE_COLISAO_v413.json")) or {}
pil = lj(os.path.join(HERE, "PORTAO_DO_PILAR_v413.json")) or {}
der = lj(os.path.join(HERE, "DERIVACAO_ETAPA1_v413.json")) or {}
inv = lj(os.path.join(HERE, "INVENTARIO_CADEIA_v413.json")) or {}
ult = lj(os.path.join(KD, "ULTIMA_INSTALACAO_v413.json")) or {}
base = lj(os.path.join(HERE, "BASE_V412_COPIA.json")) or {}
man_p = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413.json"); man = lj(man_p) or {}
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(KD, "construir_marcas.txt")) else ""
kernel_ok = bool(pos.get("ok"))
DESVIOS = [
    "a derivacao (item 4) foi por trocas de texto EXATO com contagem registrada; nos tres scripts que mudam de logica (o preparador, o pos-build e este fecho) as trocas sao em BLOCO (o trecho entre "
    "marcas unicas trocado pelo texto de derivacao_blocos\\, lido em bytes): o formato do manifesto da v413 (modulos_novos, sha256_pedra_limpa, imports_tglext, ordem_topologica_sugerida), as fontes ja' "
    "na forma do kernel (nenhum import trocado) e o modulo corrigido nao cabem em subida de rotulo; DERIVACAO_ETAPA1_v413.json e os diffs em bump\\ dizem cada troca",
    "o fecho deriva de v412\\gerar_pronto_etapa1_v412.py (o fecho da Etapa 1 da v412: ja' tem o portao do pilar, os scripts com sha16 e os tamanhos), com checagens no molde de "
    "gerar_pronto_kernel_r7_v412.py; o r7 le recibos de rodadas da v412 que a v413 nao tem (os estados R4/R5, as listas decima e duodecima, as ancoras propostas pela gerencia)",
    "o construir_kernel_v413.sh constroi primeiro o modulo corrigido e depois os novos; o build inteiro recompila os modulos ANTIGOS que dependem do corrigido (a lista esta' em "
    "kernel\\ULTIMA_INSTALACAO_v413.json): o build e' incremental so' no que nao depende dele",
    "a TowerWedgeIndex e' modulo antigo na v413: o aviso conhecido e' lido do bloco dela no log (Replayed, ou Built se recompilada), registrado, nao consertado; os avisos dos outros modulos antigos "
    "aparecem contados a parte em POS_BUILD_v413.json (preexistentes, repetidos pelo lake; nada se conserta)",
    "a base (base_v412\\, copia de bytes do Nos) e' conferida pelo pino do selo do Nos e pelo candidato_sha16 de v412\\ESPERADOS_v412.json e de v412\\CANDIDATO_v412.json: a v413 ainda nao tem desenho "
    "nem contrato, de onde a v412 lia o sha16 da base",
    "o recibo do kernel (KERNEL_RECIBO_R3_2) lista o modulo corrigido nas pedras, junto dos novos (lido em verificar_kernel_recibo da R3_6: N1l exige pedras == os arquivos formais novos ou mudados), "
    "e ganhou o campo kernel_corrigido (path, sha256 antes e depois, declaracoes), que a ferramenta nao confere; verificar_kernel_recibo nao rodou (precisa do selo da v413)",
    "copiar_k413c.sh rodou com o texto da primeira derivacao, que so' diferia do final no comentario de autoria (a primeira derivacao subia a autoria claude-construtor-v412 e as marcas historicas; "
    "corrigido no derivador; o texto anterior esta' no .bak_ ao lado)",
    "ERRO MEU, dito: a conferencia das fontes (conferir_fontes_k412c_vs_nos_v413.py) rodou ANTES da copia e foi rodada de novo DEPOIS dela; o molde grava a saida por cima, sem backup, e a segunda "
    "rodada sobrescreveu a primeira. A comparacao das fontes e o tamanho da origem sao os mesmos nas duas; o espaco livre gravado em CONFERENCIA_FONTES_K412C_v413.json e' o da ultima rodada (depois "
    "da copia). [DECLARADO pelo construtor, da saida impressa da primeira rodada, que nao ficou em disco]: antes da copia, origem 11599961999 bytes em 17226 arquivos (sem seguir a juncao) e 2131938852864 "
    "bytes livres no disco C:. CAUSA corrigida nos quatro scripts que gravam saida assim (a conferencia das fontes, a copia da base, a pre-colisao e o portao do pilar): backup de bytes antes de "
    "regravar; os quatro rodaram de novo com o texto corrigido",
    "memoria ACOM: a ordem diz que o construtor nao escreve a memoria ACOM; nao inscrevi referencia (a regra global pede init e project ao abrir a sessao); fica para a gerencia",
    "o rotulo da Bancada nao entra em nenhum script da Etapa 1; o medido do disco esta' em INVENTARIO_CADEIA_v413.json (bancada_medida) para a Etapa 2",
]
SCRIPTS = ["derivar_scripts_etapa1_v413.py", "conferir_fontes_k412c_vs_nos_v413.py", "copiar_k413c.sh", "copiar_base_v413.py", "pre_colisao_declaracoes_v413.py", "lean_texto_v413.py",
           "preparar_bundle_v413.py", "construir_kernel_v413.sh", "pos_build_kernel_v413.py", "copiar_logs_do_kernel_v413.py", "reconstruir_kernel_v413.py", "portao_do_pilar_v413.py",
           "inventario_cadeia_v413.py", "gerar_pronto_etapa1_v413.py"]
scripts = {s: sh16(os.path.join(HERE, *s.split("/"))) for s in SCRIPTS}
runners = {n: sh16(os.path.join(T13, n)) for n in ("run_build.py", "run_pos_treino.py")}
# a derivacao (item 4): cada destino registrado em DERIVACAO_ETAPA1_v413.json, com o sha16 registrado e o que esta' em disco agora
derivados = {}
for nome_, r_ in (der.get("derivacoes") or {}).items():
    dest_ = r_.get("destino")
    derivados[nome_] = {"molde": r_.get("molde"), "molde_sha16": (r_.get("molde_sha256") or "")[:16], "destino": dest_, "destino_sha16_registrado": r_.get("destino_sha16"),
                        "destino_sha16_em_disco": sh16(dest_) if dest_ else None, "modo": r_.get("modo"), "trocas": len(r_.get("trocas") or []),
                        "rotulos_subidos": sum(v for k, v in (r_.get("rotulos_subidos") or {}).items() if k != "marcas_historicas_preservadas"),
                        "marcas_historicas_preservadas": (r_.get("rotulos_subidos") or {}).get("marcas_historicas_preservadas", 0), "diff": r_.get("diff")}
avisos = pos.get("avisos_por_modulo") or {}
n_mod = int(bd.get("n") or 0)
compilaram = sum(1 for v in (pos.get("por_modulo_marcas") or {}).values() if v.get("rc") == 0)
# o que a etapa criou e quanto ocupa (fora de work: C:\t\k413c; em work: a pasta da v413, so' o que e' desta etapa)
criados = {}
for p_ in (os.path.join(T13, "final"), os.path.join(T13, "arvore")):
    b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_, "nota": "sem seguir a juncao .lake\\packages" if p_.endswith("final") else "arvore so-fontes do recibo"}
for e in (os.scandir(T13) if os.path.isdir(T13) else []):
    if e.is_dir() and e.name.startswith("quarentena_"):
        b_, n_ = tamanho(e.path); criados[e.path] = {"bytes": b_, "arquivos": n_, "nota": "backups de bytes do que o preparo trocou no sandbox"}
soltos_t13 = [os.path.join(T13, f_) for f_ in ("run_build.py", "run_pos_treino.py", "robocopy_final.log", "robocopy_done.txt", "build_inicio.txt") if os.path.exists(os.path.join(T13, f_))]
criados[os.path.join(T13, "(arquivos soltos)")] = {"bytes": sum(os.path.getsize(q_) for q_ in soltos_t13), "arquivos": len(soltos_t13)}
for rel in ("base_v412", "kernel", "pedra", "bump", "vinculo", "derivacao_blocos"):
    p_ = os.path.join(HERE, rel)
    if os.path.exists(p_):
        b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_}
soltos = SCRIPTS + ["BUNDLE_v413.json", "kernel_modulos_novos_v413.json", "CONFERENCIA_FONTES_K412C_v413.json", "BASE_V412_COPIA.json", "PORTAO_DO_PILAR_v413.json", "DERIVACAO_ETAPA1_v413.json",
                    "INVENTARIO_CADEIA_v413.json", "PRONTO_PARA_CANDIDATO_v413.json", "TAMANHOS_CRIADOS_v413.json"]
b_soltos = sum(os.path.getsize(os.path.join(HERE, *s.split("/"))) for s in soltos if os.path.exists(os.path.join(HERE, *s.split("/"))))
criados["(arquivos soltos desta etapa na pasta da v413)"] = {"bytes": b_soltos, "arquivos": len(soltos)}
baks = [f_ for f_ in os.listdir(HERE) if ".bak_" in f_]
criados["(backups .bak_ das rederivacoes, na pasta da v413)"] = {"bytes": sum(os.path.getsize(os.path.join(HERE, f_)) for f_ in baks), "arquivos": len(baks)}
tot_fora = sum(v["bytes"] for k, v in criados.items() if k.startswith(T13))
tot_work = sum(v["bytes"] for k, v in criados.items() if not k.startswith(T13))
tam = {"criados": criados, "total_fora_de_work_bytes": tot_fora, "total_fora_de_work_gb": round(tot_fora / 1e9, 3), "total_em_work_bytes": tot_work, "total_em_work_mb": round(tot_work / 1e6, 1)}
# ---------------------------------------------------------------- as checagens do fecho (no molde de v412\gerar_pronto_kernel_r7_v412.py): cada uma diz quantos itens examinou
CH = []


def chk(nome, ok, n_itens, detalhe=None):
    CH.append({"checagem": nome, "ok": bool(ok), "n_itens_examinados": n_itens, "detalhe": detalhe})


modo = pos.get("modo_dos_modulos_no_build") or {}
kcp = pos.get("kernel_corrigido") or {}
n_kc = len(kcp.get("modulos") or [])
n_marcas = len(re.findall(r"(?m)^modulo=\S+ rc=0 s=\d+$", marcas))
chk("todos os modulos com saida zero nas marcas (o corrigido e os %d novos), rc final 0, sem parou_em" % n_mod,
    n_mod > 0 and n_kc > 0 and n_marcas == n_mod + n_kc and bool(re.search(r"(?m)^rc=0$", marcas)) and not re.search(r"(?m)^parou_em=", marcas), n_marcas)
chk("o pos_build esta verde (nenhuma falha que nao seja informativa)", pos.get("ok") is True and not pos.get("falhas"), len(pos.get("sinais") or []), pos.get("falhas"))
chk("compilacao A FRIO dos modulos novos (linha Built para todos) e o corrigido com linha Built", pos.get("todos_os_modulos_a_frio") is True and len(modo) == n_mod
    and n_kc > 0 and all(v == "Built" for v in (kcp.get("modo_no_build") or {}).values()), len(modo) + n_kc, {k: v for k, v in modo.items() if v != "Built"})
lt = pos.get("linha_TOTAL") or {}
chk("fora dos tres axiomas: zero declaracoes (linha TOTAL e criterio j1); zero sorry e zero erro no recibo do kernel",
    lt.get("fora_do_trio") == 0 and (pos.get("criterios") or {}).get("j1_fora_do_trio") == 0 and rec.get("sorry") == 0 and rec.get("erros") == 0, lt.get("decl"))
ca = pos.get("chaves_antigas") or {}
chk("nenhuma chave antiga muda de literal", not ca.get("mudam") and (ca.get("n") or 0) > 0, ca.get("n"))
pref = flg.get("prefixos") or {}
chk("os prefixos das bandeiras novas sao ext_<modulo em minusculas>_413_ e distintos entre si",
    len(set(pref.values())) == len(pref) == n_mod and all(p == "ext_%s_413_" % m.split(".")[-1].lower() for m, p in pref.items()), len(pref))
sem_flag = sorted(m for m, n in (flg.get("n_por_modulo") or {}).items() if n == 0)
chk("(informativo) todo modulo novo tem pelo menos uma bandeira (declaracao nomeada publica): %d sem" % len(sem_flag), True, len(flg.get("n_por_modulo") or {}), sem_flag)
outros_av = {m: v.get("n") for m, v in avisos.items() if v.get("n")}
chk("nenhum modulo novo nem o corrigido com aviso; o aviso conhecido e preexistente da TowerWedgeIndex (modulo antigo) registrado, nao consertado",
    not outros_av and (pos.get("aviso_conhecido_TowerWedgeIndex") or {}).get("parece_o_conhecido") is True, len(avisos), outros_av)
esc = flg.get("escada") or []
chk("a escada medida: [antes, depois] = [a da v412 (core da base), mais as bandeiras novas]",
    len(esc) == 2 and esc[1] == esc[0] + int(flg.get("n_flags") or -1) and (kh.get("linha_TOTAL") or {}).get("decl") == lt.get("decl") and pos.get("E412") == esc[0], flg.get("n_flags"), esc)
kd_ = kcp.get("declaracoes") or {}
chk("o modulo corrigido: as mesmas declaracoes da v412 com os mesmos axiomas; ANTES == o manifesto v412 pinado == sha256_origem; DEPOIS == o instalado pelo preparo",
    bool(kd_) and all(v.get("iguais") and v.get("mesmos_axiomas") for v in kd_.values())
    and bool(kcp.get("antes_depois")) and all(v.get("formal_files_v412") == v.get("sha256_origem") and v.get("depois_na_arvore") == v.get("instalado_pelo_preparo") for v in (kcp.get("antes_depois") or {}).values()),
    len(kd_), kd_)
chk("a pre-conferencia de nomes nao achou colisao (nome exato, prefixo de estrutura, entre os novos); o corrigido so' declara nomes que o kernel ja tem; as fontes do k412c eram as do Nos",
    not prec.get("colisao_com_o_kernel_nome_exato") and not prec.get("colisao_com_o_kernel_prefixo_de_estrutura") and not prec.get("colisao_entre_os_modulos_da_lista")
    and prec.get("kernel_corrigido_ok") is True and not prec.get("sha256_fora_do_manifesto") and conf.get("identico") is True and conf.get("sem_colisao_de_nome_de_modulo") is True
    and conf.get("kernel_corrigido_origem_igual_no_nos_e_no_sandbox") is True, prec.get("n_nomes_lidos"))
man_sha_ = hashlib.sha256(open(man_p, "rb").read()).hexdigest() if os.path.exists(man_p) else None
chk("a unica transformacao no texto das fontes: as linhas #print axioms retiradas; nenhum import trocado; o preparo pinou cada sha256 (BUNDLE com o manifesto atual)",
    bd.get("manifesto_sha256") == man_sha_ and sum(len(m_.get("imports_trocados") or []) for m_ in (bd.get("modulos") or [])) == 0 and n_mod > 0, n_mod,
    {"print_axioms_retirados": sum(m_.get("n_print_axioms_removidos", 0) for m_ in (bd.get("modulos") or []))})
# o Nos intacto (so' leitura): o um.py e' o que o selo v412 pina; nenhum modulo novo no kernel do Nos; o corrigido do Nos ainda e' o de origem
NOS_ = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
selo_ = lj(os.path.join(NOS_, "um_absoluto_selo.json")) or {}
um_nos = sha(open(os.path.join(NOS_, "um.py"), "rb").read())
novos_no_nos = [m_["rel"] for m_ in (bd.get("modulos") or []) if os.path.exists(os.path.join(NOS_, "tgl_kernel", *m_["rel"].split("/")))]
kc_nos = {k_["rel"]: sha(open(os.path.join(NOS_, "tgl_kernel", *k_["rel"].split("/")), "rb").read()) == k_["sha256_origem"] for k_ in (bd.get("kernel_corrigido") or [])}
chk("o Nos intacto: o um.py e' o que o selo v412 pina; nenhum modulo novo no kernel do Nos; o modulo corrigido do Nos ainda e' o de origem",
    selo_.get("um_version") == "v412" and um_nos == (selo_.get("sha256") or {}).get("um.py") and not novos_no_nos and bool(kc_nos) and all(kc_nos.values()),
    1 + n_mod + len(kc_nos), {"um_py_sha16": um_nos[:16], "novos_no_nos": novos_no_nos, "corrigido_do_nos_igual_a_origem": kc_nos})
ITEM4 = ["preparar_bundle_v413.py", "run_build.py", "pos_build_kernel_v413.py", "copiar_logs_do_kernel_v413.py", "reconstruir_kernel_v413.py", "gerar_pronto_etapa1_v413.py"]
chk("os scripts da Etapa 1 derivados (o preparador, o run_build, o pos-build, a copia dos logs, o comando unico e este fecho; o construtor do kernel e' gerado pelo preparo) com o sha16 do registro == o do disco",
    all(n_ in derivados and derivados[n_]["destino_sha16_registrado"] == derivados[n_]["destino_sha16_em_disco"] for n_ in ITEM4) and os.path.exists(os.path.join(HERE, "construir_kernel_v413.sh")),
    len(derivados), {n_: (derivados.get(n_) or {}).get("destino_sha16_em_disco") for n_ in ITEM4})
chk("o inventario dos demais scripts da cadeia da v412 (candidato, instalar, reverter, rito, conferidor, handoff) existe e descreve cada um",
    bool(inv.get("papeis")) and all(e_.get("o_que_muda") not in (None, "(a descrever)") for v_ in inv["papeis"].values() for e_ in v_.values() if not e_.get("ausente")),
    sum(len(v_) for v_ in (inv.get("papeis") or {}).values()))
om_ = pil.get("o_que_a_v413_muda") or {}
chk("o portao do pilar respondido por leitura de codigo: nada do que a v413 muda entra no fecho da chave nem no da decisao de reuso",
    pil.get("resposta") is not None and not om_.get("entra_no_fecho_da_chave") and not om_.get("nomes_de_registro_ou_artigo_no_fecho_da_chave") and not om_.get("entra_no_fecho_da_decisao_de_reuso"),
    len(pil.get("fecho_dos_nomes_de_topo_da_chave") or []))
r_logs = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "copiar_logs_do_kernel_v413.py")], capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
chk("o conferidor dos logs (copiar_logs_do_kernel_v413.py, so' leitura) confere", r_logs.returncode == 0, 1, (r_logs.stdout or "").strip().splitlines()[-1:])
tmps = [os.path.join(d_, f_) for d_ in (HERE, KD, os.path.join(KD, "bundle"), T13) if os.path.isdir(d_) for f_ in os.listdir(d_) if f_.endswith(".tmp") or ".tmp_" in f_]
chk("nenhum .tmp deixado (pasta da v413, kernel\\, kernel\\bundle\\ e C:\\t\\k413c)", not tmps, 4, tmps[:5])
etapa_ok = kernel_ok and all(c_["ok"] for c_ in CH)
out = {
    "contrato": "PRONTO_PARA_CANDIDATO_v413",
    "quando": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "agente": "claude-construtor-v413, a servico da gerencia c1",
    "estado": ("ETAPA 1 CONCLUIDA: sandbox k413c, os %d modulos novos e o modulo corrigido instalados e compilados no sandbox, Audit medido, scripts da Etapa 1 derivados, inventario feito, portao do pilar "
               "respondido por leitura de codigo; PAROU aqui: nada de registros, artigo, guarda de frases nem candidato (ordem da Etapa 1 da v413, item 6)" % n_mod) if etapa_ok else
              ("ETAPA 1 NAO FECHOU: ver as checagens que falharam (%s); kernel\\POS_BUILD_v413.json: parou_em=%s; nada foi consertado em prova nem em nome" % ([c_["checagem"] for c_ in CH if not c_["ok"]], pos.get("parou_em"))),
    "etapa_1_fechou": etapa_ok,
    "checagens": CH,
    "ordem": {"arquivo": "ORDEM_ETAPA_1_v413.md", "sha16": sh16(os.path.join(HERE, "ORDEM_ETAPA_1_v413.md"))},
    "manifesto": {"arquivo": "insumos/MANIFESTO_PEDRAS_v413.json", "sha16": sh16(man_p), "gerado_em": man.get("gerado_em"), "n_modulos_novos": man.get("n_modulos_novos"),
                  "teoremas_publicos_novos": man.get("teoremas_publicos_novos"), "kernel_corrigido": sorted((man.get("kernel_corrigido") or {}).keys())},
    "base_v412": {"um_py_sha16": base.get("base_sha16"), "selo": base.get("selo_um_version"), "copia": "base_v412\\ (BASE_V412_COPIA.json, sha16 %s)" % sh16(os.path.join(HERE, "BASE_V412_COPIA.json"))},
    "kernel_k413c": {
        "sandbox": os.path.join(T13, "final"), "origem": conf.get("sandbox_origem"),
        "origem_medida_antes_da_copia": {"bytes_sem_juncoes": conf.get("origem_bytes_sem_juncoes"), "gb": conf.get("origem_gb_sem_juncoes"), "arquivos": conf.get("origem_arquivos")},
        "disco_C_livre_gb_na_ultima_conferencia": conf.get("disco_C_livre_gb"),
        "medicao_de_antes_da_copia": "[DECLARADO] a primeira rodada da conferencia, antes da copia, foi sobrescrita pela segunda (ver desvios_desta_ordem); o arquivo guarda a ultima rodada",
        "copia": "robocopy SEM /PURGE (copiar_k413c.sh), juncao .lake\\packages -> C:\\t\\k404c\\final\\.lake\\packages; fontes da origem conferidas contra o Nos v412 (CONFERENCIA_FONTES_K412C_v413.json: %s de %s iguais; diferentes %s; so' num lado: %s e %s)" % (
            conf.get("n_comuns"), conf.get("n_nos"), conf.get("n_diferentes"), len(conf.get("so_no_nos") or []), len(conf.get("so_no_sandbox") or [])),
        "marcas": dict(l.split("=", 1) for l in marcas.splitlines() if "=" in l and not l.startswith("modulo=")),
        "por_modulo": pos.get("por_modulo_marcas"), "modulos_compilados_rc0": compilaram, "n_modulos_novos": n_mod, "n_modulos_corrigidos": n_kc, "parou_em": pos.get("parou_em"),
        "duracao_build_s": pos.get("duracao_build_s"), "duracao_audit_s": pos.get("duracao_audit_s"),
        "linha_TOTAL": pos.get("linha_TOTAL"), "linha_TOTAL_v412": pos.get("linha_TOTAL_v412"), "delta_vs_v412": pos.get("delta_vs_v412"),
        "declaracoes_no_relatorio_de_axiomas": pos.get("n_decl_audit"), "todas_no_trio": (pos.get("criterios") or {}).get("declaracoes_novas_no_trio"),
        "escada_de_teoremas_e_bandeiras": pos.get("escada"), "n_bandeiras_novas": pos.get("n_flags"), "n_ancoras_print_axioms": pos.get("n_ancoras"),
        "chaves_antigas": pos.get("chaves_antigas"), "todos_os_modulos_a_frio": pos.get("todos_os_modulos_a_frio"),
        "avisos_por_modulo": {k: v.get("n") for k, v in avisos.items()}, "aviso_conhecido_TowerWedgeIndex": pos.get("aviso_conhecido_TowerWedgeIndex"),
        "avisos_modulos_antigos": {k: v for k, v in (pos.get("avisos_modulos_antigos") or {}).items() if k != "por_modulo"},
        "kernel_corrigido": kcp, "dependentes_antigos_do_corrigido_recompilados": {"n": len(ult.get("dependentes_antigos_do_corrigido_que_o_lake_recompila") or []),
                                                                                     "sem_linha_Built": kcp.get("dependentes_antigos_sem_linha_Built")},
        "falhas": pos.get("falhas"), "falhas_informativas": pos.get("falhas_informativas"),
        "colisoes": {"nome_de_modulo_sem_caixa": conf.get("colisoes_de_nome_de_modulo_sem_caixa"),
                     "pre_conferencia_de_declaracoes": {k: prec.get(k) for k in ("colisao_com_o_kernel_nome_exato", "colisao_com_o_kernel_prefixo_de_estrutura", "colisao_entre_os_modulos_da_lista", "kernel_corrigido")},
                     "juiz_definitivo": "o build da raiz no sandbox (o Lean recusa ambiente com nome repetido): %s" % ("passou" if kernel_ok else "ver POS_BUILD")},
        "recibo": {"arquivo": "kernel/KERNEL_RECIBO_v413.json", "sha16": sh16(os.path.join(KD, "KERNEL_RECIBO_v413.json")), "rc": rec.get("rc"), "sorry": rec.get("sorry"), "erros": rec.get("erros"),
                   "contrato": rec.get("contrato"), "campo_novo": "kernel_corrigido" if rec.get("kernel_corrigido") else None},
        "POS_BUILD_sha16": sh16(os.path.join(KD, "POS_BUILD_v413.json")), "FLAGS_sha16": sh16(os.path.join(KD, "FLAGS_v413.json")), "KH_N1_sha16": sh16(os.path.join(KD, "KH_N1_v413.json")),
        "LOGS_COPIADOS_sha16": sh16(os.path.join(KD, "LOGS_COPIADOS_v413.json")), "CRITERIOS_sha16": sh16(os.path.join(HERE, "vinculo", "CRITERIOS_v413.json")),
        "lake_build_log": {"bytes": os.path.getsize(os.path.join(KD, "lake_build.log")) if os.path.exists(os.path.join(KD, "lake_build.log")) else None, "sha16": sh16(os.path.join(KD, "lake_build.log"))},
        "audit_log": {"bytes": kh.get("audit_log_bytes"), "sha16": (kh.get("audit_log_sha256") or "")[:16]},
        "criterios": pos.get("criterios"),
        "copias_do_kernel_fora_de_work": [os.path.join(T13, "final") + " (o sandbox)", os.path.join(T13, "arvore") + " (a arvore so-fontes do recibo)"] + [k for k in criados if "quarentena_" in k]},
    "bundle": {"arquivo": "BUNDLE_v413.json", "sha16": sh16(os.path.join(HERE, "BUNDLE_v413.json")), "ordem_topologica": bd.get("ordem_topologica"),
               "ordem_topologica_igual_a_sugerida": bd.get("ordem_topologica_igual_a_sugerida"), "root_suffix_linhas": len((bd.get("root_suffix") or "").splitlines()),
               "mudancas_no_texto": bd.get("normalizacao"),
               "por_modulo": {m["modulo"]: {"sha256_insumo": m["sha256_insumo"], "sha256_instalado": m["sha256"], "print_axioms_removidos": m["n_print_axioms_removidos"],
                                            "imports_trocados": len(m["imports_trocados"]), "diff": m["diff"]} for m in (bd.get("modulos") or [])},
               "kernel_corrigido": {k_["modulo"]: {"sha256_origem": k_["sha256_origem"], "sha256_insumo": k_["sha256_insumo"], "sha256_instalado": k_["sha256"], "diff": k_["diff"],
                                                   "novos_que_dependem_dele": k_.get("novos_que_dependem_dele"), "n_dependentes_antigos_no_kernel": len(k_.get("dependentes_antigos_no_kernel") or [])}
                                    for k_ in (bd.get("kernel_corrigido") or [])},
               "sha256_por_modulo": "kernel/bundle/SHA256_POR_MODULO_v413.json (sha16 %s)" % sh16(os.path.join(KD, "bundle", "SHA256_POR_MODULO_v413.json")),
               "trocar_uma_fonte": "um comando: C:\\Python314\\python.exe -B -X utf8 reconstruir_kernel_v413.py --manifesto <json> --pedras <pasta> [--kernel-edits <pasta>] (preparo idempotente; o lake recompila so' o modulo trocado e os dependentes, mais a raiz e o Audit; kernel\\ULTIMA_INSTALACAO_v413.json diz quais)"},
    "scripts_da_etapa_sha16": scripts, "lancadores_em_C_t_k413c_sha16": runners,
    "derivacao": {"arquivo": "DERIVACAO_ETAPA1_v413.json", "sha16": sh16(os.path.join(HERE, "DERIVACAO_ETAPA1_v413.json")), "derivador": "derivar_scripts_etapa1_v413.py",
                  "diffs": "bump\\ (um .diff por destino)", "blocos": "derivacao_blocos\\ (os textos novos das trocas em bloco, lidos em bytes; sha256 de cada um no registro)",
                  "regra": "trocas de texto EXATO com contagem EXATA (ou bloco entre marcas unicas), registradas; subida simultanea dos rotulos (v412->v413, v411->v412, k412c->k413c, _412_->_413_); as marcas historicas de cabecalho e a autoria claude-construtor-v412 nao sobem",
                  "derivados": derivados},
    "inventario": {"arquivo": "INVENTARIO_CADEIA_v413.json", "sha16": sh16(os.path.join(HERE, "INVENTARIO_CADEIA_v413.json")), "bancada_medida": inv.get("bancada_medida"),
                   "o_que_muda": {papel: {rel: e_.get("o_que_muda") for rel, e_ in v_.items()} for papel, v_ in (inv.get("papeis") or {}).items()}},
    "portao_do_pilar": {"arquivo": "PORTAO_DO_PILAR_v413.json", "sha16": sh16(os.path.join(HERE, "PORTAO_DO_PILAR_v413.json")), "resposta": pil.get("resposta"),
                        "entradas_da_chave": pil.get("entradas_da_chave"), "fecho": pil.get("fecho_dos_nomes_de_topo_da_chave"), "o_que_a_v413_muda": pil.get("o_que_a_v413_muda"),
                        "chave_do_ultimo_rito_v412": (pil.get("estado_lido") or {}).get("chaves_no_stdout_v412"), "o_reuso_usa_a_placa": pil.get("o_reuso_toca_a_placa_de_leve")},
    "falta_para_a_etapa_2": [
        "a gerencia: a leitura de terceiro (Codex) dos textos limpos; se mudar docstring, regerar o manifesto e rodar reconstruir_kernel_v413.py --manifesto <json> --pedras <pasta> (um comando; so' o que depende da fonte recompila; a fonte corrigida vem do manifesto ou de --kernel-edits)",
        "a gerencia: o contrato da v413 (registros por especificacao, secao do artigo, guarda de frases, pagina publica) e os prefixos das bandeiras (proposta em kernel\\FLAGS_v413.json: ext_<modulo>_413_NNNN; nenhuma chave antiga muda)",
        "Etapa 2 (NOVO na v413): o gerador do candidato tem de SUBSTITUIR o texto embutido de TGLExt/OResumoEPsiBit.lean em _EMBEDDED_KERNEL_FILES (o da v412 so' acrescenta modulos); o instalador tem de conferir e guardar backup de bytes de tgl_kernel\\TGLExt\\OResumoEPsiBit.lean e o reverter restaura-lo; o conferidor pos-rito confere o sha256_saida no Nos e as mesmas declaracoes (INVENTARIO_CADEIA_v413.json, o_que_muda)",
        "Etapa 2: o B(n) le o recibo do kernel (KERNEL_RECIBO_R3_2): pela leitura de verificar_kernel_recibo (R3_6), N1l exige pedras == os arquivos formais NOVOS OU MUDADOS do manifesto pinado pelo selo; o corrigido ja' entrou nas pedras, com as declaracoes (N1k), e o campo kernel_corrigido (antes e depois) nao e' conferido pela ferramenta; rodar a ferramenta depois do selo, como sempre",
        "Etapa 2: as ancoras dos registros (as declaracoes que os registros da v413 citam); os #print axioms das fontes ja' conferiram como ancoras no Audit (n_ancoras_print_axioms)",
        "Etapa 2: o portao do pilar NO CANDIDATO (os textos do fecho da chave com o sha256 de PORTAO_DO_PILAR_v413.json) e, antes do rito, o ambiente da placa igual ao do cache (senao PARAR e avisar o operador)",
        "Etapa 2: os scripts do inventario (candidato, instalar, reverter, rito, conferidor, handoff), adaptados do molde da v412 com o caso do modulo corrigido; a v412 usou a Etapa 3 enxuta (conferir_pos_rito_v412_foco.py, esperados_v412_foco.py): decisao da gerencia se repete",
        "a gerencia: a tarefa agendada (C:\\t\\k413c\\run_pos_treino.py ja' existe e aponta para orquestrador\\pos_treino_v413.py, que ainda nao existe), instalar, o rito, a custodia"],
    "desvios_desta_ordem": DESVIOS,
    "estatuto": "[REAL] medido no sandbox C:\\t\\k413c\\final; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
p = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v413.json")
for nome, obj in ((p, out), (os.path.join(HERE, "TAMANHOS_CRIADOS_v413.json"), tam)):
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(nome):
        bk = nome + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(nome, "rb").read())
    open(nome + ".tmp", "wb").write(b); assert os.path.getsize(nome + ".tmp") == len(b); os.replace(nome + ".tmp", nome)
print(json.dumps({"etapa_1_fechou": etapa_ok, "escada": pos.get("escada"), "decl": pos.get("n_decl_audit"), "compilaram": compilaram, "n_novos": n_mod, "n_corrigidos": n_kc,
                  "checagens": "%d de %d" % (sum(1 for c_ in CH if c_["ok"]), len(CH)), "tamanhos": {"fora_gb": tam["total_fora_de_work_gb"], "work_mb": tam["total_em_work_mb"]},
                  "pronto_sha16": sh16(p)}, ensure_ascii=False))
for c_ in CH:
    if not c_["ok"]:
        print("FALHOU:", c_["checagem"], c_["n_itens_examinados"], str(c_["detalhe"])[:300])
sys.exit(0 if etapa_ok else 1)
