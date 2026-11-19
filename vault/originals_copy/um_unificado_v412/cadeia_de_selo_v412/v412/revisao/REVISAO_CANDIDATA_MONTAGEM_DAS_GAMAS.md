# CONFERENCIA DISTINTA DA CANDIDATA MontagemDasGamas (frente B da v412; 15/11/2026)

> Montado pela gerencia c1 em 15/11/2026 16:20 a partir dos retornos estruturados dos agentes (modelo Sonnet, salvo o construtor da fiacao na luz). Cada retorno e' [DECLARADO pelo agente]; o que a gerencia conferiu por conta propria esta' dito na secao "O que a gerencia fez". Nada aqui e' fala do operador. Nada esta' instalado, selado ou aberto.

## O que a gerencia fez

1. Um construtor escreveu a candidata (56 teoremas; `candidatas_c1\REV0\MontagemDasGamas.lean`, sha16 55e1c680a5a0d91b).
2. Um revisor distinto a conferiu, com script numerico proprio e quatro mutacoes: aprovada com ressalvas; nenhum erro de matematica.
3. Rodada unica de conserto (R1, a versao corrente; sha16 41de0a594e4b551c; 55 teoremas): saiu o teorema que, lido sozinho, parecia dizer que J e D anticomutam; o cabecalho diz que do sinal de J com D so' sai a metade das gamas e que o ciclo de Hochschild nao e' construido; a soma das gamas deixou de se chamar dirac; a constante que estava no rascunho do Kimi saiu do texto.
4. Ressalvas que ficam: quinze teoremas dobraveis; a secao da soma sobre as permutacoes tem valor documental; e o juizo do revisor: sem o tipo de tripla espectral no kernel o arquivo e' ilha, e ele nao o instalaria antes de se decidir se a montagem 3+1 entra no artigo. A decisao e' do operador.

## Relato do construtor

Candidata nova compilada: MontagemDasGamas.lean, namespace TGLExt.MontagemDasGamas. RC 0, zero avisos, zero sorry, 56 teoremas, cada um com #print axioms no arquivo e todos em [propext, Classical.choice, Quot.sound]. Sem native_decide e sem decide +kernel; um unico `decide` simples (24 permutacoes de Fin 4) com maxRecDepth elevado so naquele teorema. Os cinco alvos G1 a G5 fecharam, e a versao abstrata em anel (clifford_sq) saiu barata, entao G2 tem as duas. Nenhum sinal do documento divergiu da conta: (J^2, JD, J chi) = (-1, +, +) bate; o lado de D esta no nivel das gamas (C conj(D(k)) C = D(-k) = -D(k)); a parte JD = DJ em L2 depende do fator -i de D = -i lambda soma Gamma d e da reflexao de modos k para -k, nada disso esta no arquivo. A constante certa: (-1/24) vezes a soma sobre S4 e exatamente chi (teorema constante_da_orientacao). Etiqueta no cabecalho: algebra finita das gamas e sinais KO 4 das gamas; nao e tripla espectral, Dirac em L2, montagem formalizada, III1 nem (1,3). MUSCULATURA (franqueza): G1, G2 (clifford_sq e dirac_sq: o motor algebrico do D^2 = soma k^2) e G4 (o rotulo KO 4 vira teorema sobre 4 matrizes 4x4); chi = 1 (x) sigma_z e a unica ligacao concreta com o documento (chi = 1 (x) tau_3). GORDURA: G5 e verificacao de 24 termos, valor documental (trava o retorno de -1/18), nao constroi o ciclo de Hochschild; e cerca de 30 dos 56 teoremas sao auxiliares (tabela de Pauli, map_star, conjC, kron). Sem o tipo tripla espectral no kernel, tudo isto e algebra finita solta sem consumidor. Nada instalado, selado ou movido; nenhum gate tocado. Um negativo aqui seria falha de prova, nao parede fisica; nao houve negativo.

### Declaracoes entregues

- [FECHADO] `gam_sq`: G1; por kron_mul_kron + pauli_*_square do kernel
- [FECHADO] `gam_anti`: G1; via seis lemas gam_anti_01..23 e anti_kron_esq/anti_kron_dir
- [FECHADO] `gam_selfadjoint`: G1; usa pauli_*_conjTranspose do kernel
- [FECHADO] `clifford_sq`: G2 abstrato (P1); prova por Finset.sum_involution no par (i,j)
- [FECHADO] `dirac_sq`: G2 concreto, instancia de clifford_sq; dirac e so rotulo da combinacao linear, nao o Dirac de L2
- [FECHADO] `chi_eq`: G3; a conta explicita, igual a chi = 1 (x) tau_3 do documento
- [FECHADO] `chi_sq`: G3
- [FECHADO] `chi_anti`: G3
- [FECHADO] `chi_selfadjoint`: G3
- [FECHADO] `matC_sq`: G4; renomeado de Cmat porque Bicommutant.lean do kernel ja tem outra def chamada Cmat
- [FECHADO] `matC_conj_matC`: G4; sinal de J^2 = -1
- [FECHADO] `matC_inverte_gam`: G4; via quatro lemas matC_inverte_gam_0..3
- [FECHADO] `matC_fixa_chi`: G4; sinal de J chi = chi J
- [FECHADO] `matC_conj_dirac`: G4; parte finita de JD = DJ; a reflexao de modos e a analise em L2 NAO estao aqui
- [FECHADO] `soma_permutacoes_anticomutativas`: G5 (P3 geral); sem native_decide: tabela do sinal por decide simples sobre as 24 permutacoes (sinal_por_inversoes) + 256 casos de fin_cases em reordena_produto
- [FECHADO] `soma_orientacao`: G5 corolario concreto
- [FECHADO] `constante_da_orientacao`: crava -1/24 (nao -1/18); NAO constroi o ciclo de Hochschild nem o emparelhamento pi_D(c)

### Pendencias ditas pelo construtor

- Nada instalado, selado, registrado no Mapa nem movido; nomes de teorema provisorios (em portugues).
- O arquivo importa TGLExt.SitePauliObservables, que puxa grande parte da torre: o import sozinho custa cerca de 26 s de compilacao; se quiserem import mais leve, a alternativa seria copiar as tres definicoes de Pauli (decisao da gerencia).
- Um unico `decide` simples sobre as 24 permutacoes (sinal_por_inversoes) com `set_option maxRecDepth 100000 in` so nesse teorema; compila em segundos. Sem native_decide e sem decide +kernel.
- Nao construidos: J antilinear em L2, JD = DJ em L2 (precisa do fator -i de D e da reflexao de modos), condicao de primeira ordem, ciclo de Hochschild, emparelhamento pi_D(c), tripla espectral, qualquer coisa de (1,3) ou III1. Propostas P2 (sq_par_impar), P5 (contabilidade de sinais do produto de J) e P6 (escala) ficaram DE FORA de proposito: o levantamento as classifica como gordura sem consumidor.
- A etiqueta do cabecalho (algebra finita das gamas e sinais KO 4 das gamas, nao tripla do toro) e escolha de desenho a dizer ao operador antes de qualquer instalacao, conforme o P7 do levantamento.
- Divergencia de nome, nao de conta: Cmat do enunciado virou matC (evita o homonimo Cmat de Bicommutant.lean).

## Conferencia (sobre a REV0)

**Veredito:** APROVADO_COM_RESSALVAS

**Recompilou:** {"rc": 0, "avisos": 0, "sha16": "55e1c680a5a0d91b", "teoremas_no_trio": 56}

Recompilei a copia na minha pasta (cwd dentro dela, pois o lean.exe exige o arquivo sob a raiz): RC 0, 38 s, sha16 55e1c680a5a0d91b (igual ao do construtor), zero avisos, zero erros, zero sorry/native_decide/axioma novo, 56 teoremas com #print axioms, os 56 em [propext, Classical.choice, Quot.sound] [REAL, script parse_log.py].
Conferi a algebra com numpy independente do Lean (confere_gamas.py): as quatro gamas (sx x sx, sy x sx, sz x sx, 1 x sy) sao autoadjuntas, de quadrado 1 e anticomutam; -(G1G2G3G4) = 1 x sz = chi; C = sy x 1 com C^2 = 1, C conj(C) = -1, C conj(Gj) C = -Gj, C conj(chi) C = chi; D(k)^2 = |k|^2; soma sobre S4 de sgn*G..G = -24 chi, logo (-1/24) da chi e (-1/18) da (4/3) chi, igual a revisao K05 [REAL].
Fui alem do Lean: num L2 truncado (81 modos, k em {-1,0,1}^4) com J = reflexao k->-k, depois C, depois conjugacao, deu J^2 = -1, JD = DJ, J chi = chi J, D chi = -chi D: o triplo (-1,+,+) do documento bate com estas gamas e este C. Sem a reflexao de modos o sinal de JD sai trocado (JD = -DJ): so o Lean nao o diz por inteiro (achado 1).
Mutacoes (4, na minha pasta): constante -1/18, epsilon = +1, chi sem o menos e C = 1 x sy; as quatro derrubam a compilacao (RC 1) nos teoremas esperados. Os enunciados nao sao ocos.
Nenhum erro de matematica, nenhuma hipotese oca, nenhum enunciado falso. Ressalvas: docstrings e cabecalho que prometem um tico mais que o enunciado (achados 1 e 2), nomes enganosos, e musculatura: 11 teoremas de conteudo, 3 complementos baratos, 21 de apoio, 15 dobraveis e 6 de G5 (sem consumidor no kernel). Sem tripla espectral no kernel, o arquivo inteiro e ilha: nao o instalaria antes de decidir se a montagem 3+1 entra no artigo.
Etiqueta do cabecalho: honesta quanto a tripla do toro, Dirac em L2, III1 e (1,3); incompleta quanto a metade de epsilon linha e ao ciclo de Hochschild (nao construido).
Mapa de Rotas consultado por termo unico: gamas, Clifford, Dirac, KO, chi, montagem, tripla. Nada sobre estas gamas nem sobre Clifford; so a rota formal.k05_t1_montagem_gh_tau_campo_v412 (K05, ressalva da constante) e rotas gerais. Nada refeito; este exame e novo e vai ao registro da gerencia.

### Achados

1. **(MEDIO)** MontagemDasGamas.lean, matC_conj_dirac_neg (l.288-293), cabecalho l.3-4 e secao G4

   O arquivo prova por inteiro epsilon = -1 (matC_conj_matC) e epsilon'' = +1 (matC_fixa_chi), mas de epsilon' = +1 so prova a metade das gamas, e essa metade vale -1: C conj(D(k)) C = -D(k). O +1 final e o produto desse (-1) pelo (-1) de conj(-i d) = +i d, isto e, a reflexao de modos k para -k, que nao esta no arquivo. Medido: no L2 truncado com a reflexao, JD = DJ; sem a reflexao, J'D = -DJ'. A matC_conj_dirac_neg, lida sozinha, parece dizer JD = -DJ (epsilon' = -1, que seria outra dimensao KO); o cabecalho diz sinais KO 4 das gamas sem dizer que epsilon' fica pela metade.

   *Conserto pedido:* Apagar matC_conj_dirac_neg (redundante com matC_conj_dirac, que ja tem a forma D(-k) com a reflexao dita na docstring). No cabecalho e na docstring de matC_conj_dirac acrescentar: epsilon' = +1 e o produto de (-1) das gamas, provado aqui, por (-1) da reflexao de modos de -i d, nao provado aqui.

2. **(MEDIO)** constante_da_orientacao (l.430-437) e cabecalho

   A docstring diz a constante certa do ciclo de orientacao e e nao -1/18. O enunciado e so a identidade finita (-1/24) vezes a soma sobre S4 de sgn(tau) G_t0..G_t3 = chi na algebra 4x4. O ciclo (produto shuffle no complexo de Hochschild, axioma 4 de Connes) nao esta no kernel, e a ligacao pi_D(shuffle) = soma sgn*Gamma e conta de papel fora do Lean. O -1/18 e um numero de um rascunho (K05 R2, que copia D-D (35)-(36)) que nao existe no arquivo; num kernel selado vira referencia solta e sugere erro de literatura nao conferido na fonte. O cabecalho nao diz que G5 nao constroi o ciclo.

   *Conserto pedido:* Reescrever: o somatorio sobre S4 de sgn(tau) G_t0 G_t1 G_t2 G_t3, normalizado por -1/24 = -1/|S4|, vale chi. Tirar ciclo de orientacao e o -1/18 do kernel (ficam no registro da gerencia). Renomear para soma_normalizada_sobre_S4_e_chi. Acrescentar ao cabecalho que o ciclo de Hochschild nao e construido.

3. **(MEDIO)** arquivo inteiro (julgamento de musculatura)

   Nao ha consumidor no kernel: sem tipo de tripla espectral, as gamas, chi, C e D(k) sao algebra finita solta; nenhum teorema do kernel a usa e nenhum teorema do arquivo alimenta algo fora dele. O ganho real e travar numeros e sinais do documento K05 (que a gerencia ja corrigiu no texto). O G5 e o elo mais fraco: 7 declaracoes (invSign mais 6 teoremas, incluindo fin_cases de 256 casos e um decide em 24 permutacoes) para travar uma constante de um ciclo que o kernel nao tem.

   *Conserto pedido:* Instalar so G1-G4 (as gamas, chi, C, sinais) mais dirac_sq/clifford_sq, e deixar G5 arquivado em work com o recibo, a menos que a gerencia queira a trava da constante; neste caso manter so soma_permutacoes_anticomutativas, soma_orientacao e constante_da_orientacao reescrita, com invSign, sinal_por_inversoes e reordena_produto como suporte.

4. **(BAIXO)** def dirac (l.276-278) e gam (l.122-128)

   A def se chama dirac, mas e a combinacao linear D(k) = soma kj Gj dos modos (a docstring diz rotulo, o nome promete operador). E gam usa indice de 0 a 3 enquanto a docstring e o documento usam Gamma 1 a 4, e os nomes gam_anti_01..23 e matC_inverte_gam_0..3 seguem o 0-base: leitura do documento contra o Lean pede deslocamento mental.

   *Conserto pedido:* Renomear dirac para somaGamas (ou combGamas); acrescentar na docstring de gam: gam 0 = Gamma 1, ..., gam 3 = Gamma 4.

5. **(BAIXO)** cinco blocos de teoremas especificos

   Gordura dobravel (15 de 56): gam_zero, gam_um, gam_dois, gam_tres (4, so servem de rewrite; basta unfold gam ou simp [gam]); gam_anti_01, 02, 12, 03, 13, 23 (6, so alimentam gam_anti, cuja combinator first ja e o fecho); matC_inverte_gam_0..3 (4, so alimentam matC_inverte_gam por fin_cases); matC_conj_dirac_neg (1, ver achado 1). Os pauli_zx_anti e pauli_zy_anti sao add_comm dos outros dois; map_star_add, map_star_smul, conjC_add e conjC_smul sao apoio de matC_conj_dirac e podem virar have dentro dela. Sobram cerca de 41 teoremas sem perda de conteudo.

   *Conserto pedido:* Dobrar os 14 primeiros em seus teoremas gerais e apagar o _neg; manter chi_sq, chi_selfadjoint e matC_sq como complementos baratos que as docstrings invocam (chi e grading; C^-1 = C).

6. **(BAIXO)** relato do construtor (nao o arquivo)

   O relato diz um unico decide simples; no fonte ha 14 by decide: um e o das 24 permutacoes (sinal_por_inversoes, com maxRecDepth 100000 so nele, l.364); os outros 13 sao desigualdades triviais de Fin 4 (i != j) em reordena_produto e soma_permutacoes_anticomutativas. Todos no kernel, sem native_decide e sem decide +kernel; so imprecisao do relato.

   *Conserto pedido:* Corrigir a frase no recibo para um decide de 24 permutacoes e 13 decide de desigualdades triviais de Fin 4.

7. **(BAIXO)** matC (l.218-219) e a lacuna L2

   Observacao de escopo, ja dita na docstring: J = C composta com a conjugacao e antilinear e nao e construido. O arquivo prova identidades de matrizes 4x4 sobre C, nao propriedades de um operador de Hilbert; J^2 = -1 aqui e C conj(C) = -1. Honesto, mas quem citar J^2 = -1 do kernel deve citar como identidade matricial.

   *Conserto pedido:* Nenhum no arquivo; nas citacoes a jusante dizer identidade matricial das gamas.

