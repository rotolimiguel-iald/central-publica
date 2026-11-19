# REV21 da Ordem 020, Adendo C

[REAL] A fonte fixa possui 11.689 bytes. A recompilação com lean.exe 4.31.0, sobre os compilados de C:/t/k411c/final e em diretório próprio, verificou os onze enunciados, cada qual com o subconjunto de axiomas registrado pela gerência. Todos usam propext, Classical.choice e Quot.sound. A cópia, o objeto, a captura integral lean.log e os pinos estão em CONFERENCIA.json. A fala humana pinada formula a pergunta sobre Lindblad. A candidata, as estrelas e os comentários são da gerência c1. O registro conserva o caráter provisório do nome.

## Termos

Todas as linhas abaixo são da REV21/BoostEDissipador.lean. ★ denota resposta que a candidata apresenta ao operador. O uso de ★ em resultados conhecidos indica sua função na resposta, sem reivindicação de prioridade. A lista do cabeçalho marca blocos; a coluna abaixo reproduz as estrelas das docstrings individuais.

| Linha | Teorema | Conteúdo e hipóteses |
|---|---|---|
| 78 ★ | a_forma_de_minkowski_e_o_determinante | Identidade escalar para herm4(t,x,y,z), com quatro parâmetros reais e o encaixe Pauli da linha 74. O determinante produz a assinatura (+−−−) nesse encaixe. A identificação espinorial é conhecida. |
| 86 | a_forma_e_preservada_por_determinante_um | Para X complexo arbitrário, det A = 1 implica det(AXA†) = det X. Por multiplicatividade o requisito suficiente mais geral é abs(det A) = 1. |
| 93 ★ | a_anatomia_do_gerador_da_face | Identidade afim em P para toda matriz 2×2. A atribuição de duas partes escalar e sem traço requer tr P = 1. |
| 98 | o_gerador_de_boost_tem_quadrado_um | P²=P implica (2P−I)²=I. O gerador com normalização de semieixo K=(2P−I)/2 satisfaz K²=I/4. |
| 107 | o_gerador_de_boost_tem_traco_zero | tr P = 1 implica tr(2P−I)=0. A leitura «posto um» da docstring requer também idempotência. P=I/2 tem traço um e posto dois. |
| 127 | a_rotacao_e_menos_i_vezes_o_boost | Conjunção de três igualdades por definição, com Jᵢ=−iKᵢ. |
| 131 ★ | os_boosts_fecham_com_o_sinal_de_lorentz | Um colchete explícito, [Kx,Ky]=−Jz, por multiplicação das matrizes de Pauli. |
| 137 ★ | as_rotacoes_fecham_com_o_sinal_oposto | Um colchete explícito, [Jx,Jy]=Jz, vindo de (−i)²=−1. A lista completa de colchetes não integra esses dois enunciados. |
| 148 ★ | o_fluxo_do_lock_e_dilatacao_vezes_boost | Identidade hiperbólica de P+e⁻ˢ(I−P) para P arbitrário e s real. A interpretação exponencial requer P²=P, como no módulo importado TheAxiomAndTheFalseWitness.lean:161. Boost espinorial puro requer ademais P=P† e tr P=1. F é filtro de Kraus de atenuação para s≥0 e P ortogonal. |
| 181 | o_fluxo_do_lock_no_nome_do_eixo_z | Na projeção nomeZ=diag(1,0), F é diagonal com autovalores 1 e e⁻ˢ. |
| 188 | o_fluxo_do_lock_preserva_a_forma_a_menos_da_dilatacao | Para nomeZ, s real e X arbitrário, det(FXF†)=e⁻²ˢ det X. Para X≥0, FXF†≥0 por congruência. F é inversível para s finito. A afirmação de positividade é consequência algébrica, distinta do termo escalar. |

## O gerador sem salto e o cone

[DERIVED] No quadro GKLS de dimensão finita, fixada uma representação dos saltos e suprimida a parte hamiltoniana, G = −½Σ Lⱼ†Lⱼ atua sobre amplitudes. O ramo sem salto sobre densidades tem gerador X ↦ GX+XG†. Só se Σ Lⱼ†Lⱼ = 2g(I−P) se obtém o G = −g(I−P) da escala s=gt. Com P projeção ortogonal de posto um e dimensão dois, sua parte escalar é −gI/2 e a parte sem traço é g(2P−I)/2. Para taxa κ do dissipador D[Q], Q=I−P e L=√κ Q, temos g=κ/2. Normalizar o expoente a s=1 unidade por tempo significa escolher g. É necessária g≥0 para a interpretação contínua de atenuação com tempo positivo. Mais geralmente, em dimensão d a parte escalar de −g(I−P) é −g(1−rank(P)/d)I. A forma de Minkowski é a função quadrática sobre X. G é uma matriz que gera uma ação nessa função; D é um superoperador.

[DERIVED] A operação de um único salto é X ↦ LXL†. Preserva positividade em qualquer dimensão e multiplica o determinante do qubit por abs(det L)². Se L tem posto um, toda saída tem determinante zero, podendo inclusive ser o ápice. Se abs(det L)=1, o determinante é preservado. Para o estado normalizado do salto condicionado, ainda se divide pelo quadrado da probabilidade de sucesso. A soma dos saltos positivos conserva o cone positivo sólido. Uma soma de congruências pode levar a superfície nula ao interior. A preservação de positividade do semigrupo físico exp(tD), t≥0, é distinta da positividade do próprio gerador D aplicado a X.

[DERIVED] Dois saltos dão uma distinção operacional exata. Na base z, escolha Q=|1⟩⟨1|. Os saltos L₁=√κ Q e L₂=√κ |0⟩⟨1| compartilham o mesmo L†L=κQ e o mesmo ramo sem salto F. O primeiro preserva |1⟩⟨1| sob a evolução completa. O segundo transforma esse estado na mistura diag(1−e⁻ᵏᵗ,e⁻ᵏᵗ), onde k=κ, com determinante e⁻ᵏᵗ(1−e⁻ᵏᵗ)>0 para κ,t>0. Logo o gerador sem salto não determina os saltos individuais nem a evolução completa. Um candidato diferente, L=σz unitário, tem L†L=I, sem componente de boost sem traço, embora o canal completo produza descoerência.

[DERIVED] A escolha P²=P, P=P†, tr P=1 é indispensável na interpretação física. P=[[1,1],[0,0]] é idempotente de traço um e o fator hiperbólico resultante não é hermitiano em s≠0. P=I (posto dois) dá F=I e as partes −I/2 e +I/2 cancelam; a segunda tem traço não nulo. A caracterização do gerador «sem salto» é condicional a uma escolha de operadores e taxas. REV21 não dá esse vínculo aos saltos físicos específicos do runtime.

## Fontes primárias

[KNOWN] Han, Kim e Noz derivam a separação da atenuação comum do filtro diferencial na eq. (11), escrevem o atenuador de determinante um na (12) e o defasador na (14). As seções IV–VI dão a representação de Lorentz sobre as quatro componentes de Stokes, com a convenção de eixos dos autores. [Artigo, seções III–VI](https://arxiv.org/html/physics/9707016v1)

[KNOWN] Verstraete, Dehaene e De Moor, teorema 2 e eqs. (4)–(6), tratam filtros locais de dois qubits. Matrizes inversíveis A,B geram transformações próprias e ortócronas à esquerda e à direita sobre a matriz real de correlações; surgem os fatores de módulo do determinante e a normalização do estado. Para um filtro singular a divisão por abs(det A) na expressão do teorema não existe. [Artigo, teorema 2](https://arxiv.org/html/quant-ph/0011111v1)

[REAL] A fiação específica da REV21 é a identificação da expressão axiomFlow da casa com dilatação vezes filtro hiperbólico e sua consequência em nomeZ. O encaixe Pauli de Herm(2), a assinatura da forma determinante e comutadores da álgebra de Lorentz têm antecedentes. Um par específico de vínculos entre cantos já aparece em TGLExt/TheCurrentConnectsTheCorners.lean:134. A classe de TGL/FiniteThreeLocks.lean:58,73 e TGLExt/ThreeLocksCorner.lean:97 descreve três operadores de restrição e a interseção dos núcleos. A escolha dos três operadores zero é admitida e deixa todo o espaço como núcleo comum; três boosts Kᵢ=σᵢ/2 são individualmente invertíveis. Uma identificação de cada restrição com um desses três operadores exigiria hipóteses adicionais e outro termo.
