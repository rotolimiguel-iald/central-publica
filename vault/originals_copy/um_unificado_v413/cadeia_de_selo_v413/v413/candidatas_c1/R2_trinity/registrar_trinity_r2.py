# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a R2 da Trinity (o operador: «a pedra trinity refere-se à fronteira dos tres
literais», fala por bytes): (0) confere o recibo; (1) terceiro adendo ao pedido de revisao ao Codex (a R2 substitui a R1
no item 9); (2) RESULTADO na rota da Trinity; (3) transicao ACOM d341; (4) AO LADO no topico da v413; (5) registro datado
no Atlas (append com backup de bytes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_excelente_prossigamos_porque_a_pedra_trinity_refere_se_a_fronteira_dos_tres_literais_verbatim.txt")
R2, CONF = W / "Trinity.lean", W / "build" / "CONFERENCIA.json"
R1 = W.parent / "R1_trinity" / "Trinity.lean"
REV = CS / "v413" / "revisao_codex"
AD2 = REV / "ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0)
assert "a pedra trinity refere-se à fronteira dos tres literais" in FALA.read_text(encoding="utf-8")
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R2) and conf["pedidos"] == 30 and conf["relatorios"] == 30
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
txt = R2.read_text(encoding="utf-8")
for t in ("theorem na_fronteira_todo_lado_corta_uma_de_tres", "theorem a_fronteira_tem_tres_literais",
          "theorem a_inclinacao_para_so_na_fronteira", "theorem a_travessia_decide", "theorem o_preco_da_travessia",
          "theorem a_trindade_na_fronteira"):
    assert t in txt, t
print("(0) ok | R2 sha16 %s (R1 %s) | 30/30 no trio | fala sha16 %s" % (sha(R2)[:16], sha(R1)[:16], sha(FALA)[:16]))

# (1) terceiro adendo
AD3 = REV / "ADENDO_3_AO_PEDIDO_DE_REVISAO_TRINITY_R2_20nov.md"
texto = """# Terceiro adendo ao pedido de revisão de terceiro ao Codex (v413): a R2 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R2.** Revise `{r2}` (sha16 `{sr2}`), que contém a R1 inteira (sha16 `{sr1}`; nenhum enunciado mudou) e acrescenta as §9 a §11. A gerência a compilou na caixa da v412 e registrou o resultado em `{conf}` (sha16 `{sconf}`): 30 de 30 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do segundo adendo (`{ad2}`); os pontos de atenção dos dois adendos anteriores continuam valendo.

Pontos de atenção das §9 a §11:
- **A fronteira:** confira que `NaFronteira` descreve exatamente onde `inclina` devolve `.indeciso` e que `a_inclinacao_para_so_na_fronteira` não depende de combustível insuficiente.
- **O terceiro literal:** em `na_fronteira_todo_lado_corta_uma_de_tres`, confira o invariante `Dentro` (toda cláusula do lado é sublista de uma original) e a conclusão: uma cláusula de dois literais ou mais, cortada de uma original de três ou mais.
- **A travessia:** confira que `atravessa` só ramifica onde a inclinação para, que `a_travessia_decide` vale para toda fórmula com combustível maior que o tamanho, e que `o_preco_da_travessia` é cota exponencial no combustível (2^k·B − B fixações), não polinomial.
- **A docstring:** confira que ela não sugere travessia de preço polinomial.
""".format(r2=R2, sr2=sha(R2)[:16], sr1=sha(R1)[:16], conf=CONF, sconf=sha(CONF)[:16], ad2=AD2)
dados = texto.encode("utf-8")
tmp = AD3.with_name(AD3.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(AD3)
print("(1) adendo 3:", AD3.name, "sha16", sha(AD3)[:16])

# (2) Mapa
res = {
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R2: a fronteira e' o terceiro literal; a travessia por ramificacao decide toda formula, a preco exponencial",
    "resultado": ("R2 (sha16 %s; contem a R1 %s sem mudar enunciado): a_inclinacao_para_so_na_fronteira (com combustivel maior "
                  "que o tamanho, a inclinacao so' fica indecisa num resto com a mesma resposta que esta' na fronteira: vivo, "
                  "sem unidade, nao trivial, sonda sem acao); na_fronteira_todo_lado_corta_uma_de_tres (todo lado vivo deixa uma "
                  "clausula de >=2 literais cortada de uma original de >=3: um literal cai, os outros esperam); "
                  "a_fronteira_tem_tres_literais; a_travessia_decide (ramificando onde a inclinacao para, decide toda formula); "
                  "o_preco_da_travessia (no maximo 2^k*B - B fixacoes, B = (T+1)^2+1: exponencial); oito e sete nos exemplos. "
                  "30 de 30 relatorios no trio na caixa da v412.") % (sha(R2)[:16], sha(R1)[:16]),
    "veredito": "TRINITY_R2_A_FRONTEIRA_E_O_TERCEIRO_LITERAL__TRAVESSIA_POR_RAMIFICACAO_DECIDE_A_PRECO_EXPONENCIAL__TRAVESSIA_POLINOMIAL_OPEN",
    "estatuto": "REAL no sandbox (candidata, nao instalada); OPEN (travessia de preco polinomial: a pergunta do Instituto)",
    "status": "EXAMINADA", "olhou_dados": False,
    "onde": str(W), "artefatos": [str(R2), str(CONF), str(W / "fazer_r2_trinity.py"), str(FALA), str(AD3)],
    "nota": ("o preco provado e' cota superior exponencial; nao ha cota inferior para todo procedimento (isso seria resolver a "
             "pergunta do Instituto no sentido negativo); quem constroi nao aprova: revisao do Codex pedida"),
}
pj = W / "resultado_trinity_r2_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(2) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

# (3) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 367,
       "event_id": "c1-20nov-d341-trinity-r2",
       "changes": {"records": [
           {"id": "c1-20nov-d341-a-trinity-e-a-fronteira-dos-tres-literais", "kind": "decision", "statute": "INPUT",
            "text": "O autor (20/11), por bytes: «excelente, prossigamos porque a pedra trinity refere-se à fronteira dos tres literais».",
            "sources": [src(FALA)]},
           {"id": "c1-20nov-d341-trinity-r2", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R2: a inclinacao so' para na fronteira; na fronteira todo lado vivo corta uma clausula de tres "
                     "literais ou mais (um cai, os outros esperam); a travessia por ramificacao decide toda formula, a preco "
                     "provado exponencial (<= 2^k*B - B fixacoes). 30 de 30 no trio na v412. A travessia de preco polinomial "
                     "segue [OPEN] (a pergunta do Instituto). Revisao do Codex pedida (terceiro adendo)."),
            "sources": [src(R2), src(CONF), src(AD3)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R2_A_FRONTEIRA_E_O_TERCEIRO_LITERAL__REVISAO_DO_CODEX_PEDIDA",
                    "next_action": ("(1) o autor cola no Codex o pedido de revisao e os tres adendos da Trinity; (2) a travessia "
                                    "de preco polinomial da fronteira dos tres literais so' com o gesto do autor para ler a "
                                    "espera sem descer, e a partitura antes; (3) errata ao lado na v413 da docstring de "
                                    "OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; (4) seguem com o autor: o teste do "
                                    "estudo da memoria e o t* do teste de dephasing.")}}}
(W / "acom_c1_20261120_d341_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d341_transition.receipt.json").write_bytes(r.stdout)
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
acrescenta(T, "<!-- ao_lado_20nov_trinity_r2 -->",
           ("**AO LADO (20/11/2026, gerência c1): a R2 da Trinity — a fronteira dos três literais.** A fala (bytes em "
            "`work\\cunhagens_13out\\%s`, sha16 `%s`): «a pedra trinity refere-se à fronteira dos tres literais». A R2 "
            "(`work\\cadeia_de_selo\\v413\\candidatas_c1\\R2_trinity\\`, sha16 `%s`; contém a R1) prova: a inclinação só para na "
            "fronteira; na fronteira todo lado vivo corta uma cláusula de três literais ou mais (um literal cai, os outros esperam); "
            "a travessia por ramificação decide toda fórmula, a preço provado exponencial (≤ 2^k·B − B fixações). 30 de 30 no trio "
            "na v412. A travessia de preço polinomial é a pergunta do Instituto [OPEN]. Revisão do Codex pedida "
            "(`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`).") % (FALA.name, sha(FALA)[:16], sha(R2)[:16], AD3.name), "4")

# (5) Atlas
A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- registro_20nov_trinity_r2 -->",
           ("### Registro de 20/11/2026, quarto (gerência c1) — Trinity R2: a fronteira é o terceiro literal\n\n"
            "**A leitura do nome (do operador, 20/11/2026), [INPUT]:** «a pedra trinity refere-se à fronteira dos tres literais».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R2, não instalada) [REAL no sandbox]:** com combustível maior que o tamanho, "
            "a inclinação só fica indecisa num resto com a mesma resposta que está na fronteira: vivo, sem unidade, não trivial, "
            "e a sonda não age (`a_inclinacao_para_so_na_fronteira`). Na fronteira, todo lado, fixado e propagado, fica vivo e "
            "deixa uma cláusula de dois literais ou mais cortada de uma cláusula original de três literais ou mais: um literal "
            "cai, os outros esperam (`na_fronteira_todo_lado_corta_uma_de_tres`; logo `a_fronteira_tem_tres_literais`). A "
            "travessia por ramificação (`atravessa`: onde a inclinação para, segue pelos dois lados do primeiro Nome) decide toda "
            "fórmula (`a_travessia_decide`), ao preço provado de no máximo 2^k·B − B fixações, com B = (T+1)² + 1 e k o "
            "combustível: exponencial no tamanho (`o_preco_da_travessia`). As oito cláusulas estão na fronteira e a travessia diz "
            "não; sete delas param a inclinação e a travessia diz sim. Compila na caixa da v412 com 30 de 30 relatórios no trio.\n\n"
            "**O que segue aberto:** uma travessia de preço polinomial para toda fórmula de três literais, isto é, ler a espera "
            "sem descer pelos dois lados: é a pergunta do Instituto [OPEN]. O preço provado aqui é cota superior; não há cota "
            "inferior para todo procedimento.\n\n"
            "Estatuto: [INPUT] a letra do operador; [REAL no sandbox] os termos; [OPEN] a travessia polinomial; [DECLARADO] as "
            "leituras da gerência. Validade no kernel não é creditação; o gate não se move."), "5")
