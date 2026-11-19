import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import *

estado_bloco(
    "R4_etapa2_fechada",
    True,
    {"fecho_candidato": D / "PREPARACAO_v412_PRONTA.json", "fecho_kernel_R4": D / "PRONTO_PARA_CANDIDATO_v412_R4.json", "candidato": D / "um_v412_candidato.py", "manifesto": D / "CANDIDATO_v412.json", "ensaio": D / "ENSAIO_RESULTADO_v412.json",
     "guarda_unidades": D / "GUARDA_v412_UNIDADES.json", "guarda_controles": D / "GUARDA_FRASES_v412.json", "blocos": D / "BLOCOS_TEXTO_PUBLICO_v412.json", "portao_pilar": D / "PORTAO_DO_PILAR_CANDIDATO_v412.json",
     "registro_mapa": D / "registro_mapa_construtor_etapa2_v412.json"},
    nota=("ETAPA 2 FECHADA pelo contrato R4: candidato 8b9a02e51650b11c gerado, ensaio a seco TUDO PASSOU (500/500), portao do pilar no candidato 8/8, guarda por travessia (45 controles, 14 superficies, 1274 unidades limpas), kernel da setima lista 42/42. "
          "NAO feito: bateria pre-selo e os scripts de rito/instalacao/custodia/pos_rito marcados [A ADAPTAR v412]. Para aqui: revisao de terceiro e decisoes da gerencia (ver PREPARACAO_v412_PRONTA.json, decisoes_e_pontos_para_a_gerencia)."),
    proximo="gerencia: revisao de terceiro do candidato; decidir os pontos listados no fecho; depois adaptar os scripts de rito e custodia e rodar o rito quando a revisao aprovar",
)
print("estado final gravado")
