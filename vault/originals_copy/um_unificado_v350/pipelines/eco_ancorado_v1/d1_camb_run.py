# -*- coding: utf-8 -*-
"""D1_CAMB_V1 — driver: roda o `tgl_mcmc_camb_v2.py` de maio de 2026 (o «D1 via CAMB» do canonico `tgl_paper_unified.py --d1-camb`, que nunca
correu por falta do camb) SEM alterar o script do operador, e sela o relatorio num unico JSON com os sha256 dos scripts, versoes e tempos.
Fases: bestfits (Fase 1: LCDM vs TGL beta fixo, Planck comprimido + DESI + SH0ES; Fase 2: Planck + DESI sem SH0ES, anatomia de H0) e
mcmc (Fase 3: beta livre, emcee 24 walkers x 2000 passos, burn 400). O VEREDITO e do um.py."""
import os, sys, json, time, hashlib, subprocess, glob, shutil
ROOT = os.environ.get('ECHO_ROOT', '/mnt/c')
SCRIPT = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD/tgl_mcmc_camb_v2.py'); WORKER = os.path.join(ROOT, 'IALD/projetos_pyhton/IALD/tgl_camb_worker.py')
OUT_DIR = os.path.join(ROOT, 'IALD/Artigo/Haja_Luz/A Ponte e o Um/cache/d1_camb'); RUN_DIR = os.path.join(OUT_DIR, 'run')
def sha(p):
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); return h
def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else 'all'; cores = sys.argv[2] if len(sys.argv) > 2 else '40'
    os.makedirs(RUN_DIR, exist_ok=True); t0 = time.time()
    cmd = [sys.executable, SCRIPT, '--worker', WORKER, '--phase', phase, '--out-dir', RUN_DIR, '--cores', cores]
    print('CMD:', ' '.join(cmd), flush=True)
    log_p = os.path.join(OUT_DIR, 'tgl_mcmc_camb_v2_%s.log' % phase)
    with open(log_p, 'w', encoding='utf-8') as lg:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=os.path.dirname(SCRIPT))
        for line in proc.stdout:
            lg.write(line); lg.flush(); print(line.rstrip(), flush=True)
        rc = proc.wait()
    reports = sorted(glob.glob(os.path.join(RUN_DIR, 'report_*.json')), key=os.path.getmtime)
    rep = json.load(open(reports[-1], encoding='utf-8')) if reports else None
    import camb, emcee, scipy, numpy
    out = dict(version='D1_CAMB_V1', executed=time.strftime('%Y-%m-%dT%H:%M:%S'), runtime_s=time.time() - t0, returncode=rc, phase=phase, cores=int(cores),
               scripts=dict(tgl_mcmc_camb_v2=dict(path=SCRIPT, sha256=sha(SCRIPT), mtime=time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(SCRIPT)))),
                            tgl_camb_worker=dict(path=WORKER, sha256=sha(WORKER), mtime=time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(WORKER))))),
               instrument=dict(camb=camb.__version__, emcee=emcee.__version__, scipy=scipy.__version__, numpy=numpy.__version__, python=sys.version.split()[0], env='WSL Ubuntu /opt/lal_env'),
               report_path=(reports[-1] if reports else None), report=rep, log=log_p)
    p = os.path.join(OUT_DIR, 'D1_CAMB_RESULT.json'); tmp = p + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, default=str); os.replace(tmp, p)
    print('OK ->', p, '| rc', rc, '| %.0fs' % (time.time() - t0), flush=True)
if __name__ == '__main__':
    main()
