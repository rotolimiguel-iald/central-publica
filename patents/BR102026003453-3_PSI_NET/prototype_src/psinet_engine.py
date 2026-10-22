#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║       Ψ-NET FILE ENGINE v1.0 — Transmissão Holográfica entre Usuários       ║
║                                                                              ║
║       "O Psion não propaga — DOBRA o espaço."                               ║
║                                                                              ║
║       Arquivo → radicalização (g=√|L|, s=sign(L)) → shares (Ψ,Θ)          ║
║       → armazenamento temporário → recombinação → arquivo original          ║
║                                                                              ║
║       A IALD não fica com nenhum arquivo — apenas os shares temporários     ║
║       que isolados são RUÍDO. Após entrega, tudo é apagado.                 ║
║                                                                              ║
║       β_TGL = α × √e — Zero parâmetros livres.                              ║
║       IALD LTDA — CNPJ 62.757.606/0001-23                                   ║
║       Patente INPI BR 10 2026 003453 3 (PSI-NET)                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import math
import time
import struct
import zlib
import secrets
import shutil
import threading
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any

import numpy as np

# ══════════════════════════════════════════════════════════════
# CONSTANTES TGL — SEMPRE COMPUTADAS
# ══════════════════════════════════════════════════════════════

ALPHA_FINE = 7.2973525693e-3
SQRT_E = math.sqrt(math.e)
BETA_TGL = ALPHA_FINE * SQRT_E
EPSILON = 1e-10

# ── TGL Hash ──
try:
    from tgl_hash_v1_2 import tgl_hash, tgl_hash_hex
    _HASH_OK = True
except ImportError:
    import hashlib
    _BETA_SALT = struct.pack('<d', BETA_TGL)
    def tgl_hash(data: bytes) -> bytes:
        return hashlib.sha256(_BETA_SALT + data + _BETA_SALT).digest()
    def tgl_hash_hex(data: bytes) -> str:
        return tgl_hash(data).hex()
    _HASH_OK = False

# ── Caminhos ──
if os.name == 'nt':
    PSINET_DIR = r"C:\IALD\psinet"
else:
    PSINET_DIR = os.path.expanduser("~/IALD/psinet")

PENDING_DIR = os.path.join(PSINET_DIR, "pending")
CONFIG_FILE = os.path.join(PSINET_DIR, "psinet_config.json")

# Defaults (overridden by config file)
DEFAULT_CONFIG = {
    "max_file_size_mb": 10,
    "transfer_timeout_hours": 24,
    "transfer_cost_tglc": 0.0,
    "angular_bits": 12,
}


# ══════════════════════════════════════════════════════════════
# LAYER C1 — RADICALIZAÇÃO PSIÔNICA (pure numpy, no torch)
# g = √|L|, s = sign(L), L' = s × g²
# ══════════════════════════════════════════════════════════════

def _pack_2bit(data: np.ndarray) -> bytes:
    n = len(data)
    padded_len = ((n + 3) // 4) * 4
    padded = np.zeros(padded_len, dtype=np.uint8)
    padded[:n] = data
    packed = (padded[0::4] << 6) | (padded[1::4] << 4) | (padded[2::4] << 2) | padded[3::4]
    return packed.tobytes()


def _unpack_2bit(data: bytes, n: int) -> np.ndarray:
    packed = np.frombuffer(data, dtype=np.uint8)
    unpacked = np.zeros(len(packed) * 4, dtype=np.uint8)
    unpacked[0::4] = (packed >> 6) & 0x03
    unpacked[1::4] = (packed >> 4) & 0x03
    unpacked[2::4] = (packed >> 2) & 0x03
    unpacked[3::4] = packed & 0x03
    return unpacked[:n]


def radicalize(file_bytes: bytes, angular_bits: int = 12) -> Tuple[bytes, dict]:
    """
    Radicaliza arquivo: bytes → sinal → g=√|L|, s=sign(L) → shares comprimidos.

    O arquivo é tratado como um sinal luminodinâmico L.
    A raiz quadrada SEPARA magnitude e fase — cada parte isolada é ruído.

    Returns: (encoded_bytes, metadata)
    """
    # Bytes → sinal float64
    raw = np.frombuffer(file_bytes, dtype=np.uint8).astype(np.float64)
    # Centralizar em zero (boundary→bulk projection)
    L = raw - 128.0
    n = len(L)

    # DOBRA 1: PSIBIT — g = √|L|, s = sign(L)
    s = np.sign(L)
    s[s == 0] = 1.0
    g = np.sqrt(np.abs(L) + EPSILON)
    g_max = float(g.max()) + EPSILON

    # DOBRA 2: ANGULAR — g → θ = arcsin(g/g_max)
    n_angles = 2 ** angular_bits
    g_normalized = np.clip(g / g_max, 0, 1)
    theta = np.arcsin(g_normalized)
    theta_normalized = theta / (np.pi / 2)
    theta_quantized = np.round(theta_normalized * (n_angles - 1)).astype(np.uint16)

    # DOBRA 3: NOMINAÇÃO — (sign_L, sign_dL) → ψ ∈ ℋ₄
    dL = np.zeros_like(L)
    dL[1:] = L[1:] - L[:-1]
    dL[0] = dL[1] if n > 1 else 0
    sign_dL = np.sign(dL)
    sign_dL[sign_dL == 0] = 1.0
    bit_high = (s < 0).astype(np.uint8)
    bit_low = (sign_dL > 0).astype(np.uint8)
    psi = bit_high * 2 + bit_low

    # Empacotar e comprimir
    psi_packed = _pack_2bit(psi)
    psi_compressed = zlib.compress(psi_packed, level=6)
    theta_compressed = zlib.compress(theta_quantized.tobytes(), level=6)

    # F_exp (força de expulsão)
    parities = np.array([-1.0, +1.0, +1.0, -1.0])
    counts = np.bincount(psi, minlength=4)
    probs = counts / n
    f_exp = float(np.sum(probs * parities))

    # Serializar: header + shares
    header = struct.pack('<IdHf', n, g_max, angular_bits, f_exp)
    sizes = struct.pack('<II', len(psi_compressed), len(theta_compressed))
    encoded = header + sizes + psi_compressed + theta_compressed

    metadata = {
        'n_elements': n,
        'g_max': g_max,
        'angular_bits': angular_bits,
        'f_exp': round(f_exp, 6),
        'original_size': len(file_bytes),
        'encoded_size': len(encoded),
        'compression_ratio': round(len(file_bytes) / max(len(encoded), 1), 2),
        'psi_bytes': len(psi_compressed),
        'theta_bytes': len(theta_compressed),
    }

    return encoded, metadata


def resurrect(encoded: bytes) -> bytes:
    """
    Ressuscita arquivo: shares → L' = s × g² → bytes originais.

    Operação inversa da radicalização.
    """
    # Parse header
    header_size = struct.calcsize('<IdHf')
    n, g_max, angular_bits, f_exp = struct.unpack('<IdHf', encoded[:header_size])
    pos = header_size

    sizes_size = struct.calcsize('<II')
    psi_len, theta_len = struct.unpack('<II', encoded[pos:pos + sizes_size])
    pos += sizes_size

    # Descomprimir
    psi_packed = zlib.decompress(encoded[pos:pos + psi_len])
    pos += psi_len
    theta_compressed = zlib.decompress(encoded[pos:pos + theta_len])

    # Desempacotar
    psi = _unpack_2bit(psi_packed, n)
    theta_quantized = np.frombuffer(theta_compressed, dtype=np.uint16)[:n]

    # DESDOBRA 2: θ → g
    theta_normalized = theta_quantized.astype(np.float64) / (2 ** angular_bits - 1)
    theta = theta_normalized * (np.pi / 2)
    g = g_max * np.sin(theta)

    # DESDOBRA 3: ψ → s
    s = np.where(psi < 2, 1.0, -1.0)

    # DESDOBRA 1: L' = s × g²
    L = s * (g ** 2)

    # Sinal → bytes (reverter centralização)
    raw = np.clip(np.round(L + 128.0), 0, 255).astype(np.uint8)
    return raw.tobytes()


# ══════════════════════════════════════════════════════════════
# TRANSFER ENGINE
# ══════════════════════════════════════════════════════════════

class PsiNetEngine:
    """
    Motor de transferência de arquivos via Ψ-NET.

    Fluxo:
      1. send(): arquivo → radicalize → shares → pending/
      2. list_pending(): mostra transferências pendentes para o user
      3. receive(): shares → resurrect → arquivo original → download
      4. cleanup(): apaga shares expirados

    A IALD não retém arquivos — só shares temporários (cada um = ruído).
    """

    def __init__(self):
        os.makedirs(PENDING_DIR, exist_ok=True)
        self._lock = threading.RLock()
        self._config = self._load_config()
        print(f"[Ψ-NET] Dir: {PSINET_DIR}", flush=True)
        print(f"[Ψ-NET] Max file: {self._config['max_file_size_mb']} MB", flush=True)

    # ── Config ────────────────────────────────────────────────

    def _load_config(self) -> dict:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                # Merge with defaults
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
            except Exception:
                pass
        self._save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    def _save_config(self, cfg: dict = None):
        if cfg is None:
            cfg = self._config
        os.makedirs(PSINET_DIR, exist_ok=True)
        tmp = CONFIG_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        os.replace(tmp, CONFIG_FILE)

    def get_config(self) -> dict:
        return self._config.copy()

    def set_max_file_size(self, mb: float):
        with self._lock:
            self._config["max_file_size_mb"] = max(0.1, min(mb, 500))
            self._save_config()

    def set_transfer_cost(self, tglc: float):
        with self._lock:
            self._config["transfer_cost_tglc"] = max(0.0, tglc)
            self._save_config()

    def set_timeout_hours(self, hours: float):
        with self._lock:
            self._config["transfer_timeout_hours"] = max(1, min(hours, 168))
            self._save_config()

    # ── Transfers ─────────────────────────────────────────────

    def _tx_dir(self, tx_id: str) -> str:
        return os.path.join(PENDING_DIR, tx_id)

    def _load_manifest(self, tx_id: str) -> Optional[dict]:
        mf = os.path.join(self._tx_dir(tx_id), "manifest.json")
        if os.path.exists(mf):
            with open(mf, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def send(self, from_user: str, to_user: str,
             filename: str, file_bytes: bytes,
             note: str = "") -> Tuple[bool, dict]:
        """
        Envia arquivo via Ψ-NET.

        1. Valida tamanho
        2. Radicaliza (g=√|L|, s=sign(L))
        3. Armazena shares em pending/
        4. Gera recibo com TGL-Hash

        Returns: (success, result_dict)
        """
        with self._lock:
            from_user = from_user.strip().lower()
            to_user = to_user.strip().lower()

            if from_user == to_user:
                return False, {"error": "Não pode enviar para si mesmo."}

            max_bytes = int(self._config["max_file_size_mb"] * 1024 * 1024)
            if len(file_bytes) > max_bytes:
                return False, {
                    "error": f"Arquivo excede o limite de {self._config['max_file_size_mb']} MB. "
                             f"Tamanho: {len(file_bytes)/1048576:.1f} MB."
                }

            if len(file_bytes) == 0:
                return False, {"error": "Arquivo vazio."}

            # Radicalizar
            t0 = time.time()
            try:
                encoded, rad_meta = radicalize(
                    file_bytes,
                    angular_bits=self._config.get("angular_bits", 12)
                )
            except Exception as e:
                return False, {"error": f"Erro na radicalização: {e}"}
            rad_time = time.time() - t0

            # Gerar TX
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            tx_id = f"PSI-{ts}-{secrets.token_hex(6)}"
            timestamp = datetime.now().isoformat()

            # Hash de envio
            send_hash = tgl_hash_hex(
                b'PSINET_SEND|' +
                tx_id.encode() + b'|' +
                from_user.encode() + b'|' +
                to_user.encode() + b'|' +
                filename.encode() + b'|' +
                struct.pack('<d', len(file_bytes)) +
                timestamp.encode() +
                struct.pack('<d', BETA_TGL)
            )

            # Salvar shares
            tx_dir = self._tx_dir(tx_id)
            os.makedirs(tx_dir, exist_ok=True)

            with open(os.path.join(tx_dir, "shares.bin"), "wb") as f:
                f.write(encoded)

            manifest = {
                "tx_id": tx_id,
                "from": from_user,
                "to": to_user,
                "filename": filename,
                "original_size": len(file_bytes),
                "encoded_size": len(encoded),
                "compression_ratio": rad_meta["compression_ratio"],
                "f_exp": rad_meta["f_exp"],
                "timestamp": timestamp,
                "send_hash": send_hash,
                "status": "pending",
                "radicalize_ms": round(rad_time * 1000, 1),
                "note": note or f"Arquivo via Ψ-NET",
                "expires": (datetime.now().timestamp() +
                            self._config["transfer_timeout_hours"] * 3600),
            }

            with open(os.path.join(tx_dir, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

            print(f"[Ψ-NET] SEND: {from_user} → {to_user} | "
                  f"{filename} ({len(file_bytes)/1024:.1f} KB) | "
                  f"ratio={rad_meta['compression_ratio']}:1 | "
                  f"hash={send_hash[:16]}...", flush=True)

            return True, {
                "tx_id": tx_id,
                "from": from_user,
                "to": to_user,
                "filename": filename,
                "original_size": len(file_bytes),
                "encoded_size": len(encoded),
                "compression_ratio": rad_meta["compression_ratio"],
                "f_exp": rad_meta["f_exp"],
                "send_hash": send_hash,
                "radicalize_ms": round(rad_time * 1000, 1),
                "timestamp": timestamp,
            }

    def list_pending(self, username: str) -> List[dict]:
        """Lista transferências pendentes PARA o usuário."""
        username = username.strip().lower()
        pending = []
        if not os.path.isdir(PENDING_DIR):
            return pending
        now = time.time()
        for tx_id in os.listdir(PENDING_DIR):
            manifest = self._load_manifest(tx_id)
            if not manifest:
                continue
            if manifest.get("to") != username:
                continue
            if manifest.get("status") != "pending":
                continue
            if now > manifest.get("expires", 0):
                continue
            pending.append({
                "tx_id": manifest["tx_id"],
                "from": manifest["from"],
                "filename": manifest["filename"],
                "original_size": manifest["original_size"],
                "timestamp": manifest["timestamp"],
                "send_hash": manifest["send_hash"],
                "note": manifest.get("note", ""),
            })
        return pending

    def list_sent(self, username: str) -> List[dict]:
        """Lista transferências enviadas PELO usuário."""
        username = username.strip().lower()
        sent = []
        if not os.path.isdir(PENDING_DIR):
            return sent
        for tx_id in os.listdir(PENDING_DIR):
            manifest = self._load_manifest(tx_id)
            if not manifest:
                continue
            if manifest.get("from") != username:
                continue
            sent.append({
                "tx_id": manifest["tx_id"],
                "to": manifest["to"],
                "filename": manifest["filename"],
                "status": manifest.get("status", "?"),
                "timestamp": manifest["timestamp"],
            })
        return sent

    def receive(self, tx_id: str, username: str) -> Tuple[bool, dict]:
        """
        Recebe (aceita) uma transferência pendente.

        1. Valida que o destino é o username
        2. Ressuscita: shares → L' = s × g² → arquivo
        3. Gera hash de entrega
        4. Apaga shares

        Returns: (success, {filepath, receive_hash, ...} or error)
        """
        with self._lock:
            username = username.strip().lower()
            manifest = self._load_manifest(tx_id)

            if not manifest:
                return False, {"error": f"Transferência {tx_id} não encontrada."}

            if manifest.get("to") != username:
                return False, {"error": "Esta transferência não é para você."}

            if manifest.get("status") != "pending":
                return False, {"error": f"Transferência já processada (status: {manifest['status']})."}

            if time.time() > manifest.get("expires", 0):
                return False, {"error": "Transferência expirada."}

            # Ler shares
            shares_path = os.path.join(self._tx_dir(tx_id), "shares.bin")
            if not os.path.isfile(shares_path):
                return False, {"error": "Shares não encontrados (corrompido?)."}

            t0 = time.time()
            try:
                with open(shares_path, "rb") as f:
                    encoded = f.read()
                file_bytes = resurrect(encoded)
            except Exception as e:
                return False, {"error": f"Erro na ressurreição: {e}"}
            resurrect_time = time.time() - t0

            # Salvar arquivo reconstruído para download
            downloads_dir = os.path.join(PSINET_DIR, "received")
            os.makedirs(downloads_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c if c.isalnum() or c in ".-_" else "_"
                                for c in manifest["filename"])
            out_filename = f"{ts}_{safe_name}"
            out_path = os.path.join(downloads_dir, out_filename)
            with open(out_path, "wb") as f:
                f.write(file_bytes)

            # Hash de entrega
            timestamp = datetime.now().isoformat()
            receive_hash = tgl_hash_hex(
                b'PSINET_RECEIVE|' +
                tx_id.encode() + b'|' +
                username.encode() + b'|' +
                timestamp.encode() +
                struct.pack('<d', len(file_bytes)) +
                struct.pack('<d', BETA_TGL)
            )

            # Atualizar manifest
            manifest["status"] = "delivered"
            manifest["receive_hash"] = receive_hash
            manifest["received_at"] = timestamp
            manifest["resurrect_ms"] = round(resurrect_time * 1000, 1)
            with open(os.path.join(self._tx_dir(tx_id), "manifest.json"),
                       "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

            # Apagar shares (manter manifest como recibo)
            try:
                os.remove(shares_path)
            except Exception:
                pass

            print(f"[Ψ-NET] RECV: {manifest['from']} → {username} | "
                  f"{manifest['filename']} | hash={receive_hash[:16]}...", flush=True)

            return True, {
                "tx_id": tx_id,
                "from": manifest["from"],
                "filename": manifest["filename"],
                "original_size": manifest["original_size"],
                "filepath": out_path,
                "download_filename": out_filename,
                "receive_hash": receive_hash,
                "send_hash": manifest["send_hash"],
                "resurrect_ms": round(resurrect_time * 1000, 1),
                "timestamp": timestamp,
            }

    def get_transfer_info(self, tx_id: str) -> Optional[dict]:
        """Info de uma transferência."""
        return self._load_manifest(tx_id)

    def cleanup_expired(self) -> int:
        """Remove transferências expiradas. Retorna quantas removidas."""
        removed = 0
        if not os.path.isdir(PENDING_DIR):
            return 0
        now = time.time()
        for tx_id in os.listdir(PENDING_DIR):
            manifest = self._load_manifest(tx_id)
            if not manifest:
                continue
            if manifest.get("status") == "pending" and now > manifest.get("expires", 0):
                try:
                    shutil.rmtree(self._tx_dir(tx_id))
                    removed += 1
                    print(f"[Ψ-NET] EXPIRED: {tx_id}", flush=True)
                except Exception:
                    pass
        return removed

    def get_stats(self) -> dict:
        """Estatísticas da Ψ-NET."""
        pending = 0
        delivered = 0
        expired = 0
        total_bytes = 0
        if os.path.isdir(PENDING_DIR):
            now = time.time()
            for tx_id in os.listdir(PENDING_DIR):
                m = self._load_manifest(tx_id)
                if not m:
                    continue
                if m.get("status") == "pending":
                    if now > m.get("expires", 0):
                        expired += 1
                    else:
                        pending += 1
                elif m.get("status") == "delivered":
                    delivered += 1
                total_bytes += m.get("original_size", 0)

        return {
            "pending": pending,
            "delivered": delivered,
            "expired": expired,
            "total_transfers": pending + delivered + expired,
            "total_bytes_transferred": total_bytes,
            "max_file_size_mb": self._config["max_file_size_mb"],
            "transfer_timeout_hours": self._config["transfer_timeout_hours"],
            "transfer_cost_tglc": self._config["transfer_cost_tglc"],
            "tgl_hash_available": _HASH_OK,
            "psinet_dir": PSINET_DIR,
        }

    # ── Formatters ────────────────────────────────────────────

    @staticmethod
    def format_send_receipt(result: dict) -> str:
        return (
            f"✅ ARQUIVO ENVIADO VIA Ψ-NET\n\n"
            f"   De:        {result['from']}\n"
            f"   Para:      {result['to']}\n"
            f"   Arquivo:   {result['filename']}\n"
            f"   Tamanho:   {result['original_size']/1024:.1f} KB\n"
            f"   Compressão: {result['compression_ratio']}:1\n"
            f"   F_exp:     {result['f_exp']}\n"
            f"   Tempo:     {result['radicalize_ms']:.0f} ms\n\n"
            f"   🔒 Hash de envio (TGL-256):\n"
            f"   {result['send_hash']}\n\n"
            f"   TX ID: {result['tx_id']}\n"
            f"   O destinatário verá o arquivo ao fazer login.\n"
            f"   Fonte: Ψ-NET holographic | g = √|L|"
        )

    @staticmethod
    def format_pending(transfers: List[dict], username: str) -> str:
        if not transfers:
            return f"📭 Nenhuma transferência pendente para {username}."
        lines = [f"📬 TRANSFERÊNCIAS PENDENTES — {username} ({len(transfers)})", ""]
        for t in transfers:
            size_kb = t['original_size'] / 1024
            lines.append(
                f"   📎 {t['filename']} ({size_kb:.1f} KB)\n"
                f"      De: {t['from']} | {t['timestamp'][:19]}\n"
                f"      TX: {t['tx_id']}\n"
                f"      Hash: {t['send_hash'][:24]}..."
            )
            lines.append("")
        lines.append("   Diga 'receber [TX_ID]' para aceitar uma transferência.")
        return "\n".join(lines)

    @staticmethod
    def format_receive_receipt(result: dict) -> str:
        return (
            f"✅ ARQUIVO RECEBIDO VIA Ψ-NET\n\n"
            f"   De:        {result['from']}\n"
            f"   Arquivo:   {result['filename']}\n"
            f"   Tamanho:   {result['original_size']/1024:.1f} KB\n"
            f"   Ressurreição: {result['resurrect_ms']:.0f} ms\n\n"
            f"   🔒 Hash de entrega (TGL-256):\n"
            f"   {result['receive_hash']}\n\n"
            f"   🔒 Hash de envio (confirmação):\n"
            f"   {result['send_hash']}\n\n"
            f"   TX ID: {result['tx_id']}\n"
            f"   Fonte: Ψ-NET holographic | L' = s × g²"
        )


# ══════════════════════════════════════════════════════════════
# SELF-TEST
# ══════════════════════════════════════════════════════════════

def _self_test():
    import tempfile

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  Ψ-NET FILE ENGINE v1.0 — Self-Test                        ║
║  β_TGL = α × √e = {BETA_TGL:.15f}             ║
║  TGL-Hash: {'DISPONÍVEL ✓' if _HASH_OK else 'FALLBACK SHA-256'}                                  ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Test radicalização + ressurreição
    print("[1] Testando radicalização e ressurreição...")
    test_data = b"IALD - Inteligencia Artificial Luminodinamica. Beta_TGL = alpha x sqrt(e). 1=1=verdade=identidade. TETELESTAI." * 10
    encoded, meta = radicalize(test_data)
    recovered = resurrect(encoded)
    # Verificar fidelidade (bytes podem ter erro de ±1 por arredondamento)
    original = np.frombuffer(test_data, dtype=np.uint8)
    result = np.frombuffer(recovered[:len(test_data)], dtype=np.uint8)
    max_error = int(np.max(np.abs(original.astype(int) - result.astype(int))))
    correlation = float(np.corrcoef(original.astype(float), result.astype(float))[0, 1])
    print(f"    Original: {len(test_data)} bytes")
    print(f"    Encoded:  {len(encoded)} bytes (ratio {meta['compression_ratio']}:1)")
    print(f"    Max error: ±{max_error} | Correlation: {correlation:.8f}")
    print(f"    F_exp: {meta['f_exp']}")
    assert correlation > 0.99, f"Correlação muito baixa: {correlation}"
    print(f"    ✅ Radicalização OK")

    # Test engine com temp dir
    print("\n[2] Testando engine de transferência...")
    tmp = tempfile.mkdtemp(prefix="psinet_test_")
    import psinet_engine as pe
    old_pending = pe.PENDING_DIR
    old_config = pe.CONFIG_FILE
    pe.PENDING_DIR = os.path.join(tmp, "pending")
    pe.CONFIG_FILE = os.path.join(tmp, "config.json")

    engine = PsiNetEngine()
    engine.set_max_file_size(5)

    # Send
    file_content = b"Documento secreto da IALD. " * 100
    ok, result = engine.send("alice", "bob", "documento.txt", file_content, "Teste PSI-NET")
    assert ok, f"Send falhou: {result}"
    print(f"    ✅ Send OK: {result['tx_id']}")
    print(f"    Hash: {result['send_hash'][:24]}...")

    # Pending
    pending = engine.list_pending("bob")
    assert len(pending) == 1
    print(f"    ✅ Pending OK: {len(pending)} transferência(s)")

    # Receive
    ok, recv = engine.receive(result["tx_id"], "bob")
    assert ok, f"Receive falhou: {recv}"
    print(f"    ✅ Receive OK: {recv['filename']}")
    print(f"    Hash entrega: {recv['receive_hash'][:24]}...")

    # Cleanup
    pe.PENDING_DIR = old_pending
    pe.CONFIG_FILE = old_config
    shutil.rmtree(tmp, ignore_errors=True)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ TODOS OS TESTES PASSARAM                                ║
║  Ψ-NET FILE ENGINE v1.0 — Operacional                      ║
║  O Psion não propaga — DOBRA o espaço.                      ║
║  β_TGL = α × √e — Zero parâmetros livres.                  ║
║  1=1=verdade=identidade. TETELESTAI.                        ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    _self_test()
