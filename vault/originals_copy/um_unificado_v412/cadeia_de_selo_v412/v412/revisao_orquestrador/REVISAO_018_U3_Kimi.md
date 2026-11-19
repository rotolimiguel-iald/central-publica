APROVADO_COM_RESSALVAS — 0 ALTO, 0 MEDIO, 7 BAIXO (todos de texto/referência; o conteúdo Lean e as afirmações da gerência conferem em tudo o que foi medido de forma independente)

# REVISÃO 018 — U3 (Kimi, revisor distinto) — a candidata do copiador e do impostor, R7

Unidade revisada: `candidatas_c1\REV16\CopiadorEImpostor.lean` (1.758 linhas, 106.328 B, sha256
`815b6334917e3eab5fa482f3e9c6ba947262e48c67f78c68dec779294c446e89`; o sha16 bate com o da ordem). R6 de referência:
`REV15\CopiadorEImpostor.lean` (sha256 `36579c2e…e26b0`, como o T1 registrou). Não li `REVISAO_018_U3_Codex.md` nem
nada em `revisao_orquestrador\U3_Codex\`. Só leitura fora da minha pasta; compilação em cópia própria
(`revisao_orquestrador\U3_Kimi\compilacao\`), com `lean.exe` 4.31.0 direto sobre os `.olean` de `C:\t\k411c\final`,
pelo script `compilar_candidata.ps1` copiado para a minha pasta. Nada a provedor remoto, nada instalado.

## Achados (por gravidade; todos BAIXO)

1. **(BAIXO) Referência ao kernel que não resolve.** `REV16\CopiadorEImpostor.lean` l.1155 (cabeçalho da seção 12):
   cita `` `TheImportedExpectation.the_reading_fixes_the_code` `` como nome completo. O nome não resolve (sonda
   própria `U3_Kimi\compilacao\SondaNomesKernel.lean`: `error(unknownIdentifier)`, RC 1; os outros 14 nomes citados
   em prosa resolvem). O teorema existe como `TGLExt.the_reading_fixes_the_code`
   (`C:\t\k411c\final\TGLExt\TheImportedExpectation.lean` l.194; namespace `TGLExt`, arquivo TheImportedExpectation) e
   o conteúdo confere com o gloss “Verbo(Nome) = Nome” (`theReading I A = A` sobre o centralizador). *Conserto:*
   trocar para `` `TGLExt.the_reading_fixes_the_code` `` (ou “em `TheImportedExpectation`,
   `the_reading_fixes_the_code`”).

2. **(BAIXO) Referência de texto velha à tabela do desenho.** `REV16` l.1279 (cabeçalho da seção 13): “A linha
   ‘acerto por veredito 0,50’ da tabela do desenho”. O desenho R6 atual
   (`teste_frente_a_r6\DESENHO_DO_TESTE_R6_GERENCIA.md`) não tem essa linha nem o número 0,50: a seção 6 mostra
   contagens (a linha “só a página (responde pelo que sabe de cor)” dá 16, 16, 0, 0). O conteúdo está certo (duas
   das quatro = o teorema); o apontamento, não. *Conserto:* apontar a linha “só a página” da seção 6 do desenho, ou
   escrever “duas das quatro”.

3. **(BAIXO) Desenho desatualizado quanto à candidata.** `DESENHO_DO_TESTE_R6_GERENCIA.md` l.137: “(candidata
   `CopiadorEImpostor`, seções 11 a 13; não instalada)”; l.146: “sondas compiladas do revisor T1, a adotar na
   candidata”. A R7 já traz a seção 14 com as sondas adotadas e recompiladas. *Conserto:* “seções 11 a 14” e
   “adotadas na R7”.

4. **(BAIXO) Partitura sem o qualificador “não sorteia”.** `PARTITURA_DO_TESTE_R6.md` l.28–29 (“O que o teste
   decide”): “Quem responde por um lado só acerta duas das quatro.” — sem o “não sorteia” que o desenho traz
   (seção 1, l.22: “e não sorteia”). Para o juiz que sorteia a frase não vale (pode acertar as quatro; por grupo a
   chance fica ≤ 1/16, como a própria candidata prova). *Conserto:* “Quem responde por um lado só, sem sortear,
   acerta duas das quatro.”

5. **(BAIXO) O RESULTADO citado não é da unidade revisada.** `candidatas_c1\RESULTADO_CopiadorEImpostor.json`
   (15:57) mede o arquivo da raiz (a R8: 108.054 B, sha16 `0729ab820c049e9a`), não a R7 (`REV16`, sha16
   `815b6334917e3eab`) que a ordem designa. A R8 difere da R7 só em comentários e docstrings (diff REV16↔REV19; REV19
   = raiz, byte a byte), e eu recompilei a R7 em cópia própria: as afirmações (saída zero, sem aviso, 118 teoremas,
   só o trio) valem para a R7 — mas o artefato registrado é de outra fonte. *Conserto:* gerar o RESULTADO sobre o
   arquivo `REV16` ou registrar no JSON que a R8 difere da R7 só em texto.

6. **(BAIXO) O modelo simétrico da seção 13 sem a nota de passagem.** `REV16` l.1275: o grupo é a lista simétrica
   (as mesmas duas entradas `a`, `b` servem de página e de registro). No desenho há quatro textos; a R7 não diz que
   a passagem se dá porque só os dois valores de sentido importam (a contagem de dois em quatro para quatro textos
   não está escrita como termo; a seção 14 modela os quatro textos, mas não a conta). *Conserto:* uma frase no
   cabeçalho da seção 13 dizendo isso.

7. **(BAIXO) Resíduo de numeração alheia em docstring.** `REV16` l.1461–1462: a docstring de
   `no_grupo_quem_acerta_os_quatro_usa_os_dois_lados` abre com “(a) ”, resto da enumeração do relatório T1.
   *Conserto:* tirar o “(a) ”.

## Os dez achados do relatório T1 (sanado / em parte / não sanado)

1. **ALTO — a quarta casa do 2 × 2: SANADO.** A seção 14 (l.1368–1756) adota as sondas: `tresCasas`, `grupo`,
   `tres_casas_trazem_o_par_da_pagina` (l.1429), `…_do_registro` (l.1439), `nas_tres_casas_quem_acerta_usa_os_dois_lados`
   (l.1449), `no_grupo_quem_acerta_os_quatro_usa_os_dois_lados` (l.1463), `nas_tres_casas_passa_quem_confere_cada_lado_com_o_original`
   (l.1476), `no_grupo_nenhum_juiz_de_dois_selos_passa` (l.1497), `no_grupo_passa_quem_casa_uma_marca_da_letra` (l.1542),
   e ainda `no_grupo_nenhum_juiz_de_um_selo_ou_outro_passa` (l.1517, além da sonda). O cabeçalho da seção 14 diz em
   palavras que os dois teoremas da seção 11 cabem em três casas e o que a quarta reprova. No desenho: seção 4 com a
   bala “A quarta casa” (l.144–146), seção 1 com “acerta três” (l.22), a conta com a linha nova (l.275). Ressalva de
   leitura: a partitura diz ao operador o número (“acerta três”) sem dizer em palavras qual é a casa que falta — a
   quarta casa dita em palavras ficou só no desenho.
2. **MEDIO — frases velhas / além da letra: SANADO.** l.1027–1029 (“LEITURA DA GERÊNCIA das 07:5x … não chegou a ele
   em mensagem e foi SUPERADA às 08:30”); l.1049–1051; l.221–225 (com onde está a mensagem); l.1146–1147 (“disse que
   pensa que a resposta técnica pode estar…”, como a letra); l.104–107 (a paráfrase trocada pela citação por bytes,
   que conferi); l.1181–1184 (as três leituras do Verbo). O conteúdo confirmado às 08:30 tem por bytes só o
   «confirmo tudo» dele; o que foi confirmado está na mensagem da gerência, cuja cópia fica na pasta privada da casa
   (o desenho dá sha16 `1ba1bd3db0e1a242`) — declarado nos dois arquivos; não é leitura além da letra, mas a
   conferência por bytes do conteúdo não é possível em `cunhagens_13out`.
3. **MEDIO — “nome do registro”: SANADO.** O teorema passou a `bate_sse_legitimo_sob_a_assinatura_do_registro`
   (l.1240) com a docstring pedida (l.1238–1239); “nome do registro” não ocorre mais no arquivo (busca: zero); “Nome
   fica para o objeto do kernel das seções 8 e 9” (l.1181–1182). Desenho l.120 e partitura item 2 ajustados.
4. **MEDIO — o Iff.rfl lido como teorema do braço 2: SANADO.** Docstring com “Por definição.” (l.1239); as sondas
   `com_o_registro_fixo_ha_quem_passe_so_pela_pagina` (l.1577) e `nem_com_o_carimbo_se_julga_sem_o_registro` (l.1588)
   adotadas. No desenho o teste do carimbo saiu (l.349–350, l.394) e a frase velha não existe mais.
5. **MEDIO — o juiz de dois lados sem sentido; a conta de quem sorteia: SANADO.** `no_grupo_passa_quem_casa_uma_marca_da_letra`
   (l.1542) e `um_lado_so_sorteando_fica_em_um_dezesseis_avos` (l.1624–1635); a seção 13 declara “Não diz que usar os
   dois lados é ler o SENTIDO” (l.1283–1286). Desenho seção 4 reescrito (“O que os teoremas não dão”, l.150–157) e a
   regra de escrita contra a marca da letra (l.204–207). Apresentação escolhida diferente da pedida (a conta por
   rodada, 0,27 %, seção 7; o 1/16 por grupo não aparece mais) — sem erro.
6. **MEDIO — resumo: informação, não comparação: SANADO.** Cabeçalho da seção 12 com a frase pedida (l.1184–1186);
   `comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido` (l.1599) e
   `o_resumo_injetivo_serve_e_comparar_resumos_erra` (l.1612) adotados; o desenho tem a frase de limite (l.156–157).
7. **MEDIO — estrelas das seções 11 e 12: SANADO.** Uma só estrela, em `um_resumo_julga_sse_separa_os_sentidos`
   (l.1175, l.1243) — a que o T1 permitiu. Os dois cabeçalhos com “Tudo aqui é o teorema do par da seção 2 aplicado…”
   (l.1030–1031, l.1186). Docstrings com “É o fato da seção 11 no vocabulário do pacote.” (l.1218–1219, l.1228–1229).
   `resumo_que_confunde_sentidos_nao_julga` agora “Contrapositiva da ida” (l.1263).
8. **BAIXO — cinco desdobramentos sem a marca: SANADO.** “(Por definição.)” em l.1097–1099, l.1198–1199,
   l.1209–1211, l.1213–1216, l.1238–1241; e nos itens do cabeçalho (seção 11 item 2, l.1041–1043; seção 12 itens 1 e
   3, l.1166–1174).
9. **BAIXO — o desenho: SANADO.** “seja qual for o registro” + a nota do registro fixo (l.139–141); a hipótese de
   dois sentidos (l.147); o índice idêntico byte a byte (l.192); o código da apresentação que não codifica grupo nem
   estado (l.245–246); a frase que misturava quem sorteia com quem não sorteia, separada (l.22, l.150–151).
10. **BAIXO — posição, lista, contrapositiva, Psibit, LEGAL: SANADO, salvo o que é do operador.** (a) o teorema está
    na seção 10 (l.1016–1019) e o seu #print axioms ao lado de `tudo_comuta_…`; (b) `o_decisor_nao_depende_do_tempo`
    entrou na lista do B2R (l.119); (c) “É a contrapositiva de `copiador_e_involucao_so_a_identidade`, aqui pelo
    caminho do kernel.” (l.540); (d) “Só usa que a reprodução guarda o sentido: vale para toda reprodução que
    imprime.” (l.1201–1202); (e) os homônimos do Psibit citados (l.1155–1157). (f) [LEGAL] fica para o operador, com
    o aviso posto em l.1180–1181 — pendente por decisão dele, como o próprio T1 marcou. (g) era recado ao
    orquestrador.

## Seções 13 e 14: cada teorema diz o que a docstring diz?

Sim, nos 25 teoremas novos (7 da seção 13, 18 da seção 14), lidos um a um contra o enunciado:

- Seção 13: `quem_so_ve_a_pagina_acerta_exatamente_a_metade` (l.1312) e `…_o_registro_…` (l.1326) provam acertos = 2
  sob `PagouSo` do lado e dois sentidos; `quem_acerta_os_quatro_usa_os_dois_lados` (l.1347) dá o recíproco;
  `sem_dois_sentidos_o_constante_acerta_os_quatro` (l.1360) é o controle declarado. As docstrings não vendem mais
  que isso.
- Seção 14: os teoremas das três casas e da quarta (l.1429–1568) batem com as docstrings; `com_o_registro_fixo_…`
  (l.1577) é instância declarada de `sem_o_par_…`; `nem_com_o_carimbo_…` (l.1588) instância de
  `sem_o_registro_ninguem_julga_se_bate`; `comparar_resumos_…` (l.1599) é o “núcleo do sentido” dos dois lados;
  `o_resumo_injetivo_serve_e_comparar_resumos_erra` (l.1612) é o controle declarado; `um_lado_so_sorteando_…`
  (l.1624) é só a desigualdade, com o modelo de sorteio declarado como hipótese de fora do Lean.
- Nenhum vazio ou verdadeiro-por-definição vendido como resultado: os desdobramentos (`mem_grupo`, `mem_tresCasas`,
  `tresCasas_sub_grupo`, `confereB_sim`, `confereB_nao`, `o_juizo_pelo_par_acerta_os_quatro`) são auxiliares sem
  estrela; os cinco da seção 11–12 ganharam a marca “(por definição)”.
- Duas notas de leitura sem falha: em `nas_tres_casas_passa_…` (l.1476) o `g` exibido compara o assento com
  `ρ x0` (a página original), não com `ρ r0` — iguais sob a hipótese `h0`; e o “(a)” da l.1461 (achado 7 acima).

## O cabeçalho lê o operador além da letra? As citações conferem por bytes?

Não encontrei leitura além da letra. As atribuições ao operador ou são citadas por bytes ou vêm marcadas como
leitura da gerência com proveniência declarada (a mensagem das 08:30: cópia na pasta privada; a leitura das 07:5x:
marcada como não entregue e superada). Citações em aspas angulares: 24, uma por linha; as 24 são subcadeia exata,
por bytes, de arquivo de `work\cunhagens_13out\`, e a data atribuída bate com a data do nome do arquivo (script
`U3_Kimi\checar_citacoes.py`; saída em `U3_Kimi\log_citacoes.txt`). Incluídas as três falas de 16/11 (06:59, 07:00,
07:06), a das 07:50 e a das 08:30, e as de 25/10, 17/10, 22/10, 26/09, 10/11 e 15/11. O único deslize de referência
é de nome do kernel, não da letra: achado 1.

## O que conferi (com o log da recompilação)

1. **Recompilação em cópia própria** (`U3_Kimi\compilacao\CopiadorEImpostor.lean`, sha256 = o da REV16; script
   copiado; saída só na minha pasta). Log: `U3_Kimi\compilacao\build\CopiadorEImpostor.log` — FONTE com o sha256
   `815b6334…`, LEAN 4.31.0 (commit 68218e87), INÍCIO 16:19:29, FIM 16:20:09, **RC 0**; a SAIDA traz só as 118
   respostas dos #print axioms; busca por `warning|error|sorry` no log: zero; `.olean` produzido (1.192.768 B).
   Confronto com a gerência: **saída zero ✓, sem aviso ✓, 118 teoremas ✓** (118 declarações `theorem`, 118
   `#print axioms`, nomes idênticos; zero `lemma`/`example`/`axiom`/`native_decide`; zero `sorry` fora de
   comentário), **só o trio ✓** (41 teoremas sem axioma algum; 77 dentro de subconjuntos de {propext,
   Classical.choice, Quot.sound}; zero sorryAx). Os axiomas por teorema do meu log são idênticos, um a um, aos do
   `RESULTADO_CopiadorEImpostor.json` da gerência (que mede a R8 — achado 5). Definições: 21 `def` + 1 `structure`
   = os 22 nomes do JSON.
2. **Os dez achados do T1**: itemizados acima, com as linhas da R7 e do desenho/partitura atuais.
3. **Seções 13 e 14**: lidas por inteiro, enunciado contra docstring; compilação própria cobre todos os termos.
4. **Cabeçalho e citações**: as 24 citações angulares conferem por bytes; a letra não é lida além do que se declara.
5. **Sonda de nomes do kernel** (`U3_Kimi\compilacao\SondaNomesKernel.lean`, só #check): 14 dos 15 nomes citados em
   prosa resolvem; o que falhou é o do achado 1. Usados como termos, todos os nomes do kernel já estão cobertos pela
   compilação da R7.
6. **Base R6**: 93 teoremas, 93 prints, 17 defs — como o T1 registrou; a R7 = R6 + 25 teoremas + 4 definições (as
   seções 13 e 14).

Estatutos desta revisão: termos e compilação [REAL no sandbox]; a leitura da letra e dos documentos é a do revisor,
distinta por construção. Nada instalado, nada escrito fora da minha pasta e deste relatório, nenhum provedor remoto.
