#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/cadeia_parte2_v411.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/cadeia_parte2_v412.sh.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] REMISSAO CURTA: na v411 a sequencia inteira da preparacao (registro offline, guardas, candidato, comparacao, ensaio a seco, ESPERADOS, conferidores, citacoes, diff e pinos, instalar/rito, p00, fim_de_cadeia com o B20 pre-selo, relatorio) esta' em cadeia_v411.sh, uma so' e fail-closed; a logica da cadeia_parte2_v410.sh nao e' duplicada aqui.
# O que a cadeia_parte2_v411.sh fazia alem disso, na v412: a pendencia do MEMORY.md (o p00 a diz pendente; so' a gerencia escreve o MEMORY.md), a purga (purga_v412.py --listar, ~20 min, so' leitura) e o deposito do construtor (depositar_construtor_v412.py, so' com PREPARACAO_v412_PRONTA.json pronta = true) -- chamados pelo nome depois da cadeia_v412.sh.
# uso: sh ./cadeia_parte2_v412.sh   (repassa a cadeia_v412.sh; o modo de ensaio do topo proposto vem do ambiente, V412_ENSAIO_TOPO_PROPOSTO=1)
cd "$(dirname "$0")" || exit 9
[ -f ./cadeia_v412.sh ] || { echo "FALTA cadeia_v412.sh (a sequencia da v412)"; exit 9; }
exec sh ./cadeia_v412.sh "$@"
