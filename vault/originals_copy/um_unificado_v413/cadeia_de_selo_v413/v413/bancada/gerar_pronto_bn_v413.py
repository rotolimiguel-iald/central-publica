# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] o fecho da ordem ORDEM_BN_v413.md: PRONTO_BN_v413.json, com tudo LIDO por script (sha16 dos arquivos, linhas achadas pelas ancoras, resultados dos testes).
"""gerar_pronto_bn_v413.py -- grava PRONTO_BN_v413.json (novo; backup de bytes se ja existir): cada script com sha16 e bytes; cada pendencia (as 15 da lista e N1-N9) com o estado e onde (arquivo e linha, achados aqui pela
ancora de texto, nunca digitados); os testes hermeticos e os controles negativos (lidos dos resultados); os artefatos do pre-selo ja gerados (a cadeia e a bateria da v412, por sha16); o estado de agora para o pre-selo
(medido por leitura: o Nos, a Bancada, o sandbox curto, restos de rodada); o que falta. uso: python -I -B -X utf8 gerar_pronto_bn_v413.py"""
import datetime
import glob
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

s16 = lambda p: U.sha256_arquivo(p)[:16]
MEUS = ["delta_bn_v413.py", "util_bn_v413.py", "gerar_e_pinar_cadeia_v413.py", "gerar_bateria_v412_pre_selo_v413.py", "rodar_ensaio_1_pre_selo_v413.sh", "snap_producao_v413.py",
        "conferir_recibo_pre_selo_salto_v413.py", "gerar_pino_recibo_pre_selo_v413.py", "limpar_sandbox_vb24.py", "diff_e_pinos_bn_v413.py", "p00_precondicoes_bn_v413.py", "rodar_bn_pre_selo_v413.sh",
        "bn_v413.sh", "b3_recibo_v413.py", "recibo_parada_v413.py", "recibo_religamento_v413.py", "evento_c1_b3_v413.py", "fechar_bn_v413.py", "gravar_pino_bateria_v413.py",
        "conferir_exigencias_servico_v413.py", os.path.join("controle_negativo", "mutar_conferidor_v413.py"), "saude_bancada.py", "sentinela_boot_bancada.py",
        "montar_autorizacao_v413.py", "aviso_f06_v413.py", "ensaio_a_seco_pos_selo_v413.py",
        os.path.join("ensaio_hermetico", "mundo_falso_bn_v413.py"), os.path.join("ensaio_hermetico", "ensaio_hermetico_bn_v413.py"), "gerar_pronto_bn_v413.py"]
scripts = {n: {"sha16": s16(os.path.join(HERE, n)), "bytes": os.path.getsize(os.path.join(HERE, n))} for n in MEUS}


def linha(arq, ancora):
    p = os.path.join(HERE, arq)
    for i, l in enumerate(open(p, encoding="utf-8").read().splitlines(), 1):
        if ancora in l:
            return {"arquivo": arq, "linha": i, "ancora": ancora[:80]}
    raise SystemExit("ancora nao achada (o PRONTO nao digita linha): %s :: %s" % (arq, ancora))


def onde(*pares):
    return [linha(a, b) for a, b in pares]


P = {}
P["1.1"] = {"estado": "feito", "onde": onde(("gerar_pino_recibo_pre_selo_v413.py", "VEREDITO_EXATO = ("), ("gerar_pino_recibo_pre_selo_v413.py", "r[\"veredito\"] == VEREDITO_EXATO == DBN.VEREDITO_PRE_SELO"),
                                            ("gerar_pino_recibo_pre_selo_v413.py", "recibo_entre_as_fotos = bool("), ("gerar_pino_recibo_pre_selo_v413.py", "sys.exit(0 if (utilizavel is True")),
            "nota": "aceita SO' o veredito exato do salto (REPINADA_B<GER+1>__SALTO_v411_v412__..., GER lido da producao no recibo); sai 1 com o pino inutil ou a producao alterada; o pino traz a cadeia e o bloco salto"}
P["1.2"] = {"estado": "feito", "onde": onde(("rodar_bn_pre_selo_v413.sh", "SB_W=$(UV const SANDBOX_CURTO)"), ("rodar_bn_pre_selo_v413.sh", "ja existe (de outra rodada)"),
                                            ("rodar_bn_pre_selo_v413.sh", "RC_LIMPAR=0; $PY limpar_sandbox_vb24.py"), ("rodar_bn_pre_selo_v413.sh", "UTIL=$(UV json"),
                                            ("rodar_bn_pre_selo_v413.sh", '{ [ "$RC_P00" != 0 ] && [ "$RC_P00" != 3 ]; }'), ("rodar_bn_pre_selo_v413.sh", '"$OUTB/LIMPEZA_SANDBOX_$(basename "$SB").json"')),
            "nota": "o sandbox curto LIDO do delta_bn (nenhum literal vb23); rc real de cada passo, inclusive o do p00 (revisao B1: 0 ou 3 passam, 1 falha); o utilizavel lido do pino; restos de outra rodada recusados "
                    "(o pino, a prova, a conferencia e, pela revisao B2, a pasta prova_producao e o LIMPEZA_SANDBOX_vb24.json)"}
P["1.3"] = {"estado": "feito (no molde da v412); no salto o anterior e' v413\\base_v412", "onde": onde(("conferir_recibo_pre_selo_salto_v413.py", "SELO_ANT = os.path.join(DBN.BASE_UM_PY_ANTERIOR")), "nota": "o conferir do salto e' o C.1"}
P["1.4"] = {"estado": "feito no B(n); as guardas estaticas sao da Etapa 2", "onde": onde(("diff_e_pinos_bn_v413.py", 'pn["delta_bn"] = f('), ("diff_e_pinos_bn_v413.py", 'pn["delta"] = f(_dp'),
                                                                                       ("bn_v413.sh", "for k in criterios esboco_R3_6"), ("bn_v413.sh", "o delta_bn_v413.py em uso nao e' o pinado"),
                                                                                       ("delta_bn_v413.py", 'SANDBOX_CURTO = os.path.join(C, "t", "vb24")')),
            "nota": "(a) o PINOS_BN pina o delta principal (--delta), o delta_bn e o util por sha; (b) o b3_prepara confere os tres; (c) SANDBOX_CURTO = C:\\t\\vb24, EXCLUSIVO do pre-selo real (revisao M1): o controle "
                    "negativo usa uma pasta temporaria (V413_MUTAR_TEMP; padrao %TEMP%\\mutar_conferidor_v413) e recusa vb24; os testes usam vb98/vb99; o p00 recusa SANDBOX_CURTO igual a vb22, vb23 ou vb25. NAO feito aqui: o "
                    "guardas_estaticas_bancada da v413 e' derivado pela Etapa 2, que a gerencia avisou para usar C:\\t\\vb25 (nunca vb24)"}
P["1.5"] = {"estado": "feito (no molde da v412)", "onde": [], "nota": "fim_de_cadeia_v412.sh.NAO_RODAR.md; nenhum fim_de_cadeia da v413 foi criado aqui"}
P["2.1"] = {"estado": "feito", "onde": onde(("bn_v413.sh", 'ORDEM="10 10a 10b 10c 11"'), ("bn_v413.sh", "if quer 11; then"), ("fechar_bn_v413.py", "def recibos_b3():"),
                                            ("fechar_bn_v413.py", "PINO_P = os.path.join(DBN.SAIDAS_BN_DIR"), ("fechar_bn_v413.py", "# a reconferencia depois do nascimento"), ("fechar_bn_v413.py", "# a entrega onde o evento 1687 pede")),
            "nota": "os tres recibos juntos (glob bancada_B3 e bancada_B3_<k>; o APLICAR do salto cujo manifesto novo e' o do disco), o evento no livro, o pino conjunto com o seq e o hash, a reconferencia, rc 2 sem gravar, a copia na pasta bench do 1687"}
P["2.2"] = {"estado": "feito", "onde": onde(("util_bn_v413.py", "def livro_conferido(path):"), ("recibo_parada_v413.py", "LIVRO = U.livro_conferido(DBN.QUADRO)"), ("recibo_religamento_v413.py", "LIVRO = U.livro_conferido(DBN.QUADRO)")),
            "nota": "a regra do esboco (l.693-707): toda linha le como JSON (ilegivel = ValueError, nunca continue), anterior e hash conferidos, seq sem repeticao; os recibos nao tem leitor proprio"}
P["2.3"] = {"estado": "feito", "onde": onde(("recibo_religamento_v413.py", 'CANDS = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3"'), ("recibo_religamento_v413.py", "assert len(APLICADOS) == 1")), "nota": "so' o veredito do APLICAR do salto; exatamente 1 com o manifesto do disco"}
P["2.4"] = {"estado": "feito", "onde": onde(("bn_v413.sh", 'if [ -z "$a" ] || [ "$a" = "None" ]')), "nota": "pino pendente = AGUARDA (rc 20), nao traceback"}
P["2.5"] = {"estado": "feito", "onde": onde(("diff_e_pinos_bn_v413.py", "pendentes.append(_NDD)")), "nota": "sem diff no PATH, o DIFF_v412_v413.diff vai a pendentes (e o 10b exige pendentes == [])"}
P["2.6"] = {"estado": "feito", "onde": onde(("evento_c1_b3_v413.py", "assert os.path.isfile(ENSAIO_OUT)"), ("evento_c1_b3_v413.py", "assert RR.returncode == 0"), ("evento_c1_b3_v413.py", "assert r.returncode == 0"),
                                            ("evento_c1_b3_v413.py", 'print("EVENTO=%d EVENTO_HASH=%s"'), ("bn_v413.sh", "UR evento_depois_do_ensaio")),
            "nota": "(a) ENSAIO e b3_recibo dele com rc 0 antes de anotar; (b) rc do iald.py, retorno {ok, evento, hash} lido, elo conferido no livro; (c) o 10b recusa evento nao posterior ao fim do ensaio"}
P["2.7"] = {"estado": "feito", "onde": onde(("delta_bn_v413.py", "BANCADA_PINA_HOJE_FIXADA_V411 = {"), ("delta_bn_v413.py", "def _bancada_pina_hoje():"), ("delta_bn_v413.py", "def delta_v411_fixado():"),
                                            ("delta_bn_v413.py", "def delta_v412_fixado():"), ("bn_v413.sh", "UR pendentes_vazios")),
            "nota": "o B20 da v411 fixado (lido do recibo do religamento da v411); delta_v411 e delta_v412_r7 carregados por fonte com ele; _bancada_pina_hoje admite {v411/B20, v413/B21}; o 10b exige o PINOS_BN final"}
P["2.8"] = {"estado": "feito", "onde": onde((os.path.join("controle_negativo", "mutar_conferidor_v413.py"), "MUTACOES = ["), ("conferir_exigencias_servico_v413.py", "(M7)"), ("conferir_exigencias_servico_v413.py", "(M8)"),
                                            ("conferir_exigencias_servico_v413.py", "(M9)"), ("conferir_exigencias_servico_v413.py", "util (M11)")),
            "nota": "M1-M6 reapontados e M7, M8, M9, M10a/b/c, M11; cada mutacao pega pela condicao certa (ver testes)"}
P["C.1"] = {"estado": "feito", "onde": onde(("conferir_recibo_pre_selo_salto_v413.py", "aceito, recusa, res = conferir(RP, RSHA, SELO_ANT, KM_ANT)"), ("conferir_recibo_pre_selo_salto_v413.py", 'controle("sem_cadeia"')),
            "nota": "pela funcao do esboco com a cadeia; condicoes do salto; 9 controles (os 5 do plano + 4)"}
P["C.2"] = {"estado": "feito (no molde da v412)", "onde": [], "nota": "nenhum script da v413 usa nos_v411_do_cofre"}
P["N1"] = {"estado": "feito", "onde": onde(("rodar_bn_pre_selo_v413.sh", "PRAZO_DO_PRE_SELO_PERDIDO (N1)"), ("gerar_e_pinar_cadeia_v413.py", "PRAZO_DO_PRE_SELO_PERDIDO (N1)"), ("p00_precondicoes_bn_v413.py", "N1: o prazo do pre-selo")),
           "nota": "os geradores e o runner PARAM se o Nos nao estiver na v412; o p00 acusa a janela perdida"}
P["N2"] = {"estado": "feito (gerada e pinada em 20/11)", "onde": onde(("gerar_bateria_v412_pre_selo_v413.py", 'PINO_MIN = os.path.join(D, "PINO_MINIMO_CANDIDATO_v412.json")')), "nota": "caminho (a); pasta v413\\bateria_v412_pre_selo (nao ancestral da --saida)"}
P["N3"] = {"estado": "feito no p00 e no contrato para os backups e o registro; a custodia das pastas do salto (revisao M4) esta' no p00 e falta no contrato",
           "onde": onde(("p00_precondicoes_bn_v413.py", "N3: os backups de 18/11"), ("p00_precondicoes_bn_v413.py", "(2b) revisao M4"),
                        (os.path.join("..", "CONTRATO_v413_R1.md"), "são insumo do salto e não se podam até o fechamento do B21")),
           "nota": "o p00 e a cadeia conferem os backups por sha; o CONTRATO_v413_R1.md (secao 7) ja protege os .bak_20261118_235146 e o registro do instalador; o p00 confere agora tambem v413\\base_v412, v412\\base_v411, "
                   "a pasta da cadeia, a bateria da v412, o recibo pre-selo e o ensaio_1 (quando ha' pino) e a arvore do recibo do kernel (quando ha' pino); acrescentar ao contrato ou ao pedido ao LAR as pastas da M4 e' ato da gerencia"}
P["N4"] = {"estado": "feito", "onde": onde(("recibo_parada_v413.py", 'assert (("evento %d" % DBN.SEQ_AUTORIZACAO) in AUT'), ("recibo_religamento_v413.py", '("modo da placa: %s" % MODO_PLACA) in AUT'), ("delta_bn_v413.py", "SEQ_AUTORIZACAO = 1687")),
           "nota": "1687 e 1689 por hash (livro inteiro; recibo e fala pelos sha que os eventos registram) e a fala de 20/11; no religamento, a fala do modo da placa por parametro (sem ela, AGUARDA)"}
P["N5"] = {"estado": "feito", "onde": onde(("delta_bn_v413.py", "def delta_v411_fixado():")), "nota": "demonstrado: o delta_v411 vivo quebra com a Bancada em B21-v413; o fixado carrega"}
P["N6"] = {"estado": "feito", "onde": onde(("delta_bn_v413.py", 'BANCADA_ANTERIOR = "v411"'), ("delta_bn_v413.py", 'UM_PY_ANTERIOR = "v412"'), ("diff_e_pinos_bn_v413.py", 'pn["bancada_anterior_v411"]'), ("diff_e_pinos_bn_v413.py", 'pn["selo_anterior_v412"]')),
           "nota": "anterior da Bancada = v411 (religamento, PINA_HOJE, inicio da cadeia, b3_recibo); anterior do um.py = v412 (selo e kernel, fim da cadeia, DIFF_v412_v413)"}
P["N7"] = {"estado": "feito pela gerencia no contrato (lido aqui)", "onde": onde((os.path.join("..", "CONTRATO_v413_R1.md"), "ele não precisa do serviço e não grava na Bancada")),
           "nota": "o CONTRATO_v413_R1.md diz que o pre-selo nao precisa do servico; os scripts nao condicionam o B(n) ao servico no ar: o ensaio nao precisa dele e o APLICAR o exige parado"}
P["N8"] = {"estado": "feito", "onde": onde(("delta_bn_v413.py", 'SANDBOX_CURTO = os.path.join(C, "t", "vb24")'), ("limpar_sandbox_vb24.py", "ALVO = DBN.SANDBOX_CURTO")), "nota": "todos os scripts do B(n) leem o sandbox do delta_bn"}
P["N9"] = {"estado": "feito", "onde": onde(("recibo_religamento_v413.py", '_out = open(DBN.LOG_SERVIDOR, "ab")'), ("recibo_religamento_v413.py", '"log": LOG')), "nota": "o religamento lanca destacado com stdout e stderr anexados a estado\\servidor.log e servidor_erros.log e registra os tamanhos"}
medida = {"A_saude_bancada": {"estado": "feito", "arquivo": "saude_bancada.py", "nota": "so' leitura: porta, processos, /api/contratos (nunca /api/estado nem --check), contrato em disco pelo canonical.py, boot x religamento; 4 vereditos + INDETERMINADO (fail-closed)"},
          "C_portao_na_cadeia": {"estado": "feito", "onde": onde(("bn_v413.sh", "UR saude_do_dia"), ("bn_v413.sh", "UR pid_vivo_um_bancada")), "nota": "o 10 recusa sem conferencia A de hoje; o 11 sem o religamento de PID vivo"},
          "B_sentinela": {"estado": "preparada", "arquivo": "sentinela_boot_bancada.py", "nota": "a tarefa agendada NAO foi criada (ordem do operador)"}}
# a revisao independente unica (APROVADO_COM_RESSALVAS, 0 ALTO, 4 MEDIO, 13 BAIXO): o que foi aplicado, onde (ancoras achadas aqui) e o teste que o exercita
RV_P = os.path.join(HERE, "REVISAO_INDEPENDENTE_BN_v413.md")
CNM = os.path.join("controle_negativo", "mutar_conferidor_v413.py")
REV = {"revisao": {"path": RV_P, "sha16": s16(RV_P), "veredito": "APROVADO_COM_RESSALVAS (0 ALTO, 4 MEDIO, 13 BAIXO)"},
       "nota_dos_nomes": "o campo teste cita os testes do ensaio hermetico (secao + numero: A, B, C, D, E, F, NA/NB/NC); eles NAO sao os itens B1-B13 da revisao", "itens": {
    "B1": {"estado": "aplicado", "onde": onde(("rodar_bn_pre_selo_v413.sh", '{ [ "$RC_P00" != 0 ] && [ "$RC_P00" != 3 ]; }')), "teste": "E8", "nota": "o veredito final do runner le o rc do p00 (0 ou 3 passam; 1 falha), com o texto do revisor"},
    "B2": {"estado": "aplicado", "onde": onde(("rodar_bn_pre_selo_v413.sh", '"$OUTB/LIMPEZA_SANDBOX_$(basename "$SB").json"')), "teste": "E7", "nota": "a guarda de restos cobre prova_producao e LIMPEZA_SANDBOX_vb24.json"},
    "B3": {"estado": "aplicado", "onde": onde(("conferir_exigencias_servico_v413.py", 'bn13 = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", ')), "teste": "B1c",
           "nota": "o glob so' casa bancada_B3 e bancada_B3_<digitos>: a pasta do ENSAIO (bancada_B3_ensaio_*) nao da falha falsa depois do passo 10"},
    "B4": {"estado": "aplicado", "onde": onde(("aviso_f06_v413.py", 'TIPO = "AVISO_RECIBOS_B%d_ENTREGUES"'), ("bn_v413.sh", "revisao B4")), "teste": "B6c, B6d",
           "nota": "aviso_f06_v413.py anota o aviso F0.6 (--quem claude-c1 --unidade F0.6) com o pino conjunto e as copias dos tres recibos conferidas por sha256, nunca duas vezes; o passo 11 lembra o aviso como ato da gerencia"},
    "B5": {"estado": "aplicado", "onde": onde(("montar_autorizacao_v413.py", "faltam = [p_ for p_ in partes if p_ not in texto]")), "teste": "B5a, B5b, B5c, D5",
           "nota": "montar_autorizacao_v413.py monta o texto dos eventos 1687 e 1689 (livro conferido inteiro), do recibo e das falas, por script; grava bancada_B3_servico\\AUTORIZACAO_v413.txt (ou _RELIGAMENTO_<modo>.txt) com recibo; "
                   "idempotente; PARA se o arquivo existe diferente. Sobre o quadro e as falas REAIS (so' leitura, gravando numa pasta temporaria) deu o mesmo texto que o conferidor aceitou no controle negativo"},
    "B6": {"estado": "aplicado", "onde": onde(("evento_c1_b3_v413.py", "nada foi anotado de novo (B6)"), ("conferir_exigencias_servico_v413.py", 'chk("evento (B6)')), "teste": "B3c",
           "nota": "antes de anotar, procura no livro conferido o elo da claude-c1 SINCRONIZACAO_BANCADA com os mesmos dados e posterior ao fim do ensaio; se ha', devolve EVENTO= dele e sai com rc 0"},
    "B7": {"estado": "aplicado", "onde": onde(("recibo_religamento_v413.py", "RETIRADAS = []")), "teste": "B5", "nota": "as variaveis PYTHON* saem do ambiente do servidor; a lista vai ao recibo (ambiente_do_processo.variaveis_python_retiradas)"},
    "B8": {"estado": "aplicado", "onde": onde(("recibo_religamento_v413.py", "(revisao B8)")), "teste": "nenhum teste dinamico (a leitura ilegivel do PowerShell nao foi provocada); conferido por leitura; o B5 passa pelo caminho bom",
           "nota": "a leitura do processo depois do lancamento falha para RECUSA gravada com o PID, nunca traceback mudo"},
    "B9": {"estado": "aplicado", "onde": onde(("recibo_religamento_v413.py", "(revisao B9)")), "teste": "B5 (processo.breakaway no recibo)",
           "nota": "tenta CREATE_BREAKAWAY_FROM_JOB; se o Popen levanta OSError, lanca sem e o recibo diz breakaway false; se o servico sobrevive ao fim da sessao continua [OPEN] (o portao C do passo 11 pega)"},
    "B10": {"estado": "aplicado", "onde": onde(("util_bn_v413.py", "(revisao B10)")), "teste": "NB saude_do_dia (INDETERMINADO; outra Bancada)",
            "nota": "o portao C exige contrato SAUDE_BANCADA, a Bancada do delta_bn e veredito diferente de INDETERMINADO"},
    "B11": {"estado": "aplicado", "onde": onde(("bn_v413.sh", "(revisao B11)")), "teste": "E4b, E4c", "nota": "o 10b confere o modo da parada (pelo_pid | ja_fora_do_ar) e o evento da decisao 1689 no recibo da parada"},
    "B12": {"estado": "registrado para o plano da v414 (nao e' codigo da v413)", "onde": [],
            "nota": "o delta_v413.py (Etapa 2) carrega o delta_bn_v413.py por caminho e o _bancada_pina_hoje dele so' admite B20-v411 e B21-v413: depois do B22, importar o delta_v413 quebra. Na v414: fixar tambem a carga do "
                    "delta_bn dentro do delta_v413, nao so' a linha do BANCADA_PINA_HOJE"},
    "B13": {"estado": "aplicado", "onde": onde(("limpar_sandbox_vb24.py", "(revisao B13)")), "teste": "A7 (o limpar no mundo falso, irmaos conferidos)", "nota": "a conferencia dos irmaos de C:\\t compara so' as pastas vb*: log de outro agente em C:\\t nao da falha"},
    "M1": {"estado": "aplicado no meu lado; a Etapa 2 foi avisada pela gerencia (vb25)", "onde": onde((CNM, "(revisao M1)"), ("rodar_bn_pre_selo_v413.sh", "(revisao M1)"), ("p00_precondicoes_bn_v413.py", "N8/M1:")),
           "teste": "D4 (pasta temporaria no scratchpad), D4b (vb24 recusado sem criar nada)",
           "nota": "o controle negativo nunca usa C:\\t\\vb24 (padrao %TEMP%\\mutar_conferidor_v413; recusa vb24); os testes usam vb98/vb99 e o scratchpad; vb24 e' exclusivo do pre-selo real (rodar com a Etapa 2 parada e conferir que vb24 nao existe)"},
    "M2": {"estado": "aplicado (regra de execucao)", "onde": onde(("rodar_bn_pre_selo_v413.sh", "(revisao M2)")), "teste": "-",
           "nota": "o pre-selo e os passos 10 e 10b rodam com run_in_background (ou timeout de 600000 ms) e o veredito se le no arquivo de saida; o comando exato esta' em falta_para_rodar_o_pre_selo"},
    "M3": {"estado": "aplicado: (ii) no hermetico antes do selo; o ensaio a seco do pos-selo preparado para depois do selo",
           "onde": onde(("ensaio_a_seco_pos_selo_v413.py", "def finalizar(rc_final):"), (os.path.join("ensaio_hermetico", "ensaio_hermetico_bn_v413.py"), 'reg("B0a ')),
           "teste": "B0a, B0b (o esboco REAL em pos_selo ensaio do salto e o b3_recibo sobre o recibo dele); F0, F1 (auto-teste do ensaio a seco, sem bateria)",
           "nota": "ensaio_a_seco_pos_selo_v413.py: copia a Bancada (codigo e fontes relativas) e o Nos v412 para um mundo fora de work, roda o pre-selo do salto e os passos 10 a 11 com o esboco REAL em --sandbox, um servidor "
                   "minimo de contratos e um iald.py do mundo; apaga o mundo e o sandbox (C:\\t\\vb98); grava o resultado em bancada\\ensaio_a_seco. Sem bateria (auto-teste) o APLICAR, o religamento e o fechar nao rodam "
                   "(o esboco proibe aplicar sem bateria): eles so' se provam no ensaio a seco real, depois do selo"},
    "M4": {"estado": "aplicado no p00; a frase do contrato e' ato da gerencia", "onde": onde(("p00_precondicoes_bn_v413.py", "(2b) revisao M4"), ("p00_precondicoes_bn_v413.py", "revisao M4: a arvore so-fontes")),
           "teste": "A9 (o p00 no mundo falso, com o pino do pre-selo: so' o caminho bom; nenhum negativo de pasta faltando foi provocado)",
           "nota": "o p00 confere v413\\base_v412 e v412\\base_v411 (tres arquivos cada), a pasta da cadeia (cadeia e pino), a bateria da v412, e, quando ha' pino, o recibo pre-selo, o ensaio_1 e a arvore do recibo do kernel"}}}
# os testes, lidos dos resultados
RH = os.path.join(HERE, "ensaio_hermetico", "RESULTADO_ENSAIO_HERMETICO_BN_v413.json")
rh = U.ler_json(RH)
cn_p = sorted(glob.glob(os.path.join(HERE, "ensaio_hermetico", "saidas_*", "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v413.json")))[-1]
cn = U.ler_json(cn_p)
a4 = next(t for t in rh["testes"] if t["teste"].startswith("A4 "))
negs_gate = [t for t in rh["testes"] if t["teste"].startswith(("E1 ", "E2 ", "E4 ", "E5 ", "E6 ", "E4b ", "E4c ", "E7 "))]
PREF_REV = ("E7 ", "E8 ", "B0a ", "B0b ", "B1c ", "B3c ", "B5a ", "B5b ", "B5c ", "B6c ", "B6d ", "E4b ", "E4c ", "D4b ", "D5 ", "F0 ", "F1 ")
rev_t = [{"teste": t["teste"][:170], "ok": t["ok"]} for t in rh["testes"] if t["teste"].startswith(PREF_REV) or "(revisao B10)" in t["teste"]]
f1 = next((t for t in rh["testes"] if t["teste"].startswith("F1 ")), None)
seco = sorted(glob.glob(os.path.join(HERE, "ensaio_a_seco", "RESULTADO_ENSAIO_A_SECO_POS_SELO_v413_*.json")))
seco_ult = U.ler_json(seco[-1]) if seco else {}
testes = {"hermeticos": {"resultado": RH, "sha16": s16(RH), "n": rh["n_testes"], "passaram": rh["n_passaram"], "negativos_nomeados": rh["n_negativos"], "negativos_de_portao_nos_executores": len(negs_gate),
                         "rodadas_anteriores": "ensaio_hermetico\\rodadas_anteriores (rodada 1: 68/70, um defeito do proprio teste C3 e duas sobras nos scripts do servico, a data com ano e uma mencao a mais da variavel, corrigidas na causa; "
                                               "rodada 2: 70/70 antes dos testes dos .sh; rodada 3: 76/76, o molde que a revisao leu; rodada 4: 94/95 depois da revisao, a falha foi da EXPECTATIVA do teste novo B1c, que previa uma "
                                               "so' falha do mundo falso e ha' duas por desenho (o sandbox vb99 e a porta de ensaio contra o recibo da v411 copiado do real, 18777): o teste passou a conferir cada uma pela causa)"},
          "testes_da_revisao": {"n": len(rev_t), "passaram": sum(1 for t in rev_t if t["ok"]), "lista": rev_t},
          "ensaio_a_seco_auto_teste": {"teste_hermetico_F1_ok": (f1 or {}).get("ok"), "resultado": seco[-1] if seco else None, "sha16": s16(seco[-1]) if seco else None, "sem_bateria": seco_ult.get("sem_bateria"),
                                       "ok": seco_ult.get("n_ok"), "falhas": seco_ult.get("n_falhas"), "nao_executadas": seco_ult.get("n_nao_executadas"), "mundo_apagado": seco_ult.get("mundo_apagado"),
                                       "sandbox_do_esboco_apagado": seco_ult.get("sandbox_do_esboco_apagado"), "processos_vivos_no_fim": seco_ult.get("processos_vivos_no_fim"),
                                       "nota": "entradas FALSAS (o mundo falso do hermetico), sem bateria: prova o mundo, o pre-selo do salto, o passo 10 pelo esboco real em --sandbox, o b3_recibo, a conferencia A, a autorizacao, "
                                               "a parada e o evento; o APLICAR, o religamento e o fechar ficam para o ensaio a seco real, depois do selo"},
          "controles_do_conferir_do_salto": {"n": 9, "como_esperado": 9 if a4["ok"] else None, "fonte": "teste A4 (copia, mundo falso, esboco R3.6 real)"},
          "controle_negativo_do_conferidor": {"resultado": cn_p, "sha16": s16(cn_p), "controle_sem_mutacao_rc": cn["controle_sem_mutacao"]["rc"], "mutacoes": len(cn["mutacoes"]),
                                              "pegas": sum(1 for v in cn["resultados"].values() if v["pegou"]), "toda_mutacao_foi_pega": cn["toda_mutacao_foi_pega"]}}
# os artefatos do pre-selo ja gerados (prazo N1) e o estado de agora (so' leitura)
art = {}
for p_ in (DBN.CADEIA_ARQ, DBN.PINO_CADEIA_ARQ) + tuple(sorted(glob.glob(os.path.join(DBN.BATERIA_V412_DIR, "*.json")))):
    art[os.path.relpath(p_, DBN.V413)] = {"sha16": s16(p_), "bytes": os.path.getsize(p_)}
selo = U.ler_json(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
um_nos = U.sha256_arquivo(os.path.join(DBN.NOS, "um.py"))
restos = [os.path.relpath(p_, DBN.V413) for p_ in (os.path.join(DBN.OUTB_PRE_SELO, "etapa1_stdout.txt"), os.path.join(DBN.OUTB_PRE_SELO, "ensaio_1"), DBN.PINO_RECIBO_PRE_SELO_ARQ, DBN.PROVA_PRODUCAO_ARQ, DBN.PINOS_BN_ARQ) if os.path.exists(p_)]
agora = {"nos": {"um_version": selo.get("um_version"), "selo_pina_o_um_py": (selo.get("sha256") or {}).get("um.py") == um_nos, "um_py_sha16": um_nos[:16]},
         "bancada": DBN.BANCADA_PINA_HOJE, "sandbox_curto_existe": os.path.exists(DBN.SANDBOX_CURTO), "sandbox_das_guardas_da_etapa_2_vb25_existe": os.path.exists(os.path.join("C:" + os.sep, "t", "vb25")),
         "sandboxes_de_teste_vb98_vb99_existem": [os.path.exists(os.path.join("C:" + os.sep, "t", x)) for x in ("vb98", "vb99")], "restos_de_rodada_em_v413": restos,
         "aplicado_ao_canonico_da_v413": sorted(os.path.basename(x) for x in glob.glob(os.path.join(DBN.V413, "APLICADO_AO_CANONICO_*.json")))}
pronto_para = (agora["nos"]["um_version"] == "v412" and agora["nos"]["selo_pina_o_um_py"] and agora["bancada"]["version"] == "v411" and not agora["sandbox_curto_existe"] and not restos and not agora["aplicado_ao_canonico_da_v413"])
out = {"contrato": "PRONTO_BN_v413", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "ordem": {"path": os.path.join(HERE, "ORDEM_BN_v413.md"), "sha16": s16(os.path.join(HERE, "ORDEM_BN_v413.md"))},
       "plano": {"path": os.path.join(HERE, "DIAGNOSTICO_E_PLANO_BN_v413.md"), "sha16": s16(os.path.join(HERE, "DIAGNOSTICO_E_PLANO_BN_v413.md"))},
       "scripts": scripts, "pendencias": P, "medida_permanente": medida, "revisao_independente_aplicada": REV, "testes": testes, "artefatos_do_pre_selo_gerados": art, "estado_de_agora_para_o_pre_selo": agora,
       "pronto_para_rodar_o_pre_selo_quando_a_gerencia_mandar": pronto_para,
       "falta_para_rodar_o_pre_selo": ["a ordem da gerencia, com o Nos AINDA na v412 (antes do APLICADO_AO_CANONICO da v413), de preferencia com folga antes da instalacao (revisao M3 i: a bateria da v412 roda ali pela primeira vez)",
                                       "imediatamente antes (revisao M1): a Etapa 2 parada (nenhuma guarda estatica nem controle negativo em curso) e C:\\t\\vb24 inexistente (o runner recusa se existir); durante as fotos, "
                                       "nada escrevendo no Nos nem no kernel irmao (linhagem, desenho, memoria, servidor Lean)",
                                       "o comando (revisao M2: com run_in_background ou com timeout de 600000 ms na ferramenta Bash; o veredito se le no arquivo): "
                                       "cd \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada\" && mkdir -p ../bateria_pre_selo && sh ./rodar_bn_pre_selo_v413.sh > ../bateria_pre_selo/bn_pre_selo_out_v413.txt 2>&1; echo \"RC_BN=$?\"",
                                       "RC_BN=0 e a ultima linha sem FALHOU; com RC 9 nada rodou (portao); com RC 1 ler o arquivo: um negativo e' parede medida, nada foi gravado na Bancada, e se refaz enquanto o Nos estiver na v412 "
                                       "(tirar antes as saidas desta rodada e o vb24)",
                                       "nada mais de insumo: a cadeia v411 -> v412 e a bateria da v412 ja estao gravadas e pinadas (prazo N1)"],
       "falta_depois_do_pre_selo_e_antes_do_APLICAR": ["diff_e_pinos_bn_v413.py --delta <o delta principal da v413, da Etapa 2> ate' pendentes == [] (2.7); p00_precondicoes_bn_v413.py",
                                                       "acrescentar ao CONTRATO_v413_R1.md secao 7, ou ao pedido ao LAR (revisao M4, ato da gerencia): «e, ate' o fechamento do B21, tambem v413\\base_v412\\, v412\\base_v411\\, "
                                                       "v413\\cadeia_de_selos_v411_v412\\, v413\\bateria_v412_pre_selo\\, v413\\bateria_pre_selo\\ e C:\\t\\k413c\\arvore»",
                                                       "as guardas estaticas da v413 (Etapa 2) em C:\\t\\vb25, nunca vb24 (revisao M1; aviso da gerencia)",
                                                       "depois do selo e antes do pos-selo real (revisao M3): o ensaio a seco do pos-selo com a v413 selada e a bateria, em segundo plano: cd \"/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada\" && "
                                                       "/c/Python314/python.exe -I -B -X utf8 ensaio_a_seco_pos_selo_v413.py --mundo <pasta nova no scratchpad, fora de work> < /dev/null > <scratchpad>/seco_v413_out.txt 2>&1; echo \"RC_SECO=$?\" "
                                                       "(os padroes sao os caminhos reais, so' lidos; grava so' no mundo, em C:\\t\\vb98 e em bancada\\ensaio_a_seco; espera-se 15 etapas OK e 0 falhas)",
                                                       "o pos-selo real (bn_v413.sh): os passos 10 e 10b com run_in_background ou timeout de 600000 ms (revisao M2); a autorizacao pelo montar_autorizacao_v413.py (B5); depois do 11, o aviso_f06_v413.py (B4)"],
       "para_o_plano_da_v414": ["revisao B12: fixar tambem a carga do delta_bn dentro do delta_v413 (nao so' a linha do BANCADA_PINA_HOJE); depois do B22, importar o delta_v413 quebra"],
       "desvios": ["no comeco desta tarefa, duas leituras de JSON foram feitas com `python -c` (so' leitura, sem gravar nada), antes de eu reparar que a ordem proibe; dali em diante, so' scripts gravados",
                   "a conferencia A e a sentinela contra a Bancada REAL (porta fechada, permitido pela ordem) gravaram os recibos de teste em ensaio_hermetico\\saidas_*, nao em bn_pos_selo\\saude",
                   "o teste D5 leu o quadro e as falas REAIS (so' leitura) pelo montar_autorizacao copiado, gravando so' numa pasta temporaria do scratchpad",
                   "o auto-teste do ensaio a seco (F1) gravou o resultado dele em bancada\\ensaio_a_seco (entradas falsas, sem bateria; o mundo e o C:\\t\\vb98 foram apagados)",
                   "a memoria ACOM nao foi inscrita (a ordem: memoria, Atlas, ACOM e Mapa nao se escrevem; a gerencia registra)"],
       "examinado_para_o_mapa": {"consultado_antes": "rotas.py consultar \"bancada\"; rota bancada.b21_v412.revisao_e_decisao_19nov (seq 2174)", "olhou_dados": False,
                                 "nao_refazer": "a cadeia v411 -> v412 e a bateria da v412 (geradas e pinadas); o molde do B(n) do salto, a revisao aplicada (B1-B13, M1-M4) e os testes hermeticos (%d/%d)" % (rh["n_passaram"], rh["n_testes"]),
                                 "achado": "o NTFS atualiza com atraso o mtime de pasta que o scandir le: a fotografia de uma arvore recem-escrita pode acusar producao alterada (falso negativo, fail-closed); a producao real esta' parada ha' dias",
                                 "achado_da_revisao": "o esboco R3.6 em pos_selo ensaio do salto (--sandbox --sem-bateria) devolve o veredito exato e o b3_recibo aceita o recibo dele (B0a/B0b): o formato real confere com o que o molde le"},
       "nada_foi": "ligado, parado ou tocado no servico; gravado na Bancada, no Nos, na v412, em C:\\t\\k412c ou k413c, no quadro; a placa de video nao foi usada; o treino nao foi tocado",
       "escopo": "identidade e testes sinteticos; NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
dest = os.path.join(HERE, "PRONTO_BN_v413.json")
dados = (json.dumps(out, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(dest):
    antes = open(dest, "rb").read()
    bk = dest + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(bk, "xb") as fh:
        fh.write(antes)
with open(dest + ".tmp", "wb") as fh:
    fh.write(dados)
assert os.path.getsize(dest + ".tmp") == len(dados)
os.replace(dest + ".tmp", dest)
print(dest, s16(dest), "| scripts", len(scripts), "| hermeticos %d/%d" % (rh["n_passaram"], rh["n_testes"]), "| da revisao %d/%d" % (testes["testes_da_revisao"]["passaram"], testes["testes_da_revisao"]["n"]),
      "| mutacoes %d/%d" % (testes["controle_negativo_do_conferidor"]["pegas"], len(cn["mutacoes"])), "| ensaio a seco (auto-teste): ok %s, falhas %s, nao executadas %s" % (seco_ult.get("n_ok"), seco_ult.get("n_falhas"), seco_ult.get("n_nao_executadas")),
      "| pronto para o pre-selo:", pronto_para)
