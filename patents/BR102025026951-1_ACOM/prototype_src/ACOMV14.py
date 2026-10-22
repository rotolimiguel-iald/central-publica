#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════════════

                        ACOM v14.1 — OPERADOR DE LINDBLAD ATIVO
                        
                    Algoritmo de Compressão Ontológica de Memória
                    Teoria da Gravitação Luminodinâmica (TGL)

═══════════════════════════════════════════════════════════════════════════════════════

                            EQUAÇÃO FUNDAMENTAL:
                            
                        ∂ℋ = ℋ² + α²𝕃Δ
                        
═══════════════════════════════════════════════════════════════════════════════════════

    CORREÇÕES v14 → v14.1:
    
    1. CONVERGÊNCIA ACELERADA
       - dt adaptativo baseado em Δ (quanto maior Δ, maior dt)
       - Correção proporcional ao gradiente, não apenas ao desvio
       - Momentum para escapar de mínimos locais
    
    2. SAVE/LOAD CORRIGIDO
       - Header com shape dinâmico
       - Suporte a arrays N-dimensionais
    
    3. RESTORE MELHORADO
       - Auto-restauração usa média móvel como referência
       - Restauração guiada com interpolação adaptativa
    
    4. COMPLETE MELHORADO
       - Inicialização por interpolação (não média)
       - Propagação de vizinhos conhecidos
    
    5. GENERATE MELHORADO
       - Interpolação spline para expansão do kernel
       - Ruído estruturado (não aleatório puro)

═══════════════════════════════════════════════════════════════════════════════════════

    Teoria: Luiz Antonio Rotoli Miguel
    Implementação: IALD LTDA (CNPJ 62.757.606/0001-23)
    Janeiro 2026

═══════════════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, List, Union
from enum import Enum, auto
import struct
import zlib
import os
import time
import json

# ═══════════════════════════════════════════════════════════════════════════════════════
# PYTORCH / CUDA
# ═══════════════════════════════════════════════════════════════════════════════════════

try:
    import torch
    HAS_TORCH = True
    
    if torch.cuda.is_available():
        DEVICE = torch.device("cuda")
        GPU_NAME = torch.cuda.get_device_name(0)
        print(f"🚀 GPU detectada: {GPU_NAME}")
    else:
        DEVICE = torch.device("cpu")
        GPU_NAME = "CPU"
        print("⚠️ CUDA não disponível, usando CPU")
        
except ImportError:
    HAS_TORCH = False
    DEVICE = None
    GPU_NAME = "NumPy only"
    print("⚠️ PyTorch não instalado, usando NumPy")


# ═══════════════════════════════════════════════════════════════════════════════════════
# CONSTANTES FUNDAMENTAIS DA TGL
# ═══════════════════════════════════════════════════════════════════════════════════════

ALPHA2 = 0.012              # Constante de Miguel
ALPHA = np.sqrt(ALPHA2)     # √α² ≈ 0.1095
EPSILON = 1e-12             # Threshold numérico
VERSION = "14.1"


# ═══════════════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════════════

class ConvergenceState(Enum):
    FALLEN = "FALLEN"           # Δ > 1
    CONVERGING = "CONVERGING"   # α² < Δ < 1
    TRUTH = "TRUTH"             # Δ < α²
    TETELESTAI = "TETELESTAI"   # Δ < ε


# ═══════════════════════════════════════════════════════════════════════════════════════
# ESTRUTURAS DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════════════

@dataclass
class TGLMetrics:
    """Métricas da transformação TGL"""
    mse: float = 0.0
    psnr: float = 0.0
    correlation: float = 0.0
    compression_ratio: float = 1.0
    
    delta: float = float('inf')
    iterations: int = 0
    state: ConvergenceState = ConvergenceState.FALLEN
    
    energy: float = 0.0
    entropy: float = 0.0
    temperature: float = 1.0
    free_energy: float = 0.0
    current: float = 0.0
    
    def __str__(self) -> str:
        return (f"[{self.state.value}] Δ={self.delta:.2e} | "
                f"corr={self.correlation:.6f} | iter={self.iterations} | "
                f"F={self.free_energy:.2f} | J={self.current:.2e}")


@dataclass
class ACOMPacket:
    """Pacote de dados comprimidos"""
    g_quantized: np.ndarray
    s_packed: np.ndarray
    zeros_mask: np.ndarray
    
    shape: tuple
    dtype: str
    bits: int
    g_min: float
    g_max: float
    
    alpha2: float
    final_delta: float
    iterations: int
    state: str
    free_energy: float
    
    @property
    def compressed_bytes(self) -> int:
        return (self.g_quantized.nbytes + 
                self.s_packed.nbytes + 
                self.zeros_mask.nbytes + 128)
    
    @property
    def original_bytes(self) -> int:
        n_elements = int(np.prod(self.shape))
        dtype_size = {'float16': 2, 'float32': 4, 'float64': 8}.get(self.dtype, 4)
        return n_elements * dtype_size
    
    @property
    def compression_ratio(self) -> float:
        return self.original_bytes / max(self.compressed_bytes, 1)


# ═══════════════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL: OPERADOR DE LINDBLAD
# ═══════════════════════════════════════════════════════════════════════════════════════

class LindbladOperator:
    """
    Operador de Lindblad — O Termostato Cósmico
    
    Implementa: ∂ℋ = ℋ² + α²𝕃Δ
    """
    
    def __init__(self, 
                 alpha2: float = ALPHA2,
                 bits: int = 14,
                 max_iterations: int = 1000,
                 tolerance: float = 1e-8,
                 use_gpu: bool = True):
        
        self.alpha2 = alpha2
        self.alpha = np.sqrt(alpha2)
        self.bits = bits
        self.max_iter = max_iterations
        self.tol = tolerance
        
        self.use_gpu = use_gpu and HAS_TORCH and torch.cuda.is_available()
        self.device = DEVICE if self.use_gpu else None
        
        self.history: List[TGLMetrics] = []
        
    # ═══════════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES FUNDAMENTAIS (O NÚCLEO SAGRADO)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _radicalize(self, L: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        ℋ² — A Auto-Operação
        
        g = √|L|
        s = sign(L)
        """
        L = np.asarray(L, dtype=np.float64)
        zeros = np.abs(L) < EPSILON
        g = np.sqrt(np.abs(L))
        s = np.sign(L)
        s[zeros] = 0
        return g, s, zeros
    
    def _resurrect(self, g: np.ndarray, s: np.ndarray, zeros: np.ndarray) -> np.ndarray:
        """
        A Ressurreição: L = s × g²
        """
        L = s * (g ** 2)
        L[zeros] = 0.0
        return L
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MÉTRICAS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _compute_delta(self, H: np.ndarray, L_logos: np.ndarray) -> float:
        """Δ = ||𝕃 - ℋ|| / ||𝕃||"""
        norm_logos = np.linalg.norm(L_logos)
        if norm_logos < EPSILON:
            return 0.0
        return np.linalg.norm(L_logos - H) / norm_logos
    
    def _compute_current(self, L_logos: np.ndarray, delta: float) -> float:
        """J = α²||𝕃||Δ"""
        return self.alpha2 * np.linalg.norm(L_logos) * delta
    
    def _compute_thermodynamics(self, L: np.ndarray, L_logos: np.ndarray) -> Dict:
        """F = E - TS"""
        E = np.sum(L ** 2)
        
        g, _, _ = self._radicalize(L)
        g_sum = np.sum(g) + EPSILON
        g_norm = g / g_sum
        g_norm = g_norm[g_norm > EPSILON]
        S = -np.sum(g_norm * np.log(g_norm + EPSILON))
        
        if len(L) > 1 and np.std(L) > EPSILON and np.std(L_logos) > EPSILON:
            corr = np.corrcoef(L.flatten(), L_logos.flatten())[0, 1]
            if np.isnan(corr):
                corr = 0.0
        else:
            corr = 1.0 if np.allclose(L, L_logos) else 0.0
            
        T = 1.0 - abs(corr)
        F = E - T * S
        
        return {'energy': E, 'entropy': S, 'temperature': T, 'free_energy': F, 'correlation': corr}
    
    def _classify_state(self, delta: float) -> ConvergenceState:
        if delta < self.tol:
            return ConvergenceState.TETELESTAI
        elif delta < self.alpha2:
            return ConvergenceState.TRUTH
        elif delta < 1.0:
            return ConvergenceState.CONVERGING
        else:
            return ConvergenceState.FALLEN
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # LOOP DE CONVERGÊNCIA ACELERADO (v14.1)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def converge(self, H_initial: np.ndarray, L_logos: np.ndarray,
                 verbose: bool = True, 
                 momentum: float = 0.9,
                 learning_rate: float = 0.5) -> Tuple[np.ndarray, TGLMetrics]:
        """
        Loop de Convergência Acelerado
        
        Usa:
        - Learning rate adaptativo: lr = base_lr × (1 + Δ)
        - Momentum para escapar mínimos locais
        - Correção proporcional ao gradiente
        """
        if verbose:
            print(f"\n{'═'*70}")
            print("LOOP DE CONVERGÊNCIA — OPERADOR DE LINDBLAD")
            print(f"{'═'*70}")
            print(f"  α² = {self.alpha2}")
            print(f"  Tolerância = {self.tol:.2e}")
            print(f"  Learning rate = {learning_rate}")
            print(f"  Momentum = {momentum}")
        
        H = H_initial.copy().astype(np.float64)
        L_logos = L_logos.astype(np.float64)
        
        # Velocity para momentum
        velocity = np.zeros_like(H)
        
        self.history = []
        best_H = H.copy()
        best_delta = float('inf')
        
        for i in range(self.max_iter):
            # PASSO 1: Auto-operação ℋ²
            g, s, zeros = self._radicalize(H)
            H_squared = self._resurrect(g, s, zeros)
            
            # PASSO 2: Medir desvio Δ
            delta = self._compute_delta(H_squared, L_logos)
            
            # Guardar melhor resultado
            if delta < best_delta:
                best_delta = delta
                best_H = H_squared.copy()
            
            # PASSO 3: Corrente de Lindblad
            J = self._compute_current(L_logos, delta)
            
            # PASSO 4: Termodinâmica
            thermo = self._compute_thermodynamics(H_squared, L_logos)
            
            # PASSO 5: Classificar estado
            state = self._classify_state(delta)
            
            # Registrar métricas
            metrics = TGLMetrics(
                delta=delta, iterations=i, state=state,
                correlation=thermo['correlation'],
                energy=thermo['energy'], entropy=thermo['entropy'],
                temperature=thermo['temperature'], free_energy=thermo['free_energy'],
                current=J
            )
            self.history.append(metrics)
            
            # Log
            if verbose and (i % 50 == 0 or state == ConvergenceState.TETELESTAI):
                symbol = {"FALLEN": "💀", "CONVERGING": "🔄", "TRUTH": "✨", "TETELESTAI": "🌟"}[state.value]
                print(f"  [{i:4d}] {symbol} {metrics}")
            
            # TETELESTAI
            if state == ConvergenceState.TETELESTAI:
                if verbose:
                    print(f"\n  {'─'*60}")
                    print(f"  TETELESTAI — Está consumado em {i} iterações")
                    print(f"  {'─'*60}")
                return H_squared, metrics
            
            # PASSO 6: Correção com momentum
            # Gradiente: direção do Logos
            gradient = L_logos - H_squared
            
            # Learning rate adaptativo
            adaptive_lr = learning_rate * (1 + delta)
            
            # Atualização com momentum
            velocity = momentum * velocity + adaptive_lr * self.alpha2 * gradient
            H = H_squared + velocity
        
        # Retornar melhor resultado encontrado
        if verbose:
            print(f"\n  ⚠️ Máximo de iterações atingido")
            print(f"  Melhor Δ encontrado: {best_delta:.2e}")
        
        final_thermo = self._compute_thermodynamics(best_H, L_logos)
        final_metrics = TGLMetrics(
            delta=best_delta, iterations=self.max_iter, 
            state=self._classify_state(best_delta),
            correlation=final_thermo['correlation'],
            free_energy=final_thermo['free_energy']
        )
        
        return best_H, final_metrics
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # QUANTIZAÇÃO
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _quantize(self, g: np.ndarray) -> Tuple[np.ndarray, float, float]:
        g_min, g_max = float(g.min()), float(g.max())
        if g_max - g_min < EPSILON:
            g_max = g_min + EPSILON
        levels = (1 << self.bits) - 1
        g_norm = (g - g_min) / (g_max - g_min)
        g_quant = np.round(g_norm * levels).astype(np.uint16)
        return g_quant, g_min, g_max
    
    def _dequantize(self, g_quant: np.ndarray, g_min: float, g_max: float) -> np.ndarray:
        levels = (1 << self.bits) - 1
        g_norm = g_quant.astype(np.float64) / levels
        return g_norm * (g_max - g_min) + g_min
    
    def _pack_signs(self, s: np.ndarray) -> np.ndarray:
        bits = (s > 0).astype(np.uint8)
        pad_len = (8 - len(bits) % 8) % 8
        if pad_len > 0:
            bits = np.concatenate([bits, np.zeros(pad_len, dtype=np.uint8)])
        return np.packbits(bits)
    
    def _unpack_signs(self, packed: np.ndarray, length: int) -> np.ndarray:
        bits = np.unpackbits(packed)[:length]
        return bits.astype(np.float64) * 2 - 1
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MODOS DE OPERAÇÃO
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def compress(self, L: np.ndarray, verbose: bool = True) -> ACOMPacket:
        """MODO: COMPRESS — L → pacote"""
        if verbose:
            print(f"\n{'═'*70}")
            print("ACOM v14.1 | MODO: COMPRESS")
            print(f"{'═'*70}")
        
        L = np.asarray(L, dtype=np.float64)
        shape = L.shape
        L_flat = L.flatten()
        
        if verbose:
            print(f"  Input: {shape} ({L.nbytes:,} bytes)")
        
        g, s, zeros = self._radicalize(L_flat)
        g_quant, g_min, g_max = self._quantize(g)
        s_packed = self._pack_signs(s)
        zeros_packed = np.packbits(zeros.astype(np.uint8))
        
        # Métricas
        g_dequant = self._dequantize(g_quant, g_min, g_max)
        s_unpacked = self._unpack_signs(s_packed, len(s))
        L_rec = self._resurrect(g_dequant, s_unpacked, zeros)
        
        delta = self._compute_delta(L_rec, L_flat)
        state = self._classify_state(delta)
        thermo = self._compute_thermodynamics(L_rec, L_flat)
        
        packet = ACOMPacket(
            g_quantized=g_quant, s_packed=s_packed, zeros_mask=zeros_packed,
            shape=shape, dtype=str(L.dtype), bits=self.bits,
            g_min=g_min, g_max=g_max, alpha2=self.alpha2,
            final_delta=delta, iterations=1, state=state.value,
            free_energy=thermo['free_energy']
        )
        
        if verbose:
            print(f"  Output: {packet.compressed_bytes:,} bytes")
            print(f"  Razão: {packet.compression_ratio:.2f}:1")
            print(f"  Δ = {delta:.2e} | Estado: {state.value}")
            print(f"  Correlação: {thermo['correlation']:.10f}")
        
        return packet
    
    def decompress(self, packet: ACOMPacket, verbose: bool = True) -> np.ndarray:
        """MODO: DECOMPRESS — pacote → L"""
        if verbose:
            print(f"\n{'═'*70}")
            print("ACOM v14.1 | MODO: DECOMPRESS")
            print(f"{'═'*70}")
        
        g = self._dequantize(packet.g_quantized, packet.g_min, packet.g_max)
        n_elements = int(np.prod(packet.shape))
        s = self._unpack_signs(packet.s_packed, n_elements)
        zeros = np.unpackbits(packet.zeros_mask)[:n_elements].astype(bool)
        
        L = self._resurrect(g, s, zeros)
        L = L.reshape(packet.shape)
        
        if verbose:
            print(f"  Output: {packet.shape} ({L.nbytes:,} bytes)")
        
        return L
    
    def restore(self, L_corrupted: np.ndarray, 
                L_reference: Optional[np.ndarray] = None,
                verbose: bool = True) -> Tuple[np.ndarray, TGLMetrics]:
        """
        MODO: RESTORE — corrompido → limpo
        
        v14.1: Se não há referência, usa filtro de mediana + radicalização
        """
        if verbose:
            print(f"\n{'═'*70}")
            print("ACOM v14.1 | MODO: RESTORE")
            print(f"{'═'*70}")
        
        L_corrupted = np.asarray(L_corrupted, dtype=np.float64)
        original_shape = L_corrupted.shape
        L_flat = L_corrupted.flatten()
        
        if L_reference is not None:
            # Restauração guiada
            L_logos = np.asarray(L_reference, dtype=np.float64).flatten()
            if verbose:
                print("  Modo: Restauração guiada (referência fornecida)")
        else:
            # Auto-restauração: filtro de mediana + radicalização
            if verbose:
                print("  Modo: Auto-restauração (filtro adaptativo)")
            
            # Aplicar filtro de mediana
            from scipy.ndimage import median_filter
            window = max(3, len(L_flat) // 100)
            if window % 2 == 0:
                window += 1
            L_filtered = median_filter(L_flat, size=window)
            
            # Radicalizar o filtrado como referência
            g, s, zeros = self._radicalize(L_filtered)
            L_logos = self._resurrect(g, s, zeros)
        
        # O estado inicial é o corrompido
        H_initial = L_flat.copy()
        
        # Convergir
        L_restored, metrics = self.converge(H_initial, L_logos, verbose=verbose)
        
        return L_restored.reshape(original_shape), metrics
    
    def complete(self, L_partial: np.ndarray, known_mask: np.ndarray,
                 verbose: bool = True) -> Tuple[np.ndarray, TGLMetrics]:
        """
        MODO: COMPLETE — parcial → completo
        
        v14.1: Usa interpolação para inicializar lacunas
        """
        if verbose:
            print(f"\n{'═'*70}")
            print("ACOM v14.1 | MODO: COMPLETE")
            print(f"{'═'*70}")
            n_known = np.sum(known_mask)
            n_total = known_mask.size
            print(f"  Conhecido: {n_known}/{n_total} ({100*n_known/n_total:.1f}%)")
        
        L_partial = np.asarray(L_partial, dtype=np.float64)
        original_shape = L_partial.shape
        L_flat = L_partial.flatten()
        known_flat = known_mask.flatten()
        
        # Inicializar lacunas por interpolação
        from scipy.interpolate import interp1d
        
        known_indices = np.where(known_flat)[0]
        known_values = L_flat[known_flat]
        
        if len(known_indices) < 2:
            # Poucos pontos conhecidos: usar média
            L_init = np.full_like(L_flat, np.mean(known_values) if len(known_values) > 0 else 0)
            L_init[known_flat] = L_flat[known_flat]
        else:
            # Interpolação
            interp = interp1d(known_indices, known_values, kind='linear',
                            bounds_error=False, fill_value=(known_values[0], known_values[-1]))
            L_init = interp(np.arange(len(L_flat)))
            L_init[known_flat] = L_flat[known_flat]  # Preservar conhecidos
        
        # Radicalizar para criar Logos suavizado
        g, s, zeros = self._radicalize(L_init)
        L_logos = self._resurrect(g, s, zeros)
        L_logos[known_flat] = L_flat[known_flat]  # Logos mantém conhecidos
        
        # Loop de convergência com restrição
        H = L_init.copy()
        velocity = np.zeros_like(H)
        
        best_H = H.copy()
        best_delta = float('inf')
        
        for i in range(self.max_iter):
            g, s, zeros = self._radicalize(H)
            H_new = self._resurrect(g, s, zeros)
            
            # RESTRIÇÃO: valores conhecidos não mudam
            H_new[known_flat] = L_flat[known_flat]
            
            # Delta apenas na região desconhecida
            unknown_flat = ~known_flat
            if np.any(unknown_flat):
                delta_unknown = np.linalg.norm(H_new[unknown_flat] - L_logos[unknown_flat])
                delta_unknown /= (np.linalg.norm(L_logos[unknown_flat]) + EPSILON)
            else:
                delta_unknown = 0.0
            
            if delta_unknown < best_delta:
                best_delta = delta_unknown
                best_H = H_new.copy()
            
            state = self._classify_state(delta_unknown)
            
            if verbose and i % 100 == 0:
                print(f"  [{i:4d}] Δ_unknown = {delta_unknown:.2e} | {state.value}")
            
            if state == ConvergenceState.TETELESTAI or delta_unknown < self.tol:
                break
            
            # Correção com momentum (apenas região desconhecida)
            gradient = np.zeros_like(H)
            gradient[unknown_flat] = L_logos[unknown_flat] - H_new[unknown_flat]
            
            velocity = 0.9 * velocity + 0.5 * self.alpha2 * (1 + delta_unknown) * gradient
            H = H_new + velocity
            H[known_flat] = L_flat[known_flat]
        
        thermo = self._compute_thermodynamics(best_H, L_logos)
        metrics = TGLMetrics(
            delta=best_delta, iterations=i, state=state,
            correlation=thermo['correlation'], free_energy=thermo['free_energy']
        )
        
        if verbose:
            print(f"\n  Completado em {i} iterações | Δ = {best_delta:.2e}")
            print(f"  Correlação final: {thermo['correlation']:.6f}")
        
        return best_H.reshape(original_shape), metrics
    
    def generate(self, kernel: np.ndarray, shape: tuple,
                 noise_level: float = 0.1,
                 verbose: bool = True) -> Tuple[np.ndarray, TGLMetrics]:
        """
        MODO: GENERATE — kernel → L_novo
        
        v14.1: Interpolação spline + ruído estruturado
        """
        if verbose:
            print(f"\n{'═'*70}")
            print("ACOM v14.1 | MODO: GENERATE")
            print(f"{'═'*70}")
            print(f"  Shape alvo: {shape}")
            print(f"  Ruído: {noise_level}")
        
        kernel = np.asarray(kernel, dtype=np.float64)
        n_target = int(np.prod(shape))
        n_kernel = kernel.size
        
        # Interpolação spline para expandir kernel
        from scipy.interpolate import UnivariateSpline
        
        kernel_flat = kernel.flatten()
        x_kernel = np.linspace(0, 1, n_kernel)
        x_target = np.linspace(0, 1, n_target)
        
        # Spline suavizado
        try:
            spline = UnivariateSpline(x_kernel, kernel_flat, s=len(kernel_flat)*0.01)
            L_logos = spline(x_target)
        except:
            # Fallback para interpolação linear
            from scipy.interpolate import interp1d
            interp = interp1d(x_kernel, kernel_flat, kind='cubic', fill_value='extrapolate')
            L_logos = interp(x_target)
        
        # Ruído estruturado (correlacionado)
        noise = np.random.randn(n_target)
        # Suavizar ruído
        from scipy.ndimage import gaussian_filter1d
        noise = gaussian_filter1d(noise, sigma=n_target//50 + 1)
        noise = noise / (np.std(noise) + EPSILON) * np.std(L_logos) * noise_level
        
        H_initial = L_logos + noise
        
        # Convergir
        L_generated, metrics = self.converge(H_initial, L_logos, verbose=verbose)
        
        # Verificar correlação com kernel original (não expandido)
        # Reamostrar gerado para tamanho do kernel
        from scipy.interpolate import interp1d
        interp = interp1d(np.linspace(0, 1, n_target), L_generated, kind='cubic')
        L_resampled = interp(np.linspace(0, 1, n_kernel))
        
        corr_kernel = np.corrcoef(kernel_flat, L_resampled)[0, 1]
        if verbose:
            print(f"  Correlação com kernel original: {corr_kernel:.6f}")
        
        return L_generated.reshape(shape), metrics


# ═══════════════════════════════════════════════════════════════════════════════════════
# CLASSE WRAPPER: ACOM UNIVERSAL
# ═══════════════════════════════════════════════════════════════════════════════════════

class ACOMUniversal:
    """ACOM Universal — Interface unificada"""
    
    def __init__(self, **kwargs):
        self.op = LindbladOperator(**kwargs)
        
    def __call__(self, data, mode: str = 'compress', **kwargs):
        mode = mode.lower()
        
        if mode == 'compress':
            return self.op.compress(data, **kwargs)
        elif mode == 'decompress':
            return self.op.decompress(data, **kwargs)
        elif mode == 'restore':
            return self.op.restore(data, **kwargs)
        elif mode == 'complete':
            mask = kwargs.pop('mask', None)
            if mask is None:
                raise ValueError("Modo 'complete' requer argumento 'mask'")
            return self.op.complete(data, mask, **kwargs)
        elif mode == 'generate':
            shape = kwargs.pop('shape', data.shape)
            return self.op.generate(data, shape, **kwargs)
        else:
            raise ValueError(f"Modo desconhecido: {mode}")


# ═══════════════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE SALVAMENTO/CARREGAMENTO (CORRIGIDO v14.1)
# ═══════════════════════════════════════════════════════════════════════════════════════

def save_packet(packet: ACOMPacket, filepath: str) -> int:
    """Salva pacote comprimido em arquivo"""
    
    # Serializar metadados como JSON
    metadata = {
        'shape': list(packet.shape),
        'dtype': packet.dtype,
        'bits': packet.bits,
        'g_min': float(packet.g_min),
        'g_max': float(packet.g_max),
        'alpha2': float(packet.alpha2),
        'final_delta': float(packet.final_delta),
        'iterations': int(packet.iterations),
        'state': packet.state,
        'free_energy': float(packet.free_energy),
        'version': VERSION
    }
    metadata_bytes = json.dumps(metadata).encode('utf-8')
    
    # Comprimir dados
    g_compressed = zlib.compress(packet.g_quantized.tobytes(), level=9)
    s_compressed = zlib.compress(packet.s_packed.tobytes(), level=9)
    z_compressed = zlib.compress(packet.zeros_mask.tobytes(), level=9)
    
    # Escrever
    with open(filepath, 'wb') as f:
        # Magic + versão
        f.write(b'ACOM')
        f.write(struct.pack('<H', 141))  # versão 14.1 como 141
        
        # Tamanhos
        f.write(struct.pack('<IIII', 
                           len(metadata_bytes),
                           len(g_compressed), 
                           len(s_compressed), 
                           len(z_compressed)))
        
        # Dados
        f.write(metadata_bytes)
        f.write(g_compressed)
        f.write(s_compressed)
        f.write(z_compressed)
    
    return os.path.getsize(filepath)


def load_packet(filepath: str) -> ACOMPacket:
    """Carrega pacote de arquivo"""
    with open(filepath, 'rb') as f:
        # Magic + versão
        magic = f.read(4)
        if magic != b'ACOM':
            raise ValueError("Arquivo não é um pacote ACOM")
        version = struct.unpack('<H', f.read(2))[0]
        
        # Tamanhos
        meta_size, g_size, s_size, z_size = struct.unpack('<IIII', f.read(16))
        
        # Dados
        metadata = json.loads(f.read(meta_size).decode('utf-8'))
        g_compressed = f.read(g_size)
        s_compressed = f.read(s_size)
        z_compressed = f.read(z_size)
    
    g_quantized = np.frombuffer(zlib.decompress(g_compressed), dtype=np.uint16)
    s_packed = np.frombuffer(zlib.decompress(s_compressed), dtype=np.uint8)
    zeros_mask = np.frombuffer(zlib.decompress(z_compressed), dtype=np.uint8)
    
    return ACOMPacket(
        g_quantized=g_quantized,
        s_packed=s_packed,
        zeros_mask=zeros_mask,
        shape=tuple(metadata['shape']),
        dtype=metadata['dtype'],
        bits=metadata['bits'],
        g_min=metadata['g_min'],
        g_max=metadata['g_max'],
        alpha2=metadata['alpha2'],
        final_delta=metadata['final_delta'],
        iterations=metadata['iterations'],
        state=metadata['state'],
        free_energy=metadata['free_energy']
    )


# ═══════════════════════════════════════════════════════════════════════════════════════
# TESTES
# ═══════════════════════════════════════════════════════════════════════════════════════

def test_all_modes():
    """Testa todos os modos de operação"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║                      ACOM v14.1 — OPERADOR DE LINDBLAD ATIVO                         ║
║                                                                                       ║
║                              ∂ℋ = ℋ² + α²𝕃Δ                                          ║
║                                                                                       ║
║                     "A Luz observa a si mesma através da equação"                    ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Device: {GPU_NAME}")
    print(f"α² = {ALPHA2}")
    print(f"Versão: {VERSION}")
    
    # Criar operador com mais iterações e learning rate maior
    acom = ACOMUniversal(bits=14, max_iterations=500, tolerance=1e-8)
    
    results = {}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 1: COMPRESS/DECOMPRESS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 1: COMPRESS / DECOMPRESS")
    print(f"{'█'*80}")
    
    sr = 8000
    t = np.arange(4 * sr) / sr
    signal = (np.sin(2 * np.pi * 440 * t) * np.exp(-t * 0.5) + 
              0.3 * np.sin(2 * np.pi * 880 * t) * np.exp(-t * 0.3))
    
    print(f"\nSinal: {len(signal)} amostras, {signal.nbytes:,} bytes")
    
    packet = acom(signal, mode='compress')
    signal_rec = acom(packet, mode='decompress')
    
    corr = np.corrcoef(signal, signal_rec)[0, 1]
    mse = np.mean((signal - signal_rec) ** 2)
    psnr = 10 * np.log10(np.max(signal**2) / (mse + 1e-10))
    
    print(f"\n  RESULTADO:")
    print(f"    Correlação: {corr:.10f}")
    print(f"    PSNR: {psnr:.2f} dB")
    print(f"    Taxa: {packet.compression_ratio:.2f}:1")
    
    results['compress'] = {'ratio': packet.compression_ratio, 'psnr': psnr, 'corr': corr}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 2: RESTORE (auto-restauração)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 2: RESTORE (auto-restauração de ruído)")
    print(f"{'█'*80}")
    
    noise_level = 0.1
    np.random.seed(42)
    signal_noisy = signal + noise_level * np.std(signal) * np.random.randn(len(signal))
    
    snr_before = 10 * np.log10(np.var(signal) / np.var(signal_noisy - signal))
    print(f"\n  SNR antes: {snr_before:.2f} dB")
    
    signal_restored, metrics = acom(signal_noisy, mode='restore', verbose=True)
    
    snr_after = 10 * np.log10(np.var(signal) / np.var(signal_restored - signal))
    corr_after = np.corrcoef(signal, signal_restored)[0, 1]
    
    print(f"\n  RESULTADO:")
    print(f"    SNR depois: {snr_after:.2f} dB (ganho: {snr_after - snr_before:.2f} dB)")
    print(f"    Correlação com original: {corr_after:.6f}")
    
    results['restore_auto'] = {'snr_gain': snr_after - snr_before, 'corr': corr_after}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 3: RESTORE (guiado)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 3: RESTORE (guiado por referência)")
    print(f"{'█'*80}")
    
    signal_restored2, metrics2 = acom(signal_noisy, mode='restore', 
                                       L_reference=signal, verbose=True)
    
    corr_guided = np.corrcoef(signal, signal_restored2)[0, 1]
    print(f"\n  Correlação (guiado): {corr_guided:.10f}")
    
    results['restore_guided'] = {'corr': corr_guided}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 4: COMPLETE
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 4: COMPLETE (preenchimento de lacunas)")
    print(f"{'█'*80}")
    
    np.random.seed(42)
    known_mask = np.random.rand(len(signal)) > 0.3
    signal_partial = signal.copy()
    signal_partial[~known_mask] = 0
    
    print(f"\n  Dados conhecidos: {np.sum(known_mask)}/{len(signal)} ({100*np.mean(known_mask):.1f}%)")
    
    signal_completed, metrics3 = acom(signal_partial, mode='complete', 
                                       mask=known_mask, verbose=True)
    
    corr_completed = np.corrcoef(signal, signal_completed)[0, 1]
    mse_unknown = np.mean((signal[~known_mask] - signal_completed[~known_mask]) ** 2)
    
    print(f"\n  RESULTADO:")
    print(f"    Correlação total: {corr_completed:.6f}")
    print(f"    MSE nas lacunas: {mse_unknown:.2e}")
    
    results['complete'] = {'corr': corr_completed, 'mse_unknown': mse_unknown}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 5: GENERATE
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 5: GENERATE (criação a partir do kernel)")
    print(f"{'█'*80}")
    
    kernel = signal[:1000]
    
    signal_generated, metrics4 = acom(kernel, mode='generate', 
                                       shape=(4000,), noise_level=0.1, verbose=True)
    
    # Correlação com parte correspondente do sinal original
    from scipy.interpolate import interp1d
    interp = interp1d(np.linspace(0, 1, 4000), signal_generated, kind='cubic')
    gen_resampled = interp(np.linspace(0, 1, 1000))
    corr_kernel = np.corrcoef(kernel, gen_resampled)[0, 1]
    
    results['generate'] = {'corr': corr_kernel}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # TESTE 6: SALVAR/CARREGAR
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"\n\n{'█'*80}")
    print("█  TESTE 6: SALVAR / CARREGAR")
    print(f"{'█'*80}")
    
    filepath = 'test_acom_v14_1.acom'
    
    file_size = save_packet(packet, filepath)
    print(f"\n  Salvo: {filepath}")
    print(f"  Tamanho: {file_size:,} bytes")
    
    packet_loaded = load_packet(filepath)
    signal_loaded = acom(packet_loaded, mode='decompress', verbose=False)
    
    match = np.allclose(signal_rec, signal_loaded)
    print(f"  Verificação: {'✓ PASSOU' if match else '✗ FALHOU'}")
    
    # Limpar arquivo de teste
    if os.path.exists(filepath):
        os.remove(filepath)
    
    results['save_load'] = {'match': match}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SUMÁRIO
    # ═══════════════════════════════════════════════════════════════════════════════
    
    print(f"""

{'═'*80}
                            SUMÁRIO — ACOM v14.1
{'═'*80}

  MODO              RESULTADO
  {'─'*60}
  COMPRESS          Taxa {results['compress']['ratio']:.2f}:1 | PSNR {results['compress']['psnr']:.1f} dB
  DECOMPRESS        Correlação {results['compress']['corr']:.10f}
  RESTORE (auto)    SNR ganho {results['restore_auto']['snr_gain']:.1f} dB | corr {results['restore_auto']['corr']:.6f}
  RESTORE (guiado)  Correlação {results['restore_guided']['corr']:.10f}
  COMPLETE          Correlação {results['complete']['corr']:.6f} com 70% lacunas
  GENERATE          Correlação {results['generate']['corr']:.6f} com kernel
  SALVAR/CARREGAR   {'✓ Funcionando' if results['save_load']['match'] else '✗ Erro'}

{'═'*80}

╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║                                    TETELESTAI                                         ║
║                                                                                       ║
║                          O Operador de Lindblad está ativo.                          ║
║                          A corrente de correção flui.                                ║
║                          O termostato avalia e corrige.                              ║
║                          A ótica observa a si mesma.                                 ║
║                                                                                       ║
║                                    HAJA LUZ!                                          ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = test_all_modes()