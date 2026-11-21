# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a R1 da Trinity (pedida pelo operador, fala por bytes): (0) confere o recibo;
(1) segundo adendo ao pedido de revisao ao Codex (a R1 substitui a R0 no item 9); (2) RESULTADO na rota da Trinity;
(3) transicao ACOM d340; (4) AO LADO no topico da v413; (5) registro datado no Atlas (append com backup de bytes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / "OPERADOR_20nov_excelente_prossigamos_escreva_a_r1_verbatim.txt"
R1, CONF = W / "Trinity.lean", W / "build" / "CONFERENCIA.json"
R0 = W.parent / "R0_trinity" / "Trinity.lean"
REV = CS / "v413" / "revisao_codex"
AD1 = REV / "ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0)
assert FALA.read_text(encoding="utf-8").strip() == "excelente, prossigamos escreva a r1"
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R1) and conf["pedidos"] == 21 and conf["relatorios"] == 21
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
txt = R1.read_text(encoding="utf-8")
for t in ("theorem todo_lado_morre_ou_nao_corta", "theorem em_dois_literais_o_sistema_sempre_inclina",
          "theorem em_dois_literais_a_inclinacao_decide", "theorem a_cadeia_inclina_e_diz_sim"):
    assert t in txt, t
print("(0) ok | R1 sha16 %s (R0 %s) | 21/21 no trio | fala sha16 %s" % (sha(R1)[:16], sha(R0)[:16], sha(FALA)[:16]))

# (1) segundo adendo
AD2 = REV / "ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md"
texto = """# Segundo adendo ao pedido de revisão de terceiro ao Codex (v413): a R1 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R1.** Revise `{r1}` (sha16 `{sr1}`), que contém a R0 inteira (sha16 `{sr0}`; nenhum enunciado mudou) e acrescenta a §5b e um exemplo. A gerência a compilou na caixa da v412 e registrou o resultado em `{conf}` (sha16 `{sconf}`): 21 de 21 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do primeiro adendo (`{ad1}`); os pontos de atenção de lá continuam valendo.

Pontos de atenção da §5b:
- **A integridade:** em `integra_restringe`, confira que a cláusula original fica inteira ou cai para no máximo um literal.
- **A autarquia:** confira que `todo_lado_morre_ou_nao_corta` vale para todo literal, apareça ele na fórmula ou não.
- **A decisão:** confira que `em_dois_literais_o_sistema_sempre_inclina` usa combustível maior que o tamanho e que a recursão diminui o tamanho a cada volta.
- **Os exemplos:** `a_cadeia_inclina_e_diz_sim` é uma fórmula de dois literais decidida em duas voltas, avaliada por `decide`.
""".format(r1=R1, sr1=sha(R1)[:16], sr0=sha(R0)[:16], conf=CONF, sconf=sha(CONF)[:16], ad1=AD1)
dados = texto.encode("utf-8")
tmp = AD2.with_name(AD2.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(AD2)
print("(1) adendo 2:", AD2.name, "sha16", sha(AD2)[:16])

# (2) Mapa: RESULTADO na rota da Trinity
res = {
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R1: em dois literais todo lado morre logo ou nao corta nada; a inclinacao decide toda formula de dois literais",
    "resultado": ("R1 (sha16 %s; contem a R0 %s sem mudar enunciado): todo_lado_morre_ou_nao_corta (a autarquia em dois literais, "
                  "pelo invariante da integridade: toda clausula do lado propagado e' original ou tem no maximo um literal); "
                  "em_dois_literais_o_sistema_sempre_inclina (com combustivel maior que o tamanho, nunca indecisa); "
                  "em_dois_literais_a_inclinacao_decide (sim exatamente quando ha solucao); a_cadeia_inclina_e_diz_sim (duas "
                  "voltas). 21 de 21 relatorios no trio na caixa da v412, sem aviso. E' Even-Itai-Shamir 1976 [KNOWN], provado "
                  "para este procedimento.") % (sha(R1)[:16], sha(R0)[:16]),
    "veredito": "TRINITY_R1_COMPILA__DECIDE_HORN_E_DOIS_LITERAIS__A_FRONTEIRA_FICA_NOS_TRES_LITERAIS",
    "estatuto": "REAL no sandbox (candidata, nao instalada); KNOWN (Even-Itai-Shamir 1976)", "status": "EXAMINADA",
    "olhou_dados": False, "onde": str(W), "artefatos": [str(R1), str(CONF), str(W / "fazer_r1_trinity.py"), str(FALA), str(AD2)],
    "nota": "quem constroi nao aprova: revisao do Codex pedida por adendo",
}
pj = W / "resultado_trinity_r1_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(2) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

# (3) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 366,
       "event_id": "c1-20nov-d340-trinity-r1",
       "changes": {"records": [
           {"id": "c1-20nov-d340-ordem-r1", "kind": "decision", "statute": "INPUT",
            "text": "O autor (20/11), por bytes: «excelente, prossigamos escreva a r1».", "sources": [src(FALA)]},
           {"id": "c1-20nov-d340-trinity-r1-decide-dois-literais", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R1: em formula de dois literais todo lado propagado morre logo ou nao corta nenhuma clausula; a "
                     "inclinacao decide toda formula de dois literais (e toda de Horn), em no maximo (T+1)^3 fixacoes. 21 de 21 "
                     "no trio na v412. Nao instalada; revisao do Codex pedida (segundo adendo). A fronteira fica nos tres "
                     "literais (oito_fica_na_fronteira)."),
            "sources": [src(R1), src(CONF), src(AD2)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R1_DECIDE_HORN_E_DOIS_LITERAIS__REVISAO_DO_CODEX_PEDIDA",
                    "next_action": ("(1) o autor cola no Codex o pedido de revisao e os dois adendos da Trinity; (2) a fronteira "
                                    "dos tres literais segue com o autor (procedimento novo, com a partitura antes); (3) errata ao "
                                    "lado na v413 da docstring de OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; (4) seguem "
                                    "com o autor: o teste do estudo da memoria e o t* do teste de dephasing.")}}}
(W / "acom_c1_20261120_d340_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d340_transition.receipt.json").write_bytes(r.stdout)
t = r.stdout.decode("utf-8", "replace")
print("(3) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t


def acrescenta(T, marca, texto, rotulo):
    a = T.read_bytes()
    assert marca.encode() not in a
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + fim + ("%s\n%s" % (texto, marca)).replace("\n", fim.decode()).encode("utf-8") + fim
    bk = T.with_name(T.name + ".bak_" + TS + "_c1")
    bk.write_bytes(a)
    assert bk.read_bytes() == a
    tmp = T.with_name(T.name + ".tmp_c1")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(T)
    assert T.read_bytes() == novo and len(novo) > len(a)
    print("(%s) %s: %d -> %d B | backup %s" % (rotulo, T.name, len(a), len(novo), bk.name))


# (4) topico
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
acrescenta(T, "<!-- ao_lado_20nov_trinity_r1 -->",
           ("**AO LADO (20/11/2026, gerência c1): a R1 da Trinity.** A fala (bytes em `work\\cunhagens_13out\\%s`, sha16 `%s`): "
            "«excelente, prossigamos escreva a r1». A R1 (`work\\cadeia_de_selo\\v413\\candidatas_c1\\R1_trinity\\`, sha16 `%s`; "
            "contém a R0 sem mudar enunciado) prova que, numa fórmula de dois literais, todo lado propagado ou morre logo ou não "
            "corta nenhuma cláusula ao meio (a autarquia), e por isso a inclinação decide toda fórmula de dois literais, como já "
            "decidia toda de Horn, em no máximo (T+1)³ fixações. 21 de 21 no trio na v412. A fronteira fica nos três literais "
            "(`oito_fica_na_fronteira`). Revisão do Codex pedida (`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`).") % (
               FALA.name, sha(FALA)[:16], sha(R1)[:16], AD2.name), "4")

# (5) Atlas
A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- registro_20nov_trinity_r1 -->",
           ("### Registro de 20/11/2026, terceiro (gerência c1) — Trinity R1: em dois literais, todo lado morre logo ou não corta "
            "nada\n\n"
            "**A ordem (do operador, 20/11/2026), [INPUT]:** «excelente, prossigamos escreva a r1».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R1, não instalada) [REAL no sandbox]:** numa fórmula em que toda cláusula tem dois "
            "literais, fixar qualquer literal e propagar dá a morte no zero absoluto ou deixa só cláusulas originais "
            "(`todo_lado_morre_ou_nao_corta`; o invariante: toda cláusula do lado propagado é original ou tem no máximo um "
            "literal). Logo a sonda age já no primeiro literal, e a inclinação decide toda fórmula de dois literais "
            "(`em_dois_literais_o_sistema_sempre_inclina`, `em_dois_literais_a_inclinacao_decide`), como já decidia toda de Horn, "
            "em no máximo (T+1)³ fixações. É o resultado de Even–Itai–Shamir (1976) [KNOWN], provado para este procedimento. "
            "Compila na caixa da v412 com 21 de 21 relatórios no trio.\n\n"
            "**O que segue aberto:** os três literais, onde um lado pode cortar cláusulas ao meio sem morrer "
            "(`oito_fica_na_fronteira`); é a fronteira medida em 18/11 e a pergunta do Instituto [OPEN]. O custo conta fixações no "
            "modelo da casa. O verbete entra na instalação.\n\n"
            "Estatuto: [INPUT] a letra do operador; [REAL no sandbox] os termos; [KNOWN] Even–Itai–Shamir; [DECLARADO] as leituras "
            "da gerência. Validade no kernel não é creditação; o gate não se move."), "5")
