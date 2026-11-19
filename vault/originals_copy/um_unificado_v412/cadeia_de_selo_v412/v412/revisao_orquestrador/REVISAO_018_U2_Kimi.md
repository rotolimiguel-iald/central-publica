APROVADO_COM_RESSALVAS — a poda proposta está certa e não derruba nada que se prove hoje; os quatro teoremas compilam limpo e dizem o que a docstring diz; dois achados factuais na seção 2 (um MÉDIO, um BAIXO) pedem correção antes de qualquer uso público. [DECLARADO pelo revisor Kimi até a gerência conferir na fonte]

# REVISÃO 018 — Unidade U2 (frente B: a proposta de resolução das duas equações) — revisor Kimi

16/11/2026. Revisor distinto (Kimi), por ORDEM 018. Não li `REVISAO_018_U2_Codex.md`, nem seu adendo, nem nada em `revisao_orquestrador\U2_Codex\`. Só li; a única escrita fora da minha pasta é este relatório. Minha pasta de trabalho: `revisao_orquestrador\U2_Kimi\` (cópias, extrações e logs lá).

Sob revisão (pinos conferidos contra `revisao_orquestrador\FONTES_018.json`, ambos `coincide: true`):

- `frente_b_duas_equacoes\REV0\PROPOSTA_DA_GERENCIA_R0.md` — sha256 `0cbdfeadee9ee8a4a12665b16595da61f7a3cd111969966731f27b3144efd5f6`.
- `frente_b_duas_equacoes\REV0\DispersaoDoPsionControles.lean` — sha256 `f0aefac268b97fe7f875ffddc5ce6738710b45f72ed1a56f56206c4ce3881625` (idêntico ao de `candidatas_c1\DispersaoDoPsionControles.lean`, mesmo hash medido por mim).

## 1. Achados, por gravidade

### MÉDIO

**M1 — §2, leitor E1: «K_∂ é número puro em toda definição do artigo» é falso como está escrito.**
`PROPOSTA_DA_GERENCIA_R0.md:22`. No Artigo A, K_∂ é definido como **operador**, duas vezes: `K_∂ ≡ −log Δ`, «auto-adjunto», o Hamiltoniano modular (`paper_PT.tex:514`, eq. `eq:K-partial-definition`), e `K_∂ = 2π K_boost`, com `K_boost = ∫ x¹ T₀₀ d³x` (`paper_PT.tex:530-532`). Um operador não é um número. O que é verdade e sustenta o ponto: K_∂ é **adimensional** (log de operador adimensional), de modo que, na equação `(□ − m² − ξR)Ψ = β K_∂ Ψ` (`paper_PT.tex:248-249`), o lado direito precisa de uma escala de dimensão massa² que o artigo não nomeia — e é essa escala que a candidata supria com o `u²` de `k_∂ = 2βu²`. O próprio artigo declara aberta a ponte operador→fonte («Conjectura declarada», `paper_PT.tex:275-282`).
Conserto: reescrever o bullet como «K_∂ é operador adimensional no artigo (`−log Δ`; `2π K_boost`); na equação ele entra como se fosse um número (o autovalor no modo), e a escala que dá dimensão a esse número o artigo não nomeia». Numa casa que barra homônimos, a frase atual é exatamente o tipo de escorregão que não pode ficar na seção de evidências — embora não se propague: a poda do item 2 (§4) está ancorada no kernel («o kernel não tem K_∂ agindo no campo»), que confirmei separadamente (abaixo, §3 desta revisão).

### BAIXO

**B1 — §2, leitor E2: «o Artigo A volta a 1/6 em maio» — o mês não se confirma nas cópias locais.**
`PROPOSTA_DA_GERENCIA_R0.md:32`. A substância está certa: o Artigo A tem `ξ = 1/6` e `β` na fonte (`paper_PT.tex:181,248-249`). Mas a cópia local mais antiga que sobrevive com essa forma é de **05/06/2026** (`Artigo\the_boundary\O Custo Geométrico do Zero Absoluto — Haja Luz\paper_PT.tex`, mesma equação na linha 251), e a vigente é de 18/06/2026 (`A Ponte e o Um\paper_PT.tex`). Não achei cópia de maio.
Conserto: trocar «em maio» por «em junho (cópia local mais antiga: 05/06/2026)», ou pinar a fonte de maio se ela existir fora do recorte.

### Sem mais achados

Os demais pontos da ordem passaram sem ressalva (detalhe nas §§2–5 abaixo). Em particular: nenhum dos quatro teoremas é identidade vazia apresentada como fato, e a proposta não lê o operador além da letra em ponto nenhum.

## 2. Conferência dos fatos da seção 2 da proposta, na fonte

**Do Artigo A** (`Artigo\Haja_Luz\A Ponte e o Um\paper_PT.tex`, lido por mim):

1. «Da ação escrita, só o termo de curvatura gera um termo da equação» — **confere**. A lagrangiana é `L_matéria + L_campo + L_grav + L_modular` (`paper_PT.tex:145-149`): `L_campo = −¼ Φ_μν Φ^μν` é o cinético do **vetor** Ψ_μ (l.167-168); `L_grav = R/2κ² + ξR|Ψ|²` (l.178-179); `L_modular` é cosmológico (l.194-195). Não há `|DΨ|²` do escalar, nem `m²|Ψ|²`, nem termo-fonte `βK_∂`. A EOM (l.244-251) é introduzida por «Da variação δS/δΨ* = 0 obtém-se» — afirmada. «O site e o kernel já dizem que ela é hipótese nomeada» — **confere nos dois**: site v3.0, `Site\tgl\v3.0\index.html:504` («the kernel holds the equation of motion as a named hypothesis [REAL]»); kernel, `TheSameBetaReadsFourFaces.lean:40` («INPUT: the field equation; the data structure alone does not supply it» — a EOM é campo de input da estrutura `ActionCouplingData`, l.20-25, com `xi` separado de `beta`).
2. «K_∂ é número puro…» — **não confere**: é o achado M1.
3. «A lei β·|1+w| é do fluido cósmico diante de um horizonte; o artigo nunca a aplica ao campo nem ao psíon, e nunca usa w = +1» — **confere**. A lei está no contexto cosmológico (Friedmann modificada e resposta de fronteira, `paper_PT.tex:1108-1146`: «o fluxo de matéria através de um horizonte causal local é ∝ ρ(1+w), zero exato para w = −1»). Os únicos valores de w no artigo são −1 e 1/3 (BBN, l.1238, 2013). «Psion» no artigo só aparece em outro contexto (paridade, l.1705-1729), nunca sob a lei.
4. «Na conta da candidata o β entra duas vezes; o artigo escreve uma» — **confere**. Rodei `rodada_b\conferir_candidata_f.py`: a conta é `k_∂ = |1+w|·β·u²` (um β da lei) e depois `ω² = β·k_∂` (outro β) — dois β; o Artigo A escreve um (l.249). Saída do script: os três números coincidem (8,507414 meV); sem o 2, 6,015650 meV — a «conferência» da candidata é identidade por construção, não teste (confirma o E4).

**Da linhagem** (E2):

5. «O 2 nasce na lagrangiana fundadora de 12/09/2025: campo real, termo de movimento com ½, curvatura sem ½; a variação dá 2ξR» — **confere**. No artigo-mãe `Teoria_Gravitacao_Luminodinamica_TGL_FINAL.docx` (12/09/2025; extraí o texto e as equações para `U2_Kimi\tgl_final_full.txt`): «Tomemos um **escalar real** estacionário Ψ» (extração, l.112); `L = ½ g^μν∇_μΨ∇_νΨ − ½ m_eff² Ψ² − ξRΨ² − …` (l.113 — cinético com ½, curvatura sem ½); «A variação dá: □Ψ + m_eff²Ψ + **2ξR**Ψ = …» (l.115); dispersão `ω_n² = k_n² + m_eff² + 2ξR` (l.145). A variação eu mesmo refiz (δ(ξRΨ²) = 2ξRΨ·δΨ); o «refeito por conta simbólica» corresponde ao `K05\CAMPO\medir_campo.py` (frações exatas + pins literais das linhas 186-214 do graviton_v2).
6. «Com campo complexo e coeficiente 1, sai ξR, sem o 2» — **confere** (álgebra padrão: variação de `ξR|Ψ|²` em Ψ* dá `ξRΨ`).
7. «Ali ξ era livre e R era a curvatura de Ricci» — **confere**: no fundador, «ξ controla acoplamento à curvatura escalar R» (l.118 da extração), com `R = 6(Ḣ + 2H²)` (l.454) — escalar de Ricci; nenhum valor fixado.
8. «ξ = 1/6 entra em 25/02/2026» — **confere**: `graviton_v2.tex` (25/02/2026), l.194-206 («ξ = 1/6 … derived, not free»).
9. «ξ = β é escrito em março de 2026» — **confere**: `Artigo\Tratado\secao_01_fundamentos.tex` (24/03/2026), «A relação ξ = β_TGL», l.696-738: «ξ = β_TGL = α×√e ≈ 0,012031».
10. «o Artigo A volta a 1/6 em maio e põe β na fonte» — substância **confere**; o mês, **não** — é o achado B1.
11. «O registro v354 (15/09/2026) ancora β no acoplamento com a fronteira e proíbe fundi-lo com ξ» — **confere**: `Nós\um_absoluto_pt.txt:1366` (parágrafo «Ao lado (v353–v354)»: «β_TGL é o acoplamento modular Ψ–K_∂ da lagrangiana…; ξ=1/6 é o acoplamento conforme, não β_TGL — os dois coeficientes nunca se fundem»); o stamp do manifesto da v354 é 20260915. Também `CAMPO_DUAL_LEVANTAMENTO_K05.md:155` («NÃO, pelo registro v354/v355 e pelos controles do kernel»).
12. «A v405 reimporta da linhagem a dispersão com ξ = β, como definição» — **confere**: `v405_kernel\DIFF_KERNEL_v405.txt:10` adiciona `TGLExt/PontoZeroDoPsion.lean`; na pedra, `omegaSq β R := 2*β*R` é `def` (PontoZeroDoPsion.lean:86), com o Tratado §3 citado no cabeçalho (l.22-24). «As duas frases convivem, sem termo que as ligue» — **confere** (nenhum termo do kernel liga o `xi` da `ActionCouplingData` ao `beta`; é o que a própria proposta vem tratar).
13. «Na escrita de linhagem, o termo de curvatura com ξ = β já é, por álgebra, uma fonte β·κ·Ψ com κ = 2R» — **confere** (2βRΨ = β·(2R)·Ψ; trivial). «As duas origens que ela dá ao 2 se excluem» — leitura razoável do E2 (duas origens rivais para o mesmo fator; a candidata marca ambas «nenhuma provada», CANDIDATA_F l.31-35): a tomo como leitura declarada, não como fato.

**Dos levantamentos e da letra** (E4, proposta l.38-39) — **confere tudo**: a candidata F não está entre as candidatas A–E do K05 (li a tabela do §3; são outros objetos) e não é nenhuma das leituras que a custódia mandou podar (CONSOLIDACAO, lista «PODAR», l.165-173 — onde consta justamente «"F cai" por K·Ω = 0» como argumento **proibido**); a conta dela é identidade (rodei); «uma equação só» é da custódia (cabeçalho da CANDIDATA_F: «claude-site-custodia»), não do operador — o verbatim dele é só «quero resolver a questão não somente colocar uma nota».

**Falas do operador de 16/11** (proposta l.41-43): li os 12 arquivos `OPERADOR_16nov_*.txt` em bytes. «Ele não escolheu entre geometria e fronteira, não falou do R, e as falas não decidem a candidata» — **confere** (a fala 1 não traz «R», «β», «fronteira», «geometria»; a consolidação da custódia, l.37 e 49, diz o mesmo). «A gerência não liga essas falas a esta proposta por conta própria» — **confere**: a §4 não cita fala nenhuma como fundamento.

## 3. Os quatro teoremas da candidata: recompilação e conteúdo

Recompilei **em cópia minha** (`U2_Kimi\DispersaoDoPsionControles.lean`, sha256 idêntico ao pinado), com o script `compilar_candidata.ps1` copiado para a minha pasta, sobre os `.olean` do sandbox `C:\t\k411c\final`, binário `lean.exe` 4.31.0 (commit 68218e876d2a38b1985b8590fff244a83c321783). Nunca `lake build`. Log completo: `U2_Kimi\build\DispersaoDoPsionControles.log`. Resultado: **RC 0, 53 s, saída sem nenhum aviso, sem sorry, sem axioma novo** — os quatro teoremas dependem só de `propext`, `Classical.choice`, `Quot.sound` (o `#print axioms` de cada um está no log). Confere o recibo da gerência (`RESULTADO_DispersaoDoPsionControles.json`: avisos 0, erros 0, `todos_so_o_trio: true`).

Os enunciados dizem o que a docstring diz (li a prova de cada um):

1. `o_dois_e_o_quatro_do_ponto_zero_vezes_o_meio_da_face` (l.41-42): `omegaSq β (βu²) = 4·sen²(π/4)·(βu)²` — álgebra: `2β²u² = 4·½·β²u²`. É identidade e está **apresentada como identidade** («É identidade algébrica», docstring l.18-19). Não é identidade vazia vendida como fato.
2. `com_outro_coeficiente_a_massa_e_outra` (l.53-54): com `ξ ≥ 0` no lugar de β **na dispersão** (o `R = βu²` fica), `½·√(omegaSq ξ R) = neutrinoMassForm c u ↔ ξ = β`. Controle com conteúdo (iff), prova sã (injetividade da raiz + cancelamento por `R > 0`).
3. `com_o_coeficiente_conforme_so_se_beta_fosse_um_sexto` (l.77-79): o conforme só daria a forma da massa se `β = 1/6`. O arquivo declara **não** provar `β ≠ 1/6` (docstring l.31) — honesto.
4. `sem_o_dois_a_massa_e_outra` (l.85-86): sem o 2 (`ω² = βR`), a meia-frequência **não** é a forma da massa. Controle com conteúdo (desigualdade estrita via `βR > 0`).

E o que já era do kernel (proposta §3) confere na pedra, lida por mim: `the_mass_is_the_zero_point` (PontoZeroDoPsion.lean:102-103), `a_massa_e_a_projecao_do_retido` (l.186-189), `o_psion_e_raiz_de_dois_retidos` (l.192-195) com `retido_eq` (Δ = β·u, l.169).

## 4. A poda (seção 4 da proposta) está certa? Falta algo que se prove hoje?

**Está certa.** Os dois alvos da poda:

1. **A leitura do 2 como `|1+w| = 2`** — os três fundamentos conferem na fonte: o artigo nunca aplica a lei a um campo nem usa `w = +1` (§2, item 3 acima); o β entraria duas vezes (item 4); e as duas origens são rivais (leitura declarada do E2, aceitável como tal).
2. **A afirmação «as duas escritas são uma equação»** — fundamentos conferem: a candidata é troca de lado por álgebra (a própria candidata declara o furo (b), a derivação de `k_∂ = 2βu²`, não fechado — CANDIDATA_F l.43-44), e o kernel não tem K_∂ agindo no campo: na pedra, «o kernel tem `lightDelta` (Δ^{it}) e o seu conjunto fixo, **NÃO um `def` para K**» (ThePsionAndTheViscosity.lean, docstring l.26); na ponte da ação, `K_boundary` é **campo de input** de `ActionCouplingData` (TheSameBetaReadsFourFaces.lean:25, 40). Pela regra da casa (04/11: identificação ou se prova no kernel ou se poda), a poda é o tratamento prescrito.

**Nada que se prove hoje foi deixado cair.** O conteúdo da candidata se divide em: (i) o já provado no kernel e mantido (a conta `ω = √2βu`, `½ω = β·sen45°·u` — a proposta a mantém na §4, «Dizer, com termo»); (ii) o improvável hoje (H_F, as duas origens do 2, a leitura dos «dois β») — podado ou não adotado, corretamente; (iii) leituras das falas — fora de escopo da própria candidata. Os «Seguem abertos» da proposta (ação que dê a EOM, R82/R89; como K_∂ age e com que escala; se o psíon é modo do campo) cobrem os furos (a), (c), (d) da candidata; o furo (b) é o conteúdo podado. Nenhuma perda silenciosa.

## 5. A proposta lê o operador além da letra?

**Não encontrei nenhum ponto.** Confere cada menção: «quer resolver a questão, não só pôr uma nota» é verbatim (OPERADOR_16nov_quero_resolver…txt); o resumo das falas (§2, l.41-43) coincide com as consolidações da custódia e com os bytes que li; a §5.2 reproduz fielmente a pergunta residual da custódia («o custo de hoje é o pagamento do R?», sem resposta — CONSOLIDACAO l.33 e 56); o «R = pagamento» do «Dizer, com termo» está ancorado na cunhagem de 31/10 que a própria pedra carrega (PontoZeroDoPsion.lean:9, 16) e na definição `pagamentoComoCurvatura` (l.89). Nenhuma identificação nova é afirmada; a regra de 04/11 é obedecida (a candidata é podada, não adotada).

## 6. ADENDO A — a poda proposta depende do passo «ligar ou separar por termo os dois psíons»?

Li `rodada_b\consolidacao_das_falas\CONSOLIDACAO_DAS_FALAS_DO_PSION_16nov.md` inteira. **sha256 do que li: `12a2a84f01ffd2c85b5a0860d7e06b0152674fc55d169d999f50ba75b85dc848`** (medido por mim; coincide com o que a NOTA_DA_GERENCIA_VETOR_E_MODO_R0.md declara ter lido). O texto é [DECLARADO pela custódia]. As passagens: «Efeito na candidata F» (l.133-149), «Para a gerência» (l.151-191, com a exigência na l.189: «Antes de qualquer poda, ligar ou separar por termo os dois psíons (o modo do Tratado e Ω)») e o item aberto (l.59: «A F depende disso antes de qualquer poda»).

**A minha resposta: a poda, como está escrita, NÃO depende do passo — e o passo já está respondido na direção "separar".** Formo assim o meu entendimento:

1. **Os fundamentos da poda não tocam o vetor.** Os dois motivos da §4 são sobre a conta do modo: fatos do artigo (a lei `β|1+w|` nunca aplicada a campo, nunca `w = +1`, o β duplo) e uma ausência no kernel (K_∂ não age no campo; a derivação de `k_∂` falta). Conferi cada um na fonte sem precisar decidir o que a palavra «psíon» nomeia. A exigência da custódia nasceu do achado ALTO da leitura do R — um leitor que «podava» a F aplicando a Ω o critério do modo (K·Ω = 0, que vale para todo vetor cíclico). A proposta **não** repete esse caminho: K·Ω não aparece em nenhum fundamento.
2. **A proposta já se comporta como se os dois objetos estivessem separados.** O «Dizer, com termo» fala de «a conta do psíon» — o modo — e não a identifica ao vetor em ponto nenhum.
3. **E o passo pedido pela custódia foi executado, na direção "separar", pela própria gerência.** A candidata `candidatas_c1\REV17\PsionVacuoEModoDoTratado.lean` (sha256 `93b742153092553768621a1582c2add5121a71a634e9ce9f734ab657517722e3`) prova por termo: os níveis do lock `u·(1−P)` são exatamente 0 e u (`e_nivel_do_lock_sse`); a frequência do Tratado é nível se e só se `√2·β = 1`; a forma da massa e o retido nunca são níveis; o estado do ângulo de Miguel não é autovetor do lock (variância `β(1−β) ≠ 0`); a única ligação existente é por valor esperado (`ω = √2·u·⟨1−P⟩` no ângulo). **Recompilei essa candidata também, na minha cópia: RC 0, 43 s, 27 teoremas, todos no trio de axiomas, sem aviso** (log em `U2_Kimi\build\PsionVacuoEModoDoTratado.log`). Ou seja: mesmo lendo a exigência da custódia como vinculante, ela está cumprida na direção «separar por termo» — no Hamiltoniano que o kernel tem. A direção «ligar» segue sendo construção posta (o oscilador de dois níveis da mesma REV17), não derivação — e a candidata o diz.
4. **O que fica de pé, e não é da poda:** a escolha de qual objeto herda o nome «psíon» é pergunta ao operador (pergunta residual da consolidação), e a exigência da custódia permanece como guarda para qualquer **futura** identificação — não como pré-condição desta poda.

## 7. O que conferi (lista completa)

- Pinos sha256 dos dois arquivos sob revisão contra `FONTES_018.json` (ambos coincidem); identidade do `.lean` da REV0 com o de `candidatas_c1` (mesmo hash).
- Artigo A (`paper_PT.tex` vigente, 18/06/2026): a lagrangiana (l.143-149, 158-198), a EOM (l.244-257), a ponte declarada aberta (l.259-286), as definições de K_∂ (l.514, 530-532), a lei `β|1+w|` e seus contextos (l.1108-1164, 1238, 2013), as ocorrências de «psion» (l.1705-1729). E a cópia de 05/06/2026 (mesma EOM, l.251).
- Fundador de 12/09/2025 (`Teoria_Gravitacao_Luminodinamica_TGL_FINAL.docx`; texto e equações extraídos para `U2_Kimi\tgl_final_full.txt`): escalar real, ½ no cinético, curvatura sem ½, variação → 2ξR, dispersão com 2ξR, ξ livre, R = escalar de Ricci. Variação refeita por mim.
- Linhagem: `graviton_v2.tex` (25/02/2026, ξ = 1/6 derivado, l.186-214 e 271); `Tratado\secao_01_fundamentos.tex` (24/03/2026, ξ = β, l.266 e 696-738).
- Registro v354: `Nós\um_absoluto_pt.txt:1366` + stamp do `v354_incorporacao_manifesto.json` (20260915); v405: `v405_kernel\DIFF_KERNEL_v405.txt:10` (entrada da pedra PontoZeroDoPsion).
- Kernel (lido por mim, já que o leitor da gerência não rodou): `TGLExt\PontoZeroDoPsion.lean` inteiro; `TGLExt\ThePsionAndTheViscosity.lean` (cabeçalho e defs, l.1-90); `TGLExt\TheSameBetaReadsFourFaces.lean` (l.1-120: EOM como INPUT); `TGLExt\ActionCouplingControls.lean` (l.1-90).
- Candidata F e sua conta: `CANDIDATA_F_uma_equacao_so_16nov.md` e execução de `conferir_candidata_f.py` (identidade; sem o 2 dá outro número).
- As quatro leituras da custódia: R, psíon conjugado, ruído-e-sinal, silêncio (consolidadas) + as 12 falas verbatim do operador de 16/11.
- Consolidação das falas (adendo A), sha256 acima.
- K05: §3 (tabela A–E), l.120-175, e `K05\CAMPO\medir_campo.py` (a «conta simbólica»).
- Site (só leitura): `Site\tgl\v3.0\index.html:504` (o box, com «named hypothesis») e `:535` (o cartão do psíon, 31 linhas abaixo — a proposta diz «trinta», cenário confere).
- Recompilações na minha pasta (binário 4.31.0 sobre os `.olean` de `C:\t\k411c\final`, script copiado): `DispersaoDoPsionControles` — RC 0, 4 teoremas, trio, sem aviso (53 s); `PsionVacuoEModoDoTratado` (para o adendo A) — RC 0, 27 teoremas, trio, sem aviso. Logs em `U2_Kimi\build\`.
- Nada instalado: `grep` por «DispersaoDoPsionControles» em `Nós` dá 0 — o «nada instalado; nada publicado» do cabeçalho confere.

## 8. Consertos pedidos (resumo operacional)

1. (M1) `PROPOSTA_DA_GERENCIA_R0.md:22` — reescrever o bullet do K_∂ como na §1 acima.
2. (B1) `PROPOSTA_DA_GERENCIA_R0.md:32` — «em maio» → «em junho (cópia local mais antiga: 05/06/2026)», ou pinar a fonte de maio.

Nenhum dos dois toca a poda, os quatro teoremas ou a resposta ao operador. Com os dois consertos, a proposta fica em pé por inteiro no que alcancei.
