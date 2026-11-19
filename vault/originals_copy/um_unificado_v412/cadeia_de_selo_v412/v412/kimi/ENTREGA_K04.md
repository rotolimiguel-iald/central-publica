# ENTREGA K04 — o teste às cegas, rodada 2

- **Existe hoje teste cego de natureza com poder de desenho ≥ 5σ executável? Não.** Não há primeira data publicada defensável: os marcos abaixo são cenários condicionais, dependendo de covariância, sistemáticas, independência e regra ratificada.
- **O que o m₂ mais provavelmente devolve?** Com precisão alta, tensão do primário, não falsificação: na Tabela 6, `P(r≥5)=64,74%` independente e `66,13%` no brinquedo cumulativo; com a regra atual, isso vira `SINGLE_P/OPEN_RULE_GAP`, não morte do pacote da escala. Com `S` realmente `ABSENT`, **condicionalmente à regra e ao desenho, um teste que não pode devolver o negativo não é teste**; SK‑Gd permanece como candidata condicional ao lado.
- [DERIVED] **Hubble:** H0DN tem D = 7,068/8,068, mas já foi lido; a melhor linha independente nominal, SN II, tem D = 3,256, e TDCOSMO, 2,462–2,689; nenhuma é teste cego qualificado.
- [DERIVED—PLANEJAMENTO] **m₂ a 0,7 %:** `P(r≥5)=12,88%` independente e 3,48% no brinquedo cumulativo; a 0,5 %, 35,04% e 31,47%; no modelo independente (a2), sob verdade = previsão, `r<3` tem cerca de 99,86%.
- [KNOWN, a conferir] **Segunda testemunha:** nenhum par publicado fecha FALSIFIED ou MATCHED hoje; SK‑Gd está a 3,605σ e o brinquedo √T dá 380,08 dias adicionais, sem agenda ou independência demonstrada.
- [REAL] **Métrica e história:** vale m₂ até emenda (`r=1,937997`; em Δm², 1,928084). A liberação JUNO de 29/09/2026 é a primeira nova determinação JUNO posterior ao hash V2 e devolve `ARMED_CONSISTENT`, mas não é cega para a casa.
- [DERIVED] **Calendário-aritmético, não cronograma:** o brinquedo full-reactor dá 5σ em 31/03/2028 e D90 em 19/09/2031; covariância real e calendário de liberação continuam `[OPEN]`.
- [DERIVED] **Combinação:** incremento JUNO + `N_eff`/SO só é cenário; em Δm², Stouffer cruza D90 com `σ_J≤0,02642×10⁻⁵ eV²`, e 2034 é o primeiro horizonte plausível, não uma data garantida.
- [DERIVED] **Ringdown:** são necessários 25,49/25,69 eventos equivalentes; D10 pede cerca de 27 meses retrospectivos adicionais, IR1 não basta e O5 é janela condicional; o canal só decide o par retirado.
- [DECLARADO] **Sete ressalvas:** exigem teste cego/dado/calibração/covariância novos ou história declarada; as contas de R3–R7 ficaram apenas como partituras, sem execução.
- [DECLARADO] **P7/K06:** responde sobre o leitor, não resolve as ressalvas empíricas; serve apenas como disciplina metodológica de cegueira e controles.
- [INPUT] **Atos do operador:** decidir se mantém duas testemunhas, emenda para uma ou pré-fixa S; escolher métrica e se nenhuma abertura ocorre antes dessas decisões.
- [REAL] **Custódia:** revisada internamente; REV0/REV1 e erratas preservados; nenhum vetor observado, abertura, solver ou teste empírico foi executado; o gate permanece imóvel.

## A. O “agora” em Hubble ficou esgotado

`HUBBLE_JA_EXAMINADO_K04.md` reúne as rotas e sequências decisivas, incluindo R–E, R–F, R–G, as Fases 1–5, a Fase 9 e as erratas. A leitura de fluxo acumulado intermediário está **morta**, rota `d1.fase4_desvio_30set`, seq 229/231 e reprodução 410; lentes de um passo são outro caso, com ponte física aberta.

Foram cobertos masers, SN II, lentes, sirenes, SZ/raios X, FRB e linhas adicionais como BBH–AGN, SN Encore e FRB126/118. Seus agregados já são públicos e servem como linhas de independência, não como uma abertura cega nova. Forecasts TDCOSMO de 1,5 % e 1,2 % cruzam 5σ/D90 apenas em desenho e não têm data publicada.

## B. O m₂ e o desfecho que a regra permite nomear

`M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md` separa três modelos: incremento independente, posterior cumulativo com covariância e verdade condicionada ao valor atual. Nenhuma probabilidade é apresentada como resultado observado.

Na precisão da Tabela 6, a possibilidade mais frequente é uma tensão do primário ≥ 5 sem a segunda testemunha exigida pela regra. Se o operador emendar para uma única testemunha, o negativo atinge **o pacote `E0 = 1 eV` com `m₁≈0` e a identificação**, não β isoladamente, toda a TGL ou o gate. Se mantiver duas testemunhas, o canal continua medindo tensão, sem morte assegurada.

O incremento 59→207 dias dá 7,306061 ± 0,102640 por variância inversa, mas não é uma determinação independente sem a covariância interliberações. A segunda testemunha deve ser pré-fixada por fonte e versão, com covariância e robustez; não basta pedir genericamente “uma medida sem JUNO”.

## C. Combinação e ringdown

`COMBINACAO_K04.md` testa apenas o pacote das leituras derivadas, não β isolado. A independência entre JUNO e SO é condicional à covariância, ao grupo CMB e ao fechamento S/L. Stouffer, Fisher e verossimilhança são candidatas, não regras congeladas.

O ringdown permanece fora do pacote TGL: o par F2b foi retirado antes do dado, e o censo tem 14 elegíveis/10 sem hold. D10 usa 6,9 eventos/ano e cerca de 27 meses; D14 usa 9,6/ano e cerca de 14,5 meses, ambos retrospectivos.

## D. As sete ressalvas e o que as contas não podem fazer

`RESSALVAS_UMA_A_UMA_K04.md` registra o ato necessário para cada ressalva. R1/R2/R6 pedem teste cego novo; R3/R4/R5 pedem calibração/covariância independentes; R7 pede história e livro de dependências. As fórmulas de piso de variância, melhoria de calibração e Šidák estão escritas, mas **não foram avaliadas**.

A partitura contém insumos e hashes, inclusive o SHA-256 do core para R7-A. Um número ruim mediria fragilidade do erro/desenho, não falsificação automática da lei. `executar_abertura_v411.py` nunca foi chamado.

## E. Errata e decisões

`ERRATA_NEUTRINO_V412_RASCUNHO_K04.md` registra a queda autônoma 2,206054 → 1,937997, separando-a do reflexo global NuFIT e preservando `projecao_2031_sigma = 7,842905784155273` apenas como registro condicionado ao centro antigo.

`PERGUNTA_K04.md` apresenta Q1/Q2 sem escolher. `REGISTRO_MAPA_K04.json` é proposta não registrada. A errata do core não foi instalada.

## Artefatos principais

- `HUBBLE_JA_EXAMINADO_K04.md`
- `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md`
- `COMBINACAO_K04.md`
- `RESSALVAS_UMA_A_UMA_K04.md`
- `ERRATA_NEUTRINO_V412_RASCUNHO_K04.md`
- `PERGUNTA_K04.md` e `REGISTRO_MAPA_K04.json`
- Erratas Hubble/M2/combinação e medidas reproduzíveis em `K04/`.

Nenhuma instalação, nova abertura ou registro no Mapa foi feita.
