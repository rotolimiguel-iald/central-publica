import hashlib, os, re
base = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out"
for n in ["OPERADOR_28out_resposta_quatro_bocas_ramo_b_verbatim.txt",
          "OPERADOR_28out_ratificacao_calibrar_nao_e_validar_verbatim.txt",
          "OPERADOR_27e28out_prossiga_com_tudo_verbatim.txt"]:
    b = open(os.path.join(base, n), "rb").read()
    print("=====", n, len(b), "B", hashlib.sha256(b).hexdigest()[:16])
    print(b.decode("utf-8", "replace"))
