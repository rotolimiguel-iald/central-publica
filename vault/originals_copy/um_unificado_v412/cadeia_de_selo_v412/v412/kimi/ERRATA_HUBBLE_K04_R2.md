# ERRATA AO LADO R2 — K04/Hubble: duas reservas editoriais

**Estatuto:** [DECLARADO], sujeito a conferência distinta. **Conclusão principal preservada:** não existe hoje teste cego de natureza executável no setor Hubble.

**Natureza da revisão:** correção exclusivamente editorial e de consistência interna. Nenhuma fonte foi acrescentada, substituída ou alterada; nenhuma ciência foi reaberta.

A versão imediatamente anterior está preservada em `K04/HUBBLE/REV1/`, incluindo relatório, errata anterior, medidas, manifesto e validador. O SHA‑256 do relatório REV1 é `81da156a399d86617abaff5f9bf00780e93307a0ee9b2613ad7c1fece9686d2c`. A versão REV0 permanece preservada.

## 1. Distâncias nominais e linhas independentes

- Na §4, a frase sobre os casos acima de 5 passa a nomear **pseudo‑FRB e âncoras BBH–AGN, apenas nominais**. O pseudo‑FRB tem `D = 7,754` e não é qualificado; as âncoras BBH–AGN Planck/SH0ES têm `D = 7,280/7,758`, mas recuperam suas âncoras por construção e não são independentes.
- Na §5, “maior distância” passa a ser **“maior distância entre linhas independentes qualificadas”**, mantendo SN II tailored EPM com `D = 3,256`, ainda abaixo de 5 e de D90.

## 2. Compostos novos na §2

A tabela de compostos novos passa a reproduzir, em coerência com as §§3–4:

- **13 BBH–AGN e extensões:** agregados públicos e não cegos para a casa; Run 1 e estendido com `D = 1,586/1,951`; variantes ancoradas apenas nominais e não independentes.
- **SN Encore:** agregado público e não cego para a casa, fora do composto anterior, com `D = 0,500`; o duplo cegamento da colaboração não devolve cegueira à casa.
- **126 FRBs/118:** agregado público e não cego para a casa, com `D = 1,513`; NE2001/YMW16 permanece sem escolha, e 500 eventos simulados são previsão, não medida atual.

## 3. Escopo, arquivos e validação

- Atualizados `HUBBLE_JA_EXAMINADO_K04.md`, esta errata, `K04/HUBBLE/verificar_relatorio.py` e `K04/HUBBLE/SHA256SUMS_K04_HUBBLE.json`.
- As 26 medidas e 4 previsões permanecem inalteradas; não foi necessário modificar `MEDIDAS_PLANEJAMENTO_K04.md` ou `.json`.
- A validação é somente documental: consistência do relatório com as medidas, presença das correções, preservação de REV0/REV1 e recálculo dos hashes.
- Nenhum vetor observado foi lido, nenhuma estatística observada nova foi calculada e H0DN×BG1 não foi reaberto. Não foram criados `ENTREGA`, `REGISTRO` ou `DEPOSITO`.

A ausência declarada continua delimitada às fontes efetivamente consultadas e às restrições da rodada, não como prova universal de inexistência. Permanecem os bloqueios de covariância, disjointness, cegueira para a casa e primeira data futura.
