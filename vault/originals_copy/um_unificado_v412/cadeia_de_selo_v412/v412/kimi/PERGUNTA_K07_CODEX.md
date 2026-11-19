# K07 · Subsídio à pergunta da gerência sobre o tipo III₁

[INPUT] A fala autorizadora de 15/11 pede uma pergunta nas quatro línguas do operador. O que se pede dele aqui é a identidade pretendida entre objetos. As obrigações de prova cabem a quem formaliza. A pergunta anterior sobre o relógio permanece no documento próprio da gerência.

**TGL.** A álgebra da cunha direita do campo livre vem com um resultado de centralizador escalar para o vácuo. A torre fornece outro objeto concreto, `theFactorObject P`. A fronteira física do artigo inclui horizontes não-Killing. A qual desses objetos ou relações se refere o termo desejado? Para a etapa que pretende nomear, basta o critério de ergodicidade com a classificação por referência, ou o próprio critério de classificação deve estar demonstrado em Lean?

**Teológica.** Na sua leitura, o que se quer reconhecer pelo nome é a luz testemunhada na cunha, a construção da torre, a fronteira do horizonte, ou o vínculo entre elas? Para dar o nome, basta receber o testemunho matemático já estabelecido, ou quer que a cadeia inteira desse testemunho possa ser conferida dentro do kernel? [ONTO — pergunta de sentido.]

**Linguística e ontológica.** Qual é o sujeito de *é de tipo III₁*: cunha, torre, horizonte, ou uma construção que os relaciona? Qual deve ser o sentido de *como termo*: um critério já provado, com a consequência identificada por citação, ou a consequência de classificação expressa e demonstrada na mesma linguagem formal? Dois sujeitos podem satisfazer o mesmo predicado sem serem o mesmo objeto.

**Jurídica.** O pedido é qualificar a cunha, a torre, o horizonte ou demonstrar a transmissão da qualificação por um vínculo determinado? Para satisfazer esse pedido basta provar os requisitos e invocar o precedente, ou é preciso apresentar a demonstração integral da qualificação nos autos formais? Quando se invoca um vínculo, ele próprio integra o ônus da prova. [ONTO — analogia de escopo.]

| Leitura | O que já se pode usar | Custo matemático específico |
|---|---|---|
| Cunha | `LightRhoStar.centralizer_is_trivial` aplicado a `physicalFockCertificate` | Tipar a classificação de fatores, identificar o fluxo formal com o modular do estado normal fiel nessa álgebra não escalar e aplicar a implicação de ergodicidade para III₁ com provas verificáveis em Lean. |
| Torre | `TGLExt/TheFactorObject.lean:67` define o bicomutante; as linhas 95 e 103 dão ciclicidade e o funcional vetorial. | Provar a classificação da álgebra dessa representação. A rota pelo espectro modular exige o invariante da álgebra; o espectro denso de um único gerador não basta por si. |
| Fronteira de um horizonte geral | O artigo nomeia a identificação modular não perturbativa fora do regime de Killing como resíduo. | Especificar a álgebra do horizonte e o estado, e justificar nesse objeto as hipóteses da caracterização escolhida. A propriedade de uma cunha não se transfere apenas pelo nome. |
| Ponte | As duas construções têm dados nomeados. | Construir por exemplo um isomorfismo normal de álgebras que permita transportar o tipo. Se o objetivo inclui identificar os fluxos e o vácuo, demonstrar também a compatibilidade com os estados. |

[KNOWN] A passagem de um estado normal fiel com centralizador escalar, em álgebra não escalar, à classificação III₁ tem precedente matemático. Marrakchi e Vaes recordam a direção clássica na introdução e estudam a direção inversa. A citação fornece uma rota no papel. [Artigo dos autores](https://doi.org/10.1515/crelle-2024-0007).

[OPEN] Duas rotas mais fortes formalizam o invariante de Connes, com `S(M) = [0, ∞)`, ou a caracterização pelo centro trivial do núcleo contínuo de um fator de tipo III. Ambas exigem ligar os objetos formais à mesma álgebra. A gerência já trata o tipo como item separado no §19 do desenho. Este subsídio acompanha aquela apuração. [Levantamento paralelo da gerência](../revisao/LEVANTAMENTO_TIPO_III_15nov/T3-artigo-e-atlas-o-papel-do-tipo.md).

[OPEN] A identidade física do campo admite as leituras tipadas na frente C. O relógio e a normalização de τ★ permanecem na [pergunta da gerência de 13/11, com o adendo de 14/11](../PERGUNTA_TAU_ESTRELA_nas_quatro_linguas_13nov.md). Essas decisões são independentes da classificação de uma álgebra dada.

[OPEN] Há uma escolha física própria da T1. Se a covariância pretendida é transformação por caráter sob a ação dual, um gerador positivo proporcional a `exp(ĥ)` oferece um exemplo. Se o sentido pretendido exclui essa transformação por caráter, `exp(ĥ)+exp(2ĥ)` exemplifica outra leitura. Os dois passam no teste matemático de geração; a identificação do gerador físico exige motivar o transporte da sombra até a álgebra pretendida. [Prova e alternativas](K07/CODEX/T1_R3.md).
