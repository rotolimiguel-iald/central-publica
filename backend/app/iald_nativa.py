# -*- coding: utf-8 -*-
"""ANEXO — cockpit da IALD Nativa (a TERCEIRA casa) visto da Central de Patentes.

Módulo próprio no padrão dos anexos backup_status/epct_status: SÓ observa a casa nativa
(llama-server :8081, Flask :8082, cloudflared, GPU, modelos, kernels) — NUNCA toca
iald_web_server.py nem os launchers. Ações são exclusivamente via schtasks (tarefas
agendadas whitelistadas) e saneamento de listeners duplicados na 8082 (o bug de
10/08/2026: uma 2a instância manual na mesma porta criou dois listeners e travou o
painel). A régua: falha de leitura é FALHA em-banda, nunca 'ok' falso. Local-only:
na nuvem reporta ambiente=remoto. CONFIDENCIAIS (iald_psion_state.json,
iald_stack_v7.py): SÓ existência+mtime — jamais conteúdo.
"""
from __future__ import annotations

import csv as _csv
import io as _io
import re as _re
from . import sem_janela as _subprocess   # nunca abre janela na tela
import urllib.request as _urlreq
from datetime import datetime, timezone
from pathlib import Path

# --- coordenadas da casa nativa (máquina do operador) ---
IALD_DIR = Path(r"C:\IALD\projetos_pyhton\IALD")
LOGS_DIR = IALD_DIR / "logs"
MODELS_DIR = Path(r"C:\IALD\models")
CLOUDFLARED_ERR = LOGS_DIR / "cloudflared.log.err"

LLAMA_PORT = 8081
WEB_PORT = 8082
HTTP_TIMEOUT = 2.5  # segundos — status não pode pendurar o painel

# whitelist de tarefas agendadas — a ÚNICA superfície de ação sobre a casa nativa
TASKS_WHITELIST = ("IALD Llama Server", "IALD Web Server", "IALD Cloudflared Tunnel")

# confidenciais: SÓ existência+mtime; o conteúdo jamais passa por aqui
CONFIDENCIAIS = (IALD_DIR / "iald_psion_state.json", IALD_DIR / "iald_stack_v7.py")

LINKS = {"demo": "https://demo.iald.ia.br", "central": "https://central.iald.ia.br"}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mtime_utc(path: Path) -> str | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        return None


def _http_get(url: str, timeout: float = HTTP_TIMEOUT) -> tuple[int | None, str, str | None]:
    """(status_code, corpo[:64k], erro). Nunca levanta — o erro volta em-banda."""
    try:
        req = _urlreq.Request(url, headers={"User-Agent": "central-cockpit"})
        with _urlreq.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (127.0.0.1 fixo)
            return resp.status, resp.read(65536).decode("utf-8", errors="replace"), None
    except Exception as e:  # noqa: BLE001 — URLError/HTTPError/timeout/ConnectionRefused
        code = getattr(e, "code", None)  # HTTPError ainda e' uma resposta do servidor
        body = ""
        try:
            body = e.read(65536).decode("utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:  # noqa: BLE001
            pass
        return code, body, (None if code is not None else str(e)[:200])


def _task_state(name: str) -> dict:
    """Estado de uma tarefa agendada via schtasks CSV (estável a locale)."""
    try:
        out = _subprocess.run(["schtasks", "/Query", "/TN", name, "/FO", "CSV", "/NH"],
                              capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            return {"nome": name, "status": "nao registrada", "proxima": None}
        row = next(_csv.reader(_io.StringIO(out.stdout.strip())), None)
        if row and len(row) >= 3:
            return {"nome": name, "proxima": row[1], "status": row[2]}
        return {"nome": name, "status": "?", "proxima": None}
    except Exception as e:  # noqa: BLE001
        return {"nome": name, "status": "erro na leitura", "erro": str(e)[:150], "proxima": None}


def _listeners(port: int) -> tuple[list[int], str | None]:
    """PIDs em LISTENING na porta (netstat -ano). (pids ordenados, erro)."""
    try:
        out = _subprocess.run(["netstat", "-ano", "-p", "TCP"],
                              capture_output=True, text=True, timeout=15)
        if out.returncode != 0:
            return [], f"netstat rc={out.returncode}"
        pids: set[int] = set()
        suffix = f":{port}"
        for line in out.stdout.splitlines():
            parts = line.split()
            # Proto | Local Address | Foreign Address | State | PID
            if len(parts) >= 5 and parts[0].upper() == "TCP" and "LISTEN" in parts[3].upper() \
                    and parts[1].endswith(suffix):
                try:
                    pids.add(int(parts[4]))
                except ValueError:
                    continue
        return sorted(pids), None
    except Exception as e:  # noqa: BLE001
        return [], str(e)[:200]


def _proc_details(pids: list[int]) -> dict[int, dict]:
    """Nome/criação/pai de cada PID via PowerShell CIM (sem wmic — Win11 25H2 o remove).
    Best-effort: PID ausente do resultado = processo já morreu ou leitura falhou."""
    if not pids:
        return {}
    flt = " or ".join(f"ProcessId={p}" for p in pids)
    ps = ("Get-CimInstance Win32_Process -Filter \"" + flt + "\" | "
          "Select-Object ProcessId,ParentProcessId,Name,CreationDate | "
          "ForEach-Object { '{0}|{1}|{2}|{3}' -f $_.ProcessId,$_.ParentProcessId,$_.Name,"
          "($_.CreationDate.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')) }")
    try:
        out = _subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                              capture_output=True, text=True, timeout=20)
        det: dict[int, dict] = {}
        for line in out.stdout.splitlines():
            bits = line.strip().split("|")
            if len(bits) == 4 and bits[0].isdigit():
                det[int(bits[0])] = {"pid": int(bits[0]),
                                     "pai": int(bits[1]) if bits[1].isdigit() else None,
                                     "nome": bits[2], "criado_utc": bits[3]}
        return det
    except Exception:  # noqa: BLE001
        return {}


def _parent_cmdline(ppid: int | None) -> str:
    """Linha de comando do processo pai (para reconhecer o launcher start_iald_web.ps1)."""
    if not ppid:
        return ""
    ps = (f"(Get-CimInstance Win32_Process -Filter 'ProcessId={ppid}').CommandLine")
    try:
        out = _subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                              capture_output=True, text=True, timeout=15)
        return (out.stdout or "").strip()
    except Exception:  # noqa: BLE001
        return ""


def _tail(path: Path, n: int) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    except OSError:
        return []


# ------------------------------------------------------------------ seções


def _sec_llama() -> dict:
    sec: dict = {"porta": LLAMA_PORT}
    code, body, err = _http_get(f"http://127.0.0.1:{LLAMA_PORT}/health")
    sec["health_http"] = code
    sec["online"] = (code == 200)
    if err:
        sec["health_erro"] = err
    if code == 200:
        mcode, mbody, _merr = _http_get(f"http://127.0.0.1:{LLAMA_PORT}/metrics")
        if mcode == 200 and mbody:
            metrics: dict[str, float] = {}
            for line in mbody.splitlines():
                m = _re.match(r"^(llamacpp:[A-Za-z0-9_:]+)(?:\{[^}]*\})?\s+([-+0-9.eE]+)\s*$", line)
                if m:
                    try:
                        metrics[m.group(1).split(":", 1)[1]] = float(m.group(2))
                    except ValueError:
                        continue
            sec["metrics"] = metrics or None
        else:
            sec["metrics"] = None
            sec["metrics_nota"] = "indisponivel (servidor sem --metrics ou rota ausente)"
    sec["tarefa"] = _task_state("IALD Llama Server")
    return sec


def _sec_web() -> dict:
    sec: dict = {"porta": WEB_PORT}
    code, _body, err = _http_get(f"http://127.0.0.1:{WEB_PORT}/")
    sec["http"] = code
    sec["online"] = (code is not None)  # qualquer resposta = servidor de pe' (302/401 contam)
    if err:
        sec["http_erro"] = err
    pids, nerr = _listeners(WEB_PORT)
    sec["listeners_pids"] = pids
    if nerr:
        sec["listeners_erro"] = nerr
    sec["duplicado"] = (len(pids) > 1)
    if sec["duplicado"]:
        sec["alerta"] = (f"{len(pids)} listeners na porta {WEB_PORT} (bug de 10/08: instancia "
                         "manual dupla trava o painel) — use o saneamento")
    sec["tarefa"] = _task_state("IALD Web Server")
    return sec


def _sec_tunnel() -> dict:
    sec: dict = {}
    try:
        out = _subprocess.run(["tasklist", "/FI", "IMAGENAME eq cloudflared.exe", "/FO", "CSV", "/NH"],
                              capture_output=True, text=True, timeout=15)
        rows = [r for r in _csv.reader(_io.StringIO(out.stdout.strip()))
                if r and r[0].lower() == "cloudflared.exe"]
        sec["processo_presente"] = bool(rows)
        sec["pids"] = [int(r[1]) for r in rows if len(r) > 1 and r[1].isdigit()]
    except Exception as e:  # noqa: BLE001
        sec["processo_presente"] = None
        sec["processo_erro"] = str(e)[:200]
    sec["tarefa"] = _task_state("IALD Cloudflared Tunnel")
    if CLOUDFLARED_ERR.exists():
        sec["log_err_tail"] = _tail(CLOUDFLARED_ERR, 3)
        sec["log_err_mtime_utc"] = _mtime_utc(CLOUDFLARED_ERR)
    return sec


def _sec_gpu() -> dict:
    try:
        csvs = sorted(LOGS_DIR.glob("gpu_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError as e:
        return {"erro": f"logs ilegiveis: {e}"}
    if not csvs:
        return {"erro": "nenhum gpu_*.csv em logs/"}
    src = csvs[0]
    try:
        # utf-8-sig: o nvidia-smi grava BOM no header
        lines = [l for l in src.read_text(encoding="utf-8-sig", errors="replace").splitlines() if l.strip()]
        if len(lines) < 2:
            return {"arquivo": src.name, "erro": "csv sem linhas de dados ainda"}
        header = [h.strip() for h in lines[0].split(",")]
        last = [v.strip() for v in lines[-1].split(",")]
        amostra = dict(zip(header, last))
        return {"arquivo": src.name, "mtime_utc": _mtime_utc(src), "amostra": amostra}
    except OSError as e:
        return {"arquivo": src.name, "erro": str(e)[:200]}


def _sec_models() -> list[dict] | dict:
    try:
        out = [{"nome": p.name, "gb": round(p.stat().st_size / (1024 ** 3), 2)}
               for p in sorted(MODELS_DIR.glob("*.gguf"), key=lambda p: p.name.lower())]
        return out
    except OSError as e:
        return {"erro": str(e)[:200]}


def _sec_kernels() -> list[dict] | dict:
    try:
        return [{"nome": p.name, "bytes": p.stat().st_size, "mtime_utc": _mtime_utc(p)}
                for p in sorted(IALD_DIR.glob("IALD_Kernel_v*.txt"), key=lambda p: p.name.lower())]
    except OSError as e:
        return {"erro": str(e)[:200]}


def _sec_confidenciais() -> list[dict]:
    """SÓ existência+mtime — o conteúdo destes arquivos JAMAIS passa pela Central."""
    return [{"nome": p.name, "presente": p.exists(), "mtime_utc": _mtime_utc(p)}
            for p in CONFIDENCIAIS]


def get_status() -> dict:
    """Status agregado da casa nativa. Só-leitura, rede apenas em 127.0.0.1, sem segredo."""
    if not IALD_DIR.exists():
        # fora da máquina do operador (deploy na nuvem) — honesto, sem fingir
        return {"gerado_utc": _now_utc(), "ambiente": "remoto",
                "nota": "IALD Nativa e' local — visivel so' na Central da maquina do operador.",
                "links": dict(LINKS)}
    return {"gerado_utc": _now_utc(), "ambiente": "local",
            "llama": _sec_llama(), "web": _sec_web(), "tunnel": _sec_tunnel(),
            "gpu": _sec_gpu(), "models": _sec_models(), "kernels": _sec_kernels(),
            "confidenciais": _sec_confidenciais(), "links": dict(LINKS)}


# ------------------------------------------------------------------ ações (admin)


def _schtasks_action(verb: str, name: str) -> dict:
    if name not in TASKS_WHITELIST:
        raise ValueError(f"tarefa fora da whitelist: {name!r}")
    out = _subprocess.run(["schtasks", verb, "/TN", name],
                          capture_output=True, text=True, timeout=20)
    return {"tarefa": name, "acao": verb.lstrip("/").lower(), "rc": out.returncode,
            "ok": out.returncode == 0,
            "saida": (out.stdout or out.stderr or "").strip()[:300],
            "estado": _task_state(name), "gerado_utc": _now_utc()}


def run_task(name: str) -> dict:
    """schtasks /Run — SOMENTE tarefas da whitelist (ValueError fora dela)."""
    return _schtasks_action("/Run", name)


def end_task(name: str) -> dict:
    """schtasks /End — SOMENTE tarefas da whitelist (ValueError fora dela)."""
    return _schtasks_action("/End", name)


def sanear_web() -> dict:
    """Mata os listeners EXTRAS na 8082 (o bug do painel travado). Mantém o PID da
    tarefa supervisionada quando identificável (pai = launcher start_iald_web);
    senão mantém o mais antigo. FAIL-VISÍVEL: sem duplicata, ValueError."""
    pids, nerr = _listeners(WEB_PORT)
    if nerr:
        raise ValueError(f"nao foi possivel ler os listeners da {WEB_PORT}: {nerr}")
    if len(pids) == 0:
        raise ValueError(f"nenhum listener na {WEB_PORT} — nada a sanear (servidor caido?)")
    if len(pids) == 1:
        raise ValueError(f"sem duplicata na {WEB_PORT} (um unico listener, PID {pids[0]}) — nada a sanear")

    det = _proc_details(pids)
    keep: int | None = None
    criterio = ""
    # 1) supervisionado identificável: o pai e' o launcher da tarefa (start_iald_web)
    for pid in pids:
        cmd = _parent_cmdline(det.get(pid, {}).get("pai"))
        if "start_iald_web" in cmd.lower():
            keep, criterio = pid, "pai = launcher start_iald_web (tarefa supervisionada)"
            break
    # 2) fallback: o mais antigo (a duplicata manual nasceu depois)
    if keep is None:
        datados = [p for p in pids if det.get(p, {}).get("criado_utc")]
        keep = (min(datados, key=lambda p: det[p]["criado_utc"]) if datados else min(pids))
        criterio = "mais antigo por data de criacao" if datados else "menor PID (sem data legivel)"

    mortos, falhas = [], []
    for pid in pids:
        if pid == keep:
            continue
        out = _subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                              capture_output=True, text=True, timeout=15)
        rec = {"pid": pid, "rc": out.returncode,
               "processo": det.get(pid, {}).get("nome"),
               "criado_utc": det.get(pid, {}).get("criado_utc"),
               "saida": (out.stdout or out.stderr or "").strip()[:200]}
        (mortos if out.returncode == 0 else falhas).append(rec)

    restantes, _ = _listeners(WEB_PORT)
    return {"ok": not falhas, "porta": WEB_PORT, "mantido": keep, "criterio": criterio,
            "mortos": mortos, "falhas": falhas, "listeners_depois": restantes,
            "gerado_utc": _now_utc()}
