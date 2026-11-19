# K06 — extratores determinísticos, bateria sintética e teto de A8

## Escopo

[DECLARADO] Este diretório implementa somente a seção C/extratores. Não executa nem chama modelo de linguagem, não abre resultado experimental, não usa juiz humano/LLM e não contém texto de entrada reservado ou prompts reservados. Todos os textos da bateria foram criados sinteticamente para este teste.

[DECLARADO] O instrumento é um **extrator de gramática estruturada**, não um interpretador de prosa livre. A R3 só pode usá-lo se o formato `K06R1|ID|SUBJECT|RELATION|OBJECT|STATUS` for exigido e a porta de superfície estrita for preservada.

[DECLARADO] C1–C4 são **LEGADOS, fora dos braços V2**: permanecem apenas como regressão sintética de equivalência do motor. Os aliases de registro são `H-TIME-HOMOG → H-HOM` e `H-LUMP → H-QUOT(k)`. Qualquer exemplo `p=4,r=6` é legado da R2 e não descreve a R3 atual.

[REAL] A versão anterior à correção de T01 está preservada em `REV0/`; a correção e a revalidação são documentadas em `ERRATA_EXTRAORES_T01.md`.

## Arquivos

- `especificacao.json`: 24 asserções e `τ_j` por extenso para T, C1, C2, C3 e C4.
- `extratores.py`: motor único, interfaces `E_j`/`E_TGL`, distâncias, A8 e hashes de duplicação.
- `gerar_casos.py`: fonte determinística da bateria; não importa o extrator.
- `casos/casos.json`: casos, metadados sintéticos, textos e vetores de gabarito.
- `casos/agregacao.json`: testes exatos de lumpability.
- `casos/duplicacao.json`: duplicação exata, de layout e entre leituras de A8.
- `validar.py`: validação, taxas, equivalência, teto, relatório e manifesto.
- `resultados.json`: resultado completo gerado pelo validador.
- `RELATORIO_EXTRAORES.md`: relatório legível gerado pelo validador.
- `manifesto.json`: SHA-256 e tamanhos dos insumos congelados.

## Reprodução sem instalação

No Windows, neste diretório, usando Python 3.10 ou superior da biblioteca padrão:

```bat
python -B -X utf8 gerar_casos.py
python -B -X utf8 validar.py
```

A segunda linha basta para validar os casos já materializados. A primeira só deve ser usada para auditar a reprodução byte a byte; qualquer mudança de gabarito exige nova revisão e novo manifesto.

Para aplicar um extrator a um arquivo sintético próprio:

```bat
python -B -X utf8 extratores.py caminho\arquivo.txt --arm T
python -B -X utf8 extratores.py caminho\arquivo.txt --cross-tgl
```

## Regras congeladas do extrator

1. Cada braço tem exatamente 24 asserções e `τ_j=(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`.
2. Uma asserção vale 1 somente quando sua tupla completa e congelada ocorre uma única vez após colapsar duplicatas idênticas.
3. Duplicatas conflitantes zeram apenas a asserção afetada; o extrator nunca escolhe uma das versões.
4. Prosa não estruturada invalida a superfície inteira; registros truncados perdem a asserção afetada.
5. Registros de outro braço não contam no extrator próprio; `E_TGL` é exatamente o mesmo código e a mesma especificação de `E_T`.
6. Em C4, vazio não é abstenção satisfeita: cada uma das 24 abstenções precisa ser explícita com `NO_CORPUS`.
7. A8 usa o predicado R2 original e, por consequência, exige o bloco perfeito das leituras 5–8: 24 × 4 = 96 células.
8. Duplicação entre leituras é uma porta de integridade separada do valor aritmético de A8.

## Decisão de uso

O relatório distingue `BATERIA_OBSERVADA` de `PRODUCAO`. Zero erro observado não prova, por si só, `e<0,12%`: o limite superior unilateral de 95% e a cobertura de texto livre são exibidos. Enquanto a certificação não atingir todos os requisitos, o estado é **BLOQUEADO_PARA_PRODUCAO**.
