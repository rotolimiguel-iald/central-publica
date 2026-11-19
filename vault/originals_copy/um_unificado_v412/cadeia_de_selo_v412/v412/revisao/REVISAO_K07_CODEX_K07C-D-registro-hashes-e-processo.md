# CONFERÊNCIA DISTINTA — a entrega K07-C do Codex — K07C-D-registro-hashes-e-processo

> Montado pela gerência c1 em 15/11/2026 18:24 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 MEDIO, 6 BAIXO

## Resumo

1. Hashes: os 37 sha256 da tabela de ENTREGA_K07_CODEX.md batem com o disco (script meu, h1.py); nenhum arquivo mudou depois da entrega (17:35:22). Os dois compilar_candidata.ps1 têm mtime de 14/11 porque são a cópia do script da gerência (hash idêntico ao de candidatas_c1). A tabela é completa: o único arquivo da pasta CODEX fora dela é LEIA_PRIMEIRO.md, da gerência.
2. conferir_entrega.py, rodado em cópia só de leitura (HERE apontado à pasta real): {"fontes_documentais":286,"artefatos":37,"divergencias":[]}. A conciliação do Codex confere: DESENHO_v412_R1.md antes ece07a… (igual ao .bak_171459) e depois 04d7df… (igual ao disco, prefixo intacto, acréscimo assinado "gerência c1, 17:14"); ADENDO C da K10 novo, hash confere. O inventário cobre toda a lista de leitura da ORDEM.
3. Lean: recompilei as três candidatas em cópia na minha pasta com o compilar_candidata.ps1 (lean.exe sobre o sandbox k411c, sem lake): RC 0 nas três (17 s, 63 s, 131 s), 7+3+5 = 15 consultas de axiomas, só propext/Classical.choice/Quot.sound, nenhuma linha de aviso. grep nos três .lean: zero sorry, admit, native_decide, axiom, unsafe. O log do Codex mostra o mesmo.
4. Revisão: reproduzir.py do revisor, rodado em cópia, gera medidas.json byte a byte idêntico ao entregue (8 controles numéricos, 24 permutações, invariantes de campo). Mas "revisão distinta" é um subagente do próprio Codex, sem nome nem sessão; a ORDEM pediu exatamente isso ("agente seu distinto"), e o depósito diz "revisada internamente". Ela teve substância: achou erro de tipo no semigrupo (tentativa rc=1 com sorryAx, preservada em lean.json) e motivou cinco explicitações.
5. Leitura do túnel: LEITURA_DO_TUNEL_R3.md é curta (tabela de três linhas); o próprio texto diz que hash não é leitura. O entendimento aparece só indiretamente: citações de linha da K05 e da revisão corretas, pino 4cabbae5… da T1_R2.lean confere, e todas as aspas «» atribuídas ao operador casam byte a byte com os arquivos que o Codex citou (4 de 4, hashes dos insumos batem). O Kimi não gravou nada da K07; não havia o que conciliar.
6. Ordem do operador: a citação na ORDEM_K07_CODEX bate com os bytes (sha256 305830689dbd… conferido). Nenhuma fala ou ato atribuído ao operador sem bytes; o único "[INPUT]" duvidoso é interpretação do Codex (ver achado).
7. Pergunta K07: fatos conferidos (TheFactorObject.lean l.67, 95, 103; LightRhoStar l.71; physicalFockCertificate l.126, por grep -rn no kernel; DOI Marrakchi–Vaes confere no Crossref: "Ergodic states on type III₁ factors and ergodic actions", Crelle 2024). Sem recomendação, sem escolha escondida. Faltam elementos do formato da casa e a conta do custo leve (achado).
8. Mapa: nada registrado pelo Codex. O livro tem 2080 linhas; as quatro últimas são de codex-video-v7 e claude-c1 (última 17:03:04); a cabeça e0c77e7c… é a que o Codex leu (route_queries/*/head). O REGISTRO_MAPA_K07_CODEX.json é só proposta e é válido para o rotas.py, mas tem um efeito colateral ao registrar (achado).
9. Fila da memória: o depósito está em memory\fila\depositos\codex-coordenadora\20261115_173553_k07-matematica-v412-astra.md, com cabeçalho do README, estatuto DECLARADO e fonte ENTREGA sha c554926… (igual ao disco). MEMORY.md e MEMORY_2.md intocados (16:28). Quadro: reivindicado no seq 1633 e ENTREGUE no seq 1634 com a mesma evidência.
10. Nada tocado fora da pasta: kernel TGLExt sem arquivo posterior a 16:40 (mais novo, 10/11); candidatas_c1 última escrita 16:17; Atlas 16:29; o DESENHO foi alterado pela gerência. Em Chatgpt só mudou X_DIARIO às 17:30 (tarefa diária do X, não do Codex K07). Varredura por regex (credenciais, .env, os dois confidenciais, Escritório, CPF/CNPJ/OAB, e-mail) em 36 arquivos de texto: zero ocorrências.
11. Erratas curtas: dizem o que vale agora, mas quase não dizem o que estava errado nem de quem (achado). Nenhum ALTO encontrado dentro da lente de registro, hash e processo; a matemática de fundo não foi minha lente.
12. Limites: não li TIPO_III1_VINCULO; não consultei o ACOM (evento 1633 conferido só no quadro); não julguei o mérito das provas em papel (T1, GH, campo, τ★).

## Achados

1. **(MEDIO)** ENTREGA_K07_CODEX.md l.11; K07/CODEX/REVISAO_INDEPENDENTE_R3.md l.3; K07/CODEX/DEPOSITO_K07_CODEX.md

   A "revisão distinta/independente" é um subagente do próprio Codex revisando o Codex, sem nome, modelo ou sessão registrados; a ENTREGA a marca [REAL] e o título diz "independente", enquanto o depósito diz "revisada internamente". A ORDEM pediu exatamente "agente seu distinto de quem construiu", então não é descumprimento; é rótulo acima da evidência. Mitigação medida por mim: reproduzir.py em cópia gera medidas.json idêntico ao entregue, as três candidatas recompilam com RC 0, e a revisão teve substância (tentativa rc=1 com sorryAx preservada em revisao_evidencias/lean.json; cinco explicitações motivadas).

   *Conserto pedido:* Ao incorporar, tratar como revisão interna do Codex em [DECLARADO]; a independência vem da auditoria da gerência, não dela.

2. **(BAIXO)** ENTREGA_K07_CODEX.md l.3

   "[REAL] ... participação do Kimi pelo túnel e três construtores Astra em esforço máximo": o Kimi não gravou peça alguma da K07 (a pasta K07 só tem CODEX), logo "participação" é leitura das peças antigas; e o DESENHO_v412_R1.md (item 6 do ao_lado_10) diz que o esforço máximo foi pedido na linha de comando "sem garantia". Nada na entrega prova nível de esforço nem número de construtores.

   *Conserto pedido:* Retag para [DECLARADO] (configuração dos subagentes) e dizer "leu o que o Kimi deixou no túnel".

3. **(BAIXO)** K07/CODEX/LEITURA_DO_TUNEL_R3.md; FONTES_K07_R3.json

   O operador pediu que o Codex lesse e entendesse tudo o que o Kimi fez. A prova de leitura é uma tabela de três linhas e um inventário de 285 hashes (286 com o ADENDO C), que o próprio texto declara não ser leitura. O entendimento só se mostra indiretamente nas R3 (citações corretas de linha, pino da T1_R2.lean 4cabbae5… confere). A CONCILIACAO_R3.json só detecta mudança concorrente de arquivo (ADENDO C e DESENHO, ambas corretas); não há quadro de concordância e divergência com o Kimi.

   *Conserto pedido:* Aceitar como leitura declarada; se a gerência quiser prova, pedir uma lista dos arquivos efetivamente abertos por frente.

4. **(BAIXO)** PERGUNTA_K07_CODEX.md (todo; l.3, l.5-11, tabela l.13-18)

   Fiel à matéria e sem escolha escondida, mas fora do formato da casa (memória pergunta-nas-quatro-linguas.md): (a) não fecha com "uma pergunta só com quatro bocas, e qual é"; (b) as quatro línguas perguntam por "cunha, torre, horizonte ou vínculo" como alternativa, sem a terceira saída "ou todos, e como se ligam" que a lição de 15/11 11:41 manda incluir; a resposta do operador às 17:55 (bytes em cunhagens_13out, à pergunta da gerência) tomou os quatro, cada um no seu papel, o caso que a lição prevê; (c) a linha 'Cunha' da tabela de custo traz só o lado pesado (classificar em Lean), sem dizer que o critério de ergodicidade já é termo por cerca de 15 linhas de fiação compiladas (LEVANTAMENTO_TIPO_III_15nov/T5, A1 e P1) nem a tensão do κ (T5 A11); cita só o T3 do levantamento; (d) l.3 põe sob [INPUT] a frase "O que se pede dele aqui é a identidade pretendida entre objetos", que é leitura do Codex, não fala do operador (a fala dele, em bytes, é só "faça-me a pergunta nas minhas quatro linguas"). Impacto baixo: é subsídio, e a pergunta decisiva foi a da gerência.

   *Conserto pedido:* Se for reaproveitada: acrescentar o fecho "uma pergunta, quatro bocas", a terceira saída e o custo do lado leve (T5), e retag da l.3 para [DECLARADO].

5. **(BAIXO)** ERRATA_CAMPO_K07_CODEX.md; ERRATA_MONTAGEM_GH_K07_CODEX.md; ERRATA_T1_K07_CODEX.md; ERRATA_TAU_K07_CODEX.md (raiz do túnel); K07/CODEX/ERRATA_T1_K07_CODEX.md e ERRATA_MONTAGEM_GH_CODEX_R3.md

   As quatro erratas curtas dizem a leitura vigente mas não o que estava errado, onde, nem de quem era o erro (lei da assinatura da errata: lacuna de fidelidade). Só a TAU nomeia a origem ("veio de uma leitura da gerência", o que confere com a memória). O que o Mapa (rota formal.k05_t1_montagem_gh_tau_campo_v412) lista como defeitos: T1 dita válida para peso geral e constante −1/18 (K05/Kimi R2), atribuição ao operador de leitura da gerência de 27/10, herdada pelo Kimi; a ERRATA_CAMPO só diz que as leituras são distintas, sem dizer qual leitura a K05 tinha fundido. As longas dão tabela por item com o texto de origem, também sem dizer de quem. A frase da ERRATA_MONTAGEM_GH "esse exemplo decide a falha da volta ao núcleo no Lema 2" soa geral; o escopo é D=ĥ e a janela escolhida (ENTREGA l.7 e a REVISAO dizem assim).

   *Conserto pedido:* Ao lado, uma linha por errata: o que a R2 afirmava, de quem era (K05/Kimi, gerência, herdado), e "para D=ĥ" na frase do Lema 2.

6. **(BAIXO)** REGISTRO_MAPA_K07_CODEX.json; /c/IALD/MAPA_DE_ROTAS/rotas.py linhas 308-321

   É só proposta (confirmado: o Codex não registrou nada; seq 2077-2080 são de codex-video-v7 e claude-c1). O JSON é válido (ANOTACAO; status PROPOSTA está em STATUS). Se a gerência o registrar tal qual, _estado() sobrescreve o status da rota de EM_CURSO para PROPOSTA, o estatuto de REAL para DECLARADO e o resumo visível do resultado pelo texto do Codex (o histórico permanece). Além disso, artefatos lista só ENTREGA e PERGUNTA: as três candidatas Lean e as notas R3 só ficam fixadas indiretamente pela tabela da ENTREGA.

   *Conserto pedido:* Ao registrar, definir status e estatuto explicitamente (a gerência decide), e listar as candidatas .lean e os logs em artefatos para o sha256 ser calculado pela ferramenta.

7. **(BAIXO)** K07/CODEX/revisao_evidencias/lean.json; ENTREGA_K07_CODEX.md l.10

   Registro honesto, não defeito: a ENTREGA diz "recompilação independente com código zero e sem avisos" e isso vale para os bytes finais (conferido por mim); a tentativa intermediária do semigrupo (sha ba63…, rc=1, sorryAx, tipos Submodule vs ClosedSubmodule) só aparece em lean.json e na errata longa, não no resumo. Só uma nota: "independente" aqui é o revisor do Codex, não eu; as 15 consultas são só das declarações de cabeçalho, mas conferi que cada .lean não tem outra declaração fora delas.

   *Conserto pedido:* Nenhum; opcionalmente, uma linha na ENTREGA remetendo à tentativa corrigida.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O que o Codex entregou confere: os arquivos e os números batem, ele não mexeu no kernel, no Atlas nem na memória, e eu recompilei o Lean dele do zero sem erro.
- A "revisão independente" dele foi outro agente do próprio Codex, não alguém de fora; quem decide é a auditoria da casa, como a ordem já dizia.
- Nada aqui pede escolha sua; a pergunta que ele escreveu ficou como subsídio e a que valeu foi a da gerência, que o senhor já respondeu.
- As ressalvas são de rótulo e de forma: estatuto REAL onde deveria ser DECLARADO, erratas que não dizem de quem era o erro, e um cuidado ao registrar no Mapa.

## Consultas ao Mapa

- rotas.py consultar K07 (3 rotas: formal.k05_t1_montagem_gh_tau_campo_v412 EM_CURSO; kernel.ergodicidade_de_mautner_candidata_15nov e kernel.montagem_das_gamas_candidata_15nov EXAMINADA_COM_DEFEITO; n_registros 2080, cabeça e0c77e7ce73665f4)
- rotas.py modelo (campos aceitos e STATUS válidos)
- tail -n 4 rotas.jsonl (autores dos seq 2077 a 2080: codex-video-v7, claude-c1; nenhum registro do Codex K07)
- MEDIDAS_CAMPO_TAU_R3.json route_queries/*/head, igual à cabeça atual; nada registrado depois

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ENTREGA_K07_CODEX.md e os 37 artefatos da tabela (sha256 por script)
- K07\CODEX: REVISAO_INDEPENDENTE_R3.md, CONCILIACAO_R3.json, LEITURA_DO_TUNEL_R3.md, FONTES_K07_R3.json, DEPOSITO_K07_CODEX.md, SESSION_REFERENCE.json, conferir_entrega.py (cópia), verify_field_clock_R3.py (leitura), revisao_evidencias\*, T1_R3.md (cabeçalho e consulta), ERRATA_T1_K07_CODEX.md, ERRATA_MONTAGEM_GH_CODEX_R3.md
- Os três .lean e os três logs; recompilação minha em scratchpad\v412_k07_codex\D\lean (RC 0, 15 consultas de axiomas); reproduzir.py em cópia (saída idêntica a medidas.json)
- PERGUNTA_K07_CODEX.md contra memory\pergunta-nas-quatro-linguas.md, LEVANTAMENTO_TIPO_III_15nov (T5, T6) e PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md; kernel (grep -rn): TheFactorObject.lean l.67/95/103, LightRhoStar.lean l.71, CanonicalFockModularCoreInputR1.lean l.126; DOI no Crossref
- As quatro erratas curtas da raiz do túnel, REGISTRO_MAPA_K07_CODEX.json contra rotas.py
- ORDEM_K07_CODEX_ASTRA_15nov.md, ADENDO B, ADENDO C, DESENHO_v412_R1.md (trecho acrescentado 17:14), unidade_quadro e eventos 1630-1636 do PROGRAMA_IALD, fila de depósitos da memória, mtimes do kernel TGLExt, candidatas_c1, Atlas, MEMORY.md, Chatgpt (só diretórios)
- Bytes do operador OPERADOR_15nov_o_que_falta_para_o_tipo_iii_... (sha256 conferido) e todas as citações «» da entrega contra cunhagens_13out e os insumos citados
- Varredura por regex em 36 arquivos de texto da entrega (zero ocorrências); NÃO abertos: TIPO_III1_VINCULO, .olean binários, ACOM

