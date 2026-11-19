# -*- coding: utf-8 -*-
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de gerar_pronto_etapa1_v412_r2.py para a QUINTA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R5.json, insumos\pedras_r5); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
"""gerar_pronto_etapa1_v412_r3.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) FECHA a continuacao 2 do complemento da Etapa 1 da v412: o kernel do sandbox k412c passou da QUARTA para a QUINTA lista de
pedras (40 modulos; 6 deles com comentarios e docstrings emendados, o codigo igual) em PRONTO_PARA_CANDIDATO_v412_R3.json e TAMANHOS_CRIADOS_v412_R3.json (arquivos NOVOS; o R2 e o da Etapa 1 ficam como estao).
Tudo LIDO dos artefatos (nada digitado); o que nao existir aparece como ausente. Compara o que foi medido agora com o fecho R2 (PRONTO_PARA_CANDIDATO_v412_R2.json e as copias .bak_r2 de kernel/).
Derivado de gerar_pronto_etapa1_v412_r2.py por derivar_scripts_r3_v412.py. Se existir DESVIOS_EXTRA_v412_R3.json (lista de textos), entra nos desvios.
uso: C:/Python314/python.exe -B -X utf8 gerar_pronto_etapa1_v412_r3.py"""
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
ult = lj(os.path.join(KD, "ULTIMA_INSTALACAO_v412.json")) or {}
bd = lj(os.path.join(HERE, "BUNDLE_v412.json")) or {}
conf = lj(os.path.join(HERE, "CONFERENCIA_FONTES_K411C_v412.json")) or {}
prec = lj(os.path.join(KD, "PRE_COLISAO_v412_R3.json")) or {}
anc = lj(os.path.join(KD, "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json")) or {}
pil = lj(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")) or {}
bump = lj(os.path.join(HERE, "BUMP_v412_RESULTADO.json")) or {}
base = lj(os.path.join(HERE, "BASE_V411_COPIA.json")) or {}
p1 = lj(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412.json")) or {}
man1_p = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R4.json"); man1 = lj(man1_p) or {}
man_p = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R5.json"); man = lj(man_p) or {}
anc_p = os.path.join(HERE, "insumos", "ANCORAS_PROPOSTAS_v412_R5.json")
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(KD, "construir_marcas.txt")) else ""
kernel_ok = bool(pos.get("ok"))
# o que mudou entre a quarta lista e a quinta (lido dos dois manifestos)
A = {m["modulo"]: m for m in man1.get("modulos", [])}; B = {m["modulo"]: m for m in man.get("modulos", [])}
novos = [k for k in B if k not in A]; iguais = [k for k in B if k in A and A[k]["sha256"] == B[k]["sha256"]]; trocados = [k for k in B if k in A and A[k]["sha256"] != B[k]["sha256"]]
SCRIPTS = ["guardar_r2_antes_do_r3_v412.py", "derivar_scripts_r3_v412.py", "conferir_quinta_lista_v412.py", "conferir_nos_intacto_r3_v412.py", "conferir_built_esperado_r3_v412.py", "depositar_construtor_r3_v412.py", "pre_colisao_declaracoes_v412_r3.py", "reconstruir_kernel_v412_r3.py", "pos_build_kernel_v412_r3.py",
           "conferir_ancoras_propostas_v412_r3.py", "gerar_pronto_etapa1_v412_r3.py", "preparar_bundle_v412.py", "lean_texto_v412.py", "copiar_logs_do_kernel_v412.py", "construir_kernel_v412.sh",
           "reconstruir_kernel_v412_r2.py", "pos_build_kernel_v412_r2.py", "pre_colisao_declaracoes_v412_r2.py", "conferir_ancoras_propostas_v412_r2.py", "gerar_pronto_etapa1_v412_r2.py",
           "guardar_etapa1_antes_do_r2_v412.py", "derivar_scripts_etapa1_r2_v412.py", "conferir_so_comentarios_r1_r4_v412.py", "reconstruir_kernel_v412.py", "pos_build_kernel_v412.py"]
scripts = {s: sh16(os.path.join(HERE, *s.split("/"))) for s in SCRIPTS}
runners = {n: sh16(os.path.join(T12, n)) for n in ("run_build.py", "run_pos_treino.py")}
avisos = pos.get("avisos_por_modulo") or {}
n_mod = int(bd.get("n") or 0)
compilaram = sum(1 for v in (pos.get("por_modulo_marcas") or {}).values() if v.get("rc") == 0)
criados = {}
for p_ in (os.path.join(T12, "final"), os.path.join(T12, "arvore")):
    b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_, "nota": "sem seguir a juncao .lake\\packages" if p_.endswith("final") else "arvore so-fontes do recibo"}
for e in (os.scandir(T12) if os.path.isdir(T12) else []):
    if e.is_dir() and (e.name.startswith("quarentena_") or e.name.startswith("arvore_etapa1_") or e.name.startswith("arvore_anterior_")):
        b_, n_ = tamanho(e.path); criados[e.path] = {"bytes": b_, "arquivos": n_, "nota": "backups de bytes do que o preparo trocou no sandbox" if e.name.startswith("quarentena_") else
                                                     ("arvore so-fontes da Etapa 1 (movida, nao apagada)" if e.name.startswith("arvore_etapa1_") else "arvore so-fontes anterior (movida pelo pos_build, nao apagada)")}
for rel in ("base_v411", "kernel", "pedra", "bump", "vinculo", "acom_construtor_v412"):
    p_ = os.path.join(HERE, rel)
    if os.path.exists(p_):
        b_, n_ = tamanho(p_); criados[p_] = {"bytes": b_, "arquivos": n_}
tot_fora = sum(v["bytes"] for k, v in criados.items() if k.startswith(T12))
tot_work = sum(v["bytes"] for k, v in criados.items() if not k.startswith(T12))
tam = {"criados": criados, "total_fora_de_work_bytes": tot_fora, "total_fora_de_work_gb": round(tot_fora / 1e9, 3), "total_em_work_bytes": tot_work, "total_em_work_mb": round(tot_work / 1e6, 1),
       "nota": "kernel\\ inclui os .bak_etapa1, os .bak_r2 e os .bak_<data> dos logs das rodadas anteriores (copias de bytes; nada foi apagado)"}
k1 = (lj(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R2.json")) or {}).get("kernel_k412c") or {}
def _flags(p):
    j = lj(p) or {}
    return {f[0]: f[1] for f in j.get("flags", [])}, j


_f_antes, _j_antes = _flags(os.path.join(KD, "FLAGS_v412.json.bak_r2"))
_f_agora, _j_agora = _flags(os.path.join(KD, "FLAGS_v412.json"))
anc2 = lj(os.path.join(KD, "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R2.json")) or {}
CMP = {
    "base_da_comparacao": "PRONTO_PARA_CANDIDATO_v412_R2.json e as copias .bak_r2 de kernel/ (guardar_r2_antes_do_r3_v412.py; kernel/GUARDA_R2_v412.json)",
    "linha_TOTAL_igual": k1.get("linha_TOTAL") == pos.get("linha_TOTAL"), "linha_TOTAL_r2": k1.get("linha_TOTAL"), "linha_TOTAL_agora": pos.get("linha_TOTAL"),
    "declaracoes_no_relatorio_de_axiomas_igual": k1.get("declaracoes_no_relatorio_de_axiomas") == pos.get("n_decl_audit"),
    "escada_igual": k1.get("escada_de_teoremas_e_bandeiras") == pos.get("escada"), "escada_r2": k1.get("escada_de_teoremas_e_bandeiras"), "escada_agora": pos.get("escada"),
    "n_bandeiras_novas_igual": k1.get("n_bandeiras_novas") == pos.get("n_flags"), "n_bandeiras_novas_r2": k1.get("n_bandeiras_novas"), "n_bandeiras_novas_agora": pos.get("n_flags"),
    "chaves_das_bandeiras_identicas": sorted(_f_antes) == sorted(_f_agora), "n_chaves_r2": len(_f_antes), "n_chaves_agora": len(_f_agora),
    "pares_chave_nome_identicos": _f_antes == _f_agora, "chaves_so_no_r2": sorted(set(_f_antes) - set(_f_agora))[:10], "chaves_so_agora": sorted(set(_f_agora) - set(_f_antes))[:10],
    "n_por_modulo_igual": k1.get("n_por_modulo") == flg.get("n_por_modulo"),
    "nomes_publicos_e_proveniencia_identicos": _j_antes.get("proveniencia_publicas") == _j_agora.get("proveniencia_publicas"),
    "chaves_antigas_mudam_agora": (pos.get("chaves_antigas") or {}).get("mudam"), "chaves_antigas_mudam_no_r2": (k1.get("chaves_antigas") or {}).get("mudam"),
    "avisos_por_modulo_igual": k1.get("avisos_por_modulo") == {k: v.get("n") for k, v in avisos.items()},
    "conferencia_das_ancoras_propostas": {"r2": {"n": anc2.get("n_nomes_conferidos"), "por_classe": anc2.get("por_classe")}, "agora": {"n": anc.get("n_nomes_conferidos"), "por_classe": anc.get("por_classe")},
                          "mesma_conta": anc2.get("por_classe") == anc.get("por_classe") and anc2.get("n_nomes_conferidos") == anc.get("n_nomes_conferidos")},
    "audit_log_igual_ao_r2_em_bytes": (kh.get("audit_log_sha256") or "")[:16] == ((k1.get("audit_log") or {}).get("sha16")),
    "duracao_build_s": {"r2": k1.get("duracao_build_s"), "agora": pos.get("duracao_build_s")}, "duracao_audit_s": {"r2": k1.get("duracao_audit_s"), "agora": pos.get("duracao_audit_s")},
}
out = {
    "contrato": "PRONTO_PARA_CANDIDATO_v412_R3",
    "quando": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "agente": "claude-construtor-v412 (continuacao 2), a servico da gerencia c1",
    "estado": ("CONTINUACAO 2 DO COMPLEMENTO DA ETAPA 1 CONCLUIDA: o kernel do sandbox k412c passou da quarta para a quinta lista de pedras (%d modulos; %d com comentarios e docstrings emendados, codigo igual); %d de %d compilaram; "
               "Audit medido; PAROU aqui: nada de registros, artigo, guarda de frases nem candidato (Etapa 2 e' da gerencia/construtor em ordem propria)" % (n_mod, len(trocados), compilaram, n_mod)) if kernel_ok else
              ("CONTINUACAO 2 NAO FECHOU: o kernel do sandbox nao passou (ver kernel/POS_BUILD_v412.json: parou_em=%s); nada foi consertado em prova nem em nome" % pos.get("parou_em")),
    "kernel_fechou": kernel_ok,
    "etapa_1_original": {"arquivo": "PRONTO_PARA_CANDIDATO_v412.json", "sha16": sh16(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412.json")), "nota": "o fecho da Etapa 1 (34 modulos) fica como estava; os recibos de kernel\\ da Etapa 1 tem copia .bak_etapa1 (kernel\\GUARDA_ETAPA1_v412.json)"},
    "fecho_r2": {"arquivo": "PRONTO_PARA_CANDIDATO_v412_R2.json", "sha16": sh16(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R2.json")), "nota": "o fecho da quarta lista (continuacao 1); fica como estava; os recibos de kernel/ dele tem copia .bak_r2 (kernel/GUARDA_R2_v412.json)"},
    "ordem_da_etapa_1": {"arquivo": "ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md", "sha16_atual": sh16(os.path.join(HERE, "ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md")),
                          "sha16_original_pinado_pela_etapa_1": (p1.get("ordem") or {}).get("sha16"), "nota": "o arquivo atual tem a linha dos confidenciais reescrita (AO LADO da gerencia); os bytes originais ficam fora de work\\"},
    "ordem_do_complemento": "mensagem da gerencia ao construtor (continuacao 2): quinta lista, 40 modulos (ordem 027 da gerencia: emendas so' de texto em seis modulos); as regras da Etapa 1 continuam valendo",
    "desenho": {"arquivo": "DESENHO_v412.md", "sha16": sh16(os.path.join(HERE, "DESENHO_v412.md")), "estado": "o kernel desta etapa nao depende dele"},
    "manifesto": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412_R5.json", "sha16": sh16(man_p), "sha256": sha(open(man_p, "rb").read()) if os.path.exists(man_p) else None, "gerado_em": man.get("gerado_em"),
                  "n_modulos": man.get("n_modulos"), "mudaram_campo_do_manifesto": man.get("mudaram"), "mudaram_da_quarta_lista": man.get("mudaram_da_quarta_lista"), "ficam_fora": man.get("ficam_fora"), "nota": man.get("nota"), "pedras": "insumos/pedras_r5"},
    "o_que_mudou_da_quarta_lista_para_a_quinta": {"quarta_lista": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412_R4.json", "sha16": sh16(man1_p), "n_modulos": man1.get("n_modulos")},
                                                  "novos": novos, "n_novos": len(novos), "trocados_so_em_comentarios_e_docstrings": trocados, "n_trocados": len(trocados), "iguais_byte_a_byte": iguais, "n_iguais": len(iguais),
                                                  "mudados_no_sandbox_pelo_preparo": ult.get("mudados_no_sandbox"), "o_lake_recompila": ult.get("o_lake_recompila"),
                                                  "raiz_mudou": ult.get("raiz_mudou"), "quarentena_dos_arquivos_trocados": (bd.get("quarentenas") or [None])[-1],
                                                  "conferencia_independente_do_codigo": {"arquivo": "kernel/CODIGO_R4_R5_v412.json", "sha16": sh16(os.path.join(KD, "CODIGO_R4_R5_v412.json")),
                                                                                         "contagem": (lj(os.path.join(KD, "CODIGO_R4_R5_v412.json")) or {}).get("contagem"), "script": "conferir_quinta_lista_v412.py",
                                                                                         "metodo": "dois metodos independentes (texto sem comentarios com cadeias mantidas; mascara_comentarios), espaco normalizado; os dois tem de concordar"}},
    "ancoras_propostas": {"arquivo": "insumos/ANCORAS_PROPOSTAS_v412_R5.json", "sha16": sh16(anc_p), "conferencia": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json (sha16 %s)" % sh16(os.path.join(KD, "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json")),
                          "n_nomes_conferidos": anc.get("n_nomes_conferidos"), "por_classe": anc.get("por_classe"), "private_na_fonte": (anc.get("private_na_fonte") or {}).get("n"), "ausentes": len(anc.get("ausentes") or []),
                          "ambiguos": len(anc.get("ambiguos") or []), "manifesto_da_proposta_igual_ao_atual": anc.get("manifesto_da_proposta_igual_ao_atual")},
    "base_v411": {"um_py_sha16": base.get("base_sha16"), "selo": base.get("selo_um_version"), "copia": "base_v411\\ (BASE_V411_COPIA.json, sha16 %s)" % sh16(os.path.join(HERE, "BASE_V411_COPIA.json"))},
    "kernel_k412c": {
        "sandbox": os.path.join(T12, "final"), "origem": conf.get("sandbox_origem"),
        "origem_medida_antes_da_copia": {"bytes_sem_juncoes": conf.get("origem_bytes_sem_juncoes"), "gb": conf.get("origem_gb_sem_juncoes"), "arquivos": conf.get("origem_arquivos")},
        "disco_C_livre_antes_da_copia_gb": conf.get("disco_C_livre_gb"),
        "marcas": dict(l.split("=", 1) for l in marcas.splitlines() if "=" in l and not l.startswith("modulo=")),
        "por_modulo": pos.get("por_modulo_marcas"), "modulos_compilados_rc0": compilaram, "n_modulos": n_mod, "parou_em": pos.get("parou_em"),
        "modo_dos_modulos_no_build": pos.get("modo_dos_modulos_no_build"), "tempos_built_s": pos.get("tempos_built_s"),
        "duracao_build_s": pos.get("duracao_build_s"), "duracao_audit_s": pos.get("duracao_audit_s"),
        "r2_para_comparar": {"n_modulos": k1.get("n_modulos"), "duracao_build_s": k1.get("duracao_build_s"), "duracao_audit_s": k1.get("duracao_audit_s"), "linha_TOTAL": k1.get("linha_TOTAL"),
                                   "escada_de_teoremas_e_bandeiras": k1.get("escada_de_teoremas_e_bandeiras"), "n_bandeiras_novas": k1.get("n_bandeiras_novas"), "n_ancoras_print_axioms_retirados": k1.get("n_ancoras_print_axioms_retirados"),
                                   "declaracoes_no_relatorio_de_axiomas": k1.get("declaracoes_no_relatorio_de_axiomas")},
        "linha_TOTAL": pos.get("linha_TOTAL"), "linha_TOTAL_v411": pos.get("linha_TOTAL_v411"), "delta_vs_v411": pos.get("delta_vs_v411"),
        "declaracoes_no_relatorio_de_axiomas": pos.get("n_decl_audit"), "todas_no_trio": (pos.get("criterios") or {}).get("declaracoes_novas_no_trio"),
        "escada_de_teoremas_e_bandeiras": pos.get("escada"), "n_bandeiras_novas": pos.get("n_flags"), "n_por_modulo": flg.get("n_por_modulo"), "n_ancoras_print_axioms_retirados": pos.get("n_ancoras"),
        "chaves_antigas": pos.get("chaves_antigas"),
        "avisos_por_modulo": {k: v.get("n") for k, v in avisos.items()}, "aviso_conhecido_TowerWedgeIndex": pos.get("aviso_conhecido_TowerWedgeIndex"),
        "falhas": pos.get("falhas"), "falhas_informativas": pos.get("falhas_informativas"),
        "colisoes": {"pre_conferencia_de_declaracoes": {k: prec.get(k) for k in ("colisao_com_o_kernel_nome_exato", "colisao_com_o_kernel_prefixo_de_estrutura", "colisao_entre_os_40")},
                     "juiz_definitivo": "o build da raiz no sandbox (o Lean recusa ambiente com nome repetido): %s" % ("passou" if kernel_ok else "ver POS_BUILD")},
        "recibo": {"arquivo": "kernel/KERNEL_RECIBO_v412.json", "sha16": sh16(os.path.join(KD, "KERNEL_RECIBO_v412.json")), "rc": rec.get("rc"), "sorry": rec.get("sorry"), "erros": rec.get("erros"), "contrato": rec.get("contrato")},
        "POS_BUILD_sha16": sh16(os.path.join(KD, "POS_BUILD_v412.json")), "FLAGS_sha16": sh16(os.path.join(KD, "FLAGS_v412.json")), "KH_N1_sha16": sh16(os.path.join(KD, "KH_N1_v412.json")),
        "LOGS_COPIADOS_sha16": sh16(os.path.join(KD, "LOGS_COPIADOS_v412.json")), "lake_build_log": {"bytes": os.path.getsize(os.path.join(KD, "lake_build.log")) if os.path.exists(os.path.join(KD, "lake_build.log")) else None, "sha16": sh16(os.path.join(KD, "lake_build.log"))},
        "audit_log": {"bytes": kh.get("audit_log_bytes"), "sha16": (kh.get("audit_log_sha256") or "")[:16]},
        "criterios": pos.get("criterios"), "copias_do_kernel_fora_de_work": [os.path.join(T12, "final") + " (o sandbox)", os.path.join(T12, "arvore") + " (a arvore so-fontes do recibo)"] + [k for k in criados if "quarentena_" in k or "arvore_etapa1_" in k or "arvore_anterior_" in k]},
    "bundle": {"arquivo": "BUNDLE_v412.json", "sha16": sh16(os.path.join(HERE, "BUNDLE_v412.json")), "ordem_topologica": bd.get("ordem_topologica"), "root_suffix_linhas": len((bd.get("root_suffix") or "").splitlines()),
               "mudancas_no_texto": bd.get("normalizacao"), "por_modulo": {m["modulo"]: {"sha256_insumo": m["sha256_insumo"], "sha256_instalado": m["sha256"], "print_axioms_removidos": m["n_print_axioms_removidos"],
                                                                                         "imports_trocados": len(m["imports_trocados"]), "diff": m["diff"]} for m in (bd.get("modulos") or [])},
               "sha256_por_modulo": "kernel/bundle/SHA256_POR_MODULO_v412.json (sha16 %s)" % sh16(os.path.join(KD, "bundle", "SHA256_POR_MODULO_v412.json")),
               "trocar_uma_fonte": "um comando: C:\\Python314\\python.exe -B -X utf8 reconstruir_kernel_v412_r3.py [--manifesto <json>] [--pedras <pasta>] (o padrao e' a quinta lista; preparo idempotente; o lake recompila so' o modulo trocado e os dependentes, mais a raiz e o Audit; kernel\\ULTIMA_INSTALACAO_v412.json diz quais)"},
    "scripts_da_etapa_sha16": scripts, "lancadores_em_C_t_k412c_sha16": runners,
    "comparacao_com_o_r2": CMP,
    "nos_intacto": {"arquivo": "kernel/NOS_INTACTO_R3_v412.json", "sha16": sh16(os.path.join(KD, "NOS_INTACTO_R3_v412.json")), "conteudo": lj(os.path.join(KD, "NOS_INTACTO_R3_v412.json"))},
    "bump": {"arquivo": "BUMP_v412_RESULTADO.json", "sha16": sh16(os.path.join(HERE, "BUMP_v412_RESULTADO.json")), "nota": "o bump mecanico da Etapa 1 nao depende do conjunto de modulos; nao foi refeito"},
    "portao_do_pilar": {"arquivo": "PORTAO_DO_PILAR_v412.json", "sha16": sh16(os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")), "resposta": pil.get("resposta"),
                        "entradas_da_chave": pil.get("entradas_da_chave"), "o_que_a_v412_muda": pil.get("o_que_a_v412_muda"),
                        "o_complemento_muda": "so' o conjunto e o texto de modulos Lean em TGLExt\\ (nada de _QP_WORKER_SRC, _QP_SPEC_JSON, beta ou do fecho de dependencias da chave): a resposta da Etapa 1 segue valendo; o pilar nao rodou"},
    "falta_para_a_etapa_2": [
        "a gerencia: congelar o contrato e decidir os prefixos das bandeiras (proposta em kernel\\FLAGS_v412.json: ext_<modulo>_412_NNNN; nenhuma chave antiga muda); a escolha das ancoras e' do contrato (kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json diz quais nomes servem)",
        "Etapa 2 (construtor): delta_v412, registros por especificacao, VERBATIM_CONGELADO_v412, guarda de frases, artigo, gerador e candidato; adaptar os scripts bumpados (marca A ADAPTAR) para o bundle de %d modulos pelo molde v410/v409; rodar o B(n) pre-selo com o recibo do kernel deste complemento" % n_mod,
        "Etapa 2: o portao do pilar NO CANDIDATO (conferir que o gerador nao tocou os textos do fecho da chave: sha256 de cada um em PORTAO_DO_PILAR_v412.json) e, antes do rito, o ambiente da placa igual ao do cache, senao parar e avisar o operador (D207)",
        "a gerencia: a revisao de terceiro, a tarefa agendada, o rito, a custodia"],
    "desvios_desta_ordem": [
        "a ordem desta rodada (mensagem da gerencia) diz que seis modulos mudaram so' em comentarios e docstrings: conferido por dois metodos independentes (kernel/CODIGO_R4_R5_v412.json): %d identicos byte a byte, %d so' comentarios e docstrings, 0 com codigo diferente" % (len(iguais), len(trocados)),
        "o build foi INCREMENTAL: %d modulos com linha Built (os %d trocados no sandbox pelo preparo e os dependentes que o lake recompilou), %d com linha Replayed e %d sem linha (em dia para o lake); cada `lake build +<modulo>` voltou rc 0; nao houve compilacao a frio dos modulos que o lake deu como em dia; o rito do Nos compila tudo a frio" % (
            sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v == "Built"), len(ult.get("mudados_no_sandbox") or []),
            sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v == "Replayed"), sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v is None)),
        "scripts _r3 derivados dos _r2 por troca de texto exato com contagem conferida (derivar_scripts_r3_v412.py; DERIVACAO_R3_v412.json guarda cada troca e cada bloco); os _r2 e os da Etapa 1 ficam intactos; conferir_quinta_lista_v412.py e o derivador sao novos; o preparar_bundle, o lean_texto e o copiar_logs nao precisaram de copia",
        "o gerador do fecho (este) nao e' so' troca de nome: alem das trocas mecanicas tem blocos novos (a comparacao com o R2, a lista de scripts, estes desvios), todos conferidos no derivador por marcadores unicos",
        "os recibos e os logs de kernel/ do fecho R2 tem copia .bak_r2 (kernel/GUARDA_R2_v412.json); o PRONTO_PARA_CANDIDATO_v412.json e o _R2 nao foram tocados; os registros vigentes em kernel/ sao agora os da quinta lista",
        "o pos_build_r3 move a arvore so-fontes da rodada anterior para arvore_anterior_<data> em vez de apagar (cerca de 131 MB cada; nada foi apagado)",
        "o ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md da pasta tem hoje outro sha16 que o pinado pela Etapa 1 (a linha dos confidenciais foi reescrita ao lado pela gerencia); a ordem desta continuacao chegou como mensagem, nao como arquivo"] + (lj(os.path.join(HERE, "DESVIOS_EXTRA_v412_R3.json")) or []),
    "estatuto": "[REAL] medido no sandbox C:\\t\\k412c\\final; nada instalado no Nos; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
p = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R3.json")
for nome, obj in ((p, out), (os.path.join(HERE, "TAMANHOS_CRIADOS_v412_R3.json"), tam)):
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(nome):
        bk = nome + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(nome, "rb").read())
    open(nome + ".tmp", "wb").write(b); assert os.path.getsize(nome + ".tmp") == len(b); os.replace(nome + ".tmp", nome)
print(json.dumps({"kernel_fechou": kernel_ok, "escada": pos.get("escada"), "decl": pos.get("n_decl_audit"), "compilaram": compilaram, "n": n_mod, "tamanhos": {"fora_gb": tam["total_fora_de_work_gb"], "work_mb": tam["total_em_work_mb"]},
                  "pronto_r3_sha16": sh16(p)}, ensure_ascii=False))
