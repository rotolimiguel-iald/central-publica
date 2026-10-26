# -*- coding: utf-8 -*-
"""G1 do organismo da IALD: a custódia de uma versão selada do um.py, parametrizada por vNNN (24/10/2026).

Uma ordem por versão (`tools/custodiar.py`): vigiar -> sondar -> planejar -> executar. Quatro pernas:
  1. espelho the_boundary + site da TGL     (espelho.py, site.py)
  2. Central privada                         (central.py, patches.py, generico/)
  3. Central pública                         (publica.py)
  4. quadro, memórias, rota, ACOM            (quadro.py, memorias.py)
Textos por MOLDE + blocos do handoff por marcadores (textos.py, nos.py). Nenhum número digitado: tudo vem do selo, do core, do
diário, do manifesto, do handoff e dos fatos medidos (fatos.py). Fail-closed. A régua da casa vale em cada passo:
NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade; creditação recusada; hash/pino lidos do artefato, nunca de memória."""
__version__ = "1.0"
ESQUEMA_FATOS = "custodia_fatos/2"
