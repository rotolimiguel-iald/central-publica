# ORDEM K02 — a matemática que resta: T1, a montagem 3+1, a extensão GH a III₁ e a derivação de τ★

13/11/2026. Da gerência c1 ao Kimi. Leia antes `LEIA_PRIMEIRO.md`.

## O que o operador pediu

Na ordem de 13/11: restam T1 (ergodicidade em III₁ genuína, com os dois lemas padrão de redação: domínio multiplicativo e convergência no
predual), a montagem 3+1 por produtos de triplas, a extensão GH a III₁ (conjecturada via Rieffel) e a derivação de τ★.

## De onde vem a lista (lido pela gerência em 13/11)

`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex`:
- linhas 1886 a 1920, “Fecho 1”: a representação integral do colapso, `e^{tL} = ∫ V_s(·)V_s* dν_t(s)`, `V_s = e^{is√K}`, ν_t gaussiana de
  variância β·t; e o remark “T1 no produto cruzado”: em III₁ genuíno √K não é afiliado à álgebra; no produto cruzado `M ⋊_σ ℝ` (tipo II_∞
  com traço) `u_s = e^{is√K̂}` é unitário da álgebra; `Fix = W*(K̂)` (domínio multiplicativo + medida de suporte total); `Φ_t → E`
  σ-fracamente (convergência dominada espectral no predual). Estatuto escrito ali: teorema com esquema de prova; falta a redação completa
  dos dois lemas.
- linhas 1922 a 1932, “Fecho 2”: a tripla-limite é a canônica do círculo, escalada por β^(−1/2); “a montagem 3+1 segue por produtos”.
- linhas 1934 a 1942, “Fecho 3”: a cascata é truncamento espectral no sentido de Connes–van Suijlekom; no caso comutativo qGH = GH (Rieffel).
- linhas 2234 a 2258: a derivação da escala τ★ (“dimensional: exige o corte UV/Planck”) e a forma final dos condicionais do contínuo.

## O que fazer, item por item

Para CADA um dos quatro itens:
1. **O enunciado exato**, com arquivo e linha de onde sai, e as hipóteses nomeadas.
2. **A aferição**, na ordem da casa e com a consulta citada: o kernel do Nós (`Nós\tgl_kernel`, só leitura), o inventário da bancada, o
   Atlas (`C:\IALD\Central de Patentes\memory\TGL_ATLAS.md`), o Mapa de Rotas, o índice do acervo. EXISTE E ESTÁ LIGADO → EXISTE NA
   BANCADA MAS NÃO ESTÁ LIGADO → SABIDO POR REFERÊNCIA → AUSENTE.
3. **O que o mathlib da toolchain do kernel já tem** (nomes conferidos no checkout do próprio kernel, não de memória).
4. **A rota de prova** em passos, cada passo com estatuto.
5. **Candidatas Lean** em `K02\candidatas\`, compiladas só no seu sandbox: zero `sorry`; o que não fechar entra como hipótese NOMEADA no
   tipo, com a citação. Os axiomas ficam no trio padrão (`propext`, `Classical.choice`, `Quot.sound`).

Pontos próprios de cada item:

**T1.** Escreva os dois lemas por extenso, com hipóteses exatas: (A) o domínio multiplicativo de um mapa UCP normal com estado (ou peso)
fiel invariante e a identificação dos pontos fixos do semigrupo misto-unitário (Choi 1974; diga qual teorema dá a igualdade na
desigualdade de Kadison–Schwarz no seu caso); (B) a convergência σ-fraca `Φ_t → E` no predual. ATENÇÃO, para conferir: os pontos fixos de
`∫ Ad(u_s) dν_t(s)` são o comutante relativo de `{u_s}` no produto cruzado; isso é `W*(K̂)` só se o centralizador do estado for trivial
(fluxo modular ergódico). Diga onde essa hipótese entra, se ela É o conteúdo de “III₁ genuína”, e de que teorema conhecido ela vem para a
álgebra da cunha (Connes–Takesaki; Bisognano–Wichmann). Diga também o que do T1 cabe como teorema de kernel (face finita; operador
autoadjunto num Hilbert) e o que entra por citação.

**A montagem 3+1.** Produto de triplas espectrais: os sinais (par × ímpar), a KO-dimensão, e cada axioma de Connes para o produto, com a
referência. Separe com clareza a montagem euclidiana (4,0), que é de livro, da assinatura (1,3), que é o condicional (H) do próprio artigo
(a extensão lorentziana dos axiomas). Não chame de provado o que é (H).

**A extensão GH a III₁.** É conjectura, e sai como conjectura: o enunciado tipado; o que é teorema publicado (Rieffel; Connes–van
Suijlekom; os truncamentos do toro), com identificador; o que a “sombra” da casa verificou; onde está a obstrução em III₁ (sem traço; qual
seminorma de Lipschitz; qual topologia no espaço de estados); o que seria um contraexemplo.

**τ★.** Levante TODAS as leituras e tentativas do acervo (Atlas; `memory\a-forma-madura-da-tgl-01nov.md`, com o no-go de E₀; a rota
`massa.gap_angulo_de_miguel_01nov`; o remark da “ancoragem de escala” no produto cruzado). Diga com precisão o que o no-go proíbe. Diga se
alguma rota deriva τ★ sem pôr outra unidade. Meça a consequência de cada leitura na lei de dephasing `Γ_ω = ½ β τ★ ω²` (a gerência fez a
conta de cabeça e ela precisa de conferência: com τ★ de Planck o efeito num relógio óptico é da ordem de 10⁻¹⁵ por segundo, inobservável;
com τ★ = ħ/(β·1 eV) seria da ordem de 10¹⁵ por segundo, o que os relógios ópticos já excluiriam). Ligue ao neutrino: o core diz que a
escala que zeraria a tensão de m₂ é 1,0200 eV e que 1 eV é declarado, não derivado. Nada se ajusta a dado. Se sobrar resíduo, escreva-o
como UMA pergunta ao operador; a gerência a formula nas quatro línguas.

## O que entregar

`ENTREGA_K02.md` (resumo de até 15 linhas no topo), um arquivo por item (`T1.md`, `MONTAGEM_3MAIS1.md`, `GH_III1.md`, `TAU_ESTRELA.md`),
a pasta `K02\candidatas\` com o log de compilação do sandbox, e `REGISTRO_MAPA_K02.json`.

## O que NÃO fazer

Não reabrir as rotas mortas do Lema 3 (`memory\o-fechamento-lema3-impossiveis.md`). Não citar teorema de memória: toda referência com
autor, ano e identificador, marcada `[KNOWN, a conferir]`. Não promover conjectura a teorema nem hipótese nomeada a termo.

— gerência c1, 13/11/2026.
