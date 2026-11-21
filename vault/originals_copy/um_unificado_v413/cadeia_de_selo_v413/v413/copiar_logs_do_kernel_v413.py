# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\copiar_logs_do_kernel_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v410\copiar_logs_do_kernel_v410.py (bundle NAO vazio: le KH_N1_v412.json e LOGS_COPIADOS_v412.json, que o pos_build_kernel_v412.py grava);
# [v413] o molde e' o da v412 (bundle NAO vazio: le KH_N1 e LOGS_COPIADOS, que o pos_build grava); so' os rotulos sobem (v412->v413)
"""copiar_logs_do_kernel_v413.py -- CONFERIDOR IDEMPOTENTE dos logs da construcao do kernel da v413 (desde a v409 ele nao grava nada: so' compara).
A construcao (construir_kernel_v413.sh: `lake build +<modulo>` a frio de cada modulo novo do bundle, na ordem topologica, depois o `lake build` inteiro, e `lake env lean TGL/Audit.lean` no sandbox
C:\\t\\k413c\\final) escreve DIRETO em v413\\kernel\\ (lake_build.log, audit.log, construir_marcas.txt), e o pos_build_kernel_v413.py grava kernel\\LOGS_COPIADOS_v413.json (sha256 e bytes de cada log,
a linha TGL_AXIOM_COVERAGE_TOTAL). Origem e destino sao a mesma pasta: nada se copia; este script so' COMPARA e NUNCA REGRAVA (nem o JSON, nem os logs):
  (a) construir_marcas.txt diz rc=0, rc_build=0 e rc_audit=0; (b) a linha TGL_AXIOM_COVERAGE_TOTAL do build e a do audit sao a mesma e igual a linha_TOTAL do KH_N1_v413.json (decl, thm, fora_do_trio);
  (c) os tempos das marcas (epoch) == duracao_build_s e duracao_audit_s do KH_N1_v413.json; (d) o bytes e o sha256 de cada um dos tres arquivos, recalculados agora, == o que kernel\\LOGS_COPIADOS_v413.json
  registrou (o log nao mudou depois do pos_build). Sai 0 se tudo bate; 1 se algo difere ou o JSON nao existe (rode o pos_build_kernel_v413.py antes). Re-executavel: nao escreve em lugar nenhum.
uso: C:\\Python314\\python.exe -I -B -X utf8 copiar_logs_do_kernel_v413.py   (molde: v412\\copiar_logs_do_kernel_v412.py)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel")
sha = lambda b: hashlib.sha256(b).hexdigest()
falhas = []


def chk(nome, ok, det=None):
    print(("OK   " if ok else "FALHA"), nome, "" if det is None else "-> " + str(det)[:200])
    if not ok:
        falhas.append(nome)


marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
chk("construir_marcas.txt: rc=0, rc_build=0 e rc_audit=0", bool(re.search(r"^rc=0$", marcas, re.M) and re.search(r"rc_build=0\b", marcas) and re.search(r"rc_audit=0\b", marcas)))
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
atual = {}; cov = {}
for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
    b = open(os.path.join(KD, nome), "rb").read()
    atual[nome] = {"bytes": len(b), "sha256": sha(b)}
    if nome.endswith(".log"):
        cov[nome] = [x.decode() for x in re.findall(rb"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\r\n]*", b)]
chk("a linha TGL_AXIOM_COVERAGE_TOTAL do build e a do audit sao a mesma (uma so' em cada)", len(cov["lake_build.log"]) == 1 and cov["lake_build.log"] == cov["audit.log"], cov)
kh = json.load(open(os.path.join(KD, "KH_N1_v413.json"), encoding="utf-8"))
t = kh["linha_TOTAL"]
chk("a linha de cobertura == linha_TOTAL do KH_N1_v413.json (decl, thm, fora_do_trio)", cov["audit.log"] == ["TGL_AXIOM_COVERAGE_TOTAL decl=%d thm=%d fora_do_trio=%d" % (t["decl"], t["thm"], t["fora_do_trio"])], [cov["audit.log"], t])
chk("os tempos das marcas == duracao_build_s e duracao_audit_s do KH_N1_v413.json", mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0) == kh["duracao_build_s"] and mm.get("epoch_audit_fim", 0) - mm.get("epoch_build_fim", 0) == kh["duracao_audit_s"], [mm, kh["duracao_build_s"], kh["duracao_audit_s"]])
chk("o sha256 do audit.log == o que o KH_N1_v413.json registrou (audit_log_sha256) e os bytes == audit_log_bytes", atual["audit.log"]["sha256"] == kh["audit_log_sha256"] and atual["audit.log"]["bytes"] == kh["audit_log_bytes"], [atual["audit.log"]["sha256"][:16], kh["audit_log_sha256"][:16]])
jp = os.path.join(KD, "LOGS_COPIADOS_v413.json")
if not os.path.exists(jp):
    chk("kernel\\LOGS_COPIADOS_v413.json existe (o pos_build_kernel_v413.py o grava; este script NAO grava)", False, jp)
else:
    reg = json.load(open(jp, encoding="utf-8"))
    for nome in atual:
        chk("LOGS_COPIADOS_v413.json[%s]: bytes e sha256 == os recalculados agora" % nome, reg.get(nome, {}).get("bytes") == atual[nome]["bytes"] and reg.get(nome, {}).get("sha256") == atual[nome]["sha256"], [reg.get(nome, {}).get("sha256", "")[:16], atual[nome]["sha256"][:16]])
    chk("LOGS_COPIADOS_v413.json[cobertura_linha] == a linha lida agora do audit.log", reg.get("cobertura_linha") == cov["audit.log"], reg.get("cobertura_linha"))
print("LOGS DO KERNEL v413:", "CONFEREM (nada foi gravado)" if not falhas else "DIFEREM: %s" % falhas)
sys.exit(0 if not falhas else 1)
