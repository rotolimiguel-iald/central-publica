import TGLExt.AperiodicCentralizerExpectation
import TGLExt.TheImportedExpectation

set_option autoImplicit false

/-!
# O testemunho de Takesaki está em casa: os quatro campos, para todo perfil da torre
[candidata da gerência c1, 17/11/2026, R0; nome provisório; nada instalado; o nome é do operador]

## De onde vem

Em 17/11/2026 o operador mandou: «tem que descarregar e tem que resolver tomita, tem que fazer a ligação, porque é o hamiltoniano oculto» (por bytes em `Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_17nov_e_isso_exatamente_mas_tem_que_descarregar_e_resolver_tomita`).

A gerência disse a ele que a esperança condicional na torre infinita seguia importada e que a parede não tinha sido
medida. Estava errada, e o erro foi de aferição: procurou habitantes de `TakesakiInput` e não procurou habitantes de
`ExpectationInput`. O revisor (ordem 025, unidade Y5) achou o que o kernel já tinha desde setembro: a ENTREGA 046 da
bancada, selada em `TGLExt.AperiodicCentralizerExpectation`, constrói a esperança para todo perfil da torre
(`ChatgptAudit.Aperiodic046.aperiodicExpectationInput`), como limite forte da média de Cesàro do fluxo modular, com as
três cláusulas do contrato; e o levantamento já dispara sobre ela (`the_lift_fires_on_the_aperiodic_tower`, em
`TGLExt.AperiodicTowerLift`).

O que não estava escrito em lugar nenhum era a composição: que, com isso, o testemunho de quatro campos
(`TakesakiInput`, em `TGLExt.TheImportedExpectation`), cujo quarto campo o cabeçalho daquele módulo ainda chama de
conclusão importada, está habitado em casa para todo perfil. O revisor compôs os dois termos selados no arquivo
`Verificacao025.lean` da conferência dele; este arquivo é a mesma composição, recompilada pela gerência.

## O que fica provado

1. ★ `o_testemunho_de_takesaki_esta_em_casa`: para todo perfil da torre, o testemunho de Takesaki está habitado, com
   os quatro campos provados em casa. É uma linha: o teorema selado `the_testimony_is_exactly_the_conclusion` (o
   testemunho equivale à existência do contrato da esperança) aplicado ao habitante selado
   `aperiodic_contract_inhabited`.
2. `a_esperanca_existe_sem_importar`: a conclusão que o módulo importado tirava do testemunho
   (`the_expectation_exists_by_import`) vale para todo perfil, agora sem hipótese.

## Como ler

Na torre, a esperança condicional sobre o centralizador não é mais dívida importada: foi construída em casa em
setembro, e é a média do relógio (a média de Cesàro do fluxo modular, com limite forte). O teorema de Takesaki segue
sendo a referência conhecida para o caso geral [KNOWN, Takesaki 1972]; para a torre desta casa ele não é mais
necessário como importação.

## O que NÃO se afirma

* Nada de novo sobre a construção: ela é da ENTREGA 046, já selada. Este arquivo só compõe.
* Nada sobre a cunha e o vácuo da luz: o centralizador da torre tem elementos não escalares (é do estado produto); o
  setor da luz tem outros dados. Ligar o `K = −log Δ` da luz à dinâmica do custo pede uma aplicação que entrelace as
  duas representações; isso segue em aberto.
* Que o Lema 3 esteja declarado resolvido, nem que o gate se mova. Validade no kernel não é creditação.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OTestemunhoDeTakesakiEmCasa

open TGLExt

/-- ★ **O TESTEMUNHO DE TAKESAKI ESTÁ EM CASA.** Para todo perfil da torre, os quatro campos do testemunho estão
provados: a esperança condicional sobre o centralizador é a construída na ENTREGA 046. -/
theorem o_testemunho_de_takesaki_esta_em_casa (P : SiteProfile) : TakesakiInput P :=
  (the_testimony_is_exactly_the_conclusion P).2 (ChatgptAudit.Aperiodic046.aperiodic_contract_inhabited P)

/-- A conclusão que o módulo importado tirava do testemunho vale para todo perfil, sem hipótese. -/
theorem a_esperanca_existe_sem_importar (P : SiteProfile) : Nonempty (ExpectationInput P) :=
  ChatgptAudit.Aperiodic046.aperiodic_contract_inhabited P

end TGLExt.OTestemunhoDeTakesakiEmCasa

#print axioms TGLExt.OTestemunhoDeTakesakiEmCasa.o_testemunho_de_takesaki_esta_em_casa
#print axioms TGLExt.OTestemunhoDeTakesakiEmCasa.a_esperanca_existe_sem_importar
