# -*- coding: utf-8 -*-
"""e3_patch_goc_v412.py -- adapta guarda_ordem_de_chamada_v412.py (a subida mecanica tem backup em .bak_*_bump): acrescenta a ordem de chamada dos QUATRO registros por especificacao (ordem_dos_specs, controle_negativo_specs)
e liga os dois ao uso por linha de comando. Parte do arquivo bumpado se ainda tem a marca [A ADAPTAR v412]; senao, para (idempotente: nao aplica duas vezes). Script da cadeia."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "guarda_ordem_de_chamada_v412.py")
NOVO = open(r"C:\t\k412c\ensaio_adapt\novo_goc.txt", encoding="utf-8").read()
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "[A ADAPTAR v412]" not in s:
    print("ja adaptado (sem a marca); nada a fazer"); sys.exit(0)
bak = P + ".bak_antes_do_patch_e3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:80], s.count(old))
    s = s.replace(old, new)


# 1. a marca: sai (a adaptacao foi feita de verdade abaixo) e entra a linha do que foi feito
i = s.index("# [A ADAPTAR v412]"); j = s.index("\n", i)
s = s[:i] + "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a v412 nao tem registro com funcao novo: o registro da v411 (h0dn_bg1_v411) segue conferido como HERDADO (as listas abaixo ficam como a subida de rotulo as deixou, e o ensaio as confere); NOVO: ordem_dos_specs / controle_negativo_specs conferem, por AST, a instrucao do main que chama _v412_rodar_specs(core) (os QUATRO registros por especificacao): toda chave que as checagens deles leem esta pronta antes; cinco controles negativos; zero checagens examinadas reprova." + s[j:]
# 2. as funcoes novas, antes do uso por linha de comando
troca('\n\nif __name__ == "__main__":', NOVO + '\n\nif __name__ == "__main__":')
# 3. a linha de comando: tambem a ordem dos specs e o controle negativo dos specs
troca('    ctl = controle_negativo(src_) if fns == FUNCOES_V412 else None\n',
      '    ctl = controle_negativo(src_) if fns == FUNCOES_V412 else None\n    specs_ = specs_do_programa(src_); r_specs = ordem_dos_specs(src_, specs_); ctl_specs = controle_negativo_specs(src_, specs_)\n    print(json.dumps({"ordem_dos_specs_v412": {k: v for k, v in r_specs.items() if k != "chaves_lidas"}, "controle_negativo_specs": ctl_specs}, ensure_ascii=False))\n')
troca('"ordem_de_chamada": r, "controle_negativo": ctl}', '"ordem_de_chamada": r, "controle_negativo": ctl, "ordem_dos_specs_v412": r_specs, "controle_negativo_specs": ctl_specs}')
troca('    sys.exit(0 if r["ok"] and (ctl is None or ctl["ok"]) else 1)', '    sys.exit(0 if r["ok"] and (ctl is None or ctl["ok"]) and r_specs["ok"] and ctl_specs["ok"] else 1)')
tmp = P + ".tmp"
open(tmp, "wb").write(s.encode("utf-8"))
assert os.path.getsize(tmp) > len(raw)
os.replace(tmp, P)
print("guarda_ordem_de_chamada_v412.py adaptada:", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16], os.path.getsize(P), "bytes")
