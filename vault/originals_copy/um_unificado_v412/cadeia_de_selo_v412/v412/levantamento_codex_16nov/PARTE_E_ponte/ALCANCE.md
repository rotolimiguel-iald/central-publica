# Ponte entre os geradores espinoriais e a representação vetorial

**Resultado.** No referencial da v63, com a ordem `(t,x,y,z)` e a convenção `herm4` da REV21, os seis geradores espinoriais têm exatamente a ação das seis matrizes de `Solder4D`. Não é necessária permutação, inversão de eixo ou troca de sinal. Na tabela, cada linha vale para todo vetor v. [Fonte da ponte](<C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/levantamento_codex_16nov/PARTE_E_ponte/SpinorToSolder.lean>) · [Fonte REV21](<C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/candidatas_c1/REV21/BoostEDissipador.lean:74>) · [Matrizes v63](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/Solder4D.lean:102>)

| A na REV21 | Matriz em Solder4D | Velocidade nas coordenadas (t,x,y,z) |
|---|---|---|
| Kx = σx/2 | K1 | (x,t,0,0) |
| Ky = σy/2 | K2 | (y,0,t,0) |
| Kz = σz/2 | K3 | (z,0,0,t) |
| Jx = −iσx/2 | J1 | (0,0,−z,y) |
| Jy = −iσy/2 | J2 | (0,z,0,−x) |
| Jz = −iσz/2 | J3 | (0,−y,x,0) |

**A forma e sua derivada sob congruência.** Escreva H(v)=tI+xσx+yσy+zσz. O termo `determinant_eq_solder_form` une o determinante da REV21 à forma quadrática `tensorQuad eta4 v` da v63 para todo v, com a sua inclusão real em ℂ. Para F_A(s)=I+sA e s real, a identidade exata é

\[
F_A(s) X F_A(s)^\dagger
=X+s(AX+XA^\dagger)+s^2 A X A^\dagger .
\]

`congruence_derivative` prova com `HasDerivAt` a derivada em s=0, em cada entrada. O caminho reto serve para calcular a diferencial da congruência em I. É possível usar essa diferencial sem supor que I+sA pertença ao grupo especial para todo s. `six_axes` aplica o resultado aos seis A da tabela. `coordinates_embed` recupera as coordenadas pela função já existente do kernel, o que assegura a injetividade de H.

**Colchetes e combinações.** Para matrizes complexas A,B, o termo `tangent_bracket` demonstra que o comutador das ações tangentes em X é a ação tangente de AB−BA em X. Em particular, o sinal do colchete de dois boosts atravessa a ponte. Para seis coeficientes reais c, `spin c` é a combinação dos seis geradores espinoriais na ordem da tabela e `TGLExt.lorentzRep c` é a combinação vetorial existente no kernel. Para todo c e v, `all_generators` prova
\[
(\mathrm{spin}\,c)H(v)+H(v)(\mathrm{spin}\,c)^\dagger
=H((\mathrm{lorentzRep}\,c)v).
\]
Se duas ações coincidem em todos os H(v), `coefficients_unique` prova igualdade dos seis coeficientes usando a fidelidade de `lorentzRep` e a injetividade de H. O domínio de fidelidade é o espaço real destas seis combinações. Uma matriz iλI com λ real, por exemplo, anula a diferencial em todos os X. [Fidelidade da representação v63](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/Solder4D.lean:219>)

**Alcance.** [REAL, candidata local] A construção identifica por termo o ramo de dimensão finita da representação espinorial com a representação vetorial definida na v63. A escolha de Herm₂(ℂ), do determinante, do trio de Pauli e da ação por congruência especifica a realização. A igualdade descreve geradores infinitesimais e permite usar o sinal dos colchetes nas mesmas coordenadas. A origem modular de três direções independentes, sua identificação com os três vínculos da casa, os termos de salto de uma dinâmica de Lindblad, o contínuo curvo e a equação de campo têm obrigações próprias. O termo aqui usa geradores do ramo sem salto e rotações hamiltonianas. A identificação da gerência entre parte sem traço do lock e um boost usa as hipóteses do projetor de posto um da face de dois níveis.

**Inscrição e reprodução.** A fala humana e a candidata foram verificadas nos bytes contra os pinos do adendo. Para reproduzir, execute nesta pasta `C:\Python314\python.exe -B -X utf8 compile.py`. O script recompila uma cópia byte a byte da REV21 e a nova ponte, usando apenas `lean.exe` e as bibliotecas já compiladas em `C:\t\k411c\final`. Compara todas as linhas `#print axioms` com as declarações efetivamente relatadas, recusa avisos/erros e grava os pinos de entradas, logs e objetos. A revisão é ato de outra mão. [Recibo](<C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/levantamento_codex_16nov/PARTE_E_ponte/COMPILACAO.json>) · [Script](<C:/IALD/Central de Patentes/work/cadeia_de_selo/v412/levantamento_codex_16nov/PARTE_E_ponte/compile.py>)

