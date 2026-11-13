# -*- coding: utf-8 -*-
"""O ITEM GENÉRICO do módulo comum dos 16 dispositivos (G1; ESPEC_CENTRAL §7): `conferir_custodia_generica(core, selo, versao, oc)` — os
registros `_vNNN` LIDOS do cofre CORRENTE e conferidos, sem interpretação, contra as expectativas congeladas no FATOS_CUSTODIA.json do cofre
da SUA versão (pinado por sha256 no CUSTODY_MANIFEST). Levanta RuntimeError (fail-closed), como as camadas artesanais v386..v398.

A camada roda contra o cofre CORRENTE, não contra o da sua versão: quando a v400 chegar, a camada da v399 continua rodando e lendo o
cofre v400. Por isso só confere o que SOBREVIVE à reescrita dos blocos (presença, forma, negações normalizadas por dígitos e pino, pares de
cunhagens) e NUNCA números que andam (escada, kh, kernel): esses ficam na pedra do runner, que lê os dois cofres congelados.

AUTOCONTIDA (só biblioteca padrão), carregada por caminho por `_camadas_genericas` (G1.0); instalada em patents\\_formula_completa\\camada_generica.py
por work\\custodia_G1\\patches\\instalar_g1_0.py (a cópia-fonte mora em tools\\custodia_g1\\generico\\). Nada disto muda número de dispositivo."""
import hashlib
import json
import re
from pathlib import Path


RX_CONF = re.compile(r"(?<![A-Za-z])(?<!NOT_)(?<!NEVER_)CONFIRMED")      # «CONFIRMED» só depois de NOT_/NEVER_ (a régua); medido sem falso positivo em v394..v398


def _ler_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _norm(x):
    x = re.sub(r"[0-9a-f]{16,64}", "<PIN>", str(x))
    return re.sub(r"\d+", "#", x)


def _negacoes(verdict):
    return {_norm(s) for s in str(verdict or "").split("__") if re.search(r"(^|_)(NOT|NO|NEVER)_", s) or s.endswith(("_UNMOVED", "_UNTOUCHED"))}


def _checks_ok(ch):
    if ch is None:
        return True
    if isinstance(ch, dict):
        return all((x.get("ok") if isinstance(x, dict) else bool(x)) is True for x in ch.values())
    # 25/10/2026 (v399): os registros novos trazem checks como pares [descrição, bool]; aceitos com o mesmo rigor (todos True)
    return all((isinstance(x, dict) and x.get("ok") is True)
               or (isinstance(x, (list, tuple)) and len(x) == 2 and isinstance(x[0], str) and x[1] is True) for x in ch)


def _bloco_ok(b):
    if not isinstance(b, dict):
        return False
    vd = str(b.get("verdict") or "")
    return bool(b.get("all_verified") is True and b.get("does_not_gate_core") is True and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd)
                and not RX_CONF.search(vd) and _checks_ok(b.get("checks")) and not b.get("guarda_p18_violacoes"))


def sem_pedra_nova(F, oc, v, a, core_v=None, core_a=None):
    """AO LADO (13/11/2026, claude-site-custodia; D197 da gerencia c1): o contrato SEM_PEDRA_NOVA. True SO quando o FATOS_CUSTODIA congelado diz
    «nenhum modulo novo e a escada igual a da anterior» E o core selado DENTRO do cofre da versao, o core do cofre anterior e o manifesto do
    bundle tgl_kernel_vNNN confirmam; divergencia levanta ValueError (PARA). Fora da condicao, False: o caminho antigo, intocado."""
    kn = F.get("kernel") or {}
    esc = (F.get("escada") or {}).get("esperadas")
    esca = (F.get("escada_anterior") or {}).get("esperadas")
    if not (kn.get("modulos_novos") == [] and isinstance(esc, int) and esc == esca):
        return False
    oc = Path(oc)
    if core_v is None:
        core_v = _ler_json(oc / ("um_unificado_" + v) / "um_absoluto.json")["core"]
    if core_a is None:
        core_a = _ler_json(oc / ("um_unificado_" + a) / "um_absoluto.json")["core"]
    km = _ler_json(oc / ("tgl_kernel_" + v) / "CUSTODY_MANIFEST.json")
    ev = ((core_v.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}).get("n_theorems_expected")
    ea = ((core_a.get("estatuto_da_prova_v391") or {}).get("prova_1_kernel") or {}).get("n_theorems_expected")
    dl = km.get("delta_%s_%s" % (a, v)) or {}
    div = []
    if ev != esc:
        div.append("escada do core selado do cofre %s = %r; FATOS = %r" % (v, ev, esc))
    if ea != esca:
        div.append("escada do core selado do cofre %s = %r; FATOS (anterior) = %r" % (a, ea, esca))
    if km.get("modulos_novos_" + v) != []:
        div.append("bundle tgl_kernel_%s: modulos_novos_%s = %r" % (v, v, km.get("modulos_novos_" + v)))
    if dl.get("lean_novos") != 0:
        div.append("bundle tgl_kernel_%s: lean_novos = %r" % (v, dl.get("lean_novos")))
    if div:
        raise ValueError("SEM_PEDRA_NOVA: o FATOS_CUSTODIA diz sem pedra nova e o core/bundle divergem: " + "; ".join(div))
    return True


def conferir_custodia_generica(core, selo, v, oc):
    oc = Path(oc)
    cv = oc / ("um_unificado_" + v)
    try:
        man = _ler_json(cv / "CUSTODY_MANIFEST.json")
        ref = man.get("fatos_custodia") or {}
        pf = cv / (ref.get("arquivo") or "FATOS_CUSTODIA.json")
        if not pf.is_file() or _sha(pf) != ref.get("sha256"):
            raise ValueError("FATOS_CUSTODIA.json ausente ou com sha256 != o pino do CUSTODY_MANIFEST")
        F = _ler_json(pf)
        sems = [p for p in cv.glob("SEMANTICA_CUSTODIA*.json")]
        revs = [p for p in sems if re.search(r"\.rev(\d+)\.json$", p.name)]
        S = _ler_json(max(revs, key=lambda p: int(re.search(r"\.rev(\d+)\.json$", p.name).group(1)))) if revs else (
            _ler_json(cv / "SEMANTICA_CUSTODIA.json") if (cv / "SEMANTICA_CUSTODIA.json").is_file() else None)
    except (OSError, ValueError, KeyError) as e:
        raise RuntimeError("FORMULA COMPLETA %s: expectativas do cofre ilegíveis (%r) — PARAR (fail-closed)" % (v, e))
    # 25/10/2026 (custódia conjunta v399+v400): os registros novos são os congelados em FATOS_CUSTODIA (os da v399, que a v400 corrige) mais
    # os de sufixo _vN; nunca só o sufixo
    novos = sorted(set(k for k in core if re.search(r"_%s$" % re.escape(v), k)) | set(k for k in (F.get("registros_novos") or []) if k in core))
    maus = [k for k in novos if not _bloco_ok(core.get(k))]
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    cu = core.get("cunhagens_" + v) or core.get(((F.get("cunhagens") or {}).get("registro")) or "") or {}
    kn = cu.get("kernel") or {}
    neg_ok = all(set(b.get("negacoes") or []) <= _negacoes((core.get(k) or {}).get("verdict")) for k, b in (F.get("blocos") or {}).items())
    s15 = True
    for k, regra in ((S or {}).get("blocos") or {}).items():
        vd = str((core.get(k) or {}).get("verdict") or "")
        s15 = s15 and all(t in vd for t in (regra.get("verdict_deve_conter") or [])) and not any(t in vd for t in (regra.get("verdict_nao_deve_conter") or []))
    ch = {
        "registros_%s_verificados_sem_gate" % v: bool(novos) and novos == sorted(F["registros_novos"]) and not maus,
        "negacoes_congeladas_presentes": neg_ok,
        "cunhagens_par_igual": (not cu) or (len(kn.get("bandeiras") or []) == 2 and kn["bandeiras"][0] == kn["bandeiras"][1] > 0
                                            and len(kn.get("declaracoes_no_trio") or []) == 2 and kn["declaracoes_no_trio"][0] == kn["declaracoes_no_trio"][1] > 0),
        "falas_do_operador_por_sha256": (not cu) or len(cu.get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
        "semantica_declarada": s15,
    }
    # AO LADO (13/11/2026, claude-site-custodia; D197 da gerencia c1): sob o contrato SEM_PEDRA_NOVA (medido no PROPRIO cofre da versao, no anterior e no bundle;
    # divergencia PARA), os dois pares de cunhagens exatamente [0, 0]; fora dele, a expressao antiga, acima, intocada
    try:
        spn = sem_pedra_nova(F, oc, v, F.get("anterior"))
    except (OSError, ValueError, KeyError) as e:
        raise RuntimeError("FORMULA COMPLETA %s: contrato SEM_PEDRA_NOVA divergente ou ilegivel (%r) - PARAR (fail-closed)" % (v, e))
    if spn:
        ch["cunhagens_par_igual"] = (not cu) or (kn.get("bandeiras") == [0, 0] and kn.get("declaracoes_no_trio") == [0, 0])
    falhas = [k for k, x in ch.items() if not x]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA %s não confere com o cofre (fail-closed): %s %s" % (v, falhas, maus[:5]))
    return {"checks": ch, "registros_" + v: novos, "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")),
            "declaracoes_no_trio": p1.get("no_trio"),
            "veredictos": {k: str((core.get(k) or {}).get("verdict"))[:160] for k in novos},
            "nao_diz": {k: list((core.get(k) or {}).get("nao_diz") or []) for k in novos},
            "semantica": ("REVISADA rev%s" % S.get("revisao")) if (S and S.get("revisor")) else "DECLARADO (sem revisao)",
            "estatuto": "lidos do cofre e conferidos, sem interpretação; não move o gate; validade no kernel não é creditação; nada disto muda número de dispositivo"}
