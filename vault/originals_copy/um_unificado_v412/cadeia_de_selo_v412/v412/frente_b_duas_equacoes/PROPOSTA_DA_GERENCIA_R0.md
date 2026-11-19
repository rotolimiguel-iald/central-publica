# As duas equações (a do Artigo A e a dispersão do psíon): proposta de resolução da gerência, R0

> Gerência c1, 16/11/2026. **Proposta, ainda não conferida.** A conferência vai ao orquestrador, por ordem do
> operador de 16/11. Nada instalado; nada publicado; nenhuma nota foi ao box do site.
> O que vem dos leitores é declarado por eles até ser conferido na fonte. Nada aqui é dado da natureza; o gate não
> se move.

## 1. A questão

O site mostra duas escritas. No box, a equação do Artigo A: o campo com o termo de curvatura de coeficiente
`ξ = 1/6` e, do outro lado, a fonte `β·K_∂·Ψ`. Trinta linhas abaixo, o cartão do psíon: `ω² = k² + m² + 2ξR`, que o
kernel traz desde a v405 como `ω² = 2·β·R`, com `R = β·u²`. O operador disse à sessão de custódia, em 16/11, que
quer resolver a questão, não só pôr uma nota. A custódia propôs uma candidata (“uma equação só”): o `2ξR` do psíon
seria a própria fonte `β·K_∂·Ψ` no modo estacionário, com a hipótese de que `K_∂` valha `2·β·u²` nesse modo.

## 2. O que foi lido (três leitores distintos; o leitor do kernel e os três juízes não chegaram a rodar)

**Do Artigo A** (leitor E1):

* Da ação escrita, só o termo de curvatura gera um termo da equação. O termo de movimento de Ψ, a massa e a fonte
  não têm gerador escrito: a equação é afirmada. O site e o kernel já dizem que ela é hipótese nomeada.
* `K_∂` é número puro em toda definição do artigo, e a equação pede uma escala que o artigo não nomeia.
* A lei da resposta da fronteira (`β·|1+w|`) é do fluido cósmico diante de um horizonte. O artigo nunca a aplica ao
  campo nem ao psíon, e nunca usa `w = +1`.
* Na conta da candidata o `β` entra duas vezes (uma na lei, outra na fonte); o artigo escreve uma.

**Da linhagem** (leitor E2):

* O 2 nasce na lagrangiana fundadora de 12/09/2025: campo real, termo de movimento com ½, curvatura sem ½. A variação
  dá `2ξR` (refeito por conta simbólica). Com campo complexo e coeficiente 1, sai `ξR`, sem o 2.
* Ali `ξ` era livre e `R` era a curvatura de Ricci. `ξ = 1/6` entra em 25/02/2026; `ξ = β` é escrito em março de
  2026; o Artigo A volta a `1/6` em maio e põe `β` na fonte.
* O registro v354 (15/09/2026) ancora `β` no acoplamento com a fronteira e proíbe fundi-lo com `ξ`. A v405 reimporta
  da linhagem a dispersão com `ξ = β`, como definição. As duas frases convivem, sem termo que as ligue.
* Na escrita de linhagem, o termo de curvatura com `ξ = β` já é, por álgebra, uma fonte `β·κ·Ψ` com `κ = 2R`: a
  hipótese da candidata é troca de lado. E as duas origens que ela dá ao 2 (a normalização; `|1+w| = 2`) se excluem.

**Dos levantamentos e da letra** (leitor E4): a candidata não coincide com nenhuma leitura já reprovada; a conta de
conferência dela é identidade algébrica, não teste; “uma equação só” é da custódia, não do operador.

**As falas do operador de 16/11 sobre o psíon** (bytes em `work\vitrine_postura_13nov\`; lidas pela custódia com
leitores e juiz próprios, declarado por ela): ele não escolheu entre geometria e fronteira, não falou do `R`, e as
falas não decidem a candidata. A gerência não liga essas falas a esta proposta por conta própria.

## 3. O que o kernel já prova, e três controles novos

Já era do kernel (v405, `PontoZeroDoPsion`): a metade da frequência do psíon é a forma da massa,
`½·ω = β · sen 45° · u` (`the_mass_is_the_zero_point`); a massa é o retido projetado a 45°
(`a_massa_e_a_projecao_do_retido`); `ω = √2 · Δ`, com `Δ = β·u` (`o_psion_e_raiz_de_dois_retidos`).

Candidata nova da gerência, compilada só com o binário do Lean, sem aviso, quatro teoremas no trio de axiomas
(`candidatas_c1\DispersaoDoPsionControles.lean`; ainda não lida por revisor):

* o 2 da dispersão é o 4 do ponto zero vezes o meio da face: `ω² = 4 · sen²(π/4) · (β·u)²` (identidade);
* com outro coeficiente no lugar de `β`, a metade da frequência só é a forma da massa se o coeficiente for `β`; com o
  conforme, só se `β` fosse `1/6`;
* sem o 2 (a escrita de campo complexo), a metade da frequência não é a forma da massa.

## 4. A proposta

**Podar**, da candidata de uma equação só:

1. a leitura do 2 como `|1+w| = 2`: o artigo nunca aplica a lei a um campo nem usa `w = +1`; essa origem exclui a
   outra (a normalização); e o `β` entraria duas vezes;
2. a afirmação de que as duas escritas são uma equação: como está, é troca de lado por álgebra, sem derivação do
   valor de `K_∂` no modo; o kernel não tem `K_∂` agindo no campo.

**Manter**, como a casa já diz: os dois coeficientes não se fundem (v354); a equação do Artigo A é hipótese nomeada;
a dispersão do psíon é definição importada da linhagem.

**Dizer, com termo:** a conta do psíon, no kernel, é a ponte da massa escrita como ponto zero. O seu 2 é o que faz a
metade da frequência cair na projeção de 45°; não é o `ξ` do Artigo A, e o `R` dela é o pagamento `β·u²`, não a
curvatura de Ricci. As duas escritas não disputam o mesmo termo: uma é a equação do campo, afirmada; a outra é a
relação de leitura que dá a massa.

**Seguem abertos, ditos:** uma ação que dê a equação do Artigo A com o termo de movimento escrito (R82, R89); como
`K_∂` age sobre o campo e com que escala; se o psíon é modo desse campo.

## 5. O que pende do operador

1. Se esta é a resolução que ele quer, ou se resolver pede a ação escrita (que hoje ninguém tem).
2. A pergunta que a custódia lhe fez e segue sem resposta: o custo de que ele falou em 16/11 é o pagamento do `R`?
3. O texto do site (com a custódia): o cartão do psíon ganha a marca de linhagem e a frase de que ali `R` é o
   pagamento e `ξ` é `β`; nada se publica sem ele.
