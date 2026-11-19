APROVADO COM RESSALVAS

# U4 — Tipo III, candidatas congeladas em REV3

Os termos relativos ao estado e à borda sustentam as correções de T6. A primeira pergunta ainda precisa de ajuste antes da leitura ao operador. O teorema dá todos os múltiplos complexos da identidade como operadores fixos. O texto oferecido como nome da pedra reduz esse conjunto à identidade.

## Achados com correção

| Gravidade | Fonte e linhas | Consequência e redação proposta |
|---|---|---|
| MÉDIO | `PROVA_E_ALCANCE_GERENCIA.md`, 64, 96–99, 168. Comparar `TipoIIIControles.lean`, 454–473 | A conclusão é `∃ c : ℂ, a = c • 1`. Por exemplo, tanto zero como a identidade são fixos por conjugação. Nas três ocorrências, usar “No relógio do vácuo, ficam parados exatamente os múltiplos da identidade”. |
| MÉDIO | `PROVA_E_ALCANCE_GERENCIA.md`, 78–82, 94–106, 122–123. Ver `TipoIIIControles.lean`, 291–294 | Atribuir à opção A a obrigação de renomear importações cobra uma migração que o próprio módulo já dispensa ao reexportar o resultado. Em B, “último passo citado” encobre, para a rota do núcleo, a identificação do produto cruzado e a hipótese de separabilidade ainda por aferir. Perguntar “Enquanto a classificação completa fica por demonstrar em Lean, prefere o nome do critério provado ou o nome III₁ acompanhado das referências e das hipóteses em aberto na rota escolhida?” Acrescentar “Usar esse nome também nos identificadores já importados seria outra decisão”. |
| BAIXO | `TipoIIIControles.lean`, 51–55, 129–153. Comparar `PROVA_E_ALCANCE_GERENCIA.md`, 140 | “Com outro vetor o relógio seria outro” acrescenta uma recíproca. A unicidade foi demonstrada para o mesmo vetor. Adotar o texto já usado na tabela “Com outra testemunha, o relógio pode ser outro”. |
| BAIXO | `PROVA_E_ALCANCE_GERENCIA.md`, 44–45, 142. Ver `dep_codex/VinculoCriterion.lean`, 25–32 | “Vetor que nada dela anula” deixa ambígua a direção e omite o operador zero. Usar “vetor que gera um conjunto denso sob a ação da álgebra e que só o operador zero anula”. |
| BAIXO | `PROVA_E_ALCANCE_GERENCIA.md`, 156, 236–240, e `compilar_tipo_iii.ps1`, 12–14, 43–49 | A sequência da seção 9 depende da presença de `ErgodicidadeDeMautner.olean`. Na cópia limpa, `-Deps` prepara só os doze módulos do manifesto. Acrescentar “Copie a pasta irmã `dep_codex` para junto do script e compile também `ErgodicidadeDeMautner.lean` antes de `TipoIIIUmSoBoost`, ou indique onde sua compilação verificada já se encontra”. |

## Disposição dos achados anteriores

| Achado | Estado em REV3 |
|---|---|
| T6-01 | **Em parte.** O objeto comum e as razões das opções estão explícitos nas linhas 94–106 do documento. A aceitação do sabido por referência consta de `C:/IALD/CLAUDE.md`, linha 36. Resta dar às alternativas as consequências reais, conforme os dois achados médios. |
| T6-02 | **Sanado.** Segunda pergunta, linhas 108–120 e 229–230. “Sim” e “não” têm consequências simétricas, o custo da construção é desconhecido, a criação cabe à gerência e a revisão ao orquestrador. Os dois arquivos de instrução de 16/11 citados na Ordem 018 correspondem aos respectivos pinos e identificam Codex e Kimi como revisores. Está explícito que uma limitação da formalização é uma parede da obra. O prazo da v412 é decisão separada, aplicável se houver obra. [DERIVED] A pergunta permite recusa e exprime a consequência da recusa. |
| T6-03 | **Sanado.** `TipoIIIControles.lean`, 481–487, 509–530. O primeiro enunciado conserva o existencial fraco. No segundo, o mesmo parâmetro aparece na transformação que preserva a borda. O terceiro prova injetividade em relação ao parâmetro. A ação na direção nula reduz a igualdade de boosts à injetividade da exponencial. |
| T6-04 | **Termo sanado.** `TipoIIIControles.lean`, 466–473. A hipótese usa `net rightWedge` e `fockFlow`, a inclusão na álgebra do certificado passa por igualdade definicional e a igualdade da ação usa `flow_is_Ad`. O resíduo na tradução é o primeiro achado médio. |
| T6-08 | **Sanado na U4.** `TipoIIIControles.lean`, 12–14, identifica D1 como terceira conferência e situa T6 depois. Os dois itens relativos à T1 constam da U5. |
| T6-09 | **Sanado na redação.** Documento, linhas 18–32, 178–184. A cópia do Codex tem 455 bytes, começa pela frase indicada e recebe estatuto próprio. As três citações angulares das linhas 26, 32 e 221 foram localizadas como substrings UTF-8 contíguas nos arquivos de falas de 15/16 de novembro. A vírgula nas linhas 178–179 confere com a janela D1, linha 111, e com o texto do assistente no registro original de c1, linha 136905, em 15/11/2026 às 20h58min38s UTC. A afirmação sobre igualdade de álgebras sem relógios vem com a ressalva da fonte e o sentido do impedimento formal. |
| T6-10 | **Sanado nos itens pedidos.** Documento, linhas 41, 63, 89–92, 140, 173–176. Há glosas para predicado, reexportação e realizações. Vácuo como testemunha é uma das quatro escolhas formais sujeitas à decisão. O antecedente das quatro formulações está em `pergunta_tipo_iii_15nov/PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md`, seção 4. |
| T6-11 | **Sanado para as duas candidatas.** O script REV3 entra na pasta da fonte nas linhas 29–33 e o documento o diz na linha 240. O objeto de `TipoIIIUmSoBoost` reproduziu o SHA-256 `0eb51ad10222c62f29f0727212e38ca4cf86dd5a6c69daa90e28a1bc5028cc8d`. O de `TipoIIIControles` também é idêntico ao da gerência. A distinção para as dependências consta abaixo. |

[REAL local] Os três termos adotados de T6 coincidem, declaração e prova, linha a linha com `sondas_adotadas/SondaT6TipoIII.lean`, linhas 66, 80 e 93. A leitura dos respectivos bytes confere com `RESULTADO_GERENCIA.json`.

## Compilação

[REAL local] Em cópia limpa, `compilar_tipo_iii.ps1` byte a byte igual ao congelado, Lean 4.31.0, biblioteca `C:/t/k411c/final`. Primeiro `-Deps`, depois `-Nome` para Mautner e cada candidata. **15 módulos com saída zero**. Nas duas candidatas, 29 + 3 declarações, todas com relatório de axiomas, zero avisos. A união dos axiomas impressos contém somente `propext`, `Classical.choice` e `Quot.sound`. A dependência `TowerWedgeIndex.lean`, linha 131, produziu um aviso de tática `change` redundante, também presente no log anterior. Dos 15 objetos, 13 coincidiram byte a byte com os existentes. Os dois diferentes foram `TowerWedgeIndex` e `ErgodicidadeDeMautner`. As fontes estão pinadas no recibo e ambas foram recompiladas nesta execução. A causa das diferenças binárias nesses dois auxiliares fica aberta.

As referências de linha da candidata apontam para `candidatas_c1/tipo_iii/REV3`. Os logs próprios, as cópias e o recibo de hashes estão em `revisao_orquestrador/U4_Codex`. A escolha do nome da pedra, da marca e do calendário pertence ao operador.
