# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] DIAGNOSTICO_E_PLANO_BN_v413.md, N2, caminho (a): a bateria da v412 para o ensaio pre-selo do salto, gerada pelo gerador PINADO da R3.4
# a partir de um pino MINIMO do candidato (o um.py da v412, a copia de bytes v413\base_v412\um.py), gravado aqui por script, com a nota de por que existe.
"""gerar_bateria_v412_pre_selo_v413.py -- PRAZO (N1): so' com o Nos AINDA na v412. A bateria do ensaio pre-selo e' por versao (R3.4 P): o pre-selo do salto le o Nos na v412, logo a bateria tem de ser a da v412.
Ela nunca foi gerada (a v412 nao teve B(n): nao ha v412\\bateria_pos_selo nem v412\\PINOS_BN_v412.json), e o gerador exige --pinos-bn com candidato.sha256 == o um.py do Nos.
Caminho (a) do plano: um pino MINIMO {"candidato": <o um.py da v412>} (so' a chave que o gerador le, mais a nota), gravado nesta pasta e nunca na pasta selada da v412.
Faz: (1) o Nos na v412 (o selo pina o um.py do disco) e o um.py da base_v412 == o do Nos == o que o selo pina; (2) grava PINO_MINIMO_CANDIDATO_v412.json; (3) roda o gerador, a base R2 e o driver PINADOS em
v411\\PINOS_BN_v411.json (sha conferidos contra o disco) com --versao v412 --nos <Nos> --pinos-bn <pino minimo>; (4) grava PINOS_BATERIA_v412.json ao lado (o pino da bateria, como o bn_v412.sh fazia);
(5) confere a bateria PELO ESBOCO R3.6 pinado: carregar_bateria (sha do arquivo e de cada teste) e conferir_pinos_da_versao (os pinos da v412 contra o Nos lido agora).
A pasta (v413\\bateria_v412_pre_selo) NAO e' ancestral da --saida do ensaio (v413\\bateria_pre_selo\\ensaio_1): o esboco recusaria SAIDA_NA_PASTA_DE_FONTES. uso: python -I -B -X utf8 gerar_bateria_v412_pre_selo_v413.py"""
import sys

sys.dont_write_bytecode = True
import datetime
import importlib.util
import json
import os
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

D = DBN.BATERIA_V412_DIR
PINO_MIN = os.path.join(D, "PINO_MINIMO_CANDIDATO_v412.json")
PINO_UM = os.path.join(D, "PINO_UM_PY_v412.json")
BAT = os.path.join(D, "BATERIA_VINCULO_v412.json")
PINOS_BAT = os.path.join(D, "PINOS_BATERIA_v412.json")
SAIDA_GER = os.path.join(D, "gerar_bateria_v412_out.txt")
for p_ in (PINO_MIN, PINO_UM, BAT, PINOS_BAT, SAIDA_GER):
    if os.path.exists(p_):
        raise SystemExit("ja existe (%s): a bateria da v412 nao e' regerada por cima; quem quiser refazer guarda e tira a pasta antes" % p_)
assert not U.texto_normalizado(os.path.abspath(DBN.OUTB_PRE_SELO)).startswith(U.texto_normalizado(os.path.abspath(D)) + os.sep), "a pasta da bateria seria ancestral da --saida"
# (1) o prazo e a identidade do candidato
selo = U.ler_json(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
um_nos = U.sha256_arquivo(os.path.join(DBN.NOS, "um.py"))
if selo.get("um_version") != DBN.VERSAO_DO_PRE_SELO or (selo.get("sha256") or {}).get("um.py") != um_nos:
    raise SystemExit("PRAZO_DO_PRE_SELO_PERDIDO (N1): o Nos nao esta' na %s com o selo pinando o um.py do disco (selo diz %r)" % (DBN.VERSAO_DO_PRE_SELO, selo.get("um_version")))
base_um = os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um.py")
assert U.sha256_arquivo(base_um) == um_nos, "o um.py de v413\\base_v412 nao e' o do Nos"
# os pinos da cadeia anterior (gerador, driver, base R2, esboco), conferidos contra o disco
P11 = U.ler_json(DBN.PINOS_BN_V411_ARQ)
for k_ in ("gerador_bateria", "driver_t12_t14", "bateria_base_R2", "esboco_R3_6"):
    assert U.sha256_arquivo(P11[k_]["path"]) == P11[k_]["sha256"], ("o pino %s de PINOS_BN_v411.json diverge do arquivo" % k_)
# (2) o pino minimo
os.makedirs(D, exist_ok=True)
U.gravar_json_novo(PINO_MIN, {
    "contrato": "PINO_MINIMO_CANDIDATO_v412_PARA_A_BATERIA_DO_PRE_SELO_DO_SALTO",
    "candidato": U.pinar(base_um, papel="o um.py da v412 selada (copia de bytes v413\\base_v412\\um.py == o um.py do Nos == o que o selo da v412 pina)"),
    "selo_v412": U.pinar(os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um_absoluto_selo.json")),
    "por_que_existe": ("N2 (caminho a) do DIAGNOSTICO_E_PLANO_BN_v413.md: o gerar_bateria_r3_4.py exige --pinos-bn com candidato.sha256 == o um.py do Nos, e a v412 nao tem PINOS_BN_v412.json "
                       "(nao houve B(n) na v412: decisao do operador de 19/11, evento 1689). Este pino tem SO' a chave que o gerador le (candidato) e nao e' o PINOS_BN de nenhuma versao: nenhum B(n) o le como tal."),
    "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "escopo": "so' leitura do Nos; nada gravado no Nos, na Bancada ou na pasta selada da v412",
})
# (3) o gerador pinado
r = subprocess.run([DBN.PYTHON, "-I", "-B", "-X", "utf8", P11["gerador_bateria"]["path"], "--base", P11["bateria_base_R2"]["path"], "--base-sha256", P11["bateria_base_R2"]["sha256"],
                    "--versao", DBN.VERSAO_DO_PRE_SELO, "--nos", DBN.NOS, "--driver", P11["driver_t12_t14"]["path"], "--pinos-bn", PINO_MIN, "--pino-saida", PINO_UM, "--saida", BAT],
                   capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, cwd=D)
with open(SAIDA_GER + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("rc=%d\n--- stdout\n%s\n--- stderr\n%s\n" % (r.returncode, r.stdout or "", r.stderr or ""))
os.replace(SAIDA_GER + ".tmp", SAIDA_GER)
print("gerador rc", r.returncode, "|", (r.stdout or "").strip()[-500:], (r.stderr or "").strip()[-500:])
if r.returncode != 0 or not (os.path.isfile(BAT) and os.path.isfile(PINO_UM)):
    raise SystemExit("o gerador da bateria recusou (rc %s): ver %s" % (r.returncode, SAIDA_GER))
# (4) o pino ao lado
U.gravar_json_novo(PINOS_BAT, {"bateria": {"path": BAT, "sha256": U.sha256_arquivo(BAT)}, "pino_um_py": {"path": PINO_UM, "sha256": U.sha256_arquivo(PINO_UM)},
                               "pino_minimo_do_candidato": {"path": PINO_MIN, "sha256": U.sha256_arquivo(PINO_MIN)},
                               "gerador": {"path": P11["gerador_bateria"]["path"], "sha256": P11["gerador_bateria"]["sha256"], "origem": "PINOS_BN_v411.json[gerador_bateria]"},
                               "nota": "pino ao lado da bateria da v412 do pre-selo do salto (N2, caminho a), gravado quando gerar_bateria_v412_pre_selo_v413.py a gerou"})
# (5) conferida pelo esboco
_spec = importlib.util.spec_from_file_location("sincronizar_bancada_r36_bateria_v413", P11["esboco_R3_6"]["path"])
MOD = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = MOD
_spec.loader.exec_module(MOD)
bateria, _raw, bsha = MOD.carregar_bateria(Path(BAT), U.sha256_arquivo(BAT), "ensaio", "pre_selo", False)
nos_info = MOD.ler_nos(Path(DBN.NOS), DBN.VERSAO_DO_PRE_SELO)
pv = MOD.conferir_pinos_da_versao(bateria, nos_info, DBN.VERSAO_DO_PRE_SELO)
assert pv["declarados"] is True and pv["conferidos_contra_o_nos_lido"] is True and pv["versao"] == DBN.VERSAO_DO_PRE_SELO, pv
print(json.dumps({"bateria": BAT, "sha256": bsha, "n_testes": len(bateria["testes"]), "pinos_da_versao": {k_: pv[k_] for k_ in ("versao", "um_py_sha256", "testes_que_pinam_o_um_py")},
                  "pino_ao_lado": PINOS_BAT, "pino_minimo": PINO_MIN}, ensure_ascii=False))
