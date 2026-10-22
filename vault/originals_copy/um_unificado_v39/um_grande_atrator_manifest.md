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
    "cf4_ok": false,
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
    "cf4_ok": false,
    "result_obtained": "CF4 ausente nesta execucao",
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
    ]
  },
  "formal_source_hash": "07f9c3d27506b818c8c7aaf9dc50f377e20b6e32e3e93d006cb18ddbeafadafe",
  "verdict": "TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_OPEN",
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
    "zero_mod_state": true,
    "zero_mod_note": "vazio tipado: a interface-luz especificada, ainda nao realizada",
    "one_inscribed": false,
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
    "lean_kernel_full_witness_constructed": false,
    "physical_covariant_representative_selected": false,
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
    "lean_kernel_full_witness_constructed": false,
    "physical_covariant_representative_selected": false
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
  "code_sha256": "57f81e820023e51fbf78e3526a80ff2f679a5501cf9fd006705abc8f44c6e466",
  "cf4_catalog_hash": null,
  "window_hash": null,
  "selection_hash": null
}
```
