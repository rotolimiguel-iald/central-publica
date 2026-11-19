# -*- coding: utf-8 -*-
"""gerar_pronto_etapa1_v412.py -- (claude-construtor-v412, 17/11/2026) FECHA a Etapa 1 da preparacao da v412 em PRONTO_PARA_CANDIDATO_v412.json (ordem da Etapa 1, item 6): o estado MEDIDO
(o recibo do kernel, a escada, as declaracoes, os avisos por modulo, os scripts adaptados com sha16, a resposta do portao do pilar, o bump) e o que falta para a Etapa 2. Tudo LIDO dos artefatos
(nada digitado); o que nao existir aparece como ausente. Molde do formato: v411\\PRONTO_PARA_CANDIDATO_v411.json. (O gerar_pronto_para_candidato_v412.py que o bump trouxe e' a copia mecanica do
da v411, A ADAPTAR; este script e' o da Etapa 1 e tem outro nome para nao confundir.) Grava tambem TAMANHOS_CRIADOS_v412.json (o que a etapa criou e quanto ocupa).
uso: C:\\Python314\\python.exe -B -X utf8 gerar_pronto_etapa1_v412.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel")
T12 = os.path.join("C:" + os.sep, "t", "k412c")
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


pos = lj(os.path.join(KD, "POS_BUILD_v412.json")) or {}
rec = lj(os.path.join(KD, "KERNEL_RECIBO_v412.json")) or {}
flg = lj(os.path.join(KD, "FLAGS_v412.json")) or {}
kh = lj(os.path.join(KD, "KH_N1_v412.json")) or {}
bd = lj(os.path.join(HERE, "BUNDLE_v412.json")) or {}
conf = lj(os.path.join(HERE, "CONFERENCIA_FONTES_K411C_v412.json")) or {}
prec = lj(os.path.join(KD, "PRE_COLISAO_v412.json")) or {}
pil = lj(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")) or {}
bump = lj(os.path.join(HERE, "BUMP_v412_RESULTADO.json")) or {}
base = lj(os.path.join(HERE, "BASE_V411_COPIA.json")) or {}
man_p = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412.json"); man = lj(man_p) or {}
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(KD, "construir_marcas.txt")) else ""
kernel_ok = bool(pos.get("ok"))
SCRIPTS = ["acom_init_construtor_v412.py", "acom_construtor_v412/fazer_excerto_da_ordem_v412.py", "conferir_fontes_k411c_vs_nos_v412.py", "copiar_k412c.sh", "_mk_runners_k412c.py", "copiar_base_v412.py",
           "pre_colisao_declaracoes_v412.py", "lean_texto_v412.py", "preparar_bundle_v412.py", "construir_kernel_v412.sh", "varrer_tokens_pedras_v412.py", "pos_build_kernel_v412.py",
           "copiar_logs_do_kernel_v412.py", "reconstruir_kernel_v412.py", "portao_do_pilar_v412.py", "_mk_motor_v412.py", "derivar_v412_motor.py", "_bump_copia_v412.py", "gerar_pronto_etapa1_v412.py",
           "depositar_construtor_etapa1_v412.py"]
scripts = {s: sh16(os.path.join(HERE, *s.split("/"))) for s in SCRIPTS}
runners = {n: sh16(os.path.join(T12, n)) for n in ("run_build.py", "run_pos_treino.py")}
sem_pedra = {v["destino"]: v["linhas_do_molde_sobre_o_caso_sem_modulo_novo"]["n"] for v in (bump.get("arquivos") or {}).values()
             if v.get("linhas_do_molde_sobre_o_caso_sem_modulo_novo", {}).get("n")}
avisos = pos.get("avisos_por_modulo") or {}
n_mod = int(bd.get("n") or 0)
compilaram = sum(1 for v in (pos.get("por_modulo_marcas") or {}).values() if v.get("rc") == 0)
# o que a etapa criou e quanto ocupa (fora de work: C:\t\k412c; em work: a pasta da v412, so' o que e' desta etapa)
criados = {}
for p_ in (os.path.join(T12, "final"), os.path.join(T12, "arvore")):
    b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_, "nota": "sem seguir a juncao .lake\\packages" if p_.endswith("final") else "arvore so-fontes do recibo"}
for e in (os.scandir(T12) if os.path.isdir(T12) else []):
    if e.is_dir() and e.name.startswith("quarentena_"):
        b_, n_ = tamanho(e.path); criados[e.path] = {"bytes": b_, "arquivos": n_, "nota": "backups de bytes do que o preparo trocou no sandbox"}
for rel in ("base_v411", "kernel", "pedra", "bump", "vinculo", "acom_construtor_v412"):
    p_ = os.path.join(HERE, rel)
    if os.path.exists(p_):
        b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_}
soltos = SCRIPTS + ["BUNDLE_v412.json", "kernel_modulos_novos_v412.json", "CONFERENCIA_FONTES_K411C_v412.json", "BASE_V411_COPIA.json", "PORTAO_DO_PILAR_v412.json", "BUMP_v412_RESULTADO.json",
                    "SESSION_REFERENCE_construtor_v412.json", "PRONTO_PARA_CANDIDATO_v412.json"]
b_soltos = sum(os.path.getsize(os.path.join(HERE, *s.split("/"))) for s in soltos if os.path.exists(os.path.join(HERE, *s.split("/"))))
bumpados = [v["destino"] for v in (bump.get("arquivos") or {}).values()]
b_bump = sum(os.path.getsize(os.path.join(HERE, *d.split("/"))) for d in bumpados if os.path.exists(os.path.join(HERE, *d.split("/"))))
criados["(arquivos soltos desta etapa na pasta da v412)"] = {"bytes": b_soltos, "arquivos": len(soltos)}
criados["(scripts bumpados na pasta da v412)"] = {"bytes": b_bump, "arquivos": len(bumpados)}
tot_fora = sum(v["bytes"] for k, v in criados.items() if k.startswith(T12))
tot_work = sum(v["bytes"] for k, v in criados.items() if not k.startswith(T12))
tam = {"criados": criados, "total_fora_de_work_bytes": tot_fora, "total_fora_de_work_gb": round(tot_fora / 1e9, 3), "total_em_work_bytes": tot_work, "total_em_work_mb": round(tot_work / 1e6, 1)}
out = {
    "contrato": "PRONTO_PARA_CANDIDATO_v412",
    "quando": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "agente": "claude-construtor-v412, a servico da gerencia c1",
    "estado": ("ETAPA 1 CONCLUIDA: sandbox k412c, os %d modulos instalados e compilados no sandbox, Audit medido, bump mecanico feito, portao do pilar respondido por leitura de codigo; PAROU aqui: "
               "nada de registros, artigo, guarda de frases nem candidato (ordem da Etapa 1, item 6)" % n_mod) if kernel_ok else
              ("ETAPA 1 NAO FECHOU: o kernel do sandbox nao passou (ver kernel\\POS_BUILD_v412.json: parou_em=%s); nada foi consertado em prova nem em nome" % pos.get("parou_em")),
    "etapa_1_fechou": kernel_ok,
    "ordem": {"arquivo": "ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md", "sha16": sh16(os.path.join(HERE, "ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md"))},
    "desenho": {"arquivo": "DESENHO_v412.md", "sha16": sh16(os.path.join(HERE, "DESENHO_v412.md")), "estado": "RASCUNHO (o texto pode mudar; o kernel desta etapa nao depende dele)"},
    "manifesto": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412.json", "sha16": sh16(man_p), "gerado_em": man.get("gerado_em"), "n_modulos": man.get("n_modulos"), "ficam_fora": man.get("ficam_fora")},
    "base_v411": {"um_py_sha16": base.get("base_sha16"), "selo": base.get("selo_um_version"), "copia": "base_v411\\ (BASE_V411_COPIA.json, sha16 %s)" % sh16(os.path.join(HERE, "BASE_V411_COPIA.json"))},
    "kernel_k412c": {
        "sandbox": os.path.join(T12, "final"), "origem": conf.get("sandbox_origem"),
        "origem_medida_antes_da_copia": {"bytes_sem_juncoes": conf.get("origem_bytes_sem_juncoes"), "gb": conf.get("origem_gb_sem_juncoes"), "arquivos": conf.get("origem_arquivos")},
        "disco_C_livre_antes_da_copia_gb": conf.get("disco_C_livre_gb"),
        "copia": "robocopy SEM /PURGE (copiar_k412c.sh), juncao .lake\\packages -> C:\\t\\k404c\\final\\.lake\\packages; fontes da origem conferidas contra o Nos v411 (CONFERENCIA_FONTES_K411C_v412.json: %s de %s iguais)" % (conf.get("n_comuns"), conf.get("n_nos")),
        "marcas": dict(l.split("=", 1) for l in marcas.splitlines() if "=" in l and not l.startswith("modulo=")),
        "por_modulo": pos.get("por_modulo_marcas"), "modulos_compilados_rc0": compilaram, "n_modulos": n_mod, "parou_em": pos.get("parou_em"),
        "duracao_build_s": pos.get("duracao_build_s"), "duracao_audit_s": pos.get("duracao_audit_s"),
        "linha_TOTAL": pos.get("linha_TOTAL"), "linha_TOTAL_v411": pos.get("linha_TOTAL_v411"), "delta_vs_v411": pos.get("delta_vs_v411"),
        "declaracoes_no_relatorio_de_axiomas": pos.get("n_decl_audit"), "todas_no_trio": (pos.get("criterios") or {}).get("declaracoes_novas_no_trio"),
        "escada_de_teoremas_e_bandeiras": pos.get("escada"), "n_bandeiras_novas": pos.get("n_flags"), "n_ancoras": pos.get("n_ancoras"),
        "chaves_antigas": pos.get("chaves_antigas"), "todos_os_modulos_a_frio": pos.get("todos_os_modulos_a_frio"),
        "avisos_por_modulo": {k: v.get("n") for k, v in avisos.items()}, "aviso_conhecido_TowerWedgeIndex": pos.get("aviso_conhecido_TowerWedgeIndex"),
        "falhas": pos.get("falhas"), "falhas_informativas": pos.get("falhas_informativas"),
        "colisoes": {"nome_de_modulo_sem_caixa": conf.get("colisoes_de_nome_de_modulo_sem_caixa"), "pre_conferencia_de_declaracoes": {k: prec.get(k) for k in ("colisao_com_o_kernel_nome_exato", "colisao_com_o_kernel_prefixo_de_estrutura", "colisao_entre_os_34")},
                     "juiz_definitivo": "o build da raiz no sandbox (o Lean recusa ambiente com nome repetido): %s" % ("passou" if kernel_ok else "ver POS_BUILD")},
        "recibo": {"arquivo": "kernel/KERNEL_RECIBO_v412.json", "sha16": sh16(os.path.join(KD, "KERNEL_RECIBO_v412.json")), "rc": rec.get("rc"), "sorry": rec.get("sorry"), "erros": rec.get("erros"), "contrato": rec.get("contrato")},
        "POS_BUILD_sha16": sh16(os.path.join(KD, "POS_BUILD_v412.json")), "FLAGS_sha16": sh16(os.path.join(KD, "FLAGS_v412.json")), "KH_N1_sha16": sh16(os.path.join(KD, "KH_N1_v412.json")),
        "LOGS_COPIADOS_sha16": sh16(os.path.join(KD, "LOGS_COPIADOS_v412.json")), "lake_build_log": {"bytes": os.path.getsize(os.path.join(KD, "lake_build.log")) if os.path.exists(os.path.join(KD, "lake_build.log")) else None, "sha16": sh16(os.path.join(KD, "lake_build.log"))},
        "audit_log": {"bytes": kh.get("audit_log_bytes"), "sha16": (kh.get("audit_log_sha256") or "")[:16]},
        "criterios": pos.get("criterios"), "copias_do_kernel_fora_de_work": [os.path.join(T12, "final") + " (o sandbox)", os.path.join(T12, "arvore") + " (a arvore so-fontes do recibo)"] + [k for k in criados if "quarentena_" in k]},
    "bundle": {"arquivo": "BUNDLE_v412.json", "sha16": sh16(os.path.join(HERE, "BUNDLE_v412.json")), "ordem_topologica": bd.get("ordem_topologica"), "root_suffix_linhas": len((bd.get("root_suffix") or "").splitlines()),
               "mudancas_no_texto": bd.get("normalizacao"), "por_modulo": {m["modulo"]: {"sha256_insumo": m["sha256_insumo"], "sha256_instalado": m["sha256"], "print_axioms_removidos": m["n_print_axioms_removidos"],
                                                                                         "imports_trocados": len(m["imports_trocados"]), "diff": m["diff"]} for m in (bd.get("modulos") or [])},
               "sha256_por_modulo": "kernel/bundle/SHA256_POR_MODULO_v412.json (sha16 %s)" % sh16(os.path.join(KD, "bundle", "SHA256_POR_MODULO_v412.json")),
               "trocar_uma_fonte": "um comando: C:\\Python314\\python.exe -B -X utf8 reconstruir_kernel_v412.py [--manifesto <json>] [--pedras <pasta>] (preparo idempotente; o lake recompila so' o modulo trocado e os dependentes, mais a raiz e o Audit; kernel\\ULTIMA_INSTALACAO_v412.json diz quais)"},
    "scripts_da_etapa_sha16": scripts, "lancadores_em_C_t_k412c_sha16": runners,
    "bump": {"arquivo": "BUMP_v412_RESULTADO.json", "sha16": sh16(os.path.join(HERE, "BUMP_v412_RESULTADO.json")), "n_arquivos": bump.get("n_arquivos"), "molde": bump.get("molde"),
             "deployment_da_producao_lido": bump.get("deployment_da_producao_lido"), "rotulo_do_B_n_da_v412": bump.get("rotulo_do_B_n_da_v412"), "motor": bump.get("motor"),
             "diffs": "bump\\ (um .diff por arquivo)", "marca": "cada arquivo bumpado traz `# [A ADAPTAR v412]` (o p00 recusa ate' a adaptacao)",
             "arquivos_com_linhas_do_caso_sem_modulo_novo": sem_pedra,
             "adaptados_a_mao_do_molde_v410": ["preparar_bundle_v412.py (do preparar_bundle_v410_*)", "construir_kernel_v412.sh (gerado pelo preparo; do construir_kernel_v410.sh)", "pos_build_kernel_v412.py (do pos_build_kernel_v410.py)",
                                               "copiar_logs_do_kernel_v412.py (do copiar_logs_do_kernel_v410.py)", "copiar_k412c.sh e conferir_fontes_k411c_vs_nos_v412.py (dos da v411)", "copiar_base_v412.py (do copiar_base_v411.py, sem delta)"]},
    "portao_do_pilar": {"arquivo": "PORTAO_DO_PILAR_v412.json", "sha16": sh16(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")), "resposta": pil.get("resposta"),
                        "entradas_da_chave": pil.get("entradas_da_chave"), "fecho": pil.get("fecho_dos_nomes_de_topo_da_chave"), "o_que_a_v412_muda": pil.get("o_que_a_v412_muda"),
                        "chave_do_ultimo_rito_v411": (pil.get("estado_lido") or {}).get("chaves_no_stdout_v411"), "o_reuso_usa_a_placa": pil.get("o_reuso_toca_a_placa_de_leve")},
    "falta_para_a_etapa_2": [
        "a gerencia: receber a revisao do Codex (ordem 022/023) e, se ela mudar texto de fonte, regerar o manifesto e rodar reconstruir_kernel_v412.py (um comando; so' o que depende da fonte recompila)",
        "a gerencia: congelar o contrato (DESENHO_v412.md ainda e' RASCUNHO) e decidir os prefixos das bandeiras (proposta em kernel\\FLAGS_v412.json: ext_<modulo>_412_NNNN; nenhuma chave antiga muda)",
        "Etapa 2 (construtor): delta_v412, registros por especificacao (iald_camada_cientifica_v412, matematica_que_restava_v412, parede_do_teste_cego_v412, cunhagens_v412), VERBATIM_CONGELADO_v412, guarda de frases, artigo, gerador e candidato",
        "Etapa 2: adaptar os %d scripts bumpados (marca A ADAPTAR; mais 2 copias literais do quadro da v397) do caso SEM modulo novo da v411 para o bundle de %d modulos pelo molde v410/v409 (lista das linhas em BUMP_v412_RESULTADO.json); rodar o B(n) pre-selo com o recibo do kernel desta etapa (B21; a producao pina %s)" % (
            sum(1 for k_, v_ in (bump.get("arquivos") or {}).items() if v_.get("destino") != k_), n_mod, bump.get("deployment_da_producao_lido")),
        "Etapa 2: o portao do pilar NO CANDIDATO (conferir que o gerador nao tocou os textos do fecho da chave: sha256 de cada um em PORTAO_DO_PILAR_v412.json) e, antes do rito, o ambiente da placa (torch, cuda, numpy, scipy, python, gpu) igual ao do cache, senao parar e avisar o operador (D207)",
        "a gerencia: a revisao de terceiro, a tarefa agendada (C:\\t\\k412c\\run_pos_treino.py ja existe, aponta para orquestrador\\pos_treino_v412.py), o rito, a custodia"],
    "desvios_desta_ordem": [
        "ACOM: o init da ordem original foi RECUSADO com erro visivel (ConfidentialContent: dotenv_name e escritorio_path, na linha 33, a da regra dos confidenciais); inscrevi um EXCERTO DECLARADO (acom_construtor_v412\\ORDEM_v412_ETAPA_1_EXCERTO_PARA_ACOM.md: a ordem menos a linha 33, com o sha256 da ordem e o da linha no cabecalho); a regra continua valendo",
        "o build foi POR MODULO (lake build +<modulo>, na ordem topologica) e depois inteiro, nao um `lake build` unico como na v410: para parar no primeiro modulo que nao compilasse e contar avisos por modulo; o efeito e' um lake_build.log maior (cada invocacao repete as mensagens das dependencias)",
        "as linhas #print axioms de TODA a fonte sairam (na ErgodicidadeDeMautner ha #print axioms no meio do arquivo, antes da secao 8): e' o que o molde da IALD2 (v410) fez -- o RX do molde remove em qualquer lugar; nenhuma estava em comentario",
        "o teste de fumaca do comando unico (reconstruir_kernel_v412.py --so-preparar, sem mudanca) regravou os registros da instalacao com carimbo novo e sem o historico da quarentena; corrigi a CAUSA no preparo (sem mudanca nada e' regravado; com mudanca o historico acumula) e devolvi os tres arquivos ao estado da instalacao que o build usou (_restaurar_apos_fumaca_v412.py; os estados intermediarios ficam em .bak); o kernel e os recibos nao foram tocados",
        "o bump trouxe tambem sete scripts nascidos na v411 (a cadeia unica, as guardas da conversa e do material privado, o modulo do conferidor, o pronto do pos-rito, e os dois do topo com o resultado) e cinco do pos-rito da v411, para que os imports dos outros nao fiquem orfaos"],
    "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
p = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412.json")
for nome, obj in ((p, out), (os.path.join(HERE, "TAMANHOS_CRIADOS_v412.json"), tam)):
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(nome):
        bk = nome + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(nome, "rb").read())
    open(nome + ".tmp", "wb").write(b); assert os.path.getsize(nome + ".tmp") == len(b); os.replace(nome + ".tmp", nome)
print(json.dumps({"etapa_1_fechou": kernel_ok, "escada": pos.get("escada"), "decl": pos.get("n_decl_audit"), "compilaram": compilaram, "n": n_mod, "tamanhos": {"fora_gb": tam["total_fora_de_work_gb"], "work_mb": tam["total_em_work_mb"]},
                  "pronto_sha16": sh16(p)}, ensure_ascii=False))
