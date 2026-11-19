# -*- coding: utf-8 -*-
"""_bump_copia_v412.py -- COPIA + SUBIDA DE ROTULO (nao e' o motor de regras) dos scripts da cadeia v411 para cadeia_de_selo\\v412 (claude-construtor-v412, a servico da gerencia c1, 17/11/2026; Etapa 1, item 4).
Receita (molde: v411\\_bump_copia_v411.py): copiar o molde de cadeia_de_selo\\v411 (SO' LEITURA; as versoes FINAIS da v411, as que rodaram no rito selado 1203b1f9202020d6) e subir SO' os rotulos de versao:
410 -> 411 e 411 -> 412 (uma passada, simultanea), k411c -> k412c, base_v410 -> base_v411, B19 -> B20 e B20 -> B21 (so' como palavra solta), B19-v410-AAAAMMDD-R1 -> o deployment que a Bancada de producao pina
HOJE (LIDO de C:\\IALD\\Bancada_Um\\canonical_contracts.json: a v411 aplicada, B20), vb22 -> vb23. Os nomes nascidos no um.py v411 (identificadores com 410/411 que existem no texto da base) NAO sobem: usa-se a
funcao bump() do derivar_v412_motor.py (gerado por _mk_motor_v412.py a partir do da v411).
NAO muda logica, narrativa nem listas: cada arquivo ganha um comentario de UMA linha `# [A ADAPTAR v412] ...` (o p00 recusa arquivo com essa marca; ela sai quando o arquivo for adaptado de verdade).
A v411 NAO tinha modulo novo: o corpo copiado traz o caminho SEM pedra nova (contrato R3_6, [0,0], recibo complementado); o que depende de bundle NAO vazio se adapta pelo molde da v410 (e da v409) na Etapa 2.
Para guiar isso, o resultado lista, por arquivo, as linhas do MOLDE v411 que falam do caso sem modulo novo (expressoes da lista RX_SEM_PEDRA), sem tocar nelas.
FICAM FORA (autorais da v412 ou proprias da v411, nao sobem do molde): delta, registros (inclusive os do H0DN), runtime, guarda_frases, gerar_candidato, copiar_base, copiar_insumos, copiar_k412c, construir_kernel,
pos_build_kernel, conferir_fontes, o preparo do bundle (todos escritos na Etapa 1 a partir do molde da v410), copiar_logs_do_kernel (o da v411 e' o do caso sem modulo novo: o da v412 e' adaptado do da v410),
complementar_recibo_kernel e repinar_bn (o conserto R3_6 da v411, so' para versao sem pedra), base_um_v410, gerar_pronto_para_gerar, os depositos de etapa da v411, os artigos e os _adapt/_fix/_r* (historico).
Para cada arquivo: bump/<nome>.diff, verificacao INDEPENDENTE de que toda linha alterada difere do molde so' em rotulos, ast.parse / sh -n. NUNCA executa os scripts copiados. Nao sobrescreve nada existente sem
backup de bytes (.bak_<ts>). Uso: C:\\Python314\\python.exe -B -X utf8 _bump_copia_v412.py [--seco] [--so ARQ ...]"""
import ast, datetime, difflib, hashlib, importlib.util, json, os, re, subprocess, sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)
V11 = os.path.join(CH, "v411")
BUMPDIR = os.path.join(HERE, "bump")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
_spec = importlib.util.spec_from_file_location("derivar_v412_motor", os.path.join(HERE, "derivar_v412_motor.py"))
MOTOR = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(MOTOR)

RAIZ = ["acom_conferencias_v411.py", "acom_inscrever_prep_v411.py", "carimbar_stdout_v411.py", "comparar_v410_v411.py", "conferir_citacoes_v411.py", "conferir_instalar_rito_v411.py", "conferir_rito_v411.py",
        "diff_e_pinos_v411.py", "ensaio_a_seco_v411.py", "exame_pontos_v411.py", "fechar_preparacao_v411.py", "fim_de_cadeia_v411.sh", "gerar_esperados_v411.py", "gerar_relatorio_v411.py",
        "guarda_ordem_de_chamada_v411.py", "guarda_p18_v411.py", "guardas_estaticas_bancada_v411.py", "instalar_v411.py", "p00_precondicoes_v411.py", "pino_memoria_py_v411.py", "purga_v411.py", "refazer_arvore_v411_pos_selo.py",
        "refazer_candidato_v411.sh", "refazer_sandbox_v411_pos_selo.sh", "regerar_v411.sh", "regras_v411.py", "reverter_v411.py", "rito_v411.sh", "simular_arvore_do_nos_v411.py", "teste_conferidor_positivo_v411.py",
        "varredura_fock_omega_v411.py", "depositar_construtor_v411.py", "kernel/refazer_audit_v411.sh", "cadeia_parte2_v411.sh", "gerar_pronto_para_candidato_v411.py",
        # nascidos na v411 e da cadeia (genericos; o corpo e' o da v411): a cadeia unica, as guardas da conversa (D181) e do material privado (D133), o modulo do conferidor, o pronto do pos-rito,
        # e os dois do topo com o resultado (o texto do topo da v412 e' da Etapa 2: sobem so' para que os imports dos outros nao fiquem orfaos)
        "cadeia_v411.sh", "guarda_conversa_v411.py", "guarda_material_privado_v411.py", "conferir_conversa_v411.py", "gerar_pronto_para_o_pos_rito_v411.py", "topo_com_resultado_v411.py", "quadro_v411.py"]
POS_RITO = ["b3_recibo_v411.py", "chain_pos_rito_v411.sh", "fechar_v411.py", "fila_memoria_v411.py", "gerar_derivacao_pos_rito_v411.py", "gerar_x_custodia_v411.py", "harness_fechar_sandbox_v411.py",
            "harness_textos_ensaio_v411.py", "leitura_v411.py", "montar_textos_v411.py", "registrar_mapa_v411.py", "superficies_v411.py", "textos_v411.py", "textos_v411.semente", "textos_v411_novo.pysnip",
            "textos_custodia_handoff_v411.py", "teste_gatilho_custodia_sem_candidato_v411.py", "teste_mapa_sem_candidato_v411.py", "teste_textos_custodia_sem_candidato_v411.py", "teste_x_custodia_sem_candidato_v411.py",
            # nascidos na v411 no pos-rito (importados pelos de cima)
            "blocos_custodia_v411.py", "consts_mapa_x_v411.py", "gerar_pronto_pos_rito_v411.py", "teste_blocos_custodia_v411.py", "teste_textos_sem_candidato_v411.py"]
ORQ = ["pos_treino_v411.py"]
PRE_SELO = ["conferir_recibo_pre_selo_v411.py", "derivar_pre_selo_v411.py", "gerar_pino_recibo_pre_selo_v411.py", "limpar_sandbox_vb22.py", "rodar_bn_pre_selo_v411.sh", "rodar_ensaio_1_pre_selo_v411.sh", "snap_producao_v411.py"]
SERVICO = ["conferir_exigencias_servico_v411.py", "evento_c1_b3_v411.py", "recibo_parada_v411.py", "recibo_religamento_v411.py", "controle_negativo/mutar_conferidor_v411.py"]
MOLDES = list(RAIZ) + ["pos_rito/" + x for x in POS_RITO] + ["orquestrador/" + x for x in ORQ] + ["bateria_pre_selo/" + x for x in PRE_SELO] + ["bancada_B3_servico/" + x for x in SERVICO]
COPIA_LITERAL = ["quadro_v397.py", "runtime_quadro_v397.py"]       # v397: nao sobem (o quadro do Teste da Unica Palavra segue intocado)
RENOMEIA = {"limpar_sandbox_vb22.py": "limpar_sandbox_vb23.py"}
RX_N = re.compile(r"(?<![0-9])(410|411)(?![0-9])")
MAPA_N = {"410": "411", "411": "412"}
RX_B = re.compile(r"(?<![0-9A-Za-z_])B(19|20)(?![0-9A-Za-z_])")
_BANC = json.load(open(r"C:\IALD\Bancada_Um\canonical_contracts.json", encoding="utf-8"))
DEP_NOVO = str(_BANC["deployment_id"]); assert re.match(r"B20-v411-\d{8}-R1$", DEP_NOVO), DEP_NOVO
DEP_VELHO_RX = re.compile(r"B19-v410-\d{8}-R1")
# as expressoes do caso SEM modulo novo (a v411): so' LISTADAS no resultado, para a adaptacao da Etapa 2 (molde v410/v409); nada e' trocado
RX_SEM_PEDRA = re.compile(r"sem modulo novo|SEM modulo novo|SEM_PEDRA|sem_pedra|R3_6|R3\.6|nenhum modulo novo|NAO tem modulo novo|nao tem modulo novo|bundle\W+vazio|pedras vazias|\[0, ?0\]|byte a byte|"
                          r"sem pedra|nenhuma bandeira nova|n_flags\W*==\W*0|nenhum modulo compilado|nada a compilar", re.I)


def nome_destino(rel):
    d = RX_N.sub(lambda m: MAPA_N[m.group(1)], rel)
    base = d.split("/")[-1]
    if base in RENOMEIA:
        d = "/".join(d.split("/")[:-1] + [RENOMEIA[base]])
    return d


def norm(s):
    s = re.sub(r"B(?:19|20|21)-v(?:410|411|412)-\d{8}-R1", "@DEP", s)
    s = re.sub(r"(?<![0-9])(?:410|411|412)(?![0-9])", "@N", s)
    s = re.sub(r"(?<![0-9A-Za-z_])B(?:19|20|21)(?![0-9A-Za-z_])", "@B", s)
    return re.sub(r"vb2[23]", "vb@", s)


def _modulos_da_cadeia():
    out = set()
    for sub in ("", "pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico"):
        d = os.path.join(V11, sub)
        if os.path.isdir(d):
            out |= {f[:-3] for f in os.listdir(d) if f.endswith(".py")}
    return out


_MODS = _modulos_da_cadeia()
RX_IMPORT = re.compile(r"^[ \t]*(?:import[ \t]+(?P<imp>[^#\n]+)|from[ \t]+(?P<frm>[A-Za-z0-9_]+)[ \t]+import(?![A-Za-z0-9_]))", re.M)


def consertar_imports(t, novo):
    ln = novo.split("\n")
    n = 0
    for m in RX_IMPORT.finditer(t):
        i = t.count("\n", 0, m.start())
        mods = [m.group("frm")] if m.group("frm") else [x.strip().split()[0] for x in m.group("imp").split(",") if x.strip()]
        for md in mods:
            if RX_N.search(md) and md in _MODS and md in ln[i]:
                novo_md = RX_N.sub(lambda mm: MAPA_N[mm.group(1)], md)
                ln[i] = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(md) + r"(?![A-Za-z0-9_])", novo_md, ln[i], count=1); n += 1
    return "\n".join(ln), n


def subir(t):
    c = {}
    novo = MOTOR.bump(t, (), "v411")
    novo, c["imports_consertados"] = consertar_imports(t, novo)
    c["deployment_antes"] = len(DEP_VELHO_RX.findall(t))
    novo = RX_B.sub(lambda m: "B" + str(int(m.group(1)) + 1), novo)
    novo, c["deployment_trocado"] = re.subn(r"B20-v411-\d{8}-R1", DEP_NOVO, novo)
    novo = novo.replace("vb22", "vb23")
    # as MARCAS HISTORICAS de cabecalho ("# [ADAPTADO v411, ...]", "# [AUTORAL v411, ...]") sao registro de quem adaptou e quando: NAO sobem
    lo_, ln_ = t.split("\n"), novo.split("\n")
    c["marcas_historicas_preservadas"] = 0
    for i_, l_ in enumerate(lo_):
        if re.match(r"^#\s*\[(?:ADAPTADO|AUTORAL|ADAPTADA)\s+v4\d\d\b", l_) and ln_[i_] != l_:
            ln_[i_] = l_; c["marcas_historicas_preservadas"] += 1
    return "\n".join(ln_), c


def cabecalho(dest_rel, molde_rel):
    return ("# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/%s; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): "
            "o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/%s.diff") % (molde_rel, dest_rel.replace("/", "__"))


def insere_cabecalho(texto, linha):
    ls = texto.split("\n"); i = 0
    if ls and ls[0].startswith("#!"):
        i = 1
    if i < len(ls) and re.match(r"#.*coding[:=]", ls[i]):
        i += 1
    ends_cr = "\r" if (len(ls) > i and ls[i].endswith("\r")) or (len(ls) > 0 and ls[0].endswith("\r")) else ""
    ls.insert(i, linha + ends_cr)
    return "\n".join(ls), i


def grava(dst, novo_b):
    if os.path.exists(dst):
        atual = open(dst, "rb").read()
        if atual == novo_b:
            return "igual"
        open(dst + ".bak_" + TS, "wb").write(atual); estado = "regravado_com_backup"
    else:
        estado = "gravado"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst + ".tmp", "wb").write(novo_b); assert os.path.getsize(dst + ".tmp") == len(novo_b); os.replace(dst + ".tmp", dst)
    return estado


def main():
    so = sys.argv[sys.argv.index("--so") + 1:] if "--so" in sys.argv else None
    res = {}
    os.makedirs(BUMPDIR, exist_ok=True)
    for rel in MOLDES + COPIA_LITERAL:
        if so and rel not in so and os.path.basename(rel) not in so:
            continue
        ps = os.path.join(V11, *rel.split("/"))
        if not os.path.exists(ps):
            res[rel] = {"erro": "molde ausente em v411"}; continue
        raw = open(ps, "rb").read(); t = raw.decode("utf-8")
        if rel in COPIA_LITERAL:
            dest_rel, novo, c = rel, t, {}
        else:
            dest_rel = nome_destino(rel)
            novo, c = subir(t)
            lo, ln = t.split("\n"), novo.split("\n")
            assert len(lo) == len(ln), ("numero de linhas mudou", rel)
            ruins = [i + 1 for i, (a, b) in enumerate(zip(lo, ln)) if a != b and norm(a) != norm(b)]
            assert not ruins, ("linha alterada alem de rotulos", rel, ruins[:5], [(lo[i - 1][:120], ln[i - 1][:120]) for i in ruins[:2]])
            if dest_rel.endswith((".py", ".sh", ".pysnip", ".semente")):
                novo, _ = insere_cabecalho(novo, cabecalho(dest_rel, rel))
            if dest_rel.endswith(".py"):
                ast.parse(novo)
            elif dest_rel.endswith(".sh"):
                r = subprocess.run(["sh", "-n"], input=novo.encode("utf-8"), capture_output=True)
                assert r.returncode == 0, (dest_rel, r.stderr[:200])
        pd = os.path.join(HERE, *dest_rel.split("/"))
        novo_b = novo.encode("utf-8")
        estado = "seco" if SECO else grava(pd, novo_b)
        d = "".join(difflib.unified_diff(t.splitlines(True), novo.splitlines(True), fromfile="v411/" + rel, tofile="v412/" + dest_rel, n=0))
        if not SECO and dest_rel != rel:
            open(os.path.join(BUMPDIR, dest_rel.replace("/", "__") + ".diff"), "w", encoding="utf-8", newline="").write(d)
        sem_pedra = [[i + 1, l.strip()[:180]] for i, l in enumerate(t.split("\n")) if RX_SEM_PEDRA.search(l)]
        res[rel] = {"destino": dest_rel, "estado": estado, "molde_sha16": sha16(raw), "destino_sha16": sha16(novo_b),
                    "linhas_alteradas": sum(1 for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")), **c,
                    "linhas_do_molde_sobre_o_caso_sem_modulo_novo": {"n": len(sem_pedra), "primeiras": sem_pedra[:8]}}
    if not SECO and not so:
        p = os.path.join(HERE, "BUMP_v412_RESULTADO.json")
        out = {"gerado": TS, "molde": "v411 (versoes finais, rito selado 1203b1f9202020d6)", "deployment_da_producao_lido": DEP_NOVO, "rotulo_do_B_n_da_v412": "B21",
               "motor": {"arquivo": "derivar_v412_motor.py", "sha16": sha16(open(os.path.join(HERE, "derivar_v412_motor.py"), "rb").read())},
               "n_arquivos": len(res), "arquivos": res}
        open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
    print(json.dumps({k: (v.get("estado"), v.get("linhas_alteradas"), (v.get("linhas_do_molde_sobre_o_caso_sem_modulo_novo") or {}).get("n")) for k, v in res.items()}, ensure_ascii=False)[:6000])
    erros = {k: v for k, v in res.items() if "erro" in v}
    print("ERROS:", erros); print("N:", len(res))
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
