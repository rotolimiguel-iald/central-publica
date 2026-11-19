# CONFERENCIAS DISTINTAS DA CANDIDATA ErgodicidadeDeMautner (frente B da v412; 15/11/2026)

> Montado pela gerencia c1 em 15/11/2026 16:20 a partir dos retornos estruturados dos agentes (modelo Sonnet, salvo o construtor da fiacao na luz). Cada retorno e' [DECLARADO pelo agente]; o que a gerencia conferiu por conta propria esta' dito na secao "O que a gerencia fez". Nada aqui e' fala do operador. Nada esta' instalado, selado ou aberto.

## O que a gerencia fez

1. Escreveu a parte abstrata (21 teoremas; `candidatas_c1\REV0\`, sha16 df2c7deaac84169b).
2. Um construtor acrescentou a secao da luz (58 declaracoes; `candidatas_c1\REV1\`, sha16 2d772af5d658fe90). Dois revisores distintos a conferiram: nenhum erro de matematica; os dois aprovaram com ressalvas.
3. O achado ALTO do segundo revisor: a ergodicidade da cunha da luz livre JA ERA teorema do kernel, sem condicao (`LightRhoStar.centralizer_is_trivial` no certificado habitado `physicalFockCertificate`). A gerencia conferiu por busca recursiva no kernel e no core e no selo da v411 (`certificate_inhabited` verdadeiro no registro `fechamento_v406`). O levantamento, a conferencia da K05 e a gerencia tinham dado por ausente ou por condicional: falso negativo.
4. Rodada unica de conserto (R2; `candidatas_c1\REV2\`, sha16 d82674444fe29c06): o cabecalho inteiro; a subsecao 8.4 passa a REEXPORTAR o que e' do kernel; saem nove declaracoes (pontes por definicao, tres variantes da ergodicidade e as duas especializacoes chamadas de esperanca); o limite de trabalho do elaborador sai; as docstrings deixam de prometer mais que o enunciado.
5. Um terceiro revisor conferiu so' o TEXTO da R2: nenhum achado alto; cinco medios e seis baixos, todos de frase. Aplicados na R3 (a versao corrente, `candidatas_c1\ErgodicidadeDeMautner.lean`; o sha256 se le do arquivo). Nao houve nova conferencia depois da R3: as trocas foram as que o revisor ditou.
6. Ressalvas que ficam, sem conserto: algumas pontes de uma linha continuam como teoremas (o revisor contaria cerca de 25 declaracoes de conteudo proprio); o contraexemplo de peso zero so' foi compilado no nivel de vetores.

## Relato do construtor da secao da luz

[REAL, medido aqui] A secao NaLuz foi acrescentada a candidata e os seis alvos (T1 a T6) fecharam. Compilacao do arquivo final: RC 0, 0 avisos, 0 erros, 0 sorry, sha16 2d772af5d658fe90 (lido do log por script; sha256 2d772af5d658fe90e584c985c3345a06af73bf9fd80be799946535bbcb3a3e3d, igual ao do arquivo), 39 s. O #print axioms lista 58 declaracoes, todas com exatamente [propext, Classical.choice, Quot.sound]: as 21 da base mais 34 teoremas e 3 definicoes novos. Sem native_decide, sem axioma, sem linter desligado.
Os 21 teoremas da gerencia NAO mudaram: por script, as 621 linhas da base antes do end final e o sufixo estao identicos dentro do arquivo final; a copia da base tem o mesmo sha256 do original (df2c7deaac84169b...). Fora do bloco novo so entraram 9 imports no topo. O bloco novo (420 linhas) fica depois dos #print da base e antes do end final.
O que fechou: T1 wedgeBoostMap s nullMinus = exp(-s) • nullMinus; T2 as tres familias como F →L[ℂ] F com todos os lemas que a pedra pede; T3 Mautner na luz pela pedra abstrata; T4 o vacuo como unico fixo de UF (l • nullDir), concreto e sem FockCertificate; T5 a ergodicidade em CanonicalWedgeFlow.M pela pedra abstrata, mais a versao com flow do kernel, a versao com actualModularFlow e a rota direta; T6 um so boost VF s0 (s0 ≠ 0): fixos na reta do vacuo, comutante escalar e media de Cesaro igual a ⟪vacuum, v⟫ • vacuum.
A igualdade KWR de M = spectralOutput.KWR e por definicao: fechou com rfl (teorema-ponte incluido).
O kernel JA TEM (grep -r): a versao 2x2 de T1 (TGLExt.boost_null_contract, BisognanoWichmann.lean:105, reexportada em Santo.lean:1200); T5 so condicional ao certificado (LightRhoStar.centralizer_is_trivial :71); T4 so condicional (light_null_ergodic :429) ou como campo; a metade T+ de Mautner embutida em ContratoH2.no_point_spectrum. Nenhum dos enunciados concretos T1 (4D), T3, T4, T5, T6 existe no kernel nem no inventario da bancada (0 ocorrencias de mautner, de wedgeBoostMap com nullMinus e de birkhoffAverage fora do Adendo1).
ALERTA de afericao [REAL]: a ferramenta Grep devolveu 0 para 'def VF ' e 'spectralOutput' na arvore TGLExt, mas grep -r acha os dois em F1Fecho394 (ha a regra .gitignore:37 tgl_kernel/**). Consulta de ausencia sobre F1Fecho394 feita pela ferramenta Grep pode ser falso negativo; usei grep -r.
Nada foi instalado, registrado no Mapa nem escrito fora da pasta B1. E candidata; os nomes sao provisorios.

### Declaracoes entregues

- [PROVADO] `o_boost_encolhe_a_outra_direcao_nula`: T1. O lema que faltava. Componentes 0 e 1 por wedgeBoostMap_apply0/apply1 e Real.cosh_sub_sinh; 2 e 3 por simp.
- [PROVADO] `a_direcao_nula_do_contrato_e_a_da_cunha_fisica`: Ponte por rfl entre as duas constantes de mesmo literal (ContratoQG_v31.lean:109 e PhysicalWedgeNullGeometryR3.lean:13). Nao pedida; barata.
- [DEFINICAO (compila; trio)] `boostNaLuz`: T2. delta como mapa linear continuo.
- [DEFINICAO (compila; trio)] `translacaoNulaMais`: T2. T+ como mapa linear continuo.
- [DEFINICAO (compila; trio)] `translacaoNulaMenos`: T2. T- como mapa linear continuo.
- [PROVADO] `o_boost_na_luz_age_como_VF`: T2. rfl.
- [PROVADO] `a_translacao_mais_age_como_UF`: T2. rfl.
- [PROVADO] `a_translacao_menos_age_como_UF`: T2. rfl.
- [PROVADO] `o_boost_na_luz_preserva_o_produto_interno`: T2 (hδ da pedra). LinearIsometryEquiv.inner_map_map.
- [PROVADO] `a_translacao_mais_preserva_a_norma`: T2 (hTp).
- [PROVADO] `a_translacao_menos_preserva_a_norma`: T2 (hTm).
- [PROVADO] `a_translacao_mais_em_zero_e_a_identidade`: T2 (hp0). zero_smul + UF_zero.
- [PROVADO] `a_translacao_menos_em_zero_e_a_identidade`: T2 (hm0).
- [PROVADO] `a_translacao_mais_e_continua_em_zero`: T2 (hpc). translations_strong composto com a ↦ a • nullDir.
- [PROVADO] `a_translacao_menos_e_continua_em_zero`: T2 (hmc).
- [PROVADO] `a_covariancia_do_boost_com_a_translacao_mais`: T2, na forma do kernel. VF_UF_VF_symm + wedgeBoostMap_smul + wedgeBoostMap_nullDir.
- [PROVADO] `a_covariancia_do_boost_com_a_translacao_menos`: T2, na forma do kernel. Usa T1. E o enunciado de T- sob o mesmo delta que o kernel nao tinha.
- [PROVADO] `o_boost_alarga_a_translacao_mais`: T2 (hcp da pedra).
- [PROVADO] `o_boost_encolhe_a_translacao_menos`: T2 (hcm da pedra).
- [PROVADO] `a_translacao_mais_atravessa_o_boost`: Auxiliar de T6: a covariancia lida do lado que alarga (forma hcov de o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao).
- [PROVADO] `a_translacao_menos_atravessa_o_boost`: Auxiliar de T6.
- [PROVADO] `o_fixo_do_boost_da_luz_e_fixo_das_translacoes_nulas`: T3. Mautner na luz. Termo unico: o_fixo_do_boost_e_fixo_das_translacoes aplicado as tres familias.
- [PROVADO] `o_vacuo_e_o_unico_fixo_da_translacao_nula_da_luz`: T4. Concreto, sem FockCertificate. gamma_no_fixed com u := fun l => U1 (l • nullDir) e light_null_translations_no_eigen; e o corpo de light_null_ergodic sem o certificado.
- [PROVADO] `o_fixo_da_translacao_mais_e_multiplo_do_vacuo`: T4 na forma hvac da pedra. So a translacao de nullDir entra; a de nullMinus nao e usada.
- [PROVADO] `o_subespaco_da_cunha_do_fluxo_e_o_do_separador`: A ponte pedida: e por definicao (rfl compila).
- [PROVADO] `o_vacuo_separa_a_algebra_da_cunha`: canonical_wedge_separating com a pertinencia em M (igual por definicao).
- [PROVADO] `a_ergodicidade_na_luz`: T5. Termo unico: o_que_comuta_com_o_boost_e_escalar com M.toStarSubalgebra.toSubalgebra, vacuum, o separador, VF_vacuum e T4. O Mautner entra por dentro da pedra abstrata (T3 e o mesmo passo exposto na forma concreta).
- [PROVADO] `a_ergodicidade_na_luz_pelo_fluxo_da_cunha`: T5 com o fluxo do kernel. Mesma forma de LightRhoStar.centralizer_is_trivial, agora sem certificado. t := -s/(2π).
- [PROVADO] `a_algebra_do_par_de_tomita_e_a_da_cunha`: rfl. Liga M ao par de canonical_pair_tomita.
- [PROVADO] `a_ergodicidade_na_luz_pelo_fluxo_modular`: Extra barato: actualModularFlow_eq_gamma_apply (CanonicalFockBWR2.lean:26).
- [PROVADO] `a_ergodicidade_na_luz_pela_rota_direta`: T5 pela segunda rota, sem Mautner: o_um_e_o_unico_fixo_da_luz (ausencia de autovetor do BOOST em uma particula) + separador. As duas rotas usam fatos de uma particula diferentes.
- [PROVADO] `a_exponencial_de_um_negativo_encolhe`: Auxiliar de T6.
- [PROVADO] `o_fixo_de_um_so_boost_da_luz_e_o_vacuo`: T6. s₀ < 0: o_fixo_de_uma_dilatacao_e_fixo_da_translacao com U := VF s₀, q = exp s₀. s₀ > 0: em vez de trocar para VF (-s₀), usei o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao com o mesmo VF s₀ e q = exp (-s₀). Depois T4. Aqui a pedra nao e redundante: gamma_no_fixed pede o grupo inteiro.
- [PROVADO] `os_fixos_de_um_so_boost_da_luz_sao_a_reta_do_vacuo`: T6, forma se e somente se.
- [PROVADO] `o_que_comuta_com_um_so_boost_da_luz_e_escalar`: T6. o_que_comuta_com_uma_dilatacao_e_escalar; conforme o sinal de s₀ os papeis de Tp e Tm da pedra sao trocados (encolhe nullDir se s₀ < 0, nullMinus se s₀ > 0).
- [PROVADO] `a_media_de_um_so_boost_da_luz_e_a_esperanca_do_vacuo`: T6. a_media_do_boost_e_a_esperanca_do_vacuo com a mesma troca de papeis; vacuum_norm.
- [PROVADO] `a_esperanca_sobre_os_fixos_de_um_so_boost_da_luz_e_o_estado`: Corolario de uma linha (v := x vacuum), espelho de a_esperanca_sobre_os_fixos_e_o_estado.

### Pendencias ditas pelo construtor

- [OPEN como termo] Nao ha, nem escrevi, a ausencia de autovetor das translacoes ao longo de nullMinus em uma particula; logo 'fixo so por UF (a • nullMinus) => reta do vacuo' nao esta provado. Nao fez falta: a hipotese hvac da pedra foi paga so com nullDir (T4), e nos casos s₀ > 0 de T6 a translacao de nullMinus entra apenas como a que encolhe.
- [REAL] Redundancia dita: no Fock livre a rota direta (o_um_e_o_unico_fixo_da_luz + separador) ja da T5 em poucas linhas. O que a pedra abstrata compra aqui e T3 (o boost fixa => as duas translacoes fixam), T4 montado sem certificado e, sobretudo, T6 (um so boost), que o gamma_no_fixed nao da porque pede o grupo inteiro.
- [REAL] T6 divergiu da sugestao em um detalhe: para s₀ > 0 nao troquei U por VF (-s₀); usei o lema o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao da propria pedra com o mesmo VF s₀. O enunciado e o pedido.
- [REAL] M e FieldWeyl.R do subespaco canonico KWR (construcao espectral). A ligacao com a cunha direita fisica existe no kernel: physical_right_wedge_eq_KWR (F1Fecho394\PhysicalCanonicalWedgeEqualityR3.lean:27). O corolario 'todo x de FieldWeyl.R (localized physicalRightWedge) que comuta com VF s e escalar' sai por um rw; compilei como SONDA separada, fora da candidata (C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_frente_b\B1\SondaCunhaFisica.lean, RC 0, trio, sha16 5e20edfc925a3dac). Incluir ou nao e decisao da gerencia; custa mais um import.
- [REAL] Os 9 imports novos alargam o fecho de dependencias da pedra abstrata (agora puxa F1Fecho394). Se a gerencia preferir a pedra abstrata leve, o bloco esta isolado em NaLuz_secao.txt e pode virar um segundo arquivo que importa o primeiro; nao fiz porque a ordem pediu a secao dentro do mesmo namespace e arquivo.
- [REAL] O cabecalho do arquivo continua o da base ('RASCUNHO R0', sem fontes nem estatutos): nao toquei; cabe a gerencia atualizar depois da conferencia distinta.
- [REAL] O que NAO se compra: nenhum habitante de FockCertificate; nada sobre a cunha do horizonte da TGL (o residuo BW nao-Killing segue [OPEN]); vale so no campo livre (Fock canonico). O enunciado e sobre comutar com o boost unitario VF; que actualModularFlow seja esse boost e do kernel (actualModularFlow_eq_gamma).
- [REAL] ALERTA de afericao: a ferramenta Grep devolveu 'No matches found' para 'def VF ' e para 'spectralOutput' na arvore TGLExt, e grep -r acha os dois em F1Fecho394 (git check-ignore aponta .gitignore:37 tgl_kernel/**). Qualquer consulta de ausencia feita por essa ferramenta sobre F1Fecho394 merece ser refeita com grep -r; nao reli as consultas da REVISAO_K05 nem as do L3.
- [REAL] O kernel ja tem analogos que a gerencia deve citar se reexportar: boost_null_contract (BisognanoWichmann.lean:105; 2x2, vetor ![1,-1]; reexportado em Santo.lean:1200), sem ponte achada por grep entre o boost 2x2 e o boostMat 4x4 (busca nao exaustiva); centralizer_is_trivial (LightRhoStar.lean:71) e light_null_ergodic (TheImportedSecondQuantization.lean:429), ambos condicionais ao certificado; a metade T+ de Mautner dentro de ContratoH2.no_point_spectrum (ContratoQG_v31_Teoremas.lean:132).
- [DECLARADO] Compilei contra os .olean do sandbox k411c e li as fontes em Nos\tgl_kernel\TGLExt; nao conferi por hash que as duas arvores sao a mesma versao, nem a pertenca dos modulos ao selo v411.
- [REAL] Tempos: a primeira compilacao (base intocada) levou 244 s por cache frio; as seguintes, 35 a 41 s. O set_option maxHeartbeats 4000000 da base ficou como estava; nao medi se o bloco novo precisa dele.
- [REAL] Unico erro no caminho, ja corrigido: na primeira tentativa de T1 o simp desfazia a reescrita por cosh_sub_sinh (goal restante 'cosh s - sinh s = exp (-s)'); troquei por e0/e1 por rfl e ring. E o nome Real.exp_lt_one nao existe: o correto e Real.exp_lt_one_iff.
- Conferencia distinta ainda nao houve: quem construiu fui eu; os enunciados devem ser relidos por revisor diferente antes de qualquer uso. Nada foi instalado, selado nem registrado no Mapa.

## Primeira conferencia: compilacao, vacuidade e contraexemplos (sobre a REV1)

**Veredito:** APROVADO_COM_RESSALVAS

**Recompilou:** {"rc": 0, "avisos": 0, "sha16": "2d772af5d658fe90", "teoremas_no_trio": 58}

[REAL, medido aqui] Recompilei a candidata na minha pasta: RC 0, 0 avisos, 0 erros, 0 sorry, 0 sorryAx, 58 #print axioms todos exatamente [propext, Classical.choice, Quot.sound], sha256 igual ao do construtor (sha16 2d772af5d658fe90, 63 s). Rodei tambem com maxHeartbeats 800000 e com o padrao (sem a linha): RC 0 e 0 avisos nos dois, logo os 4000000 sao desnecessarios.
Por script: as 621 linhas da base vem iguais ao original (sha df2c7deaac84169b); o bloco novo tem 34 teoremas e 3 definicoes, como declarado. Grep -r no kernel: nenhum Mautner nem ergodicidade concreta pre-existente; o que existe (LightRhoStar.centralizer_is_trivial, light_null_ergodic) e condicional ao certificado, como o construtor disse.
Nenhum achado ALTO: nao achei enunciado falso, hipotese oca nem conclusao embutida em hipotese. M da secao NaLuz e mesmo a algebra de von Neumann da cunha (FieldWeyl.R KWR); VF s e o fluxo modular (actualModularFlow t = gamma (B0 (-(2 pi t))), conferido pelo teorema a_ergodicidade_na_luz_pelo_fluxo_modular).
Contraexemplos compilados (so trio): sem o vacuo unico a conclusao de o_que_comuta_com_o_boost_e_escalar falha (dim 2); com peso zero a mistura vetorial nao fixa cada ato; sem a saturacao o dominio multiplicativo falha (Phi(a,b)=(a+b)/2); com s0 = 0 os fixos de VF nao sao so o vacuo e a ergodicidade de um so boost e falsa; M nao e feito so de escalares (usa wedge_nonabelian do kernel).
Dimensao finita: compilei que as hipoteses de covariancia ja forcam T = 1 (a translacao e trivial); com o vacuo unico isso obriga dim H menor ou igual a 1. Entao as secoes 2 a 4 so tem conteudo em dimensao infinita e devem dizer isso no cabecalho; o modelo de consistencia e o Fock da luz (secao 8).
Ressalvas MEDIO sao de enquadramento (o que a pedra compra): Tm e nullMinus sao dispensaveis para T4 a T6; Mautner nao e o que fecha T5 no Fock (ha rota direta no kernel); o rotulo H_erg como teorema precisa de escopo. Os demais achados sao BAIXO. Nada foi instalado nem escrito fora da minha pasta.

### Achados

1. **(MEDIO)** secao 8; usos de hvac em a_ergodicidade_na_luz, o_que_comuta_com_um_so_boost_da_luz_e_escalar, a_media_de_um_so_boost...; docstring de o_boost_encolhe_a_outra_direcao_nula (O LEMA QUE FALTAVA)

   A translacao Tm (nullMinus) e o lema T1 4D nao entram em nenhuma conclusao de T4, T5 ou T6: todo hvac passado a pedra abstrata descarta a premissa de Tm (fun v hp _ => ...), porque o vacuo unico so e usado para a translacao que o boost encolhe. [REAL] Compilei TesteTpSo.lean (sha16 b95f50db72173b81, trio): a ergodicidade de UMA dilatacao vale com vacuo unico para UMA translacao so. Logo nullMinus so alimenta T3 (os fixos do boost sao fixos das DUAS translacoes) e metades redundantes dos teoremas abstratos. Chamar o lema de O QUE FALTAVA promete mais do que ele compra.

   *Conserto pedido:* Trocar a docstring por: a outra direcao nula e autodirecao do boost com fator exp(-s). E no cabecalho dizer que T4 a T6 dependem so de nullDir e que nullMinus serve a T3. Nao e preciso reescrever as pedras.

2. **(MEDIO)** docstring de a_ergodicidade_na_luz; cabecalho a escrever

   No Fock da luz a ergodicidade T5 nao precisa de Mautner: o kernel ja tem OUmInscrito.o_um_e_o_unico_fixo_da_luz (incondicional, v407), e a propria candidata prova T5 em 12 linhas por a_ergodicidade_na_luz_pela_rota_direta. O que Mautner compra de novo e T6 (UM so boost s0 diferente de 0, onde B0_no_eigen nao se aplica) e a forma abstrata. A docstring diz pela pedra abstrata, o que e verdadeiro mas incompleto.

   *Conserto pedido:* No cabecalho: T5 tem duas provas independentes (Mautner e rota direta); o ganho de Mautner e T6 e a independencia.

3. **(MEDIO)** secoes 2 a 4 (o_nucleo, o_fixo_de_uma_dilatacao_*, os_fixos_da_dilatacao_sao_o_vacuo, o_que_comuta_*, a_media_*); pergunta 2 do foco

   Em dimensao finita o argumento e vazio, e isso deve constar. [REAL] TesteDimFinita.lean (sha16 f3aece75d9f4a8c5, trio): H de dimensao finita, U preserva o produto interno, T 0 = 1, T fortemente continua em 0 e U (T a v) = T (q a) (U v) com |q| menor que 1 implicam T a v = v para todo a, v (continuidade forte vira continuidade em norma e a conjugacao por U^n preserva a norma). Com hvac e todos os vetores fixos, a hipotese forca dim H menor ou igual a 1. Os teoremas abstratos sao verdadeiros mas sem conteudo em dimensao finita; a consistencia das hipoteses vem de F (dimensao infinita, infinite_dimensional do kernel) e de M nao abeliano ([REAL] TesteLuz.lean, M_nao_e_so_escalares, sha16 e5687023ecb48451, trio).

   *Conserto pedido:* Frase no cabecalho: o conteudo das secoes 2 a 4 mora em dimensao infinita; em dimensao finita a translacao e forcada a ser trivial; o modelo nao trivial e o Fock da luz (secao 8).

4. **(MEDIO)** docstring de o_que_comuta_com_o_boost_e_escalar (H_erg COMO TEOREMA)

   O rotulo H_erg nao e definido no arquivo e a frase H_erg COMO TEOREMA pode ser lida como se a ergodicidade do horizonte da TGL estivesse fechada. O que a pedra prova: dados vacuo unico (hipotese nomeada) e Omega separador, o comutante escalar; e a instancia do Fock livre da luz (secao 8) fecha essas hipoteses sem certificado. Para o horizonte da TGL (GH em III1) o Mapa registra H_erg ausente no kernel (rota formal.k05_t1_montagem_gh_tau_campo_v412) e a transferencia segue [OPEN].

   *Conserto pedido:* Docstring sobria: Todo x de M que comuta com o boost e escalar, dado o vacuo unico e a separacao. O rotulo H_erg e o escopo (Fock livre; horizonte da TGL [OPEN]) vao no cabecalho.

5. **(BAIXO)** linha 20 do arquivo

   set_option maxHeartbeats 4000000 e desnecessario e pode mascarar custo: [REAL] ErgHB800k.lean e ErgHBdef.lean (sem a linha) compilam com RC 0, 0 avisos, 58 no trio.

   *Conserto pedido:* Remover a linha, ou usar 800000 como os modulos vizinhos do kernel.

6. **(BAIXO)** cabecalho do arquivo (linhas 12 a 17)

   Cabecalho ainda e o rascunho R0 provisorio: sem fontes, sem o que compra e nao compra, sem estatutos. Precisa citar como [KNOWN]: Mautner, o dominio multiplicativo de Choi, o teorema ergodico de von Neumann (A1_cesaro do Adendo1), Reeh-Schlieder/separacao, Bisognano-Wichmann; e dizer que as secoes 5 a 7 (21 teoremas da base) nao estao no caminho de T3 a T6.

   *Conserto pedido:* Completar o cabecalho depois desta revisao, com os escopos dos achados MEDIO acima.

7. **(BAIXO)** a_esperanca_sobre_os_fixos_e_o_estado; a_esperanca_sobre_os_fixos_de_um_so_boost_da_luz_e_o_estado; a_media_*_e_a_esperanca_do_vacuo

   Os nomes dizem esperanca (condicional), mas o enunciado e a projecao de von Neumann (media de Cesaro) aplicada ao VETOR x Omega, com limite <Omega, x Omega> Omega. A esperanca condicional da algebra (limite fraco de Ad(U^n)(x)) nao esta provada. A docstring diz na face de vetores, mas o nome promete mais. E <Omega, v> Omega e a projecao na reta do vacuo, nao um valor esperado.

   *Conserto pedido:* Renomear (por exemplo a_media_aplicada_a_x_vacuo...) ou acrescentar na docstring: nao e a esperanca condicional da algebra.

8. **(BAIXO)** o_boost_na_luz_age_como_VF, a_translacao_mais_age_como_UF, a_translacao_menos_age_como_UF, a_direcao_nula_do_contrato_e_a_da_cunha_fisica, o_subespaco_da_cunha_do_fluxo_e_o_do_separador, a_algebra_do_par_de_tomita_e_a_da_cunha

   Seis dos 34 teoremas novos sao rfl, e outros sao reexportacao de uma linha do kernel. Contar 34 teoremas superestima o conteudo; sao pontes por definicao, honestas, mas nao teoremas de conteudo.

   *Conserto pedido:* Dizer no cabecalho: x teoremas de conteudo mais 6 pontes por definicao.

9. **(BAIXO)** docstring de o_fixo_de_uma_dilatacao_e_fixo_da_outra_translacao; docstring de a_mistura_so_fixa_o_que_cada_ato_fixa

   Lado que ALARGA e impreciso: o teorema e o mesmo passo de Mautner para a forma T a (U v) = U (T (q a) v) com |q| menor que 1 (em NaLuz e usado para nullDir quando s0 e positivo e para nullMinus quando s0 e negativo, entao outra translacao no nome confunde). Em O LEMA A, NA FACE FINITA, face finita aqui e soma finita (Finset), mas na casa face finita costuma nomear a face de dimensao finita.

   *Conserto pedido:* Escrever a forma da relacao na docstring e trocar na face finita por para misturas finitas.

10. **(BAIXO)** processo

   O arquivo da candidata tambem existe em work\cadeia_de_selo\v412\candidatas_c1\ErgodicidadeDeMautner.lean com o mesmo sha256 (2d772af5...), gravado as 15:45:51, depois da entrega do construtor (15:32). Nao fui eu (so escrevi na minha pasta); provavelmente a copia do orquestrador. Registro para a custodia saber qual e o original.

   *Conserto pedido:* Nenhum; so conferir a origem da copia antes de instalar.

11. **(BAIXO)** limite do meu exame

   O contraexemplo de peso zero esta compilado so no nivel vetorial (o passo que usa hp: p = (1,0), w = (1,-1), v = 1); no nivel de algebra o argumento e por reducao (com p = (1,0) a mistura e o proprio alpha_0) e NAO foi compilado, porque exigia construir um StarAlgHom. As hipoteses das secoes 5 a 7 sao satisfeitas por exemplos [KNOWN] (esperanca condicional em M2 com vetor maximalmente emaranhado), nao compilados aqui.

   *Conserto pedido:* Nenhum no arquivo; apenas nao tratar o nivel de algebra como compilado.

## Segunda conferencia: duplicacao com o kernel e com o Mathlib; correspondencia com a T1 no papel (sobre a REV1)

**Veredito:** APROVADO_COM_RESSALVAS

**Recompilou:** {"avisos": 0, "rc": 0, "sha16": "2d772af5d658fe90", "teoremas_no_trio": 58}

1. [REAL] Recompilei na minha pasta: RC 0, 0 avisos, 0 erros, 0 sorry, 63 s, sha256 igual ao do arquivo do construtor (sha16 2d772af5d658fe90). Li o log por script: 58 declaracoes (55 teoremas e 3 defs), as 58 com exatamente propext, Classical.choice e Quot.sound; sem native_decide, sem axioma, sem linter desligado. Por diff contra a base de 622 linhas (df2c7deaac84169b): so entraram 9 imports no topo e 420 linhas depois dos #print da base; os 21 teoremas da gerencia estao intactos.
2. Matematica: nao derrubei nenhum enunciado. Li as 1051 linhas; as hipoteses sao satisfeitas pelos objetos concretos do kernel, nenhuma e oca, e os fatos de base (UF, VF, B0, KWR, M) estao no kernel.
3. ACHADO PRINCIPAL [REAL, compilado por mim]: T5 e T4 nao sao novidade do kernel. O kernel ja tem LightRhoStar.centralizer_is_trivial (l.71) e light_null_ergodic condicionais a FockCertificate, E o kernel ja exibe o habitante physicalFockCertificate (F1Fecho394/CanonicalFockModularCoreInputR1.lean:126, so trio). Compilei TesteDuplicacao (sha16 dd1cd43b53e96042, RC 0): t5_pelo_que_o_kernel_ja_tinha deriva a_ergodicidade_na_luz em cerca de 25 linhas daquele teorema + wedge_glue, no trio. TesteDuplicacao2 (sha16 e4b26e834e7bb421, RC 0): t4 sai de light_null_ergodic physicalFockCertificate; M e nao-abeliana; M = FieldWeyl.R (localized physicalRightWedge).
4. Logo a premissa T5 so condicional ao certificado e a linha do Mapa e da K05 e do L1 H_erg ausente no kernel sao falsos negativos de afericao (o grep procurou centralizer_trivial; o nome real e centralizer_is_trivial). A frase na luz livre H_erg deixa de ser hipotese e VERDADEIRA, mas ja era verdade no kernel; nao e merito desta pedra.
5. Genuinamente novo (kernel e Mathlib sem equivalente, por grep -r e grep no Mathlib): T1 em 4D; T3 (Mautner abstrato, com a translacao T menos e com uma so dilatacao; a metade T mais com fase esta embutida em ContratoQG_v31_Teoremas.lean no_point_spectrum, l.132, sob ContratoH2); T6 (um so boost s0 diferente de zero: fixos, comutante escalar, Cesaro), que o kernel nao tem; secoes 5 a 7 (dominio multiplicativo, fixos formam algebra, Lema A face finita): zero no kernel e zero no Mathlib.
6. O proprio a_ergodicidade_na_luz_pela_rota_direta mostra que Mautner e dispensavel para T5 na luz (usa OUmInscrito.o_um_e_o_unico_fixo_da_luz, l.36). Mautner so e necessario em T6.
7. Correspondencia com a T1 do papel: a pedra e a face de kernel da Proposicao da cunha (H_erg para a cunha: secoes 1 a 3 e 8) e, em forma finita e vetorial, de um pedaco do Lema A (secao 7); as secoes 5 e 6 sao a face do remark do artigo sobre dominio multiplicativo, que a K05 nao usa em passo algum; a secao 4 e so analoga ao passo L2 do Lema B.
8. NAO compra da T1: Lema B (traco canonico, media gaussiana Phi_t, Holder L2 para L1, passagem sigma-fraca, E_tau); Lema C (produto cruzado, comutante relativo); Lema A na forma continua (nu_t de suporte total, integral normal, q.t.p. para todo s); H_K chapeu (K afiliado e F injetiva); phi(1) finito vale aqui (estado, phi(1)=1) mas nada o usa; o residuo BW nao-Killing (H_TGL-horizon, OPEN); tipo III1 nao e termo; a condicao espectral e trocada, na luz livre, pela medida nula do nivel de energia nula (Fubini).
9. Frase que a pedra pode dizer sem exagero: na luz livre do kernel (campo sem massa, fibra complexa de dimensao 2, algebra de Weyl da cunha direita fisica, estado do vacuo), todo x de M que comuta com o fluxo modular, ou com UM so boost nao trivial, e escalar, sem hipotese de certificado. Ressalvas exatas: e o centralizador do vacuo na algebra da cunha do campo livre; nao e o horizonte da TGL; III1 nao e termo; a fase de Wigner do boost B0 esta removida por cobordo (docstring de B0 diz KNOWN a conferir); localidade causal para regioes arbitrarias fora; e o que a pedra acrescenta ao kernel e a rota por translacao nula e o um-so-boost, nao a existencia de H_erg.
10. O que esta revisao decide: matematica e compilacao (passam) e fidelidade das frases (tres frases prometem mais que o enunciado, ver achados). O negativo desta revisao nao e falsificacao: e correcao de redacao e de premissa de novidade.

### Achados

1. **(ALTO)** ErgodicidadeDeMautner.lean l.633-637 (cabecalho da secao 8), l.831-865 e l.799-818; kernel: LightRhoStar.lean:71, TheImportedSecondQuantization.lean:429, F1Fecho394/CanonicalFockModularCoreInputR1.lean:126; testes: V_B1_b/TesteDuplicacao.lean e TesteDuplicacao2.lean

   Premissa falsa de novidade: T5 (a_ergodicidade_na_luz e as tres variantes) e T4 ja existem no kernel como instancias de teoremas condicionais cujo certificado o kernel habita (physicalFockCertificate, F1.FECHO 16/10/2026, so trio). Compilei a derivacao de T5 a partir de LightRhoStar.centralizer_is_trivial + physicalCanonicalNet.wedge_glue (RC 0, trio) e de T4 a partir de light_null_ergodic physicalFockCertificate. O relato do construtor (T5 so condicional ao certificado; T4 so condicional) e o cabecalho (Nenhum enunciado daqui toma FockCertificate como hipotese) sao verdadeiros e enganosos por omissao. A linha do Mapa K05 e a conclusao L1 A9 (H_erg ausente no kernel) sao falsos negativos: o grep usou centralizer_trivial, o nome real e centralizer_is_trivial (LightRhoStar.lean:71, tambem no INVENTARIO com outro nome).

   *Conserto pedido:* Cabecalho e docstrings de T4/T5 passam a dizer: segunda rota (translacao nula / Mautner) para conclusao que o kernel ja tem em LightRhoStar.centralizer_is_trivial e light_null_ergodic instanciados em physicalFockCertificate (citar nomes e arquivos). Reservar a palavra novo para T1 4D, T3, T6 e secoes 5 a 7. Errata ao lado no Mapa (rota K05, linha H_erg ausente no kernel) e no L1 A9, a cargo da gerencia; eu nao registrei nada.

2. **(MEDIO)** l.831-833, l.887-906; OUmInscrito.lean:36

   A docstring de a_ergodicidade_na_luz (l.831-833) e o nome da pedra (Ergodicidade por Mautner) sugerem que Mautner e o que fecha H_erg na luz. A propria rota direta da candidata (l.887-906, usando OUmInscrito.o_um_e_o_unico_fixo_da_luz, kernel l.36) fecha o mesmo enunciado sem Mautner. Mautner so e indispensavel em T6 (um so boost), onde o kernel nao tem ausencia de autovetor de um boost isolado.

   *Conserto pedido:* Dizer no cabecalho: para o grupo todo de boosts a via direta basta; Mautner e a via que usa so a translacao nula e e o que habilita T6.

3. **(MEDIO)** l.157-173 (o_que_comuta_com_o_boost_e_escalar) e l.203-204

   Titulo H_erg COMO TEOREMA (l.157) na secao abstrata promete mais que o enunciado: o teorema carrega hvac (vacuo unico sob as duas translacoes) como hipotese nomeada, que esconde a condicao espectral e as direcoes transversais. So na secao 8 hvac e descarregada.

   *Conserto pedido:* Trocar por H_erg SOB O VACUO UNICO NOMEADO; deixar H_erg COMO TEOREMA para a_ergodicidade_na_luz.

4. **(MEDIO)** l.229, l.272-288, l.976-1009

   Linguagem de esperanca condicional: a_esperanca_sobre_os_fixos_e_o_estado diz a esperanca condicional sobre os fixos do boost devolve o valor do estado do vacuo vezes o Um. O enunciado e a projecao ortogonal sobre os fixos de UMA isometria (Cesaro discreto, teorema ergodico de von Neumann) aplicada a x Omega: nao e a esperanca normal M para a algebra dos fixos, nem a media gaussiana Phi_t, nem E_tau; vale so no vetor. O Um e ambiguo. Alem disso a versao da l.272 e especializacao de uma linha (v := x Omega) da l.237; a da l.1003 idem.

   *Conserto pedido:* Docstring: projecao ortogonal sobre os fixos aplicada a x Omega, na face de vetores; nao usar esperanca condicional; fundir ou cortar as duas especializacoes.

5. **(MEDIO)** final da secao 8.5; B1/SondaCunhaFisica.lean; F1Fecho394/PhysicalCanonicalWedgeEqualityR3.lean:27

   Nao-vacuidade nao esta no arquivo: nada na candidata diz que M nao e escalar (sem isso ergodico seria vazio) nem que M e a algebra da cunha direita FISICA. Ambos valem no kernel e compilei: M_nao_abeliana (de physicalFockCertificate.wedge_nonabelian) e M = FieldWeyl.R (localized physicalRightWedge) (por physical_right_wedge_eq_KWR), ambos so trio. O construtor tinha uma sonda para a cunha fisica (B1/SondaCunhaFisica.lean) que nao entrou.

   *Conserto pedido:* Acrescentar dois corolarios curtos: M nao-abeliana e a ergodicidade enunciada na algebra de Weyl da cunha direita fisica (reescrita por physical_right_wedge_eq_KWR). O cabecalho deve citar a limitacao do arquivo-fonte: localidade causal para regioes arbitrarias e outro teorema.

6. **(MEDIO)** cabecalho do arquivo (l.12-17, RASCUNHO R0)

   O cabecalho final precisa listar o que a T1 do papel NAO recebe: Lema B (traco canonico, Phi_t gaussiana, Holder L2 para L1, passagem sigma-fraca, E_tau, phi(1) finito), Lema C (produto cruzado, comutante relativo), Lema A em forma continua (nu_t gaussiana de suporte total, integral normal, q.t.p. para todo s, familia fiel; a pedra tem media finita e um unico Omega), H_K chapeu, residuo BW nao-Killing (H_TGL-horizon), tipo III1 (nao e termo), condicao espectral (na luz livre substituida por Fubini). As secoes 5 e 6 correspondem a um remark do artigo, nao a passo da prova da K05.

   *Conserto pedido:* Incluir a lista acima no cabecalho; dizer em uma frase que a pedra e a face de kernel da Proposicao da cunha e de um pedaco do Lema A, nao da T1 inteira.

7. **(BAIXO)** secoes 1 e 2 (l.27-147)

   Precedente nao citado: a metade T mais de Mautner (coeficiente invariante por escala, limite, igualdade em Cauchy-Schwarz) ja esta no kernel em ContratoQG_v31_Teoremas.lean eigen_null_correlation_dilation (l.99) e no_point_spectrum (l.132), sob ContratoH2, com fase. Novo: abstracao sem ContratoH2, a translacao T menos, uma so dilatacao, filtro geral.

   *Conserto pedido:* Citar os dois teoremas no cabecalho como precedente e dizer o que a versao abstrata acrescenta.

8. **(BAIXO)** l.529-561

   O lema de convexidade estrita da secao 7 (a_mistura_de_vetores_de_mesma_norma) e derivavel por contrapositiva do Mathlib: norm_sum_lt_of_strictConvexSpace (Analysis/Convex/StrictCombination.lean:107), com UniformConvexSpace.toStrictConvexSpace (Convex/Uniform.lean:125) e InnerProductSpace.toUniformConvexSpace (InnerProductSpace/Convex.lean:36), via espaco real subjacente. A prova da candidata e a conta direta da variancia e esta correta. Nao ha no Mathlib (grep) dominio multiplicativo, Kadison-Schwarz nem Mautner; nem no kernel.

   *Conserto pedido:* Registrar na docstring que ha rota pelo Mathlib e que a prova direta foi mantida por evitar a passagem ao espaco real.

9. **(BAIXO)** l.668-669, l.685-694, l.822-829, l.867-870, l.1003-1009

   Gordura: pelo menos nove declaracoes sao aliases rfl ou uma linha (o_boost_na_luz_age_como_VF, a_translacao_mais_age_como_UF, a_translacao_menos_age_como_UF, a_direcao_nula_do_contrato_e_a_da_cunha_fisica, o_subespaco_da_cunha_do_fluxo_e_o_do_separador, a_algebra_do_par_de_tomita_e_a_da_cunha, o_vacuo_separa_a_algebra_da_cunha, as duas especializacoes de esperanca). As 58 declaracoes superestimam a musculatura; o conteudo proprio e da ordem de 25.

   *Conserto pedido:* Manter so as pontes que o proximo teorema consome; as demais viram docstring ou saem; declarar no cabecalho quantas sao ponte.

10. **(BAIXO)** l.649-665

   O LEMA QUE FALTAVA (l.649) exagera: o kernel tem a versao 2x2 (BisognanoWichmann.lean:105, boost_null_contract, reexportada em Santo.lean:1200). O que faltava e a forma 4D com wedgeBoostMap e nullMinus (F1Fecho394/PhysicalWedgeNullGeometryR3.lean:14); grep -r no kernel inteiro nao a acha.

   *Conserto pedido:* Docstring: a forma 4D do contrato do raio nulo passado; a 2x2 e boost_null_contract.

11. **(BAIXO)** l.20

   set_option maxHeartbeats 4000000 (20 vezes o padrao) no topo: nao medi se e necessario; a compilacao levou 39 a 63 s.

   *Conserto pedido:* Medir com o valor padrao ou com um valor menor e deixar so o necessario, ou justificar no cabecalho.

## Terceira conferencia: o texto da R2

**Veredito:** APROVADO_COM_RESSALVAS

**Recompilou:** {"rc": 0, "avisos": 0, "declaracoes_no_trio": 51, "sha16": "d82674444fe29c06"}

Recompilei a R2 (sha16 d82674444fe29c06): RC 0, 0 avisos, 51 declaracoes, as 51 so com propext, Classical.choice e Quot.sound, sem sorryAx. Todos os 12 nomes do kernel do cabecalho existem e dizem o que o cabecalho diz (conferi com #check e #print axioms, tudo no trio); um tem o qualificador errado. physicalFockCertificate e def de tipo FockCertificate sobre a rede fisica, no trio, importado em TGLExt.lean e no selo (fechamento_v406). A frase central (ergodicidade da cunha da luz livre ja e teorema do kernel, sem condicao) e verdadeira; a_ergodicidade_na_luz_e_do_kernel e so mudanca de forma (hipoteses equivalentes, mesma conclusao). wedge_nonabelian e campo de FockCertificate e a docstring bate. Errata (item 5): REVISAO_K05_T1 diz AUSENTE e L3 diz condicional a certificado nao habitado, ambos confirmados. T1 no papel (item 3) bate com L1/K05/REVISAO. Teste de dimensao finita (item 6) compila RC 0 e o enunciado e o do cabecalho. Regua (item 7): zero aspa angular, zero confirm, zero poder, zero fala do operador; so natureza e gate na linha 104, em negacao. Nenhum ALTO. Ressalvas: (a) a ordem de 13/11 nao diz frente B nem o que o Artigo chama de T1, rotulos da gerencia postos como se fossem da ordem; (b) a linha 717-718 (so nullDir de 8.4 em diante) e contrariada pelo codigo e pela docstring do 8.5; (c) o cabecalho diz que o kernel tem as medias para o grupo de boosts e nao tem; (d) a lista do que nao afirma esquece a condicao espectral e BW nas secoes 1 a 4; (e) aperiodicExpectationInput com qualificador que nao resolve.

### Achados

1. **(MEDIO)** linhas 20-23 (De onde vem, item 1)

   O cabecalho diz que a ordem do operador de 13/11 poe na frente B o que o Artigo chama de T1. Nos bytes (886 B, sha16 4698446c391f9aba) o operador escreve: restam T1 (ergodicidade em III1 genuina, os dois lemas padrao de redacao: dominio multiplicativo e convergencia no predual), a montagem 3+1, a extensao GH e a derivacao de tau-estrela. Nao ha a palavra frente, nem poe nada na frente de nada, nem diz que T1 e o do Artigo; frente B e rotulo do DESENHO_v412_R0 da gerencia, e a identificacao com a T1 do Artigo (tex l.1571) e leitura da gerencia. O padrao dos dois lemas tambem some.

   *Conserto pedido:* Trocar por: a ordem da v412 (13/11/2026; bytes em ...) lista T1 entre o que resta, com os dois lemas padrao de redacao (dominio multiplicativo e convergencia no predual); a gerencia a organiza como frente B (DESENHO_v412_R0) e a identifica com a T1 de mesmo nome no Artigo.

2. **(MEDIO)** linhas 717-718 (docstring da secao 8); eco nas linhas 95-98

   Diz: de 8.4 em diante so a translacao ao longo de nullDir e usada; a de nullMinus serve a 8.3. Falso no codigo: os teoremas de 8.5 de um so boost (o_que_comuta_com_um_so_boost_da_luz_e_escalar, linhas 997-1023, e a_media_de_um_so_boost_da_luz_converge_ao_vacuo, linhas 1028-1051) passam translacaoNulaMenos e as lemmas a_translacao_menos_* como a translacao que encolhe quando s0 > 0; a docstring do proprio 8.5 (linhas 994-996) diz que, conforme o sinal de s0, a que encolhe e a de nullDir ou a de nullMinus. O que vale: o vacuo unico so e pedido (hvac) para nullDir. Na linha 95-98 a frase e so ambigua (so ela se refere ao vacuo unico).

   *Conserto pedido:* Linha 717-718: de 8.4 em diante o vacuo unico e pedido so para a translacao ao longo de nullDir (light_null_ergodic); a de nullMinus entra em 8.3 e, como a translacao que encolhe quando s0 > 0, nos teoremas de um so boost de 8.5.

3. **(MEDIO)** linhas 47-50 (O que a pedra acrescenta, item 3)

   Apos listar tres resultados do boost isolado (so o vacuo e fixo; o que comuta e escalar; as medias convergem a projecao sobre a reta do vacuo), diz: o kernel tem isto para o GRUPO inteiro de boosts. So os dois primeiros estao no kernel (o_um_e_o_unico_fixo_da_luz; centralizer_is_trivial). Medias na luz nao: grep recursivo por birkhoffAverage no kernel devolve so TheSingularityReadsTheAttractorAdendo1 (A1_cesaro, generico, com o espaco fixo nao identificado). Alem disso, e aqui que Mautner e necessario e mais forte que o provado: so se prova que e usado.

   *Conserto pedido:* O kernel tem os dois primeiros para o GRUPO inteiro de boosts; para um boost isolado, nao; as medias de um boost da luz nao estao no kernel (so A1_cesaro, generico). E aqui que Mautner e usado.

4. **(MEDIO)** linha 67-68 (O que NAO e novo, ultimo item)

   O nome AperiodicCentralizerExpectation.aperiodicExpectationInput nao resolve: #check devolve Unknown identifier. O prefixo escrito e o do ARQUIVO (TGLExt/AperiodicCentralizerExpectation.lean); o namespace real e ChatgptAudit.Aperiodic046. Os outros nomes do cabecalho usam a ponta do namespace (LightRhoStar, OUmInscrito, ContratoH2), este usa o arquivo. A declaracao existe, tem o tipo (P : SiteProfile) -> ExpectationInput P, esta no trio e a esperanca cai no omegaCentralizer por limite de medias de Cesaro do fluxo modular, como o cabecalho diz.

   *Conserto pedido:* Escrever ChatgptAudit.Aperiodic046.aperiodicExpectationInput (em AperiodicCentralizerExpectation.lean).

5. **(MEDIO)** linhas 84-104 (O que a pedra NAO afirma); linha 78

   A lista nao diz tres coisas que o enunciado deixa de fora. (1) A condicao espectral (V+ com p0 = 0 so em 0), que na proposicao da cunha do papel leva a invariancia pelas duas translacoes nulas ao grupo todo, nao e formalizada: a hipotese nomeada de vacuo unico das secoes 3 e 4 (fixo pelas duas translacoes nulas e multiplo de Omega) a absorve (o revisor de L1/P2 ja disse que Vac esconde a condicao espectral e a direcao transversal). (2) Nas secoes 1 a 4 delta e um boost abstrato: nao e identificado com Delta^{it} (BW); na luz isso vem do campo flow_is_Ad do certificado. (3) A secao 5 toma a desigualdade de Schwarz como hipotese (hS) e nao a deriva de 2-positividade nem de unitalidade, e nao ha mapa gaussiano normal. Sem isso, a linha 78 (secoes 1 a 3 e 8 sao a face de kernel da proposicao da cunha) pode ser lida como a proposicao inteira.

   *Conserto pedido:* Acrescentar: Nao formaliza a condicao espectral nem BW nas secoes 1 a 4 (o vacuo unico nomeado e o delta abstrato as absorvem); nao deriva Schwarz de 2-positividade (a secao 5 a toma como hipotese).

6. **(BAIXO)** linhas 58-60 e 727; arquivo kernel F1Fecho394/CanonicalFockModularCoreInputR1.lean

   physicalFockCertificate e def (tipo FockCertificate physicalCanonicalNet.toLightOneParticle), trio, importado em TGLExt.lean l.1131, olean de 02/11, e o selo diz fechamento_v406.certificate_inhabited = true; CanonicalFullTGLWitnessR1 diz: F1.FECHO 16/10/2026, recompilado no sandbox em 02/11/2026. Mas o cabecalho do proprio arquivo ainda diz DECLARADO / UNCOMPILED CANDIDATE, R52, 2026-10-16, texto de quando era candidata, e a pedra nao da data nem fonte. As ressalvas herdadas do certificado (R10: nao trivialidade so na cunha; nucleo II_inf como [KNOWN]; traco ENNReal ciclico) tambem nao aparecem junto de sem condicao.

   *Conserto pedido:* Acrescentar: habitado desde a v406 (selo, fechamento_v406; entregue pela bancada em 16/10/2026, recompilado em 02/11/2026); o cabecalho do arquivo ainda leva o texto de candidata. As ressalvas de nao trivialidade so na cunha herdam-se do certificado.

7. **(BAIXO)** linhas 25-27 (De onde vem, item 2)

   Diz que a caixa vale para ESTADO normal fiel. A caixa da K05 como escrita (T1_FECHADO l.22, l.238) diz peso, e a conferencia (REVISAO_K05_T1, R1, erro material) a corrigiu para estado normal fiel com phi(1) finito; sem estado nao ha E_tau. O cabecalho nao diz que o Kimi escreveu outra coisa.

   *Conserto pedido:* Acrescentar: a K05 escreveu peso; a conferencia corrigiu para estado normal fiel (R1).

8. **(BAIXO)** linhas 32-35 (De onde vem, item 3)

   A ordem K07 de 14/11 08:03 e da gerencia para o Kimi (item 2d: escrever a candidata Lean de Mautner e levantar a fiacao). O levantamento de 15/11 em LEVANTAMENTO_FRENTE_B_15nov e dos leitores da gerencia, e esta pedra e da gerencia, nao uma entrega do Kimi. A sequencia de frases deixa entender que a K07 gerou este levantamento e esta candidata.

   *Conserto pedido:* Dizer: a K07 pediu isto ao Kimi; a gerencia levantou a fiacao em 15/11 e escreveu esta candidata.

9. **(BAIXO)** linhas 65-66 e 876

   A algebra M como a cunha direita fisica e dada como physical_right_wedge_eq_KWR. O teorema do kernel e sobre subespacos reais (localized physicalRightWedge = KWR); a igualdade das algebras e uma reescrita (rw) mais definicao. Mesmo caso: a docstring do 8.4 diz E physical_right_wedge_eq_KWR.

   *Conserto pedido:* Trocar e por segue de.

10. **(BAIXO)** linha 108 (Estatutos)

   Choi 1974 e Mautner e Moore marcados [KNOWN]. L1 A6 e a conferencia (R4) dizem Choi nao conferido no primario (o PDF era pagina Incapsula, so metadados Crossref; Corollary 2.8 e Schwarz, nao a implicacao unilateral); Mautner/Moore so por Morinelli-Neeb.

   *Conserto pedido:* Marcar [KNOWN, citado, nao conferido no primario] para Choi 1974 e para Mautner e Moore.

11. **(BAIXO)** linhas 99-101

   Diz que em dimensao finita as secoes 2 a 4 sao vazias. O teste (V_B1_a/TesteDimFinita.lean, RC 0, trio) prova T a v = v sob as hipoteses de covariancia da forma de uma so dilatacao, o que torna as translacoes triviais; com vacuo unico a secao 3 forca dim H = 1. O enunciado confere, mas vazias e mais forte que triviais.

   *Conserto pedido:* Trocar vazias por triviais (as translacoes sao a identidade).

