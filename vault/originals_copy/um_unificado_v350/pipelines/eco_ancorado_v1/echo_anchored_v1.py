# -*- coding: utf-8 -*-
"""ECHO_ANCHORED_V1 — o teste decisivo do eco, EXECUTADO conforme o protocolo pre-registrado no um.py (v343, hash 1e94f77689b5017e).
Instrumento: gwfast 1.1.2 (IMRPhenomD, puro Python + jax; proveniencia: 16 wheels conferidos contra a PyPI) em gw_anchor_env (Python 3.12).
O que este script FAZ (fixado antes de olhar o dado):
  1. Para cada evento do catalogo GWTC (M_f, m1, m2, z, chi_eff, GPS) e cada detector (H1, L1) com strain de 32 s no cache de maio:
     PSD de Welch dos 14 s pre-evento; branqueamento; banda [20, 1024] Hz; segmento de analise de 2,5 s com o merger em t = 2,0 s.
  2. TEMPLATE IMRPhenomD (aligned, 22): Mc_det = Mc_src(1+z), eta de (m1, m2), chi1z = chi2z = chi_eff; grade pequena de intrinsecos
     (Mc e chi_eff a {-1, 0, +1} sigma do catalogo/posteriores); o template e branqueado com a MESMA PSD.
  3. ANCORAGEM CONJUNTA: passo 1 (correlacao) acha t_c; depois ajuste linear conjunto de 4 parametros (amplitude complexa do primario
     + amplitude complexa do eco = burst do MESMO template atrasado), em t_c +-2 amostras: a inspiral inteira ancora o primario, o eco e componente proprio.
  4. ESTATISTICA: no residuo d - p na janela W = [t_on, t_on + 6 tau_d], amplitude LSQ do template do eco e = -sqrt(beta) * p_burst(t - tau)
     (p_burst = o primario a partir do pico): a_hat, 1 = eco previsto.
  5. NULOS por injecao em ~40 janelas fora da fonte: primario so (vies, sigma), primario + eco previsto (recuperacao, poder),
     DESCASAMENTO (primario gerado a +-0,5 e +-1,5 sigma, entre e fora dos pontos da grade; sem eco) -> a induzido.
  6. Duas leis de atraso: MAY = (2GM_f/c^3) ln(1/beta); KMS = 2 pi/kappa (Kerr, spin 0.69). Empilhamento por variancia inversa.
  7. Saida: JSON com numeros, hashes (fontes, catalogo, protocolo) e versoes. O VEREDITO e emitido pelo um.py (leitor por hash), nao aqui.
Serie usada se SNR da ancoragem (passo 2) >= 6 e sem transiente > 10 sd no segmento. beta = alpha*sqrt(e) em runtime."""
import os, sys, csv, json, math, time, hashlib, argparse
import numpy as np
import gwfast
from gwfast.waveforms import IMRPhenomD
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); A_PRED = math.sqrt(BETA); SIGN = -1.0
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30
IALD = r'C:\IALD\projetos_pyhton\IALD'; SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
OUT_DIR = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw'
PROTOCOL_HASH_EXPECTED = '1e94f77689b5017e'
FS = 4096.0; SEG_S = 2.5; T_PEAK = 2.0; F_LO, F_HI = 20.0, 1024.0
A_SPIN = 0.69; MW = 1.5251 - 1.1568 * (1 - A_SPIN) ** 0.1292; Q220 = 0.7000 + 1.4187 * (1 - A_SPIN) ** (-0.4990)
SQ = math.sqrt(1 - A_SPIN ** 2); KMS_FACTOR = 4 * math.pi * (1 + SQ) / SQ
OFF_START, OFF_END, OFF_STEP = -15.5, -3.0, 0.3
SNR_MIN, TRANSIENT_SD = 6.0, 10.0
GRID_SIG = (-1.0, 0.0, 1.0); MIS_SIG = (-1.5, -0.5, 0.5, 1.5)   # em unidades da incerteza do catalogo (posteriores GWTC): grade +-1 sigma; descasamento entre e fora dos pontos da grade
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
WF = IMRPhenomD(); _tpl_cache = {}
def template_w(Mc_det, eta, chi, f_psd, P_psd, n):
    """template IMRPhenomD branqueado (mesma PSD), banda [20,1024], pico em T_PEAK; retorna serie real e analitica normalizadas."""
    key = (round(Mc_det, 6), round(eta, 6), round(chi, 4), n, id(P_psd))
    if key in _tpl_cache: return _tpl_cache[key]
    fr = np.fft.rfftfreq(n, 1 / FS); fm = fr.copy(); fm[0] = 1e-3
    ev = {'Mc': np.array([Mc_det]), 'eta': np.array([min(max(eta, 0.05), 0.25)]), 'dL': np.array([0.5]), 'iota': np.array([0.0]), 'chi1z': np.array([chi]), 'chi2z': np.array([chi]),
          'Phicoal': np.array([0.0]), 'tcoal': np.array([0.0]), 'theta': np.array([1.0]), 'phi': np.array([1.0]), 'psi': np.array([0.0])}
    A = np.array(WF.Ampl(fm, **ev), dtype=float).ravel(); Ph = np.array(WF.Phi(fm, **ev), dtype=float).ravel()
    A[~np.isfinite(A)] = 0; Ph[~np.isfinite(Ph)] = 0
    Pi = np.maximum(np.interp(fr, f_psd, P_psd, left=P_psd[1], right=P_psd[-1]), 1e-50)
    H = A * np.exp(-1j * Ph) * np.exp(-2j * np.pi * fr * T_PEAK) / np.sqrt(Pi * FS / 2) * band_mask(fr, F_LO, F_HI)
    h = np.fft.irfft(H, n); h = h / (np.sqrt(np.sum(h ** 2)) + 1e-300); ha = analytic(h)
    ipk = int(np.argmax(np.abs(ha)))
    _tpl_cache[key] = (h, ha, ipk); return _tpl_cache[key]
def anchor(d, ha, ipk, lag_mask=None, t_guess=None, win_s=0.1):
    """correlacao complexa normalizada de d (mascarada) com o template analitico; devolve (z, shift, snr). shift = deslocamento em amostras
    do template (pico do template cai em ipk + shift)."""
    n = len(d)
    if lag_mask is not None:
        dm = d * lag_mask
    else:
        dm = d
    Fd = np.fft.fft(dm); Fh = np.fft.fft(ha)
    corr = np.fft.ifft(Fd * np.conj(Fh))                      # corr[s] = sum_t dm[t] conj(ha[t - s])
    if lag_mask is not None:
        Fm = np.fft.fft(lag_mask); Fh2 = np.fft.fft(np.abs(ha) ** 2); norm = np.real(np.fft.ifft(Fm * np.conj(Fh2)))
        norm = np.maximum(norm, 1e-12 * norm.max())
    else:
        norm = np.full(n, float(np.sum(np.abs(ha) ** 2)))
    snr2 = np.abs(corr) ** 2 / norm
    if t_guess is None:
        lo, hi = 0, n
    else:
        c = int(round(t_guess)); wn = int(win_s * FS); lo, hi = max(0, c - wn), min(n, c + wn)
    idx = np.arange(n); sel = (idx >= lo) & (idx < hi)
    s = int(idx[sel][np.argmax(snr2[sel])])
    z = corr[s] / norm[s]                                       # amplitude complexa: p(t) = Re[z * ha(t - s)]
    return z, s, float(np.sqrt(snr2[s]))
def primary_from(z, ha, s):
    return np.real(z * np.roll(ha, s))
def echo_stat(d, p, ipk_abs, lag, tau_d_n):
    """a_hat na janela W = [ipk_abs + lag, + 6 tau_d]; e = -sqrt(beta) * p_burst(t - lag), p_burst = p a partir do pico."""
    n = len(d); burst = np.zeros(n); burst[ipk_abs:] = p[ipk_abs:]
    e = SIGN * A_PRED * np.roll(burst, lag); e[:lag] = 0
    i0 = ipk_abs + lag; i1 = min(n, i0 + int(6 * tau_d_n))
    r = (d - p)[i0:i1]; ee = e[i0:i1]; den = float(ee @ ee)
    return (float(r @ ee / den) if den > 0 else float('nan')), e
def joint_fit(d, h, ha, ipk, s, lag, tau_d_n):
    """ajuste CONJUNTO linear de 4 parametros: d ~ c1 h(t-s) + c2 hH(t-s) + d1 hb(t-s-lag) + d2 hHb(t-s-lag), hb = burst (t >= pico) de h.
    a_hat = -(d.c)/(sqrt(beta)|c|^2); o primario e ancorado pela inspiral inteira e o eco e um componente proprio (sem mascara)."""
    n = len(d); hr = np.roll(np.real(ha), s); hi = np.roll(-np.imag(ha), s); ipk_abs = ipk + s
    br = np.zeros(n); bi = np.zeros(n); br[ipk_abs:] = hr[ipk_abs:]; bi[ipk_abs:] = hi[ipk_abs:]
    br = np.roll(br, lag); bi = np.roll(bi, lag); br[:lag] = 0; bi[:lag] = 0
    B = np.stack([hr, hi, br, bi]); Gm = B @ B.T; tr = float(np.trace(Gm))
    if not np.isfinite(tr) or tr < 1e-12:                        # template degenerado (fcut abaixo da banda, etc.): serie invalida
        return float('nan'), -np.inf, np.zeros(n), np.zeros(n), ipk_abs, np.zeros(4)
    Gm = Gm + 1e-8 * tr / 4 * np.eye(4); r = B @ d
    try:
        cc = np.linalg.solve(Gm, r)
    except np.linalg.LinAlgError:
        cc = np.linalg.lstsq(Gm, r, rcond=None)[0]
    cn = cc[0] ** 2 + cc[1] ** 2
    a_hat = float(SIGN * (cc[2] * cc[0] + cc[3] * cc[1]) / (A_PRED * cn)) if cn > 0 else float('nan')
    p = cc[0] * hr + cc[1] * hi; e_pred = SIGN * A_PRED * (cc[0] * br + cc[1] * bi)
    return a_hat, float(cc @ r), p, e_pred, ipk_abs, cc
def analyze_series(d, tpls, Mf, law, mis_tpls, inject=None):
    """d: segmento branqueado (2,5 s). tpls: dict grade -> (h, ha, ipk). Ajuste conjunto primario+eco por grade; escolhe pela energia explicada."""
    n = len(d); tau = LAWS[law](Mf); lag = int(round(tau * FS)); f0, tau_d = qnm(Mf); tau_d_n = tau_d * FS
    best = None
    for key, (h, ha, ipk) in tpls.items():
        z1, s1, snr1 = anchor(d, ha, ipk, None, t_guess=T_PEAK * FS - ipk, win_s=0.1)
        for ds in (-2, -1, 0, 1, 2):
            a_hat, ss, p, e_pred, ipk_abs, cc = joint_fit(d, h, ha, ipk, s1 + ds, lag, tau_d_n)
            if best is None or ss > best[0]:
                best = (ss, key, a_hat, p, e_pred, ipk_abs, s1 + ds, snr1, cc)
    ss, key, a_hat, p, e_pred, ipk_abs, s, snr1, cc = best
    if not np.isfinite(ss):
        return dict(a_hat=float('nan'), snr_anchor=0.0, snr_full=snr1, grid=key, ipk_abs=ipk_abs, lag=lag, tau_ms=tau * 1e3, tau_d_ms=tau_d * 1e3, p=np.zeros(n), e=np.zeros(n), z=0j, s=s)
    snr_p = float(np.sqrt(max(cc[0] ** 2 + cc[1] ** 2, 0.0)))     # template normalizado a energia 1 em ruido branco: |c| = SNR do primario
    return dict(a_hat=a_hat, snr_anchor=snr_p, snr_full=snr1, grid=key, ipk_abs=ipk_abs, lag=lag, tau_ms=tau * 1e3, tau_d_ms=tau_d * 1e3, p=p, e=e_pred, z=complex(cc[0], cc[1]), s=s)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'ECHO_ANCHORED_V1_RESULT.json')); ap.add_argument('--n_off', type=int, default=40)
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x)
    t_start = time.time()
    events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                Mf = float(r['final_mass_source']); z = float(r['redshift']); gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception:
                continue
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            if only and r['commonName'] not in only: continue
            def _e(k, default):
                try: return abs(float(r[k]))
                except Exception: return default
            # incertezas do catalogo (posteriores): Mc a partir de (m1, m2) +- meia-largura media; chi_eff +- meia-largura media
            m1e = 0.5 * (_e('mass_1_source_lower', 0.1 * m1) + _e('mass_1_source_upper', 0.1 * m1)); m2e = 0.5 * (_e('mass_2_source_lower', 0.1 * m2) + _e('mass_2_source_upper', 0.1 * m2))
            chie = 0.5 * (_e('chi_eff_lower', 0.15) + _e('chi_eff_upper', 0.15)) or 0.15
            def _mc(a, b): return (a * b) ** 0.6 / (a + b) ** 0.2
            mc_sig = 0.5 * (_mc(m1 + m1e, m2 + m2e) - _mc(max(m1 - m1e, 1.0), max(m2 - m2e, 1.0)))
            events.append(dict(name=r['commonName'], gps=gps, Mf_det=Mf * (1 + z), m1=m1, m2=m2, z=z, chi_eff=chi, chi_sig=chie, mc_sig_rel=mc_sig / _mc(m1, m2),
                               snr_net=(float(r['network_matched_filter_snr']) if r['network_matched_filter_snr'] else None)))
    n_seg = int(SEG_S * FS); rows = []; sources = {}
    for ev in events:
        Mtot = (ev['m1'] + ev['m2']) * (1 + ev['z']); eta = ev['m1'] * ev['m2'] / (ev['m1'] + ev['m2']) ** 2; Mc_det = Mtot * eta ** 0.6
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: rows.append(dict(key='%s_%s' % (ev['name'], det), status='NAN_OR_FS')); continue
            sources[os.path.basename(p)] = sha256_file(p)
            trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd)
            def seg_at(t0_rel):   # segmento de 2,5 s cujo t = T_PEAK coincide com t0_rel (relativo ao GPS)
                i0 = int(round((t0_rel - T_PEAK - trel[0]) * fs)); return w32[i0:i0 + n_seg]
            d = seg_at(0.0)
            if len(d) < n_seg: rows.append(dict(key='%s_%s' % (ev['name'], det), status='SHORT')); continue
            sd = float(np.std(w32[(trel > -15) & (trel < -3)])); peak = float(np.max(np.abs(d[:int(1.8 * fs)])) / sd)
            tpls = {}
            for gm in GRID_SIG:
                for gc in GRID_SIG:
                    chi = min(max(ev['chi_eff'] + gc * ev['chi_sig'], -0.9), 0.9); tpls[(gm, gc)] = template_w(Mc_det * (1 + gm * ev['mc_sig_rel']), eta, chi, f_psd, P_psd, n_seg)
            mis_tpls = {}
            for ms in MIS_SIG:
                mis_tpls[(ms, 0.0)] = template_w(Mc_det * (1 + ms * ev['mc_sig_rel']), eta, min(max(ev['chi_eff'], -0.9), 0.9), f_psd, P_psd, n_seg)
                mis_tpls[(0.0, ms)] = template_w(Mc_det, eta, min(max(ev['chi_eff'] + ms * ev['chi_sig'], -0.9), 0.9), f_psd, P_psd, n_seg)
            rec = dict(key='%s_%s' % (ev['name'], det), event=ev['name'], det=det, status='OK', Mf_det=ev['Mf_det'], Mc_det=Mc_det, eta=eta, chi_eff=ev['chi_eff'], mc_sig_rel=ev['mc_sig_rel'], chi_sig=ev['chi_sig'], snr_net=ev['snr_net'], peak_over_sd=peak, laws={})
            for law in LAWS:
                on = analyze_series(d, tpls, ev['Mf_det'], law, mis_tpls)
                p_on, e_on = on['p'], on['e']
                # injecoes fora da fonte: primario ancorado (fixo) e primario + eco previsto; descasamento: primario FORA da grade, mesma escala/fase/t
                offs = np.arange(OFF_START, OFF_END, OFF_STEP)[:args.n_off]
                a_prim, a_both, a_mis = [], [], {k: [] for k in mis_tpls}
                for ts in offs:
                    dk = seg_at(ts)
                    if len(dk) < n_seg: continue
                    a_prim.append(analyze_series(dk + p_on, tpls, ev['Mf_det'], law, mis_tpls)['a_hat'])
                    a_both.append(analyze_series(dk + p_on + e_on, tpls, ev['Mf_det'], law, mis_tpls)['a_hat'])
                for k, (hm, ham, ipkm) in mis_tpls.items():
                    pm = on['z'].real * np.roll(np.real(ham), on['ipk_abs'] - ipkm) + on['z'].imag * np.roll(-np.imag(ham), on['ipk_abs'] - ipkm)    # mesmo pico, mesma amplitude complexa
                    for ts in offs[::4]:
                        dk = seg_at(ts)
                        if len(dk) < n_seg: continue
                        a_mis[k].append(analyze_series(dk + pm, tpls, ev['Mf_det'], law, mis_tpls)['a_hat'])
                a_prim = np.array(a_prim); a_both = np.array(a_both)
                bias = float(np.nanmean(a_prim)); sig = float(np.nanstd(a_prim, ddof=1)); recv = float(np.nanmean(a_both))
                mis = {'Mc%+.1fs/chi%+.1fs' % k: float(np.nanmean(v)) - bias for k, v in a_mis.items() if len(v)}
                rec['laws'][law] = dict(a_on=on['a_hat'], snr_anchor=on['snr_anchor'], snr_full=on['snr_full'], grid=list(on['grid']), tau_ms=on['tau_ms'], tau_d_ms=on['tau_d_ms'], lag=on['lag'],
                                        bias=bias, sigma=sig, recovery=recv, n_off=int(len(a_prim)), mismatch_induced=mis,
                                        used=bool(on['snr_anchor'] >= SNR_MIN and peak <= TRANSIENT_SD and sig > 0 and np.isfinite(on['a_hat'])))
            rows.append(rec)
            print('  %-22s %s' % (rec['key'], ' | '.join('%s: a=%.2f snr=%.1f bias=%.2f sig=%.2f rec=%.2f mis_max=%.2f used=%s' % (law, r2['a_on'], r2['snr_anchor'], r2['bias'], r2['sigma'], r2['recovery'], max([abs(v) for v in r2['mismatch_induced'].values()] or [float('nan')]), r2['used']) for law, r2 in rec['laws'].items())), flush=True)
    stacks = {}
    for law in LAWS:
        use = [r for r in rows if r.get('status') == 'OK' and r['laws'][law]['used']]
        if not use: stacks[law] = dict(n_used=0); continue
        a = np.array([r['laws'][law]['a_on'] - r['laws'][law]['bias'] for r in use]); sg = np.array([r['laws'][law]['sigma'] for r in use]); rc = np.array([r['laws'][law]['recovery'] - r['laws'][law]['bias'] for r in use]); wg = 1 / sg ** 2
        a_c = float(np.sum(wg * a) / wg.sum()); s_c = float(1 / np.sqrt(wg.sum())); rec_c = float(np.sum(wg * rc) / wg.sum())
        keys = sorted(set(k for r in use for k in r['laws'][law]['mismatch_induced']))
        mis_c = {k: float(np.sum(wg * np.array([r['laws'][law]['mismatch_induced'].get(k, np.nan) for r in use])) / wg.sum()) for k in keys}
        stacks[law] = dict(n_used=len(use), a_over_sqrt_beta=a_c, sigma=s_c, z_det=a_c / s_c, z_excl_1=(1 - a_c) / s_c, recovery=rec_c, power_sigma=rec_c / s_c,
                           mean_bias=float(np.mean([r['laws'][law]['bias'] for r in use])), mismatch_induced=mis_c, mismatch_max_abs=(max(abs(v) for v in mis_c.values()) if mis_c else None),
                           mean_snr_anchor=float(np.mean([r['laws'][law]['snr_anchor'] for r in use])))
        print('STACK %s: n=%d a=%.3f+-%.3f z_det=%.2f z_excl=%.2f recup=%.3f poder=%.2f mis_max=%s' % (law, len(use), a_c, s_c, a_c / s_c, (1 - a_c) / s_c, rec_c, rec_c / s_c, stacks[law]['mismatch_max_abs']))
    out = dict(version='ECHO_ANCHORED_V1', protocol_hash_expected=PROTOCOL_HASH_EXPECTED, executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(gwfast=gwfast.__version__, waveform='IMRPhenomD (aligned, 22; gwfast)', python=sys.version.split()[0], env='gw_anchor_env', note='lalsimulation/pycbc ausentes; IMRPhenomD = "equivalente" declarado; nulo de familia (Phenom vs SEOB) NAO disponivel -> substituido por descasamento de parametros fora da grade'),
               beta=BETA, amplitude_predicted=A_PRED, sign=SIGN, laws={'MAY': '(2GM_f/c^3) ln(1/beta)', 'KMS': '2 pi/kappa Kerr a=0.69 = %.4f GM_f/c^3' % KMS_FACTOR},
               pipeline=dict(fs=FS, seg_s=SEG_S, t_peak=T_PEAK, band=[F_LO, F_HI], grid_sigma=GRID_SIG, mismatch_sigma=MIS_SIG, sigma_source='incertezas do catalogo GWTC (posteriores): Mc de (m1,m2) +- meia-largura; chi_eff +- meia-largura', snr_min=SNR_MIN, transient_sd=TRANSIENT_SD, n_off=args.n_off),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events=len(events), stacks=stacks, per_series=[{k: v for k, v in r.items()} for r in rows])
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (o.tolist() if hasattr(o, 'tolist') else str(o))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start))
if __name__ == '__main__':
    main()
