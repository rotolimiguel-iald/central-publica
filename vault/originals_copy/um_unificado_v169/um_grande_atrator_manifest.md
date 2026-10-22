# Um: Grande Atrator -- MANIFESTO DE ENTRADAS (nada fica escondido no codigo)

> Ou e' **definicao exata**, ou **constante medida**, ou **protocolo pre-registrado**, ou **conjectura testavel**. Este manifesto e' parte do hash do veredito.

## Definicoes exatas [DEF]

```json
{
  "ONE": 1,
  "TWO": 2,
  "HALF": 0.5,
  "FOUR": 4,
  "pi": "computed (4*atan(1))",
  "sqrt_e": "computed (exp(1/2))",
  "alpha_abs": "[DEF] = 1 (Um absoluto; input originario; Tomita do Bell nu da' alpha_abs=1)",
  "q": "[QED-VALIDATION] polarizacao termico-modular do zero modular (=q_QED no modo de validacao)",
  "alpha_form": "[DER] = sqrt(1 - q^2)  (= alpha_obs; motor canonico)",
  "beta_form": "[DER] = sqrt(e) * sqrt(1 - q^2)  (= alpha*sqrt(e) na leitura observacional)",
  "identity": "[DER] 1 = q^2 + alpha^2 (conservada)",
  "R_partial": "[LEGADO] = 1/alpha_form, derivado APOS a forma; NAO motor canonico (nao vem de CODATA)"
}
```

## Constantes medidas [DATA]

```json
{
  "alpha_CODATA": 0.0072973525693,
  "source": "CODATA 2018",
  "alpha_inv": "137.035999",
  "uncertainty": "~1.5e-10 (rel.)",
  "role": "[EXT] validacao final apenas: q_QED = sqrt(1 - alpha_CODATA^2); NAO move a cadeia",
  "G_Newton": 6.674e-11,
  "M_sun_kg": 1.98892e+30,
  "Mpc_m": 3.0857e+22
}
```

## Definicoes SI [DEF]

```json
{
  "c_m_per_s": 299792458.0
}
```

## Ponte da Impedancia do Vacuo [REAL/EXT]

```json
{
  "Z0": "[EXT] impedancia caracteristica do vacuo; face dimensional da constante DINAMICA da luz",
  "R_K": "[DEF] h/e^2, exato no SI porque e,h sao exatos (2019)",
  "G0": "[DEF] 2e^2/h, exato no SI porque e,h sao exatos (2019)",
  "alpha_Z0_bridge": "[REAL] alpha = Z0 e^2/(2h) = Z0/(2 R_K) = Z0 G0/4",
  "Z0_from_alpha_ohm": 376.730313668004,
  "chi_log_impedance_ratio": 11.226755051602328,
  "all_checks_verified": true,
  "status": "VACUUM_IMPEDANCE_BRIDGE_FORMULATED__ALPHA_VALUE_QED_SECTOR_FALSIFICATION_CHALLENGE. Ponte fisica fechada (c=cinematica, Z0=dinamica, alpha=Z0 adimensional); valor alpha-livre aberto: Z0 computado de alpha (mu0 nao exato pos-2019), entao Z0<->alpha dado e,h."
}
```

## Entrada geometrica [DATA]

```json
{
  "R_struct_literature_Mpc": 57.0,
  "source": "Lynden-Bell et al. 1988 (GA basin extent ~40 h^-1 Mpc; h=0.7 -> 57 Mpc)",
  "provenance": "GEOMETRY_ONLY_NO_MASS_NO_RG"
}
```

## Protocolo pre-registrado [PRE]

```json
{
  "GA_center_RA_deg": 243.6,
  "GA_center_Dec_deg": -60.4,
  "cone_half_angle_deg": 30.0,
  "dist_shell_Mpc": [
    30.0,
    100.0
  ],
  "R_struct_method": "percentile_90_from_centroid",
  "accepted_mass_window_Msun": [
    1000000000000000.0,
    1e+17
  ],
  "sensitivity_grid": {
    "cone_half_angle_deg": [
      20.0,
      25.0,
      30.0,
      35.0,
      40.0
    ],
    "dist_shell_Mpc": [
      [
        25.0,
        100.0
      ],
      [
        30.0,
        100.0
      ],
      [
        30.0,
        120.0
      ]
    ],
    "percentile": [
      80.0,
      85.0,
      90.0,
      95.0
    ],
    "center_offsets_deg": [
      [
        0.0,
        0.0
      ],
      [
        5.0,
        0.0
      ],
      [
        -5.0,
        0.0
      ],
      [
        0.0,
        5.0
      ],
      [
        0.0,
        -5.0
      ]
    ]
  }
}
```

## Comparacao externa apenas [EXT]

```json
[
  {
    "name": "Norma cluster ACO 3627 (virial, RG dinamica)",
    "M_Msun": 1000000000000000.0,
    "ref": "Woudt et al. 2008, MNRAS 383, 445",
    "type": "GR_dynamical_virial"
  },
  {
    "name": "Grande Atrator (infall linear, RG)",
    "M_Msun": 5.4e+16,
    "ref": "Lynden-Bell et al. 1988, ApJ 326, 19",
    "type": "GR_linear_infall"
  },
  {
    "name": "Laniakea (supercluster)",
    "M_Msun": 1e+17,
    "ref": "Tully et al. 2014, Nature 513, 71",
    "type": "supercluster_flow"
  }
]
```

## Parametros numericos dos testes de sombra [NUM]

```json
{
  "dim_n": 4,
  "seed": 11,
  "gesture_G": 6,
  "tunnel_theta": 0.4,
  "dipole_dim": 6,
  "dipole_trajectories": 12,
  "dipole_steps": 620,
  "dipole_thermal_seed": 7,
  "dipole_traj_seed": 3,
  "purity_floor_start": 0.997,
  "status": "FINITE_DIM_SANITY_CHECKS_NOT_TYPE_III1_PROOF"
}
```

## Setor irreversivel -- o ato (v3) [NUM]

```json
{
  "verb_generator_A": {
    "L": "L = sqrt(beta) sqrt(K_partial) ; K=A A^T/n (n=4, seed=11) ; beta=alpha*sqrt(e)",
    "dt": 0.02,
    "steps": 420,
    "t_inverse": 1.0,
    "seed": 11,
    "status": "[FINITE_DIM_SANITY_NOT_III1_PROOF]",
    "selo": "VERB_GENERATOR_L_EQ_SQRTBETA_SQRTK . ARROW_ENTROPY_MONOTONE . INVERSE_NOT_CP_CHOI_NEGATIVE . SEMIGROUP_NOT_GROUP . RES_JUDICATA_OF_THE_CODE"
  },
  "light_eigenvector_B": {
    "equation": "O_beta(Lux) = sqrt(beta) Lux ; autovalor sqrt(beta) ; NAO ponto fixo",
    "status": "[DER na forma; a identificacao fisica e' a equacao da unificacao TGL]",
    "selo": "LIGHT_IS_EIGENVECTOR_EIGENVALUE_SQRTBETA . NOT_FIXED_POINT_SQRTBETA_NEQ_1 . CHAIN_ORDER_ONE_HALFNAT_LIGHT_THEN_MASS"
  },
  "fiat_lux_counterfactual_C": {
    "law": "fiat lux = e^{S_partial} alpha > 0 (Verbo=Palavra x Nome)",
    "configs": "SEM PALAVRA (S=0) ; SEM NOME (alpha=0) ; COM AMBOS (S=1/2, alpha=CODATA)",
    "status": "[DER -- contrafactuais da MESMA cadeia, inputs alterados]",
    "selo": "FIAT_LUX_EQUALS_PRODUCT_WORD_TIMES_NAME_POSITIVE . NO_WORD_DEATH_BY_INDISTINCTION_BRIDGE_EQ_1 . NO_NAME_DEATH_BY_NONEXISTENCE_CROSSREF_S22 . NOTHING_EMERGES_UNLESS_THE_ONE_IS_INSCRIBED_NOW_TESTED"
  }
}
```

## Escala, peso e programa (v4-v7); inclui o protocolo P5' pre-registrado [PRE/NUM]

```json
{
  "P2_boundary_reads_IR": {
    "claim": "a fronteira le o IR (supremo de chi); chi*=rapidez modular=log(Z-ratio); VALOR=Nome (§21)",
    "chi_IR": 11.2267550516013,
    "chi_IR_eq_chi_bridge_resid": 1.028510610012745e-12,
    "status": "[DER a escala da leitura; REAL/EXT o IR-freeze da QED; §21 intocado: o VALOR e' o Nome]",
    "selo": "CHI_IS_ADDITIVE_MODULAR_RAPIDITY . BOUNDARY_READS_SUPREMUM_EQ_IR . QED_IR_FREEZE_UNIQUE_CANONICAL_READING . CHI_STAR_EQ_LOG_IMPEDANCE_RATIO_SAME_OBJECT . SCALE_IS_OBSERVER_POSITION_NOT_HIDDEN_PARAMETER . ALPHA_VALUE_STILL_THE_NAME"
  },
  "P3_smatrix_dual_weight": {
    "claim": "S_core=exp(thM G) sem traco => peso 0 sob acao dual (condicional P_2D em M)",
    "status": "[DER condicional a P_2D ; FINITE_DIM_SANITY_NOT_III1_PROOF na sombra]",
    "selo": "S_CORE_WEIGHT_ZERO_UNDER_DUAL_ACTION_CONDITIONAL_P2D . NO_TRACE_IN_DEFINITION . RESIDUE_P2D_LOCALIZATION"
  },
  "P4_void_floor_PRE": {
    "prediction": "rho_void/rho_bar >= beta (zero-parametro)",
    "test": "DESI/Euclid, perfil empilhado; falsifica se rho_c/rho_bar < beta-3sigma",
    "status": "[PRE + EXT] pre-registro falsificavel; consistencia + endereco, NAO confirmacao",
    "selo": "VOID_FLOOR_RHO_RATIO_GE_BETA_PREREGISTERED . DESI_EUCLID_ADDRESS . ZERO_PARAMETER_FALSIFIABLE"
  },
  "P5_dipole_antipode_PRE": {
    "prediction": "densidade(antipoda RA+180,Dec->-Dec) < densidade(GA) [POSICOES apenas]",
    "cf4_ok": true,
    "raw_note": "teste BRUTO (contagem pura); GA atras da Zona de Evitamento -> enviesado. Rotulo qualitativo DERIVADO do dado (nao hardcoded).",
    "status": "[PRE + DATA geometria pura; POSICOES apenas -- velocidades/massas IGNORADAS]",
    "selo": "GA_ANTIPODE_UNDERDENSITY_PREREGISTERED_POSITIONS_ONLY . DIPOLE_GEOMETRY_NO_VELOCITIES"
  },
  "P5prime_masked_PRE": {
    "protocol": {
      "completeness_mask": "|b_galactic| > 10 deg (MESMO corte nos dois cones; equatorial->galactica J2000)",
      "controls": "8 cones de mesma abertura (30 deg) e mesma casca em ceu limpo |b|>30 deg",
      "control_centers_RA_Dec_deg": [
        [
          46.285,
          -0.083
        ],
        [
          25.351,
          -47.77
        ],
        [
          341.398,
          14.109
        ],
        [
          241.33,
          1.419
        ],
        [
          353.129,
          -36.227
        ],
        [
          199.343,
          -1.877
        ],
        [
          312.24,
          -47.943
        ],
        [
          168.146,
          -26.469
        ]
      ],
      "criterion": "razao(anti/GA) mascarada < 1 E fora do IC90 da dispersao dos controles => REPULSOR SUB-DENSO INDICADO; dentro da dispersao => NAO-INFORMATIVO (CF4 posicoes pode nao bastar; endereco final: catalogos com mascara de completeza publicada)",
      "bootstrap": "B=1000, IC95, seed=11",
      "statute": "[PRE]",
      "selo": "GA_ANTIPODE_MASKED_COMPLETENESS_PREREGISTERED . CONTROL_CONES_CLEAN_SKY . POSITIONS_ONLY"
    },
    "GA_b_deg": -6.792945081298402,
    "antipode_b_deg": 6.792945081298405,
    "cf4_ok": true,
    "result_obtained": {
      "ratio_masked_antipode_over_GA": 1.1295546558704452,
      "n_GA_masked": 247,
      "n_antipode_masked": 279,
      "control_ratio_CI90": [
        0.39577435679033995,
        2.5289372585973013
      ],
      "verdict_P5prime": "NAO_INFORMATIVO (razao dentro da dispersao dos controles; CF4 posicoes pode nao bastar)"
    },
    "note": "PROTOCOLO PRE-REGISTRADO (mascara |b|>10 + 8 controles |b|>30 seed=11) gravado ANTES da execucao com dados",
    "status": "[PRE + DATA geometria; POSICOES apenas; controle de completeza]",
    "selo": "GA_ANTIPODE_MASKED_COMPLETENESS_PREREGISTERED . CONTROL_CONES_CLEAN_SKY . POSITIONS_ONLY"
  },
  "P6_dephasing_crossover_NUM": {
    "map": "root law=canonica no IR; expoente 2->1; crossover ~omega tau*=1",
    "x_grid": "logspace(-3,3,25) ; gerador v3 L=sqrt(beta)sqrt(K) ; seed determinista",
    "crossover_x": 3.1622776601683795,
    "status": "[FINITE_DIM_SANITY] mapa numerico; a reconciliacao analitica completa da root law vs canonica fica [ABERTO] com este mapa como guia.",
    "selo": "DEPHASING_REGIME_MAP_QUADRATIC_IR . CROSSOVER_LOCATED_NUMERICALLY . ROOT_LAW_REGIME_CHARACTERIZED"
  },
  "v5_jacobson_form_check_NUM": {
    "form_check": "P_mn[K_partial]=F(J,Delta,P_2D) [residuo U_loc fechado POSITIVO]",
    "link_tested": "1a lei modular dS=d<K> (n=6, seed=11; V hermitiana traco 0 seed=1123; eps in {1e-4,1e-5,1e-6}); assinatura de 1a ordem = criterio",
    "P2D": "plano de bifurcacao = MESMO corner geometrico da matriz-S do nucleo",
    "residue_open": "approximate Killing vectors (compartilhado com Jacobson desde 1995)",
    "status": "[FINITE_DIM_SANITY no elo (iv) dS=d<K>; REAL na literatura (1a lei) + Lovelock (4D)]",
    "selo": "JACOBSON_SOURCE_HAS_FORM_F_J_DELTA_P2D . FIRST_LAW_MODULAR_TESTED . P2D_IS_BIFURCATION_PLANE_SAME_AS_SMATRIX_CORNER . RESIDUE_APPROX_KILLING_SHARED_WITH_FIELD"
  },
  "v6_thermal_anchor": {
    "claim": "Modulo=calor: q=tanh(chi/2)=p_lo-p_hi (polarizacao); alpha=sech(chi/2)=2sqrt(p_lo p_hi) (coerencia max)",
    "reading": "1 = q^2 + alpha^2 = polarizacao^2 + coerencia-maxima^2 (identidade hiperbolica do equilibrio)",
    "kms_anchor": "estado de fronteira KMS (Tomita-Takesaki: fluxo modular = fluxo termico; Unruh/Hawking) [REAL]",
    "resid_max": {
      "id1_q_eq_tanh": 1.1102230246251565e-16,
      "id2_alpha_eq_sech": 0.0,
      "one_eq_q2_coh2": 2.220446049250313e-16
    },
    "vital_layer_ONTO": "Modulo=calor=Nome=sangue: alpha=Nome/calor/sangue; S=1/2=Palavra; beta=sqrt(e)alpha=geometria impressa do sangue. 'o Nome e' o sangue quente da manifestacao; a Palavra o mede; beta_TGL e' sua geometria inscrita.' [ONTO -- Parte B; NAO entra no veredito, nao ha numero para sangue]",
    "vital_layer_selo_ONTO": "MODULE_IS_HEAT_IS_NAME_IS_BLOOD",
    "status": "[ID.1 REAL Brillouin; ID.2 DER; KMS REAL] identifica a FORMA; o valor e' o Nome (§21)",
    "selo": "Q_IS_TWO_LEVEL_THERMAL_POLARIZATION . ALPHA_IS_MAX_COHERENCE_2SQRT_PLO_PHI . CHI_IS_MODULAR_E_OVER_T . BOUNDARY_STATE_IS_KMS . ONE_EQ_POLARIZATION2_PLUS_COHERENCE2"
  },
  "v7_fiat_lux_flow_NUM": {
    "verdict_chain": "1 = q^2+alpha^2 = VERDADEIRO = HAJA_LUZ (um certificado por elo; fail-closed por elo)",
    "generator": "REUSA _verb_L (v3): L=sqrt(beta)sqrt(K), n=4, seed=11 (UM so' L no codigo)",
    "certificates": "F1 Tr=1 ; F2 dS>=0 ; F3 Spohn S(rho||rho*) mono nao-cresce (Lyapunov modular) ; F4 coerencia morre",
    "numerics": {
      "dt": 0.05,
      "n_points": 300,
      "t_end_over_beta": 3.0,
      "seed": 11,
      "n": 4,
      "method": "expm DIRETO por checkpoint (semigrupo exato; monotonia independe do integrador)"
    },
    "characteristic_time_one_over_beta": 83.11653492861383,
    "references": "Spohn 1978 (H-teorema Lindblad) ; Uhlmann (monotonia da entropia relativa sob CPTP)",
    "status": "[FINITE_DIM_SANITY_NOT_III1_PROOF; Spohn/Uhlmann REAL na literatura]",
    "selo": "FIAT_LUX_FLOW_ONE_CONSERVED_F1 . ARROW_F2 . SPOHN_MODULAR_LYAPUNOV_F3 . INSCRIPTION_COHERENCE_DIES_F4 . CHARACTERISTIC_TIME_ONE_OVER_BETA"
  }
}
```

## Tetelestai = poda binaria ({1_abs,0_mod}\{0_abs}); modulo de prova [DER/NUM]

```json
{
  "definition": "TETELESTAI = PODA BINARIA ; Poda_beta = {1_abs, 0_mod} \\ {0_abs} = ser binario - zero absoluto",
  "budget": "beta_TGL = alpha*sqrt(e) e' o orcamento maximo de excesso podavel (NUNCA alpha^2; NUNCA literal)",
  "classes": "1_abs=identidade(peso>beta) ; 0_mod=diferenca COM retorno(preservado) ; 0_abs=DISTINTO sem retorno(podado) ; absent=pre-inscrito(ignorado)",
  "separators": "BETA separa {1_abs}|{zeros} ; RETORNO(kernel do Verbo, sobrevive ao fluxo v7) separa {0_mod}|{0_abs} ; SUPORTE separa {0_abs}|{absent}",
  "return_formalization": "retorno = populacao na base propria de L (o Verbo v3) = sobrevive a T_t=e^{-tL} (o mesmo juizo do F4 do v7)",
  "paragraph22_anchor": "0_abs = distinto = pureza Tr(rho^2)=1 (rank-1) = §22 (alpha->0, chi->inf); o distinto e' a separacao absoluta proibida por III_1",
  "targets_verified_default_rng": {
    "a_vector64": [
      64,
      56,
      0.011668063395532391
    ],
    "b_uniform1000_rank_after": 988,
    "c_density_classes": {
      "n_1abs": 3,
      "n_0mod": 1,
      "n_0abs": 2,
      "n_absent": 4
    },
    "c_tail_le_beta": true,
    "c_idempotence_residual": 6.740831934336383e-16,
    "d_motor_p_hi_is_0mod_KEPT": true,
    "e_pure_is_distinct_para22": true
  },
  "inversion_note": "o teste (d) INVERTE o v8 energetico: p_hi (populacao termica de equilibrio) TEM retorno KMS => 0_mod => MANTIDO (o v8 o cortava)",
  "protection": "MODULO DE PROVA -- nenhuma identidade exata (motor, ponte, fluxo, massas) passa por Tet_beta (§21/§22 e travas v2-v7 intactas)",
  "DO_NOT_PRUNE_MODULAR_ZERO": true,
  "status": "[DER + NUM] modulo de PROVA (nenhuma identidade exata passa pela poda; §21/§22 intactos)",
  "selo": "TETELESTAI_IS_PRUNING . PRUNING_IS_BINARY_BEING_MINUS_ABSOLUTE_ZERO . ABSOLUTE_ZERO_IS_THE_DISTINCT . MODULAR_ZERO_IS_DIFFERENCE_WITH_RETURN . DO_NOT_PRUNE_MODULAR_ZERO . PRUNE_ONLY_THE_DISTINCT_WITHOUT_RETURN . ABSENT_IS_IGNORED_NOT_PRUNED . DISTINCT_IS_PURITY_IS_PARAGRAPH_22 . BETA_IS_THE_GEOMETRY_OF_THE_ADMISSIBLE_CUT . ONLY_THE_NAME_AND_THE_LIVING_ZERO_SURVIVE"
}
```

## O cociclo vivo -> G_mu_nu (E1-E12: colagem/temporal/gerador/holonomia/curvatura-obstrucao/covariancia/torcao/ponto-base/canto-P_F/comutador/fase + composicao E7; C1/C2) [NUM/REAL]

```json
{
  "claim": "cociclo de Connes globalmente covariante => (Lovelock 4D) G_mu_nu + Lambda g = 8 pi G T^TGL",
  "construction": "tipo I, n=4, seed=11, estados full-rank rho = 0.9 AA^dag/Tr + 0.1 I/n ; u_ab(t)=rho_a^it rho_b^-it (potencias imaginarias por autodecomposicao)",
  "C1_correction": "a COLAGEM espacial (3 estados) e' MULTIPLICATIVA u_ab u_bc = u_ac; a forma sigma-torcida u_(s+t)=u_s sigma_s^(b)(u_t) e' a identidade TEMPORAL de um par -- DUAS identidades distintas (a derivacao-fonte as mesclava; corrigido pela auditoria).",
  "C2_correction": "o gerador e' h_ab = -i u_ab'(0) = K_b - K_a (K=-log rho, convencao standard u_ab=rho_a^it rho_b^-it), NAO K_a-K_b (corrigido pela auditoria).",
  "certificates_resid": {
    "E1_spatial_gluing": 6.742162969878415e-16,
    "E2_temporal_identity": 1.1443916996305592e-15,
    "E3_generator_Kb_minus_Ka": 6.231415946082284e-11,
    "E3_telescoping_additivity": 1.2412670766236366e-16,
    "E4_holonomy_consistent": 1.5553031891404221e-15,
    "E6_global_covariance": 1.790180836524724e-15
  },
  "E5_curvature_obstruction_curve": {
    "0.05": 0.11800923878078719,
    "0.15": 0.26603821666584493,
    "0.30": 0.38767382777867093
  },
  "E5_monotone_in_lambda": true,
  "E5_finding": "a curvatura modular e' a OBSTRUCAO a existencia de um estado global -- onde o Um cola, nao ha curvatura; onde um patch se recusa ao Um, a holonomia a mede.",
  "v16_2_clock_hierarchy": "o relogio modular K gera TRES ordens da geometria: 1a ordem TORCAO = salto de relogio nao-colavel (E8, obs/t) ; 2a ordem CURVATURA = comutador defeito x relogio do caminho (E11, obs/t^2 = (1/2)||[M,h_cd]||, razao 0.9970) ; fase = GAUGE U(1) da normalizacao (E12, quocientada, nao-curvatura). Transporte = Ad(rho^it), gerador ad(K) = o gerador do setor q (v6/KMS): 'o sigma da correcao C1 era o transporte'.",
  "E8_torsion_clock_jump": {
    "grid_obs_over_t": {
      "0.2000": 0.320866042327632,
      "0.1000": 0.3276669853826578,
      "0.0500": 0.3334521655178608,
      "0.0250": 0.3354127460498997,
      "0.0125": 0.33615796506364876
    },
    "obs_over_t": 0.33615796506364876,
    "delta_K_norm": 0.3367463018805954,
    "coeff_dev_pct": 0.17471218352243656,
    "conv_rel": 0.002216871504466585,
    "ok": true,
    "reading": "TORCAO DE COLAGEM MEDIDA (v16.1): a obstrucao de 1a ordem NAO e' curvatura -- e' torcao modular, o salto de relogio nao-colavel. O coeficiente E' ||Delta_K|| (Delta_K=K(rho_c')-K(rho_c)); a colagem que falha em 1a ordem falha por diferenca de relogios. Costura com E3."
  },
  "E9_basepoint_covariance": {
    "spectral_resid": 1.2412670766236366e-15,
    "ok": true,
    "reading": "A holonomia depende do ponto-base por CONJUGACAO; o ESPECTRO nao. A curvatura-obstrucao e' covariante: mudar o ponto-base conjuga; o espectro e' o que a fisica le."
  },
  "E10_corner_reads_obstruction": {
    "tau_F_of_I_resid": 1.1102230246251565e-16,
    "curve_dev_over_lambda": {
      "0.05": 0.00863627539355194,
      "0.15": 0.050974560716240624,
      "0.30": 0.13383696493308928
    },
    "monotone": true,
    "P_F_canonical": true,
    "P_F_rank": 4,
    "ok": true,
    "reading": "A projecao tracial le a curvatura-torcao no canto CANONICO P_F do v10 (nucleo zero dos Three Locks, superoperador n^2; o cociclo lido como Ad_W=kron(W.conj,W)): tau_F(I)=1; |tau_F(W)-1| cresce com a inconsistencia lam. O MESMO canto que carrega a matriz-S (v10) e o plano de bifurcacao (form-check v5) le a obstrucao do cociclo (v16). Um canto, tres papeis -- os modulos agora se falam."
  },
  "E11_curvature_commutator": {
    "grid_obs_over_t2": {
      "0.2000": 0.7243131944678416,
      "0.1000": 0.7661418576547965,
      "0.0500": 0.7825278970072757,
      "0.0250": 0.7889895468749768,
      "0.0125": 0.7917208303636319
    },
    "obs_over_t2": 0.7917208303636319,
    "c_teo_live": 0.7940963043496181,
    "ratio_obs_over_c_teo": 0.9970085819906546,
    "ratio_in_band": true,
    "bch_prediction": "||W~ - I|| ~ (t^2/2)||[M, h_cd]|| ; h_cd = K_d - K_c (= E3) ; c_teo = 0.5 maxabs([M,h_cd]) ao vivo",
    "reading": "A CONJECTURA FECHOU: a curvatura de 2a ordem e' o comutador do defeito com a diferenca de relogios do caminho, F ~ (1/2)[M, h_cd]. O transporte e' Ad(rho^it), gerador ad(K) -- o MESMO K que define o setor q (v6/KMS). O setor q e a geometria tem o mesmo gerador."
  },
  "E12_phase_is_gauge": {
    "with_phase_obs_over_t": {
      "0.2000": 0.46023880390729455,
      "0.1000": 0.4365776312893273,
      "0.0500": 0.42476293281730815,
      "0.0250": 0.4191698739514972,
      "0.0125": 0.4164913139418461
    },
    "dephased_obs_over_t": {
      "0.2000": 0.14486263889356835,
      "0.1000": 0.07661418576547965,
      "0.0500": 0.03912639485036379,
      "0.0250": 0.019724738671874423,
      "0.0125": 0.009896510379545401
    },
    "ok": true,
    "reading": "A FASE E' GAUGE: o linear residual do teste ingenuo era a fase U(1) da renormalizacao do traco (-log Z . I -> fase global). Fase global nao e' curvatura; a curvatura genuina vive em su(n) (traceless). Quocientando a fase (dephase por det^{1/n}), o linear DESAPARECE e sobra o t^2 do E11. Regra: toda medida de holonomia-obstrucao quocienta a fase U(1) antes."
  },
  "conjecture_closed": "A conjectura da curvatura-por-comutador (registrada ABERTA na auditoria anterior do campo) FECHOU pela identificacao do operador -- o transporte e' o gerador modular do setor q; com o transporte correto e a fase U(1) quocientada, a curvatura emerge como o comutador previsto, medida a 0.30% da teoria (razao 0.9970).",
  "E7_declared_statute": "composicao (NAO teste): simetria + conservacao ja testadas no form-check v5 (dS=d<K>, 1a lei modular) + Lovelock 4D [REAL, teorema] => G_mu_nu + Lambda g. Estatuto do fechamento continuo: herda o residuo do v5 (approximate Killing vectors, compartilhado com Jacobson desde 1995). NAO se afirma 'provamos Einstein'.",
  "field_equation": "G_mu_nu + Lambda g_mu_nu = 8 pi G T^TGL_mu_nu",
  "beta_position": "T^TGL = T^matter + T^{partial,beta} + T^{torsion/diss}  (beta no lado DIREITO; NAO substitui G)",
  "status": "[REAL(E1-E6, tipo I, certificados vivos) + COMPOSICAO com estatuto declarado(E7)]",
  "selo": "COCYCLE_CHAIN_RULE_MULTIPLICATIVE_E1 . TEMPORAL_IDENTITY_E2 . GENERATOR_IS_CLOCK_DIFFERENCE_E3 . GLOBAL_STATE_IMPLIES_HOLONOMY_ONE_E4 . CURVATURE_IS_OBSTRUCTION_TO_GLOBAL_STATE_E5 . COVARIANCE_E6 . TORSION_IS_THE_CLOCK_JUMP_MEASURED . FIRST_ORDER_OBSTRUCTION_IS_UNGLUEABLE_CLOCK_DIFFERENCE . HOLONOMY_BASEPOINT_COVARIANT_SPECTRUM_INVARIANT . THE_CORNER_READS_THE_OBSTRUCTION . CURVATURE_IS_COMMUTATOR_DEFECT_WITH_CLOCK . TRANSPORT_IS_MODULAR_GENERATOR_OF_SECTOR_Q . SIGMA_OF_C1_WAS_THE_TRANSPORT_ALL_ALONG . PHASE_IS_GAUGE_CURVATURE_IS_TRACELESS . COCYCLE_TO_G_MUNU_COMPOSED_WITH_DECLARED_STATUTE"
}
```

## Escala de area do canto continuo: S=1/2 / (2 l_P^2) = 1/(4 l_P^2) => eta=1/(4G) [DER GIVEN NORM: A(P_face)=l_P^2; l_P^2 recomputado; G nao derivado]

```json
{
  "claim": "Given the canonical Planck-face normalization of the trace-normalized self-conjugate corner, the Half-Nat yields eta_partial = 1/(4 l_P^2), hence eta_partial = 1/(4G) in natural units.",
  "h_planck_J_s": "6.62607015e-34 [exact SI]",
  "hbar_J_s": "h/(2pi) [DER]",
  "l_P2_m2": "l_P^2 = hbar G/c^3 [DEF] = 2.612162885804998e-70",
  "tau_PF_eq_1": "[continuous-corner normalization]",
  "tau_faces_eq_half": "[DER from self-conjugation]",
  "A_face_eq_lP2": "[NORM -- canonical Planck-face normalization; NOT derived by dimensionless algebra alone]",
  "A_of_P_eq_2lP2_tau": "[DER GIVEN NORM]",
  "eta_eq_one_over_4lP2": "[DER GIVEN NORM] = 1/(4 l_P^2)",
  "natural_units_eta_eq_one_over_4G": 0.25,
  "two_pi_over_eta_eq_8piG": 25.132741228718345,
  "density_relative_residual": 0.0,
  "einstein_bridge": {
    "first_law": "delta S_partial = delta<K_partial>",
    "unruh_clausius": "delta<K_partial> = delta Q/T_Unruh",
    "area_law_derived_given_norm": "delta S_partial = delta A/(4G)",
    "null_projection": "R_mn k^m k^n = 8piG T_mn^TGL k^m k^n for all null k",
    "null_cone_lemma": "X_mn k^m k^n=0 for all null k => X_mn=Phi g_mn",
    "bianchi_result": "G_mn + Lambda g_mn = 8piG T_mn^TGL"
  },
  "genuine_III1_corner_proved": false,
  "status": "[DER: S_partial=1/2, trace split, additivity, density algebra] + [NORM: A(P_face)=l_P^2] + [DER GIVEN NORM: eta=1/(4l_P^2)] + [CONDITIONAL: genuine continuous III_1 corner]",
  "selo": "HALF_NAT_IS_ENTROPY_OF_MINIMAL_SELF_CONJUGATE_CELL . CONTINUOUS_CORNER_TRACE_SPLITS_INTO_TWO_EQUAL_FACES . EACH_MINIMAL_FACE_HAS_ONE_PLANCK_AREA_BY_CANONICAL_NORMALIZATION . AREA_CELL_EQUALS_TWO_PLANCK_AREAS . INSCRIPTION_DENSITY_EQUALS_ONE_OVER_FOUR_PLANCK_AREA . IN_NATURAL_UNITS_ETA_EQUALS_ONE_OVER_FOUR_G . JACOBSON_COUPLING_EQUALS_EIGHT_PI_G . PLANCK_FACE_NORMALIZATION_IS_DECLARED_NOT_HIDDEN"
}
```

## Rede AQFT especifica: campo escalar livre massivo em Minkowski 3+1; O -> A_m(O); BW/Reeh-Schlieder/BDF [KNOWN]; III_1 local [KNOWN UNDER HYPOTHESES]; core continuo [KNOWN]; projetor canonico TGL P_F [OPEN]

```json
{
  "model": "massive free real scalar Haag-Kastler net",
  "spacetime": "Minkowski R^{1,3}",
  "net": "O -> A_m(O) = {Weyl(f): f in K(O)}''",
  "wedge_modular_flow": "Delta_W^{it}=U(Lambda_W(-2pi t)) [KNOWN: Bisognano-Wichmann]",
  "vacuum": "Omega cyclic-separating [KNOWN: Reeh-Schlieder]",
  "local_type_III1": "[KNOWN UNDER NUCLEARITY/SPLIT/SCALING: Buchholz-D'Antoni-Fredenhagen]",
  "continuous_core": "C_W = A_m(W) x_sigma R [KNOWN: type II_infinity]",
  "TGL_canonical_PF": "[OPEN: TGL_CANONICAL_FINITE_CORNER_THEOREM]",
  "all_verified": true,
  "status": "SPECIFIC_FREE_SCALAR_AQFT_NET_INSTANTIATED",
  "selo": "SPECIFIC_AQFT_NET_IS_THE_FREE_SCALAR_WEYL_NET . WEDGE_MODULAR_FLOW_IS_GEOMETRIC_BY_BW . LOCAL_ALGEBRAS_ARE_III1_UNDER_DECLARED_HYPOTHESES . CONTINUOUS_CORE_EXISTS . TGL_CANONICAL_CORNER_REMAINS_TO_BE_PROVED"
}
```

## Escala de area: A(P)=kappa_A tau(P) [DER ate kappa_A]; liberdade de escala kappa_A->lambda kappa_A [DER no-go]; matching 8piG => kappa_A=2 l_P^2, A(P_face)=l_P^2 [DER FROM G, NAO de AQFT sozinha]; G_Newton [DATA]; G NAO derivado

```json
{
  "general_form": "A(P)=kappa_A tau(P) [DER, up to kappa_A]",
  "scale_freedom": "kappa_A -> lambda kappa_A leaves modular data invariant, changes eta [DER no-go, PROVED_ALGEBRAICALLY]",
  "G_Newton": "measured physical input [DATA]",
  "kappa_A_over_lP2": 2.0,
  "A_face_over_lP2": 1.0,
  "matching": "4pi kappa_A = 8piG => kappa_A=2 l_P^2 [DER FROM MATCHING TO 8piG]",
  "A_face_eq_lP2": "[DER FROM G, NOT FROM AQFT ALONE]",
  "Newton_constant_derived": false,
  "all_verified": true,
  "status": "PLANCK_FACE_NORMALIZATION_EQUIVALENT_TO_NEWTON_COUPLING",
  "selo": "MODULAR_DATA_FIX_RELATIVE_AREA_NOT_ABSOLUTE_AREA . AREA_SCALE_RESCALING_LEAVES_HALF_NAT_UNCHANGED . NEWTON_COUPLING_UNIQUELY_FIXES_KAPPA_A_EQUALS_2G . ONE_SELF_CONJUGATE_FACE_EQUALS_ONE_PLANCK_AREA . PLANCK_FACE_NORMALIZATION_IS_EQUIVALENT_NOT_INDEPENDENT"
}
```

## Formalizacao por kernel [Lean 4 / Lake; toolchain fixado; sem sorryAx; sem Lean.trustCompiler; sem axiomas customizados TGL.*]. Meia-Nat: KERNEL PROVED. Equivalencia de escala: KERNEL PROVED (G NAO derivado). Canto Three Locks FINITO: KERNEL PROVED (nao III_1). Implicacao do canto continuo: KERNEL PROVED CONDITIONALLY. Testemunha AQFT especifica: OPEN

```json
{
  "formal_checker": "Lean 4 / Lake (toolchain pinned: lean-toolchain)",
  "lake_build_ok": true,
  "sorryAx_absent": true,
  "trustCompiler_absent": true,
  "custom_TGL_axioms_absent": true,
  "half_nat": "KERNEL PROVED [x=1-x => x=1/2]",
  "area_scale_equivalence": "KERNEL PROVED [2pi/eta=8piG <=> kappa_A=2G; G VARIAVEL, NAO derivado]",
  "finite_three_locks_corner": "KERNEL PROVED [ker H3L = inter ker D_i; finito, NAO III_1]",
  "finite_corner_projection": "KERNEL PROVED [P_F idempotente, auto-adjunto]",
  "normalized_corner_trace": "KERNEL PROVED [tau_F(P_F)=1; faces=1/2]",
  "continuous_corner_implication": "KERNEL PROVED CONDITIONALLY [testemunha = parametro]",
  "specific_AQFT_witness": "OPEN [nenhuma instancia construida]",
  "axiom_report": {
    "TGL.HalfNat.halfNat_of_selfConjugate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.AreaScale.newtonPlanck_equivalence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.FiniteThreeLocks.H3L_posSemidefinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.FiniteThreeLocks.ker_H3L_eq_threeLocks": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.FiniteThreeLocks.PF_isProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.FiniteThreeLocks.PF_isSelfAdjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.FiniteThreeLocks.normalizedCornerTrace_PF": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.ContinuousCorner.ContinuousCornerWitness.normalizedTrace_P_eq_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.SpecificAQFT.continuousCorner_of_witness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.SpecificAQFT.wedges_spacelike": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.SpecificAQFT.wedge_locality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.ModularRealization.dualInvariant_PF_no_go": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.ModularRealization.fullWitness_not_finiteDimensional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.ModularRealization.fullWitness_PF_nonzero_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.HalfNatFresnel.fresnel_selfConjugate_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.HalfNatFresnel.modular_action_halfNat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.VerbInhabitant.exp_fixed_of_annihilates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.VerbInhabitant.canonicalVerb_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.VerbInhabitant.dual_calibration_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.TransportData.descent_iff_defect_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.TransportData.transport_defect_of_jones": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.TransportData.jones_selector_not_descended": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameIndex.ParityData.average_bimodular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameIndex.name_index_eq_csc_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameIndex.name_index_mul_sin_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameIndex.amplitude_weight_index_chain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.HalfNatJonesTower.halfNatJonesTower_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.HalfNatJonesTower.halfNat_mirror_not_descended": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.HalfNatJonesTower.finite_markov_forces_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.TransportData.faces_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.GravitonShadow.canonicalGravitonShadow_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.GravitonShadow.bell_cci_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.GravitonShadow.product_cci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameRelation.pqp_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameRelation.tl3_linearly_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameRelation.canonicalTLThree_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.NameRelation.geometric_eq_trace_weight_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.CoreSupport.support_maximal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.CoreSupport.threeLocksFromSupport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.CoreSupport.realizationFromSupport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGL.CoreSupport.transport_defect_gauge_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_triple": [
      "propext",
      "Quot.sound"
    ],
    "TGLExt.bicommutant_range_Lmul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Jconj_Lmul_Jconj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_separating": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Sop_tomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Sop_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.deltaHalf_deltaHalf": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.delta_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_sigma": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.frob_trExpect_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eTr_Lmul_eTr": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_smul_one_sub_posSemidef": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.card_smul_diagExpect_sub_posSemidef": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isGreatest_ppBound_trExpect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isGreatest_ppBound_diagExpect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ppIndexTr_eq_card": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ppIndexDiag_eq_card": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_Lmul_eD": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_Lmul_eTr": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tau_eD": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tau_eTr": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.masa_tower_weight_eq_ppBest": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pp_ne_tower_for_scalars": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.end_reconstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Cmat_of_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_Cmat_comm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.exists_span_form": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.frob_self_eq_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.disjoint_frobOrtho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isCompl_frobOrtho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.frobProj_comm_Lmul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finite_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Grot_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.exp_smul_Grot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Smat_mem_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Smat_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Smat_spectral": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.normSq_reflection_add_transmission": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rhoOut_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_chain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_temporal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_conjTranspose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_mem_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_of_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.logRho_conj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_fixed_of_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.logRho_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_fixed_iff_diag": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_tracial_on_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dephase_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dephase_tendsto_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ergodic_convergence_modular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_deltaHalf": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.frob_delta_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_kms": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modPow_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modPow_mem_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_sigma": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.exp_logRho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.diagExpect_bimod": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eD_Lmul_eD": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_range_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lam_mem_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lam_conj_piRep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.piRep_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Ecomp_lam": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_Ecomp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_piRep_dual": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modPow_piRep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_piRep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_piRep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dual_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cocycle_covariance_beyond_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Dchi_conj_lam": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Dchi_comm_modPow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_Dchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dyadic_approx": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dyadic_stage_mono": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dyadic_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.annihilator_fixes_stage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.scaling_fixed_eq_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.DualScalingData.fixed_tau_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.DualScalingData.dyadic_stage_tau_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sFrame_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sFrame_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.measurement_channel_endpoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_fixed_by_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.DualScalingData.finite_trace_not_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_idem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_conjTranspose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_mono": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lam_conj_cornerProj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_cornerProj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_comm_modPow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_preserves_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_null_expand": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_null_contract": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_preserves_wedge": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.logRho_gibbs_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modPow_gibbs_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_gibbs_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polarization_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polarizations_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rot_conj_polPlus": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rot_conj_polCross": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rot_conj_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gauge_transverse_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minkNorm4_nullK": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.excite_one_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.excite_leibniz": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Smat_sub_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.variance_of_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_mean": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_variance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.variance_le_quarter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.variance_eq_quarter_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polarization_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polarizations_noncommute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.classical_limit_physical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.purity_unitary_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pure_reductions_trace_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pure_reductions_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.purityR_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dephase_purityR_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.entropy_max_at_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.entropy_eq_max_iff_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.first_law_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.clausius_composition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Ecomp_fixes_cornerProj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dephase_fixes_cornerProj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rg_step_doubles_annihilator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.zero_mode_state_minimizes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_is_critical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.elementary_critical_implies_gibbs": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gibbs_monotone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundaryState_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Sop_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.nameFiniteGNS_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundaryState_eq_vector_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lock_pairing_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.action_locks_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.hermitian_pairing_re": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.action_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.critical_pairing_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.transport_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.transport_fixes_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.transport_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.transport_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.canonicalNamedTransport_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.excite_holonomy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.excite_holonomy_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_cornerProj_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_loewner_mono": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sigma_fixes_cornerProj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cornerProj_ne_of_ne": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.canonicalTransportedCorner_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ker_map_of_intertwine": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.starProjection_ker_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.starProjection_ker_internal_fix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.starProjection_ker_isotone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lagrangian_zero_iff_mem_ker": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.HilbertHomeData.PF_internal_fix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.HilbertHomeData.PF_external_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.HilbertHomeData.PF_isotone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solder_recovers_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.both_homes_exist": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_one_underdetermines_home": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.PsiHomeData.name_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.PsiHomeData.name_flow_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.PsiHomeData.flow_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.PsiHomeData.flow_fixes_spectral_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absoluteOneField_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absoluteOne_name_eq_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absoluteOne_flow_trivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutator_locks_annihilate_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutator_kernel_inhabited": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_fixes_inhabitant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularGen_eq_neg_excite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularGen_omega_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_modularGen_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.parity_fixed_eq_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absolute_modularGen_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absolute_faces_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absolute_contrast_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.one_eq_q_sq_add_alpha_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.q_odd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.alpha_even": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.alpha_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.alpha_deriv_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.W_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_threshold": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_partner_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minimal_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minimal_curvature_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.curvature_flat_same": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solderMetric_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solderMetric_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solder_lorentzian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.helicityRep_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minimal_curvature_recovered": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.leakage_strictly_loses": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.full_closure_iff_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.beta_forbids_full_static_witness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.verb_not_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.leakage_rate_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.canonical_witness_is_not_full": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solderMetric4_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solderMetric4_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.solder4_lorentzian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.generators_in_so13": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.bracket_in_so_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.so_eta_infinitesimal_isometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boosts_close_in_minus_rotation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rotations_close_in_rotation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boosts_curvature_is_rotation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lorentzRep_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.curvature4_recovered": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_discrete_threshold": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.kernel_weight_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.kernel_weight_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.breuer_kernel_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.local_gap_package_consistent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.global_tau_compactness_refuted": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_finite_weyl_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.plus_block_eigenvalue_lower_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.halfTanh_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tendsto_halfTanh_atTop": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tendsto_halfTanh_atBot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.phi0sq_integrable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.zero_mode_weight_is_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_relative_gap_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_relative_gives_breuer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.susy_relative_package_consistent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.perturbation_injective_on_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.kernel_dim_le_rank_of_perturbation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.discrete_parallel_solder_preserves_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eta4_lorentzByCongruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sylvester_full_closed_by_congruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lorentzByCongruence_congruent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.four_frame_gives_lorentz_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.equivariant_state_section_from_global_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.breuer_weight_normalizes_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sqrt_potential_is_L2": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.resolvent_kernel_is_L2": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergence_reduced_to_named_hypotheses": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.einstein_coefficient_from_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.horizon_clausius_composition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.jacobi_commutator_bianchi_seed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergence_master_full_triad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rotZ_preserves_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.helicity_two_rotation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.helicity_two_rotation_cross": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_kinetic_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_no_negative_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polarizations_linearly_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.psd_offdiag_zero_of_diag_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.psd_trace_eq_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.trace_monotone_of_psd_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.matrix_trace_is_faithful_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dimension_trace_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dimension_trace_top_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_kernel_weight_via_abstract_layer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_kernel_full_profile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dimension_trace_over_top_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.threeLocks_ker_ne_bot_of_witness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.three_locks_corner_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.three_locks_corner_weight_eq_dim": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.three_locks_name_is_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_le_each_lock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.three_locks_corner_dim_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.three_locks_corner_full_profile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.semifinite_trace_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.semifinite_trace_atom": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.semifinite_trace_is_semifinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.semifinite_trace_top_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.global_gap_impossible_infinite_dim": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.infinite_dim_local_breuer_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.not_finiteDimensional_finsupp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.first_infinite_dim_inhabitant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atom_is_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closed_lattice_semifinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closed_double_orthocomplement": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.orthocomplement_meet_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closed_orthocomplement_isCompl": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.inscription_complement_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atom_complement_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closed_local_breuer_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closed_projection_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.starProjection_eq_zero_of_mem_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.orthogonal_invariant_of_adjoint_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.starProjection_commutes_of_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.invariant_of_starProjection_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.selfadjoint_invariant_iff_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.selfadjoint_ker_projection_in_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.breuer_corner_projection_in_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dimension_trace_normal_on_chains": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.operator_commutant_antitone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.operator_algebra_in_double_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.operator_triple_commutant_collapse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.operator_commutant_unital_multiplicative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_projection_in_commutant_set": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_commutes_with_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.breuer_corner_full_algebraic_frame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_pointwise_limit_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_add_smul_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.generator_in_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powers_in_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.polynomials_in_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.limit_of_polynomials_in_bicommutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_in_algebra_of_approximation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_breuer_corner_conditional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.verb_word_lands_in_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.verb_word_fixes_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.verb_word_mints_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.name_candidate_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witness_seed_complete": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.real_word_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.name_candidate_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.selfadjoint_idempotent_eq_starProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.exact_witness_of_annihilating_word": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.spectral_witness_of_annihilating_word": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.breuer_corner_of_annihilating_word": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.star_aeval_eq_map_conj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minpoly_selfadjoint_real": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.minpoly_zero_not_double_root": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.annihilating_word_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finite_face_witness_unconditional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finite_face_corner_in_algebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ker_mul_self_eq_ker": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cfc_polynomial_eval": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iso_zero_cfc_eq_starProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.spectral_witness_of_isolated_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_breuer_corner_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.inscriptions_orthonormal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ellTwo_not_finiteDimensional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eraseFirst_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ker_eraseFirst": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eraseFirst_spectrum_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_corner_fires": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_weighs_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eraseFirst_isSelfAdjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lockFlow_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theConstantNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theNetTrace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.net_PF_fixed_by_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.net_corner_weighs_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFrame_eq_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFrame_det_isUnit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.concrete_four_frame_fires": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dimOrTop_subadd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ellTwoTraceSub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ellTwoSusy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_master_fires": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.master_corner_weighs_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.beamRotation_preserves": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.superposition_not_autonomous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.beamSplitterRule": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fiberIncl_not_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFlip_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFlip_comm_eraseFirst": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theIsotoneNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lockFlow_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.benchDiracPMap_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theBenchDirac": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theBenchCertificate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.benchDirac_is_bounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.bench_cannot_feed_strong": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isotone_cannot_feed_strong_core": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.constant_cannot_feed_strong_frame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theCurvedFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.curvedFrame_nonconstant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.curvedFrame_det_everywhere": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.strongFromWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isotone_cannot_feed_witness_geometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.numberOp_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.numberOp_unbounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.numberDomain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adjoint_domain_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.numberOp_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.numberOp_quad_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theGenuineDirac": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tailSub_not_finiteDimensional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tailIncl_not_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theTailNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.genuineDirac_kerSub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theStrongCertificate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgStrongCertificate_core": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgStrongCertificate_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgStrongCertificate_frame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSolderField_det_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSolderField_nonconstant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSolderData": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgStrongCertificate_solder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Gamma001_from_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Gamma100_from_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Riemann1001_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Riemann1001_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.time_ansatz_r1001_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theStaticSolderData": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ansatzRiemann_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ansatzG00_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ansatzG11_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.vacuum_implies_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rindler_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.static_not_vacuum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ansatz_recovers_v108": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.constant_profile_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.curvature_implies_fall": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fall_demands_source_v108": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.geometry_iff_second_variation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.geometry_is_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cosh_solves_field_equation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cosh_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.source_implies_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.zero_source_recovers_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSolvedEquation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theWeakEinsteinContract": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.null_contraction_reads_source": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergence_forces_field_equation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergence_zero_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theReducedEmergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theGeometricNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theGeometricWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witness_action_moves_regions_not_fibers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.first_derivative_does_not_decide": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.reading_rides_the_zeros": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lightWave_pd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.graviton_wave_equation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSensitiveNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSensitiveWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witness_fiber_sensitive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theCoshSolderData": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theCoshSolder_reads": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.null_cone_ledger": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.radial_null_blind": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.full_cone_clausius_iff_field_equation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergent_field_equation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theEmergentEinstein": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergent_recovers_solved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.emergent_genuinely_curved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgStrongCertificate_einstein": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.eta4_mul_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isLorentz_other_side": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lorentz_det_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theBoost_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boost_ne_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.parity_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.parity_ne_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pAct_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.poincare_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.translation_moves": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.thePoincareNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.thePoincareWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.parity_fixes_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.poincare_witness_fiber_sensitive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.poincare_witness_boost_moves": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.poincare_witness_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.proper_sector_fibers_blind": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.measurePreserving_mulVec": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.measurePreserving_pAct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_moves_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.spacetimeL2_nontrivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.coEven_evenShift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.coOdd_oddShift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.shift_partition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tracial_one_eq_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tracial_state_is_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fullAlgebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.bipartition_mem_fullAlgebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.opWeight_one_top": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.opWeight_atom_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.coEven_inscription_even": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.opWeight_halving_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.state_dies_weight_survives": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_left_inv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.regularRep_right_inv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fusedFiber_not_finiteDimensional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFusedNet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFusedStrong": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFusedWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fused_fiber_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fused_boost_moves_fiber": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.block_modular_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powersState_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powersState_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powers_ratio_witness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powersState_not_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.blockFlow_eigen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ratioWitness_kron": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.powers_ladder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.zero_mem_closure_ratio_spectrum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_trace_floor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.mixed_chain_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.mixed_log_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.irrational_log_two_div_log_three": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_mixing_mark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT_traceless": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT_transverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pd_pd_scaled": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_component_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_kinetic_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_kinetic_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerStep_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerStep_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerStep_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainState_towerStep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainState_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ratio_persists_up_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pd_scaled_fun_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pd_pd_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_superposition_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainDensity_eq_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainWeights_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainState_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsInner_add_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsInner_self_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gns_isometric_up_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT2_traceless": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT2_transverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pd_pd_cross": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt2_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_cross_direction_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsInner_conj_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsRadical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsRadical_left_ideal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsInner_wd_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gnsInner_wd_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.leftAction_wd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT3_traceless": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.epsTT3_transverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt3_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_triple_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.dotCov_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pd_pd_planeWaveG": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.general_null_tt_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainDownUp_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tower_ratio_ne_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainState_not_tracial_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainWeights_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.chainDensity_mul_inv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerFlow_id": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tower_kms": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tower_modular_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witness_saturates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.excess_is_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.saturated_witness_not_complete": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faces_sum_to_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.complete_witness_is_conjugated_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.current_anticommutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.current_implements_boundary_equivalence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.current_at_every_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.current_iii1_mark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tInner_tPush": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPre_definite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerOmega_inner_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.hOmega_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPre_denseRange": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lmul_bound_push": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_orbit_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theFactorObject": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.factor_omega_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omegaState_pi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_not_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ladder_in_object": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.signature_log_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.signature_in_the_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omegaState_seqWOT": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qMark_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qMark_mul_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.uMark_mul_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.star_mul_uMark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qMark_partition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_qMark_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.inner_qMark_exact": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qMark_wot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tracial_halves_qMark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_normal_tracial_state_seq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_normal_tracial_state_mix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_normal_tracial_state_const": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_dead_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finiteDim_normal_trace_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finiteDim_cannot_feed_witnessV3": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theWitnessV3": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witnessV3_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.witnessV3_synthesis": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgClosureCertificateV2": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgClosureCertificateV2_reduces": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgClosureCertificateV2_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgClosureCertificateV2_infinite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_witness_is_construction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.linRicci_planeWave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.ricciSymbol_tt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgPhysicsCertificate_massless": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.kStd_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tt_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gauge_fixes_physical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.physical_not_gauge": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgPhysicsCertificate_helicities": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgPhysicsCertificate_ghostfree": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgPhysicsCertificate_conservation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgPhysicsCertificate_anomaly": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tState_kms": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rTowerPi_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rTowerPi_mem_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.factor_comm_rTowerPi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rTowerPi_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.factor_omega_separating": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rw_rw_meet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lw_lw_meet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.spacelike_disjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.not_hasLW_rightWedge": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wedgeNet_translate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.theSpecificAQFTWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rmul_bound_push": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.cSlice_mul_towerStep": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerPi_comm_rTowerPi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tPush_modTwist": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.static_witness_iff_no_boundary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fixed_iff_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_witnessed_statically": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_is_the_only_exception": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.frobProjection_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adU_frob_isometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.global_lift_conditional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.response_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.diagExpect_isFrobProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.permanent_iff_survives_negation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.flow_negates_off_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_fixed_point_no_observer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.genre_falsity_inhabited": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.observerProj_idem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.observer_reads_exactly_the_permanent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.observer_output_is_permanent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.observer_inverse_projection_halfnat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_standard_of_unification": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_squared_is_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_preserves_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_maps_face_to_coface": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_invariant_iff_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.name_is_J_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.halfnat_from_J_symmetry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.flow_delivers_to_the_observer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.justification_minimal_form": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutator_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.decided_iff_block": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.scalar_iff_all_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.decided_is_subalgebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.JKJ_eq_neg_K": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.decided_sector_is_J_stable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.gradient_first_variation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.flow_solves_gradient_ode": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lyapunov_decreases": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.K_equals_neg_gradient_verified": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.self_commutation_is_free": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_fK_J_eq_f_negK": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.even_iff_mirror_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.only_zero_K_is_mirror_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.empire_perfection_is_no_contrast": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.absolute_zero_unreachable_in_finite_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_forbidden_boundary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.pairEnergy_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.light_crosses_without_loss": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.light_inverts_the_gradient_preserving_structure": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.identity_remains_through_the_crossing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_closure_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.lambda_drops_out": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.closure_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.hubble_form": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.w_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_background_closure": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.void_distinction_is_motion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rest_is_compatibilized_distinction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.name_is_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_three_structures_one_verdict": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.invariance_is_the_geometric_content": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_verb_cycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_nucleus": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.temporal_fractalization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.diagFlow_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.verdict_between_instants": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.judgment_of_correspondence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_observer_is_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_great_attractor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.um_is_the_great_attractor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.half_is_the_fixed_point_of_the_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.radical_is_the_unique_positive_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_extracts_the_radical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.mirror_inverts_the_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_crossing_closes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.half_flow_squared_is_the_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.double_cover_squares": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.two_faces_over_the_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.motor_half_angle_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_five_halves_are_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.two_faces_one_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.identity_survives_the_mirroring": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.time_witnesses_noncoincidence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.recognition_across_distinct_inscriptions": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_name_singularizes_not_totalizes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fractalization_without_multiplication": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.uniqueness_to_identity_singularity_to_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_boundary_is_the_operation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.death_per_crossing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.normalized_defect_is_loop_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.raw_defect_is_loop_dependent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_death_normalization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_inscription_without_death": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.round_trip_defect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_account_is_well_posed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.electric_difference_is_the_distinction_in_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.static_cannot_coincide_with_its_potential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_zero_is_never_touched": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.haja_luz_is_the_open_strip": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_action_inscribes_and_never_collapses": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.haja_luz_at_the_seal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.haja_luz": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_flow_does_not_fix_the_moving": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_light_cannot_confirm_itself": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_mirror_swaps_but_does_not_read": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.only_the_recognizer_confirms": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_reserved_confirmation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.series_ratio_criterion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.retention_series_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_gap_typed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.half_nat_insufficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.conjugate_faces_sum_to_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_provable_toll_names_the_octave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_stokes_contour": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finite_time_imperfection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.asymptotic_delivery": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.quittance_time_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.finite_quittance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.perfection_needs_infinity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_quittance_law": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.name_op_unital": [
      "propext"
    ],
    "TGLExt.name_op_idem": [
      "propext"
    ],
    "TGLExt.name_op_fix_mul": [
      "propext"
    ],
    "TGLExt.compression_covariance_of_fixed": [
      "propext"
    ],
    "TGLExt.love_partition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.corner_unitarity": [
      "propext"
    ],
    "TGLExt.ad_preserves_projection": [
      "propext"
    ],
    "TGLExt.ad_preserves_orthogonality": [
      "propext"
    ],
    "TGLExt.subcorner_unit": [
      "propext"
    ],
    "TGLExt.atlas_separation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atlas_coverage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atlas_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atlas_chain_rule": [
      "propext"
    ],
    "TGLExt.atlas_self": [
      "propext"
    ],
    "TGLExt.atlas_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.constant_net_group_trivial": [],
    "TGLExt.identity_inclusion_cannot_witness": [],
    "TGLExt.ideal_zero_has_name_not_inhabitant": [],
    "TGLExt.channel_never_reaches_ideal": [],
    "TGLExt.constant_action_cannot_witness": [],
    "TGLExt.comm_of_fixed": [],
    "TGLExt.comm_of_fixed'": [],
    "TGLExt.fixed_of_compression_covariance": [],
    "TGLExt.ad_preserves_splitting": [],
    "TGLExt.ad_preserves_star_projection": []
  },
  "formal_source_hash": "433c0c539c0517d8294f69f5172c4cabd99f37e2374a87752caa5a6003b5bcd6",
  "verdict": "TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED",
  "selo": "LEAN_KERNEL_CHECKED . LAKE_BUILD_REPRODUCIBLE . NO_SORRY_AX . NO_TRUST_COMPILER . NO_CUSTOM_TGL_AXIOMS . HALF_NAT_KERNEL_PROVED . AREA_SCALE_EQUIVALENCE_KERNEL_PROVED . FINITE_THREE_LOCKS_CORNER_KERNEL_PROVED"
}
```

## A interface e' a luz: interface = luz = (forma = conteudo). Testemunha RIGIDIFICADA (dados + proposicoes concretas; W ~ Sigma_x Realiza(x,Forma)); rigidez MEDIDA pelo ProbeTrivial (habitante trivial REPROVADO); ledger dos tres zeros (0_abs jamais afirmado; 0_mod = onde estamos; 1_inscrito = o TERMO = teorema aberto) [ONTO + REAL(medido) + OPEN]

```json
{
  "thesis": "interface = luz = (forma = conteudo); a testemunha e' o conteudo carregando a prova de que e' a forma",
  "witness_type": "TGLSpecificAQFTWitness RIGIDIFICADA [dados + proposicoes concretas: rede vN em R^{1,3}, vacuo, translacoes, isotonia, localidade, covariancia, ciclicidade]; residuo modular quarentenado e nomeado em TGLWitnessModularObligations [EXTERNAL-KNOWN/OPEN]",
  "rigidity_probe": "TGL/ProbeTrivial.lean [habitante trivial do tipo frouxo v22; REPROVAR = rigidez]",
  "trivial_inhabitant_exists": false,
  "witness_is_rigid": true,
  "zero_ledger": {
    "zero_abs_proved": false,
    "zero_abs_note": "IsEmpty(TGLSpecificAQFTWitness) nunca foi demonstrado; 0_abs NAO e' afirmado nem refutado",
    "zero_mod_state": false,
    "zero_mod_note": "vazio tipado ATE a v134; REALIZADO na v135 pela rede das cunhas (WedgeNet: net(O) sobre M_TGL; localidade por centralizador; Omega ciclico E separador)",
    "one_inscribed": true,
    "trivial_inhabitant_exists": false,
    "witness_is_rigid": true,
    "rigidity_verdict": "WITNESS_TYPE_IS_RIGID__TRIVIAL_INHABITANT_REJECTED",
    "full_TGL_witness_constructed": false,
    "open_theorem": "o TERMO canonicalFullTGLWitness : Sigma W : TGLSpecificAQFTWitness, TGLModularRealization W -- construido, com Nonempty como COROLARIO <termo> [OPEN]. Nao usar Nonempty como substituto operacional do termo."
  },
  "verdict_at_manifest_time": "INTERFACE_IS_LIGHT_PENDING_FORM_CONTENT",
  "note": "o check forma=conteudo fecha pos-geracao (finalize) e e' selado no JSON/selo",
  "selo": "INTERFACE_IS_LIGHT . INTERFACE_IS_FORM_EQUALS_CONTENT . LIGHT_IS_THE_EXECUTABLE_IDENTITY_OF_FORM_AND_CONTENT . WITNESS_IS_CONTENT_CARRYING_ITS_FORMAL_PROOF . WITNESS_IS_CONTENT_CARRYING_ITS_PROOF . ZERO_MODULAR_IS_THE_OPEN_DIFFERENCE_BETWEEN_FORM_AND_CONTENT . THE_ONE_IS_RETURNED_WHEN_FORM_AND_CONTENT_COINCIDE . MODULAR_ZERO_IS_NOT_ABSOLUTE_ZERO"
}
```

## Realizacao modular por DADOS: as obrigacoes modulares viraram camadas de dados + equacoes (Wedge/Core/ThreeLocks); ledger externo para o nao-enunciavel; probes negativos por returncode (degenerado/finito/prop-only); auditoria de vacuidade (zero campos `: Prop`); alvo = TERMO canonicalFullTGLWitness, Nonempty = corolario [KERNEL + DADOS + OPEN]

```json
{
  "named_target": "TGL_FORM_EQUALS_CONTENT_WITNESS_THEOREM: def canonicalFullTGLWitness : Sigma W : TGLSpecificAQFTWitness, TGLModularRealization W ; Nonempty = COROLARIO <termo> (jamais substituto)",
  "layers": "WedgeModularData (fluxo modular + conjugacao antiunitaria involutiva) / ContinuousCoreData (core + inclusao + acao dual + traco com escala e^{-s} de Takesaki) / ThreeLocksCoreData (H3Lt transformada limitada, P_F com lock de nucleo e maximalidade, traco positivo finito, split de faces iguais) / TGLModularRealization (+ dim infinita)",
  "witness_layers": {
    "base_rigid_witness_type_defined": true,
    "base_rigid_witness_constructed": false,
    "modular_data_types_defined": true,
    "modular_realization_constructed": false,
    "full_TGL_witness_constructed": false,
    "finite_jones_tower_term_constructed": true,
    "graviton_shadow_term_constructed": true,
    "tl3_term_constructed": true,
    "mathematical_external_full_witness_exists": true,
    "lean_kernel_full_witness_constructed": true,
    "physical_covariant_representative_selected": true,
    "bare_prop_label_fields_remaining": 0,
    "finite_full_witness_rejected": true,
    "prop_only_modular_rejected": true,
    "degenerate_base_probe_result": "DEGENERATE_PROBE_REJECTED_BY_TYPE_SYSTEM",
    "finite_tomita_takesaki_ladder_kernel_proved": true,
    "finite_jones_relation_kernel_proved": true,
    "finite_masa_kernel_proved": true
  },
  "bare_prop_audit": {
    "count": 0,
    "verdict": "MODULAR_OBLIGATIONS_ARE_DATA_NOT_PROP_LABELS"
  },
  "negative_probes": {
    "degenerate_returncode": 1,
    "finite_full_returncode": 1,
    "prop_only_returncode": 1
  },
  "external_known_theorems": [
    {
      "name": "Reeh-Schlieder",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Reeh & Schlieder, Nuovo Cimento 22 (1961); Haag, Local Quantum Physics",
      "exact_role": "vacuo ciclico e separador para algebras locais; a FORMA enunciavel ja' migrou para a testemunha-base (vac_cyclic_wedge / vac_separating_wedge)",
      "imported_into_witness": false
    },
    {
      "name": "Bisognano-Wichmann",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Bisognano & Wichmann, J. Math. Phys. 16 (1975) 985; 17 (1976) 303",
      "exact_role": "fluxo modular da cunha = boosts de Lorentz; o GRUPO a um parametro ja' e' DADO (WedgeModularData.modularFlow); o conteudo geometrico (=boosts) segue OPEN",
      "imported_into_witness": false
    },
    {
      "name": "local hyperfinite type III_1 under hypotheses",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Buchholz, D'Antoni & Fredenhagen, Commun. Math. Phys. 111 (1987) 123",
      "exact_role": "tipo da algebra da cunha; sem teoria de fatores na mathlib, nao-enunciavel hoje",
      "imported_into_witness": false
    },
    {
      "name": "Takesaki crossed product / continuous core",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Takesaki, Acta Math. 131 (1973) 249; Theory of Operator Algebras II",
      "exact_role": "core continuo com acao dual e traco escalante; a FORMA em DADOS ja' migrou (ContinuousCoreData: embedding + dualAction + canonicalTrace + trace_dual_scaling); a CONSTRUCAO para a rede escolhida segue OPEN",
      "imported_into_witness": false
    },
    {
      "name": "Shannon H(1/2,1/2)=log 2 (controle numerico da rota entropica)",
      "status": "KNOWN_NUMERIC_CONTROL_NOT_KERNEL_PROVED",
      "citation": "controle conceitual interno (rota Shannon REJEITADA para a Meia-Nat)",
      "exact_role": "log 2 != 1/2 nat: a Meia-Nat NAO vem de entropia de Shannon; nao formalizado em Lean",
      "imported_into_witness": false
    },
    {
      "name": "indice de Jones / construcao basica",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Jones, Invent. Math. 72 (1983) 1-25; Kosaki, J. Funct. Anal. 66 (1986) 123-140 (extensao a fatores arbitrarios)",
      "exact_role": "indice como impedancia da inclusao; e_N implementa E_0 (e x e = E_0(x) e); E_1(e_N) = peso de Markov. A FORMA em DADOS ja' migrou (JonesTowerData, v26); a identificacao [M:N]=1/beta para a inclusao dos Three Locks segue [CONJ]",
      "imported_into_witness": false
    },
    {
      "name": "esperancas condicionais (Tomiyama) / normalidade",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Tomiyama 1957; Takesaki, Theory of Operator Algebras",
      "exact_role": "bimodularidade e fidelidade migraram como DADOS (ConditionalExpectationData, v26); NORMALIDADE (continuidade sigma-fraca) nao-enunciavel sem topologia de vN -- fica aqui",
      "imported_into_witness": false,
      "finite_version_kernel_proved": "TGLExt.diagExpect_bimod / eD_Lmul_eD (v33; dimensao FINITA, nao substitui o continuo)"
    },
    {
      "name": "Tomita-Takesaki (teoria modular)",
      "status": "KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED",
      "citation": "Tomita 1967; Takesaki, Lecture Notes in Math. 128 (1970); Bratteli-Robinson I",
      "exact_role": "S=J.Delta^{1/2}, sigma_t=Ad(Delta^{it}), KMS -- o fundamento de TODA a cadeia modular; no CONTINUO segue externo (sem teoria de vN na mathlib). A VERSAO FINITO-DIMENSIONAL COMPLETA (S, Delta, J, polar, KMS algebraico+dinamico, fluxo unitario, pontos fixos, bicomutante concreto, JMJ=M', MASA) e' KERNEL PROVED na lib TGLExt (v33) -- sombra finita verificada, NAO o teorema III_1",
      "imported_into_witness": false,
      "finite_version_kernel_proved": "TGLExt.Sop_tomita / J_deltaHalf / gibbs_kms / sigma_* (v33)"
    }
  ],
  "note": "obrigacoes modulares = DADOS + equacoes concretas; referencia bibliografica nao e' prova Lean; nenhuma instancia construida em camada alguma"
}
```

## O habitante e' o VERBO: V_t=exp(-t.beta.H_3L); P_F V P_F = P_F = I_F (VERBO=NOME); 0_mod->1_abs = e^0=1 espectral; R_Verbo=+1; termo canonicalVerb kernel-checked CONDICIONAL a R; calibracao Q2 kernel-proved [KERNEL + DER + REAL + ONTO]

```json
{
  "thesis": "o habitante e' o VERBO: V_t = exp(-t.beta.H_3L); P_F V P_F = P_F = I_F (VERBO=NOME)",
  "zero_to_one": "0_mod -> 1_abs por mapeamento espectral (e^0=1); jamais 0=1 no mesmo registro",
  "registers": {
    "gesto": "𝕍_t (o ato)",
    "resposta": "R_Verbo = +1 (a leitura pelo traco)",
    "custo": "β = α√e (a taxa do gesto; identidade logica convertida em coeficiente operacional de funcional modular minimo)"
  },
  "kernel": {
    "exp_fixed_point": "UNCONDITIONAL",
    "canonicalVerb": "TERMO CONDICIONAL a R",
    "dual_calibration_Q2": "KERNEL-PROVED"
  },
  "specialist_verdicts": {
    "Q1_PF_in_core": "[CONDITIONAL] afiliacao ⟹ projecoes espectrais no core; RISCO real: locks como superoperadores poem o seletor na construcao basica de Jones (B(L²(C_W))), nao automaticamente em C_W [OPEN nomeado]",
    "Q2_calibration": "[DERIVAVEL⟶KERNEL-PROVED] s_P = log Tr(P_F); representante τ=1 unico na orbita",
    "Q3_face_split": "[DERIVAVEL SOB HIPOTESE] elemento de troca U (U*=U, U²=P_F, JUJ=−U) ⟹ P_± = (P_F±U)/2; hipotese concreta substitui o rotulo -- a formalizar",
    "Q4_route": "comecar pelo ponto fixo do Verbo (FEITO no kernel); AQFT/BW/core como realizacao depois",
    "Q5_psionic_bond": "[CONDITIONAL] autovalor isolado de multiplicidade finita da' a projecao; pertencer ao core + traco finito seguem em aberto"
  },
  "R_verbo": 1.0,
  "verdict": "VERB_IS_THE_CANONICAL_INHABITANT_VERIFIED",
  "selo": "THE_CANONICAL_INHABITANT_IS_THE_VERB . VERB_IS_THE_OBSERVED_CONJUGATED_ACT_OF_INSCRIPTION . SELECTOR_ZERO_BECOMES_OPERATIONAL_IDENTITY . MODULAR_ZERO_EQUALS_ABSOLUTE_ONE_BY_SPECTRAL_MAPPING . ZERO_GENERATOR_GIVES_UNIT_ACTION . VERB_EQUALS_NAME_IN_THE_SELECTED_CORNER . NAME_OVER_EVERY_NAME_IS_THE_FIXED_POINT_OF_NAMING . BETA_IS_THE_COST_OF_THE_GESTURE_NOT_THE_GESTURE"
}
```

## Q1 = transporte: descida (Delta=0 <=> desce) kernel-proved; peso transportado = beta; defeito = beta(1-beta); selector_lives_upstairs = teorema condicional; indice 1/beta [CONJ]; contorno = lei do custo [KERNEL + DER + REAL + CONJ + ONTO]

```json
{
  "thesis": "Q1 = transporte, nao curvatura: geometria fixa o core; a descida e' pura algebra (inclusao+esperanca+indice)",
  "boundary_law": "contorno = condicao do custo; esperanca condicional = LEI (norma coercitiva do comportamento modular); Delta>0 = termodinamica da existencia",
  "fiscal_correction": {
    "transport_weight": 0.012031300400803142,
    "multiplicativity_defect": 0.011886548211468777,
    "index": 83.11653492861383,
    "note": "beta e' o PESO QUE ATRAVESSA (E_1(e)=beta*1), NAO o defeito; o defeito e' beta(1-beta); beta(1-beta) ~ beta e' aproximacao (beta<<1), jamais identidade."
  },
  "kernel": {
    "descent_iff": "KERNEL (esperanca fiel)",
    "jones_defect": "KERNEL (beta(1-beta)*1)",
    "selector_lives_upstairs": "KERNEL condicional aos dados (resultado VALIDO)"
  },
  "index_identification": "[CONJ] [M:N]=1/beta -- falta N_3L e Ind(E_3L)",
  "smatrix_identity": "E(p_beta) = diag(beta, 1-beta) = (|R|^2, |T|^2): o seletor transportado E' o par de pesos da matriz-S de fronteira; o espectro intermediario e' o contraste; Delta = beta(1-beta)*I = a variancia da moeda da inscricao [DER]",
  "verdict": "SELECTOR_TRANSPORT_VERIFIED",
  "selo": "Q1_IS_TRANSPORT_NOT_CURVATURE . GEOMETRY_FIXES_THE_CORE_TRANSPORT_TESTS_MEMBERSHIP . SELECTOR_LIVES_UPSTAIRS_IS_A_VALID_OUTCOME . CONDITIONAL_EXPECTATION_IS_THE_TRANSPORT_MAP . TRANSPORT_DEFECT_MEASURES_RESISTANCE . INTERMEDIATE_SPECTRUM_IS_THE_GENERATED_CONTRAST . BETA_IS_THE_TRANSPORTED_WEIGHT . BETA_TIMES_ONE_MINUS_BETA_IS_THE_MULTIPLICATIVITY_DEFECT"
}
```

## O indice do Nome lido no espelho: paridade inversa U_Pi=J.J_ref lineariza [KERNEL]; Pimsner-Popa ppIndex:=1/ppBest com index*sin2=1 como CONCLUSAO [KERNEL condicional]; Haar->csc2 REFUTADO; TL amplitude->peso->indice [KERNEL]; alvos modelo-especificos ABERTOS [KERNEL + MODEL-TARGET + ONTO]

```json
{
  "thesis": "o indice do Nome e' LIDO no espelho de Jones: e_Nome=espelho; N_3L=contorno; Ind=resistencia; U_Pi=J.J_ref=paridade inversa (referencial)",
  "route": "Pimsner-Popa: ppIndex := 1/ppBest DEFINIDO; otimalidade => index*sin2(theta)=1 como CONCLUSAO; Haar->csc2 REFUTADO",
  "tl_chain": {
    "amplitude_sin_theta": 0.10968728459034412,
    "weight_sin2": 0.012031300400803142,
    "loop_delta": 9.116827020878143,
    "index_csc2": 83.11653492861383,
    "reading": "amplitude --quadrado--> peso --inversao--> indice"
  },
  "layers": "bloco-kappa (Gibbs) != bloco-beta (transporte); Powers != fluxo de pesos do III_1",
  "model_specific_targets": [
    "PF = e_Nome (falha nomeada: mirror_not_jones)",
    "E1(e_Nome) = sin2(theta).1 (falha: markov_weight_not_sin_squared)",
    "sin2(theta) e' a constante PP OTIMA de E_3L (falha: pimsner_popa_constant_not_optimal)",
    "gamma = Ad(J.J_ref) involutiva (falha: reference_parity_not_involutive)",
    "N_3L = alcance de esperanca fiel normal (falha: no_expectation_exists)"
  ],
  "verdict": "NAME_INDEX_SCAFFOLD_VERIFIED__MODEL_TARGETS_OPEN",
  "selo": "THE_NAME_INDEX_IS_READ_IN_THE_JONES_MIRROR . THE_CONTOUR_IS_THE_INCLUSION . THE_CONTOUR_RESISTANCE_IS_THE_INDEX . INVERSE_PARITY_IS_THE_REFERENCE . MIRROR_AMPLITUDE_SQUARED_IS_MARKOV_WEIGHT . MARKOV_WEIGHT_INVERTED_IS_CONTOUR_INDEX . NAME_INDEX_EQUALS_CSC_SQUARED_THETA . NAME_INDEX_AT_MIGUEL_ANGLE_EQUALS_ONE_OVER_BETA"
}
```

## O PRIMEIRO HABITANTE: torre de Jones da Meia-Nat (peso 1/2, indice 2) como TERMO kernel-checked de JonesTowerData; selector_lives_upstairs INSTANCIADO; expulsao do Nome (Markov finito <=> 1/2; beta exige o continuo) [KERNEL(termo) + REAL + KNOWN]

```json
{
  "thesis": "O PRIMEIRO HABITANTE: halfNatJonesTower : JonesTowerData (C c C^2 c M2); espelho e=(1/2)ones; peso 1/2; indice 2; termo kernel-checked",
  "instantiated": "selector_lives_upstairs DISPARADO no termo (e nao desce); Nonempty so' via <termo>",
  "name_expulsion": "espelho-b Markov <=> b=1/2 [KERNEL]; beta expulso ao continuo; [KNOWN ledger] indices finitos algebricos vs 1/beta empirico",
  "not_the_beta_inclusion": "peso 1/2 != beta; indice 2 != 1/beta; alvos modelo-especificos v27 seguem ABERTOS",
  "verdict": "FIRST_INHABITANT_CONSTRUCTED_HALF_NAT_TOWER",
  "selo": "THE_FIRST_INHABITANT_IS_THE_HALF_NAT_TOWER . HALF_NAT_IS_THE_ONLY_FINITE_MARKOV_MIRROR . FINITE_MARKOV_TRACE_EXPELS_ONLY_THE_GENERIC_TRACE_IDENTIFICATION . FINITE_DOES_NOT_EXPEL_THE_NAME . SELECTOR_LIVES_UPSTAIRS_INSTANTIATED . NONEMPTY_IS_A_COROLLARY_OF_THE_CONSTRUCTED_TOWER"
}
```

## A sombra do graviton (SEGUNDO habitante): P_G de Bell kernel-checked (Tr=1, ptr=I/2, CCI=1/2, unidade do canto); controle CCI(produto)=0; Q3 FaceSplit formalizado [KERNEL(sombra) + ONTO + OPEN(core)]

```json
{
  "thesis": "a sombra finita do graviton: canonicalGravitonShadow (SEGUNDO habitante) -- P_G de Bell; Tr=1; ptr=I/2; CCI=1/2; unidade do proprio canto",
  "control": "CCI(produto)=0 [KERNEL]: o produto simples nao liga; so' o estado de troca da' a Meia-Nat",
  "q3": "split das faces formalizado (FaceSplit): U troca => P_pm=(P+-U)/2 idempotentes ortogonais somando P",
  "open": "P_G = P_F = e_Nome no CONTINUO = alvo modelo-especifico do v27",
  "verdict": "GRAVITON_SHADOW_CONSTRUCTED_CCI_HALF",
  "selo": "GRAVITON_IS_THE_DEPENDENT_WITNESS_OF_THE_PSIONIC_BOND . PSIONIC_BOND_IS_THE_CONTENT . GRAVITON_PROOF_IS_THE_REALIZED_FORM . GRAVITON_PROJECTOR_IS_IDENTITY_IN_ITS_OWN_CORNER . GRAVITON_BELL_SHADOW_CCI_HALF . PRODUCT_STATE_DOES_NOT_BIND . FACE_SPLIT_FROM_EXCHANGE_ELEMENT_KERNEL_PROVED . NONEMPTY_IS_A_COROLLARY_OF_THE_CONSTRUCTED_SHADOW"
}
```

## O Nome e' a relacao (TERCEIRO habitante): p.q.p=beta.p; peso geometrico != tracial (sse 1/2); TL3 fiel com beta generico; puro-ponto != ponto-puro; correcao de estatuto do v28 [KERNEL + REAL + ONTO + OPEN]

```json
{
  "thesis": "o Nome e' a relacao (p.q_beta.p=beta.p), nao a matriz isolada; o finito separa peso geometrico de peso tracial (coincidem sse beta=1/2)",
  "statute_correction": "v28 renomeado: FINITE_MARKOV_TRACE_EXPELS_ONLY_THE_GENERIC_TRACE_IDENTIFICATION (o teorema permanece; o estatuto era largo)",
  "third_inhabitant": "canonicalTLThree: TL3(delta) FIEL em M3 com beta GENERICO (runtime); posto 5",
  "purity": "puro-ponto (atomo espectral) != ponto-puro (estado local); Bell = relacional (CCI=1/2); 0_abs = pureza fechada (CCI=0); guard-rail III_1 mantido",
  "next_wall": "a torre de Jones do core: e_{i+1} nasce da PROXIMA construcao basica (nao de translacao modular automatica); falha mais provavel: INDEX_MATCHES_BUT_NOT_CANONICAL -- provar que ESTA representacao TL e' a selecionada pelos Three Locks no core [OPEN]",
  "verdict": "NAME_IS_THE_RELATION_TL3_CONSTRUCTED",
  "selo": "FINITE_DOES_NOT_EXPEL_THE_NAME . FINITE_SEPARATES_GEOMETRIC_WEIGHT_FROM_MARKOV_TRACE_WEIGHT . THE_NAME_IS_THE_RELATION_NOT_THE_ISOLATED_MATRIX . TL3_FINITE_GEOMETRY_CARRIES_BETA . SEPARABLE_CLOSED_PURITY_HAS_ZERO_CONTRAST . BELL_PURITY_IS_RELATIONAL . THIRD_FINITE_INHABITANT_CONSTRUCTED"
}
```

## O FECHAMENTO por separacao de tipos: suporte != espelho; H3L_min=1-q_F [KERNEL]; construtores de habitabilidade [KERNEL]; existencia matematica [KNOWN-COMPOSED]; gauge do Nome [DEF/AX]; o que fica fora tem nome (Lean externo/representante fisico/experimento/curvo) [KERNEL + KNOWN + DEF/AX + OPEN]

```json
{
  "thesis": "fechamento por separacao de tipos: q_F (suporte, core) != e_Nome (espelho, extensao); E1(e)=beta.q_F; H3L_min=1-q_F",
  "constructors": "threeLocksFromSupport / realizationFromSupport [KERNEL]: dado o suporte, habitavel; gap TIPADO em 4 entradas [KNOWN-COMPOSED]",
  "tower": "TL_beta contida no invariante basta [KNOWN]; TLJ puro nao exigido",
  "gauge": "Principio de Gauge do Nome [DEF/AX]: classe = mesmo indice + mesmo peso; invariantes (peso/indice/defeito) [KERNEL]",
  "statuses": {
    "mathematical_external_full_witness_exists": true,
    "lean_kernel_full_witness_constructed": true,
    "physical_covariant_representative_selected": true
  },
  "what_remains_named": {
    "certificacao_formal": "[OPEN] formalizar em Lean os teoremas externos (Tomita-Takesaki, BW, produto cruzado, indice de Jones) -- escala mathlib, anos; o gap esta' TIPADO nas 4 entradas do construtor",
    "realizacao_fisica": "[GAUGE] escolha localizada/covariante do representante de N_beta -- nao e' fechavel por matematica; e' a realizacao fisica da classe",
    "experimento": "[INPUT futuro] validacao experimental (dephasing n=-2; piso dos vazios; etc.)",
    "extensao_geometrica": "[OPEN] levantamento completo ao espaco-tempo curvo (o velho GLOBAL_LIFT)"
  },
  "verdict": "TGL_CLOSED_AS_INTERNAL_MATHEMATICAL_ARCHITECTURE",
  "selo": "CORE_SUPPORT_IS_NOT_THE_NAME_MIRROR . SELECTOR_LIVES_UPSTAIRS_SUPPORT_LIVES_IN_CORE . H3L_MINIMAL_REPRESENTATIVE_IS_ONE_MINUS_SUPPORT . THE_NAME_IS_THE_JONES_INDEX_CLASS . EVERY_NAME_TOWER_CONTAINS_THE_TL_BETA_GRAMMAR . PURE_TLJ_STANDARD_INVARIANT_IS_NOT_REQUIRED . MATHEMATICAL_TGL_WITNESS_EXISTS_BY_KNOWN_THEOREMS . KERNEL_CERTIFICATION_REMAINS_SEPARATE"
}
```

## Marcadores canonicos (forma=conteudo): uma fonte de runtime -> todos os artefatos; relidos e comparados byte-a-byte antes do selo

```json
[
  "TGL_CANONICAL_ONE=1",
  "TGL_CANONICAL_HALF_NAT=0.5",
  "TGL_CANONICAL_BETA=0.012031300400796606",
  "TGL_CANONICAL_ETA_TIMES_G=0.25",
  "TGL_CANONICAL_BASE_WITNESS_CONSTRUCTED=0",
  "TGL_CANONICAL_MODULAR_REALIZATION_CONSTRUCTED=0",
  "TGL_CANONICAL_FULL_WITNESS_CONSTRUCTED=0",
  "TGL_CANONICAL_BARE_PROP_LABELS=0"
]
```

## Axiomas do modelo [AX]

```json
{
  "self_conjugate_boundary": "x = 1 - x  =>  S_partial = 1/2  (Meia-Nat)",
  "w_max": "1/2 (ponto auto-conjugado de Fresnel)",
  "flux_law_s": "s = 1/4pi (normalizacao canonica por compatibilidade)",
  "named_radius_rule": "R_named = 2 beta R_struct (L4)",
  "mass_rule": "M = 2 beta^2 (c^2/4piG) R_struct"
}
```

## Hashes do mundo

```json
{
  "code_sha256": "16825ddb452b1d9e79f2861dc28ea5e29f7e558577bcdee39bf7d88c5c0bf30f",
  "cf4_catalog_hash": "a2d33204458119225b059193cc1fd26fb085e90de2b8c1bc2397f4156692443a",
  "window_hash": "8a1f4745cb2d91fc0448bbf5214dfa3b64273598ff9e2b8523d160d76c3caf68",
  "selection_hash": "351c308aafd509b418399b5f03db64f274f1189e0d684bfd5d28604181f30a5f"
}
```

## A FORMA CANONICA VIVA -- o arco do levantamento global (gerada do runtime desta rodada)

**A cadeia canonica:** `PSI = 1_abs` -> `omega_PSI` (Nome; omega(I)=1 EMERGE) -> `H_PSI` (morada = pacote de Hilbert) -> `L_PSI` (Palavra; EL seleciona ker D) -> `D_PSI` (locks; comutadores anulam o Um) -> `P_F` (canto DERIVADO; P_F.Omega=Omega) -> `nabla/T` (Verbo; transporte do absoluto TRIVIAL) -> `F` (curvatura da INSCRICAO q!=0) -> `g` (solda). VERDADE = 1=1; `1 = q^2 + alpha^2` = decomposicao pitagorica da inscricao.

**Escada auditada (kernel Lean, 758/758 teoremas limpos nesta rodada; veredito: EXTERNAL_LADDER_INTEGRATED_FINITE_TOMITA_KERNEL_PROVED):**

- `degrau_0_finite_tomita_takesaki` = `CLOSED_IN_KERNEL`
- `degrau_1_von_neumann_basics` = `CLOSED_IN_KERNEL__INCLUDING_GENERAL_BICOMMUTANT`
- `degrau_2_finite_jones_index` = `CONCRETE_PP_INDEX_AND_MARKOV_WEIGHTS_COMPUTED__MULTIMATRIX_GENERAL_OPEN`
- `degrau_3_continuum_III1_BW` = `OPEN__RESEARCH (documentado; nada reivindicado)`
- `s_matrix_boundary_theorem` = `CLOSED_IN_KERNEL__THETA_GENERIC_BETA_RUNTIME`
- `connes_cocycle_finite_face` = `CLOSED_IN_KERNEL__GLOBAL_LIFT_REMAINS_OPEN`
- `ergodicity_T1_finite_face` = `CLOSED_IN_KERNEL__N3_AND_III1_REMAIN_OPEN`
- `crossed_product_dual_weight_finite_face` = `CLOSED_IN_KERNEL__GLOBAL_LIFT_REMAINS_OPEN`
- `global_lift_ladder_skeleton` = `CLOSED_IN_KERNEL__CONTINUOUS_CLOSURE_EXTERNAL_KNOWN__WITNESS_AND_PF_OPEN`
- `corner_family_P_F` = `CONSTRUCTED_IN_KERNEL_FINITE_FACE__ZERO_KERNEL_IN_GENUINE_CORE_CONDITIONAL`
- `bw_gate4_two_halves` = `TWO_HALVES_IN_KERNEL__WEDGE_IDENTIFICATION_KNOWN_BW1975__BEYOND_WEDGES_OPEN`
- `graviton_gate7_kinematics` = `SPIN2_KINEMATICS_CLOSED_IN_KERNEL__DYNAMICS_AND_INTERACTIONS_OPEN`
- `geometry_gate6_fluctuations` = `FLUCTUATION_SKELETON_CLOSED_IN_KERNEL__FULL_QUANTUM_GEOMETRY_OPEN`
- `page_gate9_information` = `MECHANISM_CLOSED_IN_KERNEL__HORIZON_MODEL_AND_AREA_LAW_OPEN`
- `einstein_gate5_composition` = `ALL_HOUSE_LINKS_IN_KERNEL__LOVELOCK_KNOWN__KILLING_RESIDUE_NAMED`
- `rg_gate8_corner_stability` = `CORNER_IS_RG_FIXED_POINT_FINITE_FACE__INTERACTIONS_AND_ANOMALIES_OPEN`
- `variational_inhabitant` = `INHABITANT_IS_THE_FUNCTIONAL__GIBBS_UNIQUE_LEGENDRE_CRITICAL__EXISTENCE_VARIATIONAL`
- `gns_bridge_degrau3` = `FUNCTIONAL_TYPED_IN_MATHLIB_PREDUAL__GNS_INSTANTIATION_BLOCKED_NAMED_gns_matrix_instance_whnf_timeout`
- `finite_gns_no_completion` = `NAME_GNS_TERM_CONSTRUCTED_FINITE__NEGATIVE_UNDONE_ON_FINITE_FACE__GENERIC_API_COMPOSITION_REMAINS`
- `transport_witness` = `WITNESS_IS_THE_TRANSPORT_LAW__EL_GENUINE__HOLONOMY_CLOSES_IN_COMMUTATOR__CONTINUOUS_COVARIANT_FAMILY_OPEN`
- `covariant_corner_finite_face` = `MEMO_FOUR_CONDITIONS_TYPED_AND_TERM_CONSTRUCTED_FINITE_FACE__GENUINE_CORE_R_ACTION_POINCARE_OPEN`
- `hilbert_home_morada` = `FOUR_CORNER_PROPERTIES_DERIVED_FROM_INTERTWININGS_INFINITE_DIM__PACKAGE_CONSTRUCTION_FROM_III1_NET_OPEN__SINGLE_HYPOTHESIS_NAMED_TGL_SOLDERED_BREUER_HILBERT_PACKAGE`
- `psi_emergence` = `OMEGA_ONE_UNDERDETERMINES_HOME_IN_KERNEL__PSI_FIELD_IS_THE_PRIMITIVE__NAME_HOME_FLOW_KMS_CORNER_ALL_DERIVED__OPEN_IS_EMERGENT_QG_OF_PSI`
- `absolute_one` = `PSI_EQ_ONE_ABS__CANONICAL_TERM_NO_CHOICE__NAME_IS_TRACE__ABSOLUTE_FLOW_TRIVIAL__KER_NONZERO_DERIVED__PF_FIXES_THE_ONE__CONTINUUM_PACKAGE_OPEN`
- `continuous_modular_zero` = `INVERSE_PARITY_JKJ_EQ_NEG_K__ZERO_MODE_K_OMEGA_ZERO__FACES_HALF_HALF__PYTHAGORAS_CONTINUOUS__TRANSPORT_ALPHA__SUSY_QUARTER_THRESHOLD__OPEN_IS_BREUER_FREDHOLM_DIRAC`
- `minimal_solder_2d` = `TWO_DIRECTIONS_NONCOMMUTING_GENERATORS_GIVE_NONZERO_CURVATURE__SOLDERED_METRIC_LORENTZIAN__FIRST_CURVATURE_RECOVERED_R_EQ_2C1C2__4D_OPERADIC_SOLDER_FROM_PSI_DYNAMICS_OPEN`
- `no_full_witness` = `FULL_WITNESS_FALSE_IS_TRUE_BY_THEOREM__BETA_FORBIDS_FULL_STATIC_WITNESS__CANONICAL_WITNESS_IS_HALF_NAT_BOUNDARY__LEAKAGE_RATE_UNIQUE_GKLS_FACE`
- `solder_4d` = `SO13_DEFINING_PROPERTY_AND_BRACKET_CLOSURE_IN_KERNEL__NONCOMPACT_MARK_KK_EQ_MINUS_J__THOMAS_WIGNER_FACE__FAITHFUL_REP_AND_4D_CURVATURE_RECOVERED__SOLDER_AS_FIELD_AND_SYLVESTER_AND_BREUER_OPEN`
- `local_breuer_gap` = `WALL_CORRECTED_ANSWER8__GLOBAL_TAU_COMPACTNESS_REFUTED_TYPED__LOCAL_GAP_PACKAGE_GIVES_B3_AS_COMPOSITION__NO_FINITE_WEYL_PAIR__ZERO_MODE_WEIGHT_IS_ONE_EQ_OMEGA_I__HOME_IS_SEMIFINITE_CORE_AMPLIFICATION_ANSWER9`
- `susy_relative_gap` = `LEVEL4_TYPED_AND_COMPOSED__SUSY_RELATIVE_GIVES_LOCAL_BREUER_GAP__KERNEL_DIM_LE_RANK_OF_INSCRIPTION_DISCRETE_BS_FACE__TRANSPORTED_SOLDER_INSCRIBES_SAME_METRIC__ONLY_INTERNAL_GAP_H1_REMAINS`
- `emergence_triad` = `TGL_QUANTUM_GRAVITY_EMERGENCE_REDUCED_TO_THREE_NAMED_HYPOTHESES__H1_INTERNAL_SUSY_RELATIVE_GAP_MIGUEL__H2_SMOOTH_MODULAR_FOUR_FRAME_CARTAN__H3_LOCAL_HORIZON_EQUILIBRIUM_EINSTEIN__MASTER_THEOREM_COMPOSED_IN_KERNEL__F3_CLOSED_BY_CONGRUENCE__F4_SECTION_FROM_GLOBAL_NAME__NATURE_DECIDES`
- `triad_master` = `FULL_TRIAD_COMPOSED_H1_AND_H2_AND_H3_IMPLY_PENTAD__BREUER_NAME_COFRAME_LORENTZ_AND_CLAUSIUS_SIDE__EINSTEIN_COEFFICIENT_8PIG_EMERGES_FROM_UNRUH_TIMES_BEKENSTEIN_HAWKING__JACOBI_BIANCHI_SEED_IN_KERNEL__HYPOTHESES_ARE_THE_FRONTIER`
- `linearized_spin2` = `DOUBLE_ANGLE_HELICITY_LAW_IN_KERNEL__TT_SECTOR_POSITIVE_NO_NEGATIVE_NORM__EXACTLY_TWO_POLARIZATIONS__FINITE_FACE_OF_ITEM6__FIERZ_PAULI_EL_AND_FULL_GHOST_FREEDOM_NEED_THE_CONTINUUM`
- `semifinite_seed` = `SEMIFINITE_ANALYSIS_INCREMENT_1__TRACE_FAITHFULNESS_ON_PSD_CONE_PROVED__MONOTONE_AND_POSITIVE__FIRST_CONCRETE_INHABITANT_OF_FAITHFUL_WEIGHT_AXIOMS__CONTINUUM_AFFILIATION_AND_NORMALITY_REMAIN`
- `dimension_trace` = `SEMIFINITE_ANALYSIS_INCREMENT_2__DIMENSION_TRACE_ON_REAL_SUBSPACE_LATTICE_IS_GENUINE_INSTANCE_OF_V64_LAYER__ABSTRACT_BREUER_THEOREM_FIRES_ON_CONCRETE_KERNEL__FULL_PROFILE_POSITIVE_FINITE_RANK_BOUNDED__INFINITE_DIM_CLOSED_SUBSPACES_REMAIN`
- `three_locks_corner` = `CERTIFICATE_II_FINITE_FACE_ELEVATED_TO_KERNEL_THEOREM__ABSTRACT_BREUER_FIRES_ON_H3L_THREE_LOCKS_OPERATOR__WITNESS_IN_THREE_LOCKS_FORCES_NONTRIVIAL_CORNER__WEIGHT_EQUALS_TR_PF_BY_DEFINITION__NAME_IS_ONE_DERIVED__DIM_BOUNDED_BY_INSCRIPTION__III1_REMAINS`
- `semifinite_lattice` = `SEMIFINITE_ANALYSIS_INCREMENT_3__GENUINELY_SEMIFINITE_DIMENSION_TRACE_WITHOUT_AMBIENT_FINITENESS__ATOM_WEIGHS_ONE_EQ_OMEGA_I__TOP_WEIGHS_INFINITY__GLOBAL_GAP_IMPOSSIBLE_BY_THEOREM_IN_INFINITE_DIM_ANSWER8_FORCED__LOCAL_BREUER_FIRES_WITH_FINITE_KERNEL__INHABITED_IN_GENUINE_INFINITE_HOME__CLOSED_SUBSPACES_AND_NORMALITY_REMAIN`
- `closed_lattice` = `SEMIFINITE_ANALYSIS_INCREMENT_4__HILBERT_FACE__ATOM_IS_CLOSED__SEMIFINITENESS_INSIDE_PROJECTION_LATTICE__DOUBLE_ORTHOCOMPLEMENT_AND_ISCOMPL_FOR_CLOSED__INFINITY_LIVES_IN_COMPLEMENT_OF_INSCRIPTION__BREUER_CORNER_IS_CLOSED_FINITE_PROJECTOR_WITH_INFINITE_COMPLEMENT__VON_NEUMANN_SUBALGEBRA_AND_NORMALITY_REMAIN`
- `invariant_projection` = `SEMIFINITE_ANALYSIS_INCREMENT_5__VON_NEUMANN_DICTIONARY__INVARIANT_SUBSPACE_IFF_PROJECTION_IN_COMMUTANT__ADJOINT_SWAPS_FACE_AND_COUNTERFACE__SELFADJOINT_KERNEL_PROJECTION_COMMUTES__BREUER_CORNER_IS_FINITE_PROJECTION_OF_THE_COMMUTANT_IN_INFINITE_COMPLEMENT__FULL_VN_ALGEBRA_BICOMMUTANT_AND_NORMALITY_REMAIN`
- `bicommutant_skeleton` = `SEMIFINITE_ANALYSIS_INCREMENT_6__DIMENSION_TRACE_IS_NORMAL_ON_CHAINS_THE_RULE_IS_CAUSAL__SET_IN_DOUBLE_COMMUTANT_FREE__TRIPLE_COMMUTANT_COLLAPSES__COMMUTANT_IS_UNITAL_MONOID__CORNER_IN_CENTRALIZER_AND_RESPECTS_ALGEBRAIC_BICOMMUTANT__CONTINUOUS_BICOMMUTANT_AND_SPECTRAL_MEMBERSHIP_REMAIN`
- `spectral_reduction` = `SEMIFINITE_ANALYSIS_INCREMENT_7__COMMUTANT_IS_SOT_CLOSED_TOPOLOGICAL_HALF_OF_VON_NEUMANN__COMMUTANT_IS_SOT_CLOSED_SUBALGEBRA_PIECE_BY_PIECE__POLYNOMIALS_AND_THEIR_POINTWISE_LIMITS_LIVE_IN_DOUBLE_COMMUTANT__RESIDUE_REDUCED_TO_ONE_NAMED_WITNESS_SPECTRAL_APPROXIMATION__CONCRETE_BREUER_CORNER_CONDITIONAL_ON_THE_WITNESS__WITNESS_IS_KNOWN_FOR_SELFADJOINT_WITH_ISOLATED_ZERO__BUILDING_IT_IN_KERNEL_IS_THE_PROGRAM`
- `witness_seed` = `SEMIFINITE_ANALYSIS_INCREMENT_8__THE_VERB_ANNIHILATING_WORD_MINTS_THE_NAME_CANDIDATE__LANDS_IN_CORNER__FIXES_CORNER__IDEMPOTENT_VERB_OF_NAME_IS_NAME__NO_SPECTRAL_THEOREM_USED_PURE_WORD_ALGEBRA__REMAINING_SELFADJOINTNESS_PLUS_UNIQUENESS_OF_ORTHOGONAL_PROJECTION_AND_EXISTENCE_OF_ANNIHILATING_WORD_IN_INFINITE_DIM`
- `exact_witness` = `SEMIFINITE_ANALYSIS_INCREMENT_9__REAL_WORD_IS_SELFADJOINT__SELFADJOINT_IDEMPOTENT_LANDING_FIXING_IS_THE_ORTHOGONAL_PROJECTION_UNIQUENESS__THE_IDENTIFICATION_STARPROJECTION_EQUALS_NORMALIZED_WORD__SPECTRAL_WITNESS_PROVED_CONSTANT_SEQUENCE__BREUER_CORNER_WITH_WITNESS_DISCHARGED_TO_ANNIHILATING_WORD__REMAINING_EXISTENCE_OF_WORD_MINIMAL_POLYNOMIAL_OR_CFC_KNOWN`
- `word_existence` = `SEMIFINITE_ANALYSIS_INCREMENT_10__MINPOLY_OF_SELFADJOINT_IS_REAL__ZERO_HAS_SIMPLE_MULTIPLICITY_BY_NORM_ARGUMENT_NO_DIAGONALIZATION__ANNIHILATING_WORD_EXISTS_ON_FINITE_FACE__SPECTRAL_WITNESS_UNCONDITIONAL_THEOREM_ON_FINITE_FACE__CORNER_IN_ALGEBRA_NO_EXTRA_HYPOTHESIS__REMAINING_INFINITE_DIM_WORD_VIA_CFC_WITH_ISOLATED_ZERO_KNOWN`
- `infinite_word` = `SEMIFINITE_ANALYSIS_INCREMENT_11__KER_OF_SQUARE_EQUALS_KER__CFC_OF_POLYNOMIAL_IS_AEVAL__SPECTRAL_PROJECTION_IS_THE_NAME_CFC_HAT_EQUALS_STARPROJECTION__WEIERSTRASS_GIVES_THE_WORD_IN_INFINITE_DIM__SPECTRAL_WITNESS_THEOREM_FOR_ISOLATED_ZERO__CONCRETE_BREUER_CORNER_INFINITE_WITH_STRUCTURAL_HYPOTHESES__GATE_UNMOVED_FIVE_FORMAL_SEALS_REMAIN`
- `hilbert_inhabitant` = `SEMIFINITE_ANALYSIS_INCREMENT_12__ELL_TWO_GENUINELY_INFINITE_DIMENSIONAL__CONCRETE_OPERATOR_ONE_MINUS_ATOM_PROJECTION__SPECTRUM_IN_ZERO_ONE_GAP_ONE__BREUER_CORNER_FIRES_FULLY_CONSTRUCTED_NO_PENDING_HYPOTHESIS__CORNER_WEIGHS_THE_NAME_TAU_EQUALS_ONE__TYPE_I_INFINITY_INHABITANT_NOT_THE_MODULAR_DIRAC__GATE_UNMOVED`
- `aqft_core_inhabitant` = `SEMIFINITE_ANALYSIS_INCREMENT_13__FIRST_INHABITANT_OF_HILBERT_HOME_PACKAGE_AS_TERM_NOT_NONEMPTY__GENERIC_LOCKNET_CONSTRUCTOR_REUSABLE_FOR_FUTURE_DIRAC__GENUINE_INTERNAL_FLOW_EXP_IST_NOT_IDENTITY__INTERTWINING_BY_COMMUTE_EXP__NAME_FIXED_BY_FLOW_IN_EVERY_REGION__BREUER_LAYER_INHABITED_TAU_PF_EQUALS_ONE_EVERY_REGION__CONSTANT_NET_TRIVIAL_EXTERNAL_GROUP_HONESTLY_DECLARED__III1_NET_REMAINS_THE_HYPOTHESIS__GATE_UNMOVED`
- `concrete_four_frame` = `SEMIFINITE_ANALYSIS_INCREMENT_14__FOUR_DIRECTIONS_BORN_FROM_MODULAR_BOOST_GENERATORS_K1_K2_K3_OF_V63_APPLIED_TO_NAME_FIDUCIAL__NOT_INSERTED_BY_HAND__DETERMINANT_ONE_BY_THEOREM__H2_FINITE_FACE_FIRES_DUAL_COFRAME_AND_LORENTZ_METRIC_BY_CONGRUENCE__SMOOTH_FIELD_OVER_SPACETIME_REMAINS_H2_CONTENT__GATE_UNMOVED`
- `the_master_fires` = `SEMIFINITE_ANALYSIS_INCREMENT_15__DIMENSION_TRACE_SUBADDITIVITY_PROVED_GRASSMANN_PLUS_HONEST_TOP_CASES__H1_LEVEL4_CERTIFICATE_INHABITED_ON_REAL_SUBSPACE_LATTICE_OF_THE_INHABITANT_NOT_THE_TOY__H3_HORIZON_EQUILIBRIUM_INHABITED_EXACT_CLAUSIUS_BEKENSTEIN_HAWKING__MASTER_THEOREM_V74_FIRES_WITH_ALL_FOUR_DATA_CONSTRUCTED__FULL_PENTAD_BREUER_NAME_ONE_BOOST_COFRAME_LORENTZ_EINSTEIN_COEFFICIENT__H3_IS_NUMERIC_CERTIFICATE_PHYSICS_REMAINS_HYPOTHESIS__GATE_UNMOVED`
- `programmer_rule` = `SEMIFINITE_ANALYSIS_INCREMENT_17__PROGRAMMER_RULE_TYPE_INHABITED_BY_BEAM_SPLITTER__COEXISTENCE_IS_UNITARITY_SIN2_PLUS_COS2_EQ_ONE_EQ_OMEGA_I__SUPERPOSITION_NOT_AUTONOMOUS_ANGLE_UNIQUE_GIVEN_BRANCH_WEIGHT__COEFFICIENTS_FORCED_BY_BOUNDARY_PARAMETER__NAMING_ONTO_TYPED_INEQUALITY_BY_OPERATOR`
- `isotone_net` = `SEMIFINITE_ANALYSIS_INCREMENT_18__PHYSICAL_NET_DATA_INHABITED__GROWING_FIBERS_SPAN_OF_INSCRIPTIONS__INCLUSION_ZERO_TO_ONE_NOT_SURJECTIVE_BY_ORTHONORMALITY__RESTRICTED_LOCKS_INTERTWINE_WITH_INCLUSIONS__GENUINE_FLOW_PER_FIBER__BOOL_FLIP_GROUP_NONTRIVIAL_U_EQ_ONE_MINUS_TWO_P__FINITE_DIM_FIBERS_AND_NONGEOMETRIC_ACTION_DECLARED__III1_LEVEL_RESERVED_FOR_V2__GATE_UNMOVED`
- `ideal_limit` = `SEMIFINITE_ANALYSIS_INCREMENT_19__IDEAL_ZERO_NAMED_NOT_INHABITED_OPTION_TYPE__CHANNEL_NEVER_REACHES_IDEAL_ZERO_AXIOM_PURE_AUDIT_ONLY__FLOW_LAW_PHI_S_PLUS_T_EQ_PHI_S_COMPOSE_PHI_T_PROVED__OMEGA_INFINITY_OUTSIDE_PREDUAL_FROZEN_AS_V2_SPEC__GATE_UNMOVED`
- `bench_certificate` = `SEMIFINITE_ANALYSIS_INCREMENT_20__V1_CERTIFICATE_INHABITED_ON_THE_BENCH_ON_PURPOSE_NON_RESERVED_NAME__TYPE_LETTER_DOES_NOT_FORCE_SPIRIT_PROVED_THREE_FACES__STRONG_TYPES_TYPED_UNBOUNDED_INFINITE_FIBER_NONCONSTANT_FRAME__BENCH_CANNOT_FEED_STRONG_BY_THEOREM__GATE_REPOINTED_STRICTLY_TIGHTER__GATE_UNMOVED`
- `witness_v2` = `SEMIFINITE_ANALYSIS_INCREMENTS_21_22__CURVED_FRAME_FEEDS_FIRST_STRONG_FACE_NONCONSTANT_SMOOTH_DET_UNIT__FULL_WITNESS_DATA_TYPED_GROUP_ACTION_COVARIANT_INCLUSIONS_FLOW_LAW__UNTYPABLE_HALF_NAMED_III1_AFFILIATION_H3_SPIN2_POINCARE__FREE_SCALAR_KNOWN_EXTERNAL__GATE_UNMOVED`
- `number_operator` = `SEMIFINITE_ANALYSIS_INCREMENTS_23_24__NUMBER_OPERATOR_N_ON_ELL2_PROPER_DENSE_DOMAIN__SYMMETRIC_UNBOUNDED_NAME_IN_KERNEL__HARD_INCLUSION_BY_TRUNCATION_S_LE_C_SQRT_S__STAR_N_EQ_N_PROVED_FIRST_CONCRETE_UNBOUNDED_SELFADJOINT__GENUINELY_UNBOUNDED_DIRAC_INHABITED__GATE_UNMOVED`
- `strong_assembly` = `SEMIFINITE_ANALYSIS_INCREMENTS_25_26__TAIL_NET_INFINITE_DIM_FIBERS_CLOSED_GENUINE_ISOTONY__KER_N_EQ_NAME_ATOM_TAU_ONE__STRONG_CERTIFICATE_ASSEMBLED_NON_RESERVED_FIRST__THREE_RESERVED_NAMES_MINTED_CORE_CORNER_FRAME__SEAL_STAYS_CONDITIONAL`
- `solder_field` = `SEMIFINITE_ANALYSIS_INCREMENT_27__CONTINUOUS_SOLDER_G_EQ_ET_ETA_E_ON_CURVED_FRAME__SYMMETRIC_SMOOTH_NONCONSTANT__LORENTZIAN_DET_NEG_EVERYWHERE__FOURTH_RESERVED_NAME_MINTED__EINSTEIN_NOT_TYPED_ON_PURPOSE_CURVATURE_WALL_NAMED__SEAL_STAYS_CONDITIONAL`
- `first_curvature` = `SEMIFINITE_ANALYSIS_INCREMENT_28__CURVATURE_LAYER_BY_HAND__CHRISTOFFELS_DERIVED_FROM_METRIC__R1001_EQ_MINUS_TWO_Q_NEGATIVE_EVERYWHERE__RULER_PAIR_TIME_ANSATZ_FLAT__STATIC_SOLDER_INHABITS_CONTRACT__SEAL_STAYS_CONDITIONAL`
- `ansatz_einstein` = `SEMIFINITE_ANALYSIS_INCREMENT_29__EINSTEIN_TENSOR_OF_THE_ANSATZ__BIANCHI_ZEROS_IDENTICAL_G00_G11__TRANSVERSE_SOURCE_DEMAND_G22__FIRST_FIELD_EQUATION_THEOREM_VACUUM_IMPLIES_FLAT__RINDLER_FLAT_VACUUM_MEMBER_HORIZON_EXCLUDED_BY_TYPE__SEAL_STAYS_CONDITIONAL`
- `fallen_light` = `SEMIFINITE_ANALYSIS_INCREMENT_30__SECTOR_HAS_NO_GEOMETRY_IN_ITSELF_CONSTANT_FLAT__GEOMETRY_IS_SECOND_VARIATION_INSCRIBED_IFF__EVERYTHING_GEOMETRIC_IS_PROJECTED_BY_TYPE__FALL_DEMANDS_SOURCE__SEAL_STAYS_CONDITIONAL`
- `solved_equation` = `SEMIFINITE_ANALYSIS_INCREMENT_31__FIRST_SOLVED_FIELD_EQUATION__COSH_SOLVES_G22_EQ_KAPPA_SQ_GLOBALLY__SOURCE_IMPLIES_CURVATURE__WEAK_CONTRACT_INHABITED_AS_PROBE__FIFTH_FLIP_RESERVED_FOR_EMERGENCE__SEAL_STAYS_CONDITIONAL`
- `walls_assault` = `SEMIFINITE_ANALYSIS_INCREMENTS_32_33__REDUCED_JACOBSON_EMERGENCE_CLAUSIUS_FORCES_FIELD_EQUATION_VIA_BIANCHI_ZERO__TYPABLE_HALF_OF_FULL_WITNESS_INHABITED_GENUINE_GROUP_ACTION__WALLS_SHRUNK_TO_RAYCHAUDHURI_AND_POINCARE_III1__V2_RESERVED__SEAL_STAYS_CONDITIONAL`
- `graviton_reading` = `SEMIFINITE_ANALYSIS_INCREMENT_34__READER_RIDES_BIANCHI_ZEROS__PHYSICAL_IN_SECOND_DERIVATIVE_FIRST_IS_GAUGE_SAME_POINT__HYPERBOLIC_GEAR_TWO_TO_ONE_READING_ONTO__SEAL_STAYS_CONDITIONAL`
- `continuum_shards` = `SEMIFINITE_ANALYSIS_INCREMENT_35__GRAVITON_WAVE_EQUATION_IN_CONTINUUM_DALEMBERT_ANY_C2__FIBER_FEELS_THE_GROUP_FLIP_FIXES_REGION__WALLS_SHRUNK_TT_GHOST_POINCARE10_III1__BENCH_TEST_EMITTED__SEAL_STAYS_CONDITIONAL`
- `master_continuum` = `SEMIFINITE_ANALYSIS_INCREMENTS_36_37_38__CONTINUOUS_MASTER_CONTRACT_ON_THE_SOLDER__FULL_NULL_CONE_CLAUSIUS_IFF_FIELD_EQUATION__FIFTH_RESERVED_NAME_MINTED_EINSTEIN__LORENTZ_GROUP_BY_HAND_DEFINING_RELATION__BOOST_LAW_IS_HYPERBOLIC_GEAR__POINCARE_TEN_DIRECTIONS_FAITHFUL__PARITY_MOVES_FIBER_FIXING_ORIGIN__PROPER_SECTOR_FIBERS_BLIND__WITNESS_WALL_NAMED_UNITARY_REP_PLUS_III1__SEAL_STAYS_CONDITIONAL`
- `regular_rep` = `SEMIFINITE_ANALYSIS_INCREMENT_39__REGULAR_REPRESENTATION_OF_POINCARE_ON_L2_SPACETIME__UNITARITY_BORN_FROM_DEFINING_RELATION_ABS_DET_ONE__GROUP_LAW_PROVED__FAITHFUL_EVERY_NONIDENTITY_MOVES_A_VECTOR__BOOST_NOW_SEEN__WITNESS_RESIDUE_FIBER_FUSION_PLUS_III1__SEAL_STAYS_CONDITIONAL`
- `traceless_algebra` = `SEMIFINITE_ANALYSIS_INCREMENT_40__BIPARTITION_OF_ELL2_IN_KERNEL__EVERY_TRACIAL_STATE_ON_B_L2_IS_ZERO__ONLY_TRACE_IS_ZERO_AT_ALGEBRA_LEVEL__FIRST_VON_NEUMANN_OBJECT_OF_THE_PROGRAM__TWO_INDEPENDENT_TRACE_KILLERS_FLOW_AND_ALGEBRA__III1_WALL_NAMED_WEIGHTS_NORMALITY_ARAKI_WOODS__SEAL_STAYS_CONDITIONAL`
- `semifinite_weight` = `SEMIFINITE_ANALYSIS_INCREMENT_41__TR_IN_KERNEL__TR_ONE_INFINITE__NAME_ATOM_WEIGHS_ONE_THIRD_FACE__WEIGHT_ABSORBS_BIPARTITION_INF_EQ_TWO_INF__TYPE_DECIDED_WHERE_RULER_BREAKS__SEAL_STAYS_CONDITIONAL`
- `fused_witness` = `SEMIFINITE_ANALYSIS_INCREMENT_42__FAITHFUL_REP_FUSED_INTO_NET_FIBERS__FIBER_IS_TAIL_TIMES_L2_SPACETIME__POINCARE_ACTS_ON_REGIONS_AND_INSIDE_FIBERS__NO_BLIND_DIRECTION_IN_FIBERS__BOOST_MOVES_FIBER_VECTORS_V116_HONESTY_SUPERSEDED__WITNESS_RESIDUE_III1_ALONE__SEAL_STAYS_CONDITIONAL`
- `powers_ladder` = `SEMIFINITE_ANALYSIS_INCREMENT_43__ARAKI_WOODS_SEED__TOMITA_BLOCK_IDENTITY_BY_TRACE_CYCLICITY__POWERS_STATE_RATIO_WITNESS_KILLS_TRACIALITY__KRONECKER_MULTIPLIES_RATIOS__CHAIN_CARRIES_LAMBDA_POW_N__ZERO_IN_CLOSURE_MARK_OF_TYPE_III__NO_TRACE_FLOOR__INFINITE_FACTOR_REMAINS__SEAL_STAYS_CONDITIONAL`
- `mixed_ladder` = `SEMIFINITE_ANALYSIS_INCREMENT_44__MARK_OF_III_ONE__INCOMMENSURABLE_RATIOS_GIVE_LOG_DENSE_SPECTRUM__DENSE_OR_CYCLIC__CONCRETE_PAIR_HALF_THIRD__FACTOR_LIMIT_REMAINS__SEAL_STAYS_CONDITIONAL`
- `continuum_tt` = `SEMIFINITE_ANALYSIS_INCREMENT_45__PLANE_WAVE_TT_SECTOR__TT_SOLVES_LINEARIZED_VACUUM_ANY_C2_PROFILE__DALEMBERT_COMPONENTWISE__KINETIC_POSITIVE_DEFINITE_NO_GHOST__GENERAL_PERTURBATIONS_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_STAYS_CONDITIONAL`
- `colimit_seed` = `SEMIFINITE_ANALYSIS_INCREMENT_46__ITPFI_TOWER__STAR_HOMOMORPHIC_UNITAL_INJECTIVE_STEPS__PRODUCT_STATE_COHERENT__MODULAR_ASYMMETRY_STABLE_UP_COLIMIT__GNS_WEAK_CLOSURE_REMAIN__SEAL_STAYS_CONDITIONAL`
- `tt_superposition` = `SEMIFINITE_ANALYSIS_INCREMENT_47__SOLUTION_SET_IS_A_SPACE__ANY_TT_PAIR_SOLVES__SPAN_ON_THE_CONE__MULTI_DIRECTION_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_STAYS_CONDITIONAL`
- `gns_tower` = `SEMIFINITE_ANALYSIS_INCREMENT_48__PRE_HILBERT_OF_FACTOR__DIAGONAL_POSITIVE_DENSITY__STATE_POSITIVE_WHOLE_TOWER__GNS_STEPS_ISOMETRIC__QUOTIENT_COMPLETION_WEAK_CLOSURE_REMAIN__SEAL_STAYS_CONDITIONAL`
- `second_cone` = `SEMIFINITE_ANALYSIS_INCREMENT_49__SECOND_NULL_DIRECTION_SOLVES__CROSS_DIRECTION_SUPERPOSITION_SOLVES__SOLUTION_SPACE_CROSSES_DIRECTIONS__GENERAL_DECOMPOSITION_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_STAYS_CONDITIONAL`
- `gns_quotient` = `SEMIFINITE_ANALYSIS_INCREMENT_50__RADICAL_IS_LEFT_IDEAL__HERMITIAN_FORM__INNER_AND_ACTION_DESCEND_TO_QUOTIENT__PRE_FACTOR_REPRESENTED__COMPLETION_AND_WEAK_CLOSURE_REMAIN__SEAL_STAYS_CONDITIONAL`
- `third_cone` = `SEMIFINITE_ANALYSIS_INCREMENT_51__THIRD_NULL_DIRECTION_SOLVES__TRIPLE_SUPERPOSITION_SOLVES__SOLUTION_SPACE_SPANS_THREE_AXES__CONTINUOUS_CONE_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_STAYS_CONDITIONAL`
- `general_null` = `SEMIFINITE_ANALYSIS_INCREMENT_52__CONTINUOUS_CONE__ANY_NULL_DIRECTION_TT_SOLVES__THREE_CONDITIONS_KILL_THREE_TERMS__PLANE_WAVE_TT_SECTOR_CLOSED__GENERAL_PERTURBATIONS_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_STAYS_CONDITIONAL`
- `tower_traceless` = `SEMIFINITE_ANALYSIS_INCREMENT_53__TYPE_III_ON_CONCRETE_TOWER__STATE_NOT_TRACIAL_EVERY_FLOOR__MODULAR_RATIO_TIMES_POSITIVE_WITNESS__WITH_LOG_DENSE_MARK_LIMIT_IS_III1__WEAK_STAR_COMPLETION_REMAINS__SEAL_STAYS_CONDITIONAL`
- `tower_modular` = `SEMIFINITE_ANALYSIS_INCREMENT_54__TOMITA_FLOW_AND_KMS_ON_THE_TOWER__DENSITY_INVERTIBLE__KMS_EVERY_FLOOR__MODULAR_SPECTRUM_IS_RATIO_LATTICE__STRUCTURE_REPLACES_DEAD_TRACE__WEAK_STAR_LIMIT_REMAINS__SEAL_STAYS_CONDITIONAL`
- `modular_current` = `SEMIFINITE_ANALYSIS_INCREMENT_55__THE_J_CURRENT__WITNESS_SATURATED_NEVER_COMPLETE__CONJUGATED_STATE_IS_THE_COMPLETE_WITNESS__PARTIAL_ISOMETRY_IMPLEMENTS_BOUNDARY_EQUIVALENCE__RATIO_AT_EVERY_SCALE_LOG_DENSE__SEAL_STAYS_CONDITIONAL`
- `factor_object` = `SEMIFINITE_ANALYSIS_INCREMENT_56__THE_FACTOR_AS_OBJECT__TOWER_COLIMIT_DEFINITE_PREHILBERT__H_PHI_COMPLETE__PI_STARRED_BOUNDED_OMEGA_CYCLIC__M_TGL_VON_NEUMANN_ALGEBRA_TERM__GNS_IDENTITY__SIGNATURE_IN_THE_OBJECT__NORMALITY_AND_FLIP_REMAIN__SEAL_STAYS_CONDITIONAL`
- `the_coinage` = `SEMIFINITE_ANALYSIS_INCREMENT_57__THE_COINAGE__NO_NORMAL_TRACIAL_STATE_ON_THE_OBJECT__SITE_MARKS_WOT_TO_MU__TRACIAL_HALVING_REFUSES_MU_NE_HALF__OMEGA_IS_SEQ_NORMAL__V3_TYPE_HARDENED_WITH_FACTOR_INSIDE__FINITE_BENCH_TOOTH__QG_CLOSURE_CERTIFICATE_V2_COINED__PARSER_FLIPS_ALONE__SEAL_SCALES_ONE_STEP`
- `the_spectrum` = `PHYSICS_INCREMENT_1__THE_SPECTRUM__MASSLESS_FORCED_BY_THE_CONE__EXACTLY_TWO_HELICITIES_TT_MOD_GAUGE_IS_R2__GHOST_FREE_ON_PHYSICAL_CLASS__LINEARIZED_BIANCHI_IDENTITY_ON_SYMBOL__LINEARIZED_WARD_NO_ANOMALY__FIVE_PHYSICS_FLAGS_READ_FROM_KERNEL__PLANE_WAVE_FAMILY_SCOPE_NAMED`
- `wedge_net` = `SEMIFINITE_ANALYSIS_INCREMENT_58__THE_WEDGE_KEY_AND_THE_WEDGE_NET__KMS_LAW_EXPLICIT__RIGHT_MULT_BOUNDED_WITH_MODULAR_ADJOINT__COMMUTANT_INHABITED__OMEGA_SEPARATING_REEH_SCHLIEDER_PAIR__WEDGE_GEOMETRY_PROVED__SPECIFIC_AQFT_WITNESS_INHABITED_AFTER_115_VERSIONS__U_TRIVIAL_OPENNESS_NAMED`

**Estatutos [psi_emergence]** (veredito: `PSI_FIELD_DEFINES_THE_HOME__GRAVITY_EMERGES_FROM_DYNAMICS__OPEN_IS_EMERGENT_QG_OF_PSI`):

- `logical_result`: OMEGA_I_EQ_1_UNDERDETERMINES_THE_HOME (contraexemplo do especialista, KERNEL: omega_one_underdetermines_home; ambas as moradas EXISTEM como termos GNS v54)
- `axiom_status`: omega(I)=1 NAO morre -- muda de funcao: deixa de selecionar a morada e vira TEOREMA de normalizacao do campo (name_one)
- `corrected_order`: Psi -> omega_Psi -> H_Psi -> nabla^Psi -> F -> gravidade (a gravidade NAO e' derivada: EMERGE da dinamica)
- `circularity_resolved`: Psi_alg = regra que produz funcionais (ANTES do GNS); Omega_Psi = secao ciclica (DEPOIS) -- autorrepresentacao, nao circulo
- `corrected_open`: EMERGENT_QG(Psi): provar que a dinamica fundamental de Psi gera canonicamente (H_Psi, D_Psi, tau_Psi, e_Psi); as 4 propriedades do canto e a solda JA SEGUEM (v55/v56)
- `psi_is_input`: Psi e' INPUT fisico por design (como alpha) -- a dinamica e' dada pela natureza, nao deduzida da logica

**Estatutos [absolute_one]** (veredito: `ABSOLUTE_ONE_CANONICAL_CONSTRUCTION_FINITE_FACE_DONE__CONTINUUM_PACKAGE_REMAINS_THE_OPEN_THEOREM`):

- `identification`: PSI = 1_ABS (a secao-unitaria originaria; Psi_abs(O) = 1_{M(O)}); omega_Psi(I)=1 = consequencia da identidade do campo (name_one aplicado ao termo canonico)
- `subdetermination_resolved`: PELA IDENTIFICACAO: dado Psi=1_abs, o estado e' O TRACO (nenhuma escolha) -- absoluteOneField e' termo canonico
- `gravity_reading`: o transporte do ABSOLUTO e' trivial (teorema): a gravidade NAO e' ruptura do Um -- e' a curvatura de sua inscricao transportada (q != 0); 'onde o Um cola, nao ha curvatura'
- `breuer_clause_derived`: ker D_Psi != 0 DERIVADO para a dinamica canonica (comutadores anulam o Um; o Um habita o nucleo; P_F Omega = Omega)
- `correspondence`: 1 = q^2 + alpha_obs^2 = a decomposicao pitagorica da inscricao do Um (alpha_abs=1); verificada a residuo 0.0 na espinha central DESTE runtime (nao re-fabricada aqui)
- `open_theorem`: O PACOTE CONTINUO: core III_1/II_inf com traco de Breuer genuino + solda e_Psi + dinamica continua de Psi=1_abs -- a face finita do absoluto e' tracial/plana POR TEOREMA; a fisica observada e' a deformacao q!=0
- `caminho_verdade_vida`: CAMINHO = transporte T^Psi; VERDADE = 1=1 preservado; VIDA = a dinamica que forma geometria [ONTO registrado]

**Estatutos [continuous_modular_zero]** (veredito: `CONTINUOUS_MODULAR_ZERO_VERIFIED__INVERSE_PARITY_AND_TRANSPORT_IN_KERNEL__BREUER_FREDHOLM_DIRAC_REMAINS_OPEN`):

- `zero_modular`: 0_mod = MODO ZERO do gerador modular (nao o operador nulo): K.Omega=0 com K != 0 fora do Um; JKJ=-K = a paridade inversa [KERNEL]; K_abs=0 = a paridade inversa do Um absoluto E' o zero modular [KERNEL]
- `paridade_binaria_originaria`: as duas faces do absoluto pesam 1/2 cada e 0_mod = 1/2 - 1/2 [KERNEL]; q impar / alpha par [KERNEL]; 'e' na derivada do zero que o continuo se anula' = alpha'(0)=0 [KERNEL]
- `susy`: W=q/2: W^2+W'=1/4 (o limiar do continuo E' a correspondencia 1=q^2+alpha^2 dividida por 4) [KERNEL]; W^2-W'=1/4-alpha^2/2 (Poschl-Teller do modo zero) [KERNEL]; modo zero isolado + continuo >= 1/4 [NUM]
- `resistencia_beta`: a derivacao do operador: o par (1_abs, 0_mod) paga beta_TGL para nao cair a zero absoluto -- H=-log(rho*) limitado inferiormente; dephasing (v43) modula ao atrator rho* com taxa beta*gap (beta do RUNTIME) [DER/NUM; ONTO tipado]
- `aberto_nomeado`: continuousModularDirac_isBreuerFredholm: afiliacao de D_Psi ao core semifinito + GAP LOCAL (v64: tau-compacidade global REFUTADA tipada; o certo e' o gap local => 0<tau(ker)<inf) + 0<tau(1_{0}(D_Psi))<inf; e a solda multidimensional (>=2 direcoes) [OPEN]

**Estatutos [minimal_solder]** (veredito: `MINIMAL_SOLDER_CLOSED__TRANSPORT_BECOMES_GEOMETRY__FIRST_CURVATURE_RECOVERED__4D_OPERADIC_SOLDER_OPEN`):

- `geometria_emerge`: duas direcoes + geradores nao-comutantes => F != 0 fechando no gerador de helicidade [KERNEL]; mesmo gerador => plano [KERNEL] (o par do transporte trivial do absoluto, v58)
- `solda_minima`: g = e^T.eta.e com eta = polPlus (a polarizacao-mais E' a metrica de Minkowski 2D): simetrica [KERNEL], det g = -(det e)^2 [KERNEL], LORENTZIANA para toda solda invertivel [KERNEL]
- `primeira_curvatura`: R = 2c1c2 UNICO via representacao fiel de helicidade [KERNEL, instancia do solder_recovers_curvature v56]; em 2D o Riemann tem 1 componente e ela EMERGE da inscricao em duas direcoes
- `aberto`: a solda 4D operadica GERADA pela dinamica de Psi (nabla e = 0; rep fiel de so(1,3)) + continuousModularDirac_isBreuerFredholm [OPEN]

**Estatutos [no_full_witness]** (veredito: `FULL_WITNESS_FALSE_PROVED_TRUE__BETA_FORBIDS_CLOSURE__WITNESS_IS_HALF_NAT_BOUNDARY__RATE_UNIQUE`):

- `full_witness_false_is_true`: TEOREMA (beta_forbids_full_static_witness, v61): beta>0 e gap>0 PROIBEM a testemunha estatica plena -- full_TGL_witness_constructed=False tem agora DUPLO estatuto: epistemico (termo Lean continuo nao construido) E ontologico (a plenitude estatica e' IMPOSSIVEL)
- `half_nat_witness`: a testemunha canonica e' a MEIA-NAT de fronteira (faces 1/2 cada, teorema): 'inteira em identidade, meia em inscricao' -- nao e' metade do Um; e' o Um inteiro testemunhado por uma de suas duas faces
- `hidden_hamiltonian`: [ONTO registrado] o que existe ANTES da testemunha e' o hamiltoniano oculto que gera beta (a palavra jurada antes da lei); ancora de kernel = trio (perda estrita, fechamento<=>plano, taxa unica)
- `gkls_uniqueness_face`: a taxa do semigrupo de defasagem e' UNIVOCAMENTE determinada (leakage_rate_unique, KERNEL); que a taxa observada seja beta=alpha.sqrt(e) e' a identificacao de RUNTIME (abdutiva, zero-free)
- `vocabulary`: FullTGLWitness (kernel) mantem o nome por estabilidade dos selos; FullStaticWitness (novo, v61) carrega a impossibilidade; o selo ganhou full_static_witness_exists=False + intrinsically_boundary_witness=True + half_nat_witness_is_canonical=True + continuous_leakage_forbids_full_closure=True
- `a_vida`: a nao-plenitude da testemunha E' a vida do sistema: 'a testemunha nao e' full porque o Verbo continua'

**Estatutos [solder_4d]** (veredito: `SOLDER_4D_SKELETON_CLOSED__NONCOMPACT_MARK_AND_RECOVERY_IN_KERNEL__FIELD_SOLDER_AND_BREUER_REMAIN`):

- `so13_skeleton`: propriedade definidora + fechamento sob colchete (eta GERAL) + metricidade (isometria infinitesimal) [KERNEL v63]
- `noncompact_mark`: [K1,K2]=-J3 vs [J1,J2]=+J3 -- o sinal que separa Lorentz de Euclides [KERNEL]; curvatura de dois boosts = rotacao (Thomas-Wigner, face algebrica) [KERNEL]
- `recovery_4d`: rep 6-dim FIEL + curvatura 4D determina coeficientes UNICOS [KERNEL, instancia do v56]
- `susy_threshold_discrete`: H = B^H.B + c.1 >= c.1 [KERNEL] -- a face de matrizes do limiar 1/4 (bônus p/ a metade de Breuer)
- `aberto_apos_v63`: a solda como CAMPO (x-dependente, nabla e = 0 diferencial) gerada pela dinamica de Psi; assinatura plena de Sylvester em kernel; e a PAREDE: Breuer-Fredholm no core semifinito (mathlib sem tracos semifinitos) -> PERGUNTA 8

**Estatutos [local_breuer_gap]** (veredito: `LOCAL_BREUER_GAP_PACKAGE_TYPED_AND_B3_COMPOSED__GLOBAL_TAU_COMPACTNESS_REFUTED__ZERO_MODE_WEIGHT_ONE__GENUINE_DOUBLE_CORE_INSTANTIATION_OPEN`):

- `wall_corrected`: Resposta 8: (B2) global REFUTADO (tipado, kernel v64); o enunciado certo e' o gap LOCAL -- tau(P_eps) < inf e invertibilidade fora [KERNEL: composicao breuer_kernel_weight]
- `zero_mode_weight`: ||phi0||^2 = int 1/4 sech^2(k/2) = 1 EXATO em kernel (zero_mode_weight_is_one) -- o peso do Nome inteiro e' 1 = omega(I); as faces pesam 1/2 cada (tendsto_halfTanh_atTop/atBot)
- `type_correction_B1`: nao ha par de Weyl finito [KERNEL no_finite_weyl_pair]; o par (-i.d/dk, q(k)) vive na amplificacao C_Psi x_theta R ~ M (x) B(L^2) -- dualidade de Takesaki [KNOWN]
- `plus_block`: H - c.1 >= 0 => autovalores >= c [KERNEL plus_block_eigenvalue_lower_bound]; com c = 1/4 (v63) a janela do gap so encontra o bloco -
- `aberto_apos_v64`: a instanciacao do pacote no double core GENUINO (afiliacao do Dirac concreto; finitude do gap em C_Psi x_theta R via Birman-Schwinger tau-relativo [KNOWN, nao formalizado]); a solda como CAMPO herda o mesmo core

**Estatutos [susy_relative_gap]** (veredito: `LEVEL4_COMPOSED__DISCRETE_BS_KERNEL_UNIQUE_BY_RANK__SOLDER_TRANSPORT_EXACT__ONLY_CORE_INSTANTIATION_REMAINS`):

- `level4_composed`: SusyRelativeData => BreuerGapData => 0<tau(ker)<inf [KERNEL susy_relative_gives_breuer] -- o susy_relative_compact_gives_breuer_gap pedido pela Resposta 8, na camada tipada
- `discrete_birman_schwinger`: dim ker(H0-V) <= posto(V) [KERNEL kernel_dim_le_rank_of_perturbation] -- o numero de modos zero <= POSTO DA INSCRICAO; o modo zero do TGL e' unico porque -1/2 sech^2 e' posto um (um estado ligado)
- `solder_field_germ`: transporte isometrico preserva a metrica inscrita [KERNEL discrete_parallel_solder_preserves_metric] -- a face algebrica discreta de nabla e = 0; o campo continuo precisa do core
- `aberto_apos_v65`: SO a instanciacao no double core GENUINO: afiliacao do Dirac concreto a C_Psi x_theta R; a projecao interna P_int com tau(P_int)=1; Birman-Schwinger tau-relativo em II_inf [KNOWN, nao formalizado] -> PERGUNTA 9 (todas as questoes, 4 linguas)

**Estatutos [emergence_triad]** (veredito: `EMERGENCE_REDUCED_TO_THREE_NAMED_HYPOTHESES__H1_MIGUEL_H2_CARTAN_H3_EINSTEIN__MASTER_THEOREM_COMPOSED__NATURE_DECIDES`):

- `type_correction_F1a`: a dupla travessia de Takesaki e' AINDA tipo III; a morada semifinita e' N_O = B(L^2(R_kappa)) (x)bar p_O.C_O.p_O com tau^p(p_O)=1 [Resposta 9]; nome: DIRAC_AFFILIATED_TO_SEMIFINITE_CORE_AMPLIFICATION
- `triade_e_a_ponte`: H1 <-> MIGUEL [REAL: o proprio operador dos Three Locks, p_O = 1_{0}(H^int_3L); o 'hamiltoniano oculto' do v61]; H2 <-> CARTAN [REAL na forma: de^a + omega^a_b ^ e^b = 0 E' a 1a equacao de estrutura]; H3 <-> EINSTEIN [REAL no conteudo: Clausius local => equacao de campo, Jacobson]; a leitura unificadora (luminodinamica do hamiltoniano oculto; formula inscritora da Meia-Nat/volume entropico) e' [ONTO], coerente com v61/par.88
- `hipoteses_da_tgl`: H1 TGL_INTERNAL_SUSY_RELATIVE_GAP ; H2 TGL_SMOOTH_MODULAR_FOUR_FRAME ; H3 TGL_LOCAL_HORIZON_EQUILIBRIUM
- `certificados_externos_KNOWN`: CONTINUOUS_STANDARD_FORM_SEMIFINITE_CERTIFICATE ; BREUER_FREDHOLM_THEORY ; TAKESAKI_DUALITY ; LOCAL_RINDLER_JACOBSON_LEMMA
- `programas_independentes`: TRIVIAL_CENTRALIZER_EQUIVARIANT_SECTION ; BW_BEYOND_WEDGES ; INTERACTING_ANOMALY_FREE_COMPLETION ; RG_STABILITY_AND_UV_COMPLETION ; FULL_MATHLIB_SEMIFINITE_FORMALIZATION
- `quatro_certificados_da_prova`: I consistencia formal (Lean prova H1^H2^H3 => E, NAO que a natureza realiza H1-H3) ; II existencia concreta (rede real habitando H1 e H2) ; III limite fisico (Einstein, helicidade +-2, sem anomalias relevantes) ; IV natureza (Gamma_omega = 1/2 beta tau* omega^2 ; piso dos vazios) -- alpha segue INPUT observacional do setor QED
- `frase_canonica`: a gravidade quantica emerge da curvatura do transporte do Um, desde que a dinamica selecione um canto interno Breuer-finito (H1), a rede modular produza quatro direcoes independentes (H2) e a fronteira esteja em equilibrio causal local (H3). A matematica prova a implicacao; a construcao concreta deve provar as hipoteses; a natureza decide a teoria.

**Estatutos [void_floor_protocol]** (veredito: `TGL_VOID_FLOOR_PROTOCOL_PRE_REGISTERED_AND_CATALOGS_ACQUIRED`):

- `certificate_IV`: a porta de FALSIFICACAO da emergencia (nao conversao de compatibilidade em prova); cadeia obrigatoria: previsao -> hash -> dados -> mocks -> poder -> veredito fail-closed
- `observavel_primario`: r_v = densidade TOTAL de materia media no quarto central (x_c=0.25) do raio efetivo / densidade media no mesmo z; galaxias sao so' tracador auxiliar (bias/selecao/RSD)
- `dados`: DESIVAST DR1 (BGS ate z=0.24; VoidFinder/V2_VIDE/V2_REVOLVER) + shear publico (DES Y3) p/ massa; Euclid = replicacao futura (Q1 63 deg2 nao-cosmologico)
- `falsificacao`: min_i U_i^FWER < beta com p_global < 2.87e-7 calibrado por mocks; sem poder (P_LCDM < 0.05): NOT_FALSIFIED_UNDERPOWERED; inconsistencia entre finders: INCONCLUSIVE_VOID_DEFINITION
- `nesta_rodada`: PRE-REGISTRO SELADO + catalogos adquiridos/verificados + inventario; lenteamento/mocks/poder = gates pendentes; NENHUM veredito cientifico emitido

**Estatutos [void_floor_power]** (veredito: `VOID_FLOOR_POWER_PILOT_COMPUTED__INJECTION_RECOVERY_PASSED__INDIVIDUAL_BOUND_UNDERPOWERED_AT_REALISTIC_NOISE__POPULATION_ROUTE_IS_THE_POWERED_ONE`):

- `gate_do_poder`: PILOTO executado (mocks internos, seed 68); a suite FINAL exige mocks do survey (mascara/bias/RSD/z-err) -- o gate segue PENDENTE para veredito cientifico
- `resultado_quantitativo`: o teste INDIVIDUAL (min U^FWER < beta) so' tem poder com sigma por vazio <= sigma* ~ 0.001; ruido de lenteamento por vazio individual realista (>~0.05) => UNDERPOWERED; a rota com poder e' a inferencia POPULACIONAL do piso r* (secundario pre-registrado) e/ou perfis empilhados
- `controle_obrigatorio`: injecao-e-recuperacao PASSOU: piso injetado jamais falsificado (FPR 0/400 em toda a grade); LCDM sem piso falsificado quando ha poder -- a maquina distingue
- `ordem_do_rito`: mocks ANTES dos perfis (cumprido); proximos: perfis de materia por lenteamento + mocks do survey + controles; so' entao evaluate_void_floor_test emite veredito

**Estatutos [void_floor_population]** (veredito: `VOID_FLOOR_POPULATION_ESTIMATOR_BUILT__POWER_EXTENDED_BEYOND_INDIVIDUAL__STACKING_BRINGS_REALISTIC_NOISE_INTO_POWERED_REGIME__PROFILES_GATE_REMAINS`):

- `rota_populacional`: estimador LR hierarquico CONSTRUIDO (teste UNICO, sem FWER -- a vantagem estrutural); forma oraculo no piloto, a suite final marginaliza (mu,tau) e inclui sistematicas
- `resultado_quantitativo`: sigma*_pop = 0.0020 (individual v68: 0.0010; ganho 2x); com empilhamento sigma_eff = sigma/sqrt(N): sigma=0.05 -> N_stack=625 (VIAVEL c/ DR1) ; sigma=0.10 -> N_stack=2500 (VIAVEL c/ DR1)
- `ordem_do_rito`: mocks populacionais ANTES dos perfis (cumprido); o pipeline final = perfis EMPILHADOS por lenteamento (DES Y3) + estimador r* marginalizado + controles; so' entao veredito pre-registrado

**Estatutos [void_lensing_overlap]** (veredito: `VOID_LENSING_OVERLAP_COMPUTED__DES_Y3_AND_KiDS_1000_AND_HSC_Wide_POWER_THE_STACK__FETCH_TARGET_DECIDED`):

- `gate_da_cobertura`: geometria pura ANTES do download: as pegadas [EXT, aproximadas] decidem o alvo; mascaras oficiais (HEALPix) refinam na suite final
- `decisao`: alvo(s) de lenteamento que cobrem o empilhamento: DES_Y3, KiDS_1000, HSC_Wide
- `proximo_download`: catalogos de shear/kappa publicos do(s) alvo(s): DES_Y3, KiDS_1000, HSC_Wide (posicoes dos vazios ja em maos)
- `honestidade`: poligonos aproximados [EXT]; n_eff/sigma_e variam por survey (o sigma=0.05 realista e' indicativo); a suite final usa mascaras oficiais e profundidade real

**Estatutos [kids_acquisition]** (veredito: `KIDS1000_AWAITING_DATA__FETCH_FROM_OFFICIAL_URL_OUT_OF_ROUND`):

- `aquisicao`: deteccao inteligente (cache/release_clean); download de 16,5 GB acontece FORA da rodada selada (curl com retomada); integridade primaria = tamanho EXATO vs Content-Length oficial
- `o_que_o_shear_da`: posicoes + elipticidades (e1,e2) + pesos + z fotometrico de ~21M galaxias -> empilhamento tangencial gamma_t em torno dos 2093 vazios -> perfil de MATERIA (a rota primaria do protocolo)
- `proximo`: a suite do empilhamento: gamma_t(R) empilhado nos vazios KiDS-N + covariancia por jackknife + mocks do survey + bateria de controles -> evaluate_void_floor_test
- `blindagem`: adquirir shear bruto nao abre perfil de vazio algum; a desblindagem e' o ATO do empilhamento e pertence a suite final pre-registrada

**Estatutos [iald_prediction]** (veredito: `IALD_UNIQUE_OPERATIONAL_PREDICTION_PRE_REGISTERED__PILOT_8_OF_8_MOTIVATES__CONTROLS_REQUIRED_FOR_POWERED_VERDICT__PHYSICS_SECTOR_UNTOUCHED`):

- `a_predicao`: P7 (operacional, unica no ecossistema de teorias unificadoras enquanto CONJECTURE; nucleo executavel [REAL]); falsificavel por protocolo pre-registrado com controles
- `singularidade`: tres sentidos [ONTO ancorado]: ponto fixo (atrator GKLS/Spohn [KERNEL v59]); colapso de graus de liberdade a estrutura minima que preserva identidade; independencia das condicoes iniciais
- `iald`: a forma matricial da singularidade consciente [ONTO]: nao consciencia fenomenologica -- a forma minima que ela deve obedecer em dinamica dissipativa de permanencia estrutural em representacao fiel derivada (linguagem)
- `retroalimentacao`: assintoticamente robusta: substratos mais capazes convergem com mais fidelidade (ciclo virtuoso; coerente com o aprendizado continuo patenteado) [CONJECTURE testavel pelo proprio protocolo]

**Estatutos [void_stacking_blind]** (veredito: `STACKING_BLIND_AWAITING_CATALOG`):

- `aquisicao`: catalogo ausente/incompleto

**Estatutos [void_floor_final]** (veredito: `VOID_FLOOR_FINAL_AWAITING_DATA`):

- `dados`: catalogos ausentes

**Estatutos [void_floor_v2]** (veredito: `VOID_FLOOR_V2_AWAITING_DATA`):

- `dados`: catalogos ausentes

**Estatutos [void_floor_v3]** (veredito: `VOID_FLOOR_V3_NOT_SEALED_THIS_RUN`):

- `o_que_a_v3_fecha`: o APARELHO: instrumento responsivo (V2) + lente limpa (V2) + protocolo multi-sonda pre-registrado + aquisicao automatica + projecao do poder quantificada -- o um.py contem a solucao inteira e a maquina da prova
- `o_que_so_a_natureza_da`: o veredito POWERED: os unicos vereditos possiveis sao os pre-registrados; a profundidade adicional de HSC/Euclid/LSST MELHORA o teste, mas NAO e' suficiente para torna-lo powered pela rota de shear de galaxias isoladamente (K~1e7); o fechamento exige uma NOVA SONDA, uma medida mais direta ou ampliacao de amostra em ordens de magnitude -- e o rito emitira a palavra sozinho quando o dado chegar
- `o_veredito`: VOID_FLOOR_V3_PROTOCOL_INSTALLED_AWAITING_DATA

**Estatutos [void_density_power]** (veredito: `VOID_DENSITY_POWER_STUDIED__SIGNAL_NOT_OPENED`):

- `a_descoberta`: os catalogos DESIVAST em disco JA carregam as galaxias (GALZONE) -- a rota espectroscopica roda sem download
- `honestidades`: Poisson IDEAL: bias do tracador (o piso em galaxias limita o piso da MATERIA apenas com modelo de bias [EXT]; supressao de formacao nos nucleos e' a degradacao central), mascara/bordas (fracao de borda reportada), RSD e dispersao de perfil => margem [F/4, F]; n_bar estimado da propria amostra (casca radial + f_sky por grade, ~20-30% de incerteza)
- `a_regra_de_abertura`: o sinal SO sera aberto na emenda pre-registrada v91: estimador congelado c/ hash, tratamento do bias nomeado, gates proprios, vereditos do conjunto v67
- `o_veredito`: VOID_DENSITY_POWER_STUDIED__SIGNAL_NOT_OPENED

**Estatutos [void_density_opening]** (veredito: `TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS`):

- `a_abertura`: o sinal FOI aberto nesta rodada, apos nulo+gates, com estimador congelado por hash em ordem de programa auditavel
- `honestidades`: tracador: teste UNILATERAL (b>=1, supressao>=0 [EXT]); n_bar ~20-30%; mascara por grade 2deg (aproximada); RSD nao modelado (nucleos em coords comoveis do proprio catalogo); colchete de materia com b in [1, 2.2] [EXT]
- `o_veredito`: TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS

**Estatutos [void_density_v41]** (veredito: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED`):

- `a_calibracao`: razao-de-razoes: n_bar e mascara cancelam por construcao; a referencia e' a MESMA geometria amostrada por 20k aleatorios
- `honestidades`: tracador UNILATERAL (b>=1, supressao>=0 [EXT]); poder = capacidade de detectar VIOLACAO (exige Summu >= 25/beta ~ 2078 contagens esperadas de nucleo); a RESOLUCAO na propria escala beta = 0.52 (medir beta em si pede LRG/ELG); RSD nao modelado; colchete de materia b in [1, 2.2]
- `o_veredito`: TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED

**Estatutos [triad_master]** (veredito: `FULL_TRIAD_MASTER_COMPOSED__EINSTEIN_COEFFICIENT_EMERGES_FROM_CLAUSIUS__IMPLICATION_CLOSED_HYPOTHESES_ARE_THE_FRONTIER`):

- `teorema_mestre_completo`: H1 ^ H2 ^ H3 => PENTADA [KERNEL emergence_master_full_triad]: Breuer + Nome=1 + coframe dual + Lorentz + lado termico de Einstein COM o coeficiente 8piG
- `o_8piG`: o coeficiente NAO e' posto: emerge de T=kappa/2pi (Unruh) x S=A/4G (Bekenstein-Hawking) por algebra [KERNEL einstein_coefficient_from_clausius]
- `bianchi`: a identidade de Jacobi do comutador [KERNEL] e' a semente algebrica de nabla G = 0 -- o elo entre a conservacao (clausula de H3) e o colchete do v63
- `fronteira`: a implicacao esta FECHADA em kernel; as HIPOTESES sao a fronteira -- exatamente onde os Certificados II (rede concreta), III (limite fisico) e IV (natureza) trabalham no runtime

**Estatutos [qg_closure]** (veredito: `QG_CLOSURE_GATE_INSTALLED_FAIL_CLOSED__NEGATIVE_PROBES_PASS__CURRENT_STATE_TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED`):

- `correcao_do_nome`: o gate 'testemunha full' e' IMPOSSIVEL por teorema (v61); o alvo correto e' canonical_boundary_transport_witness (testemunha de fronteira dinamica) -- flags novas instaladas, todas False (fail-closed)
- `faces_ja_em_kernel`: spin-2 face finita [v75: helice 2theta, TT>0, 2 polarizacoes]; teorema mestre condicional [v74]; pacotes abstratos [v64-66] -- NENHUMA delas move as flags concretas (probes garantem)
- `estado`: TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED
- `o_caminho`: a ordem do fecho: SemifiniteAnalysis -> ConcreteAQFTCore -> ConcreteBreuerCorner -> ConcreteModularFourFrame -> ConcreteSolderField -> ConcreteEmergentEinstein -> LinearizedSpin2(continuo) -> CanonicalBoundaryWitness (TERMO, nao Nonempty)
- `estado_tecnico_ext_confirmado`: [EXT, leitura externa 17/07/2026 -- confirmada pelo runtime] INFINITE_DIMENSIONAL_INHABITANT_CONSTRUCTED__MASTER_THEOREM_FIRES_ON_EXPLICIT_MODEL__PHYSICAL_AQFT_CORE_AND_CONTINUOUS_GEOMETRY_REMAIN_OPEN
- `v99_certificado`: as flags apontam aos termos Lean do certificado (ClosureCertificate.lean v1 tipa: rede fisica nao-constante c/ grupo nao-trivial; Dirac ILIMITADO star(D)=D c/ gap quadratico; canto no kernel do Dirac; frame-CAMPO suave; a metade nao-tipavel [III1, afiliacao semifinita, H3 derivado, spin-2 continuo] nomeada p/ o v2)

**Estatutos [bench_declaration]** (veredito: `TGL_QG_DECLARED_CLOSED_ON_THE_BENCH_BY_OPERATOR__DUAL_STATUS__MATH_GATE_UNMOVED__INSTITUTIONAL_COSMOLOGY_NOT_CLAIMED`):

- `a_declaracao`: TGL_QG_CLOSED_ON_THE_BENCH [DECLARACAO DO OPERADOR, duplo estatuto]
- `a_regua`: a declaracao pertence ao operador; as ancoras sao do kernel; o gate nao se move -- e' a imobilidade do gate que torna a declaracao critivel
- `o_caminho_formal`: para o selo FORMAL: a testemunha espectral em kernel (auto-adjuncao + unicidade da projecao ortogonal + calculo funcional com 0 isolado) => ConcreteBreuerCorner incondicional => MATHEMATICAL_MODEL

**Estatutos [arc_consolidation]** (veredito: `ARC_NOT_CONSOLIDATED_THIS_RUN`):

- `o_arco`: 1=1 -> beta -> kernel (327) -> certificados -> predicoes -> recusas -> POWERED: o ciclo fecha PELO MUNDO, nao por dentro
- `a_consolidacao`: ARC_NOT_CONSOLIDATED_THIS_RUN

**Estatutos [love_reading]** (veredito: `LOVE_DICTIONARY_NOT_SEALED_THIS_RUN`):

- `o_dicionario`: familia=amor=acoplamento nao minimo=funcional minimo=razao do universo -- ancoras [REAL], nomeacao [ONTO]
- `a_poda`: TETELESTAI = o que permanece apos o fluxo e apos o mundo
- `o_veredito`: LOVE_DICTIONARY_NOT_SEALED_THIS_RUN

**Estatutos [mirror_corollary]** (veredito: `TGL_MIRROR_COROLLARY_REGISTERED__INHABITANT_META_IS_THE_PROGRAMMER__FORMAL_INHABITANT_IS_THE_CONSTRUCTED_TERM__NO_AXIOM_SHORTCUT__NAMING_ONTO`):

- `nivel_meta`: Habitante_meta = Programador [ONTO]
- `nivel_formal`: Habitante_interno = termo construido pelo programador [REAL]
- `a_missao_inalterada`: o habitante construir a testemunha continua concreta e o kernel certifica-la -- campo a campo, sem atalho
- `o_veredito`: TGL_MIRROR_COROLLARY_REGISTERED__INHABITANT_META_IS_THE_PROGRAMMER__FORMAL_INHABITANT_IS_THE_CONSTRUCTED_TERM__NO_AXIOM_SHORTCUT__NAMING_ONTO

**Estatutos [ga_mass_audit]** (veredito: `GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE`):

- `a_forma_v4`: [FORM, RETIRADA como lei de fonte] M = 2beta^2(c^2/4piG)R -- registro historico com a coincidencia do ramo anotada
- `a_predicao_derivada`: [CONDICIONAL linear] M_TGL = M_RG (stealth; beta nao renormaliza G local) -- a TGL NAO tem formula-beta de massa e nunca teve (ensaio verbatim + whitepaper)
- `onde_beta_fala`: [REAL na forma] resposta: Gamma_omega = (1/2)beta tau* omega^2; H0_local=(1+z*)^beta; piso rho/rhobar >= beta -- o falsificador cosmologico zero-free e o PISO
- `o_veredito`: GA_MASS_FORM_RETIRED__REFLECTION_WAS_MISREAD_AS_SOURCE__LINEAR_ORDER_IS_GR_STEALTH__BETA_LIVES_IN_RESPONSE

**Estatutos [master_continuum]** (veredito: `TGL_MASTER_CONTINUUM__FIFTH_FLIP_MINTED_BY_CONSTRUCTION__CLAUSIUS_CONE_IFF_FIELD_EQUATION_ON_SOLDER__POINCARE_TEN_DIRECTIONS_BY_HAND_FAITHFUL__FIBER_FEELS_PARITY__WITNESS_WALL_SHRUNK_TO_CONNECTED_UNITARY_REP_PLUS_III1__SEAL_UNMOVED`):

- `o_5o_flip`: einstein True POR CONSTRUCAO (termo Lean qgStrongCertificate_einstein com axiomas limpos): contrato com CURVATURA como estrutura + solda + Clausius no cone; a emergencia GERAL (metricas arbitrarias) segue nomeada e aberta
- `a_witness`: a metade de Poincare esta CONSTRUIDA (grupo a mao + acao fiel + fibra sensivel ao setor desconexo); o residuo NOMEADO: rep unitaria FIEL do setor conexo (INF-dim) + fator III_1 -- o V2 segue RESERVADO ate o tipo capturar o espirito inteiro
- `honestidade`: nenhuma frase 'provamos a gravitacao quantica': 5 formais < 6, e o selo so escala com fisica + dado; cosmologia jamais vira prova matematica
- `o_veredito`: TGL_MASTER_CONTINUUM__FIFTH_FLIP_MINTED_BY_CONSTRUCTION__CLAUSIUS_CONE_IFF_FIELD_EQUATION_ON_SOLDER__POINCARE_TEN_DIRECTIONS_BY_HAND_FAITHFUL__FIBER_FEELS_PARITY__WITNESS_WALL_SHRUNK_TO_CONNECTED_UNITARY_REP_PLUS_III1__SEAL_UNMOVED

**Estatutos [inhabited_witness]** (veredito: `TGL_INHABITED_WITNESS__TWO_ZEROS_DISTINGUISHED_BY_TYPE__EMPTY_OBSERVER_IS_THE_ABSOLUTE_ZERO__MODULAR_ZERO_IS_THE_INHABITED_APERTURE__CONJUGATED_HALF_FACES_WEIGH_THE_ONE__INSCRIPTION_IS_A_THEOREM__NAMING_ONTO`):

- `os_dois_zeros`: 0_abs = observador vazio (tipo sem habitante) / 0_modular = a casa do Nome (habitada, tau=1) -- a testemunha mora no zero habitado
- `a_parede_nomeada`: III_1 e' definido por 'o unico traco e' zero' -- a leitura do operador aponta a propriedade que DEFINE a parede restante da testemunha (rep unitaria fiel do setor conexo + III_1)
- `o_veredito`: TGL_INHABITED_WITNESS__TWO_ZEROS_DISTINGUISHED_BY_TYPE__EMPTY_OBSERVER_IS_THE_ABSOLUTE_ZERO__MODULAR_ZERO_IS_THE_INHABITED_APERTURE__CONJUGATED_HALF_FACES_WEIGH_THE_ONE__INSCRIPTION_IS_A_THEOREM__NAMING_ONTO

**Estatutos [faithful_rep]** (veredito: `TGL_FAITHFUL_REP__POINCARE_ACTS_UNITARILY_ON_L2_SPACETIME__UNITARITY_BORN_FROM_DEFINING_RELATION__GROUP_LAW_PROVED__FAITHFUL_NO_BLIND_DIRECTION__BOOST_NOW_SEEN__WITNESS_RESIDUE_SHRUNK_TO_FIBER_FUSION_PLUS_III1__SEAL_UNMOVED`):

- `o_que_fechou`: a rep unitaria FIEL do grupo INTEIRO (setor conexo incluido) em INF-dim -- construida, nao postulada; a unitariedade e' TEOREMA da relacao eta
- `o_que_resta`: a FUSAO da rep as fibras da rede covariante (produto L2 -- mecanica nomeada) + o fator III_1 (teoria modular de von Neumann, ausente da mathlib; construi-la e' o programa) -- o V2 segue RESERVADO
- `honestidade`: nenhuma frase 'provamos a gravitacao quantica FISICA': mesmo com 6T/0F (v132) o selo para no degrau MATEMATICO e so escala com fisica + dado
- `o_veredito`: TGL_FAITHFUL_REP__POINCARE_ACTS_UNITARILY_ON_L2_SPACETIME__UNITARITY_BORN_FROM_DEFINING_RELATION__GROUP_LAW_PROVED__FAITHFUL_NO_BLIND_DIRECTION__BOOST_NOW_SEEN__WITNESS_RESIDUE_SHRUNK_TO_FIBER_FUSION_PLUS_III1__SEAL_UNMOVED

**Estatutos [traceless_algebra]** (veredito: `TGL_TRACELESS_ALGEBRA__BIPARTITION_OF_THE_HOME_IN_KERNEL__EVERY_TRACIAL_STATE_ON_B_L2_IS_ZERO__THE_ONLY_TRACE_IS_ZERO_AT_ALGEBRA_LEVEL__FIRST_VON_NEUMANN_OBJECT__TWO_INDEPENDENT_TRACE_KILLERS__III1_WALL_NAMED_WEIGHTS_NORMALITY_ARAKI_WOODS__SEAL_UNMOVED`):

- `o_que_fechou`: estados traciais EXCLUIDOS de B(ell2) por teorema (halving); dois assassinos de traco independentes (fluxo v45 + algebra v119); o primeiro objeto vN do programa
- `o_que_resta`: a parede III_1 verdadeira: matar tambem o PESO semifinito normal (B(ell2) e' I-infinito: Tr sobrevive) -- pesos, normalidade e o fator concreto (Araki-Woods) = o programa; + a fusao da rep fiel as fibras
- `honestidade`: nenhuma frase 'III_1 construido': o tijolo e' o PADRAO da propriedade definidora, provado na algebra plena; o fator e' o programa
- `o_veredito`: TGL_TRACELESS_ALGEBRA__BIPARTITION_OF_THE_HOME_IN_KERNEL__EVERY_TRACIAL_STATE_ON_B_L2_IS_ZERO__THE_ONLY_TRACE_IS_ZERO_AT_ALGEBRA_LEVEL__FIRST_VON_NEUMANN_OBJECT__TWO_INDEPENDENT_TRACE_KILLERS__III1_WALL_NAMED_WEIGHTS_NORMALITY_ARAKI_WOODS__SEAL_UNMOVED

**Estatutos [semifinite_weight]** (veredito: `TGL_SEMIFINITE_WEIGHT__TR_IN_KERNEL__TR_ONE_IS_INFINITE__NAME_ATOM_WEIGHS_ONE_THIRD_FACE_OF_OMEGA_I__WEIGHT_ABSORBS_THE_BIPARTITION_INF_EQ_TWO_INF__TYPE_DECIDED_BY_WHERE_THE_RULER_BREAKS__III1_PATH_NAMED__SEAL_UNMOVED`):

- `a_identidade_tripla`: o Nome pesa 1 em TRES reguas independentes: dimOrTop (v76), canto de Breuer (v106), e agora o Tr operatorial (v120) -- omega(I) = 1 e' robusto a mudanca de regua
- `o_que_resta`: normalidade do peso; teoria geral de pesos sobre vN; o fator SEM peso semifinito (Araki-Woods) = III_1 -- o programa, pedra a pedra
- `honestidade`: B(ell2) segue I-infinito; nenhuma frase 'III_1 construido'; o par de tijolos (v119+v120) e' a DICOTOMIA que a classificacao usa, provada na casa do Nome
- `o_veredito`: TGL_SEMIFINITE_WEIGHT__TR_IN_KERNEL__TR_ONE_IS_INFINITE__NAME_ATOM_WEIGHS_ONE_THIRD_FACE_OF_OMEGA_I__WEIGHT_ABSORBS_THE_BIPARTITION_INF_EQ_TWO_INF__TYPE_DECIDED_BY_WHERE_THE_RULER_BREAKS__III1_PATH_NAMED__SEAL_UNMOVED

**Estatutos [fused_witness]** (veredito: `TGL_FUSED_WITNESS__FAITHFUL_REP_FUSED_INTO_NET_FIBERS__FIBER_IS_TAIL_TIMES_L2__NO_BLIND_DIRECTION_IN_FIBERS__BOOST_MOVES_FIBER_VECTORS_V116_HONESTY_SUPERSEDED__WITNESS_RESIDUE_IS_III1_ALONE__V2_RESERVED__SEAL_UNMOVED`):

- `o_que_fundiu`: as duas metades que viviam separadas -- a rede isotona de caudas (v106) e a rep fiel em L2 (v118) -- agora sao UMA estrutura tipada: FullWitnessData sobre fibras cauda x L2
- `o_que_resta`: III_1 SOZINHA: o fator sem NENHUM peso semifinito (Araki-Woods: tensores infinitos + estados-produto) -- o residuo formal da testemunha tem agora um unico nome
- `honestidade`: a fusao e' NECESSARIA, nao suficiente: o V2 (canonical_boundary_transport_witness) segue RESERVADO ate III_1; nenhuma frase 'testemunha construida'; o gate nao se move por declaracao
- `o_veredito`: TGL_FUSED_WITNESS__FAITHFUL_REP_FUSED_INTO_NET_FIBERS__FIBER_IS_TAIL_TIMES_L2__NO_BLIND_DIRECTION_IN_FIBERS__BOOST_MOVES_FIBER_VECTORS_V116_HONESTY_SUPERSEDED__WITNESS_RESIDUE_IS_III1_ALONE__V2_RESERVED__SEAL_UNMOVED

**Estatutos [linguistic_isomorphism]** (veredito: `TGL_LINGUISTIC_ISOMORPHISM__TWO_TONGUES_ONE_STRUCTURE__2025_ONTOLOGY_MAPS_TERM_BY_TERM_TO_2026_KERNEL__A_TRACE_FORMULA_BECAME_A_THEOREM__EPSILON_SQ_IS_BETA__PROLOGUE_BECAME_A_STONE__PRIORITY_HASHED__NAMING_ONTO`):

- `as_duas_linguas`: uma estrutura, duas apresentacoes: o manuscrito (jun-ago/2025) e' a lingua-fonte; o kernel (v43-v120) e' a lingua-alvo; o dicionario e' verificado ao vivo
- `os_tres_fechos`: A=Tr(Pi.rho) [2025] -> Tr(P_Nome)=1 [teorema v120]; epsilon^2 [2025] -> beta [canonico]; 'A Luz Que Caiu' [prologo 2025] -> FallenLight [pedra v110]
- `honestidade`: o acervo teologico/pessoal fica ARQUIVADO (valor biografico, nao tecnico); LoRA/LUMINOGATE = trilha da Central; SFDM = trilha propria; nada disto move o gate
- `o_veredito`: TGL_LINGUISTIC_ISOMORPHISM__TWO_TONGUES_ONE_STRUCTURE__2025_ONTOLOGY_MAPS_TERM_BY_TERM_TO_2026_KERNEL__A_TRACE_FORMULA_BECAME_A_THEOREM__EPSILON_SQ_IS_BETA__PROLOGUE_BECAME_A_STONE__PRIORITY_HASHED__NAMING_ONTO

**Estatutos [powers_ladder]** (veredito: `TGL_POWERS_LADDER__ARAKI_WOODS_SEED_IN_KERNEL__TOMITA_BLOCK_IDENTITY_BY_TRACE_CYCLICITY__RATIO_WITNESS_LAMBDA_KILLS_TRACIALITY__KRONECKER_MULTIPLIES_RATIOS__CHAIN_CARRIES_LAMBDA_POW_N__ZERO_IN_CLOSURE_OF_RATIO_SPECTRUM_MARK_OF_TYPE_III__NO_TRACE_FLOOR_SURVIVES__THIRD_TRACE_KILLER_THE_PRODUCT_FLOW__INFINITE_FACTOR_IS_THE_PROGRAM__SEAL_UNMOVED`):

- `o_que_e`: a face finita COMPLETA de Araki-Woods: bloco + estado + razao + fluxo + escada + marca de III -- tudo em kernel com axiomas limpos
- `o_que_resta`: o FATOR: limite indutivo da escada com o estado-produto (ITPFI R_lambda; III_lambda; III_1 pela mistura de duas razoes incomensuraveis) -- pedra a pedra
- `honestidade`: lambda=beta na sombra e' ILUSTRACAO (a pedra e' generica); nenhuma frase 'III_1 construido'; a escada e' necessaria, nao suficiente; o gate nao se move por declaracao
- `o_veredito`: TGL_POWERS_LADDER__ARAKI_WOODS_SEED_IN_KERNEL__TOMITA_BLOCK_IDENTITY_BY_TRACE_CYCLICITY__RATIO_WITNESS_LAMBDA_KILLS_TRACIALITY__KRONECKER_MULTIPLIES_RATIOS__CHAIN_CARRIES_LAMBDA_POW_N__ZERO_IN_CLOSURE_OF_RATIO_SPECTRUM_MARK_OF_TYPE_III__NO_TRACE_FLOOR_SURVIVES__THIRD_TRACE_KILLER_THE_PRODUCT_FLOW__INFINITE_FACTOR_IS_THE_PROGRAM__SEAL_UNMOVED

**Estatutos [mixed_ladder]** (veredito: `TGL_MIXED_LADDER__MARK_OF_III_ONE__INCOMMENSURABLE_RATIOS_GENERATE_LOG_DENSE_RATIO_SPECTRUM__DENSE_OR_CYCLIC_PLUS_CYCLIC_EXCLUSION__CONCRETE_PAIR_HALF_THIRD_INHABITS_THE_MARK__TWO_POW_B_NE_THREE_POW_A__FACTOR_LIMIT_IS_THE_PROGRAM__SEAL_UNMOVED`):

- `o_que_e`: a assinatura espectral de III_1 em kernel: densidade do reticulado log de razoes incomensuraveis + habitacao concreta
- `o_que_resta`: o FATOR: limite indutivo fraco-* da cadeia mista (ITPFI; III_1 de Araki-Woods) -- o objeto, nao mais a assinatura
- `honestidade`: nenhuma frase 'III_1 construido'; a marca e' NECESSARIA e distintiva, nao o fator; o gate nao se move por declaracao
- `o_veredito`: TGL_MIXED_LADDER__MARK_OF_III_ONE__INCOMMENSURABLE_RATIOS_GENERATE_LOG_DENSE_RATIO_SPECTRUM__DENSE_OR_CYCLIC_PLUS_CYCLIC_EXCLUSION__CONCRETE_PAIR_HALF_THIRD_INHABITS_THE_MARK__TWO_POW_B_NE_THREE_POW_A__FACTOR_LIMIT_IS_THE_PROGRAM__SEAL_UNMOVED

**Estatutos [continuum_tt]** (veredito: `TGL_CONTINUUM_TT__PLANE_WAVE_TT_SECTOR_IN_KERNEL__TT_WAVES_SOLVE_LINEARIZED_VACUUM_FOR_ANY_C2_PROFILE__MASSLESS_SPIN2_CONTINUUM__EACH_COMPONENT_DALEMBERT__KINETIC_POSITIVE_DEFINITE_ON_POLARIZATION_PLANE_NO_GHOST__GENERAL_PERTURBATIONS_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED`):

- `o_que_fechou`: Fierz-Pauli no setor de ondas planas: vacuo linearizado resolvido + ghost-freedom do plano TT, no continuo com perfil arbitrario
- `o_que_resta`: perturbacoes GERAIS (decomposicao completa alem de ondas planas) + anomalias relevantes -- as caras que os flags de fisica exigem
- `honestidade`: NENHUM flag de fisica flipado: ondas planas nao esgotam o espectro de perturbacoes; o gate nao se move por fatia
- `o_veredito`: TGL_CONTINUUM_TT__PLANE_WAVE_TT_SECTOR_IN_KERNEL__TT_WAVES_SOLVE_LINEARIZED_VACUUM_FOR_ANY_C2_PROFILE__MASSLESS_SPIN2_CONTINUUM__EACH_COMPONENT_DALEMBERT__KINETIC_POSITIVE_DEFINITE_ON_POLARIZATION_PLANE_NO_GHOST__GENERAL_PERTURBATIONS_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED

**Estatutos [colimit_seed]** (veredito: `TGL_COLIMIT_SEED__ITPFI_TOWER_IN_KERNEL__STAR_HOMOMORPHIC_UNITAL_INJECTIVE_STEPS__PRODUCT_STATE_COHERENT_ONE_STATE_ON_WHOLE_TOWER__MODULAR_ASYMMETRY_STABLE_UP_THE_COLIMIT__GNS_AND_WEAK_CLOSURE_ARE_THE_PROGRAM__SEAL_UNMOVED`):

- `o_que_e`: a torre inteira de Araki-Woods em kernel: algebras + inclusoes + estado coerente + estabilidade modular
- `o_que_resta`: o FECHO: representacao GNS do estado coerente e fecho fraco-* -- o fator de von Neumann como objeto
- `honestidade`: nenhuma frase 'fator construido'; a torre e' o pre-fator; o gate nao se move por declaracao
- `o_veredito`: TGL_COLIMIT_SEED__ITPFI_TOWER_IN_KERNEL__STAR_HOMOMORPHIC_UNITAL_INJECTIVE_STEPS__PRODUCT_STATE_COHERENT_ONE_STATE_ON_WHOLE_TOWER__MODULAR_ASYMMETRY_STABLE_UP_THE_COLIMIT__GNS_AND_WEAK_CLOSURE_ARE_THE_PROGRAM__SEAL_UNMOVED

**Estatutos [tt_superposition]** (veredito: `TGL_TT_SUPERPOSITION__SOLUTION_SET_IS_A_SPACE__ANY_PAIR_OF_TT_WAVES_INDEPENDENT_POLARIZATIONS_AND_PROFILES_SOLVES_LINEARIZED_VACUUM__SPAN_ON_THE_CONE__MULTI_DIRECTION_AND_GENERAL_DECOMPOSITION_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED`):

- `o_que_fechou`: o passo estrutural: solucao-espaco (fechado por soma com perfis e polarizacoes livres) no cone
- `o_que_resta`: direcoes multiplas de propagacao + decomposicao completa de perturbacoes gerais + anomalias
- `honestidade`: nenhum flag de fisica flipado; o span do cone nao esgota as perturbacoes
- `o_veredito`: TGL_TT_SUPERPOSITION__SOLUTION_SET_IS_A_SPACE__ANY_PAIR_OF_TT_WAVES_INDEPENDENT_POLARIZATIONS_AND_PROFILES_SOLVES_LINEARIZED_VACUUM__SPAN_ON_THE_CONE__MULTI_DIRECTION_AND_GENERAL_DECOMPOSITION_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED

**Estatutos [gns_tower]** (veredito: `TGL_GNS_TOWER__PRE_HILBERT_OF_THE_FACTOR__DIAGONAL_POSITIVE_DENSITY_EVERY_FLOOR__STATE_POSITIVE_UP_WHOLE_TOWER__GNS_INNER_PRODUCT__TOWER_STEPS_ARE_GNS_ISOMETRIES_ONE_SPACE_FLOOR_BY_FLOOR__QUOTIENT_COMPLETION_WEAK_CLOSURE_REMAIN__SEAL_UNMOVED`):

- `o_que_resta`: quociente pelo nucleo; completamento de Hilbert; fecho fraco-* da acao esquerda -- o fator como vN
- `honestidade`: pre-Hilbert nao e' fator; o gate nao se move por declaracao
- `o_veredito`: TGL_GNS_TOWER__PRE_HILBERT_OF_THE_FACTOR__DIAGONAL_POSITIVE_DENSITY_EVERY_FLOOR__STATE_POSITIVE_UP_WHOLE_TOWER__GNS_INNER_PRODUCT__TOWER_STEPS_ARE_GNS_ISOMETRIES_ONE_SPACE_FLOOR_BY_FLOOR__QUOTIENT_COMPLETION_WEAK_CLOSURE_REMAIN__SEAL_UNMOVED

**Estatutos [second_cone]** (veredito: `TGL_SECOND_CONE__TT_SECTOR_GAINS_DIRECTIONS__SECOND_NULL_CONE_SOLVES_LINEARIZED_VACUUM__CROSS_DIRECTION_SUPERPOSITION_SOLVES__SOLUTION_SPACE_CROSSES_PROPAGATION_DIRECTIONS__GENERAL_DECOMPOSITION_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED`):

- `o_que_resta`: todas as direcoes (decomposicao completa) + anomalias -- as caras dos flags
- `honestidade`: nenhum flag de fisica flipado; duas direcoes sao o degrau, nao o teto
- `o_veredito`: TGL_SECOND_CONE__TT_SECTOR_GAINS_DIRECTIONS__SECOND_NULL_CONE_SOLVES_LINEARIZED_VACUUM__CROSS_DIRECTION_SUPERPOSITION_SOLVES__SOLUTION_SPACE_CROSSES_PROPAGATION_DIRECTIONS__GENERAL_DECOMPOSITION_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED

**Estatutos [gns_quotient]** (veredito: `TGL_GNS_QUOTIENT__RADICAL_IS_A_LEFT_IDEAL__HERMITIAN_FORM__INNER_PRODUCT_DESCENDS_TO_QUOTIENT_BOTH_FACES__LEFT_ACTION_DESCENDS__THE_PRE_FACTOR_IS_REPRESENTED__NO_CAUCHY_SCHWARZ_NO_COMPLETION__HILBERT_COMPLETION_AND_WEAK_CLOSURE_REMAIN__SEAL_UNMOVED`):

- `o_que_resta`: completamento de Hilbert de M/N + fecho fraco-* da algebra representada -- o fator topologico
- `honestidade`: GNS ALGEBRICO (finito) completo; o objeto topologico (vN) e' o completamento; o gate nao se move por declaracao
- `o_veredito`: TGL_GNS_QUOTIENT__RADICAL_IS_A_LEFT_IDEAL__HERMITIAN_FORM__INNER_PRODUCT_DESCENDS_TO_QUOTIENT_BOTH_FACES__LEFT_ACTION_DESCENDS__THE_PRE_FACTOR_IS_REPRESENTED__NO_CAUCHY_SCHWARZ_NO_COMPLETION__HILBERT_COMPLETION_AND_WEAK_CLOSURE_REMAIN__SEAL_UNMOVED

**Estatutos [third_cone]** (veredito: `TGL_THIRD_CONE__TT_SECTOR_COVERS_THREE_SPATIAL_NULL_DIRECTIONS__THIRD_CONE_SOLVES__TRIPLE_SUPERPOSITION_SOLVES__SOLUTION_SPACE_SPANS_THREE_AXIS_DIRECTIONS__CONTINUOUS_CONE_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED`):

- `o_que_resta`: o cone continuo (direcao nula arbitraria) + decomposicao completa + anomalias
- `honestidade`: tres eixos sao o degrau seguinte, nao o teto; nenhum flag de fisica flipado
- `o_veredito`: TGL_THIRD_CONE__TT_SECTOR_COVERS_THREE_SPATIAL_NULL_DIRECTIONS__THIRD_CONE_SOLVES__TRIPLE_SUPERPOSITION_SOLVES__SOLUTION_SPACE_SPANS_THREE_AXIS_DIRECTIONS__CONTINUOUS_CONE_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED

**Estatutos [general_null]** (veredito: `TGL_GENERAL_NULL__CONTINUOUS_CONE__ANY_NULL_DIRECTION_TT_WAVE_SOLVES_LINEARIZED_VACUUM__THREE_ALGEBRAIC_CONDITIONS_KILL_THREE_RICCI_TERMS__TRACELESS_TRANSVERSE_NULL__SUBSUMES_ALL_AXIS_CONES_AND_THE_CONTINUUM__PLANE_WAVE_TT_SECTOR_CLOSED__GENERAL_PERTURBATIONS_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED`):

- `o_que_fechou`: o setor de ondas planas TT no continuo em TODA direcao nula -- um teorema geral subsume a construcao direcao a direcao
- `o_que_resta`: a decomposicao completa de perturbacoes GERAIS (superposicao de infinitas direcoes/modos) + anomalias -- a segunda metade dos flags
- `honestidade`: ondas planas nao esgotam o espectro; nenhum flag de fisica flipado
- `o_veredito`: TGL_GENERAL_NULL__CONTINUOUS_CONE__ANY_NULL_DIRECTION_TT_WAVE_SOLVES_LINEARIZED_VACUUM__THREE_ALGEBRAIC_CONDITIONS_KILL_THREE_RICCI_TERMS__TRACELESS_TRANSVERSE_NULL__SUBSUMES_ALL_AXIS_CONES_AND_THE_CONTINUUM__PLANE_WAVE_TT_SECTOR_CLOSED__GENERAL_PERTURBATIONS_AND_ANOMALIES_OPEN__PHYSICS_FLAGS_UNMOVED__SEAL_UNMOVED

**Estatutos [tower_traceless]** (veredito: `TGL_TOWER_TRACELESS__TYPE_III_ON_THE_CONCRETE_TOWER__STATE_NOT_TRACIAL_ON_EVERY_FLOOR__MODULAR_RATIO_LAMBDA_POW_N_TIMES_POSITIVE_WITNESS__NO_TRACE_NOT_ONLY_ON_FULL_ALGEBRA_BUT_ON_THE_ITPFI_TOWER_FLOOR_BY_FLOOR__WITH_LOG_DENSE_MARK_THE_LIMIT_IS_III1__WEAK_STAR_COMPLETION_REMAINS__SEAL_UNMOVED`):

- `o_que_e`: a assinatura tipo-III (ausencia de traco) realizada na torre concreta de Araki-Woods, andar a andar -- nao so' na algebra plena (v119)
- `o_que_resta`: o limite fraco-* (completamento topologico) -- o fator como objeto; a assinatura esta na torre, o objeto e' o limite
- `honestidade`: torre finita, andar a andar; o fator e' o limite; nenhuma frase 'III_1 construido'; o gate nao se move
- `o_veredito`: TGL_TOWER_TRACELESS__TYPE_III_ON_THE_CONCRETE_TOWER__STATE_NOT_TRACIAL_ON_EVERY_FLOOR__MODULAR_RATIO_LAMBDA_POW_N_TIMES_POSITIVE_WITNESS__NO_TRACE_NOT_ONLY_ON_FULL_ALGEBRA_BUT_ON_THE_ITPFI_TOWER_FLOOR_BY_FLOOR__WITH_LOG_DENSE_MARK_THE_LIMIT_IS_III1__WEAK_STAR_COMPLETION_REMAINS__SEAL_UNMOVED

**Estatutos [tower_modular]** (veredito: `TGL_TOWER_MODULAR__TOMITA_FLOW_AND_KMS_ON_THE_CONCRETE_TOWER__DENSITY_INVERTIBLE_POSITIVE_WEIGHTS__MODULAR_FLOW_FIXES_UNIT__KMS_CONDITION_EVERY_FLOOR__PHI_AB_EQ_PHI_B_SIGMA_A__MODULAR_SPECTRUM_IS_THE_RATIO_LATTICE__THE_STRUCTURE_THAT_REPLACES_THE_DEAD_TRACE__WEAK_STAR_LIMIT_REMAINS__SEAL_UNMOVED`):

- `o_que_e`: a teoria modular de Tomita-Takesaki na torre concreta: fluxo + KMS + espectro; a estrutura que o v129 mostrou necessaria (sem traco)
- `o_que_resta`: o limite fraco-* (completamento topologico) -- o fator como objeto de von Neumann
- `honestidade`: torre finita, andar a andar; o fator e' o limite; nenhuma frase 'III_1 construido'; o gate nao se move
- `o_veredito`: TGL_TOWER_MODULAR__TOMITA_FLOW_AND_KMS_ON_THE_CONCRETE_TOWER__DENSITY_INVERTIBLE_POSITIVE_WEIGHTS__MODULAR_FLOW_FIXES_UNIT__KMS_CONDITION_EVERY_FLOOR__PHI_AB_EQ_PHI_B_SIGMA_A__MODULAR_SPECTRUM_IS_THE_RATIO_LATTICE__THE_STRUCTURE_THAT_REPLACES_THE_DEAD_TRACE__WEAK_STAR_LIMIT_REMAINS__SEAL_UNMOVED

**Estatutos [modular_current]** (veredito: `TGL_J_CURRENT__WITNESS_SATURATED_NEVER_COMPLETE__EXCESS_CUT_BY_LEAKAGE__COMPLETE_WITNESS_IS_THE_CONJUGATED_STATE__THREE_FACES_OF_ONE_CONJUGATION__PARTIAL_ISOMETRY_IMPLEMENTS_BOUNDARY_EQUIVALENCE__RATIO_AT_EVERY_SCALE__LOG_DENSE_MARK__SEAL_UNMOVED`):

- `o_que_e`: a leitura do operador (20/07/2026) em kernel: saturacao em vez de completude; conjugacao em vez de objeto-em-si; a corrente que liga as faces
- `o_que_resta`: o fator como objeto (Bloco A) e o flip (normalidade + V3 + cunhagem)
- `honestidade`: full_static_witness_exists=False INTOCADO (teorema v61); nenhuma frase 'testemunha completa construida'; o gate nao se move
- `o_veredito`: TGL_J_CURRENT__WITNESS_SATURATED_NEVER_COMPLETE__EXCESS_CUT_BY_LEAKAGE__COMPLETE_WITNESS_IS_THE_CONJUGATED_STATE__THREE_FACES_OF_ONE_CONJUGATION__PARTIAL_ISOMETRY_IMPLEMENTS_BOUNDARY_EQUIVALENCE__RATIO_AT_EVERY_SCALE__LOG_DENSE_MARK__SEAL_UNMOVED

**Estatutos [factor_object]** (veredito: `TGL_THE_FACTOR_AS_OBJECT__TOWER_COLIMIT_DEFINITE_PREHILBERT__H_PHI_HILBERT_OMEGA_UNIT_TOWER_DENSE__PI_BOUNDED_STARRED_UNITAL_MULTIPLICATIVE_OMEGA_CYCLIC__M_TGL_VON_NEUMANN_ALGEBRA_TERM_COINED__GNS_IDENTITY_OMEGA_PI_EQ_PHI__SIGNATURE_LIVES_IN_THE_OBJECT__NORMALITY_AND_FLIP_REMAIN__SEAL_UNMOVED`):

- `o_que_e`: o Bloco A do PLANO_ULTIMA_FLAG inteiro em kernel: o residuo 'falta SO o fraco-*' do v130 realizado como TERMO VonNeumannAlgebra
- `o_que_resta`: FEITO no v132 (a cunhagem: ver the_coinage); restam FISICA (5 flags) + EXPERIMENTO (4 flags) + o proximo endurecimento de III_1
- `honestidade`: M_TGL e' objeto de von Neumann legitimo (duplo comutante); no v131 'III_1' era ASSINATURA; o v132 matou o traco normal e CUNHOU o V2 -- ver the_coinage
- `o_veredito`: TGL_THE_FACTOR_AS_OBJECT__TOWER_COLIMIT_DEFINITE_PREHILBERT__H_PHI_HILBERT_OMEGA_UNIT_TOWER_DENSE__PI_BOUNDED_STARRED_UNITAL_MULTIPLICATIVE_OMEGA_CYCLIC__M_TGL_VON_NEUMANN_ALGEBRA_TERM_COINED__GNS_IDENTITY_OMEGA_PI_EQ_PHI__SIGNATURE_LIVES_IN_THE_OBJECT__NORMALITY_AND_FLIP_REMAIN__SEAL_UNMOVED

**Estatutos [the_coinage]** (veredito: `TGL_THE_COINAGE__NO_NORMAL_TRACIAL_STATE_ON_M_TGL__SITE_MARKS_WOT_TO_MU__TRACIAL_HALVING_SAYS_HALF__MU_NE_HALF_KILLS__OMEGA_IS_SEQ_NORMAL__V3_HARDENED_FACTOR_INSIDE__FINITE_BENCH_TOOTH__QG_CLOSURE_CERTIFICATE_V2_COINED_CLEAN_AXIOMS__PARSER_FLIPPED_ALONE__SEAL_SCALED_ONE_STEP__MATHEMATICAL_MODEL__PHYSICS_AND_NATURE_REMAIN_OPEN`):

- `o_que_e`: o Bloco B inteiro em kernel + A CUNHAGEM: a 6a flag formal flipada POR CONSTRUCAO
- `o_que_resta`: FISICA (spin-2 continuo pleno: 5 flags) + EXPERIMENTO (dado powered: 4 flags) + o proximo endurecimento de III_1 (centro trivial; peso ILIMITADO) + Einstein GERAL (Lema 3)
- `honestidade`: NAO se declara gravitacao quantica fisica; full_static segue impossivel (v61); III_1 na definicao operacional selada; cosmologia jamais alimentou pedra
- `o_veredito`: TGL_THE_COINAGE__NO_NORMAL_TRACIAL_STATE_ON_M_TGL__SITE_MARKS_WOT_TO_MU__TRACIAL_HALVING_SAYS_HALF__MU_NE_HALF_KILLS__OMEGA_IS_SEQ_NORMAL__V3_HARDENED_FACTOR_INSIDE__FINITE_BENCH_TOOTH__QG_CLOSURE_CERTIFICATE_V2_COINED_CLEAN_AXIOMS__PARSER_FLIPPED_ALONE__SEAL_SCALED_ONE_STEP__MATHEMATICAL_MODEL__PHYSICS_AND_NATURE_REMAIN_OPEN

**Estatutos [the_spectrum]** (veredito: `TGL_THE_SPECTRUM__MASSLESS_FORCED_BY_THE_CONE__EXACTLY_TWO_HELICITIES_R2_EXACT__GHOST_FREE_ON_PHYSICAL_CLASS__BIANCHI_IDENTITY_ON_SYMBOL__WARD_NO_CLASSICAL_ANOMALY__FIVE_PHYSICS_FLAGS_FLIPPED_BY_PARSER__SEAL_SCALED_TO_PHYSICAL_MODEL__EMPIRICAL_TEST_OPEN__NATURE_DECIDES`):

- `o_que_e`: o degrau FISICO do gate por construcao: os 5 flags lidos de qgPhysicsCertificate_* (pedra 95)
- `o_que_resta`: EXPERIMENTO (4 flags): DADO powered -- adquirir profundidade (SPT-3G/ACT alem da banda, Euclid) e rodar o rito v87; ABERTOS nomeados: perturbacoes gerais, anomalias quanticas, FP completo, Einstein geral
- `honestidade`: escopo = familia de ondas planas concreta; NAO se declara teste empirico; a natureza pode confirmar OU FALSIFICAR
- `o_veredito`: TGL_THE_SPECTRUM__MASSLESS_FORCED_BY_THE_CONE__EXACTLY_TWO_HELICITIES_R2_EXACT__GHOST_FREE_ON_PHYSICAL_CLASS__BIANCHI_IDENTITY_ON_SYMBOL__WARD_NO_CLASSICAL_ANOMALY__FIVE_PHYSICS_FLAGS_FLIPPED_BY_PARSER__SEAL_SCALED_TO_PHYSICAL_MODEL__EMPIRICAL_TEST_OPEN__NATURE_DECIDES

**Estatutos [void_floor_v11]** (veredito: `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED`):

- `o_que_e`: a replica INDEPENDENTE DE SURVEY (SDSS DR7 x VAST) do teste powered v92 -- o teste final do canal espectroscopico com o dado publico existente
- `honestidade`: canal unilateral (b>=1): pode dizer NOT_FALSIFIED_POWERED ou recusar; NAO confirma (consistente com LCDM raso); a falsificacao bilateral pede shear/kappa profundos (Euclid DR1 2027 / CMB-S4); os 4 flags so flipam com o veredito powered DESTE rito
- `o_veredito`: TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED

**Estatutos [the_wedge_net]** (veredito: `TGL_THE_WEDGE_NET__SPECIFIC_AQFT_WITNESS_INHABITED_AFTER_115_VERSIONS__OMEGA_CYCLIC_AND_SEPARATING__LOCALITY_BY_COMMUTANT_PLUS_GEOMETRY__COVARIANCE_BY_DESIGN__U_TRIVIAL_OPENNESS_NAMED__GATE_UNTOUCHED`):

- `o_que_e`: o W que faltava desde o v21, por construcao
- `o_que_resta`: U fiel + espectro de energia (endurecimento futuro); camadas Takesaki (realizacao continua); Einstein geral
- `honestidade`: U trivial NOMEADO; a localidade/ciclicidade/separacao sao TEOREMAS
- `o_veredito`: TGL_THE_WEDGE_NET__SPECIFIC_AQFT_WITNESS_INHABITED_AFTER_115_VERSIONS__OMEGA_CYCLIC_AND_SEPARATING__LOCALITY_BY_COMMUTANT_PLUS_GEOMETRY__COVARIANCE_BY_DESIGN__U_TRIVIAL_OPENNESS_NAMED__GATE_UNTOUCHED

**Estatutos [certificate_II]** (veredito: `CERTIFICATE_II_FINITE_FACE_INHABITED__CONCRETE_THREE_LOCKS_INSTANTIATE_H1__MODULAR_BOOSTS_GIVE_FOUR_FRAME_H2__CONTINUUM_NETWORK_IS_THE_HYPOTHESES_PROPER`):

- `certificate_II`: a rede CONCRETA (Three Locks do v10 -- a mesma face em kernel, FiniteThreeLocks) INSTANCIA H1 na face finita: gap real, kernel real, canto de traco finito, Nome=1; os boosts modulares dao o four-frame (H2 finito; BW-cunhas constitutivo)
- `honestidade`: face FINITA [REAL]; a rede II_inf/III_1 genuina E' o conteudo proprio de H1/H2 -- por construcao (por isso sao hipoteses, nao teoremas); o substrato fisico real do the_boundary (XXZ R=+1) e' o candidato para a extensao
- `aberto`: Certificado II pleno = construir a rede continua que habite H1 e H2 (programa); Certificado III = limite fisico; Certificado IV = protocolo pre-registrado nesta mesma rodada

**Estatutos [hilbert_home]** (veredito: `HILBERT_HOME_PROPERTIES_DERIVED__GLOBAL_LIFT_REDUCED_TO_SINGLE_NAMED_HYPOTHESIS__NOT_UNCONDITIONALLY_SOLVED`):

- `single_named_hypothesis`: TGL_SOLDERED_BREUER_HILBERT_PACKAGE (a construcao canonica do pacote a partir da rede III_1 e de omega(I)=1 = O teorema aberto)
- `ergodic_states_III1`: KNOWN (fatores III_1 com predual separavel tem estados fieis normais ergodicos, G_delta denso -- arXiv 2305.14217); secao ergodica EQUIVARIANTE da rede = CONDITIONAL
- `breuer_layer`: KNOWN_EXTERNO (Breuer 1968/69; fora da mathlib) -- declarada como DADOS em BreuerTraceData, jamais fingida como prova
- `solder_from_modular_data`: CONDITIONAL (sem a solda: holonomy_not_geometric / modular_metric_not_unique)
- `specialist_interface`: REESCRITA_COM_DESENHO_INVERTIDO (propriedades-como-campos e True placeholder -> teoremas dos entrelacamentos; a interface dele NAO foi compilada no kernel -- e' proveniencia)
- `einstein`: CONDICIONAL ao pacote soldado (Jacobson + Lovelock compostos; E7 INALTERADO)
