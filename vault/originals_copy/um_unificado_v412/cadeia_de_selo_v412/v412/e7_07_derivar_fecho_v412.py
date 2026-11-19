"""R7: deriva gerar_preparacao_pronta_v412_r7.py (o FECHO PREPARACAO_v412_PRONTA_R7.json) de gerar_preparacao_pronta_v412_r5.py, com as trocas especificas do R7 (lista de 156 modulos, pagina R21, adendo R7)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_deriv_v412 as DV

ESTE = "e7_07_derivar_fecho_v412.py"
COM = [("contrato R5", "contrato R11", 0), ("pagina R18", "pagina R25", 0), ("DECIMA lista", "DECIMA SEGUNDA lista", 0), ("decima lista", "decima segunda lista", 0), ("manifesto R10", "manifesto R12", 0), ("ancoras R10", "ancoras R12", 0),
       ("contrato_REV5", "contrato_REV11", 0)]   # (R11, gerencia c1, 18/11) a copia congelada do contrato vigente esta' em contrato_REV11
T = [
    ('Exame("fecho_R5")', 'Exame("fecho_R11")', 1), ("cresceu com os 153 modulos compilados", "cresceu com os 156 modulos compilados", 1), ("CANDIDATO REGERADO PELO CONTRATO R5 E ENSAIADO", "CANDIDATO REGERADO PELO CONTRATO R11 E ENSAIADO", 1),
    ("ETAPA 2 PELO R5 NAO FECHOU", "ETAPA 2 PELO R11 NAO FECHOU", 1),
    ('"(contrato R7, manifesto R10, ancoras R10, pagina R21)"', '"(contrato R7, manifesto R11, ancoras R11, pagina R21)"', 0),
    ("(contrato R7, manifesto R10, ancoras R10, pagina R21)", "(contrato R7, manifesto R11, ancoras R11, pagina R21)", 0),
    ("o kernel da decima segunda lista fechou", "o kernel da decima segunda lista (156 modulos) fechou", 1),
    ('"lista": "decima (insumos\\\\MANIFESTO_PEDRAS_v412_R10.json)"', '"lista": "duodecima (insumos\\\\MANIFESTO_PEDRAS_v412_R12.json)"', 0),
    ('"lista": "decima (insumos\\\\MANIFESTO_PEDRAS_v412_R12.json)"', '"lista": "duodecima (insumos\\\\MANIFESTO_PEDRAS_v412_R12.json)"', 0),
    ('"estado_da_adaptacao": "ENSAIO_R5_ESTADO_v412.json", "estado_sha16": s16(D / "ENSAIO_R5_ESTADO_v412.json")}', '"estado_da_adaptacao": "DERIVACAO_R7_PIPELINE_v412.json", "estado_sha16": s16(D / "DERIVACAO_R7_PIPELINE_v412.json")}', 1),
    ('ens_est = j(D / "ENSAIO_R5_ESTADO_v412.json") or {}', 'ens_est = j(D / "DERIVACAO_R7_PIPELINE_v412.json") or {}', 1),
    ('"delta_vs_setima_lista": kfecho.get("delta_vs_setima_lista"),', '"delta_vs_setima_lista": kfecho.get("delta_vs_setima_lista"), "decima_lista_build_anterior": kfecho.get("decima_lista_build_anterior"),', 1),
    ("(6) a pagina e' a R18","(6) a pagina e' a R25 (sha16 lido do arquivo, pinado pelo contrato R11)", 1),
    ("cunhagens_v412: as entradas passaram de 10 para 18 (os modulos", "cunhagens_v412: as entradas passaram de 10 para 21 (os modulos", 1),
    ("compilacao a frio dos 153: os artefatos de build dos 42 modulos da setima lista foram movidos (nao apagados) para fora da arvore do lake antes do build; o kernel antigo da v411 foi reaproveitado",
     "compilacao a frio dos 156: os artefatos de build dos 153 modulos da decima lista foram movidos (nao apagados) para C:\\\\t\\\\k412c\\\\quarentena_build_153_<data>, fora de work\\\\, antes do build; o kernel antigo da v411 foi reaproveitado; o build a frio da decima lista (153 modulos, saida zero, so' os tres axiomas) tinha terminado antes e fica so' como informacao (campo decima_lista_build_anterior)", 1),
    ("os recibos regravados conservam o nome (os consumidores os leem pelo nome); os do R4 estao em copia de bytes fora de work\\\\ (GUARDA_R4_ETAPA2_v412.json) e o fecho do R4 fica como esta'; os scripts do R4 ficam intactos e os novos sao copias _r5 ou e5_* (DERIVACAO_R5_v412.json e DERIVACAO_R5_PIPELINE_v412.json)",
     "os recibos regravados conservam o nome (os consumidores os leem pelo nome); os do R4 estao em copia de bytes fora de work\\\\ (GUARDA_R4_ETAPA2_v412.json), os do kernel da decima lista tambem (kernel/GUARDA_R5_KERNEL_v412.json) e o fecho do R4 fica como esta'; os scripts anteriores ficam intactos e os novos sao copias _r7 ou e7_* (DERIVACAO_R7_PIPELINE_v412.json); nao ha' fecho R5: a etapa pelo R5 foi interrompida antes de fechar", 1),
    ("a adaptacao do ensaio a seco foi feita por subagente (cópias _r5 do ensaio e dos auxiliares; ENSAIO_R5_ESTADO_v412.json)", "o ensaio a seco e os auxiliares _r7 foram derivados das copias _r5 (adaptadas por subagente na etapa anterior) por troca de nome de arquivo e de rotulo; o conteudo do ensaio le contagens do contrato, do manifesto e do kernel", 1),
    ("os nomes curtos das oito entradas novas de cunhagens_v412", "os nomes curtos das onze entradas novas de cunhagens_v412 (as oito do R5 e as tres do R7: OPolinomioFixoEBeta, ORazaoDoColapsoEBeta, OCustoEAIsometria)", 1),
    ("os scripts da Etapa 3 (rito, instalacao, custodia, pos-rito) seguem marcados [A ADAPTAR v412] e importam delta_v412 (o do R4)", "os scripts da Etapa 3 (rito, instalacao, custodia, pos-rito) seguem marcados [A ADAPTAR v412] e importam delta_v412 (o do R4)", 1),
    ("        \"os scripts da Etapa 3", "        \"a pagina R25 cita `a_trava_no_nome` (em TraducaoTuring), `the_angle_is_prior` e `the_name_is_the_born_reading_of_the_post` (declaracoes do kernel selado da v411, nao de modulo da lista de 156): por isso nao sao ancora de nenhum registro desta versao; o recibo ANCORAS_ESCOLHIDAS_v412.json lista os nomes da pagina que nao sao declaracao de modulo da lista\",\n        \"os scripts da Etapa 3", 1),
]
DV.derivar("gerar_preparacao_pronta_v412_r5.py", "gerar_preparacao_pronta_v412_r7.py", COM + T, ESTE)
