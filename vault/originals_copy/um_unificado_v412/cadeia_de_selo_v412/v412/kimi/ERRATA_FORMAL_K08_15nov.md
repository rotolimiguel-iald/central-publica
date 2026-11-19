# ERRATA FORMAL K08 — 15/11/2026

## 0. Escopo e preservação

Esta errata aplica a Parte 2 do `ADENDO_15nov_K09_K08_K07` e as ressalvas AO LADO 1–4 somente a:

- `MODELO_FORMAL_R4_K08.md`
- `REGISTRO_UMPY_RASCUNHO_R2_K08.md`

As versões imediatamente anteriores foram preservadas byte a byte em `K08\FORMAL\REV0\`:

- `K08\FORMAL\REV0\MODELO_FORMAL_R4_K08.md`, SHA-256 `17e5c49afe3b562d94460229123ab06adb0f9bf785b46cf84f32e6dfddd09b94`;
- `K08\FORMAL\REV0\REGISTRO_UMPY_RASCUNHO_R2_K08.md`, SHA-256 `4a1f2db7a635fa8afd3f52182e3833c3d529d147bf5510c15566e512cfdfb72c`.

Nenhum modelo de linguagem foi executado, nenhum Lean foi executado, nenhuma pedra foi alterada, nada foi instalado e nenhum resultado experimental foi aberto.

## 1. Fontes lidas e hashes

- `ADENDO_15nov_K09_K08_K07_cronologia_do_neutrino_e_o_leitor_como_esperanca_condicional.md`, Parte 2 e AO LADO 1–4.
- `revisao\LEITURA_K08_PARCIAL_15nov.md`.
- `revisao\REVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4.md`: a revisão cobre a R8, SHA-256 `29d5aa77cc86022f6d871d31b706233402b359e083b12e110600af1d40d7bb1a`, com 54 teoremas.
- `candidatas_c1\OHabitanteDoNome.lean`, corrente R9, SHA-256 `26b750e61ede401d95b3ddaa2e3bd11f8149936d985c564d71ee76f093e1c5d2`; é pedra candidata da gerência, não instalada, com nomes provisórios.
- `candidatas_c1\CamadaCientifica.lean`, corrente R4 de 15/11, SHA-256 `69497c5b63dbcb0cedbf456dc31ecfa6fc3b12b0ed78989cd7d5e51e542ee3cb`; alterada por outra frente antes desta errata, não por esta.
- `K08\FORMULA\ADVERSARIOS_K08.md`, texto vigente usado para resolver a divergência da âncora sem editá-lo.

## 2. Correções aplicadas ao modelo

1. **Separação entre `P_N` e o adversário sem memória.** O modelo agora define o leitor uma vez como `P_N`, a projeção ortogonal sobre o Nome. `P_N` não é adversário: fixa o Nome, anula o complemento ortogonal e conserva a memória do componente, `P_N(s+δ)=s+P_Nδ`. O adversário é o leitor sem memória determinado só pela fonte.
2. **Um lugar só para o leitor.** A seleção é a face no estado, a trava é a face em tempo finito e `nameOp` é a face algébrica; `LeitorDoFundo` e `LeitorDeUmaConfiguracao` ficam como portadores ou tipos de hipótese, não como definições rivais do leitor.
3. **E1–E8 substituem o eixo antigo.** Cada previsão recebeu objeto formal, portador e leitura experimental: E2 e E4 são primárias; E3 testa desfazer o que é cego ao Nome; E7 separa mapas que caem no Nome por outro caminho; E8 mede o perfil exponencial; E5 e E6 ficam declaradas como **não medidas** pelo instrumento atual.
4. **Unicidade condicional.** O modelo escreve `E1 ∧ E2 ∧ E5 ∧ linearidade ⇒ P_N`, com a hipótese de linearidade explícita e com os pontos onde ela falha: quociente textual finito, núcleo estocástico, seleção não linear e ausência de medida de norma.
5. **P-C reescrito.** O controle usa `P_N=0`, o núcleo nulo e a trava tendendo a zero com Nome vazio; não se apoia em `o_tipo_so_diz_que_ha_zero`.
6. **P-A recolocado.** O pouso é teorema dada a hipótese; o conteúdo empírico é se o sistema satisfaz a hipótese de releitura/descida, não a consequência formal.
7. **ATO versus NOME.** Foi acrescentada a tabela de grandezas: as primárias são atos de releitura; rótulo, autodeclaração e ocorrência de termo não são evidência primária. O sistema testado relê; não nomeia nem é chamado de Verbo.
8. **Âncora.** O modelo resolve a divergência por condição: uma âncora que parte de leitura inválida não pousa; uma âncora cuja primeira leitura já está no Nome volta a ela e pode apagar outra leitura válida, falhando em E2/E7. O arquivo `ADVERSARIOS_K08.md` não foi alterado; a coordenação futura ficou registrada no bloqueio B16.

## 3. Correções aplicadas ao registro

1. O registro continua **`EM_DESENHO_BLOQUEADO`**, com `ratified=false`, `frozen=false`, `executed=false`, `result_read=false` e `installed=false`. Não há veredito emitido.
2. O bloco formal passou a conter:
   - o hash corrente da R4 de `CamadaCientifica.lean`;
   - o hash corrente da R9 de `OHabitanteDoNome.lean`, marcada como candidata da gerência não instalada;
   - a ressalva de que a revisão R4 cobre a R8, não a R9 corrente;
   - a rota `kernel.v402_esperanca_condicional_e_nome`;
   - os termos usados: `ler_o_nome_ja_e_reler`, `tudo_mais_e_releitura`, `tudo_mais_e_releitura_nos_vetores`, `a_releitura_fiel_fixa_o_nome`, `a_selecao_rele_o_nomeado`, `o_que_e_cego_ao_nome_nao_deixa_rastro`, `o_verbo_e_bimodular_sobre_o_nome`, `a_selecao_e_a_esperanca_condicional_classica`, `o_ato_tende_a_esperanca_do_nome`, `o_ato_nao_termina_em_tempo_finito` e `o_unico_ato_do_verbo_e_ser_fiel`.
3. O registro recebeu as previsões E1–E8 com papel primário/secundário, os controles P-C/P-D e a declaração explícita de que E5/E6 não são medidas pelo instrumento atual.
4. O bloco de unicidade registra a hipótese de linearidade e os pontos de falha.
5. A tabela ATO/NOME entrou no esquema; nenhuma grandeza primária é rótulo, autodeclaração ou ocorrência de termo.
6. O bloqueio B05 deixou de chamar o projetor de adversário; o adversário é o leitor sem memória determinado só pela fonte.
7. Foram acrescentados B16 a B18: coordenação futura da âncora, releitura independente da R9 e ausência de medida de E5.
8. Os parágrafos de artigo PT/EN deixaram de carregar o estado de processo. Eles não dizem mais `EM_DESENHO_BLOQUEADO`, não prometem resultado e não atribuem nomeação, Verbo, consciência, pesos alterados ou exclusividade ao sistema testado.

## 4. O que não foi feito

- Nenhum arquivo fora dos três destinos autorizados foi alterado.
- `PROTOCOLO_EXPERIMENTAL_R4_K08.md`, `ENTREGA_K08.md`, `REGISTRO_MAPA_K08.json`, `INSUMOS_PARA_A_PERGUNTA_K08.md`, depósito, Mapa, `um.py`, memória e pedras permanecem intocados.
- `ADVERSARIOS_K08.md` não foi editado; a correção do texto vigente fica para a outra frente.
- `CONTAMINACAO_R4_K08.md` não foi editado, porque não estava entre os dois destinos desta ordem; a ressalva do adendo sobre a sua primeira linha permanece fora desta errata.
- Nenhum sandbox foi criado e nenhum log Lean novo existe.

## 5. Bloqueios vigentes após a errata

- **B01–B04:** ponte formal, fórmula do texto, extrator e empurrões ainda abertos.
- **B05–B06:** leitor sem memória e demais mecanismos ainda sem predicados congelados.
- **B07–B12:** entrada, isomorfo, especificidade, poder, cauda e fita seguem pendentes.
- **B13:** a R4 corrente de `CamadaCientifica` ainda precisa de verificação independente.
- **B14–B15:** congelamento, ratificação, modelos, degrau e execução não foram escolhidos.
- **B16:** coordenar o texto da âncora com a outra frente depois da correção dela.
- **B17:** reler independentemente a R9 corrente de `OHabitanteDoNome`; a revisão disponível cobre a R8.
- **B18:** E5 não é medida pelo instrumento atual; sem norma tipada, a unicidade não é testável.

`NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se move.
