# -*- coding: utf-8 -*-
"""Blindagem da Central (Fase A) — controle remoto SEGURO pelo iald.ia.br.

DOIS MODOS (via env CENTRAL_MODE):
  * local  (padrao): comportamento de hoje — 127.0.0.1, sem auth, CORS aberto. Zero friccao
    para desenvolver em casa. NENHUMA chamada externa.
  * access (opt-in): a Central so' responde a quem passou pelo PASSKEY do Cloudflare Access.
    Cada request carrega o JWT `Cf-Access-Jwt-Assertion` (injetado pela borda do Cloudflare);
    aqui validamos assinatura (RS256 via JWKS do seu time), audience (AUD do app) e emissor,
    e opcionalmente restringimos a e-mails permitidos. Defense-in-depth: mesmo que a porta
    8765 fosse alcancada por fora do tunel, sem JWT valido -> 403.

Alem disso (nos dois modos remotos): headers de seguranca, CORS restrito ao dominio da Central,
e rate-limit por IP. NUNCA serve arquivos confidenciais (reforco do guard ja existente).

Variaveis de ambiente:
  CENTRAL_MODE=local|access                 (default local)
  CF_ACCESS_TEAM_DOMAIN=https://<time>.cloudflareaccess.com
  CF_ACCESS_AUD=<AUD tag do app Access>
  CENTRAL_ALLOWED_EMAILS=voce@dominio,...   (vazio = qualquer identidade que o Access liberou)
  CENTRAL_CORS_ORIGIN=https://central.iald.ia.br   (default * em local)
  CENTRAL_RATE_MAX=120                       (req/min por IP; 0 = sem limite)
"""
import os
import json
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

_AUDIT_PATH = Path(__file__).resolve().parent.parent / "data" / "audit.log"
_AUDIT_LOCK = threading.Lock()
_AUDIT_SKIP = ("/api/health", "/api/whoami", "/api/audit")   # ruido de polling da UI
_AUDIT_SKIP_OK_PREFIX = "/api/iald-sync/"                     # so' as FALHAS entram no log geral
_AUDIT_MAX_LINES = 20000

MODE = os.environ.get("CENTRAL_MODE", "local").strip().lower()
CF_TEAM = os.environ.get("CF_ACCESS_TEAM_DOMAIN", "").strip().rstrip("/")
CF_AUD = os.environ.get("CF_ACCESS_AUD", "").strip()
ALLOWED_EMAILS = {e.strip().lower() for e in os.environ.get("CENTRAL_ALLOWED_EMAILS", "").split(",") if e.strip()}
CORS_ORIGIN = os.environ.get("CENTRAL_CORS_ORIGIN", "" if MODE == "access" else "*").strip()
RATE_MAX = int(os.environ.get("CENTRAL_RATE_MAX", "120") or "0")

IS_ACCESS = (MODE == "access")
# quando a AUTENTICACAO e' a criptografia do operador (ACOM Crypto), ELA gateia /api/*; o guard
# de borda do modo local nao deve rejeitar (na nuvem/Render o trafego chega com cabecalhos cf-*).
CRYPTO_AUTH = (os.environ.get("CENTRAL_AUTH", "").strip().lower() == "crypto")

# ------------------------------------------------------------------ Cloudflare Access JWT
_jwk_client = None
_jwk_lock = threading.Lock()


def _jwks():
    """PyJWKClient para os certs do time Cloudflare Access. Busca/caso sob demanda (so' em
    modo access). Uma chamada de rede ao SEU provedor de auth — nunca em modo local."""
    global _jwk_client
    if _jwk_client is None:
        with _jwk_lock:
            if _jwk_client is None:
                from jwt import PyJWKClient
                _jwk_client = PyJWKClient(f"{CF_TEAM}/cdn-cgi/access/certs")
    return _jwk_client


def verify_access_jwt(token: str) -> dict:
    """Valida o JWT do Cloudflare Access. Levanta em qualquer falha (fail-closed)."""
    import jwt
    signing_key = _jwks().get_signing_key_from_jwt(token).key
    claims = jwt.decode(token, signing_key, algorithms=["RS256"],
                        audience=CF_AUD, issuer=CF_TEAM,
                        options={"require": ["exp", "iat", "aud", "iss"]})
    email = (claims.get("email") or claims.get("identity") or "").lower()
    if ALLOWED_EMAILS and email not in ALLOWED_EMAILS:
        raise PermissionError(f"identidade nao autorizada: {email or '(sem email)'}")
    return {"email": email, "sub": claims.get("sub"), "exp": claims.get("exp")}


def _extract_token(request) -> str:
    tok = request.headers.get("cf-access-jwt-assertion")
    if tok:
        return tok
    return request.cookies.get("CF_Authorization", "")


def identity_of(request):
    """Identidade autenticada (dict) ou None. Em modo local devolve um usuario local."""
    if not IS_ACCESS:
        return {"email": "local", "sub": "local", "mode": "local"}
    tok = _extract_token(request)
    if not tok:
        return None
    try:
        ident = verify_access_jwt(tok)
        ident["mode"] = "access"
        return ident
    except Exception:
        return None


# ------------------------------------------------------------------ middlewares
# Quem pode embutir a Central num iframe: ela mesma + a Lar Miguel local.
FRAME_CSP = "frame-ancestors 'self' http://127.0.0.1:8900 http://localhost:8900;"

HSTS = "max-age=31536000; includeSubDomains"
# 21/09/2026 — CSP ESTRITA da casca do app quando o LOGIN DA CENTRAL esta' ativo (nuvem/Render):
# sem script inline, sem terceiros, sem ser embutida. style-src sem 'unsafe-inline': React e
# three aplicam estilo por CSSOM (el.style.x / cssText), que a CSP nao bloqueia. UM <style> e'
# injetado: o OpenSeadragon 6.0.2 poe no <head> o CSS "mobile" (data-openseadragon-mobile-css,
# tira o contorno de foco em telas de toque). Ele entra pelo HASH abaixo — o texto e' uma
# concatenacao de literais no fonte do OSD, logo identico em dev e no bundle; ao atualizar o
# OpenSeadragon, recalcule (o teste test_iald_app_users.auth_csp_hash_do_openseadragon confere
# contra node_modules). Sem o hash so' aquele contorno some (cosmetico). img-src inclui blob:
# porque o OpenSeadragon 6 converte tiles em blob (caminho rasterBlob do bundle).
OSD_MOBILE_CSS_HASH = "'sha256-9xTiqzfwFaL2SGb1rmr8gysEwVVjIvqWAgmZgqFqpEE='"
STRICT_APP_CSP = ("default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; "
                  "frame-ancestors 'none'; form-action 'self'; img-src 'self' data: blob:; "
                  f"style-src 'self' {OSD_MOBILE_CSS_HASH}; connect-src 'self'")

# O sandbox dos arquivos do acervo so' vale onde ha' privilegio a proteger: a Central na nuvem
# (login pela cripto) ou atras do Cloudflare Access. A Central LOCAL (127.0.0.1, sem login) segue
# como sempre — os painéis HTML do acervo rodam em casa como antes.
SANDBOX_ARQUIVOS = CRYPTO_AUTH or IS_ACCESS


def precisa_sandbox(tipo: str | None) -> bool:
    """Tipos que NAO executam script ficam fora do sandbox: PDF (visor isolado do navegador),
    imagem raster, video e audio. O sandbox (origem opaca) quebraria o video — o documento de
    midia passa a pedir o proprio arquivo como outra origem e o CORS o barra. SVG e' imagem
    que roda script: fica DENTRO. Tipo desconhecido tambem fica dentro."""
    t = (tipo or "").lower()
    if t == "application/pdf":
        return False
    if t.startswith(("video/", "audio/")):
        return False
    if t.startswith("image/") and t != "image/svg+xml":
        return False
    return True


def sandbox_csp() -> str:
    """CSP para arquivos do acervo servidos na origem da Central (ex.: HTML guardado): o
    'sandbox' sem allow-scripts/allow-same-origin impede que o arquivo rode script com os
    privilegios do cockpit. A rota que a declara tem a CSP PRESERVADA pelo middleware."""
    ancestors = "frame-ancestors 'none'" if CRYPTO_AUTH else FRAME_CSP.rstrip(";")
    return ("sandbox; default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
            "font-src 'self' data:; media-src 'self'; " + ancestors)


def _has_sandbox(csp: str) -> bool:
    return any(d.strip().split(" ", 1)[0].lower() == "sandbox" for d in (csp or "").split(";"))


def apply_security_headers(resp):
    """Aplica os cabecalhos de seguranca. Usado pelo middleware E pelas recusas do portao da
    cripto (que ficam FORA do middleware e antes saiam sem nenhum destes cabecalhos)."""
    rota_csp = resp.headers.get("Content-Security-Policy", "")
    keep = _has_sandbox(rota_csp)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    # ANEXO LAR MIGUEL (19/08/2026): o cockpit local (127.0.0.1:8900) precisa
    # EMBUTIR esta Central lado a lado com as outras casas. frame-ancestors da CSP
    # substitui o X-Frame-Options nos navegadores modernos e e' mais granular: so a
    # Lar Miguel local pode embutir; qualquer site externo continua BLOQUEADO.
    resp.headers["Content-Security-Policy"] = rota_csp if keep else FRAME_CSP
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if CRYPTO_AUTH:
        # nuvem com o login da Central: HSTS + CSP estrita (a Lar Miguel embute so' a local)
        resp.headers["Strict-Transport-Security"] = HSTS
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Content-Security-Policy"] = rota_csp if keep else STRICT_APP_CSP
    elif IS_ACCESS:
        resp.headers["Strict-Transport-Security"] = HSTS
        # CSP: a SPA e' self-hosted (bundle com hash); nada de terceiros.
        resp.headers["Content-Security-Policy"] = rota_csp if keep else (
            "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; connect-src 'self'; " + FRAME_CSP + " base-uri 'self'")
    return resp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        resp = await call_next(request)
        return apply_security_headers(resp)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_per_min: int):
        super().__init__(app)
        self.max = max_per_min
        self.hits = defaultdict(deque)
        self.lock = threading.Lock()

    async def dispatch(self, request, call_next):
        if self.max <= 0:
            return await call_next(request)
        ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
        now = time.time()
        with self.lock:
            dq = self.hits[ip]
            while dq and dq[0] < now - 60:
                dq.popleft()
            if len(dq) >= self.max:
                return JSONResponse({"detail": "rate limit"}, status_code=429)
            dq.append(now)
            # evita crescimento ilimitado do dict (memory DoS por IPs distintos): poda IPs ociosos
            if len(self.hits) > 4096:
                for k in [k for k, v in self.hits.items() if not v or v[-1] < now - 120]:
                    del self.hits[k]
        return await call_next(request)


def _audit_write(entry: dict):
    try:
        _AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _AUDIT_LOCK:
            with open(_AUDIT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            # rotacao simples: se passar do teto, mantem a metade mais recente
            try:
                if _AUDIT_PATH.stat().st_size > 4_000_000:
                    lines = _AUDIT_PATH.read_text(encoding="utf-8").splitlines()
                    _AUDIT_PATH.write_text("\n".join(lines[-_AUDIT_MAX_LINES // 2:]) + "\n",
                                           encoding="utf-8")
            except Exception:
                pass
    except Exception:
        pass


class _Estrangulador:
    """No maximo UMA linha de log por chave a cada `janela` s; as repeticoes sao CONTADAS e o
    total sai na proxima linha daquela chave ("suprimidas"). As chaves nao levam IP (o IP e'
    forjavel fora do Cloudflare): cardinalidade limitada a caminho x status x ator."""

    def __init__(self, janela: float = 60.0, teto: int = 4096):
        self.janela, self.teto = janela, teto
        self.mapa: dict = {}          # chave -> [ts da ultima linha, suprimidas desde entao]
        self.descartadas = 0          # linhas perdidas com o mapa cheio (vao na proxima linha)
        self.lock = threading.Lock()

    def passa(self, chave, agora: float | None = None) -> tuple[bool, int]:
        agora = time.time() if agora is None else agora
        with self.lock:
            ent = self.mapa.get(chave)
            if ent is not None and agora - ent[0] < self.janela:
                ent[1] += 1
                return False, 0
            if ent is None and len(self.mapa) >= self.teto:
                for k in [k for k, v in self.mapa.items() if agora - v[0] >= self.janela and not v[1]]:
                    del self.mapa[k]
                if len(self.mapa) >= self.teto:
                    self.descartadas += 1
                    return False, 0
            suprimidas = (ent[1] if ent else 0) + self.descartadas
            self.descartadas = 0
            self.mapa[chave] = [agora, 0]
            return True, suprimidas


_ESTRANGULA = _Estrangulador()


def _ip_de(request) -> str:
    return request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")


def audit_negado(request, status: int, motivo: str, payload: dict | None, chave: str) -> None:
    """Recusa do PORTAO da cripto (que fica FORA do AuditMiddleware) no log geral, com o ator
    tirado do token quando houver. Estrangulada por (chave, status, ator)."""
    uid = (payload or {}).get("uid") if isinstance(payload, dict) else None
    papel = (payload or {}).get("role") if isinstance(payload, dict) else None
    passa, suprimidas = _ESTRANGULA.passa(("negado", chave, status, uid or "-"))
    if not passa:
        return
    e = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "email": f"{uid} ({papel})" if uid else "(sem sessão)", "uid": uid, "papel": papel,
         "method": request.method, "path": request.url.path, "status": status,
         "ip": _ip_de(request), "mode": MODE, "motivo": motivo, "origem": "portao"}
    if suprimidas:
        e["suprimidas"] = suprimidas
    _audit_write(e)


def read_audit(n: int = 200) -> list:
    try:
        lines = _AUDIT_PATH.read_text(encoding="utf-8").splitlines()
        return [json.loads(x) for x in lines[-n:] if x.strip()][::-1]
    except Exception:
        return []


class AuditMiddleware(BaseHTTPMiddleware):
    """Log append-only de ACESSOS a /api (quem entrou, quando, o quê, resultado). Fica FORA do
    guard para registrar tambem tentativas NEGADAS (403). Nao loga polling da UI (health/whoami)."""
    async def dispatch(self, request, call_next):
        resp = await call_next(request)
        path = request.url.path
        # a sincronizacao da IALD (poll a cada poucos segundos) so' entra aqui quando FALHA;
        # o sucesso fica na trilha propria (backend/data/iald_app/auditoria.jsonl). As falhas
        # sao ESTRANGULADAS (1 linha/min por status, com a contagem das suprimidas): a rota e'
        # aberta, e sem isto qualquer um encheria o log geral de "assinatura invalida".
        suprimidas = 0
        if path.startswith(_AUDIT_SKIP_OK_PREFIX):
            if resp.status_code == 200:
                return resp
            passa, suprimidas = _ESTRANGULA.passa(("sync", path, resp.status_code))
            if not passa:
                return resp
        if path.startswith("/api/") and path not in _AUDIT_SKIP:
            # com o login da Central, o portao da cripto poe em request.state.identity o ator
            # do TOKEN (uid + papel); sem ele, identity_of devolve "local"/Access como antes.
            ident = getattr(request.state, "identity", None) or identity_of(request)
            email = (ident or {}).get("email") if ident else None
            e = {
                "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "email": email or ("(negado)" if resp.status_code in (401, 403) else "(anon)"),
                "method": request.method, "path": path, "status": resp.status_code,
                "ip": _ip_de(request), "mode": MODE,
            }
            if suprimidas:
                e["suprimidas"] = suprimidas
            _audit_write(e)
        return resp


class AccessGuardMiddleware(BaseHTTPMiddleware):
    """Em modo access: /api/* exige JWT valido do Cloudflare Access (passkey). O restante
    (SPA estatica) tambem so' e' util apos o Access na borda, mas a API e' o que carrega dados."""
    async def dispatch(self, request, call_next):
        h = request.headers
        # trafego que passou pela BORDA do Cloudflare (tunel) sempre carrega estes cabecalhos,
        # adicionados pelo edge e NAO forjaveis pelo cliente. Sua ausencia => acesso DIRETO local.
        is_edge = bool(h.get("cf-ray") or h.get("cf-access-jwt-assertion") or h.get("cf-connecting-ip"))
        if not IS_ACCESS:
            # modo LOCAL: rejeita tráfego de borda (tunel apontando p/ instancia sem auth);
            # acesso direto em 127.0.0.1 (voce em casa) segue livre.
            # EXCECAO: se a cripto do operador esta' ativa (nuvem/Render), ELA e' o portao ->
            # deixa passar (o middleware crypto_auth_gate exige o login por Tunel de Hilbert).
            if is_edge and not CRYPTO_AUTH:
                return JSONResponse(
                    {"detail": "Central em modo LOCAL nao aceita trafego de borda; ative CENTRAL_MODE=access"},
                    status_code=403)
            return await call_next(request)
        # modo ACCESS:
        if request.method != "OPTIONS" and request.url.path.startswith("/api/"):
            if is_edge:
                # veio pelo tunel do Cloudflare -> EXIGE o JWT do Access (passkey)
                ident = identity_of(request)
                if ident is None:
                    return JSONResponse(
                        {"detail": "nao autenticado (Cloudflare Access / passkey requerido)"},
                        status_code=403)
                request.state.identity = ident
            else:
                # acesso DIRETO em 127.0.0.1 (voce na propria maquina) -> livre, sem passkey
                request.state.identity = {"email": "local-direto", "sub": "local", "mode": "access-local"}
        return await call_next(request)


def install_security(app):
    """Instala a blindagem. O ULTIMO add_middleware fica MAIS EXTERNO (roda 1o na requisicao,
    por ultimo na resposta). Queremos: SecurityHeaders o mais externo (poe headers em TODO
    response, ate' 403/429) -> rate-limit (rejeita cedo) -> guard (proximo da rota)."""
    app.add_middleware(AccessGuardMiddleware)
    if RATE_MAX > 0:
        app.add_middleware(RateLimitMiddleware, max_per_min=RATE_MAX)
    app.add_middleware(AuditMiddleware)          # fora do guard: registra ate' 403 negados
    app.add_middleware(SecurityHeadersMiddleware)  # o mais externo: headers em todo response


def summary() -> dict:
    return {"mode": MODE, "access_enabled": IS_ACCESS,
            "cors_origin": CORS_ORIGIN or "(nenhum)",
            "team_domain_set": bool(CF_TEAM), "aud_set": bool(CF_AUD),
            "allowed_emails": sorted(ALLOWED_EMAILS) if ALLOWED_EMAILS else "qualquer-do-access",
            "rate_max_per_min": RATE_MAX}
