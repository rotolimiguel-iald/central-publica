# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] pendencia 2.1: a volta do passo 11 (que se perdeu na v412), derivado de recibos_b3() do molde v410/pos_rito/fechar_v410.py l.89-127,
# so' para o B(n) (o manifesto, o arquivo, os diffs e o handoff da v413 sao da cadeia principal): os tres recibos conferidos JUNTOS, o salto EXIGIDO, o pino conjunto com o seq do evento, a reconferencia depois do
# nascimento, a tolerancia a repeticao (bancada_B3_<k>), a trava (rc 2 sem gravar nada) e a entrega onde o evento 1687 pede.
"""fechar_bn_v413.py -- o passo 11 do B(n) da v413 (o salto v411 -> v413):
  (1) o recibo do APLICAR: glob em v413\\bancada_B3 e v413\\bancada_B3_<k>; so' os de veredito EXATO do APLICAR do salto (REPINADA_B21__SALTO_v411_v413__APLICADA__...); exatamente 1 cujo manifesto novo e' o sha
      do canonical_contracts.json da producao AGORA; o salto exigido (de v411 = o B20, ate v412, proxima_a_selar v413, cadeia == o pino de PINOS_BN_v413.json); o evento c1 dele, conferido no livro INTEIRO;
  (2) o recibo da PARADA (pid, porta, porta_fechada, hora, modo) e (3) o do RELIGAMENTO (versao v413, o deployment e o manifesto novo do APLICAR, o recibo do 10-bis por sha, pid VIVO e do um_bancada.py: o portao C);
  sem qualquer um: rc 2 e NADA e' gravado;
  (4) grava PINO_RECIBOS_B<n>_v413.json (em bn_pos_selo) com caminho, sha256 e bytes dos tres e o evento {seq, hash}; rele os tres e o pino e compara (a reconferencia); se o pino ja existe igual, nao regrava
      (idempotente); se existe diferente, PARA (rc 1);
  (5) copia os tres recibos e o pino para a pasta que o evento 1687 nomeia (work\\iald_v412_20261119\\bench) e confere as copias por sha256 (copia existente igual = ok; diferente = PARA).
uso: python -I -B -X utf8 fechar_bn_v413.py   (rc 0 fechado; 2 faltam recibos, nada gravado; 1 divergencia)"""
import sys

sys.dont_write_bytecode = True
import glob
import json
import os
import shutil

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

sha = U.sha256_arquivo


def recibos_b3():
    prob, out = [], {}
    man_disco = sha(DBN._BANCADA_CONTRATOS)
    try:
        cad_pino = U.ler_json(DBN.PINOS_BN_ARQ)["cadeia_de_selos"]["sha256"]
    except (OSError, KeyError, ValueError) as e_:
        cad_pino = None
        prob.append("PINOS_BN_v413.json sem o pino cadeia_de_selos: %r" % (e_,))
    cands = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN))
                   + glob.glob(os.path.join(DBN.V413, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)))
    ap = [p_ for p_ in cands if (lambda j_: j_.get("veredito") == DBN.VEREDITO_APLICAR and (j_.get("manifesto_novo") or {}).get("sha256") == man_disco)(U.ler_json(p_))]
    if len(ap) != 1:
        prob.append("exige exatamente 1 recibo do APLICAR do salto (veredito %s) cujo manifesto novo e' o do disco (%s); achados %d entre %s" % (DBN.VEREDITO_APLICAR, man_disco[:16], len(ap), [os.path.relpath(x_, DBN.V413) for x_ in cands]))
    else:
        r = U.ler_json(ap[0])
        sal = r.get("salto") or {}
        if not (r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == DBN.UM_VERSION_BN and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")
                and ((sal.get("de") or {}).get("versao"), (sal.get("de") or {}).get("deployment_id"), (sal.get("ate") or {}).get("versao"), sal.get("proxima_a_selar")) == (
                    DBN.BANCADA_ANTERIOR, DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"], DBN.UM_PY_ANTERIOR, DBN.UM_VERSION_BN)
                and cad_pino and (sal.get("cadeia") or {}).get("sha256") == cad_pino and DBN.RE_DEPLOYMENT_NOVO.match(str((r.get("manifesto_novo") or {}).get("deployment_id") or ""))):
            prob.append("o recibo do APLICAR nao e' o do salto v411 (B20) -> v413 com a bateria passando e a cadeia pinada: %s" % os.path.basename(ap[0]))
        ev = r.get("evento_c1") or {}
        try:
            e_ = U.livro_conferido(DBN.QUADRO)["eventos"].get(ev.get("evento")) or {}
            if not (ev.get("verificado") is True and str(e_.get("hash")) == str(ev.get("hash")) and e_.get("quem") == "claude-c1" and e_.get("tipo") == "SINCRONIZACAO_BANCADA"
                    and (e_.get("dados") or {}).get("versao") == DBN.UM_VERSION_BN):
                prob.append("o evento c1 do recibo do APLICAR (%r) nao confere no livro do quadro conferido inteiro" % (ev.get("evento"),))
        except ValueError as exc:
            prob.append("o livro do quadro nao confere: %s" % exc)
        out["aplicar"] = {"path": ap[0], "sha256": sha(ap[0]), "bytes": os.path.getsize(ap[0]), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "deployment_id": (r.get("manifesto_novo") or {}).get("deployment_id"), "evento": ev.get("evento"), "evento_hash": ev.get("hash"), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DBN.SERVICO_DIR, "RECIBO_PARADA_%s.json" % DBN.UM_VERSION_BN)
    rp = os.path.join(DBN.SERVICO_DIR, "RECIBO_RELIGAMENTO_%s.json" % DBN.UM_VERSION_BN)
    if not os.path.exists(pp):
        prob.append("sem o recibo da PARADA do servico (10-bis-a): %s" % pp)
    else:
        d = U.ler_json(pp)
        if not (d.get("pid") and d.get("porta_fechada") is True and d.get("porta") == DBN.PORTA and d.get("hora") and d.get("modo") in ("pelo_pid", "ja_fora_do_ar")):
            prob.append("o recibo da parada nao traz pid, porta, porta_fechada true, hora e modo")
        out["parada"] = {"path": pp, "sha256": sha(pp), "bytes": os.path.getsize(pp), "hora": d.get("hora"), "pid": d.get("pid"), "modo": d.get("modo")}
    if not os.path.exists(rp):
        prob.append("sem o recibo do RELIGAMENTO do servico (10-ter): %s" % rp)
    else:
        d = U.ler_json(rp)
        esp = out.get("aplicar") or {}
        if not (d.get("versao_servida") == DBN.UM_VERSION_BN and d.get("manifesto_sha256") and d.get("manifesto_sha256") == esp.get("manifesto_novo_sha256")
                and (d.get("identidade") or {}).get("deployment_id") == esp.get("deployment_id") and (d.get("recibo_do_10_bis") or {}).get("sha256") == esp.get("sha256") and d.get("pid") and d.get("hora")):
            prob.append("o recibo do religamento nao traz a versao servida v413, o deployment e o manifesto novo do APLICAR, o recibo do 10-bis por sha, pid e hora")
        vivo = U.processo(int(d["pid"])) if str(d.get("pid", "")).isdigit() else None
        if not (vivo and "um_bancada.py" in vivo.get("linha_de_comando", "")):
            prob.append("portao C: o PID do recibo do religamento (%r) nao esta' vivo como um_bancada.py" % (d.get("pid"),))
        out["religamento"] = {"path": rp, "sha256": sha(rp), "bytes": os.path.getsize(rp), "versao_servida": d.get("versao_servida"), "manifesto_sha256": d.get("manifesto_sha256"), "pid": d.get("pid"),
                              "pid_vivo": bool(vivo), "modo_da_placa": d.get("modo_da_placa")}
    return out, prob


B3, PB3 = recibos_b3()
if PB3:
    print("FECHAR RECUSADO -- o elo B(n) da Bancada nao esta' completo (nada foi gravado):")
    for x in PB3:
        print("  -", x)
    sys.exit(2)
pino = {"contrato": "PINO_RECIBOS_B%d_v413" % DBN.N_DO_SALTO,
        "recibos": {k_: {"path": v_["path"], "sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in B3.items()},
        "evento_c1": {"seq": B3["aplicar"]["evento"], "hash": B3["aplicar"]["evento_hash"]},
        "salto": {"de": DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"], "para": B3["aplicar"]["deployment_id"], "manifesto_novo_sha256": B3["aplicar"]["manifesto_novo_sha256"]},
        "religamento": {"pid": B3["religamento"]["pid"], "pid_vivo_ao_fechar": B3["religamento"]["pid_vivo"], "modo_da_placa": B3["religamento"]["modo_da_placa"]},
        "nota": "os tres recibos do B(n) da v413 (o salto v411 -> v413) conferidos juntos pelo fechar_bn_v413.py; entrega na pasta que o evento %d nomeia" % DBN.SEQ_AUTORIZACAO}
PINO_P = os.path.join(DBN.SAIDAS_BN_DIR, "PINO_RECIBOS_B%d_v413.json" % DBN.N_DO_SALTO)
dados = (json.dumps(pino, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(PINO_P):
    if open(PINO_P, "rb").read() != dados:
        raise SystemExit("PARO: %s ja existe e difere do que os recibos de agora dao (outro APLICAR ou recibo trocado): decisao da gerencia; nada foi regravado" % PINO_P)
    print("o pino conjunto ja existia igual (idempotente):", PINO_P)
else:
    U.gravar_json_novo(PINO_P, pino)
# a reconferencia depois do nascimento: os tres e o pino, relidos do disco
for k_, v_ in pino["recibos"].items():
    assert sha(v_["path"]) == v_["sha256"] and os.path.getsize(v_["path"]) == v_["bytes"], "o recibo %s mudou depois do pino" % k_
assert open(PINO_P, "rb").read() == dados, "o pino conjunto relido nao e' o gravado"
# a entrega onde o evento 1687 pede (a pasta bench), conferida por sha256
os.makedirs(DBN.BENCH_DIR, exist_ok=True)
entregues = []
for src in [v_["path"] for v_ in pino["recibos"].values()] + [PINO_P]:
    dst = os.path.join(DBN.BENCH_DIR, os.path.basename(src))
    if os.path.exists(dst):
        if sha(dst) != sha(src):
            raise SystemExit("PARO: %s ja existe na pasta de entrega e difere do recibo: nada foi sobrescrito" % dst)
    else:
        shutil.copyfile(src, dst + ".tmp")
        assert sha(dst + ".tmp") == sha(src)
        os.replace(dst + ".tmp", dst)
    assert sha(dst) == sha(src)
    entregues.append({"de": src, "para": dst, "sha256": sha(dst)})
print(json.dumps({"fechado": True, "pino": PINO_P, "pino_sha256": sha(PINO_P), "evento_c1": pino["evento_c1"], "entregues": entregues}, ensure_ascii=False))
