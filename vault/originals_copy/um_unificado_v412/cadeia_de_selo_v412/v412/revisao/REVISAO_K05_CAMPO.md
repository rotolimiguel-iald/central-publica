# REVISAO_K05_CAMPO — revisão distinta da frente CAMPO DUAL e da integração da entrega K05 (v412)

Revisor distinto: Claude (subagente da gerência c1; sessão 6da8f00d), 14/11/2026. Quem constrói não aprova: o Kimi construiu; aqui só se confere.
Só leitura de tudo do Kimi. Escrito apenas nesta pasta: este relatório e `scripts_k05_campo\` (`conta_campo.py`, `conferir_integracao.py` e as saídas `*_saida.json`).
Nada foi registrado no Mapa, nada foi depositado na fila, nada foi instalado, `lake` não foi rodado, `C:\Escritorio` e `C:\IALD\TGL_IALD_NATIVE_QWEN5090` não foram tocados.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura · [DERIVED] derivado por mim · [DECLARADO] do Kimi, não conferido · [OPEN]. Nas minhas frases uso aspas “ ”; « » só para a fala do operador copiada do arquivo de bytes.

## 0. Veredito: APROVADA COM RESSALVAS

O que o Kimi afirma de fato conferiu: as citações de arquivo:linha (todas as que abri), a álgebra do fator 2, os números de massa, o 1/12, a fala por bytes, a REV0 e os hashes, o REGISTRO e o depósito. A conclusão central (duas equações convivem, nenhuma ação única escrita as dá, nenhuma das cinco candidatas fecha) se sustenta e não foi enfraquecida pelo que achei.

O que impede a aprovação plena: a aferição do §2 (“existe?/está ligado?”) é incompleta em quatro pontos (R1, R2 abaixo). Cada um troca uma classificação “ausente/aberto” por “EXISTE, MAS NÃO ESTÁ LIGADO AO TIPO” (regra “aferidor, não cego”); nenhum muda a conclusão. Há também uma derivação minha (sinal e normalização do artigo fundador, R3) que o levantamento deveria registrar, e uma ausência de rota/critério de poda (R5), que a ordem não exigia mas a PERGUNTA_K05 pressupõe.

## 1. Mapa de Rotas (consultado antes; nada registrado)

`rotas.py consultar` com termos únicos: `campo` n=58; `lagrangiana` n=3; `psion` n=60. Livro: 2059 registros, cabeça `cab386c822ca5a3e` (o Kimi consultou com 2056 / `03042aca2e30e8cf`; o livro andou).
Rotas que tocam o tema: `artigo_a.acao.normalizacao_do_acoplamento_nao_minimo` (claude-site-custodia: o 2ξR está no cânone como dispersão do psíon [INPUT]; não escrever o ½ na vitrine), `kernel.v386_tipagem_do_verbo` (Lagrangiana não tipada no kernel), `gate.qg_closure`. Nenhuma rota anterior examinou as cinco candidatas nem a conta do 1/12 com Weyl; nada a refazer além do que o Mapa já diz.

## 2. Tarefa 1 — verificações na fonte (cada citação aberta)

| afirmação do documento | fonte aberta | veredito |
|---|---|---|
| `omegaSq β R := 2*β*R`; cabeçalho `ω² = m₀² + 2ξR, ξ = β`; ½·√(2β²) = β/√2 = β·sen45° | `PontoZeroDoPsion.lean:22,36,85,86` (e 32–37, 91–113) | CERTO |
| `√2/τ = ω_psíon ⟺ τ = tempoDoRetido` | `PontoZeroDoPsion.lean:197–199` | CERTO |
| lagrangiana fundadora: `½g^{μν}(D_μΨ†)(D_νΨ) − V + ξR|Ψ|² − ¼F²`; `D_μ = ∇_μ − ieA_μ`, “U(1) local”; EOM com `2ξRΨ`; dispersão `k_n² + m_eff² + 2ξR`; “ξ = 1/6 forced” | `graviton_v2.tex:186,192,200,204,214,271` | CERTO |
| expansão `a_n u_n e^{-iωt} + a_n† u_n* e^{+iωt}` | `graviton_v2.tex:234` (232–239) | CERTO |
| Artigo A: `ℒ_campo = −¼Φ²`, `Φ_μν = ∂_μΨ_ν − ∂_νΨ_μ`, “conjugado canonicamente a Ψ*”, Ψ “campo escalar de fronteira”, U(1); `+ξR|Ψ|²`, ξ=1/6; EOM por `δS/δΨ*` com coeficiente 1 | `paper_PT.tex:167–173,175–182,244–257` | CERTO |
| `m_Ψ` só na linha 248; nenhum termo cinético escalar para Ψ | `grep -F 'm_{\Psi}'` → só `:248`; `grep` de `\partial…\Psi`, `D_\mu\Psi`, `\Box\Psi` → vazio | CERTO |
| ponte operador-modular → fonte é conjectura | `paper_PT.tex:259–286` | CERTO |
| “carga modular |Ψ|²” | `paper_PT.tex:410` (o Kimi cita 403–411; a custódia cita 412: a linha certa é 410) | CERTO |
| R82 (Ψ escalar × Ψ_μ, [OPEN]) | `DESENHO_DO_FECHAMENTO_QG.md:2587–2592` (2591) | CERTO |
| R87 (gradiente puro ⟹ d²ψ = 0; mapa tipado falta) | `DESENHO…:2646` | CERTO; omite a ressalva da própria fonte “isso não exclui outras identificações” (lacuna menor) |
| R88 (salto √β√K; Φ_D = β‖[D,X]‖²/4; Dirac do círculo; conexão q/2 dκ; sem identificar) | `DESENHO…:2655`; `SPECTRAL_RULE_REUSE_R88.md:13,19–35,39` | CERTO |
| R89 (`E_A = div(dA) + 2ξR A + E_rest`; resíduo `−grad(div A) − Ric·A + 3ξR A + m²A + βK A + E_rest`) | `DESENHO…:2668` | CERTO |
| `ξR A²` quebra gauge; `−¼F²` isolado não; `u = g^{ab}A_aA_b` lorentziano | `ONE_FORM_FULL_SOURCE_R88.md:14,70–74` | CERTO |
| v354: “`ξ=1/6` é o acoplamento conforme, não β_TGL — os dois coeficientes nunca se fundem” | `um.py:182860` (texto lido) | CERTO (ver R6 sobre o que os “dois” são) |
| v355: EOM como quarta face “com ξ separado” | `um.py:182865`; `TheSameBetaReadsFourFaces.lean:8–12` | CERTO |
| manifesto v354 lista `TheSameBetaReadsThreeFaces` | `work\cadeia_de_selo\v354_incorporacao_manifesto.json:43,279–283` (o Kimi não dá o caminho) | CERTO |
| controles: `reject_xi_as_beta` (hxi: D.xi ≠ c.beta ⊢ fieldOperator ≠ D.xi•K) e `xi_is_not_selected` | `ActionCouplingControls.lean:62–65,73–80`; direção da E1 da errata correta | CERTO |
| kernel: `conjJ`, `J∘J=1`, `JKJ=−K`; conjugação das fases “não ligada ao towerJ”; `Ψ=1_abs`, fluxo trivial; `excite_holonomy`, plano; morte do sinal; `α′=−(q/2)α`; corrente `L†L=P₀` | `ConjugateAct.lean:58–105`; `LightIsJ.lean:59–74`; `TheGravitonIsTheConjugatedPhase.lean:55–66`; `AbsoluteOne.lean:83–107,117–131`; `TransportWitness.lean:39–45,259–279`; `TheDeathOfTheSignal.lean:73–88,128–149`; `ContinuousModularZero.lean:203–217`; `ModularCurrent.lean:56–61,75–115`; `TheCurrentConnectsTheCorners.lean:132–168` | CERTO (todos) |
| Fecho 1, T1 no produto cruzado, tripla do círculo, `g=√|L|`, `ds=√β|d√k|` | `A Ponte Einstein Cartan Miguel.tex:1104–1118,1886–1901,1903–1919,1922–1932`; `um.py:1500–1516,2312–2328,2832–2840,2863–2875,6726–6747,6750–6769` | CERTO |
| recursão histórica `Ψ_{n+1}=𝓕[Ψ_n]`, `𝓕 = Û∘Π_Nome∘L_GKLS`; corrente `j^ν_Ψ`; β ~ 10⁻⁶ ≠ β_TGL | `recursive_light_v3.tex:82–136,229–255,393–418` | CERTO |
| rito imprime 8,507414 e 6,015650 meV; dispersão como `[INPUT, Tratado §3]` | `um_absoluto_pt.txt:304,312` | CERTO |
| Atlas: 737–747, 792–801, 898–902, 1593–1595, 1624–1628, 2296–2309, 2381–2388 | `TGL_ATLAS.md` (o 2381–2388 está em 2383–2389; o v354 do “5522–5524” está em 5526) | CERTO com deriva de linha (R10) |
| custódia: `LEIA_PRIMEIRO.md:7–16`, `ERRATA_DA_LEITURA…:16–19,41–47,57–69`, `VEREDITO_VERIFICADOR…:5–7` | lidos | CERTO |

Lacuna menor adicional do §1.2: no mesmo `graviton_v2.tex`, a equação dos modos (`:239`) usa `[−½∇² + V + ξR]u = ω²u` (ξR, não 2ξR), contra `:271` (`+2ξR`). Ver R3.

## 3. Tarefa 2 — a conta do ξ_L = 1/12 (feita por mim, `scripts_k05_campo\conta_campo.py`, sympy 1.14)

**3.1 Equação de movimento da linha 186 como escrita.** ℒ = ½ g^{μν}(∂_μΨ†)(∂_νΨ) − V + ξ_L R Ψ†Ψ, com Ψ e Ψ† independentes, V = ½m²Ψ†Ψ, R como fundo (não varia com Ψ). Euler–Lagrange em Ψ†:
∂ℒ/∂Ψ† = −½m²Ψ + ξ_L RΨ ; ∂ℒ/∂(∂_μΨ†) = ½∂^μΨ ; ∂_μ(∂ℒ/∂(∂_μΨ†)) = ½□Ψ.
⟹ ½□Ψ = −½m²Ψ + ξ_L RΨ ⟹ **□Ψ + m²Ψ − 2ξ_L RΨ = 0**. O sympy dá o mesmo nas assinaturas (+−−−) e (−+++): `a = −2ξ`, `b = 1`, resto nulo. Em módulo, o coeficiente de RΨ na EOM é **2ξ_L**: o 2 do artigo fundador é real.

**3.2 Valor conforme.** Verificado por mim por covariância de Weyl (sem usar a fórmula citada): para g = e^{2σ}η em n dimensões, R = −2(n−1)e^{−2σ}[□σ + ((n−2)/2)(∂σ)²], Ψ = e^{−(n−2)σ/2}Ψ₀, a identidade e^{(n+2)σ/2}(□_g − ξ_c R)Ψ = □_ηΨ₀ vale simbolicamente para **ξ_c = 1/8, 1/6, 3/16 em n = 3, 4, 5** (= (n−2)/(4(n−1))); o controle com a metade de ξ_c falha nos três. Portanto o coeficiente de R na EOM, em módulo, deve ser 1/6 em 4D. Com a EOM da linha 186, 2ξ_L = 1/6 ⟹ **ξ_L = 1/12** [DERIVED; confere o Kimi, a custódia e o verificador anterior]. Equivalente: Ψ = √2 Φ leva ½|∂Ψ|² a |∂Φ|² e ξ_L R|Ψ|² a 2ξ_L R|Φ|²; a normalização canônica pede 2ξ_L = ξ_c.

**3.3 O que o Kimi não disse e deveria (R3).**
(a) Sinal/assinatura. Da lagrangiana literal sai **−2ξ_L RΨ** (acima), não o +2ξRΨ de `graviton_v2.tex:214`; o relativo entre o termo de ξ e o potencial só concorda sob outra convenção de sinal de R ou de assinatura. O Artigo A (□ − m² − ξR) fecha em (−+++) (verificador anterior, item 8). O 1/12 vale em módulo; a frase deve dizer isso.
(b) O arquivo fundador tem três normalizações de ξ: `:186→:214` (2ξ), `:239` (ξ, com −½∇²) e o “forçado ξ=1/6” (`:204`). O “forçado” de `:204` convive com a inconsistência que o Kimi nomeou; o levantamento acerta em não refazer a derivação pelo traço.
(c) A mesma mistura (½ cinético, ξR|Ψ|² sem ½) aparece em `recursive_light_v3.tex:200–216`, e a EOM de lá (`:243`) tem coeficiente 1 para ξ (`−ξRΨ`): outro caso do mesmo desencontro de fator 2. [DERIVED, leitura minha.]

**3.4 “A régua muda |Ψ|², que é carga modular” (ENTREGA l.12; CAMPO §1.3).** Aritmética certa: Ψ_{½} = √2 Ψ₁ ⟹ |Ψ_{½}|² = 2|Ψ₁|² (sympy, `parte4`). A EOM é linear e homogênea, logo preserva a forma por reescala; a normalização vem da ação. Condição que falta dizer: “carga modular” é aqui o |Ψ|² do Artigo A (a Palavra c², `paper_PT.tex:410`), uma amplitude absoluta, e não a carga de Noether U(1): j⁰ = i·a(Ψ†∂_tΨ − ∂_tΨ†Ψ) com a = ½ ou 1 é **invariante** pela mesma reescala (a·|Ψ|² fixo), então a carga conservada não muda; muda o que se lê como |Ψ|² e o peso de ξR|Ψ|² frente a R/(2κ²) (a não minimalidade desloca G_eff por ξ|Ψ|²). Certo, mas a frase da ENTREGA, sem essa condição, pode induzir a leitura de que a carga conservada muda (R9).

**3.5 Um só ξ não reconcilia, em nenhuma normalização [DERIVED]:** (1/6)/β = 13,853; (1/6)/(2β) = 6,926; nem o fator 2 (½ vs 1) fecha. Reforça o “β ≠ 1/6” do Kimi (§1.5): são dois acoplamentos (ou uma hipótese nova nomeada).

## 4. Tarefa 3 — os números (script próprio; α lido de `um.py:5584`, não de memória)

α = 7,2973525693e-3 (`um.py:5584`, CODATA 2018); β = α·exp(½) em runtime = 0,012031300400803141; **com o 2: 8,507414099900328 meV** (= β·u/√2, u = 1 eV posto); **sem o 2: 6,015650200401570 meV** (= β·u/2); razão √2 = 1,414213562373095; ħω = 17,014828 meV. **Confere `medidas_campo.json` até o último dígito impresso** (50 dígitos, mesmos) e os números impressos do rito (`um_absoluto_pt.txt:304,312`). Pequeno: `medir_campo.py` digita o α (`Decimal("0.0072973525693")`) com comentário apontando o Atlas, em vez de lê-lo de `um.py:5584` (a régua pede ler); β está em runtime, então a régua do β se cumpre (R12).

## 5. Tarefa 4 — as cinco candidatas e a regra “aferidor, não cego”

Consultas que fiz (além das do Kimi): `grep -rE` no kernel `TGLExt`/`TGL` para `holonom|Holonom|Wilson|gauge connection|covDeriv|derivada covariante|Circle|inner fluctuation|carga modular|Noether|U(1)|U1`; `grep` do INVENTARIO_BANCADA_CHATGPT.md (1,9 MB) para `holonom` (0), `Wilson` (0), `loop` (0), `gauge` (33 linhas), `covariant derivative` (4), `charge conjugation|PCT` (7), `Connes distance|spectral triple|inner fluctuation` (0), `Maxwell` (545); `NOS_VIVO\consultar.py` para “Jcandidate helicity”, “MaxwellOnShellBivector”, “Lagrangiana radicalizada”, “Wilson loop”; cruzamento kernel `omegaSq` × `ActionCouplingData` (nenhum arquivo cita os dois). Classe: **E** = EXISTE E ESTÁ LIGADA · **N** = EXISTE MAS NÃO ESTÁ LIGADA AO TIPO · **M** = MEDIDA (a bancada/a casa marcou) · **A** = AUSENTE (com a consulta).

| candidata · ponte que o Kimi deixa aberta | classe | consulta e o que achei |
|---|---|---|
| A · ação única que dê as duas equações | **A** | `omegaSq` aparece em 6 arquivos (`PontoZeroDoPsion`, `TonicaDoHamiltoniano`, `PonteDaMassa`, `LeiDoDiminuto`, `MassaTensaoPura`, `DiscoDeEuler`); `ActionCouplingData` em 3 (`TheSameBetaReadsFourFaces`, `ActionCouplingControls`, `TGL/Audit`); interseção vazia. Confirma o Kimi |
| A · Ψ_μ = A_μ e Φ = F (escalar × vetor) | **N** (peça F=dA) / **A** (a ponte) | **o Kimi não viu:** o kernel tem a intensidade de campo on-shell com gauge e Bianchi: `TGLExt/F1Fecho394/MaxwellOnShellBivectorR2.lean` (`strength p e = p∧e`; `strength_gauge`: e→e+a·p; `strength_bianchi`; `strength_source_free`), `CartesianMaxwellBivectorR6`, `MaxwellScreenDualTensorR2`. Não ligam ao Ψ nem a `ActionCouplingData`; ponte Ψ_μ=A_μ segue R82/R87 [OPEN] |
| A · W_γ = P exp(ie∮A) como o loop | **A** (holonomia de A) · **N** (vizinhas) | `Wilson`/ordenação por caminho: 0 no kernel e no inventário. Existem: holonomia de transporte (`TransportWitness.excite_holonomy`), caractere U(1) do pequeno grupo (`photonPhase`, `O16/PhotonScreenCharacters_v3.lean:70`, `LightHelicityWigner`), e o contorno que fecha em 2π (`PolarPeriod016.faithful_period_iff`, `wick_boost_two_pi`, ver `Palavra.lean`). O Kimi não cita as duas últimas |
| A/C · origem do √K na ação | **N** | √K existe como operador (`um.py:2312–2328`, Ponte Fecho 1) e não está na ação; confirma o Kimi |
| B · alocação dos termos de curvatura; gauge total; carga modular comum | **A** | gauge total: M/DERIVED em R88 (`ξR A²` quebra gauge), sem ação invariante construída; “carga modular”: no kernel só há `O16/ModularChargeLink.lean` (carga modular do tensor T₀ no plano nulo): **homônimo**, não é |Ψ|² |
| B · resíduo R89 | **M** | derivado no DESENHO (l.2668), “requisito de correspondência a conferir”; não resolvido |
| C · d_D f ou (q/2)dκ = Ψ_μ; D=√K = D_circ | **N** | `ContinuousModularZero.alpha_transport` (conexão escalar) e `[D_circ,M_f]ψ = −iβ^{-1/2}f′ψ` existem; a identificação foi recusada por nome em R88 (`SPECTRAL_RULE_REUSE_R88.md:29,35,39`) |
| C · fluxo GKLS = loop do vetor | **A** (a identidade) | o fluxo existe e está ligado (`DecisionCommutation`, `TheRuleInTheContinuousMotor`) |
| D · J ↔ Ψ* (conjugação do campo) | **N** (fóton) / **A** (Ψ escalar de `ActionCouplingData`) | **o Kimi não viu:** `F1Fecho394/ScreenGeometricReflectionR4.lean`: `Jcandidate_eq_helicity_halfTurn_Theta`, `Jcandidate_conjugates_helicity`; `Jcandidate` (`CanonicalWedge.lean:38`) é antilinear (`starRingEnd ℂ`): conjugação complexa + troca de helicidade + meia-volta, com ressalva do próprio arquivo (“geometric covariance/localization … NOT asserted”); também `CircularConjugationR1`, `FiberConjugation`, `O16/BoostScreenPolarizations_v2.circularScreen_conjugate`. O Kimi disse “no kernel só há tipagem complexa, sem Ψ*”: vale só para `ActionCouplingData` |
| D · W (holonomia de transporte) ↔ holonomia de gauge | **A** | as holonomias do kernel são de matrizes/subespaços; nenhuma de conexão U(1) |
| E · recursão histórica = loop; corrente EM = vetor | **N** (documento, [DECLARADO 2025]) | recursão afim no kernel: `TheDeathOfTheSignal` (n travessias), `psion_is_fixed_by_the_light`; nada ligado à ação histórica; R87: `SectorFluidClosure` não identifica correntes com P |

**Candidatas/antecedentes que faltam no §2.4 e no §3 (R2):**
1. **Lagrangiana radicalizada** 𝓛 = √|g⁻¹(F∧⋆F)| [DECLARADO 2025]: `TGL_ATLAS.md:1891–1899` e `C:\IALD\papers_latex\luz\luz.tex:74,108,227` (Zenodo 10.5281/zenodo.17736434, como o Atlas dá). É literalmente “vetor (F) + radical”, com a EOM `∇_μ(F^{μν}/√|F²|) = J^ν` (`luz.tex:108`). O Kimi consultou o Atlas na vizinhança (l.737–747, 2296–2309), listou “radicalização” em CONSULTAS, mas o corpo só trata √K do Fecho 1.
2. **`TGLExt/Par.lean`** (o par de psíons ligado = gráviton; nome do operador `Par`, v407; na raiz `TGLExt.lean:1134`) e `TGL_ATLAS.md:1624–1628, 2298–2301` (“dois psions conjugados (A_C, JA_CJ) reproduzem o spin-2 selado 21/21”): é o “dual, porque conjugado” que a casa já tem tipado; o Kimi o lista em CONSULTAS (Atlas 1624–1628) e não o traz ao §2.1.
3. **“Dual” de Hodge** (F ↔ ⋆F: `luz.tex:142–175`, `MaxwellScreenDualTensorR2`): terceira leitura de “dual” além da conjugação complexa e da conjugação modular. O Kimi lê “dual” como conjugado (a fala diz “porque é conjugado”; correto), mas a memória da casa (`campo-dual-vetor-cinetico-13nov.md`, “Como aplicar”) manda não ler “dual” como “complexo” por conta própria. A candidata A chama-se “escalar complexo dual”: herda a leitura da ORDEM (“escalar complexo (o dual, por conjugado)”), sem avisar que é leitura da ordem/custódia.

## 6. Tarefa 5 — a fala

Todos os trechos «…» de todos os documentos K05 do campo (CAMPO_DUAL, ERRATA_CAMPO, ENTREGA, PERGUNTA, DEPOSITO, CONSULTAS) foram extraídos por script: **há exatamente um**, `CAMPO_DUAL_LEVANTAMENTO_K05.md:7`: «eu acho que é dual (porque é conjugado), eu traduziria como campo de processamento dual estabilizado radicalmente por vetor cinético (que é o loop recursivo)». Está **byte a byte** no arquivo de fala (529 B, sha256 `2772005945b946c12172956c12c06421710d7d665cacf4dba63f40bd07ec304c`, conferidos por mim). Sem paráfrase dentro de « ». Fora das aspas o documento usa “vetor cinético”, “loop recursivo”, “dual (porque é conjugado)”: todas as expressões estão na fala. (Nota: a fala é “eu traduziria como…”, uma proposta de nome; o Kimi a tratou como identificação, [INPUT]/[DECLARADO], o que é certo.)

## 7. Tarefa 6 — estatuto, escolha silenciosa, rota e critério

- Estatuto: a cunhagem está `[INPUT]/[DECLARADO — identificação do operador, não teorema]` (§0), nada promovido; ENTREGA l.13 marca as candidatas `[DECLARADO]`. A casa registra a cunhagem como `[ONTO]` (memória `campo-dual-vetor-cinetico-13nov.md`); sugiro acrescentar [ONTO] (R13).
- ½ do box: não decidido (§0 “Nada neste levantamento decide o fator ½…”; §5; PERGUNTA l.3). Sem escolha silenciosa de candidata; a única inclinação é a frase do §5, “a arquitetura mais diretamente sugerida pelos arquivos é o escalar complexo com derivada covariante e um vetor com curvatura”, imediatamente qualificada como “não é escolha nem fechamento”. Aceitável.
- **Rota para provar no kernel e critério para podar: só lista (R5).** Há “hipótese NOMEADA e o que NÃO fecha” por candidata (H_A…H_E) e o bloqueio resumido no §5; a PERGUNTA_K05 diz que a gerência “deve tentar provar” uma ação com tipos e régua “enquanto não existe, nenhuma das cinco candidatas é escolhida ou podada”. Não diz **como** (qual estrutura Lean, qual enunciado) nem **quando** uma candidata cai. A ordem pedia só o levantamento, então não é defeito de cumprimento; é a falta que o próximo passo (provar ou podar) vai sentir. Proposta mínima, a ser decidida pela gerência: rota — estender `ActionCouplingData` (ou estrutura nova) com par conjugado, conexão e coeficiente cinético explícito, e provar o teorema “ação ⟹ EOM com coeficiente 2ξ_L/(2a) e dispersão”; critério de poda — a candidata cai se (i) não entrega no mesmo objeto ξ_A=1/6 com coeficiente 1 **e** ω²=2βR, ou (ii) exige ξ_A=ξ_P (§3.5: razão 6,9), ou (iii) pede Ψ_μ=A_μ sem mapa tipado e sem ação total gauge-invariante (R88).

## 8. Tarefa 7 — a errata e a REV0

- As quatro correções (E1–E4) estão certas e no diff REV0→vigente (`conferir_integracao_saida.json`): E1 (direção de `reject_xi_as_beta`, `ActionCouplingControls.lean:62–65`): certa; E2 (“o único código executado que grava artefato foi `medir_campo.py`”): certa; E3 (inventário como snapshot histórico): certa na natureza, com um desvio no pin (R11); E4 (`Fix = W*(K̂)` como enunciado do artigo, não teorema desta seção; H_K̂, H_erg, H_TGL-horizon `[OPEN]`): certa e conferida contra `T1_FECHADO.md:4,30–34,120–121`.
- Hashes por script: os 11 pares de `HASHES_CAMPO_K05.txt` (vigentes e REV0) **conferem**; a tabela da ERRATA (antes/depois) **confere**; `medir_campo.py`, `medidas_campo.json`, `execucao_medidas.log` são idênticos à REV0, como a errata diz. REV0 do levantamento = `5ec65dd2…4bc4` ✓; vigente = `fb9b1255…2252` ✓.

## 9. Tarefa 8 — integração

**8a (14 bullets não vazios + título = 15 linhas; o limite é 15).** Cada linha tem frase de apoio no documento correspondente (a matemática fica com os outros revisores):
l.3 → `T1_FECHADO.md:4,30–34,120–121,216`; l.4 → `T1_FECHADO.md:250–262,273` e logs (`T1_R2.log`, `T1_R2_audit.log`: `RC: 0`, `FALHAS: 0`, 11 `#print axioms` no trio); l.5–6 → `MONTAGEM_3MAIS1_R2.md:5,7,41,45–93`; l.7 → `GH_III1_R2.md:5,7,9,43–46`; l.8–9 → `TAU_ESTRELA_R2.md:7,8,11,220–226`; l.10 → `TAU_ESTRELA_R2.md:169–175,233`; l.11–13 → `CAMPO_DUAL…` §0, §1.2–1.3, §3–§5; l.14 → logs Lean (sem `sorry` nos dois `.lean`; `TAU_ESTRELA_R2.log` só trio); l.15–16 → `PERGUNTA_K05.md`, `ERRATA_*`. Ressalva: **l.11** leva o prefixo [REAL] para “sem ação única localizada”, que é uma ausência por consulta e que o CAMPO §4 marca `[OPEN]` (R7). Ressalva: l.12 sem a condição sobre “carga modular” (R9).

**8b `REGISTRO_MAPA_K05.json`:** (i) as 20 chaves de `rotas.py modelo` presentes, nenhuma a mais (script); (ii) **passa na guarda da casa**: rodei a própria `_valida` do `rotas.py` em dry-run (importada, sem `registrar`; o livro, de 2059 registros, só foi lido, a cadeia de hash conferida): sem erro, 17 artefatos resolvidos; (iii) nenhum caractere « ou »; (iv) a única palavra começada por “confirm” é “CONFIRMED” no campo `nota` (“NOT_FALSIFIED não é CONFIRMED”), precedida de negação, e `nota` nem entra na guarda (que só olha `titulo`, `resultado`, `veredito`). Pela leitura estrita pedida (“nenhuma palavra começada por confirm”) **falha em `nota`**: trocar por “NOT_FALSIFIED não é a palavra da creditação” antes de registrar; (v) os três `refs` (`cadeia.preparacao_v412`, `massa.gap_angulo_de_miguel_01nov`, `relogios.v1`) existem no livro; `rota_id` novo; tamanhos de texto < 6000; `olhou_dados: true` (conservador; o Kimi diz só leitura de registro selado: aceitável porque conta no fator de tentativas); `status: EXAMINADA_COM_DEFEITO` e `estatuto` válidos. O conteúdo do registro não repete a classificação “AUSENTE” retirada e traz o `nao_refazer` certo.

**8c `DEPOSITO_K05.md`:** abre com `[DECLARADO]`; diz “revisada internamente”; **não** diz “aprovada em revisão independente”; nenhuma palavra “confirm…”; as três linhas SHA-256 (ENTREGA, REGISTRO, VALIDACAO) **conferem** por script; fecha “Gate imóvel”. Ressalva (R8): `VALIDACAO_K05.json` (campo `review`) diz “revisada internamente; integração e quatro frentes conferidas **por revisores distintos**”: expressão que se aproxima de revisão independente, ato da gerência; trocar por “conferidas por subagentes internos” ou apagar a segunda oração. Os 18 pins do `VALIDACAO` conferem por script.

## 10. Ressalvas, em ordem de exigência

**Exigem correção antes de a gerência apoiar-se no documento (nenhuma muda a conclusão):**

- **R1 — aferição do kernel incompleta (CAMPO §2.1, §2.2, §4 linhas “Existe par complexo e conjugação?” e “Existe vetor associado?”).** Consulta: `grep -rE "strength_gauge|circularScreen_conjugate|ScreenChargeConjugation|Jcandidate" TGLExt`; NOS_VIVO “Jcandidate helicity”. Achado: `F1Fecho394/ScreenGeometricReflectionR4.lean` (`Jcandidate_eq_helicity_halfTurn_Theta`, `Jcandidate_conjugates_helicity`), `CanonicalWedge.lean:38` (a definição, antilinear), `CircularConjugationR1.lean`, `O16/BoostScreenPolarizations_v2.lean:41`; `F1Fecho394/MaxwellOnShellBivectorR2.lean` (F=p∧e, gauge, Bianchi). Corrigir para: “existe e está ligado no fóton; não ligado ao Ψ escalar de `ActionCouplingData` nem ao Φ_μν do Artigo A”. A frase “no kernel só há tipagem complexa, sem Ψ*” fica restrita a `ActionCouplingData`.
- **R2 — candidatas/antecedentes ausentes (§2.4, §3).** Consulta: Atlas `grep -n "radicaliza"` → l.1885–1899; `luz.tex`; kernel `Par.lean`; Atlas 1624–1628. Acrescentar a Lagrangiana radicalizada [DECLARADO 2025], o `Par` e a leitura de Hodge, com o aviso da memória da casa sobre “dual”≠“complexo”.
- **R3 — sinal e normalização (CAMPO §1.2).** Dizer assinatura e sinal de R; registrar que a lagrangiana literal dá −2ξ_L RΨ e que `graviton_v2.tex:239` e `recursive_light_v3.tex:243` carregam outras normalizações (§3.3).

**Recomendadas:**

- **R4 — referências sem autor/ano** (`QFT-CONFORMAL-SCALAR-001`, `MAXWELL-CONFORMAL-U1-002`, `U1-CURVATURE-HOLONOMY-003`, §1.2, §1.4, §2.2): a ORDEM K05 pede autor, ano e identificador. Verifiquei a fórmula por Weyl (§3.2); a referência primária sugerida é Callan–Coleman–Jackiw, Ann. Phys. 59 (1970) 42, e Birrell–Davies (1982), ambas [KNOWN, a conferir].
- **R5 — sem rota nem critério de poda** (§7 acima).
- **R6 — “os coeficientes não se fundem” (§4, última pergunta de acoplamento).** `um.py:182860` fala de ξ (curvatura) contra β_TGL (fonte modular); os controles do kernel (`reject_xi_as_beta`, `xi_is_not_selected`) separam o coeficiente da FONTE modular de `D.xi`; nada ali proíbe ξ_P = β, que a dispersão do psíon FUNDE por definição [INPUT]. Dizer os pares (ξ_A × β; ξ_A × ξ_P) em vez de um “NÃO” único.
- **R7 — prefixo de estatuto** da ENTREGA l.11 ([REAL] para uma ausência; o CAMPO §4 diz [OPEN]).
- **R8 — `VALIDACAO_K05.json`, campo `review`** (“por revisores distintos”).
- **R9 — “carga modular”** (§3.4): precisar que é |Ψ|² do Artigo A, e que a carga de Noether é invariante.
- **R10 — citações de linha ao `TGL_ATLAS.md`** (15 MB, mtime 13/11 21:06, blocos repetidos): `5522–5524` já está deslocado (o v354 está em 5526); citar por título de seção.
- **R11 — pin do banco do NOS_VIVO (ERRATA E3).** O sha256 e o tamanho conferem (92a2831b…, 35.868.672 B), mas o conteúdo do `.bak` não é o do texto lido: `meta.gerado_em` = 10:26:30 (não 20:01:35) e `nos` do tipo `arquivo` = 5746 (o texto lido tinha 5776). Os demais números do snapshot conferem no `.bak` (4114 `lean_bancada`, 1757 `pedra`, 306 arestas `ligado_ao_kernel`, 4114−306 = 3808). Retirar “banco histórico correspondente” ou dizer que é o anterior; não muda nenhuma conclusão (as pedras `ScreenGeometricReflectionR4`, `MaxwellOnShellBivectorR2`, `Par`, `PontoZeroDoPsion` já estavam no `.bak`: o Kimi poderia tê-las achado por ele).
- **R12 — `medir_campo.py` digita o α**; ler de `um.py:5584`.
- **R13 — rótulo da cunhagem**: acrescentar [ONTO].

## 11. O que não consegui conferir

- A matemática de T1, GH, τ★ e a literatura [KNOWN, a conferir] (outros três revisores).
- Que a conta do “peso do termo gravitacional” (|Ψ|² fixo) seja a leitura física que o operador quer: depende da decisão dele sobre a régua.
- `index.html:505–507` (a caixa “Lineage” do site) e `um.py:127996` (que o verificador anterior cita para a dispersão): não abri.
- Não recompilei Lean (`PontoZeroDoPsion`, `ScreenGeometricReflectionR4`): li as fontes; o estado de compilação vem do selo, não de mim.
- Não reexecutei as consultas do Kimi ao NOS_VIVO e ao índice do acervo; refiz as minhas (§5).
- Se o `Jcandidate` está alcançável por import a partir da raiz `TGLExt.lean`: vi `TGLExt.Par` (l.1134) e `PontoZeroDoPsion` (l.1130) na raiz; `F1Fecho394/*` entra por cadeia de imports e figura como `pedra` no NOS_VIVO.

## 12. O que examinei (para o registro do Mapa pela gerência; eu não registrei)

- Mapa: `rotas.py consultar campo | lagrangiana | psion`; `rotas.py modelo`; `rotas._le/_valida` em dry-run sobre `REGISTRO_MAPA_K05.json`.
- Kimi: `CAMPO_DUAL_LEVANTAMENTO_K05.md`, `ERRATA_CAMPO_K05.md`, `K05\CAMPO\` (`REV0`, `CONSULTAS_CAMPO_K05.md`, `medir_campo.py`, `medidas_campo.json`, `HASHES_CAMPO_K05.txt`), `ORDEM_K05_matematica_rodada_2.md` (seção E), `ORDEM_K05_ADENDO_A_…`, `ENTREGA_K05.md`, `PERGUNTA_K05.md`, `REGISTRO_MAPA_K05.json`, `DEPOSITO_K05.md`, `VALIDACAO_K05.json`, e as frases de apoio em `T1_FECHADO.md`, `MONTAGEM_3MAIS1_R2.md`, `GH_III1_R2.md`, `TAU_ESTRELA_R2.md`, logs Lean de `K05\sandbox_t1` e `K05\TAU\sandbox`.
- Kernel (só leitura): `PontoZeroDoPsion`, `TheSameBetaReadsFourFaces`, `ActionCouplingControls`, `ConjugateAct`, `LightIsJ`, `TheGravitonIsTheConjugatedPhase`, `AbsoluteOne`, `TransportWitness`, `TheDeathOfTheSignal`, `ContinuousModularZero`, `ModularCurrent`, `TheCurrentConnectsTheCorners`, `Palavra`, `Par`, `IALDGraviton`, `ThePsionReducesToTheCurrent`, `F1Fecho394\{MaxwellOnShellBivectorR2, MaxwellScreenDualTensorR2, CartesianMaxwellBivectorR6, ScreenGeometricReflectionR4, CanonicalWedge, CircularConjugationR1, FiberConjugation, GeometricFiberConjugation, CanonicalFockConjugationActionR3}`, `O16\{BoostScreenPolarizations_v2, PolarMinimalPeriod_v2, ModularChargeLink}`; `TGLExt.lean` (imports).
- Fontes: `graviton_v2.tex`, `paper_PT.tex`, `A Ponte Einstein Cartan Miguel.tex`, `um.py` (182860, 5584, e os intervalos citados), `um_absoluto_pt.txt`, `recursive_light_v3.tex`, `luz.tex`, `DESENHO_DO_FECHAMENTO_QG.md` (R82, R87–R89), `SPECTRAL_RULE_REUSE_R88.md`, `ONE_FORM_FULL_SOURCE_R88.md`, `TGL_ATLAS.md` (várias seções), `INVENTARIO_BANCADA_CHATGPT.md`, `NOS_VIVO` (`consultar.py`, `.bak_20261113_200150` em modo somente leitura), `v354_incorporacao_manifesto.json`, custódia (`LEIA_PRIMEIRO`, `ERRATA_DA_LEITURA_DO_MEIO_13nov`, `VEREDITO_VERIFICADOR_LEITURA_DO_MEIO_13nov`), memória `campo-dual-vetor-cinetico-13nov.md`, fala (`OPERADOR_13nov_…verbatim.txt`).
- Scripts meus: `revisao\scripts_k05_campo\conta_campo.py` (+ `conta_campo_saida.json`), `conferir_integracao.py` (+ `conferir_integracao_saida.json`).
