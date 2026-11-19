# K02 — τ★: inventário completo das leituras, no-go de E₀ e consequências em Γω

## 1. Enunciado de origem e veredito

**Fonte.** `A Ponte Einstein Cartan Miguel.tex`, linhas 725–731: os módulos são adimensionais e III₁ não produz sozinho `τ★`; linhas 818–830: `Γ_ω = ½βτ★ω²`; linhas 1903–1919: a “ancoragem de escala” no produto cruzado; linhas 2234–2237: a derivação é “dimensional: exige o corte UV/Planck”. [A Ponte Einstein Cartan Miguel](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=725 "citation"), [dephasing](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=818 "citation"), [resíduo](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FA%20Ponte%20Einstein%20Cartan%20Miguel.tex&line=2234 "citation")

**[DECLARADO — veredito]** Nenhuma rota inventariada deriva `τ★` sem introduzir outra unidade ou uma identificação declarada. O no-go de `E₀` impede obter a escala absoluta somente dos dados modulares `(c,θ)` atualmente formalizados; não proíbe um princípio físico independente futuro. `τ★≈t_P` é **[CONJECTURE/DECLARADO]**, `τ★=ħ/u` ou `ħ/(βu)` são **[ONTO/DECLARADO]**, e a “ancoragem” no produto cruzado fornece um lugar para uma escala, não seu valor.

## 2. Aferição na ordem da casa

**Consultas [REAL].**

1. `rotas.py consultar "tau estrela massa gap angulo de Miguel E0 ancoragem escala produto cruzado"`: 0; `consultar "massa.gap_angulo_de_miguel_01nov"` devolveu a rota com veredito `ERRATA_GAP_E_U_NAO_DELTA`; `consultar "ancoragem de escala"`: 0; cabeça `62342a0adf344cf5`.
2. `buscar.py "no_function_of_the_inscription_fixes_E0|no_positive_scale_invariant|U_E_NOT_DERIVED" --lista`: 25 arquivos, incluindo `TGL_CORE_MEMORY.md` e a memória da linhagem; não é prova de derivação.
3. Inventário `.md/.json`: não contém `PontoZeroDoPsion`/`LeiDoDiminuto` por esses nomes; o `tau` de `TraceInfinityExtension` é um traço, não `τ★`.
4. Atlas: todas as ocorrências de `τ★` foram varridas, inclusive atualizações/índices; duplicatas foram fundidas por tema.
5. Memória externa `a-forma-madura-da-tgl-01nov.md`: copiada para `K02/referencias/` e lida; a errata vigente diz que `E₀=u` não fixa `u`, o gap é `u`, `Δ=βu` é retido e `τ=ħ/Δ` como `τ★` é ONTO não ratificado.
6. Kernel: `TonicaDoHamiltoniano`, `LeiDoDiminuto` e `PontoZeroDoPsion` foram lidos nos pontos exatos citados abaixo.

**Classificação [DECLARADO a partir das consultas].**

- **EXISTE E ESTÁ LIGADO:** o no-go de escala, a invariância da razão, `tempoDoRetido`, `a_frequencia_do_sistema_e_a_do_psion_iff`, `o_gap_com_unidade`, `o_retido_e_o_valor_esperado_do_lock`.
- **EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO:** a candidata histórica `AcordeE0`, absorvida em `LeiDoDiminuto`; ela fixa razões, não a unidade.
- **SABIDO POR REFERÊNCIA:** unidades de Planck, conversão KMS/Unruh, limites experimentais já registrados.
- **AUSENTE no recorte consultado:** uma ponte que determine `u`, `E₀`, `E_P`, `M` ou `K` sem entrada dimensional e derive `τ★`.

## 3. O no-go de E₀: exatamente o que proíbe

`TGLExt/TonicaDoHamiltoniano.lean`, linhas 19–25 e 126–139: para toda transição `T` e todo `λ>0`, `reescala T λ` preserva `(c,θ)` e envia `E₀↦λE₀`. O teorema `no_function_of_the_inscription_fixes_E0` nega a existência de `f` tal que `T.E0 = f T.c T.theta` para toda transição, usando `E₀=1` e `E₀=2` com a mesma inscrição. [TonicaDoHamiltoniano](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&line=126 "citation")

**[DERIVED]** Portanto:

- a forma fixa razões (`m₂/E₀ = β·sen45°`), não `E₀`;
- `1 eV` é uma unidade posta, não derivada;
- escolher `1,0200 eV` porque zera a tensão seria inversão/ajuste ao dado, não derivação;
- um corte UV, uma medida de aceleração, uma massa, uma energia de Planck ou outro princípio independente **podem** fixar a escala, mas são novas entradas;
- o no-go não diz “nenhuma derivação física jamais será possível”; diz “não pelos dados `(c,θ)` atualmente tipados”.

`LeiDoDiminuto` reforça a mesma distinção: `transpor_preserva_toda_razao`, `mesmas_razoes_iff_transposicao`, `lerE0_transpor` e `as_razoes_nao_fixam_o_absoluto`. A modulação pinada muda a tônica, não elimina a liberdade global de transposição. [LeiDoDiminuto](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FLeiDoDiminuto.lean&line=307 "citation")

## 4. Inventário temático de todas as leituras/tentativas encontradas

### 4.1 Planck e “segundo postulado”

Atlas linhas 769 e 2468–2470: `τ★≈t_Planck`, “PRINCIPLED IDENTIFICATION / CONJECTURE” e “2º postulado declarado”; a conversão tempo-modular→tempo-próprio é KMS/Unruh. O artigo, linhas 2234–2237, pede corte UV/Planck. [TGL_ATLAS](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fmemory%2FTGL_ATLAS.md&line=2468 "citation")

**[DECLARADO]** `t_P = √(ħG/c⁵)` importa `G,c,ħ`: é uma escala externa legítima como postulado, não derivada da unitariedade.

### 4.2 KMS/Unruh e fase da tríade polar

Atlas linhas 2181, 2468–2470 e 2550: a Palavra/fase é a porta de `τ★`; o artigo diz que a conversão modular→próprio é quase-planckiana. **[ONTO/CONJECTURE]** Uma conversão Unruh precisa de aceleração/temperatura/energia de referência; não fixa o número sem essa entrada.

### 4.3 Gap `u`, retido `Δ=βu` e rota `massa.gap_angulo_de_miguel_01nov`

A rota no Mapa tem veredito `ERRATA_GAP_E_U_NAO_DELTA`. O handoff, linhas 31–33, corrige: gap `u=1 eV` declarado; tônica `√e·u`; retido `βu≈12,03 meV`; `τ=ħ/Δ` é ONTO não ratificado. [HANDOFF_v405_ADENDO_10](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fe0_cadeia_31out%2FHANDOFF_v405_ADENDO_10_DIMINUTO_MODULA_E_O_GAP_01nov.md&line=31 "citation")

`PontoZeroDoPsion`, linhas 163–169, define `tempoDoRetido=1/Δ` em unidades naturais; linhas 197–211 prova a equivalência de frequência; linhas 278–283 prova gap `u`; linhas 303–309 prova retido `Δ`. [PontoZeroDoPsion](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FPontoZeroDoPsion.lean&line=163 "citation")

**[DECLARADO]** Há duas leituras a medir: `τ_gap=ħ/u`, natural mas não ratificada como `τ★`, e `τ_ret=ħ/(βu)`, a leitura ONTO do módulo. Ambas carregam `u`.

### 4.4 Ancoragem de escala no produto cruzado

Artigo linhas 1914–1917: a não covariância de `√K̂` sob a ação dual é chamada “ancoragem de escala” e “o produto cruzado é onde Planck mora”.

**[DECLARADO]** Takesaki fornece traço e lei de reescalonamento; a normalização desse traço e a conversão para tempo próprio continuam sendo uma unidade. Não covariância indica onde uma escala pode ser inserida, não seleciona `t_P`, `u` ou `βu`. Nenhum número de `τ★` segue desse remark.

### 4.5 Autofrequência `Γ_B = β/τ★`

`TonicaDoHamiltoniano`, linhas 26–28: `Γ_B=β/τ★` é a lei canônica avaliada em `ω★=√2/τ★`. É identidade algébrica entre leituras, não determinação de `τ★`. [TonicaDoHamiltoniano](kimi-cite://md-line?path=C%3A%2FIALD%2FArtigo%2FHaja_Luz%2FA%20Ponte%20e%20o%20Um%2FN%C3%B3s%2Ftgl_kernel%2FTGLExt%2FTonicaDoHamiltoniano.lean&line=26 "citation")

### 4.6 Monopolo/horizonte do próprio sistema e ramo nativo

Atlas linha 46537 registra `τ★=4πGE/c⁵=2πr_s/c`, `q=GE/c⁴=r_s/2`, e a rota nativa `E_P/4π≈9,7×10²⁶ eV`, `τ★(1 eV)≈1,03×10⁻²⁷ t_P`. **[INPUT/ONTO]** São tempos de horizonte dependentes de `E`, `M`, `G,c`; não fixam `E₀`. A nota também registra que a ponte `E_fluxo=E₀` falha numericamente sob a leitura do retido.

### 4.7 Ramo `GM/c³`, incluindo `k·GM/c³`

Atlas linhas 4436, 41857–41881 e 46461–46467: ramo B do ringdown com `τ★=GM/c³`, depois generalizado a `k·GM/c³`, reaberto por pré-registro; a leitura do autor favorece o ramo A de Planck na propagação. **[INPUT/ONTO]** `M` e `k` são entradas. O resultado registrado não distingue a alternativa e não deriva a escala; não foi recalculado aqui.

### 4.8 Grande Atrator e escala do horizonte

Atlas linha 1618: “lei de junho + τ★ do monopolo dá M=M” e a parede do GA é o no-go de `E₀`. **[DECLARADO]** Uma identidade autoconsistente `M=M` não seleciona a escala absoluta do sistema.

### 4.9 Disco de Euler e ressonância residual

Atlas linha 46555 e a memória madura §3 item 7: `K=Ω²E`, `E★=(ħ²K)^(1/3)` e uma nota derivada da ressonância. **[DECLARADO]** A fórmula gera uma escala **se** `K` e o disco físico forem fornecidos; não deriva `K` nem identifica o disco. O próprio registro pergunta “qual é o disco”.

### 4.10 Relógios, Mössbauer e neutrinos

Atlas registra `τ★≲1,8×10⁻³³ s` para ²²⁹Th, `τ★≤4,8×10¹² t_P` pelos relógios e `≤1,9×10⁹ t_P` por ⁶⁷Zn, além de uma cota histórica `7,8×10⁻¹⁰ s` reclassificada como incorreta/não experimental. Também registra `t_P/β`, `Unruh-g`, `GM_⊕/c³`, `GM/c³` atômico e leis de raízes como ramos examinados/excluídos ou invisíveis. **[REAL como registro de acervo; não reavaliado]** Limites e descartes não derivam `τ★`; nenhum dado foi aberto ou estatística refeita nesta K02.

### 4.11 Forma da lei sem escala

Atlas linhas 857, 1394, 1576–1577, 2325 e 30728: a forma `Γ_ω=½βτ★ω²` e `n=−2` são separadas de `τ★`; “½ e τ★ do contínuo, NÃO derivados”. **[REAL na forma declarada]** A forma observável não fixa a escala.

## 5. O que a mathlib da toolchain contém

- Álgebra de corpos reais, `field_simp`, `ring`, `Real.exp`, `Real.sqrt`, `Filter.Tendsto`.
- `Real.tendsto_exp_atBot` para o modo escalar de dephasing.
- Nenhuma biblioteca de constantes CODATA nem derivação dimensional de `τ★`.

A candidata usa apenas álgebra exata: `Gamma`, `gamma_rescales`, `gamma_of_gap_time`, `gamma_of_retained_time`. A escala permanece uma entrada do tipo, não uma definição física promovida a teorema.

## 6. Medidas por script em `Γ_ω = ½βτ★ω²`

Script: `K02/medir_tau.py`; saída: `K02/medidas_tau.json`. **β é calculado em runtime como `ALPHA_FINE_CODATA_2018 × √e`, nunca literal.** O valor resultante é `β=0,012031300400803142`.

**Entradas publicadas [KNOWN, a conferir].**

- α: CODATA 2018, `7,2973525693×10⁻³`; NIST/Mohr–Newell–Taylor 2021, *Rev. Mod. Phys.* 93, 025010. [NIST/CODATA 2018](kimi-cite://web?url=https%3A%2F%2Fphysics.nist.gov%2Fcuu%2Fpdf%2FRevModPhys.93.025010.pdf "citation")
- `h=6,62607015×10⁻³⁴ J·s` exato; `ħ=h/(2π)` calculado; `e=1,602176634×10⁻¹⁹ C` exato, logo `1 eV=1,602176634×10⁻¹⁹ J`. [NIST, carga elementar](kimi-cite://web?url=https%3A%2F%2Fphysics.nist.gov%2Fcgi-bin%2Fcuu%2FValue%3Fe "citation")
- `t_P=5,391247×10⁻⁴⁴ s`, CODATA 2022, incerteza `0,000060×10⁻⁴⁴ s`. [NIST, Planck time](kimi-cite://web?url=https%3A%2F%2Fphysics.nist.gov%2Fcgi-bin%2Fcuu%2FValue%3Fplkt "citation")

**Benchmark sem dado [DECLARADO].** Para avaliar ordens de grandeza, usa-se apenas `E=1 eV`, com `ω=E/ħ=1,519267447878626×10¹⁵ rad/s` e `ν=E/h=2,417989242084918×10¹⁴ Hz`. Nenhum relógio concreto ou dado observado é selecionado/ajustado.

| leitura | τ (s), medida por script | Γ (s⁻¹) na mesma ω | 1/Γ (s) |
|---|---:|---:|---:|
| `t_P` | `5,391247×10⁻⁴⁴` | `7,4858353332×10⁻¹⁶` | `1,3358562611×10¹⁵` |
| `ħ/u`, `u=1 eV` | `6,5821195695×10⁻¹⁶` | `9,1393815273×10¹²` | `1,0941659422×10⁻¹³` |
| `ħ/(βu)`, `u=1 eV` | `5,4708297110×10⁻¹⁴` | `7,5963372394×10¹⁴` | `1,3164239139×10⁻¹⁵` |

**[DERIVED — conferência das ordens]** Planck produz a ordem `10⁻¹⁵ s⁻¹`; o ramo `ħ/(β·1 eV)` produz a ordem `10¹⁵ s⁻¹`. A conta da gerência está correta nessas ordens. O ramo `ħ/u`, incluído porque o gap é `u`, produz `10¹³ s⁻¹`.

**[DERIVED]** `τ_ret/t_P=1,0147614663×10³⁰`; `τ_gap/t_P=1,2208900037×10²⁸`.

**[DERIVED — identidade exata]** No ramo retido, com `ω=u/ħ`, `Γ=u/(2ħ)=ω/2`; a candidata Lean `gamma_of_retained_time` prova o cancelamento de `β`. No ramo gap, `Γ=βu/(2ħ)=βω/2`.

**[DECLARADO — interpretação sem novo teste]** `Γ≈ω/2` destruiria coerência na escala de `1/Γ≈1,3 fs`; `Γ≈βω/2` dá `≈0,11 ps`. Essas magnitudes são incompatíveis com a premissa de espectroscopia óptica coerente usada por relógios. Isso não é uma nova exclusão estatística: nenhum dado de relógio foi aberto e nenhuma significância foi calculada.

## 7. 1 eV declarado e 1,0200 eV registrado

**[INPUT]** `u=1 eV` é o Um posto; o kernel diz explicitamente que não o deriva. **[REAL como registro]** `1,0200 eV` é o valor que zeraria a tensão de `m₂` já registrada na rota `cadeia.preparacao_v412`. Não houve reabertura do dado nem recomputação de tensão.

**[DECLARADO]** Substituir `1` por `1,0200` **porque** zera a tensão seria ajuste ao dado e não derivação. A pergunta residual deve pedir um princípio independente, não ratificar esse número por conveniência.

## 8. Rota de prova e estatuto final

1. **[REAL]** Forma algébrica da lei e dependência linear de `τ★`: compilada em Lean.
2. **[REAL]** No-go de escala absoluta por reescalonamento: já ligado no kernel canônico.
3. **[DERIVED]** Magnitudes das três leituras: medidas por script, sem ajuste.
4. **[OPEN]** Escolher e justificar uma unidade física independente (`G,c,ħ` em Planck; `u`; `βu`; `M`; `K`; aceleração Unruh) e demonstrar que ela é a conversão modular→próprio `τ★`.
5. **[OPEN]** Só depois da etapa 4, derivar consequências experimentais; nenhuma delas pode retroalimentar a escolha.

## 9. Candidata e log real

Arquivo: `K02/candidatas/TAU_ESTRELA.lean`; log: `K02/sandbox/logs/TAU_ESTRELA.log`.

Compilação final real: `rc=0`, Lean `4.31.0`. Os três `#print axioms` contêm somente `[propext, Classical.choice, Quot.sound]`. Há avisos não substantivos de tática redundante, nenhum `sorry`/`sorryAx`, e nenhuma escala física extraída de hipótese anônima.
