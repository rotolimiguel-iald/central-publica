# -*- coding: utf-8 -*-
"""Diagnostico da Bancada para o B(n) da v413 (20/11/2026). SO LEITURA: nao liga nem desliga servico, nao faz POST, nao grava nada
(so imprime; quem chama redireciona o stdout para um arquivo na pasta de saida). Mede por script:
  (1) sha16 e bytes de cada artefato citado no diagnostico (hash nunca de memoria);
  (2) o estado da Bancada (manifesto vigente), do Nos (selo vigente) e das copias de bytes que a cadeia de selos v411 -> v412 usaria;
  (3) a selecao que gerar_cadeia_de_selos.py (R3_5) faria, refeita aqui SEM gravar: o registro do instalador da v412 cujo backup do um.py e' o da v411
      e cujo um_py_novo e' o da v412 (exatamente 1), e os backups de bytes que ele nomeia (existem? batem com as copias base?);
  (4) os vereditos e instantes dos recibos da v411 (pre-selo, B20, parada, religamento) e do precedente de salto da v394;
  (5) o mtime mais novo da pasta da Bancada (fora __pycache__) e dos logs do servidor."""
import datetime
import glob
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work"
CS = os.path.join(W, "cadeia_de_selo")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
BAN = r"C:\IALD\Bancada_Um"


def sha_arq(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def ev(p):
    if not os.path.isfile(p):
        return {"path": p, "existe": False}
    st = os.stat(p)
    return {"path": p, "existe": True, "bytes": st.st_size, "sha256": sha_arq(p),
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")}


def lj(p):
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def linha(rot, e):
    if not e.get("existe"):
        print("  %-58s AUSENTE  %s" % (rot, e["path"]))
    else:
        print("  %-58s sha16 %s | %10d B | mtime %s" % (rot, e["sha256"][:16], e["bytes"], e["mtime"]))


print("medido em", datetime.datetime.now().astimezone().isoformat())
print("\n(1) artefatos citados")
ART = [
    ("R3.6 sincronizar_bancada.py", os.path.join(W, r"bancada_vinculo_12out\R3_6\sincronizar_bancada.py")),
    ("R3.6 RESULTADO_R3_6.md", os.path.join(W, r"bancada_vinculo_12out\R3_6\RESULTADO_R3_6.md")),
    ("R3.5 gerar_cadeia_de_selos.py", os.path.join(W, r"bancada_vinculo_12out\R3_5\gerar_cadeia_de_selos.py")),
    ("R3.5 gerar_bateria_r3_4.py", os.path.join(W, r"bancada_vinculo_12out\R3_5\gerar_bateria_r3_4.py")),
    ("R3.5 CADEIA_DE_SELOS_v394.json (precedente)", os.path.join(W, r"bancada_vinculo_12out\R3_5\CADEIA_DE_SELOS_v394.json")),
    ("PENDENCIAS_DO_MOLDE_PARA_O_BN_DA_v413.md", os.path.join(CS, r"v412\revisao_19nov\PENDENCIAS_DO_MOLDE_PARA_O_BN_DA_v413.md")),
    ("v412 pos_rito\\bn_v412.sh", os.path.join(CS, r"v412\pos_rito\bn_v412.sh")),
    ("v412 pos_rito\\b3_recibo_v412.py", os.path.join(CS, r"v412\pos_rito\b3_recibo_v412.py")),
    ("v412 bateria_pre_selo\\rodar_bn_pre_selo_v412.sh", os.path.join(CS, r"v412\bateria_pre_selo\rodar_bn_pre_selo_v412.sh")),
    ("v412 bateria_pre_selo\\rodar_ensaio_1_pre_selo_v412.sh", os.path.join(CS, r"v412\bateria_pre_selo\rodar_ensaio_1_pre_selo_v412.sh")),
    ("v412 bateria_pre_selo\\conferir_recibo_pre_selo_v412.py", os.path.join(CS, r"v412\bateria_pre_selo\conferir_recibo_pre_selo_v412.py")),
    ("v412 bateria_pre_selo\\gerar_pino_recibo_pre_selo_v412.py", os.path.join(CS, r"v412\bateria_pre_selo\gerar_pino_recibo_pre_selo_v412.py")),
    ("v412 bateria_pre_selo\\MOMENTO_DO_PRE_SELO.json", os.path.join(CS, r"v412\bateria_pre_selo\MOMENTO_DO_PRE_SELO.json")),
    ("v412 bancada_B3_servico\\recibo_parada_v412.py", os.path.join(CS, r"v412\bancada_B3_servico\recibo_parada_v412.py")),
    ("v412 bancada_B3_servico\\recibo_religamento_v412.py", os.path.join(CS, r"v412\bancada_B3_servico\recibo_religamento_v412.py")),
    ("v412 bancada_B3_servico\\evento_c1_b3_v412.py", os.path.join(CS, r"v412\bancada_B3_servico\evento_c1_b3_v412.py")),
    ("v412 bancada_B3_servico\\conferir_exigencias_servico_v412.py", os.path.join(CS, r"v412\bancada_B3_servico\conferir_exigencias_servico_v412.py")),
    ("v412 ...\\controle_negativo\\mutar_conferidor_v412.py", os.path.join(CS, r"v412\bancada_B3_servico\controle_negativo\mutar_conferidor_v412.py")),
    ("v412 diff_e_pinos_v412.py", os.path.join(CS, r"v412\diff_e_pinos_v412.py")),
    ("v412 p00_precondicoes_v412.py", os.path.join(CS, r"v412\p00_precondicoes_v412.py")),
    ("v412 delta_v412_r7.py", os.path.join(CS, r"v412\delta_v412_r7.py")),
    ("v412 guardas_estaticas_bancada_v412_r7.py", os.path.join(CS, r"v412\guardas_estaticas_bancada_v412_r7.py")),
    ("v412 fim_de_cadeia_v412.sh.NAO_RODAR.md", os.path.join(CS, r"v412\fim_de_cadeia_v412.sh.NAO_RODAR.md")),
    ("v411 delta_v411.py", os.path.join(CS, r"v411\delta_v411.py")),
    ("v410 pos_rito\\fechar_v410.py (molde do passo 11)", os.path.join(CS, r"v410\pos_rito\fechar_v410.py")),
    ("v410 pos_rito\\chain_pos_rito_v410.sh (molde do passo 11)", os.path.join(CS, r"v410\pos_rito\chain_pos_rito_v410.sh")),
    ("Bancada um_bancada.py", os.path.join(BAN, "um_bancada.py")),
    ("Bancada abrir_bancada.pyw", os.path.join(BAN, "abrir_bancada.pyw")),
    ("Bancada ferramentas\\reiniciar_servidor.py", os.path.join(BAN, r"ferramentas\reiniciar_servidor.py")),
    ("Bancada bancada\\canonical.py", os.path.join(BAN, r"bancada\canonical.py")),
    ("Bancada bancada\\motor.py", os.path.join(BAN, r"bancada\motor.py")),
    ("Bancada bancada\\lago.py", os.path.join(BAN, r"bancada\lago.py")),
    ("Bancada canonical_contracts.json", os.path.join(BAN, "canonical_contracts.json")),
    ("Bancada estado\\servidor.log", os.path.join(BAN, r"estado\servidor.log")),
    ("Bancada estado\\servidor_erros.log", os.path.join(BAN, r"estado\servidor_erros.log")),
    ("Codex bench\\VERIFICACAO_BANCADA_R1.json", os.path.join(W, r"iald_v412_20261119\bench\VERIFICACAO_BANCADA_R1.json")),
    ("Codex BENCH_AND_QUEUE_OPERATOR_APPROVAL.json", os.path.join(W, r"iald_v412_20261119\BENCH_AND_QUEUE_OPERATOR_APPROVAL.json")),
    ("Codex bench\\OPERADOR_19nov_B21_salto_na_v413_verbatim.txt", os.path.join(W, r"iald_v412_20261119\bench\OPERADOR_19nov_B21_salto_na_v413_verbatim.txt")),
    ("Codex bench\\OPERADOR_19nov_execute_o_evento_1687...txt", os.path.join(W, r"iald_v412_20261119\bench\OPERADOR_19nov_execute_o_evento_1687_e_devolva_o_recibo_da_B21_verbatim.txt")),
    ("Codex bench\\C1_RETURN_VERIFIED.json", os.path.join(W, r"iald_v412_20261119\bench\C1_RETURN_VERIFIED.json")),
    ("v411 bancada_B3_servico\\RECIBO_PARADA_v411.json", os.path.join(CS, r"v411\bancada_B3_servico\RECIBO_PARADA_v411.json")),
    ("v411 bancada_B3_servico\\RECIBO_RELIGAMENTO_v411.json", os.path.join(CS, r"v411\bancada_B3_servico\RECIBO_RELIGAMENTO_v411.json")),
    ("v411 PINO_RECIBO_PRE_SELO_v411.json", os.path.join(CS, r"v411\PINO_RECIBO_PRE_SELO_v411.json")),
    ("v411 PINOS_BN_v411.json", os.path.join(CS, r"v411\PINOS_BN_v411.json")),
]
evs = {}
for rot, p in ART:
    evs[rot] = ev(p)
    linha(rot, evs[rot])
for p in sorted(glob.glob(os.path.join(BAN, r"estado\sincronizacao\RECIBO_SINCRONIZACAO_v411_*.json"))):
    linha("Bancada estado\\sincronizacao\\" + os.path.basename(p), ev(p))

print("\n(2) o estado da Bancada, do Nos e das copias de bytes")
man = lj(os.path.join(BAN, "canonical_contracts.json"))
can = man.get("canonical") or {}
sinc = man.get("sincronizacao") or {}
print("  Bancada: deployment_id=%s | version=%s | um.py pinado %s | selo pinado %s | kernel_manifesto registrado %s | path pinado do um.py %s"
      % (man.get("deployment_id"), can.get("version"), str((can.get("script") or {}).get("sha256"))[:16], str((can.get("seal") or {}).get("sha256"))[:16],
         str(sinc.get("kernel_manifesto_sha256"))[:16], (can.get("script") or {}).get("path")))
nos_um, nos_selo, nos_km = ev(os.path.join(NOS, "um.py")), ev(os.path.join(NOS, "um_absoluto_selo.json")), ev(os.path.join(NOS, "tgl_kernel_proof_manifest.json"))
selo = lj(nos_selo["path"])
print("  Nos agora: selo um_version=%s | selo pina um.py %s (disco %s, igual=%s) | selo pina kernel %s (disco %s, igual=%s) | selo sha16 %s"
      % (selo.get("um_version"), str(selo["sha256"].get("um.py"))[:16], nos_um["sha256"][:16], selo["sha256"].get("um.py") == nos_um["sha256"],
         str(selo["sha256"].get("tgl_kernel_proof_manifest.json"))[:16], nos_km["sha256"][:16], selo["sha256"].get("tgl_kernel_proof_manifest.json") == nos_km["sha256"], nos_selo["sha256"][:16]))
print("  o um.py que a Bancada pina == o do Nos agora? %s (a Bancada pina o CAMINHO do Nos: o canonical.py instalado recusa com PIN_CHANGED enquanto forem diferentes)"
      % ((can.get("script") or {}).get("sha256") == nos_um["sha256"]))
bases = {}
for v, pasta in (("v411", os.path.join(CS, r"v412\base_v411")), ("v412", os.path.join(CS, r"v413\base_v412"))):
    d = {k: ev(os.path.join(pasta, k)) for k in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")}
    bases[v] = d
    sj = lj(d["um_absoluto_selo.json"]["path"]) if d["um_absoluto_selo.json"]["existe"] else {}
    print("  base %s (%s): um.py %s | selo %s (um_version=%s, pina um.py igual=%s, pina kernel igual=%s) | kernel %s"
          % (v, pasta, d["um.py"].get("sha256", "AUSENTE")[:16], d["um_absoluto_selo.json"].get("sha256", "AUSENTE")[:16], sj.get("um_version"),
             (sj.get("sha256") or {}).get("um.py") == d["um.py"].get("sha256"), (sj.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") == d["tgl_kernel_proof_manifest.json"].get("sha256"),
             d["tgl_kernel_proof_manifest.json"].get("sha256", "AUSENTE")[:16]))
print("  base v411 == o que a Bancada pina (um.py, selo, kernel registrado)? %s %s %s"
      % (bases["v411"]["um.py"].get("sha256") == (can.get("script") or {}).get("sha256"), bases["v411"]["um_absoluto_selo.json"].get("sha256") == (can.get("seal") or {}).get("sha256"),
         bases["v411"]["tgl_kernel_proof_manifest.json"].get("sha256") == sinc.get("kernel_manifesto_sha256")))
print("  base v412 == o Nos agora (um.py, selo, kernel)? %s %s %s"
      % (bases["v412"]["um.py"].get("sha256") == nos_um["sha256"], bases["v412"]["um_absoluto_selo.json"].get("sha256") == nos_selo["sha256"],
         bases["v412"]["tgl_kernel_proof_manifest.json"].get("sha256") == nos_km["sha256"]))

print("\n(3) a selecao do gerar_cadeia_de_selos.py (R3_5, l.54-69), refeita aqui sem gravar: elo v411 -> v412")
s_ant, s_novo = bases["v411"]["um.py"]["sha256"][:16], bases["v412"]["um.py"]["sha256"][:16]
achados = []
for rp in sorted(glob.glob(os.path.join(CS, "v412", "APLICADO_AO_CANONICO_*.json"))):
    rj = lj(rp)
    b = (rj.get("backups") or {}).get("um.py") or {}
    n = rj.get("um_py_novo") or {}
    print("  %s: backup um.py sha16 %s | um_py_novo sha16 %s" % (os.path.basename(rp), b.get("sha16"), n.get("sha16")))
    if b.get("sha16") == s_ant and n.get("sha16") == s_novo:
        achados.append((rp, rj))
print("  registros que conferem (exigido exatamente 1):", len(achados))
for rp, rj in achados:
    linha("registro do instalador " + os.path.basename(rp), ev(rp))
    for nome, base_k in (("um.py", "um.py"), ("um_absoluto_selo.json", "um_absoluto_selo.json"), ("tgl_kernel_proof_manifest.json", "tgl_kernel_proof_manifest.json")):
        bk = (rj.get("backups") or {}).get(nome) or {}
        e = ev(bk.get("backup") or "")
        linha("backup " + os.path.basename(bk.get("backup") or "?"), e)
        if e.get("existe"):
            print("      == copia base v411 (%s)? %s | sha16 do registro %s confere? %s"
                  % (base_k, e["sha256"] == bases["v411"][base_k].get("sha256"), bk.get("sha16"), e["sha256"].startswith(str(bk.get("sha16")))))

print("\n(4) recibos e instantes")
r_pin411 = lj(os.path.join(CS, r"v411\PINO_RECIBO_PRE_SELO_v411.json"))
print("  PINO_RECIBO_PRE_SELO_v411: veredito=%s | utilizavel=%s | quando=%s | versao_nos=%s"
      % (r_pin411.get("veredito"), r_pin411.get("utilizavel_como_recibo_pre_selo_do_B_n"), r_pin411.get("quando"), r_pin411.get("versao_nos")))
for p in sorted(glob.glob(os.path.join(BAN, r"estado\sincronizacao\RECIBO_SINCRONIZACAO_v41[01]_*.json"))) + sorted(glob.glob(os.path.join(BAN, r"estado\sincronizacao\RECIBO_SINCRONIZACAO_v394_*.json"))):
    r = lj(p)
    print("  %s: veredito=%s | inicio=%s | fim=%s | salto=%s" % (os.path.basename(p), r.get("veredito"), r.get("inicio_utc"), r.get("fim_utc"),
          (None if not r.get("salto") else {"de": r["salto"]["de"]["versao"], "ate": r["salto"]["ate"]["versao"], "puladas": r["salto"]["versoes_puladas"], "proxima": r["salto"]["proxima_a_selar"]})))
for nome in ("RECIBO_PARADA_v411.json", "RECIBO_RELIGAMENTO_v411.json"):
    r = lj(os.path.join(CS, "v411", "bancada_B3_servico", nome))
    print("  %s: pid=%s | hora=%s | no_ar_desde=%s | pronta=%s | comando=%s" % (nome, r.get("pid"), r.get("hora"), r.get("no_ar_desde"), r.get("pronta"), r.get("comando") or r.get("religar")))
for v in ("v394",):
    for p in sorted(glob.glob(os.path.join(CS, v, "bancada_B3_servico", "RECIBO_PARADA_%s.json" % v))):
        r = lj(p)
        print("  %s: pid=%s | hora=%s | pid_estado=%s" % (os.path.basename(p), r.get("pid"), r.get("hora"), str(r.get("pid_estado"))[:220]))
for p in sorted(glob.glob(os.path.join(NOS, "um.py.bak_2026111*"))):
    print("  backup do instalador no Nos:", os.path.basename(p))

print("\n(5) mtimes")
mais_novo = (0, None)
for dp, dn, fn in os.walk(BAN):
    if "__pycache__" in dp.split(os.sep):
        continue
    for f in fn:
        try:
            t = os.path.getmtime(os.path.join(dp, f))
        except OSError:
            continue
        if t > mais_novo[0]:
            mais_novo = (t, os.path.join(dp, f))
print("  arquivo mais novo da Bancada (fora __pycache__): %s | %s" % (datetime.datetime.fromtimestamp(mais_novo[0]).strftime("%Y-%m-%d %H:%M:%S"), mais_novo[1]))
