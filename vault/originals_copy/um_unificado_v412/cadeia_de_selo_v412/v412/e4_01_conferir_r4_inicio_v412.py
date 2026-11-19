"""R4: confere por sha16 os insumos que o contrato R4 pina; compara os manifestos R5 e R7 (40 iguais? 2 novos?); procura numero 40 fixo nos scripts do kernel."""
import hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
h16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
for rel, esp in (("CONTRATO_v412_R4.md", None), ("contrato_REV4/CONTRATO_v412_R4.md", None), ("insumos/MANIFESTO_PEDRAS_v412_R7.json", "038d9074cccee647"), ("insumos/ANCORAS_PROPOSTAS_v412_R7.json", "cd8e933ba33a51bd"),
                 ("o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "256a71e1bdf03239"), ("insumos/MARCADORES_HERDADOS_v412.json", "b67d78def8c63f64")):
    p = D / rel
    print("%-70s %s %s %s" % (rel, h16(p), esp, "OK" if esp is None or h16(p) == esp else "DIVERGE"), p.stat().st_size)
print("sha256 R4 == copia congelada:", hashlib.sha256((D / "CONTRATO_v412_R4.md").read_bytes()).hexdigest() == hashlib.sha256((D / "contrato_REV4/CONTRATO_v412_R4.md").read_bytes()).hexdigest())
m5 = json.loads((D / "insumos/MANIFESTO_PEDRAS_v412_R5.json").read_bytes().decode("utf-8"))
m7 = json.loads((D / "insumos/MANIFESTO_PEDRAS_v412_R7.json").read_bytes().decode("utf-8"))
print("chaves R7:", list(m7.keys()))
print("n_modulos R5/R7:", m5.get("n_modulos"), m7.get("n_modulos"))
print("novas_em_relacao_a_quinta_lista:", m7.get("novas_em_relacao_a_quinta_lista"))
print("mudaram_da_sexta_lista:", m7.get("mudaram_da_sexta_lista"))
print("mudaram_da_quarta_lista (R7):", m7.get("mudaram_da_quarta_lista"))
# lista de modulos e sha256
def mods(m):
    for k in ("modulos", "pedras", "lista"):
        if k in m:
            return m[k]
    return None
a, b = mods(m5), mods(m7)
print("tipo das listas:", type(a).__name__, type(b).__name__)
def idx(x):
    if isinstance(x, dict):
        return x
    return {(e.get("modulo") or e.get("nome")): e for e in x}
ia, ib = idx(a), idx(b)
print("so' na R7:", sorted(set(ib) - set(ia)), "so' na R5:", sorted(set(ia) - set(ib)))
cmp = []
for k in sorted(set(ia) & set(ib)):
    sa = {kk: vv for kk, vv in ia[k].items() if "sha256" in kk}; sb = {kk: vv for kk, vv in ib[k].items() if "sha256" in kk}
    if sa != sb:
        cmp.append(k)
print("modulos comuns com sha256 diferente (R5 x R7):", cmp)
print("exemplo de entrada R7:", {k: str(v)[:70] for k, v in list(ib[sorted(ib)[0]].items())[:12]})
# 40 fixo nos scripts do kernel
for f in ["preparar_bundle_v412.py", "pos_build_kernel_v412_c4.py", "pos_build_kernel_v412_r4.py", "reconstruir_kernel_v412_r3.py", "conferir_ancoras_propostas_v412_r3.py", "pre_colisao_declaracoes_v412_r3.py", "conferir_quinta_lista_v412.py", "copiar_logs_do_kernel_v412.py", "construir_kernel_v412.sh", "lean_texto_v412.py"]:
    p = D / f
    if p.exists():
        t = p.read_bytes().decode("utf-8")
        hits = [(i + 1, l.strip()[:120]) for i, l in enumerate(t.split("\n")) if re.search(r"\b40\b|quarenta|== 40", l)]
        print(f, len(hits), hits[:6])
