# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: passo 5 da NONA lista de pedras da v412 = a oitava (44 modulos, sem mudanca) mais TODAS as fontes novas de
pedras_novas\\ (ordem do autor de 18/11: entra tudo na v412), frente C (o leitor da formula). Exige: passo 3 com todos RC 0 e log da
fonte atual; passo 4 (tudo junto) com RC 0 sobre as MESMAS fontes; codigo de cada copia de trabalho identico ao da fonte do autor
(pedras_novas\\origem); a fonte do autor ainda igual, por sha256, ao que esta' na pasta dele (se a pasta dele mudou, PARA).
Congela os modulos em insumos\\pedras_r9 e grava MANIFESTO_PEDRAS_v412_R9.json; deriva e roda as ancoras R9 (registro novo
leitor_da_formula_v412; nos modulos sem estrela, as ancoras propostas sao as declaracoes que o proprio modulo lista em #print axioms).
Uso: nona_lista_passo5_manifesto.py [--executar]"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
LIMPAS, NOVAS, DEST = V / "pedras_limpas", V / "pedras_novas", V / "insumos" / "pedras_r9"
EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
man8 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R8.json").read_text(encoding="utf-8"))
orig = {o["modulo"]: o for o in json.loads((NOVAS / "ORIGENS.json").read_text(encoding="utf-8"))["itens"]}
emend = {m["modulo"]: m for m in json.loads((NOVAS / "EMENDAS_DE_COMENTARIO.json").read_text(encoding="utf-8"))["modulos"]}
junto = json.loads((NOVAS / "build" / "TUDO_JUNTO.json").read_text(encoding="utf-8"))
assert junto["rc"] == 0 and junto["erros"] == 0, "o teste de tudo junto nao passou"


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


itens = []
for m in man8["modulos"]:
    f = LIMPAS / (m["modulo"] + ".lean"); assert sha(f) == m["sha256"], "mudou desde a oitava lista: " + m["modulo"]
    log = (LIMPAS / "build" / (m["modulo"] + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + m["sha256"]) in log and re.search(r"^RC: 0\s*$", log, flags=re.M), "log: " + m["modulo"]
    it = dict(m, mudou_da_oitava_lista=False); it.pop("mudou_da_setima_lista", None); itens.append(it)
nomes_novos = sorted(p.stem for p in NOVAS.glob("*.lean"))
assert set(nomes_novos) == set(orig), set(nomes_novos) ^ set(orig)
RO = V / "revisao_orquestrador"
for nome in nomes_novos:
    f = NOVAS / (nome + ".lean"); b = f.read_bytes(); t = b.decode("utf-8"); o = orig[nome]
    fo = NOVAS / "origem" / (nome + ".lean"); assert sha(fo) == o["sha256_origem"], "origem mudou: " + nome
    pasta = {"candidatas_c1": V / "candidatas_c1", "candidatas_kimi": V / "candidatas_kimi"}.get(o["pasta_de_origem"], RO / o["pasta_de_origem"])
    assert sha(pasta / (nome + ".lean")) == o["sha256_origem"], "a fonte na pasta do autor mudou depois de trazida: " + nome
    assert sem_comentarios(fo.read_bytes().decode("utf-8")) == sem_comentarios(t), "codigo difere da fonte do autor: " + nome
    assert junto["sha256_das_novas"].get(nome) == sha(f), "o teste de tudo junto nao foi sobre esta fonte: " + nome
    log = (NOVAS / "build" / (nome + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + sha(f)) in log and re.search(r"^RC: 0\s*$", log, flags=re.M), "log: " + nome
    saida = log.split("SAIDA:\n", 1)[1]
    ax = [l for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
    fora = [l for l in ax if "sorryAx" in l or ("[" in l and not set(l.split("[", 1)[1].rstrip("]").replace(" ", "").split(",")) <= {"propext", "Classical.choice", "Quot.sound", ""})]
    assert not fora and "sorryAx" not in saida, "axiomas: " + nome
    imps = re.findall(r"^import\s+(\S+)", t, flags=re.M)
    itens.append({"modulo": nome, "frente": "C", "de_quem": o["de_quem"],
                  "estado_da_revisao": "nova, de 17 e 18/11; recompilada pela gerencia so' com o binario do Lean (RC 0, tres axiomas); " + ("comentarios ajustados pelo metodo de 17/11" if not emend[nome]["bytes_iguais"] else "bytes iguais aos da fonte do autor") + ("; SEM leitura de terceiro distinto de quem a escreveu" if o["de_quem"] == "gerencia" else ""),
                  "origem": str(f), "sha256": sha(f), "bytes": len(b), "pasta_do_autor": o["pasta_de_origem"], "fonte_revista_sha256": o["sha256_origem"],
                  "codigo_identico_ao_da_fonte_revista": True, "compilou_rc0_com_log_desta_fonte": True, "avisos_no_log": saida.count("warning:"),
                  "linhas_de_axiomas_no_log": len(ax), "imports": imps,
                  "imports_de_candidatas": [i for i in imps if not i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL."))],
                  "namespaces": re.findall(r"^namespace\s+(\S+)", t, flags=re.M),
                  "declaracoes_theorem_lemma": len(re.findall(r"^(?:theorem|lemma)\s", t, flags=re.M)),
                  "linhas_print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)),
                  "sorry": len(re.findall(r"\bsorry\b", re.sub(r"--.*", "", re.sub(r"/-.*?-/", "", t, flags=re.S)))), "mudou_da_oitava_lista": True})
nomes = {i["modulo"] for i in itens}; soltos = sorted({i for it in itens for i in it["imports_de_candidatas"]})
man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
       "nota": "nona lista, de 18/11: os 44 modulos da oitava, sem mudanca, mais todas as fontes novas do leitor da formula (frente C), de tres autores; cada log de compilacao e' da fonte congelada; o teste de tudo junto (kernel + 44 + novas) passou sobre estas mesmas fontes",
       "n_modulos": len(itens), "novas_em_relacao_a_oitava_lista": nomes_novos, "por_autor_nas_novas": {q: sum(1 for i in itens if i.get("frente") == "C" and i["de_quem"] == q) for q in ("gerencia", "Kimi", "Codex")},
       "ficam_fora": man8["ficam_fora"], "ficam_para_a_v413": [], "tudo_junto": {"rc": junto["rc"], "gerado_em": junto["gerado_em"], "importa": junto["importa"]},
       "imports_soltos_de_candidatas": soltos, "imports_soltos_sem_modulo_no_conjunto": [i for i in soltos if i not in nomes], "modulos": itens}
assert not man["imports_soltos_sem_modulo_no_conjunto"], man["imports_soltos_sem_modulo_no_conjunto"]
print("nona lista:", len(itens), "modulos (44 +", len(nomes_novos), ") | por autor nas novas:", man["por_autor_nas_novas"], "| declaracoes:", sum(i["declaracoes_theorem_lemma"] for i in itens), "| sorry:", sum(i["sorry"] for i in itens), "| avisos:", sum(i["avisos_no_log"] for i in itens))
if not EXEC:
    print("ENSAIO A SECO: nada congelado nem gravado."); sys.exit(0)
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    src = (NOVAS if it.get("frente") == "C" else LIMPAS) / (it["modulo"] + ".lean"); alvo = DEST / (it["modulo"] + ".lean"); b = src.read_bytes()
    if alvo.exists():
        assert alvo.read_bytes() == b, "ja' congelado e difere: " + it["modulo"]
    else:
        alvo.write_bytes(b)
out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R9.json"; assert not out.exists(), "ja' existe"
out.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
print("manifesto R9 gravado | sha16", sha(out)[:16])
a8 = (V / "ancoras_propostas_v412_r8.py").read_text(encoding="utf-8")
a9 = a8.replace("MANIFESTO_PEDRAS_v412_R8.json", "MANIFESTO_PEDRAS_v412_R9.json").replace('"pedras_r8"', '"pedras_r9"').replace("ANCORAS_PROPOSTAS_v412_R8.json", "ANCORAS_PROPOSTAS_v412_R9.json")
marca = "\n}\nde = {m: r for r, ms in REG.items() for m in ms}"
assert a9.count(marca) == 1
a9 = a9.replace(marca, '\n    "leitor_da_formula_v412": ' + json.dumps(nomes_novos, ensure_ascii=False) + ",   # (nona lista, 18/11: a frente C)" + marca)
velho = '"sem_estrela": [d["nome"] for d in decls if not d["estrela"]]})'
assert a9.count(velho) == 1
a9 = a9.replace(velho, '"sem_estrela": [d["nome"] for d in decls if not d["estrela"]],\n                                                  "listadas_em_print_axioms": [x.split(".")[-1] for x in re.findall(r"^#print axioms\\s+(\\S+)", t, flags=re.M)]})')
p9 = V / "ancoras_propostas_v412_r9.py"; assert not p9.exists(); p9.write_bytes(a9.encode("utf-8"))
ra = subprocess.run([sys.executable, "-B", "-X", "utf8", str(p9), "--executar"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("\n".join((ra.stdout or "").strip().split("\n")[-3:])); assert ra.returncode == 0, ra.stderr[-1500:]
