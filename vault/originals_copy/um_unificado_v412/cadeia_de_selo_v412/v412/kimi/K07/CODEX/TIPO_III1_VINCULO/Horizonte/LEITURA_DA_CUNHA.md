# O observador, a borda e a álgebra da mesma cunha

**[INPUT/ONTO]** O operador identifica a luz testemunhada na cunha com o Nome, a Torre com o índice, a borda do horizonte com o espectro de leitura e o próprio observador com o vínculo relativístico. A construção usa como sujeito matemático a rede de Maxwell em Minkowski e o estado de vácuo já definidos na casa. Para cada referencial admitido, ela determina simultaneamente a fronteira da região e a transformação de seus operadores físicos. [Fonte humana](../OPERADOR_RESPOSTA_15nov.txt) · [Candidata Lean](WedgeHorizonObserver.lean) · [Registro de compilação](build/WedgeHorizonObserver.log)

## A leitura em dois sentidos

Em coordenadas x=(x⁰,x¹,y,z), ponha u=x¹+x⁰ e v=x¹−x⁰. A cunha direita W é exatamente u>0 e v>0. Sua fronteira topológica é a união de duas folhas fechadas, uma com v=0 e u≥0, a outra com u=0 e v≥0. A primeira contém (r,r,y,z) e a segunda (−r,r,y,z) para cada r≥0. Elas se encontram precisamente no plano (0,0,y,z). A prova calcula o fecho por aproximação a partir de deslocamentos espaciais positivos. A leitura completa (u,v,y,z) é injetiva. Guardar apenas uv faria as duas folhas inteiras devolverem zero. [`closure_rightWedge`, `boundary_two_sheets`, `bifurcation` e `readPoint_injective`](WedgeHorizonObserver.lean)

Um boost de rapidez s age por (u,v,y,z)↦(eˢu,e⁻ˢv,y,z). O observador acelerado com raio ρ>0 e rótulos transversos (y,z) segue a órbita de (0,ρ,y,z). Nela, u/v=e²ˢ e **s=½ ln(u/v)**. A régua ρ cancela no contraste. Esse quociente é usado no interior da cunha, onde u e v são positivos. Nos geradores nulos a leitura por (u,v) continua definida. O parâmetro s é rapidez adimensional. [`boost_read`, `generator_labels` e `observer_recovers_rapidity`](WedgeHorizonObserver.lean)

## O mesmo movimento na álgebra e na fibra espectral

Se g=(L,a), com L no grupo de Lorentz gerado do kernel e a uma translação, a carta ativa é x↦Lx+a. A leitura feita no referencial g aplica a carta inversa. Portanto, o observador que acompanha gx recupera a mesma quádrupla que o referencial inicial lia em x. Pela propriedade do homeomorfismo,

$$\partial(g W)=g H_{\rm futuro}\cup g H_{\rm passado}.$$

O implementador na luz de uma partícula é U(g)=U₁(a)U_helicidade(L). A prova transporta as funções-teste compactas do Maxwell e usa, nessa mesma rede, a segunda quantização de U(g). Para A operador limitado de Fock,

$$A\in\mathcal M(W)\quad\Longleftrightarrow\quad
\Gamma(U(g)) A \Gamma(U(g))^*\in\mathcal M(gW).$$

O teorema `observer_and_wedge_algebra` entrega as duas igualdades com **o mesmo g** e a mesma W. `transported_light_witness` transporta um vetor de luz não nulo realmente localizado na cunha e coloca seu operador de Weyl na álgebra transformada. Nenhuma álgebra auxiliar é identificada por nome. [Construção](WedgeHorizonObserver.lean) · [Rede física de Fock, `net` e `net_covariant`](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/F1Fecho394/PhysicalFockNetRealizationR2.lean:46>)

Os sentidos das translações nulas também importam. Para t≥0, W+t(1,1,0,0)⊆W e W−t(1,−1,0,0)⊆W. Isotonia e covariância põem as duas imagens da álgebra sob as conjugações correspondentes dentro da álgebra de W. A prova fornece inclusões, sem impor igualdade de subálgebras ou invariância por todas as translações. [`inward_null_translations` e `null_translations_fock`](WedgeHorizonObserver.lean)

No fluxo KMS do vácuo da casa, a rapidez geométrica é +2πt. Na convenção do par de Tomita é −2πt. Para este último sinal, os pesos nas coordenadas nulas são exp(−2πt) e exp(+2πt). Em frequência de rapidez ξ, o mesmo boost de uma partícula age, para quase todo ξ, por multiplicação por exp(it·4π²ξ) **sobre toda a fibra** L²(ℝ²;ℂ²). Os rótulos transversos do momento e as duas componentes da polarização permanecem presentes. As coordenadas espaciais y,z parametrizam a borda no espaço-tempo; o argumento transversal da fibra parametriza momento. A convenção de Fourier, o gerador de uma representação de uma partícula e o invariante S de Connes do fator têm definições distintas. O espectro de um só vácuo não classifica por si só um fator em III₁. [`boost_read_and_kms_action` e `modular_read_with_fiber`](WedgeHorizonObserver.lean) · [Definição do grupo espectral](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/LightNetStandardWedgeDataBGL.lean:56>) · [Símbolo canônico](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/F1Fecho394/FubiniL2.lean:291>) · [Sinais do par e do KMS](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/F1Fecho394/PhysicalFockNetRealizationR2.lean:69>)

## O que a fronteira determina em um horizonte geral

[DERIVED] Há um teste exato da pretensão de deduzir a simetria do espaço inteiro conhecendo todo o movimento da borda. Tome o cisalhamento

$$S_s(x^0,x^1,y,z)=(x^0,x^1,y+suv,z).$$

Ele compõe os parâmetros por soma. Fixa individualmente cada ponto das duas folhas, inclusive a bifurcação e cada (y,z), pois uv=0. Contudo, S_s leva o intervalo quadrático do vetor (0,1,0,0) de −1 a −1−s². Para s≠0 a transformação viola a isometria de Minkowski. Compondo o boost real B_s com S_s, obtém-se **a mesma ação de B_s em cada ponto da fronteira**, com intervalo diferente no interior. O controle executa uma refutação restrita: a ação completa sobre a borda é insuficiente para determinar sozinha a extensão isométrica. O argumento não fornece duas isometrias distintas com os mesmos dados. [`shear_add`, `shear_fixes_boundary` e `same_boundary_motion_different_interval`](WedgeHorizonObserver.lean)

[OPEN] Para um horizonte curvo sem Killing global faltam, nessa extensão, uma família especificada de regiões e redes, um estado padrão, o fluxo relevante e a prova de que sua implementação modular induz a ação geométrica nessas regiões. O kernel já tem `GeometricHorizonPencil`, com vetor nulo geodésico, tela e dados de equilíbrio, e `null_balance_produces_pencil` sob hipóteses expressas. Esses teoremas locais entregam um objeto geométrico diferente da ação modular da rede física construída em Minkowski. Da mesma forma, `modularHorizon` da Torre entrega um normalizador unitário do fator da Torre que preserva seu estado. Identificar esse índice com a cunha requer um entrelaçamento que respeite estados, álgebras e o fluxo, com as multiplicidades relevantes preservadas. [Lápis geométrico](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/GeometricAreaHorizon.lean:51>) · [Construção sob balanço nulo](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ConstructedHorizonPencil.lean:60>) · [Horizonte modular da Torre](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/TheModularFlowIsAHorizon.lean:68>) · [Jacobson, horizontes causais locais de Rindler (1995)](https://arxiv.org/abs/gr-qc/9504004)
