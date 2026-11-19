# ORDEM K01 — o teste às cegas da v412: levantamento dos canais e rascunho do pré-registro (nada se abre)

13/11/2026. Da gerência c1 ao Kimi. Leia antes `LEIA_PRIMEIRO.md`.

## O que o operador pediu

Na ordem de 13/11 (arquivo citado no `LEIA_PRIMEIRO.md`): para a v412, um teste agora ÀS CEGAS, com PODER PREDITIVO ACIMA DE 5 SIGMA,
para resolver as SETE RESSALVAS que restam no `ESTADO_ATUAL.md`.

## O que a gerência já leu (não refaça; confira e use)

- As sete ressalvas, no registro selado `h0dn_bg1_v411` (`ressalvas_secao8`) e no pré-registro
  `work\h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411.md` (seção 8): (1) regra emendada depois da guarda, teste não cego;
  (2) primário previsível por dois agregados públicos; (3) a linha das Cefeidas livres espera 4,5σ; (4) o poder é de desenho no modelo
  publicado; (5) 72 direções de variância zero na tabela de erros publicada; (6) escolhas feitas com a tabela de poder à vista;
  (7) tentativas anteriores e sobreposição dos dados locais com as Fases 4, 5 e 9.
- O desenho do H0DN: separação de desenho D = 6,71 (z_null − z_tgl), portão de 90 % em D = 6,28. Para a razão de Hubble, K − 1 = 0,0838:
  passar 5σ com 90 % de chance pede erro relativo total de cerca de 1,33 % ou menos.
- O canal do neutrino no core (`neutrino_m2`, NEUTRINO_M2_V2): previsão m₂ = β·sen45°·1 eV = 8,5074 meV contra 8,6776 ± 0,0576 meV:
  2,95σ de tensão CONTRA a previsão, crescendo com a precisão; regra de morte de 5σ em duas determinações independentes; cego desde
  08/08/2026 (`nao_e_cego_nesta_emissao`: a cegueira vale dali em diante); a linha de 5σ dentro da meta de projeto do JUNO; a escala 1 eV
  é DECLARADA, não derivada, e a que zeraria a tensão seria 1,0200 eV.
- Rotas do Mapa a ler antes de tudo (`rotas.py ver <rota>`): `investigacao.bancada_um_28set`, `hubble.fase9_razao_discriminante`,
  `cmb.nivel2_mcmc`, `cmb.fisher_gates_e_prereg_so_s4_14ago`, `cmb.neff_e_rho_mais_p`, `coma.dephasing_previsao_trancada`,
  `vazios.piso.v11`, `gate.contorno_da_verdade`, `auditoria.testes_passados_28set`, `primordial.fase8_era_da_radiacao`.
  E a pasta `work\cinco_sigma_fora_da_cosmologia_27out\`.
- A auditoria que o operador mandou você fazer em 12/11 (`work\h0dn_bg1_v410_09nov\kimi\ordem05\ESTATUTO_E_AUDITORIA_DE_SELECAO_V411.md`),
  seção 6: o que transformaria força em convergência.

## O que a gerência precisa saber (a partitura, antes de qualquer desenho)

Para cada canal em que a TGL tem previsão com zero parâmetro livre, uma linha da tabela `CANAIS_K01.json` com:

1. **A previsão:** fórmula, valor, e onde está no core selado (bloco e chave) ou no kernel.
2. **O dado:** existe hoje? É público? Algum número dele já foi lido por alguém desta casa ou é de conhecimento geral? Quando sai o
   próximo (com a fonte do calendário)?
3. **A cegueira:** é possível? Como (dado futuro; dado guardado por terceiro; outro)? O que impede?
4. **O poder de desenho:** D = |previsão − nulo| / σ_total, com a precisão publicada ou prevista (referência citada). D ≥ 6,3 dá cerca
   de 90 % de chance de passar 5σ. Mostre a conta.
5. **A independência:** os dados se sobrepõem aos já usados (H0DN, SH0ES, Pantheon+, Fases 4, 5 e 9)?
6. **As sete ressalvas, uma a uma:** quais esse canal responde e quais não.
7. **O negativo:** se o teste desse contra, seria falsificação da lei, da escala posta (o Um posto, 1 eV), ou parede medida (falta de
   poder)? Diga qual, sem suavizar.

Canais mínimos: a razão de Hubble com dado FUTURO (a próxima liberação da rede local; escadas independentes; o fundo com DESI DR3, Planck,
ACT, SPT); o neutrino m₂ (JUNO: a precisão de hoje e a de projeto; a data em que a linha de 5σ é alcançável); Σm_ν; o CMB com o Simons
Observatory (o pré-registro de agosto: o que falta decidir para ele valer); N_eff; o piso dos vazios com Euclid, LSST e DESI (é
unilateral?); ringdown e ecos; Coma e a lei de dephasing; relógios (²²⁹Th). E o que a gerência não listou.

## O que entregar

- `ENTREGA_K01.md` (resumo de até 15 linhas no topo; depois o detalhe).
- `CANAIS_K01.json` (uma entrada por canal, com os sete campos).
- `PRE_REGISTRO_CEGO_RASCUNHO_K01.md` para o canal (ou os dois canais) de maior poder: a função de veredito, os pesos, o limiar, os ramos
  (inclusive FALSIFIED), a guarda contra emenda posterior, o que cada ramo significaria, e como cada uma das sete ressalvas fica
  respondida ou segue de pé. É rascunho: nada se executa.
- `REGISTRO_MAPA_K01.json`.

## O que NÃO fazer

Não baixar nem ler vetor de dado; não calcular estatística observada; não escolher canal pelo resultado esperado a favor: a tabela
mostra todos, inclusive os que hoje andam contra a previsão. Número de literatura entra com arXiv ou DOI e a marca `[KNOWN, a conferir]`.
Se nenhum canal cumprir cegueira, poder e independência ao mesmo tempo com dado de hoje, DIGA ISSO no topo: é resultado, não falha.

— gerência c1, 13/11/2026.
