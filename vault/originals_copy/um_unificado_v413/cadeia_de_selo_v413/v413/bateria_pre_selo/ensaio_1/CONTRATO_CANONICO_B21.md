# Contrato de fidelidade da Bancada Um -- B21 / v412 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.6 (13/11/2026) em 20261120_223826 UTC, no passo B(21) da cadeia de selo da v412, sob o evento c1 None.

## Identidade pinada

- um.py v412: sha256 3e741dcaa58ef2b8c2044ff264570c5d82b499308b70a84b422170609d25bd3b (50167683 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 60f00e9818f71b73facf29afb37c04fa0d64bfead8520f3685ee10a198761fb4.
- manifesto anterior: B20-v411-20261113-R1 (sha256 f2ed66a8a6ce96f45fa341a6b3ac38a210e5566b2f58f692bd9fb095eb84e103).
- recibo pre-selo (testes finais contra a versao anterior): sha256 (ausente: so em --sandbox).

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.

## Salto (R3.4)

A Bancada pinava v411 e foi levada a v412 sem passar pelas versoes puladas v412 (nenhuma delas teve elo B(n)). A cadeia de selos (sha256 c8a584001185c599fe1d578f89982824753e55cc08c267887431b99a4b9dfeec, 2 elos) liga,
por hash, o que a Bancada pinava ao Nos que o recibo pre-selo testou (v412): copias de bytes de cada versao, o selo de cada uma pinando o seu um.py e o
seu manifesto do kernel, e o registro do instalador de cada troca com os backups de bytes. Sem cadeia verificavel o salto e recusado.
