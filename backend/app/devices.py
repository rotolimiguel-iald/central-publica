# -*- coding: utf-8 -*-
"""Despachante de DISPOSITIVOS — cada patente contém, dentro de si, uma pasta
`dispositivo/` com o próprio dispositivo *funcionando* (a interface do dispositivo).
Este módulo carrega esse código de dentro da pasta da patente (fonte da verdade no
filesystem) e o expõe ao backend. Nunca embute lógica de dispositivo aqui — só
localiza e carrega o codec que vive junto da patente.

Segurança: só carrega de patents/<dir>/dispositivo/<slug>_codec.py (caminho fixo),
nunca de caminho fornecido pelo cliente."""
from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType

from . import config as C

# mapa dispositivo → (dir da patente, arquivo do codec). Explícito, auditável.
DEVICES: dict[str, dict] = {
    "acom": {
        "patent_id": "BR102025026951-1",
        "dir": "BR102025026951-1_ACOM",
        "codec": "acom_codec.py",
        "archive": "acom_archive.py",  # empacotador multi-arquivo (backup)
        "auto": "acom_auto.py",        # a PORTA ÚNICA: o sinal escolhe o codec, sem chaveamento
        "name": "ACOM",
        "kind": "compressor",          # dispositivo de software (roda de verdade)
        "title": "Compressor Ontológico de Memória",
    },
    # O TGL-Tensor tinha o algoritmo mais rico da casa (o NOME nativo) e NENHUM dispositivo:
    # existia como protótipo e como runner, mas ninguém podia jogar um tensor nele e ver o Nome
    # responder. O `dispositivo/` NÃO reimplementa a invenção — carrega o protótipo do operador
    # (READ-ONLY) e o expõe. O que roda é o algoritmo patenteado, não uma paráfrase dele.
    "tgl_tensor": {
        "patent_id": "BR102026003441-0",
        "dir": "BR102026003441-0_TGL_TENSOR",
        "codec": "tgl_tensor_device.py",
        "name": "TGL-Tensor",
        "kind": "compressor",
        "title": "Compressão Holográfica com Integridade por NOME",
    },
}


@lru_cache(maxsize=None)
def load_archive(slug: str) -> ModuleType:
    """Importa o empacotador (acom_archive.py) de dentro da pasta da patente. Cacheado."""
    slug = slug.lower()
    if slug not in DEVICES or "archive" not in DEVICES[slug]:
        raise KeyError(f"empacotador indisponível para: {slug}")
    info = DEVICES[slug]
    path = C.PATENTS_DIR / info["dir"] / "dispositivo" / info["archive"]
    if not path.is_file():
        raise FileNotFoundError(f"empacotador do dispositivo ausente: {path}")
    mod_name = f"_archive_{slug}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não foi possível carregar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def load_auto(slug: str) -> ModuleType:
    """Importa a PORTA ÚNICA (acom_auto.py) de dentro da pasta da patente. Cacheado.

    O codec é carregado ANTES e registrado como `acom_codec`, para que o auto o reuse em
    vez de re-executar o arquivo (um só objeto de módulo, um só β)."""
    slug = slug.lower()
    if slug not in DEVICES or "auto" not in DEVICES[slug]:
        raise KeyError(f"porta única indisponível para: {slug}")
    load_codec(slug)                              # garante o codec carregado…
    sys.modules.setdefault("acom_codec", sys.modules[f"_device_{slug}"])   # …sob o nome que o auto procura
    info = DEVICES[slug]
    path = C.PATENTS_DIR / info["dir"] / "dispositivo" / info["auto"]
    if not path.is_file():
        raise FileNotFoundError(f"porta única do dispositivo ausente: {path}")
    mod_name = f"_auto_{slug}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não foi possível carregar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def load_codec(slug: str) -> ModuleType:
    """Importa o módulo do codec de dentro da pasta da patente. Cacheado."""
    slug = slug.lower()
    if slug not in DEVICES:
        raise KeyError(f"dispositivo desconhecido: {slug}")
    spec_info = DEVICES[slug]
    path = C.PATENTS_DIR / spec_info["dir"] / "dispositivo" / spec_info["codec"]
    if not path.is_file():
        raise FileNotFoundError(f"codec do dispositivo ausente: {path}")
    mod_name = f"_device_{slug}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não foi possível carregar {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def device_info(slug: str) -> dict:
    """Metadados + proveniência β do dispositivo (sem rodar compressão)."""
    meta = DEVICES[slug.lower()]
    codec = load_codec(slug)
    tensor_ok = bool(getattr(codec, "tensor_available", lambda: False)())
    info = {
        "slug": slug.lower(),
        "patent_id": meta["patent_id"],
        "name": meta["name"],
        "kind": meta["kind"],
        "title": meta["title"],
        "beta": codec.beta_provenance(),
        "tensor_available": tensor_ok,
        "max_input_mb": codec.MAX_INPUT_BYTES // (1024 * 1024),
        # `modes` fica por compatibilidade de leitura; a porta é UMA — quem roteia é o sinal.
        "modes": ["file"] + (["tensor"] if tensor_ok else []),
    }
    try:                                          # a porta única (se presente neste dispositivo)
        auto = load_auto(slug)
        info["auto"] = {
            "available": True,
            "version": auto.AUTO_VERSION,
            "signal_types": [auto.SIG_TENSOR_FLOAT, auto.SIG_TENSOR_EXACT, auto.SIG_SEALED,
                             auto.SIG_SPARSE, auto.SIG_STRUCTURED, auto.SIG_TEXT, auto.SIG_BINARY],
            "fidelity_gate": {"psnr_db": auto.PSNR_GATE_DB, "correlation": auto.CORR_GATE,
                              "min_gain": auto.GAIN_MIN,
                              "status": "[ENGENHARIA] — declarado, NÃO derivado de β"},
        }
    except (KeyError, FileNotFoundError, ImportError):
        info["auto"] = {"available": False}
    return info
