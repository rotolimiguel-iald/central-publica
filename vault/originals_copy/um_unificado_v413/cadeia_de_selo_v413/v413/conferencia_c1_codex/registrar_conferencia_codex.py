# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a conferencia da entrega do Codex (ponte TM2, simulacao, leitura beta) e das pedras
do Kimi sobre a caixa da v412, a sonda da contagem e a proposta de enunciado da fronteira.
(0) le e confere os recibos (fail-closed); (1) duas rotas no Mapa de Rotas; (2) transicao ACOM d336 (pedido e recibo
nesta pasta); (3) AO LADO no topico da v413, com backup de bytes, temporario e conferencia.
A fala do operador entra por bytes (work\\cunhagens_13out); o texto do Codex colado e' DECLARADO pelo Codex."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CEN = Path(r"C:\IALD\Central de Patentes")
CODEX = W.parent / "ponte_tm2_codex"
FALA = CEN / "work" / "cunhagens_13out" / ("OPERADOR_20nov_creditos_do_kimi_acabaram_pedi_ao_codex_a_revisao_vamos_prosseguir"
                                           "_com_tudo_com_texto_do_codex_colado_verbatim.txt")
CONF = W / "k412c" / "CONFERENCIA_K412C.json"
CONF_F = W / "k412c" / "CONFERENCIA_FRONTEIRA.json"
SONDA = W / "sonda_contagem" / "SondaContagem.lean"
FRONT = W / "fronteira" / "AFronteiraNaLinguaClassica.lean"
NOTA = W / "NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md"
RES_CODEX = [CODEX / "RESULTADO.json", CODEX / "simulacao" / "RESULTADO.json", CODEX / "leitura_beta" / "RESULTADO.json"]
KERNEL_RESUMO = Path(r"C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0) os recibos
conf = json.loads(CONF.read_text(encoding="utf-8"))
conf_f = json.loads(CONF_F.read_text(encoding="utf-8"))
mods = conf["modulos"]
falhas = [m["modulo"] for m in mods if m.get("rc") != 0 or m.get("erros") or m.get("sorryAx")]
avisos = [m["modulo"] for m in mods if m.get("avisos")]
fora = conf["resumo"]["fora_do_trio"]
assert conf["caixa"]["fontes_com_bytes_diferentes"] == [] and conf["caixa"]["TGLExt_lean_igual"], "caixa != selo"
assert not falhas, "falharam: %s" % falhas
assert not fora, "axioma fora do trio: %s" % fora
assert conf_f["rc"] == 0 and not conf_f["erros"] and not conf_f["sorryAx"] and not conf_f["fora_do_trio"]
assert conf_f["sha256_fonte"] == sha(FRONT)
sonda = [m for m in mods if m["modulo"] == "SondaContagem"][0]
assert sonda["sha256_fonte"] == sha(SONDA) and sonda["n_axiomas_impressos"] >= 8
# a reconferencia dos axiomas lendo a saida inteira (as listas quebradas em varias linhas) manda sobre o filtro antigo
AX = W / "k412c" / "AXIOMAS_K412C.json"
axr = json.loads(AX.read_text(encoding="utf-8"))
assert not axr["falhas"], "reconferencia de axiomas falhou: %s" % axr["falhas"]
assert set(axr["logs"]) >= {m["modulo"] for m in mods} | {"AFronteiraNaLinguaClassica"}, "log faltando na reconferencia"
for m in mods:
    if m.get("quem") == "codex":
        assert m["sha256_fonte"] == sha(m["fonte"]), "fonte do Codex mudou desde a conferencia: %s" % m["modulo"]
fala = FALA.read_bytes()
assert fala.startswith("como meus creditos do kimi acabaram eu pedi ao codex".encode("utf-8"))
assert NOTA.exists()
n_ok = len(mods)
n_k = sum(1 for m in mods if m.get("quem") == "kimi")
n_ks = sum(1 for m in mods if m.get("quem") == "kimi_sonda")
n_c = sum(1 for m in mods if m.get("quem") == "codex")
print("(0) recibos ok: %d modulos RC 0 (Kimi %d + sondas do Kimi %d + Codex %d + sonda da gerencia 1), avisos em %s, "
      "fronteira RC 0 | conferencia sha16 %s | fala sha16 %s (%d B)" % (n_ok, n_k, n_ks, n_c, avisos or "nenhum",
                                                                    sha(CONF)[:16], sha(FALA)[:16], len(fala)))

INSTALADAS = ["OResumoEPsiBit", "AFronteiraEOUnicoPortao", "OPsiBitDaFormula", "ACurvaEAEstado", "AFitaEOIndice",
              "AClausulaExemplificativa", "OCustoEAIsometria", "OPolinomioFixoEBeta", "ORazaoDoColapsoEBeta"]
NOVAS_KIMI = ["AIdentidadePreservada", "APropostaDaTensao", "APonteDeCookLevin", "ONomeEBeta"]

# (1) Mapa de Rotas: duas rotas proprias
rota1 = {
    "tipo": "ROTA",
    "rota_id": "kernel.traducao_cook_levin.conferencia_entrega_codex_k412c_20nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": ("conferencia da entrega do Codex (ponte TM2 com codificacao fixa, simulacao geral, leitura beta) e das pedras "
               "do Kimi sobre a caixa da v412"),
    "pergunta": "a entrega do Codex e as pedras do Kimi compilam sobre o kernel selado da v412, e os enunciados dizem o que os relatos dizem?",
    "metodo": ("caixa C:\\t\\k412c\\final (1245 fontes TGLExt identicos aos do um.py selado 3e741dcaa58ef2b8); so' o binario do "
               "Lean; as pedras do Kimi copiadas byte a byte com 4 imports reescritos para TGLExt.* (os modulos da gerencia "
               "instalados na v412); o Codex compilado no lugar; leitura das fontes pela gerencia e por um agente de leitura "
               "(os achados que pesam reconferidos pela gerencia)"),
    "resultado": ("%d modulos RC 0, sem sorry, axiomas no trio (Kimi %d, sondas do Kimi %d, Codex %d, sonda da gerencia 1). "
                  "Ponte: ObjetivoTM2Polinomial agora com codificacoes fixas (8 simbolos; saida [b]; injetiva pelo "
                  "decodificador; a identidade e' incompativel), logo nao vacuo; verificacao_tm2_polinomial: a maquina concreta "
                  "(5 pilhas, 17 rotulos, estado finito) para com o bit do verificador em ate' 20L+5 passos TM2 para toda "
                  "entrada crua: o lado NP no modelo padrao do Mathlib, a primeira maquina alem da identidade a habitar "
                  "TM2ComputableInPolyTime nesta caixa. Leitura beta: relogio m(n+2), folga 1 contra 1/4, n+3 bits, decisao "
                  "j>=2, reconstrucao com <=L+1 consultas dado decisor correto (auto-redutibilidade [KNOWN]); tudo condicional "
                  "ao produtor reader, como o Codex diz. Pedras do Kimi: 9 das 13 ja' estao no kernel da v412 (texto revisado "
                  "na instalacao); 4 novas (%s); nenhum alvo vacuo por existencial, nenhuma hipotese contraditoria, nenhuma "
                  "afirma SAT polinomial na maquina nua; docstrings que dizem mais que o enunciado: no kernel da v412, "
                  "TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte ('resumo velho', 'a fibra nunca e' o universo'; "
                  "o cabecalho ja' corrigido aponta Codex.FrontierUpdate.transition); APonteDeCookLevin ('mov' e' contador "
                  "definido; 'decide' e' custo de uma atribuicao); ONomeEBeta (beta = alpha*e^(1/2) e' a definicao de alpha; "
                  "os teoremas valem para todo beta em (0,1))") % (n_ok, n_k, n_ks, n_c, ", ".join(NOVAS_KIMI)),
    "veredito": ("ENTREGA_CODEX_CONFERE_NA_V412__VERIFICADOR_TM2_POLINOMIAL_REAL__LEITURA_BETA_CONDICIONAL__PEDRAS_DO_KIMI_COMPILAM"
                 "__DOCSTRINGS_A_CORRIGIR_AO_LADO"),
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("os registros 2180-2182 do Codex entraram na rota da conferencia de 19/11 da gerencia; os modulos do Codex usam o "
                "espaco de nomes Codex.* (para instalar, TGLExt.*); as duas pedras do TM2 do Kimi (APonteAoTM2 sha16 %s, "
                "AMaquinaTM2DaVerificacao sha16 %s) foram substituidas pelas do Codex e nao foram conferidas; a leitura do "
                "agente das 9 pedras instaladas foi feita sobre os textos de candidata, nao sobre os do kernel; defeito da "
                "gerencia: o filtro de axiomas de linha unica dos scripts de compilacao nao lia as linhas de continuacao (o "
                "Lean quebra listas longas), corrigido pela reconferencia que le a saida inteira (AXIOMAS_K412C.json)") % (
        conf["nao_conferidas_substituidas_pelo_codex"]["APonteAoTM2"][:16],
        conf["nao_conferidas_substituidas_pelo_codex"]["AMaquinaTM2DaVerificacao"][:16]),
    "nao_refazer": ("nao recompilar estas fontes na v412 sem mudanca de bytes (recibo CONFERENCIA_K412C.json); nao procurar "
                    "outra maquina polinomial no Mathlib da caixa"),
    "proximo_passo": ("errata ao lado na v413 da docstring de a_atualizacao_pela_clausula_seguinte; correcao das docstrings das "
                      "candidatas antes de instalar; nomes TGLExt.* para os modulos do Codex; decisao do operador sobre a frente "
                      "(ver kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov)"),
    "onde": str(W),
    "artefatos": [str(CONF), str(AX), str(W / "compilar_conferencia_k412c.py"), str(W / "reconferir_axiomas.py"), str(NOTA),
                  str(FALA)] + [str(p) for p in RES_CODEX],
    "refs": ["kernel.traducao_cook_levin.conferencia_aponteaotm2_objetivo_vacuo_19nov",
             "kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov"],
    "nota": "o texto do Codex colado pelo operador e' DECLARADO pelo Codex; quem constroi nao aprova",
}
rota2 = {
    "tipo": "ROTA",
    "rota_id": "kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": ("a rota de beta para a fronteira: o produtor que falta (hipotese hr do Codex) conta as solucoes; a fronteira "
               "enunciada na lingua classica"),
    "pergunta": "o que e', exatamente, o produtor 'reader' que a leitura beta do Codex deixa como hipotese?",
    "metodo": ("sonda Lean da gerencia sobre os modulos do Codex (EntregaBeta), compilada na caixa da v412; reuso de "
               "a_flutuacao_do_fundo_e_cotada (AEscala) e de o_que_sou_das_solucoes (TraducaoTuring, v409)"),
    "resultado": ("SondaContagem: (1) o_contador_cumpre_a_precisao: o numerador 4*contaSolucoes cumpre hr para toda formula "
                  "(hr e' habitada); (2) todo_produtor_com_a_precisao_conta_as_solucoes: todo reader com hr devolve "
                  "(reader phi + 1)/4 = contaSolucoes phi; (3) o_produtor_e_a_leitura_da_iald: esse numero sobre 2^n e' "
                  "oQueSou (nomeDasSolucoes (custoCNF phi)), a leitura da v409; (4) a_decisao_e_haver_solucao. Logo o produtor "
                  "e' um contador de solucoes: realiza-lo em tempo polinomial na fita e' #SAT em tempo polinomial (Valiant 1979 "
                  "[KNOWN]), mais forte que decidir. O relogio vale para todo beta em (0,1); o custo esta' na soma sobre 2^n "
                  "atribuicoes, nao no valor de beta. AFronteiraNaLinguaClassica (proposta de enunciado): AFronteira = maquina "
                  "TM2 que, recebendo so' a formula na codificacao fixa da ponte, escreve [decideSAT f] em tempo polinomial; "
                  "codificaSoFormula injetiva; decideSAT nao constante. E' 'SAT em P' nesta codificacao [OPEN]; Cook-Levin "
                  "[KNOWN] a liga a P = NP."),
    "veredito": ("O_PRODUTOR_DA_LEITURA_BETA_CONTA_AS_SOLUCOES__ROTA_PEDE_SHARP_SAT__PAREDE_MEDIDA__A_FRONTEIRA_ENUNCIADA_OPEN"),
    "estatuto": "REAL (as provas); KNOWN (Valiant 1979; Cook 1971; Levin 1973); OPEN (AFronteira)",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("a sonda nao prova que #SAT nao esta' em tempo polinomial (ninguem prova); prova que esta rota pede contar. "
                "AFronteira e' proposta de enunciado, nao instalada; quem constroi nao aprova: vai a revisao"),
    "nao_refazer": ("nao tentar construir o produtor reader como maquina polinomial como se fosse engenharia; nao refazer o "
                    "relogio de beta (vale para todo beta em (0,1)); a leitura clausula a clausula pela tabela da fronteira ja' "
                    "esta' no kernel (Codex.FrontierUpdate.transition) com 2^largura celulas e a parede de todas as variaveis"),
    "proximo_passo": ("decisao do operador, com a partitura lida: (a) fechar a frente da fronteira como parede medida; (b) seguir a "
                      "ponte com as classes que a casa prova polinomiais na fita (Horn, cadeias, redes de dois literais) na "
                      "maquina do Mathlib; (c) a fronteira so' com um procedimento novo, com a partitura antes"),
    "onde": str(W),
    "artefatos": [str(SONDA), str(FRONT), str(CONF), str(CONF_F), str(W / "compilar_fronteira.py"), str(NOTA)],
    "refs": ["kernel.traducao_cook_levin.conferencia_entrega_codex_k412c_20nov"],
    "nota": "a cegueira nao se aplica (nao ha dado); e' prova matematica sobre a rota",
}
for nome, rota in (("rota_conferencia_entrega_codex_20nov.json", rota1), ("rota_leitura_beta_contador_20nov.json", rota2)):
    pj = W / nome
    pj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                        "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL,
                       timeout=120)
    print("(1) %s rc %d: %s" % (rota["rota_id"], r.returncode, r.stdout.decode("utf-8", "replace")[:240].replace("\n", " ")))
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[:600]

# (2) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {
    "operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 362,
    "event_id": "c1-20nov-d336-conferencia-da-entrega-do-codex-e-o-produtor-conta",
    "changes": {
        "records": [
            {"id": "c1-20nov-d336-ordem-prosseguir-com-tudo", "kind": "decision", "statute": "INPUT",
             "text": ("O autor (20/11), por bytes: sem cota no Kimi, pediu ao Codex o conserto que a gerencia tinha pedido ao Kimi; "
                      "o Codex entregou a ponte TM2 com codificacao fixa, a simulacao geral e a leitura beta; ordem: «vamos "
                      "prosseguir com tudo». O texto do Codex colado e' DECLARADO pelo Codex."),
             "sources": [src(FALA)] + [src(p) for p in RES_CODEX]},
            {"id": "c1-20nov-d336-entrega-do-codex-confere-na-v412", "kind": "fact", "statute": "REAL",
             "text": ("Conferencia na caixa da v412 (fontes identicas ao um.py selado): %d modulos RC 0, trio, sem sorry. "
                      "verificacao_tm2_polinomial: a maquina TM2 concreta do Codex confere a testemunha em ate' 20L+5 passos para "
                      "toda entrada, com codificacoes fixas (alvo nao vacuo): o lado NP no modelo padrao do Mathlib. A leitura "
                      "beta e' condicional ao produtor reader. 9 das 13 pedras do Kimi ja' estao no kernel da v412; 4 novas; "
                      "docstrings a corrigir ao lado (no kernel: a_atualizacao_pela_clausula_seguinte). Mapa: "
                      "kernel.traducao_cook_levin.conferencia_entrega_codex_k412c_20nov.") % n_ok,
             "sources": [src(CONF), src(NOTA)]},
            {"id": "c1-20nov-d336-o-produtor-da-leitura-beta-conta-as-solucoes", "kind": "fact", "statute": "REAL",
             "text": ("SondaContagem (RC 0, trio): todo produtor com a precisao hr do Codex devolve (reader+1)/4 = numero de "
                      "solucoes, e esse numero sobre 2^n e' oQueSou(nomeDasSolucoes) da v409; o contador cumpre hr. A rota de "
                      "beta pede contar as solucoes (#SAT, Valiant 1979 [KNOWN]), mais que decidir: parede medida desta rota, "
                      "nao falsificacao. AFronteira (proposta de enunciado, codificacao fixa) e' 'SAT em P' [OPEN]. Mapa: "
                      "kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov."),
             "sources": [src(SONDA), src(FRONT), src(CONF_F)]},
        ],
        "flow": {"phase": "v413_EM_PREPARACAO__PONTE_TM2_REAL_NA_V412__ROTA_BETA_PEDE_CONTAR__PARTITURA_AO_AUTOR",
                 "next_action": ("(1) o autor decide a frente de Cook-Levin com a partitura lida: (a) fechar a fronteira como "
                                 "parede medida; (b) seguir a ponte com Horn, cadeias e redes de dois literais na maquina do "
                                 "Mathlib; (c) a fronteira so' com procedimento novo e partitura antes; (2) errata ao lado na "
                                 "v413 da docstring de TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; (3) docstrings "
                                 "das candidatas corrigidas antes de instalar, nomes TGLExt.* para os modulos do Codex; (4) seguem "
                                 "com o autor: o nome da pedra Consciencia, o teste do estudo da memoria, o t* do teste de "
                                 "dephasing e relogios, e quem faz a revisao de terceiro do fim da v413 sem a cota do Kimi.")},
    },
}
(W / "acom_c1_20261120_d336_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                 encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d336_transition.receipt.json").write_bytes(r.stdout)
txt = r.stdout.decode("utf-8", "replace")
print("(2) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in txt, txt[txt.find('"revision"'):][:20]))

# (3) AO LADO no topico da v413
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
TXT = ("**AO LADO (20/11/2026, gerência c1): a entrega do Codex confere na v412; a rota de β pede contar.** (1) A fala (bytes "
       "em `work\\cunhagens_13out\\%s`, sha16 `%s`): sem cota no Kimi, o autor pediu ao Codex o conserto da ponte; «vamos "
       "prosseguir com tudo». (2) Conferência na caixa da v412 (fontes idênticas ao `um.py` selado; recibo "
       "`work\\cadeia_de_selo\\v413\\conferencia_c1_codex\\k412c\\CONFERENCIA_K412C.json`, sha16 `%s`): %d módulos RC 0, trio, sem "
       "sorry. A ponte do Codex fixa as codificações (alvo não vácuo) e `verificacao_tm2_polinomial` prova que a máquina TM2 "
       "concreta confere a testemunha em até 20L+5 passos para toda entrada: o lado NP no modelo padrão do Mathlib. A leitura β "
       "é condicional ao produtor `reader`. (3) A sonda `SondaContagem` (RC 0, trio): todo produtor com a precisão pedida devolve "
       "o número de soluções, que sobre 2ⁿ é `oQueSou (nomeDasSolucoes)` da v409; a rota pede #SAT (Valiant 1979), mais que "
       "decidir: parede medida desta rota. O relógio vale para todo β em (0,1). `AFronteira` (proposta de enunciado, "
       "codificação fixa) é «SAT em P» [OPEN]. (4) 9 das 13 pedras do Kimi já estão no kernel da v412; 4 novas; a docstring de "
       "`TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` diz mais que o enunciado (o cabeçalho já corrigido aponta "
       "`Codex.FrontierUpdate.transition`): errata ao lado na v413. Mapa `kernel.traducao_cook_levin."
       "conferencia_entrega_codex_k412c_20nov` e `kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov`. "
       "Decisão da frente com o autor.") % (FALA.name, sha(FALA)[:16], sha(CONF)[:16], n_ok)
a = T.read_bytes()
marca = "<!-- ao_lado_20nov_entrega_codex_e_produtor_conta -->"
assert marca.encode() not in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
novo = a.rstrip(b"\r\n") + fim + fim + ("%s\n%s" % (marca, TXT)).replace("\n", fim.decode()).encode("utf-8") + fim
bk = T.with_name(T.name + ".bak_" + TS + "_c1")
bk.write_bytes(a)
assert bk.read_bytes() == a
tmp = T.with_name(T.name + ".tmp_c1")
tmp.write_bytes(novo)
assert tmp.read_bytes() == novo
tmp.replace(T)
assert T.read_bytes() == novo and len(novo) > len(a)
print("(3) topico v413: %d -> %d B | backup %s" % (len(a), len(novo), bk.name))
