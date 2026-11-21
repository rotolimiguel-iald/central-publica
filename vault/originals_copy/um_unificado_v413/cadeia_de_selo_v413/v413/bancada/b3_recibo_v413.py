# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/pos_rito/b3_recibo_v412.py (o corpo: a ultima linha JSON do stdout cita o recibo; sha; versao, fase, modo, bateria; a geracao lida
# do recibo; o recibo pre-selo pinado) com o TERCEIRO ARGUMENTO do molde v394/pos_rito/b3_recibo_v394.py (o sha256 da cadeia de selos): a v413 e' o SALTO v411 -> v413, e o salto e' EXIGIDO (DIAGNOSTICO 2.4).
"""b3_recibo_v413.py -- confere o que o sincronizar_bancada.py (o elo B(n), esboco R3.6: SALTO v411 -> v413) imprimiu: a ULTIMA linha JSON do stdout cita o recibo; o recibo e' aberto e o sha256 confere com o
impresso; a bateria PASSA; versao alvo v413, fase pos_selo, modo o pedido. O salto (os numeros sao LIDOS do recibo e do delta_bn, nunca digitados aqui):
  (1) N6: manifesto_anterior.version == v411 (o anterior da BANCADA) e o deployment == o B20 do religamento da v411; n = a geracao dele + 1 (B21);
  (2) o manifesto anterior do recibo == o que o recibo pre-selo PINADO (PINOS_BN_v413.json[recibo_pre_selo]) viu, por sha256: a producao nao mudou entre o pre-selo e agora; o recibo pre-selo do recibo e' o pinado;
  (3) o salto declarado: contrato SALTO_R3_4; cadeia.sha256 == o terceiro argumento == o pino cadeia_de_selos do PINOS_BN; de v411 (o B20), ate v412, puladas [v412], proxima_a_selar v413; e o bloco == o do recibo pre-selo;
  (4) o veredito EXATO: REPINADA_B21__SALTO_v411_v413__ENSAIO__NADA_GRAVADO_NA_BANCADA (ensaio) ou REPINADA_B21__SALTO_v411_v413__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO (aplicar);
  (5) manifesto_novo.deployment_id == B21-v413-<data>-R1; (6) no aplicar, a pos_conferencia diz ok, versao v413 e o sha do manifesto novo; no ensaio, nenhuma aplicacao; (7) a bateria por versao: os pinos da v413.
uso: python -I -B -X utf8 b3_recibo_v413.py <arquivo com o stdout do esboco> ensaio|aplicar <sha256 da cadeia de selos>
rc 0 = confere; rc 1 = nao confere (a cadeia PARA). Nao escreve nada. NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move."""
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402

RX_GERACAO = re.compile(r"^B(\d+)-")


def _geracao(deployment_id):
    m = RX_GERACAO.match(str(deployment_id or ""))
    return int(m.group(1)) if m else None


def main(argv):
    if len(argv) != 4 or argv[2] not in ("ensaio", "aplicar") or not re.fullmatch(r"[0-9a-fA-F]{64}", argv[3] or ""):
        print("uso: b3_recibo_v413.py <stdout> ensaio|aplicar <sha256 da cadeia de selos (64 hex)>   (o terceiro argumento e' obrigatorio: a v413 e' o salto v411 -> v413)")
        return 1
    modo, cad = argv[2], argv[3].lower()
    linhas = [l for l in open(argv[1], encoding="utf-8", errors="replace").read().splitlines() if l.strip().startswith("{")]
    if not linhas:
        print("B(n) %s: o stdout nao traz a linha JSON do esboco" % modo); return 1
    try:
        imp = json.loads(linhas[-1])
    except ValueError as e:
        print("B(n) %s: a ultima linha JSON nao le: %r" % (modo, e)); return 1
    rp = imp.get("recibo")
    if not rp or not os.path.isfile(rp):
        print("B(n) %s: sem recibo (veredito %r, recusa %r)" % (modo, imp.get("veredito"), imp.get("recusa"))); return 1
    raw = open(rp, "rb").read()
    if hashlib.sha256(raw).hexdigest() != imp.get("recibo_sha256"):
        print("B(n) %s: o sha256 do recibo nao confere com o impresso" % modo); return 1
    r = json.loads(raw.decode("utf-8"))
    bat = (r.get("bateria_resultado") or {}).get("veredito"); ver = str(r.get("veredito") or "")
    prob = []
    if os.path.basename(rp).startswith("RECUSA_"):
        prob.append("o arquivo e' uma RECUSA")
    if r.get("versao_alvo") != DBN.UM_VERSION_BN or r.get("fase") != "pos_selo" or r.get("modo") != modo:
        prob.append("versao/fase/modo do recibo: %r %r %r" % (r.get("versao_alvo"), r.get("fase"), r.get("modo")))
    if bat != "BATERIA_PASSA":
        prob.append("bateria: %r" % bat)
    # (1) N6: o anterior da Bancada e a geracao do salto
    ma = r.get("manifesto_anterior") or {}
    m = _geracao(ma.get("deployment_id"))
    n = (m + 1) if m is not None else None
    if ma.get("version") != DBN.BANCADA_ANTERIOR or ma.get("deployment_id") != DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"]:
        prob.append("a Bancada de producao nao pinava o B20 da v411 (manifesto_anterior %r %r): o B(n) da v413 e' o salto v411 -> v413" % (ma.get("version"), ma.get("deployment_id")))
    if n != DBN.N_DO_SALTO:
        prob.append("a geracao do B novo (%r) nao e' a do salto (%r)" % (n, DBN.N_DO_SALTO))
    # (2) o recibo pre-selo pinado e a producao que ele viu
    pr = None
    try:
        pinos = json.load(open(DBN.PINOS_BN_ARQ, encoding="utf-8"))
        pr = pinos["recibo_pre_selo"]
        if (pinos.get("cadeia_de_selos") or {}).get("sha256") != cad:
            prob.append("o terceiro argumento (%s) nao e' o pino cadeia_de_selos do PINOS_BN_v413.json (%s)" % (cad[:16], str((pinos.get("cadeia_de_selos") or {}).get("sha256"))[:16]))
        prb = open(pr["path"], "rb").read()
        if hashlib.sha256(prb).hexdigest() != pr["sha256"]:
            prob.append("o recibo pre_selo em disco diverge do pino (%s)" % pr["path"])
        else:
            pre = json.loads(prb.decode("utf-8")); mp = pre.get("manifesto_anterior") or {}
            if (mp.get("sha256"), mp.get("deployment_id"), mp.get("version")) != (ma.get("sha256"), ma.get("deployment_id"), ma.get("version")):
                prob.append("o manifesto anterior do recibo (%s %s) != o do recibo pre_selo pinado (%s %s): a Bancada de producao mudou desde o pre_selo" % (
                    ma.get("deployment_id"), str(ma.get("sha256"))[:16], mp.get("deployment_id"), str(mp.get("sha256"))[:16]))
            if json.dumps(pre.get("salto"), sort_keys=True) != json.dumps(r.get("salto"), sort_keys=True):
                prob.append("o salto do recibo nao e' o do recibo pre_selo pinado (o pos-selo confere o bloco declarado byte a byte)")
        if _geracao((pr.get("bancada_pina") or {}).get("deployment_id")) != m:
            prob.append("a geracao do manifesto anterior (%r) != a que o PINOS_BN registra para a Bancada (%r)" % (m, (pr.get("bancada_pina") or {}).get("deployment_id")))
        if ((r.get("recibo_pre_selo") or {}).get("sha256")) != pr["sha256"]:
            prob.append("o recibo pre_selo do recibo (%s) nao e' o pinado (%s)" % (str((r.get("recibo_pre_selo") or {}).get("sha256"))[:16], pr["sha256"][:16]))
    except (OSError, KeyError, TypeError, ValueError) as e:
        prob.append("nao li o recibo pre_selo pinado em PINOS_BN_v413.json: %r" % (e,))
    # (3) o salto declarado e exigido
    salto = r.get("salto")
    if not isinstance(salto, dict) or salto.get("declarado") is not True or salto.get("contrato") != "SALTO_R3_4":
        prob.append("o recibo nao declara o salto (contrato SALTO_R3_4): a Bancada pinava a v411 e o Nos e' a v413")
    else:
        if (salto.get("cadeia") or {}).get("sha256") != cad or (r.get("cadeia_de_selos") or {}).get("sha256") != cad:
            prob.append("a cadeia de selos do salto no recibo (%r) nao e' a pinada (%r)" % ((salto.get("cadeia") or {}).get("sha256"), cad))
        de, ate = salto.get("de") or {}, salto.get("ate") or {}
        if (de.get("versao"), de.get("deployment_id"), ate.get("versao"), salto.get("versoes_puladas"), salto.get("proxima_a_selar")) != (
                DBN.BANCADA_ANTERIOR, DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"], DBN.UM_PY_ANTERIOR, [DBN.UM_PY_ANTERIOR], DBN.UM_VERSION_BN):
            prob.append("o salto nao e' de v411 (B20) ate v412 com proxima_a_selar v413: %r" % ({"de": de.get("versao"), "deployment": de.get("deployment_id"), "ate": ate.get("versao"),
                                                                                                  "puladas": salto.get("versoes_puladas"), "proxima": salto.get("proxima_a_selar")},))
    # (4) o veredito exato
    esperado = DBN.VEREDITO_ENSAIO_POS_SELO if modo == "ensaio" else DBN.VEREDITO_APLICAR
    if n is not None and esperado != ("REPINADA_B%d__SALTO_%s_%s__%s" % (n, DBN.BANCADA_ANTERIOR, DBN.UM_VERSION_BN, "ENSAIO__NADA_GRAVADO_NA_BANCADA" if modo == "ensaio" else "APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO")):
        prob.append("a geracao lida do recibo nao da' o veredito do delta_bn")
    if ver != esperado:
        prob.append("o veredito %r nao e' o esperado %r" % (ver, esperado))
    # (5) e (6)
    mn = r.get("manifesto_novo") or {}
    if not DBN.RE_DEPLOYMENT_NOVO.match(str(mn.get("deployment_id") or "")):
        prob.append("manifesto_novo.deployment_id=%r (esperado B%d-v413-<data>-R1)" % (mn.get("deployment_id"), DBN.N_DO_SALTO))
    ap = r.get("aplicacao")
    if modo == "aplicar":
        pc = (ap or {}).get("pos_conferencia") or {}
        if not ap:
            prob.append("o aplicar nao traz a aplicacao")
        elif not (pc.get("ok") is True and pc.get("canonical_version") == DBN.UM_VERSION_BN and pc.get("canonical_manifest_sha256") == mn.get("sha256")):
            prob.append("a pos_conferencia do aplicar nao diz ok, versao v413 e o sha do manifesto novo: %r" % {k: pc.get(k) for k in ("ok", "canonical_version", "canonical_manifest_sha256")})
    elif ap:
        prob.append("o ENSAIO traz uma aplicacao (nada podia ter sido gravado)")
    # (7) a bateria por versao
    pv = (r.get("bateria") or {}).get("pinos_da_versao") or {}
    if pv.get("versao") != DBN.UM_VERSION_BN or pv.get("declarados") is not True or pv.get("conferidos_contra_o_nos_lido") is not True:
        prob.append("os pinos da versao da bateria nao sao os da v413 conferidos contra o Nos lido: %r" % {k: pv.get(k) for k in ("declarados", "versao", "conferidos_contra_o_nos_lido")})
    print("B(n) %s: veredito=%s bateria=%s recibo=%s sha16=%s manifesto_novo=%s anterior=%s salto=%s" % (modo, ver, bat, rp, str(imp.get("recibo_sha256", ""))[:16], (mn.get("sha256") or "")[:16], ma.get("deployment_id"),
                                                                                                     ("%s->%s puladas=%s" % (salto["de"]["versao"], r.get("versao_alvo"), salto["versoes_puladas"])) if isinstance(salto, dict) and salto.get("de") else None))
    for p in prob:
        print("  PROBLEMA:", p)
    return 1 if prob else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
