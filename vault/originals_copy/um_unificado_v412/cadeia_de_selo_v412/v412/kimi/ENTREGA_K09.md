# ENTREGA K09 — o teste às cegas, rodada 3

- **O que mudou em relação à K04, em três frases.** (1) A parede permanece — não existe hoje teste cego de natureza executável com poder de desenho ≥ 5σ — mas a cronologia do neutrino foi corrigida nos dois eixos: o número de 207 dias é posterior à previsão publicada (valor no acervo em 22/01/2026; Zenodo em 17/02/2026) e anterior apenas ao pino da função de veredito (08/08/2026). A amostra de 207,2 dias acumula a de 59,1; não são determinações independentes; a cegueira dita é a do número, não a dos dados. Esta nota fala só de datas e das entradas da fórmula; não diz o que o autor leu ou deixou de ler. (2) A leitura intermediária de Hubble não está morta: desfavorecida e não excluída (Fase 7, com covariância: −3,22σ → −1,66σ/−1,54σ), com a lei da face dos cronômetros pendente (poder prévio 2,33σ). (3) A tabela de desfechos do m₂ foi refeita com o módulo correto e o calendário passou a vir do orçamento do artigo de 207 dias: com o piso, 5σ, D90 e r=3 são inalcançáveis; sem piso, são brinquedos, não cronogramas.
- **Só um número do JUNO tornado público pela primeira vez depois de 08/08/2026** (e antes de qualquer acesso do selo) é posterior aos dois marcos (previsão publicada; pino da regra): é ele o observável de `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`, pronto para a gerência ler ao operador e, se ele quiser, selar por hash antes de qualquer acesso ao centro novo. O dado tomado depois de 18/05/2026 `[DECLARADO, sem resposta crua guardada]`, ainda não mostrado `[DECLARADO]`, não é, por si só, posterior aos dois marcos.
- **As duas regras lado a lado, sem escolha:** A, duas testemunhas independentes (o comportamento que o código selado descreve hoje: `r≥5` sem segunda determinação autônoma vai a `TENSION` com `tensao_global_5sigma_sem_2a_determinacao`, não a `FALSIFIED`); B, uma testemunha com limiar explícito (emenda). Manter A ou adotar B é ato futuro do operador.
- **Hubble corrigido:** a palavra "morta" saiu; as nove rotas omitidas entraram; o D da casa (6,710; Cefeidas livres 5,191) vem sempre antes e ao lado do D de bolso (7,068/8,068); o empilhamento das linhas locais diz quanto já é a Fase 9 V2; o DESI DR3 está respondido (fundo, não testemunha).
- **m₂ corrigido:** lados do erro NuFIT desfeitos (tabela 3,024242478; eq. 11 3,044179410); caudas com o módulo (68,27 % / 31,46 % / 99,73 % sob verdade = previsão); a distância do incremento a 7,50 é 1,228176σ; SK-Gd 3,605064023 fica ao lado da ressalva (está a 3,101149σ do próprio JUNO; o cenário de 380,0785536 dias só vale se a anomalia persistir); o código é descrito como ele é, e o que falta nele foi para a lista "para a gerência decidir".
- **Combinação corrigida:** Stouffer de pesos iguais é `(D_J + D_N)/√2` (σJ ≤ 0,024145×10⁻⁵ eV²; 2.162 dias vivos; poder 90,5 %); pesos proporcionais a D dão 0,0264169×10⁻⁵ e 1.806 dias; a combinação não antecipa nada; ringdown 25,5/25,7 eventos é piso sem viés (D10 satura ≈ 5,8 com o viés 0,0686); só com O4b, D14 ≈ 8,7 meses e D10 ≈ 16,6 meses.
- **Custódia:** nenhum teste executado, nenhum vetor de dados lido, nenhuma abertura; REV0–REV3 preservados; correções ao lado; `ERRATA_NEUTRINO_V412_DADOS_K09.json` é a errata do core em dados (só números com fonte; a prosa e a instalação são da gerência).
- Rodada com conferência própria do construtor (revisão interna) pós-adendo — a revisão distinta é a conferência de 15/11 —: cronologia de dois eixos nos arquivos desta rodada (resíduos de um eixo só nos arquivos antigos K01/K04, não editados, listados em `ERRATA_RESIDUOS_EIXOS_K01_K04.md`), dez passagens corrigidas, JSON renomeado e datado, datas em Δm² e m₂ lado a lado, MATCHED com modelo rotulado e válido só em H1, 22/06 marcado [DECLARADO], autoridade única para a classe "preliminar". O registro entra como ANOTACAO na rota existente; a gerência registra após conferir. Gate imóvel.

## A. Hubble — o que foi examinado e o que falta

`HUBBLE_JA_EXAMINADO_K04.md` (REV0/REV1/REV2 preservados, `ERRATA_HUBBLE_K09.md` ao lado) conclui: nenhuma linha independente de um passo está qualificada a 5σ/D90; SN II EPM 3,256 é teto estatístico e cai a cerca de 2,32 com sistemática igual à estatística; linha sem ponte examinada ("esta linha lê K·H do fundo", com rota e seq) não entra em conta de poder. A Fase 7 com covariância levou a leitura intermediária de −3,22σ a −1,66σ e −1,54σ: desfavorecida, não excluída; a lei da face dos cronômetros segue pendente (`bancada.preregistro_dois_lados_delta_k`, poder prévio 2,33σ).

## B. O neutrino m₂ — cronologia, desfechos e a segunda testemunha

`M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md` (REV0–REV3 preservados; o estado anterior a esta rodada K10 está em REV4; `ERRATA_M2_K09.md` e `ERRATA_M2_K09_15nov.md` ao lado) carrega a cronologia nos dois eixos nas frases de cronologia dos arquivos desta rodada: a tese do neutrino é de 2025 (16/10, zenodo.17372599; 04/11, zenodo.17526619) e os dois artigos não contêm a fórmula nem o valor [DECLARADO pelo revisor da conferência]; o valor 8,51 meV está no acervo desde 22/01/2026 (sem carimbo externo) e no Zenodo desde 17/02/2026; o degrau de 59,1 dias (18/11/2025) é anterior ao valor público e anterior ao pino — retrodição sem ajuste, não leitura prospectiva do valor; o número de 207,2 dias veio depois da previsão publicada e antes do pino da regra. A amostra de 207,2 dias acumula a de 59,1; não são determinações independentes; a cegueira dita é a do número, não a dos dados. O core selado lê 2,952854 (NuFIT simétrico arredondado) e devolve `ARMED_CONSISTENT`; com o erro publicado do lado da previsão seria 3,024242 (tabela) ou 3,044179 (eq. 11) e o rótulo seria `TENSION`; a letra não escolhe; escolher é do operador; `TENSION` não é falsificação. Se o perito (R3) fosse atualizado para 207,2 d, a razão seria 1,938 (<3).

A Tabela 6 reproduzida: `P(r≥5) = 64,788004 %` (independente) e `66,145584 %` (brinquedo cumulativo). Vale a forma dos dois mundos, sem escolha: sem segunda testemunha elegível, o canal só devolve `ARMED_CONSISTENT` ou `TENSION`; nenhum dos dois falsifica (parede medida). Se o valor verdadeiro for o centro público de hoje (a1/b1), o primário passa de `r=5` com `P ≈ 65 %` no desenho da Tabela 6; se a previsão for verdadeira (a2/b2), devolve `ARMED_CONSISTENT` com `P ≈ 99,7 %`. Esta entrega não adota nenhuma das duas hipóteses.

## C. O incremento — pré-registro em rascunho

`PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md`: observável (só um número do JUNO tornado público pela primeira vez depois de 08/08/2026 e antes de qualquer acesso do selo), duas formas de obtê-lo (publicado como período disjunto; ou diferença de variância inversa entre cumulativos, que sem a covariância não identifica centro nem erro), métrica congelada m₂ (trocar é emenda), fonte elegível (a classe "preliminar" é ratificada pelo operador, com proposta técnica da gerência, antes do selo), a tabela do incremento com 1/2/3 anos sob as duas hipóteses, as regras A e B lado a lado sem escolha, o significado dos desfechos (o negativo atinge o pacote da escala — o Um posto em 1 eV, m₁ ≈ 0, a identificação com sen 45° (leitura do operador, [ONTO]) e o ordenamento normal —, não β isolado nem o gate; nenhum positivo é `CONFIRMED`) e a custódia (gerência guarda; operador decide e sela; revisor independente abre uma única vez).

## D. Combinação, ringdown e ressalvas

`COMBINACAO_K04.md` e `RESSALVAS_UMA_A_UMA_K04.md` (REV2 preservada, `ERRATA_COMBINACAO_K09.md` ao lado): Stouffer corrigido; "2034" lido como fim do levantamento do SO — a combinação não antecipa nada; ringdown com o piso e a saturação ditos; R5 redesenhada como ruído por linha nas 111 linhas brutas; R3/R4 com partição documental (3 âncoras + 9 MAS como calibração; 92 HMS fora); R7 com o censo do Mapa (teto de 16 rotas Hubble e 123 que olharam dado); F2b: a retirada é conclusão da gerência (o operador autorizou o conjunto D em 29/10 e a opção (c) em 03/11 [DECLARADO pela ORDEM K09, sem bytes citados]).

## E. A errata do core em dados

`ERRATA_NEUTRINO_V412_DADOS_K09.json`: só números com fonte — identificador, data da primeira apresentação pública, data do artigo, valor, erro e `r` em m₂ e em Δm² — para os degraus de 59,1 e 207,2 dias, os dois ajustes globais e a segunda testemunha. `4bdae22a…` consta como `frozen_hash` do objeto congelado; os sha256 do `.py`, do `.resultado.json` e do dicionário portado constam separados; `previsao_publicada` e a posição relativa de cada degrau estão no JSON.

## Artefatos e hashes (SHA-256)

| artefato | hash |
|---|---|
| `HUBBLE_JA_EXAMINADO_K04.md` | `d79c4e21b04e169423c6267defe70d3494fa82f6b891b34a99a4da0611181009` |
| `M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md` | `95c59cc2ea78093532caa49a7679848a646eab764db7f642ffbcdec3f09ec8a8` |
| `COMBINACAO_K04.md` | `e4f403f5db66e7c73e67a21718b0bb79dbd1b164bb893b1424612391fc6236b2` |
| `RESSALVAS_UMA_A_UMA_K04.md` | `662fb12a2bd9fa9fa8da4210020fa9b513ca886519f293ec2bc6d43dc9163dba` |
| `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md` | `3ae989a6bae16a2dd3a80eb2879eec65ed7bd35e03eeac1469213bf7e32169b6` |
| `ERRATA_NEUTRINO_V412_DADOS_K09.json` | `deae4e3dfb72cd3cab2aa6054b2ba39d48f6a8a5545fd23e83268190ef75ab9c` |
| `ERRATA_M2_K09.md` | `dca82d9afe62a6452b04edb94ff5b65cbcb68a584c2ecc99241e428db4f7b90e` |
| `ERRATA_M2_K09_15nov.md` | `580bcaa437075de415831d11b5f2054757c1233c330abefb82391fa4ad31ad5f` |
| `ERRATA_HUBBLE_K09.md` | `9870ca099b8d435b1484eef79b3fbde12584e46df210433920316604655601eb` |
| `ERRATA_COMBINACAO_K09.md` | `0146da2c447a5f5568583c24012dfe56ccacd2de658c011bdac5346887530b76` |

`INSUMOS_PARA_A_PERGUNTA_K09.md` traz fatos, alternativas e custos sem recomendação; `REGISTRO_MAPA_K09.json` é proposta de ANOTACAO não registrada — a gerência registra após conferir.
