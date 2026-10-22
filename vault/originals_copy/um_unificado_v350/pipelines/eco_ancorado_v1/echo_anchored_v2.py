# -*- coding: utf-8 -*-
"""ECHO_ANCHORED_V2 — o teste decisivo do eco COMPLETO: mesmo protocolo pre-registrado (um.py v343, hash 1e94f77689b5017e), agora com
lalsimulation (WSL/Ubuntu, wheels conferidos contra a PyPI) e DUAS FAMILIAS de template — o nulo de familia que faltava na V1.
Fixado antes de olhar o dado (identico a V1 salvo onde dito):
  * Template por familia (lalsimulation, dominio da frequencia, aligned spins do catalogo, iota = 0): familia A = IMRPhenomXAS (Phenom),
    familia B = SEOBNRv4 (EOB, dominio do tempo, transformado por SimInspiralFD). Analise com a familia A (primaria); NULO DE FAMILIA: injeta o sinal gerado pela familia B (mesma
    amplitude complexa, mesmo pico) em ruido fora da fonte e ajusta com a grade da familia A -> a induzido (e vice-versa, relatado).
  * Grade a +-1 sigma dos posteriores do catalogo; descasamento de parametros a +-0,5/+-1,5 sigma (como V1).
  * Ajuste conjunto de 4 parametros (primario ancorado pela inspiral + eco = burst do mesmo template atrasado, sinal -1, unidades de sqrt(beta)).
  * Nulos por injecao fora da fonte (primario-so; primario + eco); duas leis de atraso (MAY, KMS); empilhamento por variancia inversa.
  * Limiar de sistematica (pre-registrado): max(|descasamento de parametros|, |descasamento de familia|) <= 0,3.
Saida: JSON com numeros, hashes e versoes. O VEREDITO e do um.py (leitor por hash)."""
import os, sys, csv, json, math, time, hashlib, argparse
import numpy as np
import lal, lalsimulation as ls
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); A_PRED = math.sqrt(BETA); SIGN = -1.0
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
IALD = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD'); SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw')
PROTOCOL_HASH_EXPECTED = '1e94f77689b5017e'
FS = 4096.0; SEG_S = 2.5; T_PEAK = 2.0; F_LO, F_HI = 20.0, 1024.0
A_SPIN = 0.69; MW = 1.5251 - 1.1568 * (1 - A_SPIN) ** 0.1292; Q220 = 0.7000 + 1.4187 * (1 - A_SPIN) ** (-0.4990)
SQ = math.sqrt(1 - A_SPIN ** 2); KMS_FACTOR = 4 * math.pi * (1 + SQ) / SQ
OFF_START, OFF_END, OFF_STEP = -15.5, -3.0, 0.3
SNR_MIN, TRANSIENT_SD = 6.0, 10.0
GRID_SIG = (-1.0, 0.0, 1.0); MIS_SIG = (-1.5, -0.5, 0.5, 1.5)
FAMILIES = {'A': 'IMRPhenomXAS', 'B': 'SEOBNRv4'}   # B e TD: SimInspiralFD condiciona e transforma (o ROM exige dados externos ausentes)
LAWS = {'MAY': lambda Mf: (2 * G * Mf * MSUN / C ** 2) / C * math.log(1 / BETA), 'KMS': lambda Mf: KMS_FACTOR * G * Mf * MSUN / C ** 3}
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
def qnm(Mf): f0 = MW * C ** 3 / (2 * math.pi * G * Mf * MSUN); return f0, Q220 / (math.pi * f0)
def welch(x, fs, seg=4 * 4096):
    w = np.hanning(seg); step = seg // 2; n = (len(x) - seg) // step + 1; P = np.zeros(seg // 2 + 1)
    for i in range(n):
        xs = x[i * step:i * step + seg]; P += np.abs(np.fft.rfft((xs - xs.mean()) * w)) ** 2
    P *= 2.0 / (n * fs * np.sum(w ** 2)); return np.fft.rfftfreq(seg, 1 / fs), P
def band_mask(fr, lo, hi, ramp_lo=4.0, ramp_hi=50.0):
    m = np.ones_like(fr); m[fr < lo - ramp_lo] = 0; m[fr > hi + ramp_hi] = 0
    a = (fr >= lo - ramp_lo) & (fr < lo + ramp_lo); m[a] = 0.5 * (1 - np.cos(np.pi * (fr[a] - (lo - ramp_lo)) / (2 * ramp_lo)))
    b = (fr > hi - ramp_hi) & (fr <= hi + ramp_hi); m[b] = 0.5 * (1 + np.cos(np.pi * (fr[b] - (hi - ramp_hi)) / (2 * ramp_hi)))
    return m
def whiten32(x, fs, f, P):
    N = len(x); fr = np.fft.rfftfreq(N, 1 / fs); ft = np.fft.rfft(x)
    Pi = np.maximum(np.interp(fr, f, P, left=P[1], right=P[-1]), 1e-50)
    return np.fft.irfft(ft / np.sqrt(Pi * fs / 2) * band_mask(fr, F_LO, F_HI), n=N)
def analytic(x):
    X = np.fft.fft(x); n = len(x); hh = np.zeros(n); hh[0] = 1; hh[1:n // 2] = 2; hh[n // 2] = 1
    return np.fft.ifft(X * hh)
_tpl_cache = {}
def fd_waveform(fam, m1_det, m2_det, chi, n):
    """h+(f) da familia, no grid rfftfreq(n, 1/FS) (deltaF = FS/n), f_min 15 Hz, f_max = Nyquist; ou None se falhar."""
    df = FS / n; fmax = FS / 2
    try:
        appr = ls.GetApproximantFromString(FAMILIES[fam])
        hp, hc = ls.SimInspiralFD(m1_det * lal.MSUN_SI, m2_det * lal.MSUN_SI, 0.0, 0.0, chi, 0.0, 0.0, chi, 500e6 * lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, df, 15.0, fmax, 20.0, lal.CreateDict(), appr)
        H = np.array(hp.data.data, dtype=complex); nf = n // 2 + 1; dfr = float(hp.deltaF)
        if abs(dfr - df) > 1e-9:                       # reamostra (amplitude e fase) para o grid pedido
            fr_src = np.arange(len(H)) * dfr; fr_dst = np.arange(nf) * df
            amp = np.interp(fr_dst, fr_src, np.abs(H), left=0.0, right=0.0); ph = np.interp(fr_dst, fr_src, np.unwrap(np.angle(H)))
            H = amp * np.exp(1j * ph)
        if len(H) < nf: H = np.concatenate([H, np.zeros(nf - len(H), dtype=complex)])
        return H[:nf]
    except Exception as e:
        return None
def template_w(fam, m1_det, m2_det, chi, f_psd, P_psd, n, psd_id):
    key = (fam, round(m1_det, 5), round(m2_det, 5), round(chi, 4), n, psd_id)
    if key in _tpl_cache: return _tpl_cache[key]
    fr = np.fft.rfftfreq(n, 1 / FS); H = fd_waveform(fam, m1_det, m2_det, chi, n)
    if H is None or not np.isfinite(H).all() or np.abs(H).max() == 0:
        _tpl_cache[key] = None; return None
    Pi = np.maximum(np.interp(fr, f_psd, P_psd, left=P_psd[1], right=P_psd[-1]), 1e-50)
    Hw = H * np.exp(-2j * np.pi * fr * T_PEAK) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI)
    h = np.fft.irfft(Hw, n); h = h / (np.sqrt(np.sum(h ** 2)) + 1e-300); ha = analytic(h); ipk = int(np.argmax(np.abs(ha)))
    # convencao de tempo: o pico deve cair perto de T_PEAK; se cair no comeco (chirp invertido), conjuga
    if abs(ipk / FS - T_PEAK) > 0.5:
        h2 = np.fft.irfft(np.conj(H) * np.exp(-2j * np.pi * fr * T_PEAK) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI), n)
        h2 = h2 / (np.sqrt(np.sum(h2 ** 2)) + 1e-300); ha2 = analytic(h2); ipk2 = int(np.argmax(np.abs(ha2)))
        if abs(ipk2 / FS - T_PEAK) < abs(ipk / FS - T_PEAK): h, ha, ipk = h2, ha2, ipk2
    _tpl_cache[key] = (h, ha, ipk); return _tpl_cache[key]
def anchor(d, ha, ipk, t_guess=None, win_s=0.1):
    n = len(d); Fd = np.fft.fft(d); Fh = np.fft.fft(ha); corr = np.fft.ifft(Fd * np.conj(Fh)); norm = float(np.sum(np.abs(ha) ** 2))
    snr2 = np.abs(corr) ** 2 / norm; c = int(round(t_guess)); wn = int(win_s * FS); lo, hi = max(0, c - wn), min(n, c + wn)
    idx = np.arange(n); sel = (idx >= lo) & (idx < hi); s = int(idx[sel][np.argmax(snr2[sel])])
    return corr[s] / norm, s, float(np.sqrt(snr2[s]))
def joint_fit(d, h, ha, ipk, s, lag):
    n = len(d); hr = np.roll(np.real(ha), s); hi = np.roll(-np.imag(ha), s); ipk_abs = ipk + s
    br = np.zeros(n); bi = np.zeros(n); br[ipk_abs:] = hr[ipk_abs:]; bi[ipk_abs:] = hi[ipk_abs:]
    br = np.roll(br, lag); bi = np.roll(bi, lag); br[:lag] = 0; bi[:lag] = 0
    B = np.stack([hr, hi, br, bi]); Gm = B @ B.T; tr = float(np.trace(Gm))
    if not np.isfinite(tr) or tr < 1e-12: return float('nan'), -np.inf, np.zeros(n), np.zeros(n), ipk_abs, np.zeros(4)
    Gm = Gm + 1e-8 * tr / 4 * np.eye(4); r = B @ d
    try: cc = np.linalg.solve(Gm, r)
    except np.linalg.LinAlgError: cc = np.linalg.lstsq(Gm, r, rcond=None)[0]
    cn = cc[0] ** 2 + cc[1] ** 2
    a_hat = float(SIGN * (cc[2] * cc[0] + cc[3] * cc[1]) / (A_PRED * cn)) if cn > 0 else float('nan')
    return a_hat, float(cc @ r), cc[0] * hr + cc[1] * hi, SIGN * A_PRED * (cc[0] * br + cc[1] * bi), ipk_abs, cc
def analyze_series(d, tpls, Mf, law):
    n = len(d); tau = LAWS[law](Mf); lag = int(round(tau * FS)); f0, tau_d = qnm(Mf)
    best = None
    for key, t in tpls.items():
        if t is None: continue
        h, ha, ipk = t
        z1, s1, snr1 = anchor(d, ha, ipk, t_guess=T_PEAK * FS - ipk, win_s=0.1)
        for ds in (-2, -1, 0, 1, 2):
            a_hat, ss, p, e_pred, ipk_abs, cc = joint_fit(d, h, ha, ipk, s1 + ds, lag)
            if best is None or ss > best[0]: best = (ss, key, a_hat, p, e_pred, ipk_abs, s1 + ds, snr1, cc, ipk, ha)
    if best is None or not np.isfinite(best[0]):
        return dict(a_hat=float('nan'), snr_anchor=0.0, snr_full=0.0, grid=None, ipk_abs=0, lag=lag, tau_ms=tau * 1e3, tau_d_ms=tau_d * 1e3, p=np.zeros(n), e=np.zeros(n), z=0j, s=0)
    ss, key, a_hat, p, e_pred, ipk_abs, s, snr1, cc, ipk, ha = best
    return dict(a_hat=a_hat, snr_anchor=float(np.sqrt(max(cc[0] ** 2 + cc[1] ** 2, 0.0))), snr_full=snr1, grid=key, ipk_abs=ipk_abs, lag=lag, tau_ms=tau * 1e3, tau_d_ms=tau_d * 1e3, p=p, e=e_pred, z=complex(cc[0], cc[1]), s=s)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'ECHO_ANCHORED_V2_RESULT.json')); ap.add_argument('--n_off', type=int, default=40); ap.add_argument('--primary', default='A')
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x); PRIM = args.primary; OTHER = 'B' if PRIM == 'A' else 'A'
    t_start = time.time(); events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                Mf = float(r['final_mass_source']); z = float(r['redshift']); gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception: continue
            if only and r['commonName'] not in only: continue
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            def _e(k, default):
                try: return abs(float(r[k]))
                except Exception: return default
            m1e = 0.5 * (_e('mass_1_source_lower', 0.1 * m1) + _e('mass_1_source_upper', 0.1 * m1)); m2e = 0.5 * (_e('mass_2_source_lower', 0.1 * m2) + _e('mass_2_source_upper', 0.1 * m2))
            chie = 0.5 * (_e('chi_eff_lower', 0.15) + _e('chi_eff_upper', 0.15)) or 0.15
            events.append(dict(name=r['commonName'], gps=gps, Mf_det=Mf * (1 + z), m1=m1, m2=m2, z=z, chi_eff=chi, chi_sig=chie, m1_sig=m1e, m2_sig=m2e, snr_net=(float(r['network_matched_filter_snr']) if r['network_matched_filter_snr'] else None)))
    n_seg = int(SEG_S * FS); rows = []; sources = {}
    for ev in events:
        z1 = 1 + ev['z']; m1d, m2d = ev['m1'] * z1, ev['m2'] * z1
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: rows.append(dict(key='%s_%s' % (ev['name'], det), status='NAN_OR_FS')); continue
            sources[os.path.basename(p)] = sha256_file(p)
            trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd); psd_id = id(P_psd)
            def seg_at(t0_rel):
                i0 = int(round((t0_rel - T_PEAK - trel[0]) * fs)); return w32[i0:i0 + n_seg]
            d = seg_at(0.0)
            if len(d) < n_seg: rows.append(dict(key='%s_%s' % (ev['name'], det), status='SHORT')); continue
            sd = float(np.std(w32[(trel > -15) & (trel < -3)])); peak = float(np.max(np.abs(d[:int(1.8 * fs)])) / sd)
            def grid(fam, sig_list):
                out = {}
                for gm in sig_list:
                    for gc in sig_list:
                        chi = min(max(ev['chi_eff'] + gc * ev['chi_sig'], -0.99), 0.99)
                        out[(gm, gc)] = template_w(fam, m1d * (1 + gm * ev['m1_sig'] / ev['m1']), m2d * (1 + gm * ev['m2_sig'] / ev['m2']), chi, f_psd, P_psd, n_seg, psd_id)
                return out
            tpls = grid(PRIM, GRID_SIG)
            if all(v is None for v in tpls.values()): rows.append(dict(key='%s_%s' % (ev['name'], det), status='NO_TEMPLATE')); continue
            mis_tpls = {}
            for ms in MIS_SIG:
                mis_tpls[(ms, 0.0)] = template_w(PRIM, m1d * (1 + ms * ev['m1_sig'] / ev['m1']), m2d * (1 + ms * ev['m2_sig'] / ev['m2']), min(max(ev['chi_eff'], -0.99), 0.99), f_psd, P_psd, n_seg, psd_id)
                mis_tpls[(0.0, ms)] = template_w(PRIM, m1d, m2d, min(max(ev['chi_eff'] + ms * ev['chi_sig'], -0.99), 0.99), f_psd, P_psd, n_seg, psd_id)
            fam_tpl = template_w(OTHER, m1d, m2d, min(max(ev['chi_eff'], -0.99), 0.99), f_psd, P_psd, n_seg, psd_id)
            rec = dict(key='%s_%s' % (ev['name'], det), event=ev['name'], det=det, status='OK', Mf_det=ev['Mf_det'], m1_det=m1d, m2_det=m2d, chi_eff=ev['chi_eff'], chi_sig=ev['chi_sig'], snr_net=ev['snr_net'], peak_over_sd=peak, primary_family=FAMILIES[PRIM], other_family=FAMILIES[OTHER], laws={})
            offs = np.arange(OFF_START, OFF_END, OFF_STEP)[:args.n_off]
            for law in LAWS:
                on = analyze_series(d, tpls, ev['Mf_det'], law); p_on, e_on = on['p'], on['e']
                a_prim, a_both, a_mis, a_fam = [], [], {k: [] for k in mis_tpls}, []
                for ts in offs:
                    dk = seg_at(ts)
                    if len(dk) < n_seg: continue
                    a_prim.append(analyze_series(dk + p_on, tpls, ev['Mf_det'], law)['a_hat']); a_both.append(analyze_series(dk + p_on + e_on, tpls, ev['Mf_det'], law)['a_hat'])
                def inj_from(tp):
                    hm, ham, ipkm = tp; sh = on['ipk_abs'] - ipkm
                    return on['z'].real * np.roll(np.real(ham), sh) + on['z'].imag * np.roll(-np.imag(ham), sh)
                for k, tp in mis_tpls.items():
                    if tp is None: continue
                    pm = inj_from(tp)
                    for ts in offs[::4]:
                        dk = seg_at(ts)
                        if len(dk) < n_seg: continue
                        a_mis[k].append(analyze_series(dk + pm, tpls, ev['Mf_det'], law)['a_hat'])
                if fam_tpl is not None:
                    pf = inj_from(fam_tpl)
                    for ts in offs[::2]:
                        dk = seg_at(ts)
                        if len(dk) < n_seg: continue
                        a_fam.append(analyze_series(dk + pf, tpls, ev['Mf_det'], law)['a_hat'])
                a_prim = np.array(a_prim); a_both = np.array(a_both)
                bias = float(np.nanmean(a_prim)); sig = float(np.nanstd(a_prim, ddof=1)); recv = float(np.nanmean(a_both))
                mis = {'m%+.1fs/chi%+.1fs' % k: float(np.nanmean(v)) - bias for k, v in a_mis.items() if len(v)}
                fam_ind = (float(np.nanmean(a_fam)) - bias) if len(a_fam) else None
                rec['laws'][law] = dict(a_on=on['a_hat'], snr_anchor=on['snr_anchor'], snr_full=on['snr_full'], grid=(list(on['grid']) if on['grid'] else None), tau_ms=on['tau_ms'], tau_d_ms=on['tau_d_ms'], lag=on['lag'],
                                        bias=bias, sigma=sig, recovery=recv, n_off=int(len(a_prim)), mismatch_induced=mis, family_induced=fam_ind,
                                        used=bool(on['snr_anchor'] >= SNR_MIN and peak <= TRANSIENT_SD and sig > 0 and np.isfinite(on['a_hat'])))
            rows.append(rec)
            print('  %-22s %s' % (rec['key'], ' | '.join('%s: a=%.2f snr=%.1f sig=%.2f rec=%.2f mis=%.2f fam=%s used=%s' % (law, r2['a_on'], r2['snr_anchor'], r2['sigma'], r2['recovery'], max([abs(v) for v in r2['mismatch_induced'].values()] or [float('nan')]), ('%.2f' % r2['family_induced']) if r2['family_induced'] is not None else 'NA', r2['used']) for law, r2 in rec['laws'].items())), flush=True)
    stacks = {}
    for law in LAWS:
        use = [r for r in rows if r.get('status') == 'OK' and r['laws'][law]['used']]
        if not use: stacks[law] = dict(n_used=0); continue
        a = np.array([r['laws'][law]['a_on'] - r['laws'][law]['bias'] for r in use]); sg = np.array([r['laws'][law]['sigma'] for r in use]); rc = np.array([r['laws'][law]['recovery'] - r['laws'][law]['bias'] for r in use]); wg = 1 / sg ** 2
        a_c = float(np.sum(wg * a) / wg.sum()); s_c = float(1 / np.sqrt(wg.sum())); rec_c = float(np.sum(wg * rc) / wg.sum())
        keys = sorted(set(k for r in use for k in r['laws'][law]['mismatch_induced']))
        mis_c = {k: float(np.nansum(wg * np.array([r['laws'][law]['mismatch_induced'].get(k, np.nan) for r in use])) / wg.sum()) for k in keys}
        fam_vals = [(r['laws'][law]['family_induced'], 1 / r['laws'][law]['sigma'] ** 2) for r in use if r['laws'][law]['family_induced'] is not None]
        fam_c = (float(sum(v * w for v, w in fam_vals) / sum(w for _, w in fam_vals)) if fam_vals else None)
        mis_max = max([abs(v) for v in mis_c.values()] + ([abs(fam_c)] if fam_c is not None else []))
        stacks[law] = dict(n_used=len(use), a_over_sqrt_beta=a_c, sigma=s_c, z_det=a_c / s_c, z_excl_1=(1 - a_c) / s_c, recovery=rec_c, power_sigma=rec_c / s_c,
                           mean_bias=float(np.mean([r['laws'][law]['bias'] for r in use])), mismatch_induced=mis_c, family_induced=fam_c, n_family=len(fam_vals), mismatch_max_abs=mis_max,
                           mean_snr_anchor=float(np.mean([r['laws'][law]['snr_anchor'] for r in use])))
        print('STACK %s: n=%d a=%.3f+-%.3f z_det=%.2f z_excl=%.2f recup=%.3f poder=%.2f mis_param=%.3f familia=%s mis_max=%.3f' % (law, len(use), a_c, s_c, a_c / s_c, (1 - a_c) / s_c, rec_c, rec_c / s_c, max(abs(v) for v in mis_c.values()), ('%.3f' % fam_c) if fam_c is not None else 'NA', mis_max))
    out = dict(version='ECHO_ANCHORED_V2', protocol_hash_expected=PROTOCOL_HASH_EXPECTED, executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(lalsuite=lal.__version__, waveform='%s (primaria) + %s (nulo de familia); lalsimulation FD, aligned spins do catalogo' % (FAMILIES[PRIM], FAMILIES[OTHER]), python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env', family_null='sim: injecao da familia %s ajustada com a grade da familia %s' % (FAMILIES[OTHER], FAMILIES[PRIM])),
               beta=BETA, amplitude_predicted=A_PRED, sign=SIGN, laws={'MAY': '(2GM_f/c^3) ln(1/beta)', 'KMS': '2 pi/kappa Kerr a=0.69 = %.4f GM_f/c^3' % KMS_FACTOR},
               pipeline=dict(fs=FS, seg_s=SEG_S, t_peak=T_PEAK, band=[F_LO, F_HI], grid_sigma=GRID_SIG, mismatch_sigma=MIS_SIG, families=FAMILIES, primary=PRIM, snr_min=SNR_MIN, transient_sd=TRANSIENT_SD, n_off=args.n_off, systematics_rule='max(|descasamento de parametros|, |descasamento de familia|) <= 0.3'),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events=len(events), stacks=stacks, per_series=rows)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (o.tolist() if hasattr(o, 'tolist') else str(o))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start))
if __name__ == '__main__':
    main()
