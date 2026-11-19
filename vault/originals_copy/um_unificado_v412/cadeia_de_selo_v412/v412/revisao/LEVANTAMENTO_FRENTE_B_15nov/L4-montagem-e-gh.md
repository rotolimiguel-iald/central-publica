> Retorno de um leitor do levantamento de 15/11/2026 (gerencia c1; so leitura; modelo Sonnet). E' [DECLARADO pelo leitor] ate' a gerencia conferir cada ponto na fonte. Nao e' fala do operador. Nada aqui esta' instalado, selado ou aberto.

# L4-montagem-e-gh

## RESUMO
LEVANTAMENTO (so leitura). Mapa de Rotas (termo unico): montagem, triplas, Gromov, KO, Kronecker, Dirac, Pauli, shuffle; so a rota formal.k05_t1_montagem_gh_tau_campo_v412 e pertinente (seq 14/11, EXAMINADA_COM_DEFEITO; proximo passo = ORDEM K07).
1. Montagem [DERIVED+KNOWN, a conferir]: 4 circulos T_j=(C^inf(S1),L2(S1),D_j=-i*lam*d/dx_j,J_j=K), lam=beta^(-1/2) -> T4 spin trivial. D=-i*lam*sum Gamma_j d_j, Gamma=(s1xt1,s2xt1,s3xt1,1xt2); chi=-G1G2G3G4; J=(s2x1)K; KO 4 = (J^2,JD,Jchi)=(-1,+,+) (MONTAGEM_R2:63-79). Rotulo T3xS1 = IMPAR x IMPAR, resultado par KO 4 (R2:33). (1,3) = (H) com moldura so para analise de Krein e sinais mod 8 (R2:139); L1-L10 listados.
2. Conferencia: D, J, chi, KO 4, rotulo, escala d_lam=sqrt(beta)*d, c_lam=lam^-4*c, vdD/BBB e o estatuto (H) conferem. ERRADO: constante do ciclo -1/18 (R2:87); certa -1/24 (D-D (36) conta nu_n=(n-1)n/2 termos, mas o shuffle tem C(n1+n2,n1): 4 em (3,1), nao 6; r=2i,3,4i). Refiz: soma S4 = 24*G1G2G3G4 = -24*chi; -1/18 da (4/3)chi, -1/24 da chi [REAL, meu script L4]. Seis itens do par.5: constante; L0 (tipo III1/traco) + elo Euclides-Lorentz + Connes 2008 em L10; onde se sustentam finitude/Poincare em T4; Lemas 1-2 independem do tipo e H_Tak reduz-se a hipotese C1 em pi(M); 'deve'->'pode' usar torcao; linha de Blackadar na errata R3.
3. GH em III1 segue [CONJECTURE] (GH_III1_R2:48): 'Com uma tripla torcida III1 para a qual L_sigma e Lip-norma, e com truncamentos que preservam todas as condicoes da metrica escolhida, afirma-se GH-R e/ou GH-S; GH-S_n nao; III1-idade e P_M->1 nao bastam.' Artigo: tex:1824-1826 e 2252-2254 ('provada na sombra; conjecturada via Rieffel'). Citacoes: Rieffel math/0011063 (Prop 4.7: qGH<=GH, Ap.1 contraexemplo; 'qGH=GH' FALSO, tex:1938); vSuijlekom 2005.08544 (Teo 5); Kaad-Kyed 2212.10874 (Obs 3.7) e 2205.06043v1 (Prop 2.14); Hekkelman 2111.13865; Leimbach-vS 2302.07877; Connes-Moscovici math/0609703; Haagerup-Musat 0706.3463 (Lema 2.11, nao existe esperanca condicional normal); Blackadar Cor III.2.1.10 NAO conferido.
4. Veio pela metade: nenhum truncamento concreto em M-chapeu (K05 C3); a ordem K07 3b repete o pedido (e_i=1_[-i,i](h-chapeu); dizer qual e o operador da tripla e a Lip-norma). Glob na pasta kimi: sem MONTAGEM_3MAIS1_R3, GH_III1_R3 nem ENTREGA_K07 [REAL].
KERNEL (TGLExt): SpectralTriple/KODim/koDim/KO_dim/Clifford/RealStructure/productTriple/Dixmier/Krein/Toeplitz/Hochschild/CliffordAlgebra = 0 -> tripla, produto, J de Connes, graduacao, KO: AUSENTE. Existem e ligados: Kronecker (ratioWitness_kron, PowersLadder:250; ~40 modulos) e Pauli 2x2 (SitePauliObservables:32-184). 'chirality' (TheTwoFolds:138) e homonimo; J do kernel e o de Tomita, nao o de Connes.
VEREDITO: so a algebra finita das gamas/J tem musculatura; o resto e gordura sem consumidor.

## ACHADOS

### A1. 1
classe: EXISTE E LIGADO (maquinaria) / AUSENTE (tripla)
onde: MONTAGEM_3MAIS1_R2.md:51-93
Entrada [DERIVED+KNOWN, a conferir]: T_j=(C^inf(S^1),L^2(S^1),D_j=-i*lam*d/dx_j,J_j=K), lam=beta_TGL^(-1/2) (l.51-53). Produto impar x impar: H=(H1xH2)xC^2, D=D1x1xs1+1xD2xs2, chi=1x1xs3; par x impar: D=D_par x1+chi_par x D_impar (l.59-60). Resultado: D_lam^prod=-i*lam[s1^a x t1 d1 + s2^a x t1 d2 + s3^a x t1 d3 + 1^a x t2 d4], chi=1^a x t3, J=(s2^a x 1_t)K (l.65-69); Gamma_1..4 = s1xt1, s2xt1, s3xt1, 1xt2, chi=-G1G2G3G4, J^2=-1, JD=DJ, Jchi=chi J = KO 4 (l.75-79). Rotulo corrigido: T3xS1 e IMPAR x IMPAR com duplicacao C^2, resultado par, dim. metrica 4, KO 4 (l.33). Orientacao: c_(4,lam)=-(1/18) x_j c^j_(1,lam), pi(c)=chi (l.87-91) [constante errada, ver 2]. Escala: d_lam=beta^(1/2) d_1; c_lam=lam^-4 c=beta^2 c; hermitiana (xi,eta)_lam=lam^4 (xi,eta)_1 (l.113-123). (1,3): (H) COM MOLDURA PUBLICADA para definicao de Krein (van den Dungen Def. 2.2) e sinais mod 8 (BBB Tab. 3); L1-L10 (l.145-160). Consulta ao kernel: ver 'examinado' e resumo (zero ocorrencias de tripla/KO/Clifford/J de Connes).

### A2. 2
classe: conferido por revisor distinto + refeito por mim
onde: REVISAO_K05_MONTAGEM_GH.md:28-72,134-141; script L4
CERTO [REAL]: gamas (quadrado 1, anticomutam), D prod, chi, J, sinais KO 4, rotulo impar x impar, escala lam, (H) de (1,3), citacoes vdD (Def 2.2, Prop 4.3, Obs 6.4) e BBB (Tab 3, so caso par). ERRADO: a constante. Refeito por mim (L4_identidades.py): soma_{tau em S4} sgn(tau) G_tau1..G_tau4 = 24*G1G2G3G4 = -24*chi; (-1/18)*soma = (4/3)*chi; (-1/24)*soma = chi. Causa: D-D (36) usa nu_n=(n-1)n/2 termos, mas o shuffle tem C(n1+n2,n1): (1,1)->2 vs nu_2=1; (2,1)->3=3; (3,1)->4 vs nu_4=6; (2,2)->6=6; r correto 2i,3,4i (produto -24), D-D literal i*3*6i=-18. Seis itens do par.5: (1) -1/18 -> -1/24 e reescrever a origem da constante (tambem ENTREGA_K05 l.5); (2) lista L1-L10: faltam item L0 do TIPO (traco/III1/II-inf/torcao; artigo tex:642-650, 2224-2227), o elo Euclides->Lorentz (tex:1803-1816) e Connes 2008 (arXiv:0810.2088: so os cinco primeiros axiomas, algebra comutativa) em L10, reordenando 'bloqueios centrais'; (3) par.4: nomear o que sustenta finitude/Poincare em T4 (Connes 1996 afirma na Obs.4; GVF so por sumario; conferido por Kunneth + forma de cunha, det +1); (4) Lemas 1 e 2 de GH independem do tipo, H_Tak reduz-se a hipotese C1 em pi(M); renomear 'degrau II-inf'; (5) 'deve usar' tripla torcida -> 'pode usar' (Connes-Moscovici); (6) errata R3 omite a linha nova de Blackadar na par.10. Nao conferidos pelo revisor: Blackadar Cor III.2.1.10, Takesaki 1973, Connes-Takesaki 1977, GVF, literatura lorentziana (Strohmaier, Paschke-Sitarz, Franco-Eckstein, Moretti); nao procurou errata publicada de D-D.

### A3. 3
classe: [CONJECTURE] / MEDIDA (o sabido entra por citacao)
onde: GH_III1_R2.md:43-48,54-62,80,166; tex:1824-1826,2252-2254
Enunciado vigente [CONJECTURE - versao tipada] (GH_III1_R2:48): 'Com uma tripla torcida III1 para a qual L_sigma e Lip-norma, e com truncamentos que preservam todas as condicoes exigidas pela metrica escolhida, afirma-se GH-R e/ou GH-S. Nao se afirma GH-S_n sem hipotese adicional. A III1-idade e P_M->1 nao bastam.' GH-R: dist_Q((E_M,L_M),(A,L_sigma))->0; GH-S: d_GH((S(E_M),d_M),(S(A),d_sigma))->0 (l.43-44), com d_sigma(a)=D a - sigma(a) D (l.31-35). Artigo: '(iii) a extensao da convergencia GH a III1 (provada na sombra; conjecturada no continuo via Rieffel)'. Correcao de fundo [KNOWN]: 'qGH=GH no caso comutativo' (tex:1938) e FALSO; Rieffel Prop 4.7 so da qGH<=GH, Ap.1 (Hanfeng Li): dist_GH=1, dist_q=1/2. Para S1 os truncamentos de Toeplitz convergem em GH-S (vS Prop 13) e GH-R (Kaad-Kyed Obs 3.7 + Prop 2.14 de 2205.06043v1, C=C'=1 -> max{gamma,gamma'}); nao e teorema de III1. Fica aberto [OPEN]: torcao sigma fixada, Lip-norma com topologia = fraca-*, mapas S_M C1-contrativos com gamma_M,gamma'_M->0, compacidade de S_n(M-chapeu), H_Tak; Sakai-Tomiyama/Haagerup-Musat Lema 2.11: nao existe esperanca condicional normal de M-chapeu (II-inf) sobre pi(M) (III1), mas extensoes normais individuais existem (Blackadar, nao conferido); sem contraexemplo construido. Lemas II-inf-1 e 2 independem do tipo (revisor B8). Candidata antiga K02/candidatas/GH_III1.lean e tipagem oca, arquivada (sha256 lido por script pelo Kimi: 8b56968a...).

### A4. 4
classe: AUSENTE (entrega) / MEDIDA
onde: ORDEM_K07 par.3b; REVISAO par.4 linha C3; GH_III1_R2:109,150
A ordem K05 (C3) pediu 'a convergencia dos truncamentos da casa no nucleo'; veio: tres lemas condicionais com a quebra dita, sem nenhuma tripla (E,H,D) concreta em M-chapeu e sem ligar a cascata P_M D P_M da casa (tex:1935-1941, licao do aliasing 1944-1950) a M-chapeu; o conteudo e independente do tipo e a metade condicional do Lema 3 e tautologica. A ordem K07 3b repete: tratar os cantos e_i=1_{[-i,i]}(h-chapeu) (os do Lema B da T1), dizer hipotese por hipotese do Lema 2 o que vale, o que falha, o que falta definir (em especial qual e o operador da tripla em M-chapeu e a sua Lip-norma), e dizer se nada concreto fecha. Estado em 15/11: nao ha MONTAGEM_3MAIS1_R3, GH_III1_R3 nem ENTREGA_K07 na pasta kimi (Glob); so ORDEM_K07 e o ADENDO. Do lado da montagem veio pela metade (revisor A6): L1-L10 sem L0/elo Euclides-Lorentz. Nao tentei o truncamento concreto: so levantamento.

### A5. kernel
classe: AUSENTE (tripla/J/KO) | EXISTE E LIGADO (Kronecker, Pauli) | homonimo (chirality, J)
onde: TGLExt: PowersLadder.lean:250; SitePauliObservables.lean:32-190; ModularCurrent.lean:77; TheTwoFolds.lean:138; Solder4D.lean:115,198
Grep so por nomes em TGLExt. SpectralTriple, KODim, koDim, KO_dim, Clifford, RealStructure, productTriple, Dixmier, Krein, Toeplitz, Hochschild, CliffordAlgebra, anticommutator, JordanWigner: 0 ocorrencias [REAL]. Kronecker: ~40 modulos com open scoped Kronecker; `theorem ratioWitness_kron {n m : Type} [Fintype n] [Fintype m] {rho1 a1 b1 : Matrix n n C} {rho2 a2 b2 : Matrix m m C} {r1 r2 : R} (h1 : RatioWitness rho1 a1 b1 r1) (h2 : RatioWitness rho2 a2 b2 r2) : RatioWitness (rho1 (x)k rho2) (a1 (x)k a2) (b1 (x)k b2) (r1 * r2)` (PowersLadder.lean:250-253): composicao por Kronecker existe e esta ligada, mas e a escada de razoes, nao produto de triplas. Pauli 2x2: `def pauliXMatrix : Matrix (Fin 2) (Fin 2) C := !![0, 1; 1, 0]` (SitePauliObservables:32; Y l.34; Z l.36); pauli_x_square, pauli_y_square, pauli_z_square (163-176), pauli_xy (178), pauli_yx (184), conjTranspose x,y,z (148-161): EXISTEM; faltam os anticomutadores {sx,sz} e {sy,sz} isolados (grep ^theorem pauli_ para na l.190). `theorem current_anticommutes : contrast * modularCurrent + modularCurrent * contrast = 0` (ModularCurrent.lean:77) e outro par (2x2, Bell), nao as gamas. HOMONIMOS a nao encadear: `the_folds_have_opposite_chirality` (TheTwoFolds:138) e o sinal -2/+2 das dobras, nao a graduacao chi; o J do kernel/da teoria e o de Tomita (J=Luz), nao o J de Connes C*K; so(1,3) em Solder4D (generators_in_so13 l.115; lorentzRep l.198) e a representacao vetorial 4x4 real, nao espinorial. Revisor (REVISAO:17): 0 em kernel_bancada para Krein/SpectralTriple/Gromov/Sakai e 0 no inventario da bancada; Tomiyama so o finito (CondExpect.lean, EsperancaCondicional.lean).

## PROPOSTAS

### P1. P1. clifford_sq: a identidade D(k)^2 = |k|^2 das quatro gamas (e, como caso particular, o quadrado do produto impar x impar)
enunciado: -- abstrato, em qualquer anel
theorem clifford_sq {R : Type*} [Ring R] {ι : Type*} [Fintype ι] [DecidableEq ι]
    (Γ k : ι → R) (hΓ : ∀ i, Γ i * Γ i = 1)
    (hanti : ∀ i j, i ≠ j → Γ i * Γ j + Γ j * Γ i = 0)
    (hkΓ : ∀ i j, Commute (k i) (Γ j)) (hkk : ∀ i j, Commute (k i) (k j)) :
    (∑ i, k i * Γ i) * (∑ i, k i * Γ i) = ∑ i, k i * k i
-- instancia concreta (reusa pauliXMatrix/Y/Z e ⊗ₖ do kernel)
def gam : Fin 4 → Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ
  | 0 => pauliXMatrix ⊗ₖ pauliXMatrix | 1 => pauliYMatrix ⊗ₖ pauliXMatrix
  | 2 => pauliZMatrix ⊗ₖ pauliXMatrix | 3 => (1 : Matrix (Fin 2) (Fin 2) ℂ) ⊗ₖ pauliYMatrix
theorem gam_sq (j) : gam j * gam j = 1
theorem gam_anti (i j) (h : i ≠ j) : gam i * gam j + gam j * gam i = 0
theorem gam_selfadjoint (j) : (gam j)ᴴ = gam j
apoio: [REAL, meu script L4] 200 sorteios de k real: erro maximo 1,8e-15; espectro de D(k) = +-|k| (multiplicidade 2); gamas de quadrado 1, autoadjuntas, anticomutantes. Reusa o que existe no kernel: pauli_x_square, pauli_y_square, pauli_z_square, pauli_xy, pauli_yx (SitePauliObservables:163-184) e a maquinaria Kronecker (PowersLadder:250). Faltam so {sx,sz} e {sy,sz}. COMPRA: o motor algebrico da lei de Weyl da Montagem (R2:101, autovalores de D_lam^2 = lam^2|k|^2) e do 'D^2 soma' dos dois produtos de D-D; a hipotese exata de CliffordAlgebra.lift (cada f m * f m = algebraMap (Q m)) [KNOWN, a conferir] -> representacao de Cl(4,0) em C^4 como homomorfismo, por teorema e nao por script; e e o primeiro termo de kernel que a montagem teria.
nao compra: Nao e operador de Dirac em L2(T4), nem autoadjuntividade/dominio, nem lei de Weyl (so o fator algebrico dela), nem axioma de Connes algum, nada de III1 nem de (1,3). Sem tipo 'tripla espectral' no kernel (AUSENTE) fica algebra finita solta; nao pode ser chamada 'montagem formalizada'.
risco: BAIXO a MEDIO. Prova da versao abstrata: expandir a soma dupla, separar diagonal e fora da diagonal, anular pares i/j trocando indices (Finset.sum_comm); a concreta e 16 entradas por fin_cases, no estilo de ModularCurrent:77. Musculatura: media, a melhor da lista. Gordura se ficar sem consumidor.

### P2. P2. sq_par_impar: o quadrado de D1 x 1 + chi x D2 (regra 'o laplaciano soma')
enunciado: theorem sq_par_impar {R : Type*} [Ring R] (x y z : R)
    (hyy : y * y = 1) (hxy : x * y + y * x = 0)
    (hxz : Commute x z) (hyz : Commute y z) :
    (x + y * z) * (x + y * z) = x * x + z * z
-- leitura: x = D1x1, y = chi1x1, z = 1xD2  (D1 impar em relacao a chi1: chi1 D1 = -D1 chi1)
apoio: [REAL, L4] par_x_impar_sq True (D1 4x4 anticomutando com chi1=diag(1,1,-1,-1), D2 hermitiana 3x3 aleatoria). Prova: (x+yz)^2 = xx + (xy+yx)z + yy zz, usando z comuta com x e y. COMPRA: a unica identidade que a formula de produto par x impar de D-D (Montagem R2:60) precisa para somar os quadrados.
nao compra: Nao compra autoadjuntividade, dominios, J, chi do produto, nem orientacao.
risco: GORDURA, com franqueza: tres linhas de algebra de anel, sem uso no kernel enquanto nao houver tripla. Seu caso impar x impar ja e coberto por P1 (k1=D1x1x1, k2=1xD2x1, G_i=1x1xsigma_i; L4 impar_x_impar_sq True). Nao subir isolada.

### P3. P3. A constante do ciclo de orientacao: soma sobre S4 = 24 G1G2G3G4 = -24 chi
enunciado: theorem sum_perm_sgn_anticomm {R : Type*} [Ring R] (Γ : Fin 4 → R)
    (h : ∀ i j, i ≠ j → Γ i * Γ j = - (Γ j * Γ i)) :
    ∑ τ : Equiv.Perm (Fin 4), (Equiv.Perm.sign τ : ℤ) • (Γ (τ 0) * Γ (τ 1) * Γ (τ 2) * Γ (τ 3))
      = (24 : ℤ) • (Γ 0 * Γ 1 * Γ 2 * Γ 3)
-- corolario concreto com chi := -(gam 0 * gam 1 * gam 2 * gam 3):
theorem orientation_sum : ∑ τ ... = (-24 : ℤ) • chi   -- logo o ciclo normalizado e -(1/24) x_j c^j, nao -(1/18)
apoio: [REAL, L4] soma_S4_igual_24_G1G2G3G4 True; soma_S4_igual_menos_24_chi True; (-1/18)*soma = (4/3)chi True; (-1/24)*soma = chi True; shuffles (1,1),(2,1),(3,1),(2,2) = 2,3,4,6 contra nu_n = 1,3,6 de D-D (36). COMPRA: crava a constante -1/24 por termo, no ponto exato em que a conta publicada falhou.
nao compra: Nao constroi o ciclo de Hochschild c, nem o emparelhamento pi_D(c) = J(a0)[D,a1]...[D,a4] (exige a acao de C^inf(T4) e os comutadores, nada disso esta no kernel), nem prova o axioma de orientacao de Connes: so a aritmetica anticomutativa.
risco: MEIA GORDURA. Prova geral por Equiv.Perm.swap_induction_on e trabalhosa em anel nao comutativo; a unica versao barata e a de n=4 sobre as matrizes explicitas (24 termos), fechada por calculo. Sem Hochschild fica uma verificacao de 24 termos; valor real e documental (impedir o retorno de -1/18). Recomendo so o corolario concreto, nunca como 'pedra de orientacao'.

### P4. P4. Estrutura real no nivel das gamas: C conj(G_j) C^-1 = -G_j; C conj(C) = -1; C conj(chi) C^-1 = chi (os sinais KO 4)
enunciado: def Cmat : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ := pauliYMatrix ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)
theorem C_conj_C : Cmat * Cmat.map star = -1                    -- J^2 = -1  (eps = -1)
theorem C_flips_gam (j : Fin 4) : Cmat * (gam j).map star * Cmat = - gam j
theorem C_fixes_chi : Cmat * chi.map star * Cmat = chi         -- J chi = chi J (eps'' = +1)
theorem C_conj_Dmode (k : Fin 4 → ℝ) :
    Cmat * (∑ j, (k j : ℂ) • gam j).map star * Cmat = ∑ j, ((-k j : ℝ) : ℂ) • gam j   -- J D(k) J^-1 = D(-k): eps' = +1
-- (aqui C = C^-1 porque Cmat * Cmat = 1; J = C ∘ conjugacao)
apoio: [REAL, L4] C_Cbar_igual_menos_1, C_conjG_Cinv_igual_menos_G, C_conjchi_Cinv_igual_chi, C_conj(D(k))_Cinv_igual_D(-k): todas True; concorda com o script do revisor (blocos b_sinais_J_doc: (-1,+1,+1)) e com Montagem R2:69,79. COMPRA: a unica parte realmente decidivel da 'identificacao' que e finito-dimensional: o rotulo KO 4 vira teorema sobre as gamas (4 matrizes 4x4 sobre C), no estilo ja usado em ModularCurrent (fin_cases + simp).
nao compra: Nao e J antilinear em L2(T4) (a reflexao de Fourier k -> -k e analise), nem a condicao de primeira ordem (precisa da acao das funcoes), nem os sinais de (1,3): na assinatura lorentziana a tabela muda (BBB mod 8) e ha simetria fundamental de Krein distinta de J; KO 4 euclidiano nao vira (1,3) (Montagem R2:141).
risco: BAIXO. Mesmo ferramental de P1; depende de P1 (gam) e de gam_anti. Musculatura: media. Etiqueta honesta: 'sinais KO 4 das gamas', nunca 'a tripla real do toro'.

### P5. P5. Contabilidade de sinais do produto de J (par x impar, J = J1 x J2): so serve se e1' = e1''*e2'
enunciado: theorem J_prod_comm {R : Type*} [Ring R] (J1 J2 D1 D2 χ1 : R) (e1' e1'' e2' : ℤ)
    (hJD1 : J1 * D1 = (e1' : R) * (D1 * J1)) (hJχ1 : J1 * χ1 = (e1'' : R) * (χ1 * J1))
    (hJD2 : J2 * D2 = (e2' : R) * (D2 * J2))
    (hc : Commute J1 J2) (c2 : ...  -- J1,χ1,D1 comutam com J2,D2)
    (hs : e1' = e1'' * e2') :
    (J1 * J2) * (D1 + χ1 * D2) = (e1' : R) * ((D1 + χ1 * D2) * (J1 * J2))
-- e uma tabela por decide: pares (n1 par, n2 impar) com eps'(n1) = eps''(n1) * eps'(n2)  <=>  (n1+n2) mod 8 in {3,7}
apoio: [REAL, L4] com a tabela de Connes (eps' = +,-,+,+,+,-,+,+; eps'' = +,-,+,- para n par) [KNOWN, a conferir: o revisor leu so n=2,3,4; o resto da tabela e de memoria da literatura], as unicas somas em que J=J1xJ2 funciona sao n1+n2 = 3 ou 7 (mod 8): (0,3),(0,7),(2,1),(2,5),(4,3),(4,7),(6,1),(6,5). O passo T2xS1 (KO 2 + KO 1 = 3) esta entre os que funcionam; nos demais (inclusive o ultimo, impar x impar com dupla C^2, KO 4) D-D tem de trocar J. COMPRA: mostra que 'os sinais somam' NAO e regra uniforme e que a escolha M_+ da Tabela 6 de D-D e o que carrega a montagem; e a unica ponte algebrica com a moldura 'sinais mod 8' de BBB que e o que (1,3) tem de publicado.
nao compra: Nao prova a tabela de Connes, nem a de BBB, nem os sinais de (1,3) (o caso impar de BBB e declarado dificil); nao constroi J nem D.
risco: GORDURA agora: bookkeeping de sinais sem consumidor, com uma tabela que nao conferi na fonte. So vale quando alguem tipar o caso de Krein (que e [OPEN]). Nao subir.

### P6. P6. Escala D -> lam*D: [lam D, a] = lam [D, a]; c_lam = lam^-4 c
enunciado: theorem comm_smul {R : Type*} [Ring R] [Algebra ℝ R] (lam : ℝ) (D a : R) :
    (lam • D) * a - a * (lam • D) = lam • (D * a - a * D)
-- a distancia d_lam = lam^-1 d exige a definicao da distancia de Connes (sup), que nao esta no kernel
apoio: [DERIVED] Mathlib: smul_mul_assoc, mul_smul_comm, smul_sub. A conta de escala da Montagem R2:113-123 foi refeita pelo revisor (bloco f_escala) e confere.
nao compra: Nao compra d_lam = beta^(1/2) d_1 (sem distancia de Connes), nem Dixmier lam^-4 = beta^2 (sem traco de Dixmier), nem Poincare.
risco: GORDURA PURA: uma linha de Mathlib, sem consumidor; nao propor. Registrar so por completude do pedido.

### P7. VEREDITO sobre o conjunto
enunciado: Das seis, so P1 (com sua instancia gam) e P4 tem musculatura: tipam o que o artigo e a Montagem de fato usam (autovalores de D^2 e os sinais KO 4 das gamas) e reusam Pauli e Kronecker que o kernel ja tem. P3 so como corolario concreto (n=4). P2, P5, P6 sao gordura enquanto nao houver o tipo 'tripla espectral' (AUSENTE); a propria Montagem R2:9 e o GH R2:11 dizem 'nenhuma candidata Lean nova e necessaria'. GH em III1 nao tem enunciado Lean que nao seja tipagem oca (a antiga GH_III1.lean foi arquivada como tal): nenhuma proposta para ele.
apoio: Regra da casa 'um.py sem gordura' (19/10): so entra o que traz musculatura. [REAL] 0 ocorrencias de tripla/KO/Clifford no kernel; [REAL] L4 numerico.
nao compra: Nem P1+P4 juntas dao 'montagem 3+1 formalizada': dao a algebra finita das gamas e dos sinais KO 4; a identificacao com o Dirac do toro, a finitude, Poincare e tudo de (1,3) seguem [KNOWN, a conferir]/[OPEN]. Nenhum gate, nenhum selo e nenhuma promocao de [CONJECTURE]. Instalacao e decisao do operador (partitura: P1+P4 sao inertes ao gate; um negativo aqui seria falha de prova, nao parede fisica).
risco: Escolha de desenho a dizer ao operador antes: a etiqueta das pedras (sinais KO 4 das gamas, nao 'tripla do toro').

## CONSULTAS AO MAPA
- rotas.py consultar montagem -> 14 rotas, todas de outros temas, exceto nenhuma da montagem 3+1 propria; consultar triplas -> 0; consultar Gromov -> 1: formal.k05_t1_montagem_gh_tau_campo_v412 (EXAMINADA_COM_DEFEITO, 14/11, proximo passo = ORDEM K07 rodada 3); consultar KO -> 6 (a unica pertinente e a mesma K05; as demais sao homonimos: pilar_v384, concrete_bosonic_kinematics)
- rotas.py consultar Kronecker -> 0; shuffle -> 0; Dirac -> 2 e Pauli -> 2, todas sem relacao (hubble.fase9, kernel.v402, a_identidade_tem_nome, tempo_santo). Conclusao [REAL]: nenhuma rota previa de tripla espectral, produto de triplas ou GH quantico alem da K05; nada a refazer, nada registrado por mim.

## EXAMINADO
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\MONTAGEM_3MAIS1_R2.md
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\GH_III1_R2.md
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K05_MONTAGEM_GH.md
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ORDEM_K07_matematica_rodada_3.md (secao 3, l.41-45)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex (l.1818-1828, 1920-1952, 2248-2257)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_mgh\revisor_montagem.py (so Grep: tabela KO)
- TGLExt\PowersLadder.lean (l.244-259), SitePauliObservables.lean (Grep l.32-190), ModularCurrent.lean (l.60-90), TheTwoFolds.lean (l.134-140), Solder4D.lean (Grep nomes)
- Grep em TGLExt: SpectralTriple|KODim|koDim|KO_dim|Clifford|chirality|RealStructure|productTriple|Kronecker; Dixmier|Krein|Toeplitz|Hochschild|CliffordAlgebra|anticommutator|JordanWigner (0); pauli_*; anticomm
- Glob em v412\kimi por K07 e _R3 (sem MONTAGEM/GH_III1 R3 nem ENTREGA_K07)
- Script proprio (rascunho): C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_frente_b\L4\L4_identidades.py, rodado com C:\Python314\python.exe -B -X utf8: todas as identidades abaixo deram True [REAL numerico, nao formal]
- Nao localizei o Mathlib em disco (um find largo foi interrompido por mim): nomes Mathlib citados (CliffordAlgebra.lift, mul_kronecker_mul) sao [KNOWN, a conferir]
