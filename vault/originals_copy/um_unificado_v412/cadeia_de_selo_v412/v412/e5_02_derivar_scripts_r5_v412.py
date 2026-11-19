"""R5 (contrato R5, decima lista, 153 modulos): deriva, por trocas de texto exato com contagem registrada, as copias `_r5` dos scripts do kernel que pressupunham a SETIMA lista (R7/pedras_r7),
a partir das `_c4`. Os originais ficam intactos. Gera: guardar_c4_antes_do_r5_v412.py, pre_colisao_declaracoes_v412_r5.py, pos_build_kernel_v412_r5.py, reconstruir_kernel_v412_r5.py,
conferir_nos_intacto_r5_v412.py. Grava DERIVACAO_R5_v412.json."""
import datetime, hashlib, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sha = lambda b: hashlib.sha256(b).hexdigest()
LOG = []
CAB = "# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R5)] copia de %s para a DECIMA lista de pedras (insumos\\MANIFESTO_PEDRAS_v412_R10.json, insumos\\pedras_r10; 153 modulos); e5_02_derivar_scripts_r5_v412.py (trocas de texto exato com contagem registrada)."


def derivar(origem, destino, trocas):
    t = (D / origem).read_bytes().decode("utf-8")
    assert "\r" not in t
    reg = {"origem": origem, "origem_sha16": sha(t.encode())[:16], "destino": destino, "trocas": []}
    for velho, novo, minimo in trocas:
        c = t.count(velho)
        assert c >= minimo, ("o original nao tem o trecho esperado", origem, velho[:80], c, minimo)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:90], "novo": novo[:90], "ocorrencias": c})
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
    print("gerado:", destino, len(out), "bytes | sha16", sha(out)[:16], "|", [(x["velho"][:34], x["ocorrencias"]) for x in reg["trocas"]])


R7R10 = [("MANIFESTO_PEDRAS_v412_R7.json", "MANIFESTO_PEDRAS_v412_R10.json", 0), ("ANCORAS_PROPOSTAS_v412_R7.json", "ANCORAS_PROPOSTAS_v412_R10.json", 0), ("pedras_r7", "pedras_r10", 0), ("SETIMA lista", "DECIMA lista", 0)]
derivar("guardar_r3_antes_do_c4_v412.py", "guardar_c4_antes_do_r5_v412.py", [
    (".bak_r3", ".bak_c4", 3), ("GUARDA_R3_v412.json", "GUARDA_C4_v412.json", 2), ("PRONTO_PARA_CANDIDATO_v412_R3.json", "PRONTO_PARA_CANDIDATO_v412_R4.json", 1), ("TAMANHOS_CRIADOS_v412_R3.json", "TAMANHOS_CRIADOS_v412_R4.json", 1),
    ("guardar_r3_antes_do_c4_v412.py", "guardar_c4_antes_do_r5_v412.py", 1), ("do estado do fecho R3 (quinta lista, 40 modulos)", "do estado do fecho R4 (setima lista, 42 modulos)", 1),
    ('n in ("CODIGO_R4_R5_v412.json", "GUARDA_R2_v412.json"):', 'n in ("CODIGO_R4_R5_v412.json", "GUARDA_R2_v412.json", "GUARDA_R3_v412.json"):', 1)])
derivar("pre_colisao_declaracoes_v412_c4.py", "pre_colisao_declaracoes_v412_r5.py", R7R10 + [("_R4.json", "_R5.json", 1), ('"colisao_entre_os_40"', '"colisao_entre_os_modulos_da_lista"', 1)])
derivar("pos_build_kernel_v412_c4.py", "pos_build_kernel_v412_r5.py", R7R10 + [
    ("BUILT_CHECAGEM_CORRIGIDA_R4_v412.json", "BUILT_CHECAGEM_CORRIGIDA_R5_v412.json", 1),
    ("medido por pos_build_kernel_v412_r3.py sobre o log do Audit do sandbox", "medido por pos_build_kernel_v412_r5.py sobre o log do Audit do sandbox", 1),
    ("gerado por pos_build_kernel_v412_r3.py (continuacao 2 do complemento da Etapa 1, quinta lista de pedras, 17/11/2026)", "gerado por pos_build_kernel_v412_r5.py (Etapa 2 pelo contrato R5, decima lista de pedras, 18/11/2026)", 1),
    ("e RECOMPILOU so' o que mudou ou depende do que mudou (\" + str(N_NOVOS) + \" modulos no bundle, na ordem topologica; kernel/ULTIMA_INSTALACAO_v412.json diz quais)",
     "e compilou os modulos do bundle (\" + str(N_NOVOS) + \" modulos, na ordem topologica; quais tiveram linha Built neste build esta' em kernel/POS_BUILD_v412.json, campo modo_dos_modulos_no_build)", 1),
    ("os logs lidos de kernel/lake_build.log (build da quinta lista, sem reconstruir)", "os logs lidos de kernel/lake_build.log (build da decima lista)", 1)])
derivar("reconstruir_kernel_v412_c4.py", "reconstruir_kernel_v412_r5.py", R7R10 + [("pos_build_kernel_v412_c4", "pos_build_kernel_v412_r5", 2),
                                                                                ('print("RECONSTRUCAO DO KERNEL v412 (r3, quinta lista): TUDO PASSOU")', 'print("RECONSTRUCAO DO KERNEL v412 (r5, decima lista): TUDO PASSOU")', 1)])
derivar("conferir_nos_intacto_c4_v412.py", "conferir_nos_intacto_r5_v412.py", R7R10 + [("reconstruir_c4_inicio_epoch.txt", "reconstruir_r5_inicio_epoch.txt", 2), ("NOS_INTACTO_C4_v412.json", "NOS_INTACTO_R5_v412.json", 2),
                                                                                    ("conferir_nos_intacto_c4_v412.py", "conferir_nos_intacto_r5_v412.py", 2), ("nenhum dos 42 modulos do manifesto R7", "nenhum dos 153 modulos do manifesto R10", 1),
                                                                                    ("n_modulos_do_manifesto_R7", "n_modulos_do_manifesto_R10", 1)])
(D / "DERIVACAO_R5_v412.json").write_bytes(json.dumps({"quando": datetime.datetime.now().isoformat(timespec="seconds"), "derivacoes": LOG}, ensure_ascii=False, indent=1).encode("utf-8"))
