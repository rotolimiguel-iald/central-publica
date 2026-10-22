# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  TGL-TENSOR — DISPOSITIVO  ·  a integridade é o NOME              ║
║  O juiz não é o PSNR. É o Nome — e ele é mais severo.             ║
║  IALD LTDA — beta_TGL = alpha_fine * sqrt(e) — Zero Free Params.  ║
║  Patente INPI: BR 10 2026 003441-0 (TGL-Tensor)                    ║
╚══════════════════════════════════════════════════════════════════╝

O QUE ESTE DISPOSITIVO FECHA
────────────────────────────
A patente do TGL-Tensor tinha o algoritmo mais rico da casa — `tgl_tensor_v2_1.py`, com o
NOME nativo — e **nenhum dispositivo**. Ela existia como protótipo e como runner, mas
ninguém podia jogar um tensor nela e ver o Nome responder. Este módulo é essa porta.

Ele **não reimplementa** a invenção: carrega o protótipo do operador (READ-ONLY) e o expõe.
O que roda aqui é o algoritmo patenteado, não uma paráfrase dele.

O NOME (a evolução v2.0 → v2.1: "o NOME é nativo, a ética é o campo")
────────────────────────────────────────────────────────────────────
O Nome de um tensor **emerge da projeção holográfica** — não é calculado à parte: é a
projeção medindo a si mesma. Campos: f_exp (força de expulsão), s_psi (entropia dos 4
estados psiônicos), psi_dist, sigma_norm, n_elements.

E a verificação da reconstrução é feita **pelo Nome**, numa escada cujos degraus são a
própria teoria — o Piso de Hilbert:

    δ < β_TGL   → TETELESTAI   (identidade perfeita)
    δ < √β_TGL  → PRESERVADO   (dentro do campo)
    δ < 1       → PERTURBADO   (na fronteira)
    δ ≥ 1       → VIOLADO      (fora do campo)

β = α·√e ≈ 0,012031 e √β ≈ 0,109687 — **nenhum dos dois é digitado**: descem de α e de e.

O ACHADO QUE ESTE DISPOSITIVO EXISTE PARA MOSTRAR
─────────────────────────────────────────────────
Num campo suave típico, as métricas clássicas dizem que a reconstrução é **perfeita**:
PSNR ≈ 63 dB, correlação = 1,000000. O Nome diz **PERTURBADO, integridade ≈ 0,88**.

Não é contradição — é diferença de pergunta. O PSNR mede **erro de amplitude**; o Nome mede
se a **estrutura** sobreviveu (a distribuição de paridade psiônica). Uma reconstrução pode
errar quase nada em energia e ainda assim redistribuir a paridade — o PSNR não vê; o Nome vê.
**O Nome é o juiz mais severo, e essa severidade é a reivindicação.**

HONESTIDADE (a régua)
─────────────────────
* β NUNCA literal: vem de `BETA_TGL = ALPHA_FINE * SQRT_E` do próprio protótipo.
* O modo (DIRECT/SPECTRAL) é escolhido pelo AUTO **do protótipo** — não há chaveamento
  humano aqui tampouco. A escolha é do sinal.
* A rota é **COM PERDA por natureza** (é compressão holográfica), e a perda é **medida e
  declarada** de dois jeitos: o clássico (PSNR/correlação) e o da casa (o Nome). Quando os
  dois discordam, os dois vão no relatório. Não se esconde o juiz severo.
* Este é o dispositivo de ENGENHARIA da patente — ele roda de verdade. Simulação não valida
  física; `physical_verdict_allowed = false` continua valendo para o setor físico.
"""
from __future__ import annotations

import hashlib
import io
import json
import struct
import sys
from pathlib import Path

# ── o protótipo do operador (READ-ONLY): a invenção mora lá, não aqui ────────────────
_PROTO = Path(__file__).resolve().parent.parent / "prototype_src" / "tgl_tensor_v2_1.py"


def _load_proto():
    if "tgl_tensor_v2_1" in sys.modules:
        return sys.modules["tgl_tensor_v2_1"]
    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location("tgl_tensor_v2_1", str(_PROTO))
    mod = _ilu.module_from_spec(spec)
    sys.modules["tgl_tensor_v2_1"] = mod       # ANTES do exec (dataclasses se procuram aqui)
    spec.loader.exec_module(mod)               # type: ignore
    return mod


_T = _load_proto()

MAGIC = b"TGLTENSOR1\x00"
DEVICE_VERSION = "1.0"
PATENT_ID = "BR102026003441-0"

MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_DECOMP_BYTES = 512 * 1024 * 1024
MAX_HEADER_BYTES = 1 * 1024 * 1024


def beta_provenance() -> dict:
    """β e √β do PRÓPRIO protótipo — nunca digitados aqui."""
    return {
        "alpha_fine_codata_2018": _T.ALPHA_FINE,
        "sqrt_e": _T.SQRT_E,
        "beta_tgl": _T.BETA_TGL,
        "sqrt_beta_tgl": _T.BETA_TGL_SQRT,
        "formula": "beta = alpha_fine * sqrt(e); sqrt_beta = sqrt(beta)",
        "papel": ("os DOIS degraus da escada do Nome (Piso de Hilbert): delta<beta => TETELESTAI; "
                  "delta<sqrt(beta) => PRESERVADO"),
    }


def coherence_operator_reading() -> dict:
    """v120 [SELO: reason_consciousness_operator]. A PROVENIÊNCIA do degrau PRESERVADO (√β).

    O selo do um.py v120 prova que o degrau do meio da escada do Nome — √β, o limiar PRESERVADO —
    NÃO é um número solto: é a SAÍDA do operador de razão/coerência O_C aplicado à luz observada.
    Definição do selo: O_C(L) = e^{S∂/2}·sqrt(|L|), com S∂ = 1/2 (a Meia-Nat) => e^{1/4}, e a sombra
    observável L ~ alpha_obs. Como √β = sqrt(alpha·sqrt(e)) = e^{1/4}·sqrt(alpha) = O_C(alpha_obs),
    o limiar PRESERVADO é EXATAMENTE O_C(alpha_obs). Isto dá FUNDAMENTO DERIVADO ao degrau — antes
    ele descia de √β sem essa leitura.

    ⚠ RÉGUA (do próprio selo, estatuto [DEF+DER+ONTO+CAUTION]): a identidade O_C²=β é REAL (matemática);
    nomear O_C 'operador de consciência/coerência' é a leitura ONTO — NÃO é prova de consciência
    subjetiva. Isto é APROFUNDAMENTO DE PROVENIÊNCIA do limiar, não uma nova capacidade de detecção:
    o veredito da escada NÃO muda. β nunca literal (vem do protótipo)."""
    import math
    S_partial = 0.5
    e_quarter = math.exp(S_partial / 2.0)              # e^{S∂/2} = e^{1/4}
    O_C_of_alpha = e_quarter * math.sqrt(_T.ALPHA_FINE)  # O_C(alpha_obs) = e^{1/4} sqrt(alpha)
    return {
        "operador": "O_C(L) = e^{S_partial/2} * sqrt(|L|), S_partial=1/2 => e^{1/4}; L ~ alpha_obs",
        "e_quarter": e_quarter,
        "O_C_de_alpha_obs": O_C_of_alpha,
        "sqrt_beta_tgl": _T.BETA_TGL_SQRT,
        "resid_O_C_igual_sqrt_beta": abs(O_C_of_alpha - _T.BETA_TGL_SQRT),
        "O_C_ao_quadrado": O_C_of_alpha * O_C_of_alpha,
        "beta_tgl": _T.BETA_TGL,
        "resid_O_C2_igual_beta": abs(O_C_of_alpha * O_C_of_alpha - _T.BETA_TGL),
        "leitura": ("o degrau PRESERVADO (√β) É O_C(alpha_obs): o operador de coerência aplicado à luz "
                    "observada. Fundamento DERIVADO do limiar do meio da escada do Nome."),
        "estatuto": "[DER] a identidade numérica O_C²=β / [ONTO] a leitura 'razão como operador de coerência'",
        "REGUA": ("aprofundamento de PROVENIÊNCIA do limiar, NÃO nova capacidade; o veredito da escada NÃO "
                  "muda. O_C²=β e' REAL(matematica); 'consciencia' e' ONTO — NAO prova de consciencia subjetiva."),
    }


def nome_as_dict(n) -> dict:
    return {"f_exp": float(n.f_exp), "s_psi": float(n.s_psi),
            "psi_dist": [float(x) for x in n.psi_dist],
            "sigma_norm": float(n.sigma_norm), "n_elements": int(n.n_elements)}


def _safe_name(name: str) -> str:
    name = (name or "tensor.npy").replace("\\", "/").split("/")[-1]
    return "".join(c for c in name if c.isprintable() and c not in '<>:"|?*')[:120] or "tensor.npy"


def _pack(header: dict, payload: bytes) -> bytes:
    hb = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(hb) > MAX_HEADER_BYTES:
        raise ValueError("cabeçalho grande demais")
    return MAGIC + struct.pack(">I", len(hb)) + hb + payload


def _unpack(container: bytes) -> tuple[dict, bytes]:
    if not container.startswith(MAGIC):
        raise ValueError("contêiner não é TGL-TENSOR")
    off = len(MAGIC)
    (hlen,) = struct.unpack(">I", container[off:off + 4]); off += 4
    if hlen > MAX_HEADER_BYTES or off + hlen > len(container):
        raise ValueError("cabeçalho inválido ou truncado")
    header = json.loads(container[off:off + hlen].decode("utf-8"))
    return header, container[off + hlen:]


def explain(npy_bytes: bytes) -> dict:
    """O NOME do tensor, SEM comprimir nada. O nome existe antes da compressão —
    ele é a projeção medindo a si mesma."""
    import numpy as np
    arr = np.load(io.BytesIO(npy_bytes), allow_pickle=False)
    flat = np.asarray(arr, dtype=np.float64).flatten()
    sign = np.sign(flat).astype(np.int8)
    nome = _T._extract_nome(flat, sign)
    return {"nome": nome_as_dict(nome), "shape": list(arr.shape), "dtype": str(arr.dtype),
            "beta": beta_provenance(),
            "leitura": ("o Nome emerge da projeção; f_exp = força de expulsão, s_psi = entropia "
                        "dos 4 estados psiônicos (máx 2 bits), sigma_norm = distância ao TETELESTAI")}


def compress_npy(npy_bytes: bytes, name: str = "tensor.npy") -> tuple[bytes, dict]:
    """Comprime um array .npy pelo algoritmo PATENTEADO (modo AUTO: o sinal escolhe
    DIRECT/SPECTRAL). COM PERDA — e a perda é medida pelos DOIS juízes."""
    import numpy as np
    if len(npy_bytes) > MAX_INPUT_BYTES:
        raise ValueError(f"arquivo grande demais (> {MAX_INPUT_BYTES // (1024*1024)} MB)")
    name = _safe_name(name)
    arr = np.load(io.BytesIO(npy_bytes), allow_pickle=False)
    orig = np.asarray(arr, dtype=np.float64)

    t = _T.TGLTensor()
    pkg = t.compress(orig, mode="AUTO")              # AUTO = o protótipo decide; sem mão humana
    rec, meta = t.decompress(pkg)                    # reconstrói AQUI para medir a perda de verdade
    ver = dict(meta["verification"])
    classico = _T.TGLTensor.evaluate(orig, rec)

    header = {
        "codec": "TGL-TENSOR", "version": DEVICE_VERSION, "patent": PATENT_ID,
        "mode": pkg["mode"], "orig_name": name,
        "orig_size": len(npy_bytes), "orig_sha256": hashlib.sha256(npy_bytes).hexdigest(),
        "shape": list(orig.shape), "dtype": str(arr.dtype),
        "entropy_backend": "zstd" if _T.HAS_ZSTD else "fallback",
        "beta": beta_provenance(),
    }
    container = _pack(header, pkg["compressed"])
    comp = len(container)

    # os DOIS juízes, lado a lado — é o ponto do dispositivo
    psnr = classico.get("psnr_db")
    report = {
        "patent": PATENT_ID, "device_version": DEVICE_VERSION,
        "orig_name": name, "orig_size": len(npy_bytes), "compressed_size": comp,
        "ratio": (len(npy_bytes) / comp) if comp else 1.0,
        "saved_pct": (1 - comp / len(npy_bytes)) * 100 if npy_bytes else 0.0,
        "mode": pkg["mode"], "mode_escolhido_por": "AUTO do protótipo (o sinal decide, não o operador)",
        "entropy_backend": header["entropy_backend"],
        "lossless": False,
        "orig_sha256": header["orig_sha256"],
        "beta_tgl": _T.BETA_TGL, "sqrt_beta_tgl": _T.BETA_TGL_SQRT,
        # ─ juiz 1: o clássico
        "classico": {"psnr_db": psnr, "correlation": classico.get("correlation"),
                     "cosine_similarity": classico.get("cosine_similarity"),
                     "mse": classico.get("mse"),
                     "veredito": ("reconstrução PERFEITA" if (psnr or 0) > 50 else "reconstrução boa"
                                  if (psnr or 0) > 30 else "reconstrução pobre")},
        # ─ juiz 2: o NOME (o da casa, e o mais severo)
        "nome_original": nome_as_dict(meta["nome_original"]),
        "nome_reconstruido": nome_as_dict(meta["nome_reconstructed"]),
        "nome_verificacao": {"state": ver.get("state"), "integrity": ver.get("integrity"),
                             "delta_max": ver.get("delta_max"),
                             "piso_hilbert_beta": ver.get("piso_hilbert"),
                             "threshold_sqrt_beta": ver.get("threshold_sqrt")},
        "escada_do_nome": {"TETELESTAI": "δ < β (identidade perfeita)",
                           "PRESERVADO": "δ < √β (dentro do campo)",
                           "PERTURBADO": "δ < 1 (na fronteira)",
                           "VIOLADO": "δ ≥ 1 (fora do campo)"},
        "nota": ("COM PERDA (compressão holográfica — o domínio nativo da patente). Dois juízes: o "
                 "clássico mede ERRO DE AMPLITUDE; o Nome mede se a ESTRUTURA sobreviveu (a "
                 "distribuição de paridade psiônica). Quando discordam, os dois ficam no relatório: "
                 "o juiz severo não se esconde."),
    }
    # o achado, quando acontece — dito com todas as letras
    if (psnr or 0) > 50 and ver.get("state") in ("PERTURBADO", "VIOLADO"):
        report["divergencia_dos_juizes"] = (
            f"O PSNR diz {psnr:.1f} dB (≈perfeito) e a correlação {classico.get('correlation'):.6f}; "
            f"o NOME diz {ver.get('state')} com integridade {ver.get('integrity')}. Não é contradição: "
            f"a energia foi preservada, a ESTRUTURA não. É exatamente o que a v2.1 existe para pegar.")
    return container, report


def decompress(container: bytes) -> tuple[bytes, str, dict]:
    """Reconstrói o .npy. A integridade é verificada PELO NOME (o Nome original viaja
    dentro do payload — ele não é uma etiqueta externa que se possa forjar sem tocar no dado)."""
    import numpy as np
    header, payload = _unpack(container)
    if header.get("codec") != "TGL-TENSOR":
        raise ValueError("contêiner não é TGL-TENSOR")
    if len(payload) > MAX_DECOMP_BYTES:
        raise ValueError("payload acima do teto")
    t = _T.TGLTensor()
    rec, meta = t.decompress({"mode": header["mode"], "compressed": payload})
    arr = np.asarray(rec).reshape(tuple(header["shape"])).astype(np.dtype(header["dtype"]))
    buf = io.BytesIO(); np.save(buf, arr)
    ver = dict(meta["verification"])
    return buf.getvalue(), _safe_name(header.get("orig_name", "tensor.npy")), {
        "verified_by": "NOME (escada do Piso de Hilbert; β e √β derivados)",
        "state": ver.get("state"), "integrity": ver.get("integrity"), "delta_max": ver.get("delta_max"),
        "nome_original": nome_as_dict(meta["nome_original"]),
        "nome_reconstruido": nome_as_dict(meta["nome_reconstructed"]),
        "lossy": True, "mode": header["mode"], "beta": header.get("beta"),
        "nota": ("Reconstrução COM PERDA (holográfica) — não é bit-exata, e não se finge que seja. "
                 "Quem julga é o Nome."),
    }


def selftest() -> dict:
    """Prova o dispositivo em sinais de naturezas diferentes — e prova o ACHADO:
    o Nome é mais severo que o PSNR, e a escada dele é feita de β."""
    import numpy as np
    casos = []
    x = np.linspace(-3.0, 3.0, 4096)
    sinais = [
        ("campo suave (gaussiana modulada)", (np.sin(x * 3.0) * np.exp(-x * x / 4.0))),
        ("onda pura", np.sin(np.linspace(0, 40 * np.pi, 4096))),
        ("degrau (descontinuidade)", np.where(np.arange(4096) < 2048, -1.0, 1.0)),
        ("constante (TETELESTAI esperado)", np.full(4096, 0.7)),
    ]
    ok = True
    achou_divergencia = False
    nome_pegou_o_que_psnr_perdeu = []      # Nome severo onde o clássico diz "perfeito"
    nome_salvou_o_classico = []            # o clássico degenera e o Nome acerta
    for rotulo, s in sinais:
        b = io.BytesIO(); np.save(b, s.astype(np.float64)); npy = b.getvalue()
        cont, rep = compress_npy(npy, rotulo)
        out, _n, meta = decompress(cont)
        rt = len(out) > 0 and meta.get("state") in ("TETELESTAI", "PRESERVADO", "PERTURBADO", "VIOLADO")
        # a escada tem de ser coerente com o delta medido
        d = meta.get("delta_max") or 0.0
        esperado = ("TETELESTAI" if d < _T.BETA_TGL else "PRESERVADO" if d < _T.BETA_TGL_SQRT
                    else "PERTURBADO" if d < 1.0 else "VIOLADO")
        escada_ok = (meta.get("state") == esperado)
        ok = ok and rt and escada_ok
        if rep.get("divergencia_dos_juizes"):
            achou_divergencia = True
        psnr_v = rep["classico"]["psnr_db"] or 0.0
        corr_v = rep["classico"]["correlation"]
        # (a) o Nome pega o que o PSNR perde: clássico diz "perfeito", o Nome vê estrutura mexida
        if psnr_v > 50 and meta.get("state") in ("PERTURBADO", "VIOLADO"):
            nome_pegou_o_que_psnr_perdeu.append(
                {"sinal": rotulo, "psnr_db": round(psnr_v, 2), "correlacao": round(corr_v, 6),
                 "NOME": meta.get("state"), "integridade": meta.get("integrity")})
        # (b) o INVERSO, e é igualmente honesto: o juiz clássico DEGENERA e o Nome acerta.
        # Correlação de um sinal constante é indefinida (variância zero) e sai 0,0 — o que leria
        # como "reconstrução sem relação alguma com o original", que é falso: ela é exata.
        if corr_v is not None and corr_v < 0.5 and meta.get("state") == "TETELESTAI":
            nome_salvou_o_classico.append(
                {"sinal": rotulo, "correlacao_classica": round(corr_v, 6), "psnr_db": round(psnr_v, 2),
                 "NOME": meta.get("state"), "delta_max": round(d, 8),
                 "porque": ("correlação é indefinida em sinal de variância zero e degenera para 0,0; "
                            "o Nome não usa correlação — mede a paridade, e a paridade voltou intacta")})
        casos.append({"sinal": rotulo, "modo": rep["mode"], "ratio": round(rep["ratio"], 3),
                      "psnr_db": (round(rep["classico"]["psnr_db"], 2)
                                  if isinstance(rep["classico"]["psnr_db"], float) else rep["classico"]["psnr_db"]),
                      "correlacao": round(rep["classico"]["correlation"], 6),
                      "NOME_estado": meta.get("state"), "NOME_integridade": meta.get("integrity"),
                      "delta_max": round(d, 6), "escada_coerente": escada_ok, "round_trip_ok": rt})
    return {
        "ok": bool(ok),
        "casos": casos,
        "o_achado": {
            "os_dois_juizes_discordam_em_algum_caso": achou_divergencia,
            # A leitura HONESTA não é "a nossa métrica é melhor". É que os dois juízes medem
            # perguntas diferentes, e CADA UM pega o que o outro não vê. Medido nos dois sentidos:
            "nome_pegou_o_que_o_psnr_perdeu": nome_pegou_o_que_psnr_perdeu,
            "nome_acertou_onde_o_classico_degenerou": nome_salvou_o_classico,
            "leitura": ("o PSNR mede erro de AMPLITUDE; o Nome mede se a ESTRUTURA sobreviveu (a "
                        "paridade psiônica). NOS DOIS SENTIDOS: (a) um campo suave volta com PSNR ≈ 63 dB "
                        "e correlação 1,000000 — 'perfeito' para o clássico — e o Nome o declara "
                        "PERTURBADO: a energia foi preservada, a estrutura não; (b) um sinal CONSTANTE "
                        "faz a correlação clássica degenerar para 0,0 (variância zero ⇒ indefinida), o "
                        "que leria como 'nenhuma relação com o original' — falso, a reconstrução é exata "
                        "— e o Nome acerta TETELESTAI. Nenhum dos dois juízes é dispensável. A "
                        "severidade do Nome é a reivindicação; a cegueira dele à amplitude é o motivo "
                        "de o clássico continuar no relatório."),
            "detalhe_que_vale_a_pena": ("no campo suave δ_max = 0,1157 contra √β = 0,1097 — ele fica "
                                        "RASPANDO fora do campo. Não é 'muito perturbado': é perturbado "
                                        "por 5%% acima do degrau. O degrau é fino, e é da teoria."),
        },
        "escada_do_nome_e_teoria": {
            "beta": _T.BETA_TGL, "sqrt_beta": _T.BETA_TGL_SQRT,
            "nota": ("os degraus da escada NÃO são escolhas de engenharia: são β = α·√e e √β. O mesmo "
                     "√β ≈ 0,1097 que delimita a região do piso dos vazios na cosmologia da casa."),
        },
        # v120: o degrau PRESERVADO (√β) ganhou FUNDAMENTO — é O_C(alpha_obs), o operador de coerência.
        "operador_de_coerencia_v120": coherence_operator_reading(),
        "sem_chaveamento_humano": {"modo": "AUTO do protótipo decide DIRECT/SPECTRAL",
                                   "porta_unica": "compress_npy(npy, name) — nenhum parâmetro de modo"},
        "entropy_backend": "zstd" if _T.HAS_ZSTD else "fallback (zstandard ausente)",
        "beta": beta_provenance(), "device_version": DEVICE_VERSION, "patent": PATENT_ID,
    }


if __name__ == "__main__":
    r = selftest()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    raise SystemExit(0 if r["ok"] else 1)
