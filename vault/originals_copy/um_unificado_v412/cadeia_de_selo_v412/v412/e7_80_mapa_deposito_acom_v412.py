"""R7: depois do fecho PREPARACAO_v412_PRONTA_R7.json, (1) monta o registro da ROTA desta etapa no Mapa de Rotas (numeros LIDOS do fecho e dos recibos) e o registra (`rotas.py registrar ... --quem claude-construtor-v412`), gravando o recibo;
(2) grava o deposito de memoria na fila da gerencia (so' acrescimo; a gerencia promove); (3) monta o arquivo de transicao da memoria ACOM (q: fato com fonte e estatuto; p: fase e proxima acao). Nao regera o fecho.
uso: C:\\Python314\\python.exe -B -X utf8 e7_80_mapa_deposito_acom_v412.py [--so-montar]"""
import datetime, json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
F = L.ler_json(D / "PREPARACAO_v412_PRONTA_R7.json")
k = F["kernel"]; esc = F["escada"]; cand = F["candidato"]; ens = F.get("ensaio_a_seco") or {}; gu = F["guarda_de_frases"]
regs = F["registros"]["n_ancoras_por_registro"]; chk = F["registros"]["n_checagens_por_registro"]
tot = k.get("linha_TOTAL") or {}
resultado = ("[DECLARADO pelo construtor; hashes e numeros lidos dos recibos] [REAL, lido dos recibos] Kernel da decima primeira lista: %s modulos compilados a frio no sandbox C:\\t\\k412c\\final, TOTAL decl %s, thm %s, fora do trio %s; escada de bandeiras %s -> %s; "
             "chaves antigas que mudam: %s. Registros por especificacao (ancoras): %s; checagens: %s. Guarda de frases pela travessia: %s controles de %s; %s superficies, %s unidades examinadas. Candidato %s (%s bytes), nao instalado. "
             "Ensaio a seco: %s, %s de %s checagens de unidade. Portao do pilar no candidato: %s. Guarda de material privado: limpo %s."
             % (k.get("n_modulos"), tot.get("decl"), tot.get("thm"), tot.get("fora_do_trio"), esc["bandeiras"]["antes_v411"], esc["bandeiras"]["depois_candidato"], k.get("chaves_antigas_mudam"), json.dumps(regs, ensure_ascii=False), json.dumps(chk, ensure_ascii=False),
                gu["controles"]["n_ok"], gu["controles"]["n"], gu["travessia"]["n_superficies"], gu["travessia"]["n_unidades_total"], cand["sha16"], cand["bytes"], ens.get("veredito"), ens.get("n_ok"), ens.get("n_checagens_unidade"),
                (F["portao_do_pilar_no_candidato"] or {}).get("ok"), (F["guarda_de_material_privado"] or {}).get("limpo")))
rota = {"tipo": "RESULTADO", "rota_id": "cadeia.preparacao_v412.etapa2_candidato_r7", "dominio": "CADEIA",
        "titulo": "18/11: Etapa 2 da v412 pelo contrato R7: candidato regerado (156 modulos, cinco registros por especificacao, pagina R21), ensaiado a seco, nao instalado",
        "pergunta": "O candidato da v412 pelo contrato R7 compila a frio os 156 modulos, passa a travessia da guarda de frases e o ensaio a seco sem mexer no que a v411 selou?",
        "dados": ["nenhum dado da natureza; kernel Lean no sandbox C:/t/k412c/final; texto da pagina R21"],
        "metodo": "construtor: decima primeira lista a frio no sandbox, ancoras pela regra do contrato com o nome completo lido do relatorio de axiomas, cinco registros por especificacao com a travessia da guarda, gerador por patches de ast sobre a v411 selada, ensaio a seco, recibos por script",
        "resultado": resultado, "veredito": "CANDIDATO_R7_GERADO__ENSAIO_A_SECO_NO_RECIBO__NAO_INSTALADO__REVISAO_DE_TERCEIRO_PENDENTE", "estatuto": "REAL", "status": "EM_CURSO", "olhou_dados": False,
        "defeito": "ver o fecho PREPARACAO_v412_PRONTA_R7.json (pontos para a gerencia); nao ha' pino exato de cobertura do kernel para a arvore nova (piso da v411, excecao declarada); Etapa 3 nao comecada",
        "nao_refazer": "Nao regerar o kernel: o sandbox k412c esta na decima primeira lista com recibo (PRONTO_PARA_CANDIDATO_v412_R7.json); trocar fonte e' um comando: reconstruir_kernel_v412_r7.py com --manifesto e --pedras",
        "proximo_passo": "revisao de terceiro do candidato; leitura da pagina R21 ao autor; Etapa 3 (scripts de rito, instalacao, custodia e pos-rito)",
        "refs": ["cadeia.preparacao_v412.etapa2_candidato"], "nota": "Rota da Etapa 2 da v412 pelo contrato R7. Consultou o Mapa antes (rotas da v412)."}
RP = D / "registro_mapa_construtor_etapa2_r7_v412.json"
L.salvar_json(RP, rota)
if "--so-montar" not in sys.argv:
    r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(RP), "--quem", "claude-construtor-v412"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (("\n--- stderr ---\n" + r.stderr) if r.stderr else "")
    L.salvar_json(D / "registro_mapa_construtor_etapa2_r7_v412.recibo.json", {"quando": L.agora(), "rc": r.returncode, "saida": out[-3000:], "registro_sha16": L.sha16_arq(RP)})
    print("registrar rc", r.returncode, out[-600:])
    if r.returncode != 0:
        sys.exit(r.returncode)
# deposito de memoria
dep = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\claude-construtor-v412")
dep.mkdir(parents=True, exist_ok=True)
nome = dep / (datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_v412-candidato-r7-etapa2-18nov.md")
texto = ("---\nquem: claude-construtor-v412\ncasa: Nós\ntipo: project\nestatuto: DECLARADO\nalvo_sugerido: v412-preparacao-etapa1-17nov.md\nfontes:\n  - C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/PREPARACAO_v412_PRONTA_R7.json  sha256:%s\n---\n"
         "Etapa 2 da v412 pelo contrato R7 fechada pelo construtor (a continuacao da etapa interrompida pelo R5). Candidato %s (%s bytes; base v411 1203b1f9202020d6), gerado e NAO instalado; rito nao rodou. "
         "Kernel da decima primeira lista: %s modulos a frio no k412c, TOTAL decl %s thm %s, fora do trio %s; escada %s -> %s. Registros por especificacao (ancoras): %s. Guarda de frases: %s controles de %s; %s unidades. Ensaio a seco: %s (%s de %s). "
         "O build da decima lista (153 modulos) terminou antes, sem erro, e fica so' como informacao. Pontos para a gerencia no fecho (campo pontos_para_a_gerencia); Etapa 3 nao comecada. [DECLARADO pelo construtor; numeros lidos dos recibos]\n"
         % (L.sha256_arq(D / "PREPARACAO_v412_PRONTA_R7.json"), cand["sha16"], cand["bytes"], k.get("n_modulos"), tot.get("decl"), tot.get("thm"), tot.get("fora_do_trio"), esc["bandeiras"]["antes_v411"], esc["bandeiras"]["depois_candidato"], json.dumps(regs, ensure_ascii=False),
            gu["controles"]["n_ok"], gu["controles"]["n"], gu["travessia"]["n_unidades_total"], ens.get("veredito"), ens.get("n_ok"), ens.get("n_checagens_unidade")))
dep_tmp = Path(str(nome) + ".tmp"); dep_tmp.write_bytes(texto.encode("utf-8")); assert dep_tmp.stat().st_size == len(texto.encode("utf-8")); dep_tmp.replace(nome)
print("deposito:", nome)
# transicao ACOM
tr = {"event_id": "construtor-v412-etapa2-candidato-r7-18nov",
      "changes": {"records": [{"id": "construtor-v412-etapa2-r7", "kind": "fact", "statute": "REAL",
                               "text": "Etapa 2 da v412 pelo contrato R7 (sha16 %s) fechada pelo construtor: candidato %s (%s bytes; base v411 1203b1f9202020d6) gerado e NAO instalado; kernel da decima primeira lista (%s modulos) a frio no sandbox, TOTAL decl %s thm %s fora do trio %s, escada %s -> %s; "
                                       "cinco registros por especificacao; guarda de frases pela travessia: controles %s de %s, %s unidades; ensaio a seco: %s (%s de %s). Etapa 3 nao feita. Rito nao rodou."
                                       % (L.sha16_arq(L.CONTRATO), cand["sha16"], cand["bytes"], k.get("n_modulos"), tot.get("decl"), tot.get("thm"), tot.get("fora_do_trio"), esc["bandeiras"]["antes_v411"], esc["bandeiras"]["depois_candidato"], gu["controles"]["n_ok"], gu["controles"]["n"],
                                          gu["travessia"]["n_unidades_total"], ens.get("veredito"), ens.get("n_ok"), ens.get("n_checagens_unidade")),
                               "sources": [{"kind": "artifact", "ref": "C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/PREPARACAO_v412_PRONTA_R7.json#sha256:%s" % L.sha256_arq(D / "PREPARACAO_v412_PRONTA_R7.json")}]}],
                  "flow": {"phase": "preparacao_v412__etapa2_r7_candidato_pronto__parado", "next_action": "gerencia: revisao de terceiro do candidato; ler a pagina R21 ao autor; Etapa 3 depois da aprovacao"}}}
TJ = D / "acom_construtor_v412" / "transicao_etapa2_r7.json"
L.salvar_json(TJ, tr)
print("transicao montada:", TJ, "(rodar: acom_init_construtor_v412.py --transicao <arquivo>)")
