# -*- coding: utf-8 -*-
"""adaptar_rito_e_carimbo_v412.py -- (gerencia c1, 18/11/2026, Etapa 3 ENXUTA: PLANO_ETAPA3_ENXUTA_v412.md) adapta DE VERDADE o rito_v412.sh
e o carimbar_stdout_v412.py herdados da v411. O CORPO dos dois e' generico (o rito confere o um.py contra ESPERADOS_v412.json[candidato_sha16],
guarda os processos, para e religa o servidor do modelo nativo, roda `echo 1 | python um.py` com o carimbador e grava RITO_RC; o carimbador
e' um tee com hora por linha): nada neles depende de modulo novo. Muda so' o CABECALHO descritivo do rito (a marca; a linha que dizia
NENHUM modulo novo; o TEMPO ESPERADO, agora lido das marcas do build a frio da v412 no sandbox k412c) e a marca do carimbador.
Backup de bytes antes; confere por texto exato. Uso: adaptar_rito_e_carimbo_v412.py [--executar]"""
import hashlib, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; EXEC = "--executar" in sys.argv; TS = time.strftime("%Y%m%d_%H%M%S")
marcas = (V / "kernel" / "construir_marcas.txt").read_text(encoding="utf-8", errors="replace")
ep = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
assert {"epoch_inicio", "epoch_build_fim", "epoch_audit_fim"} <= set(ep), ("o build ainda nao terminou ou as marcas nao tem os epochs", sorted(ep))
n_mod = len(re.findall(r"^modulo=", marcas, re.M)); build_s = ep["epoch_build_fim"] - ep["epoch_inicio"]; audit_s = ep["epoch_audit_fim"] - ep["epoch_build_fim"]
MARCA = "# [ADAPTADO v412, 18/11/2026, gerencia c1 (Etapa 3 enxuta; PLANO_ETAPA3_ENXUTA_v412.md; adaptar_rito_e_carimbo_v412.py)] "
# ---- o rito
p = V / "rito_v412.sh"; a = p.read_bytes().decode("utf-8"); L = a.split("\n")
assert L[1].startswith("# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO") and L[3].startswith("# O RITO v412 (ato da gerencia c1): roda o um.py v412 instalado no Nos -- NENHUM modulo novo")
it = [i for i, l in enumerate(L) if l.startswith("# TEMPO ESPERADO (v412, parametro lido de kernel/construir_marcas.txt")]; assert len(it) == 1
L[1] = MARCA + "o corpo e' generico (nada depende de modulo novo); muda so' este cabecalho descritivo"
L[3] = ("# O RITO v412 (ato da gerencia c1): roda o um.py v412 instalado no Nos (instalar_v412.py) -- 156 MODULOS NOVOS de kernel (a lista R12; o proprio um.py "
        "materializa o corpo embutido em tgl_kernel\\TGLExt e a raiz TGLExt.lean com os 156 imports; o Audit e' o do candidato), os cinco registros novos "
        "(iald_camada_cientifica_v412, leitor_da_formula_v412, matematica_que_restava_v412, parede_do_teste_cego_v412, cunhagens_v412) com as palavras de veredito "
        "do contrato R11; os registros anteriores sao RECRIADOS; nenhuma chave antiga muda fora dos numeros; o gate nao se move; o teste H0DN x BG1 nao se reabre.")
L[it[0]] = ("# TEMPO ESPERADO (v412, lido de kernel/construir_marcas.txt do build A FRIO da lista R12 no sandbox k412c, %s): %d modulos compilados no `lake build` = %d s "
            "e 1 Audit = %d s. No Nos o kernel da v411 ja' esta' compilado em .lake/build: o rito compila os 156 novos, a raiz e o Audit (da ordem do build acima), "
            "mais o resto do rito (a v411 levou 2 h 37 min sem nada a compilar)." % (time.strftime("%d/%m/%Y"), n_mod, build_s, audit_s))
b = "\n".join(L); assert "[A ADAPTAR v412]" not in b
# ---- o carimbador
q = V / "carimbar_stdout_v412.py"; c = q.read_bytes().decode("utf-8"); Lc = c.split("\n")
im = [i for i, l in enumerate(Lc) if l.startswith("# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO")]; assert len(im) == 1
Lc[im[0]] = MARCA + "o corpo e' generico (um tee que carimba a hora de cada linha e confere o sha256 do stdout gravado): nada depende de modulo novo"
d = "\n".join(Lc); assert "[A ADAPTAR v412]" not in d; compile(d, "carimbar_stdout_v412.py", "exec")
print("rito: build %d modulos em %d s, Audit %d s | carimbador: marca trocada" % (n_mod, build_s, audit_s))
if EXEC:
    for arq, x, y in ((p, a, b), (q, c, d)):
        bak = arq.with_name(arq.name + ".bak_antes_da_etapa3_" + TS); bak.write_bytes(x.encode("utf-8")); assert bak.read_bytes() == x.encode("utf-8")
        tmp = arq.with_name(arq.name + ".tmp_c1"); tmp.write_bytes(y.encode("utf-8")); assert tmp.stat().st_size == len(y.encode("utf-8")); tmp.replace(arq)
        print("gravado:", arq.name, "| sha16", hashlib.sha256(arq.read_bytes()).hexdigest()[:16])
