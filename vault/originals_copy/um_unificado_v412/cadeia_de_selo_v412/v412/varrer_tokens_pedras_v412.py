# -*- coding: utf-8 -*-
"""varrer_tokens_pedras_v412.py -- (claude-construtor-v412, 17/11/2026) varre os modulos INSTALADOS no sandbox (C:\\t\\k412c\\final\\TGLExt\\<Nome>.lean, os do BUNDLE_v412.json) com a
funcao de varredura do PROPRIO um.py v411 selado (base_v411\\um.py: _lean_strip_comments_and_strings e _LEAN_FORBIDDEN_TOKENS, extraidos por ast, como o pos_build do molde). So' le.
Antecipa a varredura recursiva da arvore que o pos_build faz depois do build. uso: C:\\Python314\\python.exe -B -X utf8 varrer_tokens_pedras_v412.py"""
import ast, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
um_src = open(os.path.join(HERE, "base_v411", "um.py"), "rb").read().decode("utf-8")
tree = ast.parse(um_src)
fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
ns = {"re": re, "os": os}
exec(compile(ast.get_source_segment(um_src, fn["_lean_strip_comments_and_strings"]), "<um.strip>", "exec"), ns)
TOKS = [ast.literal_eval(ast.get_source_segment(um_src, n.value)) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
bd = json.load(open(os.path.join(HERE, "BUNDLE_v412.json"), encoding="utf-8"))
hits = []
for m in bd["modulos"]:
    p = os.path.join("C:" + os.sep, "t", "k412c", "final", *m["rel"].split("/"))
    code = ns["_lean_strip_comments_and_strings"](open(p, "rb").read().decode("utf-8"))
    for tok in TOKS:
        if re.search(r"\b%s\b" % re.escape(tok), code):
            hits.append("%s:%s" % (m["rel"], tok))
print("tokens:", TOKS, "| modulos:", len(bd["modulos"]), "| hits:", hits)
sys.exit(1 if hits else 0)
