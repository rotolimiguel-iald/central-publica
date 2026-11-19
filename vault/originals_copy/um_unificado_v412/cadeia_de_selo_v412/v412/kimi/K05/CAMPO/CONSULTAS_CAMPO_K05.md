# K05/CAMPO — consultas, cobertura e classificação de existência/fiação

## 1. Regra de leitura

Estas notas documentam o recorte consultado antes de qualquer formulação de ausência. Resultado vazio em uma consulta **não** é prova de ausência universal. “Existe” distingue arquivo/documento, bancada e kernel; “ligado” exige consumo/importação/registro explícito, não homonímia.

Nenhum arquivo de origem foi alterado. Não houve execução do `um.py`, build Lean, registro ou depósito. O único código executado que grava artefato foi `medir_campo.py`, que lê fontes e escreve `medidas_campo.json` nesta pasta; os scripts de consulta foram usados somente para leitura.

## 2. Inventário vivo e índice geral

### NÓS VIVO

Fonte: `C:\IALD\NOS_VIVO\NOS_VIVO.md` e `consultar.py`.

- **Snapshot histórico usado, não contagem viva atual:** o texto `NOS_VIVO.md` foi lido quando havia sido gerado em `2026-11-13T20:01:35-03:00`, com 5.776 nós `arquivo`, 4.114 `lean_bancada`, 1.757 `pedra`, 306 arestas `ligado_ao_kernel` e 3.808 arquivos Lean candidatos ainda não ligados ao kernel. [REAL — snapshot `NOS_VIVO.md:3,7–15,32–45,132–136`]
- **Pin do snapshot:** o banco histórico correspondente `nos_vivo.sqlite3.bak_20261113_200150`, de 35.868.672 bytes e timestamp `2026-11-13 20:01:50,398453500 -0300`, tem SHA-256 `92a2831b21598da82748f9ae8fea41eef9868c9f10f859a0f69f20c6a86c8374`. O texto foi regerado depois, em `2026-11-13T20:53:54-03:00`; o snapshot histórico não foi reescrito e seus números não são apresentados como contagem viva atual.
- Consequência de método: presença como `lean_bancada` não foi promovida a presença no kernel. A data explica por que a fala e os arquivos da custódia posteriores podem não aparecer no grafo; a fala foi lida diretamente e conferida por hash.

Consultas executadas e resultado usado:

| consulta | resultado e uso |
|---|---|
| `python C:\IALD\NOS_VIVO\consultar.py "campo dual" --n 20 --max 1600` | Devolveu dual scaling, dual weight e documentos correlatos, não uma identidade da cunhagem. Não usado como ausência. |
| `... "holonomia" --n 25 --max 1600` | Localizou `TheDeathOfTheSignal`, `TransportWitness`, `Cocycle`, `AbsoluteOne` e `OIgual`. As duas primeiras fontes foram abertas e citadas. |
| `... "Fecho 1 radical" --n 25 --max 1600` | Localizou radical, regra quadrática, `TheFiveHalves`, `GNSQuotient` e investigações correlatas. A fonte primária do Fecho 1 foi aberta no artigo da Ponte. |
| `... "DecisionCommutation" --n 20 --max 1800` | Confirmou o módulo canônico `TGLExt.DecisionCommutation`; lido nas linhas 69–228. |
| `... "F1.FECHO fluxo gradiente" --n 25 --max 1800` | Localizou `ObserverInside`, `ModularFlow`, `LightIsJ`, rotas GKLS e o Fecho. Não promoveu a conexão ao campo `Ψ_μ`. |
| `... "regra quadratica" --n 30 --max 1800` | Localizou `regra_quadratica_v394` e `F1.FECHO_20261015`; usado para separar regra quadrática de normalização do campo. |
| `... "sqrt beta sqrt K" --n 30 --max 1800` | Localizou registros de dissipação e módulos de raiz positiva/grafos. A fórmula foi conferida no `um.py` e no Fecho 1. |
| `... "Psi conjugacao modular" --n 30 --max 1800` | Localizou `psi_emergence`, conjugações polar/modular e `TheRecordOfJ`; nenhuma ponte adicional foi inferida. |
| `... "omegaSq ActionCouplingData" --n 25 --max 1800` | Devolveu a tentativa `B1_PRIME_012/TheSameBetaReadsFourFaces` e a rota da massa; as duas fontes canônicas foram lidas separadamente. |
| `... "ação única Psi" --n 25 --max 1800` | Devolveu ocorrências lexicais de “única” e ações duais da representação regular, não uma ação que dê as duas equações-alvo. Classificado como não localizado no recorte, não inexistência universal. |
| `... "recursão da luz" --n 25 --max 1800` | Localizou módulos de luz e recursão, mas não substituiu a fonte histórica `recursive_light_v3.tex`, encontrada pelo índice/Atlas. |

### INDICE_DO_ACERVO/buscar.py

O índice informa 13.608 arquivos no filtro usado. As consultas abaixo foram realmente executadas:

| padrão | saída e interpretação |
|---|---|
| `"dois coeficientes|não se fundem|nao se fundem|coeficientes.{0,80}fund" --lista --max 100` | 5 arquivos, sem o registro canônico procurado. Não foi usado como negativa: a frase foi encontrada diretamente no `um.py:182860`. |
| `"os dois coeficientes nunca se fundem|TheSameBetaReadsThreeFaces" --ctx 260 --max 40` | 0 arquivo no índice consultado. O `um.py` corrente e o manifesto v354 prevalecem como fonte primária. |
| `"campo dual conjugado vetor cinético loop holonomia radical" --lista` (via rotas e buscas afins) | Consulta conjunta excessivamente restritiva; resultado vazio não usado como classificação. |
| `"campo de processamento dual" --ctx 300 --max 20` | 0 arquivo indexado; a fala original foi lida diretamente, 529 B e hash conferido. |
| `"Recursão da luz|recursão infinita|Psi_\{n\+1\}|Ψ_\{n\+1\}" --ctx 300 --max 40` | Encontrou `recursive_light_v1/v2` e documentos correlatos. A versão `recursive_light_v3.tex` indicada pelo Atlas foi aberta. |
| `"sqrt\(beta\).*sqrt\(K\)|√β.{0,20}√K|Phi_D" --ctx 300 --max 40` | Encontrou implementações e a composição R88, além de material histórico. Somente fontes abertas foram citadas. |
| `"W\*\(√K\)|W\*\(sqrt K\)|W\*\(K\).*sqrt|sqrt.*W\*\(K\)" --ctx 260 --max 30` | 6 arquivos, incluindo a métrica da fatia `ds = sqrt(beta)|d sqrt(k)|`; confirmada em `A Ponte Einstein Cartan Miguel.tex:1104–1118`. |
| `"Psi.{0,50}(conjugad|conjuga|holonom)|Ψ.{0,50}(conjugad|conjuga|holonom)" --caminho "Nós" --max 50` | Muitos documentos históricos de conjugação de psíons; não demonstrou ponte `Ψ* ↔ J ↔ holonomia`. Não usado como ausência universal. |

### Mapa de Rotas (`rotas.py`)

Estado comum das respostas: 2.056 registros, cabeça `03042aca2e30e8cf`.

| consulta | n | observação |
|---|---:|---|
| `consultar "coeficientes acoplamento conforme beta" --limite 30` | 0 | Não implica ausência; a v354 foi lida no `um.py`. |
| `consultar "campo dual conjugado vetor cinético loop holonomia radical" --limite 50` | 0 | Consulta conjunta muito restritiva; não usada como ausência. |
| `consultar "gkls sqrt radical fecho" --limite 30` | 0 | O Fecho 1 foi lido na fonte primária. |
| `consultar "holonomia loop recursão" --limite 40` | 0 | Fontes de holonomia abertas no kernel e no Artigo A. |
| `consultar "recursive_light" --limite 30` | 0 | O documento histórico existe e foi lido; não está promovido a rota canônica. |
| `consultar "v354" --limite 20` | 0 | O registro histórico foi encontrado no bloco `v353–v354` do `um.py`, não por esta consulta. |
| `consultar "artigo_a.acao.normalizacao_do_acoplamento_nao_minimo" --limite 20` | 2 | Rota vigente da errata e rota da vitrine. A vigente diz que o 2 está no cânone como dispersão do psíon `[INPUT]`, que a forma do campo segue aberta desde R82 e que não se deve escrever o ½ na vitrine. |

A rota vigente é evidência do estado da custódia, não substituto das fontes primárias; todas as suas peças centrais foram conferidas diretamente. [REAL — resposta JSON da última consulta, 13/11, e `ERRATA_DA_LEITURA_DO_MEIO_13nov.md:57–69`]

## 3. Kernel, Atlas e fontes diretas

### Kernel lido

- `PontoZeroDoPsion.lean:22,32–40,60–77,85–110,155–225`: dispersão, fator 2, massa, natureza `[INPUT/ONTO]`, tempo do retido e bicondicional de frequência.
- `TheSameBetaReadsFourFaces.lean:5–56`: EOM como input, `xi` independente, campo complexo com operadores ℝ-lineares.
- `ActionCouplingControls.lean:30–40,50–80`: modelo condicional, não seleção de `xi`, recusa de substituir β por `xi`.
- `ConjugateAct.lean:58–105`: troca de faces e involução.
- `LightIsJ.lean:59–73`: J preserva o par e inverte o gradiente.
- `TheGravitonIsTheConjugatedPhase.lean:55–66,75–128`: conjugação complexa de fases e declaração explícita de que a ponte ao `towerJ` não está feita.
- `TransportWitness.lean:259–279`: holonomia infinitesimal e caso plano.
- `TheDeathOfTheSignal.lean:73–88,104–149`: dependência do laço, normalização e ida-e-volta.
- `ContinuousModularZero.lean:66–94,203–217`: gerador modular e conexão escalar.
- `ModularCurrent.lean:56–115` e `TheCurrentConnectsTheCorners.lean:132–168`: corrente matricial entre faces.
- `AbsoluteOne.lean:83–107,117–131`: `Ψ = 1_abs` e fluxo trivial.

Buscas por `Ψ*`, `Ψ†`, `Psi.*conj`, `J.*Ψ`, `Fecho 1`, `√K` e combinações foram usadas apenas para localizar candidatos. Não se inferiu inexistência pela grafia: a mesma noção aparece como `star`, `conj`, `conjTranspose`, `sqrt`, `sqrt(K_partial)` e texto LaTeX.

### Atlas consultado, sem leitura integral

- `TGL_ATLAS.md:737–747`: auto-conjugação, radicalização e controle negativo.
- `TGL_ATLAS.md:792–801`: J, `JKJ = −K` e estatuto tipado.
- `TGL_ATLAS.md:1593–1595`: `L = √β√K_∂`.
- `TGL_ATLAS.md:1624–1628`: dois psíons conjugados e spin-2, com estratigrafia.
- `TGL_ATLAS.md:2296–2309`: camadas distintas do psíon, sem fusão.
- `TGL_ATLAS.md:2381–2388`: recursão histórica e colisão de β.
- `TGL_ATLAS.md:5522–5524`: v353/v354, `TheSameBetaReadsThreeFaces`.
- `TGL_ATLAS.md:898–902`: leituras `[INPUT/ONTO]`, dispersão e outras entradas não promovidas a teoremas.

O Atlas foi usado como índice remissivo; as afirmações centrais foram abertas nas fontes primárias.

### Custódia e R88 reutilizados

- `LEITURA_DA_PARTITURA_O_MEIO_13nov.md`: apenas álgebra e citações do Artigo A; classificação AUSENTE e recomendação não usadas.
- `ERRATA_DA_LEITURA_DO_MEIO_13nov.md`: leitura vigente, duas equações, 1/12, carga modular e R82/R89.
- `VEREDITO_VERIFICADOR_LEITURA_DO_MEIO_13nov.md:5–20`: conferência independente da álgebra e ressalva explícita de que `(Φ, Ψ*)` pode ser o par, não `(Ψ, Ψ*)`.
- `DESENHO_DO_FECHAMENTO_QG.md:2587–2670`: R82–R89.
- `SPECTRAL_RULE_REUSE_R88.md:19–47`: composição do dissipador, `D=√K` contra `D_circ`, conexão e limite da busca.
- `ONE_FORM_FULL_SOURCE_R88.md:5–120`: EOM de 1-forma, gauge, norma, versão complexa e resíduo escalar.

## 4. Classificação final de existência/fiação

| item | existência | fiação e bloqueio |
|---|---|---|
| EOM do Artigo A | Artigo A, `um.py`, kernel | Ligada como equação/input; não derivada de uma ação única comum. |
| Dispersão do psíon | Kernel e `um_absoluto_pt.txt` | Ligada como definição `[INPUT, Tratado §3]`; o 2 sustenta a massa. |
| Não fusão `xi`/β | `um.py` v354, kernel v355 | Explícita em texto e controles; posterior `ξ=β` precisa de objeto/acoplamento tipado, não fusão silenciosa. |
| `(Ψ,Ψ*)` | Fundador e Artigo A | Não presente como par no `ActionCouplingData`; o kernel só tipa valores complexos. |
| J modular | Vários módulos do kernel | Ponte com conjugação complexa do campo aberta; `TheGravitonIsTheConjugatedPhase` declara a falta da ligação ao `towerJ`. |
| Vetor gauge | Fundador e Artigo A | `A_μ`/`Ψ_μ` existe; mapa ao escalar e ação conjunta abertos. |
| Vetor espectral | Ponte, `um.py`, `ContinuousModularZero`, R88 | Existe como diferencial/conexão; mapa a `Ψ_μ` não localizado. |
| Loop/holonomia | `TransportWitness`, Artigo A, `TheDeathOfTheSignal` | Existe em tipos distintos; identidade com holonomia U(1) e recursão aberta. |
| Recursão histórica | `recursive_light_v3.tex` | Documento `[DECLARADO]`, outro β; não é fiação canônica da nova cunhagem. |
| Radical `√K` | Fecho 1, runtime, R88 | Fluxo existe; não identificado ao loop do vetor nem às duas EOM. |
| Ação única para as duas equações | Não localizada no recorte canônico consultado | `[OPEN]`; a fundadora tem arquitetura próxima, mas não os dois coeficientes/objetos na forma requerida. |

## 5. Medidas e arquivos produzidos

- `medir_campo.py`: fonte das contas e pins literais; lê apenas os arquivos-fonte e grava nesta pasta.
- `medidas_campo.json`: `1/12`, `2ξ_L = 1/6`, razão de norma ao quadrado 2, massas com/sem o fator 2, razão `√2`, 529 B e hash da fala, dez pins verificados.
- `CONSULTAS_CAMPO_K05.md`: estas consultas e classificações.
- `../CAMPO_DUAL_LEVANTAMENTO_K05.md`: achados, candidatas e bloqueios, sem escolha.

A validação final consiste em reexecutar `medir_campo.py` e conferir que suas asserções e os dez pins terminam sem erro.
