# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a R6 da Trinity («A máquina nua paga em eletricidade»; fala por bytes): (0) confere
o recibo, a conferencia dos enunciados R5 -> R6 e o adendo R6 ao Codex; (1) RESULTADO na rota da Trinity; (2) transicao
ACOM d345; (3) AO LADO no topico da v413; (4) registro datado no Atlas (append com backup de bytes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
C1 = W.parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / "OPERADOR_20nov_a_maquina_nua_paga_em_eletricidade_verbatim.txt"
R6, CONF, R5 = W / "Trinity.lean", W / "build" / "CONFERENCIA.json", C1 / "R5_trinity" / "Trinity.lean"
CONFE = C1 / "conferir_enunciados.py"
ADENDO = CS / "v413" / "revisao_codex" / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R6_TRINITY_R2_OPERADOR_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


assert FALA.read_text(encoding="utf-8").strip() == "A máquina nua paga em eletricidade"
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R6) and conf["pedidos"] == 65 and conf["relatorios"] == 65
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
r = subprocess.run([PY, "-B", "-X", "utf8", str(CONFE), str(R5), str(R6)], capture_output=True, stdin=subprocess.DEVNULL,
                   timeout=120)
saida = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0, saida
CE = W / "CONFERENCIA_ENUNCIADOS_R5_R6.json"
grava(CE, json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "script": str(CONFE), "sha256_script": sha(CONFE),
                      "velho": str(R5), "sha256_velho": sha(R5), "novo": str(R6), "sha256_novo": sha(R6),
                      "rc": r.returncode, "saida": saida}, ensure_ascii=False, indent=1).encode("utf-8"))
assert sha(R6)[:16] in ADENDO.read_text(encoding="utf-8"), "o adendo nao aponta a R6 atual"
print("(0) ok | R6 %s (R5 %s) 65/65 | fala %s | adendo %s\n    %s" % (sha(R6)[:16], sha(R5)[:16], sha(FALA)[:16],
                                                                   sha(ADENDO)[:16], saida.splitlines()[0]))

res = {
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R6: a maquina nua paga em eletricidade (a conta de luz no piso de Landauer)",
    "resultado": ("R6 (sha16 %s; contem a R5 %s sem mudar enunciado, conferido por script: 0 removidas, 0 mudadas, 9 novas). "
                  "§15: no piso de Landauer (k*T*ln 2, o termo do kernel landauer_floor_pos) a conta de luz de m Nomes e' "
                  "m pisos, linear em m, e paga o expoente da carga, nao os estados (a_conta_de_luz_de_m_nomes, "
                  "cada_nome_custa_um_piso, a_eletricidade_paga_o_expoente); a maquina da teoria acerta no patamar plano com "
                  "k <= n*ln 2/(-ln(1-beta)) + 1 passos, pagando a carga com sobra de menos de um passo "
                  "(a_maquina_da_teoria_acerta_pagando_no_piso); o leitor por plano da casa, que na familia coupled faz ao "
                  "menos 2^(m+1) movimentos (Codex.PlanTravel.coupled_physical_lower), paga ao menos 2^(m+1) pisos se apaga "
                  "um bit por movimento (hipotese nomeada; o_leitor_que_apaga_paga_a_potencia). Sintese: "
                  "a_maquina_nua_paga_em_eletricidade. 65 de 65 relatorios no trio na caixa da v412.") % (
        sha(R6)[:16], sha(R5)[:16]),
    "veredito": ("TRINITY_R6_A_CONTA_DE_LUZ_NO_PISO_E_LINEAR_NOS_NOMES__A_MAQUINA_QUE_APAGA_POR_MOVIMENTO_PAGA_2^(m+1)__"
                 "PASSOS_DA_MAQUINA_DE_TURING_OPEN"),
    "estatuto": ("REAL no sandbox (candidata, nao instalada); KNOWN (Landauer 1961; Bennett 1973); ONTO (a leitura do "
                 "operador: a maquina nua paga em eletricidade; cada passo da maquina da teoria lido como energia); OPEN "
                 "(o numero de passos de uma maquina de Turing nua para SAT: a pergunta do Instituto)"),
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(R6), str(CONF), str(W / "fazer_r6_trinity.py"), str(FALA), str(CONFE), str(CE), str(ADENDO)],
    "nota": ("o piso da eletricidade e' a carga (linear); a maquina que apaga a cada passo paga por passo; a conta de luz nao "
             "decide os passos; quem constroi nao aprova: adendo R6 ao Codex pronto para o operador colar"),
}
pj = W / "resultado_trinity_r6_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(1) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 371,
       "event_id": "c1-20nov-d345-trinity-r6-a-maquina-nua-paga-em-eletricidade",
       "changes": {"records": [
           {"id": "c1-20nov-d345-leitura-eletricidade", "kind": "decision", "statute": "INPUT",
            "text": "O autor (20/11), por bytes: «A máquina nua paga em eletricidade». Leitura [ONTO] do autor.",
            "sources": [src(FALA)]},
           {"id": "c1-20nov-d345-trinity-r6", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R6 (65 de 65 no trio na v412): no piso de Landauer (k*T*ln 2, termo do kernel) a conta de luz "
                     "de m Nomes e' m pisos, linear, e paga o expoente da carga, nao os estados; a maquina da teoria acerta no "
                     "patamar plano com numero de passos linear, pagando no piso; o leitor por plano da casa, que na familia "
                     "coupled faz ao menos 2^(m+1) movimentos, paga ao menos 2^(m+1) pisos se apaga um bit por movimento "
                     "(hipotese nomeada). O piso de Landauer e' minimo, nao conta; uma maquina reversivel (Bennett) pode chegar "
                     "perto dele sem encurtar os passos; a pergunta do Instituto conta passos e segue [OPEN]. Adendo R6 ao "
                     "Codex gerado; script: nenhum enunciado da R5 mudou."),
            "sources": [src(R6), src(CONF), src(CE), src(ADENDO)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R6_A_MAQUINA_NUA_PAGA_EM_ELETRICIDADE__ADENDO_R6_AO_CODEX_PRONTO",
                    "next_action": ("(1) o autor cola no Codex o adendo R6 (Trinity R6 e Operador R2); (2) o autor decide as "
                                    "pedras do Kimi: a gerencia recomenda deixar APonteDeCookLevin fora da v413 (ou so' como "
                                    "contador abstrato) e instalar as outras tres com o texto ajustado ao que provam; (3) o "
                                    "autor confirma o fecho da frente de Cook-Levin da v413: resultado (a Trinity) + parede "
                                    "medida (na maquina nua que apaga a cada passo, a conta e' exponencial nos Nomes; o piso "
                                    "e' linear) + aberto nomeado (os passos da maquina de Turing nua); (4) a gerencia prepara "
                                    "a instalacao na v413 (versoes condensadas; errata da docstring de OResumoEPsiBit); (5) "
                                    "seguem com o autor: o teste do estudo da memoria e o t* do dephasing.")}}}
(W / "acom_c1_20261120_d345_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d345_transition.receipt.json").write_bytes(r.stdout)
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
acrescenta(T, "<!-- ao_lado_20nov_trinity_r6_eletricidade -->",
           ("**AO LADO (20/11/2026, gerência c1): a R6 da Trinity — a máquina nua paga em eletricidade.** A fala (bytes em "
            "`work\\cunhagens_13out\\%s`, sha16 `%s`): «A máquina nua paga em eletricidade». A R6 "
            "(`work\\cadeia_de_selo\\v413\\candidatas_c1\\R6_trinity\\`, sha16 `%s`, 65/65; contém a R5) prova: no piso de "
            "Landauer (`landauer_floor_pos`, já no kernel) a conta de luz de m Nomes é m pisos, linear, e paga o expoente da "
            "carga; a máquina da teoria acerta no patamar plano com número de passos linear, pagando no piso; o leitor por "
            "plano da casa (`coupled_physical_lower`: ao menos 2^(m+1) movimentos) paga ao menos 2^(m+1) pisos se apaga um "
            "bit por movimento (hipótese nomeada). O piso é mínimo, não conta; a pergunta do Instituto conta passos e segue "
            "aberta. Adendo R6 ao Codex: `work\\cadeia_de_selo\\v413\\revisao_codex\\%s` (substitui o da R5).") % (
               FALA.name, sha(FALA)[:16], sha(R6)[:16], ADENDO.name), "3")

A = CEN / "memory" / "TGL_ATLAS.md"
atlas = A.read_bytes().decode("utf-8")
assert "<!-- registro_20nov_trinity_r5_operador_r2_parecer -->" in atlas
ORD = ["primeiro", "segundo", "terceiro", "quarto", "quinto", "sexto", "sétimo", "oitavo", "nono", "décimo"]
n = atlas.count("### Registro de 20/11/2026")
print("    Atlas: %d registros de 20/11 antes deste -> %s" % (n, ORD[n]))
acrescenta(A, "<!-- registro_20nov_trinity_r6_eletricidade -->",
           ("### Registro de 20/11/2026, %s (gerência c1) — a máquina nua paga em eletricidade (Trinity R6)\n\n"
            "**A leitura (do operador, 20/11/2026) [INPUT/ONTO]:** «A máquina nua paga em eletricidade».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R6, não instalada) [REAL no sandbox]:** com o piso de Landauer do kernel "
            "(k·T·ln 2 por bit, `landauer_floor_pos`), a conta de luz de m Nomes é m pisos: linear em m; cada Nome soma um "
            "piso enquanto os estados dobram; a conta paga o expoente da carga, não os estados "
            "(`a_conta_de_luz_de_m_nomes`, `cada_nome_custa_um_piso`, `a_eletricidade_paga_o_expoente`). A máquina da teoria "
            "acerta no patamar plano com um número de passos linear, k ≤ n·ln 2/(−ln(1−β)) + 1, e paga a carga com sobra de "
            "menos de um passo (`a_maquina_da_teoria_acerta_pagando_no_piso`; a face discreta de "
            "`TempoIgualMoeda.o_tempo_e_linear_nas_oitavas`). O leitor por plano da casa, que na família `coupled` faz ao "
            "menos 2^(m+1) movimentos (`Codex.PlanTravel.coupled_physical_lower`), paga ao menos 2^(m+1) pisos se apaga um "
            "bit por movimento, hipótese nomeada (`o_leitor_que_apaga_paga_a_potencia`). Síntese: "
            "`a_maquina_nua_paga_em_eletricidade`. Compila na caixa da v412 com 65 de 65 relatórios no trio.\n\n"
            "**O que o termo não diz:** o piso de Landauer (1961) é o mínimo por bit apagado, não a conta; uma máquina "
            "reversível (Bennett, 1973) pode chegar perto dele sem encurtar os passos. A pergunta do Instituto conta passos "
            "de uma máquina de Turing, não energia: a conta de luz não a decide [OPEN]. O piso de Landauer é térmico; o custo "
            "geométrico β não depende de temperatura (`the_two_floors_are_not_the_same`).\n\n"
            "Estatuto: [INPUT/ONTO] a leitura do operador; [REAL no sandbox] os termos; [KNOWN] Landauer e Bennett; [OPEN] "
            "os passos da máquina de Turing nua. Validade no kernel não é creditação; o gate não se move.") % ORD[n], "4")
