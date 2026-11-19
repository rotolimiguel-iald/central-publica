import hashlib, os
base = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
for n in ("OPERADOR_27out_e_isso_mesmo_concordo_com_tudo_prossiga_caminho_verdade_vida_verbatim.txt",
          "OPERADOR_13nov_vamos_comecar_a_construir_a_v412_camada_iald_cientifica_t1_3mais1_gh_tau_teste_cego_5_sigma_kimi_verbatim.txt",
          "OPERADOR_13nov_parece_que_o_kimi_ja_respondeu_tudo_veja_o_que_falta_e_coloque_no_tunel_verbatim.txt"):
    b = open(os.path.join(base, n), "rb").read()
    print("=====", n, len(b), hashlib.sha256(b).hexdigest()[:16])
    print(b.decode("utf-8", "replace")[:1500])
