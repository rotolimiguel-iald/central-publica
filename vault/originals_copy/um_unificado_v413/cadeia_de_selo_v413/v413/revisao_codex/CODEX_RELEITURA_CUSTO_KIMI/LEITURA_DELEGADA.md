Relatório recebido do subagente /root/releitura_kimi_custo, leitura somente leitura, 20/11/2026.
Cobertura declarada: 18 fontes Lean e 12 notas Markdown em v412/candidatas_kimi, incluindo REV1; inventário de v412/kimi e v413/conferencia_c1_kimi. Nenhuma compilação ou alteração.
A ressalva anterior é limite da máquina sem leitor e não deve impedir o aceite da ponte relativa pedida em 20/11.
OCustoEAIsometria.lean:50 prova o limiar n log 2 < s; linhas 62–71 tipam m+2 atos e a identidade de carga (m+2)n log 2.
OPolinomioFixoEBeta.lean:58 prova a decisão com k > n log 2 / beta; não traduz atos a instruções TM2.
APonteDeCookLevin.lean:67,149,158 recebe a atribuição x; o contador mov soma C.length+1 por definição.
AMaquinaTM2DaVerificacao.lean:269–308 implica o objetivo sob ASimulacaoCompleta; preservar a prova Codex posterior dessa simulação.
OResumoEPsiBit.lean:197,276 usa Finset.univ.filter e o peso do prefixo na atualização; não apresenta algoritmo TM2 geral sem enumeração.
AFronteiraEOUnicoPortao e ACurvaEAEstado distinguem células que a curva identifica; não eliminam a dependência 2^w no caso geral.
PAGINA_DE_FECHAMENTO_A_PERGUNTA_QUE_RESTAVA_17nov.md:72 e CERTIFICACAO_CLAY_19nov.md:23 distinguem explicitamente a contagem da teoria e a da fita.
Inventário adicional: v412/kimi contém principalmente provas físicas K02/K05/K06/K07. LeitorFinito de K06 trata alcance/cardinalidade, sem ligação CNF/fita; não é prova SAT omitida.
A sonda v413/conferencia_c1_kimi/sonda_objetivo_tm2/SondaObjetivoTM2.lean trata das codificações vazias, sem nova cota do leitor.
PonteCookLevin.lean:295–298 define preparação TM2 polinomial mais consulta; 349–379 provam SAT/NP sob CookLevin; 383–385 distinguem reconstrução em consultas de movimentos TM2.
Conclusão: reconhecer o custo beta/carga e a ponte relativa demonstrada; não repetir falta de custo sem unidade. Não foi localizada tradução integral do leitor a movimentos de fita no acervo examinado; ela não é obrigação escondida do alvo atual.
