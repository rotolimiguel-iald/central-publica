# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a candidata PonteCookLevin R0 (a ponte de Cook-Levin, construida pela gerencia
por ordem do operador) e gera o pedido de revisao FINAL ao Codex (um so' arquivo; o operador cola). (0) a fala do
operador por bytes; (1) recibo da compilacao conferido; (2) o pedido ao Codex; (3) RESULTADO no Mapa (rota 2201);
(4) transicao ACOM (revisao lida do project); (5) AO LADO no topico da v413; (6) decimo registro de 20/11 no Atlas.
Backups de bytes antes de tocar memoria; escrita por temporario; nada instalado, nada no kernel, no um.py nem no N0."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
C1 = W.parent
V413 = C1.parent
CEN = V413.parents[2]
CUNH = CEN / "work" / "cunhagens_13out"
FALA = CUNH / ("OPERADOR_20nov_perfeito_e_isso_mesmo_faca_vc_mesmo_com_seus_agentes_nao_delegue_a_modelo_menor_depois_so"
               "_a_revisao_do_codex_ao_final_verbatim.txt")
TEXTO = ("perfeito é isso mesmo, como meus créditos do kimi acabaram vc precisa fazer tudo e meus créditos com vc são mais "
         "que suficientes, portanto, não delegue a um modelo menor, faça vc mesmo com seus agentes, é exatamente isso que "
         "vc falou, depois fica apenas a revisão do codex ao final\n")
FALA_ANT = CUNH / ("OPERADOR_20nov_o_que_falta_para_fechar_a_ponte_cook_levin_a_pergunta_nao_e_a_que_vc_formulou_a_de_clay"
                   "_esta_respondida_verbatim.txt")
PONTE, CONF, LOG = W / "PonteCookLevin.lean", W / "build" / "CONFERENCIA.json", W / "build" / "PonteCookLevin.log"
COMP = W / "compilar.py"
CONF_B = V413 / "conferencia_c1_codex" / "k412c" / "build"
REV = V413 / "revisao_codex"
ADENDO7 = REV / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R7_TRINITY_R2_OPERADOR_20nov.md"
PARECER = REV / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
PEDIDO = REV / "PEDIDO_DE_REVISAO_FINAL_AO_CODEX_v413_PONTE_COOK_LEVIN_TRINITY_R7_OPERADOR_R2_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


# (0) a fala por bytes ----------------------------------------------------------------------------------------------
d = TEXTO.encode("utf-8")
if FALA.exists():
    assert FALA.read_bytes() == d, "fala ja existe com outro conteudo"
else:
    grava(FALA, d)
print("(0) fala sha16 %s (%d B)" % (s16(FALA), len(d)))

# (1) o recibo da compilacao -------------------------------------------------------------------------------------------
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(PONTE) and conf["pedidos"] == conf["relatorios"] == 22
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0 and conf["rc"] == 0
NT = conf["relatorios"]
fonte = PONTE.read_text(encoding="utf-8")
for nome in ("def CookLevin", "def EmNP", "def EmPComUmaLeitura", "theorem a_ponte_cook_levin", "theorem sat_em_np",
             "theorem a_leitura_acha_a_solucao", "theorem o_psion_le_a_soma_normalizada"):
    assert nome in fonte, nome
print("(1) PonteCookLevin R0 sha16 %s | %d de %d no trio | RC 0 | avisos 0" % (s16(PONTE), NT, conf["pedidos"]))

# (2) o pedido de revisao final ao Codex -------------------------------------------------------------------------------
texto = """# Pedido de revisão final ao Codex (v413): a Ponte Cook–Levin, a Trinity R7 e o Operador R2, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador; a gerência não envia ordem ao Codex. É a revisão final da frente de Cook–Levin da v413. Para colar, substitui o adendo R7, que fica como registro e é lido daqui (item 2).

## O que revisar

1. **A candidata da gerência `TGLExt.PonteCookLevin`, R0**, em `{ponte}` (sha16 `{sp}`). Compilada na caixa da v412 com {nt} de {nt} relatórios de axiomas no trio e nenhum aviso (`{conf}`, sha16 `{sc}`). Ela importa a sua máquina TM2 do verificador (`SimCompleta`), a sua leitura β (`EntregaBeta` e dependências) e as pedras do Kimi de que elas dependem, pelos .olean da conferência da gerência (`{confb}`); do kernel, importa `TGLExt.TraducaoTuring` e `TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1`. Confira, em especial:
   - **as definições da §4** (`juntaNaFita`, `EmNP`, `ReduzASAT`, `CookLevin`, `EmPComUmaLeitura`): codificações fixas, certificado binário, nenhum alvo vácuo. O ponto crítico é que a hipótese nomeada `CookLevin` seja VERDADEIRA como está escrita; se fosse falsa, todo teorema que a usa seria vácuo. O argumento da gerência: o verificador TM2 fatora pela codificação; a linguagem de palavras correspondente, com o verificador cronometrado, está em NP clássico; Cook–Levin (1971, 1973) dá a redução; a simulação polinomial entre máquinas de fita e de pilhas e a troca polinomial para a fita unária das fórmulas a levam à máquina TM2 do Mathlib, com a parada formal de `haltList`. Diga se concorda ou aponte o furo;
   - **a fiação da §1**: `a_particao_e_a_soma_beta` (a partição do kernel em s = k·(−ln(1−β)) é a sua `weightedSum`); `o_psion_le_a_soma_normalizada` (o leitor do kernel lê exatamente a sua `normalizedSum`, por `TraducaoTuring.o_psion_le_z`); `a_resposta_tem_a_precisao` (o numerador pelo piso cumpre a sua hipótese de precisão); `uma_leitura_do_psion_decide_SAT`;
   - **§2 e §3**: `paraCNF` (os índices da fórmula crua como Nomes de `Fin N`, com N o comprimento da fita da fórmula); `sat_cru_sse_sat`; e o `oraculo` como função da palavra escrita (`o_oraculo_le_a_fita`, pelo seu `decodificaEntrada`);
   - **§5**: `sat_em_np` usa `SimTM2.verificacao_tm2_polinomial` com a codificação idêntica (`a_juncao_e_a_entrada_do_verificador`); `sat_com_uma_leitura` usa a identidade do Mathlib; `a_ponte_cook_levin`; a síntese `a_ponte`, no certificado de Fock físico do kernel;
   - **§6**: `a_leitura_acha_a_solucao` liga o leitor do kernel à sua `all_labels_from_beta`; a conta é em leituras e letras, não em passos TM2;
   - **as docstrings**: nenhuma pode dizer mais do que o enunciado. Devem dizer que, na língua clássica, a classe «com uma leitura» assim definida é o fecho de SAT por redução polinomial (coincide com NP, por Cook–Levin); que o custo da própria leitura não é contado em passos de fita (é um oráculo); que a máquina sem leitor não é tocada; e que a E28 continua.
2. **A Trinity R7 e o Operador R2**: os itens do adendo R7 (`{adendo}`, sha16 `{sa}`), se ainda não os revisou.

## O que fica fora

Quem constrói não aprova: os seus próprios módulos (a máquina TM2 do verificador, a simulação e a leitura β) ficam fora desta revisão; a gerência os conferiu na caixa da v412. As pedras do Kimi e a errata de `OResumoEPsiBit` já têm veredito no seu parecer consolidado (`{parecer}`, sha16 `{spar}`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\\t\\k412c\\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o build da conferência da gerência (ou o seu próprio build dos mesmos módulos). O compilador da gerência: `{comp}` (sha16 `{scomp}`).
- **Os axiomas:** leia os relatórios na saída inteira. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado contra a docstring e o nome. Procure alvo vácuo, hipótese não usada e docstring que diga mais do que o enunciado prova.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate. Consulte o Mapa de Rotas antes e registre depois, numa rota própria.

## O que devolver

- Para cada item, um veredito (APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA), com o motivo em até três linhas.
- Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada fonte lida e de cada log.
""".format(ponte=PONTE, sp=s16(PONTE), nt=NT, conf=CONF, sc=s16(CONF), confb=CONF_B, adendo=ADENDO7, sa=s16(ADENDO7),
           parecer=PARECER, spar=s16(PARECER), comp=COMP, scomp=s16(COMP))
grava(PEDIDO, texto.encode("utf-8"))
print("(2) pedido final ao Codex: %s sha16 %s" % (PEDIDO.name, s16(PEDIDO)))

# (3) Mapa: RESULTADO na rota 2201 ----------------------------------------------------------------------------------------
res = {
    "tipo": "RESULTADO", "rota_id": "kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": ("a Ponte Cook-Levin construida (candidata R0 da gerencia; nome das palavras do operador): NP na maquina "
               "padrao decidido em tempo polinomial com uma leitura do leitor da TGL, com Cook-Levin nomeado"),
    "resultado": (
        "TGLExt.PonteCookLevin R0 (sha16 %s): %d de %d relatorios no trio, RC 0, sem aviso, na caixa da v412. §1 a fiacao: "
        "a particao do kernel em s = k·(-ln(1-beta)) e' a weightedSum da leitura beta; o leitor do psion le' exatamente "
        "a normalizedSum (o_psion_le_a_soma_normalizada, por o_psion_le_z); o numerador diadico pelo piso cumpre a "
        "precisao 1/(4·2^n) e decide SAT (uma_leitura_do_psion_decide_SAT); cabe em n+3 bits. §2 a formula crua e a sua "
        "CNF sobre os Nomes da fita (sat_cru_sse_sat). §3 o oraculo le' a palavra escrita (o_oraculo_le_a_fita). §4 na "
        "lingua do Mathlib: EmNP (verificador TM2 sobre a juncao fixa entrada|divisoria|certificado binario, certificado "
        "polinomial), ReduzASAT, CookLevin (hipotese nomeada), EmPComUmaLeitura. §5 sat_em_np (pela maquina TM2 do "
        "verificador do Codex, codificacao identica), sat_com_uma_leitura (identidade do Mathlib), a_ponte_cook_levin "
        "(CookLevin implica: todo problema em EmNP esta' em EmPComUmaLeitura) e a sintese a_ponte no certificado de Fock "
        "fisico do kernel, para todo acoplamento beta. §6 a_leitura_acha_a_solucao (reconstrucao com no maximo letras+1 "
        "leituras, contada em leituras e letras).") % (s16(PONTE), NT, NT),
    "veredito": ("A_PONTE_COOK_LEVIN_R0__22_DE_22_NO_TRIO__NP_EM_P_COM_UMA_LEITURA_DO_LEITOR_DA_TGL_COM_COOK_LEVIN_"
                 "NOMEADO__SAT_EM_NP_NA_MAQUINA_PADRAO__A_LEITURA_ACHA_A_SOLUCAO__CANDIDATA_NAO_INSTALADA"),
    "estatuto": ("REAL (os termos, no sandbox da v412); KNOWN (Cook 1971, Levin 1973, a simulacao polinomial entre maquinas "
                 "de fita e de pilhas: o conteudo da hipotese nomeada CookLevin; Baker-Gill-Solovay 1975; Knill-Laflamme "
                 "1998); OPEN (a maquina sem leitor)"),
    "status": "EXAMINADA", "olhou_dados": False,
    "defeito": ("na lingua classica, a classe com uma leitura assim definida e' o fecho de SAT por reducao polinomial "
                "(coincide com NP, por Cook-Levin): dado o oraculo, o resultado e' imediato; o custo da propria leitura "
                "nao e' contado em passos TM2 (oraculo); a maquina TM2 que monta as consultas da reconstrucao nao esta' "
                "construida, e a composicao de maquinas TM2 segue proof_wanted no Mathlib; Cook-Levin entra por citacao; "
                "a maquina sem leitor nao e' tocada; a E28 continua; quem constroi nao aprova: falta a revisao do Codex"),
    "nao_refazer": ("nao refazer a fiacao, as definicoes da §4 nem SAT em NP; nao tentar provar Cook-Levin dentro desta "
                    "pedra (e' citacao; formaliza-lo no Mathlib e' projeto a' parte)"),
    "proximo_passo": ("a revisao final do Codex (pedido pronto para o operador colar: %s); depois, a instalacao na v413 "
                      "junto com os modulos do Codex de que ela depende (a maquina TM2 do verificador e a leitura beta), "
                      "com nomes TGLExt e o texto condensado") % PEDIDO.name,
    "onde": str(PONTE),
    "artefatos": [str(PONTE), str(CONF), str(LOG), str(COMP), str(PEDIDO), str(FALA), str(FALA_ANT)],
    "refs": ["kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov",
             "kernel.traducao_cook_levin.conferencia_entrega_codex_k412c_20nov",
             "kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov"],
    "nota": "construida pela gerencia c1 por ordem do operador (20/11, fala por bytes); nome provisorio: PonteCookLevin",
}
pj = W / "resultado_ponte_r0_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL,
                   timeout=180)
out = r.stdout.decode("utf-8", "replace")
print("(3) Mapa RESULTADO rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]

# (4) ACOM ----------------------------------------------------------------------------------------------------------
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


def acha_revisao(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "revision" and isinstance(v, int):
                return v
            x = acha_revisao(v)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = acha_revisao(v)
            if x is not None:
                return x
    return None


rc, o = acom({"operation": "project", "reference": REF})
proj = json.loads(o.decode("utf-8"))
assert proj.get("ok") is True
rev = acha_revisao(proj)
assert isinstance(rev, int)
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d348-ponte-cook-levin-r0",
       "changes": {"records": [
           {"id": "c1-20nov-d348-ponte-cook-levin-r0", "kind": "fact", "statute": "REAL",
            "text": ("A Ponte Cook-Levin (candidata TGLExt.PonteCookLevin R0, construida pela gerencia por ordem do autor; "
                     "22 de 22 no trio na caixa da v412): o leitor do kernel le' exatamente a soma da leitura beta e, pelo "
                     "piso, decide SAT; na lingua do Mathlib, SAT esta' em NP pela maquina TM2 do verificador, e com "
                     "Cook-Levin (hipotese nomeada, KNOWN) todo problema em NP e' decidido em tempo polinomial com uma "
                     "leitura do leitor da TGL, no certificado de Fock fisico do kernel; a leitura acha a solucao com no "
                     "maximo letras+1 leituras. Nao instalada; falta a revisao final do Codex."),
            "sources": [src(PONTE), src(CONF), src(PEDIDO), src(FALA)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__PONTE_COOK_LEVIN_R0_CONSTRUIDA__REVISAO_FINAL_DO_CODEX_PRONTA",
                    "next_action": ("(1) o autor cola no Codex o pedido de revisao final (%s), que cobre a Ponte "
                                    "Cook-Levin, a Trinity R7 e o Operador R2; (2) o autor confirma o nome da pedra "
                                    "(provisorio: PonteCookLevin); (3) o autor decide as pedras do Kimi (a gerencia "
                                    "recomenda instalar as tres aprovadas com ressalvas, com texto ajustado, e deixar "
                                    "APonteDeCookLevin fora); (4) depois da revisao, a gerencia prepara a instalacao na "
                                    "v413 (versoes condensadas; os modulos do Codex de que a ponte depende; errata da "
                                    "docstring de OResumoEPsiBit); (5) seguem com o autor: o teste do estudo da memoria e o "
                                    "t* do dephasing.") % PEDIDO.name}}}
(W / "acom_c1_20261120_d348_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                  encoding="utf-8")
rc, ot = acom(req)
(W / "acom_c1_20261120_d348_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(4) ACOM project rev %d | transition rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t,
                                                                   t[t.find('"revision"'):][:20]))
assert '"ok": true' in t


# (5) e (6): memoria (backup de bytes antes) --------------------------------------------------------------------------
def acrescenta(alvo, marca, texto, marca_fim=None):
    a = alvo.read_bytes()
    assert marca.encode() not in a
    if marca_fim:
        assert marca_fim.encode() in a and len(a) - a.rfind(marca_fim.encode()) < 800
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + fim + texto.replace("\n", fim.decode()).encode("utf-8") + fim
    bk = alvo.with_name(alvo.name + ".bak_" + TS + "_c1")
    bk.write_bytes(a)
    assert bk.read_bytes() == a
    tmp = alvo.with_name(alvo.name + ".tmp_c1")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(alvo)
    assert alvo.read_bytes() == novo and len(novo) > len(a)
    return len(a), len(novo), bk.name


T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
mt = "<!-- ao_lado_20nov_ponte_cook_levin_r0 -->"
tt = ("**AO LADO (20/11/2026, gerência c1): a Ponte Cook–Levin construída (R0).** A fala (bytes, sha16 `%s`): «perfeito "
      "é isso mesmo, … faça vc mesmo com seus agentes, é exatamente isso que vc falou, depois fica apenas a revisão do "
      "codex ao final». A candidata `TGLExt.PonteCookLevin` R0 (`work\\cadeia_de_selo\\v413\\candidatas_c1\\"
      "R0_ponte_cook_levin\\`, sha16 `%s`; %d de %d no trio na caixa da v412; nome provisório, das palavras dele): o "
      "leitor do kernel lê exatamente a soma da leitura β e, pelo piso, decide SAT; na língua do Mathlib, SAT está em NP "
      "pela máquina TM2 do verificador (Codex), e, com Cook–Levin como hipótese nomeada, todo problema em NP é decidido "
      "em tempo polinomial com uma leitura do leitor da TGL, no certificado de Fock físico do kernel; a leitura acha a "
      "solução com no máximo letras+1 leituras. Na língua clássica, a classe «com uma leitura» é o fecho de SAT por "
      "redução polinomial; o custo da leitura não é contado em passos de fita; a máquina sem leitor não é tocada. Pedido "
      "de revisão final ao Codex, para o operador colar: `work\\cadeia_de_selo\\v413\\revisao_codex\\%s` (cobre também a "
      "Trinity R7 e o Operador R2). Mapa: RESULTADO na rota `kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_"
      "leitor_20nov`.\n%s") % (s16(FALA), s16(PONTE), NT, NT, PEDIDO.name, mt)
print("(5) topico: %d -> %d B | backup %s" % acrescenta(T, mt, tt))

A = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
ma = "<!-- registro_20nov_a_ponte_cook_levin_r0 -->"
ta = ("### Registro de 20/11/2026, décimo (gerência c1) — a Ponte Cook–Levin (candidata R0)\n\n"
      "**O termo (candidata `TGLExt.PonteCookLevin`, R0, não instalada; nome provisório, das palavras do operador) [REAL "
      "no sandbox]:** no tempo pago de k passos do relógio β, a partição do kernel é a soma ponderada da leitura β "
      "(`a_particao_e_a_soma_beta`); o leitor do psíon lê exatamente a soma normalizada (`o_psion_le_a_soma_normalizada`, "
      "por `TraducaoTuring.o_psion_le_z`); o numerador diádico da leitura, em n+3 bits, decide SAT "
      "(`uma_leitura_do_psion_decide_SAT`). Na língua do Mathlib (`Turing.TM2ComputableInPolyTime`): NP com verificador "
      "TM2 e certificado binário (`EmNP`), a redução a SAT (`ReduzASAT`), Cook–Levin como hipótese nomeada (`CookLevin`) e "
      "«decidido em tempo polinomial com uma leitura do leitor da TGL» (`EmPComUmaLeitura`). Provado: SAT em NP pela "
      "máquina TM2 do verificador (`sat_em_np`); SAT com uma leitura (`sat_com_uma_leitura`); com Cook–Levin, todo "
      "problema em NP com uma leitura (`a_ponte_cook_levin`; síntese `a_ponte`, no certificado de Fock físico do kernel); "
      "a leitura acha a solução com no máximo letras+1 leituras (`a_leitura_acha_a_solucao`). Compila na caixa da v412 "
      "com %d de %d relatórios no trio.\n\n"
      "**O que o termo não diz:** Cook–Levin não é provado aqui (citação [KNOWN]: Cook 1971, Levin 1973, com a simulação "
      "polinomial entre máquinas de fita e de pilhas). Na língua clássica, a classe «com uma leitura» é o fecho de SAT por "
      "redução polinomial (coincide com NP); o custo da própria leitura não é contado em passos de fita (é um oráculo); a "
      "máquina sem leitor não é tocada (Baker–Gill–Solovay 1975 [KNOWN]); que um dispositivo físico leia num ato é física "
      "(Knill–Laflamme 1998 [KNOWN]). A E28 continua.\n\n"
      "Estatuto: [REAL no sandbox] os termos; [KNOWN] Cook–Levin, nomeado; [OPEN] a máquina sem leitor. Validade no "
      "kernel não é creditação; o gate não se move.\n%s") % (NT, NT, ma)
print("(6) Atlas: %d -> %d B | backup %s" % acrescenta(A, ma, ta, "<!-- registro_20nov_o_alvo_da_ponte_cook_levin -->"))
