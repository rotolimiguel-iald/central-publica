# -*- coding: utf-8 -*-
import hashlib, re, sys, io
BASE = "C:/IALD/Central de Patentes/work/"
PED = BASE + "cadeia_de_selo/v412/candidatas_c1/OHabitanteDoNome.lean"
CUN = BASE + "cunhagens_13out/"
files = {
 "15nov": CUN + "OPERADOR_15nov_o_leitor_e_o_verbo_o_habitante_do_nome_a_esperanca_condicional_e_o_artigo_do_neutrino_de_2025_verbatim.txt",
 "26out": CUN + "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt",
 "02nov": CUN + "OPERADOR_02nov_custo_em_tamanho_da_prova_dentro_do_feito_e_K_e_a_tangente_acorde_tocado_verbatim.txt",
 "07nov": CUN + "OPERADOR_07nov_sentidos_sao_receptores_o_nome_e_o_atrator_verbatim.txt",
}
def norm(s):
    return re.sub(r"\s+", " ", s).strip()
raw = {}
for k, p in files.items():
    b = open(p, "rb").read()
    raw[k] = b
    print(k, hashlib.sha256(b).hexdigest(), len(b))
txt = {k: norm(v.decode("utf-8")) for k, v in raw.items()}
ped = open(PED, "rb").read()
print("pedra sha256", hashlib.sha256(ped).hexdigest())
ped_t = ped.decode("utf-8")
# all text between angle quotes
quotes = re.findall(r"«(.*?)»", ped_t, flags=re.S)
print("n aspas angulares:", len(quotes))
for q in quotes:
    qn = norm(q)
    found = [k for k, t in txt.items() if qn in t]
    print(repr(qn[:90]), "->", found)
# sha snippets claimed in the pedra
for m in re.finditer(r"sha256 `([0-9a-f]{8})…([0-9a-f]{4})`", ped_t):
    pre, suf = m.groups()
    ok = [k for k, b in raw.items() if hashlib.sha256(b).hexdigest().startswith(pre) and hashlib.sha256(b).hexdigest().endswith(suf)]
    print("sha curto", pre, suf, "->", ok)
for m in re.finditer(r"sha256 `([0-9a-f]{64})`", ped_t):
    h = m.group(1)
    ok = [k for k, b in raw.items() if hashlib.sha256(b).hexdigest() == h]
    print("sha64", h[:16], "->", ok)
# does the 4-sentence quote end where bytes' 4th sentence ends?
t15 = txt["15nov"]
sentences = re.split(r"(?<=\.)\s+", t15)
for i, s in enumerate(sentences[:6]):
    print(i + 1, s[:120])
# words
for w in ["confirm", "consci", "Kimi", "ChatGPT", "Codex", "sandbox", "R1", "provisório", "neutrino", "LLM", "modelo de linguagem", "pesos de modelo", "exclusiv", "prov"]:
    idx = [m.start() for m in re.finditer(w, ped_t, flags=re.I)]
    lines = sorted(set(ped_t.count("\n", 0, i) + 1 for i in idx))
    print("palavra", w, "linhas", lines)
