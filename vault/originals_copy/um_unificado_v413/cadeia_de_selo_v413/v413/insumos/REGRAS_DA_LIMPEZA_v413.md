# Regras da limpeza dos textos das pedras novas da v413

Fonte de cada módulo: `insumos\origem\TGLExt\X.lean`. Saída: `insumos\pedras_limpas\TGLExt\X.lean` (mesmo nome).
Fundamento: o método do operador de 17/11/2026 (memória central, `C:\IALD\CLAUDE.md`, bloco «O `um.py` é a compilação
do que é verdade»): no `um.py` e no kernel que ele carrega entra só o que é verdade (o enunciado, a prova, o estatuto,
os limites e a fonte conhecida); a história da conversa fica no registro paralelo.

## 1. O código não se toca

Tudo o que está fora de comentários (`/- -/`, `/-- -/`, `/-! -/`, `--`) fica byte a byte igual: imports, `set_option`,
`namespace`, `open`, `variable`, definições, enunciados, provas, `#print axioms`. Não renomear nada, não reformatar
código, não acrescentar nem tirar `#print`. A conferência compara o código sem comentários; qualquer diferença reprova.

## 2. O que sai dos textos (a história)

- quem construiu, disse, pediu, revisou ou aprovou: Codex, Kimi, gerência, operador, autor, revisor, orquestrador,
  quando aparecem como agentes («o Codex prova», «a gerência escreveu», «leitura do operador»);
- datas (20/11/2026 e afins), números de revisão (R0 a R8, «a R7 corrige»), referências a arquivos de fala e os seus
  sha16, a pareceres, a pastas de `work\`;
- palavras de processo: candidata, provisório, proposta, não instalada, não se instala, conferido, aprovado, ressalva,
  errata, emenda, pedido, ordem, entrega, sonda de conferência, «quem constrói não aprova».

## 3. O que fica

- o que cada definição e cada teorema diz, com exatidão;
- os estatutos: `[REAL]`, `[DERIVED]`, `[KNOWN]`, `[OPEN]`, `[ONTO]`, `[INPUT]`, `[POSTO]`;
- os limites (as seções «O que não prova» e afins);
- as citações da literatura, com autor e ano;
- os nomes de teoremas e definições do kernel entre crases (um nome com prefixo `Codex.` ou `TGLExt.` entre crases é
  identificador Lean, não autoria: fica);
- o conteúdo de uma leitura que entra como definição, marcado `[ONTO]` ou `[INPUT/ONTO]`, sem dizer de quem é.
  Sem aspas « » (são reservadas à fala verificada do operador e não entram no kernel).

## 4. Nada novo

Não acrescentar afirmação. Se tirar a história deixar uma frase manca, reescrever o mínimo, sem fortalecer nada. Na
dúvida, cortar em vez de inventar. Todo nome citado no texto tem de existir. Português do Brasil na prosa; os
identificadores ficam como estão. Manter o estilo (cabeçalhos `/-! # … -/`, as estrelas ★).

## 5. Correções de conteúdo por módulo (das revisões; aplicar no texto)

- **APonteDeCookLevin.** O contador `mov` é custo abstrato cobrado por definição (literais mais terminadores, cláusula
  a cláusula), não contagem demonstrada de movimentos de uma máquina de fita: tirar «movimentos exatos», «sobrecarga
  nula» e afins. `a_decisao_na_fita_e_a_mesma` verifica o custo de UMA atribuição dada (`reg = custoCNF φ x`; aceita se
  `reg = 0`), não decide se a fórmula tem solução. O polinômio: o enunciado é «para cada φ e x existe c», e a prova usa
  c = 1 para todos. A máquina padrão do Mathlib que confere a testemunha é outro módulo (`TGLExt.APonteAoTM2`,
  `TGLExt.SimTM2.verificacao_tm2_polinomial`).
- **APropostaDaTensao.** No teorema do par, as hipóteses `_hA` e `_hB` não são usadas: o lema é consequência da
  satisfatibilidade conjunta (`h : SAT (A ++ B)`), e não diz que compatibilidade local garante a global. O iff não
  computa a escolha do valor do Nome e não dá cota de busca nem elimina a enumeração.
- **ONomeEBeta.** α aqui é `TGLCoupling.alpha` = β/e^{1/2}, por definição; a identidade β = α·e^{1/2} não determina α
  nem β numericamente (nem o CODATA) e vale para todo β em (0, 1). «Anterior» (fixado antes de toda fórmula) é leitura da
  parametrização, não conteúdo provado. k conta expoentes do decaimento no critério «SAT ⟺ 1 ≤ a soma sobre as 2^n
  atribuições»; não é passo de máquina de Turing, e o módulo não produz essa soma. Se um nome de teorema diz mais do que o
  enunciado (por exemplo «beta vezes radical», quando a igualdade é β = α·e^{1/2}), a docstring diz o enunciado exato.
- **AIdentidadePreservada.** A conjunção final traz só a preservação das coordenadas de custo zero e a convergência
  (`Tendsto`); o limiar n·ln 2 está num teorema separado: a docstring não pode dizer que a conjunção inclui a carga. Não
  chamar s de número de movimentos de fita. O objeto preservado é um vetor em `EuclideanSpace` sobre as atribuições (as
  coordenadas de custo zero), não uma configuração de máquina de Turing.
- **Trinity.** As leituras e o nome entram pelo conteúdo, marcados `[ONTO]`, sem autoria; as citações (Nernst 1912,
  Landauer 1961, Bennett 1973, Haken 1985, Aaronson 2005) ficam com o estatuto que já têm.
- **SondaContagem** e **AFronteiraNaLinguaClassica.** Tirar «sonda da gerência», «não é candidata», «não se instala»,
  «proposta de enunciado … quem constrói não aprova», «ponte do Codex», «entrega»: dizer o que o módulo prova e cita.

## 6. Conferência (rodar depois de escrever)

`C:\Python314\python.exe -X utf8 "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\verificar_historia_nas_pedras.py" "C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt" --contra "C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt" --detalhe`

Para cada módulo seu: «codigo IDENTICO» é obrigatório. As linhas que ainda tiverem marca devem ser só código ou
identificador (por exemplo `open Codex.LeituraBeta`) ou palavra em sentido matemático; diga quais são. Rodar o
verificador com arquivo de script e `< /dev/null` (nunca `python -c`). Não compilar (a gerência compila o conjunto).
Não tocar em `origem\` nem em módulo de outro agente.
