# -*- coding: utf-8 -*-
"""ECHO_SEARCH_V1 — a busca de ecos de LONGO atraso (0,1–2,0 s) com coincidencia H1/L1: o `search_for_echoes` do protocolo de observacao de
outubro de 2025 (Observavel 1.2: t_echo = (2GM/c^3) ln(r_halo/r_H) ~ 0,1–1 s; A_echo/A_prim ~ 0,01–0,1; picos > 3 sigma; coincidencia em 10 ms;
«confirmar: 3+ ecos > 5 sigma com padrao de Delta t consistente»), herdado na forma e completado com o que faltava. Fixado ANTES de olhar o dado:
  * Dado: cache de maio (GWOSC, 32 s @ 4096 Hz), H1 E L1 presentes e limpos (a coincidencia exige os dois). PSD Welch dos 14 s pre-evento;
    branqueamento restrito a banda [50, 300] Hz (a do protocolo). Merger por detector = ancoragem por filtro casado (IMRPhenomD nos parametros
    do catalogo, ±100 ms do GPS) — nao o GPS grosseiro. Amplitude de referencia do primario A_prim = pico da envoltoria em ±20 ms do merger,
    em unidades da sigma fora da fonte. Previsao TGL para o pico do eco: h_pred = sqrt(beta) * A_prim (amplitude do kernel; sinal -1 irrelevante
    para a envoltoria).
  * Busca on-source: envoltoria analitica em [t_merger + 0,1; t_merger + 2,0] s por detector, em sigmas; picos > 3 (separacao minima 10 ms);
    coincidencia = |tau_H1 - tau_L1| < 10 ms (tau medido a partir do merger de cada detector). Estatistica por candidato: media das alturas
    (como no protocolo) e a soma em quadratura.
  * Fundo (nulo): a MESMA busca em K = 6 janelas de 1,9 s fora da fonte (pre-evento, [-14, -2] s), por evento -> taxa de coincidencias por janela.
  * Injecao (eficiencia): o template PhenomD ajustado (amplitude complexa do filtro casado), parte pos-pico, escalado por sqrt(beta) e injetado nas
    janelas de fundo com atraso tau ~ U[0,1; 2,0] s (N = 6 por evento; mesmo tau nos dois detectores, cada um a partir do seu merger) ->
    fracao recuperada como coincidencia a < 10 ms de tau = eps_i. E_det = soma eps_i = numero esperado de deteccoes se TODO merger tivesse um eco
    de amplitude sqrt(beta) em [0,1; 2,0] s.
  * Padrao: KS do atraso adimensional tau/(G M_f/c^3) dos candidatos on-source contra o dos candidatos de fundo.
  * Agregacao: N_on (coincidencias on-source), B_exp (fundo esperado = soma das taxas), z de Poisson; p_excl = P(N <= N_on | mu = B_exp + E_det).
beta = alpha*sqrt(e) em runtime. O VEREDITO e do um.py."""
import os, sys, csv, json, math, time, hashlib, argparse, warnings
import numpy as np
import lal, lalsimulation as ls
from scipy.signal import find_peaks
from scipy.stats import ks_2samp, poisson
warnings.filterwarnings('ignore')
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); A_PRED = math.sqrt(BETA); SIGN = -1.0
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
IALD = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD'); SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw')
FS = 4096.0; F_LO, F_HI = 50.0, 300.0; F_MIN_TPL = 20.0
SEG_S = 6.0; T_PEAK = 5.0; ANCHOR_WIN = 0.1; ANCHOR_MIN = 6.0
WIN = (0.1, 2.0); THR = 3.0; COINC = 0.010; MIN_SEP = 0.010; PRIM_WIN = 0.020
BG_STARTS = (-14.0, -12.0, -10.0, -8.0, -6.0, -4.0); N_INJ = 6; LOUD = 5.0
TEMPLATE = 'IMRPhenomD'
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
def welch(x, fs, seg=4 * 4096):
    w = np.hanning(seg); step = seg // 2; n = (len(x) - seg) // step + 1; P = np.zeros(seg // 2 + 1)
    for i in range(n):
        xs = x[i * step:i * step + seg]; P += np.abs(np.fft.rfft((xs - xs.mean()) * w)) ** 2
    P *= 2.0 / (n * fs * np.sum(w ** 2)); return np.fft.rfftfreq(seg, 1 / fs), P
def band_mask(fr, lo, hi, ramp_lo=4.0, ramp_hi=20.0):
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
def fd_waveform(m1_det, m2_det, chi, n):
    df = FS / n; fmax = FS / 2
    try:
        appr = ls.GetApproximantFromString(TEMPLATE)
        hp, hc = ls.SimInspiralFD(m1_det * lal.MSUN_SI, m2_det * lal.MSUN_SI, 0.0, 0.0, chi, 0.0, 0.0, chi, 500e6 * lal.PC_SI, 0.0, 0.0, 0.0, 0.0, 0.0, df, F_MIN_TPL, fmax, F_MIN_TPL, lal.CreateDict(), appr)
        H = np.array(hp.data.data, dtype=complex); nf = n // 2 + 1; dfr = float(hp.deltaF)
        if abs(dfr - df) > 1e-9:
            fr_src = np.arange(len(H)) * dfr; fr_dst = np.arange(nf) * df
            amp = np.interp(fr_dst, fr_src, np.abs(H), left=0.0, right=0.0); ph = np.interp(fr_dst, fr_src, np.unwrap(np.angle(H)))
            H = amp * np.exp(1j * ph)
        if len(H) < nf: H = np.concatenate([H, np.zeros(nf - len(H), dtype=complex)])
        H = H[:nf]
        return H if (np.isfinite(H).all() and np.abs(H).max() > 0) else None
    except Exception:
        return None
def template_w(H, f_psd, P_psd, n):
    fr = np.fft.rfftfreq(n, 1 / FS); Pi = np.maximum(np.interp(fr, f_psd, P_psd, left=P_psd[1], right=P_psd[-1]), 1e-50); W = band_mask(fr, F_LO, F_HI) / np.sqrt(Pi * FS / 2)
    h = np.fft.irfft(H * W * np.exp(-2j * np.pi * fr * T_PEAK), n); ha = analytic(h); ipk = int(np.argmax(np.abs(ha)))
    h2 = np.fft.irfft(np.conj(H) * W * np.exp(-2j * np.pi * fr * T_PEAK), n); ha2 = analytic(h2); ipk2 = int(np.argmax(np.abs(ha2)))
    if abs(ipk2 / FS - T_PEAK) < abs(ipk / FS - T_PEAK): h, ha, ipk = h2, ha2, ipk2
    nrm = math.sqrt(float(np.sum(h ** 2))) + 1e-300; return h / nrm, ha / nrm, ipk
def anchor(d, ha, ipk):
    n = len(d); Fd = np.fft.fft(d); Fh = np.fft.fft(ha); corr = np.fft.ifft(Fd * np.conj(Fh)); norm = float(np.sum(np.abs(ha) ** 2))
    snr2 = np.abs(corr) ** 2 / norm; c = int(T_PEAK * FS) - ipk; wn = int(ANCHOR_WIN * FS); idx = np.arange(n); sel = (idx >= c - wn) & (idx < c + wn)
    s = int(idx[sel][np.argmax(snr2[sel])]); return s, float(math.sqrt(snr2[s])), corr[s] / norm
def peaks_sigma(env_sig, i0, i1, thr):
    seg = env_sig[i0:i1]; pk, pr = find_peaks(seg, height=thr, distance=int(MIN_SEP * FS)); return (pk + i0), pr.get('peak_heights', np.array([]))
def coincidences(tH, hH, tL, hL):
    out = []
    for i, t1 in enumerate(tH):
        for j, t2 in enumerate(tL):
            if abs(t1 - t2) < COINC: out.append(dict(tau=float(0.5 * (t1 + t2)), h_H1=float(hH[i]), h_L1=float(hL[j]), mean=float(0.5 * (hH[i] + hL[j])), quad=float(math.sqrt(hH[i] ** 2 + hL[j] ** 2))))
    return out
def search(envH, envL, mH, mL, t_start, t_end, thr=THR):
    """envX em sigmas (serie inteira); mX = indice do merger no detector X; busca em [m + t_start, m + t_end] -> coincidencias em tau (s desde o merger)."""
    iH0, iH1 = mH + int(t_start * FS), mH + int(t_end * FS); iL0, iL1 = mL + int(t_start * FS), mL + int(t_end * FS)
    pH, hH = peaks_sigma(envH, iH0, iH1, thr); pL, hL = peaks_sigma(envL, iL0, iL1, thr)
    return coincidences((pH - mH) / FS, hH, (pL - mL) / FS, hL), int(len(pH)), int(len(pL))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'ECHO_SEARCH_V1_RESULT.json')); ap.add_argument('--n_inj', type=int, default=N_INJ)
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x); t_start = time.time(); rng = np.random.default_rng(20251001)
    events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                z = float(r['redshift']); gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception: continue
            if only and r['commonName'] not in only: continue
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            st, mfrac, af = ls.SimIMREOBFinalMassSpin(m1, m2, [0.0, 0.0, chi], [0.0, 0.0, chi], ls.SEOBNRv4)
            events.append(dict(name=r['commonName'], gps=gps, m1=m1, m2=m2, z=z, chi=min(max(chi, -0.99), 0.99), Mf_det=mfrac * (m1 + m2) * (1 + z), snr_net=(float(r['network_matched_filter_snr']) if r['network_matched_filter_snr'] else None)))
    n_seg = int(SEG_S * FS); rows = []; sources = {}; skipped = []
    for ev in events:
        dets = {}
        for det in ('H1', 'L1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: continue
            sources[os.path.basename(p)] = sha256_file(p); trel = t - ev['gps']; f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten32(s32, fs, f_psd, P_psd)
            sd = float(np.std(w32[(trel > -15) & (trel < -3)])); env = np.abs(analytic(w32)) / sd
            i0 = int(round((0.0 - T_PEAK - trel[0]) * fs)); d = w32[i0:i0 + n_seg]
            if len(d) < n_seg: continue
            H = fd_waveform(ev['m1'] * (1 + ev['z']), ev['m2'] * (1 + ev['z']), ev['chi'], n_seg)
            if H is None: continue
            h, ha, ipk = template_w(H, f_psd, P_psd, n_seg); s_shift, snr_anc, zc = anchor(d, ha, ipk)
            m_abs = i0 + ipk + s_shift   # indice do merger na serie de 32 s
            # primario ajustado (para injecao): Re[zc * ha] deslocado; parte pos-pico
            fit = np.real(zc * np.roll(ha, s_shift)); post = fit[ipk + s_shift:ipk + s_shift + int(0.25 * FS)]
            A_prim = float(np.max(env[max(0, m_abs - int(PRIM_WIN * FS)):m_abs + int(PRIM_WIN * FS)]))
            dets[det] = dict(env=env, w=w32, m=int(m_abs), sd=sd, snr_anc=snr_anc, A_prim=A_prim, post=post / sd, trel0=float(trel[0]), n=len(w32))
        if len(dets) < 2: skipped.append((ev['name'], 'NEED_H1_AND_L1')); continue
        if min(dets[d]['snr_anc'] for d in dets) < ANCHOR_MIN: skipped.append((ev['name'], 'ANCHOR_%s' % {d: round(dets[d]['snr_anc'], 1) for d in dets})); continue
        H1, L1 = dets['H1'], dets['L1']
        on, nH, nL = search(H1['env'], L1['env'], H1['m'], L1['m'], WIN[0], WIN[1])
        gm = G * ev['Mf_det'] * MSUN / C ** 3
        bg = []; bg_counts = []
        for bs in BG_STARTS:
            off = int(bs * FS)
            c, a, b = search(H1['env'], L1['env'], H1['m'] + off, L1['m'] + off, WIN[0], WIN[1]); bg.extend(c); bg_counts.append(len(c))
        # injecoes de eficiencia: eco = SIGN*sqrt(beta)*post-pico do primario, no mesmo tau nos dois detectores, em janelas de fundo
        inj = []
        for k in range(args.n_inj):
            tau = float(rng.uniform(WIN[0], WIN[1])); bs = BG_STARTS[k % len(BG_STARTS)]; off = int(bs * FS); rec = {}
            for name, D in (('H1', H1), ('L1', L1)):
                e2 = D['w'].copy() / D['sd']; j0 = D['m'] + off + int(tau * FS); L = min(len(D['post']), len(e2) - j0)
                if L <= 0: rec[name] = None; continue
                e2[j0:j0 + L] += SIGN * A_PRED * D['post'][:L]; rec[name] = np.abs(analytic(e2))
            if rec['H1'] is None or rec['L1'] is None: continue
            c, a, b = search(rec['H1'], rec['L1'], H1['m'] + off, L1['m'] + off, WIN[0], WIN[1])
            hit = any(abs(x['tau'] - tau) < COINC for x in c)
            inj.append(dict(tau=tau, hit=bool(hit), h_pred_H1=A_PRED * H1['A_prim'], h_pred_L1=A_PRED * L1['A_prim'], best_mean=(max([x['mean'] for x in c if abs(x['tau'] - tau) < COINC]) if hit else None)))
        eps = (sum(1 for x in inj if x['hit']) / len(inj)) if inj else None
        rows.append(dict(event=ev['name'], Mf_det=ev['Mf_det'], gm_s=gm, snr_net=ev['snr_net'], anchor_snr={'H1': H1['snr_anc'], 'L1': L1['snr_anc']}, A_prim={'H1': H1['A_prim'], 'L1': L1['A_prim']},
                         h_pred={'H1': A_PRED * H1['A_prim'], 'L1': A_PRED * L1['A_prim']}, n_on=len(on), on=on, n_peaks_on={'H1': nH, 'L1': nL}, bg_counts=bg_counts, bg_rate=float(np.mean(bg_counts)), bg=bg, inj=inj, eff=eps,
                         loud_on=[x for x in on if x['mean'] >= LOUD]))
        print('  %-22s anc=%s A_prim=%s h_pred=%s | on: %d coinc (%s) | fundo %.2f/janela | eff(sqrt beta)=%s' % (ev['name'], {d: round(v, 1) for d, v in rows[-1]['anchor_snr'].items()}, {d: round(v, 1) for d, v in rows[-1]['A_prim'].items()}, {d: round(v, 2) for d, v in rows[-1]['h_pred'].items()}, len(on), [round(x['tau'], 3) for x in on][:6], rows[-1]['bg_rate'], eps), flush=True)
    N_on = sum(r['n_on'] for r in rows); B_exp = sum(r['bg_rate'] for r in rows); E_det = sum((r['eff'] or 0.0) for r in rows)
    z_pois = (N_on - B_exp) / math.sqrt(max(B_exp, 1e-9)); p_excess = float(poisson.sf(N_on - 1, B_exp)) if B_exp > 0 else None
    p_excl = float(poisson.cdf(N_on, B_exp + E_det)) if (B_exp + E_det) > 0 else None
    tau_on = [x['tau'] / r['gm_s'] for r in rows for x in r['on']]; tau_bg = [x['tau'] / r['gm_s'] for r in rows for x in r['bg']]
    ks = ks_2samp(tau_on, tau_bg) if (len(tau_on) >= 3 and len(tau_bg) >= 3) else None
    n_loud_events = sum(1 for r in rows if r['loud_on']); loud_list = [(r['event'], [round(x['tau'], 3) for x in r['loud_on']], [round(x['mean'], 2) for x in r['loud_on']]) for r in rows if r['loud_on']]
    bg_rate_mean = float(np.mean([r['bg_rate'] for r in rows])) if rows else None
    summary = dict(n_events=len(rows), n_skipped=len(skipped), N_on=N_on, B_exp=B_exp, z_poisson=z_pois, p_excess=p_excess, E_det=E_det, p_excl=p_excl, mean_eff=(E_det / len(rows) if rows else None),
                   bg_rate_mean_per_window=bg_rate_mean, n_loud_events=n_loud_events, loud=loud_list, ks_tau_over_M=(dict(stat=float(ks.statistic), p=float(ks.pvalue), n_on=len(tau_on), n_bg=len(tau_bg)) if ks else None),
                   h_pred_median={'H1': float(np.median([r['h_pred']['H1'] for r in rows])) if rows else None, 'L1': float(np.median([r['h_pred']['L1'] for r in rows])) if rows else None})
    print('RESUMO: eventos %d | N_on %d | B_exp %.2f | z %.2f | p_excess %s | E_det %.2f (eff media %s) | p_excl %s | eventos com coinc >= 5: %d | KS tau/M %s | h_pred mediana %s' % (
        len(rows), N_on, B_exp, z_pois, ('%.3g' % p_excess) if p_excess is not None else 'NA', E_det, ('%.3f' % summary['mean_eff']) if summary['mean_eff'] is not None else 'NA', ('%.3g' % p_excl) if p_excl is not None else 'NA', n_loud_events, ('p=%.3g' % ks.pvalue) if ks else 'NA', {k: (round(v, 2) if v else None) for k, v in summary['h_pred_median'].items()}), flush=True)
    out = dict(version='ECHO_SEARCH_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start,
               instrument=dict(lalsuite=lal.__version__, anchor_template=TEMPLATE, final_state='SimIMREOBFinalMassSpin (SEOBNRv4)', python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env', scipy=__import__('scipy').__version__),
               beta=BETA, a_pred=A_PRED, sign=SIGN, protocol_2025=dict(window_s=list(WIN), band_hz=[F_LO, F_HI], threshold_sigma=THR, coincidence_s=COINC, confirm='3+ ecos > 5 sigma com padrao de Delta t consistente'),
               pipeline=dict(fs=FS, band=[F_LO, F_HI], window=list(WIN), threshold=THR, coincidence=COINC, min_sep=MIN_SEP, prim_win=PRIM_WIN, anchor_min=ANCHOR_MIN, bg_starts=list(BG_STARTS), n_inj=args.n_inj, loud=LOUD, inj_amplitude='sqrt(beta) x primario ajustado (pos-pico), sinal -1', rng_seed=20251001),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, n_events_catalog=len(events), skipped=skipped, summary=summary, per_event=rows)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (bool(o) if isinstance(o, np.bool_) else (o.tolist() if hasattr(o, 'tolist') else str(o)))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start), flush=True)
if __name__ == '__main__':
    main()
