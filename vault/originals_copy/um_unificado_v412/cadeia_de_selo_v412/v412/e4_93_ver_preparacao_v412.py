import json, sys
sys.stdout.reconfigure(encoding="utf-8")
p = json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\PREPARACAO_v412_PRONTA.json", encoding="utf-8"))
nulos = [k for k, v in p.items() if v is None]
print("chaves nulas:", nulos)
for k in ("estado", "contrato_seguido", "candidato", "escada", "ensaio_a_seco"):
    print(k, "=", json.dumps(p[k], ensure_ascii=False)[:700])
kn = p["kernel"]
print("kernel:", json.dumps({k: kn[k] for k in ("n_modulos", "pos_build_ok", "linha_TOTAL", "delta_vs_quinta_lista", "declaracoes_dos_dois_modulos_novos", "fora_do_trio", "avisos_fora_o_conhecido", "chaves_antigas_mudam", "checagem_built_corrigida", "nos_intacto")}, ensure_ascii=False)[:900])
print("registros:", json.dumps({k: p["registros"][k] for k in ("nomes", "recibo_ok", "n_ancoras_total")}, ensure_ascii=False), p["registros"]["ancoras_escolhidas"]["n_por_registro"])
g = p["guarda_de_frases"]
print("guarda:", json.dumps({"controles": g["controles"]["n_ok"], "de": g["controles"]["n"], "trav": g["travessia"], "hist": g["verificador_de_historia"], "f43": g["formas_da_F43_nos_textos_emitidos"], "marc": g["marcadores_herdados"]}, ensure_ascii=False)[:900])
print("pilar:", p["portao_do_pilar_no_candidato"]["ok"], p["portao_do_pilar_no_candidato"]["resumo"], "| privado:", p["guarda_de_material_privado"])
