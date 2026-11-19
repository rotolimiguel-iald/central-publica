# -*- coding: utf-8 -*-
"""depositar_construtor_r3_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) (1) o deposito do construtor na FILA DA MEMORIA (memory/fila/depositos/claude-construtor-v412/), no formato de
memory/fila/README.md (so' acrescimo: nunca edita deposito existente; nome com data e hora); (2) o JSON do RESULTADO da rota cadeia.preparacao_v412.etapa1_k412c para o Mapa de Rotas (o registro pelo rotas.py
e' feito fora deste script). Os numeros e hashes sao LIDOS de PRONTO_PARA_CANDIDATO_v412_R3.json e dos recibos (nada digitado). Molde: depositar_construtor_etapa1_v412.py.
uso: C:/Python314/python.exe -B -X utf8 depositar_construtor_r3_v412.py [--seco]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v412")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PP = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R3.json")
P = json.load(open(PP, encoding="utf-8"))
K = P["kernel_k412c"]; C = P["comparacao_com_o_r2"]; N = (P.get("nos_intacto") or {}).get("conteudo") or {}
M = P["manifesto"]; Q = P["o_que_mudou_da_quarta_lista_para_a_quinta"]; A = P["ancoras_propostas"]
T = K.get("linha_TOTAL") or {}
fontes = [PP, os.path.join(HERE, "kernel", "KERNEL_RECIBO_v412.json"), os.path.join(HERE, "kernel", "POS_BUILD_v412.json"), os.path.join(HERE, "kernel", "FLAGS_v412.json"),
          os.path.join(HERE, "kernel", "CODIGO_R4_R5_v412.json"), os.path.join(HERE, "kernel", "NOS_INTACTO_R3_v412.json"), os.path.join(HERE, "kernel", "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R3.json"),
          os.path.join(HERE, "DERIVACAO_R3_v412.json"), os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R5.json")]
fontes = [f for f in fontes if os.path.exists(f)]
agora = datetime.datetime.now()
av = {k: v for k, v in (K.get("avisos_por_modulo") or {}).items() if v}
fechou = bool(P.get("kernel_fechou"))
corpo = (
    "v412, continuacao 2 do complemento da Etapa 1, por claude-construtor-v412 para a gerencia c1, %s: %s. Nada instalado no Nos; o rito nao rodou.\n\n"
    "[REAL, lido dos artefatos] A quinta lista de pedras (manifesto R5, sha16 %s; %s modulos; %s emendados so' em comentarios e docstrings, com o codigo igual por dois metodos independentes; %s identicos byte a byte aos da quarta) "
    "foi levada ao sandbox %s por reconstruir_kernel_v412_r3.py (um comando; so' o que depende da fonte recompila). Compilaram %s de %s (rc 0); build %s s e Audit %s s (rodada anterior: %s s e %s s); "
    "TOTAL decl %s, thm %s, fora do trio %s; escada %s; %s bandeiras novas; chaves das bandeiras identicas as do R2: %s (pares chave-nome identicos: %s); chaves antigas que mudam: %s; "
    "ancoras propostas: %s nomes, por classe %s (mesma conta do R2: %s); avisos fora a TowerWedgeIndex: %s; recibo do kernel sha16 %s.\n\n"
    "Comparacao com o R2: linha TOTAL igual %s; escada igual %s; n de bandeiras igual %s; avisos por modulo iguais %s; nomes publicos e proveniencia iguais %s; audit.log igual em bytes %s.\n\n"
    "O um.py do Nos segue sha16 %s (igual ao fecho R2: %s); nenhum dos %s modulos do manifesto existe no kernel do Nos (existem: %s); modificados no Nos desde o inicio da rodada: %s.\n\n"
    "Licoes: (1) o preparo regravou so' os %s modulos trocados; o lake recompilou %s modulos mais a raiz e o Audit; (2) o gerador do fecho e' derivado do da rodada anterior por trocas de texto exato e blocos com marcador unico, "
    "e o derivador confere a contagem de cada troca (DERIVACAO_R3_v412.json); (3) a copia de bytes do estado do R2 (.bak_r2) foi feita ANTES do build, por script, e cobre os recibos e os logs de kernel/; "
    "(4) a checagem do pos_build 'os modulos que ESTE build tinha de compilar tem linha Built' passa VAZIA (0 exigidos: o filtro pede o prefixo TGLExt. e a lista de ULTIMA_INSTALACAO traz nomes sem prefixo; tambem no R2): "
    "a gerencia deve consertar no molde antes do candidato; aqui a leitura direta foi feita a parte (conferir_built_esperado_r3_v412.py: os 8 previstos tem Built, nenhum outro).\n\n"
    "Quem constroi nao aprova: a revisao de terceiro, o congelamento do contrato, a Etapa 2, a tarefa agendada, o rito e a custodia sao da gerencia. Validade no kernel nao e' creditacao; o gate nao se move.\n"
) % (agora.strftime("%d/%m/%Y"), P["estado"], M["sha16"], M["n_modulos"], Q["n_trocados"], Q["n_iguais"], K["sandbox"], K["modulos_compilados_rc0"], K["n_modulos"],
     K["duracao_build_s"], K["duracao_audit_s"], C["duracao_build_s"]["r2"], C["duracao_audit_s"]["r2"], T.get("decl"), T.get("thm"), T.get("fora_do_trio"), K.get("escada_de_teoremas_e_bandeiras"), K.get("n_bandeiras_novas"),
     C["chaves_das_bandeiras_identicas"], C["pares_chave_nome_identicos"], C["chaves_antigas_mudam_agora"], A["n_nomes_conferidos"], A["por_classe"], (C.get("conferencia_das_ancoras_propostas") or {}).get("mesma_conta"),
     {k: v for k, v in av.items() if k != "TGLExt.TowerWedgeIndex"} or "nenhum", K["recibo"]["sha16"],
     C["linha_TOTAL_igual"], C["escada_igual"], C["n_bandeiras_novas_igual"], C["avisos_por_modulo_igual"], C["nomes_publicos_e_proveniencia_identicos"], C["audit_log_igual_ao_r2_em_bytes"],
     N.get("um_py_sha16"), N.get("um_py_igual_ao_fecho_R2"), N.get("n_modulos_do_manifesto_R5"), N.get("modulos_que_existem_no_kernel_do_Nos"), N.get("n_modificados_no_Nos_apos_o_inicio_da_rodada"),
     len(Q.get("mudados_no_sandbox_pelo_preparo") or []), len([m for m in (Q.get("o_lake_recompila") or []) if m not in ("TGLExt (raiz)", "TGL.Audit")]))
cab = ["---", "quem: claude-construtor-v412", "casa: Central de Patentes", "tipo: project", "estatuto: REAL", "alvo_sugerido: v412-preparacao-etapa1-17nov (ou novo:v412-quinta-lista-17nov)",
       "depositado_em: %s" % agora.astimezone().isoformat(timespec="seconds"), "fontes:"] + ["  - %s  sha256:%s" % (f, sha(f)) for f in fontes] + ["---"]
txt = "\n".join(cab) + "\n" + corpo
nome = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v412-quinta-lista-kernel-17nov.md")
iguais_r2 = all([C["linha_TOTAL_igual"], C["escada_igual"], C["n_bandeiras_novas_igual"], C["chaves_das_bandeiras_identicas"], C["avisos_por_modulo_igual"]])
rota = {"tipo": "RESULTADO", "rota_id": "cadeia.preparacao_v412.etapa1_k412c", "dominio": "CADEIA",
        "titulo": "17/11: continuacao 2 do complemento da Etapa 1: o kernel do sandbox k412c passou da quarta para a quinta lista de pedras (seis modulos com texto emendado); conferiu por script",
        "pergunta": "Os 40 modulos da quinta lista (seis com comentarios e docstrings emendados, codigo igual) compilam no sandbox e deixam as medicoes do fecho R2 como estavam?",
        "dados": ["nenhum dado; build Lean no sandbox C:/t/k412c/final (lake so' no sandbox)"],
        "metodo": "agente construtor em segundo plano: conferencia da quinta lista (sha256 contra o manifesto R5; 34 identicos byte a byte; codigo dos 6 emendados igual por dois metodos), copia de bytes do estado do R2 (.bak_r2), scripts _r3 derivados dos _r2 por troca exata com contagem conferida, reconstruir_kernel_v412_r3.py (um comando), medicoes e recibos, comparacao com o fecho R2",
        "resultado": ("[DECLARADO pelo construtor; hashes e numeros lidos dos recibos] %s de %s modulos com saida zero no sandbox; build %s s e Audit %s s (R2: %s s e %s s); TOTAL decl %s, thm %s, fora do trio %s; escada %s; %s bandeiras novas; "
                      "chaves das bandeiras identicas as do R2: %s; ancoras propostas %s nomes %s; avisos fora a TowerWedgeIndex: %s; igual ao R2 em tudo medido: %s. O um.py do Nos segue sha16 %s; nenhum modulo do manifesto no kernel do Nos.") % (
            K["modulos_compilados_rc0"], K["n_modulos"], K["duracao_build_s"], K["duracao_audit_s"], C["duracao_build_s"]["r2"], C["duracao_audit_s"]["r2"], T.get("decl"), T.get("thm"), T.get("fora_do_trio"),
            K.get("escada_de_teoremas_e_bandeiras"), K.get("n_bandeiras_novas"), C["chaves_das_bandeiras_identicas"], A["n_nomes_conferidos"], A["por_classe"], {k: v for k, v in av.items() if k != "TGLExt.TowerWedgeIndex"} or "nenhum",
            iguais_r2, N.get("um_py_sha16")),
        "veredito": ("CONTINUACAO_2_FECHADA__QUINTA_LISTA_40_MODULOS_NO_SANDBOX__MEDICOES_IGUAIS_AO_R2__NOS_INTACTO__FALTA_CONGELAR_O_CONTRATO_E_A_ETAPA_2" if (fechou and iguais_r2) else
                     ("CONTINUACAO_2_FECHADA__QUINTA_LISTA_40_MODULOS_NO_SANDBOX__HA_DIFERENCA_PARA_O_R2__VER_O_FECHO" if fechou else "CONTINUACAO_2_NAO_FECHOU__VER_KERNEL_POS_BUILD")),
        "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False,
        "defeito": "o build foi incremental (o lake recompilou so' o que mudou ou depende do que mudou; o rito do Nos compila tudo a frio); a escolha dos prefixos das bandeiras e das ancoras e' do contrato, ainda rascunho; a arvore so-fontes da rodada anterior fica ao lado (movida, nao apagada); a checagem do pos_build que exige Built nos modulos a recompilar passa vazia (filtro de prefixo TGLExt. contra nomes sem prefixo; tambem no R2), suprida a parte por leitura direta",
        "nao_refazer": "Nao reinstalar os 40 modulos: estao no sandbox k412c com recibo da quinta lista. Trocar uma fonte e' um comando: reconstruir_kernel_v412_r3.py com --manifesto e --pedras",
        "proximo_passo": "se o revisor pedir outro texto, regerar a lista e trocar a fonte pelo mesmo comando; congelar o contrato; ordem da Etapa 2 pelo metodo",
        "onde": "C:\\t\\k412c\\final (sandbox); work\\cadeia_de_selo\\v412 (fecho R3, recibos em kernel\\, scripts _r3)",
        "artefatos": [PP, os.path.join(HERE, "kernel", "KERNEL_RECIBO_v412.json"), os.path.join(HERE, "kernel", "CODIGO_R4_R5_v412.json"), os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R5.json")],
        "refs": ["cadeia.v412_limpeza_das_pedras_pelo_metodo_17nov"], "nota": "Registro do construtor. Consultou o Mapa antes e leu o resultado anterior desta rota; nada refeito."}
rota_p = os.path.join(HERE, "registro_mapa_construtor_r3_v412.json")
if "--seco" in sys.argv:
    print(txt[:6000]); print(json.dumps(rota, ensure_ascii=False)[:2500]); sys.exit(0)
os.makedirs(FILA, exist_ok=True)
assert not os.path.exists(nome), nome
open(nome + ".tmp", "wb").write(txt.encode("utf-8")); assert os.path.getsize(nome + ".tmp") == len(txt.encode("utf-8")); os.replace(nome + ".tmp", nome)
open(rota_p + ".tmp", "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(rota_p + ".tmp", rota_p)
print("deposito:", nome, "| sha16", sha(nome)[:16]); print("rota (para o rotas.py):", rota_p)
