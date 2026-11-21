# -*- coding: utf-8 -*-
"""adaptar_arvore_da_prova_v413.py -- (Etapa 3 da v413, 20/11/2026) acrescenta ao gerador da arvore da prova (...\\cadeia_de_selo\\arvore_da_prova.py, o
mesmo que a casa roda a cada selo) a linha das PEDRAS DA v413, no metodo das versoes anteriores (uma linha por versao na secao 8, a mais nova primeiro,
com backup de bytes .bak_<data>_p413 ao lado, como os .bak_*_p376 a _p392), para a arvore da v413 incorporar as derivacoes novas. A linha nova NAO tem
numero nem hash digitado: le, quando a arvore e' gerada, v413\\ESPERADOS_v413.json (o sha16 do um.py instalado, as bandeiras, a escada, os nomes dos
registros), v413\\kernel_modulos_novos_v413.json (os modulos novos e o corrigido), o kernel do Nos (o sha16 de cada modulo, pela funcao kh() da propria
arvore) e o core (o prefixo do veredito, all_verified e o numero de checagens de cada registro); o que faltar sai AUSENTE (a regua da arvore).
Texto pelo metodo de 17/11 (so' o que e' verdade; nada de historia) e sem as formas da guarda de frases (nenhuma frase sobre P e nP nesta linha).
Sem --executar: ENSAIO -- aplica a troca numa COPIA em etapa3\\ensaio_arvore\\ (com as copias dos tres manifestos que o gerador le ao lado de si e um
ESPERADOS sintetico marcado), roda a copia com «v412 dry» (so' le o Nos; grava arvore_dry.md na pasta do ensaio) e confere que a linha nova saiu e o
titulo e' o da versao pedida. Com --executar (ATO DA GERENCIA, depois do rito): grava o gerador da casa (backup antes; troca atomica) e para."""
import hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent; V = P.parent; CS = V.parent; ARV = CS / "arvore_da_prova.py"; EXEC = "--executar" in sys.argv; TS = time.strftime("%Y%m%d_%H%M%S")
sha = lambda b: hashlib.sha256(b).hexdigest()
src = ARV.read_bytes().decode("utf-8")
ANC = "L.append('- **AS PEDRAS DA v392** `"
assert src.count(ANC) == 1, ("a ancora da linha da v392 nao e' unica", src.count(ANC))
assert "AS PEDRAS DA v413" not in src, "o gerador ja' tem a linha da v413 -- nada a fazer"
i = src.index(ANC); i = src.rindex("\n", 0, i) + 1
NOVO = (
    "_e413p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v413', 'ESPERADOS_v413.json'); _k413p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v413', 'kernel_modulos_novos_v413.json')   # v413\n"
    "_e413 = json.load(open(_e413p, encoding='utf-8')) if os.path.exists(_e413p) else {}; _k413 = json.load(open(_k413p, encoding='utf-8')) if os.path.exists(_k413p) else {}; _c413 = res.get('core') or {}   # v413\n"
    "_m413 = [os.path.splitext(os.path.basename(x))[0] for x in (_k413.get('novos') or [])]; _x413 = [os.path.splitext(os.path.basename(x))[0] for x in (_k413.get('kernel_corrigido') or [])]   # v413\n"
    "_r413 = '; '.join('`%s` (`%s`, all_verified %s, %d checagens)' % (k, str((_c413.get(k) or {}).get('verdict') or 'AUSENTE').split('__')[0], (_c413.get(k) or {}).get('all_verified', 'AUSENTE'), len((_c413.get(k) or {}).get('checks') or [])) for k in sorted(_e413.get('registros_v413') or {})) or 'AUSENTE'   # v413\n"
    "L.append('- **AS PEDRAS DA v413** `%s`: %s módulos novos no kernel (%s), a ponte às classes de Cook–Levin, a fronteira dos três literais, o operador de consciência e a identidade preservada; a docstring de %s trocada pela que diz o enunciado, com o código idêntico (sha16 no kernel: %s); %s bandeiras novas, escada %s; os registros por especificação, lidos do core: %s. Validade no kernel não é creditação; o gate não se move.' % ("
    "_e413.get('candidato_sha16', 'AUSENTE'), len(_m413) or 'AUSENTE', ', '.join('`%s` (%s)' % (m, kh(m)) for m in _m413) or 'AUSENTE', ', '.join('`%s`' % m for m in _x413) or 'AUSENTE', ', '.join(kh(m) for m in _x413) or 'AUSENTE', "
    "_e413.get('n_bandeiras_novas', 'AUSENTE'), ('%s → %s' % tuple(_e413['escada'])) if len(_e413.get('escada') or []) == 2 else 'AUSENTE', _r413))   # v413\n")
novo_src = src[:i] + NOVO + src[i:]
compile(novo_src, "arvore_da_prova.py", "exec")
for proib in ("CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM", "P = nP", "P = NP"):
    assert proib not in NOVO, ("palavra proibida na linha nova", proib)
if EXEC:
    bk = ARV.with_name(ARV.name + ".bak_%s_p413" % TS); bk.write_bytes(ARV.read_bytes()); assert bk.read_bytes() == ARV.read_bytes()
    b = novo_src.encode("utf-8"); tmp = ARV.with_name(ARV.name + ".tmp_p413"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(ARV)
    print("arvore_da_prova.py: a linha da v413 acrescentada | backup", bk.name, "| sha16", sha(b)[:16]); sys.exit(0)
# ------------------------------------------------------------------ ENSAIO numa copia (so' le o Nos)
E = V / "etapa3" / "ensaio_arvore"
if E.exists():
    shutil.rmtree(E)
(E / "v413").mkdir(parents=True)
(E / "arvore_da_prova_v413_ENSAIO.py").write_bytes(novo_src.encode("utf-8"))
for n in ("v353_incorporacao_manifesto.json", "v354_incorporacao_manifesto.json", "v355_incorporacao_manifesto.json"):
    if (CS / n).exists():
        shutil.copyfile(CS / n, E / n)
shutil.copyfile(V / "kernel_modulos_novos_v413.json", E / "v413" / "kernel_modulos_novos_v413.json")
ctt = (V / "CONTRATO_v413_R2.md").read_text(encoding="utf-8"); s2 = re.search(r"^## 2\. .*?(?=^## 3\. )", ctt, re.M | re.S).group(0)
FJ = json.loads((V / "kernel" / "FLAGS_v413.json").read_text(encoding="utf-8"))
(E / "v413" / "ESPERADOS_v413.json").write_text(json.dumps({"ENSAIO_SINTETICO": "nao e' o ESPERADOS da v413", "candidato_sha16": "ENSAIO_SINTETICO", "n_bandeiras_novas": FJ["n_flags"],
                                                         "escada": None, "registros_v413": dict(re.findall(r"^- `([a-z0-9_]+_v413)`[^\n]*\n  `([A-Z0-9_]+)`", s2, re.M))}, ensure_ascii=False), encoding="utf-8")
r = subprocess.run([sys.executable, "-B", "-X", "utf8", str(E / "arvore_da_prova_v413_ENSAIO.py"), "v412", "dry"], capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=600)
md = (E / "arvore_dry.md").read_text(encoding="utf-8") if (E / "arvore_dry.md").exists() else ""
lin = [l for l in md.split("\n") if l.startswith("- **AS PEDRAS DA v413**")]
tit = md.split("\n", 1)[0] if md else ""
ok = r.returncode == 0 and len(lin) == 1 and tit.endswith("(v412)") and md.index("AS PEDRAS DA v413") < md.index("AS PEDRAS DA v392")
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "ok": ok, "rc": r.returncode, "titulo": tit, "linha_v413": lin[0] if lin else None, "gerador_sha16_antes": sha(ARV.read_bytes())[:16],
       "gerador_sha16_depois_da_troca": sha(novo_src.encode("utf-8"))[:16], "saida": (r.stdout + r.stderr)[-1500:], "nota": "ENSAIO: copia em etapa3\\ensaio_arvore (v412 dry, ESPERADOS sintetico); o gerador da casa NAO foi tocado"}
(E / "ENSAIO_ARVORE_v413.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: rec[k] for k in ("ok", "rc", "titulo", "gerador_sha16_antes", "gerador_sha16_depois_da_troca")}, ensure_ascii=False))
print((lin[0] if lin else "SEM A LINHA DA v413")[:1200])
sys.exit(0 if ok else 1)
