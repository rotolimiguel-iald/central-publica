"""Etapa 2, passo 0: confere por sha16 o contrato, a copia congelada, o fecho R3, a pagina R9 e as ancoras R5."""
import hashlib, json, sys
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


alvos = [
    (D / "CONTRATO_v412.md", "02b0f44e62aee5a5"),
    (D / "contrato_REV1" / "CONTRATO_v412.md", "02b0f44e62aee5a5"),
    (D / "PRONTO_PARA_CANDIDATO_v412_R3.json", "88fc32dbaf7d2008"),
    (D / "o_que_fica_claro_REV9" / "O_QUE_FICA_CLARO_v412_R9.md", "c17f2403f4a123c8"),
    (D / "insumos" / "ANCORAS_PROPOSTAS_v412_R5.json", "0fb86258327ec508"),
    (D / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json", "14dcf65ae9a5ed22"),
]
ok = True
for p, esperado in alvos:
    if not p.exists():
        print("AUSENTE", p)
        ok = False
        continue
    h = sha16(p)
    print(("OK   " if h == esperado else "DIVERGE"), h, esperado, p.name, p.stat().st_size)
    ok = ok and h == esperado
print("R2_do_contrato_existe:", (D / "CONTRATO_v412_R2.md").exists())
print("TUDO_OK" if ok else "PARAR")
sys.exit(0 if ok else 1)
