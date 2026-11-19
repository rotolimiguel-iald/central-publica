"""R5: antes de regravar qualquer recibo ou o candidato, COPIA por bytes (nada e' movido nem apagado) os artefatos da Etapa 2 fechada pelo contrato R4 para FORA de work\\:
C:\\t\\k412c\\guarda_R4_etapa2_<data>\\ (o candidato 8b9a02e51650b11c, o manifesto dele, o mapa formal, o runtime, os recibos das ancoras, dos registros, da guarda, do texto publico, do ensaio, do portao do pilar e os dois fechos).
Confere cada copia por sha256 e grava GUARDA_R4_ETAPA2_v412.json (na pasta da cadeia e na guarda), com o caminho, os bytes e o sha16 de cada uma."""
import datetime, hashlib, json, os, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L
D = L.D
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ja = sorted(Path(r"C:\t\k412c").glob("guarda_R4_etapa2_*"))
G = ja[-1] if ja else Path(r"C:\t\k412c") / ("guarda_R4_etapa2_" + TS)
NOMES = ["um_v412_candidato.py", "CANDIDATO_v412.json", "FORMAL_MAP_v412.json", "v412_pins.py", "ANCORAS_ESCOLHIDAS_v412.json", "BLOCOS_TEXTO_PUBLICO_v412.json", "TEXTO_PUBLICO_v412.json", "TEXTO_PUBLICO_PDFLATEX_v412.json",
         "GUARDA_FRASES_v412.json", "GUARDA_v412_UNIDADES.json", "GUARDA_MATERIAL_PRIVADO_v412.json", "REGISTROS_v412_RECIBO.json", "VERBATIM_CONGELADO_v412.json", "PORTAO_DO_PILAR_CANDIDATO_v412.json", "ENSAIO_RESULTADO_v412.json",
         "ENSAIO_SAIDA_v412.txt", "ensaio_a_seco_v412.json", "TITULOS_DOS_CABECALHOS_v412.json", "TOPO_RATIFICADO_v412_DERIVADO.json", "EXAME_PONTOS_8b9a02e51650b11c.json", "SIMULACAO_ARVORE_NOS_8b9a02e51650b11c.json",
         "GUARDAS_ESTATICAS_BANCADA_v412.json", "GUARDA_ORDEM_DE_CHAMADA_v412.json", "conferir_citacoes_v412.json", "PREPARACAO_v412_PRONTA.json", "PRONTO_PARA_CANDIDATO_v412_R4.json", "ETAPA_2_ESTADO_v412.json",
         "ENSAIO_ADAPTACAO_ESTADO_v412.json", "GUARDA_CONVERSA_BASE_v411.json", "DERIVACAO_C4_v412.json", "O_QUE_FICA_CLARO_v412_R13_EN.md"]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
G.mkdir(parents=True, exist_ok=True)
rec = []; faltam = []; ja_iguais = 0; diverge = []
for n in NOMES:
    p = D / n
    if not p.exists():
        faltam.append(n); continue
    d = G / n
    h = sha(p)
    if d.exists():
        if sha(d) == h:
            ja_iguais += 1
        else:
            diverge.append(n)     # (o original ja' mudou depois da guarda: a guarda NAO e' sobrescrita)
        rec.append({"arquivo": n, "guarda": str(d), "bytes": d.stat().st_size, "sha16": sha(d)[:16], "sha256": sha(d)}); continue
    tmp = Path(str(d) + ".tmp")
    shutil.copyfile(p, tmp); assert tmp.stat().st_size == p.stat().st_size
    os.replace(tmp, d); assert sha(d) == h
    rec.append({"arquivo": n, "guarda": str(d), "bytes": d.stat().st_size, "sha16": h[:16], "sha256": h})
cand = next((r for r in rec if r["arquivo"] == "um_v412_candidato.py"), None)
out = {"quando": TS, "guarda": str(G), "n": len(rec), "bytes": sum(r["bytes"] for r in rec), "faltavam_na_pasta": faltam, "ja_estavam_iguais": ja_iguais, "original_mudou_depois_da_guarda": diverge,
       "candidato_R4": cand, "copias": rec, "nota": "copia de bytes, conferida por sha256; nada movido nem apagado; a guarda fica fora de work\\"}
L.salvar_json(D / "GUARDA_R4_ETAPA2_v412.json", out)
(G / "GUARDA_R4_ETAPA2_v412.json").write_bytes((D / "GUARDA_R4_ETAPA2_v412.json").read_bytes())
print("guarda:", G, "| copias:", len(rec), "| bytes:", out["bytes"], "| faltavam:", faltam, "| candidato R4:", cand and cand["sha16"], "| divergem:", diverge)
sys.exit(0 if cand and cand["sha16"] == "8b9a02e51650b11c" or (cand and diverge) else 1)
