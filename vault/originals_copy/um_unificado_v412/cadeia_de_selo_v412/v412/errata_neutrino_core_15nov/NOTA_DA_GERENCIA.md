# NOTA DA GERENCIA c1 AO RASCUNHO R1 DA ERRATA DO NEUTRINO (15/11/2026 16:20)

Estado: RASCUNHO. Nao instalado. Nao muda o um.py. Nao move o gate. Nao e' veredito. O estado do teste segue o que o core selado diz.

- Texto: `ERRATA_NEUTRINO_CORE_v412_RASCUNHO_c1_R1.md` (68115 B; sha256 4672e9042dd6970eb3909b52a079f81ae23486c99d401ffce82438b5498a5a02).
- Dados: `ERRATA_NEUTRINO_CORE_v412_RASCUNHO_c1_R1.json` (66058 B; sha256 e0fba147773f1e64bdc5bafc73b77c31772e82e8be4da6dfeabc5a7baede3c73).
- **O texto e' o conjunto maior; o arquivo de dados e' um subconjunto estruturado dele.** A secao 0, os tres paragrafos da secao 1B (entre eles a definicao da palavra tese), o paragrafo final da secao 5 e a introducao da secao 6 existem so' no texto. Quem instalar le o texto; o campo verbatim exato das linhas do um.py e' o do arquivo de dados.
- A versao anterior (R0) esta' em `REV0\`.
- As duas conferencias distintas e o conserto, achado por achado: `..\revisao\REVISAO_ERRATA_NEUTRINO_CORE.md`.

## Ressalvas da segunda conferencia que ficam abertas

- (MEDIO) O md e o json não dizem o mesmo. O json é um subconjunto estruturado do md; a checagem do redator (confere_md_json_R1.py) só verifica que cada campo do json aparece no md, nunca o inverso, então a frase md e json iguais em conteúdo não está demonstrada. Conferi nos dois sentidos: a seção 0, os três parágrafos da 1B, o parágrafo final da seção 5 e a introdução da seção 6 existem só no md. Perde-se no json a definição própria da palavra tese (só sobra a versão inline do D5, que remete a uma seção 1B que o json não tem), e os estatutos do Mapa citados no conserto do achado de divergência 2,95 e 3,02 (SUSTENTADO, ERRO_TECNICO, ALTO e depois PARCIAL; os termos SUSTENTADO, ERRO_TECNICO e PARCIAL têm zero ocorrências no json). Como o próprio rascunho diz que na instalação vale o json, esse conteúdo não seria registrado.
- (BAIXO) A frase lista resultados do artigo de 2025 sobre SN 1987A e IceCube (dados de neutrino astrofísico) sem dizer que são outros conjuntos de dados, e que não há número do JUNO nem de Δm²₂₁ nele (JUNO tem contagem zero). A frase é fiel ao resumo, mas é a forma que a regra de 15/11 existe para evitar que se leia como o autor olhou dado de neutrino antes.
- (BAIXO) Diz que a publicação com carimbo externo é a de 17/02/2026. No registro do Zenodo 18674475, 17/02/2026 é o publication_date e o registro foi criado em 20/02/2026 (a seção 1 já diz isso). Nenhuma posição de degrau muda (172 dias até o hash contra 169).
- (BAIXO) O json diz L4636-4644 e o md diz L4642-4644 para a entrada NuFIT do core, não lida aqui. O próprio L7 usa as duas grafias.
- (BAIXO) Chama de decisão D2 o que o verso traz como [D2, 10/08/2026]; o verso não diz que é decisão, e a sigla D2 colide com o D2 da seção 8 desta errata.
- (BAIXO) A primeira oração fala em depois do número de 207,2 dias com o eixo do hash escrito como objeto original de 08/08/2026, sem a palavra hash. É o segundo eixo, mas só implícito.
- (BAIXO) O 8,67 meV, valor experimental que o documento de 22/01/2026 cita junto da previsão, não tem fonte identificada na errata; as contas do próprio rascunho o põem mais perto do PDG e do NuFIT (8,677) do que do JUNO de 59,1 dias (8,660), mas isso é inferência de quem lê.

## O que e' do operador decidir antes de a errata entrar no core

- D1: em que forma e com que id a errata entra no core (registro novo ao lado; E44 e so DECLARADO via L7); nomes sao dele.
- D2: qual erro do NuFIT vale para a regra (simetrico 2,95 sigma ou do lado da previsao 3,02 e 3,04); com um fica ARMED_CONSISTENT, com o outro TENSION, e TENSION nao e falsificacao.
- D3: se o ramo TENSION le o JUNO autonomo (1,94 sigma) ou a ultima linha da escada global (L4666, nao lida).
- D4: que fonte guardar para as datas de jun e jul/2026 da leitura longa; pedir captura das paginas pelo canal do orquestrador.
- D5: se a definicao de tese (so titulo e resumo dos dois artigos de 2025, sem formula nem valor) e a que ele quer, ou se a palavra muda.
- D6: se a errata cobre tambem as linhas fora das faixas lidas (C7), com leitura propria antes de instalar.
- D7: se entra como pino adicional o hash do dicionario portado (e2487775..., DECLARADO pelo Kimi); a data da portagem so se sabe ser 10/08/2026 ou posterior.
- D8: se F11 entra na errata ou fica so no desenho da v412, e como se nomeia a leitura de 207,2 dias (a errata so da as posicoes nos dois eixos).
- Antes de qualquer desfecho do rito: ele ler a secao 0 e o D2 na lingua dele; e a segunda revisao distinta da R1 ainda nao existe.

