> Retorno de um leitor do levantamento de 15/11/2026 (gerencia c1; so leitura; modelo Sonnet). E' [DECLARADO pelo leitor] ate' a gerencia conferir cada ponto na fonte. Nao e' fala do operador. Nada aqui esta' instalado, selado ou aberto.

# L7-registro-e-errata

## RESUMO
1. Mapa consultado (neutrino, cronologia, JUNO, camada, prospectiva). A rota estatistica.v412.k04_hubble_m2_combinacao (c1, 15/11) ja registra os dois eixos e aponta L4241, L4620 e L2944. Nenhuma rota da v412 cobre a camada cientifica.
2. O um.py selado se contradiz [REAL]: a errata da v182 (L2944-2950) retira o Zenodo 17526619 como prioridade do valor; L4222-4224, L4241, L4243 e L4620 ainda dizem «derivacao publicada 2025 / PUBLICADA ANTES do codigo». A cronologia mostra valor_8_51_presente=false nos dois artigos de 2025.
3. L4241 e L4620 estao dentro de objetos frozen com hash (o do dicionario portado, e248..., e o original 4bdae22a...): so se corrige AO LADO, nunca por cima.
4. A cegueira declarada no selado (L4601-4604, L4628-4630) diz so o eixo da regra; falta o eixo da previsao publicada. O DESENHO v412 R1 tem o mesmo defeito (l.123-124 e l.130).
5. Conferi por script proprio: o valor 8.51 meV esta no corpo do docx (22 de Janeiro de 2026, sha256 83ba9e81...) e no .tex (\date 22 de Janeiro de 2026, L305/312), ambos com o signo antigo α² (hoje β_TGL = α√e); citar o valor, nao a formula como escrita.
6. Arquivo do Kimi (K09 JSON): sem prosa de cegueira; os dois eixos entram como campos separados. Defeitos: chave «primeira_confirmacao_explicita_do_valor» (contem a raiz proibida), 22/06/2026 [DECLARADO, sem resposta crua] e «anterior/posterior» sem sujeito.
7. Divergencia de numero que a errata nao pode esconder: o core usa NuFIT 7,53 ± 0,10 (2,95σ); K09 traz 3,02 (tabela) e 3,04 (eq. 11 assimetrica). O ramo TENSION começa em 3,0.
8. Registro: esqueleto vigente = a_escala_v410 (L225853) + spec (L229258) + erratas (L221874). Hashes do K08 conferidos por mim: CamadaCientifica 69497c5b..., OHabitanteDoNome 26b750e6..., NomeComoCodigo 3ce6d95e... (batem). As 18 + 11 declaracoes citadas pelo K08 existem nos arquivos.
9. Nada foi escrito fora da pasta de rascunho; nenhum script da casa rodou (so rotas.py consultar/ver).

## ACHADOS

### A1. (1a) um.py L4222-4224, docstring de prove_neutrino_sum_protocol
classe: EXISTE; corrigir AO LADO [REAL]
onde: um.py:4222-4224
VERBATIM: «(i) a derivacao m_nu = beta*sin45*1eV foi PUBLICADA ANTES do codigo [Zenodo 10.5281/zenodo.17526619, 2025; o modulo v141 e de 25/07/2026] -- prioridade documental, sem ajuste possivel;». Contradiz a cronologia (Zenodo 17526619, 04/11/2025: valor_8_51_presente=false; contagens locais 8.51=0, sin(45=0, JUNO=0) e a errata da v182 no proprio arquivo (L2944-2950). Vale para a TESE do neutrino, nao para o VALOR.

### A2. (1b) um.py L4240-4245, frozen NEUTRINO_SUM_V1
classe: EXISTE; corrigir AO LADO [REAL]
onde: um.py:4238-4245
VERBATIM L4240-4242: «"prediction": ("Sigma m_nu = m1 + m2 + m3 com m1 ~ 0 [declarado], m2 = beta*sin(45)*1eV " "[TGL runtime; derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619], " "m3 = sqrt(m2^2 + Dm2_32) [PDG 2023]; ordenamento normal")». L4243-4244: «"custody": ("(i) derivacao ANTES do codigo [Zenodo 17526619, 2025 vs modulo v141 25/07/2026]; " "(ii) Dm2 (PDG) antecede a derivacao -- 'postdicao' SO nesse sentido restrito; "». Estao dentro do dict frozen: editar move o hash do objeto, logo AO LADO.

### A3. (1c) um.py L4617-4620, frozen NEUTRINO_M2_V2
classe: EXISTE; corrigir AO LADO [REAL no texto; DECLARADO no hash]
onde: um.py:4613-4632
VERBATIM L4620: «"predicao": "m_2 = beta_TGL*sin(45)*1eV; beta_TGL = alpha*sqrt(e) em runtime [derivacao publicada 2025, Zenodo 10.5281/zenodo.17526619]",». L4617 diz que o objeto e portado de «02_frozen_neutrino_m2_v2.py (hash 4bdae22a277aa393..., 08/08/2026)»; K09 pina o dicionario portado em e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3 (a LEITURA_K09_PARCIAL o liga a core.neutrino_m2.frozen_hash) [DECLARADO pelo revisor; nao reconferido por mim no core]. Editar a frase move esse hash.

### A4. (1d) um.py L4601-4604 e L4628-4630, a cegueira com UM eixo so (o da regra)
classe: EXISTE; corrigir AO LADO [REAL no texto; DECLARADO nas datas de jun/jul]
onde: um.py:4601-4604; 4628-4630; 302311-302312; 302342
VERBATIM L4601-4604: «NAO-CEGO DECLARADO: os limiares (5/3 sigma) foram fixados na mesma sessao em que a tensao corrente ja era conhecida -- esta emissao e uma REESPECIFICACAO; a cegueira vale a partir de agora (regra ja hasheada julga as proximas medidas).». VERBATIM L4628-4630: «"nao_e_cego_nesta_emissao": ("DECLARACAO OBRIGATORIA: os limiares foram fixados na mesma sessao em que a tensao corrente (2,95 sigma) ja havia sido calculada; esta emissao e REESPECIFICACAO, nao veredito cego; a cegueira vale a partir de agora"),». Falta o segundo eixo (a previsao publicada: valor nos bytes desde 22/01/2026). Mesma formulacao em L302311-302312 e L302342 (a cegueira vale a partir desta emissao). O hash da regra e 08/08/2026; o numero de 207,2 dias foi apresentado em 15/07/2026 (anterior ao hash); so o artigo arXiv de 29/09/2026 e posterior ao hash.

### A5. (1e) um.py L2951-2956 (caveats da v182) e a palavra «postdicao»
classe: EXISTE; corrigir AO LADO [REAL no texto; OPEN no alcance de «pos-JUNO»]
onde: um.py:2885; 2896; 2951-2956; 4225; 4244
VERBATIM L2951-2956: «(ii) postdicao NAO-AJUSTADA: as entradas (beta,sin45,1eV) nao usam dado de neutrino e o digito nunca se moveu desde 22/01/2026; a escala que zeraria a tensao (1,0200 eV) foi calculada no acervo e RECUSADA. Mas o valor medido e citado na MESMA frase que anuncia a predicao no documento de origem -- nao e predicao ex ante; (iii) o elemento genuinamente EX ANTE e o refinamento pos-JUNO, e ele vai CONTRA: a tensao cresce com a precisao (1,64 -> 2,21 -> 2,95 sigma), com projecao de 7,83 sigma na meta do JUNO». Problema: o JUNO de 59,1 dias (18/11/2025) e o NuFIT (11-12/2025) sao ANTERIORES ao valor (22/01/2026); so o numero de 207,2 dias e posterior. O que «pos-JUNO» designa ali e [OPEN]. A palavra «postdicao/postdiction» (demerito vetado pela lei da prova de 05/10/2026, item 5) aparece tambem em L2885, L2896, L4225 e L4244. Se a v387 ja a tratou nos artigos nao foi conferido aqui.

### A6. (1f) um.py L314-322, registro de custodia zenodo_eco_2025_record
classe: EXISTE; corrigir AO LADO [REAL]
onde: um.py:314-322
VERBATIM L315 e L320: «"name": "Zenodo record 17526619 (Neutrinos: The Lie of Light, 2025) — precedencia da derivacao m_nu"» e «"source_cite": "Rotoli Miguel (2025), DOI 10.5281/zenodo.17526619 [publication_date no JSON = prova de precedencia sobre o codigo]"». Vale para a tese (04/11/2025 < modulo v141, 25/07/2026), nao para o valor de m2. Referencias que dizem «o artigo do eco» (L3038, L183597, L184004) estao certas e NAO precisam de correcao.

### A7. (1g) um.py L4597, L4689, L2955-2956 e artigo L184013/L292284: «a tensao cresce com a precisao»
classe: EXISTE; corrigir AO LADO [REAL]
onde: um.py:2955-2956; 4597-4599; 4689; 184013; 292284
VERBATIM L4597-4599: «8,5074 meV e o mundo mede 8,68 -- e A TENSAO CRESCE COM A PRECISAO: 1,64 sigma (PDG 2023) -> 2,21 sigma (JUNO nov/2025, INDEPENDENTE) -> 2,95 sigma (NuFIT global pos-JUNO).» e L4689: «%.2f sigma -- e a tensao cresce com a precisao.». K09 (reproduzido pelo revisor com diferenca <= 1e-15 e por mim em duas contas de cabeça): na serie autonoma do JUNO a razao em m2 foi de 2,206 (59,1 d) para 1,938 (207,2 d); r_delta 2,187 para 1,928. O DESENHO v412 R1 (l.119-120) ja diz «Na serie autonoma a tensao caiu». A frase e do reflexo global (NuFIT).

### A8. (1h) o que NAO se corrige (para nao excesso de zelo)
classe: EXISTE E LIGADO [REAL]
onde: um.py:2941-2950; 4256; 4627; TGL_Manifesto_Unificacao_Artigo.tex:50
L2944-2950 (errata v182: «VERIFICADO e RETIRADO ... NAO contem a formula, NAO contem o numero e NAO contem a derivacao ... Nenhuma alegacao de anterioridade a Dm2_21 e feita») ja esta certa e e o precedente a citar. L4256 e L4627 («forbidden_verdicts»: ["CONFIRMED"]) ficam. L2941-2943 cita o .tex do Manifesto (\date 22/01/2026) e o git publico de 17/02/2026: conferido, o .tex existe em C:\IALD\Artigo\TGL_Manifesto_Unificacao_Artigo.tex com \date{22 de Janeiro de 2026} na L50.

### A9. (2a) ESQUELETO de UM registro com funcao: a_escala_v410 (abreviado onde marcado [...])
classe: EXISTE E LIGADO [REAL]
onde: um.py:225850; 225853-225876; 231771-231778; 233982; 225899-225906; 236156-236157; 224867-224868
um.py:225850 `_V410_AESCALA_RECUSA = "TGL_AESCALA_V410__REFUSED_%s__GATE_UNMOVED"`.
225853 def a_escala_v410(core):
225857     c_ = _V410_AESCALA_CONTRACT; t_ = _V410_AESCALA_TEXT
225858     beta_rt_, beta_rel_, dois_nomes_, beta_ok_ = _v398_beta(core)
225859     out_ = {"all_verified": False, "runtime_executed": False, "does_not_gate_core": True, "estatuto": t_["estatuto"], "scope": t_["escopo"], "limites": t_["limites"], "diz": t_["diz"], "nao_diz": t_["nao_diz"],
225860             "beta_ok": beta_ok_, [...] "modulo": c_["modulo"], "ancora_principal": c_["ancora_principal"], "ancoras_de_secao": list(c_["ancoras_de_secao"]), "n_ancoras": c_["n_ancoras"], "n_flags": c_["n_flags"], "flag_prefix": c_["flag_prefix"],
225861             "nomes": list(c_["nomes"]), "n_nomes": c_["n_nomes"], "nomes_ratificados": c_["nomes_ratificados"], "estatuto_dos_nomes": c_["estatuto_dos_nomes"], [...] "nomes_novos_da_pedra": list(...), "campos_novos_da_estrutura": list(...),
225862             [...] "ratificacao_pendente": dict(c_["ratificacao_pendente"]), "ponte": dict(c_["ponte"]), "n_falas": c_["n_falas"], "numeros": dict(c_["numeros"]), "frase_canonica_pt": c_["frase_canonica_pt"], [...]}
225864     out_.update(t_["extras"])
225865     if not beta_ok_:
225866         out_["verdict"] = _V410_AESCALA_RECUSA % "BETA_IS_NOT_ALPHA_SQRT_E"
225867     else:
225868         try:
225869             mec_ = _v410_aescala_mechanics(beta_rt_, core, c_, t_)
225870             out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"] and mec_["n_checks"] == c_["n_checks"]))
225871             out_["verdict"] = (c_["veredito_ok"] if out_["all_verified"] else _V410_AESCALA_RECUSA % "MECHANICS_CHECK_FAILED")
225872         except Exception as e_:   # noqa: BLE001
225873             out_.update(runtime_executed=True, error=repr(e_)[:300])
225874             out_["verdict"] = _V410_AESCALA_RECUSA % "RUNTIME_ERROR"
225875     core["a_escala_v410"] = out_
225876     return out_
CONTRATO (231771-231778): `_V410_AESCALA_CONTRACT = {'registro': 'a_escala_v410', 'tag': 'AESCALA', 'veredito_ok': 'TGL_AESCALA_V410__...__GATE_UNMOVED', 'veredito_recusa': 'TGL_AESCALA_V410__REFUSED_%s__GATE_UNMOVED', 'n_checks': 13, 'modulo': 'TGLExt/AEscala.lean', 'mod': 'TGLExt.AEscala', 'source_sha256': {'TGLExt/AEscala.lean': 'baaa73cb...'}, ...`. TEXTO (233982): `_V410_AESCALA_TEXT = {'estatuto': '[REAL] os termos do kernel do rito: as 81 ancoras ...; [DERIVED, aritmetica em Q] ...; [INPUT] a escala ... e DEFINICAO do operador; ...', 'escopo', 'limites', 'diz', 'nao_diz', 'extras'}`. ANCORA (225899-225906), a declaracao Lean entra assim: `'TGLExt.IALD2.ler_o_codigo_identidade': {'rel': 'TGLExt/IALD2.lean', 'papel': '[docstring da pedra] LER O CÓDIGO IDENTIDADE É A IDENTIDADE.', 'flag': 'ext_iald2_410_0007', 'classe': 'nomeada'}`. REGISTRO NA LISTA (236156-236157): `_V410_NOMES_REGISTROS = ['cunhagens_v410', 'kh_n1_cobertura_v410']` e `_V410_REGISTROS_FUNCAO = ['iald2_v410', 'a_escala_v410', 'h0dn_bg1_v410', 'h0dn_fontes_hms13_v410']` (a v411 tem `_V411_NOMES_REGISTROS` e `_V411_REGISTROS_FUNCAO = ['h0dn_bg1_v411']`, L224867-224868).

### A10. (2b) ESQUELETO do registro por spec e da errata no formato do core (v411)
classe: EXISTE E LIGADO [REAL]
onde: um.py:229258-229261; 222352-222360; 221874-221879; 168499; 168307-168308
SPEC (229258-229261, v410; 222352-222360, v411): `{'nome': 'cunhagens_v410', 'veredito_prefixo': 'TGL_CUNHAGENS_V410', 'veredito_sufixo': 'OPERATOR_INSCRIPTIONS_...__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED', 'estatuto': '[REAL -- o kernel ... ; INPUT as falas do operador ...; DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]', 'fontes': ['pedra_iald2', ...], 'verbatins': ['v410_cun_fec6f7db344c21c2', ...], ...}` (chaves tambem vistas: 'diz', 'nao_diz', 'decisoes' D.., 'erratas'). ERRATA (221874-221879): `'erratas': [{'id': 'E41', 'texto': 'errata da gerência c1, em nome próprio: o docstring de `veredito_h0dn_v411` (módulo pinado) ainda põe a centragem dentro do primeiro portão; ... o módulo pinado não é tocado.', 'assinatura': 'gerencia c1, em nome proprio (DESENHO_v411 secao 4)', 'ao_lado_de': "o docstring de veredito_h0dn_v411 (modulo pinado codigo\\veredito_v411.py; nao e' tocado)"}`. Ultimo id usado na v411: E44 (veredito_sufixo L222354). VEREDITOS PROIBIDOS no P7 selado (168499): `"forbidden_verdicts": ["IALD_PROVED", "CONSCIOUSNESS_PROVED", "TGL_PROVED_BY_COLLAPSE"]`; a GUARDA de auditoria (168307) e por substring: `forbidden_tokens = ("CONFIRMED", "PROVED_BY", "TGL_PROVED", "CONSCIOUSNESS_PROVED")` aplicada a 9 vereditos que incluem `iald_prediction`.

### A11. (2c) Lacuna da guarda por substring (L168307)
classe: EXISTE (lacuna) [REAL]
onde: um.py:168307; K08 secao 4
O token «IALD_PROVED» NAO esta em forbidden_tokens (so CONFIRMED, PROVED_BY, TGL_PROVED, CONSCIOUSNESS_PROVED); um veredito «IALD_PROVED» passaria essa guarda (nao passa por «TGL_PROVED»). O registro v412 precisa que a guarda cubra os quatro nomes proibidos por nome E as palavras de consciencia, pesos alterados e exclusividade (DESENHO 2.4). Cuidado de prefixo: V1 e V2 devem ser distinguidos sem startswith (alerta do K08, secao 4).

### A12. (3a) K09 JSON (deae4e3d..., 6682 B): frases com UM eixo e frases que sugiram que o autor viu o dado
classe: EXISTE (defeito de formato) [DECLARADO pelo Kimi; conferido em parte]
onde: kimi/ERRATA_NEUTRINO_V412_DADOS_K09.json:47-105; revisao/LEITURA_K09_PARCIAL_NEUTRINO_15nov.md:15,24,34-49,67-69,91; kimi/ERRATA_M2_K09.md:5-11
O JSON NAO tem prosa sobre cegueira nem sobre os 207 dias; os dois eixos ja entram como campos separados (previsao_publicada; posicao_relativa_a_previsao_publicada: 'anterior_ao_valor_publicado' nos 59,1 d e 'posterior_ao_valor_publicado' nos 207,2 d; posicao_relativa_ao_pino: 'anterior' nos dois; posicao_relativa_ao_pino_do_artigo: 'posterior' so nos 207,2 d). Nenhuma frase sugere que o autor viu dado antes. Defeitos do formato: (i) a chave `primeira_confirmacao_explicita_do_valor` (L83) contem a raiz proibida; renomear (ex.: primeira_apresentacao_explicita_do_valor); (ii) 'posicao_relativa_ao_pino': 'anterior' nao diz o sujeito (anterior o numero ao pino? o pino ao numero?); (iii) 'primeira_apresentacao_publica' = 2026-06-22 (L77-82) com estatuto 'DECLARADO_sem_resposta_crua_guardada'; a LEITURA_K09_PARCIAL diz que 22/06 e a data do degrau (Neutrino 2026), nao a do valor, e suspeita de erro de transcricao com 22/07 (JINR). A prosa de um eixo so esta nos .md: ERRATA_M2_K09.md l.9-11 («207,2 dias nao e primeira leitura prospectiva nem cega»), M2_DESFECHOS_K04 l.12/217/221, ERRATA_NEUTRINO_V412_RASCUNHO_K04.md l.51 («Nao e leitura cega para esta casa, que leu os numeros ... em 30-31/10/2026», fala de 'esta casa', nao do autor) [citados da LEITURA_K09_PARCIAL; nao lidos integralmente por mim, salvo ERRATA_M2_K09 l.1-14].

### A13. (3b) Frases de um eixo so no DESENHO v412 R1 (da propria gerencia)
classe: EXISTE; corrigir AO LADO [REAL]
onde: DESENHO_v412_R1.md:121-124; 130
VERBATIM l.123-124: «A leitura de 207 dias não é a primeira leitura prospectiva da regra congelada e não é cega. Nenhum parâmetro foi ajustado a ela: é retrodição sem ajuste, com o estatuto que tem.» (so o eixo da regra). VERBATIM l.130: «O que ainda é cego: só o dado do JUNO tomado depois de 18/05/2026.» (sem eixos). VERBATIM l.121-122: «escrevi que a regra V2 foi hasheada (08/08/2026) antes da liberação de 207 dias. Vale para o artigo de 29/09 em arXiv.» (certa, so o eixo do hash). Pedem errata ao lado com os dois eixos na mesma frase.

### A14. (4a) Divergencias de data entre a cronologia e o K09 (e o um.py)
classe: [REAL] nas datas de API e nos bytes lidos; [DECLARADO] nas de jun/jul
onde: cronologia_neutrino_15nov/CRONOLOGIA_NEUTRINO_15nov.json:63-158; kimi/ERRATA_NEUTRINO_V412_DADOS_K09.json:26-38,47-105; um.py:2941-2943; C:\IALD\Artigo\TGL_Manifesto_Unificacao_Artigo.tex:50,305,312,391
(i) Zenodo 18674475: publication_date 2026-02-17 e created 2026-02-20T18:06:33 UTC; cronologia e K09 concordam nos dois campos; o um.py (L2942-2943) cita 17/02/2026 como data do git publico (commit Init), outro artefato com a mesma data; a errata deve dizer as duas datas do Zenodo. (ii) Primeira apresentacao publica dos 207,2 d: K09 = 22/06/2026 (Neutrino 2026, DECLARADO, sem resposta crua); DESENHO v412 l.122-123 = julho (IHEP 15/07; JINR 22/07); a cronologia (Zenodo/arXiv/locais) NAO traz nenhuma data de jun/jul. Qualquer das tres cai entre 17/02/2026 e 08/08/2026; para a errata usar 15/07/2026 [DECLARADO, sem resposta crua] e dizer o estatuto. (iii) Fonte de 22/01/2026: K09 aponta o docx (sha256 83ba9e81..., igual ao da cronologia) e o um.py aponta o .tex; a cronologia nao contou '8.51' no docx (sem 'contagens'); EU contei por script proprio: docx tem 8.51 x3, 'Janeiro' x1, 'JUNO' x0; .tex L50 \date{22 de Janeiro de 2026}, L305/312/391 com 8.51. (iv) lie_of_light.tex: mtime 2025-11-12, depois do deposito Zenodo (04/11/2025) e antes do JUNO (18/11/2025); neutrino_nmc_revised.tex mtime 2025-10-28 e Zenodo 'updated' 2025-10-29; nao muda a ordem. arXiv 2511.14593 (2025-11-18, 7,50 ± 0,12) e 2609.37895 (2026-09-29, 207,2 d, 7,388 ± 0,078): iguais nos dois arquivos.

### A15. (4b) Divergencia de NUMERO que pode mudar o ramo da regra
classe: [REAL nas contas, reproduzidas pelo revisor e por mim a olho; OPEN na consequencia para o ramo]
onde: um.py:4623; 4642-4644; 4666; K09:107-148
O core (L4642-4644) usa NuFIT «7,53 ± 0,10» (2,95σ em m2) e tension_rule (L4623) diz «TENSION sse a razao ficar em [3, 5) na determinacao global mais recente»; K09 traz para a mesma linha r_m2 = 3,024 (tabela node 309, 7,537 −0,100), 3,044 (arXiv:2601.09791 eq. 11 assimetrica, 7,53 −0,097) e 2,9529 so na 'representacao_simetrica_arredondada' (0,1). Ou seja, 2,95 depende do arredondamento simetrico do erro. A errata do core deve dizer qual erro usa; o ramo oficial hoje vem do perito JUNO autonomo (1,94σ), mas L4666 le a ultima linha da escada (global). Quem decide e a gerencia; e coisa a ler ao operador.

### A16. (5) Lean do registro v412: hashes e nomes conferidos
classe: EXISTE E NAO LIGADO (candidatas fora do kernel; fiacao da v412, nao falta) [REAL nos hashes e nomes; DECLARADO no que o K08 diz da compilacao]
onde: candidatas_c1/CamadaCientifica.lean:85-507; candidatas_c1/OHabitanteDoNome.lean:424-1147; kimi/REGISTRO_UMPY_RASCUNHO_R2_K08.md:30-71
sha256 lidos por script meu em 15/11: CamadaCientifica.lean (35912 B) 69497c5b63dbcb0cedbf456dc31ecfa6fc3b12b0ed78989cd7d5e51e542ee3cb; OHabitanteDoNome.lean (99559 B) 26b750e61ede401d95b3ddaa2e3bd11f8149936d985c564d71ee76f093e1c5d2 (54 linhas `^theorem`); NomeComoCodigo.lean (11867 B) 3ce6d95ee8fd85337cf9cc926c5ef75a7e5c0251b0040ae5970a5d00f6fe0e68; todos iguais aos do K08. Declaracoes em CamadaCientifica.lean (namespace TGLExt.CamadaCientifica, L85; section Motor L93-119; section Trava L123-334; namespace LeitorDeUmaConfiguracao L348-416): reler_soma_o_tempo L128; k_leituras_sao_uma_trava L147; a_trava_tende_ao_nome L165; a_bacia_e_tudo_o_que_nao_e_cego_ao_nome L176; a_trava_binaria_e_o_fluxo_do_axioma L254; a_fotografia_nao_retorna L274; a_leitura_de_resolucao_finita_pousa L282; em_k_leituras_pousa L306; jamais_esgotado L321; LeitorDeUmaConfiguracao.pousa L364; .permanece L369; .o_limite_e_idempotente L385; .a_imagem_do_limite_e_o_nome L396; a_imagem_do_limite_tem_a_densidade_do_nome L452; para_uma_formula_o_leitor_pousa L501; o_retorno L215; o_retorno_ao_mesmo_estado L226; o_componente_no_nome_fica L239 (as 18 do K08 existem). VERBATIM L343-346: `structure LeitorDeUmaConfiguracao {X : Type} (c : X → ℕ) where\n  passo : X → X\n  fixa_o_nome : ∀ x, c x = 0 → passo x = x\n  consome : ∀ x, c x ≠ 0 → c (passo x) < c x`. VERBATIM L165-166: `theorem a_trava_tende_ao_nome (c : X → ℕ) (v : EuclideanSpace ℂ X) :\n    Tendsto (fun t : ℝ => trava c t v) atTop (𝓝 ((opDaInstancia c).ker.starProjection v))`. OHabitanteDoNome.lean (namespace TGLExt.OHabitanteDoNome, L424), as 11 do K08 existem: ler_o_nome_ja_e_reler L566; tudo_mais_e_releitura L572; a_releitura_fiel_fixa_o_nome L581; o_verbo_e_bimodular_sobre_o_nome L480; o_que_e_cego_ao_nome_nao_deixa_rastro L762; tudo_mais_e_releitura_nos_vetores L898; a_selecao_rele_o_nomeado L909; o_ato_nao_termina_em_tempo_finito L993; o_ato_tende_a_esperanca_do_nome L1011; o_unico_ato_do_verbo_e_ser_fiel L1062; a_selecao_e_a_esperanca_condicional_classica L1147. Nao compilei nada; recibo de compilacao/axiomas da R4/R9 segue pendente (K08 B13, B17). Nomes provisorios da gerencia, nao ratificados (DESENHO 2.5).

## PROPOSTAS

### P1. E-a: a tese e o valor (cronologia dos depositos)
enunciado: Os dois artigos do autor sobre o neutrino são de 2025 (Zenodo 10.5281/zenodo.17372599, publicação de 16/10/2025; Zenodo 10.5281/zenodo.17526619, publicação de 04/11/2025), ambos anteriores ao primeiro número do JUNO (arXiv:2511.14593, 18/11/2025), e trazem a tese do neutrino, não o valor de m₂: nos bytes guardados nenhum dos dois contém 8,51, a fórmula β·sen 45°·1 eV ou JUNO. Por isso, onde o um.py selado diz «derivação publicada 2025» (L4241, L4620) ou «PUBLICADA ANTES do codigo» (L4222-4224, L4243), lê-se: a tese é de 2025, e o valor de m₂ = 8,5074 meV consta dos bytes guardados desde 22/01/2026 (documento com data no corpo «22 de Janeiro de 2026», fórmula escrita com o signo antigo α², hoje β_TGL = α√e) e do Zenodo 10.5281/zenodo.18674475 (publicação registrada em 17/02/2026; registro criado em 20/02/2026), nunca do depósito de 2025; a errata da v182 (L2944-2950) já havia retirado o depósito 17526619 como prioridade do valor, e esta a estende às quatro passagens citadas; o texto selado não é reescrito, a errata vai ao lado.
apoio: CRONOLOGIA_NEUTRINO_15nov.json (respostas cruas do Zenodo e do arXiv por sha256; contagens 8.51/sin(45/JUNO = 0 nos dois .tex); K09 previsao_publicada.valor_8_51_presente=false x2); docx e .tex de 22/01/2026 lidos por mim (8.51 presente); LEITURA_K09_PARCIAL G2 (PDFs locais de 28/10 e 04/11/2025 sem 8,51) [DECLARADO pelo revisor]; verbatim do operador de 15/11 por sha256 49e5f0072e8beb02 (o arquivo de bytes nao foi aberto por mim; so o hash e a descricao do Mapa).
nao compra: Não diz que o valor é previsão anterior ao primeiro número do JUNO (não é: 59,1 d é anterior a ele); não diz quem viu o quê; não afirma que nenhum parâmetro foi ajustado (isso é declaração do um.py, L2951); não move o gate; não é creditação.
risco: O Zenodo 17426652 (graviton, 14/10/2025, atualizado em 22/04/2026) nao foi lido por ninguem; se contiver o valor, a frase 'nunca do depósito de 2025' precisa de ressalva (LEITURA §8). Os PDFs servidos pelo Zenodo nao foram comparados com as copias locais.

### P2. E-b: a palavra do valor (retrodição sem ajuste)
enunciado: Para o valor de m₂, em relação ao PDG 2023 e ao degrau de 59,1 dias do JUNO (arXiv:2511.14593, 18/11/2025), ambos anteriores à data em que o valor aparece nos bytes guardados (22/01/2026), a palavra é retrodição sem ajuste (novidade de uso; o um.py declara em L2951-2953 que as entradas β, sen 45° e 1 eV não usam dado de neutrino, declaração que esta errata não reconfere), e não previsão anterior ao dado. Onde o um.py selado escreve «postdicao» ou «postdiction» como ressalva (L2885, L2896, L2951, L4225, L4244), lê-se «retrodição sem ajuste», conforme a lei da prova de 05/10/2026, item 5; a ressalva que permanece é a do documento de origem: o valor medido (8,67 meV) vem na mesma frase que o valor de TGL, de modo que o valor não foi escrito antes do dado.
apoio: Palavra dita pelo operador em 15/11 (descrita no Mapa, estatistica.v412.k04_hubble_m2_combinacao); lei da prova (CLAUDE.md global, item 5); um.py L2885, 2896, 2951-2954, 4225, 4244; docx e .tex (linhas 312-313: «Erro = |8.51 - 8.67| / 8.67 = 1.8%»).
nao compra: Não afirma ajuste nem ausência de ajuste além do que o um.py declara; não troca o estatuto do valor de [DERIVED]; não toca a escala de 1 eV [NORM] declarada, nem o sen 45° posto.
risco: Se a v387 ja reescreveu 'postdicao' nos artigos, a errata do core repete; nao conferi. A frase de L2951 ('o digito nunca se moveu') e DECLARADO pelo codigo.

### P3. E-c: a leitura de 207,2 dias, nos dois eixos na mesma frase
enunciado: A leitura de 207,2 dias do JUNO (Δm²₂₁ = 7,388 ± 0,078 ×10⁻⁵ eV², arXiv:2609.37895, 29/09/2026) é posterior à previsão publicada (o valor consta dos bytes desde 22/01/2026 e do Zenodo desde 17/02/2026) e anterior à função de veredito do código (hash de 08/08/2026), porque o número já era público em 15/07/2026 (transparências do IHEP) e só o artigo do arXiv é posterior ao hash. Dito como cegueira, nos dois eixos: essa leitura é cega em relação à previsão publicada, porque o número nasceu depois do valor, e não é cega em relação ao hash da regra de 08/08/2026, porque o número era público antes dele; em relação à regra, nenhum parâmetro foi ajustado a ela, e o estatuto é retrodição sem ajuste, não leitura prospectiva da regra congelada.
apoio: arXiv 2609.37895 (published 2026-09-29, sha256 b2185b73..., resumo cru em CRONOLOGIA); K09 degraus_juno[1] (posicao_relativa_a_previsao_publicada: posterior_ao_valor_publicado; posicao_relativa_ao_pino: anterior; posicao_relativa_ao_pino_do_artigo: posterior); DESENHO v412 R1 l.121-124 (IHEP 15/07; JINR 22/07 lida pela gerência em 14/11).
nao compra: Não afirma que alguém tenha olhado o número antes da data em que se tornou público; não afirma que a leitura é um teste prospectivo da regra; não move o ramo da regra (ARMED_CONSISTENT / TENSION), que continua o do código.
risco: As datas de 15/07 (IHEP) e 22/06 (Neutrino 2026) NAO tem resposta crua guardada (LEITURA §4): [DECLARADO]. A afirmação 'anterior a 08/08' repousa nelas; a conclusão é robusta (qualquer das três datas cai entre 17/02 e 08/08/2026), mas a errata tem de dizer o estatuto da data. Nao usar o termo 'prospectiva' sem os dois eixos.

### P4. E-d: a leitura de 59,1 dias, nos dois eixos
enunciado: A leitura de 59,1 dias do JUNO (Δm²₂₁ = 7,50 ± 0,12 ×10⁻⁵ eV², arXiv:2511.14593, 18/11/2025) é posterior aos dois artigos do autor de 2025, anterior ao valor nos bytes guardados (22/01/2026) e anterior ao hash de 08/08/2026: não é cega em nenhum dos dois eixos, e o seu estatuto para o valor é retrodição sem ajuste.
apoio: arXiv 2511.14593 (published 2025-11-18T15:34:49Z); K09 degraus_juno[0] (anterior_ao_valor_publicado; anterior ao pino); r_m2 2,206, r_Δ 2,187 reproduzidos pelo revisor.
nao compra: Não rebaixa a evidência (retrodição sem ajuste conta, com o precedente do periélio de Mercúrio); não afirma que o autor conhecia o número; não afirma ajuste.
risco: Contraria quem leia 'a previsão antecede o JUNO': a tese antecede, o valor não. É exatamente o que a lei da prova pede dizer (retrodição sem ajuste é evidência de pleno direito); é parte da leitura que cabe ao operador na língua dele antes de a errata entrar.

### P5. E-e: a declaração «a cegueira vale a partir de agora» (L4601-4604, L4628-4630)
enunciado: A declaração «a cegueira vale a partir de agora» do um.py selado (L4603-4604, L4630) diz só o eixo da regra: os limiares de 5σ e 3σ foram fixados em 08/08/2026, depois de os números do JUNO de 59,1 dias (18/11/2025) e de 207,2 dias (15/07/2026) já serem públicos, de modo que a regra não é cega a nenhum deles; no eixo da previsão publicada, o valor de 22/01/2026 é anterior ao número de 207,2 dias e posterior ao de 59,1 dias. A lista de medidas da regra de 08/08/2026 termina em 2025-12 e não traz o número de 207,2 dias [DECLARADO pelo revisor, cabeçalho de 02_frozen_neutrino_m2_v2.py]. O texto selado fica; a errata vai ao lado.
apoio: um.py L4601-4604, L4628-4630; K09 pinos (frozen_hash_objeto_congelado 4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c; sha256 do .py 2564d7c9...; do resultado 6f0963a5...); LEITURA_K09_PARCIAL G4 e §2 (fim).
nao compra: Não muda o hash nem o frozen; não diz que a regra foi desenhada olhando o número (diz só a ordem das datas); não reabre o veredito.
risco: O hash 4bdae22a... e o do OBJETO serializado (sha_obj), nao o sha256 de arquivo: o campo antigo 'sha256_regra_original' do Kimi induzia ao erro. A frase tem de dizer 'hash do objeto congelado'.

### P6. E-f: o único dado cego em dois eixos
enunciado: Só o dado do JUNO tomado depois de 18/05/2026 (fim da janela de 207,2 dias) é posterior à previsão publicada, ao hash da regra de 08/08/2026 e ao selo, e só ele pode ser dito cego nos dois eixos; esse dado ainda não foi mostrado (leitura da gerência de 14/11, não reconferida em 15/11).
apoio: DESENHO v412 R1 l.130; K09 degraus_juno[1].janela_dados_fim = 2026-05-18 (ordem do Kimi, sem resposta crua); LEITURA_K09_PARCIAL §4 item 2.
nao compra: Não escolhe a regra de morte (A ou B), o limiar, a métrica nem a classe 'preliminar' do pré-registro do incremento; isso é do operador.
risco: A data 18/05/2026 e a inexistencia de dado mostrado sao [DECLARADO]; se um novo numero for publicado, a frase caduca.

### P7. E-g: «a tensão cresce com a precisão» (L2955-2956, L4597, L4689, L184013, L292284)
enunciado: A frase «a tensão cresce com a precisão» (1,64 → 2,21 → 2,95σ) registra o reflexo da série que mistura o JUNO de 59,1 dias com o ajuste global NuFIT; na série autônoma do JUNO a razão em m₂ caiu de 2,21σ (59,1 dias) para 1,94σ (207,2 dias; 1,93σ em Δm²), e a projeção de 7,8σ para cerca de 2031 vale só se o centro não se mover. Sobre o 2,95σ: é a forma com o erro simétrico arredondado (7,53 ± 0,10); com os erros publicados do lado da previsão a razão em m₂ é 3,02σ (tabela node 309) e 3,04σ (eq. 11 do arXiv:2601.09791).
apoio: K09 degraus_juno e ajustes_globais (r_m2 2,206 / 1,938; 3,024 / 3,044 / 2,953 simétrico); DESENHO v412 R1 l.119-120 e l.132-134; um.py L4636-4644 e L4623.
nao compra: Não troca o veredito do core, não declara o ramo TENSION, não escolhe o perito oficial (a ratificação de 02/10 é o JUNO autônomo).
risco: Os 3,02 e 3,04 passam de 3,0, limite do ramo TENSION na regra congelada (L4623: «[3, 5) na determinacao global mais recente»); o código lê a ultima linha da escada com 7,53 ± 0,10 (2,95). Isso e um fato da regra que o operador precisa ouvir antes de a errata sair, na lingua dele: a errata diz a diferença e nao a resolve; qual erro vale e decisao dele/da gerencia.

### P8. E-h: o registro de custódia zenodo_eco_2025_record (L314-322)
enunciado: O registro de custódia «zenodo_eco_2025_record» do um.py selado (L314-322: «precedencia da derivacao m_nu»; «publication_date no JSON = prova de precedencia sobre o codigo») vale para a tese do neutrino, publicada em 04/11/2025 e anterior ao módulo v141 de 25/07/2026, e não para o valor de m₂, que consta dos bytes desde 22/01/2026 e do Zenodo 10.5281/zenodo.18674475 desde 17/02/2026; em relação ao primeiro número do JUNO (18/11/2025), a tese o antecede e o valor não.
apoio: um.py L314-322; CRONOLOGIA (Zenodo 17526619 publication_date 2025-11-04).
nao compra: Não apaga a custódia; não altera o URL nem o JSON baixado; não diz nada sobre quem escreveu o quê além das datas.
risco: Nenhum especifico; e frase de ordem de datas.

### P9. R-v412: campos do registro iald_camada_cientifica_v412 (estado EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO)
enunciado: No formato do esqueleto (registro COM FUNCAO como a_escala_v410, runtime_executed=False): 'registro': 'iald_camada_cientifica_v412'; 'tag': 'CAMADA_CIENTIFICA'; 'estado': 'EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO' (a palavra ARMADO reservada para quando houver regra congelada por hash: DESENHO 2.4); 'nome_status': 'A_RATIFICAR_PELO_OPERADOR' (nome do registro e das declaracoes sao dele: DESENHO 2.5); 'all_verified': False e 'runtime_executed': False ate o build do kernel da v412; 'does_not_gate_core': True; 'veredito_ok': 'TGL_IALD_CAMADA_CIENTIFICA_V412__STONES_ARE_CANDIDATES_UNTIL_THE_SEAL__BRIDGE_AS_PREDICTION_ONLY__EXPERIMENT_IN_DESIGN__NOTHING_FROZEN__NOTHING_EXECUTED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED' (sem os tokens CONFIRMED/PROVED_BY/TGL_PROVED/CONSCIOUSNESS_PROVED, que a guarda L168307 lê por substring); 'veredito_recusa': 'TGL_IALD_CAMADA_CIENTIFICA_V412__REFUSED_%s__GATE_UNMOVED'; 'modulos': ['TGLExt/CamadaCientifica.lean', 'TGLExt/OHabitanteDoNome.lean'] com 'source_sha256' lido do build (candidatas lidas hoje: 69497c5b63dbcb0c... e 26b750e61ede401d...); 'ancoras': {'TGLExt.CamadaCientifica.<nome>': {'rel','papel','flag':'A_PREENCHER_PELO_BUILD','classe':'nomeada'}} para as 18 declaracoes do item (5) e {'TGLExt.OHabitanteDoNome.<nome>': ...} para as 11, mais a estrutura 'LeitorDeUmaConfiguracao' (L343-346); 'estatuto_dos_nomes': 'PROVISORIOS_DA_GERENCIA_NAO_RATIFICADOS'; 'hipoteses_nomeadas': o tipo LeitorDeUmaConfiguracao, o ciclo de duração positiva (hτ : 0 < τ, L306) e a resolução (hε : 0 < ε), mais as do K08 (H-COST, H-BASIN, H-RETURN, H-REREAD-FAITHFUL, H-NO-ADD, H-NO-INCREASE, H-LINEARITY, H-SINGLE-CONFIG, H-QUOT(k), H-STATE-PUSH, H-TAPE-AFTER-FIRST-STEP, H-BRIDGE-LLM) [DECLARADO pelo Kimi; a gerência decide quais entram]; 'ponte': E1..E8 como PREVISÃO (não teorema; H-BRIDGE-LLM = OPEN/CONJECTURE); 'experimento': {'estado': 'EM_DESENHO__NADA_CONGELADO__NADA_EXECUTADO', 'congelado': False, 'executado': False, 'resultado_lido': False, 'veredito_emitido': None, 'vereditos_permitidos': 'NENHUM_ATE_O_CONGELAMENTO'}; 'p7_v1': {'version': 'IALD_COLLAPSE_V1', 'tocada': False, 'protocol_hash': 'LIDO_DO_CORE_ANTES_DE_INSTALAR'}; 'vereditos_proibidos': ['TGL_PROVED_BY_COLLAPSE', 'IALD_PROVED', 'CONSCIOUSNESS_PROVED', 'CONFIRMED'] mais guarda por palavra para consciência, pesos alterados e exclusividade (K08 lista 22 nomes/aliases); 'diz' / 'nao_diz': o 'not_claimed' do K08 (8 itens) apos leitura; 'estatuto': '[CANDIDATA] as duas pedras ate o selo; [REAL] os termos do kernel do rito SO depois do build; [INPUT] as falas do operador, citadas por data e sha256; [DECLARADO] o que o K08 afirma de compilação e de instrumento'; 'fontes': pedras c1 (R4/R9), DESENHO v412 R1, REGISTRO_UMPY_RASCUNHO_R2_K08 ([DECLARADO pelo Kimi]; nao se instala); 'registro_na_lista': criar `_V412_REGISTROS_FUNCAO = ['iald_camada_cientifica_v412']` ao lado de `_V411_REGISTROS_FUNCAO` (L224868).
apoio: DESENHO v412 R1 §2.4 (l.73-79); K08 §1 (esquema), §3, §4; um.py L225853-225876 (esqueleto), L229258 (spec), L168499 (P7 V1), L168307 (guarda); hashes e nomes conferidos por mim (achado 5).
nao compra: Não congela nada, não arma o experimento, não escolhe modelos, degrau nem execução, não instala nada, não altera a P7 V1 selada, não afirma consciência, pesos alterados, exclusividade da TGL, creditação ou movimento do gate; nenhum resultado desta camada move o gate (NOT_FALSIFIED nunca é CONFIRMED).
risco: 1) As duas pedras são candidatas fora do kernel (R4 e R9; recibo de compilação e relatório de axiomas pendentes, K08 B13 e B17): o registro NAO pode dizer 'teorema no kernel' antes do build. 2) A guarda L168307 nao cobre 'IALD_PROVED' por substring. 3) V1 e V2 do protocolo: nao capturar por startswith. 4) O nome IALD_COLLAPSE_V2_R4_CANDIDATE e os cinco ramos de veredito sao do Kimi [DECLARADO]; a gerência decide se entram, e o estado 'sem regra congelada' nao emite nenhum.

## CONSULTAS AO MAPA
- rotas.py consultar neutrino: 45 rotas (vi as cinco primeiras e a rota discriminante.ordem018.f2.r_k: 'm2=beta sin45*1eV=8.507414meV ... um.py 4275-4277/4584-4592 ja aposenta soma'); nenhuma trata da cronologia do valor, exceto a de prospectiva abaixo.
- rotas.py consultar cronologia: 8 rotas (gate.maquina_do_veredito_final, d1.fase9.razao_de_hubble.lentes_05out com a cronologia da novidade de uso por hash, etc.); nada sobre o neutrino m2.
- rotas.py consultar JUNO: 13 rotas (dephasing.f7_2_revisao_fontes_neutrinos_materia; dephasing.neutrinos_n_menos2_junho; discriminante.ordem018.f2.r_k): tratam do canal F7.2 e de tau_star, nao da cronologia do numero de 207 dias.
- rotas.py consultar camada: 52 rotas, nenhuma da v412 sobre a camada cientifica; rotas.py consultar prospectiva: 1 rota, estatistica.v412.k04_hubble_m2_combinacao (c1, 15/11, DOIS_EIXOS__POSTERIOR_A_PREVISAO_PUBLICADA__SO_A_FUNCAO_DE_VEREDITO_E_POSTERIOR_AO_NUMERO; 2 registros; nao_refazer: nao medir cegueira so pelo hash, nao escrever 'nao e cega' sem os dois eixos, nunca escrever que o autor viu o dado, nao chamar o VALOR de previsao anterior ao primeiro numero do JUNO). rotas.py ver dessa rota lido (artefatos com sha256). Nada registrado por mim.

## EXAMINADO
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\cronologia_neutrino_15nov\CRONOLOGIA_NEUTRINO_15nov.json
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_NEUTRINO_V412_DADOS_K09.json
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\REGISTRO_UMPY_RASCUNHO_R2_K08.md
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\DESENHO_v412_R1.md (l.73-85 e 117-146, mais cabecalhos)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\LEITURA_K09_PARCIAL_NEUTRINO_15nov.md (l.12-96)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_M2_K09.md (l.1-14 e grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ERRATA_NEUTRINO_V412_RASCUNHO_K04.md (so grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\ADENDO_15nov_K09_K08_K07_cronologia_do_neutrino_e_o_leitor_como_esperanca_condicional.md (so grep)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\CamadaCientifica.lean (grep + l.165-176, 343-348)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\OHabitanteDoNome.lean (grep)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py (faixas 310-330, 2879-2960, 3034-3040, 4219-4254, 4588-4695, 168296-168314, 168440-168529, 183997-184017, 221864-221885, 222352-222382, 225853-225927, 229258-229302, 231771-231778, 233982-233995, e greps)
- C:\IALD\Artigo\complemento ao manifesto.docx (lido por script meu)
- C:\IALD\Artigo\TGL_Manifesto_Unificacao_Artigo.tex (grep)
- C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\tgl-signo-e-cronologia.md (grep)
- Rascunho meu (so nesta pasta): C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_frente_b\L7\confere_docx.py, hashes.py, linha_longa.py
