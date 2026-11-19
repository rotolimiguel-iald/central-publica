# -*- coding: utf-8 -*-
# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R5)] copia de conferir_nos_intacto_c4_v412.py para a DECIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R10.json, insumos\pedras_r10; 153 modulos); e5_02_derivar_scripts_r5_v412.py (trocas de texto exato com contagem registrada).
"""conferir_nos_intacto_r5_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) so' LEITURA do Nos. Confere, por script:
  (1) o sha256 do um.py do Nos tem o mesmo sha16 que o fecho R2 registra em base_v411.um_py_sha16 (e que o selo do Nos, e que a copia base_v411/um.py);
  (2) nenhum dos 153 modulos do manifesto R10 existe no kernel do Nos (tgl_kernel/TGLExt/<Modulo>.lean) e a raiz TGLExt.lean do Nos nao importa nenhum deles;
  (3) (informativo) arquivos do tgl_kernel do Nos e o um.py com data de modificacao posterior ao inicio da rodada (epoch lido de /c/t/k412c/reconstruir_r5_inicio_epoch.txt).
Grava kernel/NOS_INTACTO_R5_v412.json. Nada no Nos e' escrito.
uso: C:/Python314/python.exe -B -X utf8 conferir_nos_intacto_r5_v412.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
sha = lambda b: hashlib.sha256(b).hexdigest()
r2 = json.load(open(os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v412_R2.json"), encoding="utf-8"))
man = json.load(open(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R10.json"), encoding="utf-8"))
um_b = open(os.path.join(NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
base = json.load(open(os.path.join(HERE, "BASE_V411_COPIA.json"), encoding="utf-8"))
um_base = open(os.path.join(HERE, "base_v411", "um.py"), "rb").read()
falhas = []
sha16_r2 = (r2.get("base_v411") or {}).get("um_py_sha16")
if sha(um_b)[:16] != sha16_r2:
    falhas.append(["sha16 do um.py do Nos difere do fecho R2", sha(um_b)[:16], sha16_r2])
if um_b != um_base:
    falhas.append(["o um.py do Nos difere de base_v411/um.py em bytes"])
if selo.get("um_version") != "v411":
    falhas.append(["o selo do Nos nao e' v411", selo.get("um_version")])
kern = os.path.join(NOS, "tgl_kernel")
existem = [m["modulo"] for m in man["modulos"] if os.path.exists(os.path.join(kern, "TGLExt", m["modulo"] + ".lean"))]
if existem:
    falhas.append(["modulo do manifesto existe no kernel do Nos", existem])
raiz = open(os.path.join(kern, "TGLExt.lean"), "rb").read().decode("utf-8")
importados = [m["modulo"] for m in man["modulos"] if ("import TGLExt.%s" % m["modulo"]) in raiz]
if importados:
    falhas.append(["a raiz do Nos importa modulo do manifesto", importados])
ini = int(open(os.path.join("C:" + os.sep, "t", "k412c", "reconstruir_r5_inicio_epoch.txt")).read().strip())
mod_depois = []
for raiz_d, ds, fs in os.walk(kern):
    ds[:] = [d for d in ds if d not in (".lake",)]
    for f in fs:
        p = os.path.join(raiz_d, f)
        try:
            if os.path.getmtime(p) > ini:
                mod_depois.append(os.path.relpath(p, NOS))
        except OSError:
            pass
for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json"):
    p = os.path.join(NOS, f)
    if os.path.exists(p) and os.path.getmtime(p) > ini:
        mod_depois.append(f)
rep = {"um_py_sha256": sha(um_b), "um_py_sha16": sha(um_b)[:16], "um_py_sha16_no_fecho_R2": sha16_r2, "um_py_igual_ao_fecho_R2": sha(um_b)[:16] == sha16_r2, "um_py_igual_a_base_v411_em_bytes": um_b == um_base,
       "selo_do_nos_um_version": selo.get("um_version"), "n_modulos_do_manifesto_R10": len(man["modulos"]), "modulos_que_existem_no_kernel_do_Nos": existem, "modulos_importados_pela_raiz_do_Nos": importados,
       "informativo_modificados_no_Nos_apos_o_inicio_da_rodada": sorted(mod_depois)[:50], "n_modificados_no_Nos_apos_o_inicio_da_rodada": len(mod_depois), "falhas": falhas,
       "metodo": "so' leitura; sha256 dos bytes; existencia de arquivo; texto da raiz; mtime (informativo, outras sessoes podem tocar o Nos)"}
out = os.path.join(HERE, "kernel", "NOS_INTACTO_R5_v412.json")
with open(out + ".tmp", "w", encoding="utf-8") as fh:
    fh.write(json.dumps(rep, ensure_ascii=False, indent=1))
os.replace(out + ".tmp", out)
print(json.dumps({k: v for k, v in rep.items() if k != "metodo"}, ensure_ascii=False)[:1500], "| gravado sha16", sha(open(out, "rb").read())[:16])
sys.exit(1 if falhas else 0)
