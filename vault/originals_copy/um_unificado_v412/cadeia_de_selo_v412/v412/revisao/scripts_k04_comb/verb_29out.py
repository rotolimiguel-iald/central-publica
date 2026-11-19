import hashlib, os
base = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
for n in ("OPERADOR_29out_autoriza_conjunto_D_verbatim.txt",
          "OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt"):
    b = open(os.path.join(base, n), "rb").read()
    print("=====", n, len(b), hashlib.sha256(b).hexdigest()[:16])
    t = b.decode("utf-8", "replace")
    print(t[:1800])
