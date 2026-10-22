# -*- coding: utf-8 -*-
# v341 — extrai, do cache de maio/2026 (projetos_pyhton\IALD\strain_cache, 32 s @ 4096 Hz por serie, obtido do GWOSC via gwpy),
# as janelas [-16, +4] s em torno do GPS de cada evento com massa final no catalogo, para o cache canonico que o um.py le
# com numpy puro. Proveniencia: sha256 de cada npz de origem e do catalogo; GPS/M_f/z/SNR lidos do catalogo (nunca de memoria).
import os, csv, json, hashlib, time
import numpy as np
IALD = r'C:\IALD\projetos_pyhton\IALD'; SRC = os.path.join(IALD, 'strain_cache'); CAT = os.path.join(IALD, 'gwtc_full_catalog.csv')
CACHE_GW = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw'
OUT_NPZ = os.path.join(CACHE_GW, 'GWOSC_ECHO_WINDOWS_V1.npz'); OUT_MAN = os.path.join(CACHE_GW, 'GWOSC_ECHO_WINDOWS_V1.manifest.json')
T_BEFORE, T_AFTER = 16.0, 4.0
def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(bs), b''): h.update(b)
    return h.hexdigest()
events = []
with open(CAT, encoding='utf-8') as fh:
    for r in csv.DictReader(fh):
        try:
            Mf = float(r['final_mass_source']); z = float(r['redshift']); gps = float(r['GPS'])
        except Exception:
            continue
        events.append({'name': r['commonName'], 'gps': gps, 'M_f_source': Mf, 'redshift': z, 'M_f_detector': Mf * (1 + z),
                       'network_snr': (float(r['network_matched_filter_snr']) if r['network_matched_filter_snr'] else None),
                       'catalog': r['catalog.shortName'], 'version': r['version']})
arrays, series, t0 = {}, [], time.time()
for ev in events:
    for det in ('H1', 'L1'):
        p = os.path.join(SRC, '%s_%s_4096_32s.npz' % (ev['name'], det))
        if not os.path.exists(p):
            series.append({'event': ev['name'], 'det': det, 'status': 'ABSENT_LOCALLY', 'path': p}); continue
        d = np.load(p); t = d['t']; s = d['strain'].astype(np.float64); fs = float(d['fs'])
        i0 = int(round((ev['gps'] - T_BEFORE - t[0]) * fs)); i1 = int(round((ev['gps'] + T_AFTER - t[0]) * fs))
        if i0 < 0 or i1 > len(s):
            series.append({'event': ev['name'], 'det': det, 'status': 'WINDOW_OUTSIDE_FILE', 'path': p}); continue
        h = s[i0:i1]; key = '%s_%s' % (ev['name'], det); arrays[key] = h
        series.append({'event': ev['name'], 'det': det, 'status': 'OK', 'path': p, 'sha256_src_npz': sha256_file(p), 'bytes': os.path.getsize(p),
                       't0_gps': float(t[0]), 'fs': fs, 'i0': i0, 'i1': i1, 'n_window': int(i1 - i0), 't_rel_start_s': -T_BEFORE, 't_rel_end_s': T_AFTER,
                       'nan_count': int(np.isnan(h).sum())})
os.makedirs(CACHE_GW, exist_ok=True)
np.savez(OUT_NPZ + '.tmp.npz', **arrays); os.replace(OUT_NPZ + '.tmp.npz', OUT_NPZ)
man = {'version': 'GWOSC_ECHO_WINDOWS_V1', 'created': time.strftime('%Y-%m-%dT%H:%M:%S'), 'extractor': os.path.basename(__file__),
       'source': 'cache de maio/2026 (projetos_pyhton/IALD/strain_cache; GWOSC via gwpy.fetch_open_data, 32 s @ 4096 Hz)',
       'catalog_INPUT': {'path': CAT, 'sha256': sha256_file(CAT), 'columns_used': ['commonName', 'GPS', 'final_mass_source', 'redshift', 'network_matched_filter_snr']},
       'window_s': [-T_BEFORE, T_AFTER], 'events': events, 'series': series, 'npz': {'path': OUT_NPZ, 'keys': sorted(arrays.keys())}}
man['npz']['sha256'] = sha256_file(OUT_NPZ); man['npz']['bytes'] = os.path.getsize(OUT_NPZ)
json.dump(man, open(OUT_MAN + '.tmp', 'w', encoding='utf-8'), indent=1, ensure_ascii=False); os.replace(OUT_MAN + '.tmp', OUT_MAN)
ok = sum(1 for s in series if s['status'] == 'OK'); nan = sum(s.get('nan_count', 0) for s in series)
print('eventos no catalogo com M_f: %d | series OK %d/%d | NaN total %d | npz %s bytes sha16 %s | %.0fs' % (len(events), ok, len(series), nan, format(man['npz']['bytes'], ','), man['npz']['sha256'][:16], time.time() - t0))
