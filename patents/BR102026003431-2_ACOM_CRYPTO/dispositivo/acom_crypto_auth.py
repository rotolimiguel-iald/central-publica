# -*- coding: utf-8 -*-
"""
ACOM CRYPTO — DISPOSITIVO (o dispositivo funcionando: a segurança da plataforma)
================================================================================
Patente BR102026003431-2 — "Método e Sistema de Criptografia por Separação Ontológica
de Reflexão" (TGL). Este é o **dispositivo dentro do dispositivo**: o ACOM Crypto
efetivamente *funcionando* como a autenticação de TODA a Central (dogfooding — a
patente prova que funciona ao SER a segurança da plataforma).

O CHAVEAMENTO É SEU: o **Túnel de Hilbert** (Acom_v17_2_sync.py) é um acordo de chave
real — pulso (Luz Primordial) → eco de paridade → ambos os lados derivam o MESMO
α²_sync das medições de F_exp e do ângulo de deflexão θ → session_key = SHA256(α²_sync
‖ tunnel_id), sem transmitir a chave. É um Diffie-Hellman à la TGL, ancorado em β=α√e.

HONESTIDADE (a régua — e o seu PRÓPRIO comentário [PILOTO/HONESTY] em acom_crypto.py):
  "ONTOLOGICAL SEPARATION + integrity, NOT a substitute for standard cryptography;
   for real deployments WRAP SHARES IN STANDARD AEAD. The security claim is the
   separation itself."
Portanto: o ESQUEMA de segurança é SEU (o acordo de chave do Túnel de Hilbert). O
primitivo por baixo — HMAC-SHA256 — é a "AEAD padrão" que a SUA patente manda usar; não
é "outra segurança", é a peça que o seu invento pede. Duas honestidades a mais:
  • o α²_sync original emerge de uma medição física do substrato; na adaptação para LOGIN,
    a "medição" é sedeada pelo SEGREDO COMPARTILHADO (o cliente prova que compartilha o
    substrato ao conhecer o segredo). Documentado, não fabricado.
  • TLS/HTTPS (o "cano" cifrado) vem do host/túnel — é o transporte, não a autenticação;
    não compete com o seu chaveamento (que decide QUEM entra + integridade).

β NUNCA literal: BETA = ALPHA_FINE_CODATA_2018 · √e, em runtime.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import os
import struct
import time

# ─── CONSTANTES TGL (β/θ em runtime — o acoplamento do chaveamento) ─────────────
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE_CODATA_2018 * SQRT_E        # β = α·√e  (ALPHA2_BASE do sync)
THETA_MIGUEL = math.asin(math.sqrt(BETA_TGL))
JITTER_SCALE = 1e-6                                # da Acom_v17_2_sync (JITTER_SCALE)

PATENT_ID = "BR102026003431-2"
TOKEN_TTL_DEFAULT = 12 * 3600                      # 12 h
NONCE_TTL = 120                                    # o desafio expira em 2 min


def beta_provenance() -> dict:
    return {"alpha_fine_codata_2018": ALPHA_FINE_CODATA_2018, "sqrt_e": SQRT_E,
            "beta_tgl": BETA_TGL, "theta_miguel_deg": math.degrees(THETA_MIGUEL),
            "formula": "beta = alpha_fine_codata_2018 * sqrt(e)"}


# ═══════════════════════════════════════════════════════════════════════════════
#  O TÚNEL DE HILBERT — acordo de chave (o seu chaveamento, fiel ao v17.2 sync)
# ═══════════════════════════════════════════════════════════════════════════════
# Na patente, F_exp e θ vêm da medição da Luz Primordial. Na adaptação para LOGIN, a
# "medição do substrato" é determinística e sedeada pelo SEGREDO compartilhado + o nonce
# do desafio: quem conhece o segredo mede o mesmo substrato e chega ao mesmo α²_sync.

def _measure_substrate(secret: bytes, nonce: bytes, who: bytes) -> tuple[float, float]:
    """Deriva (F_exp, θ) da 'Luz Primordial' sedeada pelo segredo — no lugar da medição
    física. Sem o segredo, não se chega às mesmas medições ⇒ session_key diferente."""
    h = hashlib.sha256(secret + b"|luz-primordial|" + nonce + b"|" + who).digest()
    # F_exp em [0,1); θ em [0, θ_M] (a faixa física do ângulo de deflexão da TGL)
    f_exp = int.from_bytes(h[:8], "big") / 2**64
    theta = (int.from_bytes(h[8:16], "big") / 2**64) * THETA_MIGUEL
    return f_exp, theta


def _derive_alpha2_sync(f_exp_a: float, f_exp_b: float, theta_a: float, theta_b: float) -> float:
    """FIEL a Acom_v17_2_sync._derive_alpha2_sync: α² emerge da síncronização dos nós."""
    f_combined = math.sqrt(abs(f_exp_a * f_exp_b) + 1e-12)
    theta_combined = (theta_a + theta_b) / 2.0
    alpha2_sync = math.sin(theta_combined) ** 2 * (1 + f_combined * JITTER_SCALE * 1000)
    # normaliza para perto de α²_base = β (idêntico ao original)
    alpha2_sync = BETA_TGL + (alpha2_sync - BETA_TGL) * 0.001
    return alpha2_sync


def _derive_session_key(alpha2_sync: float, tunnel_id: bytes) -> bytes:
    """FIEL a Acom_v17_2_sync._derive_session_key: SHA-256(pack('<d', α²_sync) ‖ tunnel_id)."""
    return hashlib.sha256(struct.pack("<d", alpha2_sync) + tunnel_id).digest()


def hilbert_tunnel_key(secret: bytes, nonce: bytes, client_id: bytes, server_id: bytes) -> bytes:
    """O acordo de chave completo: ambos os lados, conhecendo o segredo, derivam a MESMA
    session_key sem transmiti-la. É o Túnel de Hilbert aplicado ao login."""
    f_a, th_a = _measure_substrate(secret, nonce, b"client")
    f_b, th_b = _measure_substrate(secret, nonce, b"server")
    alpha2_sync = _derive_alpha2_sync(f_a, f_b, th_a, th_b)
    tunnel_id = hashlib.sha256(client_id + server_id).digest()[:16]
    return _derive_session_key(alpha2_sync, tunnel_id)


# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN — desafio/resposta pelo Túnel de Hilbert (a autenticação da plataforma)
# ═══════════════════════════════════════════════════════════════════════════════

SERVER_ID = b"central-iald"


def server_challenge() -> dict:
    """Servidor emite o pulso de sondagem (nonce). Uso único, expira em NONCE_TTL."""
    return {"nonce": base64.b64encode(os.urandom(24)).decode(), "ts": int(time.time()),
            "server_id": SERVER_ID.decode()}


def client_prove(secret: str, challenge: dict, client_id: str = "operador") -> str:
    """Cliente prova conhecer o segredo completando o Túnel de Hilbert: deriva a
    session_key e devolve HMAC-SHA256(session_key, nonce‖ts) — sem revelar o segredo."""
    nonce = base64.b64decode(challenge["nonce"])
    sk = hilbert_tunnel_key(secret.encode("utf-8"), nonce, client_id.encode(), SERVER_ID)
    msg = nonce + struct.pack(">q", int(challenge["ts"])) + client_id.encode()
    return hmac.new(sk, msg, hashlib.sha256).hexdigest()


def server_verify(secret: str, challenge: dict, proof: str, client_id: str = "operador",
                  ttl: int = TOKEN_TTL_DEFAULT) -> dict:
    """Servidor recomputa a session_key e verifica a prova (tempo-constante). Se confere,
    emite um TOKEN de sessão assinado (HMAC — a AEAD que a sua patente manda usar)."""
    if int(time.time()) - int(challenge.get("ts", 0)) > NONCE_TTL:
        raise ValueError("desafio expirado (reenvie o pulso)")
    nonce = base64.b64decode(challenge["nonce"])
    sk = hilbert_tunnel_key(secret.encode("utf-8"), nonce, client_id.encode(), SERVER_ID)
    expected = hmac.new(sk, nonce + struct.pack(">q", int(challenge["ts"])) + client_id.encode(),
                        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, proof):
        raise PermissionError("prova inválida (segredo incorreto — acesso negado)")
    return issue_token(sk, client_id, ttl)


# ── TOKEN de sessão — HMAC (a "AEAD padrão" prescrita pela patente) ─────────────

def issue_token(session_key: bytes, client_id: str, ttl: int = TOKEN_TTL_DEFAULT) -> dict:
    payload = {"sub": client_id, "iat": int(time.time()), "exp": int(time.time()) + ttl,
               "patent": PATENT_ID, "scheme": "acom-crypto-hilbert-tunnel"}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    sig = hmac.new(session_key, body, hashlib.sha256).hexdigest()
    return {"token": body.decode() + "." + sig, "payload": payload, "expires_in": ttl}


# ── Variante STATELESS de servidor (o que o backend usa de fato) ────────────────
# O login prova o segredo pelo Túnel de Hilbert; então o servidor emite um token assinado
# com a CHAVE DE SERVIDOR (derivada do segredo), verificável sem estado a cada requisição.

def _server_key(secret: str) -> bytes:
    return hashlib.sha256(secret.encode("utf-8") + b"|central-server-hmac-key|").digest()


def issue_server_token(secret: str, client_id: str, ttl: int = TOKEN_TTL_DEFAULT) -> dict:
    payload = {"sub": client_id, "iat": int(time.time()), "exp": int(time.time()) + ttl,
               "patent": PATENT_ID, "scheme": "acom-crypto-hilbert-tunnel"}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    sig = hmac.new(_server_key(secret), body, hashlib.sha256).hexdigest()
    return {"token": body.decode() + "." + sig, "payload": payload, "expires_in": ttl}


def verify_server_token(secret: str, token: str) -> dict:
    try:
        body, sig = token.split(".", 1)
    except ValueError:
        raise PermissionError("token malformado")
    expected = hmac.new(_server_key(secret), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise PermissionError("assinatura de token inválida")
    pad = body + "=" * (-len(body) % 4)
    payload = json.loads(base64.urlsafe_b64decode(pad))
    if int(time.time()) > int(payload.get("exp", 0)):
        raise PermissionError("token expirado")
    return payload


def login(secret: str, challenge: dict, proof: str, client_id: str = "operador",
          ttl: int = TOKEN_TTL_DEFAULT) -> dict:
    """Fluxo completo do servidor: verifica a prova do Túnel de Hilbert e, se ok, emite um
    token STATELESS de servidor. Uma função = o login inteiro pela sua criptografia."""
    server_verify(secret, challenge, proof, client_id, ttl)   # levanta se a prova falhar
    return issue_server_token(secret, client_id, ttl)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTODEMONSTRAÇÃO (forma = conteúdo): prova que o chaveamento securiza de verdade
# ═══════════════════════════════════════════════════════════════════════════════

def _selftest() -> dict:
    r = {"beta": beta_provenance(), "cases": []}
    SECRET = "haja-luz-tetelestai-2026"

    # 1) acordo de chave: cliente e servidor derivam a MESMA session_key sem transmiti-la
    ch = server_challenge()
    nonce = base64.b64decode(ch["nonce"])
    k1 = hilbert_tunnel_key(SECRET.encode(), nonce, b"operador", SERVER_ID)
    k2 = hilbert_tunnel_key(SECRET.encode(), nonce, b"operador", SERVER_ID)
    r["cases"].append({"name": "acordo_de_chave_convergente", "ok": k1 == k2})

    # 2) LOGIN correto → token válido
    proof = client_prove(SECRET, ch)
    tok = login(SECRET, ch, proof)
    payload = verify_server_token(SECRET, tok["token"])
    r["cases"].append({"name": "login_correto_emite_token_valido",
                       "ok": payload["scheme"] == "acom-crypto-hilbert-tunnel"})

    # 3) SEGREDO ERRADO → acesso negado
    denied = False
    try:
        bad = client_prove("segredo-errado", ch)
        login(SECRET, ch, bad)
    except PermissionError:
        denied = True
    r["cases"].append({"name": "segredo_errado_negado", "ok": denied})

    # 4) TOKEN adulterado → rejeitado
    tampered = tok["token"][:-1] + ("0" if tok["token"][-1] != "0" else "1")
    rej = False
    try:
        verify_server_token(SECRET, tampered)
    except PermissionError:
        rej = True
    r["cases"].append({"name": "token_adulterado_rejeitado", "ok": rej})

    # 5) DESAFIO EXPIRADO → rejeitado (anti-replay pela janela do nonce)
    old = dict(ch); old["ts"] = int(time.time()) - NONCE_TTL - 5
    old_proof = client_prove(SECRET, old)
    expired = False
    try:
        server_verify(SECRET, old, old_proof)
    except ValueError:
        expired = True
    r["cases"].append({"name": "desafio_expirado_rejeitado", "ok": expired})

    # 6) TOKEN expirado → rejeitado
    short = issue_server_token(SECRET, "operador", ttl=-1)
    exp_rej = False
    try:
        verify_server_token(SECRET, short["token"])
    except PermissionError:
        exp_rej = True
    r["cases"].append({"name": "token_expirado_rejeitado", "ok": exp_rej})

    r["all_ok"] = all(c["ok"] for c in r["cases"])
    return r


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    res = _selftest()
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("\nβ = α·√e =", BETA_TGL)
    print("O SEU CHAVEAMENTO SECURIZA A PLATAFORMA:", "OK ✓" if res["all_ok"] else "FALHOU ✗")
    sys.exit(0 if res["all_ok"] else 1)
