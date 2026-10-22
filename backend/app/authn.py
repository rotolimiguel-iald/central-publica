# -*- coding: utf-8 -*-
"""Autenticação da Central PELA CRIPTOGRAFIA DO OPERADOR (ACOM Crypto — Túnel de Hilbert).
Dogfooding: a patente BR102026003431-2 É a segurança da plataforma (não "outra segurança").

MULTI-USUÁRIO com PAPÉIS:
  • admin  — o operador (CENTRAL_CRYPTO_SECRET). Faz tudo + gerencia usuários.
  • editor — pode ALTERAR conteúdo (notas, reindex, compilar).
  • viewer — SOMENTE LEITURA.
O admin cadastra usuários pela página Usuários; o sistema gera uma CHAVE (mostrada uma vez)
para o admin entregar a quem quiser. Cada chave é verificada pelo Túnel de Hilbert (a cripto
do operador) como KDF, em tempo-constante. A chave de sessão nunca é transmitida; o token de
sessão é assinado por HMAC (a "AEAD padrão" que a própria patente manda usar).

Persistência: backend/data/users.json (disco persistente na nuvem; fora do git; o reindex NÃO
mexe nele). Ativa só com CENTRAL_AUTH=crypto + CENTRAL_CRYPTO_SECRET (env, NUNCA no repo);
fail-closed se pedir cripto sem o segredo. β nunca literal (α·√e em runtime, herdado do codec)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import importlib.util
import json
import os
import secrets
import sys
import time
from pathlib import Path
from types import ModuleType

from . import config as C

# ── carrega o dispositivo de cripto de DENTRO da pasta da patente (caminho fixo) ──
_CRYPTO_DIR = "BR102026003431-2_ACOM_CRYPTO"
_CRYPTO_CODEC = "acom_crypto_auth.py"

AUTH_MODE = os.environ.get("CENTRAL_AUTH", "").strip().lower()   # "" | "crypto"
SECRET = os.environ.get("CENTRAL_CRYPTO_SECRET", "")
# 21/09/2026 — prefixo __Host- (Secure, Path=/, sem Domain): um subdomínio irmão
# (demo.iald.ia.br, iald.ia.br — o mesmo "site", pois ia.br está na Public Suffix List) não
# consegue plantar/fixar este cookie. O nome antigo NÃO é mais lido (um novo login basta).
COOKIE = "__Host-central_session"
LEGACY_COOKIE = "central_session"
# As DUAS origens da Central na nuvem. SameSite=Strict NÃO separa subdomínios irmãos (mesmo
# "site"): quem separa é a checagem de Origin/Sec-Fetch-Site do portão (recusa_csrf, abaixo).
ORIGENS_PROPRIAS = ("https://central.iald.ia.br", "https://central-de-patentes.onrender.com")
# FAIL-CLOSED: pedir cripto SEM segredo NÃO pode subir aberto (defesa do deploy em nuvem).
if AUTH_MODE == "crypto" and not SECRET:
    raise RuntimeError(
        "CENTRAL_AUTH=crypto exige CENTRAL_CRYPTO_SECRET definido (o servidor recusa subir "
        "sem o segredo para não ficar aberto na internet).")
AUTH_ENABLED = (AUTH_MODE == "crypto" and bool(SECRET))
_LOGIN_TTL = int(os.environ.get("CENTRAL_AUTH_TTL", str(12 * 3600)) or "0")

# ── 2FA por e-mail (obrigatória p/ quem pode EDITAR: editor e admin) ──
EMAIL_2FA = (os.environ.get("CENTRAL_2FA", "").strip().lower() == "email")
ADMIN_EMAIL = os.environ.get("CENTRAL_ADMIN_EMAIL", "").strip()
SMTP_HOST = os.environ.get("CENTRAL_SMTP_HOST", "").strip()
SMTP_PORT = int(os.environ.get("CENTRAL_SMTP_PORT", "465") or "465")
SMTP_USER = os.environ.get("CENTRAL_SMTP_USER", "").strip()
SMTP_PASS = os.environ.get("CENTRAL_SMTP_PASS", "")
SMTP_FROM = os.environ.get("CENTRAL_SMTP_FROM", "").strip() or SMTP_USER
_OTP_TTL = 600          # 10 min
_OTP_MAX_TRIES = 5
_2FA: dict[str, dict] = {}   # challenge_id -> {uid,name,role,email,code_hash,exp,tries}

# /api/iald-sync/ não usa cookie: a própria rota se autentica por HMAC (fail-closed, 503 sem
# segredo) — ver iald_app_users.py.
_OPEN_PREFIXES = ("/api/auth/", "/api/health", "/api/acom/", "/api/iald-sync/")
USERS_FILE = C.DATA_DIR / "users.json"
ROLES = ("admin", "editor", "viewer")
_ADMIN = {"name": "operador", "uid": "operador", "role": "admin"}


def _load() -> ModuleType:
    path = C.PATENTS_DIR / _CRYPTO_DIR / "dispositivo" / _CRYPTO_CODEC
    spec = importlib.util.spec_from_file_location("_acom_crypto_auth", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não foi possível carregar {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_acom_crypto_auth"] = mod
    spec.loader.exec_module(mod)
    return mod


_M: ModuleType | None = None


def _mod() -> ModuleType:
    global _M
    if _M is None:
        _M = _load()
    return _M


_CANON_NONCE = b"central-de-patentes-login-v1"


def _verifier(key: str, uid: str) -> str:
    """Verificador da chave = Túnel de Hilbert(key, uid) em hex (a cripto do operador como KDF)."""
    m = _mod()
    return m.hilbert_tunnel_key(key.encode("utf-8"), _CANON_NONCE, uid.encode("utf-8"), m.SERVER_ID).hex()


# ── usuários (disco persistente) ─────────────────────────────────────────────
def _load_users() -> list[dict]:
    if not USERS_FILE.exists():
        return []
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8")).get("users", [])
    except Exception:
        return []


def _save_users(users: list[dict]) -> None:
    C.DATA_DIR.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps({"users": users}, ensure_ascii=False, indent=2), encoding="utf-8")


def _mask_email(email: str) -> str:
    if not email or "@" not in email:
        return "(sem e-mail)"
    a, b = email.split("@", 1)
    return (a[0] + "***" if len(a) > 1 else "***") + "@" + b


def list_users() -> list[dict]:
    """Lista pública (sem verificadores): o admin (operador) + os cadastrados."""
    out = [{"uid": "operador", "name": "operador", "role": "admin", "builtin": True,
            "email": _mask_email(ADMIN_EMAIL) if ADMIN_EMAIL else "(defina CENTRAL_ADMIN_EMAIL)",
            "created_at": None}]
    for u in _load_users():
        out.append({"uid": u["uid"], "name": u["name"], "role": u["role"], "builtin": False,
                    "email": _mask_email(u.get("email", "")), "created_at": u.get("created_at")})
    return out


def add_user(name: str, role: str, email: str = "") -> dict:
    """Cria um usuário com CHAVE aleatória forte. Devolve a chave UMA vez (o admin a entrega).
    E-mail é obrigatório para EDITOR (2FA); opcional para viewer."""
    name = (name or "").strip()[:60]
    email = (email or "").strip()[:120]
    if not name:
        raise ValueError("nome vazio")
    if role not in ("editor", "viewer"):
        raise ValueError("papel inválido (use editor ou viewer)")
    if role == "editor" and EMAIL_2FA and "@" not in email:
        raise ValueError("editor exige e-mail válido (para a autenticação dupla)")
    users = _load_users()
    if any(u["name"].lower() == name.lower() for u in users) or name.lower() == "operador":
        raise ValueError("já existe um usuário com esse nome")
    uid = "u_" + secrets.token_hex(6)
    key = secrets.token_urlsafe(18)                     # a chave que o admin entrega
    users.append({"uid": uid, "name": name, "role": role, "email": email,
                  "verifier": _verifier(key, uid), "created_at": int(time.time())})
    _save_users(users)
    return {"uid": uid, "name": name, "role": role, "email": email, "key": key}


def remove_user(uid: str) -> bool:
    users = _load_users()
    new = [u for u in users if u["uid"] != uid]
    if len(new) == len(users):
        return False
    _save_users(new)
    return True


def set_role(uid: str, role: str) -> bool:
    if role not in ("editor", "viewer"):
        raise ValueError("papel inválido")
    users = _load_users()
    hit = False
    for u in users:
        if u["uid"] == uid:
            u["role"] = role
            hit = True
    if hit:
        _save_users(users)
    return hit


# ── verificação de login: admin OU um usuário cadastrado (tempo-constante) ────
def verify_secret(submitted: str) -> dict | None:
    """Confere a chave submetida. Retorna {name, uid, role, email} do dono, ou None."""
    if not submitted:
        return None
    try:
        submitted.encode("utf-8")   # surrogate solto (JSON "\ud800") → recusa, não 500
    except UnicodeEncodeError:
        return None
    # 1) admin (operador)
    if hmac.compare_digest(_verifier(submitted, "operador"), _verifier(SECRET, "operador")):
        return {**_ADMIN, "email": ADMIN_EMAIL}
    # 2) usuários cadastrados
    for u in _load_users():
        if hmac.compare_digest(_verifier(submitted, u["uid"]), u["verifier"]):
            return {"name": u["name"], "uid": u["uid"], "role": u["role"], "email": u.get("email", "")}
    return None


# ── 2FA por e-mail ────────────────────────────────────────────────────────────
def needs_2fa(user: dict) -> bool:
    """Editor e admin (quem pode ALTERAR) exigem o código por e-mail; viewer não.
    ANTI-TRAVAMENTO: o admin (você) só é exigido quando o envio de e-mail está pronto —
    se o SMTP cair, o admin ainda entra (e conserta), mas o editor fica bloqueado até voltar."""
    if not EMAIL_2FA:
        return False
    role = user.get("role")
    if role == "editor":
        return True
    if role == "admin":
        return smtp_ready() and "@" in (user.get("email") or "")
    return False


def smtp_ready() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS and SMTP_FROM)


def _send_email(to: str, subject: str, body: str) -> None:
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg.set_content(body)
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)


def start_2fa(user: dict) -> dict:
    """Gera um código de 6 dígitos, envia ao e-mail do usuário e devolve o desafio."""
    email = user.get("email", "")
    if "@" not in email:
        raise ValueError("usuário sem e-mail cadastrado para a autenticação dupla")
    if not smtp_ready():
        raise RuntimeError("envio de e-mail não configurado (defina CENTRAL_SMTP_* no servidor)")
    code = f"{secrets.randbelow(1000000):06d}"
    challenge = secrets.token_urlsafe(18)
    _2FA[challenge] = {"uid": user["uid"], "name": user["name"], "role": user["role"],
                       "email": email, "code_hash": hashlib.sha256(code.encode()).hexdigest(),
                       "exp": time.time() + _OTP_TTL, "tries": 0}
    # poda desafios expirados
    for k in [k for k, v in _2FA.items() if v["exp"] < time.time()]:
        _2FA.pop(k, None)
    _send_email(email, "Central de Patentes — seu código de acesso",
                f"Olá, {user['name']}.\n\nSeu código de acesso à Central de Patentes é:\n\n"
                f"    {code}\n\nEle expira em 10 minutos. Se você não tentou entrar, ignore este e-mail.\n")
    return {"challenge": challenge, "email_hint": _mask_email(email)}


def verify_2fa(challenge: str, code: str) -> dict | None:
    """Confere o código do desafio. Retorna o usuário {name,uid,role} ou None."""
    ch = _2FA.get(challenge)
    if not ch:
        return None
    if time.time() > ch["exp"] or ch["tries"] >= _OTP_MAX_TRIES:
        _2FA.pop(challenge, None)
        return None
    ch["tries"] += 1
    if hmac.compare_digest(hashlib.sha256((code or "").encode()).hexdigest(), ch["code_hash"]):
        _2FA.pop(challenge, None)
        return {"name": ch["name"], "uid": ch["uid"], "role": ch["role"]}
    return None


# ── token de sessão (HMAC de servidor; payload carrega o papel) ──────────────
def _server_key() -> bytes:
    return hashlib.sha256(SECRET.encode("utf-8") + b"|central-server-hmac-key|").digest()


def issue(user: dict) -> dict:
    payload = {"sub": user["name"], "uid": user["uid"], "role": user["role"],
               "iat": int(time.time()), "exp": int(time.time()) + _LOGIN_TTL,
               "scheme": "acom-crypto-hilbert-tunnel"}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    sig = hmac.new(_server_key(), body, hashlib.sha256).hexdigest()
    return {"token": body.decode() + "." + sig, "role": user["role"], "name": user["name"],
            "expires_in": _LOGIN_TTL}


def token_payload(token: str) -> dict | None:
    """Valida o token e devolve o payload (com role/uid/sub) ou None."""
    if not token or "." not in token:
        return None
    try:
        body, sig = token.split(".", 1)
        if not hmac.compare_digest(hmac.new(_server_key(), body.encode(), hashlib.sha256).hexdigest(), sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
        if int(time.time()) > int(payload.get("exp", 0)):
            return None
        # o usuário ainda existe? (admin sempre; cadastrados devem constar)
        uid = payload.get("uid")
        if uid and uid != "operador" and not any(u["uid"] == uid for u in _load_users()):
            return None
        return payload
    except Exception:
        return None


def token_valid(token: str) -> bool:
    return token_payload(token) is not None


# ── papéis: o que cada um pode ──────────────────────────────────────────────
_MUTATING = ("POST", "PUT", "DELETE", "PATCH")
# rotas que MUTAM estado e exigem editor+ (viewer NÃO pode); device/auth são livres p/ todos
_VIEWER_ALLOWED_MUT_PREFIXES = ("/api/device/", "/api/auth/")
# só admin, INCLUSIVE para GET: gerência de usuários da Central, overlay de escrita da nuvem,
# usuários do app IALD (dados pessoais mascarados + comandos) e o log de auditoria.
_ADMIN_ONLY_PREFIXES = ("/api/users", "/api/cloud-writes", "/api/iald-app", "/api/audit")


def is_admin_only(path: str) -> bool:
    return any(path.startswith(p) for p in _ADMIN_ONLY_PREFIXES)


def can_request(payload: dict | None, method: str, path: str) -> bool:
    """Regra de papel para uma requisição já autenticada."""
    if payload is None:
        return False
    role = payload.get("role", "viewer")
    if any(path.startswith(p) for p in _ADMIN_ONLY_PREFIXES):
        return role == "admin"
    if method in _MUTATING and not any(path.startswith(p) for p in _VIEWER_ALLOWED_MUT_PREFIXES):
        return role in ("admin", "editor")     # viewer não muta conteúdo
    return True                                 # GET e device/auth: todos


# ── CSRF de subdomínio irmão (21/09/2026) ────────────────────────────────────
# ia.br está na Public Suffix List ⟹ central./demo./www.iald.ia.br e iald.ia.br são o MESMO
# site: o cookie SameSite=Strict VAI junto num POST disparado de um irmão. Todo navegador manda
# Origin em requisição não-GET (e os modernos, Sec-Fetch-Site). Então, com o login ligado:
#   • Sec-Fetch-Site presente e ≠ same-origin → recusa;
#   • Origin presente e fora das origens da Central → recusa;
#   • nenhum dos dois → cliente fora de navegador (ex.: tools/harvest_cloud.py) → segue para o
#     portão do cookie de sempre (não há navegador de vítima para forjar).
# Fora: /api/acom/* (o descompactador público, cross-origin por desenho, sem cookie) e
# /api/iald-sync/* (servidor→servidor, HMAC, sem cabeçalhos de navegador).
_CSRF_ISENTOS = ("/api/acom/", "/api/iald-sync/")


def recusa_csrf(method: str, path: str, headers) -> str | None:
    """None se a requisição pode seguir; senão o motivo (curto, sem eco do valor recebido)."""
    if method not in _MUTATING or not path.startswith("/api/") or path.startswith(_CSRF_ISENTOS):
        return None
    sfs = headers.get("sec-fetch-site")
    if sfs is not None and sfs != "same-origin":
        return "requisição de outro site recusada (Sec-Fetch-Site)"
    origem = headers.get("origin")
    if origem is not None and origem not in ORIGENS_PROPRIAS:
        return "origem não permitida"
    return None


def status() -> dict:
    return {"enabled": AUTH_ENABLED, "scheme": "acom-crypto-hilbert-tunnel",
            "patent": "BR102026003431-2",
            "email_2fa": EMAIL_2FA, "smtp_ready": smtp_ready(),
            "beta": (_mod().beta_provenance() if AUTH_ENABLED else None)}


# ── rate-limit de tentativas de login (anti-força-bruta) ─────────────────────
_ATTEMPTS: dict[str, list[float]] = {}
_MAX_ATTEMPTS = 8
_WINDOW = 300.0


def rate_ok(ip: str) -> bool:
    now = time.time()
    xs = [t for t in _ATTEMPTS.get(ip, []) if now - t < _WINDOW]
    _ATTEMPTS[ip] = xs
    if len(_ATTEMPTS) > 4096:
        _ATTEMPTS.clear()
    return len(xs) < _MAX_ATTEMPTS


def note_attempt(ip: str) -> None:
    _ATTEMPTS.setdefault(ip, []).append(time.time())


def is_open_path(path: str) -> bool:
    if any(path.startswith(p) for p in _OPEN_PREFIXES):
        return True
    return not path.startswith("/api/")
