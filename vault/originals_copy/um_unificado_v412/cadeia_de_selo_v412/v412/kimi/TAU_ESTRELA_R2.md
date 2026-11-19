# K05 — τ★, rodada 2: o relógio selado, a âncora e o número puro

**Escopo.** Seção D de K05 e ligação do ADENDO a `√2`. Levantamento e derivação condicional; nada promovido a teorema físico, nada instalado, registrado ou depositado. Nenhum dado observado foi reaberto e nenhuma estatística observada foi refeita. Os números deste relatório vêm de `K05/TAU/medir_tau_r2.py`, com `β = ALPHA_FINE_CODATA_2018 × sqrt(e)` em runtime.

## 0. Resposta curta

1. **[DERIVED sobre registro selado]** Em P1, `ħ/(1 eV)` excede a cota de 95 % de Kim2025 por `2,55×10^15` (`15,4058` ordens), e `ħ/(β·1 eV)` por `2,12×10^17` (`17,3255` ordens). Entre as quatro leituras principais `t_P`, `t_P/β`, `ħ/u`, `ħ/(βu)`, só as duas ancoradas em Planck/G passam. Isso não se generaliza a todo ramo gravitacional: o tempo do átomo e o monopolo de 1 eV também passam; Unruh-g e `GM⊕/c³` falham.
2. **[DERIVED]** Os cinco fatores `c★ = 1, 1/β, √2, 2π, 4π` sobre `t_P` passam em todas as cotas P1 lidas. O maior deles, `1/β`, ainda fica `10,7612` ordens abaixo da cota de Kim e `7,34993` abaixo da cota nominal de Zn. O relógio não escolhe `c★`.
3. **[REAL no sandbox]** A candidata Lean compila com `rc=0`, zero `sorry`/`sorryAx`, e prova a análise dimensional, `G ↔ N=E_P/u`, a álgebra condicional da célula `√2`, a frequência canônica `2/(βτ)` e o termo cúbico do monopolo. O kernel anterior cobre o no-go de escala, mas não enunciava todo esse lema dimensional.
4. **[REAL no kernel + DERIVED]** O `√2` de `ω★=√2/τ` e o da dispersão `ω²=2βR` são ligados pelo teorema da linha 199 **se e somente se** `τ=tempoDoRetido`. O `√2` da célula `A=2ℓ_P²` é outra cadeia: área não basta para definir travessia, e nenhuma ponte com o psíon foi encontrada.
5. **[DECLARADO — candidata; OPEN como derivação]** `τ_eff=max(t_P,τ_hor)` é UMA definição tipada que devolve Planck para 1 eV e Sr, e horizonte para 60 M☉ e Hubble, sem nova constante numérica. Mas ela não é única (`soma` e `quadratura` dão os mesmos limites), depende de nomear o horizonte e **não deriva** `K=E(z*)^(2β/3)`. A parede é `PAREDE_RELOGIO_E_PONTE_HUBBLE`.

## 1. Aferição e fronteira do trabalho

**[REAL — consultas]** Foram consultados, nesta ordem: Mapa de Rotas (`tau estrela relogio Planck horizonte retido`, `horizonte proprio dois regimes tau Hubble K E z`, `analise dimensional hbar c G tempo Planck N EP u`: todas `n=0`, cabeça `03042aca2e30e8cf`, 2056 registros); inventário da bancada; kernel; Atlas; índice do acervo. O índice devolveu zero para os quatro nomes da nova candidata dimensional (`no_time_from_hbar_c`, `unique_planck_exponents`, `dimensionless_ratio_mul_planck`, `newton_eq_of_dimensionless_ratio`), entre 13.608 documentos filtrados. As memórias pedidas estão na memória da gerência, não no índice do acervo (`missao-relogios-v369`: zero no índice, arquivo localizado e lido diretamente).

O inventário K02 anterior e a revisão inteira foram lidos. A conclusão de ausência é limitada: **os módulos consultados não enunciam o lema dimensional completo**; não se afirma que nenhum princípio futuro possa fechá-lo. [TAU_ESTRELA](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fcadeia_de_selo%2Fv412%2Fkimi%2FTAU_ESTRELA.md&line=41&text=Invent%C3%A1rio%20tem%C3%A1tico%20de%20todas%20as%20leituras%2Ftentativas%20encontradas "citation"), [REVISAO_K02](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fcadeia_de_selo%2Fv412%2Frevisao%2FREVISAO_K02.md&line=123&text=%CF%84%E2%98%85 "citation")

O core foi lido por `K05/TAU/extrair_clock_selado.py`; SHA-256 lido por script: `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`. O extrato preserva as duas ocorrências de `clock_test_result_v369`; a análise usa a ocorrência completa em `core.clock_test_result_v369`.

## 2. O que o relógio selado decide

### 2.1 Cotas: não há uma única cota “Zn/Th”

**[REAL — leitura de campos selados]** Kim2025 tem `tau_star_max_s = 2,585701911772075×10^-31 s`, 95 %; Ma2025 tem `1,5236679465435584×10^-31 s`, nominal. O registro P1 atual também contém Al, duas determinações de Th e Zn. [um_absoluto](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Fum_absoluto.json&text=%22tau_star_max_s%22%3A%202.585701911772075e-31 "citation")

| plataforma | identificador | cota τ★ (s) | tipo |
|---|---|---:|---|
| ⁸⁷Sr, Kim2025 | `sr87_kim2025` | `2,5857×10^-31` | 95 % |
| ⁸⁷Sr, Ma2025 | `sr87_ma2025` | `1,5237×10^-31` | nominal |
| ²⁷Al⁺, Clements2020 | `al27_clements2020` | `4,1960×10^-31` | nominal |
| ²²⁹Th, Morawetz2026 | `th229_morawetz2026` | `3,0556×10^-25` | 95 % |
| ²²⁹Th, Ooi2026 | `th229_ooi2026` | `1,0255×10^-25` | 95 % |
| ⁶⁷Zn, Potzel1976 | `zn67_potzel1976` | `1,0030×10^-34` | nominal; Mössbauer, não relógio |
| registro auxiliar do Atlas | `atlas_legacy_1p8e_m33` | `1,8000×10^-33` | registro não reavaliado |

O `τ★≲1,8×10^-33 s` está no verbete ²²⁹Th do Atlas. Ele **não coincide** com as cotas Th atuais do core nem com a cota Zn; fica preservado como registro auxiliar, sem fundir fontes nem substituir o core. [TGL_ATLAS](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fmemory%2FTGL_ATLAS.md&line=997&text=%CF%84%E2%98%85%20%E2%89%B2%201%2C8%C3%9710%E2%81%BB%C2%B3%C2%B3%20s "citation"), [missao-relogios-v369](kimi-cite://md-line?path=C%3A%2FUsers%2Frotol%2F.claude%2Fprojects%2Fc--IALD-Central-de-Patentes%2Fmemory%2Fmissao-relogios-v369.md&line=46&text=Zn%209%2C27%20NOMINAL "citation")

Referências das plataformas, todas **[KNOWN, a conferir]** no sentido desta entrega, pois foram lidas do registro e não reabertas: Kim et al. 2025, *PRL* 135, 103601, arXiv:2505.06444, DOI `10.1103/3wtv-sty2`; Ma et al. 2025, *PRX Quantum* 6, 040340, arXiv:2505.06437, DOI `10.1103/2rqf-r9gw`; Clements et al. 2020, *PRL* 125, 243602, arXiv:2007.02193; Morawetz et al. 2026, arXiv:2604.16640v2; Ooi et al. 2026, *Nature* 650, 72, arXiv:2507.01180; Potzel–Forster–Kalvius 1976, *J. Phys. Colloq.* 37, C6-691, DOI `10.1051/jphyscol:19766143`.

### 2.2 Todas as leituras numericamente determinadas do inventário e das alternativas

As células mostram `τ/cota; log10(τ/cota); veredito`. **Positivo = falha em P1; negativo = passa em P1.** “Passa” significa somente “não excluído condicionalmente”, nunca detectado ou confirmado. `t_P=5,3912464483×10^-44 s` é recomputado de `ħ,G,c`; `β=0,012031300400803142`.

| leitura | τ (s) | Sr Kim 95 % | Sr Ma nominal | Al nominal |
|---|---:|---:|---:|---:|
| `c★=1` | `5,391×10^-44` | `2,09×10^-13; −12,68; PASSA` | `3,54×10^-13; −12,45; PASSA` | `1,28×10^-13; −12,89; PASSA` |
| `c★=1/β` | `4,481×10^-42` | `1,73×10^-11; −10,76; PASSA` | `2,94×10^-11; −10,53; PASSA` | `1,07×10^-11; −10,97; PASSA` |
| `c★=√2` | `7,624×10^-44` | `2,95×10^-13; −12,53; PASSA` | `5,00×10^-13; −12,30; PASSA` | `1,82×10^-13; −12,74; PASSA` |
| `c★=2π` | `3,387×10^-43` | `1,31×10^-12; −11,88; PASSA` | `2,22×10^-12; −11,65; PASSA` | `8,07×10^-13; −12,09; PASSA` |
| `c★=4π`* | `6,775×10^-43` | `2,62×10^-12; −11,58; PASSA` | `4,45×10^-12; −11,35; PASSA` | `1,61×10^-12; −11,79; PASSA` |
| `ħ/u`, `u=1 eV` | `6,582×10^-16` | `2,55×10^15; +15,41; FALHA` | `4,32×10^15; +15,64; FALHA` | `1,57×10^15; +15,20; FALHA` |
| `ħ/(βu)`, `u=1 eV` | `5,471×10^-14` | `2,12×10^17; +17,33; FALHA` | `3,59×10^17; +17,56; FALHA` | `1,30×10^17; +17,12; FALHA` |
| Unruh-g, `2πc/g` | `1,921×10^8` | `7,43×10^38; +38,87; FALHA` | `1,26×10^39; +39,10; FALHA` | `4,58×10^38; +38,66; FALHA` |
| `GM⊕/c³` | `1,479×10^-11` | `5,72×10^19; +19,76; FALHA` | `9,71×10^19; +19,99; FALHA` | `3,53×10^19; +19,55; FALHA` |
| `GM(⁸⁷Sr)/c³`, `A·m_u` | `3,578×10^-61` | `1,38×10^-30; −29,86; PASSA` | `2,35×10^-30; −29,63; PASSA` | `8,53×10^-31; −30,07; PASSA` |
| monopolo `4πG(1 eV)/c⁵` | `5,549×10^-71` | `2,15×10^-40; −39,67; PASSA` | `3,64×10^-40; −39,44; PASSA` | `1,32×10^-40; −39,88; PASSA` |

| leitura | τ (s) | Th Morawetz 95 % | Th Ooi 95 % | Zn nominal |
|---|---:|---:|---:|---:|
| `c★=1` | `5,391×10^-44` | `1,76×10^-19; −18,75; PASSA` | `5,26×10^-19; −18,28; PASSA` | `5,38×10^-10; −9,27; PASSA` |
| `c★=1/β` | `4,481×10^-42` | `1,47×10^-17; −16,83; PASSA` | `4,37×10^-17; −16,36; PASSA` | `4,47×10^-8; −7,35; PASSA` |
| `c★=√2` | `7,624×10^-44` | `2,50×10^-19; −18,60; PASSA` | `7,43×10^-19; −18,13; PASSA` | `7,60×10^-10; −9,12; PASSA` |
| `c★=2π` | `3,387×10^-43` | `1,11×10^-18; −17,96; PASSA` | `3,30×10^-18; −17,48; PASSA` | `3,38×10^-9; −8,47; PASSA` |
| `c★=4π`* | `6,775×10^-43` | `2,22×10^-18; −17,65; PASSA` | `6,61×10^-18; −17,18; PASSA` | `6,75×10^-9; −8,17; PASSA` |
| `ħ/u`, `u=1 eV` | `6,582×10^-16` | `2,15×10^9; +9,33; FALHA` | `6,42×10^9; +9,81; FALHA` | `6,56×10^18; +18,82; FALHA` |
| `ħ/(βu)`, `u=1 eV` | `5,471×10^-14` | `1,79×10^11; +11,25; FALHA` | `5,33×10^11; +11,73; FALHA` | `5,45×10^20; +20,74; FALHA` |
| Unruh-g, `2πc/g` | `1,921×10^8` | `6,29×10^32; +32,80; FALHA` | `1,87×10^33; +33,27; FALHA` | `1,92×10^42; +42,28; FALHA` |
| `GM⊕/c³` | `1,479×10^-11` | `4,84×10^13; +13,68; FALHA` | `1,44×10^14; +14,16; FALHA` | `1,47×10^23; +23,17; FALHA` |
| `GM(⁸⁷Sr)/c³`, `A·m_u` | `3,578×10^-61` | `1,17×10^-36; −35,93; PASSA` | `3,49×10^-36; −35,46; PASSA` | `3,57×10^-27; −26,45; PASSA` |
| monopolo `4πG(1 eV)/c⁵` | `5,549×10^-71` | `1,82×10^-46; −45,74; PASSA` | `5,41×10^-46; −45,27; PASSA` | `5,53×10^-37; −36,26; PASSA` |

| leitura | Atlas auxiliar `1,8×10^-33 s`: `τ/cota; ordens; veredito` |
|---|---:|
| `c★=1` | `3,00×10^-11; −10,52; PASSA` |
| `c★=1/β` | `2,49×10^-9; −8,60; PASSA` |
| `c★=√2` | `4,24×10^-11; −10,37; PASSA` |
| `c★=2π` | `1,88×10^-10; −9,73; PASSA` |
| `c★=4π`* | `3,76×10^-10; −9,42; PASSA` |
| `ħ/u` | `3,66×10^17; +17,56; FALHA` |
| `ħ/(βu)` | `3,04×10^19; +19,48; FALHA` |
| Unruh-g | `1,07×10^41; +41,03; FALHA` |
| `GM⊕/c³` | `8,22×10^21; +21,91; FALHA` |
| `GM(⁸⁷Sr)/c³` | `1,99×10^-28; −27,70; PASSA` |
| monopolo de 1 eV | `3,08×10^-38; −37,51; PASSA` |

`*` A linha `4π` usa P1 apenas no sentido de uma constante em `τ=c★t_P` dentro da lei `ω²`. O monopolo físico depende de energia e muda a forma para `ω³`; a comparação P1 não se transporta automaticamente a essa outra lei.

As três alternativas `Γ` do core foram reproduzidas por álgebra, sem estatística nova: Unruh-g, Terra e átomo de Sr, com diferença relativa máxima `0` entre a fórmula e o campo selado. O protocolo nomeia expressamente `t_P`, `t_P/β`, Unruh-g, `GM⊕/c³` e `GM(átomo)/c³`. [um_absoluto](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Fum_absoluto.json&text=t_P%20%28canonico%29%2C%20t_P%2Fbeta%20%28Artigo%20A%29 "citation")

### 2.3 Inventário sem número determinado

| leitura do inventário | por que não entra na razão numérica |
|---|---|
| KMS/Unruh genérico | exige aceleração, temperatura ou energia de referência |
| ancoragem no produto cruzado | localiza onde uma escala pode entrar, não seu valor |
| `Γ_B=β/τ★` | identidade em `ω★=√2/τ★`, não determinação de `τ★` |
| autoconsistência `ω=2/τ★` | fixa frequência dada `τ★`, não `τ★` |
| Grande Atrator `M=M` | autoconsistência, não nova âncora |
| disco de Euler `E★=(ħ²K)^(1/3)` | faltam `K` e a identificação do disco físico |
| lei de raízes | `τ★` cancela na transposição |
| forma `Γ=½βτ★ω²` | a forma não fixa a escala |

### 2.4 P3 universal

**[REAL — protocolo]** P3 usa o Hamiltoniano total e um tempo estocástico comum: o protocolo registra “nenhum local”, porque é reparametrização do tempo; comparações de relógios e interferômetros são cegos por construção, veredito `P3_NO_LOCAL_OBSERVABLE`. Logo as exclusões numéricas acima são P1, não P3. [um_absoluto](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Fum_absoluto.json&text=P3_NO_LOCAL_OBSERVABLE%20%28nao%20e%27%20teste%3B%20e%27%20dito%20como%20tal%29 "citation")

## 3. Lema dimensional: âncora não é número puro

**Lema D.** Em dimensões `(M,L,T)`:

1. `ħ^a c^b` não pode ter dimensão de tempo com números puros `a,b`: `a=0`, `2a+b=0` e `−a−b=1` são incompatíveis.
2. Com `G`, os expoentes de `ħ^aG^bc^d` que formam tempo são únicos: `a=b=1/2`, `d=−5/2`, isto é `t_P=√(ħG/c⁵)`.
3. Uma energia posta `u` fornece a outra âncora possível `τ_u=ħ/u`.
4. Definindo `E_P=√(ħc⁵/G)` e `N=E_P/u`, tem-se `τ_u=N t_P`; para o retido, `ħ/(βu)=(N/β)t_P`.
5. Fixados `ħ,c,u`, medir `G` ou medir o número puro `N` é equivalente: `N u=E_P` e `G=ħc⁵/(N²u²)`. Para `u=1 eV`, o script dá `N=1,2208901286×10^28`.

**[DERIVED — separação obrigatória]** “Derivar τ★” tem dois sentidos: (i) **escolher a âncora** — `G` medido ou `u` posto, não teorema; (ii) **derivar o número puro** `c★` em `τ★=c★t_P`. O relógio restringe (i) em P1; não resolve (ii).

`TheScaleHasNoFixedPoint` prova que uma quantidade positiva não é invariante sob todo reescalonamento; não prova os expoentes dimensionais nem `N=E_P/u`. [TheScaleHasNoFixedPoint](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTheScaleHasNoFixedPoint.lean&text=theorem%20no_positive_scale_invariant "citation") `TonicaDoHamiltoniano` prova que nenhuma função da inscrição `(c,θ)` fixa `E₀`, e também tipa monopolo e autoconsistência; tampouco contém o lema D inteiro. [TonicaDoHamiltoniano](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&text=theorem%20no_function_of_the_inscription_fixes_E0 "citation")

A equivalência algébrica `newtonPlanck_equivalence` de `TGL.AreaScale` também declara que `G` é entrada medida, não derivada. [AreaScale](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGL%2FAreaScale.lean&text=theorem%20newtonPlanck_equivalence "citation")

**[REAL no sandbox]** A candidata `K05/TAU/candidatas/TAU_ESTRELA_R2.lean` cobre o lema D sem `sorry`; `planckTime_sq`, `gap_time_is_dimensionless_ratio_mul_planck`, `newton_eq_of_dimensionless_ratio` e `dimensionless_ratio_eq_of_newton` são os enunciados principais.

## 4. Os candidatos ao número puro `c★`

Nenhum candidato é escolhido por dado. As margens abaixo são `log10(cota/τ)`, em ordens, contra Kim 95 % e Zn nominal.

| candidato | cadeia e hipótese NOMEADA | τ (s) | Kim | Zn | veredito |
|---|---|---:|---:|---:|---|
| `1` | `H_CANONE_PLANCK`: corte UV/Planck e identificação principiada `τ★=t_P` | `5,391×10^-44` | 12,68 | 9,27 | passa |
| `1/β` | `H_ARTIGO_A_FLUXO`: o tempo do fluxo `1/β` lido sobre `t_P`; não é `ħ/(βu)` sem `u=E_P` | `4,481×10^-42` | 10,76 | 7,35 | passa |
| `√2` | `H_CELULA_MEIA_NAT` + `H_TRAVESSIA_QUADRADA`: Meia-Nat é a entropia da célula e há uma travessia de luz do lado quadrado | `7,624×10^-44` | 12,53 | 9,12 | passa; derivação física aberta |
| `2π` | `H_VOLTA_KMS`: `τ★` é a volta modular inteira, não só o passo | `3,387×10^-43` | 11,88 | 8,47 | passa |
| `4π` | `H_MONOPOLO`: `τ★=4πGE/c⁵`; `c★=4π` só se `E=E_P` | `6,775×10^-43` | 11,58 | 8,17 | passa como constante; outra lei se `E=ħω` |

O artigo pede explicitamente o corte UV/Planck, mas isso não deriva por si só `c★=1`. [A Ponte Einstein Cartan Miguel](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&text=escala%20%24%5Ctau_%5Cstar%24%20%28dimensional%3A%20exige%20o%20corte%20UV%2FPlanck%29 "citation") O período `2π` é uma hipótese de volta: `o_relogio_do_retido`, por exemplo, mostra que **se** `κ` dá uma volta em `τ`, então `κ/(2π)=Δ`; não mostra `τ★=2πt_P`. [PontoZeroDoPsion](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPontoZeroDoPsion.lean&text=theorem%20o_relogio_do_retido "citation") A condição KMS/Unruh é referência externa: Connes–Rovelli 1994, arXiv:gr-qc/9406019; Unruh 1976, *Phys. Rev. D* 14, 870, DOI `10.1103/PhysRevD.14.870`, ambos **[KNOWN, a conferir]**.

### 4.1 `√2`: Clausius, célula, dispersão e segunda derivação da massa

**Cadeia da célula [DERIVED sob hipóteses].**

`S=A/(4ℓ_P²)` e `S=1/2` implicam apenas `A=2ℓ_P²`. Para obter `τ=√2t_P` são necessárias mais duas identificações: (i) a Meia-Nat é a entropia dessa célula de horizonte; (ii) a célula é quadrada e o tempo é UMA travessia de luz do seu lado, `τ=√A/c`. Então `√A=√2ℓ_P` e `ℓ_P/c=t_P`. Área sozinha não escolhe forma nem tempo de travessia.

O kernel tem `dS=dA/(4G)` como campo de `HorizonEquilibriumData`, não a identificação global `S=A/(4ℓ_P²)` com a Meia-Nat. [TriadMaster](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTriadMaster.lean&text=area_entropy%20%3A%20dS%20%3D%20dA%20%2F%20%284%20%2A%20G%29 "citation") `PageInformation` diz expressamente que a composição plena `S_BH=A/4G` com `S_∂=½ nat` é leitura/futuro, não teorema desse módulo. [PageInformation](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPageInformation.lean&text=a%20composi%C3%A7%C3%A3o%0Aplena%20%C3%A9%20leitura%2Ffuturo "citation") Bekenstein 1973, *Phys. Rev. D* 7, 2333, DOI `10.1103/PhysRevD.7.2333`; Hawking 1975, *Commun. Math. Phys.* 43, 199, DOI `10.1007/BF02345020`; Jacobson 1995, *PRL* 75, 1260, arXiv:gr-qc/9504004 — **[KNOWN, a conferir]**.

**Cadeia do psíon [REAL no kernel].** `omegaSq β R := 2βR` e `pagamentoComoCurvatura β u := βu²` dão `ω_psíon=√2βu`; então `½ω_psíon=β·sen45°·u`, a segunda derivação da massa. O fator 2 da dispersão é indispensável: sem ele haveria `β/2`, não a projeção `β·sen45°`. [PontoZeroDoPsion](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPontoZeroDoPsion.lean&text=theorem%20the_mass_is_the_zero_point "citation")

**Ligação do ADENDO.** A linha 199 prova

`√2/τ = ω_psíon  ⇔  τ = tempoDoRetido = 1/Δ` (unidades naturais; em SI, `ħ/Δ`).

Portanto o `√2` da frequência do sistema e o `√2` da dispersão são o **mesmo fator algébrico ligado pelo teorema**, sob a condição `τ=tempoDoRetido`; não é mera coincidência nessa cadeia. [PontoZeroDoPsion](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPontoZeroDoPsion.lean&text=Real.sqrt%202%20%2F%20%CF%84%20%3D%20Real.sqrt%20%28omegaSq "citation")

Isso **não** implica `τ★=√2t_P`, nem liga a célula de área ao psíon. Pelo contrário: identificar o `τ` da linha 199 ao `τ★` da matéria local impõe `τ★=ħ/(βu)`, que falha P1 por `17,33` ordens em Kim e `20,74` em Zn. O próprio comentário do módulo marca essa identificação como `[ONTO]`, não ratificada. A pedra não foi alterada.

### 4.2 `4π`: energia e mudança de expoente

`TonicaDoHamiltoniano` prova `4πGE/c⁵=2πr_s/c`, com `r_s=2GE/c⁴`. Em termos de `E_P`, `τ_mon=4πt_P(E/E_P)`. Assim:

- `E=E_P` dá `c★=4π`;
- o ramo nativo `E=E_P/(4π)` devolve `c★=1`, não `4π`;
- para 1 eV, `τ_mon=5,549×10^-71 s=1,029×10^-27t_P`;
- se `E=ħω`, então `Γ=½βτ_monω²=(2πβGħ/c⁵)ω³`: a lei deixa `ω²` e passa a `ω³`.

[TonicaDoHamiltoniano](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&text=theorem%20monopole_time_is_the_horizon_light_time "citation") A última identidade também está compilada na candidata desta rodada.

## 5. As três frequências e o β

| frequência | premissa e fonte | estatuto |
|---|---|---|
| `ω★=√2/τ★` | escolha da “frequência do próprio sistema”; `gammaB_is_the_canonical_law_at_the_systems_frequency`, `TonicaDoHamiltoniano` 144–148; linha 199 do psíon liga ao retido | identidade na lei canônica: `Γ_B=β/τ★` |
| `ω=2/τ★` | `ħω=ħ·½τ★ω²`, `self_consistent_readout_fixes_the_frequency`, `TonicaDoHamiltoniano` 165–173 | teorema exato **sem β na premissa** |
| `ω=2/(βτ★)` | nova derivação: impor `Γ=ω` à lei canônica `Γ=½βτ★ω²`, com `β,τ,ω≠0` | compilada na candidata R2; é `1/β` vezes a anterior |

Com `τ=t_P`, o script dá respectivamente `2,623×10^43`, `3,710×10^43` e `3,083×10^45 rad/s`; a razão entre a terceira e a segunda é `1/β=83,1165`. [TonicaDoHamiltoniano](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&text=theorem%20self_consistent_readout_fixes_the_frequency "citation")

**Por que o β falta na segunda?** Pelo texto, é intencional como **outra premissa**: “a energia do modo é a sua própria leitura modular”, não a equação `ħω=ħΓ` da taxa canônica. A conferência de 31/10 corrige `|L_φ|` para taxa, escreve `f(ω)=½τ★ω²` e depois usa `E₀=ħf(ω₀)` na leitura autoconsistente. Isso explica a forma sem alterar o kernel. [CONFERENCIA_E0_KIMI_E_CADEIA_31out](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fe0_cadeia_31out%2FCONFERENCIA_E0_KIMI_E_CADEIA_31out.md&line=39&text=E%E2%82%80%20%3D%20%C4%A7%C2%B7f%28%CF%89%E2%82%80%29%20%3D%20%C4%A7%C2%B7%C2%BD%CF%84%E2%98%85%CF%89%E2%82%80%C2%B2 "citation")

O que permanece **[OPEN]** é a decisão física: a autoconsistência pretendida é essa leitura modular sem β ou é `Γ=ω` com a lei canônica? A revisão K02 formula exatamente essa pergunta; nenhuma fonte foi “corrigida” aqui. [REVISAO_K02](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fcadeia_de_selo%2Fv412%2Frevisao%2FREVISAO_K02.md&line=135&text=a%20premissa%20%C3%A9%20intencional%3F "citation")

**Cancelamentos de 31/10 não se confundem.** Na rota do monopolo, `𝓕=βR_B` e `R_B=cτ★/β` fazem β cancelar em `E=c⁵τ★/(4πG)`. Isso não autoriza retirar β da lei canônica. [CONFERENCIA_E0_KIMI_E_CADEIA_31out](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fe0_cadeia_31out%2FCONFERENCIA_E0_KIMI_E_CADEIA_31out.md&line=44&text=sob%20%F0%9D%93%95%20%3D%20%CE%B2R_B%20e%20R_B%20%3D%20c%CF%84%E2%98%85%2F%CE%B2 "citation") Outro cancelamento, `Γ(ħ/(βu),u/ħ)=u/(2ħ)`, é a álgebra do tempo do retido já compilada em K02; também não muda a premissa autoconsistente.

## 6. Uma definição para os dois regimes?

As falas de 27/10 e 28/10 pedem duas leituras: Planck no laboratório; horizonte próprio onde ele existe; e o pedágio de Planck lido na propagação. [cinco-sigma-fora-da-cosmologia-27out](kimi-cite://md-line?path=C%3A%2FUsers%2Frotol%2F.claude%2Fprojects%2Fc--IALD-Central-de-Patentes%2Fmemory%2Fcinco-sigma-fora-da-cosmologia-27out.md&line=21&text=no%20laborat%C3%B3rio%20%CE%B2%20vem%20multiplicado%20por%20t_Planck "citation"), [ramo-b-reaberto-05out](kimi-cite://md-line?path=C%3A%2FUsers%2Frotol%2F.claude%2Fprojects%2Fc--IALD-Central-de-Patentes%2Fmemory%2Framo-b-reaberto-05out.md&line=35&text=ped%C3%A1gio%20de%20planck%20lido%20na%20propaga%C3%A7%C3%A3o "citation")

### 6.1 Candidatas tipadas

Para um sistema `S` com energia `E_S`, define-se `τ_hor(S)=4πG E_S/c⁵` (o horizonte/monopolo já inventariado). As candidatas, todas **[DECLARADO]**, são:

- **R0 — seletor:** `τ_eff=t_P` se não há horizonte próprio; `τ_eff=τ_H` se há. Hipótese `H_SELETOR_HORIZONTE`.
- **R1 — piso/max:** `τ_eff=max(t_P,τ_hor)`. Hipóteses `H_PISO_PLANCK` e `H_HORIZONTE_MONOPOLO`.
- **R2 — soma:** `τ_eff=t_P+τ_hor`.
- **R3 — quadratura:** `τ_eff=√(t_P²+τ_hor²)`.

Nenhuma introduz constante numérica nova. R1 é a única apresentada como definição candidata principal porque faz as duas leituras sem um `if`, mas R0/R2/R3 mostram que a forma funcional não é derivada nem única. Para Hubble usa-se, apenas como hipótese cosmológica nomeada `H_HUBBLE_CRITICO`, a massa dentro do raio de Hubble com densidade crítica: `E_H=c⁵/(2GH₀)`, logo `τ_hor=2π/H₀`.

### 6.2 Previsões das candidatas

Os números usam `GM☉=1,3271244×10^20 m³s^-2` [IAU 2015, Resolução B3; KNOWN, a conferir], `H₀=67,4 km s^-1 Mpc^-1` apenas como benchmark publicado de Planck 2018 [Planck Collaboration 2020, arXiv:1807.06209; KNOWN, a conferir], e `A·m_u` para Sr como no protocolo. Não são ajustes.

| sistema | `τ_hor` (s) | `max(t_P,τ_hor)` (s) | `max/t_P` | leitura |
|---|---:|---:|---:|---|
| 1 eV | `5,549×10^-71` | `5,391×10^-44` | 1 | Planck; o horizonte é sub-Planck |
| Sr, energia da transição P1 | `9,850×10^-71` | `5,391×10^-44` | 1 | Planck |
| Sr, massa de repouso `A·m_u` | `4,497×10^-60` | `5,391×10^-44` | 1 | Planck |
| remanescente 60 M☉ | `3,714×10^-3` | `3,714×10^-3` | `6,888×10^40` | horizonte; `GM/c³=2,955×10^-4 s` antes do `4π` |
| Hubble, `H_HUBBLE_CRITICO` | `2,877×10^18` | `2,877×10^18` | `5,336×10^61` | horizonte; `1/H₀=4,578×10^17 s` |

R2 e R3 reproduzem os mesmos números mostrados, na precisão exibida, porque `τ_hor/t_P` é ou muito menor ou muito maior que 1. As previsões extremas, portanto, não distinguem as candidatas.

Se `ω=H₀`, R1 prediz `Γ/H₀=πβ=3,780×10^-2`: ordem β, sem supressão de Planck. O expoente cosmológico conhecido é outra quantidade, `2β/3=8,021×10^-3`.

### 6.3 A parede com nome

`TheFlowLawContrast` deriva `K=(E(N)/E(0))^(2β/3)` de `H_local=H_fundo·exp(β∫g)` e de `g=(2/3)d lnE/dN`; `τ★` não aparece nessa dedução. [TheFlowLawContrast](kimi-cite://text?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTheFlowLawContrast.lean&text=theorem%20the_derived_kernel_factor_normalized "citation")

**Conclusão dos dois regimes.** R1 dá a **escala** pedida — Planck no relógio e horizonte no setor de Hubble — e deixa β sem supressão. Ela não deriva `K`, não prova quem possui horizonte próprio e não escolhe entre max/soma/quadratura. Logo não há, no material consultado, UMA definição **derivada** que feche os dois regimes inteiros. A obstrução é dupla e recebe o nome:

> `PAREDE_RELOGIO_E_PONTE_HUBBLE` = (i) critério físico de propriedade/seleção do relógio do horizonte + (ii) ponte entre o `τ★` da defasagem e o fluxo integrado que produz `K`.

## 7. O observável atual e a pergunta nas quatro línguas

**[DERIVED sobre P1]** Nenhum observável atual lido distingue `1,1/β,√2,2π,4π` como fatores constantes. Em uma mesma frequência, `Γ` escala por `c★`; as cotas atuais estão muito acima de todos. Para o maior candidato, `1/β`, faltam `10,7612` ordens até a cota de Kim e `7,34993` até a cota nominal de Zn; distinguir fatores próximos exige ainda chegar à razão entre eles. O monopolo dependente de energia oferece, em princípio, outro discriminador (`ω³` contra `ω²`), mas nenhum resultado novo foi calculado ou aberto.

A pergunta existente conserva suas quatro peças — relógio, âncora, retido e volta — e ganha duas clarificações:

1. **Na peça “volta”:** separar explicitamente o `√2` da célula, o `√2` da dispersão e o numerador de `ω★`; só os dois últimos têm ponte no kernel, condicionada ao tempo do retido.
2. **Nova peça, “o seletor e a ponte”:** quem tem horizonte próprio, qual regra escolhe entre `t_P` e `τ_H`, e como essa escolha se relaciona — ou não — ao fluxo que já deriva `K=E(z*)^(2β/3)`.

Há ainda uma pergunta técnica indispensável: **a autoconsistência deve ser a leitura modular `ħω=ħ·½τω²`, sem β, ou a condição canônica `ħω=ħΓ`, que dá `ω=2/(βτ)`?** Isso não altera a pergunta original; explicita a premissa que o revisor marcou como aberta.

## 8. Artefatos, verificação e bloqueios

Arquivos produzidos, todos sob o escopo permitido:

- `K05/TAU/extrair_clock_selado.py` e `medidas/clock_selado_extraido.json`: leitura e hash do core, sem estatística nova.
- `K05/TAU/medir_tau_r2.py`: todas as contas deste relatório.
- `K05/TAU/medidas/medidas_tau_r2.json`: medidas, razões, alternativas, regimes e hashes das fontes.
- `K05/TAU/medidas/tabelas_tau_r2.md`: tabelas geradas por script.
- `K05/TAU/candidatas/TAU_ESTRELA_R2.lean`: candidata dimensional e algébrica.
- `K05/TAU/sandbox/{compilar.sh,sources,build,logs}`: compilação direta, sem `lake` e sem escrita no kernel.
- `K05/TAU/validar_tau_r2.py` e `medidas/validacao_tau_r2.json`: validação final e hashes dos artefatos.

**Lean [REAL].** Lean 4.31.0, `RC: 0`; os `#print axioms` dos 14 enunciados auditados contêm somente `propext`, `Classical.choice`, `Quot.sound`; nenhum `sorryAx`. A candidata prova álgebra e dimensão, não a física das hipóteses nomeadas.

**Bloqueios preservados.** P1 é condicional e o protocolo é não-cego/registrado após avaliação completa; P3 não tem observável local; a cota auxiliar do Atlas difere do core atual; `c★` continua indeterminado; a identificação `τ=tempoDoRetido` como `τ★` local falha P1; a seleção do horizonte e a ponte com `K` permanecem abertas. Nenhum valor foi ajustado a dado, nenhuma pedra foi tocada, nada foi registrado ou depositado.

## Referências externas usadas como entradas

- CODATA 2018: Mohr, Newell, Taylor 2021, *Rev. Mod. Phys.* 93, 025010 — **[KNOWN, a conferir]**.
- Milburn 1991, *Phys. Rev. A* 44, 5401, DOI `10.1103/PhysRevA.44.5401` — **[KNOWN, a conferir]**; apenas a forma citada no protocolo.
- `g=9,80665 m s^-2`, `GM⊕=3,986004418×10^14 m³s^-2`, `m_u=1,66053906660×10^-27 kg`: entradas efetivamente usadas no módulo v369, com CODATA/IERS 2010 indicados no próprio código — **[KNOWN, a conferir]**.
- Demais identificadores experimentais e cosmológicos estão nas seções 2, 4 e 6, sempre com o mesmo estatuto **[KNOWN, a conferir]** e sem reabertura dos dados.
