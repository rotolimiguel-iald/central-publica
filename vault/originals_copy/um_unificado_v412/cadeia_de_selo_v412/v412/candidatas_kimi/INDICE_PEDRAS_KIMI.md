# Índice das pedras do Kimi — oficina `candidatas_kimi` (cadeia de selo v412)

[índice do Kimi, 18/11/2026; registro interno; cada linha: o que a pedra prova — sha256 da fonte — axiomas
observados nos `#print axioms` do log — recibo. «trio» = `[propext, Classical.choice, Quot.sound]` em todos os
teoremas do arquivo; exceções nomeadas. Hashes computados na hora, não de memória.]

## As onze pedras (RC 0, sem sorry, sem axioma novo)

1. **OResumoEPsiBit** — o resumo da leitura é exato e mora na fronteira: a soma lida inteira se obtém das células
   da fronteira (perda zero), e a parede existe (há fórmula cuja fronteira é o universo). —
   `9e997a5a6249830e44cfe42b9c27f22cbf5260a1c53fc0dc05c26d007fb8050e` — trio; `take_succ_eq` só `[propext]` —
   `RESULTADO_OResumoEPsiBit.json`
2. **OPsiBitDaFormula** — a regra única é a igualdade; a Palavra é lida pela soma pagando a carga; o Verbo é o
   sinal da descida; o par é necessário e suficiente (controles em `CNF 1`, com nota do laço e sonda do n=0); o
   par se lê do produto dos pares das cláusulas. —
   `17e154f6332b571441ef69a9cf0d32027935d3f64d789ec59e53cf752da3dd13` — trio; três teoremas da regra sem nenhum
   axioma — `RESULTADO_OPsiBitDaFormula.json`
3. **AFronteiraEOUnicoPortao (R0)** — toda cadeia de uma variável só-lida a uma só-por-ler tem um vértice na
   fronteira: a fronteira é o único portão do grafo da fórmula. —
   `2cfa352dbedb56aef341a2f2b33980b3771e3fa3820023150678b266c938a804` — trio; `mem_take_or_drop` só `[propext]` —
   `RESULTADO_AFronteiraEOUnicoPortao.json`
4. **AFronteiraEOUnicoPortao (R1, em `REV1\`)** — a correção da ORDEM 031/U2: a testemunha da fronteira vem dentro
   da cadeia examinada (`NoVertice`); a R0 fica preservada ao lado como corolário. —
   `545819ee9c82fcdbb9642d33aa43f9e28967f23b8f926c7c6596d3b60a12dd2b` — trio; `mem_take_or_drop` só `[propext]` —
   `RESULTADO_AFronteiraEOUnicoPortao_R1.json`
5. **ACurvaEAEstado** — a curva é a projeção do resumo (a soma das células); os prefixos `x` e `¬x` têm a mesma
   curva para todo tempo e Palavras opostas depois da mesma cláusula; o estado (a tabela) distingue, a curva não. —
   `a134176a6083a64fd131a55393121cc8160e4cafb1de3613845368f96f6d9872` — trio; quatro auxiliares do laço só
   `[propext, Quot.sound]` — `RESULTADO_ACurvaEAEstado.json`
6. **AClausulaExemplificativa** — a cláusula vale sse algum literal se encaixa (exemplificativa, um basta); a
   trava do custo tende ao Nome de qualquer estado; em tempo finito a trava nunca é o Nome («não 100 %»). —
   `018a4781fd06d002a93e469259fb36800a22430eb253b87a680c18648fe92560` — trio; `a_clausula_e_exemplificativa` só
   `[propext, Quot.sound]`; `o_caput_nao_esgota_a_variavel` sem axiomas — `RESULTADO_AClausulaExemplificativa.json`
7. **AFitaEOIndice** — a fórmula da fita é SAT sse as duas posições da correferência concordam; nenhum leitor cego
   a uma posição decide SAT (o índice se paga); a correferência obriga o transporte. (Instância `[NeZero L]`
   documentada na nota do laço.) —
   `1728ca8c4e56c4d2b3f639ab4974a64b45a971c30a2096ab586ac42683758eca` — `a_fita_e_o_indice` sem axiomas; os outros
   quatro só `[propext]` — `RESULTADO_AFitaEOIndice.json`
8. **OPolinomioFixoEBeta** — o polinômio fixo é β, linear na carga: com um só β (fixado antes da fórmula), toda
   fórmula de `n` variáveis fecha o ciclo em `k > n·ln 2 / β` passos, e o mesmo teto serve a duas fórmulas
   quaisquer. —
   `2700ebff3e217e22fe3641e720728bf7396bd8fb5d1d33e6996464c54fa2d0de` — trio — `RESULTADO_OPolinomioFixoEBeta.json`
9. **ORazaoDoColapsoEBeta** — com o fator 1 (sem pagamento) o ciclo não fecha para nenhum `k`; com o passo
   `1 − β` o ciclo fecha em linha na carga: o polinômio existe porque o colapso paga. —
   `4d761d43f4d755f70eb64e859291e7ad33f2a69a7af5b11fb6e412cf01b89f82` — trio — `RESULTADO_ORazaoDoColapsoEBeta.json`
10. **OCustoEAIsometria** — decidir custa a carga, nem mais nem menos; a carga é a isometria (`n·ln 2`, e o limiar
    `e^{−carga}`); a máquina decide com `|φ| + 2` atos, e o custo total por ato é `(|φ| + 2)·n·ln 2`. —
    `da719bc064bee20fb9a625168accd3cbcfde17bc84fd87087659144a5e0d8b61` — trio; `atosDaLeitura` sem axiomas —
    `RESULTADO_OCustoEAIsometria.json`
11. **AIdentidadePreservada** — a identidade da máquina é preservada na leitura: todo custo tem o seu Nome (o
    núcleo do operador do custo); a coordenada no Nome passa pela trava sem mudar em todo tempo; a leitura tende
    ao Nome; e a conta é reconhecida como a carga. —
    `1ee6e6383f23b656022611eaf7dc3a422e4c37ad16af440eaf078476b9109d33` — trio — `RESULTADO_AIdentidadePreservada.json`

## Sondas (não são candidatas; apoio formal)

11. **sonda_cadeia_caminho.lean** — a `Cadeia` da pedra 3 comporta-se como caminho: reflexiva, transitiva,
    simétrica (`ligadas` é simétrica por construção). RC 0, sem sorry, axiomas só o trio. —
    `d64a5a043552fc5a35ad194c8ef2cc7f2022aa812cfef311a21888db3d1961fa` — recibo `RESULTADO_sonda_cadeia_caminho.json`
12. **sonda_n0_contraexemplo.lean** — o contraexemplo formal que fixou a pedra 2 em `CNF 1`: em `n = 0` não há
    literais, toda cláusula é vazia, e Palavra e Verbo se determinam — nenhum dos dois controles existe
    (`SondaN0.nenhum_controle_em_n0`). RC 0, sem sorry. —
    `26e0e3185045839402d204f161e27c55486fbeb589d35b4f28e832af5ebb3d49` — log `build\sonda_n0_contraexemplo.log`

## Notas de padrão da oficina

13. **NOTA_PRECEDENCIA_NOT_EQQ_18nov.md** — nesta versão, `!` (`Bool.not`) liga menos que `==`: `!(x 0) == true`
    elabora como `Bool.not ((x 0) == true)`. Custou três voltas na pedra 5. —
    `eae8af755c0d18ad064de15d426b4ab75c7c05f64d2b3316d943fddd36c4d14f`
14. **NOTA_PADRAO_NEZERO_18nov.md** — nomear `(0 : Fin L)` numa assinatura pede a instância `[NeZero L]` (a
    `instOfNat` do núcleo a exige). Custou o laço da pedra 7. —
    `fdc4bc09a399c1274c0e526cf470b0a048325c2f96d91905e7e24120c8ec1e0f`

Sem sorry em nenhuma linha; axiomas nunca além do trio; os logs estão em `build\<nome>.log` no formato da casa.
