# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a correcao de texto do modulo do kernel TGLExt.OResumoEPsiBit para a v413 (aprovada no
parecer consolidado do Codex, item 8). So' a docstring de a_atualizacao_pela_clausula_seguinte muda: o integrando e' o
peso de cada atribuicao no prefixo, nao o resumo anterior; a fibra pode ser o universo quando a fronteira nova e' vazia.
Origem: o arquivo da caixa da v412 (C:\\t\\k412c\\final, identico ao do um.py selado). Saida:
insumos\\kernel_edits\\TGLExt\\OResumoEPsiBit.lean, com o codigo (fora de comentarios) conferido identico; depois
compila como TGLExt.OResumoEPsiBit sobre a caixa e audita os axiomas de todo teorema publico."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
ORIG = Path(r"C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean")
RAIZ = AQUI / "kernel_edits"
DEST = RAIZ / "TGLExt" / "OResumoEPsiBit.lean"
sys.path.insert(0, str(AQUI))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ANTES = ("/-- ★ **A ATUALIZAÇÃO PELA CLÁUSULA SEGUINTE**: o resumo novo, na célula `u`, é a soma sobre a fibra de `u` do resumo\n"
         "velho vezes o fator da cláusula lida — estender pagando ou não pagando, depois contrair. A fibra nunca é o universo:\n"
         "é a célula da fronteira. -/\n")
DEPOIS = ("/-- ★ **A ATUALIZAÇÃO PELA CLÁUSULA SEGUINTE**: o resumo novo, na célula `u`, é a soma, sobre a fibra de `u` na\n"
          "fronteira nova, do peso de cada atribuição nas `j` cláusulas lidas vezes o fator da cláusula seguinte. O integrando é o\n"
          "peso de cada atribuição, não o resumo anterior; a fibra é a célula da fronteira nova, e é o universo das atribuições\n"
          "quando essa fronteira é vazia (por exemplo, ao fim da fórmula). -/\n")
t = ORIG.read_bytes().decode("utf-8")
assert "\r" not in t and t.count(ANTES) == 1
novo = t.replace(ANTES, DEPOIS)


def sem_comentarios(s):
    out, i, n, prof = [], 0, len(s), 0
    while i < n:
        if s.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and s.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if s.startswith("--", i):
            while i < n and s[i] != "\n":
                i += 1
            continue
        out.append(s[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


assert sem_comentarios(t) == sem_comentarios(novo), "o codigo mudou"
DEST.parent.mkdir(parents=True, exist_ok=True)
dados = novo.encode("utf-8")
tmp = DEST.with_name(DEST.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(DEST)
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "origem": str(ORIG), "sha256_origem": sha(ORIG),
       "saida": str(DEST), "sha256_saida": sha(DEST), "codigo_identico": True, "antes": ANTES, "depois": DEPOIS,
       "fundamento": str(AQUI.parent / "revisao_codex" / "CODEX_CONSOLIDADO_R3" / "PARECER.md") + " (item 8)",
       "sha256_fundamento": sha(AQUI.parent / "revisao_codex" / "CODEX_CONSOLIDADO_R3" / "PARECER.md")}
d = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = RAIZ / "ERRATA_OResumoEPsiBit.json.tmp"
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(RAIZ / "ERRATA_OResumoEPsiBit.json")
print("OResumoEPsiBit: origem %s -> saida %s | codigo identico | %d -> %d B" % (
    sha(ORIG)[:16], sha(DEST)[:16], len(t.encode("utf-8")), len(dados)))
