# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: congela em insumos\\pedras\\ as fontes Lean que entram na v412 (copia de BYTES) e gera o manifesto
MANIFESTO_PEDRAS_v412.json, tudo lido dos arquivos: sha256, tamanho, imports, espaco de nomes, numero de declaracoes theorem/lemma.
Nao sobrescreve copia existente com conteudo diferente: nesse caso para e avisa (regerar exige pasta nova ou a palavra da gerencia).
Uso: manifesto_pedras_v412.py [--executar]"""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
C = V / "candidatas_c1"
DEST = V / "insumos" / "pedras"
ENTRAM = [
    # (origem, frente, de quem, revisao/estado)
    (C / "CamadaCientifica.lean", "A", "gerencia", "conferida em 14/11"),
    (C / "MinimoFuncionalDeEnergia.lean", "A", "gerencia", "R2 (REV32); ordem 023 pendente"),
    (C / "OLeitorEALei.lean", "A", "gerencia", "R1 (REV30); ordem 023 pendente"),
    (C / "AContagemEACarga.lean", "A", "gerencia", "R1 (REV34); ordem 023 pendente"),
    (C / "AMaquinaEALeitura.lean", "A", "gerencia", "R1 (REV35); ordem 023 pendente"),
    (C / "OPassoEORetorno.lean", "A", "gerencia", "R1 (REV36); ordem 023 pendente"),
    (C / "OHabitanteDoNome.lean", "A", "gerencia", "aprovada com ressalvas"),
    (C / "NomeComoCodigo.lean", "A", "gerencia", "aprovada com ressalvas"),
    (C / "CopiadorEImpostor.lean", "A", "gerencia", "R9 (REV23); aprovada na ordem 022"),
    (C / "ErgodicidadeDeMautner.lean", "B", "gerencia", "aprovada com ressalvas"),
    (C / "t1" / "dep_codex" / "T1GaussianSpectrum.lean", "B", "Codex", "dependencia da T1 finita"),
    (C / "t1" / "T1CompostoFinito.lean", "B", "gerencia", "R4"),
    (C / "t1" / "T1PontesAoKernel.lean", "B", "gerencia", "R5 (t1/REV5); aprovada na ordem 022"),
    (C / "MontagemDasGamas.lean", "B", "gerencia", "conferida"),
    (C / "BoostEDissipador.lean", "B", "gerencia", "R1 (REV31); ordem 023 pendente"),
    (C / "OParFixaORelogio.lean", "B", "gerencia", "R1 (REV33); ordem 023 pendente"),
    (C / "tipo_iii" / "TipoIIIControles.lean", "B", "gerencia", "R4"),
    (C / "tipo_iii" / "TipoIIIUmSoBoost.lean", "B", "gerencia", "R4"),
]
for p in sorted((C / "tipo_iii" / "dep_codex").glob("*.lean")):
    ENTRAM.append((p, "B", "Codex", "dependencia do tipo III (manifesto dele)"))
for n in ("ProdutoFinito", "ProdutoTresUm", "ConjugacaoFinita", "SpinorToSolder"):
    ENTRAM.append((V / "conferencia_gerencia_16nov" / (n + ".lean"), "B", "Codex", "conferida pela gerencia por recompilacao propria"))
FORA = ["PsionVacuoEModoDoTratado", "DispersaoDoPsionControles", "OVerdadeiroEDivisivel"]

itens, nomes = [], set()
for src, frente, quem, estado in ENTRAM:
    b = src.read_bytes(); t = b.decode("utf-8")
    nome = src.stem
    assert nome not in nomes, "nome repetido: " + nome
    nomes.add(nome)
    imps = re.findall(r"^import\s+(\S+)", t, flags=re.M)
    ns = re.findall(r"^namespace\s+(\S+)", t, flags=re.M)
    itens.append({"modulo": nome, "frente": frente, "de_quem": quem, "estado_da_revisao": estado, "origem": str(src),
                  "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "imports": imps,
                  "imports_de_candidatas": [i for i in imps if not i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL."))],
                  "namespaces": ns, "declaracoes_theorem_lemma": len(re.findall(r"^(?:theorem|lemma)\s", t, flags=re.M)),
                  "linhas_print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)),
                  "sorry": len(re.findall(r"\bsorry\b", re.sub(r"/-.*?-/", "", t, flags=re.S)))})
soltos = sorted({i for it in itens for i in it["imports_de_candidatas"]})
faltam = [i for i in soltos if i not in nomes]
man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "nota": "lido dos arquivos por script; candidatas, nada instalado; a ordem 023 pode mudar TEXTO (cabecalhos e docstrings) de sete fontes: regerar depois dela",
       "n_modulos": len(itens), "ficam_fora": FORA, "imports_soltos_de_candidatas": soltos, "imports_soltos_sem_modulo_no_conjunto": faltam, "modulos": itens}
print("modulos:", len(itens), "| declaracoes:", sum(i["declaracoes_theorem_lemma"] for i in itens), "| imports soltos:", soltos, "| sem modulo no conjunto:", faltam,
      "| sorry fora de comentario:", sum(i["sorry"] for i in itens))
for it in itens:
    print(" ", it["modulo"].ljust(28), it["de_quem"].ljust(9), it["sha256"][:16], str(it["bytes"]).rjust(7), "B |", it["declaracoes_theorem_lemma"], "decl | importa", it["imports_de_candidatas"])
if "--executar" not in sys.argv:
    print("ENSAIO A SECO: nada gravado."); sys.exit(0)
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    alvo = DEST / (it["modulo"] + ".lean"); b = Path(it["origem"]).read_bytes()
    if alvo.exists():
        assert alvo.read_bytes() == b, "copia existente difere da origem: " + alvo.name
    else:
        alvo.write_bytes(b); assert alvo.stat().st_size == len(b)
out = V / "insumos" / "MANIFESTO_PEDRAS_v412.json"
tmp = out.with_suffix(".json.tmp_c1"); tmp.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
if out.exists():
    out.replace(out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")))
tmp.replace(out)
print("gravado:", out, "| sha16", hashlib.sha256(out.read_bytes()).hexdigest()[:16])
