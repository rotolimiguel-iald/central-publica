# -*- coding: utf-8 -*-
"""Etapa 2 da v413: confere, por sha256 lido dos bytes, os seis insumos que a ordem pina.

Sai com codigo 0 se todos batem; 2 se algum diverge ou falta (fail-closed).
Grava CONFERENCIA_ENTRADA_ETAPA2_v413.json (por temporario e troca)."""
import hashlib
import json
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

ESPERADOS = [
    ("PRONTO_PARA_CANDIDATO_v413.json", "ea57114bfd524579"),
    ("CONTRATO_v413_R1.md", "e25a439a3c4e0de6"),
    (os.path.join("insumos", "MANIFESTO_PEDRAS_v413.json"), "08c5ef6bbfb74384"),
    (os.path.join("insumos", "ANCORAS_PROPOSTAS_v413.json"), "aaee9804be6bff61"),
    (os.path.join("o_que_fica_claro_v413", "O_QUE_FICA_CLARO_v413_R0.md"), "528d7a6606e77145"),
    ("INVENTARIO_CADEIA_v413.json", "39deb7ec0a85ec68"),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def main():
    linhas = []
    ok_total = True
    for rel, esperado in ESPERADOS:
        p = os.path.join(BASE, rel)
        if not os.path.isfile(p):
            linhas.append({"arquivo": rel, "esperado_sha16": esperado, "medido_sha16": None,
                           "bytes": None, "ok": False, "erro": "AUSENTE"})
            ok_total = False
            continue
        s = sha256_file(p)
        ok = s[:16] == esperado
        ok_total = ok_total and ok
        linhas.append({"arquivo": rel, "esperado_sha16": esperado, "medido_sha16": s[:16],
                       "sha256": s, "bytes": os.path.getsize(p), "ok": ok})
    # a copia congelada do contrato
    copia = os.path.join(BASE, "contrato_REV1")
    copias = []
    if os.path.isdir(copia):
        for nome in sorted(os.listdir(copia)):
            pp = os.path.join(copia, nome)
            if os.path.isfile(pp):
                s = sha256_file(pp)
                copias.append({"arquivo": os.path.join("contrato_REV1", nome), "sha16": s[:16],
                               "bytes": os.path.getsize(pp)})
    contrato_sha = next(x for x in linhas if x["arquivo"] == "CONTRATO_v413_R1.md").get("medido_sha16")
    copia_identica = any(c["sha16"] == contrato_sha and c["arquivo"].endswith(".md") for c in copias)
    ok_total = ok_total and copia_identica
    out = {
        "o_que_e": "conferencia de entrada da Etapa 2 da v413 (os seis sha16 pinados pela ordem)",
        "quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "linhas": linhas,
        "copias_contrato_REV1": copias,
        "copia_congelada_do_contrato_identica": copia_identica,
        "ok": ok_total,
    }
    dst = os.path.join(BASE, "CONFERENCIA_ENTRADA_ETAPA2_v413.json")
    tmp = dst + ".tmp"
    data = json.dumps(out, ensure_ascii=False, indent=2).encode("utf-8")
    with open(tmp, "wb") as f:
        f.write(data)
    if os.path.getsize(tmp) != len(data):
        print("FALHA: temporario com tamanho errado")
        sys.exit(3)
    os.replace(tmp, dst)
    for x in linhas:
        print(("OK  " if x["ok"] else "FALHA ") + x["arquivo"] + "  esperado " + x["esperado_sha16"]
              + "  medido " + str(x.get("medido_sha16")))
    for c in copias:
        print("copia " + c["arquivo"] + " " + c["sha16"])
    print("copia congelada identica:", copia_identica)
    print("RESULTADO:", "OK" if ok_total else "PARAR")
    sys.exit(0 if ok_total else 2)


if __name__ == "__main__":
    main()
