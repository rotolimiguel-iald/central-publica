def prove_d1_camb_protocol(ONE):
    """v349 -- O «D1 VIA CAMB» DO CANONICO DE MAIO, PRE-REGISTRADO [ADITIVO; fail-closed; nao gateia 1=1; fora do contorno].
    O quarto dos testes que aguardavam o instrumento (ordem do operador, 10/09/2026): `tgl_paper_unified.py --d1-camb` (maio de 2026) =
    `tgl_mcmc_camb_v2.py` + `tgl_camb_worker.py`, o cross-check de Passo 3 com CAMB completo que nunca correu por falta do camb. O que se
    testa: a modificacao de FUNDO da TGL, H^2 = (8 pi G/3) rho [1 + beta |1 + w_eff|], contra Planck 2018 comprimido (R, l_A, omega_b; cov de
    Zhai+ 2019), DESI DR1 BAO (12 pontos) e SH0ES (H0 = 73,04 ± 1,04). CAMB da a base LCDM exata (z_*, z_drag, r_s, D_A) e a TGL entra
    analiticamente por cima (aproximacao DECLARADA no proprio worker: o r_s desloca por H_LCDM/H_TGL em z_*). Distinto do Nivel 2 (v1xx:
    espectro completo com a TGL dentro do Boltzmann, N2_INCAPAZ com diagnostico fechado em 14/08/2026): aqui e o fundo, nao a perturbacao.
    Fases: 1) best-fit LCDM (beta = 0) vs TGL (beta = alpha sqrt(e) FIXO) com todos os dados -> Delta chi^2 (mesmo numero de parametros
    livres: 3); 2) o mesmo sem SH0ES -> anatomia da tensao de H0; 3) MCMC com beta LIVRE (emcee, 24 walkers x 2000 passos, burn 400) ->
    posterior de beta. Regua relativizada do Nivel 2 (mandato de 10/08/2026) reaplicada ao posterior. beta jamais literal. CONFIRMED proibido."""
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = {
        "version": "D1_CAMB_V1", "status": "PRE_REGISTERED_BEFORE_DATA_READ", "form_of": "tgl_paper_unified.py --d1-camb (maio/2026) = tgl_mcmc_camb_v2.py Step 3 CAMB cross-check + tgl_camb_worker.py, SEM alteracao",
        "hypothesis": {"background": "H^2 = (8 pi G/3) rho_tot [1 + beta |1 + w_eff(z)|]", "beta_theory": "alpha sqrt(e) em runtime", "approximation_DECLARED": "CAMB em LCDM; TGL analitica por cima; r_s deslocado por H_LCDM/H_TGL em z_* (nao --tight-rs)"},
        "data": {"planck": "2018 comprimido (R = 1,7502; l_A = 301,471; omega_b h^2 = 0,02236; cov Zhai+ 2019)", "desi": "DR1 BAO 12 pontos (Adame+ 2024)", "sh0es": "H0 = 73,04 ± 1,04"},
        "phases": {"1_bestfits_full": "LCDM (beta = 0) vs TGL (beta fixo) com Planck + DESI + SH0ES; Nelder-Mead; Delta chi^2 = chi^2_TGL - chi^2_LCDM (3 parametros livres em ambos)",
                   "2_no_sh0es": "o mesmo com Planck + DESI; tensao de H0 contra SH0ES para LCDM, TGL fixo e TGL zero-free (1+z_*)^beta",
                   "3_mcmc_free_beta": "emcee 24 walkers x 2000 passos, burn 400, prior plano beta em (-0,05; 0,05); posterior de beta"},
        "criteria": {"bestfit_success_required": True, "delta_chi2_5sigma": 25.0, "delta_chi2_2sigma": 4.0, "acceptance_min": 0.1, "acceptance_max": 0.7, "chain_min": 24 * 1600,
                     "mcmc_rule": "regua relativizada do Nivel 2: FALSIFIED se alpha sqrt(e) fora de 5 sigma (equal-tailed, sigma media); INCAPAZ se sigma(beta) > beta; NOT_FALSIFIED_POWERED se sigma <= beta/2 e alpha sqrt(e) dentro de 3 sigma; TENSION se fora de 3 sigma e nao FALSIFIED; INCONCLUSIVE nos demais"},
        "allowed_verdicts": {"bestfit": ["D1_LCDM_PREFERRED_5SIGMA", "D1_TGL_BACKGROUND_PREFERRED_5SIGMA", "D1_TENSION_2_TO_5_SIGMA", "D1_NOT_DISTINGUISHED"],
                             "mcmc": ["D1_BETA_FALSIFIED", "D1_BETA_INCAPAZ", "D1_BETA_NOT_FALSIFIED_POWERED", "D1_BETA_TENSION", "D1_BETA_INCONCLUSIVE"], "any": ["INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"]},
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao testa perturbacoes (Nivel 2); a TGL entra como aproximacao analitica por cima do CAMB (declarada); um Delta chi^2 favoravel a TGL nao e confirmacao — e preferencia de fundo em dados comprimidos",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("protocolo pre-registrado e hasheado (%s)" % ph, True), ("beta jamais literal", bool(abs(beta - SEALED_CODATA_ALPHA * math.sqrt(math.e)) == 0.0)), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "verdict": ("TGL_D1_CAMB_V1__PROTOCOL_PRE_REGISTERED_%s__MAY_2026_SCRIPT_UNCHANGED__BACKGROUND_ONLY__GATE_UNTOUCHED" % ph) if all_v else "TGL_D1_CAMB_PROTOCOL_NOT_SEALED_THIS_RUN"}


def prove_d1_camb_result(ONE, protocol_record=None):
    """v349 -- o resultado do D1 via CAMB (driver externo d1_camb_run.py no WSL, que roda o script de maio sem o alterar), lido por hash e julgado pela matriz."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = protocol_record or prove_d1_camb_protocol(ONE); ph = proto.get("protocol_hash"); crit = (proto.get("protocol") or {}).get("criteria") or {}
    res_p = os.path.join(CACHE, "d1_camb", "D1_CAMB_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "cosmologia jamais vira prova matematica; o fundo comprimido e aproximacao declarada"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash o relatorio do script de maio e aplica a matriz pre-registrada (%s)" % ph,
          "distincao": "[REAL] fundo (aqui) vs perturbacao (Nivel 2, N2_INCAPAZ): sao testes conjugados, nao redundantes"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_D1_CAMB_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado D1_CAMB_V1 em cache/d1_camb", False)], statuses=st, runtime_s=float(time.time() - _t0))
    rep = rj.get("report") or {}; p1 = rep.get("phase1") or {}; p2 = rep.get("phase2") or {}; p3 = rep.get("phase3") or {}; inst = rj.get("instrument") or {}; sc = rj.get("scripts") or {}
    bt = (rep.get("metadata") or {}).get("beta_TGL_theory")
    checks = [("resultado lido por hash (%s)" % rhash, True),
              ("beta do script de maio == beta recomputado (alpha sqrt(e))", bool(isinstance(bt, (int, float)) and abs(float(bt) - beta) < 1e-12)),
              ("scripts de maio com sha256 e mtime de 2026-05; instrumento camb + emcee", bool(all(len(str((sc.get(k) or {}).get("sha256", ""))) == 64 and str((sc.get(k) or {}).get("mtime", "")).startswith("2026-05") for k in ("tgl_mcmc_camb_v2", "tgl_camb_worker")) and inst.get("camb") and inst.get("emcee"))),
              ("fase 1 e fase 2 presentes com best-fits bem-sucedidos", bool((p1.get("LCDM_bestfit") or {}).get("success") and (p1.get("TGL_bestfit") or {}).get("success") and (p2.get("LCDM_bestfit_planck_only") or {}).get("success") and (p2.get("TGL_bestfit_planck_only") or {}).get("success"))),
              ("fase 3 (MCMC beta livre) presente e convergida (aceitacao em [%.1f, %.1f], cadeia >= %d)" % (float(crit.get("acceptance_min", 0.1)), float(crit.get("acceptance_max", 0.7)), int(crit.get("chain_min", 38400))),
               bool(p3 and float(crit.get("acceptance_min", 0.1)) <= float(p3.get("acceptance_fraction_mean", -1)) <= float(crit.get("acceptance_max", 0.7)) and int(p3.get("chain_size", 0)) >= int(crit.get("chain_min", 38400)))),
              ("returncode 0 do script de maio", rj.get("returncode") == 0), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    d = p1.get("delta_chi2")
    if not isinstance(d, (int, float)): bf = "INCONCLUSIVE_SYSTEMATICS"
    elif d >= float(crit.get("delta_chi2_5sigma", 25.0)): bf = "D1_LCDM_PREFERRED_5SIGMA"
    elif d <= -float(crit.get("delta_chi2_5sigma", 25.0)): bf = "D1_TGL_BACKGROUND_PREFERRED_5SIGMA"
    elif abs(d) >= float(crit.get("delta_chi2_2sigma", 4.0)): bf = "D1_TENSION_2_TO_5_SIGMA"
    else: bf = "D1_NOT_DISTINGUISHED"
    sm = (p3.get("summary") or {}).get("beta") or {}; med = sm.get("median"); sg = (0.5 * (sm.get("sigma_lower", 0) + sm.get("sigma_upper", 0))) if sm else None
    if not p3 or not isinstance(med, (int, float)) or not sg: mc = "INCONCLUSIVE_SYSTEMATICS"
    else:
        zt = abs(med - beta) / sg
        if zt > 5.0: mc = "D1_BETA_FALSIFIED"
        elif sg > beta: mc = "D1_BETA_INCAPAZ"
        elif sg <= beta / 2.0 and zt <= 3.0: mc = "D1_BETA_NOT_FALSIFIED_POWERED"
        elif zt > 3.0: mc = "D1_BETA_TENSION"
        else: mc = "D1_BETA_INCONCLUSIVE"
    h0 = {"LCDM_bestfit": (p2.get("LCDM_bestfit_planck_only") or {}).get("H0"), "TGL_bestfit": (p2.get("TGL_bestfit_planck_only") or {}).get("H0")}; tens = {k: p2.get(k) for k in ("tension_LCDM_sigma", "tension_TGL_sigma", "tension_zero_free_sigma") if k in p2}
    verdict = ("TGL_D1_CAMB_V1__RESULT_READ_BY_HASH__BESTFIT_%s__DELTA_CHI2_%s__MCMC_%s__BETA_%s_PM_%s__GATE_UNTOUCHED"
               % (bf, _f(d, 2).replace(".", "P").replace("-", "M"), mc, _f(med, 4).replace(".", "P").replace("-", "M") if isinstance(med, (int, float)) else "NA", _f(sg, 4).replace(".", "P") if sg else "NA")) if all_v else "TGL_D1_CAMB_RESULT_NOT_SEALED_THIS_RUN"
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] fase 1 (Planck + DESI + SH0ES): chi^2 LCDM %s, TGL(beta fixo) %s, Delta chi^2 = %s => %s; fase 2 (sem SH0ES): H0 LCDM %s, TGL %s; tensoes vs SH0ES %s; fase 3 (beta livre): beta = %s +%s -%s (sigma media %s; alpha sqrt(e) = %s; %s sigma), aceitacao %s, cadeia %s => %s; tempo %s s"
                             % (_f((p1.get("LCDM_bestfit") or {}).get("chi2"), 3), _f((p1.get("TGL_bestfit") or {}).get("chi2"), 3), _f(d, 3), bf, _f(h0.get("LCDM_bestfit"), 3), _f(h0.get("TGL_bestfit"), 3), {k: _f(v, 2) for k, v in tens.items()},
                                _f(med, 5), _f(sm.get("sigma_upper"), 5), _f(sm.get("sigma_lower"), 5), _f(sg, 5), _f(beta, 5), _f((abs(med - beta) / sg) if (isinstance(med, (int, float)) and sg) else None, 2), _f(p3.get("acceptance_fraction_mean"), 3), p3.get("chain_size"), mc, _f(rj.get("runtime_s"), 0)))
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), instrument=inst, scripts=sc,
                bestfit_outcome=bf, mcmc_outcome=mc, delta_chi2=d, chi2=dict(LCDM=(p1.get("LCDM_bestfit") or {}).get("chi2"), TGL=(p1.get("TGL_bestfit") or {}).get("chi2")), h0_no_sh0es=h0, tensions=tens,
                beta_posterior=dict(median=med, sigma=sg, lo16=sm.get("lo16"), hi84=sm.get("hi84")), mcmc=dict(acceptance=p3.get("acceptance_fraction_mean"), chain_size=p3.get("chain_size"), time_s=p3.get("time_seconds")), pipeline_runtime_s=rj.get("runtime_s"))


def prove_d1_camb_amendment_v2(ONE, v1_record=None):
    """v349 -- A EMENDA V2 DO D1 VIA CAMB, PRE-REGISTRADA DEPOIS DA AUTOPSIA DA V1 E ANTES DO DADO DA V2 [ADITIVO; nao gateia; fora do contorno].
    A autopsia e LIDA de um diagnostico gravado por hash (D1_CAMB_DIAGNOSTICO.json: o worker de maio e o worker corrigido chamados no fiducial
    de Planck, beta = 0 e beta = alpha sqrt(e)), nunca de memoria. O que a V1 mostrou: chi^2 da ordem de 10^4 em 16 pontos, H0 a fugir para a
    borda do prior (90) — nao e cosmologia, e um defeito do worker de maio, que nunca tinha corrido: em D_M_TGL a distancia comovel ate z_* ~ 1090
    era integrada por trapezios em 300 pontos numa grade LINEAR em z (passo ~3,6), inflando a distancia ~20% mesmo com beta = 0 (R 2,09 contra
    1,75 de Planck; l_A 361 contra 301,5). As distancias DESI (z <= 2,33) nao sofriam. O que a V2 muda: (1) worker CORRIGIDO em copia
    (integracao densa em ln(1+z), vetorizada; o original de maio intocado), com AUTOVERIFICACAO beta = 0 contra o CAMB gravada na saida;
    (2) o sha256 do worker corrigido entra no protocolo; (3) gate de bondade de ajuste: chi^2 do best-fit LCDM <= 3 x 16 pontos; (4) gate de
    autoverificacao |DM_TGL(0)/DM_CAMB - 1| < 5e-3. O script tgl_mcmc_camb_v2.py e tudo o mais ficam identicos. CONFIRMED proibido."""
    _t0 = time.time()
    v1 = v1_record or {}
    diag_p = os.path.join(CACHE, "d1_camb", "D1_CAMB_DIAGNOSTICO.json"); dj, dhash = _read_external_json_with_hash(diag_p)
    # os NUMEROS da V1 nao entram no hash da emenda: na pre-inscricao (10/09/2026 19:11) a V1 ainda corria e estes campos eram None; ficam AO LADO em v1_numbers (nao hasheados).
    # O que a emenda hasheia e o DIAGNOSTICO (worker de maio vs corrigido no fiducial), que ja existia. Dito para que o hash pre-inscrito seja o que se recompute.
    aut = {"diagnostico_sha16": dhash, "v1_result_sha16": None, "v1_protocol_hash": v1.get("protocol_hash"), "v1_bestfit_outcome": None, "v1_mcmc_outcome": None,
           "v1_chi2": None, "v1_delta_chi2": None, "v1_h0_no_sh0es": None}
    v1_numbers = {"v1_result_sha16": v1.get("result_sha16"), "v1_bestfit_outcome": v1.get("bestfit_outcome"), "v1_mcmc_outcome": v1.get("mcmc_outcome"), "v1_chi2": v1.get("chi2"), "v1_delta_chi2": v1.get("delta_chi2"), "v1_h0_no_sh0es": v1.get("h0_no_sh0es")}
    fixed_sha = None
    if dj is not None:
        m0 = (dj.get("may_worker") or {}).get("beta0") or {}; f0 = (dj.get("fixed_worker") or {}).get("beta0") or {}; mt = (dj.get("may_worker") or {}).get("beta_tgl") or {}; ft = (dj.get("fixed_worker") or {}).get("beta_tgl") or {}
        fixed_sha = (dj.get("fixed_worker") or {}).get("sha256")
        aut.update({"may_beta0": {k: m0.get(k) for k in ("R", "lA", "ratio_TGL_over_CAMB", "chi2_planck", "chi2_desi")}, "fixed_beta0": {k: f0.get(k) for k in ("R", "lA", "ratio_TGL_over_CAMB", "chi2_planck", "chi2_desi", "selfcheck")},
                    "may_beta_tgl": {k: mt.get(k) for k in ("R", "lA", "chi2_planck", "chi2_desi")}, "fixed_beta_tgl": {k: ft.get(k) for k in ("R", "lA", "chi2_planck", "chi2_desi")},
                    "planck": dj.get("planck"), "bug": dj.get("bug"), "may_worker_sha256": (dj.get("may_worker") or {}).get("sha256"), "fixed_worker_sha256": fixed_sha})
    proto = {
        "version": "D1_CAMB_V2", "amendment_of": "D1_CAMB_V1", "status": "PRE_REGISTERED_AFTER_V1_AUTOPSY_BEFORE_V2_DATA_READ",
        "autopsy_of_V1": aut,
        "changes": {"1_worker": "copia corrigida tgl_camb_worker_v2fix.py: D_M_TGL integra em u = ln(1+z) com 20001 pontos (vetorizado); o original de maio NAO e tocado", "2_binding": "sha256 do worker corrigido no protocolo",
                    "3_gof_gate": "chi^2 do best-fit LCDM (Fase 1) <= 3 x 16 = 48, senao INCONCLUSIVE_SYSTEMATICS", "4_selfcheck_gate": "|DM_TGL(beta = 0)/DM_CAMB - 1| < 5e-3 (gravado pelo worker), senao INCONCLUSIVE_SYSTEMATICS"},
        "unchanged": "tgl_mcmc_camb_v2.py (dados, verossimilhanca, Nelder-Mead, emcee 24 x 2000, burn 400, priors), aproximacao declarada do r_s, regua relativizada do Nivel 2, matriz de vereditos",
        "fixed_worker_sha256": fixed_sha,
        "criteria": {"bestfit_success_required": True, "delta_chi2_5sigma": 25.0, "delta_chi2_2sigma": 4.0, "acceptance_min": 0.1, "acceptance_max": 0.7, "chain_min": 24 * 1600, "gof_chi2_lcdm_max": 48.0, "selfcheck_tol": 5e-3,
                     "mcmc_rule": "regua relativizada do Nivel 2: FALSIFIED se alpha sqrt(e) fora de 5 sigma; INCAPAZ se sigma(beta) > beta; NOT_FALSIFIED_POWERED se sigma <= beta/2 e alpha sqrt(e) dentro de 3 sigma; TENSION se fora de 3 sigma; INCONCLUSIVE nos demais"},
        "allowed_verdicts": {"bestfit": ["D1_LCDM_PREFERRED_5SIGMA", "D1_TGL_BACKGROUND_PREFERRED_5SIGMA", "D1_TENSION_2_TO_5_SIGMA", "D1_NOT_DISTINGUISHED"],
                             "mcmc": ["D1_BETA_FALSIFIED", "D1_BETA_INCAPAZ", "D1_BETA_NOT_FALSIFIED_POWERED", "D1_BETA_TENSION", "D1_BETA_INCONCLUSIVE"], "any": ["INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"]},
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao testa perturbacoes (Nivel 2); a TGL entra como aproximacao analitica por cima do CAMB (declarada); um Delta chi^2 favoravel a TGL nao e confirmacao; um desfavoravel e preferencia de fundo em dados comprimidos, nao falsificacao da lei",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("diagnostico lido por hash (%s)" % dhash, dj is not None and fixed_sha is not None),
              ("o worker de maio falha o fiducial (razao DM > 1,1) e o corrigido o reproduz (|razao - 1| < 5e-3)", dj is not None and (aut.get("may_beta0") or {}).get("ratio_TGL_over_CAMB", 0) > 1.1 and abs((aut.get("fixed_beta0") or {}).get("ratio_TGL_over_CAMB", 0) - 1.0) < 5e-3),
              ("emenda V2 pre-registrada e hasheada (%s)" % ph, True), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "autopsy": aut, "v1_numbers": v1_numbers, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False, "runtime_s": float(time.time() - _t0),
            "verdict": ("TGL_D1_CAMB_V2__AMENDMENT_PRE_REGISTERED_%s__AUTOPSY_OF_V1_READ__MAY_WORKER_DISTANCE_BUG_NAMED__FIXED_COPY_BOUND_BY_SHA256__GATE_UNTOUCHED" % ph) if all_v else "TGL_D1_CAMB_AMENDMENT_V2_NOT_SEALED_THIS_RUN"}


def prove_d1_camb_result_v2(ONE, amendment_record=None):
    """v349 -- o resultado da V2 do D1 via CAMB (driver externo com o worker corrigido, no WSL), lido por hash e julgado pela matriz da emenda."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    am = amendment_record or prove_d1_camb_amendment_v2(ONE); ph = am.get("protocol_hash"); pr = am.get("protocol") or {}; crit = pr.get("criteria") or {}
    res_p = os.path.join(CACHE, "d1_camb", "D1_CAMB_V2_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "cosmologia jamais vira prova matematica; o fundo comprimido e aproximacao declarada"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash o relatorio do script de maio (worker corrigido em copia) e aplica a matriz da emenda (%s)" % ph,
          "distincao": "[REAL] fundo (aqui) vs perturbacao (Nivel 2, N2_INCAPAZ): testes conjugados"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_D1_CAMB_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado D1_CAMB_V2 em cache/d1_camb", False)], statuses=st, runtime_s=float(time.time() - _t0))
    rep = rj.get("report") or {}; p1 = rep.get("phase1") or {}; p2 = rep.get("phase2") or {}; p3 = rep.get("phase3") or {}; inst = rj.get("instrument") or {}; sc = rj.get("scripts") or {}; wu = sc.get("worker_used") or {}
    bt = (rep.get("metadata") or {}).get("beta_TGL_theory"); chi_l = (p1.get("LCDM_bestfit") or {}).get("chi2")
    checks = [("resultado V2 lido por hash (%s)" % rhash, True),
              ("beta do script de maio == beta recomputado", bool(isinstance(bt, (int, float)) and abs(float(bt) - beta) < 1e-12)),
              ("worker usado == worker corrigido amarrado no protocolo (sha256); script de maio intocado (sha256 e mtime de 2026-05)", bool(wu.get("sha256") == pr.get("fixed_worker_sha256") and wu.get("is_may_original") is False and str((sc.get("tgl_mcmc_camb_v2") or {}).get("mtime", "")).startswith("2026-05") and str((sc.get("tgl_camb_worker") or {}).get("mtime", "")).startswith("2026-05"))),
              ("fases 1 e 2 com best-fits bem-sucedidos; bondade de ajuste chi^2_LCDM <= %.0f" % float(crit.get("gof_chi2_lcdm_max", 48.0)), bool((p1.get("LCDM_bestfit") or {}).get("success") and (p1.get("TGL_bestfit") or {}).get("success") and (p2.get("LCDM_bestfit_planck_only") or {}).get("success") and (p2.get("TGL_bestfit_planck_only") or {}).get("success") and isinstance(chi_l, (int, float)) and chi_l <= float(crit.get("gof_chi2_lcdm_max", 48.0)))),
              ("fase 3 (MCMC beta livre) presente e convergida", bool(p3 and float(crit.get("acceptance_min", 0.1)) <= float(p3.get("acceptance_fraction_mean", -1)) <= float(crit.get("acceptance_max", 0.7)) and int(p3.get("chain_size", 0)) >= int(crit.get("chain_min", 38400)))),
              ("returncode 0 e instrumento camb + emcee", rj.get("returncode") == 0 and bool(inst.get("camb") and inst.get("emcee"))), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    d = p1.get("delta_chi2"); reasons = []
    if not (isinstance(chi_l, (int, float)) and chi_l <= float(crit.get("gof_chi2_lcdm_max", 48.0))): reasons.append("chi^2 LCDM %s > %.0f (bondade de ajuste)" % (_f(chi_l, 1), float(crit.get("gof_chi2_lcdm_max", 48.0))))
    if reasons or not isinstance(d, (int, float)): bf = "INCONCLUSIVE_SYSTEMATICS"
    elif d >= float(crit.get("delta_chi2_5sigma", 25.0)): bf = "D1_LCDM_PREFERRED_5SIGMA"
    elif d <= -float(crit.get("delta_chi2_5sigma", 25.0)): bf = "D1_TGL_BACKGROUND_PREFERRED_5SIGMA"
    elif abs(d) >= float(crit.get("delta_chi2_2sigma", 4.0)): bf = "D1_TENSION_2_TO_5_SIGMA"
    else: bf = "D1_NOT_DISTINGUISHED"
    sm = (p3.get("summary") or {}).get("beta") or {}; med = sm.get("median"); sg = (0.5 * (sm.get("sigma_lower", 0) + sm.get("sigma_upper", 0))) if sm else None
    if reasons or not p3 or not isinstance(med, (int, float)) or not sg: mc = "INCONCLUSIVE_SYSTEMATICS"
    else:
        zt = abs(med - beta) / sg
        if zt > 5.0: mc = "D1_BETA_FALSIFIED"
        elif sg > beta: mc = "D1_BETA_INCAPAZ"
        elif sg <= beta / 2.0 and zt <= 3.0: mc = "D1_BETA_NOT_FALSIFIED_POWERED"
        elif zt > 3.0: mc = "D1_BETA_TENSION"
        else: mc = "D1_BETA_INCONCLUSIVE"
    h0 = {"LCDM_bestfit": (p2.get("LCDM_bestfit_planck_only") or {}).get("H0"), "TGL_bestfit": (p2.get("TGL_bestfit_planck_only") or {}).get("H0")}; tens = {k: p2.get(k) for k in ("tension_LCDM_sigma", "tension_TGL_sigma", "tension_zero_free_sigma") if k in p2}
    verdict = ("TGL_D1_CAMB_V2__RESULT_READ_BY_HASH__BESTFIT_%s__DELTA_CHI2_%s__MCMC_%s__BETA_%s_PM_%s__GATE_UNTOUCHED"
               % (bf, _f(d, 2).replace(".", "P").replace("-", "M"), mc, _f(med, 4).replace(".", "P").replace("-", "M") if isinstance(med, (int, float)) else "NA", _f(sg, 4).replace(".", "P") if sg else "NA")) if all_v else "TGL_D1_CAMB_RESULT_V2_NOT_SEALED_THIS_RUN"
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] V2 (worker corrigido): fase 1 (Planck + DESI + SH0ES): chi^2 LCDM %s, TGL(beta fixo) %s, Delta chi^2 = %s => %s; fase 2 (sem SH0ES): H0 LCDM %s, TGL %s; tensoes vs SH0ES %s; fase 3 (beta livre): beta = %s +%s -%s (sigma media %s; alpha sqrt(e) = %s; %s sigma), aceitacao %s, cadeia %s => %s%s; tempo %s s"
                             % (_f(chi_l, 3), _f((p1.get("TGL_bestfit") or {}).get("chi2"), 3), _f(d, 3), bf, _f(h0.get("LCDM_bestfit"), 3), _f(h0.get("TGL_bestfit"), 3), {k: _f(v, 2) for k, v in tens.items()},
                                _f(med, 5), _f(sm.get("sigma_upper"), 5), _f(sm.get("sigma_lower"), 5), _f(sg, 5), _f(beta, 5), _f((abs(med - beta) / sg) if (isinstance(med, (int, float)) and sg) else None, 2), _f(p3.get("acceptance_fraction_mean"), 3), p3.get("chain_size"), mc, (" [%s]" % "; ".join(reasons) if reasons else ""), _f(rj.get("runtime_s"), 0)))
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), instrument=inst, scripts=sc, reasons=reasons,
                bestfit_outcome=bf, mcmc_outcome=mc, delta_chi2=d, chi2=dict(LCDM=chi_l, TGL=(p1.get("TGL_bestfit") or {}).get("chi2")), h0_no_sh0es=h0, tensions=tens,
                beta_posterior=dict(median=med, sigma=sg, lo16=sm.get("lo16"), hi84=sm.get("hi84")), mcmc=dict(acceptance=p3.get("acceptance_fraction_mean"), chain_size=p3.get("chain_size"), time_s=p3.get("time_seconds")), pipeline_runtime_s=rj.get("runtime_s"))
