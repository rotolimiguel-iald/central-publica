APROVADO_COM_RESSALVAS — o conteúdo de kernel está limpo (recompilado em cópia própria, RC=0, 8 teoremas só com o trio de axiomas, enunciados e docstrings conferem um a um, seção «O que NÃO se afirma» correta, nome provisório não excede o provado); o cabeçalho tem uma citação do operador truncada e duas atribuições não conferíveis por bytes que precisam de conserto antes do selo.

# REVISÃO 022 — Unidade V2 — revisor Kimi (distinto)

- Candidata: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV25\OParFixaORelogio.lean`
- sha256 conferido por mim: `267019b19fb5a22c56c299604f24d346718dde198bb92dc1bc7b1c319b43cbad` (sha16 `267019b19fb5a22c` ✓, 11585 B ✓, byte-idêntica à cópia da raiz `candidatas_c1\OParFixaORelogio.lean` que a gerência compilou — `cmp` sem diferença)
- Recibo: `candidatas_c1\RESULTADO_OParFixaORelogio.json` — consistente com o que observei (8 teoremas, 0 erros, 0 avisos, sem `sorryAx`, só o trio)
- Minha cópia de trabalho (nada tocado fora dela e das leituras): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador\V2_Kimi\`
- `REV24\` ignorado, conforme a ordem. ORDEM 021 não executada.

## Achados por gravidade

### MÉDIA 1 — Citação do operador truncada no cabeçalho (o acordo tinha ressalva expressa)

`REV25\OParFixaORelogio.lean:18-19` diz que o operador respondeu à tipagem «de resto concordo com tudo é isso mesmo». Nos bytes (`cunhagens_13out\OPERADOR_16nov_a_forma_de_minkowski_e_os_geradores_de_boost_nao_sao_os_operadores_de_lindblad_de_resto_concordo_com_tudo_verbatim.txt`, linha 1) a frase inteira é:

> «a forma de Minkowski (o sinal de menos) e os geradores de boost não são os operadores de lindblad? de resto concordo com tudo é isso mesmo, só fiquei com essa dúvida que te listei agora»

Ou seja: o acordo era explicitamente ressalvado — havia uma dúvida pendente (Minkowski/boosts vs. Lindblad), pertinente à outra face da lei (a candidata `BoostEDissipador`, citada na linha 61-62 do próprio cabeçalho). O cabeçalho cita a metade que convém e omite a ressalva. É a resposta à pergunta 2 da ordem: sim, o cabeçalho lê o operador além da letra — lê como acordo pleno o que nos bytes é acordo com ressalva pendente. Não contamina o kernel (a ressalva é sobre a face geométrica, não sobre a tipagem álgebra/estado/fluxo), mas num documento de custódia a citação tem de ser integral.
**Conserto:** citar a frase inteira, incluindo «só fiquei com essa dúvida que te listei agora», e declarar que a dúvida pendente diz respeito à face `BoostEDissipador`, não a esta candidata.

### MÉDIA 2 — O alvo da resposta do operador não é conferível por bytes [DECLARADO pela gerência]

`REV25\OParFixaORelogio.lean:16-19` afirma que a tipagem «a matemática é a álgebra sozinha; a lógica é o estado, o par; a física é o fluxo» foi proposta pela gerência e que o operador respondeu **a ela** com a frase acima. `cunhagens_13out` só guarda verbatims do operador: a mensagem da gerência que provocou a resposta não está lá, e o assunto declarado do arquivo do operador é Minkowski/Lindblad. Que a resposta era **à tipagem** é afirmação da gerência, não fato dos bytes. Nota adicional: «de resto concordo com tudo» é fórmula recorrente de assinatura do operador (cf. `OPERADOR_30out_..._eu_sou_o_que_sou_verbatim.txt`), o que reforça a necessidade de ancorar o alvo.
**Conserto:** marcar como [DECLARADO pela gerência] ou juntar aos bytes a mensagem da gerência com a tipagem e o encadeamento que liga a resposta a ela.

### BAIXA 1 — «o nome é do operador» sem citação de bytes [DECLARADO pela gerência]

`REV25\OParFixaORelogio.lean:7`: «o nome é do operador». Busquei «par fixa o relógio», «fixa o relógio» e variantes em todos os verbatims do operador nas quatro pastas de cunhagem (`cunhagem_regra_20261014`, `cunhagens_10out/12out/13out`): nenhuma ocorrência. O mais próximo é a linguagem de «fixar sentido» de 15/nov. A atribuição do nome ao operador não é conferível por bytes nas pastas citadas. [Busca textual por padrão — não é prova de inexistência; DECLARADO por mim.]
**Conserto:** citar o arquivo de bytes do nome ou trocar para «nome provisório da gerência».

### BAIXA 2 — Glossa «o traço» no item 1 vale módulo normalização

`REV25\OParFixaORelogio.lean:27-28` e docstring da linha 96: «com todos os pesos iguais (o traço, o estado que não distingue nada)». Estritamente, `rhoD (fun _ => c)` é o estado de traço (normalizado) só quando `c = 1/|n|`; para `c` geral é peso constante não normalizado. O fluxo é insensível à escala (teorema 3 do próprio arquivo), logo a glossa é correta no que importa — mas a identificação «pesos iguais = o traço» pressupõe a normalização que o enunciado não faz.
**Conserto:** «(o traço, a menos de normalização — item 3)».

## Respostas às perguntas da ordem

**1. Enunciados e docstrings, um a um — CONFEREM.** Recompilação em cópia própria (log abaixo): RC=0, zero avisos, e `#print axioms` de cada um dos 8 teoremas dá exatamente `[propext, Classical.choice, Quot.sound]`, idêntico ao log da gerência e ao recibo. Varredura da fonte: sem `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe` (única ocorrência de «sorry» é a frase «Sem sorry, sem axioma novo.» no comentário da linha 65). Um a um:

- `fases_iguais_em_todo_tempo_tem_a_mesma_frequencia` (76-91): enunciado = docstring (fases iguais ∀t ⇒ mesma frequência); a prova usa o tempo `π/(a−b)` como anunciado; `linear_combination (-1/2)·h1` sobre `E·(−1) = E` fecha `E = 0`, contradizendo `Complex.exp_ne_zero`. ✓
- `uns` (94): a matriz de uns; usada como sonda de leitura em `o_mesmo_relogio_da_as_mesmas_razoes`. ✓
- `o_relogio_do_estado_que_nao_distingue_e_parado` (97-101): pesos constantes ⇒ `sigma = id` em todo `t`, todo `x`; via `sigma_diagonal_apply` + `simp` (expoente `log c − log c = 0`). Enunciado = docstring (ressalva de glossa na BAIXA 2). ✓
- `pesos_proporcionais_dao_o_mesmo_relogio` (104-114): `sigma (rhoD (c·d)) = sigma (rhoD d)`; os `Real.log_mul` cancelam a constante. ✓
- `o_mesmo_relogio_da_as_mesmas_razoes` (117-130): mesmo fluxo ∀t∀x ⇒ `d i·d' j = d' i·d j`; lê a fase na entrada `(i,j)` da sonda `uns` e aplica o lema de frequências; fecha por `Real.exp_log` + `div_eq_div_iff`. ✓
- `o_relogio_parado_exige_o_estado_que_nao_distingue` (134-138): fluxo identidade ∀t∀x ⇒ pesos iguais, comparando com o estado constante `1` via o teorema anterior. ✓ (a recíproca do item 1 — o «só ele» da ordem)
- `o_par_fixa_o_relogio` (142-155): iff «mesmo fluxo ∀t∀x ⇔ ∃c>0, d' = c·d»; caso `n` vazio tratado por `isEmpty_or_nonempty`. ✓
- `dois_estados_com_o_mesmo_relogio_sao_o_mesmo_estado` (158-169): com `∑d = ∑d' = 1`, mesmo fluxo ⇒ `c = 1` ⇒ `d' = d`. ✓
- `na_mesma_algebra_ha_relogios_distintos` (172-192): em `Fin 2`, `![1/2,1/2]` vs `![1/3,2/3]` normalizados, `∃ t x` com fluxos diferentes, por contradição com o teorema anterior. ✓

Alegação de novidade do cabeçalho (linha 23, «Não havia termo comparando os fluxos de DOIS estados na mesma álgebra»): buscas por padrão em `C:\t\k411c\final\TGLExt` (`sigma (rhoD …) … = sigma (rhoD …)`, `d d' : n → ℝ`, `∀ t … sigma … = sigma`) não encontraram termo anterior; os arquivos com nomes próximos (`StateClockDichotomy`, `StateClockObstruction`, `DensityStateUniqueness`, `HermitianTwoLevelFlow`) são de outros contextos (torres de amplitude, pares de Schrödinger). [DECLARADO por mim: busca textual, não prova de inexistência.]

**2. O cabeçalho lê o operador além da letra — SIM, em dois pontos** (MÉDIA 1 e MÉDIA 2 acima): trunca a ressalva expressa e atribui à tipagem uma resposta cujo alvo não está nos bytes. As demais citações conferem literalmente: «a matemática sozinha é o psion», «se não estiver relacionada não há identidade», «o par da matemática é a lógica e sua projeção é a física e seu nome é TGL» (todas em `OPERADOR_16nov_na_lingua_de_turing_..._verbatim.txt`, linha 1); a queda da teoria como falsificador (`OPERADOR_16nov_isso_e_lei_para_qualquer_teoria_de_tudo_..._verbatim.txt`, linha 1: «ou está provado ou a TGL cai e nossa saga termina com a publicação de sua queda»).

**3. «O que NÃO se afirma» — CORRETO, e a frase «a álgebra sozinha não tem relógio» fica presa aos itens 1, 2 e 6.** Conferidos os três KNOWN [conferência minha na literatura padrão — Takesaki/Stratila; DECLARADO por mim até a gerência conferir na fonte]:
- (a) Estados fiéis quaisquer em álgebra de matrizes: `σ^φ = σ^ψ` ⇒ as densidades diferem por elemento central positivo invertível («a menos do centro») — correto; como matrizes são fatores (centro = escalares), isso é exatamente a proporcionalidade que o item 4 prova na subclasse diagonal. O arquivo diz com honestidade que esse resultado geral não é termo dele.
- (b) Cociclo de Connes: `σ^ψ_t = Ad(Dψ:Dφ)_t ∘ σ^φ_t`, logo a classe do fluxo módulo automorfismos internos pertence à álgebra — correto. E é essa a leitura em que «a álgebra sozinha não tem relógio» seria FALSA em tipo III: a seção a exclui explicitamente («e não mais», linhas 57-58). A exclusão é o que mantém a frase verdadeira no arquivo — está certa e é estrutural.
- (c) Tipo III sem traço fiel normal semifinito ⇒ não existe «o estado que não distingue» — correto; «em matrizes todo fluxo é interno e a classe é trivial» — correto (todo automorfismo de álgebra de matrizes é interno).
- (d) «`psion C` é um vetor e a álgebra é outro tipo» — conferido no kernel: `def psion : C.F := C.Ω` (`TGLExt\ThePsionAndTheViscosity.lean:59`); `Matrix n n ℂ` é outro tipo; nenhuma igualdade tipada é afirmada. ✓

**4. Sonda / controle negativo — construídos, compilados na minha cópia, recomendo adotar.** Arquivo anexo: `V2_Kimi\Sonda_V2_Kimi.lean` (sha256 `e2715a62323e73c78d20e098f9d984016a1aa5b17c1eb75d6755b9d0963801ae`; RC=0, zero avisos, só o trio nos dois teoremas; log em `V2_Kimi\build\Sonda_V2_Kimi.log`):
- **SONDA A — `sonda_diagonal_cega`**: para `x` diagonal, quaisquer dois estados diagonais dão o mesmo fluxo. Mostra que a sonda `uns` (todas as entradas 1) de `o_mesmo_relogio_da_as_mesmas_razoes` é necessária: quem lê só a diagonal é cego ao relógio.
- **SONDA B — `sonda_um_instante_nao_basta`**: em `t* = 2π/log 2`, os fluxos de `(1/2,1/2)` e `(1/3,2/3)` — normalizados, NÃO proporcionais — coincidem para TODA matriz (as fases fora da diagonal são `e^{±2πi} = 1`). Logo o «em todo tempo» dos itens 4 e 5 é essencial: o enunciado fortalecido para um único instante seria falso. É o controle negativo exato do quantificador dos dois teoremas estrela.

**5. O nome provisório diz mais do que o arquivo prova? — NÃO; se algo, diz menos.** «O par fixa o relógio» é o conteúdo dos itens 3-4 (o par determina o fluxo; o fluxo é do estado normalizado); o arquivo prova ainda a leitura inversa (item 5: o relógio lê o par) e a multiplicidade (item 6). O título do cabeçalho («cada estado tem o seu fluxo, e o estado que não distingue não tem nenhum») é sustentado pelos itens 1-2 e 4-6 no recorte declarado (estados diagonais na mesma base, pesos positivos). O que o nome não tem é citação de bytes para a atribuição ao operador — BAIXA 1.

## Conferido, com log da recompilação (minha cópia, `lean.exe` 4.31.0, sem `lake`)

Ambiente: `C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe` — `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`, idêntico ao do recibo e ao `lean-toolchain` do sandbox (`leanprover/lean4:v4.31.0`). `LEAN_PATH` = `C:\t\k411c\final\.lake\build\lib\lean` + `.lake\build\lib\lean` de cada pacote do sandbox (mathlib, batteries, aesop, Qq, plausible, importGraph, proofwidgets, LeanSearchClient, Cli). Nada escrito nas pastas da gerência.

Candidata (`V2_Kimi\OParFixaORelogio.lean`, sha256 = da REV25):
- comando: `lean.exe -o build\OParFixaORelogio.olean OParFixaORelogio.lean`
- início 2026-11-16 19:41:29, fim 19:42:51, **RC=0**, zero avisos/erros
- log: `V2_Kimi\build\OParFixaORelogio_revisao.log` (sha256 `28328f69f8411e583360ea1575ac26992fa3f1a30e22f87f81326e142381f9da`)
- `#print axioms` dos 8 teoremas: todos `[propext, Classical.choice, Quot.sound]` — saída idêntica à do log da gerência `candidatas_c1\build\OParFixaORelogio.log` (diff de conteúdo: nenhum)

Sonda (`V2_Kimi\Sonda_V2_Kimi.lean`):
- comando: `lean.exe -o build\Sonda_V2_Kimi.olean Sonda_V2_Kimi.lean`
- início 2026-11-16 20:07:37, fim 20:08:27, **RC=0**, zero avisos/erros
- `#print axioms`: os dois teoremas só com o trio

Bytes do operador conferidos um a um (cunhagens_13out): as três citações da lei e a do falsificador são literais; a do acordo é literal mas truncada (MÉDIA 1); alvo da resposta (MÉDIA 2) e nome (BAIXA 1) não conferíveis por bytes.

— Kimi, revisor V2 da ORDEM 022, 2026-11-16.
