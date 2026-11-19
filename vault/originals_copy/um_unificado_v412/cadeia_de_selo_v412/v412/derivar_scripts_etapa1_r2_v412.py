# -*- coding: utf-8 -*-
"""derivar_scripts_etapa1_r2_v412.py -- (claude-construtor-v412, complemento da Etapa 1, 17/11/2026) gera, em COPIAS novas com sufixo `_r2` (os originais ficam intactos), os scripts da
Etapa 1 que pressupunham a primeira lista (34 modulos, insumos\\MANIFESTO_PEDRAS_v412.json, insumos\\pedras) para a QUARTA lista (40 modulos, insumos\\MANIFESTO_PEDRAS_v412_R4.json,
insumos\\pedras_r4, insumos\\ANCORAS_PROPOSTAS_v412_R4.json). Cada troca e' de texto exato e conferida (numero de ocorrencias); falha visivel se o original nao tem o trecho esperado.
Gera: pos_build_kernel_v412_r2.py, reconstruir_kernel_v412_r2.py, pre_colisao_declaracoes_v412_r2.py. (conferir_ancoras_propostas_v412_r2.py e gerar_pronto_etapa1_v412_r2.py sao escritos a mao.)
O preparar_bundle_v412.py, o lean_texto_v412.py e o copiar_logs_do_kernel_v412.py NAO precisam de copia: o primeiro recebe --manifesto/--pedras, os outros leem so' o que o preparo e o
pos_build gravam em kernel\\.
uso: C:\\Python314\\python.exe -B -X utf8 derivar_scripts_etapa1_r2_v412.py"""
import hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sha = lambda b: hashlib.sha256(b).hexdigest()


def derivar(origem, destino, trocas, cabecalho):
    po = os.path.join(HERE, origem); pd_ = os.path.join(HERE, destino)
    b = open(po, "rb").read()
    assert b"\r" not in b, ("CR no original", origem)
    t = b.decode("utf-8")
    for velho, novo, n in trocas:
        assert t.count(velho) == n, ("o original nao tem o trecho esperado o numero esperado de vezes", origem, velho[:80], t.count(velho), n)
        t = t.replace(velho, novo)
    linhas = t.split("\n")
    # o cabecalho entra logo depois da linha de codificacao
    assert linhas[0].startswith("# -*- coding")
    t = "\n".join([linhas[0], cabecalho] + linhas[1:])
    out = t.encode("utf-8")
    if os.path.exists(pd_):
        if open(pd_, "rb").read() == out:
            print("ja existe, igual:", destino); return
        assert "--regerar" in sys.argv, ("a copia _r2 ja existe e difere: nao sobrescrevo sem --regerar", destino)
        bk = pd_ + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        open(bk, "wb").write(open(pd_, "rb").read()); assert open(bk, "rb").read() == open(pd_, "rb").read()
        print("backup de bytes:", bk)
    with open(pd_ + ".tmp", "wb") as f:
        f.write(out)
    assert os.path.getsize(pd_ + ".tmp") == len(out)
    os.replace(pd_ + ".tmp", pd_)
    print("gerado:", destino, len(out), "bytes | sha16", sha(out)[:16], "| original", sha(b)[:16])


R4 = "MANIFESTO_PEDRAS_v412_R4.json"
derivar("pos_build_kernel_v412.py", "pos_build_kernel_v412_r2.py", [
    ('os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412.json")', 'os.path.join(HERE, "insumos", "%s")' % R4, 2),
    ("        shutil.rmtree(ARV)\n",
     "        # (r2: a arvore so-fontes da Etapa 1 NAO e' apagada: vai para arvore_<etapa1|anterior>_<data>, ao lado, e a nova nasce no mesmo caminho)\n"
     "        os.replace(ARV, ARV + \"_anterior_\" + datetime.datetime.now().strftime(\"%Y%m%d_%H%M%S\"))\n", 1),
    ('        if md in NEWMODS and st == "Built":\n',
     '        if md in NEWMODS and st in ("Built", "Replayed") and (st == "Built" or md not in avisos):   # (r2: o modulo que o build nao recompilou mostra o aviso no bloco Replayed; o bloco Built manda)\n', 1),
    ('"nota": "sem bloco Built neste log" if modo.get(m) != "Built" else None', '"nota": "sem bloco Built nem Replayed neste log (sem mensagem)" if modo.get(m) is None else None', 1),
    ('"gerado por pos_build_kernel_v412.py (preparacao, Etapa 1, 17/11/2026); NAO conferido',
     '"gerado por pos_build_kernel_v412_r2.py (complemento da Etapa 1, quarta lista de pedras, 17/11/2026); NAO conferido', 1),
    ('medido por pos_build_kernel_v412.py sobre o log do Audit', 'medido por pos_build_kernel_v412_r2.py sobre o log do Audit', 1),
    ('e A FRIO nos " + str(N_NOVOS) + " modulos novos (um a um, na ordem topologica; linha Built)',
     'e RECOMPILOU so\' o que mudou ou depende do que mudou (" + str(N_NOVOS) + " modulos no bundle, na ordem topologica; kernel/ULTIMA_INSTALACAO_v412.json diz quais)', 1),
],"# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de pos_build_kernel_v412.py para a QUARTA lista (40 modulos): le insumos\\MANIFESTO_PEDRAS_v412_R4.json; a arvore so-fontes da Etapa 1 e' movida, nao apagada. O resto e' identico (derivar_scripts_etapa1_r2_v412.py).")

derivar("reconstruir_kernel_v412.py", "reconstruir_kernel_v412_r2.py", [
    ('extra = []\nfor k in ("--manifesto", "--pedras"):\n    if k in sys.argv:\n        extra += [k, sys.argv[sys.argv.index(k) + 1]]\n',
     'extra = []\nPADRAO = {"--manifesto": os.path.join(HERE, "insumos", "%s"), "--pedras": os.path.join(HERE, "insumos", "pedras_r4")}   # (r2: a quarta lista e\' o padrao)\n'
     'for k in ("--manifesto", "--pedras"):\n    extra += [k, sys.argv[sys.argv.index(k) + 1] if k in sys.argv else PADRAO[k]]\n' % R4, 1),
    ('"pos_build_kernel_v412.py"', '"pos_build_kernel_v412_r2.py"', 1),
    ('"3 pos_build_kernel_v412"', '"3 pos_build_kernel_v412_r2"', 1),
    ('RECONSTRUCAO DO KERNEL v412: TUDO PASSOU', 'RECONSTRUCAO DO KERNEL v412 (r2, quarta lista): TUDO PASSOU', 1),
], "# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de reconstruir_kernel_v412.py: o padrao passa a ser a QUARTA lista (insumos\\MANIFESTO_PEDRAS_v412_R4.json + insumos\\pedras_r4) e o passo 3 e' o pos_build_kernel_v412_r2.py; --manifesto/--pedras ainda valem. Para trocar uma fonte: regerar o manifesto e rodar este comando.")

derivar("pre_colisao_declaracoes_v412.py", "pre_colisao_declaracoes_v412_r2.py", [
    ('os.path.join(PK, "insumos", "MANIFESTO_PEDRAS_v412.json")', 'os.path.join(PK, "insumos", "%s")' % R4, 1),
    ('PED = os.path.join(PK, "insumos", "pedras")', 'PED = os.path.join(PK, "insumos", "pedras_r4")', 1),
    ('OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v412.json")', 'OUT = os.path.join(PK, "kernel", "PRE_COLISAO_v412_R2.json")', 1),
    ('"colisao_entre_os_34"', '"colisao_entre_os_40"', 1),
], "# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de pre_colisao_declaracoes_v412.py para a QUARTA lista (40 modulos); grava kernel\\PRE_COLISAO_v412_R2.json (o da Etapa 1 fica). Os nomes do kernel vem do audit.log da v411.")
