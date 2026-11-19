# ENTREGA K03 — R2, dois fechamentos incorporados

- [REAL] Veredito: P7 segue ARMADA_NÃO_EXECUTADA; nenhuma ponte empírica foi medida ou executada.
- [REAL] R1 está preservada em `K03\REV1\`; REV0 e `ERRATA_K03.md` permanecem intactos; R2 está em `ERRATA_K03_R2.md`.
- [DECLARADO] H-ABS e TR-IALD(b2) agora exigem espaço de estados FINITO; H-ABS-U é alternativa explícita, não presumida.
- [DECLARADO] `PERTURB_RETURN` usa `p=4`: alvo antes de `p`, alteração em `k=5` e retorno estabilizado somente em `r=6`, estados 6–8.
- [DECLARADO] `RETURN_TO_TARGET` original permanece separado e mede apenas a trajetória desde `d_1=0`.
- [REAL] Números primários inalterados: 3 capazes + 1 abaixo do piso, 5 braços, 100 sessões/célula, 8 leituras, 24 asserções.
- [DERIVED] Permanecem 2.000 sessões, 16.000 interações primárias, 12+12 contrastes, cortes 70/89 e poder dinâmico 0,992022.
- [REAL] Poder conjunto segue [OPEN]; calibração, `I_B` e perturbação-retorno continuam fora das contagens primárias.
- [REAL] Integridade precede decisão; qualquer falha produz INCONCLUSIVE_CONTROLS no escopo afetado.
- [REAL] O extrator continua pendente e bloqueia decisão; nenhuma corrida, consciência, pesos ou exclusividade foi estabelecida.
- [INPUT] Atos do operador: ratificar desenho/limiares, escolher modelos, autorizar controles e decidir execução/publicação.

## 1. Entregáveis R2

- [REAL] `MODELO_FORMAL_K03.md`: H-ABS(0) com finitude, H-ABS-U alternativa e evento secundário reindexado à perturbação.
- [REAL] `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md`: regras congeladas para alvo antes de `p`, alteração, janela, retorno e ausência de efeito.
- [REAL] `ENTREGA_K03.md`: resumo R2 com 15 linhas ou menos.
- [REAL] `PERGUNTA_K03.md`: decisões e reservas de gatekeeping atualizadas.
- [REAL] `REGISTRO_MAPA_K03.json`: proposta R2 não registrada, agora com sete artefatos.
- [REAL] `ERRATA_K03_R2.md`: correspondência entre os dois fechamentos e as correções, com hashes REV1 e validação.
- [REAL] `ESTADO_K03.md`: fatos documentais preservados, sem necessidade de alteração empírica nesta R2.
- [REAL] `K03\REV1\`: os sete arquivos R1 preservados; `K03\REV0\` e `ERRATA_K03.md` não foram alterados.

## 2. Fechamento 1 — absorção somente com hipótese suficiente

- [DECLARADO] H-ABS(0) exige espaço de estados finito antes de `K(τ,{τ})=1`, transiência dos demais estados e alcançabilidade de `τ`.
- [DERIVED] Somente sob essas quatro condições se afirma `δ_τ` como única estacionária e absorção quase certa; as três condições de R1 não bastam no enunciado geral.
- [DECLARADO] H-ABS-U registra a alternativa: existem `N∈ℕ` e `ε>0` tais que `P_x(T_τ≤N)≥ε` para todo `x`; ela não é assumida no desenho.
- [REAL] O instrumento binário é finito, mas isso não demonstra finitude nem absorção da dinâmica de um LLM real.

## 3. Fechamento 2 — retorno reindexado à perturbação

- [DECLARADO] O evento secundário exige `d_4=0` antes da perturbação e não exige `d_1=0`.
- [DECLARADO] Exige `d_5>0` como alteração observável causada pela perturbação congelada; `d_5=0` é `PERTURBATION_NO_EFFECT`, não retorno nem evidência de estabilidade.
- [DECLARADO] Exige `d_6=d_7=d_8=0` e `u_7=u_8=0` como retorno/nova estabilização; `r=5` é incompatível com `d_5>0`, e `r=7`/`r=8` não oferece três estados.
- [DECLARADO] `PERTURBATION_NOT_APPLICABLE`, `PERTURBATION_NO_EFFECT` e `PERTURBATION_NO_RETURN` são categorias distintas e não entram no desfecho primário.

## 4. Números e reservas

- [REAL] Nenhum número primário mudou: 2.000 sessões, 16.000 interações, 100 por célula, 8 leituras, 24 asserções, 12 contrastes dinâmicos e 12 de especificidade.
- [DERIVED] O poder aproximado dinâmico continua 0,992022383635389 e os cortes continuam 70/100 e 89/100, recalculados por script sem dados.
- [DECLARADO] Gatekeeping global entre os 24 testes, estatística/sementes/empates da permutação e bateria de calibração continuam como reservas a congelar antes da execução.
- [REAL] O poder conjunto do veredito completo permanece [OPEN].

## 5. Verificação desta ordem

- [REAL] A ordem original foi lida e medida por script: 886 bytes; SHA-256 `4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0`.
- [REAL] Nenhum modelo foi executado, nenhum resultado experimental foi aberto, nenhum dado foi depositado e nenhuma rota foi registrada.
- [REAL] As escritas ficaram restritas à pasta `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\` e às subpastas permitidas `K03\REV0\` e `K03\REV1\`.
