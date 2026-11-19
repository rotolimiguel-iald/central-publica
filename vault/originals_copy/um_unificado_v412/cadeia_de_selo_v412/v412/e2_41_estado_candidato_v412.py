import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import *

estado_bloco(
    "1_delta_e_gerador_e_candidato",
    True,
    {"delta": D / "delta_v412.py", "gerador": D / "gerar_candidato_v412.py", "candidato": D / "um_v412_candidato.py", "manifesto": D / "CANDIDATO_v412.json", "formal_map": D / "FORMAL_MAP_v412.json", "runtime_pins": D / "v412_pins.py",
     "texto_publico": D / "TEXTO_PUBLICO_v412.json", "traducao_en": D / "O_QUE_FICA_CLARO_v412_R9_EN.md", "registros": D / "registros_v412.py", "guarda": D / "guarda_frases_v412.py"},
    nota="candidato gerado (43 patches: kernel 40 modulos, 903 bandeiras, escada 12308->13211, 4 registros por spec, guarda v412, secao PT/EN, resumo com o paragrafo de P = nP, pisos nos registros da v411); NAO instalado; ensaio a seco ainda por adaptar e rodar",
    proximo="adaptar e rodar ensaio_a_seco_v412.py sobre um_v412_candidato.py; portao do pilar no candidato; guarda de material privado; bateria pre-selo; textos do README/estado/handoff (pos_rito); verificador de historia sobre tudo; recibo das unidades P=nP/fluidos; fecho PRONTO_PARA_GERAR_v412.json",
    extra={"pendencias_conhecidas_do_ensaio": [
        "o registro h0dn_bg1_v411 (funcao selada) pode cobrar a escada exata via _V411_H0DN_CONTRACT baseline.escada (12308); se o ensaio mostrar falha, patchar o literal como o expected_ladder e dizer no relatorio",
        "o resumo mudou: os conferidores do topo (TOPO_RATIFICADO_v411 / _TR11.confere) comparam com o texto ratificado: devem comparar com o texto da v412 (a frase de P = nP trocada; ver CANDIDATO_v412.json resumo_troca_de_pnp)",
        "kh_n1_cobertura_v411 virou piso; nao ha kh_n1_cobertura_v412 no contrato (a arvore nova nao tem pino exato: ponto a dizer a gerencia)",
        "scripts bumpados marcados [A ADAPTAR v412] fazem a cadeia PARAR no passo (rc 4): so' tirar a marca depois de adaptar de verdade",
    ]},
)
print("estado gravado")
