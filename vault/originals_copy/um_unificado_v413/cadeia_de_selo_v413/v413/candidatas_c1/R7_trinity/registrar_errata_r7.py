# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ERRATA AO LADO, em nome proprio da gerencia. A R6 da Trinity e o registro 2198 do Mapa
atribuiram ao operador a leitura de cada passo da maquina da teoria como energia; a fala dele, por bytes, e' so'
«A máquina nua paga em eletricidade». A R7 corrige o texto (nenhum enunciado mudou). Registra: (0) recibo da R7, conferencia
R6 -> R7 e adendo R7; (1) ERRATA no Mapa (corrige 2198); (2) transicao ACOM d346; (3) AO LADO no topico da v413."""
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
R7, CONF, R6 = W / "Trinity.lean", W / "build" / "CONFERENCIA.json", C1 / "R6_trinity" / "Trinity.lean"
CONFE = C1 / "conferir_enunciados.py"
REV = CS / "v413" / "revisao_codex"
ADENDO = REV / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R7_TRINITY_R2_OPERADOR_20nov.md"
ADENDO6 = REV / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R6_TRINITY_R2_OPERADOR_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


assert FALA.read_text(encoding="utf-8").strip() == "A máquina nua paga em eletricidade"
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(R7) and conf["pedidos"] == 65 and conf["relatorios"] == 65
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
r = subprocess.run([PY, "-B", "-X", "utf8", str(CONFE), str(R6), str(R7)], capture_output=True, stdin=subprocess.DEVNULL,
                   timeout=120)
saida = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0 and "novas 0" in saida, saida
CE = W / "CONFERENCIA_ENUNCIADOS_R6_R7.json"
grava(CE, json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "script": str(CONFE), "sha256_script": sha(CONFE),
                      "velho": str(R6), "sha256_velho": sha(R6), "novo": str(R7), "sha256_novo": sha(R7),
                      "rc": r.returncode, "saida": saida}, ensure_ascii=False, indent=1).encode("utf-8"))
ad = ADENDO.read_text(encoding="utf-8")
assert sha(R7)[:16] in ad and "leitura da gerência" in ad
t7 = R7.read_text(encoding="utf-8")
assert "(a leitura do\noperador [ONTO])" not in t7 and "leitura da\ngerência" in t7
print("(0) ok | R7 %s (R6 %s) 65/65 | adendo R7 %s (R6 %s fica como registro)\n    %s" % (
    sha(R7)[:16], sha(R6)[:16], sha(ADENDO)[:16], sha(ADENDO6)[:16], saida.splitlines()[0]))

err = {
    "tipo": "ERRATA", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "corrige": 2198, "dominio": "KERNEL_FORMAL",
    "titulo": ("ERRATA AO LADO (gerencia c1, em nome proprio): ler cada passo da maquina da teoria como energia e' leitura "
               "da gerencia, nao do operador"),
    "resultado": ("No registro 2198 o estatuto atribuiu ao operador duas leituras. A fala dele (bytes, sha16 %s) e' so' "
                  "«A máquina nua paga em eletricidade». A extensao a' maquina da teoria (cada passo lido como a carga "
                  "-ln(1-beta) paga em energia) e' da gerencia. A R7 (sha16 %s; so' texto; conferida por script contra a R6 "
                  "%s: 0 removidas, 0 mudadas, 0 novas; 65 de 65 no trio) corrige as duas docstrings. O adendo R7 ao Codex "
                  "(sha16 %s) substitui os da R5 e da R6, que ficam como registro.") % (
        sha(FALA)[:16], sha(R7)[:16], sha(R6)[:16], sha(ADENDO)[:16]),
    "veredito": "ERRATA_ATRIBUICAO__A_EXTENSAO_A_MAQUINA_DA_TEORIA_E_DA_GERENCIA__ENUNCIADOS_INTACTOS",
    "estatuto": "REAL (a correcao, conferida por script); ONTO (a extensao da gerencia)",
    "status": "EXAMINADA", "olhou_dados": False, "onde": str(W),
    "artefatos": [str(R7), str(CONF), str(W / "fazer_r7_trinity.py"), str(CE), str(ADENDO), str(FALA)],
    "nota": "atribuir ao operador so' por bytes; a correcao fica ao lado; a R6 e o registro 2198 ficam como estao",
}
pj = W / "errata_trinity_r6_r7_20nov.json"
pj.write_text(json.dumps(err, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(1) Mapa ERRATA rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 372,
       "event_id": "c1-20nov-d346-errata-atribuicao-trinity-r7",
       "changes": {"records": [
           {"id": "c1-20nov-d346-errata-atribuicao", "kind": "fact", "statute": "REAL",
            "text": ("ERRATA AO LADO (gerencia c1, em nome proprio): a R6 da Trinity e o registro 2198 do Mapa atribuiram ao "
                     "autor a leitura de cada passo da maquina da teoria como energia; a fala dele e' so' «A máquina nua paga "
                     "em eletricidade»; a extensao e' da gerencia. A R7 corrige o texto (65 de 65; nenhum enunciado mudou, "
                     "conferido por script); errata no Mapa; o adendo R7 ao Codex substitui os da R5 e da R6."),
            "sources": [src(R7), src(CONF), src(CE), src(ADENDO), src(FALA)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R7_ERRATA_DE_ATRIBUICAO__ADENDO_R7_AO_CODEX_PRONTO",
                    "next_action": ("(1) o autor cola no Codex o adendo R7 (Trinity R7 e Operador R2); (2) o autor decide as "
                                    "pedras do Kimi: a gerencia recomenda deixar APonteDeCookLevin fora da v413 (ou so' como "
                                    "contador abstrato) e instalar as outras tres com o texto ajustado ao que provam; (3) o "
                                    "autor confirma o fecho da frente de Cook-Levin da v413: resultado (a Trinity) + parede "
                                    "medida (na maquina nua que apaga a cada passo, a conta e' exponencial nos Nomes; o piso "
                                    "e' linear) + aberto nomeado (os passos da maquina de Turing nua); (4) a gerencia prepara "
                                    "a instalacao na v413 (versoes condensadas; errata da docstring de OResumoEPsiBit); (5) "
                                    "seguem com o autor: o teste do estudo da memoria e o t* do dephasing.")}}}
(W / "acom_c1_20261120_d346_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d346_transition.receipt.json").write_bytes(r.stdout)
t = r.stdout.decode("utf-8", "replace")
print("(2) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
marca = "<!-- ao_lado_20nov_errata_trinity_r7 -->"
a = T.read_bytes()
assert marca.encode() not in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
texto = ("**ERRATA AO LADO (20/11/2026, gerência c1, em nome próprio):** na R6 da Trinity e no registro 2198 do Mapa, a "
         "gerência atribuiu ao operador a leitura de cada passo da máquina da teoria como energia. A fala dele é só «A "
         "máquina nua paga em eletricidade»; a extensão é da gerência. A R7 (`candidatas_c1\\R7_trinity\\`, sha16 `%s`) "
         "corrige só o texto (65/65; nenhum enunciado da R6 mudou, conferido por script); ERRATA no Mapa. O adendo para "
         "colar no Codex passa a ser `work\\cadeia_de_selo\\v413\\revisao_codex\\%s`; os da R5 e da R6 ficam como registro.\n%s"
         ) % (sha(R7)[:16], ADENDO.name, marca)
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
