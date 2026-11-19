# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de gerar_preparacao_pronta_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_07_derivar_fecho_v412.py). O original fica intacto.
"""gerar_preparacao_pronta_v412_r7.py -- (claude-construtor-v412, Etapa 2 pelo contrato R11) o FECHO do candidato regerado: PREPARACAO_v412_PRONTA_R7.json (o do R4, PREPARACAO_v412_PRONTA.json, fica como esta').
Tudo LIDO dos artefatos por script (sha16, numeros, resultados); a prosa so' no que e' dito como pendencia, divergencia ou ponto para a gerencia. Nao instala, nao roda o rito. Grava tambem TAMANHOS_CRIADOS_v412_R7.json.
uso: C:\\Python314\\python.exe -B -X utf8 gerar_preparacao_pronta_v412_r7.py"""
import datetime, hashlib, json, os, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e7_lib_v412 import D, ler_json, salvar_json, sha16_arq, MANIFESTO, PAGINA, ANCORAS, CONTRATO, Exame

K = D / "kernel"
j = lambda p: ler_json(p) if Path(p).exists() else None
s16 = lambda p: sha16_arq(p) if Path(p).exists() else None
cand = j(D / "CANDIDATO_v412.json") or {}
pos = j(K / "POS_BUILD_v412.json") or {}
fl = j(K / "FLAGS_v412.json") or {}
kfecho = j(D / "PRONTO_PARA_CANDIDATO_v412_R7.json") or {}
ens = j(D / "ENSAIO_RESULTADO_v412.json")
gf = j(D / "GUARDA_FRASES_v412.json") or {}
gu = j(D / "GUARDA_v412_UNIDADES.json") or {}
pil = j(D / "PORTAO_DO_PILAR_CANDIDATO_v412.json") or {}
priv = j(D / "GUARDA_MATERIAL_PRIVADO_v412.json") or {}
reg = j(D / "REGISTROS_v412_RECIBO.json") or {}
anc = j(D / "ANCORAS_ESCOLHIDAS_v412.json") or {}
ancc = j(K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R7.json") or {}
ini = j(D / "INICIO_R11_v412.json") or {}
g4 = j(D / "GUARDA_R4_ETAPA2_v412.json") or {}
verb = j(D / "VERBATIM_CONGELADO_v412.json") or {}
man = ler_json(MANIFESTO)
ens_est = j(D / "DERIVACAO_R7_PIPELINE_v412.json") or {}
mapa = j(D / "registro_mapa_construtor_etapa2_r7_v412.recibo.json") or {}
cand_p = D / "um_v412_candidato.py"
cand_b = cand_p.read_bytes() if cand_p.exists() else b""
cand_sha16 = hashlib.sha256(cand_b).hexdigest()[:16] if cand_b else None
real = (ens or {}).get("real") or {}
ex = Exame("fecho_R11")
ex.chk("os quatro sha16 do inicio conferem (contrato R11, manifesto R12, ancoras R12, pagina R25)", (ini.get("exame") or {}).get("ok") is True, (ini.get("exame") or {}).get("n_checagens", 0))
ex.chk("o kernel da decima segunda lista (156 modulos) fechou (PRONTO_PARA_CANDIDATO_v412_R7.json)", kfecho.get("kernel_fechou") is True, (kfecho.get("resumo") or {}).get("n_checagens", 0), (kfecho.get("resumo") or {}))
ex.chk("o candidato em disco e' o do manifesto CANDIDATO_v412.json (sha16 e bytes lidos do arquivo)", bool(cand_b) and cand.get("sha16") == cand_sha16 and cand.get("bytes") == len(cand_b), 1, [cand.get("sha16"), cand_sha16])
ex.chk("a escada do candidato e' a medida no kernel", cand.get("escada") == pos.get("escada") == fl.get("escada") and bool(cand.get("escada")), 1, [cand.get("escada"), pos.get("escada")])
ex.chk("os cinco registros: recibo verde", reg.get("ok") is True and len(reg.get("registros") or {}) == 5, len(reg.get("registros") or {}), (reg.get("resumo") or {}))
ex.chk("as ancoras escolhidas: nenhum problema; nenhuma sem nome no relatorio de axiomas", anc.get("problemas") == [] and anc.get("ancoras_sem_nome_no_relatorio_de_axiomas") == 0, anc.get("n_ancoras_total", 0))
ex.chk("a guarda de frases: os controles todos como devem", gf.get("ok") is True and gf.get("n_controles") == gf.get("n_ok") and (gf.get("n_controles") or 0) > 0, gf.get("n_controles", 0))
ex.chk("a travessia sobre todo o texto novo: recibo verde", gu.get("ok") is True and (gu.get("n_unidades_total") or 0) > 0, gu.get("n_unidades_total", 0), (gu.get("resumo") or {}))
ex.chk("o verificador de historia sobre todo o texto novo: zero achado", ((gu.get("historia") or {}).get("achados") == []) and ((gu.get("historia") or {}).get("n_unidades") or 0) > 0, (gu.get("historia") or {}).get("n_unidades", 0))
ex.chk("o portao do pilar no candidato", pil.get("ok") is True and pil.get("candidato_sha16", cand_sha16) == cand_sha16, (pil.get("resumo") or {}).get("n_checagens", 0), pil.get("resumo"))
ex.chk("a guarda de material privado sobre os insumos pinados: limpo", priv.get("limpo") is True and (priv.get("n_arquivos") or 0) > 0, priv.get("n_arquivos", 0), priv.get("com_material_privado"))
ex.chk("o ensaio a seco sobre ESTE candidato: tudo passou", bool(real) and real.get("sha16_do_candidato") == cand_sha16 and real.get("n_falhas") == 0 and (real.get("n_checagens_unidade") or 0) > 0 and str(real.get("veredito", "")).startswith("TUDO PASSOU") and (real.get("saida") or {}).get("rc") == "rc=0",
       real.get("n_checagens_unidade", 0), {"veredito": real.get("veredito"), "falhas": (real.get("falhas_da_unidade") or [])[:8], "componentes_nao_verdes": {a: b for a, b in (real.get("componentes") or {}).items() if b is not True and a != "variantes"}, "candidato_do_ensaio": real.get("sha16_do_candidato")})
# o que foi criado em disco nesta ordem (arquivos com data de modificacao a partir do inicio desta etapa)
t0 = (D / "e7_lib_v412.py").stat().st_mtime - 600
criados = []; tot = 0
for raiz, ds, fs in os.walk(D):
    for f in fs:
        p = os.path.join(raiz, f)
        try:
            st = os.stat(p)
        except OSError:
            continue
        if st.st_mtime >= t0:
            criados.append((os.path.relpath(p, D), st.st_size)); tot += st.st_size
fora = {}
for d in sorted(Path(r"C:\t\k412c").iterdir()):
    try:
        if d.stat().st_mtime >= t0 and d.name not in ("final",):
            n = 0; b = 0
            if d.is_dir():
                for raiz, ds, fs in os.walk(d):
                    for f in fs:
                        try:
                            b += os.path.getsize(os.path.join(raiz, f)); n += 1
                        except OSError:
                            pass
            else:
                n, b = 1, d.stat().st_size
            fora[str(d)] = {"arquivos": n, "bytes": b}
    except OSError:
        pass
tam = {"desde": datetime.datetime.fromtimestamp(t0).isoformat(timespec="seconds"), "na_pasta_da_cadeia": {"n_arquivos": len(criados), "bytes": tot, "maiores": sorted(criados, key=lambda x: -x[1])[:25], "n_backups_bak": sum(1 for a, _ in criados if ".bak" in a)},
       "fora_de_work_em_C_t_k412c": fora, "bytes_fora": sum(v["bytes"] for v in fora.values()),
       "nota": "inclui o que os subprocessos desta etapa regravaram (recibos, logs, backups de bytes); o sandbox C:\\t\\k412c\\final cresceu com os 156 modulos compilados e nao esta' somado aqui; nada foi apagado"}
salvar_json(D / "TAMANHOS_CRIADOS_v412_R7.json", tam)
regs = reg.get("registros") or {}
fecho = {
    "contrato": "PREPARACAO_v412_PRONTA_R7", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v412 (Etapa 2 pelo contrato R11), a servico da gerencia c1",
    "fechou": ex.ok, "checagens_do_fecho": ex.linhas, "resumo_do_fecho": ex.resumo(),
    "estado": ("CANDIDATO REGERADO PELO CONTRATO R11 E ENSAIADO A SECO, NAO INSTALADO, RITO NAO RODADO; para aqui, para a revisao de terceiro; a Etapa 3 NAO foi comecada" if ex.ok else
               "ETAPA 2 PELO R11 NAO FECHOU: ver checagens_do_fecho (as que estao com ok falso) e ETAPA_2_R7_ESTADO_v412.json; nada instalado; rito nao rodado"),
    "contrato_seguido": {"arquivo": "CONTRATO_v412_R11.md", "sha16": s16(CONTRATO), "copia_congelada_igual": hashlib.sha256(CONTRATO.read_bytes()).hexdigest() == hashlib.sha256((D / "contrato_REV11" / "CONTRATO_v412_R11.md").read_bytes()).hexdigest(),
                         "os_quatro_sha16_do_inicio": {k: v.get("sha16_lido") for k, v in (ini.get("lidos") or {}).items()}},
    "candidato": {"arquivo": "um_v412_candidato.py", "caminho": str(cand_p), "sha16": cand_sha16, "bytes": len(cand_b), "base_v411_sha16": cand.get("base_v411_sha16"), "manifesto": "CANDIDATO_v412.json", "manifesto_sha16": s16(D / "CANDIDATO_v412.json"),
                  "gerador": cand.get("gerador"), "n_patches": cand.get("n_patches"), "patches": [p["id"] for p in cand.get("patches", []) if not p["id"].startswith("C12_expected")], "n_literais_expected_ladder": cand.get("expected_ladder_literais"),
                  "candidato_do_R4_guardado_fora_de_work": g4.get("candidato_R4"), "guarda_do_R4": g4.get("guarda")},
    "escada": {"bandeiras": {"antes_v411": (cand.get("escada") or [None, None])[0], "depois_candidato": (cand.get("escada") or [None, None])[1], "novas": cand.get("n_bandeiras"), "kernel_medido": pos.get("escada"), "igual_a_do_kernel": cand.get("escada") == pos.get("escada")},
               "teoremas_no_relatorio_de_axiomas": {"antes_v411": (pos.get("linha_TOTAL_v411") or {}).get("thm"), "depois": (pos.get("linha_TOTAL") or {}).get("thm")},
               "declaracoes_no_relatorio_de_axiomas": {"antes_v411": (pos.get("linha_TOTAL_v411") or {}).get("decl"), "depois": (pos.get("linha_TOTAL") or {}).get("decl"), "fora_do_trio": (pos.get("linha_TOTAL") or {}).get("fora_do_trio")},
               "do_candidato_do_R4": (kfecho.get("escada") or {}).get("escada_do_R4"), "ensaio": real.get("escada")},
    "kernel": {"fecho": "PRONTO_PARA_CANDIDATO_v412_R7.json", "fecho_sha16": s16(D / "PRONTO_PARA_CANDIDATO_v412_R7.json"), "sandbox": "C:\\t\\k412c\\final", "n_modulos": man.get("n_modulos"), "por_frente": (kfecho.get("manifesto") or {}).get("por_frente"), "por_autor": (kfecho.get("manifesto") or {}).get("por_autor"),
               "lista": "duodecima (insumos\\MANIFESTO_PEDRAS_v412_R12.json)", "manifesto_sha16": s16(MANIFESTO), "resumo_das_checagens": kfecho.get("resumo"), "a_frio": pos.get("todos_os_modulos_a_frio"), "linha_TOTAL": pos.get("linha_TOTAL"), "delta_vs_v411": pos.get("delta_vs_v411"),
               "delta_vs_setima_lista": kfecho.get("delta_vs_setima_lista"), "decima_lista_build_anterior": kfecho.get("decima_lista_build_anterior"), "avisos_fora_o_conhecido": {m: v.get("n") for m, v in (pos.get("avisos_por_modulo") or {}).items() if v.get("n") and m != "TGLExt.TowerWedgeIndex"},
               "chaves_antigas_mudam": (pos.get("chaves_antigas") or {}).get("mudam"), "instalacao": kfecho.get("instalacao"), "duracao_build_s": kfecho.get("duracao_build_s"), "duracao_audit_s": kfecho.get("duracao_audit_s")},
    "registros": {"nomes": cand.get("registros"), "recibo": "REGISTROS_v412_RECIBO.json", "recibo_sha16": s16(D / "REGISTROS_v412_RECIBO.json"), "recibo_ok": reg.get("ok"), "por_registro": regs,
                  "n_ancoras_por_registro": {k: v.get("n_ancoras") for k, v in regs.items()}, "n_checagens_por_registro": {k: v.get("n_checagens") for k, v in regs.items()}, "n_checagens_total": sum((v.get("n_checagens") or 0) for v in regs.values()),
                  "ancoras_escolhidas": {"recibo": "ANCORAS_ESCOLHIDAS_v412.json", "sha16": s16(D / "ANCORAS_ESCOLHIDAS_v412.json"), "n_total": anc.get("n_ancoras_total"), "n_por_registro": {r: v["n_ancoras"] for r, v in (anc.get("registros") or {}).items()},
                                         "modulos_em_recuo_pelos_print_axioms": anc.get("n_modulos_em_recuo_print_axioms"), "comparacao_com_o_R4_nos_42_modulos": {k: v for k, v in (anc.get("comparacao_com_o_recibo_do_R4_nos_42_modulos") or {}).items() if k != "recibo_R4"},
                                         "tabela_do_leitor": anc.get("tabela_do_leitor")}},
    "nomes_completos_das_ancoras": {"como": "o nome completo de cada declaracao foi LIDO do relatorio de axiomas do sandbox (kernel/FLAGS_v412.json: a proveniencia das publicas por modulo e as linhas #print axioms de cada fonte, que o pos_build resolveu no relatorio); nenhum nome foi montado pelo prefixo do modulo; "
                                            "o namespace do insumo so' serve de desempate entre nomes que ja' sao do relatorio",
                                    "conferencia": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R7.json", "n_nomes_propostos_conferidos": ancc.get("n_nomes_conferidos"), "por_classe": ancc.get("por_classe"), "por_via": ancc.get("por_via"),
                                    "vias_das_ancoras_escolhidas": anc.get("vias_dos_nomes_completos_das_ancoras"), "ancoras_sem_nome_no_relatorio_de_axiomas": anc.get("ancoras_sem_nome_no_relatorio_de_axiomas"), "identificador_renomeado": "nenhum"},
    "guarda_de_frases": {"controles": {"n": gf.get("n_controles"), "n_ok": gf.get("n_ok"), "numerados": gf.get("controles_numerados")}, "recibo_controles": "GUARDA_FRASES_v412.json", "fonte": "runtime_v412_guarda.py (a do R4, sem mudanca: a secao 5 do contrato nao mudou)", "fonte_sha16": s16(D / "runtime_v412_guarda.py"),
                         "travessia": {"recibo": "GUARDA_v412_UNIDADES.json", "ok": gu.get("ok"), "n_superficies": gu.get("n_superficies"), "n_unidades_total": gu.get("n_unidades_total"), "n_unidades_com_p_igual_np_ou_fluidos": len(gu.get("unidades_com_p_igual_np_ou_fluidos") or []),
                                       "unidades_por_superficie": {k: v.get("n_unidades") for k, v in (gu.get("superficies") or {}).items()}},
                         "verificador_de_historia": gu.get("historia"), "formas_da_F43_nos_textos_emitidos": (gu.get("f43") or {}).get("achados"), "marcadores_herdados": {k: v for k, v in (gu.get("marcadores_herdados") or {}).items() if k in ("n", "diferem")}},
    "portao_do_pilar_no_candidato": {"ok": pil.get("ok"), "resumo": pil.get("resumo"), "recibo": "PORTAO_DO_PILAR_CANDIDATO_v412.json", "n_nomes_do_fecho": pil.get("n_nomes_do_fecho"), "falta_antes_do_rito": pil.get("falta_antes_do_rito")},
    "guarda_de_material_privado": {"limpo": priv.get("limpo"), "n_arquivos": priv.get("n_arquivos"), "com_material_privado": priv.get("com_material_privado"), "recibo": "GUARDA_MATERIAL_PRIVADO_v412.json"},
    "ensaio_a_seco": (real and {"veredito": real.get("veredito"), "rc": (real.get("saida") or {}).get("rc"), "saida": (real.get("saida") or {}).get("arquivo"), "n_checagens_unidade": real.get("n_checagens_unidade"), "n_ok": real.get("n_ok"), "n_falhas": real.get("n_falhas"), "falhas_da_unidade": real.get("falhas_da_unidade"),
                               "candidato_sha16": real.get("sha16_do_candidato"), "escada": real.get("escada"), "chaves_novas_no_core": real.get("chaves_novas_no_core"), "componentes": real.get("componentes"),
                               "examinou": {k: v for k, v in (real.get("v412_examinou") or {}).items() if k != "guarda_de_frases"}}) or None,
    "ensaio_a_seco_arquivo": "ENSAIO_RESULTADO_v412.json", "ensaio_sha16": s16(D / "ENSAIO_RESULTADO_v412.json"), "ensaio_script": {"arquivo": "ensaio_a_seco_v412_r7.py", "sha16": s16(D / "ensaio_a_seco_v412_r7.py"), "estado_da_adaptacao": "DERIVACAO_R7_PIPELINE_v412.json", "estado_sha16": s16(D / "DERIVACAO_R7_PIPELINE_v412.json")},
    "verbatim_congelado": {"arquivo": "VERBATIM_CONGELADO_v412.json", "sha16": s16(D / "VERBATIM_CONGELADO_v412.json"), "n": verb.get("n"), "padrao": verb.get("padrao"), "por_dia": verb.get("por_dia")},
    "resumo_troca_de_pnp": cand.get("resumo_troca_de_pnp"),
    "respostas_da_D224_aplicadas": [
        "(1) o patch de DADO no literal 'escada' do contrato do teste H0DN fica (patch C12b_h0dn_baseline_escada), junto dos literais 'expected_ladder' (C12): valor antigo %s, valor novo %s" % tuple(cand.get("escada") or [None, None]),
        "(2) sem pino exato de cobertura do kernel para a arvore nova: o da v411 fica como piso (C13_specs_v411_pisos); o ensaio segue cobrando as entradas do hash formal",
        "(3) os ids r1, r2, r3 das checagens de cunhagens_v412 passaram a selo_camada, selo_leitor, selo_matematica, selo_parede (um por registro cujo selo ele cobra)",
        "(4) o topo versionado fica (_V412_TOPO e _v412_topo_texto); (5) a regra das ancoras com o recuo pelos #print axioms, agora da secao 1; (6) a pagina e' a R25 (sha16 lido do arquivo, pinado pelo contrato R11)",
        "(7) VERBATIM_CONGELADO_v412.json vai ate' os arquivos de 18/11, fora do programa e fora da varredura dos insumos pinados",
    ],
    "divergencias_do_molde_ou_da_ordem": [
        "o verificador de historia ganhou copia _r5 com duas mudancas, cada uma com controle no autoteste: (a) a palavra comum “ordem” deixa de ser recusada (a pagina R25 traz “cadeia binaria na ordem prometida”); ORDEM em maiusculas, “ordem <numero>” e “ordem do autor/operador” seguem recusadas; "
        "(b) um identificador do kernel com ponto (nome completo de declaracao do relatorio de axiomas ou espaco de nome do manifesto) sai da prosa antes do exame, e o recibo diz quantos sairam: a frente C conserva os espacos de nome dos autores (contrato R11, secao 1), e um deles coincide com nome de modelo; a palavra solta segue recusada",
        "o padrao das chaves de bandeira no gerador passou a aceitar sublinhado no nome do modulo (dois modulos tem nome de arquivo em minusculas com sublinhado); a checagem nova cobra o prefixo exato ext_<modulo em minusculas>_412_ e que nenhuma chave traga data, nome de pessoa ou de modelo, ou palavra de processo",
        "regra (b) das ancoras: o termo citado numa linha da tabela do bloco “O leitor da formula” so' ancora declaracao de modulo da PROPRIA linha (a frente C repete nomes curtos entre modulos); fora dessa tabela vale a regra do R4",
        "registro leitor_da_formula_v412: as linhas do que o artefato mostra saem da tabela da pagina por script, uma a uma, e a montagem PARA se um termo citado nao for ancora de modulo da linha; a linha “nao esta demonstrado” vira limite [OPEN]",
        "cunhagens_v412: as entradas passaram de 10 para 21 (os modulos cujo cabecalho tem a secao do que o arquivo tipa, medido por script); “a recusa e' um nome com conteudo” nao tem secao propria em cabecalho e entra so' na lista das definicoes da pagina",
        "compilacao a frio dos 156: os artefatos de build dos 153 modulos da decima lista foram movidos (nao apagados) para C:\\t\\k412c\\quarentena_build_153_<data>, fora de work\\, antes do build; o kernel antigo da v411 foi reaproveitado; o build a frio da decima lista (153 modulos, saida zero, so' os tres axiomas) tinha terminado antes e fica so' como informacao (campo decima_lista_build_anterior)",
        "os recibos regravados conservam o nome (os consumidores os leem pelo nome); os do R4 estao em copia de bytes fora de work\\ (GUARDA_R4_ETAPA2_v412.json), os do kernel da decima lista tambem (kernel/GUARDA_R5_KERNEL_v412.json) e o fecho do R4 fica como esta'; os scripts anteriores ficam intactos e os novos sao copias _r7 ou e7_* (DERIVACAO_R7_PIPELINE_v412.json); nao ha' fecho R5: a etapa pelo R5 foi interrompida antes de fechar",
        "o ensaio a seco e os auxiliares _r7 foram derivados das copias _r5 (adaptadas por subagente na etapa anterior) por troca de nome de arquivo e de rotulo; o conteudo do ensaio le contagens do contrato, do manifesto e do kernel",
    ],
    "pontos_para_a_gerencia": [
        "conferir o recibo ANCORAS_ESCOLHIDAS_v412.json (a operacionalizacao da regra das ancoras; quantos modulos cairam no recuo pelos #print axioms)",
        "a traducao para o ingles do bloco “O leitor da formula” (O_QUE_FICA_CLARO_v412_R25_EN.md) e' do construtor: mesma estrutura, mesmos termos entre crases na mesma ordem e mesmos numeros, conferidos por script; a redacao vai com o candidato a revisao de terceiro",
        "os nomes curtos das onze entradas novas de cunhagens_v412 (as oito do R5 e as tres do R7: OPolinomioFixoEBeta, ORazaoDoColapsoEBeta, OCustoEAIsometria) sao escolha do construtor (textos_registros_v412_r7.py, NOMES_CURTOS), tirados do titulo e da secao de cada cabecalho",
        "a pagina R25 cita `a_trava_no_nome` (em TraducaoTuring), `the_angle_is_prior` e `the_name_is_the_born_reading_of_the_post` (declaracoes do kernel selado da v411, nao de modulo da lista de 156): por isso nao sao ancora de nenhum registro desta versao; o recibo ANCORAS_ESCOLHIDAS_v412.json lista os nomes da pagina que nao sao declaracao de modulo da lista",
        "os scripts da Etapa 3 (rito, instalacao, custodia, pos-rito) seguem marcados [A ADAPTAR v412] e importam delta_v412 (o do R4): na Etapa 3 passam a importar delta_v412_r7",
    ],
    "nao_feito_ou_pendente": [
        "a Etapa 3 nao foi comecada: os scripts de rito, instalacao, custodia e pos-rito marcados [A ADAPTAR v412] e a bateria pre-selo ficam para a outra ordem, depois da revisao de terceiro do candidato",
        "portao do pilar antes do rito: conferir que o ambiente da placa e' o do cache (ato da gerencia; ha' treino em curso, que nao foi tocado nem medido)",
        "a revisao de terceiro, a leitura do texto publico ao autor, a tarefa agendada, o rito e a custodia sao da gerencia",
    ],
    "texto_publico": {"pagina_pt": "o_que_fica_claro_REV25/O_QUE_FICA_CLARO_v412_R25.md", "pagina_pt_sha16": s16(PAGINA), "traducao_en": "O_QUE_FICA_CLARO_v412_R25_EN.md", "traducao_en_sha16": s16(D / "O_QUE_FICA_CLARO_v412_R25_EN.md"),
                      "secao_do_artigo": "TEXTO_PUBLICO_v412.json", "secao_sha16": s16(D / "TEXTO_PUBLICO_v412.json"), "pdflatex_isolado": (j(D / "TEXTO_PUBLICO_PDFLATEX_v412.json") or {}).get("ok"), "blocos": "BLOCOS_TEXTO_PUBLICO_v412.json", "blocos_sha16": s16(D / "BLOCOS_TEXTO_PUBLICO_v412.json")},
    "criado_em_disco": {"recibo": "TAMANHOS_CRIADOS_v412_R7.json", "na_pasta_da_cadeia": {k: v for k, v in tam["na_pasta_da_cadeia"].items() if k != "maiores"}, "fora_de_work": tam["fora_de_work_em_C_t_k412c"], "bytes_fora": tam["bytes_fora"]},
    "estado_em_disco": {"arquivo": "ETAPA_2_R7_ESTADO_v412.json", "sha16": s16(D / "ETAPA_2_R7_ESTADO_v412.json")},
    "mapa_de_rotas": mapa or "registrado depois deste fecho: ver registro_mapa_construtor_etapa2_r7_v412.json e o recibo ao lado",
    "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final e nos recibos desta pasta; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
salvar_json(D / "PREPARACAO_v412_PRONTA_R7.json", fecho)
print("gravado PREPARACAO_v412_PRONTA_R7.json", s16(D / "PREPARACAO_v412_PRONTA_R7.json"), "| fechou:", ex.ok, ex.resumo())
for l in ex.linhas:
    if not l["ok"]:
        print("  NAO:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:400])
sys.exit(0 if ex.ok else 1)
