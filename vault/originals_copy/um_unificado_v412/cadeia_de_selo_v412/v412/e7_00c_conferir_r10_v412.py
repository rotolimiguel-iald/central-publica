"""R10, bloco 0b: confere por sha16 lido de cada arquivo o contrato R10 e a pagina R24; a copia congelada do contrato; que o R10 pina os mesmos manifesto e ancoras R11 do R7; que as palavras de veredito dos cinco registros sao as mesmas do R7
(copiadas por script do texto do contrato); mede o que mudou da R22 para a R24. Grava INICIO_R10_v412.json e o estado."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
ex = L.Exame("inicio_R10")
ESPERADO = [("CONTRATO_v412_R10.md", "c1305cad6036468b"), ("o_que_fica_claro_REV24/O_QUE_FICA_CLARO_v412_R24.md", "4869b970c17eacf4"), ("insumos/MANIFESTO_PEDRAS_v412_R11.json", "63b37d347da3c2c1"),
            ("insumos/ANCORAS_PROPOSTAS_v412_R11.json", "cd9155b05c9dbae6"), ("CONTRATO_v412_R7.md", "482955270f39acc5"), ("o_que_fica_claro_REV21/O_QUE_FICA_CLARO_v412_R21.md", "629cd08a0f8f779e")]
lidos = {}
for rel, esp in ESPERADO:
    p = D / rel; h = L.sha16_arq(p)
    lidos[rel] = {"sha16_lido": h, "sha16_esperado": esp, "bytes": p.stat().st_size}
    ex.chk("sha16 de " + rel, h == esp, 1, {"lido": h, "esperado": esp})
    print("%-60s %s %s %s" % (rel, h, esp, "OK" if h == esp else "DIVERGE"))
r8 = (D / "CONTRATO_v412_R10.md").read_bytes().decode("utf-8").replace("\r\n", "\n"); r7 = (D / "CONTRATO_v412_R7.md").read_bytes().decode("utf-8").replace("\r\n", "\n")
ex.chk("a copia congelada do contrato (contrato_REV10) e' igual por sha256", L.sha256_arq(D / "contrato_REV10" / "CONTRATO_v412_R10.md") == L.sha256_arq(D / "CONTRATO_v412_R10.md"), 1)
m = re.search(r"o_que_fica_claro_REV24\\O_QUE_FICA_CLARO_v412_R24\.md` \(sha16 `([0-9a-f]{16})`; (\d+) bytes\)", r8)
ex.chk("o contrato R10 pina a pagina R24 (sha16 e bytes)", bool(m) and m.group(1) == lidos[ESPERADO[1][0]]["sha16_lido"] and int(m.group(2)) == (D / ESPERADO[1][0]).stat().st_size, 1, m.groups() if m else None)
mm = re.search(r"insumos\\MANIFESTO_PEDRAS_v412_R11\.json` \(sha16 `([0-9a-f]{16})`\)", r8); aa = re.search(r"insumos\\ANCORAS_PROPOSTAS_v412_R11\.json` \(sha16 `([0-9a-f]{16})`\)", r8)
ex.chk("o R10 pina o mesmo manifesto e as mesmas ancoras R11", bool(mm and aa) and mm.group(1) == "63b37d347da3c2c1" and aa.group(1) == "cd9155b05c9dbae6", 2, [mm and mm.group(1), aa and aa.group(1)])
nomes = ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]
pal = {}
for nome in nomes:
    a8 = re.findall(r"^- `%s`\n  `([A-Z0-9_]+)`" % nome, r8, re.M); a7 = re.findall(r"^- `%s`\n  `([A-Z0-9_]+)`" % nome, r7, re.M)
    pal[nome] = {"r8": len(a8), "r7": len(a7), "iguais": a8 == a7 and len(a8) == 1}
ex.chk("as cinco palavras de veredito do R10 sao as do R7 (uma de cada, iguais)", all(v["iguais"] for v in pal.values()), 5, pal)
rec = {"quando": L.agora(), "exame": ex.resumo(), "linhas": ex.linhas, "lidos": lidos, "palavras": pal}
L.salvar_json(D / "INICIO_R10_v412.json", rec)
print(json.dumps(ex.resumo(), ensure_ascii=False))
if not ex.ok:
    print("PARE: algo nao bate"); sys.exit(2)
L.estado_bloco("0c_contrato_r10", True, {"recibo": D / "INICIO_R10_v412.json", "contrato_r10": D / "CONTRATO_v412_R10.md", "pagina_r22": D / "o_que_fica_claro_REV24" / "O_QUE_FICA_CLARO_v412_R24.md"},
               nota="o contrato vigente passou a R10 (pagina R24; lista de pedras e ancoras R11 inalteradas); sha16 conferidos por script; o texto publico passa a ser montado pela R24",
               proximo="remontar a traducao EN pela R24 (e7_22b_en_r24_v412.py), os scripts _r7 (e7_04, e7_05, e7_06, e7_07, depois da build do kernel e7_02) e o texto publico (e7_23)")
