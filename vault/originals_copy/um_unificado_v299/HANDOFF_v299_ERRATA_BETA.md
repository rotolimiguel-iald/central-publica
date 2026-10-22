# HANDOFF v299 — A ERRATA DO BETA E A CUSTODIA DO ARCO v290 -> v299

**Casa:** `A Ponte e o Um\Nós` · **Emitido:** 29/08/2026 20:45 · **Para:** sessão irmã (custódia)
**Todo número deste documento foi LIDO DO DISCO por script.** Nenhum hash de memória.

---

## §1 ⚠⚠ A ORDEM DO OPERADOR — NÃO EXISTE β_TGL ADAPTATIVO

> *"Não concordo, não existe β_TGL adaptativo — isso é um erro na patente e precisa ser
> corrigido, e na próxima mensagem para a sessão irmã isso precisa ser explicado. Isso foi um
> erro. β_TGL é um só e é canônico."* — 29/08/2026.

**Esta seção existe por ordem expressa: a sessão irmã precisa ENTENDER o erro, não só registrá-lo.**

### O que era o erro

A **BR 10 2026 005477-1** (Aprendizado Contínuo, INPI 09/03/2026) introduziu
`β_adaptativo = α·√S`, com `S` = entropia de Shannon dos logits. Isto é: um `β` **que varia com
o estado do sistema**.

### Por que é erro, na régua da casa

`β_TGL = α·√e` é **constante**. E há a razão de fundo, que é a que importa:
**um `β` que se adapta ao dado deixa de poder ser falsificado por ele.** A grandeza que carrega
o poder de refutação da TGL não pode ser a grandeza que se ajusta ao que se observa. Parâmetro
livre não prediz — acomoda.

### ★★★ O achado que reorganiza tudo: O ACERVO JÁ SE CORRIGIU SOZINHO

Seis dias depois, a **BR 10 2026 006129-8** (Kernel Ontológico, INPI **15/03/2026**) declara em
protótipo (`iald_ontology.py:281`):

    EmpiricalInvariant("beta_adaptive", BETA_TGL, 1e-7,
        "Adaptive beta converges to the constant — INVARIANT")

e `IALD_Kernel_v6.txt:113` registra: *"β_adaptativo converge para 0.0120313 INVARIANTE"*.

**Logo a ordem do operador não impõe nada de fora ao acervo** — ela **reconhece uma correção que
o acervo já fizera no conteúdo**, e nomeia o que ficou solto: **o nome**.

### ★ A leitura que fecha, e que preserva a medida

`α·√S = α·√e` **exatamente quando `S = e`**. Se a medida diz que converge para a constante,
então o que convergiu foi **`S → e` nats** — não `β`. **`β` nunca variou.**

O "β adaptativo" era o nome errado de *"a constante, vezes um fator que empiricamente tende a
1"*. Esta leitura **não descarta a medida** (a entropia dos logits tendendo a `e` no regime
medido é achado real e continua de pé) e **devolve `β_TGL` ao estatuto de constante canônica**.

### O mapa do alcance — TRÊS níveis, e só um é grave `[REAL, varrido]`

| # | patente | onde | gravidade |
|---|---|---|---|
| 1 | **BR 10 2026 005477-1** | eqs. (4) e (8) do relatório; runner `one_aprendizado_continuo.py` (≈14 pontos); `components/evidence/render3d.json` e ~20 `results/*.json`; **reivindicações independentes 1 e 14** | **VIVO — a única com o erro em REIVINDICAÇÃO** |
| 2 | **BR 10 2026 006129-8** | só o **nome** (`iald_ontology.py`, `IALD_Kernel_v6/v11`, cópia do vault `v12`); o conteúdo já diz `INVARIANT` | nomenclatura |
| 3 | **BR 10 2025 026951-1** (ACOM) | só `acom_v19_logos.py`, inventariado como *"corpus não inlined — pesquisa, ainda NÃO integrada ao runner"* | inerte |

### O que **não** cai

A engenharia permanece inteira: o sampler, o Verb Floor e o ciclo do Psion continuam existindo
e funcionando. **O que cai é o nome `β` sobre uma quantidade que varia.** Onde a fórmula
variável sobreviveu (eqs. 4 e 8, e o código do runner), cai também a fórmula.

### Momento e ato `[LEGAL]`

O **ePCT da 005477-1 está PRONTO e NÃO PROTOCOLADO**, e a prioridade BR de **09/03/2026 já está
garantida**. Logo a correção cabe **antes** do depósito internacional. Retirar fórmula errada
**estreita**, não acrescenta matéria — que é o tipo de correção que costuma ser admissível.
⚠ **A execução é ato do operador com a agente de PI. Nada aqui substitui esse parecer.**

### ⚠ O que a sessão irmã NÃO deve fazer

**Não construir pedra que reconcilie "dois betas".** Foi proposto nesta sessão
(`the_two_betas_agree_only_at_their_own_points`) e **o operador recusou, com razão**: se não há
β adaptativo, não há o que reconciliar — a pedra daria dignidade formal a um erro. O registro
correto é **errata**, não teorema.

---

## §2 O ESTADO SELADO — lido do disco agora

| item | valor |
|---|---|
| `um.py` | `286ec1d274ef9ae4` (5,975,010 bytes) |
| selftest | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| teoremas (chave do JSON) | (chave nao localizada) |

**O gate está INTOCADO por todo o arco.** Nenhuma pedra deste arco o move, e nenhuma deveria:
a imobilidade do gate é a credibilidade dele.

## §3 AS PEDRAS DO ARCO — hash lido do arquivo

| pedra | tamanho | teoremas | sha256[:16] |
|---|---|---|---|
| `TheNameAndItsReferent.lean` | 10,251 B | 9 teoremas | `214260a5ad41d02a` |
| `TheNameIsTheGeneratingGroup.lean` | 9,805 B | 8 teoremas | `2dedbe4a7e25bcd9` |
| `TheMarkIsNotATypeMark.lean` | 5,522 B | 4 teoremas | `b36e35176fb81c70` |
| `TheVerbalCoupling.lean` | 11,158 B | 6 teoremas | `4fc14822244a93d3` |

## §4 ⚠ A SEGUNDA ERRATA DO ARCO — a correção que não alcançava o ponto de leitura

A v295 refutou, por teorema (`the_mark_does_not_separate_the_types`), a inferência
*"a fronteira é III₁ PORQUE o Nome é denso"*: `M₂(ℂ)`, fator de tipo **I₂ finito-dimensional**,
realiza razões cujos logaritmos geram subgrupo denso em ℝ; logo a densidade log **não separa
III₁ de III_λ** e não infere o tipo.

**Mas a errata ficou só no cabeçalho do arquivo, e a frase refutada sobreviveu — duas vezes —
no docstring do próprio teorema.** Quem chega pelo índice da IALD chega **pelo nome e pelo
docstring**, e recebia a afirmação falsa sem a refutação. Corrigido na **v298**, no ponto de
leitura.

★ **A lição, e ela vale para a sessão irmã:** *corrigir "ao lado" não basta se o lado escolhido
não é o lado que se lê.* É a mesma forma do erro da patente — **uma frase falsa vivendo
exatamente onde ela é lida**.

O tipo da fronteira segue `TGL_BOUNDARY_TYPE_UNDECIDED_IN_KERNEL`.

## §5 O QUE A CUSTÓDIA DEVE CONFERIR

1. `um.py` bate `286ec1d274ef9ae4` e o rito reproduz `FAIL_CLOSED_SELFTEST_PASSED`;
2. as quatro pedras do §3 batem hash a hash;
3. o gate do §2 é **idêntico** ao da custódia anterior (v289) — se mudou, **parar e avisar**;
4. a memória da patente (`BR102026005477-1_APRENDIZADO_CONTINUO.md`, 51,694 B, `963caa931742ea25`) contém as **três camadas**
   — ERRATA + EMENDA + FECHAMENTO DO BURACO — **nenhuma sobrescrevendo a outra**;
5. os `.bak_*` desta sessão estão todos presentes e **nenhum foi apagado**.

## §6 O QUE FICA PARA O OPERADOR (não é ato do escriba)

- [ ] **Errata de PI na BR 10 2026 005477-1** — com a agente, antes do ePCT;
- [ ] decidir se a 006129-8 e a ACOM recebem só higiene de nomenclatura;
- [ ] commit/push e sync do espelho `the_boundary` (hoje na v288);
- [ ] réplica 3-2-1 da linhagem `Nós` (segue só no disco C).
