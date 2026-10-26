# -*- coding: utf-8 -*-
"""Utilitários de G1: hash, leitura, escrita atômica com backup de BYTES, trocas contadas que preservam o fim de linha,
subprocesso com código de saída sempre à vista (nunca `| tail` escondendo rc).

Regra da casa (backup imediato, 22/08/2026 + emenda de 29/08): o backup é cópia de BYTES; escrita por temporário -> conferir
-> substituir; nunca `open(P, "w")` direto sobre arquivo de memória."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ------------------------------------------------------------------ erros com código de saída (tabela da ESPEC_ESPELHO §6)
# 0 completo/nada a fazer · 1 pendente · 5 G1 terminou, decisões do operador abertas · 10 WAIT · 20 STOP · 30 falha de leitura · 40 divergência
COD_OK, COD_PENDENTE, COD_OPERADOR, COD_WAIT, COD_STOP, COD_LEITURA, COD_DIVERGENCIA = 0, 1, 5, 10, 20, 30, 40


class G1Erro(Exception):
    codigo = COD_STOP

    def __init__(self, motivo, faltam=None):
        super().__init__(motivo)
        self.motivo = motivo
        self.faltam = list(faltam or [])


class Parar(G1Erro):
    """STOP: falta insumo, âncora ou gate; a lista do que falta vai junto (nunca em silêncio)."""
    codigo = COD_STOP


class FalhaLeitura(G1Erro):
    """Falha de leitura é falha visível (régua): nunca vira 'ok'."""
    codigo = COD_LEITURA


class Esperar(G1Erro):
    """WAIT: o Nós está em obra (um.py != pino do selo) ou há trava recente."""
    codigo = COD_WAIT


class Divergencia(G1Erro):
    """O ar/GitHub não serve o que o selo descreve."""
    codigo = COD_DIVERGENCIA


# ------------------------------------------------------------------ hash e leitura
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_arquivo(p, n=64):
    h = hashlib.sha256()
    with open(lp(p), "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()[:n]


def sha16(p):
    return sha256_arquivo(p, 16)


def lp(p):
    """Caminho longo do Windows (prefixo \\\\?\\) quando preciso; no resto, o próprio caminho."""
    s = str(p)
    if os.name == "nt" and len(s) > 240 and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + os.path.abspath(s)
    return s


def mkdir(p):
    """mkdir -p que aguenta caminho longo do Windows (as fontes pinadas do espelho passam de 250 caracteres)."""
    os.makedirs(lp(p), exist_ok=True)


def ler_bytes(p):
    try:
        with open(lp(p), "rb") as f:
            return f.read()
    except OSError as e:
        raise FalhaLeitura("não li %s: %r" % (p, e))


def ler_texto(p, erros="strict"):
    b = ler_bytes(p)
    try:
        return b.decode("utf-8", erros)
    except UnicodeDecodeError as e:
        raise FalhaLeitura("%s não é UTF-8: %r" % (p, e))


def ler_json(p):
    try:
        return json.loads(ler_texto(p))
    except ValueError as e:
        raise FalhaLeitura("JSON inválido em %s: %r" % (p, e))


def existe(p):
    try:
        return Path(lp(p)).exists()
    except OSError:
        return False


# ------------------------------------------------------------------ tempo
def agora_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")      # com fuso (L24)


def carimbo():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def instante(s):
    """Texto de instante -> datetime ingênuo LOCAL (o que o selo, o quadro e as pastas de subida usam); None se ilegível.
    Aceita «2026-10-24 09:32:40», «20261024_092423[_dryrun]», «24/10/2026 09:32:40» e ISO com fuso."""
    if isinstance(s, datetime):
        return s
    t = str(s or "").strip()
    if not t:
        return None
    for f in ("%Y-%m-%d %H:%M:%S", "%Y%m%d_%H%M%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(t[:len(datetime(2000, 1, 1).strftime(f))], f)
        except ValueError:
            pass
    try:
        d = datetime.fromisoformat(t)
        return d.astimezone().replace(tzinfo=None) if d.tzinfo else d
    except ValueError:
        return None


def fmt_instante(d):
    return d.strftime("%d/%m %H:%M:%S") if isinstance(d, datetime) else str(d)


def mtime_max(caminhos, ignorar_dirs=(".git", "node_modules", "__pycache__", ".lake"), limite=300000):
    """A última modificação (datetime local) entre arquivos e pastas (recursivo; sem .git/node_modules/__pycache__, sem .bak_/.tmp);
    None se nada existe. Tolera caminho longo e arquivo que some no meio."""
    mx, n = None, 0
    for c in caminhos:
        p = Path(c)
        achados = []
        try:
            if p.is_file():
                achados.append(str(p))
            elif p.is_dir():
                for root, dirs, files in os.walk(lp(p)):
                    dirs[:] = [d for d in dirs if d not in ignorar_dirs]
                    for f in files:
                        if ".bak_" in f or f.endswith((".tmp", ".tmp_custodia")):
                            continue
                        achados.append(os.path.join(root, f))
                        n += 1
                        if n > limite:
                            break
        except OSError:
            continue
        for a in achados:
            try:
                mt = datetime.fromtimestamp(os.path.getmtime(lp(a)))
            except OSError:
                continue
            if mx is None or mt > mx:
                mx = mt
    return mx


# ------------------------------------------------------------------ escrita atômica com backup de bytes
def escrever_atomico(p, dados, backup=True, ts=None, exigir_cresceu=False, pode_encolher=True):
    """Grava `dados` (bytes) em `p`: backup de BYTES ao lado (`<arquivo>.bak_<TS>`), temporário, conferência de tamanho,
    `os.replace`. Devolve {antes, depois, backup}. Se `exigir_cresceu`, o arquivo não pode encolher nem ficar igual."""
    p = Path(p)
    ts = ts or carimbo()
    antes = None
    bak = None
    if p.exists():
        raw = ler_bytes(p)
        antes = len(raw)
        if backup:
            bak = p.with_name(p.name + ".bak_" + ts)
            with open(lp(bak), "wb") as g:
                g.write(raw)
            if sha256_bytes(ler_bytes(bak)) != sha256_bytes(raw):
                raise FalhaLeitura("backup de bytes diverge: %s" % bak)
    else:
        mkdir(p.parent)
    tmp = p.with_name(p.name + ".tmp_" + ts)
    with open(lp(tmp), "wb") as g:
        g.write(dados)
    if os.path.getsize(lp(tmp)) != len(dados):
        raise FalhaLeitura("temporário com tamanho errado: %s" % tmp)
    if antes is not None and exigir_cresceu and len(dados) <= antes:
        os.remove(lp(tmp))
        raise Parar("o arquivo não cresceu (%d -> %d): %s" % (antes, len(dados), p))
    if antes is not None and not pode_encolher and len(dados) < antes:
        os.remove(lp(tmp))
        raise Parar("o arquivo encolheu sem motivo declarado (%d -> %d): %s" % (antes, len(dados), p))
    os.replace(lp(tmp), lp(p))
    return {"arquivo": str(p), "antes": antes, "depois": len(dados), "backup": str(bak) if bak else None}


def escrever_json(p, obj, **kw):
    return escrever_atomico(p, json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"), **kw)


def copiar_bytes(src, dst):
    """Cópia de bytes por temporário; pula se já igual (tamanho e sha). Devolve True se copiou."""
    src, dst = Path(src), Path(dst)
    if dst.is_file() and dst.stat().st_size == src.stat().st_size and sha256_arquivo(dst) == sha256_arquivo(src):
        return False
    mkdir(dst.parent)
    data = ler_bytes(src)
    tmp = dst.with_name(dst.name + ".tmp_custodia")
    with open(lp(tmp), "wb") as g:
        g.write(data)
    if os.path.getsize(lp(tmp)) != len(data):
        raise FalhaLeitura("cópia incompleta: %s" % dst)
    os.replace(lp(tmp), lp(dst))
    return True


# ------------------------------------------------------------------ trocas contadas, preservando o fim de linha
def ler_eol(p):
    """(texto com \\n, 'crlf'|'lf', bytes originais). O texto volta com LF para casar âncoras; gravar_eol refaz o fim de linha."""
    raw = ler_bytes(p)
    s = raw.decode("utf-8")
    eol = "crlf" if b"\r\n" in raw else "lf"
    return s.replace("\r\n", "\n"), eol, raw


def para_eol(texto_lf, eol):
    return texto_lf.replace("\n", "\r\n") if eol == "crlf" else texto_lf


def contar(s, a):
    return s.count(a)


def trocar_contado(s, velho, novo, n=1, rot=""):
    """Troca exatamente `n` ocorrências ou PARA (assert s.count(a) == n)."""
    c = s.count(velho)
    if c != n:
        raise Parar("troca contada falhou (%s): esperado %d, achado %d: %r" % (rot, n, c, velho[:100]))
    return s.replace(velho, novo)


def py_compile_bytes(dados, nome="x.py"):
    """Compila `dados` num temporário (sem executar). Devolve (ok, mensagem)."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        t = Path(d) / nome
        t.write_bytes(dados)
        r = subprocess.run([sys.executable, "-m", "py_compile", str(t)], capture_output=True, text=True)
        return r.returncode == 0, (r.stderr or "")[-1500:]


# ------------------------------------------------------------------ subprocesso (rc sempre à vista)
_GIT_EXE = None


def git_exe():
    """O executável do git: `G1_GIT_EXE` (ensaios), o do PATH, ou os lugares usuais de instalação no Windows (uma tarefa agendada roda
    com PATH mínimo). Se não achar, devolve «git» e a falha APARECE (rc 127 -> FalhaLeitura): nunca vira «sem commit» nem «árvore limpa»."""
    global _GIT_EXE
    forcado = os.environ.get("G1_GIT_EXE")
    if forcado:
        return forcado
    if _GIT_EXE is None:
        achado = shutil.which("git")
        if not achado:
            for cand in (r"C:\Program Files\Git\cmd\git.exe", r"C:\Program Files\Git\bin\git.exe", r"C:\Program Files (x86)\Git\cmd\git.exe"):
                if os.path.isfile(cand):
                    achado = cand
                    break
        _GIT_EXE = achado or "git"
    return _GIT_EXE


def rodar(cmd, cwd=None, entrada=None, timeout=None, env=None, log=None):
    """Roda `cmd` (lista). Devolve dict {rc, saida, stdout, stderr, stdout_bytes, segundos, cmd}. NUNCA esconde o rc; grava o log integral
    se pedido. Não usa shell. A saída é UTF-8 (PYTHONIOENCODING). `saida` = stdout + «[stderr]» (para mensagens); `stdout` é só o stdout
    (o que o chamador interpreta). `git` na posição 0 é resolvido por git_exe()."""
    e = dict(os.environ)
    e["PYTHONIOENCODING"] = "utf-8"
    if env:
        e.update(env)
    cmd = list(cmd)
    if cmd and str(cmd[0]) == "git":
        cmd[0] = git_exe()
        e["GIT_OPTIONAL_LOCKS"] = "0"          # o vigia só LÊ: `git status`/`git diff` não tomam o index.lock opcional (outra sessão pode estar em `git add`/`commit` no mesmo repositório)
    t0 = time.time()
    out_b = b""
    try:
        r = subprocess.run(cmd, cwd=str(cwd) if cwd else None, input=entrada, capture_output=True, timeout=timeout, env=e)
        out_b = r.stdout or b""
        out_t, err_t = out_b.decode("utf-8", "replace"), (r.stderr or b"").decode("utf-8", "replace")
        saida = out_t + (("\n[stderr]\n" + err_t) if err_t else "")
        rc = r.returncode
    except subprocess.TimeoutExpired as ex:
        out_t, err_t, saida, rc = "", "TIMEOUT após %ss: %r" % (timeout, ex), "TIMEOUT após %ss: %r" % (timeout, ex), 124
    except OSError as ex:
        out_t, err_t, saida, rc = "", "não executou: %r" % (ex,), "não executou: %r" % (ex,), 127
    res = {"rc": rc, "saida": saida, "stdout": out_t, "stderr": err_t, "stdout_bytes": out_b, "segundos": round(time.time() - t0, 1), "cmd": [str(x) for x in cmd]}
    if log:
        Path(log).parent.mkdir(parents=True, exist_ok=True)
        Path(log).write_text(saida, encoding="utf-8")
    return res


def git(repo, *args):
    """stdout do git, sem espaços nas pontas. Falha (rc != 0, git ausente, repositório ilegível) é FalhaLeitura — NUNCA a string vazia, que os
    chamadores leriam como «sem commit» ou «árvore limpa» (falha de leitura é falha visível)."""
    r = rodar(["git", "-c", "core.quotepath=off", "-C", str(repo)] + list(args))
    if r["rc"] != 0:
        raise FalhaLeitura("git %s falhou (rc %s) em %s: %s" % (" ".join(str(a) for a in args)[:90], r["rc"], repo, (r["stderr"] or r["saida"]).strip()[-220:]))
    return r["stdout"].strip()


def git_bytes(repo, *args):
    """stdout do git em BYTES (blobs), com a mesma regra: rc != 0 é FalhaLeitura."""
    r = rodar(["git", "-c", "core.quotepath=off", "-C", str(repo)] + list(args))
    if r["rc"] != 0:
        raise FalhaLeitura("git %s falhou (rc %s) em %s: %s" % (" ".join(str(a) for a in args)[:90], r["rc"], repo, (r["stderr"] or r["saida"]).strip()[-220:]))
    return r["stdout_bytes"]


def git_rc(repo, *args):
    """Só o código de saída — para quem sabe interpretá-lo (use git_ancestral para merge-base)."""
    return rodar(["git", "-c", "core.quotepath=off", "-C", str(repo)] + list(args))["rc"]


def git_ancestral(repo, ancestral, descendente):
    """True/False se `ancestral` é ancestral de `descendente`. rc 0 = sim, rc 1 = não; QUALQUER outro (git ausente, objeto desconhecido) é
    FalhaLeitura — antes um rc 128 virava «ainda não está em origin/main»."""
    rc = git_rc(repo, "merge-base", "--is-ancestor", ancestral, descendente)
    if rc == 0:
        return True
    if rc == 1:
        return False
    raise FalhaLeitura("git merge-base --is-ancestor %s %s falhou (rc %s) em %s" % (str(ancestral)[:12], str(descendente)[:12], rc, repo))


def commit_da_custodia(repo, v):
    """O commit mais recente cujo assunto é «custodia(<versões>): …» com `v` entre as versões — aceita a custódia CONJUNTA
    (`custodia(v393+v394)`, `custodia(v387+v388+v389)`). Percorre TODA a história (--grep), sem teto de commits. None = não há; erro de git = FalhaLeitura."""
    out = git(repo, "log", "--extended-regexp", "--grep=^custodia\\(.*%s.*\\):" % v, "--format=%H%x09%s")      # candidatos; o casamento exato da versão é abaixo
    for ln in out.splitlines():
        h, _, s = ln.partition("\t")
        m = re.match(r"custodia\(([^)]*)\):", s)
        if m and v in re.findall(r"v\d{3,}", m.group(1)):
            return h
    return None


def data_do_commit(repo, h):
    """Data do commit (datetime com fuso -> naive local) para comparar com o instante do quadro."""
    iso = git(repo, "log", "-1", "--format=%cI", h)
    try:
        return datetime.fromisoformat(iso).astimezone().replace(tzinfo=None)
    except ValueError:
        raise FalhaLeitura("data do commit %s ilegível: %r" % (h[:8], iso))


def git_blob_sha256(repo, rev, caminho):
    """sha256 dos bytes do blob `rev:caminho` (git cat-file blob). Ausente no commit = FalhaLeitura."""
    return sha256_bytes(git_bytes(repo, "cat-file", "blob", "%s:%s" % (rev, caminho)))


# ------------------------------------------------------------------ formatos
def fmt_milhar(n):
    return format(int(n), ",")


def virgula(x, casas):
    return ("%." + str(casas) + "f") % x


_TRANSLIT = {  # 25/10/2026: as gregas e os sinais da casa viram palavras ANTES da decomposição (o commit b8e028fb perdeu o «α»)
    "\u03b1": "alfa", "\u03b2": "beta", "\u03b3": "gama", "\u03b4": "delta", "\u0394": "Delta", "\u03b5": "epsilon",
    "\u03b8": "theta", "\u03ba": "kappa", "\u03bb": "lambda", "\u039b": "Lambda", "\u03bc": "mu", "\u03bd": "nu",
    "\u03c0": "pi", "\u03c1": "rho", "\u03c3": "sigma", "\u03a3": "Sigma", "\u03c4": "tau", "\u03c6": "phi",
    "\u03c7": "chi", "\u03c8": "psi", "\u03c9": "omega", "\u03a9": "Omega",
    "\u2260": "!=", "\u2192": "->", "\u2190": "<-", "\u21d2": "=>", "\u2264": "<=", "\u2265": ">=", "\u2014": "-", "\u2013": "-",
    "\u00d7": "x", "\u221a": "sqrt", "\u2248": "~", "\u00b7": ".", "\u2026": "...",
}


def ascii_sem_acento(s):
    import unicodedata
    s = "".join(_TRANSLIT.get(ch, ch) for ch in s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def so_digitos_e_pino(a, b):
    """Dois vereditos são 'o mesmo, a menos de dígitos e pino' (ESPEC_CENTRAL §6.2 S8)."""
    def n(x):
        x = re.sub(r"[0-9a-f]{16,64}", "<PIN>", str(x))
        return re.sub(r"\d+", "#", x)
    return n(a) == n(b)


def versao_num(v):
    m = re.fullmatch(r"v(\d{3,})", str(v))
    if not m:
        raise Parar("versão inválida: %r" % (v,))
    return int(m.group(1))


def nome_versao(n):
    return "v%d" % n


# ------------------------------------------------------------------ patch contado sobre arquivo existente (CRLF ou LF), com backup de bytes
def patch_bytes(p, pares, marca, exige_crescer=True, ts=None, rot=""):
    """Aplica `pares` [(velho, novo)] ao arquivo `p`: já aplicado se `marca` está no texto; senão backup de BYTES ao lado, cada troca
    exige `count == 1` (o fim de linha do arquivo é respeitado: CRLF se o arquivo tem CRLF), temporário, crescimento, `os.replace`.
    Devolve {estado: 'ja_aplicado'|'aplicado', antes, depois, backup}."""
    p = Path(p)
    raw = ler_bytes(p)
    s = raw.decode("utf-8")
    if marca in s:
        return {"estado": "ja_aplicado", "antes": len(raw), "depois": len(raw), "backup": None}
    crlf = b"\r\n" in raw
    for velho, novo in pares:
        if crlf:
            velho, novo = velho.replace("\r\n", "\n").replace("\n", "\r\n"), novo.replace("\r\n", "\n").replace("\n", "\r\n")
        c = s.count(velho)
        if c != 1:
            raise Parar("troca contada falhou em %s (%s): esperado 1, achado %d: %r" % (p.name, rot, c, velho[:90]))
        s = s.replace(velho, novo)
    r = escrever_atomico(p, s.encode("utf-8"), backup=True, ts=ts, exigir_cresceu=exige_crescer)
    r["estado"] = "aplicado"
    return r
