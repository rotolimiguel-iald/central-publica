# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ERRATA AO LADO, em nome proprio. Nos registros desta manha (Mapa seq 2186, ACOM d337, topico
da v413, Atlas) a gerencia escreveu que a casa prova polinomiais na fita 'Horn e as formulas de dois literais'. O
levantamento da fita da v412 (Mapa seq 2171) diz: Horn (CompilaHornNaFita.flat_horn_stages), as cadeias (FitaComCusto) e
as redes serie-paralelo de dois literais (FitaDeUmaCabeca.one_head_fixed_polynomial). Para TODA formula de dois literais,
o empurrao na morte imediata decide [KNOWN: Even-Itai-Shamir 1976; Aspvall-Plass-Tarjan 1979], e o kernel tem o fecho da
eliminacao de pares (EliminacaoDePares.binary_closed), nao a cota na fita. A correcao vai ao lado nas quatro superficies."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CEN = W.parents[3]
K = Path(r"C:\t\k412c\final\TGLExt")
for nome, t in (("CompilaHornNaFita.lean", "theorem flat_horn_stages"), ("FitaDeUmaCabeca.lean", "theorem one_head_fixed_polynomial"),
                ("EliminacaoDePares.lean", "theorem binary_closed")):
    assert t in (K / nome).read_text(encoding="utf-8"), nome


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


CORRETO = ("na fita, a casa prova a cota polinomial para Horn (flat_horn_stages), para as cadeias (FitaComCusto) e para as redes "
           "serie-paralelo de dois literais (one_head_fixed_polynomial); para TODA formula de dois literais o empurrao na morte "
           "imediata decide em tempo polinomial [KNOWN: Even-Itai-Shamir 1976; Aspvall-Plass-Tarjan 1979], e o kernel tem o "
           "fecho da eliminacao de pares (binary_closed), nao a cota na fita")

# (1) Mapa: ERRATA ao lado do seq 2186
err = {"tipo": "ERRATA", "rota_id": "kernel.traducao_cook_levin.a_inclinacao_do_nome_20nov", "corrige": 2186,
       "dominio": "KERNEL_FORMAL", "titulo": "errata ao lado (gerencia c1, em nome proprio): o que a casa prova na fita",
       "resultado": "onde o seq 2186 diz 'a casa prova as duas classes polinomiais na fita (Horn e dois literais)', leia-se: " + CORRETO,
       "estatuto": "REAL (os termos citados); KNOWN (Even-Itai-Shamir; Aspvall-Plass-Tarjan)", "status": "EXAMINADA",
       "olhou_dados": False, "onde": str(W), "artefatos": [str(K / "FitaDeUmaCabeca.lean"), str(K / "EliminacaoDePares.lean")],
       "nota": "achado da propria gerencia ao reler antes de responder"}
pj = W / "errata_rota_inclinacao_20nov.json"
pj.write_text(json.dumps(err, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(1) errata no Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

# (2) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 364,
       "event_id": "c1-20nov-d338-errata-o-que-a-casa-prova-na-fita",
       "changes": {"records": [
           {"id": "c1-20nov-d338-errata-dois-literais", "kind": "fact", "statute": "REAL",
            "text": ("Correcao ao lado do registro c1-20nov-d337-a-inclinacao-do-nome-nos-termos-do-kernel, em nome proprio da "
                     "gerencia: onde diz 'polinomial em Horn e dois literais (provado na fita)', leia-se: " + CORRETO + "."),
            "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (K / "FitaDeUmaCabeca.lean", sha(K / "FitaDeUmaCabeca.lean"))},
                        {"kind": "artifact", "ref": "%s#sha256:%s" % (K / "EliminacaoDePares.lean", sha(K / "EliminacaoDePares.lean"))}]}]}}
(W / "acom_c1_20261120_d338_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d338_transition.receipt.json").write_bytes(r.stdout)
txt = r.stdout.decode("utf-8", "replace")
print("(2) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in txt, txt[txt.find('"revision"'):][:20]))
assert '"ok": true' in txt


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


CORRETO_PT = ("na fita, a casa prova a cota polinomial para Horn (`flat_horn_stages`), para as cadeias (`FitaComCusto`) e para as "
              "redes série-paralelo de dois literais (`one_head_fixed_polynomial`); para toda fórmula de dois literais, o "
              "empurrão na morte imediata decide em tempo polinomial [KNOWN: Even–Itai–Shamir 1976; Aspvall–Plass–Tarjan 1979], e "
              "o kernel tem o fecho da eliminação de pares (`binary_closed`), não a cota na fita")
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
acrescenta(T, "<!-- errata_20nov_o_que_a_casa_prova_na_fita -->",
           ("**ERRATA AO LADO (20/11/2026, gerência c1, em nome próprio):** na nota acima, onde diz «polinomial em Horn e dois "
            "literais, provado na fita», leia-se: %s. Mapa: ERRATA ao lado do seq 2186.") % CORRETO_PT, "3")
A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- errata_20nov_o_que_a_casa_prova_na_fita -->",
           ("**ERRATA AO LADO do registro acima (20/11/2026, gerência c1, em nome próprio):** onde diz «decide Horn e as fórmulas "
            "de dois literais, que a casa prova polinomiais na fita», leia-se: %s. O registro acima fica como está.") % CORRETO_PT,
           "4")
