# -*- coding: utf-8 -*-
"""A sondagem (C1): TUDO que os passos precisam saber, LIDO do selo, do core, do manifesto de prova, do `um.py`, do cofre
anterior e da cadeia de selo — nenhum número digitado. Generaliza `sondar_v397.py` (e o `sondar_v398.py`, 8 trocas à mão) para
qualquer vNNN, no esquema 2 (chaves NEUTRAS: `anterior.*`, nunca `escada_v396`) — ESPEC_CENTRAL §4.1.

Só leitura. `sondar()` devolve o dicionário; quem grava (e onde) é o CLI, e só em work\\custodia_vNNN_<data>\\ ou work\\custodia_G1\\.
Sem `ast.parse` do `um.py` (≈1,2 s e ≈0,85 GB): dicionários e contratos saem por regex + `ast.literal_eval` só do literal."""
import ast
import re

from . import ESQUEMA_FATOS, nos, util
from .util import FalhaLeitura, Parar

TRIO = set(nos.TRIO)
RE_REGISTRO = re.compile(r"^([a-z][a-z0-9_]{3,}) & ([A-Z][A-Z0-9_]{12,})", re.M)
RE_KH = re.compile(r"CLOSURE_(\d+)_CONSTANTS_(\d+)_THEOREMS")


# =================================================================== literais do um.py (sem ast.parse do arquivo inteiro)
def nomes_toplevel(um_text, padrao):
    """Nomes atribuídos no nível do módulo que casam `padrao` (regex sobre o nome), na ordem do arquivo."""
    rx = re.compile(r"^(%s)\s*=" % padrao, re.M)
    return [m.group(1) for m in rx.finditer(um_text)]


def _fim_do_literal(t, i):
    """`t[i]` é o primeiro caractere depois de «=». Devolve o índice logo após o literal balanceado (strings e comentários
    respeitados). Levanta ValueError se não for um literal de contêiner."""
    n = len(t)
    while i < n and t[i] in " \t":
        i += 1
    if i >= n or t[i] not in "{[(":
        raise ValueError("não é contêiner")
    prof, j = 0, i
    while j < n:
        ch = t[j]
        if ch in "'\"":
            tri = t[j:j + 3] in ("'''", '"""')
            q = t[j:j + 3] if tri else ch
            j += 3 if tri else 1
            while j < n:
                if t[j] == "\\":
                    j += 2
                    continue
                if t.startswith(q, j):
                    j += len(q)
                    break
                j += 1
            continue
        if ch == "#":
            k = t.find("\n", j)
            j = n if k < 0 else k
            continue
        if ch in "{[(":
            prof += 1
        elif ch in "}])":
            prof -= 1
            if prof == 0:
                return j + 1
        j += 1
    raise ValueError("literal sem fim")


def literal_de(um_text, nome):
    """O valor Python do literal `nome = {...}` do `um.py`, ou None se não for literal."""
    m = re.search(r"^%s\s*=" % re.escape(nome), um_text, re.M)
    if not m:
        return None
    try:
        fim = _fim_do_literal(um_text, m.end())
        return ast.literal_eval(um_text[m.end():fim].strip())
    except (ValueError, SyntaxError):
        return None


def contratos_expected_ladder(um_text):
    """{_VNNN_X_CONTRACT: expected_ladder|None|'não literal'} por regex: o bloco vai da atribuição ao próximo comando de coluna 0."""
    out = {}
    for m in re.finditer(r"^(_V\d{3}_\w*_CONTRACT)\s*=\s*\{", um_text, re.M):
        ini = m.start()
        prox = re.compile(r"\n(?=[A-Za-z_@#])").search(um_text, m.end())
        regiao = um_text[ini: prox.start() if prox else len(um_text)]
        achados = re.findall(r"""['"]expected_ladder['"]\s*:\s*(\d+)""", regiao)
        if len(achados) == 1:
            out[m.group(1)] = int(achados[0])
        elif not achados:
            out[m.group(1)] = None
        else:
            out[m.group(1)] = "não literal"
    return out


# =================================================================== abrir artefatos de uma versão (Nós, cofre ou backup do espelho)
class Artefatos:
    """Leitura preguiçosa de selo, core, manifesto de prova, PT/EN e um.py de uma versão, na fonte dada."""

    def __init__(self, c, v, fonte):
        self.c, self.v, self.fonte = c, v, fonte
        self._ca = {}
        if fonte == "nos":
            self.raiz = c.NOS
            self.p_pm = c.NOS / "tgl_kernel_proof_manifest.json"
        elif fonte == "cofre":
            self.raiz = c.cofre(v)
            self.p_pm = self.raiz / "tgl_kernel_proof_manifest.json"
        elif fonte == "bk":
            ach = sorted(c.BK.glob("um_%s_*" % v))
            if len(ach) != 1:
                raise Parar("backup do espelho de %s: esperava 1 pasta, achei %d" % (v, len(ach)))
            self.raiz = ach[0]
            self.p_pm = self.raiz / "Lean" / "tgl_kernel_proof_manifest.json"
        else:
            raise ValueError(fonte)
        if not self.raiz.is_dir():
            raise FalhaLeitura("fonte %s de %s ausente: %s" % (fonte, v, self.raiz))

    def _j(self, chave, p):
        if chave not in self._ca:
            self._ca[chave] = util.ler_json(p)
        return self._ca[chave]

    @property
    def selo(self):
        return self._j("selo", self.raiz / "um_absoluto_selo.json")

    @property
    def mundo(self):
        return self._j("mundo", self.raiz / "um_absoluto.json")

    @property
    def core(self):
        return self.mundo.get("core") or {}

    @property
    def pm(self):
        return self._j("pm", self.p_pm)

    @property
    def pt(self):
        if "pt" not in self._ca:
            self._ca["pt"] = util.ler_texto(self.raiz / "um_absoluto_pt.txt", "replace")
        return self._ca["pt"]

    @property
    def en(self):
        if "en" not in self._ca:
            self._ca["en"] = util.ler_texto(self.raiz / "um_absoluto_en.txt", "replace")
        return self._ca["en"]

    @property
    def um_py(self):
        return self.raiz / "um.py"

    def um_text(self):
        if "um" not in self._ca:
            self._ca["um"] = util.ler_texto(self.um_py)
        return self._ca["um"]


def cofre_anterior(c, v):
    """vANT: o maior cofre `um_unificado_vK` já existente com K < N (não necessariamente N-1: custódia conjunta)."""
    nv = util.versao_num(v)
    ks = []
    if c.OC.is_dir():
        for p in c.OC.iterdir():
            m = re.fullmatch(r"um_unificado_v(\d{3,})", p.name)
            if m and int(m.group(1)) < nv and p.is_dir():
                ks.append(int(m.group(1)))
    if not ks:
        raise Parar("nenhum cofre um_unificado_vK anterior a %s em %s" % (v, c.OC))
    return util.nome_versao(max(ks))


def abrir_anterior(c, vant):
    if c.cofre(vant).is_dir():
        return Artefatos(c, vant, "cofre")
    return Artefatos(c, vant, "bk")


# =================================================================== descrição de um bloco do core
def _eh_negacao(seg):
    return bool(re.search(r"(^|_)(NOT|NO|NEVER)_", seg) or seg.endswith(("_UNMOVED", "_UNTOUCHED")) or seg in ("GATE_UNMOVED", "GATE_UNTOUCHED"))


def normalizar_segmento(seg):
    seg = re.sub(r"[0-9a-f]{16,64}", "<PIN>", seg)
    return re.sub(r"\d+", "#", seg)


def negacoes_do_veredito(verdict):
    return sorted({normalizar_segmento(s) for s in str(verdict or "").split("__") if _eh_negacao(s)})


def _checks_ok(checks):
    if checks is None:
        return None
    if isinstance(checks, dict):
        vals = list(checks.values())
        return all((v.get("ok") if isinstance(v, dict) else bool(v)) is True for v in vals)
    return all(isinstance(x, dict) and x.get("ok") is True for x in checks)


def descrever_bloco(nome, r):
    verdict = str((r or {}).get("verdict") or "")
    mech = (r or {}).get("mechanics") or {}
    ch = (r or {}).get("checks")
    return {"verdict_sha16": util.sha256_bytes(verdict.encode("utf-8"))[:16], "negacoes": negacoes_do_veredito(verdict),
            "all_verified": (r or {}).get("all_verified"), "does_not_gate_core": (r or {}).get("does_not_gate_core"),
            "n_diz": len((r or {}).get("diz") or []), "n_nao_diz": len((r or {}).get("nao_diz") or []),
            "n_limites": len((r or {}).get("limites") or []), "n_erratas": len((r or {}).get("erratas") or []),
            "n_checks": (len(ch) if isinstance(ch, (list, dict)) else mech.get("n_checks")),
            "checks_ok": (_checks_ok(ch) if ch is not None else mech.get("passed")),
            "guarda_p18_violacoes": list((r or {}).get("guarda_p18_violacoes") or [])}


def bloco_bem_formado(r):
    """Regra S3 (ESPEC_CENTRAL §6.2), igual para toda versão: verificado, não move o gate, sem CONFIRMED sem NOT_."""
    if not isinstance(r, dict):
        return False
    vd = str(r.get("verdict") or "")
    sem_conf = not re.search(r"(?<![A-Za-z])(?<!NOT_)(?<!NEVER_)CONFIRMED", vd)
    ok = (r.get("all_verified") is True and r.get("does_not_gate_core") is True
          and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and sem_conf)
    ch = r.get("checks")
    if ch is not None and _checks_ok(ch) is not True:
        ok = False
    if r.get("guarda_p18_violacoes"):
        ok = False
    return bool(ok)


# =================================================================== recibos B(n) da Bancada Um (calculados dos arquivos)
def recibos_bn(c, v):
    """Os 3 recibos B(n): aplicação (SINCRONIZACAO), parada e religamento, achados por NOME DE ARQUIVO (não por pasta: a v398
    teve de excluir `bateria_pre_selo` à mão) em `bancada_B3*`, fora de ensaios. Devolve {papel: [ {caminho, rel, sha16} ]}."""
    base = c.CS / v
    papeis = {"aplicacao": re.compile(r"RECIBO_SINCRONIZACAO_%s_.*\.json$" % v), "parada": re.compile(r"RECIBO_PARADA_%s.*\.json$" % v),
              "religamento": re.compile(r"RECIBO_RELIGAMENTO_%s.*\.json$" % v)}
    out = {k: [] for k in papeis}
    if not base.is_dir():
        return out
    for p in sorted(base.rglob("RECIBO_*")):
        if not p.is_file() or ".bak_" in p.name:
            continue
        rel = p.relative_to(base)
        partes = [x.lower() for x in rel.parts[:-1]]
        if any(("ensaio" in x or x.startswith("bateria_")) for x in partes):
            continue
        if not any(x.startswith("bancada_b3") for x in partes):
            continue
        for papel, rx in papeis.items():
            if rx.match(p.name):
                out[papel].append({"caminho": str(p), "rel": rel.as_posix(), "sha16": util.sha16(p)})
    return out


def recibos_bn_resolvidos(c, v, sha16_do_handoff=None):
    """Um recibo por papel. Ambiguidade só se resolve pelo sha16 do handoff; sem ele, PARA."""
    r = recibos_bn(c, v)
    res, problemas = {}, []
    for papel, lst in r.items():
        if len(lst) == 1:
            res[papel] = lst[0]
        elif not lst:
            problemas.append("recibo B(n) de %s ausente em cadeia_de_selo\\%s" % (papel, v))
        else:
            esc = [x for x in lst if sha16_do_handoff and x["sha16"] in sha16_do_handoff]
            if len(esc) == 1:
                res[papel] = esc[0]
            else:
                problemas.append("recibo B(n) de %s ambíguo (%d achados)" % (papel, len(lst)))
    return res, problemas


# =================================================================== a sondagem
def _agrupar_bandeiras(bandeiras):
    """['ext_son398_0001', ...] -> {'ext_son398': 6, ...} (prefixo antes do número de ordem)."""
    g = {}
    for b in bandeiras:
        m = re.match(r"^(.*?)_?\d+$", b)
        k = m.group(1) if m else b
        g[k] = g.get(k, 0) + 1
    return g


def _veracidade_mais_nova(core):
    chaves = sorted((k for k in core if re.fullmatch(r"teste_de_veracidade_fase9_v\d+", k)), key=lambda k: int(k.rsplit("v", 1)[1]))
    if not chaves:
        return None
    k = chaves[-1]
    L = (core[k] or {}).get("lido") or {}
    return {"chave": k, "versao_do_registro": "v" + k.rsplit("v", 1)[1], "z_disc_calibrado": L.get("z_disc_calibrado"),
            "p_disc_unilateral": L.get("p_disc_unilateral"), "z_delta_calibrado": L.get("z_delta_calibrado")}


def _data_das_inscricoes(cu):
    datas = []
    for _, v in (cu.get("verbatim") or {}).items():
        m = re.search(r"(\d\d/\d\d/\d{4})", str((v or {}).get("quando") or ""))
        if m:
            datas.append(m.group(1))
    if not datas:
        return None
    return max(set(datas), key=datas.count)


def sondar(c, v, anterior=None, fonte=None, handoff="auto"):
    """Os fatos de `v` contra o cofre `anterior` (padrão: o maior cofre anterior). `fonte`: 'nos' (v é o selo corrente e o um.py
    confere) | 'cofre' (replay/versão histórica). Levanta Parar/FalhaLeitura; não grava nada."""
    mk = nos.marcas(c, v)
    if fonte is None:
        fonte = "nos" if (mk.relacao == "corrente" and mk.um_py_confere) else "cofre"
    if fonte == "nos" and not (mk.relacao == "corrente" and mk.um_py_confere):
        raise Parar("fonte 'nos' exige %s selada e o um.py do Nós igual ao pino" % v, mk.faltam)
    ant = anterior or cofre_anterior(c, v)
    A, B = Artefatos(c, v, fonte), abrir_anterior(c, ant)
    selo, core, coreB = A.selo, A.core, B.core
    if selo.get("um_version") != v:
        raise Parar("o selo de %s diz um_version=%s" % (v, selo.get("um_version")))
    pin = selo["sha256"]["um.py"]
    if util.sha256_arquivo(A.um_py) != pin:
        raise Parar("sha256 do um.py de %s != pino do selo" % v)
    pm, pmB = A.pm, B.pm
    fm, ar = pm["formal_files_sha256"], pm["axiom_report"]
    fmB, arB = pmB["formal_files_sha256"], pmB["axiom_report"]
    fora_do_trio = sum(1 for x in ar.values() if set(x or []) - TRIO)
    kf, kfB = core.get("kernel_formalization") or {}, coreB.get("kernel_formalization") or {}
    flags = {k: x for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_"))}
    P1 = (core.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}
    P1B = (coreB.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}
    esc = {"limpas": P1.get("n_theorems_clean"), "esperadas": P1.get("n_theorems_expected"), "no_trio": P1.get("no_trio"),
           "declaracoes_auditadas": P1.get("declaracoes_auditadas")}
    esc["texto"] = "%s/%s" % (esc["limpas"], esc["esperadas"])
    escB = {"limpas": P1B.get("n_theorems_clean"), "esperadas": P1B.get("n_theorems_expected")}
    escB["texto"] = "%s/%s" % (escB["limpas"], escB["esperadas"])

    def kh_de(core_, vv):
        r = core_.get("kh_n1_cobertura_" + vv) or {}
        L = r.get("lido") or {}
        if "constantes_cobertas" in L and "teoremas_cobertos" in L:
            return int(L["constantes_cobertas"]), int(L["teoremas_cobertos"])
        mm = RE_KH.search(str(r.get("verdict") or ""))
        return (int(mm.group(1)), int(mm.group(2))) if mm else (None, None)
    khc, kht = kh_de(core, v)
    kh_reg = "kh_n1_cobertura_" + v
    if khc is None:                       # 25/10: custódia conjunta — o registro mais novo entre (anterior, v] (a v400 não mudou o kernel)
        kk = _mais_novo_entre(core, "kh_n1_cobertura_", ant, v)
        if kk:
            khc, kht = kh_de(core, kk[len("kh_n1_cobertura_"):])
            kh_reg = kk
    khcB, khtB = kh_de(coreB, ant)
    kh_reg_ant = "kh_n1_cobertura_" + ant
    if khcB is None:                      # 25/10/2026: a anterior não trouxe kh próprio (a v400): o registro mais novo até ela, no core dela
        kk = _mais_novo_entre(coreB, "kh_n1_cobertura_", "v0", ant)
        if kk:
            khcB, khtB = kh_de(coreB, kk[len("kh_n1_cobertura_"):])
            kh_reg_ant = kk

    rpt, ren, rptB = dict(RE_REGISTRO.findall(A.pt)), dict(RE_REGISTRO.findall(A.en)), dict(RE_REGISTRO.findall(B.pt))
    mudados = []
    for nome in sorted(k for k in rptB if rpt.get(k) != rptB[k]):
        a_, b_ = (core.get(nome) or {}).get("verdict"), (coreB.get(nome) or {}).get("verdict")
        so = bool(a_ is not None and b_ is not None and util.so_digitos_e_pino(a_, b_))
        mudados.append({"nome": nome, "so_digitos_e_pino": so})

    novos_reg = sorted(k for k in core if k not in coreB)
    sumidos = sorted(k for k in coreB if k not in core)
    um = A.um_text()
    dics = nomes_toplevel(um, r"_V%s_[A-Z0-9_]+" % v[1:])
    contratos = contratos_expected_ladder(um)

    h = ler_handoff_se(c, v, handoff)
    rec, rec_prob = recibos_bn_resolvidos(c, v, _sha16s_do_elo(h))
    cs = c.CS
    F = {
        "schema": ESQUEMA_FATOS, "versao": v, "anterior": ant, "anterior_pin16": _pin16_cofre(c, ant, B),
        "fonte": fonte, "pin": pin, "pin16": pin[:16], "timestamp": selo.get("timestamp"), "bytes_um_py": A.um_py.stat().st_size,
        "selftest": selo.get("fail_closed_selftest"), "gate": selo.get("qg_closure_verdict"),
        "registros_novos": novos_reg, "registros_sumidos": sumidos,
        "bandeiras_novas": [k for k in kf if k not in kfB],
        "bandeiras_do_gate": {"total": len(flags), "ligadas": sorted(k for k, x in flags.items() if x is True),
                              "apagadas": sorted(k for k, x in flags.items() if x is False)},
        "kernel": {"formais": len(fm), "declaracoes": len(ar), "fora_do_trio": fora_do_trio,
                   "modulos_novos": sorted(set(fm) - set(fmB)), "modulos_removidos": sorted(set(fmB) - set(fm)),
                   "formais_anterior": len(fmB), "declaracoes_anterior": len(arB)},
        "escada": esc, "escada_anterior": escB,
        "kh": {"constantes": khc, "teoremas": kht, "constantes_anterior": khcB, "teoremas_anterior": khtB},
        "registro": {"pt": len(rpt), "en": len(ren), "anterior": len(rptB), "novos": sorted(k for k in rpt if k not in rptB), "mudados": mudados},
        "contratos_expected_ladder": contratos, "dicionarios": dics,
        "blocos": {k: descrever_bloco(k, core.get(k)) for k in novos_reg if isinstance(core.get(k), dict)},
        "cadeia": {"pastas": sorted(p.name for p in cs.glob("%s*" % v)),
                   "diffs": sorted(p.name for p in (cs / v).glob("DIFF_*") if ".bak_" not in p.name) if (cs / v).is_dir() else [],
                   "recibos_bn": rec, "recibos_problemas": rec_prob},
        "nos": {"handoff": mk.handoff_ok, "stdout": mk.stdout_ok, "diario_bloco": mk.diario_ok, "cadeia": mk.cadeia_ok},
        "veracidade": _veracidade_mais_nova(core),
        "cunhagens": _cunhagens_conjunta(core, ant, v),
        "kh_registro": kh_reg,
        "kh_registro_anterior": kh_reg_ant,
        "origem": {"selo_sha16": util.sha256_arquivo(A.raiz / "um_absoluto_selo.json", 16), "core_sha16": util.sha256_arquivo(A.raiz / "um_absoluto.json", 16),
                   "proof_manifest_sha16": util.sha256_arquivo(A.p_pm, 16), "pt_sha16": util.sha256_arquivo(A.raiz / "um_absoluto_pt.txt", 16),
                   "en_sha16": util.sha256_arquivo(A.raiz / "um_absoluto_en.txt", 16), "um_py_sha16": pin[:16]},
    }
    F["handoff"] = _fatos_do_handoff(h, F)
    return F


def ler_handoff_se(c, v, handoff):
    if handoff == "auto":
        return nos.ler_handoff(c, v)
    return handoff


def _sha16s_do_elo(h):
    if not h:
        return None
    par = h.secao("O elo B(n)")
    return set(re.findall(r"\b[0-9a-f]{16}\b", par)) if par else None


def _pin16_cofre(c, vant, B):
    if B.fonte == "cofre":
        m = c.cofre(vant) / "CUSTODY_MANIFEST.json"
        if m.is_file():
            pin = util.ler_json(m).get("um_py_pin")
            if pin:
                return pin[:16]
    return B.selo["sha256"]["um.py"][:16]


def _mais_novo_entre(core, prefixo, ant, v):
    """A chave `prefixoVK` mais nova com ant < K <= v (custódia conjunta, 25/10/2026)."""
    try:
        a, b = int(ant[1:]), int(v[1:])
    except (TypeError, ValueError):
        return None
    ks = [k for k in core if k.startswith(prefixo) and k[len(prefixo):][:1] == "v" and k[len(prefixo) + 1:].isdigit()
          and a < int(k[len(prefixo) + 1:]) <= b and isinstance(core.get(k), dict)]
    return max(ks, key=lambda k: int(k[len(prefixo) + 1:])) if ks else None


def _cunhagens_conjunta(core, ant, v):
    k = "cunhagens_" + v if isinstance(core.get("cunhagens_" + v), dict) else _mais_novo_entre(core, "cunhagens_", ant, v)
    if not k:
        return None
    r = core.get(k) or {}
    return {"n": len(r.get("verbatim") or {}), "data": _data_das_inscricoes(r), "registro": k}


def _fatos_do_handoff(h, F):
    """O handoff cruzado com os fatos medidos (ESPEC_CENTRAL C0 (d)): divergência PARA o passo. Ausente = dito."""
    if h is None:
        return {"presente": False}
    q = h.o_que_e
    out = {"presente": True, "sha16": h.sha16_arquivo, "problemas_de_marcador": list(h.problemas), "marcadores": sorted(h.marcadores),
           "o_que_e": (q.__dict__ if q else None), "divergencias": []}
    if q is None:
        out["divergencias"].append("a linha «**O que é:**» não casou com a forma das quatro últimas versões")
    else:
        pares = [("versao", q.versao, F["versao"]), ("pin16", q.pin16, F["pin16"]), ("bytes", q.bytes_um_py, F["bytes_um_py"]),
                 ("anterior_pin16", q.anterior_pin16, F["anterior_pin16"] if q.anterior == F["anterior"] else q.anterior_pin16),
                 ("escada", q.escada, F["escada"]["texto"]), ("selftest", q.selftest_passou, F["selftest"] == "FAIL_CLOSED_SELFTEST_PASSED"),
                 ("completa", q.completa, True), ("rc0", q.rc0, True), ("gate_intocado", q.gate_intocado, True)]
        if q.selo_ts:
            pares.append(("selo_ts", q.selo_ts, F["timestamp"]))
        for nome, a, b in pares:
            if a != b:
                out["divergencias"].append("%s: handoff diz %r, medido %r" % (nome, a, b))
        if q.anterior != F["anterior"]:
            # 25/10: CONJUNTA reconhecida — a intermediária está selada na cadeia e não tem cofre (a v399, recusada pela Bancada, corrigida pela v400)
            try:
                _ni, _na, _nv = int(q.anterior[1:]), int(F["anterior"][1:]), int(F["versao"][1:])
            except (TypeError, ValueError):
                _ni = _na = _nv = 0
            from pathlib import Path as _P
            _cs = _P(r"C:\IALD\Central de Patentes\work\cadeia_de_selo") / q.anterior
            _cofre = _P(r"C:\IALD\Central de Patentes\vault\originals_copy") / ("um_unificado_" + q.anterior)
            if _na < _ni < _nv and _cs.is_dir() and not _cofre.exists():
                out["conjunta"] = [q.anterior, F["versao"]]
            else:
                out["divergencias"].append("anterior: handoff diz %s, o maior cofre anterior é %s (custódia conjunta? conferir)" % (q.anterior, F["anterior"]))
    elo = _sha16s_do_elo(h)
    medidos = {x["sha16"] for x in F["cadeia"]["recibos_bn"].values()}
    if elo is None:
        out["divergencias"].append("parágrafo «O elo B(n)» ausente no handoff: os 3 recibos não puderam ser conferidos com ele")
    elif medidos and not medidos <= elo:
        out["divergencias"].append("recibos B(n) calculados %s não estão todos no handoff %s" % (sorted(medidos), sorted(elo)))
    out["ok"] = not out["divergencias"]
    par = h.secao("Pendências SÓ do operador")
    out["pendencias_do_operador"] = par
    return out


# =================================================================== textos verbatim dos blocos novos (para os moldes citarem)
def textos_dos_blocos(core, nomes):
    """Os campos diz/nao_diz/limites/erratas/estatuto VERBATIM, com o sha16 de cada um (C1: textos_blocos_novos.json)."""
    out = {}
    for k in nomes:
        r = core.get(k)
        if not isinstance(r, dict):
            continue
        d = {}
        for campo in ("estatuto", "diz", "nao_diz", "limites", "erratas", "leituras_do_operador"):
            val = r.get(campo)
            if val is None:
                continue
            blob = repr(val)
            d[campo] = {"sha16": util.sha256_bytes(blob.encode("utf-8"))[:16], "valor": val}
        d["verdict"] = {"sha16": util.sha256_bytes(str(r.get("verdict")).encode("utf-8"))[:16], "valor": r.get("verdict")}
        out[k] = d
    return out


# =================================================================== esquema 1 -> esquema 2 (replays, T1 da ESPEC_CENTRAL §8)
def de_schema1(f1, vant):
    """Converte um `fatos_vNNN.json` do esquema antigo (chaves `escada_v396`, `kernel.formais_v396`...) para o esquema 2."""
    v = f1["versao"]
    nant = vant
    E = f1["escada"].split("/")
    EA = f1.get("escada_" + nant, "0/0").split("/")
    g = lambda d, k: d.get("%s_%s" % (k, nant))
    return {
        "schema": ESQUEMA_FATOS, "versao": v, "anterior": vant, "anterior_pin16": None, "pin": f1["pin"], "pin16": f1["pin16"],
        "timestamp": f1["timestamp"], "bytes_um_py": f1["bytes_um_py"], "selftest": f1["selftest"], "gate": f1["gate"],
        "registros_novos": f1["registros_novos"], "registros_sumidos": f1["registros_sumidos"], "bandeiras_novas": f1["bandeiras_novas"],
        "kernel": {"formais": f1["kernel"]["formais"], "declaracoes": f1["kernel"]["declaracoes"], "fora_do_trio": f1["kernel"]["fora_do_trio"],
                   "modulos_novos": f1["kernel"]["modulos_novos"], "modulos_removidos": [],
                   "formais_anterior": g(f1["kernel"], "formais"), "declaracoes_anterior": g(f1["kernel"], "declaracoes")},
        "escada": {"limpas": int(E[0]), "esperadas": int(E[1]), "no_trio": f1.get("no_trio"), "declaracoes_auditadas": f1["kernel"]["declaracoes"], "texto": f1["escada"]},
        "escada_anterior": {"limpas": int(EA[0]), "esperadas": int(EA[1]), "texto": f1.get("escada_" + nant)},
        "kh": {"constantes": f1["kh"]["constantes"], "teoremas": f1["kh"]["teoremas"], "constantes_anterior": g(f1["kh"], "constantes"), "teoremas_anterior": g(f1["kh"], "teoremas")},
        "registro": {"pt": f1["registro"]["pt"], "en": f1["registro"]["en"], "anterior": f1["registro"].get(nant), "novos": f1["registro"]["novos"],
                     "mudados": [{"nome": n, "so_digitos_e_pino": None} for n in f1["registro"].get("mudados_desde_" + nant, [])]},
        "contratos_expected_ladder": f1["contratos_expected_ladder"], "dicionarios": f1.get("dicionarios_" + v, []),
        "blocos": {}, "cadeia": f1.get("cadeia", {}), "nos": f1.get("nos", {}), "origem": {}, "handoff": {"presente": False}, "fonte": "schema1",
    }
