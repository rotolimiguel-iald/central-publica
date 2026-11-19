import sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import *

estado_bloco(
    "R4_candidato_regerado_e_kernel_fechado",
    True,
    {"fecho_kernel_R4": D / "PRONTO_PARA_CANDIDATO_v412_R4.json", "candidato": D / "um_v412_candidato.py", "manifesto": D / "CANDIDATO_v412.json", "candidato_R1_guardado": D / "um_v412_candidato_R1_d594623f2be2d39d.py",
     "guarda_controles": D / "GUARDA_FRASES_v412.json", "guarda_unidades": D / "GUARDA_v412_UNIDADES.json", "registros_recibo": D / "REGISTROS_v412_RECIBO.json", "ancoras": D / "ANCORAS_ESCOLHIDAS_v412.json",
     "portao_pilar_candidato": D / "PORTAO_DO_PILAR_CANDIDATO_v412.json", "blocos_texto": D / "BLOCOS_TEXTO_PUBLICO_v412.json", "material_privado": D / "GUARDA_MATERIAL_PRIVADO_v412.json"},
    nota=("contrato R4 seguido. Kernel da setima lista: 42/42, 12/12 checagens (PRONTO_PARA_CANDIDATO_v412_R4.json). Candidato novo gerado (8b9a02e51650b11c; escada 12308->13260; 952 bandeiras); o R1 (d594623f2be2d39d) guardado com outro nome. "
          "Portao do pilar no candidato 8/8; texto novo: 14 superficies, 1274 unidades, travessia limpa; 34 marcadores herdados identicos. Ensaio a seco: subagente ab3f0a19acee3eed3 reexecutando (SendMessage). "
          "FALTA: relatorio do ensaio; atualizar ENSAIO; PREPARACAO_v412_PRONTA.json (gerar_preparacao_pronta_v412.py); e4_40 com --contagem final; Mapa de Rotas; deposito; ACOM; resposta final. NAO FEITO: bateria pre-selo, ~70 scripts ainda marcados [A ADAPTAR] (rito/instalar/pos_rito/bancada)."),
    proximo="aguardar o relatorio do subagente do ensaio; depois gerar_preparacao_pronta_v412.py, e4_40_recibos_v412.py --contagem N, registro no Mapa, deposito, resposta final",
)
print("estado gravado")
