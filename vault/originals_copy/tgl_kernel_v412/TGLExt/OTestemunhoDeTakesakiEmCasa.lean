import TGLExt.AperiodicCentralizerExpectation
import TGLExt.TheImportedExpectation

set_option autoImplicit false

/-!
# O testemunho de Takesaki está em casa: os quatro campos, para todo perfil da torre

Para todo perfil da torre, o testemunho de quatro campos (`TakesakiInput`, em `TGLExt.TheImportedExpectation`;
ciclicidade, separação, continuidade WOT sequencial do estado, existência da esperança) está habitado. A esperança
condicional sobre o centralizador é o limite forte das médias de Cesàro do fluxo modular da própria torre
(`ChatgptAudit.Aperiodic046.aperiodicExpectationInput`, em `TGLExt.AperiodicCentralizerExpectation`). O teorema de
Takesaki [KNOWN, 1972] segue sendo a referência do caso geral. Nada se afirma sobre a cunha e o vácuo da luz, nem que o
gate se mova.

## O que fica provado

1. ★ `o_testemunho_de_takesaki_esta_em_casa`: para todo perfil da torre, o testemunho de Takesaki está habitado, com
   os quatro campos provados em casa. É uma linha: o teorema selado `the_testimony_is_exactly_the_conclusion` (o
   testemunho equivale à existência do contrato da esperança) aplicado ao habitante selado
   `aperiodic_contract_inhabited`.
2. `a_esperanca_existe_sem_importar`: a conclusão que o módulo importado tirava do testemunho
   (`the_expectation_exists_by_import`) vale para todo perfil, agora sem hipótese.

## Como ler

Na torre, a esperança condicional sobre o centralizador não é mais dívida importada: está construída em casa, e é a média do relógio (a média de Cesàro do fluxo modular, com limite forte). O teorema de Takesaki segue
sendo a referência conhecida para o caso geral [KNOWN, Takesaki 1972]; para a torre desta casa ele não é mais
necessário como importação.

## O que NÃO se afirma

* Nada de novo sobre a construção: ela é a de `aperiodicExpectationInput`, já selada. Este arquivo só compõe.
* Nada sobre a cunha e o vácuo da luz: o centralizador da torre tem elementos não escalares (é do estado produto); o
  setor da luz tem outros dados. Ligar o `K = −log Δ` da luz à dinâmica do custo pede uma aplicação que entrelace as
  duas representações; isso segue em aberto.
* Que o Lema 3 esteja declarado resolvido, nem que o gate se mova. Validade no kernel não é creditação.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OTestemunhoDeTakesakiEmCasa

open TGLExt

/-- ★ **O TESTEMUNHO DE TAKESAKI ESTÁ EM CASA.** Para todo perfil da torre, os quatro campos do testemunho estão
provados: a esperança condicional sobre o centralizador é a construída em `aperiodicExpectationInput`. -/
theorem o_testemunho_de_takesaki_esta_em_casa (P : SiteProfile) : TakesakiInput P :=
  (the_testimony_is_exactly_the_conclusion P).2 (ChatgptAudit.Aperiodic046.aperiodic_contract_inhabited P)

/-- A conclusão que o módulo importado tirava do testemunho vale para todo perfil, sem hipótese. -/
theorem a_esperanca_existe_sem_importar (P : SiteProfile) : Nonempty (ExpectationInput P) :=
  ChatgptAudit.Aperiodic046.aperiodic_contract_inhabited P

end TGLExt.OTestemunhoDeTakesakiEmCasa
