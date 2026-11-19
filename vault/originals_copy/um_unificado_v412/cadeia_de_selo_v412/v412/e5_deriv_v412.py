"""R5: o derivador comum. Cada copia `_r5` nasce de um original (que fica intacto) por trocas de TEXTO EXATO, cada uma com o numero minimo de ocorrencias exigido e o numero achado registrado em DERIVACAO_R5_PIPELINE_v412.json
(o registro acumula; cada destino tem uma entrada, regravada se o destino for regerado). O destino tem de compilar (py). Escrita por temporario; backup de bytes do destino anterior."""
import datetime, hashlib, json, os
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
LOGP = D / "DERIVACAO_R5_PIPELINE_v412.json"
sha = lambda b: hashlib.sha256(b).hexdigest()
CAB = "# [DERIVADO v412 r5, claude-construtor-v412 (contrato R5)] copia de %s; trocas de texto exato com contagem registrada em DERIVACAO_R5_PIPELINE_v412.json (derivador: %s). O original fica intacto."
# os modulos da cadeia que ganham copia _r5: toda linha de import e todo nome de arquivo .py deles passa a apontar para a copia
MODS_R5 = ["delta_v412", "registros_v412", "textos_registros_v412", "guarda_frases_v412", "runtime_v412_codigo", "texto_publico_v412", "blocos_texto_publico_v412", "gerar_candidato_v412", "verificar_historia_texto_v412"]


def trocas_de_import(t, mods=None):
    """as trocas (velho, novo, 0) que apontam os imports e os nomes de arquivo para as copias _r5; so' formas de import e de nome de arquivo, nunca a palavra solta (ha' chaves do core com o mesmo nome)"""
    out = []
    for m in (mods or MODS_R5):
        for velho, novo in (("import %s as " % m, "import %s_r5 as " % m), ("import %s  " % m, "import %s_r5  " % m), ("import %s\n" % m, "import %s_r5\n" % m), ("from %s import " % m, "from %s_r5 import " % m),
                            ('"%s.py"' % m, '"%s_r5.py"' % m), ("'%s.py'" % m, "'%s_r5.py'" % m)):
            if velho in t:
                out.append((velho, novo, 1))
    return out


def derivar(origem, destino, trocas, derivador, imports=True, mods=None):
    t = (D / origem).read_bytes().decode("utf-8")
    assert "\r" not in t, origem
    reg = {"origem": origem, "origem_sha16": sha(t.encode())[:16], "destino": destino, "derivador": derivador, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "trocas": []}
    todas = (trocas_de_import(t, mods) if imports else []) + list(trocas)
    for velho, novo, minimo in todas:
        c = t.count(velho)
        assert c >= minimo, ("o original nao tem o trecho esperado", origem, velho[:120], c, minimo)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:160], "novo": novo[:160], "ocorrencias": c})
    linhas = t.split("\n")
    k = 1 if linhas[0].startswith("# -*- coding") else 0
    t = "\n".join(linhas[:k] + [CAB % (origem, derivador)] + linhas[k:])
    if destino.endswith(".py"):
        compile(t, destino, "exec")
    out = t.encode("utf-8")
    reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    p = D / destino
    if not (p.exists() and p.read_bytes() == out):
        if p.exists():
            bk = Path(str(p) + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes()); assert bk.read_bytes() == p.read_bytes()
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(out); assert tmp.stat().st_size == len(out); os.replace(tmp, p)
    log = json.loads(LOGP.read_bytes().decode("utf-8")) if LOGP.exists() else {"derivacoes": {}}
    log["derivacoes"][destino] = reg
    tmp = Path(str(LOGP) + ".tmp"); b = json.dumps(log, ensure_ascii=False, indent=1).encode("utf-8"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, LOGP)
    print("derivado: %-44s <- %-40s %6d bytes sha16 %s | trocas %d (%s)" % (destino, origem, len(out), sha(out)[:16], len(reg["trocas"]), ", ".join(str(x["ocorrencias"]) for x in reg["trocas"])))
    return reg
