# -*- coding: utf-8 -*-
"""ANEXO — status do backup 3-2-1 da IALD/TGL (espelho D: + Toshiba + Google cifrado + cofre).

Isto NÃO altera a substância da Central: é um módulo separado, só-leitura, que LÊ os artefatos
que o sistema de backup (`C:\\IALD\\_BACKUP_SYSTEM\\`) já grava — exatamente como o monitor de
patentes lê o store em `andamentos/`. A régua: uma falha de leitura é FALHA em-banda; nunca
'ok' falso. Local-first: os discos de backup são da máquina do operador; na nuvem (paths
ausentes) reporta honestamente `ambiente=remoto`. NUNCA lê/expõe senha — só STATUS.
"""
from __future__ import annotations

import csv as _csv
import io as _io
import json as _json
import shutil as _shutil
from . import sem_janela as _subprocess   # nunca abre janela na tela
import threading as _threading
import time as _time
from datetime import datetime, timezone
from pathlib import Path

# --- caminhos do sistema de backup (máquina do operador) ---
BACKUP_SYSTEM = Path(r"C:\IALD\_BACKUP_SYSTEM")
D_REPORTS = Path(r"D:\_BACKUP_LOGS\gate2")          # report_*.json do espelho inteligente
COFRE = Path(r"C:\IALD\_COFRE\_COFRE_TGL.hc")
DAILY_LOG = BACKUP_SYSTEM / "backup_daily.log"
TOSHIBA_LOG = BACKUP_SYSTEM / "toshiba_backup.log"
RCLONE_LOG = BACKUP_SYSTEM / "rclone_upload.log"
DAILY_PS1 = BACKUP_SYSTEM / "backup_daily.ps1"
TOSHIBA_LABEL = "TOSHIBA EXT"
TOSHIBA_SMB = r"\\10.95.94.160\TOSHIBA EXT(1)"   # Toshiba no roteador Linksys (cred IALD no cmdkey/DPAPI)

# frescor esperado (horas): diário deve rodar todo dia (04:00); Toshiba é semanal
FRESH_DAILY_WARN, FRESH_DAILY_BAD = 30, 72
FRESH_WEEKLY_WARN, FRESH_WEEKLY_BAD = 8 * 24, 16 * 24

# estado do botão "rodar backup agora" — uma execução por vez (serializada)
_STATE: dict = {"running": False, "started": None, "finished": None, "rc": None, "erro": None}
_LOCK = _threading.Lock()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _age_hours(path: Path) -> float | None:
    """Idade em horas do mtime do arquivo (quando o backup terminou). None se ausente."""
    try:
        return round((_time.time() - path.stat().st_mtime) / 3600.0, 1)
    except OSError:
        return None


def _mtime_utc(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        return None


def _free_gb(drive: str) -> float | None:
    try:
        return round(_shutil.disk_usage(drive).free / (1024 ** 3), 1)
    except OSError:
        return None


def _tail(path: Path, n: int = 40) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    except OSError:
        return []


def _find_toshiba() -> str | None:
    """Acha a letra da Toshiba pelo RÓTULO de volume via ctypes (sem wmic, que o Win11 25H2
    remove). Lê o label de cada letra montada e casa com 'TOSHIBA EXT' (E: direto ou onde estiver)."""
    import ctypes
    import string
    buf = ctypes.create_unicode_buffer(1024)
    fsbuf = ctypes.create_unicode_buffer(1024)
    for letter in string.ascii_uppercase:
        try:
            ok = ctypes.windll.kernel32.GetVolumeInformationW(  # type: ignore[attr-defined]
                ctypes.c_wchar_p(f"{letter}:\\"), buf, ctypes.sizeof(buf),
                None, None, None, fsbuf, ctypes.sizeof(fsbuf))
            if ok and buf.value.strip().lower() == TOSHIBA_LABEL.lower():
                return f"{letter}:"
        except Exception:  # noqa: BLE001
            continue
    # no roteador: share SMB (credencial guardada no cmdkey/DPAPI do usuario)
    try:
        if Path(TOSHIBA_SMB).is_dir():
            return TOSHIBA_SMB
    except OSError:
        pass
    return None


def _latest_report() -> dict | None:
    """O report_*.json mais recente do espelho inteligente (D:)."""
    try:
        reps = sorted(D_REPORTS.glob("report_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return None
    for p in reps:
        try:
            r = _json.loads(p.read_text(encoding="utf-8"))
            r["_mtime_utc"] = _mtime_utc(p)
            r["_idade_horas"] = _age_hours(p)
            return r
        except (OSError, _json.JSONDecodeError):
            continue
    return None


def _semaforo(idade: float | None, warn: float, bad: float, extra_ok: bool = True) -> str:
    """verde / laranja / vermelho / cinza — a régua: sem dado = cinza, nunca verde."""
    if idade is None:
        return "cinza"
    if not extra_ok:
        return "vermelho"
    if idade > bad:
        return "vermelho"
    if idade > warn:
        return "laranja"
    return "verde"


def _tasks() -> list[dict]:
    """Estado das tarefas agendadas (schtasks CSV — estável a locale)."""
    tasks = []
    for tn in ("IALD Backup Diario", "IALD Backup Toshiba"):
        try:
            out = _subprocess.run(["schtasks", "/query", "/tn", tn, "/fo", "CSV", "/nh"],
                                  capture_output=True, text=True, timeout=10)
            if out.returncode != 0:
                tasks.append({"nome": tn, "status": "não registrada", "proxima": None})
                continue
            row = next(_csv.reader(_io.StringIO(out.stdout.strip())), None)
            if row and len(row) >= 3:
                tasks.append({"nome": tn, "proxima": row[1], "status": row[2]})
            else:
                tasks.append({"nome": tn, "status": "?", "proxima": None})
        except Exception as e:  # noqa: BLE001
            tasks.append({"nome": tn, "status": "erro na leitura", "erro": str(e)[:120], "proxima": None})
    return tasks


def get_status() -> dict:
    """Status agregado das camadas de backup. Só-leitura, rápido, sem rede, sem senha."""
    if not BACKUP_SYSTEM.exists():
        # rodando fora da máquina do operador (ex.: deploy na nuvem) — honesto, sem fingir
        return {"gerado_utc": _now_utc(), "ambiente": "remoto", "camadas": [], "tarefas": [],
                "resumo": {"ok": None, "protegido": None,
                           "nota": "Backup local — visível só na Central da máquina do operador (127.0.0.1)."},
                "execucao": dict(_STATE)}

    camadas: list[dict] = []
    alertas: list[str] = []

    # C: — origem (trabalho)
    camadas.append({"id": "C", "nome": "C: — trabalho (origem)", "presente": True, "cor": "verde",
                    "detalhe": "a mais nova; fonte da verdade", "livre_gb": _free_gb("C:\\")})

    # D: — espelho inteligente (report_*.json)
    rep = _latest_report()
    if rep is None:
        camadas.append({"id": "D", "nome": "D: — espelho inteligente", "presente": D_REPORTS.exists(),
                        "cor": "cinza", "detalhe": "nenhuma rodada registrada ainda"})
    else:
        idade = rep.get("_idade_horas")
        abortado = bool(rep.get("aborted"))
        canon_ok = rep.get("canonicals_ok")
        breaker_ok = rep.get("breaker_ok")
        extra_ok = (not abortado) and (canon_ok is not False)
        cor = _semaforo(idade, FRESH_DAILY_WARN, FRESH_DAILY_BAD, extra_ok)
        det = f"versionados {rep.get('versioned_ok', 0)} · arquivados {rep.get('archived', 0)}"
        if abortado:
            det = "⚠ DISJUNTOR DISPAROU — espelho não tocado; investigue o C:"
            alertas.append("Espelho D:: disjuntor disparou (possível ataque no C:).")
        elif rep.get("canonical_drift"):
            det += " · [drift no anchor de um.py — confira se foi você]"
        if idade is not None and idade > FRESH_DAILY_WARN and not abortado:
            alertas.append(f"Espelho D:: última rodada há {idade:.0f}h (esperado ≤ 24h).")
        camadas.append({"id": "D", "nome": "D: — espelho inteligente", "presente": True, "cor": cor,
                        "ultimo_utc": rep.get("_mtime_utc"), "idade_horas": idade,
                        "disjuntor_ok": breaker_ok, "canonicos_ok": canon_ok,
                        "detalhe": det, "livre_gb": _free_gb("D:\\")})

    # Toshiba — 3ª cópia (log + presença por rótulo)
    tosh = _find_toshiba()
    if tosh is None:
        camadas.append({"id": "Toshiba", "nome": "Toshiba — 3ª cópia física", "presente": False,
                        "cor": "cinza", "detalhe": "desconectada (normal se está no roteador/desligada)"})
    else:
        idade = _age_hours(TOSHIBA_LOG)
        cor = _semaforo(idade, FRESH_WEEKLY_WARN, FRESH_WEEKLY_BAD)
        if idade is not None and idade > FRESH_WEEKLY_WARN:
            alertas.append(f"Toshiba: última há {idade / 24:.0f} dia(s) (semanal).")
        no_router = tosh.startswith("\\\\")
        via = "roteador" if no_router else tosh
        free_path = tosh if no_router else (tosh + "\\")
        det = "backup semanal aditivo (não-destrutivo)" + (" — no roteador (SMB)" if no_router else "")
        camadas.append({"id": "Toshiba", "nome": f"Toshiba ({via}) — 3ª cópia física", "presente": True,
                        "cor": cor, "ultimo_utc": _mtime_utc(TOSHIBA_LOG), "idade_horas": idade,
                        "detalhe": det, "livre_gb": _free_gb(free_path)})

    # Google — nuvem cifrada (rclone log)
    idade = _age_hours(RCLONE_LOG)
    cor = _semaforo(idade, FRESH_DAILY_WARN, FRESH_DAILY_BAD)
    camadas.append({"id": "Google", "nome": "Google — nuvem cifrada (offsite)", "presente": RCLONE_LOG.exists(),
                    "cor": cor if RCLONE_LOG.exists() else "cinza", "ultimo_utc": _mtime_utc(RCLONE_LOG),
                    "idade_horas": idade, "detalhe": "rclone crypt — o Google só recebe ruído"})

    # Cofre — AES-256 (só presença/tamanho; NUNCA a senha, NUNCA re-hash aqui)
    camadas.append({"id": "Cofre", "nome": "Cofre AES-256 (canônicos)", "presente": COFRE.exists(),
                    "cor": "verde" if COFRE.exists() else "vermelho",
                    "atualizado_utc": _mtime_utc(COFRE),
                    "tamanho_gb": (round(COFRE.stat().st_size / (1024 ** 3), 2) if COFRE.exists() else None),
                    "detalhe": "só a SUA senha abre — o painel jamais a guarda"})
    if not COFRE.exists():
        alertas.append("Cofre não encontrado em C:\\IALD\\_COFRE — verifique.")

    protegido = sum(1 for c in camadas if c["id"] in ("C", "D", "Toshiba") and c.get("presente"))
    ok = (not alertas) and all(c.get("cor") in ("verde", "cinza") for c in camadas if c["id"] != "Cofre") \
        and COFRE.exists()
    return {"gerado_utc": _now_utc(), "ambiente": "local", "camadas": camadas, "tarefas": _tasks(),
            "resumo": {"ok": ok, "protegido": f"{protegido} disco(s) físico(s) + cofre cifrado",
                       "alertas": alertas},
            "execucao": dict(_STATE)}


# --------------------------------------------------------------- o botão (admin) ---
def _run_bg() -> None:
    try:
        proc = _subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(DAILY_PS1)],
            capture_output=True, text=True, timeout=1800)
        with _LOCK:
            _STATE.update(running=False, finished=_time.time(), rc=proc.returncode, erro=None)
    except Exception as e:  # noqa: BLE001 — uma falha aqui é FALHA, reportada como tal
        with _LOCK:
            _STATE.update(running=False, finished=_time.time(), rc=-1, erro=str(e)[:300])


def run_backup() -> dict:
    """Dispara o backup diário (espelho C->D + sync cifrado C->Google) em background. Uma vez."""
    if not DAILY_PS1.exists():
        return {"status": "indisponivel", "erro": "backup_daily.ps1 não encontrado (Central remota?)"}
    with _LOCK:
        if _STATE["running"]:
            return {"status": "ja_rodando", "started": _STATE["started"]}
        _STATE.update(running=True, started=_time.time(), finished=None, rc=None, erro=None)
    _threading.Thread(target=_run_bg, daemon=True).start()
    return {"status": "disparado", "started": _STATE["started"],
            "nota": "rodando em background; consulte GET /api/backup/status para o desfecho"}
