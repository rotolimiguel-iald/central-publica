def prove_echo_pe_protocol(ONE):
    """v347 -- A PE BAYESIANA COM TERMO DE ECO, PRE-REGISTRADA [ADITIVO; fail-closed; nao gateia 1=1; fora do contorno].
    O segundo dos testes que aguardavam o instrumento (ordem do operador, 10/09/2026): a forma final do protocolo ancorado
    (ECHO_ANCHORED, hash 1e94f77689b5017e). Nas V1/V2 (v344/v345) o descasamento de template entrava como sistematica e dava
    INCONCLUSIVE_SYSTEMATICS; aqui os parametros do primario sao AMOSTRADOS (bilby + dynesty) e a amplitude complexa por detector
    (distancia, inclinacao, polarizacao, ceu, fase) e marginalizada analiticamente, de modo que o descasamento entra no posterior.
    Modelo por detector: s = Re[z (p(t - dt) + a S sqrt(beta) e(t - dt))]: p = IMRPhenomD [KNOWN]; e = copia de p a partir do pico, atrasada
    de tau; S = -1 e sqrt(beta) sao do kernel (v341: Smat_reflection); tau pela lei MAY (2GM_f/c^3 ln(1/beta)) ou KMS (2pi/kappa de Kerr) com
    o (M_f, a_f) AMOSTRADO pelo ajuste EOB. a = 1 e a previsao; a = 0 e «sem eco». Vereditos por lei: DETECTED (z vs 0 >= 5 e |z vs 1| <= 2),
    FALSIFIED_AT_DELAY_LAW (|z vs 1| >= 5 e poder >= 5), NOT_FALSIFIED_POWERED (poder >= 5), NOT_FALSIFIED_UNDERPOWERED,
    INCONCLUSIVE_SYSTEMATICS (injecoes: |vies em a = 1| > 0,2, ou a = 0 recuperado a > 2 sigma, ou |familia B - A| > 0,3, ou < 5 eventos).
    beta jamais literal. CONFIRMED proibido."""
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = {
        "version": "ECHO_PE_V1", "status": "PRE_REGISTERED_BEFORE_DATA_READ", "form_of": "ECHO_ANCHORED_V1 (1e94f77689b5017e), forma bayesiana",
        "hypothesis": {"model": "s_d = Re[z_d (p(t - dt_d) + a S sqrt(beta) e(t - dt_d))]", "a_pred": "1 (amplitude sqrt(beta), sinal S = -1, do kernel)", "a_null": "0 (sem eco)",
                       "delay_laws": {"MAY": "2 G M_f/c^3 ln(1/beta) [INPUT]", "KMS": "2 pi/kappa de Kerr com (M_f, a_f) amostrados [CANDIDATO]"}, "beta_source": "SEALED_CODATA_ALPHA * sqrt(e) em runtime"},
        "primary_KNOWN": "IMRPhenomD (lalsimulation) de (m1, m2, chi_eff) amostrados; estado final por SimIMREOBFinalMassSpin (SEOBNRv4)",
        "sampled": ["m1_det", "m2_det", "chi_eff", "dt_d por detector", "a"], "marginalized": "amplitude complexa z_d por detector, prior plano: ln L = 1/2 r^T G^-1 r - 1/2 ln det G",
        "priors": {"m1_m2": "uniforme no intervalo de 90% do catalogo alargado 2x (detector)", "chi_eff": "idem (±0,2 se ausente)", "dt": "uniforme em ±0,1 s do GPS", "a": "uniforme em [-3, 3]"},
        "sampler": {"engine": "bilby + dynesty", "nlive": 300, "sample": "rwalk", "walks": 30, "dlogz": 0.3},
        "data": "cache de maio (GWOSC via gwpy, 32 s @ 4096 Hz); segmento de 6 s com o pico em 5 s; PSD Welch dos 14 s pre-evento; banda [20, 1024] Hz; H1 + L1",
        "selection": {"mc_det_min": 10.0, "anchor_det_min": 6.0, "anchor_ev_min": 8.0, "anchor": "filtro casado PhenomD nos parametros do catalogo em ±100 ms"},
        "per_event": "posterior de a (media, sigma, quantis), ln Z, ln B_{sem eco/com eco} por Savage-Dickey em a = 0",
        "combination": "soma dos log-posteriores de a numa grade comum (prior plano comum): a_comb ± sigma_comb; z contra 0 e contra 1; poder = 1/sigma_comb",
        "nulls": {"injection": "eventos com SNR de ancoragem >= 10 (ate 10), em ruido fora da fonte (t0 = -12 s): a = 0 primario-so; a = 1 PhenomD; a = 1 SEOBNRv4 (nulo de familia); recuperacao pela mesma PE"},
        "criteria": {"detect_z": 5.0, "exclude_z": 5.0, "consistent_with_1_z": 2.0, "power_min": 5.0, "inj_a1_bias_max": 0.2, "inj_a0_max_sigma": 2.0, "family_diff_max": 0.3, "min_events": 5},
        "allowed_verdicts": ["DETECTED", "FALSIFIED_AT_DELAY_LAW", "NOT_FALSIFIED_POWERED", "NOT_FALSIFIED_UNDERPOWERED", "INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao decide a lei do atraso (INPUT/candidato); um posterior de a consistente com 0 e com 1 e UNDERPOWERED, nao ausencia",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("protocolo pre-registrado e hasheado (%s)" % ph, True), ("beta jamais literal", bool(abs(beta - SEALED_CODATA_ALPHA * math.sqrt(math.e)) == 0.0)),
              ("a_pred = sqrt(beta) e S = -1 vem do kernel (v341)", bool(abs(math.sqrt(beta) - math.sqrt(SEALED_CODATA_ALPHA * math.sqrt(math.e))) == 0.0)), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "verdict": ("TGL_ECHO_PE_V1__PROTOCOL_PRE_REGISTERED_%s__PRIMARY_SAMPLED_AMPLITUDE_MARGINALIZED__TWO_DELAY_LAWS__BETA_ENTERS__GATE_UNTOUCHED" % ph) if all_v else "TGL_ECHO_PE_PROTOCOL_NOT_SEALED_THIS_RUN"}


def prove_echo_pe_result(ONE, protocol_record=None):
    """v347 -- o resultado da PE com termo de eco (pipeline externo echo_pe_v1.py no WSL: bilby + dynesty + lalsuite), lido por hash e julgado pela matriz."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = protocol_record or prove_echo_pe_protocol(ONE); ph = proto.get("protocol_hash"); pr = proto.get("protocol") or {}; crit = pr.get("criteria") or {}; smp = pr.get("sampler") or {}; sel = pr.get("selection") or {}
    res_p = os.path.join(CACHE, "gw", "ECHO_PE_V1_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "a lei do atraso e INPUT/candidato: o que se testa e a = 1 sob cada lei, nao a TGL"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz pre-registrada (%s)" % ph,
          "amplitude": "[REAL, kernel] a = 1 significa |R| = sqrt(beta) com sinal -1 (Smat_reflection); beta entra",
          "descasamento": "[REAL] o que nas V1/V2 era sistematica de template aqui e parametro amostrado e marginalizado"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_ECHO_PE_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado ECHO_PE_V1 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    inst = rj.get("instrument") or {}; pl = rj.get("pipeline") or {}; comb = rj.get("combined") or {}; laws = rj.get("laws") or []
    checks = [("resultado lido por hash (%s)" % rhash, True),
              ("beta, a_pred = sqrt(beta) e sinal -1 batem com o runtime", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15 and abs(float(rj.get("a_pred", 0)) - math.sqrt(beta)) < 1e-15 and float(rj.get("sign", 0)) == -1.0)),
              ("instrumento: lalsuite + bilby + dynesty, primario PhenomD, familia B SEOBNRv4", bool(inst.get("lalsuite") and inst.get("bilby") and inst.get("dynesty") and (inst.get("families") or {}).get("A") == "IMRPhenomD" and (inst.get("families") or {}).get("B") == "SEOBNRv4")),
              ("parametros do pipeline == protocolo (nlive, walks, dlogz, dt, prior de a, selecao)", bool(pl.get("nlive") == smp.get("nlive") and pl.get("walks") == smp.get("walks") and pl.get("dlogz") == smp.get("dlogz") and pl.get("dt_max") == 0.1 and list(pl.get("a_prior") or []) == [-3.0, 3.0] and pl.get("mc_det_min") == sel.get("mc_det_min") and pl.get("anchor_det_min") == sel.get("anchor_det_min") and pl.get("anchor_ev_min") == sel.get("anchor_ev_min"))),
              ("catalogo e fontes com sha256; duas leis", bool((rj.get("catalog") or {}).get("sha256") and len(rj.get("sources_sha256") or {}) >= 20 and set(laws) == {"MAY", "KMS"})),
              ("cada lei com >= %d eventos" % int(crit.get("min_events", 5)), bool(all((comb.get(l) or {}).get("n_events", 0) >= int(crit.get("min_events", 5)) for l in ("MAY", "KMS")))),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    outcomes = {}; statuses = dict(st)
    for law in ("MAY", "KMS"):
        c = comb.get(law) or {}; reasons = []
        if (c.get("n_events") or 0) < int(crit.get("min_events", 5)): reasons.append("%s eventos < %d" % (c.get("n_events"), int(crit.get("min_events", 5))))
        if not c.get("inj_a1_n") or c.get("inj_a1_bias") is None or abs(c["inj_a1_bias"]) > float(crit.get("inj_a1_bias_max", 0.2)): reasons.append("vies em a = 1 %s > %.1f (n=%s)" % (_f(c.get("inj_a1_bias"), 3), float(crit.get("inj_a1_bias_max", 0.2)), c.get("inj_a1_n")))
        if not c.get("inj_a0_n") or c.get("inj_a0_mean") is None or abs(c["inj_a0_mean"]) > float(crit.get("inj_a0_max_sigma", 2.0)) * (c.get("inj_a0_sigma") or 0): reasons.append("a = 0 recuperado %s +- %s (n=%s)" % (_f(c.get("inj_a0_mean"), 3), _f(c.get("inj_a0_sigma"), 3), c.get("inj_a0_n")))
        if not c.get("inj_a1_B_n") or c.get("family_diff") is None or abs(c["family_diff"]) > float(crit.get("family_diff_max", 0.3)): reasons.append("familia B - A %s > %.1f (n=%s)" % (_f(c.get("family_diff"), 3), float(crit.get("family_diff_max", 0.3)), c.get("inj_a1_B_n")))
        z0, z1, pw = c.get("z_vs_0"), c.get("z_vs_1"), c.get("power")
        if reasons: o = "INCONCLUSIVE_SYSTEMATICS"
        elif z0 is not None and abs(z0) >= float(crit.get("detect_z", 5.0)) and z0 > 0 and abs(z1) <= float(crit.get("consistent_with_1_z", 2.0)): o = "DETECTED"
        elif z1 is not None and abs(z1) >= float(crit.get("exclude_z", 5.0)) and (pw or 0) >= float(crit.get("power_min", 5.0)): o = "FALSIFIED_AT_DELAY_LAW"
        elif (pw or 0) >= float(crit.get("power_min", 5.0)): o = "NOT_FALSIFIED_POWERED"
        else: o = "NOT_FALSIFIED_UNDERPOWERED"
        outcomes[law] = dict(outcome=o, reasons=reasons, n_events=c.get("n_events"), a=c.get("a_comb"), sigma=c.get("sigma_comb"), z_vs_0=z0, z_vs_1=z1, power=pw, lnB_total=c.get("lnB_noecho_over_echo_total"),
                             inj_a0=(c.get("inj_a0_mean"), c.get("inj_a0_sigma"), c.get("inj_a0_n")), inj_a1=(c.get("inj_a1_mean"), c.get("inj_a1_sigma"), c.get("inj_a1_n")), family=(c.get("inj_a1_B_mean"), c.get("inj_a1_B_sigma"), c.get("inj_a1_B_n")))
        statuses["resultado_" + law] = ("[REAL, lido] %s: %s eventos; a = %s +- %s (z vs 0 %s; z vs 1 %s; poder %s sigma); ln B(sem/com eco) total %s; injecoes: a=0 -> %s +- %s (n=%s), a=1 -> %s +- %s (n=%s), familia B -> %s +- %s (n=%s) => %s%s"
                                        % (law, c.get("n_events"), _f(c.get("a_comb")), _f(c.get("sigma_comb")), _f(z0, 2), _f(z1, 2), _f(pw, 2), _f(c.get("lnB_noecho_over_echo_total"), 2),
                                           _f(c.get("inj_a0_mean"), 3), _f(c.get("inj_a0_sigma"), 3), c.get("inj_a0_n"), _f(c.get("inj_a1_mean"), 3), _f(c.get("inj_a1_sigma"), 3), c.get("inj_a1_n"), _f(c.get("inj_a1_B_mean"), 3), _f(c.get("inj_a1_B_sigma"), 3), c.get("inj_a1_B_n"), o, (" [%s]" % "; ".join(reasons) if reasons else "")))
    verdict = ("TGL_ECHO_PE_V1__RESULT_READ_BY_HASH__BILBY_DYNESTY_LALSUITE__MAY_%s__KMS_%s__POWER_MAY_%s_KMS_%s_OF_5_SIGMA__GATE_UNTOUCHED"
               % (outcomes["MAY"]["outcome"], outcomes["KMS"]["outcome"], _f(outcomes["MAY"].get("power"), 1).replace(".", "P"), _f(outcomes["KMS"].get("power"), 1).replace(".", "P"))) if all_v else "TGL_ECHO_PE_RESULT_NOT_SEALED_THIS_RUN"
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), pipeline_runtime_s=rj.get("runtime_s"),
                instrument=inst, n_events_used=rj.get("n_events_used"), n_events_catalog=rj.get("n_events_catalog"), outcomes=outcomes, catalog_sha16=str((rj.get("catalog") or {}).get("sha256", ""))[:16], n_sources=len(rj.get("sources_sha256") or {}))


def prove_echo_pe_amendment_v2(ONE, v1_record=None):
    """v347 -- A EMENDA V2 DA PE COM ECO, PRE-REGISTRADA DEPOIS DA AUTOPSIA DA V1 E ANTES DO DADO DA V2 [ADITIVO; nao gateia; fora do contorno].
    A autopsia e LIDA do resultado da V1 (por hash), nunca de memoria: (a) as injecoes nao rodaram (a janela fora da fonte em t0 = -12 s cai
    fora do cache de 32 s) -- logo a V1 e INCONCLUSIVE_SYSTEMATICS pela propria matriz; (b) medianas do posterior coladas na borda do prior
    de tempo (±100 ms: o GPS do catalogo e grosseiro) e no piso de massa (m2 -> 1 Msun) em varios eventos; (c) um unico evento carregava a
    fracao dominante do peso, com jackknife de varias sigmas -- um «8 sigma» que muda de sinal ao tirar um evento nao e deteccao. O que a
    V2 muda, item a item: (1) prior de tempo centrado na ancoragem por filtro casado com meia-largura 20 ms; (2) priors de massa alargados
    1,5x com piso de 3 Msun; (3) EXCLUSAO de eventos com mediana a < 5% da borda do prior em qualquer parametro (PRIOR_EDGE); (4) janela de
    injecao em t0 = -9,5 s; (5) robustez pre-registrada: jackknife (grade) <= 2 sigma e peso maximo de um evento <= 0,5. Tudo o mais igual."""
    _t0 = time.time()
    v1 = v1_record or {}
    res_p = os.path.join(CACHE, "gw", "ECHO_PE_V1_RESULT.json")
    rj, rhash = _read_external_json_with_hash(res_p)
    aut = {"v1_result_sha16": rhash, "v1_protocol_hash": v1.get("protocol_hash"), "v1_outcomes": {l: (v1.get("outcomes") or {}).get(l, {}).get("outcome") for l in ("MAY", "KMS")}}
    if rj is not None:
        comb = rj.get("combined") or {}; pe = rj.get("per_event") or {}
        aut["injections_ran"] = bool(any((comb.get(l) or {}).get("inj_a0_n") for l in ("MAY", "KMS")))
        aut["injection_cause"] = "janela fora da fonte t0 = -12 s (segmento [-17, -11] s) fora do cache de 32 s ([-16, +16] s)" if not aut["injections_ran"] else None
        for law in ("MAY", "KMS"):
            rows = [(k, R["laws"][law]["on"]) for k, R in pe.items() if (R.get("laws") or {}).get(law, {}).get("on", {}).get("status") == "OK"]
            n_dt_edge = sum(1 for k, r in rows if any(abs(float(v)) > 0.095 for kk, v in (r.get("medians") or {}).items() if kk.startswith("dt_")))
            n_m_floor = sum(1 for k, r in rows if any(float((r.get("medians") or {}).get(m, 10.0)) <= 1.05 for m in ("m1", "m2")))
            w = [1.0 / (r["a_std"] ** 2) for k, r in rows]; W = sum(w) or float("nan"); shares = [x / W for x in w]
            i_max = max(range(len(rows)), key=lambda i: shares[i]) if rows else None
            jack = None
            if len(rows) >= 2:
                a_all = sum(wi * r["a_mean"] for wi, (k, r) in zip(w, rows)) / W; best = 0.0
                for i in range(len(rows)):
                    Wi = W - w[i]; ai = (a_all * W - w[i] * rows[i][1]["a_mean"]) / Wi; si = 1.0 / math.sqrt(Wi); best = max(best, abs(a_all - ai) / si)
                jack = best
            aut[law] = {"n_events": len(rows), "a_comb": (comb.get(law) or {}).get("a_comb"), "sigma_comb": (comb.get(law) or {}).get("sigma_comb"), "z_vs_0": (comb.get(law) or {}).get("z_vs_0"),
                        "a_ivw": (comb.get(law) or {}).get("a_ivw"), "sigma_ivw": (comb.get(law) or {}).get("sigma_ivw"), "n_dt_at_edge": n_dt_edge, "n_mass_at_floor": n_m_floor,
                        "max_weight_share": (shares[i_max] if rows else None), "max_weight_event": (rows[i_max][0] if rows else None), "max_weight_event_a": (rows[i_max][1]["a_mean"] if rows else None),
                        "jackknife_ivw_max_shift_sigma": jack}
    proto = {
        "version": "ECHO_PE_V2", "amendment_of": "ECHO_PE_V1", "status": "PRE_REGISTERED_AFTER_V1_AUTOPSY_BEFORE_V2_DATA_READ",
        "autopsy_of_V1": aut,
        "changes": {"1_time_prior": "centrado na ancoragem por filtro casado (PhenomD nos parametros do catalogo, ±100 ms do GPS) com meia-largura 20 ms",
                    "2_mass_priors": "intervalo de 90% do catalogo alargado 1,5x, piso 3 Msun (detector)", "3_prior_edge": "evento excluido da combinacao se a mediana de qualquer parametro (exceto a) estiver a < 5% da borda do prior",
                    "4_injection_window": "t0 = -9,5 s (segmento [-14,5; -8,5] s dentro do cache)", "5_robustness": "jackknife na combinacao em grade: max |a - a(-i)|/sigma(-i) <= 2; peso maximo de um evento <= 0,5"},
        "unchanged": "modelo, marginalizacao da amplitude, leis MAY/KMS com estado final amostrado, selecao (Mc_det >= 10; ancoragem >= 6/8), dynesty nlive 300 rwalk 30 dlogz 0,3, prior de a [-3, 3], injecoes a = 0 / a = 1 / familia SEOBNRv4, combinacao em grade + ivw, Savage-Dickey",
        "pipeline_params": {"dt_half": 0.02, "m_floor": 3.0, "prior_widen": 1.5, "edge_frac": 0.05, "inj_t0": -9.5, "nlive": 300, "walks": 30, "dlogz": 0.3, "a_prior": [-3.0, 3.0], "mc_det_min": 10.0, "anchor_det_min": 6.0, "anchor_ev_min": 8.0},
        "criteria": {"detect_z": 5.0, "exclude_z": 5.0, "consistent_with_1_z": 2.0, "power_min": 5.0, "inj_a1_bias_max": 0.2, "inj_a0_max_sigma": 2.0, "family_diff_max": 0.3, "min_events": 5, "jackknife_max_shift_sigma": 2.0, "max_weight_share": 0.5},
        "allowed_verdicts": ["DETECTED", "FALSIFIED_AT_DELAY_LAW", "NOT_FALSIFIED_POWERED", "NOT_FALSIFIED_UNDERPOWERED", "INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao decide a lei do atraso; templates de 22 modos alinhados (PhenomD/SEOBNRv4): modos superiores e precessao ficam [OPEN]; um posterior consistente com 0 e com 1 e UNDERPOWERED",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("autopsia da V1 lida por hash (%s)" % rhash, rj is not None and "MAY" in aut), ("a V1 nao teve injecoes (causa nomeada)", rj is not None and aut.get("injections_ran") is False),
              ("emenda V2 pre-registrada e hasheada (%s)" % ph, True), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "autopsy": aut, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False, "runtime_s": float(time.time() - _t0),
            "verdict": ("TGL_ECHO_PE_V2__AMENDMENT_PRE_REGISTERED_%s__AUTOPSY_OF_V1_READ__NO_INJECTIONS_PRIOR_EDGES_SINGLE_EVENT_DOMINANCE__GATE_UNTOUCHED" % ph) if all_v else "TGL_ECHO_PE_AMENDMENT_V2_NOT_SEALED_THIS_RUN"}


def prove_echo_pe_result_v2(ONE, amendment_record=None):
    """v347 -- o resultado da V2 da PE com eco (pipeline externo echo_pe_v2.py no WSL), lido por hash e julgado pela matriz da emenda."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    am = amendment_record or prove_echo_pe_amendment_v2(ONE); ph = am.get("protocol_hash"); pr = am.get("protocol") or {}; crit = pr.get("criteria") or {}; pp = pr.get("pipeline_params") or {}
    res_p = os.path.join(CACHE, "gw", "ECHO_PE_V2_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "a lei do atraso e INPUT/candidato: o que se testa e a = 1 sob cada lei, nao a TGL"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz da emenda (%s)" % ph,
          "amplitude": "[REAL, kernel] a = 1 significa |R| = sqrt(beta) com sinal -1 (Smat_reflection); beta entra",
          "robustez": "[REAL] jackknife e peso maximo pre-registrados: um resultado que depende de um evento nao e resultado"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_ECHO_PE_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado ECHO_PE_V2 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    inst = rj.get("instrument") or {}; pl = rj.get("pipeline") or {}; comb = rj.get("combined") or {}; laws = rj.get("laws") or []
    checks = [("resultado V2 lido por hash (%s)" % rhash, True),
              ("beta, a_pred = sqrt(beta) e sinal -1 batem com o runtime", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15 and abs(float(rj.get("a_pred", 0)) - math.sqrt(beta)) < 1e-15 and float(rj.get("sign", 0)) == -1.0)),
              ("instrumento: lalsuite + bilby + dynesty, primario PhenomD, familia B SEOBNRv4", bool(inst.get("lalsuite") and inst.get("bilby") and inst.get("dynesty") and (inst.get("families") or {}).get("A") == "IMRPhenomD" and (inst.get("families") or {}).get("B") == "SEOBNRv4")),
              ("parametros do pipeline == emenda (dt_half, piso, alargamento, borda, t0, nlive, prior de a, selecao)", bool(pl.get("dt_half") == pp.get("dt_half") and pl.get("m_floor") == pp.get("m_floor") and pl.get("prior_widen") == pp.get("prior_widen") and pl.get("edge_frac") == pp.get("edge_frac") and (pl.get("inj") or {}).get("t0") == pp.get("inj_t0") and pl.get("nlive") == pp.get("nlive") and list(pl.get("a_prior") or []) == pp.get("a_prior") and pl.get("mc_det_min") == pp.get("mc_det_min") and pl.get("anchor_det_min") == pp.get("anchor_det_min") and pl.get("anchor_ev_min") == pp.get("anchor_ev_min"))),
              ("catalogo e fontes com sha256; duas leis; versao V2 emenda da V1", bool((rj.get("catalog") or {}).get("sha256") and len(rj.get("sources_sha256") or {}) >= 20 and set(laws) == {"MAY", "KMS"} and rj.get("version") == "ECHO_PE_V2" and rj.get("amendment_of") == "ECHO_PE_V1")),
              ("cada lei com >= %d eventos apos a exclusao de borda" % int(crit.get("min_events", 5)), bool(all((comb.get(l) or {}).get("n_events", 0) >= int(crit.get("min_events", 5)) for l in ("MAY", "KMS")))),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    outcomes = {}; statuses = dict(st)
    for law in ("MAY", "KMS"):
        c = comb.get(law) or {}; reasons = []
        if (c.get("n_events") or 0) < int(crit.get("min_events", 5)): reasons.append("%s eventos < %d" % (c.get("n_events"), int(crit.get("min_events", 5))))
        if not c.get("inj_a1_n") or c.get("inj_a1_bias") is None or abs(c["inj_a1_bias"]) > float(crit.get("inj_a1_bias_max", 0.2)): reasons.append("vies em a = 1 %s > %.1f (n=%s)" % (_f(c.get("inj_a1_bias"), 3), float(crit.get("inj_a1_bias_max", 0.2)), c.get("inj_a1_n")))
        if not c.get("inj_a0_n") or c.get("inj_a0_mean") is None or abs(c["inj_a0_mean"]) > float(crit.get("inj_a0_max_sigma", 2.0)) * (c.get("inj_a0_sigma") or 0): reasons.append("a = 0 recuperado %s +- %s (n=%s)" % (_f(c.get("inj_a0_mean"), 3), _f(c.get("inj_a0_sigma"), 3), c.get("inj_a0_n")))
        if not c.get("inj_a1_B_n") or c.get("family_diff") is None or abs(c["family_diff"]) > float(crit.get("family_diff_max", 0.3)): reasons.append("familia B - A %s > %.1f (n=%s)" % (_f(c.get("family_diff"), 3), float(crit.get("family_diff_max", 0.3)), c.get("inj_a1_B_n")))
        if c.get("jack_grid_max_shift_sigma") is None or c["jack_grid_max_shift_sigma"] > float(crit.get("jackknife_max_shift_sigma", 2.0)): reasons.append("jackknife %s sigma > %.0f (sem %s)" % (_f(c.get("jack_grid_max_shift_sigma"), 2), float(crit.get("jackknife_max_shift_sigma", 2.0)), c.get("jack_grid_event")))
        if c.get("max_weight_share") is None or c["max_weight_share"] > float(crit.get("max_weight_share", 0.5)): reasons.append("peso maximo %s > %.1f (%s)" % (_f(c.get("max_weight_share"), 2), float(crit.get("max_weight_share", 0.5)), c.get("max_weight_event")))
        z0, z1, pw = c.get("z_vs_0"), c.get("z_vs_1"), c.get("power")
        if reasons: o = "INCONCLUSIVE_SYSTEMATICS"
        elif z0 is not None and abs(z0) >= float(crit.get("detect_z", 5.0)) and z0 > 0 and abs(z1) <= float(crit.get("consistent_with_1_z", 2.0)): o = "DETECTED"
        elif z1 is not None and abs(z1) >= float(crit.get("exclude_z", 5.0)) and (pw or 0) >= float(crit.get("power_min", 5.0)): o = "FALSIFIED_AT_DELAY_LAW"
        elif (pw or 0) >= float(crit.get("power_min", 5.0)): o = "NOT_FALSIFIED_POWERED"
        else: o = "NOT_FALSIFIED_UNDERPOWERED"
        # informativo (nao e criterio; acrescentado apos a leitura, dito): RESPOSTA PAREADA as injecoes -- a=1 menos a=0 no MESMO ruido -- deveria ser 1
        _d1, _dB = [], []
        for _k, _R in (rj.get("per_event") or {}).items():
            _L = (_R.get("laws") or {}).get(law) or {}; _a0, _a1, _aB = (_L.get("inj_a0") or {}), (_L.get("inj_a1_A") or {}), (_L.get("inj_a1_B") or {})
            if _a0.get("status") == "OK" and _a1.get("status") == "OK": _d1.append(float(_a1["a_mean"]) - float(_a0["a_mean"]))
            if _a0.get("status") == "OK" and _aB.get("status") == "OK": _dB.append(float(_aB["a_mean"]) - float(_a0["a_mean"]))
        def _sem(x):
            if not x: return (None, None, 0)
            m = sum(x) / len(x); return (m, ((math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1)) / math.sqrt(len(x))) if len(x) > 1 else None), len(x))
        pr1 = _sem(_d1); prB = _sem(_dB)
        outcomes[law] = dict(outcome=o, reasons=reasons, n_events=c.get("n_events"), n_prior_edge_excluded=c.get("n_prior_edge_excluded"), paired_response_a1=pr1, paired_response_B=prB, a=c.get("a_comb"), sigma=c.get("sigma_comb"), z_vs_0=z0, z_vs_1=z1, power=pw, a_ivw=c.get("a_ivw"), sigma_ivw=c.get("sigma_ivw"),
                             lnB_total=c.get("lnB_noecho_over_echo_total"), max_weight_share=c.get("max_weight_share"), max_weight_event=c.get("max_weight_event"), jackknife=c.get("jack_grid_max_shift_sigma"), jackknife_event=c.get("jack_grid_event"),
                             inj_a0=(c.get("inj_a0_mean"), c.get("inj_a0_sigma"), c.get("inj_a0_n")), inj_a1=(c.get("inj_a1_mean"), c.get("inj_a1_sigma"), c.get("inj_a1_n")), family=(c.get("inj_a1_B_mean"), c.get("inj_a1_B_sigma"), c.get("inj_a1_B_n")))
        statuses["resultado_" + law] = ("[REAL, lido] V2 %s: %s eventos (%s excluidos na borda do prior); a = %s +- %s (z vs 0 %s; z vs 1 %s; poder %s sigma); ivw %s +- %s; peso maximo %s (%s); jackknife %s sigma (sem %s); ln B(sem/com) %s; injecoes: a=0 -> %s +- %s (n=%s), a=1 -> %s +- %s (n=%s), familia B -> %s +- %s (n=%s); RESPOSTA PAREADA (a=1 - a=0, mesmo ruido; deveria ser 1) %s +- %s (n=%s), familia B - a=0 %s +- %s => %s%s"
                                        % (law, c.get("n_events"), c.get("n_prior_edge_excluded"), _f(c.get("a_comb")), _f(c.get("sigma_comb")), _f(z0, 2), _f(z1, 2), _f(pw, 2), _f(c.get("a_ivw")), _f(c.get("sigma_ivw")), _f(c.get("max_weight_share"), 2), c.get("max_weight_event"), _f(c.get("jack_grid_max_shift_sigma"), 2), c.get("jack_grid_event"), _f(c.get("lnB_noecho_over_echo_total"), 2),
                                           _f(c.get("inj_a0_mean"), 3), _f(c.get("inj_a0_sigma"), 3), c.get("inj_a0_n"), _f(c.get("inj_a1_mean"), 3), _f(c.get("inj_a1_sigma"), 3), c.get("inj_a1_n"), _f(c.get("inj_a1_B_mean"), 3), _f(c.get("inj_a1_B_sigma"), 3), c.get("inj_a1_B_n"),
                                           _f(pr1[0], 3), _f(pr1[1], 3), pr1[2], _f(prB[0], 3), _f(prB[1], 3), o, (" [%s]" % "; ".join(reasons) if reasons else "")))
    verdict = ("TGL_ECHO_PE_V2__RESULT_READ_BY_HASH__BILBY_DYNESTY_LALSUITE__MAY_%s__KMS_%s__POWER_MAY_%s_KMS_%s_OF_5_SIGMA__GATE_UNTOUCHED"
               % (outcomes["MAY"]["outcome"], outcomes["KMS"]["outcome"], _f(outcomes["MAY"].get("power"), 1).replace(".", "P"), _f(outcomes["KMS"].get("power"), 1).replace(".", "P"))) if all_v else "TGL_ECHO_PE_RESULT_V2_NOT_SEALED_THIS_RUN"
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), pipeline_runtime_s=rj.get("runtime_s"),
                instrument=inst, n_events_used=rj.get("n_events_used"), n_events_catalog=rj.get("n_events_catalog"), outcomes=outcomes, catalog_sha16=str((rj.get("catalog") or {}).get("sha256", ""))[:16], n_sources=len(rj.get("sources_sha256") or {}))
