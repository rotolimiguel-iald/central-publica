"""
tgl_camb_worker_v2fix.py — copia CORRIGIDA do tgl_camb_worker.py de maio de 2026 (o original NAO foi tocado).
=====================================================================================================
AUTOPSIA (10/09/2026): em D_M_TGL a distancia comovel ate z_* ~ 1090 era integrada por trapezios em 300 pontos numa grade LINEAR em z
(passo ~3,6), onde c/H varia mais depressa; o resultado, mesmo com beta = 0, dava DM_* = 16589 Mpc contra 13871 Mpc do proprio CAMB
(+19,6%): R = 2,09 (Planck 1,75), l_A = 361 (Planck 301,5), chi^2 ~ 16000 em 16 pontos. As distancias DESI (z <= 2,33; 200 pontos) nao
sofriam. CORRECAO (unica): integrar em u = ln(1+z) com grade densa e vetorizada, e AUTOVERIFICAR em beta = 0 contra o CAMB
(dm_selfcheck_ratio = DM_TGL(beta=0)/DM_LCDM gravado na saida). Tudo o mais e identico ao worker de maio, inclusive a aproximacao
DECLARADA do r_s (escala por H_LCDM/H_TGL em z_*).
"""
import sys
import json
import numpy as np

try:
    import camb
    from camb import model
except ImportError:
    print("ERROR: camb not installed. Install with: pip install camb", file=sys.stderr)
    sys.exit(1)


C_KMS = 299792.458


def _omega_r0(H0, TCMB=2.7255, Neff=3.046):
    h2 = (H0 / 100.0) ** 2
    Ogamma_h2 = 4.4814e-7 * TCMB**4
    Onu_h2 = Ogamma_h2 * Neff * (7.0/8.0) * (4.0/11.0)**(4.0/3.0)
    return (Ogamma_h2 + Onu_h2) / h2


def H_z_TGL(z, beta, H0, ombh2, omch2, TCMB=2.7255, Neff=3.046, mnu=0.06):
    """TGL-modified Friedmann analytic H(z). (identico a maio; aceita arrays)"""
    h2 = (H0 / 100.0) ** 2
    Or0 = _omega_r0(H0, TCMB=TCMB, Neff=Neff)
    Om0 = (ombh2 + omch2 + mnu/93.14) / h2
    OL0 = 1.0 - Or0 - Om0
    a = 1.0 / (1.0 + np.asarray(z, dtype=float))
    rho_r = Or0 / a**4
    rho_m = Om0 / a**3
    rho_L = OL0
    rho_tot = rho_r + rho_m + rho_L
    we = (rho_r / 3.0 - rho_L) / rho_tot
    Phi = 1.0 + beta * np.abs(1.0 + we)
    return H0 * np.sqrt(rho_tot * Phi)


def D_M_TGL(z, beta, H0, ombh2, omch2, npts=20001, TCMB=2.7255, Neff=3.046, mnu=0.06):
    """Comoving transverse distance with TGL H(z). CORRIGIDO: integra em u = ln(1+z), grade densa e vetorizada."""
    u = np.linspace(0.0, np.log1p(z), npts)
    zz = np.expm1(u)
    H = H_z_TGL(zz, beta, H0, ombh2, omch2, TCMB=TCMB, Neff=Neff, mnu=mnu)
    return float(np.trapezoid(C_KMS * (1.0 + zz) / H, u))


def main():
    if len(sys.argv) != 3:
        print("Usage: python tgl_camb_worker_v2fix.py input.json output.npz", file=sys.stderr)
        sys.exit(2)

    path_in = sys.argv[1]
    path_out = sys.argv[2]

    with open(path_in, 'r') as fh:
        p = json.load(fh)

    beta = float(p['beta'])
    H0 = float(p['H0'])
    ombh2 = float(p['ombh2'])
    omch2 = float(p['omch2'])
    tau = float(p.get('tau', 0.0544))
    ns = float(p.get('ns', 0.9649))
    As = float(p.get('As', 2.1e-9))
    mnu = float(p.get('mnu', 0.06))
    TCMB = float(p.get('TCMB', 2.7255))
    Neff = float(p.get('Neff', 3.046))
    lmax = int(p.get('lmax', 20))
    desi_z = p.get('desi_z', [])

    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, tau=tau, TCMB=TCMB, nnu=Neff)
    pars.InitPower.set_params(ns=ns, As=As)
    pars.set_dark_energy(w=-1.0, wa=0.0)
    pars.set_for_lmax(lmax, lens_potential_accuracy=0)

    results = camb.get_background(pars)

    derived = results.get_derived_params()
    z_star = float(derived['zstar'])
    z_drag = float(derived['zdrag'])
    r_star_LCDM_Mpc = float(derived['rstar'])
    r_drag_LCDM_Mpc = float(derived['rdrag'])
    DAstar_LCDM_Mpc = float(results.angular_diameter_distance(z_star))
    DM_star_LCDM_Mpc = DAstar_LCDM_Mpc * (1.0 + z_star)

    h2 = (H0/100.0)**2
    Or0 = _omega_r0(H0, TCMB=TCMB, Neff=Neff)
    Om0 = (ombh2 + omch2 + mnu/93.14) / h2
    OL0 = 1.0 - Or0 - Om0

    H_LCDM_zstar = H0 * np.sqrt(Or0/(1.0/(1+z_star))**4 + Om0/(1.0/(1+z_star))**3 + OL0)
    H_TGL_zstar = float(H_z_TGL(z_star, beta, H0, ombh2, omch2, TCMB=TCMB, Neff=Neff, mnu=mnu))

    r_star_TGL = r_star_LCDM_Mpc * (H_LCDM_zstar / H_TGL_zstar)
    r_drag_TGL = r_drag_LCDM_Mpc * (H_LCDM_zstar / H_TGL_zstar)

    DM_star_TGL_Mpc = D_M_TGL(z_star, beta, H0, ombh2, omch2, TCMB=TCMB, Neff=Neff, mnu=mnu)
    DAstar_TGL_Mpc = DM_star_TGL_Mpc / (1.0 + z_star)
    # AUTOVERIFICACAO: a integracao analitica em beta = 0 tem de reproduzir o CAMB
    DM_star_check = D_M_TGL(z_star, 0.0, H0, ombh2, omch2, TCMB=TCMB, Neff=Neff, mnu=mnu)
    dm_selfcheck_ratio = DM_star_check / DM_star_LCDM_Mpc

    Om_h2 = ombh2 + omch2 + mnu/93.14
    Omega_m = Om_h2 / h2
    R = np.sqrt(Omega_m) * (H0 / C_KMS) * DM_star_TGL_Mpc
    lA = np.pi * DM_star_TGL_Mpc / r_star_TGL

    H_at_DESI = [float(H_z_TGL(z, beta, H0, ombh2, omch2, TCMB=TCMB, Neff=Neff, mnu=mnu)) for z in desi_z]
    DM_at_DESI = [D_M_TGL(z, beta, H0, ombh2, omch2, npts=4001, TCMB=TCMB, Neff=Neff, mnu=mnu) for z in desi_z]

    np.savez(path_out,
             beta=beta, H0=H0, ombh2=ombh2, omch2=omch2,
             z_star=z_star, z_drag=z_drag,
             r_star_LCDM=r_star_LCDM_Mpc, r_drag_LCDM=r_drag_LCDM_Mpc,
             r_star_TGL=r_star_TGL, r_drag_TGL=r_drag_TGL,
             DAstar_LCDM=DAstar_LCDM_Mpc, DAstar_TGL=DAstar_TGL_Mpc,
             DM_star_LCDM=DM_star_LCDM_Mpc, DM_star_TGL=DM_star_TGL_Mpc,
             dm_selfcheck_ratio=dm_selfcheck_ratio,
             R=R, lA=lA, Omega_m=Omega_m,
             desi_z=np.array(desi_z),
             H_at_DESI=np.array(H_at_DESI),
             DM_at_DESI=np.array(DM_at_DESI))


if __name__ == "__main__":
    main()
