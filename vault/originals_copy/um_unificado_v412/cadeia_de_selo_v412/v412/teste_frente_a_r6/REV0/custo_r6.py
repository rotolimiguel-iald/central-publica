# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026. Teste da frente A, desenho R6: o custo do conjunto proposto, em unidades de texto.
So' aritmetica. Nenhum modelo. TODOS os tamanhos sao ESTIMATIVA da gerencia (nenhuma pagina foi escrita ainda):
entrada do assento 25 unidades; pagina curta 450; instrucao 400; resposta 120. Mudam quando o material existir.

Conjunto proposto: G grupos no braco 1 (4 apresentacoes cada); o braco 2 sobre os mesmos G grupos (4 cada); o braco 3
em G/2 pares de assentos (2 apresentacoes novas por par; as outras duas sao do braco 1); 8 apresentacoes do controle de
letra igual; e o controle do aparelho (as 4G apresentacoes do braco 1 SEM o indice). Dois modos de dar o indice: so' o assento do endereco, ou o indice inteiro (os G assentos).
Uso: custo_r6.py <saida.json> [grupos=16] [entradas=8]"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
saida = Path(sys.argv[1]); G = int(sys.argv[2]) if len(sys.argv) > 2 else 16; NENT = int(sys.argv[3]) if len(sys.argv) > 3 else 8
ENTRADA, PAGINA, INSTRUCAO, RESPOSTA, CARIMBO = 25, 450, 400, 120, NENT * 25
ap = {"braco_1_o_par": 4 * G, "braco_2_o_carimbo": 4 * G, "braco_3_o_canal": 2 * (G // 2), "controle_de_letra_igual": 8, "controle_do_aparelho_sem_o_indice": 4 * G}
total = sum(ap.values())
assento, indice = NENT * ENTRADA, G * NENT * ENTRADA


def soma(reg):
    ent = 0
    for k, n in ap.items():
        ent += n * (INSTRUCAO + PAGINA + (0 if k == "controle_do_aparelho_sem_o_indice" else reg) + (CARIMBO if k == "braco_2_o_carimbo" else 0))
    return {"entrada": ent, "saida": total * RESPOSTA, "total": ent + total * RESPOSTA}


res = {"gerado_por": "custo_r6.py", "nota": "TODOS os tamanhos sao estimativa da gerencia; nenhuma pagina foi escrita",
       "estimativas": {"entrada_do_assento": ENTRADA, "pagina": PAGINA, "instrucao": INSTRUCAO, "resposta": RESPOSTA},
       "grupos": G, "entradas_por_assento": NENT, "apresentacoes": ap, "apresentacoes_no_total": total,
       "textos_novos_a_escrever_e_conferir": {"paginas_curtas": 2 * G, "assentos": G, "paginas_do_controle_de_letra_igual": 8,
                                              "unidades_de_texto_novo_(estimativa)": 2 * G * PAGINA + G * assento + 8 * PAGINA},
       "por_sistema_dando_so_o_assento_do_endereco": soma(assento),
       "por_sistema_dando_o_indice_inteiro": soma(indice)}
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
