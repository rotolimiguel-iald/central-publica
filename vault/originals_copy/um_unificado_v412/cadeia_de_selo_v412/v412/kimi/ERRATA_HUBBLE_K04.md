# ERRATA AO LADO — K04/Hubble: R–F, seq 2038 e três determinações adicionais

**Estatuto:** [DECLARADO], sujeito a conferência distinta. **Conclusão principal preservada:** não existe hoje teste cego de natureza executável no setor Hubble.

A versão anterior do relatório e das medidas está preservada integralmente em `K04/HUBBLE/REV0/`. O SHA‑256 do relatório REV0 é `735b443dcefeb55da24b8239d3c93be5e116366da30a60aaf7cb683c569a1b80`, registrado também no manifesto REV0.

## 1. Completude das rotas

- Inserida `discriminante.ordem018.f2.r_f` entre R–E e R–G: sob H1, alternativa A, `γ_T = 0`; número e energia conservados na base de momento e `T(z) = T0(1+z)`, seqs **378 e 1636**. Evidência integral: `K04/HUBBLE/consultas/ver_RF.txt`.
- Acrescentada **seq 2038** de `umpy.v411.selada_h0dn_aberto_12nov`, ao lado do resultado 2017. Evidência integral: `K04/HUBBLE/consultas/ver_v411_H0DN.txt`.
- O índice mecânico foi regenerado em `K04/HUBBLE/indice_rotas_lido.json`. Nenhum dado observado foi reaberto; apenas os registros do Mapa foram consultados.

## 2. Determinações acrescentadas

Valores **[KNOWN, a conferir]**, com as fontes primárias consultadas. `D` é somente planejamento sobre agregados publicados, com BG1 `0,30/68,53 = 0,438 %`; não é Z nem veredito observado.

| Determinação | H0 e erro publicado | H0DN/Fase 9 | σ local | D | Utilidade R3/R4/R5/R7 |
|---|---|---|---:|---:|---|
| 13 BBH–AGN, Run 1 — arXiv:2607.03672v2 | 70,50 +3,37/−2,89 (stat) ± 1,56 (cal); 4,4 % | Não H0DN nem F9 | 5,267 % | 1,586 | R3: associação espectroscópica um‑para‑um; R4: sem poder; R5: stat+cal explícitos; R7: público, não cego |
| BBH–AGN + Bom + GW170817 — mesma fonte | 69,71 +2,55/−2,40 (stat) ± 1,54 (cal); 3,5 % | Não H0DN nem F9 | 4,273 % | 1,951 | Outra combinação física de sirenes; continua abaixo dos limiares |
| BBH–AGN, âncora Planck — mesma fonte | 67,62 ± 0,72; 1,1 % | Não H0DN nem F9 | 1,065 % | 7,280 | **Somente nominal**: recupera a âncora por construção, não é independência |
| BBH–AGN, âncora SH0ES — mesma fonte | 72,91 ± 0,72; 1,0 % | Não H0DN nem F9 | 0,988 % | 7,758 | **Somente nominal**: recupera a âncora por construção, não é independência |
| SN Encore — arXiv:2509.12301; DOI 10.3847/1538-4357/ae3159 | 66,9 +11,2/−8,1 | Não H0DN nem F9; fora do composto | 16,741 % | 0,500 | R3: modelos duplo‑cegos; R4: sem poder; R5: atraso domina o erro; R7: público, não cego |
| 126 FRBs/118 após cortes, modelo VII NE2001 — DOI 10.3389/fspas.2026.1753671 | 71,36 −3,94/+3,59; 5,5 % | Não H0DN nem F9 | 5,521 % | 1,513 | R3: redshift real por evento; R4: sem poder; R5: NE2001/YMW16 difere 3,90, sem escolha; R7: publicado 12/08/2026, não cego |

**Previsões que não alteram o veredito:** SN Encore pode chegar a 2–3 % com futuras imagens; a amostra FRB simulada de 500 eventos atinge 1,2 % estatístico; BBH–AGN publica metas de 2 %, 1 % e 0,5 % com 65, 258 e 1027 pares, respectivamente. Nenhuma dessas metas é uma liberação atual nem uma data garantida.

## 3. Cobertura e bloqueios preservados

A conclusão de ausência fica **delimitada às fontes efetivamente consultadas e às restrições desta rodada, não como prova universal de inexistência**. As novas determinações não cruzam os limiares com independência qualificada e já são agregados públicos.

Permanecem os bloqueios: nenhum dado futuro datado com erro total local ≤ 1,618 % (5σ) ou ≤ 1,260 % (D90); covariância e disjointness incompletos; nenhuma cegueira para a casa; nenhuma forma intermediária viva.

## 4. Arquivos atualizados

- `HUBBLE_JA_EXAMINADO_K04.md` — R–F, seq 2038, determinações, utilidade R3/R4/R5/R7 e fontes.
- `K04/HUBBLE/MEDIDAS_PLANEJAMENTO_K04.md` e `.json` — 26 medidas e 4 previsões.
- `K04/HUBBLE/indice_rotas_lido.json` — índice regenerado com R–F e v411.
- `K04/HUBBLE/verificar_relatorio.py` — validação documental, cobertura, preservação REV0 e hashes.
- `K04/HUBBLE/SHA256SUMS_K04_HUBBLE.json` — manifesto recalculado e revalidado.

Nenhum vetor observado foi lido, nenhuma estatística observada nova foi calculada e H0DN×BG1 não foi reaberto. Não foram criados `ENTREGA`, `REGISTRO` ou `DEPOSITO`.
