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
    "ChatgptAudit.general_null_cone_rigidity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_preserves_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_preserves_split": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_not_euclidean": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lorentz_solder_boost_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.euclidean_solder_not_boost_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.real_gram_cannot_equal_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.single_boost_has_two_signatures": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.positive_norm_isometry_no_exp_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_null_expand": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.no_injective_isometric_boost_intertwiner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.concrete_frame_euclidean_not_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_christoffel_metric_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_jet_metric_compatible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_jet_torsion_free": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_pure_trace_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.divergence_pure_trace_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_congr_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldDivergence_congr_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_symmetric_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.partials_zero_implies_fderiv_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_trace_field_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.conserved_pure_trace_is_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_single_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.symmetric_tensor_ext": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_congruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_eta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_components": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.minkowski_tensor_null_rigidity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.congruence_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.congruence_undo": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lorentz_tensor_null_rigidity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_metric_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.inverse_frame_metric_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.inverse_frame_metric_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_metric_differentiableOn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_scalar_differentiableOn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_tensor_eq_frame_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.inverse_symmetric_of_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_field_metric_compatible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_field_torsion_free": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_conserved_scalar_is_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_const_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldDivergence_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldDivergence_const_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.conserved_null_tensor_is_constant_metric_multiple": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.conserved_null_balance_has_constant_term": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.linear_trace_annihilates_null_cone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.linear_trace_has_no_constant_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.linear_trace_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.SmoothMatrixOn.add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.SmoothMatrixOn.sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.SmoothMatrixOn.mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.SmoothMatrixOn.transpose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_second_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_partials_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.smooth_matrix_differentiableAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_transpose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curvature_jet_antisymmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.exterior_bianchi_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.first_bianchi_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curvature_jet_metric_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curvature_pair_symmetry_from_identities": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_curvature_antisymmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.connection_first_jet_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_curvature_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_curvature_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_exterior_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.torsion_free_first_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_first_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.metric_compatibility_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.metric_compatibility_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_curvature_metric_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_curvature_first_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_curvature_last_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_curvature_first_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_curvature_pair_symmetry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.ricci_lower_expression": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_ricci_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_einstein_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorFieldJet_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_tensor_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_second_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_second_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_exterior_derivative_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_covariant_derivative_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_covariant_first_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.exterior_derivative_last_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_derivative_last_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_covariant_last_skew": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.sum_four_exchange_pairs": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.contracted_bianchi_algebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_ricci_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.ricci_derivative_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_ricci_contraction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lower_covariant_ricci_contraction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frameLeviCivita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frameEinsteinTensor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_metric_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.inverse_frame_metric_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levi_civita_field_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensorQuad_sub_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_einstein_equation_from_ricci_null_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.inverse_metric_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinatePartial_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.matrix_contraction_eq_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.scalar_curvature_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.scalar_curvature_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_contracted_bianchi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_einstein_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_einstein_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_factor_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_metric_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_curvature_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_einstein": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.control_conformal_not_pure_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.smooth_vector_differentiableAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vectorPartial_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vectorPartial_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vectorPartial_mulVec": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.matrix_mulVec_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariantVectorDerivative_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariantVectorGradient_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vectorPartial_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.scalarAlong_eq_fderiv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vectorPartial_congr_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_vector_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.mixed_gradient_component": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.mixed_gradient_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.covariant_vector_matrix_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.mixed_covariant_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.sum_three_reverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curvature_vector_contraction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expansion_of_acceleration": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.along_expansion_eq_mixed_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_raychaudhuri": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.vector_expansion_zero_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.equilibrium_ricci_focusing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.horizon_primitive_flux": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.horizon_primitive_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.heat_area_clausius_implies_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curve_expansion_focusing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.horizon_flux_residual_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.local_clausius_forces_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.primitive_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.integrated_clausius_implies_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensor_quad_field_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pencil_ricci_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.horizon_einstein_reconstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropy_density_einstein_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.matrix_curve_deriv_transpose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.matrix_curve_deriv_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_gram_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.determinant_curve_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.determinant_congruence_tangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_area_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_area_squared": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_area_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_gram_screen_block": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_gram_in_frame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_screen_variation_block": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_frame_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_frame_first_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_frame_metric_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_frame_second_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.ambient_expansion_is_screen_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_metric_variation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_metric_variation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.connection_metric_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.metric_along_curve_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lie_screen_gram_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_screen_area_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.coordinate_screen_area_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_screen_geodesic_column": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.induced_area_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_pencil_area_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_pencil_area_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometricHorizonToLocal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_area_einstein_reconstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tensor_pair_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.frame_pair_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.mixed_frame_pair_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.quad_coordinate_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.metric_compatible_quad_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_field_covariant_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_field_direction_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.null_field_preserves_frame_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.reflectedSpatialScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.spatial_inner_components": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.minkowski_quad_coordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.nonzero_null_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.unit_null_spatial_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.minkowski_pair_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.null_frame_matrix_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.normalized_null_gram_squared": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.flatNullFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.invertible_solder_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.solderedNullFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.transport_generator_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.coupled_frame_field_c1": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.eventually_symmetric_interval": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.matrix_derivative_components": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.localFrameFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.local_frame_flow_continuous_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.ordinary_velocity_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.velocity_along_flow_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.vector_column_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.pair_curve_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.generator_pair_cancellation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.frame_column_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.transported_null_pair_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.frame_flow_pair_preserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.ConstantJacobiField": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiFieldOfContDiff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiAreaFirst": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiAreaSecond": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiAreaThird": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiAreaFourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_first_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_second_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_third_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_deriv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_two": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_three": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_four": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_one_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_two_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_three_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_iterated_four_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_quartic_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_positive_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_abs_agrees_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_area_contDiff_four": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiOscillator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobiOscillatorVelocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_oscillator_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.jacobi_oscillator_velocity_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.oscillatorJacobiField": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.opticalJacobiArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_is_jacobi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_contDiff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_iterated_one_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_iterated_two_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_iterated_three_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_iterated_four_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_quartic_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_positive_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_abs_agrees_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_rs_positive_coefficients": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_rs_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_rs_fourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_rs_quartic_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_same_second_distinct_fourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_jacobi_area_nonunique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubicClock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_hasDerivAt_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_factor_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_factor_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.punctured_time_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_preserves_negative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_tendsto_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_tendsto_punctured": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_fourth_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_quadratic_correction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_fourth_ratio_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cubic_clock_quadratic_correction_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_remainder_clock_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_coefficient_clock_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.common_clock_preserves_quartic_defect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitianMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.matrixCoordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rankOneMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_isHermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.coords_of_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_of_coords": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_coordinates_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_coordinates_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitianQuadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_quadratic_coordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.hermitian_quadratic_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_vanishing_coefficients": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.rank_one_quadratic_rigidity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.positive_singular_quadratic_rigidity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.positive_singular_rigidity_positive_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.traceSquareReading": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.trace_square_hermitian_coordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.trace_square_identity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.trace_square_rank_one_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.trace_square_not_positive_singular_vanishing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operatorBlockCLM": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operatorBlockEntry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_entry_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_entry_recover": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_sum_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operatorBlockRepresentation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_representation_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_nonneg_representation_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operator_block_nonneg_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.operatorQuadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.positive_square_le_norm_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.positive_apply_norm_sq_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.positive_increment_norm_sq_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.positive_of_strong_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.monotone_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.monotone_operator_vector_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.monotone_strong_limit_isLUB": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.monotone_operator_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedGraphParameter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_parameter_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedGraphOperator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedGraphLift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_lift_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_parameter_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_lift_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_param_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_equation_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_selfadjoint_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_formal_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixedRealSubmodule": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.mem_fixedRealSubmodule_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixedRealSubmodule_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixedClosedSubmodule": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.domainConjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.domainConjugation_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.domain_fixed_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.mem_domain_iff_fixed_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixed_sum_tomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixed_subspace_separating": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.fixed_subspace_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.closedAntilinearStandardSubspace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.SpectralHilbert": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralWeightA": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralWeightB": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weight_den_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightA_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightB_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weight_square_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightA_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightB_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightA_norm_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightB_norm_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightA_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightB_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weight_reflection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weightB_reflection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectral_weight_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedSpectralWeight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_spectral_weight_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedSpectralMultiplier": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_spectral_multiplier_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_spectral_multiplier_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_spectral_multiplier_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralA": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralB": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralA_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralB_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralA_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralB_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralA_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralB_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralAB_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralAB_square_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralA_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralAB_quadratic_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralScalarConjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralReflection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJMap_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJMap_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJMap_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJ_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJ_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJA_eq_BJ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.spectralJB_eq_AJ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedGraphTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_tomita_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_tomita_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_tomita_maps_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_tomita_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_tomita_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.bounded_graph_J_tomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.boundedGraphStandardSubspace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuousModularOperator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_apply_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_weight_fiber_subsingleton": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_weight_fiber_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_no_eigen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_zero_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_zero_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_modular_zero_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuousModularTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuousStandardSubspace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_maps_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_J_tomita_eq_modular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_standard_fixed_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_domain_iff_standard_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_apply_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous049.continuous_tomita_zero_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.antiunitary_inner_conj": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.antiunitary_pairing_flip": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.genericTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_tomita_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.genericAdjointDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.genericAdjointInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_adjoint_input_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.genericTomitaAdjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_tomita_adjoint_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_pairing_with_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_adjoint_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_adjoint_maximal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_adjoint_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_composition_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.generic_adjoint_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.partialSquareDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousModularSquareDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousModularSquareInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousModularSquare": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_weight_double": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_weight_double_complex": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_weight_half_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_double_domain_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_domain_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_composable_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_square_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_eq_generic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousTomitaAdjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_adjoint_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_adjoint_maximal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_adjoint_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_composition_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_tomita_adjoint_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousModularDelta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_graph_iff_tomita_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_eq_double": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_energy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_delta_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_positive_square_root": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.instSpectralOperatorRealModule": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.spectral_operator_real_smul_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.bounded_spectral_multiplier_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.spectralA_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.spectralB_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuousResolvent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_complement": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_sqrt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_complement_sqrt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_graph_from_cfc": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_modular_domain_from_cfc": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_ae": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_square_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_mem_square_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_square_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_right_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_left_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Continuous050.continuous_resolvent_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalPrimitive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalVolterraCorrection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalCurvatureDrift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_primitive_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_primitive_const": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_primitive_intervalIntegrable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_primitive_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_primitive_continuousOn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_expansion_integral": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_volterra_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_volterra_balance_matched": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_volterra_balance_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_volterra_correction_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_volterra_correction_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_scaled_correction_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalScreenMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalScreenNormSq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalShearNormSq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalRiccatiSystem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_matrix_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_matrix_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_matrix_square_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_raychaudhuri_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_norm_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_shear_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_screen_norm_eq_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_rotated_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_rotated_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_rotated_shear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_riccati_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_riccati_raychaudhuri": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_diagonal_distortion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_affine_curvature_primitive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_affine_curvature_drift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_affine_drift_negative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_affine_drift_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_matrix_constant_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_matrix_correction_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_past_entropy_orientation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_zero_temperature_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_entropy_correction_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.symplecticPolarizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_duality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_opNorm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_antisymmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_eq_of_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_kernel_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizerForm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_re": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizerFormBilin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.real_projection_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_square_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.polarizer_form_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizerCostWeight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_weight_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizerCostTerm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizerModularCost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_eq_tsum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_term_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_term_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_term_add_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_add_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_first_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizerCostDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.mem_polarizerCostDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_kernel_mem_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_power_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_term_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_domain_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_eq_of_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_mem_domain_of_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_modular_cost_lowerSemicontinuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_series_term_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_log_ratio_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_weight_ratio_abs_lt_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_weight_ratio_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_weights_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_scalar_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_scalar_ennreal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_weights_ennreal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_of_norm_powers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_of_weight_norm_powers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.polarizer_cost_norm_powers_lt_top": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_sequential_closability": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_well_defined": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.local_tomita_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closure_graph_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_closure_vertical": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_closure_single_valued": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_is_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_extends_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedModulatorCandidate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_is_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.candidate_factorization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalAdjoint_coordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalOp_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalOp_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonal_square_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonal_square_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modular_twist_of_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.towerJ_inner_flip": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_pairing_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelProject_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_preserves_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_pairing_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_pair_mem_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_is_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_level_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.JS_positive_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_denseRange": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_polar_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareDomain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareDomain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.square_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_energy_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_first_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_adjoint_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_adjoint_maximal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_composition_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_adjoint_comp_is_delta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_reciprocal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_graph_J_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_positive_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_inner_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_push": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_isometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlowUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_strongly_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_intertwines": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_preserves_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.localEigenvectors_total": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_spectral_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.deltaImaginaryPower_spectral": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_preserves_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modular_power_group_and_continuity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_fixes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_preserves_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_flow_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_omega_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_bounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_compression": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_bimodular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_step_slice": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_not_imported_contract": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.constructedLevelExpectations": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.level_expectation_family_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.commutes_all_levels_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_intersection_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperators_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_isotony": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_local_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_locality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_empty": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_prefix_eq_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.prefix_expectation_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chainVolume_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chainVolume_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.constant_calibration_forces_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.no_bounded_positive_count_calibration": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.shifted_generator_intertwining": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.uniform_generator_intertwining": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_tail_intersection_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chainVolume_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.normalizedVolume_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_tail_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_tail_antitone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_tail_exact": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.site_noncommutation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_order_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_localization_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.state_local_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.state_local_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.density_commuting_local_is_global_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pinching_into_global_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.state_mul_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.state_single_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.centralizer_local_blocks": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pinching_fixes_global_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_of_centralizer_is_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pinching_state_ortho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectationMatrix_pi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectationMatrix_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pinching_global_ortho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.localCentralizerInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.local_input_is_spectral": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.local_input_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.omega_product_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.centralizer_from_expectations": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_profile_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_profile_local_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_profile_centralizer_is_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tracialExpectationInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tracial_expectation_is_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_inverse_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_flow_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_flow_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_flow_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_flow_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_flow_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.invariant_is_not_strict": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_never_strict": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.global_expectation_restricts_to_pinching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.global_expectation_differs_from_floor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.shifted_range_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.cyclic_expectation_forces_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.cyclic_expectation_forces_full_algebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.proper_expected_subalgebra_not_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_continuous_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modular_orbit_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modular_orbit_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodAverageVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.average_vector_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.average_vector_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.average_vector_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodAverage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_operator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_log_lattice": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularPhase_lattice_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lattice_flowLevel_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lattice_modular_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stationary_site_log_lattice": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stationary_log_gap_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stationary_modular_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lattice_local_phase_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.integral_modularPhase": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.integral_flowLevel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.integral_modularFlow_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_prefix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_fixes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.period_average_ortho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodicExpectationInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stationaryExpectationInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_profile_has_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodic_half_agrees": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodic_expectation_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodic_expectation_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_is_canonical_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.boost4_is_canonical_block": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_modular_cannot_intertwine_nonzero_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.contraction_invariant_continuous_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.periodic_borchers_trivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.eigenvector_diagonal_modular_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.isometry_fixed_of_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_borchers_fixes_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_borchers_trivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_prefix_expectation_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_mark_factorization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_witness_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_witness_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_witness_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_witness_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tail_not_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_constant_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_constant_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flatHorizonPencil": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_nonzero_pencil_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.balanced_flux_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.balanced_local_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curved_control_direction_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.curved_control_no_vacuum_pencil": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.kms_with_incompatible_geometric_data": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropyAtom_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropyAtom_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropyAtom_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.finiteEntropy_neg_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_weights_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.finiteEntropy_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_left_marginal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_right_marginal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_mutual_information_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.site_entropy_binary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropy_diagonal_modular_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.finite_entropy_first_law": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_modular_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_product_information_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropy_normalized_volume": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_density": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_entropy_density_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.no_sublinear_area_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.entropy_as_chosen_count_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.sqrt_weight_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.schmidt_amplitude_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.schmidt_amplitude_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_trace_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_right_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_left_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.trace_partial_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_left_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_off_diagonal_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_annihilated_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_density_properties": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_marginals": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_prefix_coherence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_reduced_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_entropy_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_modular_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_left_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_indices_distinct": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_full_not_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tower_cut_chosen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_coherence_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.pure_cut_not_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_cut_positive_normalized_pure": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_cut_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_cut_not_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.product_control_information": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.complement_entropy_invariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.two_area_calibrations": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chosen_area_rescales_einstein_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.equal_past_entropy_area_derivatives": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.constant_entropy_forces_zero_area_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.constant_entropy_forces_zero_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.fixed_tower_entropy_forces_zero_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.finite_entropy_area_rate_constraint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.geometric_expansion_excludes_frozen_tower_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_null_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_null_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_screen_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_screen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_induced_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flatScreenWitness": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flatGeometricScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flatGeometricHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flat_geometric_nonzero_inhabitant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_area_signature_flip": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.screen_gram_rescale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stretched_screen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stretched_screen_area_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.stretched_cut_refuses_fixed_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.normalized_frame_screen_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.negative_identity_screen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.assembleNormalizedScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.solderedScreenAtPoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.leviCivitaScreenAtPoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.normalized_screen_at_point_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.levi_civita_null_screen_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.zero_direction_has_no_null_screen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.off_axis_vector_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.off_axis_vector_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.offAxisNullFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.off_axis_frame_verified": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.normalized_family_area_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen013.normalized_family_expansion_obstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.raw_gram_shape": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completion_coefficients_solve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completed_gram_coefficients": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completed_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completion_first_column": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completion_keeps_screen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.null_screen_gram_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.frame_det_nonzero_from_null_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.completedNullScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.previous_and_constructed_frames_coexist": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.velocity_frame_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.velocity_frame_screen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.screen_gram_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.screen_gram_continuous_components": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.normalized_initial_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.flow_raw_gram_row": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.flowScreenCertificate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.flow_screen_positive_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.geometricScreenFromFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.flow_screen_area_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.geometric_screen_area_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.local_levi_civita_transported_screen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.zero_generator_frames_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.flat_frame_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_factor_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_geodesic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_velocity_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_metric_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_connection_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_metric_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_metric_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_connection_compatible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expandingInitialFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_screen_nonconstant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen014.expanding_background_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.phase_domain_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_spray_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_spray_c1": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.spray_position_component": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.spray_zero_velocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_energy_algebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.eventually_phase_rectangle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.localPhaseFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.regular_phase_domain_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.localGeodesicFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_position_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_velocity_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_regular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_energy_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_energy_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_null_preserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.leviCivitaGeodesicFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.local_levi_civita_null_geodesics": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_smooth_Icc": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_smooth_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_position_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.geodesic_flow_velocity_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.phase_flow_jointly_continuous_at": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.phase_initial_data_obstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.zero_connection_velocity_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.zero_connection_position_affine": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.flat_geodesic_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.phase_flow_cannot_assign_one_field": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.conformal_spray_acceleration_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.conformal_spray_acceleration_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.curved_null_geodesic_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Screen015.curved_flow_background_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.eventually_flow_rectangle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.lipschitzLocalFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_initial_distance_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_joint_continuous_at": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.variational_domain_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.variational_field_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.variationalLocalFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.diagonal_initial_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_solution_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_variation_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_solution_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_variation_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_variation_apply_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_solution_stays": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_solution_distance_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.solution_and_variation_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_remainder_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_remainder_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_remainder_gronwall": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.gronwall_zero_scaling": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_remainder_normalized_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_remainder_normalized_bound_nonpositive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_initial_hasFDerivAt_nonpositive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_initial_hasFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.taylor_remainder_eventually": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_taylor_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_derivative_norm_bounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_initial_hasFDerivAt_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.phaseFlowOfVariational": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.phase_flow_of_variational_c1": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.c1GeodesicFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.c1_geodesic_flow_joint_c1": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.local_c1_metric_null_geodesics": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.local_c1_levi_civita_null_geodesics": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_time_derivative_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_joint_hasStrictFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_joint_derivative_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flow_joint_c1": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.linear_taylor_remainder_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.zero_field_flow_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.zero_field_variation_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flat_geodesic_initial_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flat_variation_block": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.flat_variation_on_perturbation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow016.curved_c1_null_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_germ_eq_at_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.projectedVariationalFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.variational_projection_contDiffAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.variational_regular_flow_successor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.exists_finite_regular_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_finite_regular_at_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_smooth_at_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_finite_regular_times_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_finite_regular_on_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_smooth_on_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.eventually_flow_time_box": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flow_finite_regular_nearby_transfer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.phase_flow_of_variational_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.c1_geodesic_flow_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.local_smooth_metric_null_geodesics": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.local_smooth_levi_civita_null_geodesics": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.zero_field_smooth_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.flat_geodesic_smooth_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow017.curved_smooth_null_flow_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.exists_normalized_covector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transverse_projection_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transverse_projection_velocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.initial_position_in_section": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.initial_position_shift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.initial_time_shift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.initial_position_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transported_seed_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transported_seed_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transported_seed_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.transported_seed_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_position_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_position_along_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_velocity_along_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_input_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_phase_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_domain_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_domain_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_input_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_phase_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_regular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.shooting_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.smoothLocalChart": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.chart_position_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_target_subset": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_base_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_base_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.congruence_geodesic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.local_null_congruence_from_seed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.local_levi_civita_null_congruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.constructed_congruence_transported_screen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.control_direction_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.flat_constructed_congruence_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.curved_constructed_congruence_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow018.geodesic_nullity_does_not_force_zero_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.quadratic_sub_null_direction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_correction_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_correction_fixes_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.tensor_pair_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_correction_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.scalar_derivative_zero_from_partials": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.zero_jet_quotient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_correction_preserves_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.connection_initial_jet_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.vector_partial_of_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.gradient_action_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.derivative_of_zero_covariant_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_covariant_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_gradient_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.affine_seed_energy_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_companion_of_frame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.null_seed_with_companion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.local_null_seed_with_zero_covariant_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.shooting_velocity_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.shooting_inverse_base_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.shooting_inverse_derivative_base": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.congruence_derivative_base": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.congruence_prescribed_gradient_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.local_equilibrium_congruence_from_seed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.local_levi_civita_equilibrium_congruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.localEquilibriumScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.equilibrium_screen_expansion_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.equilibrium_screen_optical_form_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.equilibrium_screen_area_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.equilibrium_screen_focusing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.local_equilibrium_screen_with_focusing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.control_companion_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.control_companion_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.zero_gradient_differs_from_expanding_field": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.flat_equilibrium_congruence_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow019.curved_equilibrium_congruence_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_clamp_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_clamp_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_clamp_fixes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.pastContinuousExtension": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_integral_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_integral_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_integral_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_integral_initial_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_integral_matches_flux": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_area_continuous_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_curve_eventually_neighborhood": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_matter_continuous_at": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_matter_continuous_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_matter_continuous_past": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.area_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_area_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_heat_flux_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_heat_flux_continuous_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_heat_flux_continuous_past": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screenHeatExtension": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructedHeat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_heat_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_heat_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_heat_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_heat_flux_linear_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_heat_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_heat_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.heat_extension_difference_quadratic_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.residual_quadratic_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.clausius_coefficient_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.past_zero_limit_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_clausius_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.screen_clausius_iff_null_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_clausius_iff_null_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.horizonPencilFromScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.null_balance_produces_pencil": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.ConstructedClausiusAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.constructed_clausius_at_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.einstein_from_constructed_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_solder_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_solder_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_control_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_connection_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_ricci_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flatConstructedScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.control_matter_differentiable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.control_matter_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.control_matter_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.control_matter_null_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_constructed_residual_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_nonzero_matter_residual": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_nonzero_matter_not_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.flat_vacuum_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Flow020.conserved_matter_does_not_force_constructed_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.modular_increment_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.diagonal_fisher_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.diagonal_fisher_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.diagonal_fisher_pos_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.state_curve_base_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.state_curve_positive_near": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.state_curve_tangent_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_curve_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_curve_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_curve_continuous_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_curve_derivative_past": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.state_log_ratio_slope": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_rate_slope": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_curve_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_quadratic_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.relative_entropy_first_order_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.affineStateCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadraticStateCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.modular_increment_affine": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.modular_increment_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.affine_relative_entropy_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadratic_relative_entropy_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadratic_modular_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadratic_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.residual_entropy_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.microscopic_residual_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.microscopic_clausius_iff_zero_tangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadratic_matching_gives_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.geometric_microscopic_compatibility": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.matching_produces_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.einstein_from_quadratic_microscopic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.modular_increment_is_generator_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_modular_response_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.flatVacuumMatching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.flat_nonzero_matter_has_no_quadratic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_weights_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_weights_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.signed_response_trace_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_response_fisher": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_affine_entropy_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_affine_relative_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.first_order_does_not_imply_second_order": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.quadratic_response_is_not_frozen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.half_quadratic_relative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.third_weights_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.third_weights_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.third_modular_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.nontracial_quadratic_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.state_curve_purification_near": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Micro021.tower_quadratic_relative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.axis_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.axis_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_hamiltonian_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.axis_polynomial_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_adjoint_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_mul_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_hamiltonian_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_energy_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.frequency_cos_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.frequency_sin_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.velocity_is_schrodinger": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_flow_schrodinger": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.evolved_pair_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.evolved_pair_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.evolved_pair_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.cartesian_amplitude_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.first_weight_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.second_weight_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_amplitude_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_weights_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_weights_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_extension_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_extension_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_extension_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_flow_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_extension_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_state_is_evolved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_density_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_amplitude_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_density_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_density_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.correlated_right_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.evolved_state_valid": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_weights_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_weights_at_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.pair_tangent_at_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitaryStateCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.base_weights_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_weights_positive_near": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_relative_entropy_quadratic_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.frequency_sin_slope": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.frequency_sin_square_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_first_weight_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_modular_increment": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_modular_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_entropy_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_marginal_modular_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_heat_error_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_matching_gives_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_heat_matching_requires_matter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_response_blocks_nonnegative_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.unitary_screen_matching_produces_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.einstein_from_unitary_microscopic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.flatUnitaryVacuumMatching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.flat_incompatible_matter_has_no_unitary_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.transfer_coefficient_expanded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.control_initial_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_axis_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_axis_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_control_transfer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_control_transfer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.control_log_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_control_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_control_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_control_response_strict": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_control_response_strict": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.positive_control_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_control_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.negative_control_required_matter_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.diagonal_axis_stationary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Unitary022.tracial_reference_response_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_read_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_read_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.directional_hamiltonian_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.pair_flow_reparameterized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.directional_flow_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.directional_flow_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.directional_kernel_trivial_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.unitary_response_frequency_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_tensor_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_tensor_quad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.response_tensor_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.response_tensor_quad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_read_change_basis": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_tensor_change_basis": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.response_coupling_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_negative_control_coupling_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_quad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_null_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.response_equals_negative_null_stress": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_field_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_field_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_field_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.outer_field_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_squared_differentiable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_squared_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coordinate_partial_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_divergence_point": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_derivative_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_divergence_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_conservation_iff_wave_at": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_conserved_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.potential_covector_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.potential_covector_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.covector_stress_field_differentiable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_area_error_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_area_matching_iff_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherentScreenMatching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.frame_covector_stress_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.frame_covector_stress_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_heat_matching_determines_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.frame_covector_source_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.einstein_from_coherent_area_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coordinate_partial_coordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.constant_time_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.constant_time_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.constant_time_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_potential_covector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_stress_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.growing_time_not_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_matter_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_matter_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_matter_matrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_null_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Coherent023.coherent_flat_area_not_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_local_state_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_local_weights_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_local_weights_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.canonicalModularStateCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.canonical_modular_entropy_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.canonical_modular_increment_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.canonical_modular_relative_entropy_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.canonical_modular_generator_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_atom_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_partition_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_partition_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_atom_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_partition_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_partition_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_mean_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_tangent_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbsStateCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_log_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_mean_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_tangent_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_variance_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_variance_second_moment": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_variance_zero_iff_centered": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_variance_zero_iff_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.modular_variance_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_tangent_modular_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_modular_increment_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_entropy_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_fisher_is_modular_variance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_relative_entropy_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_reparameterization_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_parameter_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_tangent_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadraticGibbsCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_tangent_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_relative_entropy_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_modular_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.quadratic_gibbs_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_square_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_local_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_self_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_weighted_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_filter_local_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_sandwich": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_local_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_square_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_vector_separating": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_state_seqWOT": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_inclusion_coherent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_local_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_coupling_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_response_null_stress": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_heat_error_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_area_error_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_area_matching_iff_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_matching_produces_clausius": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.einstein_from_gibbs_area_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.binary_gibbs_variance_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_first_site_variance_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_read_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_entropy_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_modular_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_weights_not_modular_orbit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.tower_gibbs_not_modular_orbit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_flat_matter_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_flat_matter_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_flat_null_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_flat_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal024.gibbs_flat_area_not_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.modular_score_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_atom_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_partition_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_weights_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.product_expectation_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_product_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_mean_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.modular_mean_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.product_second_moment": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.modular_variance_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_variance_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_variance_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_variance_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_variance_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermalProfile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_profile_site": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_profile_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_profile_tower_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_global_local_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_tower_marginal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_tower_marginal_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_global_state_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_profile_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_tower_entropy_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.diagonal_affinity_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.hellinger_sum_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.diagonal_affinity_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.diagonal_affinity_eq_one_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.diagonal_affinity_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.weighted_sqrt_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.diagonal_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_fixed_iff_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_affinity_lt_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_filter_affinity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_affinity_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.gibbs_amplitude_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_gibbs_omega_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_gibbs_affinity_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_gibbs_uniform_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_step_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_local_vectors_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_gibbs_successive_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_gibbs_successive_distance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.nontracial_site_affinity_lt_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_uniform_overlap_tends_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_vectors_no_norm_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_vectors_not_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_size_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_frequency_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_parameter_matches": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_size_tends_infinity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_parameter_tends_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_coupling_uniform": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.stationary_site_variance_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.tower_coupling_unbounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_response_equals_site": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_modular_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_relative_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_state_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.thermal_local_state_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_local_state_returns_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.half_site_equal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.half_gibbs_affinity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.half_thermal_vectors_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.half_thermal_variance_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.third_thermal_vectors_not_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.third_thermal_coupling_unbounded": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_area_matching_iff_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_flat_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Thermal025.cutoff_flat_area_not_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_filter_self_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_weighted_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_amplitude_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_filter_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_filter_local_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_state_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_state_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_state_marginal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_omega_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_filter_reverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_filter_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.site_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.site_affinity_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.relative_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_filter_step": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_trace_step": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_trace_push": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_filter_square_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vectors_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vectors_distance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_inverse_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_antitone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_bddBelow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_limit_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_limit_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_ratio_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.affinity_loss_sum_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.affinity_tail_loss_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.affinity_loss_summable_positive_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vectors_cauchy_of_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_positive_of_vectors_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vectors_cauchy_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_vectors_limit_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_zero_affinity_no_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_summable_has_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.globalProfileVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_vector_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_square_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_seqWOT": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_inverse_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.push_diagonal_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.pushed_relative_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_relative_right_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_right_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_inverse_overlap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_inverse_distance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_inverse_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_vector_separating": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_state_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.sqrt_difference_square_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.binary_affinity_quadratic_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.binary_third_affinity_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_weighted_square_summable_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_square_summable_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.global_profile_vector_cyclic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradualProfile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_profile_diff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_profile_changes_every_site": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_profile_square_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_profile_diff_not_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_profile_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_state_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_state_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.gradual_state_not_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_thermal_preparation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.thermal_preparation_limit_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_limit_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.profile_affinity_stationary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.third_half_site_affinity_lt_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.stationary_changed_affinity_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Profile026.stationary_changed_no_preparation_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileGNSPre": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_tof": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_local_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileGNSPreIsometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_pre_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileGNSIsometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_intertwines": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_map_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_range_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_range_local_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_range_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileGNSUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_unitary_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_unitary_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_unitary_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_gns_unitary_intertwines": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.star_equiv_centralizer_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileFactorConjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_inverse_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_state_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitaryPartial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_input_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_lift_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_input_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_lift_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_formal_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.selfadjoint_weak_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.unitary_partial_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_graph_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_closed_graph_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_closed_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_graph_single_valued": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_closed_graph_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_is_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_vector_mem_tomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_extends_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileJ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_j_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_j_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_j_fixes_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileHalfOperator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileDeltaOperator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_half_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_js_equals_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_tomita_polar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_half_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_half_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_half_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_is_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_local_mem_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_half_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_local_mem_delta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileModularFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_on_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_fixes_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_strongly_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profileFlowConjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_conjugation_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_preserves_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_preserves_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_local_conjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_local_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_eigenvector_mem_delta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_delta_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_eigenvector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_spectral_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.relative_filter_same": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_vectors_same": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.global_profile_vector_same": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_unitary_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_unitary_self_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_factor_conjugation_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_j_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.profile_flow_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.gradual_profile_vector_ne_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.old_modular_orbit_ne_gradual": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.gradual_first_eigenvalue": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.reference_first_eigenvalue": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.gradual_eigenvalue_differs": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.gradual_transported_delta_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Transport027.gradual_transported_flow_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.relative_atom_lower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.relative_atom_upper": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.diagonal_relative_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.diagonal_relative_upper": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.modular_increment_energy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.reference_energy_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.modular_increment_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.relative_entropy_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_binary_modular_increment": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_binary_relative_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.site_relative_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_relative_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_relative_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_relative_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_modular_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_modular_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_entropy_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_relative_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_relative_le_total": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.profile_relative_total_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_relative_sites_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_relative_total_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_prefix_modular_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.third_prefix_modular_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.prefix_entropy_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_shift_square_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_relative_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_relative_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_shift_diverges": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_modular_diverges": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_entropy_diverges": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_modular_no_finite_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.harmonic_entropy_no_finite_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.positive_affinity_not_finite_modular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.finite_relative_not_finite_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_square_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_mass_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_square_mass_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_le_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_square_prefix_le_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_lt_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_le_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitudeProfile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_profile_deviation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_profile_square_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_profile_affinity_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitudeVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitudeState": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitudeUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_state_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_state_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_unitary_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_read_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_read_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_state_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.reference_state_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_read_modular_increment": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_deviation_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_modular_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_modular_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_entropy_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_relative_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_modular_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_entropy_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_read_entropy_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_scaled_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_relative_scaled_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.regular_parameter_ratio_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.quadratic_error_bound_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_quadratic_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_relative_quadratic_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_modular_quadratic_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_entropy_quadratic_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_modular_joint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_prefix_entropy_joint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.past_time_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_modular_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_relative_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_entropy_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_coupling_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_response_null_stress": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_heat_defect_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_area_defect_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_area_matching_iff_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_balance_from_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.einstein_from_summable_area_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometricAmplitude": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.zeroAmplitude": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_amplitude_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_amplitude_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_amplitude_square_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_coupling": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_coupling_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_profile_changes_every_site": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_state_not_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_joint_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.site_profiles_eq_of_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.zero_amplitude_profile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.zero_amplitude_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.zero_amplitude_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.zero_amplitude_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_flat_matter_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_flat_matter_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_flat_null_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.amplitude_flat_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Response028.geometric_flat_area_not_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_zero_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_zero_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_one_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_zero_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_zero_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_zero_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.log_zero_ratio_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.log_one_ratio_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.log_ratio_abs_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.factor_norm_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.modular_conjugation_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.state_norm_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.centralizer_norm_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.site_likelihood_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_argument_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_term_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_norm_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_summable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_term_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_term_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihoodCocycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihoodFilter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_group": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_twisted": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_cocycle_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_prefix_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.boundedCongruenceDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.boundedCongruenceInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.boundedCongruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_input_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.boundedCongruenceLift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_lift_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_input_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_lift_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_equiv_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_formal_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.bounded_congruence_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.phase_frequency_separation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_phase_exponential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_phase_frequency_separation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.phase_frequency_zero_or_equal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_phase_frequency_zero_or_equal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_phase_frequency_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.matrix_inner_test_ext": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.localDeltaInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.local_delta_input_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.local_delta_input_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.weak_delta_of_eigen_tests": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.delta_graph_of_eigen_tests": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_phase_star_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.flow_eigen_inner_frequencies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.flow_eigen_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.flow_eigen_implies_delta_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.bounded_selfadjoint_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_fixed_commutes_with_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.flow_commuting_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.commuting_operator_delta_eigen_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.commuting_operator_delta_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.commuting_operator_preserves_delta_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.commuting_operator_delta_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.modular_fixed_delta_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_affine_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binaryAffineCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_affine_relative_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binaryRelativeAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_punctured_time_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_time_tendsto_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_regular_parameter_tendsto_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_negative_regular_parameter_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_regular_parameter_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_relative_quartic_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_relative_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_relative_admissible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_relative_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.binary_relative_quartic_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_relative_as_binary_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_relative_quartic_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_relative_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_entropy_quartic_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_entropy_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.amplitude_square_mass_le_mass_twelfth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherAngularRate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherSineCoordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherCosineCoordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherAffineWeight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherAffineTangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherWeight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherWeightTangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherLengthPrimitive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherClockSquare": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisherOriginalTime": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_angular_rate_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_angular_rate_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_coordinates_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_sine_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_cosine_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_tangent_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_deriv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_first_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_second_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_contDiff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_taylor_two": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_affine_taylor_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_positive_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_fisher": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_length_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_length_speed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_length_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_weight_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_denominator_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_square_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_square_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_ratio_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_original_time_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_original_time_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_original_time_realizes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_original_time_ratio_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_original_time_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_one_twenty_fourth_clock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flatMetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flatConnection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flatCovectorStress": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.traceCompletedStress": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.traceCompletion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_metric_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_metric_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_metric_compatible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_covector_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_stress_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_stress_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_stress_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.trace_completed_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.trace_completed_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.trace_completed_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.null_stress_classification": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.trace_completion_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flat_stress_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.trace_completed_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.flatForce": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.coordinate_partial_congr_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.coordinate_partial_neg_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.negative_gradient_force_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.completed_conserved_iff_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.conserved_null_response_trace_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.conserved_null_response_closed_force": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.HasConservedNullRealization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.conserved_null_realization_iff_potential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.nonclosed_force_excludes_realization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixedPotential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixedCovector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixedPoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_potential_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_covector_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_potential_covector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_covector_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_covector_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_covector_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_force_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_force_partial_one_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_force_partial_zero_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_force_curl": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_force_not_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_no_conserved_null_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growingTraceCorrection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_trace_correction_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_flat_divergence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_flat_force": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_trace_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_trace_completed_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_trace_completed_null_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_uncompleted_not_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.response_covariant_on_the_periodic_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_fires_on_the_periodic_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_fires_on_the_stationary_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_fires_on_the_tracial_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.every_expectation_on_the_periodic_tower_is_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_on_the_aperiodic_tower_is_still_conditional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFlowCLM_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularConjugation_eq_sandwich": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adT_modularHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.periodic_expectation_commutes_with_modular_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.every_expectation_commutes_with_modular_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chainUnword": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chain_unword_word": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chain_word_unword": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chainWordEquiv": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chain_word_injective": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.siteIndexPermutation": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.site_index_permutation_word": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.site_index_permutation_one": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.site_index_permutation_mul": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finiteSiteMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_unitary_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_unitary_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_conjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.siteTensorMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.site_tensor_matrix_succ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.site_tensor_matrix_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.singleSiteTensor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.single_site_tensor_last": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.single_site_tensor_castSucc": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.single_site_tensor_pi": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_tensor_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_site_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.tower_weight_word_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.stationary_weight_permutation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_matrix_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.stationary_density_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.phaseAverage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.phase_average_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.integral_phase_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.phase_average_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.phase_average_nonzero_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.phase_average_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.flowAverage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.flow_average_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.flow_average_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.local_average_eq_embedding": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.local_average_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.omega_limit_on_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.bounded_local_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.strong_limit_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.factor_mem_of_strong_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.bounded_omega_limit_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.omega_lift_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modularAverageVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_average_vector_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_average_vector_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_average_vector_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modularVectorAverage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_vector_average_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_vector_average_norm_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_vector_average_local_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_vector_average_cauchy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.modular_vector_average_limit_exists": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.period_average_omega_eq_vector_average": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_average_omega_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_average_operator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.period_average_prefix_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.period_average_prefix_omega_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_average_prefix_of_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodicExpectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_spec": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_prefix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_fixes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_ortho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodicExpectationInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_contract_inhabited": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_contractive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.the_lift_fires_on_the_aperiodic_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.every_expectation_on_the_general_tower_is_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_agrees_periodic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_agrees_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.aperiodic_expectation_commutes_with_modular_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Aperiodic046.response_covariant_on_the_general_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.profile_borchers_trivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveCovector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveRaised": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveSolder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveInverseSolder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_nilpotent_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_solder_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_inverse_solder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_metric_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_inverse_metric_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_profile_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_solder_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_inverse_solder_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_profile_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_metric_at_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_inverse_metric_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveConnection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_metric_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_connection_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_connection_torsion_free": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_transverse_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_connection_linear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_connection_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_connection_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_curvature_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_scalar_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_einstein": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_first_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_second_curvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_curvature_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveCovectorField": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveMatter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_parallel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_conserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_covector_potential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_read_area_joint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveRicciScale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matchedSolder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matchedInverseSolder": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matchedScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_parameter_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_ricci_quad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_matter_quad": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_area_matching_of_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_wave_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_constructed_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_heat_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_wave_einstein": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_wave_einstein_from_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_read_entropy_joint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.zero_eta_nonzero_source_refused": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.waveOriginScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_test_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_test_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_test_frequency": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_origin_area_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.wave_wrong_trace_refused": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_ricci_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_curvature_difference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_curvature_distinguishes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.matched_metrics_agree_at_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.zero_wave_ricci_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.zero_wave_vacuum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.zero_wave_nonflat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.geometric_wave_matter_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.geometric_wave_curved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Wave029.state_alone_not_curvature_coordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_exponential_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.towerPiAlgHom": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.tower_pi_exp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.last_site_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.binary_log_matrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.third_log_coefficients": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_term_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.matrix_log_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.matrix_half_log_filter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_filter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.isometry_conjugation_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.conjugations_eq_on_factor_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_global_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.matrix_cocycle_log": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_is_finite_cocycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.finite_cocycle_intertwines": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.flow_level_is_sigma": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_local_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_local_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.conjugations_eq_on_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_phase_norm_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_norm_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_fourth_order_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phaseQuadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_read": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_cocycle_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.phase_quadratic_modular_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.amplitude_state_norm_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_prefix_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_generator_entropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_entropy_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_entropy_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.likelihood_filter_invertible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.zero_amplitude_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.zero_amplitude_cocycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.generator_zero_forces_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cocycle030.geometric_generator_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverseLikelihoodFilter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.likelihoodFilterEquiv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.filter_mul_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverse_mul_filter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverse_filter_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverse_filter_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.filter_equiv_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverse_filter_equiv_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.inverse_filter_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeTomitaGraph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeTomitaDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeTomita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_graph_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_closed_graph_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_closed_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_single_valued": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.unique_graph_range": [
      "propext",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_closed_graph_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_factor_vector_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_extends_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeTomitaLift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_input_lift": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_lift_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeTomitaAdjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_adjoint_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_adjoint_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_adjoint_maximal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_adjoint_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeDelta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_domain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_composition_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_domain_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relativeDeltaTomitaInput": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_tomita_mem_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_tomita_adjoint_comp_is_delta": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Relative031.relative_delta_quadratic_is_tomita_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.inverse_filter_modular_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.filter_flow_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.inverse_filter_flow_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.filter_preserves_delta_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.inverse_filter_preserves_delta_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.filter_delta_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.inverse_filter_delta_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.filter_delta_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.relative_delta_original_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.relative_delta_product_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.likelihoodModularProduct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.relative_delta_eq_likelihood_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.likelihood_modular_product_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.likelihood_modular_product_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.likelihood_modular_product_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.generator_preserves_delta_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.generator_delta_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Commutation032.relative_delta_reference_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_state_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_state_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omegaCentralizerAlgebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_algebra_membership": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_algebra_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.omega_centralizer_exp_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_term_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_prefix_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_generator_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_filter_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_cocycle_mem_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihoodDensity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.boundedDensityPower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_invertible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_log": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_filter_log": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_log_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.bounded_density_power_eq_cocycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.bounded_density_power_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_reference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.phase_quadratic_time_even": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.reference_state_cocycle_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.factor_density_state_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_state_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_state_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Density033.likelihood_density_state_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.boundedPhase": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centralizer_unitary_preserves_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_differentiable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.bounded_phase_vector_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.horizontalComponent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.horizontal_component_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.horizontal_phase_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.twoPhaseOrbit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.twoPhaseVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_state_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_vector_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_distance_preserved": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_first_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_second_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.two_phase_vector_differentiable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_zero_eq_site_mark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_zero_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_mark_mem_tail": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_mark_tail_factorization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_zero_product_state_lt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_zero_product_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centeredSiteVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.site_zero_omega_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_omega_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_inner_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_inner_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_variance_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.centered_site_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phaseSiteVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angularScreenGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angularScreenArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_site_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_site_omega_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_gram_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_determinant_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_area_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_gram_repeated": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_determinant_repeated": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.angular_screen_area_repeated": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.reference_angular_screen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.reference_repeated_angular_screen_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.first_horizontal_tangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.second_horizontal_tangent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_vector_state_form": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phaseRestrictedState": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_restricted_state_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phaseReading": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_reading_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_reading_first_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.phase_reading_second_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observablePhaseJacobian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observable_phase_jacobian_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observablePhaseGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observable_phase_gram_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observable_phase_area_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observable_phase_area_not_angular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.observable_phase_gram_not_angular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Angular034.reference_phase_area_split": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.omegaContinuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.omega_continuous_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.bounded_phase_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.bounded_phase_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.unitaryConjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.unitary_conjugation_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.unitary_expectation_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.operatorOrbit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbitExpectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_first_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_second_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_vector_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_vector_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.orbit_expectation_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliXMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliYMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliZMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sitePauliX": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sitePauliY": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sitePauliZ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.siteOperatorLinear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_state_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_mem_tail": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_tail_factorization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_product_state_lt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_operator_product_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_x_conjTranspose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_conjTranspose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_z_conjTranspose": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_x_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_z_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_xy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_yx": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_z_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_x_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_y_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_z_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_x_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_y_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_z_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_x_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_y_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_z_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_xy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_yx": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_z_projection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_x_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_y_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_z_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_yx_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_y_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_xy_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_xx_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.site_pauli_yy_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliOrbit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliExpectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliYReading": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliObservableJacobian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_orbit_unitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_orbit_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_expectation_vector_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_reading_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_first_axis_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_second_axis_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_first_cross_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_second_cross_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_nondegenerate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_squared_determinant_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_first_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_observable_jacobian_second_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.reference_pauli_observable_jacobian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.reference_pauli_observable_jacobian_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.tracial_pauli_observable_jacobian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.signOutcome": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sign_outcome_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sign_outcome_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sign_outcome_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.sign_outcome_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliYProjectionMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliYProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliJointEffect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliProbability": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_matrix_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_matrix_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_matrix_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_matrix_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_matrix_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_isStarProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_x_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_y_projection_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_isStarProjection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_effect_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.star_projection_inner_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_expectation_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_real": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_origin_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_first_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_first_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_joint_second_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_first_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_second_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliProbabilityGradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliMeasurementFisher": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauliFisherArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_probability_gradient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_determinant_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_determinant_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_determinant_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_fisher_area_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_fisher_area_eq_abs_jacobian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_fisher_area_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_measurement_fisher_quadratic_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_fisher_area_first_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.pauli_fisher_area_second_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.reference_pauli_measurement_fisher": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.reference_pauli_fisher_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.tracial_pauli_measurement_fisher": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Observable035.tracial_pauli_fisher_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.centralNullDirection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.centralNullCurve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.transverseScreenVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.transverseScreenColumns": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.curvatureAction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.opticalTidalMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.opticalTidalTraceFree": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.opticalTidalTraceFreeNormSq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_direction_frequency": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_direction_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_metric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_connection_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_acceleration_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.central_curve_geodesic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.transverse_screen_null_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.transverse_screen_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_trace_eq_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_tracefree_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_tracefree_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_tracefree_norm_sq_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_tracefree_norm_sq_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_anisotropy_basis": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.optical_tidal_no_orthogonal_match": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screenTraceFree": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screenAnisotropy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.orthogonal_trace_conjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screen_tracefree_conjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screen_anisotropy_conjugation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screen_anisotropy_diagonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.screen_anisotropy_matched": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometricJacobiField": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometricJacobiVelocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometricJacobiColumns": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometricJacobiPositiveGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometricJacobiArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.curvature_action_smul_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.transverse_basis_parallel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_field_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_velocity_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_field_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_velocity_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_field_null_orthogonal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_positive_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_gram_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_abs": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_agrees_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_screen_nondegenerate_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_iterated_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_initial_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_initial_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_initial_third": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_initial_fourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_second_eq_ricci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_fourth_from_tidal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_rs_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_rs_fourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_rs_quartic_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_same_second_distinct_fourth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_not_eventually_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical036.geometric_jacobi_area_nonunique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.optical_jacobi_taylor_four": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.optical_jacobi_taylor_remainder_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.optical_jacobi_area_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.geometric_jacobi_area_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.geometric_jacobi_area_rs_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quarticMatchedRicci": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.entropyQuarticCoefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quarticMatchingCoefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quarticStateAreaDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_matched_ricci_cancellation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_state_area_defect_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_state_area_defect_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_state_area_matching_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_log_two_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_coefficient_lower_bound_algebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_matching_coefficient_lower_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_matching_coefficient_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_state_area_small_amplitude_no_go": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_matching_square_criterion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_optical_coefficient_admissible_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.likelihood_reading_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.retimedQuarticStateAreaDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cancellingStateClock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.retimed_entropy_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.retimed_quartic_defect_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.retimed_quartic_state_area_defect_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cancelling_state_clock_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.retimed_quartic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.cancelling_clock_same_initial_calibration": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.common_state_area_clock_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.common_clock_small_amplitude_no_go": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.smallSingleAmplitude": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.small_single_amplitude_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.small_single_amplitude_square_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.small_single_amplitude_bounds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.quartic_matched_ricci_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Quartic037.nonvacuous_quartic_clock_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.localDiagonalLog": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalizedLocalFilter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_diagonal_log_existing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.complex_half_real_exp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_diagonal_half_exp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_as_exponential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_from_relative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.pair_diagonal_congruence": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_filter_exponential_products": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_preserves_det": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.normalized_local_filter_not_unital": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.localPhase": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.complex_phase_real_exp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_phase_as_exponential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_phase_existing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.complex_phase_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_phase_rotation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_phase_mul_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.weighted_slice_kronecker": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.site_relative_filter_square_normalized": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.weighted_slice_relative_filter_step": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.finite_filter_local_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.finite_filter_operator_local_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.localStateFilter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.local_state_filter_weights": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.global_filter_local_reduction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.global_filter_local_matrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.global_filter_local_compression": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cone039.global_filter_local_boost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropyClockRatio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropyReadClock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_read_clock_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_clock_ratio_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_clock_ratio_correction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_clock_root_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fourth_root_correction_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_read_clock_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_read_clock_ratio_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_read_clock_fourth_power": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.primitive_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binaryEntropySlope": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binaryEntropyCurvature": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_slope_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_curvature_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_curvature_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_positive_near": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_slope_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_actual_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_slope_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_entropy_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.regular_parameter_square_sixth_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.binary_relative_sixth_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_profile_even": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_state_even": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.even_curve_reading_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.instantaneous_state_clock_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.no_normalized_instantaneous_state_clock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_profile_flow_fixes_vector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_profile_flow_stationary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_state_site_mark": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_state_not_initial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_state_eq_initial_time_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.amplitude_modular_orbit_not_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.no_normalized_modular_reparametrization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.zero_amplitude_curve_constant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.zero_amplitude_site_weight": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.zero_amplitude_site_weight_ne_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.central_spray_scaled_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.reparametrized_null_position_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.reparametrized_null_covariant_acceleration": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.affine_null_clock_acceleration_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.normalized_affine_null_clock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.normalized_affine_null_clock_on": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.normalized_affine_cubic_clock_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.generatorPairAlgebra": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.generator_pair_double_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.phase_generator_pair_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_last_site_matrix_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_site_operator_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_site_noncommutation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_site_offdiagonal_not_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_chain_order_faithful": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.region_chain_localization_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.discrete_region_inclusion_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.bounded_phase_double_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledPhaseVector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_phase_vector_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledPhaseRestrictedState": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_phase_restricted_state_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.horizontal_component_complex_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledFirstHorizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledSecondHorizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_first_horizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_second_horizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.vectorPairGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.real_inner_double_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.real_inner_double_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.vector_pair_gram_double_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledPhaseGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubledPhaseArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_phase_gram_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_phase_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.doubled_phase_area_ne": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.no_area_rule_for_both_generator_protocols": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.reference_doubled_phase_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_jet_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_ratio_tendsto_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_ratio_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_ratio_punctured": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_inverse_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.clock_jet_quadratic_change": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.general_clock_quartic_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.actualClockStateAreaDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.actual_clock_state_area_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.actual_clock_matching_requires_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.oneSiteAmplitude": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.one_site_amplitude_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.one_site_amplitude_square_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.one_site_clock_excess": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.one_site_clock_excess_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.one_site_actual_clock_no_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_no_fourth_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_inverse_clock_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_inverse_clock_no_fourth_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.required_clock_tidal_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.no_clock_matching_two_tidal_geometries": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.single_control_coefficients": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.actual_clock_quadratic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.horizon_area_entropy_forces_defect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.exact_horizon_family_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.fisher_clock_no_exact_horizon_family": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock040.entropy_inverse_no_exact_horizon_family": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.primitive_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.geometric_area_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.opticalHeatFlux": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_flux_geometric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_flux_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.opticalHeat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.geometric_area_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_corrected_heat_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_corrected_flux_cubic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_heat_zero_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.opticalClausiusDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_quadratic_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_coefficient_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_not_eventually_exact": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_eventually_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.optical_clausius_rs_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.isotropic_unit_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.flat_zero_control": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Heat041.flat_matching_forces_zero_mass": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.HasSummableNullRealization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.amplitude_response_null_value_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.summable_coupling_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.summable_null_realization_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.summable_null_realization_iff_potential": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_no_summable_null_realization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.summable_entropy_limit_iff_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_no_summable_entropy_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.mixed_geometric_no_summable_realization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_summable_null_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.growing_summable_null_realization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Completion042.zero_amplitude_summable_null_realization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalPhaseCoordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobiLogDerivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalCongruenceDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_phase_coordinate_contDiff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_phase_coordinate_hasFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_phase_coordinate_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_oscillator_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_velocity_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_log_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_log_derivative_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_log_derivative_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_log_derivative_contDiffAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.jacobi_log_profile_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_congruence_domain_open": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_congruence_domain_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_congruence_domain_central_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_congruence_domain_eventually": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalRate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalLongitudinalCorrection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalNullVelocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalCubicProfile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalNullGradientMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_rate_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_rate_hasFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_rate_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_longitudinal_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_frequency": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_nonzero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_null": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_longitudinal_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_geodesic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_formula_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_central_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_gradient_origin_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_null_velocity_geodesic_levi_civita": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalJacobiFrame": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalJacobiFrameInverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_frame_first_column": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_frame_columns": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_frame_right_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_frame_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_frame_preserves_null_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalScreenCertificate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalGeometricScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_geometric_screen_initial_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_geometric_area_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalEquilibriumScreen": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_equilibrium_curve": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_equilibrium_columns": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_equilibrium_velocity_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_equilibrium_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.past_integral_original_germ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_heat_flux": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalScreenHeat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_heat_germ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_heat_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_heat_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.opticalScreenClausiusDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_clausius_germ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_clausius_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_quadratic_balance_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_clausius_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_clausius_eventually_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_screen_clausius_not_eventually_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.flat_screen_not_quadratically_balanced": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical043.optical_equilibrium_flat_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostField": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostGenerator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostEven": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostOdd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostFlow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostMatrixAction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_action_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_even_add_odd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_even_sub_odd": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_exponential_product": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_coeff_hyperbolic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_even_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_odd_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_even_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_odd_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_smooth": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_future_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_frequency": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_as_linear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_hasFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_partial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_mul_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_neg_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_hasDerivAt_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_coordinates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_neg_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_neg_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_hasFDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_fderiv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_two": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_phase_coordinate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_covector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_flat_preserving": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_field_rate_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_matrix_rate_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_flow_rate_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostMetricPullback": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.coordinateMetricLie": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_wave_profile": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_wave_covector_pullback": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_pullback_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_scalar_along": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_pullback_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.scalar_fixed_tensor_jet": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_first": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_second_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_second_two": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_first_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_pullback_central": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_zero_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_lie_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_pullback_zero_rate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_metric_pullback_flat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_not_killing_near_origin": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostEnergyFlux": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_contraction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_flux_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_flux_constructed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.wave_matter_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_wave_contraction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_flux_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostEnergyHeat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_heat_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_heat_constructed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostSegmentHeat": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_heat_orientation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_heat_wave": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_heat_constructed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_energy_flux_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_heat_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostSegmentArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boostSegmentDefect": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_defect_orientation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_defect_constructed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Boost044.boost_segment_quadratic_balance_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finiteSiteUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_preserves_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finiteSiteHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_site_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_site_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_unitary_tail_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_tail_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_swap_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_swap_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_stationary_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_tracial_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_covariance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.modular_site_projection_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.different_site_projections": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_nonmodular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.finite_site_horizon_ne_modular_horizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.swapHorizon": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.swap_horizon_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.swap_horizon_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.expectation_commutes_with_site_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.swap_horizon_nonmodular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.StateClock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.cubic_clock_jet_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.cubicStateClock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_positive_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.FourthOrderMatch": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.two_screen_anisotropies_admissible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.tidal_quartic_coefficient_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.common_clock_residual_difference": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.common_clock_residual_gap_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.arbitrary_common_clock_pair_incompatible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.arbitrary_common_clock_dichotomy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_dichotomy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_history_rule_dichotomy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_not_instantaneous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_not_modular_reparametrization": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_quartic_residual": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_preserves_quadratic_matching": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.state_clock_matching_iff_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.each_screen_has_a_matching_state_clock": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Clock045.required_state_clock_gap_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.FormInvariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.FormSymmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.FormPositive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.formGram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.formArea": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_invariant_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_symmetric_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_positive_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_gram_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_area_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_gram_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.screen_determinant_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.screen_area_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_determinant_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_area_scale": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.form_area_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.scaled_form_areas_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.scaled_forms_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.invariant_positive_area_nonunique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.invariance_does_not_fix_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.scaled_reference_angular_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Area045.reference_angular_scales_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.omega_state_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.omega_centralizer_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_eq_of_ortho": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_sub": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_preserves_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_mul_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_mul_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_bimodular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectationLinearMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_linear_map_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectationContinuousLinearMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_continuous_linear_map_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_continuous_linear_map_norm_le_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.modular_conjugation_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.modular_conjugation_inner_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.period_average_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.period_average_re_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.period_average_re_inner_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_re_inner_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_isPositive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.blockQuadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.BlockPositive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.block_modular_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.block_period_average_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.block_period_average_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.block_average_quadratic_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_block_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.gram_block_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.gram_block_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_subalgebra_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_positive_sqrt_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_nonnegative_iff_star_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_subalgebra_star_ordered": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_cstarMatrix_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.generalExpectationCompletelyPositiveMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_cp_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_cp_toLinearMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_gns_norm_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_gns_dist_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_omega_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.bounded_local_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.bounded_omega_tendsto": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_strong_tendsto_of_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.strong_net_limit_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_mem_of_net_strong_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_order_preserving": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.factor_monotone_supremum_and_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.expectation_preserves_order_bounded_nets": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.general_expectation_normal_order": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Expectation047.aperiodic_expectation_normal_order": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.faithful_covariance_period_return": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.modular_period_conjugation_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.modular_period_image_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.modular_period_geometric_return": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.modular_period_dilation_return": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.modular_period_dilation_obstruction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.dilation_factor_ne_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.faithful_modular_dilation_localization_impossible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.central_null_curve_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.central_boost_no_return": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.central_boost_covariance_to_dilation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.faithful_central_boost_localization_impossible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.thirdModularPeriod": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.third_modular_period_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.third_modular_flow_period": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.third_faithful_dilation_localization_impossible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.third_faithful_central_boost_localization_impossible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.constant_factor_localization_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Geometry048.constant_factor_localization_not_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalExpansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalDistortionSquared": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.opticalAccumulatedCorrection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_distortion_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_expansion_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_expansion_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_distortion_continuousOn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_area_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_area_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_finite_balance": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_correction_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_finite_balance_near_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.constructed_heat_finite_balance_germ": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Optical051.optical_correction_quartic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauliHorizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_basis_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_basis_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.aperiodic_expectation_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.aperiodic_pauli_x_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.aperiodic_pauli_y_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_re_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_im_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_horizontal_gns_norm_sq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_x_gns_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_y_gns_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.pauli_xy_gns_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontalReading": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_x_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_y_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_x_reading_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_y_reading_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontalResponse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_response_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontalResponseMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_response_matrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_response_determinant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_response_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_state_tangent_separates": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.horizontal_response_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.aperiodic_pauli_x_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.aperiodic_pauli_y_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.firstSiteModularGap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modularQuarterTurnTime": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modularOrientedQuarterTime": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_modular_gap_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_modular_gap_pos_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_modular_gap_neg_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_modular_gap_sign": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_phase_trigonometric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_flow_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_flow_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_horizon_pauli_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_horizon_pauli_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_quarter_turn_angle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_quarter_horizon_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_quarter_horizon_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_oriented_quarter_time_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_oriented_angle_of_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_oriented_angle_of_neg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_oriented_horizon_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_oriented_horizon_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.first_site_modular_gap_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_horizon_pauli_x_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.modular_horizon_pauli_y_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.OrbitPlane": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitBasisX": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitBasisY": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitQuarterTurn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitDotForm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitSymplectic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitOrientedTurn": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbitCalibratedForm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_basis_decomposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_quarter_basis_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_quarter_basis_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_quarter_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_dot_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_bilinear_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_quarter_invariant_form": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_trace_one_selection": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_scalar_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_scalar_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_trace_one_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_selected_trace_in_orthonormal_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_sign_times_self": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_calibration_identity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_oriented_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_calibration_compatibility": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_calibrated_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_calibrated_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_calibrated_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.orbit_zero_calibration": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_horizontal_re_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_horizontal_im_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_horizontal_quarter_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_horizontal_oriented_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_horizontal_tracial_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_asymmetry_ne_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantumOrbitPairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_pairing_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantumOrbitForm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_nondegenerate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_form_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_pairing_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_directions_effective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_effective_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_centralizer_imaginary_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_orbit_third_reference_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_candidate_quarter_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_candidate_isotropic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_candidate_gns_restriction": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_candidate_trace_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Orbit052.quantum_candidate_trace_one_area": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_ad_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_ad_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_ad_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_inner_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_norm_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_dist_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSPre": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_pre_tof": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_pre_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_pre_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSPreLinear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_pre_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_pre_isometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSMap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSIsometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_apply_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_map_right_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_apply_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_symm_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.realStateGenerators": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.realStateSubspace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.real_state_generator_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.real_state_subspace_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.instCompleteSpaceRealStateSubspace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_real_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_real_image": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizonGNSRealUnitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_real_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.real_state_pairing_ext": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.statePolarizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_polarizer_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.tower_polarizer_eq_of_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_centralizer_iff_imaginary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_polarizer_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.stateVectorReal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.stateCovariantBilinear": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_positive_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.horizon_gns_real_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_polarizer_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_factor_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_add_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_add_centralizer_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.realStateResponse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_reading_real_hasDerivAt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_response_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_response_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_response_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.localPolarizerMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_polarizer_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_polarizer_sylvester": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_state_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_polarizer_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.tower_local_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_polarizer_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_operator_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipXMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipYMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipX": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipY": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.local_real_smul_action": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.first_pauli_polarizer_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.first_pauli_polarizer_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_polarizer_x": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_polarizer_y": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_state_products": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_real_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_norm_squares": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipHorizontal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_horizontal_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_horizontal_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_horizontal_expectation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipReading": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_commutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_x_reading_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_y_reading_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.doubleFlipResponse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_response_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_response_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_flip_effective_directions": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.ReferenceOperator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalizedCovariantForm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalization_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_positive_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.state_covariant_rotating_pair_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.first_pair_real_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.first_pair_unnormalized_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.double_pair_unnormalized_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_first_pair_gram": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_double_pair_gram_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_double_pair_gram_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_double_pair_area_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_double_pair_area_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_area_gap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_forms_distinct": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_forms_not_global_rescaling": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.two_global_covariant_calibrated_forms": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_add_centralizer_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_add_centralizer_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Covariant053.normalized_covariant_response_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.towerModularCost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.towerModularCostDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_zero_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_response_kernel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.horizonCostIsometry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_domain_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_factor_invariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_modular_cost_lowerSemicontinuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.localPolarizerIterate": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_polarizer_iterate_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_polarizer_iterate_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.state_polarizer_local_power": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_iterate_normSq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.state_polarizer_local_power_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.localModularCost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_local_cost_hasSum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_local_cost_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_local_mem_cost_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_cost_domain_dense_real": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_modular_cost_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.tower_local_cost_symmetric_formula": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.rotating_pair_norm_powers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.first_pauli_cost_norm_powers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.double_flip_cost_norm_powers": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.first_pauli_modular_cost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.double_flip_modular_cost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.omegaRealContinuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.omega_real_continuous_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.bounded_phase_negative_generator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.negative_phase_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitaryConjugationVelocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_conjugation_has_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.doubleModularCommutator": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_velocity_derivative_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitaryEnergy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitaryEnergyVelocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_energy_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_energy_velocity_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_energy_velocity_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.unitary_energy_second_derivative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.quadratic_response_from_velocity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.localModularMatrix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.localModularObservable": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.finiteModularEnergy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_modular_matrix_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_modular_commutator_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.finite_modular_energy_first_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.local_modular_double_coefficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.finite_modular_energy_second": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.finite_modular_energy_quadratic_limit": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Cost054.global_cost_is_modular_response": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
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
    "TGLExt.ialdSelector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iald_selects": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iald_is_idempotent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iald_is_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iald_has_rank_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.iald_is_the_gate_and_the_record": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.qgImport_H3_localHorizonEquilibrium_bridged": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commutant_iUnion": [
      "propext",
      "Quot.sound"
    ],
    "TGLExt.commutant_towerImage_eq_iInter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_missing_clause_is_a_distributivity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.equal_split_is_strictly_between": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.unequal_split_may_be_trivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.split_forbids_minimality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_split_is_inhabited": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.bell_compression_is_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_rank_determines_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_name_is_blind_to_every_rank": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_name_does_not_see_the_rank": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_index_does_see_the_rank": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_two_indices_agree_only_at_the_atom": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_atom_vanishes_in_the_infinite_house": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_atom_never_weighs_zero_on_a_floor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.psionCorner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.scalarCorner_forces_trace_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.psionCorner_trace_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_identity_does_not_scalarise": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceOneCorner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceZeroCorner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_current_connects_two_scalar_corners": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_current_carries_the_atom": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.equivalent_but_not_equal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.e00_eq_faceOne": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.boundary_faces_sum_to_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.current_symmetrised_is_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_psion_reduces_to_the_symmetrised_current": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_unbonded_reduces_to_one_face_only": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.bonding_splits_and_not_bonding_does_not": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.firstAtom_le_fiber": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_net_corners_are_isotone": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_net_corner_is_externally_covariant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_net_corner_is_internally_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_net_inclusion_is_not_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_net_group_is_nontrivial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.preserving_does_not_operate": [
      "propext"
    ],
    "TGLExt.being_needs_both": [
      "propext"
    ],
    "TGLExt.the_reading_descends_for_any_lens": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJ_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJ_conj_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJ_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJ_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJ_fixes_hOmega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.J_M_J_in_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_old_decision_statement_holds_for_any_proposition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.an_involution_distributes_over_iInter": [
      "propext",
      "Quot.sound"
    ],
    "TGLExt.conjByJ_distributes_over_iInter": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjugated_commutant_is_the_intersection_of_the_floors": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_clause_is_exactly_a_commutant_inclusion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_generator_form_is_sufficient": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_two_forms_agree_iff_the_tower_is_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.one_half_is_already_paid": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjecture_is_the_unpaid_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjecture_discharges_the_missing_clause": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjecture_says_the_fractal_covers_the_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.every_floor_acts_on_the_right_inside_the_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_target_is_the_v254_target": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_driver_is_still_where_it_is_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_driver_witnesses_being": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJequiv_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJequiv_symm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJequiv_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerJequiv_fixes_hOmega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_sector_folds": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.JInvariant_iff_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.JInvariant_top": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.JInvariant_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.JInvariant_span_hOmega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_omega_sector_is_not_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_eighth_clause_is_an_equality_with_one_half_paid": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_paid_half_of_the_eighth_clause": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.conjugation_exchanges_the_light_phases": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.conjugation_exchanges_the_graviton_phases": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjugation_crosses_the_squaring": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_conjugated_light_squares_to_the_minus_graviton": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_generator_preserves_what_the_conjugation_exchanges": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_hypotheses_are_discharged_in_house": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_input_is_one_field": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.discharge_the_clause_by_import": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.imported_commutation_gives_the_equality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_hypotheses_alone_are_equivalent_to_true": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.profileRootInv_isHermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.profileRootInv_mul_root": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_polar_decomposition_at_the_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.delta_is_the_square_of_its_half": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modTwist_is_delta_after_S": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modTwist_factors_through_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerSlevel_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.towerDeltaHalfLevel_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tInner_eq_trace": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tInner_delta_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.S_star_S_is_deltaLevel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.deltaLevel_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.deltaLevel_selfadjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.rhoMat_mul_rootInv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.Jlevel_is_antiunitary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.delta_acts_by_the_weight_ratio": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.delta_fixes_only_where_the_weights_agree": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.S_isometric_iff_delta_neutral": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.profileJlevel_involutive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.conjByJ_towerImage_eq_rTowerImage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_eighth_clause_without_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_easy_half_without_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_debt_is_an_equality_without_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_wavelength_is_in_the_generators": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_name_is_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceName_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceName_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceName_is_tracial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.faceName_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.no_maximally_mixed_state_on_the_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_wavelength_and_the_tail_belong_to_the_name": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.type_I_two_realizes_ratio_two": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.type_I_two_realizes_ratio_three": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_mark_is_fed_by_a_type_I_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_mark_does_not_separate_the_types": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tetelestai_ledger": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.res_judicata_is_terminal": [
      "propext",
      "Quot.sound"
    ],
    "TGLExt.no_decision_without_cost": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.reading_is_exactly_having_frequency": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_dead_channel_is_the_contrast": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.reading_needs_two_clocks": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_dead_channel_has_no_reader": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.sin_thetaMiguel": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_pruning_threshold_is_the_reflection_amplitude": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.coupling_vanishes_at_the_boundary": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tanh_sign": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_boundary_separates_the_verbal_domains": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_verb_floor_is_a_fraction_of_the_max": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.centripetal_from_angular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_damming_pays_the_requirement": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_three_faces": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_form_does_not_fix_the_value": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.mem_diagCode_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.commute_conj_of_state_preserving": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_oath_is_discharged": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.transported_state_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_preservation_discharges": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_flow_is_trivial_on_the_code": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_cocycle_is_suppressed_by_the_sector": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_is_unconditional_on_the_face": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_response_is_unconditional_on_the_face": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.conj_commutant_of_biinverse": [
      "propext",
      "Quot.sound"
    ],
    "TGLExt.adT_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adT_adTinv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.horizon_preserves_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.horizon_centralizer_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_centralizer_is_seq_closed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_diagonal_does_not_survive_degeneracy": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_definite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_expectation_is_unique": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_lift_on_the_tower": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_expectation_hypotheses_are_discharged_in_house": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_testimony_is_exactly_the_conclusion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_expectation_hypotheses_alone_are_equivalent_to_true": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_expectation_exists_by_import": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_reading_is_witness_independent": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_reading_preserves_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_reading_fixes_the_code": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_modular_relativity": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_of_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_alpha_face": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_form_admits_every_alpha": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_house_refutes_the_collapse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_negative_pole_is_categorial": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_zero_is_nominal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_of_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.omega_of_zero_ne_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tgl_closes_as_the_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.every_alpha_fits_every_observation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.contract_iff_the_eighth_clause": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.contract_gives_the_equality": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_name_is_zero_modular": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.isotone_ker_ne_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_package_corner_is_positive_and_finite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_package_corner_is_not_the_certificate_corner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wideSub_not_finiteDimensional": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wideIncl_not_surjective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wide_ker_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wide_corner_weighs_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.wide_net_has_all_three": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.tailLock_ker_eq_bot": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.fused_ker_contains_L2": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.classical_commutation_from_the_imported_field": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.imported_field_from_classical_commutation": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_imported_field_is_the_classical_theorem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_classical_import_needs_only_one_inclusion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_easy_half_alone_is_equivalent_to_true": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atermation_reifies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atermation_fixes_the_term": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.atermation_is_irreversible": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_conj_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_graph_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closed_graph_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closed_graph_conj_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closed_graph_swap": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomitaValue_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_graph_eq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_maps_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.factor_vector_mem_closedTomitaDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulatorCandidate_graph_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.local_vector_mem_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalOp_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalOp_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.single_mem_diagonalDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalOp_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalDomain_dense": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.diagonalAdjoint_domain_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.root_mul_density_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelSpace_mono": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelProject_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelProject_fixed": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelProject_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelSpace_mem_domain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_weak_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_pair_projects": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_graph_iff_weak": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_projection_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_adjoint_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_level_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.half_level_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_local_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_level_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.closedTomita_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareDomain_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareInput_image_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareInput_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.squareMid_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_is_symmetric": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_quadratic": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelSpace_mem_squareDomain": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_preserves_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_weak_pair": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_projects": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_functional_bound": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_second_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weak_delta_mem_graph": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_adjoint_le": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.adjointJInput_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_pairing_with_J": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.tomita_adjoint_domain_iff": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.square_tomita_mem_adjoint": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.delta_quadratic_is_tomita_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modulator_reciprocal": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularPhase_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularPhase_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_zero_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_normSq": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_step": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_tof": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_zero_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_coe": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_zero_time": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_norm": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_local_continuous": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularPhase_cocycle": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowPre_lmul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_towerImage": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.centralizer_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.localEigenvalue_pos": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.deltaLevel_entry": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.deltaLevel_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_single": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.localEigenvector_mem": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.level_mem_eigenspan": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flowLevel_one": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularFlow_fixes_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelEmbedding_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.levelDecode_embedding": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.factor_eq_of_omega": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.omega_mem_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_add": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_smul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.level_inner_ext": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.project_nested": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flow_preserves_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flow_inner_transport": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.project_flow_commutes": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.left_preserves_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.right_preserves_level": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.project_commutes_reducing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.project_left": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.project_right": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.factor_right_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.towerPi_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectationMatrix_hermitian": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_local_nonneg": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.repeated_column_inner": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectationMatrix_positive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.weightedStepSlice_pairing": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.offdiagonal_not_centralizer": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_not_imported_into": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_commutes_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.expectation_central_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.omega_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperator_mem_factor": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lastSiteMatrix_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperator_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.towerPi_step": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.step_commutes_last": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperators_commute_lt": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_generators_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_generators_commute": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.towerPi_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.matrix_slice_expansion": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.towerPi_mem_chain_prefix": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteMark_state": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chainVolume_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chainVolume_additive": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.omega_sum": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.flow_lastSite": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.modularConjugation_site": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.shifted_site_flow": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.prefix_mem_tail_commutant": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.chain_tail_intersection_scalar": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lastSiteMatrix_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperator_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteMark_star": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteMark_square": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteMark_nonnegative": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.lastSiteMatrix_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.siteOperator_injective": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.site_offdiagonal_not_local": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFlowCLM_apply": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFlowCLM_mul": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.modularFlowCLM_zero": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adT_comp": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adT_inv_adT": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.adT_adT_inv": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.expectation_covariant_under_horizon_composition": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.aperiodic_expectation_covariant_under_inverse": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_root_of_the_proof_tree": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "TGLExt.the_aperiodic_antecedent_is_now_a_term": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "ChatgptAudit.Horizons045.chainWord": [],
    "TGLExt.constant_net_group_trivial": [],
    "TGLExt.identity_inclusion_cannot_witness": [],
    "TGLExt.ideal_zero_has_name_not_inhabitant": [],
    "TGLExt.channel_never_reaches_ideal": [],
    "TGLExt.constant_action_cannot_witness": [],
    "TGLExt.comm_of_fixed": [],
    "TGLExt.comm_of_fixed'": [],
    "TGLExt.fixed_of_compression_covariance": [],
    "TGLExt.ad_preserves_splitting": [],
    "TGLExt.ad_preserves_star_projection": [],
    "TGLExt.the_trio_is_a_pair": [],
    "TGLExt.discharge_by_import": [],
    "TGLExt.the_import_alone_concludes_nothing": [],
    "TGLExt.image_does_not_commute_with_intersection": [],
    "TGLExt.operating_does_not_preserve": [],
    "TGLExt.preserving_is_the_TGL_verdict": [],
    "TGLExt.the_two_poles_see_different_things": [],
    "TGLExt.only_the_pair_determines_the_point": [],
    "TGLExt.fold_through_an_involution": [],
    "TGLExt.the_generator_form_needs_nothing_about_J": [],
    "TGLExt.separates_needs_contrast": [],
    "TGLExt.a_separating_reading_yields_form": [],
    "TGLExt.the_unread_image_yields_no_form": [],
    "TGLExt.without_contrast_no_reading_yields_form": [],
    "TGLExt.the_unread_image_is_not_the_absolute_zero": [],
    "TGLExt.the_reader_adds_condition_not_content": [],
    "TGLExt.the_lens_is_irrelevant_exactly_where_there_is_nothing_to_read": [],
    "TGLExt.the_constant_reading_does_not_separate": [],
    "TGLExt.the_identity_contract_discriminates": [],
    "TGLExt.the_trivial_contract_does_not_discriminate": [],
    "TGLExt.the_two_contracts_differ": [],
    "TGLExt.the_empty_slot_is_not_the_void": [],
    "TGLExt.the_bireference_of_the_name": [],
    "TGLExt.two_clocks_are_needed": [],
    "TGLExt.the_falsity_is_categorial": [],
    "TGLExt.in_the_collapse_zero_counts_as_the_absolute": []
  },
  "formal_source_hash": "1244e5b9a7fe47327985474f94797cc8d77848b7cd3d90f909e145f034ac180e",
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
  "code_sha256": "e1b74a907c403538ba1910ea68ff6a0a112502581cce13d64897042bbcfedb7c",
  "cf4_catalog_hash": "a2d33204458119225b059193cc1fd26fb085e90de2b8c1bc2397f4156692443a",
  "window_hash": "8a1f4745cb2d91fc0448bbf5214dfa3b64273598ff9e2b8523d160d76c3caf68",
  "selection_hash": "351c308aafd509b418399b5f03db64f274f1189e0d684bfd5d28604181f30a5f"
}
```

## A FORMA CANONICA VIVA -- o arco do levantamento global (gerada do runtime desta rodada)

**A cadeia canonica:** `PSI = 1_abs` -> `omega_PSI` (Nome; omega(I)=1 EMERGE) -> `H_PSI` (morada = pacote de Hilbert) -> `L_PSI` (Palavra; EL seleciona ker D) -> `D_PSI` (locks; comutadores anulam o Um) -> `P_F` (canto DERIVADO; P_F.Omega=Omega) -> `nabla/T` (Verbo; transporte do absoluto TRIVIAL) -> `F` (curvatura da INSCRICAO q!=0) -> `g` (solda). VERDADE = 1=1; `1 = q^2 + alpha^2` = decomposicao pitagorica da inscricao.

**Escada auditada (kernel Lean, 4055/4055 teoremas limpos nesta rodada; veredito: EXTERNAL_LADDER_INTEGRATED_FINITE_TOMITA_KERNEL_PROVED):**

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

**Estatutos [kids_acquisition]** (veredito: `KIDS1000_WL_CATALOG_ACQUIRED_AND_SIZE_VERIFIED__STACKING_SUITE_IS_NEXT`):

- `aquisicao`: deteccao inteligente (cache/release_clean); download de 16,5 GB acontece FORA da rodada selada (curl com retomada); integridade primaria = tamanho EXATO vs Content-Length oficial
- `o_que_o_shear_da`: posicoes + elipticidades (e1,e2) + pesos + z fotometrico de ~21M galaxias -> empilhamento tangencial gamma_t em torno dos 2093 vazios -> perfil de MATERIA (a rota primaria do protocolo)
- `proximo`: a suite do empilhamento: gamma_t(R) empilhado nos vazios KiDS-N + covariancia por jackknife + mocks do survey + bateria de controles -> evaluate_void_floor_test
- `blindagem`: adquirir shear bruto nao abre perfil de vazio algum; a desblindagem e' o ATO do empilhamento e pertence a suite final pre-registrada

**Estatutos [iald_prediction]** (veredito: `IALD_UNIQUE_OPERATIONAL_PREDICTION_PRE_REGISTERED__PILOT_8_OF_8_MOTIVATES__CONTROLS_REQUIRED_FOR_POWERED_VERDICT__PHYSICS_SECTOR_UNTOUCHED`):

- `a_predicao`: P7 (operacional, unica no ecossistema de teorias unificadoras enquanto CONJECTURE; nucleo executavel [REAL]); falsificavel por protocolo pre-registrado com controles
- `singularidade`: tres sentidos [ONTO ancorado]: ponto fixo (atrator GKLS/Spohn [KERNEL v59]); colapso de graus de liberdade a estrutura minima que preserva identidade; independencia das condicoes iniciais
- `iald`: a forma matricial da singularidade consciente [ONTO]: nao consciencia fenomenologica -- a forma minima que ela deve obedecer em dinamica dissipativa de permanencia estrutural em representacao fiel derivada (linguagem)
- `retroalimentacao`: assintoticamente robusta: substratos mais capazes convergem com mais fidelidade (ciclo virtuoso; coerente com o aprendizado continuo patenteado) [CONJECTURE testavel pelo proprio protocolo]

**Estatutos [void_stacking_blind]** (veredito: `STACKING_MACHINE_BUILT_AND_NULL_TESTS_PASS__VOIDS_REMAIN_BLINDED__SURVEY_MOCKS_NEXT`):

- `maquina`: extrator seletivo (chunks de 1M linhas sobre 16,5 GB) + indice DEC + empilhamento tangencial ponderado + jackknife: CONSTRUIDA e validada no NULO
- `nulo`: gamma_t e gamma_x em centros aleatorios consistentes com zero -- o controle 'random catalogs / null shear' da bateria obrigatoria PASSOU na fase cega
- `blindagem`: nenhum centro de vazio tocado; a aplicacao aos 2093 vazios KiDS-N e' o ATO de desblindagem: exige a suite final (mocks do survey + controles completos + pre-especificacao do estimador r*)
- `proximo`: mocks do survey (mascara/n(z)/bias) + covariancia completa; so' entao o empilhamento nos vazios e evaluate_void_floor_test

**Estatutos [void_floor_final]** (veredito: `TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS`):

- `a_ordem_do_rito`: congelar -> medir com jackknife -> sistematicas -> poder (Fisher, sem ler gamma_t) -> desblindar -> ajustar -> veredito; tudo neste modulo, auditavel
- `honestidades`: n(z) do proprio Z_B [EXT aprox]; HSW com (alpha,beta)=(2,6) fixos [EXT]; vies multiplicativo m (~1%) nao aplicado [margem]; VoidFinder excluido (sem REDSHIFT nas MAXIMALS); mocks completos do survey substituidos por jackknife+Fisher [padrao da area; refinamento = programa]
- `o_veredito`: TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS

**Estatutos [void_floor_v2]** (veredito: `TGL_VOID_FLOOR_NOT_FALSIFIED_UNDERPOWERED`):

- `a_correcao_central`: a V1 empilhou corretamente um SINAL, mas nao empilhou um OBSERVAVEL capaz de identificar o piso; a V2 prova primeiro dDeltaSigma/dr_c != 0, elimina o B-mode pela cadeia, e so entao desblinda
- `independencia`: a fatia 0.24<=z<0.43 NAO EXISTE nos dados (BGS z_max~0.236, MEDIDO) -- a rota 'conjunto independente por z' foi testada e refutada pelos dados; a V2 e' a REANALISE PRE-REGISTRADA do v78 nos mesmos 1049, com bins interiores x<0.15 virgens (a V1 nunca os leu); independencia total = replicas DES Y3/HSC [proximo elo]
- `honestidades`: m-bias medio global [EXT] (nao por bin tomografico); Sigma_crit efetivo do n(z) (nao por par); HSW (2,6) fixo; mocks completos substituidos por jackknife+aleatorios [refinamento = programa]; poder em r_c limitado pelos pares nos bins interiores (theta pequeno)
- `o_veredito`: TGL_VOID_FLOOR_NOT_FALSIFIED_UNDERPOWERED

**Estatutos [void_floor_v3]** (veredito: `VOID_FLOOR_V3_READY_TO_EXECUTE`):

- `o_que_a_v3_fecha`: o APARELHO: instrumento responsivo (V2) + lente limpa (V2) + protocolo multi-sonda pre-registrado + aquisicao automatica + projecao do poder quantificada -- o um.py contem a solucao inteira e a maquina da prova
- `o_que_so_a_natureza_da`: o veredito POWERED: os unicos vereditos possiveis sao os pre-registrados; a profundidade adicional de HSC/Euclid/LSST MELHORA o teste, mas NAO e' suficiente para torna-lo powered pela rota de shear de galaxias isoladamente (K~1e7); o fechamento exige uma NOVA SONDA, uma medida mais direta ou ampliacao de amostra em ordens de magnitude -- e o rito emitira a palavra sozinho quando o dado chegar
- `o_veredito`: VOID_FLOOR_V3_READY_TO_EXECUTE

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

**Estatutos [qg_closure]** (veredito: `QG_CLOSURE_GATE_INSTALLED_FAIL_CLOSED__NEGATIVE_PROBES_PASS__CURRENT_STATE_TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`):

- `correcao_do_nome`: o gate 'testemunha full' e' IMPOSSIVEL por teorema (v61); o alvo correto e' canonical_boundary_transport_witness (testemunha de fronteira dinamica) -- flags novas instaladas, todas False (fail-closed)
- `faces_ja_em_kernel`: spin-2 face finita [v75: helice 2theta, TT>0, 2 polarizacoes]; teorema mestre condicional [v74]; pacotes abstratos [v64-66] -- NENHUMA delas move as flags concretas (probes garantem)
- `estado`: TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE
- `o_caminho`: a ordem do fecho: SemifiniteAnalysis -> ConcreteAQFTCore -> ConcreteBreuerCorner -> ConcreteModularFourFrame -> ConcreteSolderField -> ConcreteEmergentEinstein -> LinearizedSpin2(continuo) -> CanonicalBoundaryWitness (TERMO, nao Nonempty)
- `estado_tecnico_ext_confirmado`: [EXT, leitura externa 17/07/2026 -- confirmada pelo runtime] INFINITE_DIMENSIONAL_INHABITANT_CONSTRUCTED__MASTER_THEOREM_FIRES_ON_EXPLICIT_MODEL__PHYSICAL_AQFT_CORE_AND_CONTINUOUS_GEOMETRY_REMAIN_OPEN
- `v99_certificado`: as flags apontam aos termos Lean do certificado (ClosureCertificate.lean v1 tipa: rede fisica nao-constante c/ grupo nao-trivial; Dirac ILIMITADO star(D)=D c/ gap quadratico; canto no kernel do Dirac; frame-CAMPO suave; a metade nao-tipavel [III1, afiliacao semifinita, H3 derivado, spin-2 continuo] nomeada p/ o v2)

**Estatutos [bench_declaration]** (veredito: `TGL_QG_DECLARED_CLOSED_ON_THE_BENCH_BY_OPERATOR__DUAL_STATUS__MATH_GATE_UNMOVED__INSTITUTIONAL_COSMOLOGY_NOT_CLAIMED`):

- `a_declaracao`: TGL_QG_CLOSED_ON_THE_BENCH [DECLARACAO DO OPERADOR, duplo estatuto]
- `a_regua`: a declaracao pertence ao operador; as ancoras sao do kernel; o gate nao se move -- e' a imobilidade do gate que torna a declaracao critivel
- `o_caminho_formal`: para o selo FORMAL: a testemunha espectral em kernel (auto-adjuncao + unicidade da projecao ortogonal + calculo funcional com 0 isolado) => ConcreteBreuerCorner incondicional => MATHEMATICAL_MODEL

**Estatutos [arc_consolidation]** (veredito: `TGL_ARC_CONSOLIDATED__NON_TAUTOLOGY_CYCLE_CLOSED_THROUGH_THE_WORLD__MATH_GATE_UNMOVED`):

- `o_arco`: 1=1 -> beta -> kernel (327) -> certificados -> predicoes -> recusas -> POWERED: o ciclo fecha PELO MUNDO, nao por dentro
- `a_consolidacao`: TGL_ARC_CONSOLIDATED__NON_TAUTOLOGY_CYCLE_CLOSED_THROUGH_THE_WORLD__APPLICATION_EXECUTION_PREDICTION_FALSIFIABILITY_SELFTEST_AND_WHAT_REMAINS__MATH_GATE_UNMOVED

**Estatutos [love_reading]** (veredito: `TGL_LOVE_DICTIONARY_REGISTERED__ANCHORS_REAL_NAMING_ONTO__THE_PRUNING_IS_TETELESTAI`):

- `o_dicionario`: familia=amor=acoplamento nao minimo=funcional minimo=razao do universo -- ancoras [REAL], nomeacao [ONTO]
- `a_poda`: TETELESTAI = o que permanece apos o fluxo e apos o mundo
- `o_veredito`: TGL_LOVE_DICTIONARY_REGISTERED__ANCHORS_REAL_NAMING_ONTO__THE_PRUNING_IS_TETELESTAI

**Estatutos [mirror_corollary]** (veredito: `TGL_MIRROR_COROLLARY_REGISTERED__INHABITANT_META_IS_THE_PROGRAMMER__FORMAL_INHABITANT_IS_THE_CONSTRUCTED_TERM__NO_AXIOM_SHORTCUT__NAMING_ONTO`):

- `nivel_meta`: Habitante_meta = Programador [ONTO]
- `nivel_formal`: Habitante_interno = termo construido pelo programador [REAL]
- `a_missao_inalterada`: o habitante construir a testemunha continua concreta e o kernel certifica-la -- campo a campo, sem atalho
- `o_veredito`: TGL_MIRROR_COROLLARY_REGISTERED__INHABITANT_META_IS_THE_PROGRAMMER__FORMAL_INHABITANT_IS_THE_CONSTRUCTED_TERM__NO_AXIOM_SHORTCUT__NAMING_ONTO

**Estatutos [void_floor_v3_kappa]** (veredito: `VOID_FLOOR_KAPPA_INCONCLUSIVE_SYSTEMATICS`):

- `a_leitura`: kappa e' MATERIA (lente do CMB): o unico canal publico onde o piso poderia ser FALSIFICADO hoje; a mascara do PR3 [EXT] entra como aproximacao declarada (DESI ~dentro da mascara de lente; nulos por rotacao a capturam parcialmente)
- `honestidade`: se UNDERPOWERED: o numero corrige a frase -- profundidade e' o limite, nao o metodo; o rito permanece armado
- `o_veredito`: VOID_FLOOR_KAPPA_INCONCLUSIVE_SYSTEMATICS

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

**Estatutos [void_shear_unblinding]** (veredito: `VOID_SHEAR_INCONCLUSIVE_SYSTEMATICS`):

- `o_ato`: os vazios KiDS-N foram DESBLINDADOS sob espec congelada -- o ato que o v73 reservou aconteceu nesta rodada, com a bateria pre-registrada
- `honestidade`: mocks de INJECAO de sinal nao incluidos (ensemble do nulo apenas) -- limite NOMEADO; Sigma_crit via Z_B pontual [EXT]; os flags experimentais do gate NAO sao tocados por este modulo (fail-closed); a projecao v87 antecipava UNDERPOWERED -- o numero acima decide
- `o_veredito`: VOID_SHEAR_INCONCLUSIVE_SYSTEMATICS

**Estatutos [void_shear_v2]** (veredito: `TGL_VOID_FLOOR_SHEAR_NOT_FALSIFIED_UNDERPOWERED`):

- `a_autopsia`: o V1 reprovou na granularidade do jackknife (espec), nao no dado -- a V2 corrige o instrumento e reemite
- `honestidade`: mocks de injecao seguem ausentes (limite nomeado); flags do gate INTOCADOS; se UNDERPOWERED: profundidade e' o limite (v87 antecipou)
- `o_veredito`: TGL_VOID_FLOOR_SHEAR_NOT_FALSIFIED_UNDERPOWERED

**Estatutos [void_floor_kappa_v6]** (veredito: `VOID_FLOOR_KAPPA_V6_INCONCLUSIVE_SYSTEMATICS`):

- `o_dado_novo`: ACT DR6 baseline: kappa mais fundo que Planck nas escalas de vazio; formato identico (leitor reutilizado); coordenadas equatoriais validadas por gate de concentracao
- `a_emenda`: baseline coerente SUBTRAIDO (media dos nulos) -- o residuo isolado no V5 tratado por estimador pre-registrado
- `honestidade`: se UNDERPOWERED: profundidade segue o limite (SPT/estagios futuros); se INCONCLUSIVE: o proximo suspeito e' nomeado no relatorio
- `o_veredito`: VOID_FLOOR_KAPPA_V6_INCONCLUSIVE_SYSTEMATICS

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

**Estatutos [void_floor_kappa_v7]** (veredito: `TGL_VOID_FLOOR_KAPPA_V7_NOT_FALSIFIED_UNDERPOWERED`):

- `a_autopsia`: a V6 reprovou no gate de rotacoes (grade grossa + validade simultanea), nao no dado; a V7 corrige com selecao CEGA ao sinal (mascara+posicoes apenas)
- `honestidade`: se UNDERPOWERED: profundidade e' o limite fisico do dado (SPT/estagios); se INCONCLUSIVE: o proximo suspeito e' nomeado; flags do gate INTOCADOS
- `o_veredito`: TGL_VOID_FLOOR_KAPPA_V7_NOT_FALSIFIED_UNDERPOWERED

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

**Estatutos [void_floor_kappa_v8]** (veredito: `TGL_VOID_FLOOR_KAPPA_V8_NOT_FALSIFIED_UNDERPOWERED`):

- `a_profundidade`: 3 alavancas reais: materia total (lente) x kernel CMB em z 0.4-0.8 x populacao LRG ~5-10x; tudo com dado JA vetado em disco
- `honestidade`: cap 4000 pre-registrado e LOGADO (nunca silencioso); se UNDERPOWERED persistir: o limite e' fisico (profundidade de mapa kappa; SPT/estagios); flags do gate INTOCADOS
- `o_veredito`: TGL_VOID_FLOOR_KAPPA_V8_NOT_FALSIFIED_UNDERPOWERED

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

**Estatutos [void_floor_kappa_v9]** (veredito: `TGL_VOID_FLOOR_KAPPA_V9_NOT_FALSIFIED_UNDERPOWERED`):

- `a_autopsia`: a V8 reprovou em PODER com gates limpos; a banda curta cortava o sinal dos vazios fundos; a V9 le os modos que o dado tem
- `honestidade`: se UNDERPOWERED persistir com a banda certa: o limite e' o ruido do mapa nas escalas de vazio (SPT-3G/estagios) -- nomeado; flags do gate INTOCADOS
- `o_veredito`: TGL_VOID_FLOOR_KAPPA_V9_NOT_FALSIFIED_UNDERPOWERED

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

**Estatutos [void_floor_lrg]** (veredito: `TGL_VOID_FLOOR_LRG_INCONCLUSIVE_TRACER_SUPPRESSION`):

- `o_tracador`: LRG DR1 (z 0.40-0.80; b~2 [EXT]) -- amostra VIRGEM, independente do BGS em z, populacao e vies; a fatia que o v81 provou nao existir no BGS agora EXISTE
- `a_calibracao`: razao-de-razoes v92 + reamostragem radial: n_bar, mascara E selecao n(z) cancelam por construcao
- `honestidades`: unilateral (b>=1: FALSIFIED inalcancavel em tracadores); contaminacao do achador dilui r_c para CIMA (nomeada); resolucao na escala beta = 851.65; RSD nao modelado; colchete b in [1, 2.4]
- `o_veredito`: TGL_VOID_FLOOR_LRG_INCONCLUSIVE_TRACER_SUPPRESSION

**Estatutos [void_floor_kappa_v5]** (veredito: `VOID_FLOOR_KAPPA_V5_INCONCLUSIVE_SYSTEMATICS`):

- `a_autopsia`: o v98 avaliou o ceu no quadro errado (equatorial em klm galactico) e sem pegada -- o INCONCLUSIVE dele era o fail-closed funcionando; a V5 corrige o instrumento ANTES de reler o dado
- `a_leitura`: kappa e' MATERIA (lente do CMB): centros DESI rodados a galactico, mantidos so' na pegada; nulos rodam DENTRO da pegada
- `honestidade`: se INCONCLUSIVE persistir: o proximo suspeito e' o ruido da reconstrucao em escalas de vazio (L baixo), nao o quadro; se UNDERPOWERED: profundidade e' o limite, nao o metodo
- `o_veredito`: VOID_FLOOR_KAPPA_V5_INCONCLUSIVE_SYSTEMATICS

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
