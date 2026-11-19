#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/refazer_sandbox_v411_pos_selo.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/refazer_sandbox_v412_pos_selo.sh.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] pos-selo: chama refazer_arvore_v411_pos_selo.py (NAO executado na preparacao); a v411 nao tem modulo novo (o recibo nao lista pedra)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] pos-selo: chama refazer_arvore_v410_pos_selo.py (NAO executado na preparacao); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# pos-selo: a v412 ja esta no Nos; a arvore so-fontes do recibo (C:/t/k412c/arvore) e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v412.json (raiz, Audit, os modulos novos em TGLExt/ -- nenhum na v412 -- e as contagens de .lean). SO' DEPOIS do selo/instalacao; apaga e refaz a arvore.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v412_pos_selo.py
