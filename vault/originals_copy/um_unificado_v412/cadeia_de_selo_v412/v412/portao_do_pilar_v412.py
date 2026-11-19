# -*- coding: utf-8 -*-
"""portao_do_pilar_v412.py -- (claude-construtor-v412, 17/11/2026) Etapa 1, item 5: o PORTAO DO PILAR por LEITURA DE CODIGO (nada roda; nada importa torch; nada toca a placa de video).
Le o um.py v411 SELADO (base_v411\\um.py, conferido por sha256 contra o selo do Nos) por ast e responde:
  (1) como o rito decide REAPROVEITAR o resultado do pilar quantico (quantum_pillar_start_v384): a chave (_qp_key) e as condicoes do reuso;
  (2) de que ENTRADAS a chave depende (os nomes de topo que a funcao da chave e as que a alimentam leem), e o sha256 do texto de cada uma no um.py selado;
  (3) se algo do que a v412 muda (modulos Lean novos -> _EMBEDDED_KERNEL_FILES e _LEAN_THEOREM_FLAGS; registros por especificacao; texto do artigo) entra nessas entradas: por fecho de dependencias
      sobre os nomes de topo (que funcao/constante cada uma le), procurando se _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS ou algum nome de registro/artigo aparece no fecho;
  (4) o estado do cache e do ultimo rito (so' LEITURA de arquivos: o stdout do rito da v411 no Nos e o result.json do cache, se existir).
Grava PORTAO_DO_PILAR_v412.json. uso: C:\\Python314\\python.exe -B -X utf8 portao_do_pilar_v412.py"""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
UM = os.path.join(HERE, "base_v411", "um.py")
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = open(UM, "rb").read(); src = raw.decode("utf-8")
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo["um_version"] == "v411" and selo["sha256"]["um.py"] == sha(raw), "a base nao e' o um.py da v411 selada"
tree = ast.parse(src)
top = {}
for n in tree.body:
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        top[n.name] = n
    elif isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name):
                top[tg.id] = n
    elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
        top[n.target.id] = n


def nomes_lidos(no):
    return sorted({x.id for x in ast.walk(no) if isinstance(x, ast.Name) and x.id in top and x.id != getattr(no, "name", None)})


def fecho(raizes, parar=()):
    vis = set(); fila = list(raizes)
    while fila:
        a = fila.pop()
        if a in vis or a not in top:
            continue
        vis.add(a)
        if a in parar:
            continue
        fila.extend(nomes_lidos(top[a]))
    return vis


# (1) a decisao: o texto da funcao que decide
dec = ast.get_source_segment(src, top["quantum_pillar_start_v384"])
# (2) as entradas da chave: o que _qp_key recebe na chamada dentro da decisao, e o fecho de cada uma
chamada = re.search(r"key = _qp_key\(([^\n]+)\)", dec).group(1)
ENTRADAS = {"worker_sha256": ["_qp_materialize", "_QP_WORKER_SRC", "_qp_dir"], "spec_canonica": ["_QP_SPEC_JSON", "_qp_canon", "_QP_SPEC_SHA256"], "beta_hex": ["_qp_beta"]}
fecho_chave = fecho(["_qp_key"] + sum(ENTRADAS.values(), []))
# o reuso: as condicoes lidas do texto
cond = {"interruptor": "_RITE_CKPT_ON or _QP_REUSE_V386" in dec, "_QP_REUSE_V386": ast.literal_eval(top["_QP_REUSE_V386"].value) if "_QP_REUSE_V386" in top else None,
        "cache_com_sha256_conferido": "_qp_cached_ok(cdir)" in dec, "ambiente_igual": all(k in dec for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu")),
        "veredito_do_cache": "TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__" in dec, "motor_roda_de_novo_no_ambiente_presente": "_qp_engine_now(mat)" in dec}
fecho_reuso = fecho(["quantum_pillar_start_v384"], parar=("run_um",))
# (3) o que a v412 muda entra no fecho da chave?
MUDA_V412 = ["_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS"]
reg_e_artigo = sorted(n for n in top if re.match(r"^(_v4\d\d_|registro|_registros|build_paper|_artigo|paper_|_paper)", n))
entra_chave = sorted(set(MUDA_V412) & fecho_chave)
entra_chave_reg = sorted(set(reg_e_artigo) & fecho_chave)
entra_reuso = sorted(set(MUDA_V412) & fecho_reuso)
# o trabalhador: o modo engine (o autoteste que o reuso roda de novo) usa a placa?
wsrc = ast.literal_eval(top["_QP_WORKER_SRC"].value)
i_eng = wsrc.find("def engine") if "def engine" in wsrc else wsrc.find('"engine"')
# (o corpo de engine_selftest nao fala de cuda: o DISPOSITIVO e' escolhido no main do trabalhador -- dev = torch.device("cuda") -- e o Engine(torch, dev, ...) do autoteste e' construido nele;
#  o modo engine devolve logo depois do autoteste)
_main = wsrc[wsrc.index("def main():"):]
_i_eng = _main.find('args.mode == "engine"')
engine_trecho_usa_cuda = bool('dev = torch.device("cuda")' in _main and "E = Engine(torch, dev" in _main and "engine_selftest(E" in _main and _i_eng > _main.find('dev = torch.device("cuda")') > 0)
# o sha256 do texto de cada entrada no um.py selado (o candidato da v412 tem de trazer os MESMOS textos para a chave nao mudar)
textos = {n: sha(ast.get_source_segment(src, top[n]).encode("utf-8")) for n in sorted(fecho_chave)}
# (4) o estado: o stdout do rito da v411 no Nos (leitura) e o cache
stdout = os.path.join(NOS, "rodada_v411_stdout.txt")
linhas_pilar = []
if os.path.exists(stdout):
    for ln in open(stdout, "rb").read().decode("utf-8", "replace").splitlines():
        if "pilar quantico" in ln:
            linhas_pilar.append(ln.strip()[:300])
chave_no_stdout = sorted(set(re.findall(r"chave ([0-9a-f]{24})", "\n".join(linhas_pilar))))
pq = json.load(open(os.path.join(NOS, "um_absoluto_pilar_quantico.json"), encoding="utf-8")) if os.path.exists(os.path.join(NOS, "um_absoluto_pilar_quantico.json")) else {}
cache_m = re.search(r'^CACHE\s*=\s*(.+)$', src, re.M)
rep = {"um_py": UM, "um_py_sha256": sha(raw), "selo_um_version": selo["um_version"],
       "decisao": {"funcao": "quantum_pillar_start_v384", "chamada_da_chave": "_qp_key(%s)" % chamada, "condicoes_do_reuso": cond,
                   "texto_da_funcao_da_chave": ast.get_source_segment(src, top["_qp_key"])},
       "entradas_da_chave": {"worker_sha256": "sha256 dos bytes de _QP_WORKER_SRC materializado em quantum_pillar\\pilar_quantico_worker.py ao lado do um.py",
                             "spec_canonica": "o JSON canonico (sort_keys, separadores compactos) de _QP_SPEC_JSON, conferido contra _QP_SPEC_SHA256",
                             "beta_hex": "float.hex de beta pelo motor do run_um: alpha_lagrange_form(validate_against_qed(0.0, SEALED_CODATA_ALPHA)['q_QED'])['beta_form'] (nunca literal)"},
       "fecho_dos_nomes_de_topo_da_chave": sorted(fecho_chave), "sha256_do_texto_de_cada_nome_no_um_py_selado": textos,
       "o_que_a_v412_muda": {"nomes": MUDA_V412 + ["registros por especificacao (texto do core)", "texto do artigo"],
                             "entra_no_fecho_da_chave": entra_chave, "nomes_de_registro_ou_artigo_no_fecho_da_chave": entra_chave_reg,
                             "entra_no_fecho_da_decisao_de_reuso": entra_reuso},
       "o_reuso_toca_a_placa_de_leve": {"sonda_do_ambiente": "_qp_env_probe importa torch e chama torch.cuda.is_available() e get_device_name(0) num subprocesso",
                                        "motor_de_novo": "_qp_engine_now roda o trabalhador em --mode engine (autoteste E1..E8) no ambiente presente antes de aceitar o reuso",
                                        "o_autoteste_do_motor_roda_na_placa": engine_trecho_usa_cuda,
                                        "nota": "no main do trabalhador o dispositivo e' cuda e o Engine do autoteste E1..E8 e' construido nele; o modo engine devolve logo depois do autoteste: e' curto, mas usa a placa"},
       "estado_lido": {"stdout_v411": stdout if os.path.exists(stdout) else None, "linhas_do_pilar_no_stdout_v411": linhas_pilar[:12], "chaves_no_stdout_v411": chave_no_stdout,
                       "pilar_json_do_nos": {k: pq.get(k) for k in ("verdict", "mode", "key", "cache_key", "status", "this_run") if k in pq}, "CACHE_no_um_py": cache_m.group(1).strip()[:200] if cache_m else None},
       "resposta": None}
rep["resposta"] = ("a chave depende so' de tres entradas: o sha256 do trabalhador embutido (_QP_WORKER_SRC), a especificacao canonica (_QP_SPEC_JSON) e beta em hexadecimal (do motor do run_um); "
                   "nenhuma delas le _EMBEDDED_KERNEL_FILES, _LEAN_THEOREM_FLAGS, registro ou artigo (fecho de dependencias por ast: %s); logo os modulos Lean novos, os registros por especificacao e o texto da v412 NAO "
                   "entram na chave, desde que o gerador do candidato nao toque os textos do fecho (sha256 de cada um no relatorio). O reuso ainda exige: _QP_REUSE_V386 verdadeiro, o result.json do cache com sha256 conferido, "
                   "o mesmo ambiente (torch, cuda, numpy, scipy, python, gpu) e o motor passando de novo; a sonda (torch.cuda) e o autoteste do motor (Engine no dispositivo cuda) usam a placa, curto, mesmo no reuso "
                   "(foi assim na v410 e na v411, com o treino junto). Se o ambiente da placa mudar (o treino da Nativa pode ter "
                   "trocado algo no mesmo Python), o reuso e' recusado e o rito CALCULA: esse e' o caso de parar e avisar o operador (D207).") % ("nada entra" if not (entra_chave or entra_chave_reg) else "ENTRA: %s %s" % (entra_chave, entra_chave_reg))
out = os.path.join(HERE, "PORTAO_DO_PILAR_v412.json")
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({k: rep[k] for k in ("decisao", "o_que_a_v412_muda", "o_reuso_toca_a_placa_de_leve")}, ensure_ascii=False, indent=1)[:3500])
print("fecho da chave:", sorted(fecho_chave))
print("estado:", json.dumps(rep["estado_lido"], ensure_ascii=False)[:1500])
