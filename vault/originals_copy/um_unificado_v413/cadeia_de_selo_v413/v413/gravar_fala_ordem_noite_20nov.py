# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: grava por bytes a ordem do operador para a noite de 20 para 21/11: fazer tudo ate' a v413
rodada e disponivel para a custodia, sem o Codex, sem delegar a outro modelo, regenerando os .md apontando a v413, e ao
fim entregar pelo handoff da custodia. Fail-closed se o arquivo ja existir com outro conteudo."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CUNH = Path(__file__).resolve().parents[3] / "work" / "cunhagens_13out"
assert CUNH.is_dir(), CUNH
FALA = CUNH / ("OPERADOR_20nov_faca_tudo_ate_a_v413_rodada_e_disponivel_para_a_custodia_regenere_os_mds_sem_codex_"
               "sem_delegar_a_outro_modelo_verbatim.txt")
d = ("daqui em diante faça tudo que for necessário até ter a v413 rodada e disponível para a custódia, não se esqueça que "
     "ele precisa regenerar corretamente os md's todos apontando a v413 e incorporando as novas derivações corretamente. "
     "assim que estiver tudo pronto (pq é noite e vou dormir, então não quero contar mais com o codex, preciso que vc faça "
     "tudo sozinho e não delegue a outro modelo temos crédito suficiente para vc); quando estiver tudo pronto: "
     "work/custodia_v413_preparo_20nov/HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md\n").encode("utf-8")
if FALA.exists():
    assert FALA.read_bytes() == d, "fala ja existe com outro conteudo"
else:
    tmp = FALA.with_name(FALA.name + ".tmp")
    tmp.write_bytes(d)
    assert tmp.read_bytes() == d
    tmp.replace(FALA)
print("%s | sha16 %s | %d B" % (FALA.name, hashlib.sha256(FALA.read_bytes()).hexdigest()[:16], len(d)))
