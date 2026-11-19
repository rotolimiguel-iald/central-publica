# -*- coding: utf-8 -*-
"""Revisor Kimi, ORDEM 018, U1: confere por BYTES cada citacao entre aspas angulares do
DESENHO_DO_TESTE_R6_GERENCIA.md (REV1) contra os arquivos de fala em cunhagens_13out.
Cada citacao tem de estar numa linha so no desenho e ser subcadeia exata de UM arquivo de fala.
Tambem procura a citacao em TODOS os arquivos da pasta (para ver se o prefixo indicado aponta o arquivo certo)."""
import re, sys, hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DES = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\teste_frente_a_r6\REV1\DESENHO_DO_TESTE_R6_GERENCIA.md")
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")

txt = DES.read_text(encoding="utf-8")
linhas = txt.splitlines()

# extrai citacoes «...» com o numero da linha
cits = []
for i, ln in enumerate(linhas, 1):
    for m in re.finditer("«([^»]*)»", ln):
        cits.append((i, m.group(1)))

print("total de citacoes encontradas:", len(cits))
arquivos = list(CUN.glob("*.txt"))
cache = {a: a.read_bytes() for a in arquivos}
print("arquivos de fala na pasta:", len(arquivos))
print()

for i, (linha, cit) in enumerate(cits, 1):
    b = cit.encode("utf-8")
    hits = [a.name for a, conteudo in cache.items() if b in conteudo]
    # quebra de linha dentro da citacao? (a regra: cada uma numa linha)
    uma_linha = "\n" not in cit
    print(f"[{i:02d}] desenho linha {linha:4d} | uma_linha={uma_linha} | bytes={len(b)} | achados={len(hits)}")
    if hits:
        for h in hits:
            print("     em:", hits and hits[0] if False else "     em:", h)
    else:
        # tenta variante com espacos duplos / finais para diagnostico
        b2 = re.sub(r"\s+", " ", cit).strip().encode("utf-8")
        hits2 = [a.name for a, conteudo in cache.items() if b2 in re.sub(rb"\s+", b" ", conteudo)]
        print("     NAO achada por bytes. Normalizando espacos:", hits2 if hits2 else "tambem nao")
        print("     inicio:", cit[:90])
    print()

# sha256 dos arquivos apontados pelos prefixos da secao 2
print("=== sha256 dos arquivos referenciados ===")
for nome in sorted(n for n in cache if n.startswith("OPERADOR_1") and ("15nov" in n or "16nov" in n or "10nov" in n or "13nov" in n)):
    if any(k in nome for k in ("toda_leitura_e_copia", "o_impostor_e_o_falso", "ressalva_o_habitante", "o_unico_ato_do_verbo",
                               "o_fractal_e_espelho", "a_copia_governa", "o_nome_do_impostor", "a_sua_pergunta_ja",
                               "a_resposta_tecnica_pode", "e_isso_mesmo_confirmo", "poder_preditivo", "vamos_comecar")):
        print(hashlib.sha256(cache[[a for a in arquivos if a.name == nome][0]]).hexdigest()[:16], nome[:80])
