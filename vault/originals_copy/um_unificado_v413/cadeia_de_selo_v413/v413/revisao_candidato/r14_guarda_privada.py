# r14 -- a contagem da guarda privada da G1 (E03) sobre o um.py v412 selado e o CANDIDATO v413, so' contagens (nenhum padrao impresso nem gravado).
# SO LEITURA. Com e sem o nome de modulo "Trinity" isento (para ver se todo acerto novo se explica so' por ele).
import os, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools\custodia_g1")
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
import importlib.util

ESP = r"C:\IALD\Central de Patentes\tools\custodia_g1\espelho_pares.py"
BASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"


def main():
    try:
        spec = importlib.util.spec_from_file_location("custodia_g1.espelho_pares", ESP, submodule_search_locations=None)
        import custodia_g1.espelho_pares as EP   # noqa
    except Exception:
        EP = None
    if EP is None:
        print("nao carreguei espelho_pares"); return
    priv = EP.carregar_marcadores_privados()
    b = EP.guarda_conta(BASE, priv)
    c = EP.guarda_conta(CAND, priv)
    ci = EP.guarda_conta(CAND, priv, isentos=("Trinity", "trinity", "TRINITY"))
    bi = EP.guarda_conta(BASE, priv, isentos=("Trinity", "trinity", "TRINITY"))
    print("n_marcadores_privados:", len(priv))
    print("base v412: %s acertos ; candidato v413: %s acertos ; delta: %s" % (b, c, (c - b) if (b is not None and c is not None) else None))
    print("com o nome de modulo isento (Trinity/trinity/TRINITY): base %s ; candidato %s ; delta %s" % (bi, ci, (ci - bi) if (bi is not None and ci is not None) else None))
    for iso in (("Trinity",), ("Trinity", "trinity"), ("Trinity", "TRINITY")):
        print("so' %s isento: base %s ; candidato %s" % ("/".join(iso), EP.guarda_conta(BASE, priv, isentos=iso), EP.guarda_conta(CAND, priv, isentos=iso)))


if __name__ == "__main__":
    main()
