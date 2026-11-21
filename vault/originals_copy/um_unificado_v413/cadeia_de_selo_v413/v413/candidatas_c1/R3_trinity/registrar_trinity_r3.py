# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a R3 da Trinity (o operador: «excelente, prossigamos», fala por bytes): (0) confere o
recibo; (1) quarto adendo ao pedido de revisao ao Codex (a R3 substitui a R2 no item 9); (2) RESULTADO na rota da Trinity;
(3) transicao ACOM d342; (4) AO LADO no topico da v413; (5) registro datado no Atlas (append com backup de bytes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / "OPERADOR_20nov_excelente_prossigamos_apos_a_R2_da_trinity_verbatim.txt"
R3, CONF = W / "Trinity.lean", W / "build" / "CONFERENCIA.json"
R2 = W.parent / "R2_trinity" / "Trinity.lean"
REV = CS / "v413" / "revisao_codex"
AD3 = REV / "ADENDO_3_AO_PEDIDO_DE_REVISAO_TRINITY_R2_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert FALA.read_text(encoding="utf-8").strip() == "excelente, prossigamos"
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R3) and conf["pedidos"] == 37 and conf["relatorios"] == 37
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
txt = R3.read_text(encoding="utf-8")
for t in ("theorem a_travessia_pelos_nomes_decide", "theorem o_preco_dos_nomes", "theorem o_preco_da_fronteira_esta_nos_nomes",
          "theorem a_trindade_dos_nomes"):
    assert t in txt, t
print("(0) ok | R3 sha16 %s (R2 %s) | 37/37 no trio | fala sha16 %s" % (sha(R3)[:16], sha(R2)[:16], sha(FALA)[:16]))

AD4 = REV / "ADENDO_4_AO_PEDIDO_DE_REVISAO_TRINITY_R3_20nov.md"
texto = """# Quarto adendo ao pedido de revisão de terceiro ao Codex (v413): a R3 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R3.** Revise `{r3}` (sha16 `{sr3}`), que contém a R2 inteira (sha16 `{sr2}`; nenhum enunciado mudou) e acrescenta a §12, os Nomes da fronteira. A gerência a compilou na caixa da v412 e registrou o resultado em `{conf}` (sha16 `{sconf}`): 37 de 37 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do terceiro adendo (`{ad3}`); os pontos de atenção dos adendos anteriores continuam valendo.

Pontos de atenção da §12:
- **O toque:** em `toca_restringe`, confira que a cláusula de três literais que sobra depois de fixar um Nome não foi cortada (é a original) e continua tocada pelo resto da lista.
- **A decisão:** confira que `a_travessia_pelos_nomes_decide` usa, no fim da lista, a decisão dos dois literais da R1.
- **O preço:** confira que `o_preco_dos_nomes` é exponencial só no comprimento da lista e polinomial no tamanho.
- **A docstring:** confira que ela não sugere que os Nomes da fronteira sejam poucos em geral.
""".format(r3=R3, sr3=sha(R3)[:16], sr2=sha(R2)[:16], conf=CONF, sconf=sha(CONF)[:16], ad3=AD3)
dados = texto.encode("utf-8")
tmp = AD4.with_name(AD4.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(AD4)
print("(1) adendo 4:", AD4.name, "sha16", sha(AD4)[:16])

res = {
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R3: o preco da fronteira esta' nos Nomes que tocam as clausulas de tres literais",
    "resultado": ("R3 (sha16 %s; contem a R2 %s sem mudar enunciado): numa formula de ate' tres literais, se a lista S toca toda "
                  "clausula de tres literais, atravessaPelos S (ramificar so' nos Nomes de S e deixar o resto a inclinacao) decide "
                  "a formula (a_travessia_pelos_nomes_decide), ao preco de no maximo 2^|S|*((T+1)^3+2) fixacoes "
                  "(o_preco_dos_nomes): exponencial so' no numero de Nomes da fronteira. A lista dos primeiros Nomes das "
                  "clausulas de tres literais sempre toca (os_nomes_da_fronteira_tocam). Nas oito e nas sete clausulas um so' "
                  "Nome toca todas. 37 de 37 relatorios no trio na caixa da v412.") % (sha(R3)[:16], sha(R2)[:16]),
    "veredito": "TRINITY_R3_O_PRECO_DA_FRONTEIRA_ESTA_NOS_NOMES__EXPONENCIAL_SO_EM_S__TRAVESSIA_POLINOMIAL_OPEN",
    "estatuto": "REAL no sandbox (candidata, nao instalada); OPEN (Nomes da fronteira poucos em geral; travessia polinomial)",
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(R3), str(CONF), str(W / "fazer_r3_trinity.py"), str(FALA), str(AD4)],
    "nota": ("cota superior; no kernel, atravessar um corte de n Nomes partilhados pede 2^n retangulos "
             "(Codex.PairCut.exact_cover_iff); quem constroi nao aprova"),
}
pj = W / "resultado_trinity_r3_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(2) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 368,
       "event_id": "c1-20nov-d342-trinity-r3",
       "changes": {"records": [
           {"id": "c1-20nov-d342-prossigamos-r3", "kind": "decision", "statute": "INPUT",
            "text": "O autor (20/11), por bytes, depois da R2: «excelente, prossigamos».", "sources": [src(FALA)]},
           {"id": "c1-20nov-d342-trinity-r3", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R3: numa formula de ate' tres literais, ramificar so' nos Nomes que tocam as clausulas de tres "
                     "literais decide a formula, ao preco <= 2^|S|*((T+1)^3+2) fixacoes: exponencial so' nos Nomes da "
                     "fronteira. 37 de 37 no trio na v412. Que esses Nomes sejam poucos em geral, e a travessia polinomial, "
                     "seguem [OPEN]. Revisao do Codex pedida (quarto adendo)."),
            "sources": [src(R3), src(CONF), src(AD4)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R3_O_PRECO_ESTA_NOS_NOMES__REVISAO_DO_CODEX_PEDIDA",
                    "next_action": ("(1) o autor cola no Codex o pedido de revisao e os quatro adendos da Trinity; (2) a "
                                    "travessia sem pagar por Nome da fronteira so' com o gesto do autor e a partitura antes; (3) "
                                    "errata ao lado na v413 da docstring de OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; "
                                    "(4) seguem com o autor: o teste do estudo da memoria e o t* do teste de dephasing.")}}}
(W / "acom_c1_20261120_d342_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d342_transition.receipt.json").write_bytes(r.stdout)
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


T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
acrescenta(T, "<!-- ao_lado_20nov_trinity_r3 -->",
           ("**AO LADO (20/11/2026, gerência c1): a R3 da Trinity — o preço da fronteira está nos Nomes.** A fala (bytes em "
            "`work\\cunhagens_13out\\%s`, sha16 `%s`): «excelente, prossigamos». A R3 "
            "(`work\\cadeia_de_selo\\v413\\candidatas_c1\\R3_trinity\\`, sha16 `%s`; contém a R2) prova que, numa fórmula de até "
            "três literais, ramificar só nos Nomes que tocam as cláusulas de três literais decide a fórmula, ao preço de no "
            "máximo 2^|S|·((T+1)³+2) fixações: exponencial só nos Nomes da fronteira. 37 de 37 no trio na v412. Revisão do Codex "
            "pedida (`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`).") % (FALA.name, sha(FALA)[:16], sha(R3)[:16], AD4.name), "4")

A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- registro_20nov_trinity_r3 -->",
           ("### Registro de 20/11/2026, quinto (gerência c1) — Trinity R3: o preço da fronteira está nos Nomes da fronteira\n\n"
            "**A ordem (do operador, 20/11/2026), [INPUT]:** «excelente, prossigamos».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R3, não instalada) [REAL no sandbox]:** numa fórmula de até três literais, se "
            "uma lista de Nomes toca toda cláusula de três literais, ramificar só nesses Nomes e deixar o resto à inclinação "
            "decide a fórmula (`a_travessia_pelos_nomes_decide`), ao preço de no máximo 2^|S|·((T+1)³ + 2) fixações "
            "(`o_preco_dos_nomes`): exponencial só no número de Nomes da fronteira, polinomial no resto. A lista dos primeiros "
            "Nomes das cláusulas de três literais sempre toca (`os_nomes_da_fronteira_tocam`). Nas oito e nas sete cláusulas um "
            "só Nome toca todas, e a travessia por ele paga dois lados. Compila na caixa da v412 com 37 de 37 relatórios no "
            "trio.\n\n"
            "**O que segue aberto:** que os Nomes da fronteira sejam poucos em geral; no kernel, atravessar um corte de n Nomes "
            "partilhados pede 2ⁿ retângulos (`Codex.PairCut.exact_cover_iff`). Um gesto que atravesse sem pagar por Nome da "
            "fronteira é a pergunta do Instituto [OPEN].\n\n"
            "Estatuto: [INPUT] a letra do operador; [REAL no sandbox] os termos; [OPEN] os Nomes poucos e a travessia polinomial; "
            "[DECLARADO] as leituras da gerência. Validade no kernel não é creditação; o gate não se move."), "5")
