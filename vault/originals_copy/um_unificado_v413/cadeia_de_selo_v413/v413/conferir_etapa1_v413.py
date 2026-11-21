# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: confere, por conta propria, o fecho da Etapa 1 da v413 (quem constroi nao aprova). Le o
PRONTO_PARA_CANDIDATO_v413.json e os recibos do kernel; confere no sandbox C:\\t\\k413c\\final que (a) os 21 modulos novos
estao em TGLExt com o texto das pedras limpas menos as linhas #print axioms do fim, (b) o OResumoEPsiBit e' o corrigido,
(c) a raiz TGLExt.lean importa os 21, (d) as fontes antigas sao as do Nos (amostra: todas as que nao mudaram), e imprime a
escada e o relatorio de axiomas lidos dos recibos. So' le. Recibo: CONFERENCIA_ETAPA1_v413.json."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
SB = Path(r"C:\t\k413c\final")
NOSK = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
PL = V / "insumos" / "pedras_limpas" / "TGLExt"
KE = V / "insumos" / "kernel_edits" / "TGLExt" / "OResumoEPsiBit.lean"
MAN = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v413.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sem_print(t):
    """tira TODA linha #print axioms (o instalador as tira onde estiverem, inclusive antes do `end` do namespace) e as
    linhas vazias que sobram no fim."""
    linhas = [l for l in t.split("\n") if not l.startswith("#print axioms")]
    return "\n".join(linhas).rstrip("\n")


pronto = json.loads((V / "PRONTO_PARA_CANDIDATO_v413.json").read_text(encoding="utf-8"))
res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "pronto_sha256": sha(V / "PRONTO_PARA_CANDIDATO_v413.json")}
novos = sorted(m.split(".", 1)[1] for m in MAN["modulos_novos"])
dif = []
for m in novos:
    inst = (SB / "TGLExt" / (m + ".lean")).read_text(encoding="utf-8")
    fonte = (PL / (m + ".lean")).read_text(encoding="utf-8")
    if sem_print(inst) != sem_print(fonte) or "#print axioms" in inst:
        dif.append(m)
res["novos_iguais_as_pedras_sem_print"] = len(novos) - len(dif)
res["novos_divergentes"] = dif
k_inst = (SB / "TGLExt" / "OResumoEPsiBit.lean").read_text(encoding="utf-8")
res["oresumo_corrigido"] = sem_print(k_inst) == sem_print(KE.read_text(encoding="utf-8"))
raiz = (SB / "TGLExt.lean").read_text(encoding="utf-8")
res["raiz_importa_os_21"] = all(("import TGLExt.%s\n" % m) in raiz for m in novos)
mudados = set(novos) | {"OResumoEPsiBit"}
iguais, diverg = 0, []
for f in sorted(NOSK.glob("TGLExt/*.lean")):
    if f.stem in mudados:
        continue
    g = SB / "TGLExt" / f.name
    if g.exists() and sha(g) == sha(f):
        iguais += 1
    else:
        diverg.append(f.name)
res["antigos_iguais_ao_nos"] = iguais
res["antigos_divergentes"] = diverg[:20]
achatado = json.dumps(pronto, ensure_ascii=False)
for chave in ("escada", "bandeiras", "declaracoes", "teoremas", "checagens"):
    m = re.findall(r'"([^"]*%s[^"]*)":\s*(\[[^\]]*\]|[0-9]+|"[^"]*"|true|false)' % chave, achatado)
    res["pronto_" + chave] = m[:8]
res["bom"] = (not dif) and res["oresumo_corrigido"] and res["raiz_importa_os_21"] and not diverg
d = json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")
tmp = V / "CONFERENCIA_ETAPA1_v413.json.tmp"
tmp.write_bytes(d)
tmp.replace(V / "CONFERENCIA_ETAPA1_v413.json")
print("novos iguais as pedras (sem #print): %d/21 | OResumo corrigido %s | raiz importa os 21 %s | antigos iguais ao Nos %d, "
      "divergentes %d | bom %s" % (res["novos_iguais_as_pedras_sem_print"], res["oresumo_corrigido"], res["raiz_importa_os_21"],
                                   iguais, len(diverg), res["bom"]))
for k in ("pronto_escada", "pronto_bandeiras", "pronto_declaracoes", "pronto_teoremas", "pronto_checagens"):
    print(k, res[k][:4])
