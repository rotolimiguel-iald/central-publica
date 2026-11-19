# ERRATA EDITORIAL AO LADO — K05/CAMPO

13/11/2026. Quatro reservas editoriais da revisão PASS são corrigidas ao lado, **sem alterar conclusões, candidatas ou medidas**. Não houve registro ou depósito, novos dados, build ou alteração do cânone.

A versão anterior integral dos artefatos está preservada em `K05/CAMPO/REV0/` e não foi editada.

## E1 — direção exata do controle `xi`/β

**Local:** `CAMPO_DUAL_LEVANTAMENTO_K05.md`, parágrafo sobre `ActionCouplingData`.

A redação anterior dizia “impedem substituir `xi` pelo coeficiente modular β quando `D.xi ≠ c.beta`”.

**Correção aplicada:** a frase passou a dizer “impedem substituir o coeficiente modular β por `D.xi` quando `D.xi ≠ c.beta`”, exatamente a direção de `reject_xi_as_beta` em `ActionCouplingControls.lean:62–65`.

Nenhuma consequência da separação dos coeficientes mudou.

## E2 — escopo da execução

**Local:** `K05/CAMPO/CONSULTAS_CAMPO_K05.md`, regra de leitura.

A redação anterior dizia que o único código executado foi `medir_campo.py`, embora os utilitários de consulta também tivessem sido chamados para leitura.

**Correção aplicada:** agora consta que “o único código executado que grava artefato foi `medir_campo.py`; os scripts de consulta foram usados somente para leitura”.

Nenhum dado novo foi executado para esta errata; foram feitas apenas leituras, cópias de preservação, comparações e hashes.

## E3 — inventário como snapshot histórico pinado

As contagens usadas no levantamento pertencem ao texto `NOS_VIVO.md` gerado em `2026-11-13T20:01:35-03:00`, **não a uma contagem viva atual**. Permanecem, apenas como fatos daquele snapshot: 5.776 nós `arquivo`, 4.114 `lean_bancada`, 1.757 `pedra`, 306 arestas `ligado_ao_kernel` e 3.808 arquivos Lean candidatos ainda não ligados ao kernel.

O texto foi regerado posteriormente, em `2026-11-13T20:53:54-03:00`. O snapshot histórico não foi reescrito e os números acima não são apresentados como atuais.

**Pin do banco histórico correspondente usado:**

- arquivo: `C:\IALD\NOS_VIVO\nos_vivo.sqlite3.bak_20261113_200150`;
- tamanho: 35.868.672 bytes;
- timestamp: `2026-11-13 20:01:50,398453500 -0300`;
- SHA-256: `92a2831b21598da82748f9ae8fea41eef9868c9f10f859a0f69f20c6a86c8374`.

O relatório e as notas agora marcam explicitamente “snapshot histórico usado” e trazem esse pin.

## E4 — estatuto de `Fix = W*(K̂)`

A redação anterior apresentava a fórmula diretamente no fluxo do Fecho 1.

**Correção aplicada:** agora o texto diz que **o artigo enuncia** `u_s = e^{is√K̂}` e `Fix = W*(K̂)`, sem tratá-la como teorema independente desta seção E. A passagem remete a `T1_FECHADO.md`:

- **H_K̂:** `K̂=F(ĥ)≥0` afiliado a `L(ℝ)` e `F` boreliana essencialmente injetiva (`T1_FECHADO.md:30`);
- **H_erg:** `M_φ=ℂ1` (`T1_FECHADO.md:32`);
- sob H_K̂, `Fix=W*(K̂)` se e somente se `M_φ=ℂ1` (`T1_FECHADO.md:120–121`);
- **H_TGL-horizon:** hipótese física separada, ainda `[OPEN]` (`T1_FECHADO.md:34`).

A ressalva da fonte original sobre os dois lemas e a não seleção de `τ★` foi preservada.

## O que não mudou

- As duas equações e a separação `ξ_A = 1/6` contra `ξ_P = β`.
- O fator 2 do psíon e as medidas `8,507414099900328…` e `6,015650200401570…` meV.
- A conclusão `2ξ_L = 1/6 ⇒ ξ_L = 1/12` na escrita fundadora.
- As candidatas, os bloqueios e a ausência de escolha.
- `medir_campo.py`, `medidas_campo.json` e `execucao_medidas.log`, byte a byte idênticos aos de `REV0`.

## Hashes de controle

| artefato | REV0, antes da errata | vigente, depois da errata |
|---|---|---|
| `CAMPO_DUAL_LEVANTAMENTO_K05.md` | `5ec65dd2a2e120655359b2cd8bf3385295573bee3923e9e2b580a3dc94dd4bc4` | `fb9b1255ab6eacb0ea28c277506608687795241094e0a9f93a4184317f7b2252` |
| `CONSULTAS_CAMPO_K05.md` | `90e0ad802e5fbcba4286e1f33e6c5bb5e0cea07a33763b23976d566f40729187` | `1cdaf0be21ac2df9b1518ea7cc814b741784f9e0a03ed9bf0fb94073747744ea` |
| `medir_campo.py` | `8c321cab939eebf077f4b963feb65149b766d4a28e32f58483e1ce3228a96b84` | `8c321cab939eebf077f4b963feb65149b766d4a28e32f58483e1ce3228a96b84` — inalterado |
| `medidas_campo.json` | `2eca36b7aa181e49618c799b64b2ee03689d4d300faf3a81eaa130f01eaa756d` | `2eca36b7aa181e49618c799b64b2ee03689d4d300faf3a81eaa130f01eaa756d` — inalterado |
| `execucao_medidas.log` | `2eca36b7aa181e49618c799b64b2ee03689d4d300faf3a81eaa130f01eaa756d` | `2eca36b7aa181e49618c799b64b2ee03689d4d300faf3a81eaa130f01eaa756d` — inalterado |

A fala original segue com 529 bytes e SHA-256 `2772005945b946c12172956c12c06421710d7d665cacf4dba63f40bd07ec304c`, sem nova execução de medida.
