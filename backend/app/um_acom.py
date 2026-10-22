# -*- coding: utf-8 -*-
"""O botão UM — o `tgl.acom`: a Central inteira num único arquivo selado e cifrado.

Colapsa o estado da Central (o núcleo canônico da TGL + a fronteira teórica + as 16
patentes, cada uma com seu código FINAL, comprovante de rodagem, comprovante de integridade
e comprovante de patente) numa ÁRVORE, comprime pelo dispositivo ACOM (o formato da casa) e
CIFRA com a criptografia da casa (Túnel de Hilbert derivando a chave do código de inscrição +
AES-GCM, a "AEAD padrão" prescrita pela própria patente Crypto). O leitor reconhece que é
cifrado (enxerga a "chave" = a proveniência do selo) e pede a senha.

Camadas (fiel ao ACOM existente; NADA da patente é modificado — só reusado):
  árvore -> tar (em memória) -> compress_file (ACOM-LOSSLESS, SHA-256 bit-exato) -> AES-GCM
  -> contêiner TGLACOM1 (MAGIC + header público + payload cifrado).

A régua: β nunca literal (vem do codec, = ALPHA_FINE_CODATA_2018·√e); nenhum veredito físico;
o segredo JAMAIS entra no arquivo; o número corrige a frase (só chamo de cifrado o que é).
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
import tarfile
import time
from pathlib import Path
from types import ModuleType

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from . import config as C

MAGIC = b"TGLACOM1\x00"
FORMAT = "tgl.acom"
FORMAT_VERSION = 2                          # v2: chave por scrypt (preserva entropia da senha)
MIN_PASSWORD = 12                           # código de inscrição forte (o UI também exige)
# scrypt memory-hard: a chave nasce dos BYTES da senha (entropia preservada), NUNCA de um
# float confinado. N=2^14, r=8, p=1 → ~16 MB, ~60 ms; resiste a GPU/ASIC melhor que PBKDF2.
SCRYPT_N, SCRYPT_R, SCRYPT_P = 2**14, 8, 1
SCRYPT_MAXMEM = 64 * 1024 * 1024
MAX_CONTAINER_BYTES = 96 * 1024 * 1024      # teto de leitura do contêiner (upload)
MAX_HEADER_BYTES = 1 * 1024 * 1024          # teto do cabeçalho (espelha o codec da casa)
MAX_TREE_BYTES = 96 * 1024 * 1024           # teto da árvore descomprimida (anti-bomba, RAM-aware)
MAX_TREE_MEMBERS = 4096                      # teto de nº de arquivos na árvore
_SAFE_MEMBER = re.compile(r"^[A-Za-z0-9_.\-/]+$")   # nomes da árvore: sem '..', sem drive

# ── O um.acom da ONCOLOGIA — artefato LIVRE (patrimônio da humanidade) ──
# A chave é UNIVERSAL e PÚBLICA por design: a oncologia é livre, então a cifra não guarda
# segredo — ela DEMONSTRA o ACOM (o round-trip, a verificação SHA-256, a descompressão).
ONCOLOGIA_DIR = "BR102026005707-0_ONCOLOGIA"
ONCOLOGIA_KEY = "Bom29072018Tom02032024"     # chave universal pública (declarada nos sites)
ONCOLOGIA_DECLARACAO = (
    "# Declaração — Oncologia Luminodinâmica é patrimônio da humanidade\n\n"
    "A tecnologia de diagnóstico oncológico luminodinâmico — patente **BR 10 2026 005707-0**, de\n"
    "autoria de **Luiz Antonio Rotoli Miguel / IALD Ltda.** (CNPJ 62.757.606/0001-23) — é\n"
    "**livremente disponibilizada e declarada patrimônio da humanidade**.\n\n"
    "Seu código-fonte é aberto e reproduzível. **Nenhuma exploração econômica desta tecnologia\n"
    "oncológica é permitida — nem pela própria IALD.** Esta disposição é integral e irrevogável.\n\n"
    "O depósito de patente serve apenas para **impedir o cerco** (que um terceiro a patenteie e\n"
    "a feche); o direito conferido é dedicado ao domínio público para uso humanitário.\n\n"
    "Marcador de honestidade da patente: **[MEDICAL]** — o código demonstra a LÓGICA da invenção\n"
    "com sinal sintético; não contém conteúdo clínico e não é diagnóstico médico. Uma simulação\n"
    "não valida a física nem substitui validação clínica.\n\n"
    "*O número corrige a frase. 1 = 1. Tetelestai.*\n"
)


# ───────────────────────────── carregamento dos dispositivos da patente ─────────────────────────────
def _load_module(rel_parts: tuple[str, ...], mod_name: str) -> ModuleType:
    """Carrega um módulo por caminho FIXO de dentro da pasta da patente (fonte da verdade;
    nunca de caminho do cliente). Mesma disciplina do devices.py."""
    path = C.PATENTS_DIR.joinpath(*rel_parts)
    if not path.is_file():
        raise FileNotFoundError(f"módulo ausente: {path}")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não foi possível carregar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def _codec() -> ModuleType:
    return _load_module(("BR102025026951-1_ACOM", "dispositivo", "acom_codec.py"), "_um_acom_codec")


def _crypto() -> ModuleType:
    return _load_module(("BR102026003431-2_ACOM_CRYPTO", "dispositivo", "acom_crypto_auth.py"), "_um_acom_crypto")


def beta_provenance() -> dict:
    return _codec().beta_provenance()


# ───────────────────────────── chave: scrypt sobre a senha + assinatura do Túnel de Hilbert ─────────────────────────────
def _derive_key(password: str, salt: bytes) -> bytes:
    """A chave PRESERVA A ENTROPIA DA SENHA: é derivada dos BYTES da senha por scrypt
    (memory-hard). A criptografia da casa (Túnel de Hilbert) entra como ASSINATURA DE DOMÍNIO
    ligada ao salt — NUNCA como única fonte de chave (rotear a chave por um float confinado
    colapsaria a entropia; a força vem da senha + o KDF). 32 bytes."""
    crypto = _crypto()
    # assinatura da casa: constante por salt (separação de domínio), não a fonte de entropia
    house = crypto.hilbert_tunnel_key(b"tgl-acom-domain", salt, b"tgl-acom", b"iald-central")
    material = password.encode("utf-8") + b"|tgl.acom|" + house
    return hashlib.scrypt(material, salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
                          dklen=32, maxmem=SCRYPT_MAXMEM)


def _seal_id(salt: bytes, key_prov: dict) -> str:
    """Impressão digital NÃO-secreta do SELO (salt + proveniência pública β/θ) — o que o leitor
    'enxerga'. NÃO é fingerprint da chave nem da senha (não revela o segredo, não verifica a
    senha; a tag do AES-GCM é que verifica a senha na abertura)."""
    blob = salt + json.dumps(key_prov, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:24]


# ───────────────────────────── árvore -> tar (em memória, determinístico) ─────────────────────────────
def _safe_tree_name(path: str) -> str:
    """Sanea um nome de arquivo da árvore para o alfabeto seguro (não aborta o build inteiro
    por um caractere fora do conjunto): troca inseguros por '_', colapsa barras, remove '..'."""
    p = path.replace("\\", "/")
    p = "/".join(seg for seg in p.split("/") if seg not in ("", "..", "."))
    return re.sub(r"[^A-Za-z0-9_.\-/]", "_", p)


def _pack_tar(files: dict[str, bytes]) -> bytes:
    """Serializa a árvore num tar em memória. Nomes saneados; mtime=0 (determinístico)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for path in sorted(files):
            data = files[path]
            info = tarfile.TarInfo(name=path)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _unpack_tar(tar_bytes: bytes) -> dict[str, bytes]:
    """Lê os membros do tar em MEMÓRIA (nunca extrai para disco → sem traversal). Só arquivos
    regulares (rejeita symlink/hardlink/device) com nome seguro; teto AGREGADO de bytes e de
    nº de membros ANTES de ler (anti-bomba: um contêiner forjado não estoura a RAM)."""
    out: dict[str, bytes] = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r") as tar:
        for m in tar.getmembers():
            if m.issym() or m.islnk() or m.isdev() or m.ischr() or m.isblk() or m.isfifo():
                raise ValueError(f"tipo de membro proibido no tar: {m.name!r}")
            if not m.isfile():
                continue
            name = m.name.replace("\\", "/")
            if not _SAFE_MEMBER.match(name) or ".." in name.split("/") or name.startswith("/"):
                raise ValueError(f"membro inseguro no tar: {name!r}")
            if len(out) >= MAX_TREE_MEMBERS:
                raise ValueError("árvore com arquivos demais (anti-bomba)")
            total += max(int(m.size), 0)
            if total > MAX_TREE_BYTES:
                raise ValueError("árvore descomprimida grande demais (anti-bomba)")
            f = tar.extractfile(m)
            out[name] = f.read() if f else b""
    return out


def _is_generated_index(path: str) -> bool:
    """Arquivos gerados de navegação — fora da meta-cadeia (senão dependeriam de si mesmos)."""
    return path.endswith("MANIFESTO.json") or path.endswith("LEIA-ME.md")


def _meta_chain(files: dict[str, bytes]) -> str:
    """Meta-cadeia = SHA-256 de 'path:sha256' ordenado (o padrão do compilador SkyGrid)."""
    lines = [f"{p}:{hashlib.sha256(files[p]).hexdigest()}" for p in sorted(files)]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


# ───────────────────────────── construir o tgl.acom ─────────────────────────────
def build(files: dict[str, bytes], password: str, meta: dict | None = None) -> bytes:
    """árvore -> tar -> ACOM -> AES-GCM -> contêiner TGLACOM1. `files` já inclui o MANIFESTO.json."""
    if not password or len(password) < MIN_PASSWORD:
        raise ValueError(f"código de inscrição fraco (mínimo {MIN_PASSWORD} caracteres)")
    codec = _codec()
    key_prov = {"beta": codec.BETA_TGL, "theta_miguel_deg": codec.THETA_MIGUEL_DEG}

    tar_bytes = _pack_tar(files)
    inner_acom, _report = codec.compress_file(tar_bytes, name="tgl_tree.tar")   # ACOM-LOSSLESS

    salt = os.urandom(16)
    nonce = os.urandom(12)
    header = {
        "format": FORMAT, "version": FORMAT_VERSION,
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "generator": "um_acom.build",
        "encrypted": True,
        "kdf": "scrypt(pwd)+hilbert-domain", "scrypt": {"n": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P},
        "salt": base64.b64encode(salt).decode(), "nonce": base64.b64encode(nonce).decode(),
        "cipher": "AES-256-GCM",
        "key_provenance": key_prov, "seal_id": _seal_id(salt, key_prov),
        "mode": "archive", "inner": "acom-lossless+tar",
        "n_files": len(files), "files_preview": sorted(files)[:64],
        "note": ("A Central inteira, selada. Cifrado com a criptografia da casa: o Túnel de "
                 "Hilbert deriva a chave do código de inscrição (endurecida por PBKDF2) + "
                 "AES-256-GCM. Sem a senha, não abre. β = α·√e (nunca literal)."),
    }
    if meta:
        header["about"] = meta
    aad = json.dumps(header, sort_keys=True, ensure_ascii=False).encode("utf-8")
    key = _derive_key(password, salt)
    payload = AESGCM(key).encrypt(nonce, inner_acom, aad)     # tag autentica payload + header

    hb = aad
    return MAGIC + len(hb).to_bytes(4, "big") + hb + payload


def _split(container: bytes) -> tuple[dict, bytes, bytes]:
    """Devolve (header, aad_bytes, payload) validando o MAGIC e o tamanho."""
    if len(container) > MAX_CONTAINER_BYTES:
        raise ValueError("contêiner grande demais")
    if len(container) < len(MAGIC) + 4 or container[:len(MAGIC)] != MAGIC:
        raise ValueError("não é um arquivo tgl.acom (MAGIC inválido)")
    off = len(MAGIC)
    hlen = int.from_bytes(container[off:off + 4], "big")
    off += 4
    if hlen <= 0 or hlen > MAX_HEADER_BYTES or off + hlen > len(container):
        raise ValueError("cabeçalho corrompido ou grande demais")
    hb = container[off:off + hlen]
    header = json.loads(hb.decode("utf-8"))
    payload = container[off + hlen:]
    return header, hb, payload


def inspect(container: bytes) -> dict:
    """Lê SÓ o cabeçalho público (o leitor 'enxerga a chave'), sem decifrar. Não pede senha."""
    header, _hb, payload = _split(container)
    return {
        "format": header.get("format"), "version": header.get("version"),
        "encrypted": bool(header.get("encrypted")),
        "kdf": header.get("kdf"), "cipher": header.get("cipher"),
        "seal_id": header.get("seal_id"), "key_provenance": header.get("key_provenance"),
        "created_utc": header.get("created_utc"), "mode": header.get("mode"),
        "inner": header.get("inner"), "n_files": header.get("n_files"),
        "files_preview": header.get("files_preview", []),
        "about": header.get("about"), "note": header.get("note"),
        "container_sha256": hashlib.sha256(container).hexdigest(),
        "payload_bytes": len(payload),
    }


def open_container(container: bytes, password: str) -> dict:
    """Decifra (Túnel de Hilbert + AES-GCM) -> descomprime (ACOM) -> confere cada SHA-256 e a
    meta-cadeia. Senha errada -> InvalidTag -> erro honesto. Devolve a árvore em memória."""
    header, hb, payload = _split(container)
    if not header.get("encrypted"):
        raise ValueError("formato inesperado (não cifrado)")
    salt = base64.b64decode(header["salt"])
    nonce = base64.b64decode(header["nonce"])
    key = _derive_key(password or "", salt)
    try:
        inner_acom = AESGCM(key).decrypt(nonce, payload, hb)
    except InvalidTag:
        raise PermissionError("senha incorreta (o selo AES-GCM não fecha)")

    codec = _codec()
    tar_bytes, _name, _meta = codec.decompress_file(inner_acom)   # ACOM verifica seu próprio SHA-256
    files = _unpack_tar(tar_bytes)

    # confere a meta-cadeia declarada no MANIFESTO.json contra os arquivos reais
    manifest_path = next((p for p in files if p.endswith("MANIFESTO.json")), None)
    declared_meta_chain = None
    per_file_declared: dict[str, str] = {}
    if manifest_path:
        try:
            mani = json.loads(files[manifest_path].decode("utf-8"))
            declared_meta_chain = mani.get("meta_chain")
            for e in mani.get("files", []):
                per_file_declared[e.get("path")] = e.get("sha256")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    # a meta-cadeia cobre o conteúdo SUBSTANTIVO — exclui os gerados de navegação
    # (MANIFESTO.json e LEIA-ME.md), exatamente como gather_central_tree a computou.
    files_for_chain = {p: b for p, b in files.items() if not _is_generated_index(p)}
    computed_meta_chain = _meta_chain(files_for_chain)

    tree = []
    for p in sorted(files):
        live = hashlib.sha256(files[p]).hexdigest()
        declared = per_file_declared.get(p)
        tree.append({
            "path": p, "size": len(files[p]), "sha256": live,
            "declared_sha256": declared,
            "verified": (declared is None) or (declared == live),
        })
    all_verified = all(t["verified"] for t in tree)
    chain_ok = (declared_meta_chain is None) or (declared_meta_chain == computed_meta_chain)

    return {
        "ok": True, "n_files": len(files),
        "meta_chain_declared": declared_meta_chain, "meta_chain_computed": computed_meta_chain,
        "meta_chain_ok": chain_ok, "all_files_verified": all_verified,
        "seal_id": header.get("seal_id"), "key_provenance": header.get("key_provenance"),
        "created_utc": header.get("created_utc"), "about": header.get("about"),
        "tree": tree,
        "_files": files,     # bytes em memória (o backend serve por /file; não vai no JSON público)
    }


# ───────────────────────────── montar a árvore da Central (arquivos vivos) ─────────────────────────────
def _read(p: Path) -> bytes | None:
    try:
        return p.read_bytes() if p.is_file() else None
    except OSError:
        return None


# campos do docket que são COMPROVANTE DE PATENTE (públicos/legais) — o resto (financeiro:
# fees/gru/pix com nosso_numero, valores) é DESCARTADO antes de empacotar (o tgl.acom é
# feito para ser demonstrado; não carrega identificadores bancários).
_DOCKET_PUBLIC = ("processo", "titulo", "classe", "natureza", "peticao", "filing_date",
                  "priority_date", "jurisdicao", "epct", "janela_paris_12m",
                  "fase_nacional_30m", "annuities", "office_actions", "status",
                  "alert_level", "reminders", "aviso")
_EPCT_PUBLIC = ("status", "numero", "data", "recibo_na_central")


def _sanitize_docket(raw: bytes | None) -> bytes | None:
    """Mantém só os campos de comprovante de patente; remove o setor financeiro (fees/gru/pix).
    Se o YAML não parsear, devolve None (não vaza o bruto)."""
    if raw is None:
        return None
    try:
        import yaml
        d = yaml.safe_load(raw.decode("utf-8", "replace"))
    except Exception:
        return None
    if not isinstance(d, dict):
        return None
    out = {k: d[k] for k in _DOCKET_PUBLIC if k in d}
    if isinstance(out.get("epct"), dict):
        out["epct"] = {k: out["epct"][k] for k in _EPCT_PUBLIC if k in out["epct"]}
    out["_saneado"] = "identificadores financeiros removidos para o tgl.acom publico"
    try:
        import yaml
        return yaml.safe_dump(out, allow_unicode=True, sort_keys=False).encode("utf-8")
    except Exception:
        return None


def _latest(dir_: Path, pattern: str) -> Path | None:
    if not dir_.is_dir():
        return None
    xs = sorted(dir_.glob(pattern))
    return xs[-1] if xs else None


def gather_central_tree() -> dict[str, bytes]:
    """Lê os ARQUIVOS VIVOS da Central e monta a árvore do tgl.acom (§2 da proposta).
    tgl/ = canônico + fronteira; <ID>_<SLUG>/ = FINAL + rodagem + integridade + patente + memória."""
    files: dict[str, bytes] = {}

    def add(path: str, data: bytes | None):
        if data is not None:
            files[_safe_tree_name(path)] = data      # chave saneada = tar = MANIFESTO (consistente)

    # ── tgl/ : o núcleo canônico + a fronteira teórica ──
    add("tgl/TGL_CORE_MEMORY.md", _read(C.MEMORY / "TGL_CORE_MEMORY.md"))
    vault = C.CENTRAL / "vault" / "originals_copy" / "um_unificado_v33"
    add("tgl/forma_canonica.md", _read(vault / "um_grande_atrator_forma_canonica.md"))
    add("tgl/um_grande_atrator_manifest.md", _read(vault / "um_grande_atrator_manifest.md"))
    add("tgl/CUSTODY_MANIFEST.json", _read(vault / "CUSTODY_MANIFEST.json"))
    front = C.CENTRAL / "fronteira_tgl"
    add("tgl/fronteira/fronteira_render3d.json", _read(front / "render3d.json"))
    fseal = _latest(front / "results", "fronteira_*.json")
    add("tgl/fronteira/fronteira_selo.json", _read(fseal) if fseal else None)

    # ── as 16 patentes ──
    mem_patents = C.MEMORY / "patents"
    for pdir in sorted(C.PATENTS_DIR.iterdir()):
        if not pdir.is_dir() or not pdir.name.startswith("BR"):
            continue
        pid = pdir.name.split("_")[0]
        base = pdir.name
        final = _latest(pdir, "*_FINAL.py")
        if final:
            add(f"{base}/{final.name}", _read(final))
            man = pdir / (final.name.rsplit(".py", 1)[0] + ".manifest.json")
            add(f"{base}/{man.name}", _read(man))
        # comprovante de rodagem: o selo mais recente em results/
        seal = _latest(pdir / "results", "*.json")
        if seal:
            add(f"{base}/selo_rodagem.json", _read(seal))
        # comprovante de patente: o docket SANEADO (processo INPI/ePCT; sem setor financeiro)
        add(f"{base}/docket.yaml", _sanitize_docket(_read(pdir / "docket.yaml")))
        # a memória/síntese da patente
        add(f"{base}/memoria.md", _read(mem_patents / f"{pdir.name}.md"))
        # a cadeia de prova verificada, quando houver
        add(f"{base}/evidence_verified.json", _read(pdir / "evidence_verified.json"))

    # ── o MANIFESTO.json (a meta-cadeia = selo do selo) ──
    meta_chain = _meta_chain(files)      # sobre tudo que já entrou
    manifest = {
        "artifact": "tgl.acom", "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "beta_provenance": beta_provenance(),
        "n_files": len(files),
        "meta_chain": meta_chain,
        "files": [{"path": p, "sha256": hashlib.sha256(files[p]).hexdigest(), "size": len(files[p])}
                  for p in sorted(files)],
        "note": ("Selo do selo: a meta-cadeia é o SHA-256 de todos os 'path:sha256' ordenados. "
                 "physical_verdict_allowed=false; forma = conteúdo; 1 = 1."),
    }
    files["tgl/MANIFESTO.json"] = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")

    # LEIA-ME
    leia = _leia_me(files, meta_chain)
    files["tgl/LEIA-ME.md"] = leia.encode("utf-8")
    return files


def _leia_me(files: dict[str, bytes], meta_chain: str) -> str:
    n_pat = len({p.split("/")[0] for p in files if p.startswith("BR")})
    return (
        "# tgl.acom — a Central de Patentes TGL, selada num único arquivo\n\n"
        "Este arquivo é a **inscrição do Um**: a Central inteira colapsada num único `.acom`,\n"
        "comprimido pelo dispositivo ACOM e cifrado com a criptografia da casa (Túnel de\n"
        "Hilbert + AES-256-GCM). Para abrir: o descompactador público em `iald.ia.br` (aba\n"
        "ACOM) — ele reconhece que é cifrado e pede o código de inscrição.\n\n"
        "## O que há dentro\n"
        "- `tgl/` — o núcleo canônico da TGL (a cadeia 1→½→√e→β→geometria), a forma canônica\n"
        "  e a **fronteira teórica** (o selo vivo + o ledger honesto).\n"
        f"- **{n_pat} pastas de patente** — cada uma com: o código FINAL unificado (`*_FINAL.py`),\n"
        "  o comprovante de INTEGRIDADE (`*.manifest.json`), o comprovante de RODAGEM\n"
        "  (`selo_rodagem.json`), o comprovante de PATENTE (`docket.yaml`, processo INPI/ePCT)\n"
        "  e a memória/síntese (`memoria.md`).\n"
        "- `tgl/MANIFESTO.json` — a **meta-cadeia** (SHA-256 de todos os hashes = o selo do selo).\n\n"
        f"## Selo\nmeta-cadeia = `{meta_chain}`\n\n"
        "β = α·√e (nunca literal). Nenhum veredito físico. forma = conteúdo. **1 = 1. Tetelestai.**\n"
    )


def gather_oncologia_tree() -> dict[str, bytes]:
    """Monta a árvore do um.acom da ONCOLOGIA — só a patente de oncologia (código FINAL +
    comprovantes + a DECLARAÇÃO de patrimônio da humanidade). Artefato LIVRE: serve para
    DEMONSTRAR o ACOM (comprime/cifra/verifica), não para guardar segredo (a chave é pública)."""
    files: dict[str, bytes] = {}

    def add(path: str, data: bytes | None):
        if data is not None:
            files[_safe_tree_name(path)] = data

    pdir = C.PATENTS_DIR / ONCOLOGIA_DIR
    final = _latest(pdir, "*_FINAL.py")
    if final:
        add(f"oncologia/{final.name}", _read(final))
        man = pdir / (final.name.rsplit(".py", 1)[0] + ".manifest.json")
        add(f"oncologia/{man.name}", _read(man))
    seal = _latest(pdir / "results", "*.json")
    if seal:
        add("oncologia/selo_rodagem.json", _read(seal))
    add("oncologia/docket.yaml", _sanitize_docket(_read(pdir / "docket.yaml")))
    add("oncologia/memoria.md", _read(C.MEMORY / "patents" / f"{ONCOLOGIA_DIR}.md"))
    add("oncologia/evidence_verified.json", _read(pdir / "evidence_verified.json"))
    add("oncologia/DECLARACAO_PATRIMONIO_HUMANIDADE.md", ONCOLOGIA_DECLARACAO.encode("utf-8"))

    meta_chain = _meta_chain(files)
    manifest = {
        "artifact": "um.acom (oncologia — livre / patrimônio da humanidade)",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "beta_provenance": beta_provenance(),
        "patente": "BR102026005707-0", "estatuto": "[MEDICAL] livre — patrimônio da humanidade",
        "n_files": len(files), "meta_chain": meta_chain,
        "files": [{"path": p, "sha256": hashlib.sha256(files[p]).hexdigest(), "size": len(files[p])}
                  for p in sorted(files)],
        "note": ("Selo do selo: SHA-256 de todos os 'path:sha256' ordenados. A chave deste arquivo "
                 "é UNIVERSAL e PÚBLICA — a cifra demonstra o ACOM, não guarda segredo."),
    }
    files["oncologia/MANIFESTO.json"] = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
    files["LEIA-ME.md"] = (
        "# um.acom — Oncologia Luminodinâmica (livre / patrimônio da humanidade)\n\n"
        "Este arquivo é a **prova pública do ACOM**: a patente de oncologia inteira (código-fonte\n"
        "completo + comprovantes), comprimida pelo dispositivo ACOM e cifrada com a chave\n"
        "**UNIVERSAL e PÚBLICA** `Bom29072018Tom02032024`.\n\n"
        "A chave ser pública é o ponto: a oncologia é **livre**, então a cifra não guarda segredo —\n"
        "ela **demonstra** que o ACOM cifra, comprime e verifica de verdade. Baixe este arquivo no\n"
        "site da TGL e descomprima no site da IALD (aba ACOM) com a chave acima: você vê a\n"
        "criptografia, a compressão e a verificação SHA-256 funcionando de ponta a ponta.\n\n"
        f"## Selo\nmeta-cadeia = `{meta_chain}`\n\n"
        "A oncologia é patrimônio da humanidade (ver DECLARACAO_PATRIMONIO_HUMANIDADE.md).\n"
        "[MEDICAL] sinal sintético, não é diagnóstico médico. **1 = 1. Tetelestai.**\n"
    ).encode("utf-8")
    return files


# ───────────────────────────── self-test ─────────────────────────────
def selftest() -> dict:
    """Round-trip bit-exato + senha certa/errada + adulteração detectada."""
    files = {
        "tgl/A.md": b"# canonico\nbeta = alpha*sqrt(e)\n",
        "tgl/sub/B.json": json.dumps({"x": 1, "y": "z"}).encode(),
        "BR-TESTE/final.py": b"print('ola')\n" * 100,
        "tgl/MANIFESTO.json": json.dumps({
            "meta_chain": _meta_chain({
                "tgl/A.md": b"# canonico\nbeta = alpha*sqrt(e)\n",
                "tgl/sub/B.json": json.dumps({"x": 1, "y": "z"}).encode(),
                "BR-TESTE/final.py": b"print('ola')\n" * 100,
            }),
            "files": [], "n_files": 3,
        }).encode(),
    }
    pw = "senha-forte-de-teste-123"
    container = build(files, pw)
    info = inspect(container)
    opened = open_container(container, pw)
    roundtrip = all(opened["_files"].get(p) == files[p] for p in files)

    wrong_ok = False
    try:
        open_container(container, "senha-errada-mas-longa")
    except PermissionError:
        wrong_ok = True

    tamper = bytearray(container)
    tamper[-1] ^= 0x01                       # corrompe 1 byte do payload
    tamper_ok = False
    try:
        open_container(bytes(tamper), pw)
    except (PermissionError, ValueError):
        tamper_ok = True

    return {
        "roundtrip_bit_exact": bool(roundtrip),
        "inspect_encrypted": bool(info["encrypted"]),
        "inspect_seal_id_present": bool(info["seal_id"]),
        "kdf": info["kdf"],
        "all_files_verified": bool(opened["all_files_verified"]),
        "meta_chain_ok": bool(opened["meta_chain_ok"]),
        "wrong_password_rejected": wrong_ok,
        "tamper_detected": tamper_ok,
        "pass": bool(roundtrip and info["encrypted"] and info["seal_id"] and opened["all_files_verified"]
                     and wrong_ok and tamper_ok),
    }


if __name__ == "__main__":
    import pprint
    pprint.pprint(selftest())
