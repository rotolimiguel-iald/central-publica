# -*- coding: utf-8 -*-
"""Diagnostico do worker de maio vs o worker corrigido, no fiducial de Planck (beta = 0 e beta = alpha sqrt(e)): R, l_A, DM_*, razao contra o CAMB,
e o chi^2 de cada bloco de dados com as formulas do proprio tgl_mcmc_camb_v2.py. Grava JSON lido por hash pela emenda (v349)."""
import os, sys, json, math, time, hashlib, subprocess, tempfile
import numpy as np
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
MAY = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD/tgl_camb_worker.py'); FIX = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/eco_ancorado_v1/tgl_camb_worker_v2fix.py')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/d1_camb')
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e); C = 299792.458
PL = np.array([1.7502, 301.471, 0.02236]); COV = np.array([[2.1167e-05, 3.4659e-05, -4.5466e-08], [3.4659e-05, 8.0901e-03, -1.6087e-06], [-4.5466e-08, -1.6087e-06, 2.2497e-08]]); CI = np.linalg.inv(COV)
DESI = np.array([[0.295, 2, 7.93, 0.15], [0.510, 0, 13.62, 0.25], [0.510, 1, 20.98, 0.61], [0.706, 0, 16.85, 0.32], [0.706, 1, 20.08, 0.60], [0.930, 0, 21.71, 0.28], [0.930, 1, 17.88, 0.35], [1.317, 0, 27.79, 0.69], [1.317, 1, 13.82, 0.42], [1.491, 2, 26.07, 0.67], [2.330, 0, 39.71, 0.94], [2.330, 1, 8.52, 0.17]])
def call(worker, beta, H0=67.4, ombh2=0.02237, omch2=0.12):
    with tempfile.TemporaryDirectory() as tmp:
        ip = os.path.join(tmp, 'p.json'); op = os.path.join(tmp, 'r.npz')
        json.dump(dict(beta=beta, H0=H0, ombh2=ombh2, omch2=omch2, tau=0.0544, ns=0.9649, As=2.1e-9, mnu=0.06, TCMB=2.7255, Neff=3.046, lmax=20, desi_z=sorted(set(DESI[:, 0].tolist()))), open(ip, 'w'))
        t0 = time.time(); pr = subprocess.run([sys.executable, worker, ip, op], capture_output=True, text=True, timeout=300); dt = time.time() - t0
        if pr.returncode != 0: return dict(error=pr.stderr[-500:])
        d = np.load(op); r = {k: (d[k].item() if d[k].shape == () else d[k].tolist()) for k in d.files}
        rd = float(r['r_drag_TGL']); Z = np.asarray(r['desi_z']); DM = np.asarray(r['DM_at_DESI']); H = np.asarray(r['H_at_DESI']); chi = 0.0
        for z, kind, obs, sig in DESI:
            i = int(np.argmin(np.abs(Z - z))); dm = DM[i]; dh = C / H[i]; pred = {0: dm / rd, 1: dh / rd, 2: (z * dm ** 2 * dh) ** (1 / 3) / rd}[int(kind)]; chi += ((pred - obs) / sig) ** 2
        v = np.array([float(r['R']), float(r['lA']), ombh2]) - PL; chi_pl = float(v @ CI @ v)
        return dict(R=float(r['R']), lA=float(r['lA']), DM_star_TGL=float(r['DM_star_TGL']), DM_star_LCDM=float(r['DM_star_LCDM']), ratio_TGL_over_CAMB=float(r['DM_star_TGL']) / float(r['DM_star_LCDM']),
                    r_drag_TGL=rd, chi2_planck=chi_pl, chi2_desi=float(chi), chi2_total_no_sh0es=chi_pl + float(chi), selfcheck=(float(r['dm_selfcheck_ratio']) if 'dm_selfcheck_ratio' in r else None), call_s=dt)
out = dict(version='D1_CAMB_DIAGNOSTICO', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), fiducial=dict(H0=67.4, ombh2=0.02237, omch2=0.12), planck=dict(R=1.7502, lA=301.471),
           may_worker=dict(path=MAY, sha256=hashlib.sha256(open(MAY, 'rb').read()).hexdigest(), beta0=call(MAY, 0.0), beta_tgl=call(MAY, BETA)),
           fixed_worker=dict(path=FIX, sha256=hashlib.sha256(open(FIX, 'rb').read()).hexdigest(), beta0=call(FIX, 0.0), beta_tgl=call(FIX, BETA)),
           bug='D_M_TGL: trapezio em 300 pontos numa grade linear em z ate z_* ~ 1090 (passo ~3,6) sobre-estima a distancia; corrigido por integracao densa em ln(1+z)')
for k in ('may_worker', 'fixed_worker'):
    b0 = out[k]['beta0']; print('%-13s beta=0: R %.4f lA %.3f DM_TGL/CAMB %.4f chi2 Planck %.1f DESI %.1f | selfcheck %s' % (k, b0.get('R', float('nan')), b0.get('lA', float('nan')), b0.get('ratio_TGL_over_CAMB', float('nan')), b0.get('chi2_planck', float('nan')), b0.get('chi2_desi', float('nan')), b0.get('selfcheck')))
    bt = out[k]['beta_tgl']; print('%-13s beta=a*sqrt(e): R %.4f lA %.3f chi2 Planck %.1f DESI %.1f' % (k, bt.get('R', float('nan')), bt.get('lA', float('nan')), bt.get('chi2_planck', float('nan')), bt.get('chi2_desi', float('nan'))))
os.makedirs(OUT_DIR, exist_ok=True); p = os.path.join(OUT_DIR, 'D1_CAMB_DIAGNOSTICO.json'); tmp = p + '.tmp'
json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1); os.replace(tmp, p); print('OK ->', p)
