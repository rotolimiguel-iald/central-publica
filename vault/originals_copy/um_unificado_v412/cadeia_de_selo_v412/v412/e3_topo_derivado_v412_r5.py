# -*- coding: utf-8 -*-
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R5)] copia de e3_topo_derivado_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R5_PIPELINE_v412.json (derivador: e5_70_derivar_ensaio_r5_v412.py). O original fica intacto.
"""e3_topo_derivado_v412.py -- deriva, POR SCRIPT, o texto ratificado do topo da v412: e' o TOPO_RATIFICADO_v411.json com SO' a troca da frase final de P = nP do resumo (a antiga e a nova vem do CANDIDATO_v412.json, chave resumo_troca_de_pnp; nada digitado).
Grava TOPO_RATIFICADO_v412_DERIVADO.json na pasta da cadeia (por temporario, conferindo o tamanho) com a proveniencia; o resto do topo (o resultado do teste com a natureza, os marcadores, o painel do README, a frase de estado) fica como a v411 o escreveu.
Os conferidores do topo (topo_com_resultado_v412, conferir_rito_v412) leem DL.TOPO_RATIFICADO_ARQ: o ensaio e a cadeia o apontam para este arquivo. Script da cadeia; nada daqui entra no programa."""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(HERE), "v411", "TOPO_RATIFICADO_v411.json")
MANIF = os.path.join(HERE, "CANDIDATO_v412.json")
SAIDA = os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")


def derivar():
    raw = open(BASE, "rb").read()
    d = json.loads(raw.decode("utf-8"))
    troca = json.load(open(MANIF, encoding="utf-8"))["resumo_troca_de_pnp"]
    saida = json.loads(raw.decode("utf-8"))
    n_trocas = 0
    for lang in ("pt", "en"):
        antiga, nova = troca[lang]["antiga"], troca[lang]["nova"]
        assert saida[lang].count(antiga) == 1, ("a frase antiga de P = nP nao esta uma vez so' no resumo ratificado da v411", lang, saida[lang].count(antiga))
        saida[lang] = saida[lang].replace(antiga, nova)
        assert saida[lang].count(nova) == 1 and antiga not in saida[lang]
        n_trocas += 1
    assert n_trocas == 2 and all(saida[k] == d[k] for k in saida if k not in ("pt", "en", "derivacao_v412"))
    saida["derivacao_v412"] = {"o_que_e": "o texto ratificado do topo da v411 com SO' a troca da frase final de P = nP do resumo (PT e EN); derivado por script, nada digitado",
                               "base": {"arquivo": "v411\\TOPO_RATIFICADO_v411.json", "sha256": hashlib.sha256(raw).hexdigest()},
                               "troca": {"manifesto": "CANDIDATO_v412.json", "chave": "resumo_troca_de_pnp", "sha256_do_manifesto": hashlib.sha256(open(MANIF, "rb").read()).hexdigest(),
                                         "antiga_pt_sha256": hashlib.sha256(troca["pt"]["antiga"].encode("utf-8")).hexdigest(), "nova_pt_sha256": hashlib.sha256(troca["pt"]["nova"].encode("utf-8")).hexdigest(),
                                         "antiga_en_sha256": hashlib.sha256(troca["en"]["antiga"].encode("utf-8")).hexdigest(), "nova_en_sha256": hashlib.sha256(troca["en"]["nova"].encode("utf-8")).hexdigest()}}
    return saida


if __name__ == "__main__":
    s = derivar()
    b = json.dumps(s, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(SAIDA) and open(SAIDA, "rb").read() == b:
        print("ja' igual:", SAIDA); sys.exit(0)
    if os.path.exists(SAIDA):
        open(SAIDA + ".bak_" + __import__("time").strftime("%Y%m%d_%H%M%S"), "wb").write(open(SAIDA, "rb").read())
    open(SAIDA + ".tmp", "wb").write(b)
    assert os.path.getsize(SAIDA + ".tmp") == len(b) > 10000
    os.replace(SAIDA + ".tmp", SAIDA)
    print("gravado", SAIDA, len(b), "bytes, sha16", hashlib.sha256(b).hexdigest()[:16])
