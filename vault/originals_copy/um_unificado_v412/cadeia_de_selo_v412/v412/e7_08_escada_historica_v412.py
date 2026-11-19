"""R7 (D224, ponto 1 e a excecao dita no R7): registra a ESCADA HISTORICA do contrato do teste H0DN herdado (o literal sob baseline, na v411 selada) e o seu hash historico, ao lado da escada esperada desta versao
(lida do kernel medido) e da regra do patch. So' leitura: le o um.py da base (base_v411) por ast, sem executa-lo; le o literal do candidato quando existe. Grava ESCADA_HISTORICA_v412.json."""
import ast, hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
base = (D / "base_v411" / "um.py").read_bytes().decode("utf-8")
tree = ast.parse(base)
alvo = None
for no in tree.body:
    if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_V411_H0DN_CONTRACT" for t in no.targets):
        alvo = no
assert alvo is not None, "_V411_H0DN_CONTRACT nao achado na base"
contrato = ast.literal_eval(alvo.value)
bl = contrato.get("baseline")
assert isinstance(bl, dict), ("baseline nao e' dict", type(bl))
hashes = {k: v for k, v in bl.items() if isinstance(v, str) and re.fullmatch(r"[0-9a-f]{16,64}", v)}
fl = L.ler_json(D / "kernel" / "FLAGS_v412.json")
cand_p = D / "um_v412_candidato.py"
no_cand = None
if cand_p.exists():
    ct = cand_p.read_bytes().decode("utf-8")
    ca = ast.parse(ct)
    for no in ca.body:
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_V411_H0DN_CONTRACT" for t in no.targets):
            no_cand = ast.literal_eval(no.value).get("baseline")
rec = {"quando": L.agora(), "base_v411_sha16": hashlib.sha256(base.encode("utf-8")).hexdigest()[:16],
       "baseline_do_contrato_herdado": bl, "chaves_de_hash_do_baseline": hashes, "sha256_do_baseline_serializado": hashlib.sha256(json.dumps(bl, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
       "escada_historica_literal": bl.get("escada"), "versao_do_baseline": bl.get("version"), "escada_esperada_nesta_versao": fl["escada"][1], "escada_da_v411": fl["escada"][0],
       "regra_do_patch": "o patch C12b_h0dn_baseline_escada troca so' o literal 'escada' dentro de _V411_H0DN_CONTRACT: o registro herdado compara a escada do rito com a do contrato; os literais 'expected_ladder' (patch C12) acompanham; a escada historica e o seu hash ficam aqui como referencia",
       "baseline_no_candidato": no_cand, "n_chaves_baseline": len(bl)}
L.salvar_json(D / "ESCADA_HISTORICA_v412.json", rec)
print("baseline:", {k: (v if not isinstance(v, (dict, list)) else "...") for k, v in bl.items()}, "| hashes:", hashes, "| esperada", fl["escada"][1])
