# -*- coding: utf-8 -*-
# v340 — extrai janelas de strain GWOSC (publico) dos HDF5 locais de acom\gw_cache para um cache .npz que o um.py
# le com numpy puro (o interprete do um.py nao tem h5py). Roda com tgl_pycbc_env (h5py 3.15).
# Proveniencia: sha256 de cada HDF5 lido em bytes; GPS/massas [INPUT] parseados da tabela do script v1.4 (nunca de memoria).
import os, re, sys, json, hashlib, time
import numpy as np, h5py
ACOM = r'C:\IALD\projetos_pyhton\acom'
SRC_SCRIPT = os.path.join(ACOM, 'tgl_gw_echo_unification_v1_4.py')
CACHE_GW = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw'
OUT_NPZ = os.path.join(CACHE_GW, 'GWOSC_WINDOWS_V1.npz')
OUT_MAN = os.path.join(CACHE_GW, 'GWOSC_WINDOWS_V1.manifest.json')
T_BEFORE, T_AFTER = 8.0, 4.0     # segundos antes/depois do GPS do merger (folga para filtro; a analise usa [-2,+1])
os.makedirs(CACHE_GW, exist_ok=True)

def sha256_file(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(bs)
            if not b: break
            h.update(b)
    return h.hexdigest()

txt = open(SRC_SCRIPT, encoding='utf-8', errors='replace').read()
rows = re.findall(r'GWEvent\("(GW\d+)",\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([-\d.]+),\s*([-\d.]+),\s*([\d.]+),\s*"([^"]+)",\s*([\d.]+)\)', txt)
assert len(rows) == 12, len(rows)
events = [{'name': r[0], 'mass1': float(r[1]), 'mass2': float(r[2]), 'distance_Mpc': float(r[3]), 'spin1z': float(r[4]),
           'spin2z': float(r[5]), 'gps': float(r[6]), 'type': r[7], 'E_rad_Msun': float(r[8])} for r in rows]
arrays, series, t0 = {}, [], time.time()
for ev in events:
    for det in ('H1', 'L1'):
        p = os.path.join(ACOM, 'gw_cache', '%s_%s.hdf5' % (ev['name'], det))
        if not os.path.exists(p):
            series.append({'event': ev['name'], 'det': det, 'status': 'ABSENT_LOCALLY', 'path': p}); continue
        with h5py.File(p, 'r') as f:
            ds = f['strain/Strain']; xs = float(ds.attrs['Xstart']); dt = float(ds.attrs['Xspacing']); n = int(ds.shape[0])
            fs = 1.0 / dt
            i0 = int(round((ev['gps'] - T_BEFORE - xs) * fs)); i1 = int(round((ev['gps'] + T_AFTER - xs) * fs))
            if i0 < 0 or i1 > n:
                series.append({'event': ev['name'], 'det': det, 'status': 'WINDOW_OUTSIDE_FILE', 'path': p, 'Xstart': xs, 'n': n}); continue
            h = ds[i0:i1].astype(np.float64)
            dq = f['quality/simple/DQmask'][()] if 'quality/simple/DQmask' in f else None
            meta = {k: (f['meta'][k][()].decode() if isinstance(f['meta'][k][()], bytes) else int(f['meta'][k][()])) for k in f['meta']}
        nan = int(np.isnan(h).sum())
        key = '%s_%s' % (ev['name'], det)
        arrays[key] = h
        series.append({'event': ev['name'], 'det': det, 'status': 'OK', 'path': p, 'sha256_hdf5': sha256_file(p), 'bytes': os.path.getsize(p),
                       'Xstart': xs, 'fs': fs, 'i0': i0, 'i1': i1, 'n_window': int(i1 - i0), 't_rel_start_s': -T_BEFORE, 't_rel_end_s': T_AFTER,
                       'nan_count': nan, 'meta': meta, 'dq_bits': (int(dq.min()) if dq is not None else None)})
        print('  %-18s n=%d nan=%d sha16=%s (%.0fs)' % (key, i1 - i0, nan, series[-1]['sha256_hdf5'][:16], time.time() - t0), flush=True)
np.savez(OUT_NPZ + '.tmp.npz', **arrays)
os.replace(OUT_NPZ + '.tmp.npz', OUT_NPZ)
man = {'version': 'GWOSC_WINDOWS_V1', 'created': time.strftime('%Y-%m-%dT%H:%M:%S'), 'extractor': os.path.basename(__file__),
       'source_script_INPUT': {'path': SRC_SCRIPT, 'sha256': sha256_file(SRC_SCRIPT), 'what': 'tabela GWEvent (GPS, massas) de fev/2026'},
       'gwosc_source': 'GWOSC (gw-openscience.org) strain 4 kHz, arquivos locais de acom/gw_cache', 'window_s': [-T_BEFORE, T_AFTER],
       'events': events, 'series': series, 'npz': {'path': OUT_NPZ, 'keys': sorted(arrays.keys())}}
man['npz']['sha256'] = sha256_file(OUT_NPZ); man['npz']['bytes'] = os.path.getsize(OUT_NPZ)
json.dump(man, open(OUT_MAN + '.tmp', 'w', encoding='utf-8'), indent=1, ensure_ascii=False); os.replace(OUT_MAN + '.tmp', OUT_MAN)
ok = sum(1 for s in series if s['status'] == 'OK')
print('OK %d/%d series; npz %s bytes sha16 %s; manifesto %s' % (ok, len(series), format(man['npz']['bytes'], ','), man['npz']['sha256'][:16], OUT_MAN))
