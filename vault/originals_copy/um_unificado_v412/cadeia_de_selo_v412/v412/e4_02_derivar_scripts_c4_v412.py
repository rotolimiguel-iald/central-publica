"""R4 (contrato R4, setima lista, 42 modulos): deriva, por trocas de texto exato com contagem registrada, as copias `_c4` dos scripts do kernel que pressupunham a QUINTA lista (R5/pedras_r5), a partir das `_r3`
(e do pos_build `_r4` com a checagem do Built corrigida). Os originais ficam intactos. Gera: guardar_r3_antes_do_c4_v412.py, pre_colisao_declaracoes_v412_c4.py, pos_build_kernel_v412_c4.py, reconstruir_kernel_v412_c4.py,
conferir_ancoras_propostas_v412_c4.py. Grava DERIVACAO_C4_v412.json."""
import datetime, hashlib, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sha = lambda b: hashlib.sha256(b).hexdigest()
LOG = []
CAB = "# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de %s para a SETIMA lista de pedras (insumos\\MANIFESTO_PEDRAS_v412_R7.json, insumos\\pedras_r7; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada)."


def derivar(origem, destino, trocas):
    t = (D / origem).read_bytes().decode("utf-8")
    assert "\r" not in t
    reg = {"origem": origem, "origem_sha16": sha(t.encode())[:16], "destino": destino, "trocas": []}
    for velho, novo, minimo in trocas:
        c = t.count(velho)
        assert c >= minimo, ("o original nao tem o trecho esperado", origem, velho[:80], c, minimo)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:80], "novo": novo[:80], "ocorrencias": c})
    linhas = t.split("\n")
    assert linhas[0].startswith("# -*- coding")
    t = "\n".join([linhas[0], CAB % origem] + linhas[1:])
    compile(t, destino, "exec")
    out = t.encode("utf-8")
    reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    p = D / destino
    if p.exists():
        if p.read_bytes() == out:
            print("ja existe, igual:", destino); LOG.append(reg); return
        bk = Path(str(p) + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes())
    tmp = Path(str(p) + ".tmp"); tmp.write_bytes(out); assert tmp.stat().st_size == len(out); tmp.replace(p)
    LOG.append(reg)
    print("gerado:", destino, len(out), "bytes | sha16", sha(out)[:16], "|", [(x["velho"][:30], x["ocorrencias"]) for x in reg["trocas"]])


R5R7 = [("MANIFESTO_PEDRAS_v412_R5.json", "MANIFESTO_PEDRAS_v412_R7.json", 0), ("ANCORAS_PROPOSTAS_v412_R5.json", "ANCORAS_PROPOSTAS_v412_R7.json", 0), ("pedras_r5", "pedras_r7", 0), ("QUINTA lista", "SETIMA lista", 0)]
derivar("guardar_r2_antes_do_r3_v412.py", "guardar_r3_antes_do_c4_v412.py", [
    (".bak_r2", ".bak_r3", 3), ("GUARDA_R2_v412.json", "GUARDA_R3_v412.json", 2), ("PRONTO_PARA_CANDIDATO_v412_R2.json", "PRONTO_PARA_CANDIDATO_v412_R3.json", 1), ("TAMANHOS_CRIADOS_v412_R2.json", "TAMANHOS_CRIADOS_v412_R3.json", 1),
    ("guardar_r2_antes_do_r3_v412.py", "guardar_r3_antes_do_c4_v412.py", 1), ("do estado do fecho R2 (quarta lista, 40 modulos)", "do estado do fecho R3 (quinta lista, 40 modulos)", 1),
    ('if ".bak" in n or n.endswith(".tmp") or n == "CODIGO_R4_R5_v412.json":', 'if ".bak" in n or n.endswith(".tmp") or n in ("CODIGO_R4_R5_v412.json", "GUARDA_R2_v412.json"):', 1)])
derivar("pre_colisao_declaracoes_v412_r3.py", "pre_colisao_declaracoes_v412_c4.py", R5R7 + [("_R3.json", "_R4.json", 1)])
derivar("pos_build_kernel_v412_r4.py", "pos_build_kernel_v412_c4.py", R5R7 + [("pos_build_kernel_v412_r4", "pos_build_kernel_v412_c4", 0), ("== 40", "== 42", 0)])
derivar("reconstruir_kernel_v412_r3.py", "reconstruir_kernel_v412_c4.py", R5R7 + [("pos_build_kernel_v412_r3", "pos_build_kernel_v412_c4", 2)])
derivar("conferir_ancoras_propostas_v412_r3.py", "conferir_ancoras_propostas_v412_c4.py", R5R7 + [("_R3.json", "_R4.json", 1), ("conferir_ancoras_propostas_v412_r3", "conferir_ancoras_propostas_v412_c4", 0), ("pos_build_kernel_v412_r3", "pos_build_kernel_v412_c4", 0)])
(D / "DERIVACAO_C4_v412.json").write_bytes(json.dumps({"quando": datetime.datetime.now().isoformat(timespec="seconds"), "derivacoes": LOG}, ensure_ascii=False, indent=1).encode("utf-8"))
