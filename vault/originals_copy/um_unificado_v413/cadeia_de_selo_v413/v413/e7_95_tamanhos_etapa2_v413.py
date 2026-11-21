# -*- coding: utf-8 -*-
"""Etapa 2 da v413: mede o que esta etapa criou em disco (por tamanho lido do disco) e grava TAMANHOS_ETAPA2_v413.json: na pasta da cadeia, os arquivos com data de modificacao depois do inicio da etapa que nao sao
da Etapa 1 nem do B(n) (a pasta bancada\\ e' de outro agente) nem da gerencia (os do contrato e da pagina); fora de work\\, as pastas de C:\\t\\k413c que a Etapa 2 cria (candidato, ensaio, dry, texto_teste, sim_*, imp_*).
Apaga os .tmp desta etapa que tenham sobrado. So' mede; nada mais e' apagado."""
import datetime, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

INICIO = time.mktime(time.strptime("2026-11-20 21:40:00", "%Y-%m-%d %H:%M:%S"))   # (a ordem da Etapa 2 foi gravada as 21:37; o primeiro arquivo desta etapa e' posterior)
GERENCIA = {"CONTRATO_v413_R2.md", "ORDEM_ETAPA_3_v413.md", "PLANO_DA_NOITE_v413_20nov.md"}
# (correcao) so' as subpastas que a Etapa 2 cria entram na conta; as outras subpastas recentes sao de outros agentes (bateria_pre_selo do B(n), etapa3, pos_rito, vinculo, contrato_REV1/REV2 da gerencia)
ETAPA2_SUBPASTAS = ("proposta_pagina_R1",)
# arquivos da raiz de OUTROS agentes, reconhecidos pelo conteudo ou pelo nome (a regra fica no recibo, com o motivo de cada um)
PREFIXOS_BN = ("PINOS_BN_", "PINO_RECIBO_PRE_SELO_", "PRECONDICOES_BN_", "PROVA_PRODUCAO_INTACTA_")


def de_outro_agente(p):
    nome = re.sub(r"\.bak_\d{8}_\d{6}$", "", p.name)   # o backup de bytes segue o dono do arquivo de que e' copia
    if nome in GERENCIA or nome.startswith(("acom_c1_", "PRONTO_ETAPA3", "ORDEM_", "fazer_", "gravar_fala", "mapa_", "marcar_plano")):
        return "da gerencia"
    if nome.startswith(PREFIXOS_BN):
        return "do pre-selo do B(n)"
    try:
        cab = p.read_bytes()[:1200].decode("utf-8", "replace")
    except OSError:
        return None
    if "claude-construtor-v413" in cab:
        return None
    if "Etapa 3" in cab or "rito_v413.sh" in cab:
        return "da Etapa 3"
    return None


apagados_tmp = []
na_pasta = []
excluidos = []
for p in sorted(L.D.iterdir()):
    if p.is_dir():
        if p.name not in ETAPA2_SUBPASTAS:
            continue
        for q in p.rglob("*"):
            if q.is_file() and q.stat().st_mtime >= INICIO:
                na_pasta.append((str(q.relative_to(L.D)), q.stat().st_size))
        continue
    if p.name.endswith(".tmp") and p.stat().st_mtime >= INICIO:
        p.unlink(); apagados_tmp.append(p.name); continue
    if p.stat().st_mtime >= INICIO:
        m = de_outro_agente(p)
        if m:
            excluidos.append({"arquivo": p.name, "motivo": m}); continue
        na_pasta.append((p.name, p.stat().st_size))
fora = {}
k = L.SANDBOX_PAI
for p in sorted(k.iterdir()):
    if p.is_dir() and (p.name.startswith(("candidato", "ensaio", "dry_v413", "texto_teste", "sim_", "imp_", "falso_nos_v413", "candidatos_anteriores")) or p.name == "guarda_privada_tmp"):
        if p.stat().st_mtime < INICIO and not p.name.startswith(("candidato", "ensaio")):
            continue
        n = 0; t = 0
        for q in p.rglob("*"):
            if q.is_file():
                n += 1; t += q.stat().st_size
        fora[str(p)] = {"arquivos": n, "bytes": t}
vb25 = Path(r"C:\t\vb25")
out = {"contrato": "TAMANHOS_ETAPA2_v413", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "na_pasta_da_cadeia": {"n": len(na_pasta), "bytes": sum(b for _, b in na_pasta), "arquivos": [{"arquivo": a, "bytes": b} for a, b in na_pasta]},
       "excluidos_de_outros_agentes": excluidos, "subpastas_da_etapa_2": list(ETAPA2_SUBPASTAS),
       "fora_de_work": fora, "bytes_fora": sum(v["bytes"] for v in fora.values()), "tmp_apagados": apagados_tmp, "sandbox_curto_da_etapa_2_existe_no_fim": vb25.exists(), "sandbox_curto_do_bn_tocado": False,
       "nota": "o C:\\t\\vb24 (do pre-selo do B(n)) nunca foi criado nem tocado pela Etapa 2; o vb25 e' o proprio da Etapa 2 (as guardas estaticas da Bancada o criam e o apagam vazio no fim)"}
L.salvar_json(L.D / "TAMANHOS_ETAPA2_v413.json", out)
print("na pasta da cadeia: %d arquivos, %d bytes | fora de work: %d bytes em %d pastas | .tmp apagados: %d | vb25 no fim: %s" % (len(na_pasta), out["na_pasta_da_cadeia"]["bytes"], out["bytes_fora"], len(fora), len(apagados_tmp), vb25.exists()))
