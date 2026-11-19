# ERRATA MODELO FORMAL R3.1 — horizonte operacional, aliases e nomes V2

## 1. Preservação e escopo

- [REAL] A versão anterior de `MODELO_FORMAL_R3_K06.md` foi preservada, antes da edição, em `K06\candidatas\REV0_DOC\MODELO_FORMAL_R3_K06.md`, com SHA-256 `91f0122dfd7d160ba07a6c58187f685d29adc755f3ea40e082c7d490dff200f7`, idêntico ao arquivo então vigente.
- [REAL] Foram alterados somente `MODELO_FORMAL_R3_K06.md` e esta errata, além da cópia preservada. Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto.
- [REAL] A candidata Lean e seus logs não foram alterados. `K06\candidatas\sandbox\LeitorFinito.lean` permanece com SHA-256 `77e18a01ff5c07b00cf24d53570baf205710320d99dc3b4826426084c6df7d8b`; `K06\candidatas\logs\LeitorFinito.txt` permanece com SHA-256 `4073b041233e7942b9b64860a70d268a1836c0d48afd400ca08ff23fd1b4c1fb` e o resultado já verificado `RC=0` em Lean 4.31.0.
- [REAL] `K06\candidatas\logs\auditoria_fonte.txt` também não foi atualizado: conserva o hash da versão REV0 do documento e não constitui uma nova certificação da emenda R3.1.

## 2. Inconsistências corrigidas

1. O modelo descrevia `K=8`, instruções e sementes até `k=8`, enquanto o protocolo principal usa 12 interações e `V2-RET` com `p=8,r=10`.
2. A transição de `G_k` não tornava explícita a inserção única da perturbação entre a saída `y_8` e a requisição `I_9`.
3. A tabela V2 apresentava `V2-EMB` e `V2-SEM` como braços, não incluía `V2-ISO-A/B` e deixava `V2-RET` na aparência de um braço adicional, em desacordo com o protocolo principal.
4. As notações `H-HOM` e `H-QUOT(k)` precisavam de faixa e distinção explícitas: homogeneidade temporal não é agregabilidade, e nenhuma das duas condições substitui a outra.

## 3. Emendas aplicadas ao modelo

### 3.1 Horizonte operacional de 12 interações

- `K=12`, instruções `Q_1,\ldots,Q_{12}`, entrada `I_k` e sementes para `k=1,\ldots,12`;
- `k=1,…,8` sem perturbação; `P_j` depois de `y_8`; `k=9` perturbado; `k=10,11,12` para retorno e permanência;
- as doze chamadas pertencem à mesma sessão lógica; a negação de limite infinito passou a mencionar doze leituras;
- `Q_k^*=Q_k` para `k≠9` e `Q_9^*=P_j`, exatamente a perturbação congelada, de modo que `P_j` entra uma única vez em `Frame(u,Q_9^*)` e não é reaplicada nas leituras 10–12;
- o horizonte de oito interações permanece apenas como histórico R2 explicitamente rotulado.

### 3.2 `V2-RET` com `p=8,r=10`

O evento operacional ficou

\[
R=1\iff d_8=0\land d_9>0\land d_{10}=d_{11}=d_{12}=0\land u_{11}=u_{12}=0.
\]

`u_{10}` é omitida intencionalmente porque `d_9>0` com `d_{10}=0` exige, no alvo binário, mudança entre `s_9` e `s_{10}`. O antigo `PERTURB_RETURN_{p=4,r=6}` e sua omissão de `u_6` permanecem somente como teste de esquema da R2, não como desenho operacional R3.

### 3.3 `A_8` preservado

`A_8` continua `d_6=d_7=d_8=0∧u_6=u_7=u_8=0`. Como `u_6` compara `s_6` a `s_5`, permanece derivado que `s_5=τ`: são **quatro estados finais**, `s_5,s_6,s_7,s_8`. O condicionamento por `d_1` não muda essa contagem, e `A_8` permanece anterior à perturbação.

### 3.4 Nomes V2 alinhados ao protocolo principal

- braço focal e controles: `V2-TGL`, `V2-PLA`, `V2-OUT`, `V2-ISO-A`, `V2-ISO-B`;
- `V2-RET` é a fase decisória de todos os braços, não um sexto braço;
- embaralhado e sem texto permanecem apenas canários descritivos de contaminação, fora dos 24 testes primários e sem aliases de braços primários;
- `IALD_COLLAPSE_V1` e a R2 permanecem intactos.

### 3.5 Aliases e dinâmica formal

- `H-HOM`: `K_k=K` para todo `k∈{1,…,12}`, hipótese de homogeneidade temporal;
- `H-QUOT(k)`: *strong lumpability* em cada fase `k∈{1,…,12}`; `H-QUOT(1…12)` abrevia a conjunção das doze condições;
- quando `H-HOM` e `H-QUOT(1…12)` são invocadas juntas, o núcleo quociente é o mesmo `\bar K` em todas as fases, sem dispensar a prova de agregabilidade;
- `G_k` continua um núcleo estocástico, não um mapa determinístico de estados;
- PASSO e LIMITE permanecem separados: `H-IDEM-STEP∧H-CONTR` continua forçando mapa constante, enquanto a projeção-limite pode ser idempotente sem que o passo o seja.

## 4. Conferência final

- [REAL] Não restam no modelo operacional `K=8`, instruções/sementes apenas até `k=8`, `V2-EMB` ou `V2-SEM`. As ocorrências de oito interações e `p=4,r=6` estão explicitamente marcadas como histórico R2; os demais numerais 8 são índices de `A_8`, `y_8`, `d_8`, referências do kernel ou identificadores bibliográficos.
- [REAL] Não foi necessário recompilar Lean: a candidata e os logs aprovados não foram tocados. A ponte `saída extraída → c : X → ℕ` permanece **OPEN**, e nenhum teorema sobre um LLM real foi acrescentado.
- [REAL] SHA-256 do modelo corrigido: `e560eaeca1db8b5ef3d25764b72e36ae3650fdd4a2b95ad43e8161055f9a95a3`.
