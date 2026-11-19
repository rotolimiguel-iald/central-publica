import os, re
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
def rd(n): return open(os.path.join(base, n), "rb").read().decode("utf-8")
detail = {n: rd(n) for n in ("M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md", "HUBBLE_JA_EXAMINADO_K04.md", "COMBINACAO_K04.md", "RESSALVAS_UMA_A_UMA_K04.md", "ERRATA_NEUTRINO_V412_RASCUNHO_K04.md")}
# + jsons de medidas
for n in (r"K04\M2\medidas\resultados_planejamento.json", r"K04\HUBBLE\MEDIDAS_PLANEJAMENTO_K04.json", r"K04\M2\medidas\tabelas_planejamento.md", r"K04\HUBBLE\MEDIDAS_PLANEJAMENTO_K04.md"):
    detail[n] = rd(n)
topo = {n: rd(n) for n in ("ENTREGA_K04.md", "PERGUNTA_K04.md", "DEPOSITO_K04.md")}
nums = ["64,74", "66,13", "12,88", "3,48", "35,04", "31,47", "99,86", "99,42", "1,937997", "1,928084", "3,605", "380,08", "31/03/2028", "19/09/2031", "7,306061", "0,102640", "7,068", "8,068", "3,256", "2,462", "2,689", "2,206054", "7,842905784155273", "0,02642", "25,49", "25,69", "6,9", "9,6", "14,5", "2034", "6,2663", "96,4"]
alt = lambda s: [s, s.replace(",", ".")]
for s in nums:
    em_topo = [n for n, t in topo.items() if s in t]
    em_det = [n for n, t in detail.items() if any(a in t for a in alt(s))]
    print("%-20s topo=%-34s detalhe=%s" % (s, ",".join(x.split("_")[0] for x in em_topo), ",".join(x.split("_")[0].split("\\")[-1][:10] for x in em_det)))
