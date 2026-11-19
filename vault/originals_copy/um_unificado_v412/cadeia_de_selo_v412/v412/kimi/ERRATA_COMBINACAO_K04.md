# ERRATA AO LADO — COMBINACAO_K04

**Escopo.** Correções documentais aos dois achados da revisão. Nenhum vetor observado foi lido, nenhuma conta da seção D foi executada, \(N_\mathrm{indep}\) não foi calculado e nenhum teste foi realizado.

## Preservação

A versão anterior foi preservada, sem alterações, em:

- `K04\COMBINACAO\REV0\COMBINACAO_K04.md`;
- `K04\COMBINACAO\REV0\RESSALVAS_UMA_A_UMA_K04.md`;
- `K04\COMBINACAO\REV0\NOTAS_C_FONTES_E_DESENHO.md`;
- `K04\COMBINACAO\REV0\NOTAS_D_E_MAPA_E_PINOS.md`.

## E1 — D10 usa a taxa dos 10 sem hold, não a dos 14 elegíveis

**Onde estava o erro.** Em `COMBINACAO_K04.md`, C.5.4, e em `K04\COMBINACAO\NOTAS_C_FONTES_E_DESENHO.md`, a extrapolação temporal de D10 usava 9,6 elegíveis/ano e devolvia aproximadamente 19 meses.

**Correção.** A taxa de 9,6/ano pertence aos **14 elegíveis (D14)**. D10 contém **10 eventos sem hold**, cuja taxa retrospectiva bruta é **6,9/ano**. O tempo adicional de D10 é, portanto, **15,4874/6,9 ≈ 2,24 anos, aproximadamente 27 meses**.

**O que permanece.** D14 continua em aproximadamente **14,5 meses**. IR1 continua insuficiente; O5, 2029–2031, continua apenas como janela condicional, sem data interna defendida. Nenhuma taxa foi promovida a forecast oficial.

## E2 — Proveniência de R7-A e snapshot exigido para R7-B

**O que faltava.** R7-A nomeava os valores de \(z_\mathrm{local}\) e \(p_\mathrm{local}\) sem trazer o hash atual do arquivo que os contém.

**Correção.** Foi acrescentado, em `RESSALVAS_UMA_A_UMA_K04.md` e nas notas D–E:

- caminho: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json`;
- chave: `h0dn_bg1_v411.values.primario`;
- SHA-256 atual, lido por script: `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`.

Os valores continuam apenas citados da chave já selada; não foram recalculados.

**Futuro censo R7-B.** Passa a ser obrigatória uma consulta/exportação do Mapa acompanhada de **manifesto de snapshot**, contendo caminho, data, consulta realizada, SHA-256 do manifesto e SHA-256 do artefato exportado. Cada tentativa deve manter `rota_id`, seq, hipótese, dados, calibradores, fundo, sobreposição, covariância, data de conhecimento, cegueira e papel. Nenhum censo ou exportação foi criado nesta correção.

## Validação documental

- O hash acima foi obtido por leitura de bytes com `sha256sum`, sem executar código do core.
- Os dois arquivos de C foram corrigidos para separar explicitamente D10/6,9/ano de D14/9,6/ano.
- As referências anteriores a 19 meses e a D10 dividindo por 9,6 foram substituídas.
- A errata e a exigência de snapshot foram incorporadas aos documentos correspondentes.
- Nenhuma fórmula de R3/R4, R5 ou R7 foi avaliada; nenhum solver, estimador, abertura ou executor foi chamado.
