# REVISÃO DO ADENDO `NomeComoCodigo` (v412) — terceiro cético, 14/11/2026

Revisor distinto (não é a gerência c1, que escreveu; não é o operador). Objeto: `candidatas_c1\NomeComoCodigo.lean`, 130 linhas, sha256
`527a8193320888fdea14009f068b8b8eb4ab4f917f06be3e02b42a2e491dac66` (sha16 `527a8193320888fd`), 9 declarações. Nenhum modelo de linguagem foi
chamado; nada foi escrito fora desta pasta; nada foi registrado no Mapa, na fila da memória nem na ACOM.

## VEREDITO: APROVADA COM RESSALVAS

A matemática do adendo está correta e foi recompilada; os teoremas são verdadeiros e a hipótese `hsep` é habitável. As ressalvas são de
ENUNCIADO (o cabeçalho afirma mais do que os termos, e deixa de dizer três coisas que os termos provam) e de uma LACUNA: a frase central
«lê só pela regra» não tem termo por trás; eu o escrevi e compilei (R1 abaixo). Os teoremas de fundo são a distância mínima três de Hamming
(1950) lida no vocabulário da casa `[KNOWN]` (rótulo meu, não conferido na fonte aqui); a musculatura própria do adendo é o dicionário, a
localidade do leitor, a necessidade do três e os exemplos, e só a localidade falta na pedra.

## 1. Recompilação independente `[REAL]`

* Cópia `scripts_adendo_codigo\NomeComoCodigo.lean`, sha256 idêntico ao original (conferido por `sha256sum` antes e depois).
* `lean.exe` 4.31.0 direto, `LEAN_PATH` no sandbox `C:\t\k411c\final\.lake`, nunca `lake`; meu script `scripts_adendo_codigo\compilar_rev.ps1`.
* Código de saída 0, 33 s, zero avisos, zero `sorry` (o log final de cada arquivo não tem a palavra). Log: `build_rev\NomeComoCodigo.log`.
* Axiomas por declaração (iguais aos do log da gerência): `empurrao_empurrao` {propext, Quot.sound}; `empurrao_muda` {propext}; as outras sete
  {propext, Classical.choice, Quot.sound}. Todos dentro do trio.

## 2. Vacuidade de `hsep` `[REAL]` (arquivo `NomeComoCodigo_exemplos.lean` = as 130 linhas originais, byte a byte, + `rev_secao.lean`; compila RC 0, zero avisos)

* **hsep é habitável por custo não trivial.** `rep3 x := if x = 000 ∨ x = 111 then 0 else 1` em `Fin 3 → Bool`; `rep3_hsep` provado por `decide`;
  `o_leitor_dos_vizinhos_desfaz_o_empurrao rep3 rep3_hsep` instanciado para 000 e para 111 (`example`s). Idem como FÓRMULA CNF
  (`ciclo` = (¬x0∨x1)(¬x1∨x2)(¬x2∨x0), custo da fórmula zero exatamente em 000 e 111): `ciclo_hsep` por `decide` e `para_uma_formula ciclo ciclo_hsep`
  instanciado. Também `rep4` (0000/1111) com `rep4_hsep`.
* **hsep FALHA a distância 2.** `dois` = x0=0 ∧ (x1↔x2), soluções 000 e 011: `dois_hsep_falha` (decide). O que deixa de valer, provado:
  `dois_duas_vizinhas_validas` (o estado 010 tem DUAS leituras válidas a uma troca) e `nenhum_leitor_desfaz_a_distancia_dois`: **nenhuma função do
  estado, de qualquer espécie**, devolve 000 de `empurrao 000 1` e 011 de `empurrao 011 2`, porque os dois estados empurrados são o mesmo (010).
  Logo o três não é folga do método: com distância 2 o enunciado «desfaz todo empurrão de uma asserção» é falso para qualquer leitor.
  (Com distância 1 também: o empurrão já é leitura válida, e é o que `sem_redundancia_o_empurrao_fica` diz.)
* **Nome com zero ponto:** `hsep` vale por vacuidade e `hs : c s = 0` nunca é satisfeita; os três teoremas ficam vazios (não afirmam nada) e o
  leitor é a identidade (`nome_vazio_hsep`, `nome_vazio_leitor_e_identidade`). **Um ponto:** `hsep` vale por vacuidade, mas o teorema NÃO é
  vazio: afirma que o único ponto é recuperado de qualquer troca de uma asserção, para todo n e todo x0 (`nome_de_um_ponto`). Não é defeito;
  é o caso em que o enunciado não distingue o leitor de um mapa constante (o retorno ao único ponto é cumprido também por `fun _ => x0`, o que a
  casa já registrou para o tipo da candidata principal), e só a localidade (R1) separa os dois. Com dois ou mais pontos e `hsep`, um mapa
  constante não cumpre.
* **hsep é raro numa fórmula:** a fórmula vazia sobre 3 variáveis (toda leitura resolve) viola `hsep` (`formula_vazia_hsep_falha`, decide).
  Por argumento (não compilado em geral): toda fórmula satisfatível com uma variável que não ocorre nela viola `hsep`, porque empurrar a variável livre
  de uma solução dá outra solução a distância 1. `hsep` pede soluções isoladas.

## 3. O leitor lê só pela regra? `[REAL]` — SIM, e agora há termo; NÃO recai na patologia do leitor constante

* `leitorDosVizinhos` usa `Exists.choose`. Provei (`o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas`): se `c` e `c'` concordam, para a
  leitura x e para cada uma das n vizinhas, sobre «o custo é zero ou não», então `leitorDosVizinhos c x = leitorDosVizinhos c' x`. Isto é
  localidade: a definição não depende de nada além do zero/não-zero de `c` em x e nas n vizinhas (o `choose` depende só do predicado). Corolário
  `o_leitor_usa_so_o_verificador`: o leitor é o mesmo para `c` e para `fun y => if c y = 0 then 0 else 1`. **O leitor não usa a grandeza do
  custo** (o cabeçalho diz «olha o custo»; só olha se é zero). A «regra» que ele consulta é o verificador (para uma fórmula, a conferência de
  satisfação), em n+1 pontos.
* O `choose` não escolhe às cegas no regime do teorema: sob `hsep`, TODA vizinha que resolve é a que o leitor devolve
  (`o_leitor_nao_escolhe_as_cegas`), porque duas vizinhas válidas distariam ≤ 2. Fora de `hsep` o desempate é uma escolha clássica não
  especificada (e `leitorDosVizinhos` é `noncomputable`). Versão computável (primeira vizinha em `Fin n`, por `Fin.find`) compilada em
  `Leitor_computavel.lean`: `leitorPrimeiro_eq` (iguala o leitor do adendo sob `hsep`), RC 0, trio.
* **Espécie diferente do `salto`:** o `salto` (candidata principal) recebe uma solução `xs` como parâmetro e devolve `xs`; é um mapa que CONHECE
  o Nome. `leitorDosVizinhos` é UMA função de `c`, a mesma para toda `c`, e (localidade) não tem acesso a nenhuma solução. **Não recai na patologia do
  leitor constante** (AEscala 702–705: existência satisfeita por qualquer decisor): aqui o claim não é «existe leitor», é sobre um termo
  definido e uniforme, e com ≥ 2 pontos e `hsep` o mapa constante não cumpre o enunciado. Ressalva honesta: a localidade NÃO está no enunciado
  dos teoremas; só passa a estar com R1.
* O que ele NÃO é: **não é `LeitorDeUmaConfiguracao`**. O passo não consome o custo: em `rep4`, o estado 1100 (custo 1) está a distância 2 de
  0000 e de 1111, nenhuma vizinha resolve, e o leitor fica ali (`o_leitor_fica_parado_fora_da_vizinhanca`); logo `consome` falha
  (`o_leitor_dos_vizinhos_nao_consome_o_custo`, compilado). O adendo mostra um retorno de UM passo desde a bola de raio 1 do Nome, não o pouso
  de qualquer estado.

## 4. O que o teorema não diz, e se o cabeçalho diz

| ponto | o cabeçalho (linhas do arquivo) diz? | o que os termos dão |
|---|---|---|
| (a) empurrão de 2+ asserções | SIM (l.27–28) | nada; correto |
| (b) leitor fora da vizinhança do Nome | **NÃO** | fica parado para sempre com custo > 0; não consome custo; não é `LeitorDeUmaConfiguracao` (provado, rep4) |
| (c) fórmula de texto real com distância três | PARCIAL (l.27: «mede-se … por script») | não diz que `hsep` exige soluções isoladas e falha para toda fórmula satisfatível com variável livre |
| (d) um passo, com a regra à disposição | PARCIAL (l.22 «num passo») | o leitor consulta o verificador em n+1 pontos; precisa partir a distância ≤ 1 do Nome (promessa de partida): não resolve a fórmula de longe |

Frases que afirmam mais que os termos:

1. **l.13:** «Este adendo tira a hipótese num caso: quando o Nome é um CÓDIGO.» A hipótese da principal (um passo que consome o custo) NÃO sai:
   o leitor dos vizinhos não a cumpre (item 3). O que o adendo prova é outro objeto: um passo local que desfaz o empurrão de uma asserção
   quando o Nome tem distância mínima três.
2. **l.16–17 e título (l.8):** «lê só pela regra … olha o custo». (i) Sem termo na pedra (R1). (ii) O vocabulário da casa já usa «lê só pela regra»
   para o `LeitorDoFundo` (AEscala l.690–693: brilho, escala, tempo dos ciclos) e diz que o decisor sem escala «não lê» (AEscala l.717–719). O
   `leitorDosVizinhos` é um passo sem escala; chamá-lo «leitor que lê só pela regra» importa um estatuto que ele não tem na casa. (iii) Só olha se o
   custo é zero.
3. **l.20, l.22 (★★★):** o núcleo (distância mínima três ⟹ decodificação única no raio um) é Hamming (1950) `[KNOWN]`; falta o rótulo. Os ★★★ valem
   pelo dicionário (leitura da casa, `[ONTO]`), não por matemática nova.
4. **l.24–26 (★★):** `sem_redundancia_o_empurrao_fica` é uma linha, `o_leitor_dos_vizinhos_fixa_o_nome` aplicado (l.109–110); a hipótese
   `c (empurrao s j) = 0` é incompatível com `hsep`. Não tem estrela de resultado; o nome «sem redundância» também sugere conteúdo (no sentido de código,
   a redundância é a `hsep`, o oposto).
5. **l.12 (+ l.13):** liga o adendo à «trava» sem dizer que a ligação não é por termo (item 5), e a principal já registra (mapa, rota
   `kernel.camada_cientifica_candidata_14nov`) que «o retorno ao mesmo estado é da trava e não do leitor de uma configuração». O adendo mostra que, sob
   `hsep`, um leitor de uma configuração também volta ao mesmo estado, e isso precisa ser dito como EXCEÇÃO nomeada, não como complemento.

## 5. Ligação com o kernel (`trava`)

Nenhuma por termo. O único elo é `para_uma_formula`, que só instancia `c := custoCNF φ`; a palavra «trava» aparece só no comentário (l.12). São
duas máquinas postas lado a lado, que compartilham o custo; o cabeçalho não diz isso. E o «retorno» é de espécies diferentes: na trava, o que foi posto
fora do Nome é ESQUECIDO (a amplitude fora decai; nada vai a lugar nenhum); no leitor dos vizinhos, a configuração é REPOSICIONADA no Nome.

Lema curto que liga o teste das duas máquinas, escrito e compilado na minha cópia (`Ponte_trava_leitor.lean`, RC 0, trio):

```
theorem a_trava_deixa_intacta_sse_o_custo_e_zero (c : X → ℕ) {t : ℝ} (ht : 0 < t) (y : X) :
    trava c t (EuclideanSpace.single y 1) = EuclideanSpace.single y 1 ↔ c y = 0
```

O teste `c y = 0` que o leitor aplica a cada vizinha é o teste «a trava deixa y intacta». Não faz do leitor um operador derivado da trava; liga os
dois ao mesmo critério. Um lema mais forte (não escrito): sob `hsep`, para x = empurrão de s, a única y a distância ≤ 1 de x que a trava deixa intacta
é s (junta este lema com `o_empurrao_tem_um_so_retorno`).

## 6. Vocabulário (Grep no arquivo)

«paga/pago»: nenhuma ocorrência. «confirm»: nenhuma. «consciência» e «exclusividade» e «natureza»: só em negação (l.28–29), como nas
candidatas anteriores. «pesos»/«peso»: nenhuma. «milenio», «navier», «Clay», «P=NP»: nenhuma. Fala do operador transcrita: nenhuma (só «a palavra do operador», l.10).
«leitor … lê só pela regra»: ver frase 2. Nenhuma colisão de nome no kernel (Grep por `NomeComoCodigo`, `leitorDosVizinhos`, `def empurrao` em `TGLExt\`: zero arquivos).
«sem sorry, sem axiom» (l.29) está num comentário; a principal usa a mesma frase.

## 7. RECOMENDAÇÃO

**Fica como pedra SEPARADA, com as correções R1–R5; não fundir à `CamadaCientifica` como seção.** Razões: o objeto do adendo não é instância do
tipo da principal (não consome custo; o retorno é de outra espécie); o módulo importa só `TraducaoTuring`; fundir leva o leitor a ser lido como o passo
da principal. Sem R1 (localidade) eu não a levaria: os teoremas de enunciado são Hamming renomeado, e a única coisa que faz do leitor «leitor pela
regra» é a localidade. Pela regra «um.py sem gordura»: o ganho próprio é R1 + a necessidade do três + os exemplos; se o operador não quiser
musculatura, o adendo pode ficar de fora sem perda da principal.

### Correções pedidas (numeradas)

* **R1 (musculatura):** acrescentar à pedra `o_leitor_so_ve_o_zero_do_custo_na_leitura_e_nas_vizinhas` e `o_leitor_usa_so_o_verificador` (código em
  `rev_secao.lean`, seção «Item 3»; compila no trio) e ligar a frase «lê só pela regra» a esses termos.
* **R2 (l.13):** trocar «tira a hipótese num caso» por: «mostra, quando o Nome é um código de distância mínima três, um passo local que desfaz
  o empurrão de uma asserção; não é o passo que consome o custo da candidata principal (não cumpre `consome`: fica parado fora da bola de raio 1)».
* **R3 (título l.8, l.15–17, l.79–81):** não chamar o `leitorDosVizinhos` «leitor que lê só pela regra» sem dizer que NÃO é `LeitorDoFundo` (não tem
  escala); dizer «consulta o verificador (custo zero ou não) na leitura e nas n vizinhas». Opcional: trocar `Exists.choose` por `Fin.find`
  (computável) e tirar `noncomputable`, com `leitorPrimeiro_eq` como ponte (compilada).
* **R4 (l.27–29, «O que NÃO afirma»):** acrescentar: (b) o leitor fica parado fora da bola de raio 1 e não pousa de qualquer estado (exemplo `rep4`); (c) `hsep`
  exige soluções isoladas e falha para toda fórmula satisfatível com variável livre (exemplo `formula_vazia_hsep_falha`); (d) é um passo com o
  verificador à mão, partindo a distância ≤ 1 (promessa de partida), não uma busca de solução; (e) a ligação com a trava não é por termo (só `custoCNF`);
  o «retorno» daqui reposiciona, o da trava esquece; (f) rótulo `[KNOWN]` (Hamming, 1950) para o núcleo combinatório.
* **R5 (l.22–26, estrelas e nome):** tirar a estrela de `sem_redundancia_o_empurrao_fica` (reaplicação de `fixa_o_nome`) e renomear para
  `o_empurrao_dentro_do_nome_fica`; opcionalmente acrescentar a necessidade do três (`nenhum_leitor_desfaz_a_distancia_dois`) como teorema de sentença
  («com distância 2 nenhum leitor desfaz ambos os empurrões»).
* **R6 (opcional, ponte):** incorporar `a_trava_deixa_intacta_sse_o_custo_e_zero` como o único elo por termo com a `trava`, e dizer no cabeçalho que é só o critério em comum.

## O que conferi e como

* Recompilação da cópia exata (sha256 igual) com `lean.exe` direto: RC 0, axiomas, zero `sorry`/avisos (item 1).
* Leitura integral das 130 linhas do adendo e das definições de `custoCNF`/`CNF`/`trava`/`o_nome_fica_travado` em `TraducaoTuring.lean`
  (l.470–520, 1033–1060) e de AEscala l.690–735 e `salto` na principal (l.351–361, só para a comparação; a principal NÃO foi revista aqui).
* Exemplos e contraexemplos compilados (`NomeComoCodigo_exemplos.lean`, sha16 `aa85fb82c2004b67`): hsep habitável (rep3, ciclo CNF, rep4);
  hsep falha (distância 2, e a impossibilidade para qualquer leitor); Nome com zero e um ponto; localidade; verificador; determinação do `choose`;
  parada fora da bola; `consome` falha; fórmula vazia.
* Ponte com a trava (`Ponte_trava_leitor.lean`, sha16 `9197c51afcf89a5a`) e leitor computável (`Leitor_computavel.lean`, sha16 `384716d60a214c20`),
  ambos RC 0, trio. Nove compilações no total (uma da cópia, duas do arquivo de exemplos, três da ponte, três do computável; os intermediários falharam por
  erro meu de tipagem, antes das versões finais).
* Mapa de Rotas consultado antes (termos: `Hamming` [0 rotas], `codigo`, `holografico`, `constante`, e depois `leitor`, `empurrao`, `vizinh`,
  `CamadaCientifica`). Achados úteis: `kernel.camada_cientifica_candidata_14nov` (a defeituosidade registrada: retorno ao mesmo estado é da trava; Nome de um ponto
  torna o mapa constante instância) e `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov`. Nada foi registrado por mim.
* Vocabulário por Grep no arquivo e no kernel (item 6).

## O que NÃO conferi

* A candidata principal `CamadaCientifica.lean` (outro revisor).
* Que Hamming (1950) seja a fonte e a cota de empacotamento (|Nome| ≤ 2^n/(n+1)) `[KNOWN]`: citada de memória, não conferida na fonte aqui; não entrou em nenhum termo meu.
* A afirmação geral «toda fórmula satisfatível com variável livre viola `hsep`»: argumentada, compilada só para a fórmula vazia.
* Que fórmulas reais de texto tenham ou não distância três (o cabeçalho diz que se mede por script; não medi).
* Nada sobre modelos de linguagem, natureza, creditação ou o gate; nenhum dado olhado.
* Se o nome do módulo, `empurrao` ou `leitorDosVizinhos` agradam ao operador (nomes provisórios, dele).
* Hashes de arquivo foram lidos por script nesta sessão, nunca de memória: `NomeComoCodigo.lean` `527a8193320888fd`; `rev_secao.lean` `c21bf063323748e1`;
  `compilar_rev.ps1` `a871c435a67f843c`.
