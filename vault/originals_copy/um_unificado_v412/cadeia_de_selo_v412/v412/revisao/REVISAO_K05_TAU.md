# REVISÃO DISTINTA DA FRENTE τ★ DA ENTREGA K05 (v412) — `TAU_ESTRELA_R2.md`

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nada instalado, nenhum `lake`, nenhuma escrita no kernel nem na pasta do Kimi.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura · [DERIVED] derivado por mim aqui · [DECLARADO] do Kimi, não conferido por mim · [OPEN].
`NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada. O gate não se mexe.

## 0. Veredito

**APROVADA COM RESSALVAS.** Os números conferem todos (cinco casas ou mais onde o Kimi as mostra), a candidata Lean recompila limpa, só o relógio selado foi lido, as cotas ficaram separadas e as citações do kernel dizem o que o documento afirma. As ressalvas são de enquadramento e de omissão, não de conta. Cinco pedem correção antes de o documento seguir; quatro são menores.

**Pedem correção:**
1. **R1 — a consulta ao Mapa de Rotas foi inconclusiva por construção** (§1, `TAU_ESTRELA_R2.md:15`): frase devolve zero. Com termos únicos há rotas relevantes que o documento não cita (lista em §2).
2. **R2 — o 60 M☉ da candidata R1 fica pela METADADE do ramo B já pré-registrado** (§6, tabela `:209`; §4.2 `:160`): `4πGM/c³` = 3,714×10⁻³ s contra `k·GM/c³` com `k = 2π/κ̂ = 8π` em χ = 0 = 7,427×10⁻³ s. O documento não confronta as duas.
3. **R3 — o `√2` da célula omite a leitura por face que o kernel já tem** (`TAU_ESTRELA_R2.md:134,144`; `AreaScale.lean:35–37`): 2G = duas faces de G cada; com a face como quadrado, o tempo é `t_P`, não `√2·t_P`.
4. **R4 — «não é mera coincidência» (`:154`) afirma mais do que o teorema prova.** O iff de `PontoZeroDoPsion.lean:198–199` mostra compatibilidade (o `√2` cancela), não origem comum.
5. **R5 — a atribuição ao operador (`:187`) é da gerência.** «Laboratório: Planck; onde há horizonte próprio: o horizonte» é leitura medida pela gerência em 27/10, herdada da ORDEM K05 §D.5, não fala dele.

**Menores:** R6 (ω³ só vale se E = ħω, nota `:87`), R7 (R1 «sem constante nova» esconde a escolha da volta), R8 (G de CODATA em `t_P` e G do core no átomo, não dito no texto), R9 (o que cada teorema Lean é de fato; §4).

## 1. Consulta ao Mapa de Rotas (antes de tudo) [REAL]

`rotas.py consultar` com termos únicos: `dephasing` → 49 rotas; `relogio` → 33; `tau` → 54 (primeiras chamadas); depois `planck` 34, `horizonte` 9, `retido` 5, `pedagio` 9, `hubble` 26 (`scripts_k05_tau\revisor_mapa.py`, saída em `revisor_mapa_saida.json`). `consultar K05` → 1 rota (`cadeia.preparacao_v412`). Nada refeito, nada registrado.
**Achado R1.** O documento (`:15`) diz que as três consultas ao Mapa foram «todas `n=0`». São consultas por FRASE («tau estrela relogio Planck horizonte retido»), que devolvem zero por construção (regra da casa: termo único). Zero por frase não é ausência. O texto do documento ainda diz «a conclusão de ausência é limitada», o que ajuda; mas a ordem da gerência pedia a consulta citada e ela não mostra o que o Mapa tem. Rotas relevantes que o documento não cita:
- `natureza.horizontes_proprios_sem_ponte_tgl_27out` (EXAMINADA, OPEN): «ponte τ★ ausente» para BEC, fibra, água, Unruh, Casimir, PTA; «só reabre se alguém DERIVAR a identificação do tempo do contorno com τ★». É a mesma parede (i) do `PAREDE_RELOGIO_E_PONTE_HUBBLE`, já examinada. `nao_refazer`: não calcular N/tempo para 5σ sem a ponte τ★.
- `ringdown.dephasing` e `ringdown.ramo_b_preregistro_v386`: o ramo B (τ★ = k·G·M_f/c³; k = 2π/κ̂; 8π em χ = 0 [KNOWN]; Kerr [CONJECTURE]) é o ÚNICO sistema com horizonte próprio e observável derivado. É o caso do «remanescente de 60 M☉» (R2).
- `hubble.k_sem_portador_fisico_02nov` e `hubble.k_como_transposicao_inteira_ffat_02nov` (BLOQUEADA): «R1 ratificada em 02/11: β entra uma vez, no reflexo; o fundo é nu». É o contexto da parede (ii) (ponte τ★ → K).
- `massa.e0.conferencia_kimi_e_no_go_tipado_31out`: a origem das três frequências e do no-go.

## 2. Tarefa 1 — os números refeitos [REAL]

Script meu e independente: `scripts_k05_tau\revisor_tau_numeros.py` (saída `revisor_tau_numeros_saida.json`). Core lido por script: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json`, sha256 `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e` (16 642 521 bytes), chave `core.clock_test_result_v369`. β = `ALPHA_FINE_CODATA_2018 × √e` em runtime = 0,012031300400803142 (idêntico ao `beta_runtime` do core, diferença 0). Constantes: CODATA 2018 (α, G = 6,67430×10⁻¹¹), SI exatos (h, c, e), IAU 2015 (GM☉), Planck 2018 (H₀ = 67,4) [KNOWN].

**Conferem, todos:**

| quantidade | meu valor | do Kimi | confere |
|---|---|---|---|
| ħ/(1 eV) vs Kim 95 % | +15,4058 ordens (razão 2,5456×10¹⁵) | 15,4058; 2,55×10¹⁵ | sim, 4 casas |
| ħ/(β·1 eV) vs Kim | +17,3255 (2,1158×10¹⁷) | 17,3255; 2,12×10¹⁷ | sim, 4 casas |
| mesmas, Ma/Al/Morawetz/Ooi/Zn/Atlas | 15,64/15,20/9,33/9,81/18,82/17,56 e 17,56/17,12/11,25/11,73/20,74/19,48 | idem na tabela | sim, 2 casas |
| margem de 1/β·t_P vs Kim | 10,7612 | 10,7612 | sim, 4 casas |
| margem vs Zn | 7,3499 (o core guarda `tP_over_beta_vs_best_matter_bound_orders` = 7,349938736594645) | 7,34993 | sim, 5 casas, e bate com o campo selado |
| margens de 1/β vs Ma/Al/Th(2)/Atlas | 10,5315/10,9715/16,8337/16,3596/8,6039 | 10,53/10,97/16,83/16,36/8,60 | sim |
| `c★ = 1, √2, 2π, 4π` vs Kim | 12,6809; 12,5304; 11,8827; 11,5817 | 12,68; 12,53; 11,88; 11,58 | sim (12,6809 = `deficit_orders_bound` do core) |
| Unruh-g / GM⊕/c³ / GM(Sr)/c³ / monopolo 1 eV, vs Kim | +38,87 / +19,76 / −29,86 / −39,67 | idem | sim |
| as 3 alternativas Γ contra os campos selados | diferença relativa ≤ 1,7×10⁻¹⁶ (Terra: 0) | «0» | sim |
| τ_hor: 1 eV; Sr transição; Sr repouso | 5,5491×10⁻⁷¹; 9,8505×10⁻⁷¹; 4,4970×10⁻⁶⁰ s | 5,549; 9,850; 4,497 | sim |
| 60 M☉: 4π·60·GM☉/c³; GM/c³; max/t_P | 3,7137×10⁻³; 2,9553×10⁻⁴ s; 6,8885×10⁴⁰ | 3,714; 2,955; 6,888 | sim |
| Hubble: 2π/H₀; 1/H₀; max/t_P | 2,8765×10¹⁸; 4,5782×10¹⁷ s; 5,3356×10⁶¹ | 2,877; 4,578; 5,336 | sim |
| Γ/H₀ = πβ; 2β/3 | 0,037797; 0,0080209 | 3,780×10⁻²; 8,021×10⁻³ | sim |
| frequências com τ = t_P: √2/τ; 2/τ; 2/(βτ); razão | 2,6232×10⁴³; 3,7097×10⁴³; 3,0834×10⁴⁵ rad/s; 83,1165 | idem | sim |
| N = E_P/(1 eV) | 1,220890128584×10²⁸ (G reconstruído de N: 6,6743×10⁻¹¹) | 1,2208901286×10²⁸ | sim, 10 casas |
| soma e quadratura = max «na precisão exibida» | diferença relativa 0 nos cinco sistemas | idem | sim |

**«Hubble sob a hipótese crítica» — qual hipótese?** [REAL, refeito] Densidade igual à crítica (ρ_c = 3H₀²/8πG, universo plano), dentro da esfera de raio de Hubble c/H₀, toda ela lida como energia E = Mc²; daí `E_H = c⁵/(2GH₀)` (conferi por integração independente: diferença relativa 1,8×10⁻¹⁶) e, com `τ_hor = 4πGE/c⁵ = 2πr_s/c`, `τ_hor = 2π/H₀`. É a coincidência conhecida de que o raio de Hubble é o raio de Schwarzschild da massa crítica. Hipóteses embutidas: ρ = ρ_c, raio c/H₀ (e não o horizonte de eventos), E = Mc² para todo o conteúdo, H₀ = 67,4 [KNOWN]. O documento nomeia `H_HUBBLE_CRITICO`; as três outras ficam só implícitas.
Nota: o core guarda `tau_star_s = 5,391125×10⁻⁴⁴` (G = 6,674×10⁻¹¹); o Kimi usa `t_P = 5,391246×10⁻⁴⁴` (CODATA); diferença 2,2×10⁻⁵, sem efeito nas ordens (R8).

## 3. Tarefa 2 — só o relógio selado foi lido? [REAL]

Li os três scripts por inteiro.
- `extrair_clock_selado.py`: abre só o core (`rb`), grava em `K05\TAU\medidas\`. Nenhuma rede.
- `medir_tau_r2.py`: lê o JSON extraído; confere que o sha256 do core não mudou; lê `P1.platforms` e `tau_star_alternatives` do registro; lista 24 arquivos só para HASH (core, `um.py`, seis `.lean`, Atlas, inventário, quatro memórias, documentos do Kimi, REVISAO_K02, os próprios arquivos); calcula tudo por álgebra. Não importa `urllib`, `socket`, `requests`; não abre `.npz`, `.fits`, `.h5` nem nenhuma série observada. Escreve só em `K05\TAU\medidas\`.
- `validar_tau_r2.py`: lê o próprio material; `urllib.parse` só para decompor links `kimi-cite://`; sem rede.
- Nenhum dado observado novo foi aberto; nenhuma estatística refeita. As asserções internas (`assert relative_difference < 2e-12`) são cálculo de álgebra, não teste.
- **As cotas ficam separadas?** Sim: sete colunas (Kim 95 %, Ma nominal, Al nominal, Morawetz 95 %, Ooi 95 %, Zn nominal, Atlas auxiliar), cada uma com tipo; a do Atlas (1,8×10⁻³³ s) é marcada como registro não reavaliado e NÃO coincide com Th do core (3,06×10⁻²⁵ e 1,03×10⁻²⁵) nem com Zn (1,00×10⁻³⁴). Nenhuma é fundida. A frase final «nenhuma cota P1 lida distingue os candidatos» está bem formulada (a de Zn dá 7,35, não «mais de 10», e o documento diz isso).
- Ressalva de rótulo (menor): `:34` chama Zn de «nominal; Mössbauer, não relógio»; o core diz mais: `verification` = «SÓ O RESUMO … texto integral NÃO aberto (anti-bot)» e, para Th, «versão de revista NÃO aberta (login)». A margem de 7,34993 é justamente a do Zn; vale levar a ressalva junto (a memória `missao-relogios-v369.md:47` já diz «só abstract»).
- Observação: o documento diz (`:249`) «nada foi registrado ou depositado»; verdadeiro na hora da validação TAU (20:53). Depois, às 21:35, o Kimi depositou `fila\depositos\kimi\20261113_213522_declarado-k05-…md` e deixou `REGISTRO_MAPA_K05.json` como PROPOSTA não registrada (`consultar K05` confirma: o Mapa não tem a rota). Isso é permitido pela regra da fila; só aviso para a frase não ser lida como se valesse para o fim da entrega.

## 4. Tarefa 3 — a candidata Lean [REAL]

Cópia minha: `scripts_k05_tau\src\TAU_ESTRELA_R2.lean`, sha256 `4d652ab44da6da7857540057e4b9b76170590112d25273511e0311a57d65ee4c`, idêntico byte a byte ao arquivo do Kimi. Método do revisor da rodada 1: `lean.exe` 4.31.0 direto, `LEAN_PATH` só nos `.olean` de Mathlib do kernel, saída em `scripts_k05_tau\build\` (`recompilar_revisor_k05_tau.sh`; log `build\TAU_ESTRELA_R2.revisor.log` e `build\saida_recompilacao.txt`). Nunca `lake`, nada escrito no kernel.
- **rc = 0**; um único aviso (variável `hc` não usada, l.117: `half_nat_square_light_crossing`).
- **`#print axioms`** dos 14 enunciados do Kimi: só `propext`, `Classical.choice`, `Quot.sound`. Fiz uma segunda cópia (`TAU_REV_EXTRA.lean`, sha256 `4e8980efb24ce6a1a9326ed0b7bf58796b83ea359a67a4e1380ff0311ce344c8`) com mais nove `#print axioms` (`planckEnergy_pos/ne/sq`, `sqrt_half_nat_cell_area`, `half_nat_square_light_crossing`, `planckEnergy`, `planckTime`, `Gamma`, `tauMax`): também só o trio, rc = 0.
- **Zero `sorry`/`admit`/`axiom`/`native_decide`/`opaque`** (grep no fonte).
- Em palavras simples, o que cada um prova:
  - `no_time_from_hbar_c`: o sistema linear «ħ^a·c^b tem dimensão de tempo» é inconsistente (a=0, b=0 e 0=1). [DERIVED por mim também: eliminação exata em frações; inconsistente.] A tabela de dimensões (ħ = M L² T⁻¹, c = L T⁻¹) está só na docstring; no Lean entram as três equações já escritas à mão.
  - `unique_planck_exponents`: o sistema para ħ^a G^b c^d com dimensão de tempo tem solução única (1/2, 1/2, −5/2). [DERIVED por mim: determinante −2 ≠ 0.]
  - `planckTime_sq`, `planckTime_mul_planckEnergy`: definições `E_P = √(ħc⁵/G)`, `t_P = ħ/E_P`; `t_P² = ħG/c⁵` e `t_P·E_P = ħ`. Conteúdo real, álgebra de raiz.
  - `gap_time_is_dimensionless_ratio_mul_planck` e `retained_time_is_dimensionless_ratio_mul_planck`: `ħ/u = (E_P/u)·t_P` e `ħ/(βu) = (E_P/(βu))·t_P`. É uma identidade (reescrever ħ/u como (E_P/u)(ħ/E_P)); o conteúdo é só dizer qual é o número puro. **Nome promete um pouco mais que o enunciado**: todas as variáveis são reais; «adimensional» está na docstring.
  - `newton_eq_of_dimensionless_ratio` e `dimensionless_ratio_eq_of_newton`: com ħ, c, u > 0 fixos, `N·u = E_P(G)` ⟺ `G = ħc⁵/(N²u²)`. As duas direções valem; é o enunciado de «medir G = medir N». Tem conteúdo (usa `E_P² = ħc⁵/G`).
  - `half_nat_cell_area`: de `1/2 = A/(4ℓ²)` segue `A = 2ℓ²`. Condicional, correto; a hipótese `S = A/(4ℓ_P²)` é a premissa.
  - `half_nat_square_light_crossing(_planck)`: de `A = 2ℓ²`, `√A/c = √2·ℓ/c`. O «quadrado» e a «travessia» estão na própria definição `√A/c` do enunciado, não provados. O nome diz «half_nat», mas a Meia-Nat só aparece na hipótese `hA`.
  - `canonical_readout_fixes_frequency`: `ħω = ħ·(½βτω²)` ⟹ `ω = 2/(βτ)`. É o teorema do kernel (`TonicaDoHamiltoniano.lean:166`) com β na premissa. Correto e curto.
  - `monopole_gamma_is_cubic`: `Γ(β, 4πG(ħω)/c⁵, ω) = (2πβGħ/c⁵)·ω³` por `ring`. Correto, mas o «E = ħω» está embutido no enunciado (R6).
  - `tauMax_local` e `tauMax_horizon`: são `max_eq_left`/`max_eq_right`. **Ocos como física**: dizem que o `max` devolve o maior. Quem escolhe que o horizonte do átomo é menor que Planck é o script Python, não o Lean. A docstring avisa «candidata de seleção, não derivação».
- Nenhum teorema é falso, nenhum prova a física das hipóteses; o documento diz isso em `:247` («prova álgebra e dimensão, não a física das hipóteses nomeadas»). Está honesto.

## 5. Tarefa 4 — as citações do kernel [REAL]

`scripts_k05_tau\revisor_citacoes.py` (saída `revisor_citacoes_saida.json`): 24 de 24 citações `kimi-cite://` do relatório têm arquivo existente, linha existente e o trecho dentro de ±3 linhas (mais estrito que o validador do Kimi, que só testa «trecho no arquivo»). Lidas à mão as que pesam:
- **`PontoZeroDoPsion.lean:198–199`** (R4): o teorema `a_frequencia_do_sistema_e_a_do_psion_iff` diz exatamente `√2/τ = √(omegaSq β (βu²)) ↔ τ = tempoDoRetido c u`, com `tempoDoRetido = 1/(βu)` (ħ = 1). O documento a cita bem. O módulo diz (l.157–161): «os demais são álgebra dada a definição de τ. **Ler τ como o τ★ do sistema é [ONTO]**». O documento repete esse [ONTO]. ✓.
- **«autoconsistente sem β»** `TonicaDoHamiltoniano.lean:166–173`: `self_consistent_readout_fixes_the_frequency (ħ τ ω) … (h : ħ·ω = ħ·((1/2)·τ·ω²)) : ω = 2/τ`. Não há β na hipótese. ✓. A razão está no cabeçalho do módulo (l.33–35) e na conferência de 31/10 (`CONFERENCIA_E0_KIMI_E_CADEIA_31out.md:39`: `|L_φ| = β·ρ_modular` é TAXA; `E₀ = ħ·f(ω₀) = ħ·½τ★ω₀²`, com `f = Γ/β`). A premissa sem β é, pelo texto, intencional como leitura «a energia do modo é a sua própria leitura modular»; que ela seja a escolha física é leitura da gerência, não fala do operador.
- **«`K = E(z*)^(2β/3)` vem de `TheFlowLawContrast`, não de τ★»**: `the_derived_kernel_factor_normalized` (l.166) sai de `H₀_local = H₀_fundo·exp(β∫g)` (`the_flow_law_contrast`, l.72) e `g = (2/3)·d ln E/dN` (`frwContrast`, l.54). O módulo usa `leakVerb β g t x` (de `TheFlowLawD1a.lean:37`: `exp(−t·β·g)·x`). Nem em `TheFlowLawContrast.lean` (grep «τ★|tau|tauStar»: zero ocorrência) nem no cabeçalho aparece τ★. ✓ Atenção ao alcance: é ausência no módulo e na sua definição de `leakVerb`; não é teorema de independência.
- `o_relogio_do_retido` (`:251`): `κ·tempoDoRetido = 2π ⟹ κ/(2π) = Δ`. ✓ como o documento o descreve (hipótese de volta, não prova `τ★ = 2π t_P`).
- `AreaScale.lean:12`: «ISTO NÃO AFIRMA QUE G FOI DERIVADO. G é entrada física medida». ✓.
- `TriadMaster.lean:63` (`area_entropy : dS = dA/(4G)` como campo de `HorizonEquilibriumData`) ✓; `PageInformation.lean:39` («a composição plena é leitura/futuro») ✓.

**R3 — o que o documento não diz sobre `AreaScale`.** O módulo tem mais que a equivalência de Newton–Planck: `A(P) = κ_A·τ(P)`, `η = (1/2)/κ_A`, `κ_A = 2G ⟺ 2π/η = 8πG` e **`face_area_eq_G` (l.35–37): `A_face = κ/2 = G`** e `halfNat_over_two_faces_eq_quarter` (l.40–42). O `PageInformation` (l.39) o resume como «[κ=2G, face=G]». Ou seja, a «área 2ℓ_P²» da Meia-Nat tem no kernel a forma «DUAS faces de ℓ_P² cada». O documento (`:144`, tabela `:134`) trata os 2ℓ_P² como UM quadrado de lado √2·ℓ_P. A leitura por face (quadrado de lado ℓ_P) daria `τ = t_P` (c★ = 1), não √2·t_P. A hipótese `H_TRAVESSIA_QUADRADA` precisa dizer qual das duas (o par ou a face) é a célula. Correção sugerida: acrescentar essa frase ao parágrafo da célula e à linha `√2` da tabela.

## 6. Tarefa 5 — o lema dimensional (§3) [DERIVED por mim; REAL no sandbox]

`scripts_k05_tau\revisor_lema_e_regimes.py`:
- ħ^a·c^b como tempo: sistema inconsistente (eliminação exata, frações). ✓
- ħ^a·G^b·c^d como tempo: solução única (1/2, 1/2, −5/2), determinante da matriz de dimensões −2. ✓
- ħ^a·u^b como tempo: `(a,b) = (1,−1)`, isto é, `ħ/u`. ✓ (a outra âncora).
- `τ_u = N·t_P` com `N = E_P/u`; `ħ/(βu) = (N/β)·t_P`; para u = 1 eV, `N = 1,220890128584×10²⁸`, `t_P = ħ/E_P`. ✓
- «Fixados ħ, c, u, medir G equivale a medir N»: `G = ħc⁵/(N²u²)`, conferido (reconstruído 6,6743×10⁻¹¹). A equivalência vale como bijeção entre números positivos; nota: N só é «puro» depois de fixada a unidade u (1 eV é a convenção da unidade; o documento diz «u posto»). ✓
- O que o kernel cobre: `TheScaleHasNoFixedPoint.no_positive_scale_invariant` (l.99) e `no_function_of_the_inscription_fixes_E0` (Tônica, l.128) não enunciam o lema; o documento diz isso e eu confirmo [REAL: li os dois enunciados]. A afirmação de ausência é limitada aos módulos consultados, e o documento a limita assim.
- A separação «(i) escolher a âncora; (ii) derivar o número puro c★» está correta e é a contribuição útil da rodada.

## 7. Tarefa 6 — §4: os três `√2` e o monopolo [REAL no kernel; DERIVED]

- **São objetos distintos no kernel?** Sim, e há mais de três:
  1. célula: `A = 2ℓ_P²`, `τ = √A/c`. NÃO é objeto de kernel (só aritmética na candidata; ver R3 para o que o kernel tem em `AreaScale`).
  2. dispersão do psíon: `omegaSq β R := 2·β·R` (`PontoZeroDoPsion.lean:86`), `psion_quantum`: `ω = √2·β·u` (l.92).
  3. frequência do sistema: `ω★ = √2/τ★`, escolhida (`TonicaDoHamiltoniano.lean:144`: «Não é lei nova; é a escolha da frequência») para que `½βτ(√2/τ)² = β/τ`.
  4. (o documento não conta) o gap da estação `stationKappa 1 = √2` (`TheStation.lean:52`) e o `sen 45° = √2/2` da projeção.
  O 2 da dispersão e o numerador de ω★ são definidos separadamente e só se ligam pelo iff das l.198–199.
- **R4.** O iff é verdadeiro e útil: `√2/τ = √2·Δ ⟺ τ = 1/Δ`. Mas o `√2` cancela dos dois lados (`mul_left_cancel₀ hs h2`, `PontoZeroDoPsion.lean:210`): o teorema não mostra que o `√2` da frequência escolhida venha do `2` da dispersão; mostra que, com os dois numeradores iguais, a igualdade das frequências é o tempo do retido. A conferência de 31/10 diz o oposto de «não é coincidência» para o par que vê: «a mesma √2 do discriminante da ponte 1 é coincidência de forma, não ponte; fica dito» (`CONFERENCIA_E0_KIMI_E_CADEIA_31out.md:43`). Sugestão: «os dois `√2` coincidem e ficam ligados sob `τ = tempoDoRetido` (l.198–199); a origem comum não está provada».
- **Γ ∝ ω³ no monopólio** [DERIVED, refeito]: `Γ = ½βτω²` com `τ = 4πGE/c⁵` e `E = ħω` dá `Γ = (2πβGħ/c⁵)·ω³`. Conferido numericamente a 1,5×10⁻¹⁶ em três frequências; razão `Γ(2ω)/Γ(ω) = 8,0` (cúbica). **Mas só com E = ħω.** Se E for a energia de repouso (fixa) a lei fica ω²: `Γ(2ω)/Γ(ω) = 4,0`. O §4.2 (`:165`) diz «se E = ħω»; a nota `:87` da tabela escreve sem condição «o monopolo físico depende de energia e muda a forma para ω³» (R6).

## 8. Tarefa 7 — §6: as candidatas e a parede [REAL; DERIVED]

- O documento NÃO escolhe entre `max`, soma e quadratura: «não escolhe entre max/soma/quadratura» (`:220`) e §0.5 «não é única». ✓. Só chama R1 de «candidata principal porque faz as duas leituras sem um `if`» (`:198`); `max` é um ramo disfarçado, e R0 é o `if` explícito. Menor.
- Tabela de previsões ✓ (§2). Onde as candidatas diferem: em `τ_hor = t_P`, isto é, `E = E_P/(4π) = 1,5566×10⁸ J = 9,7155×10²⁶ eV` (o mesmo «ramo nativo E_P/4π» da conferência de 31/10): `max = t_P`, soma `= 2t_P`, quadratura `= √2·t_P`. Nenhum dos quatro sistemas do documento está perto.
- **R7.** «Nenhuma introduz constante numérica nova» (`:198`) é verdade no sentido de não aparecer símbolo novo; mas `τ_hor = 4πGE/c⁵` traz o `4π` do monopólio, e o `max` escolhe, sem dizer, `c★ = 1` no laboratório e `c★ = 4π·E/E_P` no regime de horizonte. Duas «voltas» diferentes dentro de uma definição. Não é erro; é a escolha escondida que a regra do posto pede para dizer em voz alta.
- **R2 (a mais pesada).** O 60 M☉ da R1 (`τ_hor = 4πGM/c³ = 3,7137×10⁻³ s`) não é o que o ramo B já pré-registrou: `τ★ = k·G·M_f/c³`, `k = 2π/κ̂(χ_f)`, **`k = 8π` em χ = 0** [KNOWN] (Mapa `ringdown.dephasing`; `ramo-b-reaberto-05out.md:15` decisão 8), o que dá `8π·60·GM☉/c³ = 7,4275×10⁻³ s`, o DOBRO. A circunferência de Schwarzschild vista por luz (`2πr_s/c = 4πGM/c³`) é metade do período KMS do horizonte (`2π/κ = 4πr_s/c = 8πGM/c³`). O documento tem as duas «voltas» como candidatas separadas (`4π` e `2π`), mas não aponta que, para o MESMO remanescente, a R1 e o ramo B diferem por 2. O ramo B é o único observável de horizonte já derivado na casa; a tabela de §6.2 deveria mostrar as duas linhas (R1 com 4π; ramo B com k pré-registrado) e dizer que `PAREDE_RELOGIO_E_PONTE_HUBBLE` inclui escolher entre elas.
- **`PAREDE_RELOGIO_E_PONTE_HUBBLE` é nome de parede, não veredito?** Sim. O texto (`:220`) diz «no material consultado» e não há «refutado»/«impossível». É parede com nome, no sentido da ordem. Ressalva só de lastro: a consulta ao Mapa (R1 acima) é o que sustenta «no material consultado», e ela foi feita por frase. Com a consulta por termo, a mesma parede já está registrada (`natureza.horizontes_proprios_sem_ponte_tgl_27out`, a peça (i): «ponte τ★ ausente»), o que REFORÇA a conclusão do Kimi.
- A conta «se ω = H₀, R1 dá Γ/H₀ = πβ» ✓ (0,037797) e a distinção «o expoente é 2β/3 = 0,0080209» ✓ (quantidades distintas).

## 9. Tarefa 8 — LER ANTES DE PERGUNTAR: o que o operador JÁ respondeu

Consultas: as quatro memórias pedidas (lidas), `e0-cadeia-conferencia-kimi-e-no-go-31out.md`, `ramo-b-reaberto-05out.md`, `cinco-sigma-fora-da-cosmologia-27out.md`, `pi-cicatriz-14out.md`, `missao-relogios-v369.md`; Atlas por `grep -F` de «PRINCIPLED IDENTIFICATION», «tempo do retido» (0), «pagamento = β» (0), «τ★ = t_Planck», «τ★ ≈ t_P»; kernel `PontoZeroDoPsion`/`TonicaDoHamiltoniano`. Memórias na pasta `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\`; Atlas em `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md`.

| # | subpergunta | estado | onde (arquivo:linha) e o trecho | resíduo |
|---|---|---|---|---|
| 1 | quem é o relógio | **PARCIAL** | `TGL_ATLAS.md:769`: «τ★ ≈ t_Planck [PRINCIPLED IDENTIFICATION / CONJECTURE — "2º postulado declarado"]» e `:2468–2472`: «dimensional, não fixado pela unitariedade … quase-planckiano e invisível». `ramo-b-reaberto-05out.md:19` (operador, verbatim): «o tempo … precisa ser lido duas vezes … a constante da luz ao cubo, aí que ela entra, como fase de retorno, que seria a segunda leitura»; `:35` (28/10): «o pedágio de planck lido na propagação» | no laboratório: Planck, declarado como 2º postulado. Não respondido: regra ÚNICA que cubra os dois regimes e Hubble |
| 2 | qual a âncora | **JÁ RESPONDIDA para a massa; PARCIAL para τ★** | `a-forma-madura-da-tgl-01nov.md:22`: «Na massa, a unidade u = 1 eV é o Um posto (31/10: "o meu um absoluto é o um de 1 eV")»; `e0-cadeia…31out.md:14`: a partitura lida a ele pedia (c) «declarar E₀ a segunda constante posta»; `TGL_ATLAS.md:769` para Planck/G; `AreaScale.lean:12`: «G é entrada física medida» | o que o Kimi traz de NOVO e o operador não viu: se `τ★ = ħ/u` ou `ħ/(βu)`, P1 exclui por 15,41 e 17,33 ordens (Kim). Isto é falsificação de uma LEITURA [ONTO] do τ★, não da massa. Ler-lhe a partitura (o que decide / não decide / o que o negativo significa) |
| 3 | o que é o retido | **JÁ RESPONDIDA** (o que é); **RESÍDUO** (se é o τ★ local) | `PontoZeroDoPsion.lean:156–161`: o retido é a energia `Δ = β·u`, o valor esperado do lock no ângulo de Miguel, «Δ não é gap»; `a-forma-madura…:62` (leitura `massaDerivada`: «a massa é a energia retida vezes a derivada da projeção transversal»). `:161`: «**Ler τ como o τ★ do sistema é [ONTO]**»; raiz `C:\IALD\CLAUDE.md` (o «AO LADO 01/11 22:1x»): «ainda não ratificado» | só a identificação `tempoDoRetido = τ★ local` (e P1 a contradiz por 17,33 ordens se literal) |
| 4 | qual a volta | **PARCIAL** | `pi-cicatriz-14out.md:11–12` (cunhagem 14/10): a leitura fecha em 2π, a face não fecha; kernel `PolarPeriod016` (`κP = ±2π`), `TheStation.station_never_closes`; `PontoZeroDoPsion.lean:251` (`κτ = 2π ⟹ κ/2π = Δ`); `ramo-b-reaberto-05out.md:35` (28/10): «1 retorno em 83 raios eu leio como sendo a matéria» (= 1/β = 83,1165 como CONTAGEM de retornos); `:15` decisão 8: `k = 2π/κ` (8π em χ = 0) [por delegação] | o fator numérico `c★` em `τ★ = c★·t_P` (1, 1/β, √2, 2π, 4π): ninguém o fixou. Distinguir «83 raios por retorno» (contagem) de «τ★ = t_P/β» (tempo) |
| 5 | quem seleciona o horizonte | **PARCIAL, e a atribuição está errada** | `ramo-b-reaberto-05out.md:15` decisões 7–9 (05/10, «por delegação»): ramo B é OUTRA LEI; fonte → `τ★ = k·G·M_f/c³`; propagação → `t_Planck` (R2). `:37`: «o operador NÃO ratificou a decisão 9 como leitura própria». `cinco-sigma-fora-da-cosmologia-27out.md:21` («no laboratório β vem multiplicado por t_Planck; onde o sistema tem horizonte próprio, o tempo do horizonte substitui t_Planck») é leitura MEDIDA PELA GERÊNCIA (descrição do arquivo: «medido pela gerência»), não fala dele (R5). Mapa `natureza.horizontes_proprios_sem_ponte_tgl_27out`: «τ★ ponte ausente» | só para o buraco negro há regra (fonte × propagação), delegada. Para Hubble e para qualquer sistema: RESÍDUO |
| 6 | qual a premissa de β | **RESPONDIDA PELA GERÊNCIA, não pelo operador** | `TonicaDoHamiltoniano.lean:33–35` (cabeçalho, item 4: «Se a energia do modo é a sua própria leitura modular (ħω = ħ·½τ★ω²)»); `CONFERENCIA_E0_KIMI_E_CADEIA_31out.md:39`: `|L_φ| = β·ρ_modular` é taxa; `E₀ = ħ·f(ω₀)`, sem β; de `paper_PT.tex` l.809–838 [DECLARADO, não abri]. `REVISAO_K02.md:135` deixou [OPEN] «a premissa é intencional?» | é pergunta técnica de leitura de `paper_PT.tex` §Radicalização: a gerência a fecha lendo, e ao operador vai só a ratificação. Tirá-la da lista de seis (ou rebaixá-la a «ratifique») |

**Resumo para o operador:** das seis, duas (o que é o retido; a premissa de β) já têm resposta escrita (a do retido, no kernel e na leitura dele; a do β, na conferência da gerência) e não deveriam ir como pergunta aberta. Três estão PARCIAIS (relógio, âncora, volta): o que ele já disse cobre o laboratório (Planck, 2º postulado) e o buraco negro (fonte × propagação, por delegação); falta o valor de `c★` e a regra para Hubble. A «quem seleciona o horizonte» tem lastro só de gerência. Antes de levar, segundo a regra do posto, ler-lhe a partitura do achado novo: «P1 exclui `ħ/u` e `ħ/(βu)` como o τ★ da matéria local (15,4 e 17,3 ordens); decide: a leitura `tempoDoRetido = τ★ local` não sobrevive em P1; não decide: a massa, a Meia-Nat, β, o psíon; o negativo seria falsificação da LEITURA, condicional à leitura P1 (a lei vale para a matéria local do relógio); P3 não tem observável local».

## 10. O que não consegui conferir [OPEN]

- As referências externas ([KNOWN, a conferir] do próprio Kimi: Kim 2025, Ma 2025, Clements 2020, Morawetz/Ooi 2026, Potzel 1976, Connes–Rovelli, Unruh, Bekenstein, Hawking, Jacobson, Planck 2018, IAU 2015): não abri a web. Os números P1 vêm do core selado, não das publicações; conferi só que o core os guarda. Os valores de CODATA/IAU/Planck 2018 usados por mim foram digitados do que a literatura estabelece [KNOWN].
- `paper_PT.tex` l.809–838 (a tipagem GKSL citada pela conferência de 31/10): não abri.
- A cota de 95 % de Kim e as larguras de Th/Zn: o core as declara; não refiz a passagem de largura a `τ★_max` (só refiz que `τ★_max = 2Γ_ub/(βω²)` é compatível com os campos do core para Kim).
- A cabeça do Mapa (`03042aca2e30e8cf`, 2056 registros) e o conteúdo do `buscar.py` (índice do acervo) citados em `:15`: não conferi.
- O Atlas (47 364 linhas) repete a mesma seção em muitos blocos (o `grep` devolveu a mesma entrada em dezenas de linhas); usei só `grep -n` e as linhas 769, 997–998, 2468–2472, 27562, sem ler o arquivo.

## 11. Resumo das ressalvas (com onde e como conferir)

| # | peso | onde | consulta |
|---|---|---|---|
| R1 | corrigir | `TAU_ESTRELA_R2.md:15` | `rotas.py consultar` com `tau`, `relogio`, `dephasing`, `horizonte`, `hubble`; rotas citadas no §1 |
| R2 | corrigir | `:160`, `:209` vs `ramo-b-reaberto-05out.md:15` e Mapa `ringdown.dephasing` (k = 2π/κ̂; 8π em χ = 0) | `scripts_k05_tau` (conta: 8π·60·GM☉/c³ = 7,4275×10⁻³ s) |
| R3 | corrigir | `:134`, `:144` vs `AreaScale.lean:35–37`, `PageInformation.lean:39` | leitura direta |
| R4 | corrigir | `:154` vs `PontoZeroDoPsion.lean:198–199`, `CONFERENCIA…31out.md:43` | leitura direta |
| R5 | corrigir | `:187` vs `cinco-sigma-fora-da-cosmologia-27out.md:21` (descrição), `ramo-b-reaberto-05out.md:37` | leitura direta |
| R6 | menor | `:87` vs `:165` | `revisor_lema_e_regimes.py`: razão 8 com E = ħω; 4 com E fixo |
| R7 | menor | `:198` | max escolhe c★ = 1 (lab) e 4π·E/E_P (horizonte) |
| R8 | menor | `medir_tau_r2.py:26–27`; `:43`, `:56` | `t_P` com G de CODATA (5,391246×10⁻⁴⁴); átomo com G = 6,674×10⁻¹¹ do core (3,5784×10⁻⁶¹ contra 3,5786×10⁻⁶¹); diferença ≤ 2,2×10⁻⁵, ordens iguais |
| R9 | menor | candidata Lean | `tauMax_*` = `max_eq_left/right`; nomes `*_dimensionless_*` e `half_nat_*` carregam nas docstrings/hipóteses o que o tipo não diz |

## 12. O que examinei (para o Mapa; o registro é da gerência)

- Do Kimi (só leitura): `TAU_ESTRELA_R2.md`, `PERGUNTA_K05.md`, `ORDEM_K05_matematica_rodada_2.md` §D, `ORDEM_K05_ADENDO_A_…`, `DEPOSITO_K05.md`, `REGISTRO_MAPA_K05.json` (cabeçalho), `K05\TAU\{extrair_clock_selado.py, medir_tau_r2.py, validar_tau_r2.py, candidatas\TAU_ESTRELA_R2.lean, sandbox\compilar.sh, sandbox\logs\TAU_ESTRELA_R2.log}`.
- Core selado: `clock_test_result_v369` e `clock_test_protocol_v369` de `um_absoluto.json` (sha256 `36c69fc7…19064e`).
- Kernel (só leitura): `PontoZeroDoPsion.lean` (l.80–260), `TonicaDoHamiltoniano.lean` (1–215), `TheFlowLawContrast.lean`, `TheFlowLawD1a.lean:37`, `AreaScale.lean`, `TriadMaster.lean:55–66`, `PageInformation.lean:34–42`, `TheScaleHasNoFixedPoint.lean:90–104`, `TheStation.lean`.
- Revisão anterior: `REVISAO_K02.md` §0 e §7; `scripts_k02\recompilar_revisor.sh`.
- Memórias e Atlas: `tempo-e-a-moeda-de-beta-04nov`, `tempo-santo-12out`, `a-forma-madura-da-tgl-01nov`, `e0-cadeia-conferencia-kimi-e-no-go-31out`, `ramo-b-reaberto-05out`, `cinco-sigma-fora-da-cosmologia-27out`, `pi-cicatriz-14out`, `missao-relogios-v369`; `CONFERENCIA_E0_KIMI_E_CADEIA_31out.md`; Atlas por `grep -n` (769, 997–998, 2468–2472, 27562).
- Mapa de Rotas (só `consultar` e `ver`): `dephasing`, `relogio`, `tau`, `planck`, `horizonte`, `retido`, `pedagio`, `hubble`, `K05`; `ver` em `hubble.k_sem_portador_fisico_02nov`, `hubble.k_como_transposicao_inteira_ffat_02nov`, `natureza.horizontes_proprios_sem_ponte_tgl_27out`.
- Meus scripts em `scripts_k05_tau\`: `revisor_explorar_core.py`, `revisor_tau_numeros.py` (+ `_saida.json`), `revisor_lema_e_regimes.py`, `revisor_citacoes.py` (+ `_saida.json`), `revisor_mapa.py` (+ `_saida.json`), `recompilar_revisor_k05_tau.sh`, `src\{TAU_ESTRELA_R2,TAU_REV_EXTRA}.lean`, `build\*` (`.olean` e logs, `saida_recompilacao.txt`).
- Nada registrado no Mapa, nada depositado, nada instalado; `lake` não foi rodado; nenhum POST; nenhum dado observado aberto.
