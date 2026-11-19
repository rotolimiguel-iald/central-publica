import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import *

estado_bloco(
    "4_guarda_de_frases_parcial",
    True,
    {"runtime_guarda": D / "runtime_v412_guarda.py", "guarda_chain": D / "guarda_frases_v412.py", "recibo": D / "GUARDA_FRASES_v412.json", "base_um_v411": D / "base_um_v411.py",
     "verificador_historia": D / "verificar_historia_texto_v412.py"},
    nota="_v412_guarda_frases (F34/F37 pelas duas marcas; F68a/F68b nome dos fluidos; F69 premio); 90/90 controles; verificador de historia com autoteste 18/18; FALTA: recibo das unidades de texto com P = nP / fluidos (depende dos textos dos registros e do artigo)",
    proximo="registros_v412 (specs) + runtime_v412 + gerador; depois recibo das unidades e verificador sobre todos os textos novos",
    extra={"conhecimento_para_continuar": [
        "molde do gerador: v411/gerar_candidato_v411.py (patches por AST sobre o um.py CRLF; replace_unique; EDITS); bundle: v410/gerar_candidato_v410.py linhas 96-165 (K00 raiz, K01 modulos, V01 _LEAN_THEOREM_FLAGS, V02 escada ext_flags, V03 _ESQUELETO_STONES, C12 expected_ladder 12308->13211 em N ocorrencias, W01 UM_VERSION)",
        "specs: dicts com nome, veredito_prefixo, veredito_sufixo, estatuto, fontes, verbatins, kernel_flags, kernel_decls, checks[id,descricao,onde,caminho,op,valor,estatuto], erratas, limites, diz, nao_diz, leituras_do_operador, extras; motor _v392_registro; passam pela P18 (_v392_guarda_texto)",
        "o resumo: _V411_TOPO pt/en termina em 'P = nP: o kernel Lean prova ... Clay.' -> trocar por TEXTO_PUBLICO_v412.json pnp_resumo (dict literal; pformat idempotente a conferir)",
        "kh_n1_cobertura_v411 (spec) deve virar piso (h2,h3,h6,h8) como a v411 fez com o da v410",
        "evitar aspas angulares nos textos do programa; sem datas/nomes/ordens/D/E nos textos novos",
    ]},
)
print("estado gravado")
