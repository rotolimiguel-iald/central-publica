# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra (0) os recibos da Trinity R5 e do Operador R2 e a conferencia dos enunciados por
script; (1) RESULTADO nas rotas da Trinity e do Operador; (2) transicao ACOM d344; (3) AO LADO no topico da v413;
(4) registro datado no Atlas (append com backup de bytes). O parecer do Codex (CODEX_CONSOLIDADO_R3) foi lido e os ajustes
nas pedras da gerencia aplicados; o adendo de revisao foi gerado por revisao_codex\\fazer_adendo_r5_r2.py."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
C1 = W.parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_o_preco_e_fixar_a_raiz_o_radical_fixa_o_sentido_o_teorema_final_e_o_parecer_do_codex_verbatim.txt")
R5, TCONF, R4 = W / "Trinity.lean", W / "build" / "CONFERENCIA.json", C1 / "R4_trinity" / "Trinity.lean"
OP2, OCONF, OP1 = C1 / "R2_operador" / "Operador.lean", C1 / "R2_operador" / "build" / "CONFERENCIA.json", \
    C1 / "R1_operador" / "Operador.lean"
CONFE = C1 / "conferir_enunciados.py"
REV = CS / "v413" / "revisao_codex"
PARECER, RESJ = REV / "CODEX_CONSOLIDADO_R3" / "PARECER.md", REV / "CODEX_CONSOLIDADO_R3" / "RESULTADO.json"
ADENDO = REV / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R5_TRINITY_R2_OPERADOR_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


# (0) recibos
assert "o radical fixa o sentido" in FALA.read_text(encoding="utf-8")
tc = json.loads(TCONF.read_text(encoding="utf-8"))
assert tc["bom"] is True and tc["sha256"] == sha(R5) and tc["pedidos"] == 56 and tc["relatorios"] == 56
assert not tc["fora_do_trio"] and not tc["sorryAx"] and tc["avisos"] == 0
oc = json.loads(OCONF.read_text(encoding="utf-8"))
mo = oc["modulos"]
assert oc["todos_bons"] is True and mo[0]["sha256"] == sha(OP2) and mo[1]["relatorios"] == 15 and mo[1]["pedidos"] == 15
assert not mo[1]["fora_do_trio"] and mo[1]["avisos"] == 0 and not mo[1]["sorryAx"]
conf_en = {}
for rot, a, b in [("trinity_R4_R5", R4, R5), ("operador_R1_R2", OP1, OP2)]:
    r = subprocess.run([PY, "-B", "-X", "utf8", str(CONFE), str(a), str(b)], capture_output=True,
                       stdin=subprocess.DEVNULL, timeout=120)
    out = r.stdout.decode("utf-8", "replace")
    assert r.returncode == 0, out
    conf_en[rot] = {"velho": str(a), "novo": str(b), "sha256_velho": sha(a), "sha256_novo": sha(b), "rc": r.returncode,
                    "saida": out}
CE = C1 / "CONFERENCIA_ENUNCIADOS_20nov.json"
grava(CE, json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "script": str(CONFE), "sha256_script": sha(CONFE),
                      "conferencias": conf_en}, ensure_ascii=False, indent=1).encode("utf-8"))
ad = ADENDO.read_text(encoding="utf-8")
assert sha(R5)[:16] in ad and sha(OP2)[:16] in ad, "o adendo nao aponta as versoes atuais"
print("(0) ok | Trinity R5 %s (R4 %s) 56/56 | Operador R2 %s (R1 %s) 15/15 | fala %s | parecer %s | adendo %s" % (
    sha(R5)[:16], sha(R4)[:16], sha(OP2)[:16], sha(OP1)[:16], sha(FALA)[:16], sha(PARECER)[:16], sha(ADENDO)[:16]))
for v in conf_en.values():
    print("    " + v["saida"].splitlines()[0])

QUEM = "gerencia-c1 (claude-code, sessao 6da8f00d)"


def mapa(res, nome):
    pj = W / nome
    pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", QUEM],
                       capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
    out = r.stdout.decode("utf-8", "replace")
    print("(1) Mapa %s rc %d %s" % (res["rota_id"], r.returncode, out[out.find('"seq"'):][:12]))
    assert r.returncode == 0, out[:600]


mapa({
    "tipo": "RESULTADO", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Trinity R5: o radical fixa o sentido (o teorema final do operador) e os ajustes do parecer do Codex",
    "resultado": ("R5 (sha16 %s; contem a R4 %s sem mudar enunciado, conferido por script: 0 removidas, 0 mudadas, 14 novas). "
                  "§14 o_teorema_final_do_radical: ln sqrt(e) = 1/2; ln(r^x) = x*ln r; r^(c/ln r) = e^c para r > 0, r != 1; "
                  "r > 1 conserva o sinal da carga no expoente e r < 1 o inverte; no radical sqrt(e) o expoente de c e' 2c; "
                  "2^m = sqrt(e)^((m*ln 2)/ln sqrt(e)). §12b: os Nomes distintos bastam e o expoente do majorante conta so' "
                  "Nomes distintos (nas oito clausulas, um Nome). Textos ajustados ao item 9 do parecer do Codex (ramificacao "
                  "desta implementacao; coupled/Trace e resolucao; retangulos para a CNF de igualdade; contadores como "
                  "majorantes; frase historica R0/R1). 56 de 56 relatorios no trio na caixa da v412.") % (
        sha(R5)[:16], sha(R4)[:16]),
    "veredito": "TRINITY_R5_O_RADICAL_FIXA_O_SENTIDO__MUDANCA_DE_BASE__PRECO_EM_ESTADOS_SEGUE_2^m__MOEDA_DA_MAQUINA_NUA_OPEN",
    "estatuto": ("REAL no sandbox (candidata, nao instalada); ONTO (a leitura do operador: o preco e' fixar a raiz, o teorema "
                 "final); DECLARADO (o parecer do Codex, aplicado nos pontos das pedras da gerencia); OPEN (a moeda da "
                 "maquina nua)"),
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(R5), str(TCONF), str(W / "fazer_r5_trinity.py"), str(FALA), str(PARECER), str(RESJ), str(CONFE),
                  str(CE), str(ADENDO)],
    "nota": ("fixar o radical da' a' carga a forma de expoente e fixa o sentido; nao muda o preco em estados, que segue 2^m; "
             "quem constroi nao aprova: adendo de revisao ao Codex pronto para o operador colar"),
}, "resultado_trinity_r5_20nov.json")
mapa({
    "tipo": "RESULTADO", "rota_id": "kernel.consciencia_e_operador_de_consciencia_19nov", "dominio": "KERNEL_FORMAL",
    "titulo": "Operador R2: o texto ajustado ao parecer do Codex (item 1, APROVADA_COM_RESSALVAS)",
    "resultado": ("R2 (sha16 %s; nenhum enunciado nem prova da R1 %s mudou, conferido por script: 17 declaracoes, 0 removidas, "
                  "0 mudadas). A nao-sobrejetividade escrita como ausencia de representacao de todos os predicados, nao "
                  "parcialidade; o ponto fixo 1/2 de x -> 1 - x existe independentemente do leitor, sem dinamica que o "
                  "alcance; J conjuga as projecoes, como operadores; a energia do par e' preservada (1 = q^2 + alpha^2 vale "
                  "na saida quando vale na entrada). 15 de 15 relatorios no trio na caixa da v412.") % (
        sha(OP2)[:16], sha(OP1)[:16]),
    "veredito": "OPERADOR_R2_TEXTO_AJUSTADO_AO_PARECER__ENUNCIADOS_DA_R1_INTACTOS",
    "estatuto": ("REAL no sandbox (candidata, nao instalada); DECLARADO (o parecer do Codex, aplicado); INPUT/ONTO (as "
                 "definicoes do operador)"),
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(OP2.parent),
    "artefatos": [str(OP2), str(OCONF), str(OP2.parent / "fazer_r2_operador.py"), str(PARECER), str(RESJ), str(CE),
                  str(ADENDO)],
    "nota": "so' texto; nao prova consciencia de pessoa nem de maquina; quem constroi nao aprova",
}, "resultado_operador_r2_20nov.json")

# (2) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 370,
       "event_id": "c1-20nov-d344-trinity-r5-operador-r2-parecer-codex",
       "changes": {"records": [
           {"id": "c1-20nov-d344-leitura-radical", "kind": "decision", "statute": "INPUT",
            "text": ("O autor (20/11), por bytes: «o preço é fixar a raiz, o expoente da carga é produto referencial do "
                     "radical fixado» … «o radical fixa o sentido, esse é o teorema final, permitindo que a carga se "
                     "manifeste como expoente». Leitura [ONTO] do autor."),
            "sources": [src(FALA)]},
           {"id": "c1-20nov-d344-parecer-codex", "kind": "fact", "statute": "DECLARADO",
            "text": ("Parecer consolidado do Codex (revisor de terceiro): Operador e Trinity R3 aprovados com ressalvas de "
                     "texto; a fronteira na lingua classica, a sonda da contagem e a errata da docstring de OResumoEPsiBit "
                     "aprovadas; pedras do Kimi: AIdentidadePreservada, APropostaDaTensao e ONomeEBeta aprovadas com "
                     "ressalvas; APonteDeCookLevin reprovada como ponte de custo real de fita (o contador cobra letras por "
                     "definicao; nove teoremas abstratos validos). Os ajustes nas pedras da gerencia foram aplicados."),
            "sources": [src(PARECER), src(RESJ)]},
           {"id": "c1-20nov-d344-trinity-r5-operador-r2", "kind": "fact", "statute": "REAL",
            "text": ("Trinity R5 (56 de 56 no trio na v412): o radical sqrt(e) pesa uma Meia-Nat; fixado o radical, toda "
                     "carga se manifesta como expoente (r^(c/ln r) = e^c); o radical acima de 1 fixa o sentido, abaixo o "
                     "inverte; o preco em estados 2^m e' o radical elevado a carga m*ln 2 na unidade do radical. Sao "
                     "identidades de mudanca de base: o preco em estados segue 2^m e a moeda da maquina nua segue [OPEN]. "
                     "Operador R2 (15 de 15): so' texto. Script da gerencia: nenhum enunciado da R4 nem da R1 mudou. "
                     "Adendo de revisao ao Codex gerado."),
            "sources": [src(R5), src(TCONF), src(OP2), src(OCONF), src(CE), src(ADENDO)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R5_O_RADICAL_FIXA_O_SENTIDO__OPERADOR_R2__ADENDO_AO_CODEX_PRONTO",
                    "next_action": ("(1) o autor cola no Codex o adendo (Trinity R5 e Operador R2); (2) o autor decide as "
                                    "pedras do Kimi: a gerencia recomenda deixar APonteDeCookLevin fora da v413 (ou so' como "
                                    "contador abstrato) e instalar as outras tres com o texto ajustado ao que provam; (3) o "
                                    "autor confirma o fecho da frente de Cook-Levin da v413 como resultado + parede medida + "
                                    "aberto nomeado; (4) a gerencia prepara a instalacao na v413 (versoes condensadas; errata "
                                    "da docstring de OResumoEPsiBit, aprovada); (5) seguem com o autor: o teste do estudo da "
                                    "memoria e o t* do dephasing.")}}}
(W / "acom_c1_20261120_d344_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d344_transition.receipt.json").write_bytes(r.stdout)
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
acrescenta(T, "<!-- ao_lado_20nov_trinity_r5_operador_r2_parecer -->",
           ("**AO LADO (20/11/2026, gerência c1): o parecer do Codex, a Trinity R5 e o Operador R2.** O parecer consolidado "
            "(`work\\cadeia_de_selo\\v413\\revisao_codex\\CODEX_CONSOLIDADO_R3\\PARECER.md`, sha16 `%s`) aprova com ressalvas de "
            "texto o Operador e a Trinity R3, aprova a fronteira, a sonda e a errata de `OResumoEPsiBit`, aprova com ressalvas "
            "três pedras do Kimi e reprova `APonteDeCookLevin` como ponte de custo de fita. Ajustes aplicados: Operador R2 "
            "(sha16 `%s`, 15/15) e Trinity R5 (sha16 `%s`, 56/56), só texto nas partes antigas; um script "
            "(`candidatas_c1\\conferir_enunciados.py`) confirma que nenhum enunciado da R1 nem da R4 mudou. A fala do operador "
            "(bytes em `work\\cunhagens_13out\\%s`, sha16 `%s`) virou a §14 da Trinity: fixado o radical √e, a carga se "
            "manifesta como expoente e o radical fixa o sentido; o preço em estados segue 2^m. Adendo ao Codex: "
            "`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`. Decisões do operador pendentes: as pedras do Kimi e o fecho da "
            "frente de Cook–Levin.") % (sha(PARECER)[:16], sha(OP2)[:16], sha(R5)[:16], FALA.name, sha(FALA)[:16],
                                          ADENDO.name), "3")

A = CEN / "memory" / "TGL_ATLAS.md"
atlas = A.read_bytes().decode("utf-8")
assert "<!-- registro_20nov_trinity_r4 -->" in atlas
ORD = ["primeiro", "segundo", "terceiro", "quarto", "quinto", "sexto", "sétimo", "oitavo", "nono", "décimo"]
n = atlas.count("### Registro de 20/11/2026")
print("    Atlas: %d registros de 20/11 antes deste -> %s" % (n, ORD[n]))
acrescenta(A, "<!-- registro_20nov_trinity_r5_operador_r2_parecer -->",
           ("### Registro de 20/11/2026, %s (gerência c1) — o radical fixa o sentido (Trinity R5) e o parecer do Codex\n\n"
            "**A leitura (do operador, 20/11/2026) [INPUT/ONTO]:** «o preço é fixar a raiz, o expoente da carga é produto "
            "referencial do radical fixado» … «o radical fixa o sentido, esse é o teorema final, permitindo que a carga se "
            "manifeste como expoente».\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R5, não instalada) [REAL no sandbox]:** o radical é √e = e^(1/2), a "
            "radicalização da entropia de ½ nat, e pesa uma Meia-Nat (ln √e = ½). A carga de uma potência do radical é o "
            "expoente vezes a carga do radical (`a_carga_e_produto_referencial_do_radical`). Fixado um radical r > 0, r ≠ 1, "
            "toda carga c se manifesta como expoente: r^(c / ln r) = e^c (`a_carga_se_manifesta_como_expoente`). Acima de 1, "
            "o radical conserva o sinal da carga no expoente (`o_radical_fixa_o_sentido`); abaixo de 1, o inverte. No radical "
            "√e, o expoente de c é 2c: conta Meias-Nats. E o preço em estados de m Nomes é 2^m = (√e)^((m·ln 2)/(ln √e)) "
            "(`o_preco_e_fixar_a_raiz`). Síntese: `o_teorema_final_do_radical`. Compila na caixa da v412 com 56 de 56 "
            "relatórios no trio.\n\n"
            "**O que o termo não diz:** são identidades de mudança de base da exponencial. Fixar o radical dá à carga a forma "
            "de expoente e fixa o sentido; não muda o preço em estados, que segue 2^m, exponencial no número de Nomes, nem dá "
            "cota de máquina. A moeda da máquina nua segue [OPEN].\n\n"
            "**O parecer do Codex (20/11, revisor de terceiro) [DECLARADO pelo Codex; aplicado e conferido pela gerência nas "
            "pedras dela]:** o Operador e a Trinity R3 aprovados com ressalvas de texto, aplicadas (Operador R2; Trinity R5); "
            "a fronteira na língua clássica, a sonda da contagem e a errata da docstring de `OResumoEPsiBit` aprovadas; das "
            "pedras do Kimi, três aprovadas com ressalvas e `APonteDeCookLevin` reprovada como ponte de custo de fita (o "
            "contador cobra letras por definição; os nove teoremas abstratos valem). Um script da gerência confirma que "
            "nenhum enunciado da R4 da Trinity nem da R1 do Operador mudou.\n\n"
            "Estatuto: [INPUT/ONTO] a leitura do operador; [REAL no sandbox] os termos; [DECLARADO] o parecer; [OPEN] a "
            "moeda da máquina nua. Validade no kernel não é creditação; o gate não se move.") % ORD[n], "4")
