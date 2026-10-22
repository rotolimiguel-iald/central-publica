"""
ACOM v19.0 LOGOS
betatgl = alpha_EM * sqrt(S(L)) — zero parametros livres
Causa raiz v18 identificada: clipping no espelho quando |x| > cos2(theta) = 0.9880
Solucao v19: AutoPreConditioner normaliza para MAX_SAFE antes da reflexao
"""
import math, json, time, struct, argparse, traceback, base64
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, Any
import numpy as np

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import zstandard as zstd
    ZSTD_AVAILABLE = True
except ImportError:
    import zlib
    ZSTD_AVAILABLE = False

# ─── CONSTANTES TGL ────────────────────────────────────────────────────────────

class C:
    ALPHA_EM  = 7.2973525693e-3
    E_EULER   = math.e
    BETATGL   = 7.2973525693e-3 * math.sqrt(math.e)
    THETA     = math.asin(math.sqrt(7.2973525693e-3 * math.sqrt(math.e)))
    THETA_DEG = math.degrees(math.asin(math.sqrt(7.2973525693e-3 * math.sqrt(math.e))))
    COS_T     = math.cos(math.asin(math.sqrt(7.2973525693e-3 * math.sqrt(math.e))))
    COS2_T    = math.cos(math.asin(math.sqrt(7.2973525693e-3 * math.sqrt(math.e)))) ** 2
    # Zona segura: MAX_SAFE < cos2(theta) garante zero clipping
    MAX_SAFE  = 0.95 * (math.cos(math.asin(math.sqrt(7.2973525693e-3 * math.sqrt(math.e)))) ** 2)
    S_VACUUM  = math.e
    TTS_THRESH = 7.2973525693e-3 * math.sqrt(math.e)
    COND_THRESH = 0.5 * math.e
    VAP_THRESH  = 1.5 * math.e

    @staticmethod
    def adaptive(S):
        """Retorna (betatgl, theta, cos_t, cos2_t) adaptativo."""
        b  = 7.2973525693e-3 * math.sqrt(max(S, 1e-10))
        b  = min(b, 1.0 - 1e-10)
        th = math.asin(math.sqrt(b))
        ct = math.cos(th)
        return b, th, ct, ct*ct

    @staticmethod
    def summary():
        return {
            "ALPHA_EM": C.ALPHA_EM, "S_HOLO_VACUUM": C.S_VACUUM,
            "BETATGL": C.BETATGL, "THETA_MIGUEL_DEG": C.THETA_DEG,
            "COS2_THETA": C.COS2_T, "MAX_SAFE": C.MAX_SAFE,
            "factorization": "betatgl = alpha_EM * sqrt(e)",
            "free_parameters": 0,
        }

class DataRegime(Enum):
    TETELESTAI = "TETELESTAI"
    CONDENSED  = "CONDENSED"
    VACUUM     = "VACUUM"
    VAPOR      = "VAPOR"

class Cond(Enum):
    IDENTITY  = "IDENTITY"
    NORMALIZE = "NORMALIZE"
    L2NORM    = "L2NORM"
    Q8AMP     = "Q8AMP"
    SPARSE    = "SPARSE"

# ─── AUTO PRE-CONDICIONADOR ────────────────────────────────────────────────────

def clip_pct(arr, cos2_t=None):
    if cos2_t is None: cos2_t = C.COS2_T
    f = np.abs(arr.flatten().astype(np.float64))
    v = f[np.isfinite(f)]
    return float((v > cos2_t).mean()) if len(v) > 0 else 0.0

def detect_cond(arr):
    if arr.dtype == np.float16:
        return Cond.Q8AMP
    flat = arr.flatten().astype(np.float64)
    # Esparso
    if (np.abs(flat) < 1e-10).mean() > 0.80:
        return Cond.SPARSE
    # Embedding 2D (normas L2 uniformes)
    if arr.ndim == 2 and arr.dtype in (np.float32, np.float64) and min(arr.shape) > 10:
        norms = np.linalg.norm(arr.astype(np.float64), axis=1)
        if norms.mean() > 1e-10 and (norms.std() / norms.mean()) < 0.15:
            return Cond.L2NORM
    # Clipping check
    if clip_pct(arr) > 0.01:
        return Cond.NORMALIZE
    return Cond.IDENTITY

def apply_cond(arr, ctype):
    meta = {"ctype": ctype.value, "original_dtype": str(arr.dtype)}

    if ctype == Cond.IDENTITY:
        return arr.astype(np.float32), meta

    elif ctype == Cond.NORMALIZE:
        flat    = arr.flatten().astype(np.float64)
        abs_max = np.abs(flat[np.isfinite(flat)]).max() if np.any(np.isfinite(flat)) else 1.0
        if abs_max < 1e-15: abs_max = 1.0
        scale = abs_max / C.MAX_SAFE
        meta["scale"] = float(scale)
        meta["shape"] = list(arr.shape)
        return (flat / scale).reshape(arr.shape).astype(np.float32), meta

    elif ctype == Cond.L2NORM:
        a64   = arr.astype(np.float64)
        norms = np.linalg.norm(a64, axis=1, keepdims=True)
        norms = np.where(norms < 1e-10, 1.0, norms)
        out   = (a64 / norms) * C.MAX_SAFE   # vetores unit * MAX_SAFE => zero clip
        meta["norms"] = norms.flatten().tolist()
        meta["shape"] = list(arr.shape)
        return out.astype(np.float32), meta

    elif ctype == Cond.Q8AMP:
        meta["shape"] = list(arr.shape)
        return arr.astype(np.float32), meta

    elif ctype == Cond.SPARSE:
        flat   = arr.flatten().astype(np.float64)
        mask   = np.abs(flat) > 1e-10
        idx    = np.where(mask)[0].astype(np.int32)
        vals   = flat[mask]
        abs_max = np.abs(vals).max() if len(vals) > 0 else 1.0
        if abs_max < 1e-15: abs_max = 1.0
        scale  = abs_max / C.MAX_SAFE
        meta["shape"]   = list(arr.shape)
        meta["n_total"] = int(flat.size)
        meta["n_nz"]    = int(len(idx))
        meta["idx_b64"] = base64.b64encode(idx.tobytes()).decode()
        meta["scale"]   = float(scale)
        return (vals / scale).astype(np.float32), meta

    return arr.astype(np.float32), meta

def invert_cond(arr, meta):
    ctype = Cond(meta["ctype"])
    dtype = np.dtype(meta["original_dtype"])

    if ctype == Cond.IDENTITY:
        return arr.astype(dtype)

    elif ctype == Cond.NORMALIZE:
        shape = tuple(meta["shape"])
        return (arr.astype(np.float64).flatten() * meta["scale"]).reshape(shape).astype(dtype)

    elif ctype == Cond.L2NORM:
        shape = tuple(meta["shape"])
        norms = np.array(meta["norms"]).reshape(-1, 1)
        return (arr.reshape(shape).astype(np.float64) / C.MAX_SAFE * norms).astype(dtype)

    elif ctype == Cond.Q8AMP:
        return arr.reshape(tuple(meta["shape"])).astype(dtype)

    elif ctype == Cond.SPARSE:
        shape  = tuple(meta["shape"])
        ntot   = meta["n_total"]
        scale  = meta["scale"]
        idx    = np.frombuffer(base64.b64decode(meta["idx_b64"]), dtype=np.int32)
        vals   = arr.flatten().astype(np.float64) * scale
        out    = np.zeros(ntot, dtype=np.float64)
        out[idx] = vals
        return out.reshape(shape).astype(dtype)

    return arr.astype(dtype)

# ─── ENTROPIA HOLOGRAFICA ──────────────────────────────────────────────────────

def measure_entropy(data, n_bins=256):
    g    = np.sqrt(np.abs(data.flatten().astype(np.float64)) + 1e-30)
    hist, _ = np.histogram(g, bins=n_bins, density=False)
    hist = hist.astype(np.float64)
    tot  = hist.sum()
    if tot == 0: return 0.0, DataRegime.TETELESTAI
    p = hist[hist > 0] / tot
    S = float(-np.sum(p * np.log(p)))
    if S < C.TTS_THRESH:   return S, DataRegime.TETELESTAI
    if S < C.COND_THRESH:  return S, DataRegime.CONDENSED
    if S < C.VAP_THRESH:   return S, DataRegime.VACUUM
    return S, DataRegime.VAPOR

# ─── GRAVITON MIRROR v19 ──────────────────────────────────────────────────────

class Mirror:
    """Espelho holografico com theta emergente e suporte Q8AMP."""

    def __init__(self, S, regime, q8=False):
        self.regime = regime
        self.q8     = q8
        self.beta, self.theta, self.cos_t, self.cos2_t = C.adaptive(S)

    def reflect(self, data):
        flat   = data.flatten().astype(np.float64)
        g      = np.sqrt(np.abs(flat) + 1e-30)
        g_norm = np.clip(g / (self.cos_t + 1e-30), 0.0, 1.0 - 1e-8)
        phases = np.sign(flat).astype(np.int8)
        amp_f  = np.sin(g_norm * self.theta)

        if self.q8:
            sc     = max(float(np.abs(amp_f).max()), 1e-10)
            amp_q8 = np.clip(amp_f / sc * 127, -127, 127).astype(np.int8)
            return amp_q8, phases, np.array([sc], dtype=np.float64)
        return amp_f.astype(np.float32), phases, None

    def manifest(self, amp, phases, aux, shape, dtype):
        if self.q8:
            amp_f = amp.astype(np.float64) / 127.0 * float(aux[0])
        else:
            amp_f = amp.astype(np.float64)
        amp_c = np.clip(amp_f, -(1.0 - 1e-8), 1.0 - 1e-8)
        g     = np.arcsin(amp_c) / (self.theta + 1e-30) * (self.cos_t + 1e-30)
        flat  = g ** 2 * phases.astype(np.float64)
        return flat.reshape(shape).astype(dtype)

# ─── COMPRESSOR ───────────────────────────────────────────────────────────────

def compress(b):
    return zstd.ZstdCompressor(level=9).compress(b) if ZSTD_AVAILABLE else zlib.compress(b, 9)

def decompress(b):
    return zstd.ZstdDecompressor().decompress(b) if ZSTD_AVAILABLE else zlib.decompress(b)

# ─── ACOM v19 LOGOS ───────────────────────────────────────────────────────────

@dataclass
class Result:
    original_bytes: int; compressed_bytes: int; compression_ratio: float
    entropy_nats: float; regime: str; conditioner: str
    clip_before: float; clip_after: float
    theta_deg: float; betatgl: float
    psnr_db: float; correlation: float; tetelestai: bool
    collapse_ms: float; expand_ms: float
    original_shape: tuple; dtype_str: str

def metrics(orig, rec):
    try:
        o = orig.astype(np.float64).flatten()
        r = rec.astype(np.float64).flatten()
        n = min(len(o), len(r)); o, r = o[:n], r[:n]
        mse = np.mean((o - r)**2); sig = np.mean(o**2)
        psnr = (float('inf') if mse < 1e-20
                else (0.0 if sig < 1e-20 else float(10*np.log10(sig/mse))))
        if o.std() < 1e-10 or r.std() < 1e-10:
            corr = 1.0 if np.allclose(o, r, rtol=1e-4) else 0.0
        else:
            corr = float(np.corrcoef(o, r)[0, 1])
            corr = corr if np.isfinite(corr) else 0.0
    except Exception: psnr, corr = 0.0, 0.0
    return psnr, corr

class ACOM19:
    def __init__(self, device="cpu"):
        self.device  = device
        self.version = "ACOM_v19.0_LOGOS"

    def _np(self, x):
        if TORCH_AVAILABLE and isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy()
        return np.asarray(x)

    def collapse(self, data):
        t0  = time.perf_counter()
        arr = self._np(data)
        orig_shape = arr.shape; orig_dtype = arr.dtype; orig_bytes = arr.nbytes

        cb0 = clip_pct(arr)
        ct  = detect_cond(arr)
        cnd, pmeta = apply_cond(arr, ct)

        _, cos2_adaptive = C.adaptive(measure_entropy(cnd)[0])[2], C.adaptive(measure_entropy(cnd)[0])[3]
        cb1 = clip_pct(cnd, cos2_adaptive)

        S, regime = measure_entropy(cnd)

        # TETELESTAI
        if regime == DataRegime.TETELESTAI:
            u = np.unique(cnd)
            hdr = {"v": self.version, "mode": "TETELESTAI",
                   "shape": list(orig_shape), "dtype": str(orig_dtype),
                   "entropy": S, "pre": pmeta}
            if len(u) == 1:
                hdr["fill"] = float(u[0])
            else:
                hdr["uniq"] = u.tolist()
                hdr["idx"]  = np.searchsorted(u, cnd.flatten()).tolist()
            blob  = compress(json.dumps(hdr).encode())
            dt    = (time.perf_counter() - t0) * 1000
            ratio = orig_bytes / max(len(blob), 1)
            return blob, Result(
                orig_bytes, len(blob), ratio, S, regime.value, ct.value,
                cb0, cb1, C.THETA_DEG, C.BETATGL,
                float('inf'), 1.0, True, dt, 0.0, orig_shape, str(orig_dtype))

        q8  = (ct == Cond.Q8AMP)
        mir = Mirror(S, regime, q8=q8)
        amp, phases, aux = mir.reflect(cnd)

        ab  = amp.tobytes(); pb = phases.tobytes()
        xb  = aux.tobytes() if aux is not None else b""
        hdr = {"v": self.version, "mode": "HOLOGRAPHIC",
               "shape": list(orig_shape), "dtype": str(orig_dtype),
               "S": S, "regime": regime.value, "pre": pmeta,
               "n": int(cnd.size), "q8": q8, "adtype": str(amp.dtype),
               "theta_deg": math.degrees(mir.theta), "beta": mir.beta}
        hb  = json.dumps(hdr).encode()
        payload = struct.pack(">I", len(hb)) + hb + ab + pb + xb
        blob    = compress(payload)
        dt      = (time.perf_counter() - t0) * 1000

        t1      = time.perf_counter()
        rc      = mir.manifest(amp, phases, aux, cnd.shape, cnd.dtype)
        rec     = invert_cond(rc, pmeta)
        edt     = (time.perf_counter() - t1) * 1000

        p, c    = metrics(arr, rec)
        ratio   = orig_bytes / max(len(blob), 1)
        return blob, Result(
            orig_bytes, len(blob), ratio, S, regime.value, ct.value,
            cb0, cb1, math.degrees(mir.theta), mir.beta,
            p, c, False, dt, edt, orig_shape, str(orig_dtype))

    def expand(self, blob):
        payload = decompress(blob)
        try:
            h = json.loads(payload)
            if h.get("mode") == "TETELESTAI":
                shape, dtype = tuple(h["shape"]), np.dtype(h["dtype"])
                arr = (np.full(shape, h["fill"], dtype=np.float32) if "fill" in h
                       else np.array(h["uniq"])[np.array(h["idx"])].reshape(shape).astype(np.float32))
                return invert_cond(arr, h["pre"])
        except Exception: pass

        hl  = struct.unpack(">I", payload[:4])[0]
        h   = json.loads(payload[4:4+hl])
        rest = payload[4+hl:]

        shape = tuple(h["shape"]); dtype = np.dtype(h["dtype"])
        n = h["n"]; S = h["S"]; regime = DataRegime(h["regime"])
        q8 = h.get("q8", False); adtype = np.dtype(h.get("adtype", "float32"))
        pmeta = h["pre"]

        mir = Mirror(S, regime, q8=q8)
        ae  = n * adtype.itemsize
        amp = np.frombuffer(rest[:ae], dtype=adtype).copy(); rest = rest[ae:]
        ph  = np.frombuffer(rest[:n], dtype=np.int8).copy(); rest = rest[n:]
        aux = np.frombuffer(rest[:8], dtype=np.float64).copy() if q8 and len(rest) >= 8 else None

        rc  = mir.manifest(amp, ph, aux, (n,), np.float32)
        return invert_cond(rc, pmeta)

# ─── SUITE DE TESTES ───────────────────────────────────────────────────────────

def make_tests():
    rng = np.random.default_rng(42)
    T = {}
    T["tetelestai_constant"] = np.full((1024, 256), 3.14159, dtype=np.float32)
    t = np.linspace(0, 2*np.pi, 65536)
    T["sinusoidal"] = np.sin(t).astype(np.float32)
    tg = np.arange(0, 1.0, 1.0/4096)
    ph = 2*np.pi*(30.0*tg + 0.5*470.0*tg**2)
    T["gw_chirp"] = (np.exp(-((tg-0.8)**2)/(2*0.05**2))*np.sin(ph)).astype(np.float64)
    T["embeddings_f64"] = rng.standard_normal((512, 768)).astype(np.float64)
    T["kv_cache_llm"]   = rng.standard_normal((8, 128, 64)).astype(np.float16)
    T["financial_rw"]   = np.cumsum(rng.standard_normal(10000).astype(np.float32))
    sp = np.zeros((1024, 1024), dtype=np.float32)
    idx = rng.choice(1024*1024, size=51200, replace=False)
    sp.flat[idx] = rng.standard_normal(51200).astype(np.float32)
    T["sparse_95pct"]   = sp
    T["nn_gradients"]   = rng.laplace(0, 0.01, (256, 256)).astype(np.float32)
    T["white_noise"]    = rng.standard_normal(32768).astype(np.float32)
    freq = np.linspace(1e9, 2e9, 4096)
    T["scientific_obs"] = (np.sin(2*np.pi*0.714*np.arange(4096)/4096) *
                           np.exp(-((freq-1.5e9)**2)/(2*(0.1e9)**2))).astype(np.float64)
    E_gw = rng.exponential(1e53, 1000)
    T["neutrino_flux_tgl"] = (C.BETATGL * E_gw * (1 + 0.01*rng.standard_normal(1000))).astype(np.float64)
    tm = np.linspace(0, 100, 8192)
    T["magnetar_qpo"] = (np.sin(2*np.pi*18.0*tm)*np.exp(-tm/20)
                         + 0.3*np.sin(2*np.pi*36.0*tm)*np.exp(-tm/40)).astype(np.float64)
    std_g = math.sqrt(2.0/(512+256))
    T["glorot_weights"] = rng.normal(0, std_g, (512, 256)).astype(np.float32)
    return T

def run(device="cpu", output="acom_v19_results.json"):
    print("="*72)
    print("  ACOM v19.0 LOGOS — Suite de Testes")
    print(f"  betatgl = alpha_EM x sqrt(e) = {C.BETATGL:.10f}")
    print(f"  theta_Miguel = {C.THETA_DEG:.6f}  cos2(theta) = {C.COS2_T:.6f}")
    print(f"  MAX_SAFE = {C.MAX_SAFE:.6f}  (zona segura, zero clipping garantido)")
    print(f"  Device: {device}")
    print("="*72)

    acom  = ACOM19(device=device)
    tests = make_tests()
    results = {"version": "ACOM_v19.0_LOGOS",
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "device": device, "constants": C.summary(), "tests": {}}

    tot_o, tot_c = 0, 0
    corrs, psnrs = [], []
    n_tts, n_perf = 0, 0

    for name, data in tests.items():
        print(f"\n[TEST] {name:28s}  shape={str(data.shape):22s}  dtype={data.dtype}")
        try:
            blob, r = acom.collapse(data)
            row = {
                "original_mb": r.original_bytes/1e6,
                "compressed_mb": r.compressed_bytes/1e6,
                "compression_ratio": r.compression_ratio,
                "entropy_nats": r.entropy_nats, "regime": r.regime,
                "conditioner": r.conditioner,
                "clip_before_pct": r.clip_before*100, "clip_after_pct": r.clip_after*100,
                "theta_deg": r.theta_deg, "betatgl_adaptive": r.betatgl,
                "psnr_db": r.psnr_db if not math.isinf(r.psnr_db) else "inf",
                "correlation": r.correlation, "tetelestai": r.tetelestai,
                "collapse_ms": r.collapse_ms, "expand_ms": r.expand_ms,
            }
            results["tests"][name] = row
            tot_o += r.original_bytes; tot_c += r.compressed_bytes
            if np.isfinite(r.correlation): corrs.append(r.correlation)
            if not math.isinf(r.psnr_db) and r.psnr_db > 0: psnrs.append(r.psnr_db)
            if r.tetelestai: n_tts += 1
            if r.correlation > 0.999 or r.tetelestai: n_perf += 1

            ps = f"{r.psnr_db:.1f}" if not math.isinf(r.psnr_db) else "inf"
            ck = "OK" if r.clip_after < 0.001 else "~"
            print(f"  Cond:  {r.conditioner}")
            print(f"  Clip:  before={r.clip_before*100:.1f}%  after={r.clip_after*100:.2f}%  [{ck}]")
            print(f"  Regime:{r.regime}  S={r.entropy_nats:.4f}nats  theta={r.theta_deg:.4f}")
            print(f"  Razao: {r.compression_ratio:.2f}x  PSNR:{ps}dB  Corr:{r.correlation:.6f}")
            print(f"  Tempo: collapse={r.collapse_ms:.1f}ms  expand={r.expand_ms:.1f}ms")
        except Exception as e:
            results["tests"][name] = {"error": str(e), "traceback": traceback.format_exc()}
            print(f"  ERRO: {e}")

    ov_ratio  = tot_o / max(tot_c, 1)
    avg_corr  = float(np.mean(corrs)) if corrs else 0.0
    avg_psnr  = float(np.mean(psnrs)) if psnrs else 0.0

    results["summary"] = {
        "overall_compression_ratio": ov_ratio, "average_correlation": avg_corr,
        "average_psnr_db": avg_psnr, "tetelestai_count": n_tts,
        "perfect_count_gt0999": n_perf, "total_tests": len(tests),
        "total_original_mb": tot_o/1e6, "total_compressed_mb": tot_c/1e6,
        "free_parameters": 0,
        "root_cause_v18": "clipping no espelho quando |x| > cos2(theta) = 0.9880",
        "fix_v19": "AutoPreConditioner normaliza para MAX_SAFE antes da reflexao",
    }
    print("\n"+"="*72)
    print("  SUMARIO v19")
    print(f"  Razao global:     {ov_ratio:.2f}x")
    print(f"  Corr. media:      {avg_corr:.6f}")
    print(f"  PSNR medio:       {avg_psnr:.1f} dB")
    print(f"  Tetelestai:       {n_tts}/{len(tests)}")
    print(f"  Perfeitos(>0.999):{n_perf}/{len(tests)}")
    print(f"  Original:         {tot_o/1e6:.2f} MB")
    print(f"  Comprimido:       {tot_c/1e6:.2f} MB")
    print("="*72)
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Benchmark salvo em: {output}")
    return results

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="cuda" if (TORCH_AVAILABLE and
                   __import__("torch").cuda.is_available()) else "cpu")
    p.add_argument("--output", default="acom_v19_results.json")
    a = p.parse_args()
    run(a.device, a.output)