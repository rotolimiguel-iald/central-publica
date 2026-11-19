"""R11, bloco 0b: confere por sha16 lido de cada arquivo o contrato R11 e a pagina R25; a copia congelada do contrato; que o R11 pina os mesmos manifesto e ancoras R11 do R7; que as palavras de veredito dos cinco registros sao as mesmas do R7
(copiadas por script do texto do contrato); mede o que mudou da R24 para a R25. Grava INICIO_R11_v412.json e o estado."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
ex = L.Exame("inicio_R11")
ESPERADO = [("CONTRATO_v412_R11.md", "30fe6e3d93e9bc15"), ("o_que_fica_claro_REV25/O_QUE_FICA_CLARO_v412_R25.md", "ce313a4c57dec103"), ("insumos/MANIFESTO_PEDRAS_v412_R12.json", "1028adf7293b432f"),
            ("insumos/ANCORAS_PROPOSTAS_v412_R12.json", "31af18a86183002f"), ("CONTRATO_v412_R7.md", "482955270f39acc5"), ("o_que_fica_claro_REV21/O_QUE_FICA_CLARO_v412_R21.md", "629cd08a0f8f779e")]
lidos = {}
for rel, esp in ESPERADO:
    p = D / rel; h = L.sha16_arq(p)
    lidos[rel] = {"sha16_lido": h, "sha16_esperado": esp, "bytes": p.stat().st_size}
    ex.chk("sha16 de " + rel, h == esp, 1, {"lido": h, "esperado": esp})
    print("%-60s %s %s %s" % (rel, h, esp, "OK" if h == esp else "DIVERGE"))
r8 = (D / "CONTRATO_v412_R11.md").read_bytes().decode("utf-8").replace("\r\n", "\n"); r7 = (D / "CONTRATO_v412_R7.md").read_bytes().decode("utf-8").replace("\r\n", "\n")
ex.chk("a copia congelada do contrato (contrato_REV11) e' igual por sha256", L.sha256_arq(D / "contrato_REV11" / "CONTRATO_v412_R11.md") == L.sha256_arq(D / "CONTRATO_v412_R11.md"), 1)
m = re.search(r"o_que_fica_claro_REV25\\O_QUE_FICA_CLARO_v412_R25\.md` \(sha16 `([0-9a-f]{16})`; (\d+) bytes\)", r8)
ex.chk("o contrato R11 pina a pagina R25 (sha16 e bytes)", bool(m) and m.group(1) == lidos[ESPERADO[1][0]]["sha16_lido"] and int(m.group(2)) == (D / ESPERADO[1][0]).stat().st_size, 1, m.groups() if m else None)
mm = re.search(r"insumos\\MANIFESTO_PEDRAS_v412_R12\.json` \(sha16 `([0-9a-f]{16})`\)", r8); aa = re.search(r"insumos\\ANCORAS_PROPOSTAS_v412_R12\.json` \(sha16 `([0-9a-f]{16})`\)", r8)
ex.chk("o R11 pina o mesmo manifesto e as mesmas ancoras R11", bool(mm and aa) and mm.group(1) == "1028adf7293b432f" and aa.group(1) == "31af18a86183002f", 2, [mm and mm.group(1), aa and aa.group(1)])
nomes = ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]
pal = {}
# (gerencia c1, 18/11, D236) o parecer da 034 trocou de proposito tres trechos da palavra de leitor_da_formula_v412; as outras quatro
# palavras seguem iguais as do R7, e a de leitor_da_formula_v412 tem de ser a do R7 com exatamente estas tres trocas, e nada mais.
D236_TROCAS = [("ON_THE_THEORY_MACHINE_THE_FIXED_POLYNOMIAL_OF_THE_STEPS_IS_GIVEN_BY_BETA_BEFORE_ANY_FORMULA", "ON_THE_THEORY_MACHINE_BETA_GIVES_BEFORE_ANY_FORMULA_A_SUFFICIENT_LINEAR_THRESHOLD_OF_STEPS"),
               ("WITHOUT_PAYMENT_THE_CYCLE_DOES_NOT_CLOSE_AND_WITH_THE_STEP_ONE_MINUS_BETA_IT_CLOSES_LINEARLY_IN_THE_LOAD", "WITHOUT_PAYMENT_NO_NUMBER_OF_STEPS_DECIDES_EVERY_FORMULA_AND_WITH_THE_STEP_ONE_MINUS_BETA_LINEARLY_MANY_STEPS_SUFFICE"),
               ("DECIDING_COSTS_THE_LOAD_NEITHER_MORE_NOR_LESS", "THE_LOAD_IS_THE_STRICT_THRESHOLD_OF_THE_READING_TIME_THAT_DECIDES_EVERY_FORMULA")]
for nome in nomes:
    a8 = re.findall(r"^- `%s`\n  `([A-Z0-9_]+)`" % nome, r8, re.M); a7 = re.findall(r"^- `%s`\n  `([A-Z0-9_]+)`" % nome, r7, re.M)
    esperado = a7
    if nome == "leitor_da_formula_v412" and len(a7) == 1:
        e = a7[0]
        for velho, novo in D236_TROCAS:
            e = e.replace(velho, novo) if e.count(velho) == 1 else "TROCA_D236_NAO_CASOU_" + velho
        esperado = [e]
    pal[nome] = {"r11": len(a8), "r7": len(a7), "iguais": a8 == esperado and len(a8) == 1, "com_as_tres_trocas_da_d236": nome == "leitor_da_formula_v412"}
ex.chk("as cinco palavras de veredito do R11 sao as do R7 (uma de cada), salvo as tres trocas da D236 em leitor_da_formula_v412", all(v["iguais"] for v in pal.values()), 5, pal)
rec = {"quando": L.agora(), "exame": ex.resumo(), "linhas": ex.linhas, "lidos": lidos, "palavras": pal}
L.salvar_json(D / "INICIO_R11_v412.json", rec)
print(json.dumps(ex.resumo(), ensure_ascii=False))
if not ex.ok:
    print("PARE: algo nao bate"); sys.exit(2)
L.estado_bloco("0d_contrato_r11", True, {"recibo": D / "INICIO_R11_v412.json", "contrato_r11": D / "CONTRATO_v412_R11.md", "pagina_r25": D / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md"},
               nota="o contrato vigente passou a R11 (pagina R25; lista de pedras R12, com tres fontes mudadas so' em comentario; ancoras R12); sha16 conferidos por script; a palavra de leitor_da_formula_v412 e' a do R7 com as tres trocas da D236; o texto publico passa a ser montado pela R25 (bloco gravado pela gerencia c1, que termina a Etapa 2 com o construtor parado)",
               proximo="remontar a traducao EN pela R25 (e7_22c_en_r25_v412.py), os scripts _r7 (e7_04, e7_05, e7_06, e7_07, depois da build do kernel e7_02) e o texto publico (e7_23)")
