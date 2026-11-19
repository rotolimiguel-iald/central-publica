"""R7: deriva as copias `_r7` dos scripts do KERNEL a partir das `_r5` (decima lista, 153 modulos) para a DECIMA SEGUNDA lista (156 modulos; insumos\\MANIFESTO_PEDRAS_v412_R11.json, insumos\\pedras_r11).
Cada troca especifica tem contagem minima; o que sobra dos padroes de risco e' listado no log para a proxima troca."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_deriv_v412 as DV

ESTE = "e7_02_derivar_kernel_v412.py"
COM = [("contrato R5", "contrato R11", 0), ("pagina R18", "pagina R25", 0), ("DECIMA lista", "DECIMA SEGUNDA lista", 0), ("decima lista", "decima segunda lista", 0), ("DECIMA_LISTA_CONFERIDA_v412", "DUODECIMA_LISTA_CONFERIDA_v412", 0)]

# bloco novo da conferencia da lista: as tres fontes emendadas so' em comentario tem o mesmo codigo que as da decima lista
CHECK_COMENTARIO = '''
def _sem_comentarios(t):
    """tira os comentarios de linha (--) e os blocos /- ... -/ (aninhados; inclui /-- docstring e /-! cabecalho) e normaliza os espacos; o que sobra e' o codigo"""
    out = []; i = 0; n = len(t); prof = 0; instr = False
    while i < n:
        c = t[i]
        if prof == 0 and instr:
            out.append(c)
            if c == "\\\\" and i + 1 < n:
                out.append(t[i + 1]); i += 2; continue
            if c == '"':
                instr = False
            i += 1; continue
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof > 0:
            if t.startswith("-/", i):
                prof -= 1; i += 2; continue
            i += 1; continue
        if t.startswith("--", i):
            j = t.find("\\n", i)
            i = n if j < 0 else j; continue
        if c == '"':
            instr = True
        out.append(c); i += 1
    return " ".join("".join(out).split())


R10_ANT = HERE / "insumos" / ("pedras_" + "r10")
mud = list(M10.get("mudaram_da_decima_lista") or [])
dif_cod = [m for m in mud if _sem_comentarios((R10_ANT / (m + ".lean")).read_text(encoding="utf-8")) != _sem_comentarios((R10 / (m + ".lean")).read_text(encoding="utf-8"))]
dif_bytes = [m for m in mud if (R10_ANT / (m + ".lean")).read_bytes() != (R10 / (m + ".lean")).read_bytes()]
e.chk("as tres fontes que mudaram da decima lista (campo mudaram_da_decima_lista) mudaram so' em comentario: o codigo sem comentarios e' identico; os bytes diferem (a emenda existe)", mud == ["AClausulaExemplificativa", "AFitaEOIndice", "OPsiBitDaFormula"] and not dif_cod and sorted(dif_bytes) == sorted(mud), len(mud), {"codigo_diferente": dif_cod, "bytes_diferentes": dif_bytes})
resto_igual = [m for m in ent10 if m not in mud and m not in (M10.get("novas_em_relacao_a_decima_lista") or []) and (R10_ANT / (m + ".lean")).read_bytes() != (R10 / (m + ".lean")).read_bytes()]
e.chk("as outras 150 fontes sao identicas byte a byte as da decima lista; as tres novas (novas_em_relacao_a_decima_lista) nao existem na decima", not resto_igual and all(not (R10_ANT / (m + ".lean")).exists() for m in M10["novas_em_relacao_a_decima_lista"]) and len(M10["novas_em_relacao_a_decima_lista"]) == 3, len(ent10) - 3, resto_igual[:5])
'''

EXTRAS_PAGINA = '''        extras_pag = []
        for n_full in sorted(set(re.findall(RX_CR, pagina))):
            if "." in n_full:
                ja_ = {i_["nome_no_audit"] for i_ in publicas}
                for k_ in sorted(prov):
                    if prov[k_] == "TGLExt/%s.lean" % mod and (k_ == n_full or k_.endswith("." + n_full)) and k_ in flag_de and k_ not in ja_:
                        it_ = {"modulo": mod, "lista": "pagina", "classe": "publica", "nome_proposto": n_full, "nome_no_audit": k_, "via": "proveniencia", "no_trio": True, "bandeira_proposta": flag_de[k_]}
                        publicas.append(it_); its.append(it_); por_ultimo.setdefault(ultimo(k_), {})[k_] = it_; extras_pag.append(k_)
'''
DERIVACOES = [
    ("pre_colisao_declaracoes_v412_r5.py", "pre_colisao_declaracoes_v412_r7.py", COM + []),
    ("pos_build_kernel_v412_r5.py", "pos_build_kernel_v412_r7.py", COM + []),
    ("reconstruir_kernel_v412_r5.py", "reconstruir_kernel_v412_r7.py", COM + [("(r5, decima segunda lista)", "(r7, decima segunda lista)", 0), ('"RECONSTRUCAO DO KERNEL v412 (r5, ', '"RECONSTRUCAO DO KERNEL v412 (r7, ', 0)]),
    ("conferir_nos_intacto_r5_v412.py", "conferir_nos_intacto_r7_v412.py", COM + [("nenhum dos 153 modulos do manifesto R10", "nenhum dos 156 modulos do manifesto R11", 1), ("n_modulos_do_manifesto_R10", "n_modulos_do_manifesto_R11", 1)]),
    ("conferir_decima_lista_v412.py", "conferir_duodecima_lista_v412.py", COM + [
        ("== 153,", "== 156,", 0), ("== 153 ", "== 156 ", 0), ("== 109 ", "== 112 ", 0), ("(17, 27, 109)", "(17, 27, 112)", 1), ('"TGLExt": 8,', '"TGLExt": 11,', 1), ("- 109", "- 112", 0),
        ('e.chk("os 109 restantes', 'e.chk("os 112 restantes', 0), ("len(novas) == 109", "len(novas) == 112", 0), ("C=109", "C=112", 0), ("A=17, B=27, C=109", "A=17, B=27, C=112", 0), ("TGLExt 8,", "TGLExt 11,", 1), ("dos 153 arquivos", "dos 156 arquivos", 0), ("os 153 compilou", "os 156 compilou", 0), ("e os 153", "e os 156", 0),
        ("os 109 restantes", "os 112 restantes", 0), ("os 153 compilou", "os 156 compilou", 0), (", 153, dict(fr))", ", 156, dict(fr))", 1), ("conferir_decima_lista_v412.py -- (contrato R5) confere a DECIMA SEGUNDA lista", "conferir_undecima_lista_v412.py -- (contrato R7) confere a DECIMA SEGUNDA lista", 0),
        ('tj = HERE / "pedras_novas"', CHECK_COMENTARIO + '\ntj = HERE / "pedras_novas"', 1)]),
    ("conferir_ancoras_propostas_v412_r5.py", "conferir_ancoras_propostas_v412_r7.py", COM + []),
    ("e5_11_ancoras_escolhidas_v412.py", "e7_11_ancoras_escolhidas_v412.py", COM + [("(a pagina R18)", "(a pagina R25)", 0), ("contrato R5", "contrato R11", 0),
        ("        regras = {}; info = {}\n", EXTRAS_PAGINA + "        regras = {}; info = {}\n", 1),
        ('"n_ancoras": len(sel), "ancoras": sel}', '"n_ancoras": len(sel), "extras_da_pagina": extras_pag, "ancoras": sel}', 1),
        ('"regra": __doc__.split("Operacionalizacao")[0].strip(), ', '"regra": __doc__.split("Operacionalizacao")[0].strip() + " [R7] Em QUALQUER modulo, com ou sem estrela, entram tambem as declaracoes QUALIFICADAS (nome com ponto) que a pagina cita entre crases e que sao publicas do modulo no relatorio de axiomas, ainda que o insumo das ancoras propostas nao as liste (extras_da_pagina).", ', 1)]),
    ("e5_03_frio_dos_42_v412.py", "e7_03_frio_das_153_v412.py", COM + [
        ('m7 = L.ler_json(L.D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")', 'm7 = L.ler_json(L.D / "insumos" / ("MANIFESTO_PEDRAS_v412_R1" + "0.json"))', 1), ("nomes = [x[\"modulo\"] for x in m7[\"modulos\"]]\nassert len(nomes) == 42", "nomes = [x[\"modulo\"] for x in m7[\"modulos\"]]\nassert len(nomes) == 153", 1),
        ("um dos 42 existe no Nos", "um dos 153 existe no Nos", 1), ('"quarentena_build_42_"', '"quarentena_build_153_"', 1), ("dos 42 modulos que o proprio construtor instalou e compilou no sandbox; nada apagado; as fontes ficam; o lake recompila os 42 a frio",
         "dos 153 modulos da DECIMA lista que o proprio construtor instalou e compilou no sandbox; nada apagado; as fontes ficam; o lake recompila a frio os 153 e as tres pedras novas", 1), ("fontes_dos_42_seguem_no_sandbox", "fontes_dos_153_seguem_no_sandbox", 1),
        ("dos 42 modulos da setima lista", "dos 153 modulos da decima lista", 0), ("os 42 modulos da setima lista", "os 153 modulos da decima lista", 0)]),
]
for orig, dest, trocas in DERIVACOES:
    DV.derivar(orig, dest, trocas, ESTE)
