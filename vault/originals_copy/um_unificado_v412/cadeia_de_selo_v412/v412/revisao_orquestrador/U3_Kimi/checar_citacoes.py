# -*- coding: utf-8 -*-
import os, re, sys

fonte = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV16\CopiadorEImpostor.lean"
raiz = r"C:\IALD\Central de Patentes\work\cunhagens_13out"

with open(fonte, 'rb') as f:
    texto = f.read().decode('utf-8')

# citacoes entre aspas angulares, uma por linha
citacoes = []
for i, linha in enumerate(texto.split('\n'), 1):
    for m in re.finditer('«([^»]+)»', linha):
        citacoes.append((i, m.group(1)))

# junta os bytes de todos os arquivos da pasta (recursivo)
arquivos = []
for dp, _, fs in os.walk(raiz):
    for fn in fs:
        p = os.path.join(dp, fn)
        try:
            with open(p, 'rb') as f:
                arquivos.append((p, f.read()))
        except Exception as e:
            print("ERRO lendo", p, e)

print(f"arquivos de fala lidos: {len(arquivos)}")
print(f"citacoes angulares na R7: {len(citacoes)}")
print()
for ln, c in citacoes:
    cb = c.encode('utf-8')
    achou = [p for p, b in arquivos if cb in b]
    if achou:
        print(f"OK   L{ln}: {os.path.basename(achou[0])}")
    else:
        print(f"FALHOU L{ln}: {c[:90]}")
