# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] as funcoes comuns dos scripts do B(n) da v413 e a linha de comando que os .sh usam (nenhum `python -c` nos runners).
"""util_bn_v413.py -- funcoes comuns do B(n) da v413. Importar este modulo NAO le nem grava nada (nenhuma E/S no nivel do modulo; o delta_bn so' e' importado sob pedido).
  livro_conferido(path)  : o livro do quadro conferido INTEIRO pela regra do esboco R3.6 (sincronizar_bancada.py l.693-707): toda linha nao vazia le como JSON (senao ValueError, nunca `continue`),
                           anterior == o hash do elo anterior, hash == sha256 do proprio elo sem o campo hash, seq sem repeticao (2.2).
  porta_aberta, pid_da_porta, processo, processos_um_bancada, ultimo_boot: leitura do sistema (socket e PowerShell; nada e' parado nem lancado).
  gravar_json_novo: temporario -> conferir tamanho -> os.replace; recusa sobrescrever.
Linha de comando (os .sh do B(n)): python -I -B -X utf8 util_bn_v413.py <subcomando> [args]; rc 0 = sim/ok, 1 = nao, 2 = uso errado. Os subcomandos so' leem (nenhum grava)."""
import datetime
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import unicodedata
import urllib.request

RX_DATA_BR = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_arquivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 22), b""):
            h.update(bloco)
    return h.hexdigest()


def ler_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _sem_duplicatas(pares):
    vistas = {}
    for k, v in pares:
        if k in vistas:
            raise ValueError("chave duplicada %r no mesmo objeto JSON" % (k,))
        vistas[k] = v
    return vistas


def ler_json_estrito(p):
    """JSON que recusa chave duplicada (o leitor humano le a primeira; o json.loads ficaria com a ultima)."""
    with open(p, "rb") as f:
        return json.loads(f.read().decode("utf-8"), object_pairs_hook=_sem_duplicatas)


def pinar(p, **extra):
    """{path, sha256, bytes} lidos do arquivo (nunca digitados), mais as chaves extras."""
    return dict({"path": os.path.abspath(p), "sha256": sha256_arquivo(p), "bytes": os.path.getsize(p)}, **extra)


def gravar_json_novo(p, obj):
    """grava um arquivo NOVO: temporario -> conferir tamanho e bytes -> os.replace; recusa sobrescrever (SystemExit)."""
    if os.path.exists(p):
        raise SystemExit("ja existe, nao sobrescrevo: " + p)
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    dados = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = p + ".tmp"
    with open(tmp, "xb") as f:
        f.write(dados)
    if os.path.getsize(tmp) != len(dados) or open(tmp, "rb").read() != dados:
        os.remove(tmp)
        raise SystemExit("o temporario nao confere: " + tmp)
    os.replace(tmp, p)
    if open(p, "rb").read() != dados:
        raise SystemExit("o arquivo gravado nao confere: " + p)
    return p


def hash_evento(e):
    return hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def livro_conferido(path):
    """2.2: o livro do quadro conferido do primeiro ao ultimo elo, pela regra do esboco R3.6 (l.693-707). Linha ilegivel, elo fora da cadeia ou seq repetida = ValueError (fail-closed).
    Devolve {eventos: {seq: evento}, n_elos, cabeca (o hash do ultimo elo), sha256 do arquivo, bytes}."""
    raw = open(path, "rb").read()
    ant, n, eventos = "0" * 64, 0, {}
    for i, linha in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not linha.strip():
            continue
        try:
            e = json.loads(linha)
        except ValueError as exc:
            raise ValueError("EVENTOS_JSONL_ILEGIVEL: linha %d: %s" % (i, exc))
        n += 1
        if not isinstance(e, dict) or e.get("anterior") != ant or e.get("hash") != hash_evento(e):
            raise ValueError("EVENTOS_CADEIA_QUEBRADA: no evento seq %r (elo %d, linha %d)" % (e.get("seq") if isinstance(e, dict) else None, n, i))
        ant = e["hash"]
        if e.get("seq") in eventos:
            raise ValueError("EVENTO_SEQ_DUPLICADO: %r" % (e.get("seq"),))
        eventos[e.get("seq")] = e
    return {"eventos": eventos, "n_elos": n, "cabeca": ant, "sha256": sha256_bytes(raw), "bytes": len(raw)}


def texto_normalizado(s):
    """NFKC -> NFD sem marcas combinantes nem caracteres de formato -> caixa dobrada (para comparar palavras sem acento)."""
    n = unicodedata.normalize("NFKC", str(s))
    return "".join(c for c in unicodedata.normalize("NFD", n) if unicodedata.category(c) not in ("Mn", "Cf")).casefold()


def porta_aberta(porta, timeout=1.5):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        return s.connect_ex(("127.0.0.1", int(porta))) == 0
    finally:
        s.close()


def _ps(cmd, timeout=60):
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout, r.stderr


def pid_da_porta(porta):
    """o PID que escuta na porta (Get-NetTCPConnection), ou None."""
    rc, out, _ = _ps("(Get-NetTCPConnection -State Listen -LocalPort %d -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess" % int(porta))
    linhas = [x.strip() for x in out.splitlines() if x.strip()]
    return int(linhas[-1]) if (rc == 0 and linhas and linhas[-1].isdigit()) else None


def processo(pid):
    """{pid, nome, criado (ISO local), linha_de_comando} do processo `pid`, ou None se ele nao existe (Win32_Process; so' leitura)."""
    rc, out, _ = _ps("$p = Get-CimInstance Win32_Process -Filter 'ProcessId=%d'; if ($p) { 'VIVO|' + $p.Name + '|' + $p.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') + '|' + $p.CommandLine } else { 'AUSENTE' }" % int(pid))
    linhas = [x for x in out.splitlines() if x.strip()]
    ult = linhas[-1].strip() if linhas else ""
    if ult == "AUSENTE":
        return None
    if not ult.startswith("VIVO|"):
        raise RuntimeError("leitura do processo %s ilegivel (rc %s): %r" % (pid, rc, out[-300:]))
    _, nome, criado, linha = ult.split("|", 3)
    return {"pid": int(pid), "nome": nome, "criado": criado, "linha_de_comando": linha}


def processos_um_bancada():
    """os processos cuja linha de comando cita um_bancada.py (menos o proprio PowerShell da consulta): [{pid, nome, criado, linha_de_comando}]."""
    rc, out, err = _ps("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*um_bancada.py*' -and $_.ProcessId -ne $PID } | "
                       "ForEach-Object { 'P|' + $_.ProcessId + '|' + $_.Name + '|' + $_.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') + '|' + $_.CommandLine }")
    if rc != 0:
        raise RuntimeError("a consulta dos processos falhou (rc %s): %s" % (rc, err[-300:]))
    saida = []
    for x in out.splitlines():
        if x.startswith("P|"):
            _, pid, nome, criado, linha = x.strip().split("|", 4)
            saida.append({"pid": int(pid), "nome": nome, "criado": criado, "linha_de_comando": linha})
    return saida


def ultimo_boot():
    rc, out, _ = _ps("(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('yyyy-MM-ddTHH:mm:ss')")
    linhas = [x.strip() for x in out.splitlines() if x.strip()]
    if rc != 0 or not linhas or not re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$", linhas[-1]):
        raise RuntimeError("o ultimo boot nao foi lido (rc %s)" % rc)
    return linhas[-1]


def get_json(url, timeout=10):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def instante(s):
    """um instante ISO (com ou sem fuso; sem fuso = hora local da maquina) como datetime com fuso."""
    d = datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return d if d.tzinfo else d.astimezone()


# ---------------------------------------------------------------- a linha de comando dos runners (.sh): so' leitura
def _dbn():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import delta_bn_v413 as DBN   # noqa: E402
    return DBN


def _cli(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, a = argv[0], argv[1:]
    if cmd == "const" and len(a) == 1:                      # uma constante do delta_bn (str/int)
        v = getattr(_dbn(), a[0])
        print(v)
        return 0
    if cmd == "pino" and len(a) == 3:                       # ARQ CHAVE CAMPO: o campo de um pino (ex.: PINOS_BN_v411.json esboco_R3_6 path)
        v = ler_json(a[0])[a[1]][a[2]]
        print(v)
        return 0
    if cmd == "json" and len(a) == 2:                       # ARQ a.b.c: um valor aninhado
        v = ler_json(a[0])
        for k in a[1].split("."):
            v = v[int(k)] if isinstance(v, list) else v[k]
        print(v if not isinstance(v, (dict, list)) else json.dumps(v, ensure_ascii=False))
        return 0
    if cmd == "tem_chave" and len(a) == 2:                  # ARQ CHAVE: rc 0 se a chave de topo existe
        return 0 if a[1] in ler_json(a[0]) else 1
    if cmd == "sha256" and len(a) == 1:
        print(sha256_arquivo(a[0]))
        return 0
    if cmd == "porta_fechada" and len(a) <= 1:              # rc 0 se a porta (padrao: a da Bancada) NAO responde
        return 1 if porta_aberta(int(a[0]) if a else _dbn().PORTA) else 0
    if cmd == "nos_versao" and not a:                       # o um_version do selo do Nos, se o selo pina o um.py do disco
        D = _dbn()
        selo = ler_json(os.path.join(D.NOS, "um_absoluto_selo.json"))
        pina = (selo.get("sha256") or {}).get("um.py") == sha256_arquivo(os.path.join(D.NOS, "um.py"))
        print("%s %s" % (selo.get("um_version"), "SELO_PINA_O_UM_PY" if pina else "SELO_NAO_PINA_O_UM_PY"))
        return 0 if pina else 1
    if cmd == "pid_vivo_um_bancada" and len(a) == 1:        # rc 0 se o PID existe e e' o um_bancada.py
        p = processo(int(a[0]))
        print(json.dumps(p, ensure_ascii=False))
        return 0 if (p and "um_bancada.py" in p["linha_de_comando"]) else 1
    if cmd == "pendentes_vazios" and len(a) == 1:           # rc 0 se o PINOS_BN nao tem pendentes nem pino sem sha256
        pn = ler_json(a[0])
        sem = sorted(k for k, v in pn.items() if isinstance(v, dict) and "path" in v and not v.get("sha256"))
        print(json.dumps({"pendentes": pn.get("pendentes"), "pinos_sem_sha256": sem}, ensure_ascii=False))
        return 0 if (pn.get("pendentes") == [] and not sem) else 1
    if cmd == "evento_depois_do_ensaio" and len(a) == 3:    # SEQ HASH RECIBO_DO_ENSAIO: o evento (livro conferido inteiro) e' da c1, confere o hash e e' POSTERIOR ao fim do ensaio (2.6 c)
        D = _dbn()
        seq, h, rp = int(a[0]), a[1].strip().lower(), a[2]
        L = livro_conferido(D.QUADRO)
        e = L["eventos"].get(seq)
        if not e or not re.match(r"^[0-9a-f]{16,64}$", h) or not str(e.get("hash")).startswith(h) or e.get("quem") != "claude-c1" or e.get("tipo") != "SINCRONIZACAO_BANCADA":
            print("o evento %s nao esta' no livro, nao confere o hash dado ou nao e' SINCRONIZACAO_BANCADA da claude-c1" % seq)
            return 1
        r = ler_json(rp)
        ok = instante(e["quando"]) > instante(r["fim_utc"])
        print("evento %s quando %s | fim do ensaio %s | posterior: %s" % (seq, e["quando"], r["fim_utc"], ok))
        return 0 if ok else 1
    if cmd == "recibo_do_stdout" and len(a) == 1:           # ARQ: o caminho do recibo citado na ULTIMA linha JSON de um stdout do esboco
        linhas = [x for x in open(a[0], encoding="utf-8", errors="replace").read().splitlines() if x.strip().startswith("{")]
        if not linhas:
            return 1
        rp = json.loads(linhas[-1]).get("recibo")
        print(rp or "")
        return 0 if (rp and os.path.isfile(rp)) else 1
    if cmd == "saude_do_dia" and len(a) == 1:               # DIR: rc 0 se ha' uma conferencia A de HOJE (data local) em DIR, desta Bancada e com veredito conhecido; imprime o caminho e o veredito
        D = _dbn()
        hoje = datetime.date.today().strftime("%Y%m%d")
        cand = sorted(x for x in os.listdir(a[0]) if x.startswith("SAUDE_BANCADA_%s_" % hoje) and x.endswith(".json")) if os.path.isdir(a[0]) else []
        validas = []                                         # (revisao B10) o contrato SAUDE_BANCADA, a Bancada do delta_bn e um veredito que nao seja INDETERMINADO
        for x in cand:
            j = ler_json(os.path.join(a[0], x))
            if j.get("contrato") == "SAUDE_BANCADA" and os.path.normcase(str(j.get("bancada"))) == os.path.normcase(D.PRODUCAO) and j.get("veredito") not in (None, "INDETERMINADO"):
                validas.append((os.path.join(a[0], x), j.get("veredito")))
        if not validas:
            print("nenhuma conferencia A valida de hoje (%s) em %s (contrato SAUDE_BANCADA, Bancada %s, veredito conhecido); arquivos de hoje: %d" % (hoje, a[0], D.PRODUCAO, len(cand)))
            return 1
        print("%s %s" % validas[-1])
        return 0
    print("subcomando desconhecido ou argumentos errados: %r" % (argv,))
    return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(_cli(sys.argv[1:]))
