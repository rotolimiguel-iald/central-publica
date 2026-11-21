from pathlib import Path
import os, subprocess, hashlib, time, sys

root = Path(__file__).resolve().parent
lake = Path('C:/t/k411c/final/.lake')
v412 = root.parents[2] / 'v412'
libraries = [root, root.parent, lake / 'build/lib/lean',
             *(p / '.lake/build/lib/lean' for p in sorted((lake / 'packages').iterdir())),
             v412 / 'candidatas_c1/build', v412 / 'candidatas_c1/build_sobre_limpas',
             v412 / 'candidatas_kimi/build']
env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libraries if p.is_dir()))
lean = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
source = root / 'Reconstrucao.lean'
digest = hashlib.sha256(source.read_bytes()).hexdigest()
start = time.monotonic()
result = subprocess.run([str(lean), '-j', '2', '-o', 'Reconstrucao.olean', source.name],
                        cwd=root, env=env, capture_output=True, timeout=180)
output = (result.stdout + result.stderr).decode('utf8')
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
log = f'SHA256 {digest}\nRC {result.returncode}\n{output}'
temp = root / 'Reconstrucao.log.tmp'
temp.write_bytes(log.encode('utf8'))
assert temp.read_bytes() == log.encode('utf8')
temp.replace(root / 'Reconstrucao.log')
print(f'RC {result.returncode}, {time.monotonic()-start:.2f}s\n{output}')
sys.exit(result.returncode)
