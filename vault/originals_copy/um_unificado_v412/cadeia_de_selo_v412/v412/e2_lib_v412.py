"""Etapa 2 da v412: utilidades comuns (backup de bytes, escrita por temporario, sha16 lido do arquivo, estado em disco, exame nao vazio)."""
import datetime, hashlib, json, os
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
ESTADO = D / "ETAPA_2_ESTADO_v412.json"


def sha256_arq(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha16_arq(p) -> str:
    return sha256_arq(p)[:16]


def agora() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def salvar_bytes(p, dados: bytes, backup=True) -> None:
    """Backup de BYTES do arquivo existente; escrita por temporario; confere o tamanho; substitui."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if backup and p.exists():
        bak = Path(str(p) + ".bak_" + agora())
        n = 0
        while bak.exists():
            n += 1
            bak = Path(str(p) + ".bak_" + agora() + "_%d" % n)
        bak.write_bytes(p.read_bytes())
        assert bak.read_bytes() == p.read_bytes(), ("o backup nao e' copia de bytes", str(bak))
    tmp = Path(str(p) + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.stat().st_size == len(dados), ("escrita truncada", str(p))
    os.replace(tmp, p)
    assert p.stat().st_size == len(dados)


def salvar_json(p, obj, backup=True) -> None:
    salvar_bytes(p, json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"), backup=backup)


def ler_json(p):
    return json.loads(Path(p).read_bytes().decode("utf-8"))


def estado_ler() -> dict:
    return ler_json(ESTADO) if ESTADO.exists() else {"blocos": {}}


def estado_bloco(bloco: str, feito: bool, arquivos: dict, nota: str = "", proximo: str = "", extra: dict | None = None) -> None:
    """Grava o bloco no estado (por temporario e troca, guardando o anterior com .bak_<data>). `arquivos`: {rotulo: caminho}; o sha16 de cada um e' lido do arquivo."""
    est = estado_ler()
    est.setdefault("blocos", {})
    reg = {"feito": bool(feito), "quando": datetime.datetime.now().isoformat(timespec="seconds"), "nota": nota,
           "arquivos": {k: {"caminho": str(v), "sha16": sha16_arq(v), "bytes": Path(v).stat().st_size} for k, v in arquivos.items()}}
    if extra:
        reg["extra"] = extra
    est["blocos"][bloco] = reg
    est["proximo_comando"] = proximo
    est["agente"] = "claude-construtor-v412 (Etapa 2)"
    est["contrato_sha16"] = sha16_arq(D / "CONTRATO_v412.md")
    est["contrato_R2_existe"] = (D / "CONTRATO_v412_R2.md").exists()
    salvar_json(ESTADO, est)


class Exame:
    """Contador de checagens: cada checagem diz quantos itens examinou; zero itens e' falha visivel, nunca passagem."""

    def __init__(self, nome=""):
        self.nome = nome
        self.linhas = []

    def chk(self, rotulo, ok, n_itens, detalhe=None):
        passou = bool(ok) and n_itens > 0
        self.linhas.append({"checagem": rotulo, "ok": passou, "n_itens_examinados": int(n_itens), "detalhe": detalhe,
                            **({"falha_por_zero_itens": True} if (bool(ok) and n_itens <= 0) else {})})
        return passou

    @property
    def ok(self):
        return all(l["ok"] for l in self.linhas) and len(self.linhas) > 0

    def resumo(self):
        return {"nome": self.nome, "n_checagens": len(self.linhas), "n_ok": sum(1 for l in self.linhas if l["ok"]), "n_itens_total": sum(l["n_itens_examinados"] for l in self.linhas), "ok": self.ok}
