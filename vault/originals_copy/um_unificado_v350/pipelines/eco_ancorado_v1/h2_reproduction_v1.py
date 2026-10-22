# -*- coding: utf-8 -*-
"""H2_REPRODUCTION_V1 — a reproducao, com pycbc e dados reais, da hipotese H2 do Protocolo #12 (Tgl_gw_echo_unification_v1.py, fev/2026) e do
Echo Analyzer v8 (jan/2026): «a fase pos-ringdown apresenta Echo Ratio = E_res/E_total -> alpha^2 = 0,012031», com criterio h2_ok = desvio < 30% e
correlacao > 0,90. Roda no WSL (/opt/pycbc_env: pycbc 2.11). Fixado ANTES de olhar o dado:
  * `_echo_analysis` COPIADA do script de fevereiro (normaliza, correlaciona, alinha, escala pela amplitude otima, E_res/E_total = 1 - rho^2 na pratica).
  * (A) SINTETICO, como o script fazia em modo «synthetic»: dado = gerador consistente com noise_level = 0,1 (add_echo = False, como no analyze) e
    template = gerador consistente sem ruido; ALEM DISSO os niveis 0,05 e 0,2 (se a razao seguir noise_level^2, o «alpha^2» era o ruido escolhido).
  * (B) REAL BRUTO, como o script faria com pycbc: strain do cache (32 s @ 4096 Hz) na janela [-2, +1] s do GPS, SEM branqueamento (o loader de
    fevereiro nao branqueava), contra template pycbc get_td_waveform (IMRPhenomD; massas de FONTE do catalogo, como no script) normalizado pelo desvio-padrao.
  * (C) REAL BRANQUEADO: strain branqueado (PSD Welch dos 14 s pre-evento; banda 20-1024 Hz) na mesma janela, contra o template branqueado com a
    mesma PSD (a versao justa do teste).
  * (D) FORA DA FONTE: janelas branqueadas em -10 s e -7 s (2 por serie), mesmo template: o que a razao mede em ruido puro.
  * Eventos: o catalogo de 12 do proprio script (os que existem no cache) E o catalogo completo (89) para estatistica; detectores L1 e H1.
  * Agregacao por modo: media, desvio-padrao, n, fracao h2_ok; z de |media_C - beta| / (sd/sqrt(n)); z de |media_C - media_D|.
beta = alpha*sqrt(e) em runtime. O VEREDITO e do um.py."""
import os, sys, csv, json, math, time, hashlib, argparse, warnings
import numpy as np
from scipy import signal
warnings.filterwarnings('ignore')
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); SQRT_BETA = math.sqrt(BETA)
G = 6.674e-11; C = 2.99792458e8; MSUN = 1.98892e30
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
IALD = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD'); SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
FEB = os.path.join(ROOT, 'IALD/projetos_pyhton/acom/Tgl_gw_echo_unification_v1.py'); JAN = os.path.join(ROOT, 'IALD/projetos_pyhton/acom/TGL_Echo_Analyzer_v8.py')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/gw')
FS = 4096.0; F_LO, F_HI = 20.0, 1024.0; WB, WA = 2.0, 1.0; OFF_T0 = (-10.0, -7.0); NOISE_LEVELS = (0.1, 0.05, 0.2)
SCRIPT_CATALOG = ['GW150914', 'GW151226', 'GW170104', 'GW170608', 'GW170729', 'GW170809', 'GW170814', 'GW170818', 'GW170823', 'GW170817', 'GW190521', 'GW190814']
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
# ---- COPIADO do script de fevereiro (Tgl_gw_echo_unification_v1.py, _echo_analysis), sem alteracao ----
def _echo_analysis(h_data, h_template):
    hd = (h_data - np.mean(h_data)) / (np.std(h_data) + 1e-30)
    ht = (h_template - np.mean(h_template)) / (np.std(h_template) + 1e-30)
    corr = signal.correlate(hd, ht, mode='full')
    lags = signal.correlation_lags(len(hd), len(ht), mode='full')
    norm = np.sqrt(np.sum(hd**2) * np.sum(ht**2))
    corr_norm = corr / norm if norm > 0 else corr
    max_idx = np.argmax(np.abs(corr_norm))
    max_corr = float(corr_norm[max_idx])
    best_lag = lags[max_idx]
    N = len(hd)
    ht_aligned = np.zeros(N)
    if best_lag >= 0:
        end = min(len(ht), N - best_lag)
        if end > 0:
            ht_aligned[best_lag:best_lag+end] = ht[:end]
    else:
        start = -best_lag
        end = min(len(ht) - start, N)
        if end > 0:
            ht_aligned[:end] = ht[start:start+end]
    denom = np.dot(ht_aligned, ht_aligned)
    if denom > 0:
        amplitude = np.dot(hd, ht_aligned) / denom
        ht_scaled = amplitude * ht_aligned
    else:
        ht_scaled = ht_aligned
    h_res = hd - ht_scaled
    E_total = np.sum(hd**2)
    E_res = np.sum(h_res**2)
    echo_ratio = E_res / E_total if E_total > 0 else 0
    return abs(max_corr), echo_ratio, E_res
# ---- gerador consistente do script de fevereiro (generate_consistent), reimplementado fielmente (f_isco = c^3/(6^{3/2} pi G M)) ----
def f_isco(M_total_solar): return C ** 3 / (6.0 ** 1.5 * math.pi * G * M_total_solar * MSUN)
def generate_consistent(m1, m2, duration=2.0, add_echo=False, noise_level=0.0, rng=None, sample_rate=FS):
    dt = 1.0 / sample_rate; N = int(duration * sample_rate); t = np.arange(N) * dt
    M_total = (m1 + m2) * MSUN; M_chirp = (m1 * m2) ** 0.6 / (m1 + m2) ** 0.2 * MSUN; M_chirp_s = M_chirp * G / C ** 3
    fi = min(f_isco(m1 + m2), 500.0); t_merger = duration * 0.7
    tau = np.maximum(t_merger - t, 1e-6)
    f_inst = (1 / (8 * np.pi * M_chirp_s)) * (5 * M_chirp_s / tau) ** (3 / 8); f_inst = np.clip(f_inst, 20, fi)
    amp = (f_inst / fi) ** (2 / 3); phase = 2 * np.pi * np.cumsum(f_inst) * dt; h = amp * np.cos(phase)
    mask_rd = t > t_merger
    if np.any(mask_rd):
        t_rd = t[mask_rd] - t_merger; tau_rd = 0.05; f_rd = 0.9 * fi; phase_rd = 2 * np.pi * f_rd * t_rd + phase[~mask_rd][-1]
        h[mask_rd] = amp[~mask_rd][-1] * np.exp(-t_rd / tau_rd) * np.cos(phase_rd)
    h = h * signal.windows.tukey(N, alpha=0.1); h = h / np.std(h)
    if add_echo:
        delay_samples = max(int(0.0 * sample_rate), 50); h_echo = np.zeros(N); h_echo[delay_samples:] = SQRT_BETA * h[:-delay_samples]; h = h + h_echo; h = h / np.std(h)
    if noise_level > 0:
        h = h + noise_level * (rng or np.random).standard_normal(N); h = h / np.std(h)
    return t - t_merger, h
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
def whiten(x, fs, f, P):
    N = len(x); fr = np.fft.rfftfreq(N, 1 / fs); Pi = np.maximum(np.interp(fr, f, P, left=P[1], right=P[-1]), 1e-50)
    return np.fft.irfft(np.fft.rfft(x) / np.sqrt(Pi * fs / 2) * band_mask(fr, F_LO, F_HI), n=N)
def pycbc_template(m1, m2, chi, dist, approx='IMRPhenomD'):
    from pycbc.waveform import get_td_waveform
    hp, hc = get_td_waveform(approximant=approx, mass1=m1, mass2=m2, spin1z=chi, spin2z=chi, delta_t=1.0 / FS, f_lower=20.0, distance=max(dist, 10.0))
    h = np.array(hp.data, dtype=float); t = np.array(hp.sample_times.data, dtype=float); pk = int(np.argmax(np.abs(h))); t = t - t[pk]; h = h / np.std(h); return t, h, approx
def stats(vals):
    v = np.array([x for x in vals if x is not None and np.isfinite(x)], dtype=float)
    if len(v) == 0: return dict(n=0)
    return dict(n=int(len(v)), mean=float(v.mean()), sd=(float(v.std(ddof=1)) if len(v) > 1 else None), median=float(np.median(v)), min=float(v.min()), max=float(v.max()))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--events', default=''); ap.add_argument('--out', default=os.path.join(OUT_DIR, 'H2_REPRODUCTION_V1_RESULT.json'))
    args = ap.parse_args(); only = set(x for x in args.events.split(',') if x); t_start = time.time(); rng = np.random.default_rng(20260218)
    import pycbc
    events = []
    with open(CAT, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            try:
                gps = float(r['GPS']); m1 = float(r['mass_1_source']); m2 = float(r['mass_2_source'])
            except Exception: continue
            if only and r['commonName'] not in only: continue
            chi = float(r['chi_eff']) if r.get('chi_eff') not in (None, '') else 0.0
            try: dist = float(r['luminosity_distance'])
            except Exception: dist = 500.0
            events.append(dict(name=r['commonName'], gps=gps, m1=m1, m2=m2, chi=min(max(chi, -0.99), 0.99), dist=dist, in_script_catalog=(r['commonName'] in SCRIPT_CATALOG)))
    rows = []; sources = {}; n_tpl_fail = 0
    for ev in events:
        try: tt, ht, approx = pycbc_template(ev['m1'], ev['m2'], ev['chi'], ev['dist'])
        except Exception as e:
            try: tt, ht, approx = pycbc_template(ev['m1'], ev['m2'], ev['chi'], ev['dist'], 'SEOBNRv4')
            except Exception as e2: n_tpl_fail += 1; rows.append(dict(event=ev['name'], status='NO_TEMPLATE', err=repr(e2)[:120])); continue
        # (A) sintetico fiel: dado = gerador com ruido; template = gerador sem ruido (mesmo evento)
        _, h_tpl_syn = generate_consistent(ev['m1'], ev['m2'], 2.0, False, 0.0)
        syn = {}
        for nl in NOISE_LEVELS:
            _, h_syn = generate_consistent(ev['m1'], ev['m2'], 2.0, False, nl, rng); c, er, _ = _echo_analysis(h_syn, h_tpl_syn); syn[str(nl)] = dict(corr=c, ratio=er, h2_ok=bool(abs(er - BETA) / BETA * 100 < 30 and c > 0.90))
        rec = dict(event=ev['name'], in_script_catalog=ev['in_script_catalog'], status='OK', template=approx, synthetic=syn, real={})
        for det in ('L1', 'H1'):
            p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
            if not os.path.exists(p): continue
            dd = np.load(p); t = dd['t']; s32 = dd['strain'].astype(float); fs = float(dd['fs'])
            if np.isnan(s32).any() or abs(fs - FS) > 1e-6: continue
            sources[os.path.basename(p)] = sha256_file(p); trel = t - ev['gps']; m = (trel >= -WB) & (trel <= WA)
            if m.sum() < 1000: continue
            raw = s32[m]; n = min(len(raw), len(ht)); c_raw, er_raw, _ = _echo_analysis(raw[:n], ht[:n])
            f_psd, P_psd = welch(s32[trel < -2.0], fs); w32 = whiten(s32, fs, f_psd, P_psd)
            # (C) template branqueado com a mesma PSD e ALINHADO PELO PICO no GPS (o modo B, fiel ao script, usa ht[:n], que e inspiral inicial):
            # segmento do template em torno do pico cobrindo [-WB, +WA] s, colocado numa serie de 32 s de zeros na posicao da janela, branqueado no mesmo grid
            i0 = int(np.argmax(m)); L = int(m.sum()); pk = int(np.argmax(np.abs(ht))); seg = np.zeros(L); a0 = pk - int(WB * FS); b0 = a0 + L
            src_a, src_b = max(a0, 0), min(b0, len(ht)); seg[src_a - a0:src_a - a0 + (src_b - src_a)] = ht[src_a:src_b]
            tpl32 = np.zeros_like(s32); tpl32[i0:i0 + L] = seg; wt = whiten(tpl32, fs, f_psd, P_psd)[i0:i0 + L]
            wd = w32[m][:L]; c_wh, er_wh, _ = _echo_analysis(wd, wt)
            offs = []
            for t0 in OFF_T0:
                mo = (trel >= t0 - WB) & (trel <= t0 + WA)
                if mo.sum() < L: continue
                c_o, er_o, _ = _echo_analysis(w32[mo][:L], wt); offs.append(dict(t0=t0, corr=c_o, ratio=er_o))
            rec['real'][det] = dict(raw=dict(corr=c_raw, ratio=er_raw, h2_ok=bool(abs(er_raw - BETA) / BETA * 100 < 30 and c_raw > 0.90)), whitened=dict(corr=c_wh, ratio=er_wh, h2_ok=bool(abs(er_wh - BETA) / BETA * 100 < 30 and c_wh > 0.90)), off=offs)
        rows.append(rec)
        print('  %-20s tpl=%s | syn ratio 0.1/0.05/0.2 = %.4f/%.4f/%.4f | real: %s' % (ev['name'], approx, syn['0.1']['ratio'], syn['0.05']['ratio'], syn['0.2']['ratio'], {d: 'raw %.3f (c %.2f) wh %.3f (c %.2f) off %s' % (v['raw']['ratio'], v['raw']['corr'], v['whitened']['ratio'], v['whitened']['corr'], [round(o['ratio'], 3) for o in v['off']]) for d, v in rec['real'].items()}), flush=True)
    ok = [r for r in rows if r.get('status') == 'OK']
    def collect(sel):
        S = {}
        for nl in NOISE_LEVELS: S['synthetic_%s' % nl] = stats([r['synthetic'][str(nl)]['ratio'] for r in sel]); S['synthetic_%s_h2ok_frac' % nl] = (float(np.mean([r['synthetic'][str(nl)]['h2_ok'] for r in sel])) if sel else None)
        raw = [v['raw']['ratio'] for r in sel for v in r['real'].values()]; wh = [v['whitened']['ratio'] for r in sel for v in r['real'].values()]; off = [o['ratio'] for r in sel for v in r['real'].values() for o in v['off']]
        cr = [v['raw']['corr'] for r in sel for v in r['real'].values()]; cw = [v['whitened']['corr'] for r in sel for v in r['real'].values()]
        S['real_raw'] = stats(raw); S['real_raw_corr'] = stats(cr); S['real_raw_h2ok_frac'] = (float(np.mean([v['raw']['h2_ok'] for r in sel for v in r['real'].values()])) if raw else None)
        S['real_whitened'] = stats(wh); S['real_whitened_corr'] = stats(cw); S['real_whitened_h2ok_frac'] = (float(np.mean([v['whitened']['h2_ok'] for r in sel for v in r['real'].values()])) if wh else None)
        S['off_source'] = stats(off)
        w_ = S['real_whitened']; o_ = S['off_source']
        S['z_whitened_vs_beta'] = ((w_['mean'] - BETA) / (w_['sd'] / math.sqrt(w_['n']))) if w_.get('n', 0) > 1 and w_.get('sd') else None
        S['z_whitened_vs_off'] = ((w_['mean'] - o_['mean']) / math.sqrt((w_['sd'] ** 2 / w_['n']) + (o_['sd'] ** 2 / o_['n']))) if (w_.get('n', 0) > 1 and o_.get('n', 0) > 1 and w_.get('sd') and o_.get('sd')) else None
        S['synthetic_tracks_noise_sq'] = all(abs(S['synthetic_%s' % nl]['mean'] - nl ** 2) / nl ** 2 < 0.3 for nl in NOISE_LEVELS if S['synthetic_%s' % nl].get('n')) if sel else None
        return S
    summary = dict(all=collect(ok), script_catalog=collect([r for r in ok if r['in_script_catalog']]), n_events_ok=len(ok), n_no_template=n_tpl_fail, beta=BETA)
    a = summary['all']
    print('RESUMO (todos): sintetico 0.1 = %.4f (h2_ok %.0f%%), 0.05 = %.4f, 0.2 = %.4f | segue noise^2: %s | real bruto %.4f (corr %.3f; h2_ok %.0f%%) | real branqueado %.4f +- %.4f (n=%d; corr %.3f; h2_ok %.0f%%) | fora da fonte %.4f | z vs beta %s | z vs fora %s' % (
        a['synthetic_0.1']['mean'], 100 * a['synthetic_0.1_h2ok_frac'], a['synthetic_0.05']['mean'], a['synthetic_0.2']['mean'], a['synthetic_tracks_noise_sq'], a['real_raw']['mean'], a['real_raw_corr']['mean'], 100 * a['real_raw_h2ok_frac'], a['real_whitened']['mean'], a['real_whitened']['sd'] or 0, a['real_whitened']['n'], a['real_whitened_corr']['mean'], 100 * a['real_whitened_h2ok_frac'], a['off_source']['mean'], ('%.1f' % a['z_whitened_vs_beta']) if a['z_whitened_vs_beta'] is not None else 'NA', ('%.1f' % a['z_whitened_vs_off']) if a['z_whitened_vs_off'] is not None else 'NA'), flush=True)
    out = dict(version='H2_REPRODUCTION_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t_start, beta=BETA, sqrt_beta=SQRT_BETA,
               instrument=dict(pycbc=pycbc.version.version, numpy=np.__version__, python=sys.version.split()[0], env='WSL Ubuntu /opt/pycbc_env'),
               scripts=dict(unification_feb2026=dict(path=FEB, sha256=sha256_file(FEB)), analyzer_v8_jan2026=dict(path=JAN, sha256=sha256_file(JAN))),
               pipeline=dict(fs=FS, window=[-WB, WA], band=[F_LO, F_HI], off_t0=list(OFF_T0), noise_levels=list(NOISE_LEVELS), h2_ok_rule='desvio < 30% e correlacao > 0,90 (linha 1110 do script)', synthetic='gerador consistente, add_echo=False, noise_level como no analyze', rng_seed=20260218),
               catalog=dict(path=CAT, sha256=sha256_file(CAT)), sources_sha256=sources, script_catalog=SCRIPT_CATALOG, summary=summary, per_event=rows)
    os.makedirs(OUT_DIR, exist_ok=True); tmp = args.out + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=lambda o: (float(o) if isinstance(o, (np.floating,)) else (bool(o) if isinstance(o, np.bool_) else (o.tolist() if hasattr(o, 'tolist') else str(o)))))
    os.replace(tmp, args.out); print('OK ->', args.out, '| %.0fs' % (time.time() - t_start), flush=True)
if __name__ == '__main__':
    main()
