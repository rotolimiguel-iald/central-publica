# -*- coding: utf-8 -*-
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de guardar_r2_antes_do_r3_v412.py para a SETIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R7.json, insumos\pedras_r7; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de guardar_etapa1_antes_do_r2_v412.py (que guardava o estado da Etapa 1 com .bak_etapa1; este guarda o do R2 com .bak_r3) para a QUINTA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R5.json, insumos\pedras_r5); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
"""guardar_r3_antes_do_c4_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) copia de BYTES, com o sufixo `.bak_r3`, do estado do fecho R3 (quinta lista, 40 modulos) antes que a continuacao 2
(quinta lista, 40 modulos com seis emendados) regrave os recibos e os logs de kernel/. Nada e' apagado nem movido; se o `.bak_r3` ja existe, nao e' sobrescrito (confere-se so' que e' igual).
Cobre: kernel/* (inclusive kernel/bundle/*, menos o que ja' e' copia .bak e o CODIGO_R4_R5_v412.json, que nasceu depois), BUNDLE_v412.json, kernel_modulos_novos_v412.json, construir_kernel_v412.sh,
vinculo/CRITERIOS_v412.json, PRONTO_PARA_CANDIDATO_v412_R3.json, TAMANHOS_CRIADOS_v412_R3.json. NAO toca em nenhum original (so' cria os `.bak_r3`). Grava kernel/GUARDA_R3_v412.json (caminho, bytes, sha16 de cada copia).
uso: C:/Python314/python.exe -B -X utf8 guardar_r3_antes_do_c4_v412.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sha = lambda b: hashlib.sha256(b).hexdigest()
alvos = []
for raiz, _, nomes in os.walk(os.path.join(HERE, "kernel")):
    for n in nomes:
        if ".bak" in n or n.endswith(".tmp") or n in ("CODIGO_R4_R5_v412.json", "GUARDA_R2_v412.json"):
            continue
        alvos.append(os.path.join(raiz, n))
for rel in ("BUNDLE_v412.json", "kernel_modulos_novos_v412.json", "construir_kernel_v412.sh", os.path.join("vinculo", "CRITERIOS_v412.json"), "PRONTO_PARA_CANDIDATO_v412_R3.json", "TAMANHOS_CRIADOS_v412_R3.json"):
    p = os.path.join(HERE, rel)
    if os.path.exists(p):
        alvos.append(p)
rec = []; ja = 0; novos = 0; difere = []
for p in sorted(alvos):
    b = open(p, "rb").read(); bk = p + ".bak_r3"
    if os.path.exists(bk):
        if open(bk, "rb").read() == b:
            ja += 1
        else:
            difere.append(bk)   # o original mudou depois do backup (nao sobrescrito)
        continue
    tmp = bk + ".tmp"
    with open(tmp, "wb") as f:
        f.write(b)
    assert os.path.getsize(tmp) == len(b)
    os.replace(tmp, bk)
    assert open(bk, "rb").read() == b
    novos += 1
    rec.append({"arquivo": os.path.relpath(p, HERE), "backup": os.path.relpath(bk, HERE), "bytes": len(b), "sha16": sha(b)[:16]})
out = os.path.join(HERE, "kernel", "GUARDA_R3_v412.json")
dados = json.dumps({"quando": __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"), "novos": novos, "ja_existiam_iguais": ja, "backup_diverge_do_original": difere, "copias": rec}, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(out):
    os.replace(out, out + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"))
with open(out + ".tmp", "wb") as f:
    f.write(dados)
os.replace(out + ".tmp", out)
print("copias novas:", novos, "| ja existiam iguais:", ja, "| backup diverge:", difere, "| bytes copiados:", sum(r["bytes"] for r in rec))
