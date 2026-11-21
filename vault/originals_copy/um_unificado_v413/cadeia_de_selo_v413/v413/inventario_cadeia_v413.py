# -*- coding: utf-8 -*-
"""inventario_cadeia_v413.py -- (claude-construtor-v413, 20/11/2026, a servico da gerencia c1) Etapa 1 da v413, item 4 (segunda metade): o INVENTARIO, SEM ADAPTAR, dos demais scripts da
cadeia da v412 que a v413 vai precisar (candidato, instalar, reverter, rito, conferidor, handoff). Para cada um: sha16 e tamanho do molde (pasta da v412, SO' LEITURA), as dependencias locais
(imports e nomes de script da cadeia citados no texto), o que no texto e' proprio da v412 e tera de mudar (rotulos v412/v411, k412c, base_v411, rodadas R5/R7/R11/R12/R25, os numeros medidos
da v412 que aparecem como literal, hashes pinados de 16+ hexadecimais, rotulos e deployments da Bancada) e a descricao do que muda na v413 (o_que_muda, escrita pelo construtor a partir da
leitura do cabecalho de cada script). O rotulo da Bancada e' MEDIDO do disco (C:\\IALD\\Bancada_Um\\canonical_contracts.json), nunca suposto. Nada e' executado nem adaptado; grava so'
INVENTARIO_CADEIA_v413.json. uso: C:\\Python314\\python.exe -B -X utf8 inventario_cadeia_v413.py [--cabecalhos]"""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V412 = os.path.join(os.path.dirname(HERE), "v412")
OUT = os.path.join(HERE, "INVENTARIO_CADEIA_v413.json")
sha = lambda b: hashlib.sha256(b).hexdigest()

# os scripts principais por papel (as versoes FINAIS da v412: o gerador vem de CANDIDATO_v412.json; o handoff, de RECIBO_HANDOFF_v412.json)
PAPEIS = {
    "candidato": ["gerar_candidato_v412_r7.py", "delta_v412_r7.py", "registros_v412_r7.py", "runtime_v412_codigo_r7.py", "textos_registros_v412_r7.py", "texto_publico_v412_r7.py",
                  "guarda_frases_v412_r7.py", "guarda_conversa_v412_r7.py", "guarda_material_privado_v412_r7.py", "guarda_ordem_de_chamada_v412_r7.py", "guardas_estaticas_bancada_v412_r7.py",
                  "verificar_historia_texto_v412_r7.py", "topo_com_resultado_v412_r7.py", "exame_pontos_v412_r7.py", "simular_arvore_do_nos_v412_r7.py", "ensaio_a_seco_v412_r7.py",
                  "gerar_esperados_v412.py", "gerar_preparacao_pronta_v412_r7.py", "portao_do_pilar_candidato_v412.py", "e7_lib_v412.py"],
    "instalar": ["instalar_v412.py", "conferir_instalar_rito_v412.py"],
    "reverter": ["reverter_v412.py"],
    "rito": ["rito_v412.sh", "carimbar_stdout_v412.py", "cadeia_v412.sh", "cadeia_parte2_v412.sh", "fim_de_cadeia_v412.sh", "refazer_candidato_v412.sh", "regerar_v412.sh"],
    "conferidor": ["conferir_rito_v412.py", "conferir_pos_rito_v412_foco.py", "esperados_v412_foco.py", "teste_conferidor_positivo_v412.py"],
    "handoff": ["montar_handoff_e_linhagem_v412.py", "pos_rito/textos_custodia_handoff_v412.py"],
}
_KC = ("NOVO na v413: um modulo ANTIGO muda de texto (kernel_corrigido: TGLExt.OResumoEPsiBit, so' a docstring); a v412 so' ACRESCENTAVA modulos")
O_QUE_MUDA = {   # descricoes do construtor (claude-construtor-v413), por leitura do cabecalho de cada molde; nada adaptado aqui
    "gerar_candidato_v412_r7.py": "base_v411 -> base_v412 (o um.py v412 selado); o kernel: os modulos novos de kernel_modulos_novos_v413.json embutidos em _EMBEDDED_KERNEL_FILES do sandbox k413c, a raiz regenerada, as bandeiras de kernel\\FLAGS_v413.json (ext_<modulo>_413_NNNN) e a escada lida do core da v412; " + _KC + ": o gerador precisa de um caminho para SUBSTITUIR o texto embutido de um arquivo que ja' existe (hoje so' acrescenta) e manter formal_files/ledger coerentes; UM_VERSION v413; registros, secao do artigo e resumo pelo contrato da v413 (gerencia); as ancoras de patch tem de ocorrer uma vez no um.py v412.",
    "delta_v412_r7.py": "importa o delta_v412 por caminho e sobrescreve o que a v413 muda; le BUNDLE_v413.json, kernel_modulos_novos_v413.json e kernel\\FLAGS_v413.json; precisa expor o kernel_corrigido (path e sha256 antes/depois) para o gerador, o ensaio e os conferidores; os registros e o artigo vem do contrato da v413.",
    "registros_v412_r7.py": "os registros por especificacao da v413 (quais e com que texto) sao do contrato da gerencia; o motor (_v392_registro) e a regra de ancora por nome seguem; caminhos e1_lib/pagina/manifesto passam aos da v413.",
    "runtime_v412_codigo_r7.py": "as funcoes novas da v413 que entram no programa (secao do artigo e rodada dos registros por especificacao), se o contrato da v413 as tiver; o nome _v412_* passa a _v413_*.",
    "textos_registros_v412_r7.py": "texto dos registros da v413, tirado da pagina publica da v413 e dos cabecalhos das pedras limpas (contrato da gerencia).",
    "texto_publico_v412_r7.py": "conversor da pagina publica da v413 para TeX; o corpo e' generico (rotulos).",
    "guarda_frases_v412_r7.py": "carrega a _v412_guarda_frases do um.py v412 selado (base_um_v412) e o codigo novo da v413; as obrigacoes novas sao do contrato da v413.",
    "guarda_conversa_v412_r7.py": "o mecanismo nao muda; a lista das falas e os pinos da base passam aos da v412 selada (GUARDA_CONVERSA_BASE_v412).",
    "guarda_material_privado_v412_r7.py": "so' rotulos e a pasta insumos da v413 (pedras limpas, kernel_edits, origem); a guarda da E03 da G1 e' a mesma.",
    "guarda_ordem_de_chamada_v412_r7.py": "depende de a v413 ter ou nao registro com funcao novo (contrato); se nao tiver, o da v412 segue como herdado (rotulos).",
    "guardas_estaticas_bancada_v412_r7.py": "so' as linhas unicas de ALPHA e UM_VERSION sao lidas; rotulos e o sandbox curto (vb2x); o pino do esboco do CANDIDATO_v413.json.",
    "verificar_historia_texto_v412_r7.py": "generico (rotulos); roda sobre os textos novos da v413.",
    "topo_com_resultado_v412_r7.py": "o topo ratificado/derivado da v413 (TOPO_RATIFICADO_v413_DERIVADO.json, da gerencia); rotulos.",
    "exame_pontos_v412_r7.py": "o ponto novo da v413 no main (se houver registro novo), os da v412 herdados; --flags kernel\\FLAGS_v413.json; --core0/--selo0 da v412 selada.",
    "simular_arvore_do_nos_v412_r7.py": "a arvore do Nos depois do rito = os embutidos do candidato da v413 (com o OResumoEPsiBit CORRIGIDO no lugar do da v412) + os residuais; recomputa formal_files; os registros da v413 depois dos da v412. " + _KC + ".",
    "ensaio_a_seco_v412_r7.py": "o kernel embutido == o sandbox k413c (inclusive o arquivo corrigido, que DIFERE do Nos); a escada da v412 -> a da v413; as bandeiras novas; os registros da v413; os herdados da v412 recriados iguais. " + _KC + ".",
    "gerar_esperados_v412.py": "NAO rodou na v412 (marca A ADAPTAR; substituido por esperados_v412_foco.py); o molde da v413 e' o esperados_v412_foco.py.",
    "gerar_preparacao_pronta_v412_r7.py": "o fecho do candidato da v413 (Etapa 2): os recibos da v413 (PRONTO_PARA_CANDIDATO_v413.json desta etapa, CANDIDATO_v413.json, ensaio, portoes).",
    "portao_do_pilar_candidato_v412.py": "base_v412\\um.py e PORTAO_DO_PILAR_v413.json; confere que o gerador nao tocou os textos do fecho da chave; acrescentar que a correcao de texto so' muda _EMBEDDED_KERNEL_FILES.",
    "e7_lib_v412.py": "os caminhos (contrato, manifesto, pagina, pedras, sandbox) passam aos da v413: CONTRATO da gerencia, insumos\\MANIFESTO_PEDRAS_v413.json, insumos\\pedras_limpas\\TGLExt, C:\\t\\k413c\\final.",
    "instalar_v412.py": "o Nos tem de ser a v412 selada; os modulos novos (kernel_modulos_novos_v413.json) nao podem estar no kernel do Nos; " + _KC + ": o instalador tem de conferir que tgl_kernel\\TGLExt\\OResumoEPsiBit.lean do Nos e' o da v412 (sha256_origem) e guardar BACKUP DE BYTES dele junto dos 10 de hoje (o rito o reescreve pelo texto embutido); o desvio do B(n) declarado na v412 e' para a gerencia decidir de novo.",
    "conferir_instalar_rito_v412.py": "NAO rodou na v412 (marca A ADAPTAR, molde da v411 sem modulo novo); para a v413 a condicao do modulo novo e' a de uma lista NAO vazia e mais o arquivo corrigido.",
    "reverter_v412.py": "restaura os backups gravados pelo instalador (o APLICADO_AO_CANONICO mais novo); " + _KC + ": precisa restaurar tambem tgl_kernel\\TGLExt\\OResumoEPsiBit.lean e conferir que voltou ao sha256_origem; os modulos novos vao a quarentena.",
    "rito_v412.sh": "o corpo e' generico; o cabecalho diz os numeros da v413 lidos de kernel\\construir_marcas.txt (modulos, tempo do build e do Audit) e o pacote v413; o pilar reaproveitado pela chave (ver PORTAO_DO_PILAR_v413.json).",
    "carimbar_stdout_v412.py": "generico (rotulos e o nome do stdout rodada_v413_stdout.txt).",
    "cadeia_v412.sh": "NAO rodou na v412 (A ADAPTAR; a Etapa 3 foi a enxuta); decisao da gerencia se a v413 volta a cadeia unica ou repete a enxuta.",
    "cadeia_parte2_v412.sh": "remissao a cadeia_v412.sh; mesma decisao.",
    "fim_de_cadeia_v412.sh": "NAO rodou na v412 (fim_de_cadeia_v412.sh.NAO_RODAR.md); B(n) pre-selo, servico estatico, harnesses do pos-rito: decisao da gerencia (a rota bancada.b21_v412 diz: no B(n) da v413, o salto v411->v413).",
    "refazer_candidato_v412.sh": "A ADAPTAR na v412; chama a cadeia_v412.sh; mesma decisao.",
    "regerar_v412.sh": "A ADAPTAR na v412 (texto de versao sem modulo novo); na v413 o comando do kernel e' reconstruir_kernel_v413.py.",
    "conferir_rito_v412.py": "NAO rodou na v412 (A ADAPTAR; substituido por conferir_pos_rito_v412_foco.py).",
    "conferir_pos_rito_v412_foco.py": "o conferidor enxuto da v412 (o que rodou): base v412 selada (backups do instalador), os modulos novos e as bandeiras da v413, os registros da v413 pelo contrato; " + _KC + ": conferir que tgl_kernel\\TGLExt\\OResumoEPsiBit.lean do Nos ficou com o sha256_saida e que as declaracoes dele seguem as mesmas.",
    "esperados_v412_foco.py": "os ESPERADOS da v413 lidos dos artefatos (CANDIDATO_v413.json, PRONTO_PARA_CANDIDATO_v413.json, kernel_modulos_novos_v413.json, o manifesto da v413, o sandbox k413c, o Nos v412, o contrato da v413, o portao do pilar); acrescentar o kernel_corrigido.",
    "teste_conferidor_positivo_v412.py": "A ADAPTAR na v412 (nao rodou); depende do conferidor escolhido para a v413.",
    "montar_handoff_e_linhagem_v412.py": "R2 da gerencia na v412: o bloco v413 SELADA da linhagem e o HANDOFF_v413_CUSTODIA.md com os marcadores _v413, a partir da pagina da v413 aprovada e dos textos ratificados (verbatim); confere com os parsers da G1; e' ato da gerencia.",
    "pos_rito/textos_custodia_handoff_v412.py": "A ADAPTAR na v412 (o S6d do orquestrador); se a v413 usar o orquestrador, adaptar ao handoff da v413.",
}
RX_TOK = {"v412": r"(?<![0-9A-Za-z])v412(?![0-9])", "v411": r"(?<![0-9A-Za-z])v411(?![0-9])", "k412c": r"k412c", "base_v411": r"base_v411",
          "rodadas_R5_R7_R11_R12_R25": r"(?<![A-Za-z0-9])(?:R5|R7|R11|R12|R25|r5|r7|c4)(?![0-9A-Za-z])", "decima_segunda_lista": r"(?i)decima segunda lista|DUODECIMA",
          "Bancada_B2x": r"(?<![0-9A-Za-z_])B2[0-2](?![0-9A-Za-z_])", "deployment_B2x": r"B2[0-2]-v41[0-3]-\d{8}-R\d"}
NUMEROS_V412 = {}   # os numeros MEDIDOS da v412 (lidos dos recibos, nunca digitados) que um script pode trazer como literal


def numeros_medidos():
    out = {}
    try:
        pos = json.load(open(os.path.join(V412, "kernel", "POS_BUILD_v412.json"), encoding="utf-8"))
        out["n_modulos_novos_v412"] = len(pos.get("por_modulo_marcas") or {})
        out["n_bandeiras_novas_v412"] = pos.get("n_flags")
        out["escada_v412"] = pos.get("escada")
        out["decl_v412"] = (pos.get("linha_TOTAL") or {}).get("decl")
        out["thm_v412"] = (pos.get("linha_TOTAL") or {}).get("thm")
    except Exception as e_:
        out["erro"] = repr(e_)
    return out


def deps_locais(t, todos):
    ims = set(re.findall(r"(?m)^\s*(?:import|from)\s+([A-Za-z0-9_]+)", t))
    cit = set(re.findall(r"([A-Za-z0-9_]+_v41[0-2](?:_[A-Za-z0-9]+)?\.(?:py|sh))", t))
    return sorted((ims & todos) | {c[:-3] for c in cit if c[:-3] in todos or c in todos})


def main():
    todos = set()
    for dp, dn, fn in os.walk(V412):
        dn[:] = [d for d in dn if not d.startswith(("contrato_REV", "o_que_fica_claro_REV", "__pycache__"))]
        for f in fn:
            if f.endswith((".py", ".sh")) and ".bak" not in f:
                todos.add(f[:-3])
    NUMEROS_V412.update(numeros_medidos())
    banc = json.load(open(r"C:\IALD\Bancada_Um\canonical_contracts.json", encoding="utf-8"))
    dep_prod = str(banc.get("deployment_id"))
    m_ = re.match(r"B(\d+)-v(\d+)-", dep_prod)
    rep = {"contrato": "INVENTARIO_CADEIA_v413", "gerado": datetime.datetime.now().isoformat(timespec="seconds"), "molde": V412,
           "bancada_medida": {"arquivo": r"C:\IALD\Bancada_Um\canonical_contracts.json", "deployment_id_em_producao": dep_prod,
                              "rotulo_em_producao": ("B" + m_.group(1)) if m_ else None, "versao_em_producao": ("v" + m_.group(2)) if m_ else None,
                              "nota": "a producao ainda pina o deployment lido aqui; o rotulo do B(n) da v413 (o salto desde a versao em producao) e' decisao da Etapa 2/gerencia, conferida no disco na hora"},
           "numeros_medidos_v412": NUMEROS_V412, "papeis": {}}
    cab = "--cabecalhos" in sys.argv
    for papel, lista in PAPEIS.items():
        rep["papeis"][papel] = {}
        for rel in lista:
            p = os.path.join(V412, *rel.split("/"))
            if not os.path.exists(p):
                rep["papeis"][papel][rel] = {"ausente": True}; continue
            b = open(p, "rb").read(); t = b.decode("utf-8", "replace")
            toks = {k: len(re.findall(rx, t)) for k, rx in RX_TOK.items()}
            hexs = sorted(set(re.findall(r"(?<![0-9a-f])[0-9a-f]{16}(?:[0-9a-f]{48})?(?![0-9a-f])", t)))
            nums = {k: len(re.findall(r"(?<![0-9])%d(?![0-9])" % v, t)) for k, v in NUMEROS_V412.items() if isinstance(v, int) and v > 99}
            linhas = t.split("\n")
            ent = {"sha16": sha(b)[:16], "bytes": len(b), "linhas": len(linhas), "dependencias_locais": deps_locais(t, todos), "tokens_proprios_da_v412": toks,
                   "hashes_pinados_16hex": {"n": len(hexs), "primeiros": hexs[:8]}, "numeros_medidos_da_v412_como_literal": {k: v for k, v in nums.items() if v},
                   "o_que_muda": O_QUE_MUDA.get(rel, "(a descrever)")}
            rep["papeis"][papel][rel] = ent
            if cab:
                print("=" * 20, papel, rel, ent["sha16"], ent["bytes"])
                print("\n".join(l[:230] for l in linhas[:14]))
    if not cab:
        tmp = OUT + ".tmp"
        bb = json.dumps(rep, ensure_ascii=False, indent=1).encode("utf-8")
        if os.path.exists(OUT):
            bk = OUT + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(open(OUT, "rb").read())
        open(tmp, "wb").write(bb); assert os.path.getsize(tmp) == len(bb); os.replace(tmp, OUT)
        print("INVENTARIO:", OUT, "| papeis:", {k: len(v) for k, v in rep["papeis"].items()}, "| bancada em producao:", dep_prod,
              "| sem descricao:", [r for v in rep["papeis"].values() for r, e in v.items() if e.get("o_que_muda") == "(a descrever)"])


if __name__ == "__main__":
    main()
