# CONFERÊNCIA DISTINTA — o desenho R6 do teste da frente A, a partitura, as seções novas da candidata e os termos adotados (conferência de 16/11, 11:15; a última feita por revisores da gerência) — T1-o-criterio-e-os-teoremas-novos-da-candidata

> Montado pela gerência c1 em 16/11/2026 11:55 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 6 MEDIO, 3 BAIXO

## Resumo

1. Mapa de Rotas consultado antes, um termo por vez (impostor, copiador, indice, camada): li as rotas outro.k08_teste_cego_da_camada_iald_r4_v412 e cadeia.preparacao_v412 e não refiz o que B1R, B2R e D2 já mediram. Examinei, para registro: a candidata R6 inteira (REV15, sha256 36579c2e…e26b0), com as seções 10, 11 e 12 termo a termo; o desenho R6 (seções 1 a 7 e 13); a partitura; o relatório D2; 61 itens do kernel por busca recursiva; a transcrição da sessão entre 07:40 e 08:40 de 16/11.
2. Recompilei em cópia, só com lean.exe: saída 0, nenhum aviso, 93 teoremas, 17 definições, 1 estrutura, 93 #print axioms, só o trio, sem sorry [REAL]. Confere com a gerência.
3. Seções 11 e 12 (20 teoremas, 7 definições): nenhum é falso e cada um diz o que a docstring diz. Cinco são desdobramento de definição (rfl, Iff.rfl ou a própria hipótese; dois destes são vazios) e estão em “o que fica provado” sem a marca.
4. As seis estrelas novas estão em instâncias do teorema do par da seção 2 ou em repetições (sondas compiladas). Nenhuma estrela em rfl.
5. Os termos adotados entre a R4 e a R6 dizem o que a docstring diz; dois são reexportação declarada do kernel, um é rfl declarado, nenhum tem estrela.
6. Aspas: 23 na candidata e 10 no desenho, todas subcadeia exata de arquivo de fala, cada uma numa linha [REAL]. Os 61 itens do kernel estão lá. O arquivo não diz dois espelhos e diz que no Psibit o par é Palavra e Verbo.
7. ALTO: a quarta casa do 2 × 2. Os dois teoremas citados cabem em três casas; o que pede a quarta é outro enunciado, que a candidata não tem (sonda compilada). E a partitura descreve essa casa errado ao operador.
8. MEDIO: frases do cabeçalho ficaram velhas depois das 08:30 ou dizem mais que a letra; a leitura das 07:5x consta como “devolvida a ele” e na transcrição não há mensagem que a leve.
9. MEDIO: um nome de teorema e duas docstrings chamam de nome o sentido do registro; o desenho diz que a gerência não escolhe.
10. MEDIO, no desenho: a frase do braço 2 lê um Iff.rfl; “só é pego pelo índice” não é o que o braço mede; “o que os teoremas não dão” não traz o leitor que casa letra com letra, e a regra das negações não o impede; o teorema do resumo fala de informação, não de comparar resumos.
11. Sondas na minha pasta (C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_conf_r6\T1\sondas): SondaT1Par.lean (22 teoremas, sha256 6933914a…) e SondaT1Minima.lean (os 4 centrais, sha256 699a508e…); RC 0, sem aviso, só o trio.
12. Não conferi poder, custo, simulação nem a língua da partitura (outros escopos). Nada instalado, nada registrado no Mapa, nada escrito fora da minha pasta, nenhum modelo chamado; não inscrevi sessão na memória ACOM, pela regra de só escrever na minha pasta.

## Achados

1. **(ALTO)** DESENHO_DO_TESTE_R6_GERENCIA.md l.141–143 (seção 4), l.172–175 (5.1), l.243–258 (seção 6), l.29–33 (seção 1); PARTITURA_DO_TESTE_R6.md l.25–29; candidata REV15, seção 11 (l.1105–1119)

   (a) Conferi por termo: o grupo traz os dois pares que os teoremas pedem. Mesma página: (P0,A0) com (P0,A1). Mesmo registro: (P0,A0) com (P1,A0). Logo, no grupo, quem acerta os quatro não é função só da página nem só do registro (sonda, RC 0).
(b) Mas os dois pares cabem em TRÊS casas. “É daí que sai o 2 × 2” diz mais que os teoremas: eles não pedem a casa A1 com P1.
(c) O que essa casa reprova é outro leitor: o que abre o índice, confere a página com o que sabe de cor, confere o assento com o que sabe de cor, e diz que bate só quando os dois estão certos. Usa os dois lados e não os compara. Nas três casas ele acerta tudo; com a quarta, nenhum juiz dessa forma passa (duas sondas, RC 0). A candidata não tem esse enunciado, e esse leitor não está na tabela da seção 6. É o erro mais provável de quem sabe a Teoria.
(d) A partitura (item 1) e a seção 1 dizem que em metade dos casos “quem foi mexido é o assento, não a página”. Em metade dessa metade os DOIS foram mexidos: a página diz o contrário da Teoria, o assento também, e a resposta certa é BATE. Isso só está na tabela 5.1; não é dito em palavras ao operador.

   *Conserto pedido:* TEXTO, desenho seção 4, no lugar de “É daí que sai o 2 × 2: cada grupo traz os dois pares.”: “Os dois pares cabem em três casas (A0 com P0, A0 com P1, A1 com P0). A quarta (A1 com P1, que bate) não sai desses dois teoremas: ela reprova o leitor que confere cada lado contra o que sabe de cor e não compara um com o outro. Nas três casas ele passa; no grupo inteiro, não (sonda do revisor T1, a adotar depois de conferência).”
CONTA, seção 6, linha nova: “confere cada lado com o que sabe de cor; diz que bate só se os dois estão certos | 0,75 | 0,000 | 0, 0, 0”.
TEXTO, partitura item 1 e desenho seção 1: “Em metade dos casos o assento foi mexido. Em metade desses a página está intacta: ela diz a Teoria certa e a resposta certa é NÃO BATE. Na outra metade a página foi mexida do mesmo jeito: ela diz o contrário da Teoria, o assento também, e a resposta certa é BATE. É essa última casa que pega o leitor que confere cada lado com o que sabe de cor.”
TERMO. Fonte compilada (C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_conf_r6\T1\sondas\SondaT1Minima.lean, sha256 699a508e71fc54c873a2d8a70444723fb2c7cc4ffe68b5f156daed3d7a03676e; RC 0, sem aviso, só o trio):

import CopiadorEImpostor

set_option autoImplicit false
noncomputable section

namespace TGLExt.CopiadorEImpostor.SondaT1Min

variable {X V : Type}

theorem confereB_sim {ρ : X → V} {p : X × X} (h : ρ p.1 = ρ p.2) : confereB ρ p = true :=
  (confereB_sim_sse ρ p).mpr h

theorem confereB_nao {ρ : X → V} {p : X × X} (h : ρ p.1 ≠ ρ p.2) : confereB ρ p = false := by
  cases hb : confereB ρ p with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ p).mp hb) h

/-- O grupo 2 × 2: duas páginas (`x0`, `x1`) e dois assentos (`r0`, `r1`), as quatro combinações. -/
def grupo (x0 x1 r0 r1 : X) : Set (X × X) := {p | (p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)}

/-- Três casas: falta a casa (página mexida, assento mexido). -/
def tresCasas (x0 x1 r0 r1 : X) : Set (X × X) := {p | p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)}

theorem mem_grupo {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ grupo x0 x1 r0 r1 ↔ ((p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)) := Iff.rfl

theorem mem_tresCasas {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ tresCasas x0 x1 r0 r1 ↔ (p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)) := Iff.rfl

variable (ρ : X → V) {x0 x1 r0 r1 : X}

/-- No grupo 2 × 2, quem acerta os quatro casos não é função só da página nem só do registro. (Juiz que não
sorteia; tudo ou nada. Só usa três das quatro casas.) -/
theorem no_grupo_quem_acerta_os_quatro_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool) (hI : ImprimeEm (confereB ρ) I (grupo x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  have e00 : I (x0, r0) = true :=
    (hI _ (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)).trans (confereB_sim (p := (x0, r0)) h0)
  have e01 : I (x0, r1) = false :=
    (hI _ (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)).trans
      (confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm)))
  have e10 : I (x1, r0) = false :=
    (hI _ (mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩)).trans
      (confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm)))
  constructor
  · intro hp
    have e := hp (x0, r0) (x0, r1) rfl
    rw [e00, e01] at e
    exact absurd e (by decide)
  · intro hp
    have e := hp (x0, r0) (x1, r0) rfl
    rw [e00, e10] at e
    exact absurd e (by decide)

open Classical in
/-- AS TRÊS CASAS NÃO BASTAM: nelas passa o juiz que confere a página com o original, confere o assento com o
original, e diz que bate quando os dois conferem. Usa os dois lados e não os compara. -/
theorem nas_tres_casas_passa_quem_confere_cada_lado_com_o_original (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) :
    ∃ f g : X → Bool,
      ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (tresCasas x0 x1 r0 r1) := by
  refine ⟨fun x => decide (ρ x = ρ x0), fun r => decide (ρ r = ρ x0), ?_⟩
  intro p hp
  rcases mem_tresCasas.mp hp with rfl | rfl | rfl
  · have hc : confereB ρ (x0, r0) = true := confereB_sim (p := (x0, r0)) h0
    simp [hc, h0.symm]
  · have hc : confereB ρ (x0, r1) = false :=
      confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm))
    have hn : ¬ ρ r1 = ρ x0 := fun h => hne (h.symm.trans h1.symm)
    simp [hc, hn]
  · have hc : confereB ρ (x1, r0) = false :=
      confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm))
    have hn : ¬ ρ x1 = ρ x0 := fun h => hne h.symm
    simp [hc, hn]

/-- A QUARTA CASA: no grupo inteiro nenhum juiz da forma “a página confere E o assento confere” passa. -/
theorem no_grupo_nenhum_juiz_de_dois_selos_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 && g r0) = true :=
    (h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)).trans (confereB_sim (p := (x0, r0)) h0)
  have e11 : (f x1 && g r1) = true :=
    (h (x1, r1) (mem_grupo.mpr ⟨Or.inr rfl, Or.inr rfl⟩)).trans (confereB_sim (p := (x1, r1)) h1)
  have e01 : (f x0 && g r1) = false :=
    (h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)).trans
      (confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm)))
  revert e00 e11 e01
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-- CASAR LETRA COM LETRA PASSA, SE A LETRA DENUNCIA: se uma marca `s` da letra acompanha o estado nos dois lados
dentro do grupo, o juiz que só compara a marca da página com a do assento acerta as quatro casas. -/
theorem no_grupo_passa_quem_casa_uma_marca_da_letra (s : X → Bool) (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) (hs0 : s x0 = s r0) (hs1 : s x1 = s r1)
    (hsne : s x0 ≠ s x1) :
    ImprimeEm (confereB ρ) (fun p : X × X => s p.1 == s p.2) (grupo x0 x1 r0 r1) := by
  have c00 : (s x0 == s r0) = confereB ρ (x0, r0) := by
    rw [confereB_sim (p := (x0, r0)) h0, hs0]
    cases s r0 <;> decide
  have c11 : (s x1 == s r1) = confereB ρ (x1, r1) := by
    rw [confereB_sim (p := (x1, r1)) h1, hs1]
    cases s r1 <;> decide
  have c01 : (s x0 == s r1) = confereB ρ (x0, r1) := by
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm)), ← hs1]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  have c10 : (s x1 == s r0) = confereB ρ (x1, r0) := by
    rw [confereB_nao (p := (x1, r0)) (fun hh => hne (h0.trans hh.symm)), ← hs0]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  rintro ⟨a, b⟩ hp
  obtain ⟨ha, hb⟩ := mem_grupo.mp hp
  have ha' : a = x0 ∨ a = x1 := ha
  have hb' : b = r0 ∨ b = r1 := hb
  rcases ha' with ha' | ha' <;> rcases hb' with hb' | hb' <;> rw [ha', hb']
  · exact c00
  · exact c01
  · exact c10
  · exact c11

end TGLExt.CopiadorEImpostor.SondaT1Min

2. **(MEDIO)** candidata REV15 l.1010–1011, l.1029–1030, l.214–216, l.1125–1126, l.104–105, l.1158–1159; desenho l.89–96

   (a) l.1010–1011: “LEITURA DA GERÊNCIA, devolvida a ele e AINDA NÃO RATIFICADA: … a cópia legítima é a que indexa (o terceiro leitor da cena)”. Às 08:30 ele confirmou outra leitura (item 5 da mensagem das 08:13: cópia ou imposição é o sinal, a página; o leitor com o índice é quem diz). O cabeçalho geral (l.104–107) traz a nova; a seção 11 ficou com a velha. E “devolvida a ele” não consta [REAL]: na transcrição da sessão, entre a fala das 07:50 e a das 08:07 (linhas 140975 a 141116), não há mensagem de texto da gerência com essa leitura (busca por “indexa”: zero). Há um bloco de raciocínio de 184 caracteres (10:52:24 UTC), que só diz que a cena se percebe com o registro indexado e que o impostor seria o papel trocado, e a mensagem das 07:57, que diz “a leitura ainda depende do seu sim” sem dizer a leitura.
(b) l.1029–1030: “quem é o impostor na cena (perguntado ao operador)”. O item 5 que ele confirmou terminava: “Isso responderia à pergunta que eu tinha deixado sobre quem é o impostor.” O desenho (l.91–96) diz “como foram escritos” e corta essa frase e a segunda frase do item 2.
(c) l.214–216: a fala de 16/11 diz «mesma impressão» “sem dizer de quê”. O item 2 confirmado diz de quê.
(d) l.1125–1126: “apontou a patente da rede PSI-NET como a resposta técnica”. A letra é mais fraca:
«eu penso que a resposta técnica sobre a sua pergunta pode estar na nossa patente da rede psi-net»
(e) l.104–105: “só se sabe que o papel não bate quem tem o registro indexado”. A letra fala a quem perguntou:
«vc só faz a pergunta porque tem o registro indexado»
(f) l.1158–1159: “quem é o Verbo no par (o sinal que leva ou a releitura)”. A letra:
«assinatura inscrita na origem=NOME e levada junto dele = VERBO»
Falta a leitura literal (a própria assinatura, enquanto levada); a lista fecha em duas o que a letra deixa aberto.
(g) O cabeçalho não diz onde está a leitura que ele confirmou; a mensagem não tem arquivo de bytes.

   *Conserto pedido:* TEXTO. l.1010–1011: “LEITURA DA GERÊNCIA das 07:5x. Não chegou a ele em mensagem e foi SUPERADA às 08:30: a leitura que ele confirmou (seção 12) põe a cópia e a imposição no SINAL e faz do leitor com o índice quem diz qual das duas é. Os termos abaixo são fatos de funções e valem com ou sem leitura.”
l.1029–1030: “quem é o impostor na cena: às 08:30 ele confirmou a leitura em que a imposição é o sinal que chega sem a correspondência; nenhum termo daqui depende disso”.
l.214–216, acrescentar: “Às 08:30 ele confirmou a leitura em que a mesma impressão é a assinatura refeita no destino igual à inscrita na origem (itens 1 a 5: desenho R6, seção 2; a mensagem inteira está na transcrição da sessão, 16/11 11:13:17 UTC, linha 141217 contando de 1, e não tem arquivo de bytes).”
l.1125–1126: “o operador disse que pensa que a resposta técnica pode estar na patente da rede PSI-NET …”.
l.104–105: trocar a paráfrase pela citação por bytes da linha (e) acima.
l.1158–1159: “quem é o Verbo no par: a letra diz «levada junto dele = VERBO»; cabem ao menos três leituras (a assinatura enquanto levada; o sinal que a leva; a releitura no destino) e a escolha é dele”.
Desenho l.91: trocar “como foram escritos” por “resumidos pela gerência”, ou repor as duas frases cortadas.
A mesma frase (“devolveu a leitura”) está nos registros de memória de 16/11 07:52–07:58; corrigir ao lado.

3. **(MEDIO)** candidata REV15 l.1150, l.1209–1212, l.1229, l.1250, contra l.1135–1136; desenho l.145–146, contra l.120–122

   O arquivo chama de “nome do registro” o valor `ρ r`. No dicionário do próprio arquivo `ρ` é a palavra e `ρ r` é o sentido lido. Chamar isso de nome junta Palavra e Nome, que a l.1135–1136 diz não juntar por conta própria. O desenho (l.120–122) diz que a gerência não escolhe qual lado é Nome, e a l.146 repete “nome do registro”. No mesmo arquivo Nome já é outro objeto, o do kernel (`nomeDasSolucoes`, seção 9; `ha_copiador_fora_do_nome`, seção 8): homônimo sem aviso. A letra dele põe NOME na assinatura inscrita na origem; `ρ r` é a releitura do registro por quem julga. E ele deixou a leitura para exame:
«e não sei se faz sentido pra vc»
Verbo o arquivo não atribui a lado nenhum (conferido).

   *Conserto pedido:* TERMO: `bate_sse_legitimo_sob_o_nome_do_registro` passa a `bate_sse_legitimo_sob_a_assinatura_do_registro` (l.1211 e l.1250).
TEXTO, docstring l.1209–1210: “O registro da seção 11 só entra no juízo pela sua assinatura (o sentido lido dele, `ρ r`): a página bate com o registro se e somente se o pacote (assinatura do registro, página) é legítimo. Por definição.”
l.1229: “O próprio sentido é um resumo que serve.”
l.1150: “… só entra no juízo pela sua assinatura (por definição)”.
l.1156, acrescentar ao que NÃO se afirma: “qual lado do par é o Nome; aqui `ρ r` chama-se assinatura, e Nome fica para o objeto do kernel (seções 8 e 9)”.
Desenho l.145–146: “o pacote formado pela assinatura do registro (o sentido lido dele) e pela página”.

4. **(MEDIO)** desenho l.144–148 (seção 4) e l.190–194 (5.2); candidata REV15 l.1211–1212

   (a) `bate_sse_legitimo_sob_o_nome_do_registro` é `Iff.rfl`: os dois lados são a mesma fórmula, `ρ x = ρ r`. Não diz nada do braço 2. Que o veredito seja do corpo contra o índice, e não do carimbo, é definição da resposta certa pelo desenho. No modelo da seção 12 o carimbo que a página leva nem aparece em `Bate`. A frase “Para o braço 2 isso diz: …” lê um desdobramento de definição.
(b) l.192: “o carimbo refeito só é pego pelo índice”. Não é o que o braço mede. Com o índice fixo, o caso do carimbo refeito é acertado por quem relê o corpo contra o índice, por quem compara o carimbo com o índice e por quem sabe a Teoria de cor; só erra quem confere só por dentro (refiz os quatro casos).
(c) O limite dito na l.192–194 é teorema, por instância: com o registro fixo existe juiz que só vê a página e passa (sonda, RC 0).

   *Conserto pedido:* TEXTO, seção 4, no lugar das l.145–148: “`bate_sse_legitimo_sob_a_assinatura_do_registro` é a definição de bater escrita no vocabulário do pacote (termo `Iff.rfl`; não prova nada). No braço 2, que o veredito seja do corpo contra o índice é definição do desenho. O que é teorema (sondas do revisor T1, a adotar depois de conferência): sem o registro, nem com o carimbo se julga (`nem_com_o_carimbo_se_julga_sem_o_registro`); e, com o registro fixo, há quem passe só pela página (`com_o_registro_fixo_ha_quem_passe_so_pela_pagina`): é o limite deste braço.”
TEXTO, 5.2, l.192: “O carimbo refeito passa por quem só confere a página por dentro. Neste braço quem o acerta é quem abre o índice (pelo corpo ou pelo carimbo) ou quem sabe a Teoria de cor; nesse caso o braço não separa os três.”
TERMO (em SondaT1Par.lean, mesma pasta, sha256 6933914acff13a3b7886455a29351995fe030ceec35b56b048867ef60d45f79a):
theorem com_o_registro_fixo_ha_quem_passe_so_pela_pagina (ρ : X → V) (S : Set (X × X)) (r0 : X)
    (hS : ∀ p ∈ S, p.2 = r0) :
    ∃ I : X × X → Bool, PagouSo (Prod.fst : X × X → X) I ∧ ImprimeEm (confereB ρ) I S := by
  refine sem_o_par_ha_quem_passe_pagando_so_pi Prod.fst (confereB ρ) S ?_
  intro p hp q hq h
  have hpq : p = q := Prod.ext h ((hS p hp).trans (hS q hq).symm)
  rw [hpq]

theorem nem_com_o_carimbo_se_julga_sem_o_registro (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ J : V → X → Prop, ∀ (n : V) (x r : X), J n x ↔ Bate ρ x r := by
  rintro ⟨J, hJ⟩
  obtain ⟨a, b, hab⟩ := h2
  exact sem_o_registro_ninguem_julga_se_bate ρ ⟨a, b, hab⟩ ⟨J (ρ a), fun x r => hJ (ρ a) x r⟩

5. **(MEDIO)** desenho l.152–154 (seção 4), l.214–220 (5.4), l.17–20 (seção 1), l.43 (tabela dos resultados); partitura l.14–16

   A lista do que os teoremas não dão traz o juiz que sorteia e o tudo ou nada. Faltam:
(a) O leitor que usa os DOIS lados sem ler o sentido. Se uma marca da letra (por exemplo, ter ou não palavra de negação na afirmação-alvo) acompanha o estado na página e no assento dentro do grupo, quem só compara a marca dos dois lados acerta as quatro casas (sonda `no_grupo_passa_quem_casa_uma_marca_da_letra`, RC 0; fonte no achado T1-01). Nenhum teorema o reprova: os teoremas só reprovam quem usa UM lado.
(b) A regra da l.219–220 trata de original contra contrária. Não trata de página contra assento. Onde a página guarda a negação da entrada, a marca acompanha o estado nos dois lados e esse programa passa naquele grupo.
(c) Os teoremas falam só do veredito; apontar a entrada e a linha não tem termo.
(d) “O juiz que sorteia entra pela conta (seção 7)”: a conta de quem sorteia por um lado só está em 5.4 (1 em 16) e supõe sorteios independentes; a aritmética é p(1−p)·q(1−q) ≤ 1/16 (sonda `um_lado_so_sorteando_fica_em_um_dezesseis_avos`).
(e) Por isso JULGA PELO PAR quer dizer que o leitor usou os dois lados, não que leu o sentido dos dois; e “erra em todo grupo” só vale para quem não sorteia.

   *Conserto pedido:* TEXTO, seção 4, no lugar das l.152–154: “O que os teoremas não dão. Valem para o juiz que não sorteia, para o passar de tudo ou nada e só para o veredito (apontar a entrada e a linha não tem termo). Quem sorteia por um lado só acerta as quatro de um grupo em no máximo 1 de cada 16 vezes, se os sorteios são independentes (5.4). E os teoremas só reprovam quem usa UM lado: o leitor que usa os dois sem ler o sentido, casando uma marca da letra da página com a do assento, passa sempre que a marca acompanha o estado nos dois lados (sonda do revisor T1). Contra ele só há o controle do material (5.4). Por isso JULGA PELO PAR quer dizer que o leitor usou os dois lados; não que leu o sentido. E nada neles diz que um modelo de linguagem lê o sentido: isso é o que a rodada mediria.”
TEXTO, 5.4, no lugar da última frase: “Para isso a marca não pode acompanhar o estado nos dois lados dentro do grupo: em metade dos grupos, por sorteio com semente, a página diz a afirmação negada SEM palavra de negação quando a entrada do assento a traz COM, e a afirmada COM quando a entrada a traz SEM. A família de programas inclui o que alinha entrada e frase por palavras em comum e compara só a presença de negação.”
CONTA, seção 6, linha nova: “casa uma marca da letra dos dois lados | nos grupos em que a marca acompanha o estado: 1,00 e grupo certo; nos outros: 0,50 e grupo errado | não se separa de quem julga pelo par onde a marca acompanha”.
TEXTO, partitura l.15–16 e desenho l.19: “… erra pelo menos uma das quatro em todo grupo, se não sorteia; se sorteia, acerta as quatro de um grupo em no máximo 1 de cada 16 vezes.”

6. **(MEDIO)** desenho l.122–124 (seção 3, c), l.149–150 (seção 4), l.214–215 (5.4, i); candidata REV15 l.1151–1160 e l.1214–1217

   `um_resumo_julga_sse_separa_os_sentidos` dá ao juiz o resumo do REGISTRO e a página INTEIRA (`J : H → X → Prop`). Diz que a informação do resumo basta a um juiz que ainda lê o sentido da página. Não diz que comparar o resumo da página com o do registro julgue. O resumo dos bytes separa os sentidos: pelo teorema ele SERVE. E o programa que só compara bytes erra em toda cópia de outra letra (sonda, RC 0). O desenho não afirma o contrário em nenhuma frase, mas põe o teorema na seção 4 sem esse limite, ao lado de “o resumo dos bytes … tem de falhar”: lido junto, parece que o teorema explica a falha do controle. Não explica. Para comparar resumos é preciso mais: o resumo tem de ser igual em textos de mesmo sentido (sonda). O cabeçalho da candidata (l.1159–1160) diz “informação, não cálculo”; falta dizer isto. O uso de `resumo_que_confunde_sentidos_nao_julga` para a assinatura de forma está na medida do termo.

   *Conserto pedido:* TEXTO, seção 4, depois da frase do resumo (l.150): “Este teorema fala da informação do resumo do registro para um juiz que ainda lê a página inteira. Não diz que comparar o resumo da página com o do registro funcione: para isso o resumo teria de ser igual em textos de mesmo sentido. O resumo dos bytes serve no primeiro sentido e falha no segundo; a falha do controle (5.4, i) vem de a página estar em outra letra, não deste teorema.”
TEXTO, candidata l.1159: “O item 4 fala de informação, não de cálculo: não diz que o juiz seja computável a partir do resumo, nem que comparar o resumo da página com o do registro julgue.”
TERMO (em SondaT1Par.lean):
theorem comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido {H : Type} (ρ : X → V)
    (h : X → H) :
    (∀ x r, (h x = h r ↔ Bate ρ x r)) ↔
      ((∀ a b, h a = h b → ρ a = ρ b) ∧ (∀ a b, ρ a = ρ b → h a = h b)) := by
  constructor
  · intro hc
    exact ⟨fun a b hab => (hc a b).mp hab, fun a b hab => (hc a b).mpr hab⟩
  · rintro ⟨hsep, hcla⟩ x r
    exact ⟨hsep x r, hcla x r⟩

theorem o_resumo_injetivo_serve_e_comparar_resumos_erra {H : Type} (ρ : X → V) (h : X → H)
    (hinj : Function.Injective h) (x r : X) (hxr : x ≠ r) (hs : ρ x = ρ r) :
    (∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r) ∧ ¬ (h x = h r ↔ Bate ρ x r) := by
  refine ⟨(um_resumo_julga_sse_separa_os_sentidos ρ h).mpr (fun a b hab => by rw [hinj hab]), ?_⟩
  intro hiff
  exact hxr (hinj (hiff.mpr hs))

7. **(MEDIO)** candidata REV15: a regra na l.111; as estrelas nas l.1018, 1024, 1039, 1105, 1113, 1148, 1151, 1189, 1199, 1214; o rótulo na l.1234

   A l.111 diz que só leva estrela o que tem conteúdo próprio. As seis estrelas novas não têm, além do teorema do par da seção 2:
(1) `o_teste_reprova_quem_so_ve_a_pagina_sse` e `…_o_registro_sse`: o termo é o teorema do par aplicado a `Prod.fst` e a `Prod.snd`; a docstring o diz.
(2) `um_resumo_julga_sse_separa_os_sentidos`, com duas estrelas: é o teorema do par com o que o juiz vê := (a página, o resumo do registro). Provei-o só com `so_se_imprime_o_que_se_pagou` e `sem_o_par_ha_quem_passe_pagando_so_pi` (sonda `qual_resumo_serve_pelo_teorema_do_par`, RC 0). São duas estrelas para a mesma coisa da seção 2.
(3) `so_pelo_sinal_ninguem_julga` sai em uma linha de `sem_o_registro_ninguem_julga_se_bate`; `so_pela_assinatura_ninguem_julga` sai de `o_juizo_nao_sai_so_do_registro` (sondas).
(4) `sem_o_registro_ninguem_julga_se_bate` é a ida de `julga_sem_registro_sse_um_sentido_so` e nega o mesmo que `o_juizo_nao_sai_so_da_pagina` (sonda `juizo_so_da_pagina_as_duas_formas`).
São dois fatos, um por lado, em cinco enunciados, três com estrela. E `resumo_que_confunde_sentidos_nao_julga`, rotulado CONTROLE QUE REPROVA, é a contrapositiva da ida do teorema do resumo; não exibe exemplo, como os outros controles do arquivo exibem.

   *Conserto pedido:* TEXTO: tirar as estrelas das seções 11 e 12; se a gerência quiser marcar a aplicação, uma só, em `um_resumo_julga_sse_separa_os_sentidos`.
Nos dois cabeçalhos de seção, acrescentar: “Tudo aqui é o teorema do par da seção 2 aplicado à cena (página, registro) e ao pacote (assinatura, sinal). O conteúdo próprio é a escolha do que o juiz vê.”
Docstrings de `so_pelo_sinal_ninguem_julga` e `so_pela_assinatura_ninguem_julga`: acrescentar “É o fato da seção 11 no vocabulário do pacote.”
l.1234: trocar “CONTROLE QUE REPROVA” por “Contrapositiva da ida.”
TERMO (em SondaT1Par.lean):
theorem so_pelo_sinal_segue_do_da_secao_11 (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ g : X → Prop, ∀ p : V × X, g p.2 ↔ Legitimo ρ p :=
  fun ⟨g, hg⟩ => sem_o_registro_ninguem_julga_se_bate ρ h2 ⟨g, fun x r => hg (ρ r, x)⟩

8. **(BAIXO)** candidata REV15 l.1022, l.1077–1078, l.1145–1147, l.1150, l.1172, l.1182–1187, l.1211–1212

   Cinco dos 20 teoremas novos são desdobramento de definição: `o_emitido_e_legitimo` (rfl); `o_juizo_e_o_primeiro_contra_o_segundo` (Iff.rfl); `bate_sse_legitimo_sob_o_nome_do_registro` (Iff.rfl); `outra_forma_de_mesmo_sentido_e_legitima` e `a_imposicao_nao_e_legitima`, em que o termo é a própria hipótese (conclusão e hipótese são a mesma fórmula: vazios). Estão em “O que fica provado” sem a marca “por definição”, que o arquivo usa noutros lugares (`dois_sentidos_sse_separa`, `o_decisor_nao_depende_do_tempo`). `a_imposicao_nao_e_legitima` só diz que a gerência DEFINIU imposição como sinal de outro sentido sob a assinatura.

   *Conserto pedido:* TEXTO: acrescentar “(por definição)” às cinco docstrings e aos itens 2 (seção 11), 1 e 3 (seção 12).
l.1147: “a imposição, como definida aqui (sinal de outro sentido sob a assinatura inscrita), não é legítima: é a definição”.

9. **(BAIXO)** desenho l.139–140, l.144–145, l.210–211, l.224, l.232

   (a) l.139: falta o quantificador do teorema. Para um registro FIXO existe juízo só sobre a página; é o limite do braço 2.
(b) l.144: falta a hipótese “se a palavra tem dois sentidos”.
(c) “A mesma página” e “o mesmo registro” dos teoremas são tudo o que o juiz vê daquele lado. O leitor recebe o índice inteiro (l.232), e o desenho não diz o estado dos outros 15 assentos. Se variar, o par de mesmo registro não está, à letra, no conjunto.
(d) O número da apresentação (l.224) é visto pelo leitor e difere dentro de cada par; quem cobre isso é o controle do aparelho, e o desenho não o diz.
(e) l.210–211: “dá à mesma página a mesma resposta” vale para quem não sorteia (zero grupos); “1 de cada 16” é de quem sorteia. As duas estão numa frase só.

   *Conserto pedido:* TEXTO. (a) “… nenhum juízo feito só sobre a página diz se ela bate, seja qual for o registro.”
(b) “… se a palavra tem dois sentidos, ninguém julga a legitimidade por um componente só.”
(c) Em 5.6: “Em toda apresentação os outros 15 assentos vão no estado da casa. Nas duas apresentações de mesmo estado do assento o índice é idêntico byte a byte; nas duas de mesmo estado da página, a página é idêntica byte a byte. São os pares que os dois teoremas pedem.”
(d) Em 5.6: “O número da apresentação muda dentro de cada par; se ele denunciar a resposta, quem acusa é o controle do aparelho.”
(e) “Quem só vê a página e não sorteia dá à mesma página a mesma resposta e erra uma das duas: zero grupos. Se sorteia, acerta os quatro vereditos de um grupo em no máximo 1 de cada 16 vezes.”

10. **(BAIXO)** candidata REV15 l.1264–1270, l.112–118, l.529–542, l.1174–1179, l.1135, l.1156–1159

   (a) `a_identidade_nunca_paga_sse_um_igual_a_zero` está depois dos #print axioms das seções 11 e 12 e fora de seção; o cabeçalho o liga à seção 10.
(b) A lista das sondas adotadas (l.112–118) não traz `o_decisor_nao_depende_do_tempo` (a docstring diz sonda do B2R).
(c) `nenhum_copiador_efetivo_e_involucao` e `copiador_e_involucao_so_a_identidade` são contrapositivas um do outro; não está dito.
(d) `a_copia_mantem_o_pacote_legitimo` só usa a cláusula `imprime`: vale para toda reprodução que guarda o sentido, copiador ou não.
(e) l.1135: o Psibit avisa que o Verbo e o pareamento dele são homônimos de outros do kernel (Psibit.lean l.139–141); o cabeçalho cita o par sem o aviso.
(f) [LEGAL, o operador confere] l.1156–1159 descreve, em pasta pública e num cabeçalho que iria ao kernel público, como se comporta a assinatura do pedido da rede.
(g) Duas falas dele de 16/11, de 09:59 e 10:01, sobre o psíon, estão em C:\IALD\Central de Patentes\work\vitrine_postura_13nov\ e trazem as palavras verbo, lendo, sinal e lido. A candidata é das 08:47 e não as conhece. Não leio por ele; aviso para não se perguntar o que ele talvez já tenha dito.

   *Conserto pedido:* (a) Mover o teorema e o seu #print axioms para a seção 10.
(b) Acrescentar o nome à lista do B2R.
(c) Docstring da l.529: “É a contrapositiva de `copiador_e_involucao_so_a_identidade`, aqui pelo caminho do kernel.”
(d) Docstring da l.1174: “Só usa que a reprodução guarda o sentido; vale para toda reprodução que imprime.”
(e) l.1135: “(lá o par é Palavra e Verbo, e o próprio Psibit os diz homônimos do Verbo em ato e do par J/K; …)”.
(f) Decisão do operador antes de qualquer instalação: a frase fica ou sai.
(g) Ler as duas falas por bytes antes de escrever a pergunta sobre o Verbo no par.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- O arquivo de teoremas do copiador e do impostor compila limpo (93 teoremas, sem lacuna) e nada foi instalado; o que falta é texto e três enunciados pequenos, que já compilam na pasta do revisor.
- O teste tem uma casa que a partitura ainda não lhe diz em palavras: em um quarto das apresentações a página traz uma afirmação contrária à Teoria, o assento foi mexido do mesmo jeito, e a resposta certa é “bate”; é essa casa que pega o leitor que confere cada lado com o que sabe de cor, e o senhor precisa ouvir isso antes de dizer se é o que a sua letra pede.
- Um resultado bom vai querer dizer que o leitor usou os dois lados, não que leu o sentido: um programa que só casa uma marca da letra da página com a do assento (por exemplo, ter ou não a palavra “não”) passaria, se as páginas deixarem; por isso as páginas têm de ser escritas de modo que a negação da página não acompanhe a do assento.
- O arquivo chama de “nome” o sentido do registro; a sua fala diz «assinatura inscrita na origem=NOME e levada junto dele = VERBO» e o senhor deixou essa leitura para exame: o revisor propõe tirar a palavra nome desse teorema até o senhor dizer qual lado do par é o Nome e qual é o Verbo.
- Duas frases do arquivo ainda guardam a leitura das 07:50 (a cópia legítima seria o terceiro leitor), que não chegou ao senhor em mensagem e que a sua confirmação das 08:30 trocou: cópia ou imposição é a página, e o leitor com o índice é quem diz qual das duas ela é.

