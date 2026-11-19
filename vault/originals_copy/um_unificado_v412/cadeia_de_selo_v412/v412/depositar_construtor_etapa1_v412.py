# -*- coding: utf-8 -*-
"""depositar_construtor_etapa1_v412.py -- (claude-construtor-v412, 17/11/2026) (1) o deposito do construtor na FILA DA MEMORIA (memory\\fila\\depositos\\claude-construtor-v412\\), no formato
de memory\\fila\\README.md (so' acrescimo: nunca edita deposito existente; nome com data e hora); (2) o JSON da rota da Etapa 1 para o Mapa de Rotas (registro pelo rotas.py, fora deste script).
Os numeros e hashes sao LIDOS de PRONTO_PARA_CANDIDATO_v412.json e dos recibos (nada digitado). Molde: v411\\depositar_construtor_v411.py e os depositos de claude-construtor-v411.
uso: C:\\Python314\\python.exe -B -X utf8 depositar_construtor_etapa1_v412.py [--seco]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v412")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
P = json.load(open(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412.json"), encoding="utf-8"))
K = P["kernel_k412c"]; B = P["bump"]; PL = P["portao_do_pilar"]
fontes = [os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412.json"), os.path.join(HERE, "kernel", "KERNEL_RECIBO_v412.json"), os.path.join(HERE, "kernel", "POS_BUILD_v412.json"),
          os.path.join(HERE, "kernel", "FLAGS_v412.json"), os.path.join(HERE, "BUNDLE_v412.json"), os.path.join(HERE, "PORTAO_DO_PILAR_v412.json"), os.path.join(HERE, "BUMP_v412_RESULTADO.json")]
fontes = [f for f in fontes if os.path.exists(f)]
agora = datetime.datetime.now()
av = {k: v for k, v in (K.get("avisos_por_modulo") or {}).items() if v}
corpo = (
    "v412 em preparacao por claude-construtor-v412 para a gerencia c1, %s: %s. Nada instalado no Nos; o rito nao rodou.\n\n"
    "[REAL, lido dos artefatos] Kernel: sandbox %s (copia do k411c, robocopy sem /PURGE; origem %s GB, %s arquivos, sem a juncao; disco C: com %s GB livres antes). "
    "Os %s modulos do manifesto (sha16 %s) instalados em TGLExt\\ com so' as duas mudancas permitidas (import de candidata irma -> import TGLExt.<Nome>; as linhas #print axioms fora do corpo, como o molde da v410); "
    "compilaram %s de %s no sandbox, um a um, na ordem topologica (rc 0); build %s s; Audit %s s; TOTAL decl %s, thm %s, fora do trio %s (v411: %s, %s, %s); "
    "escada %s; %s bandeiras novas (prefixos ext_<modulo>_412_ propostos pelo construtor; nenhuma chave antiga muda: %s de %s conferidas); %s ancoras no trio; avisos fora a TowerWedgeIndex: %s. "
    "Recibo do kernel sha16 %s.\n\n"
    "Portao do pilar (so' leitura de codigo do um.py v411 selado): %s\n\n"
    "Bump: %s arquivos da cadeia da v411 copiados com o rotulo subido (B21; a producao pina %s), cada um com a marca A ADAPTAR; %s deles trazem linhas do caso sem modulo novo, a adaptar pelo molde v410/v409 na Etapa 2.\n\n"
    "Trocar uma fonte: reconstruir_kernel_v412.py (um comando; so' o que depende da fonte recompila).\n\n"
    "Licoes: (1) o init ACOM recusa a ordem que cita o arquivo de ambiente e o caminho da outra casa; o construtor inscreveu um excerto declarado; (2) cada `lake build +modulo` repete as mensagens das dependencias: "
    "o log por modulo cresce (lake_build.log com %s bytes); (3) o reuso do pilar usa a placa mesmo sem calcular (sonda torch.cuda e autoteste do motor no dispositivo cuda).\n\n"
    "Quem constroi nao aprova: a revisao de terceiro, o congelamento do contrato, a Etapa 2, a tarefa agendada, o rito e a custodia sao da gerencia. Validade no kernel nao e' creditacao; o gate nao se move.\n"
) % (agora.strftime("%d/%m/%Y"), P["estado"], K["sandbox"], K["origem_medida_antes_da_copia"]["gb"], K["origem_medida_antes_da_copia"]["arquivos"], K["disco_C_livre_antes_da_copia_gb"],
     K["n_modulos"], P["manifesto"]["sha16"], K["modulos_compilados_rc0"], K["n_modulos"], K["duracao_build_s"], K["duracao_audit_s"],
     (K.get("linha_TOTAL") or {}).get("decl"), (K.get("linha_TOTAL") or {}).get("thm"), (K.get("linha_TOTAL") or {}).get("fora_do_trio"),
     (K.get("linha_TOTAL_v411") or {}).get("decl"), (K.get("linha_TOTAL_v411") or {}).get("thm"), (K.get("linha_TOTAL_v411") or {}).get("fora_do_trio"),
     K.get("escada_de_teoremas_e_bandeiras"), K.get("n_bandeiras_novas"), (K.get("chaves_antigas") or {}).get("n", 0) - len((K.get("chaves_antigas") or {}).get("mudam") or []), (K.get("chaves_antigas") or {}).get("n"),
     K.get("n_ancoras"), {k: v for k, v in av.items() if k != "TGLExt.TowerWedgeIndex"} or "nenhum", K["recibo"]["sha16"], PL.get("resposta"),
     B.get("n_arquivos"), B.get("deployment_da_producao_lido"), len(B.get("arquivos_com_linhas_do_caso_sem_modulo_novo") or {}), (K.get("lake_build_log") or {}).get("bytes"))
cab = ["---", "quem: claude-construtor-v412", "casa: Central de Patentes", "tipo: project", "estatuto: REAL", "alvo_sugerido: novo:v412-preparacao-etapa1-17nov",
       "depositado_em: %s" % agora.astimezone().isoformat(timespec="seconds"), "fontes:"] + ["  - %s  sha256:%s" % (f, sha(f)) for f in fontes] + ["---"]
txt = "\n".join(cab) + "\n" + corpo
nome = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v412-preparacao-etapa1-17nov.md")
rota = {"tipo": "ROTA", "rota_id": "cadeia.preparacao_v412.etapa1_k412c", "dominio": "KERNEL_FORMAL",
        "titulo": "17/11: Etapa 1 da preparacao da v412 -- sandbox k412c, os %s modulos novos instalados e compilados no sandbox, Audit, bump mecanico, portao do pilar por leitura de codigo" % K["n_modulos"],
        "pergunta": "os modulos Lean da v412 compilam juntos no kernel da v411, so' no trio, sem colisao de nome, e a chave do pilar muda com o que a v412 traz?",
        "dados": ["insumos\\MANIFESTO_PEDRAS_v412.json (sha16 %s)" % P["manifesto"]["sha16"], "kernel do Nos v411 selado (so' leitura)", "C:\\t\\k411c\\final (origem do sandbox)"],
        "metodo": "robocopy sem /PURGE; preparo do bundle com conferencia de sha256 e reconstrucao independente; lake build por modulo na ordem topologica, build inteiro e Audit no sandbox; pos_build com as funcoes do um.py v411 por ast; leitura de codigo do pilar por fecho de dependencias",
        "resultado": "compilaram %s de %s; escada %s; decl %s; fora do trio %s; bandeiras novas %s; chave do pilar: %s" % (K["modulos_compilados_rc0"], K["n_modulos"], K.get("escada_de_teoremas_e_bandeiras"), K.get("declaracoes_no_relatorio_de_axiomas"),
                                                                                                      (K.get("linha_TOTAL") or {}).get("fora_do_trio"), K.get("n_bandeiras_novas"), "nao muda com a v412 (fecho sem kernel, registro nem artigo)" if not (PL.get("o_que_a_v412_muda") or {}).get("entra_no_fecho_da_chave") else "MUDA"),
        "veredito": "V412_ETAPA1__K412C_BUILT__%s_OF_%s_MODULES_IN_THE_TRIO__PILLAR_KEY_UNCHANGED_BY_THE_V412_CHANGES__NO_CANDIDATE__GATE_UNTOUCHED" % (K["modulos_compilados_rc0"], K["n_modulos"]) if P["etapa_1_fechou"] else "V412_ETAPA1__STOPPED_AT_%s" % K.get("parou_em"),
        "estatuto": "REAL", "status": "EXAMINADA" if P["etapa_1_fechou"] else "BLOQUEADA", "olhou_dados": False,
        "defeito": "o DESENHO_v412 segue RASCUNHO e a ordem 023 pode mudar texto de sete fontes: o kernel se reconstroi por reconstruir_kernel_v412.py; os scripts bumpados seguem A ADAPTAR",
        "nao_refazer": "nao recopiar o k411c nem reinstalar a mao: reconstruir_kernel_v412.py troca uma fonte e recompila so' o que depende dela; nao refazer o portao do pilar por leitura (PORTAO_DO_PILAR_v412.json)",
        "proximo_passo": "a gerencia: revisao do Codex, congelar o contrato, prefixos das bandeiras; Etapa 2 (delta, registros, artigo, guarda de frases, candidato); o portao do pilar no candidato e o ambiente da placa antes do rito",
        "onde": "work\\cadeia_de_selo\\v412 (preparar_bundle_v412.py, construir_kernel_v412.sh, pos_build_kernel_v412.py, reconstruir_kernel_v412.py, portao_do_pilar_v412.py, _bump_copia_v412.py)",
        "artefatos": fontes, "refs": ["kernel.camada_cientifica_candidata_14nov", "kernel.ergodicidade_de_mautner_candidata_15nov"],
        "nota": "o init ACOM da ordem foi recusado (regras de conteudo confidencial) e inscrito por excerto declarado; nada instalado; o rito nao rodou"}
rota_p = os.path.join(HERE, "registro_mapa_construtor_etapa1_v412.json")
if "--seco" in sys.argv:
    print(txt[:3000]); print(json.dumps(rota, ensure_ascii=False)[:1500]); sys.exit(0)
os.makedirs(FILA, exist_ok=True)
assert not os.path.exists(nome), nome
open(nome + ".tmp", "wb").write(txt.encode("utf-8")); assert os.path.getsize(nome + ".tmp") == len(txt.encode("utf-8")); os.replace(nome + ".tmp", nome)
open(rota_p + ".tmp", "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(rota_p + ".tmp", rota_p)
print("deposito:", nome, "| sha16", sha(nome)[:16]); print("rota (para o rotas.py):", rota_p)
