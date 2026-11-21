from pathlib import Path
import os, sys, subprocess, hashlib, time

root = Path(__file__).resolve().parent
lake = Path('C:/t/k411c/final/.lake')
workshop = root.parents[2] / 'v412'
compiler = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
allowed = ['RelogioBeta', 'PonteLeituraBeta', 'EntregaBeta']
names = sys.argv[1:] or allowed[:1]
assert all(n in allowed for n in names)
libs = [root, root.parent / 'simulacao', root.parent, lake / 'build/lib/lean',
        *(p / '.lake/build/lib/lean' for p in sorted((lake / 'packages').iterdir())),
        workshop / 'candidatas_c1/build', workshop / 'candidatas_c1/build_sobre_limpas',
        workshop / 'candidatas_kimi/build']
env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libs if p.is_dir()))
for n in names:
    source = root / (n + '.lean')
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    start = time.monotonic()
    run = subprocess.run([str(compiler), '-j', '2', '-o', n+'.olean', n+'.lean'],
                         cwd=root, env=env, capture_output=True)
    out = (run.stdout + run.stderr).decode('utf8')
    log = f'{n} | SHA256 {sha} | RC {run.returncode} | seconds {time.monotonic()-start:.3f}\n{out}'
    dest = root / (n + '.log')
    if dest.exists():
        backup = root / (n + '.log.bak_' + str(time.time_ns()))
        backup.write_bytes(dest.read_bytes())
    tmp = root / (n + '.log.tmp')
    tmp.write_bytes(log.encode('utf8'))
    assert tmp.read_bytes() == log.encode('utf8')
    tmp.replace(dest)
    print(log, flush=True)
    if run.returncode or 'sorryAx' in out:
        sys.exit(1)
