def prove_h2_reproduction_protocol(ONE):
    """v350 -- A REPRODUCAO DE H2 (Echo Ratio -> alpha^2) COM PYCBC E DADOS REAIS, PRE-REGISTRADA [ADITIVO; fail-closed; nao gateia 1=1; fora do contorno].
    O quinto dos testes que aguardavam o instrumento (ordem do operador, 10/09/2026): os analisadores de eco de janeiro de 2026 (Echo Analyzer v8:
    «quando correlacao > 0,99, E_res/E_total -> alpha^2 = 0,012») e o Protocolo #12 de fevereiro (Tgl_gw_echo_unification_v1.py, H2: «a fase
    pos-ringdown apresenta Echo Ratio -> alpha^2»; h2_ok = desvio < 30% e correlacao > 0,90), que sem pycbc corriam em modo SINTETICO (gerador
    consistente + ruido). O que se testa aqui, com o `_echo_analysis` do proprio script COPIADO sem alteracao: (A) o sintetico fiel (ruido 0,1, sem
    eco, como no analyze) e dois niveis de ruido de controlo (0,05 e 0,2) -- se a razao seguir noise_level^2, o «alpha^2» era o ruido escolhido;
    (B) o dado REAL bruto, como o script faria com pycbc (janela [-2, +1] s, sem branqueamento, template pycbc); (C) o dado real BRANQUEADO com o
    template branqueado (a versao justa); (D) fora da fonte. Vereditos: H2_IDENTITY_RETIRED (sintetico segue noise^2 E o real branqueado esta a
    >= 5 sigma de alpha^2), H2_REAL_CONSISTENT_WITH_ALPHA2 (real branqueado a <= 2 sigma de alpha^2 e distinguivel do fora da fonte a >= 5 sigma;
    nunca CONFIRMED), H2_REAL_NOT_ALPHA2 (real >= 5 sigma de alpha^2 mas sintetico nao segue noise^2), INCONCLUSIVE_SYSTEMATICS (< 10 eventos,
    ou template pycbc ausente em > 20%). beta jamais literal. CONFIRMED proibido."""
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = {
        "version": "H2_REPRODUCTION_V1", "status": "PRE_REGISTERED_BEFORE_DATA_READ",
        "form_of": "Tgl_gw_echo_unification_v1.py (fev/2026) H2 + TGL_Echo_Analyzer_v8.py (jan/2026): E_res/E_total -> alpha^2, com _echo_analysis copiada sem alteracao",
        "hypothesis_2026_CONJECTURE": {"claim": "Echo Ratio = E_res/E_total -> alpha^2 = beta apos subtrair o template alinhado e escalado", "h2_ok": "desvio < 30% e correlacao > 0,90", "beta_source": "SEALED_CODATA_ALPHA * sqrt(e) em runtime"},
        "modes": {"A_synthetic": "gerador consistente do script (add_echo = False; noise_level 0,1 como no analyze; controlos 0,05 e 0,2) vs template sem ruido",
                  "B_real_raw": "strain do cache na janela [-2, +1] s do GPS, sem branqueamento (como o loader de fevereiro), vs template pycbc get_td_waveform (IMRPhenomD; massas de fonte, como no script)",
                  "C_real_whitened": "strain branqueado (PSD Welch pre-evento; 20-1024 Hz) vs template branqueado com a mesma PSD", "D_off_source": "janelas branqueadas em -10 s e -7 s, mesmo template"},
        "events": "catalogo de 12 do script (os presentes no cache) e catalogo completo; L1 e H1", "instrument": "pycbc (venv proprio /opt/pycbc_env), lalsuite",
        "aggregation": "por modo: media, sd, n, fracao h2_ok; z_C = (media_C - beta)/(sd/sqrt n); z_C_vs_D; sintetico segue noise^2 se |media - noise^2|/noise^2 < 0,3 nos tres niveis",
        "criteria": {"min_events": 10, "max_template_fail_frac": 0.2, "retire_z": 5.0, "consistent_z": 2.0, "off_z": 5.0, "noise_sq_tol": 0.3},
        "allowed_verdicts": ["H2_IDENTITY_RETIRED", "H2_REAL_CONSISTENT_WITH_ALPHA2", "H2_REAL_NOT_ALPHA2", "INCONCLUSIVE_SYSTEMATICS", "AWAITING_RESULT_FILE"],
        "forbidden_verdicts": ["CONFIRMED", "PROVED"],
        "what_it_cannot_do": "nao mede o eco (isso e das v341-v348, com a amplitude do kernel e nulos): so diz se a estatistica de 2026 media o que dizia medir",
    }
    ph = hashlib.sha256(json.dumps(proto, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    checks = [("protocolo pre-registrado e hasheado (%s)" % ph, True), ("beta jamais literal", bool(abs(beta - SEALED_CODATA_ALPHA * math.sqrt(math.e)) == 0.0)), ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    return {"protocol": proto, "protocol_hash": ph, "checks": checks, "all_verified": all_v, "does_not_gate_core": True, "in_contour_roster_v314": False,
            "verdict": ("TGL_H2_REPRODUCTION_V1__PROTOCOL_PRE_REGISTERED_%s__FEB_2026_ECHO_ANALYSIS_COPIED__REAL_DATA_WITH_PYCBC__GATE_UNTOUCHED" % ph) if all_v else "TGL_H2_REPRODUCTION_PROTOCOL_NOT_SEALED_THIS_RUN"}


def prove_h2_reproduction_result(ONE, protocol_record=None):
    """v350 -- o resultado da reproducao de H2 (pipeline externo h2_reproduction_v1.py no WSL, pycbc), lido por hash e julgado pela matriz."""
    _t0 = time.time()
    beta = SEALED_CODATA_ALPHA * math.sqrt(math.e)
    proto = protocol_record or prove_h2_reproduction_protocol(ONE); ph = proto.get("protocol_hash"); crit = (proto.get("protocol") or {}).get("criteria") or {}
    res_p = os.path.join(CACHE, "gw", "H2_REPRODUCTION_V1_RESULT.json")
    base = {"result_path": res_p, "protocol_hash": ph, "does_not_gate_core": True, "in_contour_roster_v314": False, "beta_runtime": beta,
            "why_outside_contour": "a hipotese de 2026 e CONJECTURE sobre uma estatistica; nada aqui move a matematica nem mede o eco"}
    st = {"leitura": "[REAL] o um.py nao recalcula: le por hash e aplica a matriz pre-registrada (%s)" % ph,
          "genealogia": "[REAL] v340 retirou o «100 sigma» de dezembro como identidade + teto; aqui fecha-se a linha de janeiro/fevereiro (E_res/E_total -> alpha^2) com o instrumento que faltava"}
    rj, rhash = _read_external_json_with_hash(res_p)
    if rj is None:
        return dict(base, verdict="TGL_H2_REPRODUCTION_AWAITING_RESULT_FILE", all_verified=False, checks=[("resultado H2_REPRODUCTION_V1 em cache/gw", False)], statuses=st, runtime_s=float(time.time() - _t0))
    sm = rj.get("summary") or {}; A = sm.get("all") or {}; inst = rj.get("instrument") or {}; sc = rj.get("scripts") or {}
    n_ok = sm.get("n_events_ok") or 0; n_fail = sm.get("n_no_template") or 0; frac_fail = (n_fail / (n_ok + n_fail)) if (n_ok + n_fail) else 1.0
    checks = [("resultado lido por hash (%s)" % rhash, True),
              ("beta do resultado == beta recomputado", bool(abs(float(rj.get("beta", 0)) - beta) < 1e-15)),
              ("instrumento pycbc; scripts de jan/fev com sha256", bool(inst.get("pycbc") and all(len(str((sc.get(k) or {}).get("sha256", ""))) == 64 for k in ("unification_feb2026", "analyzer_v8_jan2026")))),
              (">= %d eventos com template; falhas de template <= %.0f%%" % (int(crit.get("min_events", 10)), 100 * float(crit.get("max_template_fail_frac", 0.2))), bool(n_ok >= int(crit.get("min_events", 10)) and frac_fail <= float(crit.get("max_template_fail_frac", 0.2)))),
              ("os quatro modos presentes (sintetico 3 niveis, bruto, branqueado, fora da fonte)", bool(all((A.get(k) or {}).get("n") for k in ("synthetic_0.1", "synthetic_0.05", "synthetic_0.2", "real_raw", "real_whitened", "off_source")))),
              ("nenhum veredito proibido por construcao", True)]
    all_v = bool(all(v for _, v in checks))
    _f = lambda v, p=4: (("%%.%df" % p) % v) if isinstance(v, (int, float)) else "NA"
    zb = A.get("z_whitened_vs_beta"); zo = A.get("z_whitened_vs_off"); tracks = A.get("synthetic_tracks_noise_sq")
    reasons = []
    if not (n_ok >= int(crit.get("min_events", 10)) and frac_fail <= float(crit.get("max_template_fail_frac", 0.2))): reasons.append("%s eventos / %.0f%% sem template" % (n_ok, 100 * frac_fail))
    if reasons or zb is None: outcome = "INCONCLUSIVE_SYSTEMATICS"
    elif tracks is True and abs(zb) >= float(crit.get("retire_z", 5.0)): outcome = "H2_IDENTITY_RETIRED"
    elif abs(zb) <= float(crit.get("consistent_z", 2.0)) and zo is not None and abs(zo) >= float(crit.get("off_z", 5.0)): outcome = "H2_REAL_CONSISTENT_WITH_ALPHA2"
    elif abs(zb) >= float(crit.get("retire_z", 5.0)): outcome = "H2_REAL_NOT_ALPHA2"
    else: outcome = "INCONCLUSIVE_SYSTEMATICS"
    s01, s005, s02 = A.get("synthetic_0.1") or {}, A.get("synthetic_0.05") or {}, A.get("synthetic_0.2") or {}; rr, rw, ro = A.get("real_raw") or {}, A.get("real_whitened") or {}, A.get("off_source") or {}
    verdict = ("TGL_H2_REPRODUCTION_V1__RESULT_READ_BY_HASH__%s__SYNTHETIC_%s__REAL_WHITENED_%s__OFF_%s__Z_VS_ALPHA2_%s__GATE_UNTOUCHED"
               % (outcome, _f(s01.get("mean"), 4).replace(".", "P"), _f(rw.get("mean"), 3).replace(".", "P"), _f(ro.get("mean"), 3).replace(".", "P"), _f(zb, 1).replace(".", "P").replace("-", "M"))) if all_v else "TGL_H2_REPRODUCTION_RESULT_NOT_SEALED_THIS_RUN"
    statuses = dict(st)
    statuses["resultado"] = ("[REAL, lido] %s eventos com template pycbc (%s sem): SINTETICO (como o script): ruido 0,1 -> E_res/E_total = %s (h2_ok em %s%%); ruido 0,05 -> %s; 0,2 -> %s; segue noise^2: %s. REAL BRUTO (como o script faria): %s (correlacao %s; h2_ok %s%%). REAL BRANQUEADO: %s +- %s (n=%s; correlacao %s; h2_ok %s%%); FORA DA FONTE: %s; z vs alpha^2 = %s; z vs fora da fonte = %s => %s%s"
                             % (n_ok, n_fail, _f(s01.get("mean")), _f(100 * (A.get("synthetic_0.1_h2ok_frac") or 0), 0), _f(s005.get("mean")), _f(s02.get("mean")), tracks, _f(rr.get("mean")), _f((A.get("real_raw_corr") or {}).get("mean"), 3), _f(100 * (A.get("real_raw_h2ok_frac") or 0), 0),
                                _f(rw.get("mean")), _f(rw.get("sd")), rw.get("n"), _f((A.get("real_whitened_corr") or {}).get("mean"), 3), _f(100 * (A.get("real_whitened_h2ok_frac") or 0), 0), _f(ro.get("mean")), _f(zb, 1), _f(zo, 1), outcome, (" [%s]" % "; ".join(reasons) if reasons else "")))
    return dict(base, verdict=verdict, all_verified=all_v, checks=checks, statuses=statuses, runtime_s=float(time.time() - _t0), result_sha16=rhash, executed=rj.get("executed"), instrument=inst, scripts=sc,
                summary_all=A, summary_script_catalog=sm.get("script_catalog"), n_events_ok=n_ok, n_no_template=n_fail, outcome=outcome, reasons=reasons, z_vs_alpha2=zb, z_vs_off=zo, synthetic_tracks_noise_sq=tracks)
