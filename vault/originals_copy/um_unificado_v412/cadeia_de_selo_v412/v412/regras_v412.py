# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/regras_v411.py; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/regras_v412.py.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] conferido: regras de permissao da cadeia v411 (RECUSA sem V411_REGRAS_AUTORIZADAS=sim; ato da gerencia; NAO executado); o corpo nao depende de bundle
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] regras de permissao da cadeia v410 (RECUSA sem V410_REGRAS_AUTORIZADAS=sim; ato da gerencia; nao executado); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
import datetime
import json
import os
import sys

if os.environ.get("V412_REGRAS_AUTORIZADAS") != "sim":
    raise SystemExit("RECUSO: regras_v412.py muda ~/.claude/settings.json (permissoes) e so' roda por ato da gerencia: defina V412_REGRAS_AUTORIZADAS=sim")

# regras_v412.py -- ESCRITO em 06/11/2026 pela preparacao da cadeia v412 (claude-construtor-v412, fork B) e NAO EXECUTADO (ordem da gerencia: nao rodar regras de permissao; o proprio script RECUSA sem V412_REGRAS_AUTORIZADAS=sim). Molde: regras_v411.py (subida de rotulo por _bump_copia_v412.py); os cinco comandos abaixo sao os atos que existem na pasta (instalar_v412.py, rito_v412.sh, conferir_rito_v412.py, reverter_v412.py, pos_rito/chain_pos_rito_v412.sh).
# Quando a gerencia mandar rodar: faz BACKUP de bytes de ~/.claude/settings.json e ACRESCENTA (nunca remove) as cinco regras de permissao da cadeia v412; o conteudo das regras e' so' o comando exato de cada ato.
P = "C:/Users/rotol/.claude/settings.json"
b = open(P, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts + "_regras_v412", "wb").write(b)
s = json.loads(b.decode("utf-8"))
allow = s["permissions"]["allow"]
base = 'cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v412'
regras = [
    "Bash(" + base + '" && python -B -X utf8 instalar_v412.py:*)',
    "Bash(" + base + '" && sh ./rito_v412.sh:*)',
    "Bash(" + base + '" && python -B -X utf8 conferir_rito_v412.py:*)',
    "Bash(" + base + '" && python -B -X utf8 reverter_v412.py:*)',
    "Bash(" + base + '/pos_rito" && sh ./chain_pos_rito_v412.sh:*)',
]
n0 = len(allow)
for r in regras:
    if r not in allow:
        allow.append(r)
t = json.dumps(s, ensure_ascii=False, indent=2) + "\n"
open(P + ".tmp", "w", encoding="utf-8", newline="\n").write(t)
json.load(open(P + ".tmp", encoding="utf-8"))
os.replace(P + ".tmp", P)
print("ok", n0, "->", len(allow))
