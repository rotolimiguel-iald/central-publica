# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a R4 da Trinity (a terceira lei; fala por bytes): (0) confere o recibo; (1) RESULTADO
na rota da Trinity; (2) transicao ACOM d343; (3) AO LADO no topico da v413; (4) registro datado no Atlas (append com backup
de bytes). O pedido consolidado de revisao (item 9 = R4) foi gerado por fazer_pedido_consolidado.py."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao_e_o_zero"
    "_absoluto_verbatim.txt")
R4, CONF = W / "Trinity.lean", W / "build" / "CONFERENCIA.json"
R3 = W.parent / "R3_trinity" / "Trinity.lean"
PED = CS / "v413" / "revisao_codex" / "PEDIDO_DE_REVISAO_AO_CODEX_v413_CONSOLIDADO_R4_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert "violar a terceira lei de nernst" in FALA.read_text(encoding="utf-8")
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R4) and conf["pedidos"] == 43 and conf["relatorios"] == 43
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
assert sha(R4)[:16] in PED.read_text(encoding="utf-8"), "o pedido consolidado nao aponta a R4 atual"
print("(0) ok | R4 sha16 %s (R3 %s) | 43/43 no trio | fala sha16 %s | pedido sha16 %s" % (
    sha(R4)[:16], sha(R3)[:16], sha(FALA)[:16], sha(PED)[:16]))

res = {
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R4: a terceira lei na fronteira (o zero absoluto nao se alcanca; a carga e' exata no patamar plano)",
    "resultado": ("R4 (sha16 %s; contem a R3 %s sem mudar enunciado): o_zero_absoluto_nao_se_alcanca (em passos finitos, se ha' "
                  "atribuicao que nao e' solucao, o peso passa estritamente o numero de solucoes); "
                  "no_patamar_plano_a_carga_e_exata (se toda atribuicao viola exatamente uma clausula, 1 <= peso sse "
                  "k*(-ln(1-beta)) <= n*ln 2: a leitura erra enquanto nao paga a carga, para todo beta < 1); "
                  "oito_patamar_plano e as_oito_pedem_a_carga (carga 3*ln 2); o_preco_em_estados_e_a_exponencial_da_carga "
                  "(2^m = e^(m*ln 2)). 43 de 43 relatorios no trio na caixa da v412.") % (sha(R4)[:16], sha(R3)[:16]),
    "veredito": "TRINITY_R4_A_CARGA_TEM_DE_SER_PAGA_NA_TEORIA__A_MOEDA_DA_MAQUINA_NUA_OPEN",
    "estatuto": ("REAL no sandbox (candidata, nao instalada); ONTO (a identificacao do operador com a terceira lei de Nernst); "
                 "KNOWN (Nernst 1912; Landauer 1961; Aaronson 2005 como proposta); OPEN (pagar a carga em tempo polinomial na "
                 "maquina nua)"),
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(R4), str(CONF), str(W / "fazer_r4_trinity.py"), str(FALA), str(PED)],
    "nota": "a lei diz que a carga se paga; nao diz em que moeda a maquina nua paga; quem constroi nao aprova",
}
pj = W / "resultado_trinity_r4_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(1) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 369,
       "event_id": "c1-20nov-d343-trinity-r4-a-terceira-lei",
       "changes": {"records": [
           {"id": "c1-20nov-d343-leitura-nernst", "kind": "decision", "statute": "INPUT",
            "text": ("O autor (20/11), por bytes: «atravessar a fronteira sem pagar o nome é violar a terceira lei de nernst, "
                     "porque a única solução é o zero absoluto». Leitura [ONTO] do autor."),
            "sources": [src(FALA)]},
           {"id": "c1-20nov-d343-trinity-r4", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R4: na maquina da teoria, em passos finitos o zero absoluto nao se alcanca (o peso passa "
                     "estritamente o numero de solucoes) e, no patamar plano, a leitura so' acerta depois de pagar a carga "
                     "n*ln 2 (equivalencia exata, para todo beta < 1); o preco em estados 2^m e' e^(m*ln 2). 43 de 43 no trio na "
                     "v412. A lei diz que a carga se paga; a moeda da maquina nua (tempo polinomial ou estados) segue [OPEN]. "
                     "Pedido consolidado de revisao ao Codex com a R4."),
            "sources": [src(R4), src(CONF), src(PED)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R4_A_TERCEIRA_LEI__REVISAO_DO_CODEX_PEDIDA",
                    "next_action": ("(1) o autor cola no Codex o pedido consolidado (R4); (2) depois da revisao, a gerencia "
                                    "prepara a instalacao na v413 (versao condensada da Trinity e das pedras novas, errata da "
                                    "docstring de OResumoEPsiBit); (3) seguem com o autor: o teste do estudo da memoria e o t* do "
                                    "teste de dephasing.")}}}
(W / "acom_c1_20261120_d343_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d343_transition.receipt.json").write_bytes(r.stdout)
t = r.stdout.decode("utf-8", "replace")
print("(2) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in t, t[t.find('"revision"'):][:20]))
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
acrescenta(T, "<!-- ao_lado_20nov_trinity_r4 -->",
           ("**AO LADO (20/11/2026, gerência c1): a R4 da Trinity — a terceira lei.** A fala (bytes em `work\\cunhagens_13out\\%s`, "
            "sha16 `%s`): «atravessar a fronteira sem pagar o nome é violar a terceira lei de nernst, porque a única solução é o "
            "zero absoluto». A R4 (`work\\cadeia_de_selo\\v413\\candidatas_c1\\R4_trinity\\`, sha16 `%s`; contém a R3) prova, na "
            "máquina da teoria: em passos finitos o zero absoluto não se alcança; no patamar plano a leitura só acerta depois de "
            "pagar a carga n·ln 2 (equivalência exata); e 2^m = e^(m·ln 2). 43 de 43 no trio na v412. A lei diz que a carga se "
            "paga; a moeda da máquina nua segue aberta. Pedido consolidado ao Codex com a R4 "
            "(`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`).") % (FALA.name, sha(FALA)[:16], sha(R4)[:16], PED.name), "3")

A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- registro_20nov_trinity_r4 -->",
           ("### Registro de 20/11/2026, sexto (gerência c1) — Trinity R4: a terceira lei na fronteira\n\n"
            "**A leitura (do operador, 20/11/2026), [INPUT/ONTO]:** «atravessar a fronteira sem pagar o nome é violar a terceira "
            "lei de nernst, porque a única solução é o zero absoluto».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R4, não instalada) [REAL no sandbox]:** na máquina da teoria (o fator 1 − β), a "
            "solução é o custo zero; em passos finitos o zero absoluto não se alcança: se há atribuição que não é solução, o peso "
            "passa estritamente o número de soluções (`o_zero_absoluto_nao_se_alcanca`). No patamar plano (toda atribuição viola "
            "exatamente uma cláusula), a leitura diz sim, e erra, enquanto o pagamento k·(−ln(1−β)) não passa a carga n·ln 2, e "
            "acerta depois: equivalência exata, para todo β < 1 (`no_patamar_plano_a_carga_e_exata`); nas oito cláusulas a carga é "
            "3·ln 2. O preço em estados de m Nomes é a exponencial da carga: 2^m = e^(m·ln 2). Compila na caixa da v412 com 43 de "
            "43 relatórios no trio.\n\n"
            "**O que segue aberto:** a lei diz que a carga se paga; não diz em que moeda a máquina nua paga. Pagar em tempo "
            "polinomial, e não em estados, é a pergunta do Instituto [OPEN]. Nernst (1912) e Landauer (1961) são [KNOWN]; tratar a "
            "dureza de NP como princípio físico é proposta conhecida (Aaronson, 2005), não teorema.\n\n"
            "Estatuto: [INPUT/ONTO] a leitura do operador; [REAL no sandbox] os termos; [KNOWN] as leis citadas; [OPEN] a moeda da "
            "máquina nua. Validade no kernel não é creditação; o gate não se move."), "4")
