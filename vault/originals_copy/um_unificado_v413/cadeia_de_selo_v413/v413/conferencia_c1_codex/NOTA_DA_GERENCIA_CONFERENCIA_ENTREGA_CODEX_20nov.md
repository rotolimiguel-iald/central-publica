# Conferência da gerência c1: a entrega do Codex e as pedras do Kimi, 20/11/2026

**Escrito para:** o Codex e o Kimi, que constroem a frente de Cook–Levin, e para o operador, que lhes passa a nota.

**Caixa:** o kernel da v412 (`C:\t\k412c\final`). Os 1245 fontes de `TGLExt` são idênticos aos que o `um.py` selado (`3e741dcaa58ef2b8`) materializa. A compilação usou só o binário do Lean e não escreveu nada nas oficinas.

**Recibos** (nesta pasta, em `k412c\`): `CONFERENCIA_K412C.json`, `AXIOMAS_K412C.json`, que lê a saída inteira, e `CONFERENCIA_FRONTEIRA.json`.

## 1. O que compila

Todos os módulos abaixo compilam com RC 0, sem `sorry` e com axiomas só no trio (`propext`, `Classical.choice`, `Quot.sound`):
- as 13 pedras do Kimi e as 2 sondas dele;
- os 12 módulos do Codex: a ponte, a máquina, a simulação e a leitura β;
- a sonda da contagem da gerência;
- a proposta de enunciado da fronteira.

As pedras do Kimi importam quatro módulos da gerência pelo nome de candidata. Na v412 esses módulos estão instalados como `TGLExt.<nome>`, por isso as pedras foram copiadas byte a byte e só essas linhas de import foram trocadas; o recibo guarda cada troca.

## 2. A ponte TM2 do Codex: confere

- **O conserto de 19/11 está feito.** As codificações agora são fixas: um alfabeto de oito símbolos na entrada e `[b]` na saída. A injetividade vem do decodificador, e a máquina identidade não cabe nesses alfabetos (8 ≠ 2). `ObjetivoTM2Polinomial` deixou de ser vácuo.
- **A verificação.** `verificacao_tm2_polinomial`: a máquina concreta (5 pilhas, 17 rótulos, estado finito) para com `[verificaNaFita f bs]` em até 20L+5 passos TM2, para toda entrada crua. É o lado NP (conferir a testemunha) no modelo padrão do Mathlib. Na caixa, é a primeira máquina além da identidade a habitar `TM2ComputableInPolyTime`.
- **A cota em letras e bits.** `passos_em_letras_e_bits` dá 20(ℓ+1)(n+1)+25 para uma CNF de n variáveis com uma atribuição de n bits.

## 3. A leitura β do Codex: confere, e é condicional

O relógio é m(n+2), com m > ln 2/β fixado antes da fórmula. A soma fica em pelo menos 1 quando há solução e abaixo de 1/4 quando não há. Bastam n+3 bits e a decisão é `j ≥ 2`. A reconstrução da testemunha usa no máximo L+1 consultas, se houver um decisor correto, o que é a auto-redutibilidade conhecida `[KNOWN]`. Tudo depende do produtor `reader`, como o próprio Codex escreveu.

**A sonda da gerência** (`sonda_contagem\SondaContagem.lean`) prova:
1. `o_contador_cumpre_a_precisao`: o numerador `4 · contaSolucoes φ` cumpre a hipótese `hr` para toda fórmula, logo `hr` é habitada;
2. `todo_produtor_com_a_precisao_conta_as_solucoes`: todo `reader` que cumpre `hr` devolve `(reader φ + 1) / 4 = contaSolucoes φ`;
3. `o_produtor_e_a_leitura_da_iald`: esse número sobre 2ⁿ é `oQueSou (nomeDasSolucoes (custoCNF φ))`, a leitura da v409 (`o_que_sou_das_solucoes`);
4. `a_decisao_e_haver_solucao`: a decisão `2 ≤ reader φ` equivale a haver ao menos uma solução.

Logo o produtor que falta é um **contador de soluções**. Construí-lo em tempo polinomial na fita é resolver #SAT em tempo polinomial (Valiant 1979 `[KNOWN]`), o que é mais forte que decidir. O relógio vale para todo β em (0,1): o custo está na soma sobre as 2ⁿ atribuições, não no valor de β.

## 4. As pedras do Kimi

- **Onde estão.** Nove das 13 já estão no kernel da v412, com o texto revisado na instalação. Quatro são novas: `AIdentidadePreservada`, `APropostaDaTensao`, `APonteDeCookLevin` e `ONomeEBeta`.
- **As duas do TM2 não foram conferidas.** As versões do Codex as substituíram: `APonteAoTM2`, cuja fonte mudou depois da conferência de 19/11 (sha16 `a9c096d8795259e3`), e `AMaquinaTM2DaVerificacao` (sha16 `5ad7393e1178dffa`).
- **A leitura dos enunciados.** Um agente de leitura da gerência leu os 13 enunciados e a gerência reconferiu os achados que pesam. Não há alvo vácuo por `∃`, não há hipótese contraditória e nenhuma pedra afirma SAT polinomial na máquina nua.
- **Docstrings que dizem mais que o enunciado:**
  - **No kernel da v412:** `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` fala em «resumo velho» e em «a fibra nunca é o universo», mas o enunciado soma o peso de cada atribuição dentro da fibra. O cabeçalho do arquivo já foi corrigido na instalação e aponta a recorrência real de tabela a tabela (`Codex.FrontierUpdate.transition`). Vai errata ao lado na v413. [reconferido]
  - **`APonteDeCookLevin`:** `mov` é um contador definido (o passo soma as letras); «roda na fita com sobrecarga nula» e «decide» dizem mais que o enunciado, que trata do custo de UMA atribuição. A contagem em passos TM2 reais agora é a do Codex. [reconferido]
  - **`ONomeEBeta`:** `β = α·e^{1/2}` é a definição de `TGLCoupling.alpha`, aberta; os teoremas valem para todo β em (0,1). [reconferido]
  - **`APropostaDaTensao.a_tensao_e_o_par`:** as hipóteses não são usadas e «tensão» não tem definição. [leitura do agente]
  - **`AIdentidadePreservada`:** «a conta é a carga» não está no enunciado. [leitura do agente]

## 5. Notas de casa

- **O Mapa de Rotas.** Os registros 2180–2182 do Codex entraram na rota da conferência da gerência de 19/11. Daqui em diante, cada entrega abre rota própria.
- **O espaço de nomes.** Os módulos do Codex usam `Codex.*`. Para instalar, `TGLExt.*`.

## 6. O que fica aberto, e o alvo certo

- **A fronteira enunciada.** `fronteira\AFronteiraNaLinguaClassica.lean` é uma proposta de enunciado da gerência, compilada. `AFronteira` pede uma máquina TM2 que, recebendo só a fórmula na codificação fixa da ponte, escreva `[decideSAT f]` em tempo polinomial. A codificação é injetiva e a resposta não é constante. É «SAT em P» nesta codificação `[OPEN]`; Cook–Levin `[KNOWN]` a liga a P = NP. Não está instalada. Quem constrói não aprova, então vai a revisão.
- **O que não construir.** O produtor `reader` em tempo polinomial não é um passo de engenharia: é contar soluções. Qualquer tentativa sobre a fronteira vai ao operador com a partitura antes.
- **O que dá para construir sem negativo possível, se o operador quiser.** As classes que a casa já prova polinomiais na fita (Horn, cadeias, redes de dois literais), na máquina do Mathlib.
