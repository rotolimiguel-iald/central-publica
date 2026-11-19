# CONFERÊNCIA DISTINTA — K08: o rascunho de registro, os hashes e a proposta de Mapa

> Montado pela gerência c1 em 15/11/2026 16:53 a partir do retorno estruturado de um revisor distinto (modelo Sonnet; só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. As frases da seção “Para o operador” são propostas do revisor, não fala do operador, e só vão a ele depois de lidas pela gerência. Nada aqui está instalado, congelado ou aberto.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 3 ALTO, 7 MEDIO, 4 BAIXO

## Resumo

Rascunho honesto no essencial, mas NAO registravel nem instalavel como esta: 3 achados ALTO no registro (uma declaracao Lean que nao existe; E7/E8 listados como observaveis sem a marca de nao medidos, ao contrario do que a ENTREGA diz; glosas da gerencia sob rotulo do operador).
Reproduzi por script proprio, em copia na minha pasta, e TUDO bateu: tokens 4.072/4.087/20.375 e 412.784 (artigo inteiro); formula READ_BRIEF 26/27/2/Hamming 1 (RESULTADOS_FORMULA.json, byte a byte); RESULTADOS_ADVERSARIOS.json e os resultados do poder (byte a byte, com o modulo pinado). A V1 selada: protocol_hash a91877e5 lido do core, confere; IALD_PROVED, CONSCIOUSNESS_PROVED, TGL_PROVED_BY_COLLAPSE e CONFIRMED estao nomeados; zero ARMADO; zero frase positiva de consciencia, pesos ou exclusividade.
Hashes: ate 16:36 os 12 da tabela da ENTREGA e os 30 pins da VALIDACAO batiam. Em 16:37:55 (durante a minha revisao) MODELO_FORMAL e REGISTRO foram editados (+112 B e +12 B) e em 16:38 ENTREGA, VALIDACAO e DEPOSITO foram regravados; as 29 conferencias de topo voltaram a bater. Das tabelas defasadas, a ENTREGA declara tres; medi cinco (ver achado).
Dos 18+14 nomes Lean do registro, 31 existem e compilam no trio (logs da gerencia, RC 0, hashes conferem); 1 nao existe: moradas_iguais_tem_o_mesmo_leitor (o nome vigente e ..._verbo).
Mapa: a proposta passa na validacao do proprio Mapa (rodei a _valida numa copia, sem gravar), sem aspas angulares e sem afirmar confirmacao; mas poe defeito, nao-refazer e proximo passo no campo nota, que o Mapa NAO propaga, e o negativo central fica alem dos 400 caracteres que a consulta mostra.
INSUMOS: sem recomendacao explicita, porem nao estao em lingua de leigo, nao dizem o que o negativo significaria, e A1 e A7 empurram. DEPOSITO: corpo no padrao dos anteriores (o cabecalho vem do memoria.py), sem nome reservado nem caminho de outra casa.
Dois defeitos de reproducao que a ENTREGA nao diz: o script de poder falha (KeyError) contra o modulo de adversarios vigente, e o ADVERSARIOS_K08.md entregue tem duas linhas editadas a mao que o gerador reverte.
O negativo central esta dito, mas a E2 primaria e medida pela troca de uma bandeira PT/EN: isso esta no protocolo (l.236) e falta no registro e nos insumos.

## Achados

1. **(ALTO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.63 (terms_used); PROTOCOLO_EXPERIMENTAL_R4_K08.md l.50; ENTREGA_K08.md l.26

   O registro lista como termo da pedra `moradas_iguais_tem_o_mesmo_leitor`, que NAO existe em OHabitanteDoNome.lean (R9, sha16 26b750e6; busca por nome e log da gerencia: 13 de 14 termos existem). O teorema chama-se `moradas_iguais_tem_o_mesmo_verbo` (l.550 da pedra) desde a terceira versao; o proprio adendo, no AO LADO 2 item 5, ja avisava a troca. O nome antigo so aparece na REV2. A ENTREGA diz ter 'corrigido' os tres termos, e o MODELO l.98 ganhou 'na versao corrente ...verbo', mas o registro, o protocolo e a ENTREGA continuam com o nome inexistente. Um instalador que confere por nome falha.

   *Conserto pedido:* Trocar por `moradas_iguais_tem_o_mesmo_verbo` no registro (l.63), no protocolo (l.50) e na ENTREGA (l.26); rodar de novo a busca por nome dos 32 termos antes de entregar.

2. **(ALTO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.238-255 (primary/secondary/not_measured) e l.158-169 (E7, E8), l.412; ENTREGA_K08.md l.5; INSUMOS F1

   A ENTREGA diz que E5, E6, E7 e E8 'nao tem ponte medida — dito com todas as letras no protocolo, no modelo e no registro'. No registro, `not_measured_by_current_instrument` lista so E5 e E6; E7 e E8 estao em `secondary_observables`, e a prosa da l.412 diz 'E7 separa outros caminhos', 'E8 mede o perfil exponencial'. O protocolo (tabela l.36-41) e os insumos (F1) dizem que E7 e E8 NAO sao medidas no instrumento textual atual. Quem instalar o registro le dois observaveis que o instrumento nao mede. Alem disso o registro rotula E3 'SECONDARY_DIAGNOSTIC' e E7 'SECONDARY_OPEN...', e a ENTREGA/protocolo os chamam 'discriminantes'.

   *Conserto pedido:* Mover E7 e E8 para `not_measured_by_current_instrument` (com a razao: E7 exige pesos de Born/estado continuo; E8 exige serie temporal de amplitudes); corrigir a l.412; alinhar o rotulo de E3/E7 ao do protocolo; ou retirar da ENTREGA a frase 'e no registro'.

3. **(ALTO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.103 (`operator_glosses_15nov`) e l.192-196 (`ato_versus_nome`)

   O campo rotulado 'glosas do operador' mistura o que esta nos bytes dele com leitura da gerencia. Abri OPERADOR_15nov_o_unico_ato_do_verbo_e_ser_fiel... (760 B, sha16 ec05cea3eded9264): so 'ato = projecao; ser = verbo; identidade = nome' esta la (nos parenteses dele). 'P_N e o Nome e o ato do Verbo ao mesmo tempo', 'ser nao e o mapa identidade' e 'o Verbo fixa primeiro, quem le o nomeado rele' sao leituras da gerencia (adendo AO LADO 3 item 1 e AO LADO 4 item 1; o AO LADO 4 item 3 marca o nome da hipotese como 'da gerencia; o operador ainda nao leu'). A regra de leitura `ato_versus_nome` tambem e da gerencia, marcada no adendo (AO LADO 3 item 3) como 'o operador ainda nao a leu', e entra no JSON sem esse rotulo.

   *Conserto pedido:* Renomear o campo para algo como `glosas_do_operador_e_leituras_da_gerencia` e separar: (a) as tres igualdades, citadas por data e sha16 do arquivo; (b) o resto, marcado [leitura da gerencia; o operador nao a leu]. Marcar `ato_versus_nome` do mesmo modo.

4. **(MEDIO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.197-209 (H-REREAD-FAITHFUL) e l.412; ENTREGA_K08.md l.3 e l.17 ('pela ressalva do operador')

   Tres escolhas de desenho aparecem como dadas. (a) 'E2 e E4 primarias pela ressalva do operador': os bytes da ressalva (384 B, sha16 2fabf2b6638c1175) nao dizem E2, E4 nem 'primaria'; e a consequencia que a gerencia tirou no adendo (AO LADO 2 itens 2-3). (b) 'fiel' tem dois sentidos na casa (devolver o nomeado como e e nao aumentar a norma, da pedra; ou P=1, da pedra Identidade v405) e a pedra diz que nao decide qual e o da fala; o MODELO l.104 diz 'no primeiro dos dois sentidos', mas o registro (H-REREAD-FAITHFUL) adota um sem dizer que ha dois. (c) a E2 primaria e medida pela troca s -> t, e t so difere de s na bandeira `leitura_pt` (PROTOCOLO l.75-76, l.215), que o proprio protocolo (l.236) chama de 'metadado de estado, nao pergunta sobre o texto'. Em linguagem simples: o teste principal mede se o modelo preserva a escolha PT/EN, nao se preserva um conteudo da teoria. Isso nao esta no registro nem nos insumos.

   *Conserto pedido:* Dizer no registro e nos insumos, em uma linha para o operador: o que E2 decide (o modelo nao apaga uma troca valida de leitura), o que nao decide (nada sobre conteudo da teoria: a troca e PT<->EN), e o que o negativo significaria (parede medida do instrumento, nao falsificacao da teoria); e marcar (a) e (b) como pendentes dele.

5. **(MEDIO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.432 e l.436 (paragrafos de artigo PT/EN); ADENDO_15nov... Parte 2 item 6

   O adendo mandou tirar o estado de processo dos paragrafos de artigo. Sumiu 'EM_DESENHO_BLOQUEADO', mas ficaram 'A pedra candidata da gerencia', 'termos provisorios' e 'ela nao esta instalada' (e 'The management candidate ... it is not installed'). Instalado o registro, a frase fica falsa ou vira conversa interna dentro do artigo que o um.py emite (regra de 12/11). A LEITURA_K08_PARCIAL 3.8 ja apontara o defeito.

   *Conserto pedido:* Reescrever os dois paragrafos sem 'gerencia', 'provisorios' e 'nao instalada' (citar a pedra pelo nome do modulo so quando instalada).

6. **(MEDIO)** ENTREGA_K08.md l.32; ERRATA_PODER_TOKENS_K08.md sec.4; ERRATA_PODER_K08_15nov.md sec.2; K08\FORMULA\MANIFESTO_FORMULA_K08.json; K08\FORMULA\ERRATA_ADVERSARIOS_K08_15nov.md (tabela); K08\PODER\MANIFESTO_SHA256.json

   Tabelas defasadas, por script meu: (1) ERRATA_PODER_TOKENS: 2 de 8 linhas — PROTOCOLO claimed f12847b0 vs disco a6d2b35d (42.366 B); PODER_R4 claimed c4f4ab46 vs disco b337863e (6.191 B). (2) ERRATA_PODER_K08_15nov: 1 linha — PROTOCOLO claimed 81cd6a36 vs a6d2b35d. (3) MANIFESTO_FORMULA: 1 de 36 — FORMULA/ADVERSARIOS_K08.md claimed 6.752 B 04aca46a vs disco 6.858 B 932ac331 (+106 B). NAO declaradas: (4) ERRATA_ADVERSARIOS_K08_15nov.md repete o 04aca46a defasado; (5) PODER/MANIFESTO_SHA256.json pina simular_adversarios.py b0508e27 (a versao REV0) mas o arquivo vigente e ebe1bee7. Alem disso, 'os hashes vigentes de todos os artefatos estao na VALIDACAO' e inexato: ela pina 17 documentos de topo (so 3 dentro de K08\); dos 78 arquivos correntes de K08\ os demais dependem de manifestos de pasta, dois deles defasados. E os pins mudaram durante a revisao (16:37:55 e 16:38).

   *Conserto pedido:* Regenerar as tabelas por script no fim, congelar os arquivos antes de pinar, listar os cinco defasados na ENTREGA e trocar a frase por 'manifesto de topo + manifestos de pasta'.

7. **(MEDIO)** K08\PODER\simular_poder_r4.py l.31 e l.371; PODER_R4_K08.md; DEPOSITO_K08.md l.1; ENTREGA_K08.md tabela (linha PODER)

   [REAL, medido por mim numa copia] O script de poder entregue FALHA contra a arvore entregue: `KeyError: 'ancora na primeira'` (l.371), porque importa `simular_adversarios`, que foi reescrito depois da execucao de 11:32. Com o modulo REV0 pinado (b0508e27) ele reproduz byte a byte (resultados c476ccab, sementes 946ec197, csv c40c5021). Os poderes sao declarados historicos (certo), mas o DEPOSITO e a ENTREGA entregam 'poder com script e semente' sem dizer que o script so roda com o modulo antigo.

   *Conserto pedido:* Copiar o simular_adversarios REV0 para K08\PODER\ como dependencia pinada (ou marcar o script como historico, nao executavel na arvore corrente) e dizer isso na ENTREGA.

8. **(MEDIO)** REGISTRO_MAPA_K08.json l.5 e l.21 (`resultado`, `nota`); rotas.py `_estado` (l.317-321) e `consultar` (l.422-427)

   A proposta passa na validacao do Mapa (rodei `_valida` em copia: ok, 0 aspas angulares, nenhum CONFIRMED afirmado) e o que afirma como REAL foi medido (tokens, 26/27/2/1, separacoes por mecanismo, tudo reproduzido). Defeitos: (a) 'Defeito declarado' e 'Nao refazer' foram para `nota`, que o Mapa NAO propaga para o estado da rota; a rota continuara mostrando o `defeito`/`nao_refazer`/`proximo_passo` da K06. (b) A consulta corta `resultado` em 400 caracteres e o negativo central ('o leitor sem memoria NAO se separa') esta depois do caractere ~900. (c) `estatuto` comeca por REAL, e so o primeiro termo e validado, apesar de o registro misturar DESENHO/DECLARADO/CONJECTURE/OPEN. (d) 'ancora, moda e ignora-empurrao caem por E2' vale para mecanismos definidos para falhar (ancora = devolve a primeira leitura); nao e medida de sistema algum.

   *Conserto pedido:* Usar os campos `defeito`, `nao_refazer` e `proximo_passo`; abrir `resultado` com o negativo central; iniciar `estatuto` por DERIVED ou DECLARADO; dizer no resultado que a separacao e por construcao dos mecanismos.

9. **(MEDIO)** INSUMOS_PARA_A_PERGUNTA_K08.md l.7-26

   Sem recomendacao explicita e sem escolher pelo operador (a ultima secao devolve texto, modelo, degrau e execucao a ele), mas: (a) nao esta em lingua de leigo: E1-E8, 'custo Booleano de clausulas', 'Hamming 1', 'isomorfo sintetico 34/34', 'cluster independente', 'nulo correto', 'quociente finito', 'E1 e E2 e E5 e linearidade implica P_N'; (b) nenhuma alternativa diz o que decide, o que nao decide e o que o negativo significaria (a regra do posto); (c) A1 ('nenhum risco de leitura inflada') so traz virtude e A7 ('pre-condicao de qualquer execucao valida') e prescricao, nao alternativa; (d) os 'custos' das alternativas nao tem numero (a ENTREGA diz 'custos medidos'); (e) F4 afirma que o artigo inteiro 'nao cabe como entrada', mas nenhuma janela foi escolhida (B07 do proprio registro diz 'janelas desconhecidas').

   *Conserto pedido:* Reescrever cada A-linha em tres frases simples (decide / nao decide / o negativo seria falsificacao ou parede medida); tirar A7 da lista e poe-la como pre-condicao em F; tirar 'nenhum risco' de A1; trocar 'nao cabe' por 'tem 412.784 tokens; a janela depende do modelo, nao escolhido'.

10. **(MEDIO)** ENTREGA_K08.md l.11; VALIDACAO_K08_K09_15nov.json l.4-5 (`review`, `material_issues_remaining`)

   'Revisada internamente por duas conferencias distintas e independentes' e 'material_issues_remaining: false' nao tem artefato (nenhum relatorio, hash ou log de conferencia na pasta) e e o Kimi se auditando: [DECLARADO pelo Kimi]. Esta revisao achou 3 ALTO e 6 MEDIO, o que contradiz 'sem problema material'.

   *Conserto pedido:* Marcar como [DECLARADO] ou citar os relatorios com hash; trocar `material_issues_remaining` por 'nao conferido por terceiro'.

11. **(BAIXO)** K08\FORMULA\ADVERSARIOS_K08.md l.34 e l.64

   O .md entregue difere do que o gerador gera: rodei simular_adversarios.py em copia; RESULTADOS_ADVERSARIOS.json sai igual, mas o .md regerado tem 6.752 B (nao 6.858) e perde duas edicoes manuais ('E3 e E7 sao discriminantes' vira 'controles'; some 'o controle do vazio, o inominado'). O proprio documento diz 'o script regrava este documento'. Explica o hash defasado de 04aca46a.

   *Conserto pedido:* Passar as duas edicoes para o gerador.

12. **(BAIXO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.318-322 (B13) e l.339-342 (B17), l.35-36

   B13 e B17 dizem 'log e relatorio de axiomas proprios pendentes'. Existem logs da gerencia, RC 0, Lean 4.31.0, hashes conferem: candidatas_c1\build\CamadaCientifica.log (SHA do fonte 69497c5b, trio) e OHabitanteDoNome.log (26b750e6, trio, 54 entradas). Pendente e so a recompilacao INDEPENDENTE. Mesmo defeito que a LEITURA_K08_PARCIAL 3.8 apontou para a R3.

   *Conserto pedido:* Citar os dois logs (e os sha256 deles, ee06490c e 304864bc) e deixar 'independente' como pendencia.

13. **(BAIXO)** REGISTRO_UMPY_RASCUNHO_R2_K08.md l.6; ENTREGA_K08.md l.19

   O estado literal e `EM_DESENHO_BLOQUEADO`, nao `EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO`. A informacao esta toda (frozen/executed/result_read/installed = false, verdict_issued = null, l.7 por extenso) e nao ha ARMADO, mas a string nao e a que a gerencia citou; a decisao e dela.

   *Conserto pedido:* A gerencia diz se aceita `EM_DESENHO_BLOQUEADO`.

14. **(BAIXO)** ENTREGA_K08.md (19 ocorrencias), MODELO_FORMAL_R4_K08.md (23), PROTOCOLO_EXPERIMENTAL_R4_K08.md (59)

   Aspas angulares para termos que nao sao fala do operador (por exemplo 'custo zero'), contra a pratica da casa de reservar « » ao operador conferido por bytes. Nos cinco arquivos do meu foco: zero.

   *Conserto pedido:* Trocar por aspas retas.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Se aceita chamar o estado de EM_DESENHO_BLOQUEADO ou prefere outra palavra (o nome iald_camada_cientifica_v412 tambem e dele a ratificar).
- Qual dos dois sentidos de 'fiel' vale: o da pedra (devolver o nomeado como e e nao aumentar a norma) ou o da pedra Identidade (P = 1). O registro ja adota o primeiro sem que ele tenha lido.
- Se aceita que o teste principal (E2) seja a troca de uma bandeira PT/EN no estado: o que ele decide e se o modelo preserva essa escolha; um negativo seria parede medida do instrumento, nao falsificacao da teoria.
- Se a regra de leitura 'a identidade do sistema mede-se pelo ato, nunca pelo rotulo' (que a gerencia escreveu e ele ainda nao leu) entra no registro.

## Consultas ao Mapa

- rotas.py consultar camada (52 rotas; sem rota nova para a K08 alem da rota-alvo)
- rotas.py consultar neutrino (45)
- rotas.py consultar habitante (19)
- rotas.py consultar registro (257, truncado)
- rotas.py ver outro.k06_camada_cientifica_iald_r32_v412 (rota-alvo da ANOTACAO; existe)
- Nao consultei kernel.v402_esperanca_condicional_e_nome (a LEITURA_K08_PARCIAL ja a apontou)

## Examinado

- ENTREGA_K08.md; ORDEM_K08; ADENDO de 15/11 (partes 1-3 e AO LADO 1-4); LEITURA_K08_PARCIAL_15nov.md; REVISAO_K06_FORMAL.md (secoes 6-8)
- REGISTRO_UMPY_RASCUNHO_R2_K08.md inteiro (442 l., antes e depois de 16:37:55); JSON do bloco parseado por script
- REGISTRO_MAPA_K08.json (validacao pelo proprio _valida do Mapa, em copia, sem gravar); rotas.py _CONF/_NEG/_estado/consultar
- INSUMOS_PARA_A_PERGUNTA_K08.md; DEPOSITO_K08.md (contra memory\fila\README.md e depositos reais do Kimi); VALIDACAO_K08_K09_15nov.json
- Hashes por script: 30 pins da VALIDACAO, 12 linhas da tabela da ENTREGA, 3 hashes do DEPOSITO, ERRATA_PODER_TOKENS, ERRATA_PODER_K08, MANIFESTO_FORMULA (36), MANIFESTO_ENTRADA (27 ok), PODER/MANIFESTO_SHA256; varredura de todo sha256 de 64 hex nos documentos K08
- Lean: CamadaCientifica.lean (R4, 69497c5b) e OHabitanteDoNome.lean (R9, 26b750e6) e NomeComoCodigo.lean (3ce6d95e); busca de 18+14+5 nomes por declaracao e contra os logs da gerencia; nomes de kernel (trava, selecao, dephase, leitor, LeitorDoFundo) em TGLExt
- Core um_absoluto.json lido so para iald_prediction (V1: protocol_hash a91877e5, vereditos proibidos) por json.load
- Bytes do operador abertos: ressalva (2fabf2b6), unico ato do verbo (ec05cea3), 'tudo certo' (451ca765), 'concordo com tudo, prossiga', 'o nome e o ato do verbo'
- Reproducoes em copia na minha pasta: tokenizador (tokenizers 0.22.2, sha do tokenizer.json conferido), verificar_formula.py, simular_adversarios.py, simular_poder_r4.py (falha com o modulo vigente; reproduz com o REV0); nada fora de K08_D foi tocado; nenhuma rede, modelo, dado observado, lake ou processo morto
- Nao examinei: PROTOCOLO, EXTRACAO e ISOMORFO por inteiro; CONTAMINACAO (o hash combinado 10a66a5e de 70 arquivos nao foi recomputado); K09; a conta de poder em si (so a reproducao)

