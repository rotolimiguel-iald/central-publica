# -*- coding: utf-8 -*-
# Verifica a proveniencia de cada wheel/sdist baixado de um espelho: sha256 local == digest oficial publicado pela PyPI (JSON API).
# Uso: python verify_wheels_pypi.py <dir>. Sai com 1 se qualquer arquivo nao bater (fail-closed).
import os, sys, json, hashlib, re, urllib.request
d = sys.argv[1]
ok_all = True; rows = []
for fn in sorted(os.listdir(d)):
    if not (fn.endswith('.whl') or fn.endswith('.tar.gz')):
        continue
    m = re.match(r'([A-Za-z0-9_.\-]+?)-(\d[^-]*?)(?:-py|-cp|-pp|\.tar\.gz)', fn)
    if not m:
        print('?? nome nao parseavel:', fn); ok_all = False; continue
    name, ver = m.group(1), m.group(2)
    h = hashlib.sha256(open(os.path.join(d, fn), 'rb').read()).hexdigest()
    try:
        j = json.load(urllib.request.urlopen('https://pypi.org/pypi/%s/%s/json' % (name.replace('_', '-'), ver), timeout=40))
        digests = {u['filename']: u['digests']['sha256'] for u in j['urls']}
    except Exception as e:
        print('?? PyPI JSON falhou para %s %s: %s' % (name, ver, e)); ok_all = False; continue
    off = digests.get(fn)
    ok = (off == h)
    ok_all &= ok
    rows.append((fn, ok)); print('%s %s  %s' % ('OK  ' if ok else 'FAIL', fn, h[:16] if ok else 'local %s != pypi %s' % (h[:16], str(off)[:16])))
print('%d arquivos; todos conferem com a PyPI: %s' % (len(rows), ok_all))
sys.exit(0 if ok_all else 1)
