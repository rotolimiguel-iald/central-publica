# -*- coding: utf-8 -*-
"""adaptar_instalar_e_reverter_v412.py -- (gerencia c1, 18/11/2026, Etapa 3 ENXUTA: PLANO_ETAPA3_ENXUTA_v412.md) adapta DE VERDADE o
instalar_v412.py e o reverter_v412.py herdados da v411 (versao sem modulo novo) para a v412, que tem 156 modulos novos, pelo molde da v410
(versao com modulo novo). Trocas por LINHA (o comeco de cada linha e' conferido antes) e por texto exato com contagem. O que muda:
* instalar: a marca sai (linha [ADAPTADO v412]); a docstring diz o que a versao confere; o topo e' o DERIVADO (TOPO_RATIFICADO_v412_DERIVADO.json,
  o topo ratificado da v411 com os numeros lidos); a trava do recibo pre_selo do B(n) e a do pino da Bancada SAEM, como DESVIO DECLARADO (a
  Bancada nao responde; o B(n) da v412 nao rodou; decisao aberta no handoff); as pedras anteriores vem de ESPERADOS.bundle_pedras_anteriores_sha256;
  a raiz e o Audit do Nos tem de ser os da v411 (ESPERADOS.kernel.raiz_antes_sha16, audit_antes_sha16); os 156 modulos novos (ESPERADOS.bundle_sha256
  == kernel_modulos_novos_v412.json[novos]) NAO podem estar no kernel do Nos; o registro guarda a lista dos 156 (o reverter a usa).
* reverter: a trava da lista vazia passa a exigir a lista dos 156 (a mesma do instalar, do ESPERADOS e do CANDIDATO); os textos de lista vazia.
Backup de bytes de cada arquivo antes; compila o resultado. Uso: adaptar_instalar_e_reverter_v412.py [--executar]"""
import difflib, hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; EXEC = "--executar" in sys.argv; TS = time.strftime("%Y%m%d_%H%M%S")
MARCA_NOVA = ("# [ADAPTADO v412, 18/11/2026, gerencia c1 (Etapa 3 enxuta; PLANO_ETAPA3_ENXUTA_v412.md; adaptar_instalar_e_reverter_v412.py)] o corpo e' o da v411 "
              "com o que depende de bundle NAO vazio pelo molde da v410: a v412 tem 156 modulos novos; o B(n) pre-selo sai como desvio declarado")

# ---------------- instalar ----------------
p = V / "instalar_v412.py"; t0 = p.read_bytes().decode("utf-8"); L = t0.split("\n")
def linha(n, comeco):
    assert L[n - 1].startswith(comeco), ("linha %d nao comeca com" % n, comeco[:60], L[n - 1][:80]); return n - 1
i2 = linha(2, "# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO")
i4 = linha(4, '"""instalar_v412.py -- instala o candidato v412 no canonico')
i4f = next(k for k in range(i4 + 1, len(L)) if L[k].rstrip().endswith('"""'))
i20 = linha(20, 'assert os.path.exists(os.path.join(HERE, "TOPO_RATIFICADO_v412.json"))')
i36 = linha(36, '_pino_p = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v412.json")')
i43 = linha(43, '_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache"')
i52 = linha(52, 'assert sorted("TGLExt/" + n_ + ".lean" for n_ in ("IALD2", "AEscala")) == sorted(ESP["bundle_v411_sha256"])')
i54 = linha(54, 'assert all(hashlib.sha256(open(os.path.join(NOS, "tgl_kernel", *rel.split("/")), "rb").read()).hexdigest() == s_ for rel, s_ in ESP["bund')
i55 = linha(55, '_kn = ESP["kernel"]')
i56 = linha(56, 'assert h16(open(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"), "rb").read()) == _kn["raiz_sha16"]')
i57 = linha(57, 'NOVOS_V412 = sorted(ESP["bundle_sha256"]); _N = len(NOVOS_V412)')
i58 = linha(58, 'assert _N == 0 == ESP["kernel"]["modulos_novos"] == CM["kernel"]["modulos_novos"] == ESP["n_bandeiras_novas"]')
i60 = linha(60, 'rec["modulos_novos_v412"] = {"fonte": "ESPERADOS_v412.bundle_sha256 (vazio: a v412 nao tem modulo novo)"')
i61 = linha(61, 'rec["pino_recibo_pre_selo"] = {"path": _pino_p')
DOC = ['"""instalar_v412.py -- instala o candidato v412 no canonico (ato da gerencia c1). Molde: instalar_v411.py (o corpo) e instalar_v410.py (a versao COM modulo novo).',
       'Fail-closed (para na primeira falha, antes de qualquer escrita no Nos):',
       '  * recusa o MODO DE ENSAIO do topo proposto; exige o topo DERIVADO (TOPO_RATIFICADO_v412_DERIVADO.json: o topo ratificado da v411 com os numeros lidos);',
       '  * ESPERADOS_v412.json (esperados_v412_foco.py) e CANDIDATO_v412.json concordam; nenhum processo um.py nem trabalhador do pilar rodando;',
       '  * o um.py do Nos e\' a v411 selada (ESPERADOS.origem_sha16); o candidato tem o sha16 e os bytes do ESPERADOS; o cache do pilar guarda o resultado reaproveitado;',
       '  * as pedras das versoes anteriores estao no kernel do Nos (as duas ultimas com o sha256 selado);',
       '  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos sao os da v411 selada (o rito os reescreve: o um.py materializa a raiz com os 156 imports);',
       '  * os 156 modulos novos (ESPERADOS.bundle_sha256 == kernel_modulos_novos_v412.json[novos] == CANDIDATO.kernel.modulos_novos) NAO estao no kernel do Nos;',
       '  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, o sidecar um_absoluto_selo_acom.json,',
       '    tgl_kernel_proof_manifest.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean; a copia do cache do pilar; so\' entao troca o um.py.',
       'DESVIO DECLARADO (v412): o recibo pre_selo do B(n) e o pino da Bancada NAO sao exigidos (a Bancada nao responde; o B(n) da v412 nao rodou;',
       'decisao aberta no handoff). Grava APLICADO_AO_CANONICO_<ts>.json (o reverter usa a lista dos 156)."""']
NOVOS = ['_KN = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v412.json"), encoding="utf-8"))   # (v412, molde v410) a lista dos modulos novos que o construtor gravou',
         'assert isinstance(_KN["novos"], list), "kernel_modulos_novos_v412.json tem de trazer a LISTA em \'novos\'"',
         'assert _N == 156 == len(set(NOVOS_V412)) == ESP["kernel"]["modulos_novos"] == CM["kernel"]["modulos_novos"] and set(NOVOS_V412) == set(_KN["novos"]) and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in NOVOS_V412), ("a lista dos modulos novos da v412 nao bate", _N)',
         'assert not [rel for rel in NOVOS_V412 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v412) ja esta no kernel do Nos -- nao instalo"']
N = list(L)
N[i61] = 'rec["pino_recibo_pre_selo"] = {"desvio_declarado": "o recibo pre_selo do B(n) e o pino da Bancada nao foram exigidos na v412 (a Bancada nao responde; o B(n) da v412 nao rodou); decisao aberta no handoff"}'
N[i60] = 'rec["modulos_novos_v412"] = {"fonte": "ESPERADOS_v412.bundle_sha256 (156; == kernel_modulos_novos_v412.json[novos] == CANDIDATO.kernel.modulos_novos)", "n": _N, "lista": NOVOS_V412}   # o reverter usa ESTA lista (a que o instalar conferiu)'
N[i58:i58 + 1] = NOVOS
N[i56] = (L[i56].replace('_kn["raiz_sha16"]', '_kn["raiz_antes_sha16"]').replace('_kn["audit_sha16"]', '_kn["audit_antes_sha16"]'))
assert N[i56] != L[i56] and 'raiz_antes_sha16' in N[i56] and 'audit_antes_sha16' in N[i56]
N[i55] = '_kn = ESP["kernel"]   # (v412) a raiz e o Audit do Nos tem de ser os da v411 selada; o rito os reescreve (a raiz ganha os 156 imports; lidos do ESPERADOS_v412.json, nunca digitados)'
N[i54] = L[i54].replace('ESP["bundle_v411_sha256"]', 'ESP["bundle_pedras_anteriores_sha256"]'); assert N[i54] != L[i54]
N[i52] = L[i52].replace('ESP["bundle_v411_sha256"]', 'ESP["bundle_pedras_anteriores_sha256"]'); assert N[i52] != L[i52]
N[i36:i43] = ['# (v412) DESVIO DECLARADO: o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v412.json) e o pino da Bancada de producao NAO sao exigidos nesta versao:',
              '# a Bancada (127.0.0.1:18777) nao responde e o B(n) da v412 nao rodou; o handoff leva isto as decisoes abertas. As outras travas seguem.']
N[i20] = 'assert os.path.exists(os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")), "falta TOPO_RATIFICADO_v412_DERIVADO.json (o topo ratificado da v411 com os numeros lidos): sem ele nao ha candidato -- nao instalo"'
N[i4:i4f + 1] = DOC
N[i2] = MARCA_NOVA
t1 = "\n".join(N)
assert "[A ADAPTAR v412]" not in t1 and "PINO_RECIBO_PRE_SELO_v412.json\")" not in t1 and "_N == 0" not in t1
compile(t1, "instalar_v412.py", "exec")

# ---------------- reverter ----------------
q = V / "reverter_v412.py"; r0 = q.read_bytes().decode("utf-8"); r1 = r0
def troca(velho, novo, n=1):
    global r1
    assert r1.count(velho) == n, (r1.count(velho), velho[:80]); r1 = r1.replace(velho, novo)
lin_marca = next(l for l in r1.split("\n") if l.startswith("# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO"))
troca(lin_marca, MARCA_NOVA.replace("o B(n) pre-selo sai como desvio declarado", "a lista do instalador tem os 156 e vai a quarentena se o rito falhar"))
troca('== esp["kernel"]["modulos_novos"] == 0 and set(_lista) == set(esp["bundle_sha256"])', '== esp["kernel"]["modulos_novos"] == 156 and set(_lista) == set(esp["bundle_sha256"])')
troca('"APLICADO_AO_CANONICO.modulos_novos_v412.lista (vazia)" if "lista" in _aplic else "ESPERADOS.bundle_sha256 (vazio)"',
      '"APLICADO_AO_CANONICO.modulos_novos_v412.lista (156)" if "lista" in _aplic else "ESPERADOS.bundle_sha256 (156)"')
troca("for nome in _lista:   # (vazia na v412: nenhum modulo novo; o laco fica, como no molde, para a forma ser a mesma)",
      "for nome in _lista:   # (v412: os 156 modulos novos que o rito materializou vao a quarentena, como no molde da v410)")
assert "[A ADAPTAR v412]" not in r1
compile(r1, "reverter_v412.py", "exec")

for arq, a, b in ((p, t0, t1), (q, r0, r1)):
    d = list(difflib.unified_diff(a.split("\n"), b.split("\n"), arq.name, arq.name + " (adaptado)", lineterm="", n=0))
    print("=====", arq.name, "| linhas trocadas:", sum(1 for x in d if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))))
    for x in d[:80]:
        print(x[:200])
if EXEC:
    for arq, a, b in ((p, t0, t1), (q, r0, r1)):
        bak = arq.with_name(arq.name + ".bak_antes_da_etapa3_" + TS); bak.write_bytes(a.encode("utf-8")); assert bak.read_bytes() == a.encode("utf-8")
        tmp = arq.with_name(arq.name + ".tmp_c1"); tmp.write_bytes(b.encode("utf-8")); assert tmp.stat().st_size == len(b.encode("utf-8")); tmp.replace(arq)
        print("gravado:", arq.name, "| backup:", bak.name, "| sha16", hashlib.sha256(arq.read_bytes()).hexdigest()[:16])
