"""Revisor K04/Hubble: para cada linha da tabela do Kimi, confere se os seq citados pertencem a rota citada (via 'rotas.py ver', so leitura)."""
import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
(OUT / "ver").mkdir(exist_ok=True)
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
PY = r"C:\Python314\python.exe"


def rng(a, b):
    return list(range(a, b + 1))

LINHAS = {
 1: ("supernovas.pantheon_errata_cosmologica", [34, 149]),
 2: ("d1.camb.v3_real", [50, 71, 105] + rng(145, 148) + [151, 152, 178, 180]),
 3: ("d1.fase1_eff_30set", [181] + rng(186, 192)),
 4: ("d1.fase2_dois_setores_30set", [185] + rng(193, 196) + [198, 222]),
 5: ("d1.fase3_leitores_h0", rng(203, 214) + [221]),
 6: ("d1.fase3bis_d1b_convencao_artigo", [220]),
 7: ("d1.fase4_desvio_30set", [223] + rng(225, 231) + [406, 410]),
 8: ("um_py.v378.o_que_faltou_contraste_fase4", [233, 234]),
 9: ("d1.fase5_sh0es_01out", rng(236, 242) + [388, 407]),
 10: ("discriminante.ordem018.f1b.fase45_conjunta", [405, 409] + rng(413, 415) + [418, 420] + rng(423, 425) + [427, 430, 431, 438, 440]),
 11: ("discriminante.ordem018.f2.r_d", [376, 389, 394]),
 12: ("discriminante.ordem018.f2.r_e", [377, 390, 1633, 1635]),
 13: ("discriminante.ordem018.f2.r_f", [378, 1636]),
 14: ("discriminante.ordem018.f2.r_g", [379, 391, 393, 1637]),
 "15a": ("hubble.fase9_razao_discriminante", [373, 603]),
 "15b": ("d1.fase9.razao_de_hubble.lentes_05out", [373, 603]),
 "16a": ("d1.fase9.razao_de_hubble.v1_06out", [604, 647]),
 "16b": ("hubble.fase9_razao_discriminante", [604, 647]),
 "17a": ("d1.fase9.razao_de_hubble.v1_06out", [696, 741, 742, 783]),
 "17b": ("hubble.fase9_razao_discriminante", [696, 741, 742, 783]),
 "18a": ("d1.fase9.f3_auditoria_cetica_c1_07out", [773]),
 "18b": ("d1.fase9.f3_1_reauditoria_v2r2_c1_08out", [836]),
 19: ("d1.fase9.f3_1_semantica_v1x_leitores", [751, 826, 832, 834, 876, 895, 911, 929, 942] + rng(950, 952) + [959, 961, 968, 972, 975, 978]),
 20: ("d1.fase9.v2_c1_a_unica_palavra_23out", [1353, 1354, 1360, 1656]),
 "21a": ("estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", [2017, 2038]),
 "21b": ("umpy.v411.selada_h0dn_aberto_12nov", [2017, 2038]),
 "22a": ("hubble.k_sem_portador_fisico_02nov", [1639, 1644, 1646, 1649, 1650, 1654]),
 "22b": ("hubble.k_como_transposicao_inteira_ffat_02nov", [1639, 1644, 1646, 1649, 1650, 1654]),
}

cache = {}

def seqs_da_rota(i):
    if i in cache:
        return cache[i]
    p = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "ver", i], capture_output=True, text=True, encoding="utf-8")
    (OUT / "ver" / (i + ".json")).write_text(p.stdout, encoding="utf-8")
    j = json.loads(p.stdout)
    s = set()
    for r in j.get("registros", []):
        if r.get("seq") is not None:
            s.add(int(r["seq"]))
    for h in (j.get("rota", {}).get("historico") or []):
        if isinstance(h, dict) and h.get("seq") is not None:
            s.add(int(h["seq"]))
    for h in (j.get("historico") or []):
        if isinstance(h, dict) and h.get("seq") is not None:
            s.add(int(h["seq"]))
    cache[i] = (s, j)
    return cache[i]

linhas = []
for k, (rid, seqs) in LINHAS.items():
    try:
        s, j = seqs_da_rota(rid)
    except Exception as e:
        linhas.append(f"linha {k} rota {rid}: ERRO {e}")
        continue
    ausentes = [x for x in seqs if x not in s]
    linhas.append(f"linha {k} | {rid} | status={j.get('rota',{}).get('status')} | seq_da_rota(n={len(s)}) | citados={len(seqs)} | AUSENTES na rota: {ausentes}")
txt = "\n".join(linhas)
(OUT / "confere_seq_saida.txt").write_text(txt + "\n", encoding="utf-8")
print(txt)
