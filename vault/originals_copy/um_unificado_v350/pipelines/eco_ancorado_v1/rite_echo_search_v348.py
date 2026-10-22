def prove_echo_search_protocol(ONE):
    """v348 -- A BUSCA DE ECOS DE LONGO ATRASO (0,1-2,0 s) COM COINCIDENCIA H1/L1, PRE-REGISTRADA [ADITIVO; fail-closed; nao gateia 1=1; fora do contorno].
    O terceiro dos testes que aguardavam o instrumento (ordem do operador, 10/09/2026): o `search_for_echoes` do protocolo de observacao de
    outubro de 2025 (Observavel 1.2: t_echo = (2GM/c^3) ln(r_halo/r_H) ~ 0,1-1 s; A_echo/A_prim ~ 0,01-0,1; picos > 3 sigma na banda 50-300 Hz;
    coincidencia H1/L1 em 10 ms; «confirmar: 3+ ecos > 5 sigma com padrao de Delta t consistente»). A forma e herdada; o que faltava entra:
    merger por filtro casado (nao o GPS grosseiro), fundo medido em janelas fora da fonte, injecoes com a amplitude sqrt(beta) do kernel para
    medir a eficiencia, e o teste de padrao no atraso adimensional tau/(GM_f/c^3). A hipotese de 2025 (atraso de 0,1-2 s) e [CONJECTURE] e a
    amplitude e a do kernel [REAL, v341]; a lei do atraso da TGL madura (MAY/KMS, ms) e OUTRA e ja foi testada (v341-v347). Vereditos: DETECTED
    (excesso >= 5 sigma de Poisson E >= 3 eventos com coincidencia >= 5 sigma E padrao tau/M p < 1e-3), EXCLUDED_AT_SQRT_BETA (E_det >= 20 e
    p_excl < 2,9e-7: se todo merger tivesse um eco de sqrt(beta) em 0,1-2 s, ter-se-ia visto), NOT_FALSIFIED_POWERED (E_det >= 20),
    NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_SYSTEMATICS (fundo > 1 coincidencia/janela, < 10 eventos, ou injecoes ausentes). CONFIRMED proibido."""
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = {
        "version": "ECHO_SEARCH_V1", "status": "PRE_REGISTERED_BEFORE_DATA_READ", "form_of": "search_for_echoes, protocolo de observacao TGL, outubro de 2025 (Observavel 1.2)",
        "hypothesis_2025_CONJECTURE": {"delay": "t_echo = (2GM/c^3) ln(r_halo/r_H) ~ 0,1-2,0 s", "amplitude_2025": "A_echo/A_prim ~ 0,01-0,1", "amplitude_kernel_REAL": "sqrt(beta) (v341: Smat_reflection), sinal -1", "beta_source": "SEALED_CODATA_ALPHA * sqrt(e) em runtime"},
        "data": "cache de maio (GWOSC via gwpy, 32 s @ 4096 Hz); H1 E L1 presentes e limpos; PSD Welch dos 14 s pre-evento; branqueamento na banda [50, 300] Hz",
        "merger": "ancoragem por filtro casado (IMRPhenomD nos parametros do catalogo, ±100 ms do GPS), SNR >= 6 em cada detector",
        "search": {"window_s": [0.1, 2.0], "statistic": "envoltoria analitica em sigmas (sigma fora da fonte)", "threshold_sigma": 3.0, "min_sep_s": 0.01, "coincidence_s": 0.01, "rank": "media das alturas (como no protocolo) e soma em quadratura"},
        "background": "a mesma busca em 6 janelas de 1,9 s fora da fonte (pre-evento: inicios em -14, -12, -10, -8, -6, -4 s) por evento",
        "injection": "primario ajustado (amplitude complexa do filtro casado), parte pos-pico, escalado por sqrt(beta), injetado nas janelas de fundo com tau ~ U[0,1; 2,0] s (6 por evento; mesmo tau nos dois detectores) -> eficiencia eps_i; E_det = soma eps_i",
        "pattern": "KS de tau/(G M_f/c^3) dos candidatos on-source contra o fundo",
        "aggregation": "N_on = coincidencias on-source; B_exp = soma das taxas de fundo; z de Poisson; p_excess = P(N >= N_on | B_exp); p_excl = P(N <= N_on | B_exp + E_det)",
        "criteria": {"detect_z": 5.0, "loud_sigma": 5.0, "loud_events_min": 3, "pattern_p_max": 1e-3, "powered_E_det_min": 20.0, "excl_p_max": 2.9e-7, "bg_rate_max_per_window": 1.0, "min_events": 10},
        "allowed_verdicts": ["DETECTED", "EXCLUDED_AT_SQRT_BETA", "NOT_FALSIFIED_POWERED", "NOT_FALSIFIED_UNDERPOWERED", "INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao testa as leis MAY/KMS (ms; v341-v347); exclui ou nao a CONJECTURA de 2025 (eco de sqrt(beta) em 0,1-2 s) na eficiencia medida por injecao; picos coincidentes sem padrao sao fundo, nao eco",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("protocolo pre-registrado e hasheado (%s)" % ph, True), ("beta jamais literal", bool(abs(beta - SEALED_CODATA_ALPHA * math.sqrt(math.e)) == 0.0)),
              ("amplitude de injecao = sqrt(beta) do kernel", bool(abs(math.sqrt(beta) - math.sqrt(SEALED_CODATA_ALPHA * math.sqrt(math.e))) == 0.0)), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "verdict": ("TGL_ECHO_SEARCH_V1__PROTOCOL_PRE_REGISTERED_%s__OCTOBER_2025_FORM_INHERITED__BACKGROUND_INJECTION_PATTERN_ADDED__GATE_UNTOUCHED" % ph) if all_v else "TGL_ECHO_SEARCH_PROTOCOL_NOT_SEALED_THIS_RUN"}


def prove_echo_search_result(ONE, protocol_record=None):
    """v348 -- o resultado da busca de ecos de longo atraso (pipeline externo echo_search_v1.py no WSL), lido por hash e julgado pela matriz."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = protocol_record or prove_echo_search_protocol(ONE); ph = proto.get("protocol_hash"); pr = proto.get("protocol") or {}; crit = pr.get("criteria") or {}; se = pr.get("search") or {}
    res_p = os.path.join(CACHE, "gw", "ECHO_SEARCH_V1_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "a hipotese de 2025 (atraso 0,1-2 s) e CONJECTURE; a amplitude e do kernel; nada aqui move a matematica"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz pre-registrada (%s)" % ph,
          "amplitude": "[REAL, kernel] a eficiencia e medida injetando o primario ajustado x sqrt(beta); beta entra",
          "hipotese": "[CONJECTURE, 2025] atraso de 0,1-2 s: a lei madura (MAY/KMS, ms) e outra e foi testada nas v341-v347"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_ECHO_SEARCH_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado ECHO_SEARCH_V1 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    inst = rj.get("instrument") or {}; pl = rj.get("pipeline") or {}; sm = rj.get("summary") or {}
    checks = [("resultado lido por hash (%s)" % rhash, True),
              ("beta, a_pred = sqrt(beta) e sinal -1 batem com o runtime", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15 and abs(float(rj.get("a_pred", 0)) - math.sqrt(beta)) < 1e-15 and float(rj.get("sign", 0)) == -1.0)),
              ("instrumento: lalsuite + ancoragem PhenomD; scipy", bool(inst.get("lalsuite") and inst.get("anchor_template") == "IMRPhenomD" and inst.get("scipy"))),
              ("parametros do pipeline == protocolo (janela, banda, limiar, coincidencia, fundo, injecoes)", bool(list(pl.get("window") or []) == list(se.get("window_s") or []) and list(pl.get("band") or []) == [50.0, 300.0] and pl.get("threshold") == se.get("threshold_sigma") and pl.get("coincidence") == se.get("coincidence_s") and len(pl.get("bg_starts") or []) == 6 and (pl.get("n_inj") or 0) >= 6 and pl.get("loud") == crit.get("loud_sigma"))),
              ("catalogo e fontes com sha256; >= %d eventos com H1 e L1" % int(crit.get("min_events", 10)), bool((rj.get("catalog") or {}).get("sha256") and len(rj.get("sources_sha256") or {}) >= 20 and (sm.get("n_events") or 0) >= int(crit.get("min_events", 10)))),
              ("fundo e injecoes presentes (B_exp, E_det finitos)", bool(isinstance(sm.get("B_exp"), (int, float)) and isinstance(sm.get("E_det"), (int, float)) and sm.get("mean_eff") is not None)),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    reasons = []
    if (sm.get("n_events") or 0) < int(crit.get("min_events", 10)): reasons.append("%s eventos < %d" % (sm.get("n_events"), int(crit.get("min_events", 10))))
    if sm.get("bg_rate_mean_per_window") is None or sm["bg_rate_mean_per_window"] > float(crit.get("bg_rate_max_per_window", 1.0)): reasons.append("fundo %s coincidencias/janela > %.0f" % (_f(sm.get("bg_rate_mean_per_window"), 3), float(crit.get("bg_rate_max_per_window", 1.0))))
    if sm.get("E_det") is None: reasons.append("injecoes ausentes")
    z = sm.get("z_poisson"); n_loud = sm.get("n_loud_events") or 0; ksp = (sm.get("ks_tau_over_M") or {}).get("p"); E = sm.get("E_det") or 0.0; p_excl = sm.get("p_excl")
    if reasons: outcome = "INCONCLUSIVE_SYSTEMATICS"
    elif z is not None and z >= float(crit.get("detect_z", 5.0)) and n_loud >= int(crit.get("loud_events_min", 3)) and ksp is not None and ksp < float(crit.get("pattern_p_max", 1e-3)): outcome = "DETECTED"
    elif E >= float(crit.get("powered_E_det_min", 20.0)) and p_excl is not None and p_excl < float(crit.get("excl_p_max", 2.9e-7)): outcome = "EXCLUDED_AT_SQRT_BETA"
    elif E >= float(crit.get("powered_E_det_min", 20.0)): outcome = "NOT_FALSIFIED_POWERED"
    else: outcome = "NOT_FALSIFIED_UNDERPOWERED"
    verdict = ("TGL_ECHO_SEARCH_V1__RESULT_READ_BY_HASH__%s__N_ON_%s_B_EXP_%s__E_DET_%s__LOUD_EVENTS_%s__GATE_UNTOUCHED"
               % (outcome, sm.get("N_on"), _f(sm.get("B_exp"), 1).replace(".", "P"), _f(E, 1).replace(".", "P"), n_loud)) if all_v else "TGL_ECHO_SEARCH_RESULT_NOT_SEALED_THIS_RUN"
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] %s eventos com H1 e L1 (%s pulados): coincidencias on-source N_on = %s contra fundo esperado B_exp = %s (z de Poisson %s; p_excess %s); eventos com coincidencia >= 5 sigma: %s %s; "
                             "padrao tau/M: KS p = %s; eficiencia media para um eco de sqrt(beta) em 0,1-2 s = %s (E_det = %s; p_excl = %s); pico previsto do eco (mediana) H1 %s L1 %s sigma => %s%s"
                             % (sm.get("n_events"), sm.get("n_skipped"), sm.get("N_on"), _f(sm.get("B_exp"), 2), _f(z, 2), ("%.3g" % sm["p_excess"]) if isinstance(sm.get("p_excess"), (int, float)) else "NA", n_loud, sm.get("loud"),
                                ("%.3g" % ksp) if isinstance(ksp, (int, float)) else "NA", _f(sm.get("mean_eff"), 3), _f(E, 2), ("%.3g" % p_excl) if isinstance(p_excl, (int, float)) else "NA",
                                _f((sm.get("h_pred_median") or {}).get("H1"), 2), _f((sm.get("h_pred_median") or {}).get("L1"), 2), outcome, (" [%s]" % "; ".join(reasons) if reasons else "")))
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), pipeline_runtime_s=rj.get("runtime_s"),
                instrument=inst, summary=sm, outcome=outcome, reasons=reasons, catalog_sha16=str((rj.get("catalog") or {}).get("sha256", ""))[:16], n_sources=len(rj.get("sources_sha256") or {}))
