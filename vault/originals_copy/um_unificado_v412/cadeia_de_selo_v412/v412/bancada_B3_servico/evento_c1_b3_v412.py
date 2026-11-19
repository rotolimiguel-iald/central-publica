# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/bancada_B3_servico/evento_c1_b3_v411.py; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/bancada_B3_servico__evento_c1_b3_v412.py.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] conferido: o corpo e' o certo para a v411 (versao v411, ESPERADOS_v411.json da pasta da cadeia, candidato_sha16 LIDO e conferido contra o um.py do Nos antes de anotar; passo simples B20); o evento so' roda no rito, depois do APLICAR
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] evento do B(n) da v410 (B19, passo simples v409 -> v410); candidato_sha16 LIDO de ESPERADOS_v410.json e conferido contra o um.py do Nos antes de anotar; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v411 e em 06/11/2026 pelo fork B do claude-construtor-v411, com os rotulos subidos; na v412, adaptado em 12/11/2026 pelo fork B do claude-construtor-v412, retomada) molde v411/bancada_B3_servico/evento_c1_b3_v411.py (rotulos subidos por _bump_copia_v412.py; diff em bump/); conferido em 04/11/2026: versao v412, ESPERADOS_v412.json (candidato_sha16 LIDO, conferido contra o um.py do Nos antes de anotar), unidade F0.6, B21 sobre a producao que pina B20-v411-20261113-R1 (delta_v412.BANCADA_PINA_HOJE); nada de bundle, de contagem de modulos nem de hash digitado
"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v412 (passo simples v411 -> v412, sem salto; B21, a producao pina B20-v411-20261113-R1), no conjunto fechado de chaves do esboco R3.5. O candidato_sha16 e' LIDO de ESPERADOS_v412.json (nunca digitado) e conferido contra o um.py do Nos antes de anotar."""
import hashlib
import json
import os
import subprocess

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": "v412", "acao": "sincronizacao", "bancada": r"C:\IALD\Bancada_Um",
         "um_py": sh(NOS + r"\um.py"), "selo": sh(NOS + r"\um_absoluto_selo.json"), "unidade": "F0.6"}
D = os.path.dirname(os.path.abspath(__file__))
ESP = os.path.join(D, "..", "ESPERADOS_v412.json")
assert os.path.isfile(ESP), "ESPERADOS_v412.json nao existe ainda (e gerado antes do rito, por gerar_esperados_v412): sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado no quadro"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e o candidato de ESPERADOS_v412.json", dados["um_py"][:16], CAND16)
r = subprocess.run(["python", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA",
                    "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=r"C:\IALD\PROGRAMA_IALD")
print(r.stdout.strip(), r.stderr.strip()[-300:])
