# -*- coding: utf-8 -*-
"""depositar_construtor_etapa2_v412.py -- (claude-construtor-v412, Etapa 2, contrato R4) (1) o deposito do construtor na FILA DA MEMORIA (memory/fila/depositos/claude-construtor-v412/; so' acrescimo; nome com data e hora; formato de
memory/fila/README.md) e (2) o JSON do RESULTADO da rota cadeia.preparacao_v412.etapa2_candidato para o Mapa de Rotas (o registro pelo rotas.py e' feito fora deste script). Numeros e hashes LIDOS de PREPARACAO_v412_PRONTA.json e dos recibos.
uso: C:/Python314/python.exe -B -X utf8 depositar_construtor_etapa2_v412.py [--seco]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v412")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PP = os.path.join(HERE, "PREPARACAO_v412_PRONTA.json")
P = json.load(open(PP, encoding="utf-8"))
C, K, G = P["candidato"], P["kernel"], P["guarda_de_frases"]
E = P.get("ensaio_a_seco") or {}
fontes = [PP, os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R4.json"), os.path.join(HERE, "CANDIDATO_v412.json"), os.path.join(HERE, "GUARDA_v412_UNIDADES.json"), os.path.join(HERE, "GUARDA_FRASES_v412.json"),
          os.path.join(HERE, "REGISTROS_v412_RECIBO.json"), os.path.join(HERE, "ANCORAS_ESCOLHIDAS_v412.json"), os.path.join(HERE, "PORTAO_DO_PILAR_CANDIDATO_v412.json"), os.path.join(HERE, "ENSAIO_RESULTADO_v412.json"),
          os.path.join(HERE, "kernel", "POS_BUILD_v412.json")]
fontes = [f for f in fontes if os.path.exists(f)]
agora = datetime.datetime.now()
corpo = (
    "v412, Etapa 2 (contrato R4), por claude-construtor-v412 para a gerencia c1, %s. Candidato %s (%s bytes; base v411 %s), NAO instalado, rito NAO rodado. Estado: %s.\n\n"
    "[REAL, lido dos recibos] Kernel: setima lista (42 modulos; Token2 e AMaquina novos na frente A), sandbox C:\\t\\k412c\\final, TOTAL decl %s, thm %s, fora do trio %s; escada %s -> %s (%s bandeiras novas); chaves antigas que mudam: %s. "
    "Registros por especificacao: %s (ancoras por registro %s); cada um com a checagem da guarda de frases. Guarda da v412 pela travessia (unidade por unidade): controles %s de %s; %s superficies, %s unidades examinadas, P = nP/fluidos %s unidades, todas limpas; "
    "marcadores herdados do handoff conferidos por bytes: %s. Portao do pilar no candidato: %s. Guarda de material privado: limpo %s (%s arquivos). Ensaio a seco: %s.\n\n"
    "Resumo: a emissao e' versionada (_V412_TOPO e _v412_topo_texto; os da v411 ficam). Patch de DADO que a gerencia deve ler: o literal 'escada' em _V411_H0DN_CONTRACT (baseline) sobe junto com os 30 'expected_ladder' (o registro herdado h0dn_bg1_v411 recusa sem isso). "
    "Pontos abertos: nao ha kh_n1_cobertura_v412 no contrato (a arvore nova nao tem pino exato; o da v411 virou piso); a bateria pre-selo, o rito, a instalacao e os scripts da custodia (pos_rito) seguem marcados [A ADAPTAR v412] e NAO foram adaptados.\n\n"
    "Quem constroi nao aprova: a revisao de terceiro, a tarefa agendada, o rito, o handoff e a custodia sao da gerencia. Validade no kernel nao e' creditacao; o gate nao se move.\n"
) % (agora.strftime("%d/%m/%Y"), C["sha16"], C["bytes"], C["base_v411_sha16"], P["estado"], K["linha_TOTAL"]["decl"], K["linha_TOTAL"]["thm"], K["linha_TOTAL"]["fora_do_trio"], P["escada"]["antes_v411"], P["escada"]["depois_candidato"], P["escada"]["bandeiras_novas"],
     K["chaves_antigas_mudam"], P["registros"]["nomes"], P["registros"]["ancoras_escolhidas"]["n_por_registro"], G["controles"]["n_ok"], G["controles"]["n"], G["travessia"]["n_superficies"], G["travessia"]["n_unidades_total"], G["travessia"]["n_unidades_com_p_igual_np_ou_fluidos"],
     G["marcadores_herdados"], (P["portao_do_pilar_no_candidato"].get("resumo") or {}).get("ok"), P["guarda_de_material_privado"]["limpo"], P["guarda_de_material_privado"]["n_arquivos"], E or "ver ENSAIO_RESULTADO_v412.json")
cab = ["---", "quem: claude-construtor-v412", "casa: Central de Patentes", "tipo: project", "estatuto: REAL", "alvo_sugerido: v412-preparacao-etapa2-17nov (ou novo:v412-candidato-r4-17nov)", "depositado_em: %s" % agora.astimezone().isoformat(timespec="seconds"), "fontes:"] \
      + ["  - %s  sha256:%s" % (f, sha(f)) for f in fontes] + ["---"]
txt = "\n".join(cab) + "\n" + corpo
nome = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v412-candidato-r4-etapa2-17nov.md")
rota = {"tipo": "RESULTADO", "rota_id": "cadeia.preparacao_v412.etapa2_candidato", "dominio": "CADEIA",
        "titulo": "17/11: Etapa 2 da v412 pelo contrato R4: candidato gerado (42 modulos, 4 registros por especificacao, guarda por travessia, resumo versionado), ensaiado a seco, nao instalado",
        "pergunta": "O candidato da v412 pelo contrato R4 gera, passa a guarda de frases unidade por unidade e passa o ensaio a seco sem mexer no que a v411 selou?",
        "dados": ["nenhum dado da natureza; kernel Lean no sandbox C:/t/k412c/final; texto da pagina R13"],
        "metodo": "construtor: setima lista no sandbox (42/42), registros por especificacao com a checagem da guarda, travessia com 21 controles, gerador por patches de ast sobre a v411 selada, ensaio a seco por subagente, recibos por script",
        "resultado": "[DECLARADO pelo construtor; hashes e numeros lidos dos recibos] " + corpo.split("\n\n")[1][:1800], "veredito": "CANDIDATO_R4_GERADO__ENSAIO_A_SECO_NO_RECIBO__NAO_INSTALADO__REVISAO_DE_TERCEIRO_E_DECISOES_DA_GERENCIA_PENDENTES",
        "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False,
        "defeito": "ver o recibo do ensaio; nao ha pino exato da arvore nova (kh_n1_cobertura_v412 fora do contrato); patch de dado no literal escada do contrato do H0DN herdado; bateria pre-selo e scripts de rito/custodia nao adaptados",
        "nao_refazer": "Nao regerar o kernel: o sandbox k412c esta na setima lista com recibo (PRONTO_PARA_CANDIDATO_v412_R4.json). Trocar fonte e' um comando: reconstruir_kernel_v412_c4.py com --manifesto e --pedras",
        "proximo_passo": "revisao de terceiro do candidato; decisoes da gerencia sobre os pontos abertos; adaptar os scripts de rito e custodia; palavra final do autor sobre o texto publico", "onde": "work\\cadeia_de_selo\\v412 (candidato e recibos); C:\\t\\k412c\\final (sandbox)",
        "artefatos": fontes, "refs": ["cadeia.preparacao_v412.etapa1_k412c"], "nota": "Registro do construtor. Consultou o Mapa antes (rotas da v412) e leu o resultado anterior desta cadeia."}
rota_p = os.path.join(HERE, "registro_mapa_construtor_etapa2_v412.json")
if "--seco" in sys.argv:
    print(txt[:5000]); sys.exit(0)
os.makedirs(FILA, exist_ok=True)
assert not os.path.exists(nome), nome
open(nome + ".tmp", "wb").write(txt.encode("utf-8")); assert os.path.getsize(nome + ".tmp") == len(txt.encode("utf-8")); os.replace(nome + ".tmp", nome)
open(rota_p + ".tmp", "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(rota_p + ".tmp", rota_p)
print("deposito:", nome, "| sha16", sha(nome)[:16]); print("rota (para o rotas.py):", rota_p)
