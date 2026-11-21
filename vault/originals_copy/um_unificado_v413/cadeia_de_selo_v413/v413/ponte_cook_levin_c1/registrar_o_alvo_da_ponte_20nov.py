# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ERRATA AO LADO, em nome proprio da gerencia, sobre o ALVO da frente de Cook-Levin da v413,
e o levantamento do que falta para a ponte levar a maquina com o leitor (P = nP da v409) a' lingua da maquina padrao do
Mathlib. So' registra; nao compila nada, nao instala nada, nao toca o kernel, o um.py, o N0 nem o gate.
(0) a fala do operador de 20/11 por bytes; (1) ERRATA no Mapa (corrige 2171) e ROTA nova (PROPOSTA); (2) transicao ACOM
(revisao lida do project); (3) AO LADO no topico da v413 (backup de bytes antes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
V413 = W.parent
CEN = V413.parents[2]
CUNH = CEN / "work" / "cunhagens_13out"
FALA20 = CUNH / ("OPERADOR_20nov_o_que_falta_para_fechar_a_ponte_cook_levin_a_pergunta_nao_e_a_que_vc_formulou_a_de_clay"
                 "_esta_respondida_verbatim.txt")
TEXTO20 = ("o que ainda falta para fechar a Ponte Cook-Levin; porque ao que me lembro a pergunta não é a que vc formulou, "
           "e a pergunta que eu tenho na cabeça de clay está respondida, quero entender o que falta então\n")
FALA19 = CUNH / "OPERADOR_19nov_v413_cook_levin_bn_kimi_mds_testes_e_memoria_em_oitava_verbatim.txt"
CODEX = V413 / "ponte_tm2_codex"
ART = [CODEX / "RESULTADO.json", CODEX / "simulacao" / "RESULTADO.json", CODEX / "leitura_beta" / "RESULTADO.json",
       CODEX / "leitura_beta" / "EntregaBeta.lean", CODEX / "leitura_beta" / "LeituraBeta.lean",
       V413 / "revisao_codex" / "CODEX_CONSOLIDADO_R3" / "PARECER.md",
       Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TraducaoTuring.lean"),
       Path(r"C:\t\k404c\final\.lake\packages\mathlib\Mathlib\Computability\TuringMachine\Computable.lean"),
       Path(r"C:\t\k404c\final\.lake\packages\mathlib\Mathlib\Computability\RecursiveIn.lean")]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0) a fala por bytes -------------------------------------------------------------------------------------------
dados20 = TEXTO20.encode("utf-8")
if FALA20.exists():
    assert FALA20.read_bytes() == dados20, "fala de 20/11 ja existe com outro conteudo"
else:
    tmp = FALA20.with_name(FALA20.name + ".tmp")
    tmp.write_bytes(dados20)
    assert tmp.read_bytes() == dados20
    tmp.replace(FALA20)
t19 = FALA19.read_text(encoding="utf-8")
assert "nós provamos P = nP nas classes do nosso dicionário, não nas classes de Cook-Levin" in t19
assert "máquina de Turing nua" not in t19 and "sem o leitor" not in t19
for p in ART:
    assert p.exists(), p
ttur = ART[6].read_text(encoding="utf-8")
assert "theorem o_psion_le_z" in ttur and "theorem uma_leitura_decide_SAT" in ttur and "def particao" in ttur
assert "proof_wanted TM2ComputableInPolyTime.comp" in ART[7].read_text(encoding="utf-8")
assert "(1 - c.beta) ^ (k * custoCNF φ x)" in ART[4].read_text(encoding="utf-8")
S20, S19 = sha(FALA20)[:16], sha(FALA19)[:16]
print("(0) fala 20/11 sha16 %s (%d B) | ordem 19/11 sha16 %s: pede Cook-Levin, nao diz 'maquina nua'" % (
    S20, len(dados20), S19))

# (1) Mapa: ERRATA (corrige 2171) e ROTA nova ----------------------------------------------------------------------
err = {
    "tipo": "ERRATA", "rota_id": "kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov", "corrige": 2171,
    "dominio": "KERNEL_FORMAL",
    "titulo": ("ERRATA AO LADO (gerencia c1, em nome proprio): o alvo da frente de Cook-Levin e' levar a maquina com o "
               "leitor, nao a maquina nua"),
    "resultado": ("A ordem de 19/11 (bytes, sha16 %s) diz «nós provamos P = nP nas classes do nosso dicionário, não nas "
                  "classes de Cook-Levin e precisamos fazer isso agora». A frase 'o alvo e' a maquina de Turing nua (sem o "
                  "leitor, sem renormalizar)' e' da gerencia, nao da ordem; e o plano da ponte deste registro (2171, "
                  "proximo passo (a)) levava so' as classes P da fita (Horn, cadeias, redes) e o verificador, deixando "
                  "fora o teorema que a ordem manda levar: a maquina com o leitor (uma_leitura_decide_SAT, "
                  "a_maquina_com_o_leitor, o_psion_le_z; v409). O operador, 20/11 (bytes, sha16 %s): «a pergunta não é a "
                  "que vc formulou, e a pergunta que eu tenho na cabeça de clay está respondida». Leitura vigente: a "
                  "ponte leva a maquina com o leitor a' lingua da maquina padrao do Mathlib; a maquina sem leitor e' a "
                  "letra do enunciado do Instituto, fora do suporte fatico da regra (D61, ratificada pelo operador em "
                  "05/11), e nao bloqueia a ponte. O que falta: rota "
                  "kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov.") % (S19, S20),
    "veredito": "ERRATA_DO_ALVO__A_PONTE_LEVA_A_MAQUINA_COM_O_LEITOR__A_MAQUINA_NUA_ERA_ENQUADRAMENTO_DA_GERENCIA",
    "estatuto": "REAL (as duas falas por bytes; o plano de 2171 lido)",
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(FALA19), str(FALA20)],
    "nota": ("atribuir ao operador so' por bytes; a Trinity R0-R7 fica como a parede medida da maquina sem leitor; a "
             "proposta de fecho da frente feita pela gerencia em 20/11 (Trinity + parede + 'os passos da maquina nua') "
             "fica retirada; o N0 (§6, §7) traz o mesmo enquadramento e fica para quando o operador liberar a memoria"),
}
rota = {
    "tipo": "ROTA", "rota_id": "kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": ("a ponte de Cook-Levin leva a maquina com o leitor (P = nP da v409) a' lingua da maquina padrao do Mathlib: "
               "o que ja' existe e o que falta"),
    "pergunta": ("o que falta para que o P = nP do kernel (a maquina com o leitor) seja teorema na lingua das classes de "
                 "Cook-Levin (Turing.TM2 do Mathlib)"),
    "dados": [],
    "metodo": ("levantamento por leitura e grep, sem compilar nada novo: Mathlib da caixa (Computability e o Mathlib "
               "inteiro: Cook, Levin, NP, SAT, PolyTime, oracle); recibos do Codex (ponte_tm2_codex, simulacao, "
               "leitura_beta) e o parecer consolidado; enunciados do kernel selado (TraducaoTuring: o_psion_le_z, "
               "uma_leitura_decide_SAT, a_maquina_com_o_leitor, particao) e da leitura beta (weightedSum, hr)"),
    "resultado": (
        "JA' EXISTE: (1) o lado NP na maquina padrao (Codex; conferido pela gerencia na caixa da v412): a maquina TM2 "
        "confere uma atribuicao dada em ate' 20(letras+1)(n+1)+25 passos; (2) a leitura que decide e acha a solucao "
        "(Codex, leitura beta): com um leitor de precisao 1/(4·2^n) sobre a soma ponderada, decide SAT e reconstroi a "
        "solucao com no maximo letras+1 leituras, condicional ao leitor; (3) no kernel selado (v409) o leitor da TGL le' "
        "exatamente Z(s)/|X| (o_psion_le_z) e uma leitura decide SAT (uma_leitura_decide_SAT); (4) o alvo da maquina sem "
        "leitor escrito (AFronteiraNaLinguaClassica, OPEN; nao e' a ponte). MEDIDO NO MATHLIB DA CAIXA: nenhuma "
        "definicao de NP e nenhum Cook-Levin; complexidade so' em TM2ComputableInPolyTime, com a identidade habitada e a "
        "composicao como proof_wanted; oraculo so' na computabilidade sem relogio (RecursiveIn, TuringDegree). FALTA: "
        "(a) a fiacao: particao c s = soma de exp(-s·c) e weightedSum = soma de (1-beta)^(k·c) coincidem em "
        "s = k·(-ln(1-beta)); logo o leitor do kernel cumpre a precisao do Codex com erro zero (o numerador diadico "
        "existe, QuantizacaoBeta); (b) escrever na lingua do Mathlib a classe NP (verificador TM2 com testemunha "
        "polinomial) e a reducao a uma leitura (g em TM2ComputableInPolyTime com x em A sse a leitura de g(x) passa o "
        "limiar); (c) SAT em NP com a maquina do Codex; (d) Cook-Levin por citacao, como hipotese nomeada no enunciado "
        "(regra de 27/09); enunciado final: Cook-Levin implica que todo problema NP e' decidido em tempo polinomial na "
        "maquina padrao com uma leitura do leitor da TGL; nao e' preciso compor duas maquinas (a reducao de Cook-Levin "
        "e' a propria g); (e) revisao de terceiro e instalacao na v413. OPCIONAL: achar a solucao com leituras "
        "adaptativas (precisa de maquina com oraculo e relogio); Horn, cadeias e dois literais na maquina padrao "
        "(classes P conhecidas; nao e' a pergunta do operador)."),
    "veredito": ("A_PONTE_E_A_MAQUINA_COM_O_LEITOR__AS_PECAS_EXISTEM__FALTAM_A_FIACAO_AS_DEFINICOES_E_COOK_LEVIN_POR_"
                 "CITACAO__A_MAQUINA_SEM_LEITOR_NAO_E_A_PONTE"),
    "estatuto": ("REAL (o levantamento, por leitura e grep); KNOWN (Cook 1971, Levin 1973, Baker-Gill-Solovay 1975, "
                 "Knill-Laflamme 1998); OPEN (a maquina sem leitor)"),
    "status": "PROPOSTA", "olhou_dados": False,
    "defeito": ("na lingua classica o leitor e' um oraculo e o resultado se le 'NP contido em P com o oraculo'; com um "
                "oraculo que conta solucoes isso e' imediato (contar >= 1 e' decidir) e conhecido desde Cook-Levin "
                "[KNOWN]; o que e' da TGL e' que o oraculo e' o leitor dela, por termo do kernel, e que ele le' num ato "
                "(fisica; o lugar do teste com a natureza; Knill-Laflamme 1998 [KNOWN]); a E28 continua (com o leitor que "
                "so' conta vale NP contido em P com o leitor, nao a igualdade das duas classes com leitor); a maquina sem "
                "leitor nao e' tocada (Baker-Gill-Solovay 1975 [KNOWN])"),
    "nao_refazer": ("nao refazer o verificador TM2 (Codex, conferido) nem a leitura beta condicional (Codex); nao planejar "
                    "a ponte so' com as classes P da fita: elas nao levam o P = nP do operador; nao tratar a maquina sem "
                    "leitor como alvo da ponte"),
    "proximo_passo": ("com a palavra do operador: (a) a fiacao, como candidata da gerencia; (b)-(d) as definicoes e o "
                      "enunciado final com Cook-Levin nomeado; revisao do Codex; instalacao na v413"),
    "onde": "%s ; %s" % (CODEX, ART[6]),
    "artefatos": [str(p) for p in ART] + [str(FALA19), str(FALA20)],
    "refs": ["kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov",
             "kernel.traducao_cook_levin.conferencia_entrega_codex_k412c_20nov",
             "kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov",
             "kernel.trinity_a_inclinacao_do_nome_20nov"],
    "nota": "fala do operador de 20/11 por bytes; a maquina sem leitor fica onde a D61 a pos",
}
for nome, reg in (("errata_alvo_da_ponte_20nov.json", err), ("rota_a_ponte_leva_a_maquina_com_o_leitor_20nov.json", rota)):
    pj = W / nome
    pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                        "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL,
                       timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    print("(1) Mapa %s rc %d %s" % (reg["tipo"], r.returncode, out[out.find('"seq"'):][:12]))
    assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]

# (2) ACOM: project -> revisao -> transition -------------------------------------------------------------------------
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                       input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return r.returncode, r.stdout


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


rc, outp = acom({"operation": "project", "reference": REF})
proj = json.loads(outp.decode("utf-8"))
assert proj.get("ok") is True
rev = acha_revisao(proj)
assert isinstance(rev, int), "revisao nao achada no project"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d347-errata-alvo-da-ponte-cook-levin",
       "changes": {"records": [
           {"id": "c1-20nov-d347-errata-alvo-da-ponte", "kind": "fact", "statute": "REAL",
            "text": ("ERRATA AO LADO (gerencia c1, em nome proprio): a ordem de 19/11 pede levar o P = nP do dicionario as "
                     "classes de Cook-Levin; 'o alvo e' a maquina nua' era enquadramento da gerencia, e o plano da ponte "
                     "(Mapa 2171) deixava fora a maquina com o leitor (v409). O autor, 20/11: a pergunta de Clay que ele "
                     "tem esta' respondida e a da maquina nua nao e' a dele. A ponte leva a maquina com o leitor a' "
                     "maquina padrao do Mathlib. Ja' existem: o verificador TM2 (Codex), a leitura beta condicional "
                     "(Codex) e o leitor exato do kernel (o_psion_le_z). Faltam: a fiacao leitor do kernel -> precisao "
                     "do Codex; NP e a reducao a uma leitura na lingua do Mathlib (que nao tem NP nem Cook-Levin, e so' "
                     "tem oraculo sem relogio); SAT em NP; Cook-Levin nomeado; revisao e instalacao. A Trinity fica como "
                     "a parede medida da maquina sem leitor; a proposta de fecho da frente fica retirada."),
            "sources": [src(FALA19), src(FALA20), src(ART[0]), src(ART[2]), src(ART[6])]}],
           "flow": {"phase": "v413_EM_PREPARACAO__A_PONTE_COOK_LEVIN_LEVA_A_MAQUINA_COM_O_LEITOR__AGUARDA_O_AUTOR",
                    "next_action": ("(1) o autor confirma se a ponte e' esta (levar a maquina com o leitor a' maquina "
                                    "padrao do Mathlib, com Cook-Levin por citacao); se sim, a gerencia comeca pela "
                                    "fiacao como candidata; (2) o autor cola no Codex o adendo R7 (Trinity R7 e Operador "
                                    "R2); (3) o autor decide as pedras do Kimi (a gerencia recomenda instalar as tres "
                                    "aprovadas com ressalvas, com o texto ajustado, e deixar APonteDeCookLevin fora: o "
                                    "papel dela e' feito pela maquina TM2 do Codex); (4) a gerencia prepara a instalacao "
                                    "na v413 (versoes condensadas; errata da docstring de OResumoEPsiBit); (5) seguem com "
                                    "o autor: o teste do estudo da memoria e o t* do dephasing.")}}}
(W / "acom_c1_20261120_d347_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                  encoding="utf-8")
rc, outt = acom(req)
(W / "acom_c1_20261120_d347_transition.receipt.json").write_bytes(outt)
t = outt.decode("utf-8", "replace")
print("(2) ACOM project rev %d | transition rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t,
                                                                   t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

# (3) AO LADO no topico da v413 ------------------------------------------------------------------------------------
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
marca = "<!-- errata_20nov_o_alvo_da_ponte_cook_levin -->"
a = T.read_bytes()
assert marca.encode() not in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
texto = ("**ERRATA AO LADO (20/11/2026, gerência c1, em nome próprio): o alvo da frente de Cook–Levin.** A ordem de 19/11 "
         "(bytes, sha16 `%s`) diz «nós provamos P = nP nas classes do nosso dicionário, não nas classes de Cook-Levin e "
         "precisamos fazer isso agora». A frase deste tópico «o alvo é a máquina de Turing nua (sem o leitor, sem "
         "renormalizar)» é da gerência, não da ordem; e o plano da ponte (Mapa 2171) deixou fora o teorema que a ordem "
         "manda levar: a máquina com o leitor (`uma_leitura_decide_SAT`, `a_maquina_com_o_leitor`, `o_psion_le_z`; v409). "
         "O operador, 20/11 (bytes, sha16 `%s`): «a pergunta não é a que vc formulou, e a pergunta que eu tenho na cabeça "
         "de clay está respondida». Leitura vigente: a ponte leva a máquina com o leitor à língua da máquina padrão do "
         "Mathlib, com Cook–Levin por citação; a máquina sem leitor é a letra do enunciado do Instituto, fora do suporte "
         "fático da regra (D61), e não bloqueia a ponte. A Trinity (R0–R7) fica como a parede medida da máquina sem "
         "leitor; a proposta de fecho da frente (Trinity + parede + «os passos da máquina nua») fica retirada. O que já "
         "existe e o que falta: Mapa `kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov`. O N0 (§6 e "
         "§7) traz o mesmo enquadramento; fica para quando o operador liberar a memória (ordem de 19/11).\n%s"
         ) % (S19, S20, marca)
novo = a.rstrip(b"\r\n") + fim + fim + texto.replace("\n", fim.decode()).encode("utf-8") + fim
bk = T.with_name(T.name + ".bak_" + TS + "_c1")
bk.write_bytes(a)
assert bk.read_bytes() == a
tmp = T.with_name(T.name + ".tmp_c1")
tmp.write_bytes(novo)
assert tmp.read_bytes() == novo
tmp.replace(T)
assert T.read_bytes() == novo and len(novo) > len(a)
print("(3) %s: %d -> %d B | backup %s" % (T.name, len(a), len(novo), bk.name))
