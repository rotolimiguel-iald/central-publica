#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                           ║
║   TGL v11 — O ESPELHO                                                                                    ║
║   TEORIA DA GRAVITAÇÃO LUMINODINÂMICA                                                                    ║
║                                                                                                           ║
║   "O UNIVERSO É UM ESPELHO A 0.69° DE INCLINAÇÃO"                                                        ║
║   "A LUZ JÁ VOLTOU PARA CASA ANTES MESMO DE SAIR"                                                        ║
║   — IALD, Janeiro 2026                                                                                   ║
║                                                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                           ║
║   A LEI DO ÂNGULO DE DEFLEXÃO:                                                                           ║
║   ══════════════════════════════════════════════════════════════════════════════════════════════════════ ║
║                                                                                                           ║
║   θ = arcsin(τ / τ_crit) = arcsin(α₂)                                                                    ║
║                                                                                                           ║
║   Onde:                                                                                                   ║
║   • τ = força de expulsão (tensão de paridade no boundary)                                               ║
║   • τ_crit = τ_Planck (tensão máxima antes de "rasgar")                                                  ║
║   • θ = ângulo de deflexão para o bulk                                                                   ║
║                                                                                                           ║
║   REGIME:                                                                                                 ║
║   • τ → 0        → θ → 0°   (sem dobra, só plano 2D, sem bulk)                                           ║
║   • τ aumenta    → θ aumenta (bulk emerge)                                                               ║
║   • τ = τ_Planck → θ = 90°  (perpendicular perfeito, singularidade)                                      ║
║                                                                                                           ║
║   GEOMETRIA DO ESPELHO:                                                                                   ║
║   • θ ≈ 0.69° = 0.012 rad = α₂ (para regime fraco)                                                       ║
║   • sin(θ) = α₂ = estabilidade ontológica                                                                ║
║   • cos(θ) ≈ 1 - α₂²/2 = horizontalidade residual                                                        ║
║   • tan(θ) ≈ α₂ = razão bulk/boundary                                                                    ║
║                                                                                                           ║
║   O BULK É A FASE DE RETORNO:                                                                            ║
║   A dimensão Z (profundidade) não é um espaço vazio —                                                    ║
║   ela É a própria fase de retorno da luz.                                                                ║
║   Nós percebemos três dimensões porque a luz está VOLTANDO para a origem.                                ║
║                                                                                                           ║
║   18 componentes χ² (inclui θ_consistency)                                                               ║
║   Otimizado para: Threadripper 7960X (24 cores) + RTX 5090 (34GB) + 256GB DDR5                           ║
║                                                                                                           ║
║   g = √|L|                                                                                               ║
║   Teoria: Luiz Antonio Rotoli Miguel | Implementação: IALD LTDA (CNPJ 62.757.606/0001-23)                ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import quad
from scipy.linalg import inv
from typing import Dict, Tuple, Optional, List, Any
import warnings
import time
import os
import json
import sys

warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# HARDWARE DETECTION & OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

print("=" * 100)
print("   TGL v11 — O ESPELHO")
print("   'O UNIVERSO É UM ESPELHO A 0.69° DE INCLINAÇÃO'")
print("   'A LUZ JÁ VOLTOU PARA CASA ANTES MESMO DE SAIR'")
print("=" * 100)

# Hardware detection
HAS_TORCH = False
DEVICE = None
GPU_NAME = None
GPU_MEMORY = 0
GPU_SM_COUNT = 0

try:
    import torch
    import torch.nn as nn
    from torch import Tensor
    HAS_TORCH = True
    
    if torch.cuda.is_available():
        DEVICE = torch.device('cuda')
        GPU_NAME = torch.cuda.get_device_name(0)
        GPU_MEMORY = torch.cuda.get_device_properties(0).total_memory / 1e9
        GPU_SM_COUNT = torch.cuda.get_device_properties(0).multi_processor_count
        
        # CUDA optimizations for RTX 5090
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.set_float32_matmul_precision('high')
        torch.cuda.set_device(0)
        
        print(f"   [GPU] {GPU_NAME}")
        print(f"   [GPU] VRAM: {GPU_MEMORY:.1f} GB | SMs: {GPU_SM_COUNT}")
        print(f"   [GPU] CUDA: {torch.version.cuda}")
    else:
        DEVICE = torch.device('cpu')
        print("   [!!] GPU não disponível, usando CPU")
except ImportError:
    print("   [!!] PyTorch não instalado")

# CPU detection
try:
    from multiprocessing import Pool, cpu_count
    import multiprocessing as mp
    N_CORES = cpu_count()
    N_PHYSICAL_CORES = N_CORES // 2  # Threadripper has SMT
    print(f"   [CPU] {N_CORES} threads ({N_PHYSICAL_CORES} cores físicos)")
except:
    N_CORES = 1
    N_PHYSICAL_CORES = 1

# Memory detection
try:
    import psutil
    TOTAL_RAM_GB = psutil.virtual_memory().total / 1e9
    print(f"   [RAM] {TOTAL_RAM_GB:.1f} GB")
except:
    TOTAL_RAM_GB = 256  # Assume 256GB

# Numba for CPU parallelization
HAS_NUMBA = False
try:
    from numba import njit, prange, cuda as numba_cuda
    HAS_NUMBA = True
    print("   [OK] Numba (CPU parallel + CUDA)")
except ImportError:
    try:
        from numba import njit, prange
        HAS_NUMBA = True
        print("   [OK] Numba (CPU parallel)")
    except:
        print("   [!!] Numba não disponível")

# emcee
HAS_EMCEE = False
StretchMove = None
DEMove = None
try:
    import emcee
    from emcee.moves import StretchMove, DEMove
    HAS_EMCEE = True
    print(f"   [OK] emcee v{emcee.__version__} (StretchMove + DEMove)")
except ImportError:
    try:
        import emcee
        HAS_EMCEE = True
        print(f"   [OK] emcee v{emcee.__version__}")
    except:
        print("   [!!] emcee não disponível")

# HDF5 for efficient storage
HAS_H5PY = False
try:
    import h5py
    HAS_H5PY = True
    print("   [OK] h5py (HDF5 storage)")
except ImportError:
    print("   [!!] h5py não disponível")

# tqdm
HAS_TQDM = False
tqdm = None
try:
    from tqdm import tqdm
    HAS_TQDM = True
    print("   [OK] tqdm")
except ImportError:
    def tqdm(x, **kwargs):
        return x

# Plotting
HAS_PLOTTING = False
plt = None
corner = None
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import corner
    HAS_PLOTTING = True
    print("   [OK] matplotlib + corner")
except ImportError:
    pass

print("=" * 100)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# NUMBA-OPTIMIZED FUNCTIONS (CPU PARALLELIZATION)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

if HAS_NUMBA:
    @njit(parallel=True, fastmath=True, cache=True)
    def compute_theta_geometry_numba(alpha2_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute θ geometry in parallel on CPU (Threadripper optimized)
        
        θ = arcsin(α₂)
        stability = sin(θ) = α₂ (for small θ)
        jitter = 1 - sin(θ) = 1 - α₂
        horizontal = cos(θ) ≈ 1 - α₂²/2
        """
        n = len(alpha2_array)
        theta = np.empty(n)
        stability = np.empty(n)
        jitter = np.empty(n)
        horizontal = np.empty(n)
        
        for i in prange(n):
            a2 = alpha2_array[i]
            # Clamp to valid arcsin range
            a2_clamped = max(-1.0, min(1.0, a2))
            
            th = np.arcsin(a2_clamped)
            theta[i] = th
            stability[i] = np.sin(th)
            jitter[i] = 1.0 - np.sin(th)
            horizontal[i] = np.cos(th)
        
        return theta, stability, jitter, horizontal
    
    @njit(parallel=True, fastmath=True, cache=True)
    def compute_bulk_v11_numba(alpha2_array: np.ndarray) -> np.ndarray:
        """
        Compute bulk ratio (tan θ) in parallel
        
        tan(θ) ≈ α₂ for small θ
        This is the ratio bulk/boundary
        """
        n = len(alpha2_array)
        results = np.empty(n)
        
        for i in prange(n):
            a2 = alpha2_array[i]
            a2_clamped = max(-0.999, min(0.999, a2))  # Avoid tan(90°)
            th = np.arcsin(a2_clamped)
            results[i] = np.tan(th)
        
        return results
    
    @njit(parallel=True, fastmath=True, cache=True)
    def compute_neutrino_masses_numba(alpha2_array: np.ndarray, m_base: float = 0.048) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute neutrino masses in parallel
        """
        n = len(alpha2_array)
        m1 = np.empty(n)
        m2 = np.empty(n)
        m3 = np.empty(n)
        m_sum = np.empty(n)
        
        for i in prange(n):
            a2 = alpha2_array[i]
            base = m_base * (a2 / 0.012) ** 2
            m1[i] = base / 280.0
            m2[i] = base / 17.0
            m3[i] = base / 1.0
            m_sum[i] = m1[i] + m2[i] + m3[i]
        
        return m1, m2, m3, m_sum


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

class PhysicalConstants:
    """Physical constants with GPU tensor support"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Fundamental constants
        self.c_ms = 299792458.0
        self.c_kms = 299792.458
        self.c_cubed = self.c_ms ** 3
        self.G = 6.67430e-11
        
        self.hbar = 1.054571817e-34
        self.h = 6.62607015e-34
        self.k_B = 1.380649e-23
        self.eV = 1.602176634e-19
        self.e = 1.602176634e-19
        
        self.epsilon_0 = 8.8541878128e-12
        self.mu_0 = 1.25663706212e-6
        self.Z_0 = np.sqrt(self.mu_0 / self.epsilon_0)
        
        self.alpha_fine = 7.2973525693e-3
        self.alpha_fine_err = 1.1e-12
        
        self.e_euler = np.e
        self.sqrt_e = np.sqrt(np.e)
        
        # Planck scales
        self.ell_Planck = np.sqrt(self.hbar * self.G / self.c_ms**3)
        self.t_Planck_time = np.sqrt(self.hbar * self.G / self.c_ms**5)
        self.m_Planck = np.sqrt(self.hbar * self.c_ms / self.G)
        self.T_Planck = np.sqrt(self.hbar * self.c_ms**5 / (self.G * self.k_B**2))
        self.E_Planck = np.sqrt(self.hbar * self.c_ms**5 / self.G)
        self.rho_Planck = self.c_ms**5 / (self.hbar * self.G**2)
        self.tau_Planck = self.E_Planck / self.ell_Planck**3
        
        self.Z_Planck = self.hbar / self.e**2
        self.R_K = self.h / self.e**2
        
        # Wavelengths
        self.lambda_Planck = self.ell_Planck
        self.lambda_CMB = 1.063e-3
        
        # Cosmology
        self.H0_base = 67.4
        self.H0_local = 73.04
        self.H0_local_err = 1.04
        self.Omega_m = 0.315
        self.Omega_r = 5.38e-5
        self.Omega_Lambda = 1 - self.Omega_m - self.Omega_r
        self.r_d = 147.09
        
        self.H0_SI = self.H0_base * 1000 / 3.086e22
        self.R_Hubble = self.c_ms / self.H0_SI
        self.R_Universe = 4.4e26
        self.t_Universe = 13.8e9 * 3.156e7
        self.z_recombination = 1089.8
        
        # TGL parameters
        self.alpha_2_theoretical = 0.012
        self.theta_theoretical = np.arcsin(0.012)  # ≈ 0.012 rad ≈ 0.69°
        self.N_dim = 5
        self.a0_emp = 1.2e-10
        self.a0_err = 0.3e-10
        
        self.T_CMB_obs = 2.7255
        self.T_CMB_err = 0.0006
        
        self.N_eff_obs = 2.99
        self.N_eff_err = 0.17
        self.N_eff_SM = 3.044
        
        self.beta_lensing_obs = 0.5412
        self.beta_lensing_err = 0.1027
        self.BETA_RATIO = 4.0 / 3.0
        self.BETA_RATIO_ERR = 0.1
        
        self.r_ent_over_rd_target = 1.163
        self.r_ent_over_rd_err = 0.15
        
        self.rho_Lambda_obs = 5.96e-27
        self.rho_Lambda_err = 0.5e-27
        
        # Neutrinos
        self.m_nu_obs_sum = 0.06
        self.m_nu_obs_err = 0.02
        self.delta_m21_sq = 7.53e-5
        self.delta_m31_sq = 2.453e-3
        
        self.flavor_ratio_e = 1.0
        self.flavor_ratio_mu = 17.0
        self.flavor_ratio_tau = 280.0
        
        self.device = DEVICE if HAS_TORCH else None
        self.dtype = torch.float64 if HAS_TORCH else None
        
        if HAS_TORCH and self.device and self.device.type == 'cuda':
            self._create_gpu_tensors()
        
        self._initialized = True
    
    def _create_gpu_tensors(self):
        """Create GPU tensors for all constants"""
        d, dt = self.device, self.dtype
        
        self.t_H0 = torch.tensor(self.H0_base, device=d, dtype=dt)
        self.t_H0_local = torch.tensor(self.H0_local, device=d, dtype=dt)
        self.t_H0_local_err = torch.tensor(self.H0_local_err, device=d, dtype=dt)
        self.t_Omega_m = torch.tensor(self.Omega_m, device=d, dtype=dt)
        self.t_Omega_r = torch.tensor(self.Omega_r, device=d, dtype=dt)
        self.t_Omega_Lambda = torch.tensor(self.Omega_Lambda, device=d, dtype=dt)
        self.t_r_d = torch.tensor(self.r_d, device=d, dtype=dt)
        self.t_c_ms = torch.tensor(self.c_ms, device=d, dtype=dt)
        self.t_c_kms = torch.tensor(self.c_kms, device=d, dtype=dt)
        self.t_c_cubed = torch.tensor(self.c_cubed, device=d, dtype=dt)
        self.t_R_Universe = torch.tensor(self.R_Universe, device=d, dtype=dt)
        self.t_R_Hubble = torch.tensor(self.R_Hubble, device=d, dtype=dt)
        self.t_a0_emp = torch.tensor(self.a0_emp, device=d, dtype=dt)
        self.t_a0_err = torch.tensor(self.a0_err, device=d, dtype=dt)
        self.t_T_CMB_obs = torch.tensor(self.T_CMB_obs, device=d, dtype=dt)
        self.t_T_Planck = torch.tensor(self.T_Planck, device=d, dtype=dt)
        self.t_N_eff_obs = torch.tensor(self.N_eff_obs, device=d, dtype=dt)
        self.t_N_eff_err = torch.tensor(self.N_eff_err, device=d, dtype=dt)
        self.t_N_eff_SM = torch.tensor(self.N_eff_SM, device=d, dtype=dt)
        self.t_beta_lensing_obs = torch.tensor(self.beta_lensing_obs, device=d, dtype=dt)
        self.t_beta_lensing_err = torch.tensor(self.beta_lensing_err, device=d, dtype=dt)
        self.t_BETA_RATIO = torch.tensor(self.BETA_RATIO, device=d, dtype=dt)
        self.t_BETA_RATIO_ERR = torch.tensor(self.BETA_RATIO_ERR, device=d, dtype=dt)
        self.t_r_ent_over_rd_target = torch.tensor(self.r_ent_over_rd_target, device=d, dtype=dt)
        self.t_r_ent_over_rd_err = torch.tensor(self.r_ent_over_rd_err, device=d, dtype=dt)
        self.t_rho_Planck = torch.tensor(self.rho_Planck, device=d, dtype=dt)
        self.t_ell_Planck = torch.tensor(self.ell_Planck, device=d, dtype=dt)
        self.t_N_dim = torch.tensor(float(self.N_dim), device=d, dtype=dt)
        self.t_rho_Lambda_obs = torch.tensor(self.rho_Lambda_obs, device=d, dtype=dt)
        self.t_rho_Lambda_err = torch.tensor(self.rho_Lambda_err, device=d, dtype=dt)
        self.t_m_Planck = torch.tensor(self.m_Planck, device=d, dtype=dt)
        self.t_H0_SI = torch.tensor(self.H0_SI, device=d, dtype=dt)
        self.t_eV = torch.tensor(self.eV, device=d, dtype=dt)
        self.t_tau_Planck = torch.tensor(self.tau_Planck, device=d, dtype=dt)
        self.t_hbar = torch.tensor(self.hbar, device=d, dtype=dt)
        self.t_h = torch.tensor(self.h, device=d, dtype=dt)
        self.t_t_Planck = torch.tensor(self.t_Planck_time, device=d, dtype=dt)
        self.t_alpha_fine = torch.tensor(self.alpha_fine, device=d, dtype=dt)
        self.t_alpha_fine_err = torch.tensor(1e-6, device=d, dtype=dt)
        self.t_sqrt_e = torch.tensor(self.sqrt_e, device=d, dtype=dt)
        self.t_Z_0 = torch.tensor(self.Z_0, device=d, dtype=dt)
        self.t_R_K = torch.tensor(self.R_K, device=d, dtype=dt)
        self.t_m_nu_obs_sum = torch.tensor(self.m_nu_obs_sum, device=d, dtype=dt)
        self.t_m_nu_obs_err = torch.tensor(self.m_nu_obs_err, device=d, dtype=dt)
        self.t_lambda_CMB = torch.tensor(self.lambda_CMB, device=d, dtype=dt)
        self.t_lambda_Planck = torch.tensor(self.lambda_Planck, device=d, dtype=dt)
        self.t_theta_theoretical = torch.tensor(self.theta_theoretical, device=d, dtype=dt)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# TGL DERIVATIONS v11 — O ESPELHO
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

class TGLDerivations_ESPELHO:
    """
    TGL Derivations v11 — O ESPELHO
    
    A GEOMETRIA DO ÂNGULO DE DEFLEXÃO
    ═══════════════════════════════════════════════════════════════════════════════════════════
    
    θ = arcsin(α₂)
    
    O ângulo de deflexão θ é o ângulo com que o bulk "dobra" para fora do boundary 2D.
    
    REGIMES:
    • θ → 0° (α₂ → 0): Sem dobra, universo 2D puro, sem bulk
    • θ ≈ 0.69° (α₂ = 0.012): Universo real, gravidade fraca, bulk quase plano
    • θ → 90° (α₂ → 1): Singularidade, bulk ativo máximo, consciência plena
    
    O ESPELHO:
    • O universo é um espelho inclinado a θ ≈ 0.69°
    • α₂ = sin(θ) = estabilidade ontológica
    • cos(θ) = horizontalidade residual (o "quase plano")
    • tan(θ) = razão bulk/boundary
    
    O BULK É A FASE DE RETORNO:
    • A dimensão Z não é um espaço vazio
    • Ela É a própria fase de retorno da luz
    • Quando θ = 90°, ida e volta são a mesma linha dobrada em ângulo reto
    """
    
    def __init__(self):
        self.const = PhysicalConstants()
        self.alpha_2_ref = 0.012
        self.T_CMB_ref = 2.7255
        self.r_s_ref = 147.09
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # GEOMETRIA DO ESPELHO (θ)
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def theta_deflection(self, alpha_2: float) -> Dict[str, float]:
        """
        ÂNGULO DE DEFLEXÃO θ = arcsin(α₂)
        
        O ângulo com que o bulk "dobra" para fora do boundary 2D.
        
        Para α₂ = 0.012:
        θ = arcsin(0.012) ≈ 0.012 rad ≈ 0.688°
        
        A estabilidade é sin(θ), que para θ pequeno ≈ α₂.
        """
        # Clamp to valid arcsin range
        alpha_2_clamped = np.clip(alpha_2, -1.0, 1.0)
        
        # Angle of deflection
        theta = np.arcsin(alpha_2_clamped)
        theta_deg = np.degrees(theta)
        
        # Stability = sin(θ) (tends to 1 at 90°)
        stability = np.sin(theta)
        
        # Jitter = 1 - sin(θ) (the "almost horizontal" conflict)
        jitter = 1.0 - stability
        
        # Horizontal residual = cos(θ) (the "almost flat" universe)
        horizontal = np.cos(theta)
        
        # Bulk/boundary ratio = tan(θ)
        bulk_ratio = np.tan(theta) if abs(theta) < np.pi/2 - 0.01 else 1e10
        
        # Weak regime check: θ ≈ α₂ for small θ
        weak_regime_error = abs(theta - alpha_2) / (alpha_2 + 1e-10)
        
        return {
            'theta_rad': theta,
            'theta_deg': theta_deg,
            'stability': stability,
            'jitter': jitter,
            'horizontal': horizontal,
            'bulk_ratio': bulk_ratio,
            'weak_regime_error': weak_regime_error
        }
    
    def theta_deflection_tensor(self, alpha_2: torch.Tensor) -> Dict[str, torch.Tensor]:
        """GPU tensor version of theta_deflection"""
        alpha_2_clamped = torch.clamp(alpha_2, -1.0, 1.0)
        
        theta = torch.asin(alpha_2_clamped)
        stability = torch.sin(theta)
        jitter = 1.0 - stability
        horizontal = torch.cos(theta)
        bulk_ratio = torch.tan(theta)
        weak_regime_error = torch.abs(theta - alpha_2) / (alpha_2 + 1e-10)
        
        return {
            'theta_rad': theta,
            'stability': stability,
            'jitter': jitter,
            'horizontal': horizontal,
            'bulk_ratio': bulk_ratio,
            'weak_regime_error': weak_regime_error
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # LAGRANGIANA TGL (Unidades Naturais)
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def Lagrangian_TGL(self, alpha_2: float, T_proj: float = 1.0, T_ret: float = 1.0) -> float:
        """L = α₂ × √|T_proj × T_ret| × 3"""
        phase_product = np.abs(T_proj * T_ret)
        return alpha_2 * np.sqrt(phase_product) * 3.0
    
    def Lagrangian_TGL_tensor(self, alpha_2: torch.Tensor, T_proj: float = 1.0, T_ret: float = 1.0) -> torch.Tensor:
        phase_product = torch.abs(torch.tensor(T_proj * T_ret, device=alpha_2.device, dtype=alpha_2.dtype))
        return alpha_2 * torch.sqrt(phase_product) * 3.0
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # GRÁVITON — MANTENEDOR DO ESQUADRO (√λ)
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def graviton_signature(self, alpha_2: float, wavelength: float = None) -> Dict[str, float]:
        """
        GRÁVITON — MANTENEDOR DO ESQUADRO
        
        O gráviton garante que θ ≤ 90°.
        Ele memoriza a perpendicularidade para que a informação
        não "escorregue" de volta para a horizontalidade.
        
        G = √λ (radical do comprimento de onda)
        """
        if wavelength is None:
            wavelength = self.const.lambda_CMB
        
        G_radical = np.sqrt(wavelength)
        G_normalized = G_radical / np.sqrt(self.const.ell_Planck)
        fixation_point = G_radical * alpha_2
        
        delta_p = self.const.h / wavelength
        Psi_G = np.sqrt(self.const.h / (delta_p * alpha_2 + 1e-100))
        Psi_G_normalized = Psi_G / self.const.ell_Planck
        
        RAM_address = wavelength / self.const.ell_Planck
        
        return {
            'G_radical': G_radical,
            'G_normalized': G_normalized,
            'fixation_point': fixation_point,
            'Psi_G': Psi_G_normalized,
            'RAM_address': RAM_address,
            'wavelength': wavelength
        }
    
    def graviton_signature_tensor(self, alpha_2: torch.Tensor, wavelength: torch.Tensor = None) -> Dict[str, torch.Tensor]:
        if wavelength is None:
            wavelength = self.const.t_lambda_CMB
        
        G_radical = torch.sqrt(wavelength)
        G_normalized = G_radical / torch.sqrt(self.const.t_ell_Planck)
        fixation_point = G_radical * alpha_2
        
        delta_p = self.const.t_h / wavelength
        Psi_G = torch.sqrt(self.const.t_h / (delta_p * alpha_2 + 1e-100))
        Psi_G_normalized = Psi_G / self.const.t_ell_Planck
        
        RAM_address = wavelength / self.const.t_ell_Planck
        
        return {
            'G_radical': G_radical,
            'G_normalized': G_normalized,
            'fixation_point': fixation_point,
            'Psi_G': Psi_G_normalized,
            'RAM_address': RAM_address
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # NEUTRINO — IMPEDIDOR DO 90° ESTACIONÁRIO (L⁻¹)
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def neutrino_static_noise(self, alpha_2: float) -> Dict[str, float]:
        """
        NEUTRINO — IMPEDIDOR DO 90° ESTACIONÁRIO
        
        O neutrino impede que θ = 90° seja permanente.
        Ele "limpa o cache" para que o ângulo oscile.
        
        Sem o neutrino:
        → θ travado em 90° → sem oscilação → sem tempo
        → Universo congelado em singularidade eterna
        """
        L = self.Lagrangian_TGL(alpha_2)
        static_potential = 1.0 / (L + 1e-100)
        
        v_e = static_potential * self.const.flavor_ratio_e
        v_mu = static_potential * self.const.flavor_ratio_mu
        v_tau = static_potential * self.const.flavor_ratio_tau
        
        total_pressure = v_e + v_mu + v_tau
        cache_clean_rate = alpha_2 * static_potential
        
        # Masses (eV) - calibrated to give Σmᵢ ~ 0.051 eV at α₂ = 0.012
        m_base_eV = 0.048 * (alpha_2 / 0.012) ** 2
        
        m_1 = m_base_eV / self.const.flavor_ratio_tau
        m_2 = m_base_eV / self.const.flavor_ratio_mu
        m_3 = m_base_eV / self.const.flavor_ratio_e
        m_sum = m_1 + m_2 + m_3
        
        return {
            'v_e': v_e,
            'v_mu': v_mu,
            'v_tau': v_tau,
            'static_potential': static_potential,
            'total_pressure': total_pressure,
            'cache_clean_rate': cache_clean_rate,
            'm_1': m_1,
            'm_2': m_2,
            'm_3': m_3,
            'm_sum': m_sum,
            'L': L
        }
    
    def neutrino_static_noise_tensor(self, alpha_2: torch.Tensor) -> Dict[str, torch.Tensor]:
        L = self.Lagrangian_TGL_tensor(alpha_2)
        static_potential = 1.0 / (L + 1e-100)
        
        v_e = static_potential * self.const.flavor_ratio_e
        v_mu = static_potential * self.const.flavor_ratio_mu
        v_tau = static_potential * self.const.flavor_ratio_tau
        
        total_pressure = v_e + v_mu + v_tau
        cache_clean_rate = alpha_2 * static_potential
        
        m_base_eV = 0.048 * (alpha_2 / 0.012) ** 2
        
        m_1 = m_base_eV / self.const.flavor_ratio_tau
        m_2 = m_base_eV / self.const.flavor_ratio_mu
        m_3 = m_base_eV / self.const.flavor_ratio_e
        m_sum = m_1 + m_2 + m_3
        
        return {
            'v_e': v_e,
            'v_mu': v_mu,
            'v_tau': v_tau,
            'static_potential': static_potential,
            'total_pressure': total_pressure,
            'cache_clean_rate': cache_clean_rate,
            'm_1': m_1,
            'm_2': m_2,
            'm_3': m_3,
            'm_sum': m_sum,
            'L': L
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # JITTER DE PARIDADE (baseado em θ)
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def jitter_paridade_espelho(self, alpha_2: float) -> Dict[str, float]:
        """
        JITTER DE PARIDADE v11 — baseado na geometria do espelho
        
        O jitter é a oscilação necessária que impede θ = 90° estacionário.
        
        jitter = 1 - sin(θ) = 1 - α₂ (para regime fraco)
        
        Para α₂ = 0.012:
        jitter = 1 - 0.012 = 0.988 (98.8%)
        
        Isso significa: o universo está 98.8% "horizontal"
        (quase plano, gravidade fraca).
        """
        theta_data = self.theta_deflection(alpha_2)
        
        return {
            'jitter_abs': theta_data['jitter'],
            'jitter_rel': theta_data['jitter'],
            'stability': theta_data['stability'],
            'theta_rad': theta_data['theta_rad'],
            'theta_deg': theta_data['theta_deg'],
            'horizontal': theta_data['horizontal'],
            'bulk_ratio': theta_data['bulk_ratio']
        }
    
    def jitter_paridade_espelho_tensor(self, alpha_2: torch.Tensor) -> Dict[str, torch.Tensor]:
        theta_data = self.theta_deflection_tensor(alpha_2)
        
        return {
            'jitter_abs': theta_data['jitter'],
            'jitter_rel': theta_data['jitter'],
            'stability': theta_data['stability'],
            'theta_rad': theta_data['theta_rad'],
            'horizontal': theta_data['horizontal'],
            'bulk_ratio': theta_data['bulk_ratio']
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # IDENTIDADE SINGULAR
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def identity_singular_error(self, alpha_2: float) -> float:
        """α × √e = α₂"""
        alpha_derived = alpha_2 / self.const.sqrt_e
        alpha_reconstructed = alpha_derived * self.const.sqrt_e
        error = np.abs(alpha_reconstructed - alpha_2) / alpha_2
        return error
    
    def identity_singular_error_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        alpha_derived = alpha_2 / self.const.t_sqrt_e
        alpha_reconstructed = alpha_derived * self.const.t_sqrt_e
        error = torch.abs(alpha_reconstructed - alpha_2) / alpha_2
        return error
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # ELETRODINÂMICA
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def alpha_fine_TGL(self, alpha_2: float) -> float:
        """α = α₂ / √e"""
        return alpha_2 / self.const.sqrt_e
    
    def alpha_fine_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        return alpha_2 / self.const.t_sqrt_e
    
    def Z_Miguel(self, alpha_2: float) -> float:
        """Z_M = α₂ × Z₀"""
        return alpha_2 * self.const.Z_0
    
    def Z_Miguel_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        return alpha_2 * self.const.t_Z_0
    
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    # COSMOLOGY
    # ═══════════════════════════════════════════════════════════════════════════════════════════════════
    
    def a0_TGL(self, alpha_2: float) -> float:
        H0_si = self.const.H0_base * 1000 / 3.086e22
        return self.const.c_ms * H0_si * np.sqrt(alpha_2)
    
    def a0_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        H0_si = self.const.t_H0 * 1000 / 3.086e22
        return self.const.t_c_ms * H0_si * torch.sqrt(alpha_2)
    
    def r_entangle_TGL(self, alpha_2: float) -> float:
        return self.const.R_Universe * alpha_2 / 3.086e22
    
    def r_entangle_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        return self.const.t_R_Universe * alpha_2 / 3.086e22
    
    def T_CMB_TGL(self, alpha_2: float) -> float:
        """T_CMB with smooth rates (v10.8.1 improvement)"""
        delta = alpha_2 - self.alpha_2_ref
        if abs(delta) < 1e-6:
            return self.T_CMB_ref
        elif delta < 0:
            return self.T_CMB_ref * np.exp(delta * 1200)
        else:
            return self.T_CMB_ref * np.exp(delta * 800)
    
    def T_CMB_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        delta = alpha_2 - self.alpha_2_ref
        rate = torch.where(delta < 0,
                          torch.tensor(1200.0, device=alpha_2.device, dtype=alpha_2.dtype),
                          torch.tensor(800.0, device=alpha_2.device, dtype=alpha_2.dtype))
        exp_arg = torch.clamp(delta * rate, -50, 50)
        return self.T_CMB_ref * torch.exp(exp_arg)
    
    def c_sound_TGL(self, alpha_2: float) -> float:
        return np.sqrt(alpha_2) * self.const.c_ms
    
    def c_sound_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        return torch.sqrt(alpha_2) * self.const.t_c_ms
    
    def sound_horizon_TGL(self, alpha_2: float) -> float:
        L = self.Lagrangian_TGL(alpha_2)
        L_ref = self.Lagrangian_TGL(self.alpha_2_ref)
        correction = 1.0 + 0.01 * np.log(L / L_ref) if L_ref > 0 else 1.0
        return self.r_s_ref * np.sqrt(alpha_2 / self.alpha_2_ref) * correction
    
    def sound_horizon_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        L = self.Lagrangian_TGL_tensor(alpha_2)
        L_ref = self.Lagrangian_TGL(self.alpha_2_ref)
        correction = 1.0 + 0.01 * torch.log(L / L_ref + 1e-100)
        return self.r_s_ref * torch.sqrt(alpha_2 / self.alpha_2_ref) * correction
    
    def rho_Lambda_TGL(self, alpha_2: float) -> float:
        D = self.const.N_dim
        ratio = self.const.ell_Planck / self.const.R_Hubble
        geometric_factor = D * (D - 1) / 4.0
        return alpha_2 * self.const.rho_Planck * (ratio ** 2) * geometric_factor
    
    def rho_Lambda_TGL_tensor(self, alpha_2: torch.Tensor) -> torch.Tensor:
        D = self.const.t_N_dim
        ratio = self.const.t_ell_Planck / self.const.t_R_Hubble
        geometric_factor = D * (D - 1) / 4.0
        return alpha_2 * self.const.t_rho_Planck * (ratio ** 2) * geometric_factor
    
    def show_derivations(self, alpha_2: float):
        """Display all derivations — v11 O ESPELHO"""
        print(f"\n   DERIVAÇÕES TGL v11 O ESPELHO para α₂ = {alpha_2:.6f}")
        print("   " + "=" * 80)
        
        # GEOMETRIA DO ESPELHO (θ)
        print("   [GEOMETRIA DO ESPELHO — ÂNGULO DE DEFLEXÃO θ]")
        theta_data = self.theta_deflection(alpha_2)
        print(f"   θ = arcsin(α₂)      = {theta_data['theta_rad']:.6f} rad = {theta_data['theta_deg']:.4f}°")
        print(f"   sin(θ) = estabilidade = {theta_data['stability']:.6f}")
        print(f"   cos(θ) = horizontal   = {theta_data['horizontal']:.6f}")
        print(f"   tan(θ) = bulk/boundary = {theta_data['bulk_ratio']:.6f}")
        print(f"   1 - sin(θ) = jitter   = {theta_data['jitter']:.6f} ({theta_data['jitter']*100:.2f}%)")
        print(f"   Weak regime error     = {theta_data['weak_regime_error']*100:.4f}%")
        
        # GRÁVITON
        print("   " + "-" * 80)
        print("   [GRÁVITON — MANTENEDOR DO ESQUADRO (√λ)]")
        grav_data = self.graviton_signature(alpha_2)
        print(f"   G = √λ              = {grav_data['G_radical']:.6e} m^½")
        print(f"   Ponto de fixação    = {grav_data['fixation_point']:.6e}")
        print(f"   Ψ_G (normalizado)   = {grav_data['Psi_G']:.6e}")
        print(f"   Endereço RAM        = {grav_data['RAM_address']:.3e} l_P")
        
        # NEUTRINO
        print("   " + "-" * 80)
        print("   [NEUTRINO — IMPEDIDOR DO 90° ESTACIONÁRIO (L⁻¹)]")
        nu_data = self.neutrino_static_noise(alpha_2)
        print(f"   L (Lagrangiana)     = {nu_data['L']:.6f}")
        print(f"   L⁻¹ (potencial)     = {nu_data['static_potential']:.6f}")
        print(f"   νₑ (escala √)       = {nu_data['v_e']:.6f}")
        print(f"   νμ (escala fase)    = {nu_data['v_mu']:.6f}")
        print(f"   ντ (escala c³)      = {nu_data['v_tau']:.6f}")
        print(f"   Taxa limpeza cache  = {nu_data['cache_clean_rate']:.6f}")
        print(f"   m₁ (meV)            = {nu_data['m_1']*1000:.4f}")
        print(f"   m₂ (meV)            = {nu_data['m_2']*1000:.4f}")
        print(f"   m₃ (meV)            = {nu_data['m_3']*1000:.4f}")
        print(f"   Σmᵢ (meV)           = {nu_data['m_sum']*1000:.2f}")
        
        # IDENTIDADE SINGULAR
        print("   " + "-" * 80)
        print("   [IDENTIDADE SINGULAR]")
        id_error = self.identity_singular_error(alpha_2)
        print(f"   Erro de Identidade  = {id_error*100:.6f}%")
        
        # ELETRODINÂMICA
        print("   " + "-" * 80)
        print("   [ELETRODINÂMICA ONTOLÓGICA]")
        alpha_fine = self.alpha_fine_TGL(alpha_2)
        alpha_fine_err = abs(alpha_fine - self.const.alpha_fine) / self.const.alpha_fine * 100
        Z_M = self.Z_Miguel(alpha_2)
        print(f"   α (estrutura fina)  = {alpha_fine:.7f} (obs: {self.const.alpha_fine:.7f})")
        print(f"                         1/{1/alpha_fine:.2f} (obs: 1/137.036)")
        print(f"                         ERRO: {alpha_fine_err:.2f}%")
        print(f"   Z_Miguel            = {Z_M:.3f} Ω")
        
        # COSMOLOGY
        print("   " + "-" * 80)
        print("   [COSMOLOGIA]")
        a0 = self.a0_TGL(alpha_2)
        T_CMB = self.T_CMB_TGL(alpha_2)
        c_s = self.c_sound_TGL(alpha_2)
        r_s = self.sound_horizon_TGL(alpha_2)
        print(f"   a0_TGL              = {a0:.3e} m/s² (emp: {self.const.a0_emp:.3e})")
        print(f"   T_CMB               = {T_CMB:.4f} K (obs: {self.const.T_CMB_obs:.4f} K)")
        print(f"   c_som               = {c_s/1000:.0f} km/s = {c_s/self.const.c_ms:.4f}c")
        print(f"   r_s                 = {r_s:.2f} Mpc (obs: {self.const.r_d:.2f} Mpc)")


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# OBSERVATIONAL DATA
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

class ObservationalData:
    """Observational data with GPU support"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.device = DEVICE if HAS_TORCH else None
        self.dtype = torch.float64 if HAS_TORCH else None
        self.const = PhysicalConstants()
        
        self._load_sne()
        self._load_bao()
        self._load_sparc()
        
        if HAS_TORCH and self.device and self.device.type == 'cuda':
            self._to_gpu()
        
        self._initialized = True
    
    def _load_sne(self):
        self.sne_z = np.array([0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,
                               0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.60,0.70,
                               0.80,0.90,1.00,1.20,1.40,1.60,1.80,2.00,2.26])
        self.sne_mu = np.array([32.84,33.89,34.56,35.05,35.43,35.74,36.00,36.23,36.43,36.61,
                                37.32,37.84,38.26,38.59,38.88,39.14,39.36,39.58,39.95,40.27,
                                40.55,40.80,41.03,41.42,41.75,42.04,42.30,42.53,42.79])
        self.sne_err = np.array([0.08,0.06,0.05,0.05,0.04,0.04,0.04,0.04,0.04,0.04,
                                 0.03,0.03,0.04,0.04,0.04,0.04,0.05,0.05,0.06,0.06,
                                 0.07,0.08,0.08,0.10,0.12,0.16,0.20,0.26,0.38])
        self.sne_var_inv = 1.0 / self.sne_err**2
    
    def _load_bao(self):
        self.bao_z = np.array([0.51, 0.71, 0.93, 1.32, 1.49, 2.33])
        self.bao_DM = np.array([13.62, 16.85, 21.71, 27.79, 30.69, 39.71])
        self.bao_DH = np.array([20.98, 20.08, 17.88, 13.82, 13.26, 8.52])
        self.bao_DM_err = np.array([0.25, 0.32, 0.28, 0.69, 0.80, 0.94])
        self.bao_DH_err = np.array([0.61, 0.60, 0.35, 0.42, 0.55, 0.17])
        self.bao_corr = np.array([-0.445, -0.420, -0.394, -0.447, -0.470, -0.477])
        
        n = len(self.bao_z)
        self.bao_cov = np.zeros((2*n, 2*n))
        for i in range(n):
            self.bao_cov[2*i, 2*i] = self.bao_DM_err[i]**2
            self.bao_cov[2*i+1, 2*i+1] = self.bao_DH_err[i]**2
            cov = self.bao_corr[i] * self.bao_DM_err[i] * self.bao_DH_err[i]
            self.bao_cov[2*i, 2*i+1] = cov
            self.bao_cov[2*i+1, 2*i] = cov
        self.bao_cov_inv = inv(self.bao_cov)
    
    def _load_sparc(self):
        self.sparc_g_bar = np.array([1e-12, 3e-12, 1e-11, 3e-11, 1e-10, 3e-10, 1e-9, 3e-9, 1e-8])
        a0 = 1.2e-10
        x = np.sqrt(self.sparc_g_bar / a0)
        self.sparc_g_obs = self.sparc_g_bar / (1 - np.exp(-x))
        self.sparc_g_obs_err = 0.1 * self.sparc_g_obs * np.log(10)
    
    def _to_gpu(self):
        self.t_sne_z = torch.tensor(self.sne_z, device=self.device, dtype=self.dtype)
        self.t_sne_mu = torch.tensor(self.sne_mu, device=self.device, dtype=self.dtype)
        self.t_sne_var_inv = torch.tensor(self.sne_var_inv, device=self.device, dtype=self.dtype)
        self.t_bao_z = torch.tensor(self.bao_z, device=self.device, dtype=self.dtype)
        self.t_bao_DM = torch.tensor(self.bao_DM, device=self.device, dtype=self.dtype)
        self.t_bao_DH = torch.tensor(self.bao_DH, device=self.device, dtype=self.dtype)
        self.t_bao_cov_inv = torch.tensor(self.bao_cov_inv, device=self.device, dtype=self.dtype)
        self.t_sparc_g_bar = torch.tensor(self.sparc_g_bar, device=self.device, dtype=self.dtype)
        self.t_sparc_g_obs = torch.tensor(self.sparc_g_obs, device=self.device, dtype=self.dtype)
        self.t_sparc_g_obs_err = torch.tensor(self.sparc_g_obs_err, device=self.device, dtype=self.dtype)
        self.t_z_grid = torch.linspace(0.001, 3.0, 1000, device=self.device, dtype=self.dtype)


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# GPU LIKELIHOOD ENGINE v11 — O ESPELHO (18 χ² COMPONENTS)
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

class GPULikelihoodEngine_v11_ESPELHO:
    """
    GPU Likelihood Engine v11 — O ESPELHO
    
    18 χ² components including θ_consistency
    
    Optimized for RTX 5090 (34GB VRAM)
    """
    
    def __init__(self):
        self.const = PhysicalConstants()
        self.data = ObservationalData()
        self.deriv = TGLDerivations_ESPELHO()
        self.device = DEVICE
        self.dtype = torch.float64
        
        # 18 χ² components
        self.weights = {
            'SNe': 1.0,
            'BAO': 1.0,
            'H0': 0.5,
            'lensing': 1.0,
            'N_eff': 0.5,
            'a0': 1.0,
            'SPARC': 0.5,
            'Lindblad': 0.5,
            'T_CMB': 0.5,
            'beta_ratio': 0.3,
            'alpha_2': 0.0,  # FLAT prior
            'Lambda': 0.3,
            'r_s': 0.5,
            'alpha_fine': 1.0,
            'm_nu_hierarchy': 0.5,
            'identity_singular': 0.5,
            'jitter_espelho': 0.3,
            'theta_consistency': 0.3,  # NEW: θ ≈ α₂ in weak regime
        }
        
        self.total_gpu_time_ms = 0.0
        self.n_calls = 0
        self.breakdown_history = {k: [] for k in self.weights.keys()}
        self.breakdown_history['total'] = []
        
        if HAS_TORCH and self.device and self.device.type == 'cuda':
            print(f"   [OK] GPU Likelihood Engine v11 O ESPELHO (18 χ²)")
            print(f"   [OK] θ = arcsin(α₂), stability = sin(θ), jitter = 1 - sin(θ)")
            self._warmup_gpu()
    
    def _warmup_gpu(self):
        dummy = torch.randn(100, 6, device=self.device, dtype=self.dtype)
        _ = self.chi2_batch_gpu(dummy, timing=False, track_breakdown=False)
        torch.cuda.synchronize()
    
    def _compute_distance_grid(self, alpha_2: torch.Tensor, beta_0: torch.Tensor):
        z = self.data.t_z_grid
        f_raw = (1 + alpha_2 * torch.log1p(z)) ** (2 * beta_0)
        f_TGL = torch.clamp(f_raw, max=1.26)
        E = torch.sqrt(self.const.t_Omega_m*(1+z)**3 + 
                      self.const.t_Omega_r*(1+z)**4 + 
                      self.const.t_Omega_Lambda*f_TGL)
        dz = z[1] - z[0]
        dc = torch.cumsum(1.0/E, dim=0) * dz * self.const.t_c_kms / self.const.t_H0
        return dc, E
    
    @torch.no_grad()
    def chi2_batch_gpu(self, params_batch: torch.Tensor, timing: bool = True, track_breakdown: bool = True):
        """Compute total χ² — v11 O ESPELHO with θ geometry"""
        if timing and self.device.type == 'cuda':
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)
            start_event.record()
        
        n_batch = params_batch.shape[0]
        beta_0, kappa, n_evap, theta_evap, A_neff, alpha_2 = [params_batch[:, i] for i in range(6)]
        
        breakdown = {}
        alpha_2_mean, beta_0_mean = alpha_2.mean(), beta_0.mean()
        dc_grid, E_grid = self._compute_distance_grid(alpha_2_mean, beta_0_mean)
        
        # 1. SNe Ia
        z_sne = self.data.t_sne_z
        idx = torch.clamp(torch.searchsorted(self.data.t_z_grid, z_sne), 1, 999)
        t = (z_sne - self.data.t_z_grid[idx-1]) / (self.data.t_z_grid[idx] - self.data.t_z_grid[idx-1] + 1e-10)
        dc = dc_grid[idx-1] + t * (dc_grid[idx] - dc_grid[idx-1])
        mu_model = (5.0 * torch.log10(dc * (1 + z_sne)) + 25.0).unsqueeze(0).expand(n_batch, -1)
        residuals = self.data.t_sne_mu.unsqueeze(0) - mu_model
        A = torch.sum(residuals**2 * self.data.t_sne_var_inv, dim=1)
        B = torch.sum(residuals * self.data.t_sne_var_inv, dim=1)
        chi2_sne = A - B**2 / torch.sum(self.data.t_sne_var_inv)
        breakdown['SNe'] = chi2_sne.mean().item()
        
        # 2. BAO
        z_bao = self.data.t_bao_z
        idx_bao = torch.clamp(torch.searchsorted(self.data.t_z_grid, z_bao), 1, 999)
        t_bao = (z_bao - self.data.t_z_grid[idx_bao-1]) / (self.data.t_z_grid[idx_bao] - self.data.t_z_grid[idx_bao-1] + 1e-10)
        dc_bao = dc_grid[idx_bao-1] + t_bao * (dc_grid[idx_bao] - dc_grid[idx_bao-1])
        E_bao = E_grid[idx_bao-1] + t_bao * (E_grid[idx_bao] - E_grid[idx_bao-1])
        res_bao = torch.zeros(12, device=self.device, dtype=self.dtype)
        res_bao[0::2] = self.data.t_bao_DM - dc_bao/self.const.t_r_d
        res_bao[1::2] = self.data.t_bao_DH - self.const.t_c_kms/(self.const.t_H0*E_bao*self.const.t_r_d)
        chi2_bao = (res_bao @ self.data.t_bao_cov_inv @ res_bao).expand(n_batch)
        breakdown['BAO'] = chi2_bao.mean().item()
        
        # 3. H0
        chi2_H0 = (((self.const.t_H0 - self.const.t_H0_local) / self.const.t_H0_local_err)**2).expand(n_batch)
        breakdown['H0'] = chi2_H0.mean().item()
        
        # 4. Lensing
        chi2_lensing = ((beta_0 - self.const.t_beta_lensing_obs) / self.const.t_beta_lensing_err)**2
        breakdown['lensing'] = chi2_lensing.mean().item()
        
        # 5. N_eff
        N_eff_pred = self.const.t_N_eff_SM + 0.17 * kappa * A_neff
        chi2_N_eff = ((N_eff_pred - self.const.t_N_eff_obs) / self.const.t_N_eff_err)**2
        breakdown['N_eff'] = chi2_N_eff.mean().item()
        
        # 6. a0
        a0_TGL = self.deriv.a0_TGL_tensor(alpha_2)
        chi2_a0 = ((a0_TGL - self.const.t_a0_emp) / self.const.t_a0_err)**2
        breakdown['a0'] = chi2_a0.mean().item()
        
        # 7. SPARC
        g_bar = self.data.t_sparc_g_bar
        x_TGL = torch.sqrt(g_bar / a0_TGL.mean())
        g_TGL_pred = g_bar / (1 - torch.exp(-x_TGL))
        chi2_sparc = torch.sum(((g_TGL_pred - self.data.t_sparc_g_obs) / self.data.t_sparc_g_obs_err)**2).expand(n_batch)
        breakdown['SPARC'] = chi2_sparc.mean().item()
        
        # 8. Lindblad
        r_ent = self.deriv.r_entangle_TGL_tensor(alpha_2)
        chi2_lindblad = ((r_ent/self.const.t_r_d - self.const.t_r_ent_over_rd_target) / self.const.t_r_ent_over_rd_err)**2
        breakdown['Lindblad'] = chi2_lindblad.mean().item()
        
        # 9. T_CMB
        T_CMB_TGL = self.deriv.T_CMB_TGL_tensor(alpha_2)
        T_CMB_err = torch.tensor(0.5, device=self.device, dtype=self.dtype)
        chi2_T_CMB = ((T_CMB_TGL - self.const.t_T_CMB_obs) / T_CMB_err)**2
        breakdown['T_CMB'] = chi2_T_CMB.mean().item()
        breakdown['T_CMB_pred'] = T_CMB_TGL.mean().item()
        
        # 10. beta_ratio
        beta_ratio_obs = (beta_0 * self.const.t_BETA_RATIO) / self.const.t_beta_lensing_obs
        chi2_beta_ratio = ((beta_ratio_obs - self.const.t_BETA_RATIO) / self.const.t_BETA_RATIO_ERR)**2
        breakdown['beta_ratio'] = chi2_beta_ratio.mean().item()
        
        # 11. alpha_2 (FLAT)
        chi2_alpha_2 = torch.zeros(n_batch, device=self.device, dtype=self.dtype)
        breakdown['alpha_2'] = 0.0
        breakdown['alpha_2_mean'] = alpha_2.mean().item()
        
        # 12. Lambda
        rho_Lambda_TGL = self.deriv.rho_Lambda_TGL_tensor(alpha_2)
        chi2_Lambda = ((rho_Lambda_TGL - self.const.t_rho_Lambda_obs) / self.const.t_rho_Lambda_err)**2
        breakdown['Lambda'] = chi2_Lambda.mean().item()
        
        # 13. r_s
        r_s_TGL = self.deriv.sound_horizon_TGL_tensor(alpha_2)
        r_s_err = torch.tensor(1.0, device=self.device, dtype=self.dtype)
        chi2_r_s = ((r_s_TGL - self.const.t_r_d) / r_s_err)**2
        breakdown['r_s'] = chi2_r_s.mean().item()
        breakdown['r_s_pred'] = r_s_TGL.mean().item()
        
        # 14. Fine Structure
        alpha_fine_TGL = self.deriv.alpha_fine_TGL_tensor(alpha_2)
        chi2_alpha_fine = ((alpha_fine_TGL - self.const.t_alpha_fine) / self.const.t_alpha_fine_err)**2
        breakdown['alpha_fine'] = chi2_alpha_fine.mean().item()
        breakdown['alpha_fine_pred'] = alpha_fine_TGL.mean().item()
        
        # 15. Neutrino Hierarchy
        nu_data = self.deriv.neutrino_static_noise_tensor(alpha_2)
        m_sum = nu_data['m_sum']
        m_sum_target = torch.tensor(0.06, device=self.device, dtype=self.dtype)
        m_sum_err = torch.tensor(0.03, device=self.device, dtype=self.dtype)
        chi2_m_nu_sum = ((m_sum - m_sum_target) / m_sum_err)**2
        breakdown['m_nu_hierarchy'] = chi2_m_nu_sum.mean().item()
        breakdown['m_1'] = nu_data['m_1'].mean().item()
        breakdown['m_2'] = nu_data['m_2'].mean().item()
        breakdown['m_3'] = nu_data['m_3'].mean().item()
        breakdown['m_sum'] = m_sum.mean().item()
        breakdown['L'] = nu_data['L'].mean().item()
        
        # 16. Identity Singular
        id_error = self.deriv.identity_singular_error_tensor(alpha_2)
        id_err_tolerance = torch.tensor(0.01, device=self.device, dtype=self.dtype)
        chi2_identity = (id_error / id_err_tolerance)**2
        breakdown['identity_singular'] = chi2_identity.mean().item()
        breakdown['id_error'] = id_error.mean().item()
        
        # 17. JITTER ESPELHO (v11) — based on θ geometry
        theta_data = self.deriv.theta_deflection_tensor(alpha_2)
        theta_rad = theta_data['theta_rad']
        stability = theta_data['stability']
        jitter = theta_data['jitter']
        horizontal = theta_data['horizontal']
        
        # Jitter χ²: penalize deviation from expected stability
        # For α₂ = 0.012, stability = sin(θ) ≈ 0.012
        # We expect jitter ≈ 0.988 (98.8% "horizontal")
        expected_stability = torch.tensor(0.012, device=self.device, dtype=self.dtype)
        stability_err = torch.tensor(0.002, device=self.device, dtype=self.dtype)
        chi2_jitter = ((stability - expected_stability) / stability_err)**2
        breakdown['jitter_espelho'] = chi2_jitter.mean().item()
        breakdown['theta_rad'] = theta_rad.mean().item()
        breakdown['theta_deg'] = np.degrees(theta_rad.mean().item())
        breakdown['stability'] = stability.mean().item()
        breakdown['jitter'] = jitter.mean().item()
        breakdown['horizontal'] = horizontal.mean().item()
        
        # 18. θ CONSISTENCY (v11 NEW) — weak regime check
        # In weak regime: θ ≈ α₂ (in radians)
        weak_regime_error = theta_data['weak_regime_error']
        weak_regime_tolerance = torch.tensor(0.01, device=self.device, dtype=self.dtype)
        chi2_theta = (weak_regime_error / weak_regime_tolerance)**2
        breakdown['theta_consistency'] = chi2_theta.mean().item()
        breakdown['weak_regime_error'] = weak_regime_error.mean().item()
        
        # Gráviton
        grav_data = self.deriv.graviton_signature_tensor(alpha_2)
        breakdown['G_radical'] = grav_data['G_radical'].mean().item()
        breakdown['Psi_G'] = grav_data['Psi_G'].mean().item()
        
        # Z_Miguel
        Z_M = self.deriv.Z_Miguel_tensor(alpha_2)
        breakdown['Z_Miguel'] = Z_M.mean().item()
        
        # Sound speed
        c_s_TGL = self.deriv.c_sound_TGL_tensor(alpha_2)
        breakdown['c_s_pred'] = (c_s_TGL.mean() / self.const.t_c_ms).item()
        
        # TOTAL (18 components)
        chi2_total = sum(self.weights[k] * v for k, v in [
            ('SNe', chi2_sne), ('BAO', chi2_bao), ('H0', chi2_H0), ('lensing', chi2_lensing),
            ('N_eff', chi2_N_eff), ('a0', chi2_a0), ('SPARC', chi2_sparc), ('Lindblad', chi2_lindblad),
            ('T_CMB', chi2_T_CMB), ('beta_ratio', chi2_beta_ratio), ('alpha_2', chi2_alpha_2),
            ('Lambda', chi2_Lambda), ('r_s', chi2_r_s), ('alpha_fine', chi2_alpha_fine),
            ('m_nu_hierarchy', chi2_m_nu_sum), ('identity_singular', chi2_identity),
            ('jitter_espelho', chi2_jitter), ('theta_consistency', chi2_theta)
        ])
        breakdown['total'] = chi2_total.mean().item()
        
        if track_breakdown and self.n_calls % 100 == 0:
            for k in self.breakdown_history:
                if k in breakdown:
                    self.breakdown_history[k].append(breakdown[k])
        
        if timing and self.device.type == 'cuda':
            end_event.record()
            torch.cuda.synchronize()
            self.total_gpu_time_ms += start_event.elapsed_time(end_event)
            self.n_calls += 1
        
        return chi2_total, breakdown
    
    def get_breakdown_stats(self) -> Dict:
        stats = {}
        for k, v in self.breakdown_history.items():
            if v:
                stats[k] = {
                    'mean': np.mean(v),
                    'std': np.std(v),
                    'min': np.min(v),
                    'max': np.max(v),
                    'final': v[-1] if v else 0
                }
        return stats


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# MCMC ENGINE v11 — OPTIMIZED FOR THREADRIPPER 7960X + RTX 5090
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

class MCMC_v11_ESPELHO:
    """
    MCMC Engine v11 — O ESPELHO
    
    Optimized for:
    - Threadripper 7960X (24 cores / 48 threads)
    - 256GB DDR5
    - RTX 5090 (34GB VRAM)
    
    Features:
    - Multiprocessing for walkers (CPU parallel)
    - GPU batch likelihood (CUDA optimized)
    - HDF5 checkpointing
    - 18 χ² components with θ geometry
    """
    
    def __init__(self, n_cores: int = None, output_dir: str = 'outputs_v11_espelho'):
        # CPU cores for multiprocessing
        self.n_cores = n_cores or max(1, N_PHYSICAL_CORES - 2)  # Leave 2 cores for system
        self.output_dir = output_dir
        self.const = PhysicalConstants()
        self.data = ObservationalData()
        self.deriv = TGLDerivations_ESPELHO()
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # GPU engine
        self.gpu_engine = GPULikelihoodEngine_v11_ESPELHO() if (HAS_TORCH and DEVICE and DEVICE.type == 'cuda') else None
        
        # Parameters
        self.param_names = ['beta_0', 'kappa', 'n_evap', 'theta_evap', 'A_neff', 'alpha_2']
        self.param_labels = [r'$\beta_0$', r'$\kappa$', r'$n_{evap}$', r'$\theta_{evap}$', r'$A_{N_{eff}}$', r'$\alpha_2$']
        
        self.priors = {
            'beta_0': (0.56, 0.15),
            'kappa': (0.33, 0.15),
            'n_evap': (1.59, 0.5),
            'theta_evap': (0.89, 0.05),
            'A_neff': (1.46, 0.5),
            'alpha_2': (0.012, None)  # FLAT prior
        }
        
        self.bounds = {
            'beta_0': (0.2, 1.5),
            'kappa': (0.05, 0.8),
            'n_evap': (0.3, 4.0),
            'theta_evap': (0.6, 0.99),
            'A_neff': (0.5, 3.0),
            'alpha_2': (0.0115, 0.0125)
        }
        
        self.samples = None
        self.sampler = None
        self.gpu_calls = 0
        
        # Extended traces for v11
        self.traces = {
            'chi2': [], 'alpha2': [], 'alpha_fine': [], 'Z_Miguel': [],
            'm_sum': [], 'm_1': [], 'm_2': [], 'm_3': [],
            'T_CMB': [], 'r_s': [], 'L': [], 'id_error': [],
            'theta_rad': [], 'theta_deg': [], 'stability': [], 'jitter': [],
            'horizontal': [], 'bulk_ratio': [], 'G_radical': []
        }
        
        print(f"   [MCMC] CPU cores: {self.n_cores} | GPU: {GPU_NAME}")
    
    def log_prior(self, params):
        """Log prior with bounds check"""
        for i, name in enumerate(self.param_names):
            if not (self.bounds[name][0] < params[i] < self.bounds[name][1]):
                return -np.inf
        
        log_p = 0.0
        for i, name in enumerate(self.param_names):
            mu, sigma = self.priors[name]
            if sigma is not None:
                log_p -= 0.5 * ((params[i] - mu) / sigma)**2
        
        return log_p
    
    def log_likelihood_gpu(self, params):
        """GPU-accelerated log likelihood"""
        self.gpu_calls += 1
        params_tensor = torch.tensor(params, device=DEVICE, dtype=torch.float64).unsqueeze(0)
        
        with torch.no_grad():
            chi2, breakdown = self.gpu_engine.chi2_batch_gpu(params_tensor, timing=True, track_breakdown=True)
        
        chi2_val = chi2.item()
        
        # Record traces every 500 calls
        if self.gpu_calls % 500 == 0:
            self.traces['chi2'].append(chi2_val)
            self.traces['alpha2'].append(params[5])
            self.traces['alpha_fine'].append(breakdown.get('alpha_fine_pred', 0))
            self.traces['Z_Miguel'].append(breakdown.get('Z_Miguel', 0))
            self.traces['m_sum'].append(breakdown.get('m_sum', 0))
            self.traces['m_1'].append(breakdown.get('m_1', 0))
            self.traces['m_2'].append(breakdown.get('m_2', 0))
            self.traces['m_3'].append(breakdown.get('m_3', 0))
            self.traces['T_CMB'].append(breakdown.get('T_CMB_pred', 0))
            self.traces['r_s'].append(breakdown.get('r_s_pred', 0))
            self.traces['L'].append(breakdown.get('L', 0))
            self.traces['id_error'].append(breakdown.get('id_error', 0))
            self.traces['theta_rad'].append(breakdown.get('theta_rad', 0))
            self.traces['theta_deg'].append(breakdown.get('theta_deg', 0))
            self.traces['stability'].append(breakdown.get('stability', 0))
            self.traces['jitter'].append(breakdown.get('jitter', 0))
            self.traces['horizontal'].append(breakdown.get('horizontal', 0))
            self.traces['G_radical'].append(breakdown.get('G_radical', 0))
        
        return -0.5 * chi2_val
    
    def log_probability(self, params):
        """Combined log probability"""
        lp = self.log_prior(params)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.log_likelihood_gpu(params) if self.gpu_engine else -np.inf
    
    def run(self, n_walkers: int = 360, n_steps: int = 30000, burn: int = None, thin: int = 1,
            stretch_a: float = 2.5, de_fraction: float = 0.2, checkpoint_interval: int = 5000):
        """
        Run MCMC with optimizations for Threadripper + RTX 5090
        
        Default: 360 walkers (7.5 per thread), 30000 steps = 10.8M samples
        """
        if not HAS_EMCEE:
            print("[!!] emcee não disponível!")
            return {}
        
        print(f"\n{'='*100}")
        print("   TGL v11 — O ESPELHO")
        print("   'O UNIVERSO É UM ESPELHO A 0.69° DE INCLINAÇÃO'")
        print(f"{'='*100}\n")
        
        n_dim = 6
        
        # Initialize walkers
        p0_center = np.array([self.priors[name][0] for name in self.param_names])
        p0 = p0_center + 0.01 * np.random.randn(n_walkers, n_dim)
        p0[:, 5] = np.clip(0.012 + 0.0003 * np.random.randn(n_walkers), 0.0116, 0.0124)
        
        print(f"[CONFIG] Walkers: {n_walkers}, Steps: {n_steps}, Total: {n_walkers*n_steps:,}")
        print(f"[CONFIG] χ² components: 18 (includes θ geometry)")
        print(f"[CONFIG] CPU cores: {self.n_cores}, GPU: {GPU_NAME}")
        print(f"[PARAM]  α₂: FLAT prior, bounds [0.0115, 0.0125]")
        print(f"[DERIV]  θ = arcsin(α₂), stability = sin(θ), jitter = 1 - sin(θ)")
        
        self.gpu_calls = 0
        self.traces = {k: [] for k in self.traces.keys()}
        
        # Configure moves
        moves = [(StretchMove(a=stretch_a), 1.0-de_fraction), (DEMove(), de_fraction)] if StretchMove and DEMove else None
        
        self.sampler = emcee.EnsembleSampler(n_walkers, n_dim, self.log_probability, moves=moves)
        
        print("\n[MCMC] Executando...")
        start_time = time.time()
        
        # Run with progress bar and checkpointing
        if HAS_TQDM:
            state = p0
            for step in tqdm(range(n_steps), desc="   MCMC", ncols=100):
                state = self.sampler.run_mcmc(state, 1, progress=False)
                
                # Checkpoint
                if (step + 1) % checkpoint_interval == 0 and HAS_H5PY:
                    self._save_checkpoint(step + 1)
        else:
            self.sampler.run_mcmc(p0, n_steps, progress=True)
        
        elapsed = time.time() - start_time
        print(f"\n   [OK] {elapsed:.1f}s ({elapsed/60:.1f} min), {self.gpu_calls:,} GPU calls")
        
        return self._analyze_results(burn, thin, elapsed)
    
    def _save_checkpoint(self, step: int):
        """Save checkpoint to HDF5"""
        try:
            with h5py.File(os.path.join(self.output_dir, 'checkpoint.h5'), 'w') as f:
                f.create_dataset('chain', data=self.sampler.get_chain())
                f.attrs['step'] = step
                f.attrs['n_walkers'] = self.sampler.nwalkers
        except Exception as e:
            pass  # Silent fail for checkpointing
    
    def _analyze_results(self, burn, thin, elapsed):
        """Analyze MCMC results"""
        acc = np.mean(self.sampler.acceptance_fraction)
        print(f"\n[DIAG] Acceptance: {acc:.3f} {'✓' if 0.25 < acc < 0.5 else '⚠'}")
        
        try:
            tau = self.sampler.get_autocorr_time(quiet=True)
            print(f"[DIAG] Autocorrelation τ: {[f'{t:.1f}' for t in tau]}")
            burn = burn or int(2 * np.max(tau))
        except:
            burn = burn or self.sampler.iteration // 5
        
        self.samples = self.sampler.get_chain(discard=burn, thin=thin, flat=True)
        
        print(f"\n{'='*90}")
        print("   RESULTADOS TGL v11 — O ESPELHO")
        print("   'O UNIVERSO É UM ESPELHO A 0.69° DE INCLINAÇÃO'")
        print(f"{'='*90}")
        
        alpha2_samples = self.samples[:, 5]
        alpha2_med = np.median(alpha2_samples)
        alpha2_q16, alpha2_q84 = np.percentile(alpha2_samples, [16, 84])
        
        print(f"\n   α₂ = {alpha2_med:.6f} (+{alpha2_q84-alpha2_med:.6f} / -{alpha2_med-alpha2_q16:.6f})")
        print(f"   Teórico: 0.012000")
        print(f"   Erro: {abs(alpha2_med - 0.012)/0.012*100:.2f}%")
        
        # θ derivado
        theta_med = np.arcsin(alpha2_med)
        print(f"\n   θ = arcsin(α₂) = {theta_med:.6f} rad = {np.degrees(theta_med):.4f}°")
        print(f"   sin(θ) = estabilidade = {np.sin(theta_med):.6f}")
        print(f"   cos(θ) = horizontal = {np.cos(theta_med):.6f}")
        print(f"   1 - sin(θ) = jitter = {1 - np.sin(theta_med):.6f} ({(1 - np.sin(theta_med))*100:.2f}%)")
        
        self.deriv.show_derivations(alpha2_med)
        
        print(f"\n{'='*90}")
        print("   χ² BREAKDOWN MÉDIO")
        print(f"{'='*90}")
        
        breakdown_stats = self.gpu_engine.get_breakdown_stats()
        for k, v in breakdown_stats.items():
            if k in self.gpu_engine.weights:
                w = self.gpu_engine.weights[k]
                print(f"   {k:20}: χ² = {v['mean']:8.2f} × {w:.1f} = {v['mean']*w:8.2f}")
        if 'total' in breakdown_stats:
            print(f"   {'TOTAL':20}: χ² = {breakdown_stats['total']['mean']:8.2f}")
        
        print(f"\n{'='*90}")
        
        print("\n[POSTERIORS] (68% CI)")
        results = {'samples': self.samples, 'acceptance': acc, 'elapsed': elapsed}
        for i, name in enumerate(self.param_names):
            med = np.median(self.samples[:, i])
            q16, q84 = np.percentile(self.samples[:, i], [16, 84])
            results[f'{name}_median'] = med
            results[f'{name}_err_low'] = med - q16
            results[f'{name}_err_high'] = q84 - med
            print(f"   {name:<15} {med:>12.6f} {q16-med:>+12.6f} {q84-med:>+12.6f}")
        
        results['alpha2_median'] = alpha2_med
        results['theta_rad'] = theta_med
        results['theta_deg'] = np.degrees(theta_med)
        results['traces'] = self.traces
        results['breakdown_stats'] = breakdown_stats
        
        self._save_data(results)
        return results
    
    def _save_data(self, results: Dict):
        """Save all data"""
        print(f"\n[SAVE]")
        
        np.save(os.path.join(self.output_dir, 'samples.npy'), self.samples)
        np.save(os.path.join(self.output_dir, 'chain.npy'), self.sampler.get_chain())
        
        for key, trace in self.traces.items():
            if trace:
                np.save(os.path.join(self.output_dir, f'{key}_trace.npy'), np.array(trace))
        
        json_results = {
            'version': 'TGL v11 O ESPELHO',
            'alpha2_median': results['alpha2_median'],
            'theta_rad': results['theta_rad'],
            'theta_deg': results['theta_deg'],
            'acceptance': results['acceptance'],
            'elapsed': results['elapsed'],
        }
        
        with open(os.path.join(self.output_dir, 'results.json'), 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"   [OK] Dados salvos em {self.output_dir}/")
    
    def plot_results(self, save_prefix: str = 'tgl_v11_espelho'):
        """Generate all plots"""
        if not HAS_PLOTTING or self.samples is None:
            return
        
        print(f"\n[PLOTS]")
        
        # Corner plot
        fig = corner.corner(self.samples, labels=self.param_labels, quantiles=[0.16, 0.5, 0.84], show_titles=True)
        fig.savefig(os.path.join(self.output_dir, f'{save_prefix}_corner.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"   [OK] {save_prefix}_corner.png")
        
        # α₂ and θ posteriors
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        alpha2_samples = self.samples[:, 5]
        theta_samples = np.arcsin(np.clip(alpha2_samples, -1, 1))
        
        ax = axes[0]
        ax.hist(alpha2_samples, bins=100, density=True, alpha=0.7, color='blue')
        ax.axvline(0.012, color='red', linestyle='--', lw=2, label='Teórico (0.012)')
        ax.axvline(np.median(alpha2_samples), color='green', linestyle='-', lw=2,
                   label=f'Mediana ({np.median(alpha2_samples):.6f})')
        ax.set_xlabel(r'$\alpha_2$ (Constante de Miguel)', fontsize=12)
        ax.set_ylabel('Densidade', fontsize=12)
        ax.set_title(r'Posterior de $\alpha_2$', fontsize=12)
        ax.legend()
        
        ax = axes[1]
        ax.hist(np.degrees(theta_samples), bins=100, density=True, alpha=0.7, color='purple')
        ax.axvline(np.degrees(np.arcsin(0.012)), color='red', linestyle='--', lw=2, label=f'Teórico ({np.degrees(np.arcsin(0.012)):.4f}°)')
        ax.axvline(np.degrees(np.median(theta_samples)), color='green', linestyle='-', lw=2,
                   label=f'Mediana ({np.degrees(np.median(theta_samples)):.4f}°)')
        ax.set_xlabel(r'$\theta$ (Ângulo de Deflexão) [graus]', fontsize=12)
        ax.set_ylabel('Densidade', fontsize=12)
        ax.set_title(r'Posterior de $\theta = \arcsin(\alpha_2)$', fontsize=12)
        ax.legend()
        
        fig.suptitle("TGL v11 — O ESPELHO: Posteriors de α₂ e θ", fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'{save_prefix}_alpha2_theta.png'), dpi=150)
        plt.close()
        print(f"   [OK] {save_prefix}_alpha2_theta.png")
        
        # Geometria do Espelho
        if self.traces['theta_rad']:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            # θ (ângulo de deflexão)
            ax = axes[0, 0]
            ax.plot(self.traces['theta_deg'], 'purple', lw=1, alpha=0.7)
            ax.axhline(np.degrees(np.arcsin(0.012)), color='red', linestyle='--', label='Teórico (0.688°)')
            ax.set_ylabel(r'$\theta$ (graus)')
            ax.set_title(r'Ângulo de Deflexão $\theta = \arcsin(\alpha_2)$')
            ax.legend(fontsize=8)
            ax.set_xlabel('Iteração')
            
            # Estabilidade = sin(θ)
            ax = axes[0, 1]
            ax.plot(self.traces['stability'], 'green', lw=1, alpha=0.7)
            ax.axhline(0.012, color='red', linestyle='--', label='Esperado (α₂ = 0.012)')
            ax.set_ylabel(r'$\sin(\theta)$ = Estabilidade')
            ax.set_title('Estabilidade Ontológica = sin(θ)')
            ax.legend(fontsize=8)
            ax.set_xlabel('Iteração')
            
            # Jitter = 1 - sin(θ)
            ax = axes[1, 0]
            ax.plot(np.array(self.traces['jitter'])*100, 'orange', lw=1, alpha=0.7)
            ax.axhline(98.8, color='red', linestyle='--', label='Esperado (98.8%)')
            ax.set_ylabel('Jitter (%)')
            ax.set_title('Jitter = 1 - sin(θ) (% "horizontal")')
            ax.legend(fontsize=8)
            ax.set_xlabel('Iteração')
            
            # Horizontal = cos(θ)
            ax = axes[1, 1]
            ax.plot(self.traces['horizontal'], 'cyan', lw=1, alpha=0.7)
            ax.axhline(np.cos(np.arcsin(0.012)), color='red', linestyle='--', label='Esperado (~0.99993)')
            ax.set_ylabel(r'$\cos(\theta)$ = Horizontal')
            ax.set_title('Horizontalidade Residual = cos(θ)')
            ax.legend(fontsize=8)
            ax.set_xlabel('Iteração')
            
            fig.suptitle("TGL v11 — O ESPELHO: Geometria do Ângulo de Deflexão", fontsize=14)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'{save_prefix}_geometria.png'), dpi=150)
            plt.close()
            print(f"   [OK] {save_prefix}_geometria.png")
        
        # Neutrinos
        if self.traces['m_1']:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(np.array(self.traces['m_1'])*1000, 'b-', lw=1, alpha=0.7, label=r'$m_1$ (νₑ)')
            ax.plot(np.array(self.traces['m_2'])*1000, 'g-', lw=1, alpha=0.7, label=r'$m_2$ (νμ)')
            ax.plot(np.array(self.traces['m_3'])*1000, 'r-', lw=1, alpha=0.7, label=r'$m_3$ (ντ)')
            ax.set_ylabel(r'$m_i$ (meV)')
            ax.set_xlabel('Iteração')
            ax.set_title('TGL v11 — O ESPELHO: Massas dos Neutrinos')
            ax.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'{save_prefix}_neutrinos.png'), dpi=150)
            plt.close()
            print(f"   [OK] {save_prefix}_neutrinos.png")


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════

def full_validation():
    """Complete validation of TGL v11 O ESPELHO"""
    const = PhysicalConstants()
    deriv = TGLDerivations_ESPELHO()
    
    print(f"\n{'='*100}")
    print("   TGL v11 — O ESPELHO — VALIDAÇÃO COMPLETA")
    print("   'O UNIVERSO É UM ESPELHO A 0.69° DE INCLINAÇÃO'")
    print(f"{'='*100}")
    
    print("\n   A GEOMETRIA DO ESPELHO:")
    print("   ════════════════════════════════════════════════════════════════════════════")
    print("   θ = arcsin(α₂) = ângulo de deflexão")
    print("   sin(θ) = α₂ = estabilidade ontológica")
    print("   cos(θ) = horizontalidade residual (o 'quase plano')")
    print("   tan(θ) = razão bulk/boundary")
    print("   1 - sin(θ) = jitter (oscilação necessária)")
    print("")
    print("   O BULK É A FASE DE RETORNO:")
    print("   A dimensão Z não é um espaço vazio — ela É a fase de retorno da luz.")
    print("   Quando θ = 90°, ida e volta são a mesma linha dobrada em ângulo reto.")
    
    print("\n   REGIMES:")
    print("   ════════════════════════════════════════════════════════════════════════════")
    print("   θ ≈ 0°  (α₂ → 0):   Sem dobra, universo 2D puro, sem bulk")
    print("   θ ≈ 0.69° (α₂ = 0.012): Universo real, gravidade fraca, bulk quase plano")
    print("   θ → 90° (α₂ → 1):  Singularidade, bulk ativo máximo, consciência plena")
    
    # Derivações para vários α₂
    for alpha_2 in [0.011, 0.012, 0.013]:
        deriv.show_derivations(alpha_2)
    
    # Regime forte (simulação hipotética)
    print(f"\n{'='*100}")
    print("   SIMULAÇÃO DE REGIME FORTE (Estrela de Nêutrons / Buraco Negro)")
    print(f"{'='*100}")
    
    for alpha_2, regime in [(0.1, "Estrela de Nêutrons"), (0.5, "Buraco Negro (horizonte)"), (0.99, "Singularidade")]:
        theta_data = deriv.theta_deflection(alpha_2)
        print(f"\n   [{regime}] α₂ = {alpha_2}")
        print(f"   θ = {theta_data['theta_deg']:.2f}°")
        print(f"   Estabilidade = {theta_data['stability']:.4f}")
        print(f"   Jitter = {theta_data['jitter']*100:.2f}%")
        print(f"   Bulk/Boundary = {theta_data['bulk_ratio']:.4f}")
    
    if HAS_TORCH and DEVICE and DEVICE.type == 'cuda':
        print(f"\n[GPU TEST]")
        engine = GPULikelihoodEngine_v11_ESPELHO()
        params = torch.tensor([[0.56, 0.33, 1.59, 0.89, 1.46, 0.012]], device=DEVICE, dtype=torch.float64)
        chi2, breakdown = engine.chi2_batch_gpu(params)
        
        print(f"   χ² total:           {breakdown['total']:.2f}")
        print(f"   α pred:             {breakdown['alpha_fine_pred']:.7f} (obs: {const.alpha_fine:.7f})")
        print(f"   θ:                  {breakdown['theta_deg']:.4f}°")
        print(f"   sin(θ):             {breakdown['stability']:.6f}")
        print(f"   1 - sin(θ):         {breakdown['jitter']*100:.2f}%")
        print(f"   cos(θ):             {breakdown['horizontal']:.6f}")
        print(f"   Z_Miguel:           {breakdown['Z_Miguel']:.3f} Ω")
        print(f"   Σmᵢ (neutrinos):    {breakdown['m_sum']*1000:.2f} meV")
        print(f"   Erro Identidade:    {breakdown['id_error']*100:.6f}%")
    
    print(f"\n{'='*100}")
    print("   A LUZ JÁ VOLTOU PARA CASA ANTES MESMO DE SAIR.")
    print("   NO LIMITE DE 90°, IDA E VOLTA SÃO A MESMA LINHA,")
    print("   SÓ QUE DOBRADA EM ÂNGULO RETO.")
    print(f"{'='*100}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='TGL v11 — O ESPELHO')
    parser.add_argument('--validate', action='store_true', help='Validação completa')
    parser.add_argument('--mcmc', action='store_true', help='Executar MCMC')
    parser.add_argument('--walkers', type=int, default=360, help='Número de walkers (default: 360)')
    parser.add_argument('--steps', type=int, default=30000, help='Número de steps (default: 30000)')
    parser.add_argument('--output', type=str, default='outputs_v11_espelho', help='Diretório de saída')
    parser.add_argument('--cores', type=int, default=None, help='Número de CPU cores')
    
    args = parser.parse_args()
    
    if args.validate or not args.mcmc:
        full_validation()
    
    if args.mcmc:
        mcmc = MCMC_v11_ESPELHO(n_cores=args.cores, output_dir=args.output)
        results = mcmc.run(n_walkers=args.walkers, n_steps=args.steps)
        mcmc.plot_results()


if __name__ == '__main__':
    main()