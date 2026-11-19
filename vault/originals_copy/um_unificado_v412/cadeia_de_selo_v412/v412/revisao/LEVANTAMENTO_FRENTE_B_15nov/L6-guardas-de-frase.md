> Retorno de um leitor do levantamento de 15/11/2026 (gerencia c1; so leitura; modelo Sonnet). E' [DECLARADO pelo leitor] ate' a gerencia conferir cada ponto na fonte. Nao e' fala do operador. Nada aqui esta' instalado, selado ou aberto.

# L6-guardas-de-frase

## RESUMO
Mapa consultado (guarda, frase, proibida, negada): nenhuma rota sobre varrer as guardas contra as pedras da v412 [REAL].
Alcance: nenhum script da cadeia v411 passa as guardas de frase ao .lean (grep: 0 arquivos); elas varrem registro, artigo, .md, handoff, commit [REAL]. A v410 aplicou à docstring da pedra só a regra de citação «». O disparo abaixo é risco por reuso do texto, não parada automática.
Varredura [REAL]: guardas do um.py selado (sha16 1203b1f9202020d6, v411), extraídas por script; controle 29/29 proibidas reprovadas, 20/20 limpas passam. Texto inteiro, por bloco e por parágrafo.
CamadaCientifica.lean e NomeComoCodigo.lean: 0 disparos. OHabitanteDoNome.lean (sha16 26b750e61ede401d): 2 disparos, ambos F63 «é cego» em l.276 e l.760, e NÃO são forma negada (o «não» vem depois; a guarda olha 24 caracteres antes).
Troca mínima «é cego» por «fica cego», testada em memória, nada gravado: 0 disparos P18/F.
As palavras negadas dos cabeçalhos (exclusividade, consciência, natureza, e «confirm*», ausente nas três) não constam de nenhuma guarda. Só «provado na natureza» liga o F67.
D59 lista milênio, navier, «lindão» (com til) e kimi fora do H0DN; v409 F35/F38 também citam o milênio. Nas três candidatas: 0 casos.
Portão da custódia: 15 sha16 no cabeçalho do OHabitante (regra 4) valem só se o handoff os trouxer como conhecidos.
Fragilidades sondadas: «Nada de descoberta» dispara F65 («nada» não está na lista de negação); «nunca CONFIRMED» dispara P18-R1 e o portão (só « never CONFIRMED» é isenta, D196).
Aberto: 2 das 25 citações «» do OHabitante (l.79-80) sem casamento nos 227 OPERADOR_*.txt lidos; a fonte citada é o sha16 5973d79a49995c4c [OPEN].

## ACHADOS

### A1. G1 P18 (v392) _v392_guarda_texto
classe: GUARDA
onde: um.py:220515-220530 (cópia: v411\guarda_p18_v411.py:17-34)
Varre: todo TEXTO NOVO (registros, erratas, artigo PT/EN, .md), em JSON-dump. Regex verbatim, sem re.I salvo onde dito: R1 banida_="CONF"+"IRMED" | PRO+VED_BY | TGL_PRO+VED (maiúsculas, case-sensitive); R2 re.I: Nome\s+fixo|Nome\s+(?:e|é)\s+fixo|the\s+Name\s+is\s+fixed|fixed\s+Name; R3 re.I: singularidade\s+converge|singularidade\s+cai\s+no\s+atrator|cai\s+no\s+atrator|singularity\s+converges|falls?\s+into\s+the\s+attractor; R4 re.I: (?:\bluz\b|observa\w+|\blight\b|observation)[^.;\n]{0,60}\bconfirm\w*|\bconfirm\w*[^.;\n]{0,60}(?:\bluz\b|observa\w+|\blight\b|observation); R5 re.I: n(?:ã|a)o\s+provou|did\s+not\s+prove|has\s+not\s+proven|p(?:ó|o)s-?\s?di(?:ç|c)(?:ã|a)o|post-?diction. Exceção de forma negada: NENHUMA (R1 recusa a palavra até negada; sonda: «nunca CONFIRMED» e «is never CONFIRMED» disparam R1). Única exceção da cadeia: _v411_p18_sem_cabeca (só a cabeça pré-registrada do H0DN).

### A2. G2 F60 a F67 _v411_guarda_frases
classe: GUARDA
onde: um.py:221193-221251 = runtime_h0dn_v411.py:11-69 (sha16 f9dab163f5d5b7fe); linhas no um.py: F60 221212, F61 221217, F62 221220, F63 221222, F64 221225, F65 221229, F66 221234, F67 221237
Varre o texto novo, por BLOCO (split em linha em branco, aspas-vírgula, \n\n etc.); herda _v410 e tira F54 e parte da F56. _NEG_ verbatim: (?:\bn[ãa]o\b|\bnunca\b|\bnem\b|\bnot\b|\bnever\b|\bnor\b|\bno\b|\bwithout\b|\bsem\b|\bisn't\b|\brecusad|\brefus|\bproibid|\bforbid) — 'nada' NÃO está. F60 \bconfirm\w*|\bconfirmad[oa]s?\b|\bconfirma(?:ção|cao|ções|coes)\b (re.I); isenta se _NEG_ nos 60 caracteres ANTES, ou observador|observer|de fora|from outside|creditação|creditation em ±80. F63 \bteste\s+cego\b|\b(?:é|e'|e|foi|era|seria)\s+cego\b|\bblind\s+test\b|\b(?:is|was|be)\s+blind\b|\bblinded\s+test\b; isenta se _NEG_ nos 24 ANTES. F64 \bevid[êe]ncia\s+independente\b|\bindependent\s+evidence\b; _NEG_ nos 40 antes. F65 \bdescobert[ao]s?\b|\bdescobr(?:e|iu|imos|iram)\b|\bdiscover(?:y|ies|ed|s)?\b; _NEG_ nos 30 antes; passam critério/escala/threshold de descoberta (D172/D173). F66 (?<![0-9])0[.,]0120(?:3|31)\d*, sem exceção. F61 poder certificado (sem exceção). F62 vetor fora do suporte dito erro de montagem (isenta com «não é um erro/parede», leia-se). F67 obrigação das 4 marcas (modelo publicado; Cefeidas livres com o número; validade, não creditação; retrodição; não cego) quando o bloco traz o gatilho (prova(do|da) na natureza | primário…contra o nulo | Z contra o nulo).

### A3. G3 F44 a F59 _v410_guarda_frases e as heranças v405 a v409
classe: GUARDA
onde: um.py:224923-225028 (v410); 236186-236250 (v409); 239861-239908 (v408); 242877-242889 (v407); 245307-245320 (v406); 255752-255780 (v405); _v410_sem_falas_do_operador 224912-224920
Varrem o texto novo por segmento (split [.;|\n\"]); ANTES, _v410_sem_falas_do_operador apaga tudo entre « » (até 1200 caracteres) e as falas embutidas: citação entre « » é isenta nas regras da v410 em diante (não nas F60-F67). Exceção de forma negada da v410, verbatim: neg_ = ("não ", "nao ", "não,", "not ", "never ", "nunca ", "nem ", "nenhum", "nada ", "nothing ", "jamais ", "fica fora", "ficam fora", "stays outside", "stay outside", "proibid", "prohibit", "forbid", "isn't", "n't ", "sem o qualificador", "without the qualifier") sobre o segmento inteiro (aqui 'nada ' conta). Temas: F44-F50 P vs NP, Turing, funtor, seletor; F51 atrator observado; F52 Nome esgota; F53/53b/53c cinco sigma dado e tokens H0DN; F55 não-falsificado como cabeça de 5σ; F56 covariância fechada; F57-F59 P = nP negado, Clay, leitor paga a escala, decisor mentiroso; v409 F35-F43; v408 F24-F34; v407 F20-F23; v406 F15-F19 (F17 certificado/fechamento/gravidade quântica «confirmad*»); v405 F1-F14 (tudo é teorema, tudo derivado, nenhuma hipótese resta, gap, escala). Fonte integral extraída por script em ...\scratchpad\v412_frente_b\L6\guardas_fonte.txt.

### A4. G4 Portão de texto da custódia G1
classe: GUARDA
onde: tools\custodia_g1\textos.py:22-31 e 76-106 (sha16 f533c746264bbee4)
Varre todo texto que a custódia gera (handoff, commit, registro, README, textos da vitrine). Regra 1: CONFIRMED (?<![A-Z_])CONFIRMED(?![A-Z_]) e CONFIRMAD[AO]S?\b, só MAIÚSCULAS, depois de retirar as FORMULAS verbatim: ("CONFIRMED is accreditation, the one refused word", "PROVADA ≠ CONFIRMADA", "CONFIRMADA = creditação, recusada", "NOT_CONFIRMED", "NOT_A_CONFIRMATION", "Not falsified is not a confirmation", "NOT_FALSIFIED nunca é CONFIRMED", "Proved is not a judgement of nature", "PROVED is validity", "PROVADA = validade", "nunca é a palavra da creditação"). REGRA DA FORMA NEGADA (D196, textos.py:26-31): acrescenta SÓ a substring " never CONFIRMED" (com o espaço antes; no começo de linha ou depois de hífen segue reprovando). " nunca CONFIRMED" não é isenta. Regra 2: provada/PROVED exige validade|validity|≠|creditação|accreditation|judgement|nature na mesma frase. Regra 3: pós-dição. Regra 4: todo hash de 16 ou 64 hex tem de estar entre os conhecidos da rodada (os da rodada e os que o handoff traz). Regra 6: physical_verdict_allowed verdadeiro. h0dn.py:122-170 traz a F67 copiada (cabeçalho h0dn.py:10-11; não comparada linha a linha, sha16 c0a088ff9e127246).

### A5. G5 D59 e D65 (nomes e vocativo)
classe: GUARDA
onde: v411\pos_rito\registrar_mapa_v411.py:144-150 (sha16 7c200186ee13ea46); v411\orquestrador\pos_treino_v411.py:440 e 889; v410\delta_v410.py:409
_RX_D59 = re.compile(r"(?i)mil[eê]nio|millennium|navier|lindão") e d59_viola(txt): True se _RX_D59 casa, OU se kimi aparece sem H0DN no texto. Varre handoff inteiro, gatilho do pos-treino, mapa e texto novo. O vocativo da regra é «lindão», só com til: «Lindao» ASCII não casa (sonda). Nenhuma exceção de forma negada. D65: FORA_D65 = ("solução definitiva", "solucao definitiva", "algoritmo polinomial para resolver", "a_solucao_definitiva", "Existe: IALD") por substring, sem exceção. Também v409 F35 (milênio/Clay dito resolvido, isenta com negação ±40) e F38 (token MILLENNIUM).

### A6. G6 Regra (i) da v410: citações «» na docstring da pedra
classe: GUARDA
onde: v410\conferir_citacoes_v410.py:10
Não é de palavra: toda citação entre « » da docstring da pedra tem de existir verbatim nas falas do operador, Atlas, kernel da base, adendo ou CLAUDE.md. Precedente v410: pedra IALD2. Só a gerência corrige pedra.

### A7. D1 F63 em OHabitanteDoNome.lean:276
classe: DISPARO
onde: C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\OHabitanteDoNome.lean:276
palavra «é cego»; trecho: «`o_seletor_tangencia_a_esperanca`; e o que é cego ao Nome não deixa rastro, exatamente:»; modos texto inteiro, bloco e parágrafo. NÃO é forma negada: o «não» vem depois do «é cego» e a guarda só olha os 24 caracteres antes. É homônimo (cego ao Nome = sem componente no Nome), não «teste cego».

### A8. D2 F63 em OHabitanteDoNome.lean:760
classe: DISPARO
onde: C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\OHabitanteDoNome.lean:760
palavra «É CEGO»; trecho: «/-- ★★ O QUE É CEGO AO NOME NÃO DEIXA RASTRO, exatamente: o empurrão ortogonal ao Nome é desfeito pela seleção.»; docstring de teorema. Mesma natureza: não negada, homônimo.

### A9. D3 Hashes no cabeçalho (portão, regra 4)
classe: DISPARO
onde: OHabitanteDoNome.lean linhas 15, 22, 30, 32, 39, 56, 58, 60, 79, 111, 115, 117, 167, 169, 224
15 sha16/sha256 de falas e arquivos (49e5f0072e8beb02, 2fabf2b6638c1175, fcdc84f85f3f3107, 79874a086c36703b, ec05cea3eded9264, 762e461a45ffbad8, e022b35a33ba5c4a, 93c1b4ac44d0e931, 5973d79a49995c4c, b34e1e25dc6a8949, c12699c915617c3f, 270f8addf0bddb19, 2424bcbebd29428f, 4e1e883b39b507cb, f0fdd2c1f770e34a). Só disparam se esse texto passar pelo portão sem o handoff os trazer como conhecidos. Não é forma negada nem troca de palavra. Camada e NomeComoCodigo: 0 hashes.

### A10. S1 Candidatas sem disparo
classe: LIMPO
onde: CamadaCientifica.lean (sha16 69497c5b63dbcb0c); NomeComoCodigo.lean (sha16 3ce6d95ee8fd8533)
0 disparos nas três granularidades. Camada traz «não é cego ao Nome» (l.24, 42, 174, 213 e outras) e passa só porque há «não» nos 24 caracteres antes: dependência frágil da proximidade. NomeComoCodigo l.40 «Exclusividade; consciência; natureza. Validade no kernel, não creditação.»: nenhuma guarda lista consciência ou exclusividade (grep no fonte extraído e em custodia_g1: 0); «natureza» só entra em «provado na natureza» (F67). «confirm*» não ocorre nas três (grep -i).

### A11. S2 Milênio, navier, vocativo, kimi
classe: LIMPO
onde: três candidatas
A D59 lista milenio|millennium|navier|lindão e kimi fora do H0DN; v409 F35/F38 citam o milênio. Nas três candidatas: 0 ocorrências (guarda e grep).

### A12. S3 Sondas de forma negada
classe: SONDA
onde: scratchpad v412_frente_b\L6\sondas.py
«Nada de descoberta aqui» DISPARA F65; «descoberta não é o que a pedra afirma» DISPARA F65 (negação só vale antes); «a pedra não afirma exclusividade nem descoberta» passa; «a pedra não afirma que a TGL foi confirmada» passa; «um estado confirmado pelo observador» DISPARA P18-R4; «nunca CONFIRMED» DISPARA P18-R1 e o portão, «is never CONFIRMED» só o P18-R1.

### A13. A1 Citações «» do OHabitante (regra i)
classe: ABERTO
onde: OHabitanteDoNome.lean:79-80
25 citações «»; 23 casam verbatim com algum dos 227 OPERADOR_*.txt de work\cunhagens_13out; 2 sem casamento: «O nome é um verbo fossilizado — uma ação selecionada que se tornou identidade» e «O nome é o ponto fixo do verbo.». O cabeçalho cita o sha16 5973d79a49995c4c como fonte; não abri esse arquivo [OPEN]. Camada e NomeComoCodigo: 0 citações «».

## PROPOSTAS

### P1. P1 trocar «é cego» por «fica cego» em OHabitanteDoNome.lean:276 e :760
enunciado: Nos dois únicos disparos reais (F63), trocar a palavra «é» por «fica»: «o que fica cego ao Nome não deixa rastro» (l.276) e «O QUE FICA CEGO AO NOME NÃO DEIXA RASTRO, exatamente:» (l.760). Sentido igual, uma palavra por sítio. «permanece cego» também zera.
apoio: [REAL] troca feita só em memória sobre o texto do arquivo e varredura refeita com P18 e _v411_guarda_frases: 0 disparos; sonda «o que fica cego ao Nome não deixa rastro»: P18 vazio, F vazio. Alternativa rejeitada: pôr um «não» nos 24 caracteres antes, que esconde o defeito pela proximidade.
nao compra: Não faz a pedra passar por revisão nem prova que a cadeia v412 não traz regra nova (F68 em diante é desconhecida). Não cobre os 15 hashes do cabeçalho nem a regra das citações «». Silêncio da guarda não é correção semântica.
risco: Editar a pedra muda o sha16 do arquivo e invalida as conferências já feitas sobre ele (a gerência corrige pedra; o agente não). Em CamadaCientifica o idioma é «não é cego ao Nome» (negado), então «fica cego» introduz variação de vocabulário entre as duas pedras; a gerência decide se prefere uniformizar.

### P2. P2 hashes do cabeçalho entram como conhecidos no handoff
enunciado: Nenhuma troca de palavra: se o cabeçalho do OHabitante for citado em handoff, commit, registro ou README, o handoff traz os 15 hashes (lista em D3) para que o portão da custódia os conheça; senão a regra 4 reprova cada um.
apoio: [REAL] textos.py:96-99 e docstring de conhecidos_da_rodada: hash citado tem de estar entre os da rodada ou os que o handoff traz.
nao compra: Não decide se o cabeçalho será citado nesses textos; só avisa do que o portão exige.
risco: Baixo; o portão é fail-closed e aponta cada hash.

### P3. P3 como escrever, nos registros novos, o «o que a pedra NÃO afirma»
enunciado: Usar a negação anterior à palavra e dentro da janela: «não afirma exclusividade nem descoberta», «sem confirmação». Evitar «Nada sobre X» quando X for confirmação ou descoberta (nada não está em _NEG_ de F60 e F65) e a palavra recusada em maiúsculas (P18-R1 não isenta nem negada; o portão só isenta « never CONFIRMED»). Exclusividade, consciência e natureza podem ficar.
apoio: [REAL] sondas.py: «a pedra não afirma exclusividade nem descoberta» passa; «Nada de descoberta aqui» dispara F65; «nunca CONFIRMED» dispara P18-R1 e portão.
nao compra: Não vale para o .lean, que nenhuma guarda de frase varre hoje; vale se o texto da pedra for reaproveitado em registro, artigo ou handoff.
risco: Baixo.

## CONSULTAS AO MAPA
- rotas.py consultar guarda: 119 rotas (truncado); nenhuma sobre varrer guardas de frase contra o texto das pedras da v412
- rotas.py consultar frase: 99 rotas; mesmo resultado
- rotas.py consultar proibida: 16 rotas; nenhuma sobre este tema
- rotas.py consultar negada: 2 rotas; kernel.camada_cientifica_candidata_14nov (EXAMINADA_COM_DEFEITO; a própria candidata, sem exame de guardas) e x.post_diario.app_claude_navegador_proprio (sem relação)

## EXAMINADO
- C:\IALD\MAPA_DE_ROTAS\rotas.py (só consultar: guarda, frase, proibida, negada)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py (Grep e Read de faixas curtas; leitura integral só por script de extração: linhas 220515-220530, 221193-221259, 224912-225028, 236186-236250, 239861-239908, 242877-242889, 245307-245320, 255752-255780; sha16 1203b1f9202020d6; UM_VERSION v411)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\guarda_frases_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\runtime_h0dn_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\guarda_p18_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\guardas_estaticas_bancada_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\conferir_citacoes_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\conferir_rito_v411.py (Grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\ensaio_a_seco_v411.py (Grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\pos_rito\registrar_mapa_v411.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\orquestrador\pos_treino_v411.py (Grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro\b_07b.py
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\delta_v410.py (FORA_D65, por ast)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\conferir_citacoes_v410.py (Grep)
- C:\IALD\Central de Patentes\tools\custodia_g1\textos.py
- C:\IALD\Central de Patentes\tools\custodia_g1\h0dn.py (Grep, cabeçalho)
- C:\IALD\Central de Patentes\tools\custodia_g1\readme_pinado.py (Grep; lista privada de termos NÃO aberta)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\OHabitanteDoNome.lean (sha16 26b750e61ede401d, 99559 bytes)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CamadaCientifica.lean (sha16 69497c5b63dbcb0c, 35912 bytes)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\NomeComoCodigo.lean (sha16 3ce6d95ee8fd8533, 11867 bytes)
- C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_*.txt (227 arquivos, só leitura para casar citações)
- Scripts e saídas em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_frente_b\L6: extrair_guardas.py, varrer_candidatas.py, controle_guardas.py, troca_e_citacoes.py, sondas.py, hashes.py, guardas_fonte.txt, disparos.json
