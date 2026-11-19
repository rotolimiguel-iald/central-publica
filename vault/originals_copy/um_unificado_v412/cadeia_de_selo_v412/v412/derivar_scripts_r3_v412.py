# -*- coding: utf-8 -*-
"""derivar_scripts_r3_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) gera, em COPIAS novas com sufixo `_r3` (os `_r2` e os originais da Etapa 1 ficam intactos), os scripts que
pressupunham a QUARTA lista de pedras (insumos\\MANIFESTO_PEDRAS_v412_R4.json, insumos\\pedras_r4, insumos\\ANCORAS_PROPOSTAS_v412_R4.json) para a QUINTA lista (..._R5.json, pedras_r5).
Cada troca e' de TEXTO EXATO com o numero de ocorrencias conferido (falha visivel se o original nao tem o trecho esperado o numero esperado de vezes); os pontos em que o gerador do fecho precisa
de conteudo novo (a comparacao com o fecho R2, a lista de scripts, os desvios) sao BLOCOS entre dois marcadores unicos, tambem conferidos (cada marcador aparece uma so' vez), com o sha16 do trecho
substituido registrado. Gera: guardar_r2_antes_do_r3_v412.py, pre_colisao_declaracoes_v412_r3.py, reconstruir_kernel_v412_r3.py, pos_build_kernel_v412_r3.py, conferir_ancoras_propostas_v412_r3.py,
gerar_pronto_etapa1_v412_r3.py. Grava DERIVACAO_R3_v412.json (origem, destino, sha16, cada troca e cada bloco). So' escreve esses arquivos novos.
uso: C:\\Python314\\python.exe -B -X utf8 derivar_scripts_r3_v412.py [--regerar]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sha = lambda b: hashlib.sha256(b).hexdigest()
LOG = []


def derivar(origem, destino, trocas, blocos, cabecalho):
    po = os.path.join(HERE, origem); pd_ = os.path.join(HERE, destino)
    b = open(po, "rb").read()
    assert b"\r" not in b, ("CR no original", origem)
    t = b.decode("utf-8")
    reg = {"origem": origem, "origem_sha16": sha(b)[:16], "destino": destino, "trocas": [], "blocos": []}
    for velho, novo, n in trocas:
        c = t.count(velho)
        assert c == n, ("o original nao tem o trecho esperado o numero esperado de vezes", origem, velho[:90], c, n)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:90], "ocorrencias": c})
    for ini, fim, novo in blocos:
        assert t.count(ini) == 1, ("marcador de inicio nao e' unico", origem, ini[:90], t.count(ini))
        assert t.count(fim) == 1, ("marcador de fim nao e' unico", origem, fim[:90], t.count(fim))
        i = t.index(ini); j = t.index(fim)
        assert i < j, ("marcadores fora de ordem", origem, ini[:60], fim[:60])
        velho_span = t[i:j]
        t = t[:i] + novo + t[j:]
        reg["blocos"].append({"inicio": ini[:90], "fim": fim[:90], "trecho_substituido_sha16": sha(velho_span.encode("utf-8"))[:16], "trecho_substituido_bytes": len(velho_span.encode("utf-8"))})
    linhas = t.split("\n")
    assert linhas[0].startswith("# -*- coding")
    t = "\n".join([linhas[0], cabecalho] + linhas[1:])
    out = t.encode("utf-8")
    compile(t, destino, "exec")   # o derivado tem de ser Python valido
    reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    LOG.append(reg)
    if os.path.exists(pd_):
        if open(pd_, "rb").read() == out:
            print("ja existe, igual:", destino); return
        assert "--regerar" in sys.argv, ("a copia _r3 ja existe e difere: nao sobrescrevo sem --regerar", destino)
        bk = pd_ + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        open(bk, "wb").write(open(pd_, "rb").read()); assert open(bk, "rb").read() == open(pd_, "rb").read()
        print("backup de bytes:", bk)
    with open(pd_ + ".tmp", "wb") as f:
        f.write(out)
    assert os.path.getsize(pd_ + ".tmp") == len(out)
    os.replace(pd_ + ".tmp", pd_)
    print("gerado:", destino, len(out), "bytes | sha16", sha(out)[:16], "| original", sha(b)[:16], "|", len(trocas), "trocas,", len(blocos), "blocos")


CAB = "# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de %s para a QUINTA lista de pedras (insumos\\MANIFESTO_PEDRAS_v412_R5.json, insumos\\pedras_r5); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida)."

# ---------------------------------------------------------------- 1. a copia de bytes do estado do R2 (.bak_r2)
derivar("guardar_etapa1_antes_do_r2_v412.py", "guardar_r2_antes_do_r3_v412.py", [
    (".bak_etapa1", ".bak_r2", 3),
    ("GUARDA_ETAPA1_v412.json", "GUARDA_R2_v412.json", 2),
    ('"PRONTO_PARA_CANDIDATO_v412.json", "TAMANHOS_CRIADOS_v412.json"):', '"PRONTO_PARA_CANDIDATO_v412_R2.json", "TAMANHOS_CRIADOS_v412_R2.json"):', 1),
    ('if ".bak" in n or n.endswith(".tmp"):', 'if ".bak" in n or n.endswith(".tmp") or n == "CODIGO_R4_R5_v412.json":', 1),
], [
    ('"""guardar_etapa1_antes_do_r2_v412.py', "import hashlib, json, os, sys", '''"""guardar_r2_antes_do_r3_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) copia de BYTES, com o sufixo `.bak_r2`, do estado do fecho R2 (quarta lista, 40 modulos) antes que a continuacao 2
(quinta lista, 40 modulos com seis emendados) regrave os recibos e os logs de kernel/. Nada e' apagado nem movido; se o `.bak_r2` ja existe, nao e' sobrescrito (confere-se so' que e' igual).
Cobre: kernel/* (inclusive kernel/bundle/*, menos o que ja' e' copia .bak e o CODIGO_R4_R5_v412.json, que nasceu depois), BUNDLE_v412.json, kernel_modulos_novos_v412.json, construir_kernel_v412.sh,
vinculo/CRITERIOS_v412.json, PRONTO_PARA_CANDIDATO_v412_R2.json, TAMANHOS_CRIADOS_v412_R2.json. NAO toca em nenhum original (so' cria os `.bak_r2`). Grava kernel/GUARDA_R2_v412.json (caminho, bytes, sha16 de cada copia).
uso: C:/Python314/python.exe -B -X utf8 guardar_r2_antes_do_r3_v412.py"""
'''),
], CAB % "guardar_etapa1_antes_do_r2_v412.py (que guardava o estado da Etapa 1 com .bak_etapa1; este guarda o do R2 com .bak_r2)")

# ---------------------------------------------------------------- 2. a pre-colisao
derivar("pre_colisao_declaracoes_v412_r2.py", "pre_colisao_declaracoes_v412_r3.py", [
    ("MANIFESTO_PEDRAS_v412_R4.json", "MANIFESTO_PEDRAS_v412_R5.json", 1),
    ("pedras_r4", "pedras_r5", 1),
    ("_R2.json", "_R3.json", 2),
    ("QUARTA lista", "QUINTA lista", 1),
], [], CAB % "pre_colisao_declaracoes_v412_r2.py")

# ---------------------------------------------------------------- 3. o pos_build
derivar("pos_build_kernel_v412_r2.py", "pos_build_kernel_v412_r3.py", [
    ("MANIFESTO_PEDRAS_v412_R4.json", "MANIFESTO_PEDRAS_v412_R5.json", 3),
    ("pos_build_kernel_v412_r2", "pos_build_kernel_v412_r3", 2),
    ("complemento da Etapa 1, quarta lista de pedras, 17/11/2026", "continuacao 2 do complemento da Etapa 1, quinta lista de pedras, 17/11/2026", 1),
    ("QUARTA lista", "QUINTA lista", 1),
], [], CAB % "pos_build_kernel_v412_r2.py")

# ---------------------------------------------------------------- 4. o comando unico
derivar("reconstruir_kernel_v412_r2.py", "reconstruir_kernel_v412_r3.py", [
    ("(r2, quarta lista)", "(r3, quinta lista)", 1),
    ("(r2: a quarta lista e' o padrao)", "(r3: a quinta lista e' o padrao)", 1),
    ("MANIFESTO_PEDRAS_v412_R4.json", "MANIFESTO_PEDRAS_v412_R5.json", 2),
    ("pedras_r4", "pedras_r5", 2),
    ("pos_build_kernel_v412_r2", "pos_build_kernel_v412_r3", 3),
    ("QUARTA lista", "QUINTA lista", 1),
], [], CAB % "reconstruir_kernel_v412_r2.py")

# ---------------------------------------------------------------- 5. a conferencia das ancoras propostas
derivar("conferir_ancoras_propostas_v412_r2.py", "conferir_ancoras_propostas_v412_r3.py", [
    ("ANCORAS_PROPOSTAS_v412_R4.json", "ANCORAS_PROPOSTAS_v412_R5.json", 2),
    ("MANIFESTO_PEDRAS_v412_R4.json", "MANIFESTO_PEDRAS_v412_R5.json", 1),
    ("pedras_r4", "pedras_r5", 1),
    ("_R2.json", "_R3.json", 2),
    ("conferir_ancoras_propostas_v412_r2", "conferir_ancoras_propostas_v412_r3", 2),
    ("pos_build_kernel_v412_r2", "pos_build_kernel_v412_r3", 1),
    ("QUARTA lista", "QUINTA lista", 1),
], [], CAB % "conferir_ancoras_propostas_v412_r2.py")

# ---------------------------------------------------------------- 6. o gerador do fecho (trocas mecanicas + blocos de conteudo novo)
NOVO_DOC = '''"""gerar_pronto_etapa1_v412_r3.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) FECHA a continuacao 2 do complemento da Etapa 1 da v412: o kernel do sandbox k412c passou da QUARTA para a QUINTA lista de
pedras (40 modulos; 6 deles com comentarios e docstrings emendados, o codigo igual) em PRONTO_PARA_CANDIDATO_v412_R3.json e TAMANHOS_CRIADOS_v412_R3.json (arquivos NOVOS; o R2 e o da Etapa 1 ficam como estao).
Tudo LIDO dos artefatos (nada digitado); o que nao existir aparece como ausente. Compara o que foi medido agora com o fecho R2 (PRONTO_PARA_CANDIDATO_v412_R2.json e as copias .bak_r2 de kernel/).
Derivado de gerar_pronto_etapa1_v412_r2.py por derivar_scripts_r3_v412.py. Se existir DESVIOS_EXTRA_v412_R3.json (lista de textos), entra nos desvios.
uso: C:/Python314/python.exe -B -X utf8 gerar_pronto_etapa1_v412_r3.py"""
'''

NOVO_ESTADO = '''    "estado": ("CONTINUACAO 2 DO COMPLEMENTO DA ETAPA 1 CONCLUIDA: o kernel do sandbox k412c passou da quarta para a quinta lista de pedras (%d modulos; %d com comentarios e docstrings emendados, codigo igual); %d de %d compilaram; "
               "Audit medido; PAROU aqui: nada de registros, artigo, guarda de frases nem candidato (Etapa 2 e' da gerencia/construtor em ordem propria)" % (n_mod, len(trocados), compilaram, n_mod)) if kernel_ok else
              ("CONTINUACAO 2 NAO FECHOU: o kernel do sandbox nao passou (ver kernel/POS_BUILD_v412.json: parou_em=%s); nada foi consertado em prova nem em nome" % pos.get("parou_em")),
'''

NOVO_MUDOU = '''    "o_que_mudou_da_quarta_lista_para_a_quinta": {"quarta_lista": {"arquivo": "insumos/MANIFESTO_PEDRAS_v412_R4.json", "sha16": sh16(man1_p), "n_modulos": man1.get("n_modulos")},
                                                  "novos": novos, "n_novos": len(novos), "trocados_so_em_comentarios_e_docstrings": trocados, "n_trocados": len(trocados), "iguais_byte_a_byte": iguais, "n_iguais": len(iguais),
                                                  "mudados_no_sandbox_pelo_preparo": ult.get("mudados_no_sandbox"), "o_lake_recompila": ult.get("o_lake_recompila"),
                                                  "raiz_mudou": ult.get("raiz_mudou"), "quarentena_dos_arquivos_trocados": (bd.get("quarentenas") or [None])[-1],
                                                  "conferencia_independente_do_codigo": {"arquivo": "kernel/CODIGO_R4_R5_v412.json", "sha16": sh16(os.path.join(KD, "CODIGO_R4_R5_v412.json")),
                                                                                         "contagem": (lj(os.path.join(KD, "CODIGO_R4_R5_v412.json")) or {}).get("contagem"), "script": "conferir_quinta_lista_v412.py",
                                                                                         "metodo": "dois metodos independentes (texto sem comentarios com cadeias mantidas; mascara_comentarios), espaco normalizado; os dois tem de concordar"}},
'''

NOVO_SCRIPTS = '''SCRIPTS = ["guardar_r2_antes_do_r3_v412.py", "derivar_scripts_r3_v412.py", "conferir_quinta_lista_v412.py", "conferir_nos_intacto_r3_v412.py", "conferir_built_esperado_r3_v412.py", "depositar_construtor_r3_v412.py", "pre_colisao_declaracoes_v412_r3.py", "reconstruir_kernel_v412_r3.py", "pos_build_kernel_v412_r3.py",
           "conferir_ancoras_propostas_v412_r3.py", "gerar_pronto_etapa1_v412_r3.py", "preparar_bundle_v412.py", "lean_texto_v412.py", "copiar_logs_do_kernel_v412.py", "construir_kernel_v412.sh",
           "reconstruir_kernel_v412_r2.py", "pos_build_kernel_v412_r2.py", "pre_colisao_declaracoes_v412_r2.py", "conferir_ancoras_propostas_v412_r2.py", "gerar_pronto_etapa1_v412_r2.py",
           "guardar_etapa1_antes_do_r2_v412.py", "derivar_scripts_etapa1_r2_v412.py", "conferir_so_comentarios_r1_r4_v412.py", "reconstruir_kernel_v412.py", "pos_build_kernel_v412.py"]
'''

NOVO_CMP = '''def _flags(p):
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
'''

NOVO_DESVIOS = '''    "desvios_desta_ordem": [
        "a ordem desta rodada (mensagem da gerencia) diz que seis modulos mudaram so' em comentarios e docstrings: conferido por dois metodos independentes (kernel/CODIGO_R4_R5_v412.json): %d identicos byte a byte, %d so' comentarios e docstrings, 0 com codigo diferente" % (len(iguais), len(trocados)),
        "o build foi INCREMENTAL: %d modulos com linha Built (os %d trocados no sandbox pelo preparo e os dependentes que o lake recompilou), %d com linha Replayed e %d sem linha (em dia para o lake); cada `lake build +<modulo>` voltou rc 0; nao houve compilacao a frio dos modulos que o lake deu como em dia; o rito do Nos compila tudo a frio" % (
            sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v == "Built"), len(ult.get("mudados_no_sandbox") or []),
            sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v == "Replayed"), sum(1 for v in (pos.get("modo_dos_modulos_no_build") or {}).values() if v is None)),
        "scripts _r3 derivados dos _r2 por troca de texto exato com contagem conferida (derivar_scripts_r3_v412.py; DERIVACAO_R3_v412.json guarda cada troca e cada bloco); os _r2 e os da Etapa 1 ficam intactos; conferir_quinta_lista_v412.py e o derivador sao novos; o preparar_bundle, o lean_texto e o copiar_logs nao precisaram de copia",
        "o gerador do fecho (este) nao e' so' troca de nome: alem das trocas mecanicas tem blocos novos (a comparacao com o R2, a lista de scripts, estes desvios), todos conferidos no derivador por marcadores unicos",
        "os recibos e os logs de kernel/ do fecho R2 tem copia .bak_r2 (kernel/GUARDA_R2_v412.json); o PRONTO_PARA_CANDIDATO_v412.json e o _R2 nao foram tocados; os registros vigentes em kernel/ sao agora os da quinta lista",
        "o pos_build_r3 move a arvore so-fontes da rodada anterior para arvore_anterior_<data> em vez de apagar (cerca de 131 MB cada; nada foi apagado)",
        "o ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md da pasta tem hoje outro sha16 que o pinado pela Etapa 1 (a linha dos confidenciais foi reescrita ao lado pela gerencia); a ordem desta continuacao chegou como mensagem, nao como arquivo"] + (lj(os.path.join(HERE, "DESVIOS_EXTRA_v412_R3.json")) or []),
'''

derivar("gerar_pronto_etapa1_v412_r2.py", "gerar_pronto_etapa1_v412_r3.py", [
    # mecanicas
    ("MANIFESTO_PEDRAS_v412_R4.json", "MANIFESTO_PEDRAS_v412_R5.json", 2),
    ("ANCORAS_PROPOSTAS_v412_R4.json", "ANCORAS_PROPOSTAS_v412_R5.json", 2),
    ("pedras_r4", "pedras_r5", 1),
    ("_R2.json", "_R3.json", 9),
    ('"contrato": "PRONTO_PARA_CANDIDATO_v412_R2",', '"contrato": "PRONTO_PARA_CANDIDATO_v412_R3",', 1),
    ('"pronto_r2_sha16"', '"pronto_r3_sha16"', 1),
    # o conteudo da comparacao: a quarta lista e' a anterior, o fecho R2 e' a base
    ('"MANIFESTO_PEDRAS_v412.json"); man1 = lj(man1_p) or {}', '"MANIFESTO_PEDRAS_v412_R4.json"); man1 = lj(man1_p) or {}', 1),
    ("# o que mudou entre a primeira lista e a quarta (lido dos dois manifestos)", "# o que mudou entre a quarta lista e a quinta (lido dos dois manifestos)", 1),
    ('k1 = p1.get("kernel_k412c") or {}', 'k1 = (lj(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R2.json")) or {}).get("kernel_k412c") or {}', 1),
    ("\nout = {\n", "\n" + NOVO_CMP + "out = {\n", 1),
    ('"agente": "claude-construtor-v412 (continuacao), a servico da gerencia c1"', '"agente": "claude-construtor-v412 (continuacao 2), a servico da gerencia c1"', 1),
    ('    "ordem_da_etapa_1": {"arquivo"', '    "fecho_r2": {"arquivo": "PRONTO_PARA_CANDIDATO_v412_R2.json", "sha16": sh16(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R2.json")), "nota": "o fecho da quarta lista (continuacao 1); fica como estava; os recibos de kernel/ dele tem copia .bak_r2 (kernel/GUARDA_R2_v412.json)"},\n    "ordem_da_etapa_1": {"arquivo"', 1),
    ("(continuacao): quarta lista, 40 modulos; as regras da Etapa 1 continuam valendo", "(continuacao 2): quinta lista, 40 modulos (ordem 027 da gerencia: emendas so' de texto em seis modulos); as regras da Etapa 1 continuam valendo", 1),
    ('"mudaram_campo_do_manifesto": man.get("mudaram"),', '"mudaram_campo_do_manifesto": man.get("mudaram"), "mudaram_da_quarta_lista": man.get("mudaram_da_quarta_lista"),', 1),
    ('"etapa_1_para_comparar": {"n_modulos": k1.get("n_modulos")', '"r2_para_comparar": {"n_modulos": k1.get("n_modulos")', 1),
    ('"n_ancoras": k1.get("n_ancoras"),', '"n_ancoras_print_axioms_retirados": k1.get("n_ancoras_print_axioms_retirados"),', 1),
    ("reconstruir_kernel_v412_r2.py [--manifesto <json>] [--pedras <pasta>] (o padrao e' a quarta lista;", "reconstruir_kernel_v412_r3.py [--manifesto <json>] [--pedras <pasta>] (o padrao e' a quinta lista;", 1),
    ('    "bump": {"arquivo": "BUMP_v412_RESULTADO.json"', '    "comparacao_com_o_r2": CMP,\n    "nos_intacto": {"arquivo": "kernel/NOS_INTACTO_R3_v412.json", "sha16": sh16(os.path.join(KD, "NOS_INTACTO_R3_v412.json")), "conteudo": lj(os.path.join(KD, "NOS_INTACTO_R3_v412.json"))},\n    "bump": {"arquivo": "BUMP_v412_RESULTADO.json"', 1),
    ('"arvore so-fontes da primeira rodada do pos_build r2 (identica a vigente)"', '"arvore so-fontes anterior (movida pelo pos_build, nao apagada)"', 1),
    ("inclui os .bak_etapa1 e os .bak_<data> dos logs da Etapa 1", "inclui os .bak_etapa1, os .bak_r2 e os .bak_<data> dos logs das rodadas anteriores", 1),
], [
    ('"""gerar_pronto_etapa1_v412_r2.py', "import datetime, hashlib, json, os, sys", NOVO_DOC),
    ("SCRIPTS = [", "scripts = {s: sh16(", NOVO_SCRIPTS),
    ('    "estado": (', '    "kernel_fechou": kernel_ok,', NOVO_ESTADO),
    ('    "o_que_mudou_da_primeira_lista_para_a_quarta": {', '    "ancoras_propostas": {', NOVO_MUDOU),
    ('    "desvios_desta_ordem": [', '    "estatuto": "[REAL]', NOVO_DESVIOS),
], CAB % "gerar_pronto_etapa1_v412_r2.py")

# ---------------------------------------------------------------- o registro da derivacao
out = os.path.join(HERE, "DERIVACAO_R3_v412.json")
dados = json.dumps({"quando": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "derivados": LOG}, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(out):
    bk = out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(out, "rb").read())
with open(out + ".tmp", "wb") as f:
    f.write(dados)
os.replace(out + ".tmp", out)
print("registro:", out, "sha16", sha(dados)[:16])
