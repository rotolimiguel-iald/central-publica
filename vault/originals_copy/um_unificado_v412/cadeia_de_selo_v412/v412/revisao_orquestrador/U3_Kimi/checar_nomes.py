# -*- coding: utf-8 -*-
import re, json

base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
fonte = base + r"\candidatas_c1\REV16\CopiadorEImpostor.lean"
log = base + r"\revisao_orquestrador\U3_Kimi\compilacao\build\CopiadorEImpostor.log"
res = base + r"\candidatas_c1\RESULTADO_CopiadorEImpostor.json"

src = open(fonte, encoding='utf-8').read()
# teoremas declarados (inclui os com modificadores em linhas anteriores; aqui o padrao '^theorem ' basta)
teos = re.findall(r'(?m)^theorem\s+([A-Za-z0-9_.\'áéíóúâêôãõç]+)', src)
prints = re.findall(r'(?m)^#print axioms\s+([A-Za-z0-9_.\'áéíóúâêôãõç]+)', src)
print("theorem declarations:", len(teos))
print("#print axioms:", len(prints))
print("lemma/example/axiom:", len(re.findall(r'(?m)^lemma ', src)), len(re.findall(r'(?m)^example', src)), len(re.findall(r'(?m)^axiom ', src)))
print("native_decide:", len(re.findall(r'native_decide', src)))
falta_print = set(teos) - set(prints)
print_extra = set(prints) - set(teos)
print("declarados sem print:", falta_print if falta_print else "nenhum")
print("prints sem declaracao:", print_extra if print_extra else "nenhum")

# axiomas por teorema, do MEU log
lg = open(log, encoding='utf-8').read()
ax = {}
for m in re.finditer(r"'TGLExt\.CopiadorEImpostor\.([A-Za-z0-9_']+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])", lg):
    nome, _, lista = m.group(1), m.group(2), m.group(3)
    ax[nome] = sorted([] if lista is None else [a.strip() for a in lista.split(',')])
print("teoremas com axiomas lidos do meu log:", len(ax))

# confronto com o JSON da gerencia (computado sobre a R8)
j = json.load(open(res, encoding='utf-8'))
mod = j["modulos"][0]
print("JSON: fonte:", mod["fonte"].split("\\")[-1], "| bytes:", mod["bytes"], "| sha16:", mod["sha256"][:16])
print("JSON: rc:", mod["rc"], "| avisos:", mod["avisos"], "| erros:", mod["erros"], "| teoremas:", mod["teoremas_declarados"])
diverge = []
for t in mod["teoremas"]:
    nome = t["nome"].split(".")[-1]
    meu = ax.get(nome)
    if meu is None:
        diverge.append((nome, "ausente no meu log"))
    elif meu != sorted(t["axiomas"]):
        diverge.append((nome, t["axiomas"], meu))
nomes_json = {t["nome"].split(".")[-1] for t in mod["teoremas"]}
print("nomes no JSON:", len(nomes_json), "| no meu log:", len(ax))
print("JSON sem log:", nomes_json - set(ax) or "nenhum")
print("log sem JSON:", set(ax) - nomes_json or "nenhum")
print("divergencias de axiomas:", diverge if diverge else "nenhuma")
