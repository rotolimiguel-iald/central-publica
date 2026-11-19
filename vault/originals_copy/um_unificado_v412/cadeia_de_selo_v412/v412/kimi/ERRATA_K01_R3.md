# ERRATA K01 R3 — FAIXAS INTERMEDIÁRIAS DE S NONINDEPENDENT

[DECLARADO] Errata ao lado, de 13/11/2026. `REV0`, `REV1`, `ERRATA_K01.md` e `ERRATA_K01_R2.md` permanecem intactos. A versão R2 foi preservada em `K01\REV2\` antes destas alterações. Números JUNO inalterados. Nenhum teste empírico nem dado observado; somente casos sintéticos. Nada foi registrado nem depositado.

## 1. Inconsistência corrigida

[REAL] Na versão R2, S `NONINDEPENDENT` com `3≤rS<5` podia desaparecer em `TENSION_P` quando `3≤rP<5`, ou em `UNDER/ARMED` quando `rP<3`. O caso concreto `rP=2`, S `NONINDEPENDENT`, `rS=4` era classificado como `ARMED`, escondendo a tensão intermediária de S.

[DECLARADO] A tabela NONINDEPENDENT completa agora é:

| r_P | r_S | Ramo |
|---|---|---|
| r_P ≥5 | r_S <5 | `SINGLE_P`, inalterado |
| r_P ≥5 | r_S ≥5 | `BOTH_NONINDEPENDENT`, inalterado |
| 3≤r_P<5 | r_S <3 | `TENSION_P` |
| 3≤r_P<5 | 3≤r_S<5 | `TENSION_BOTH_NONINDEPENDENT` |
| 3≤r_P<5 | r_S ≥5 | `SINGLE_S`, inalterado |
| r_P <3 | r_S <3 | `UNDER/ARMED` |
| r_P <3 | 3≤r_S<5 | `TENSION_S_NONINDEPENDENT` |
| r_P <3 | r_S ≥5 | `SINGLE_S`, inalterado |

[DECLARADO] Com S `INDEPENDENT`, `TENSION_BOTH` continua somente com ambos em `[3,5)`, e `rS≥5` com `rP<5` continua `SINGLE_S`. `FALSIFIED` permanece exclusivamente com **rP≥5 ∧ rS≥5 ∧ S INDEPENDENT ∧ integridade P/S**.

[DECLARADO] A implementação mantém a precedência especial de `rP≥5`, depois aplica a tabela para `rP<5`:

```text
if s_state == "NONINDEPENDENT":
    if r_s >= 5: return "SINGLE_S"
    if r_p >= 3 and r_s >= 3: return "BOTH_NONINDEPENDENT"
    if r_p >= 3: return "TENSION_P"
    if r_s >= 3: return "TENSION_S_NONINDEPENDENT"
    return _under_armed(d_p)
```

[DECLARADO] O caso `rP=2`, S `NONINDEPENDENT`, `rS=4` agora devolve **`TENSION_S_NONINDEPENDENT`**, não `ARMED`.

## 2. Tokens completos e cobertura sintética

[DECLARADO] `K01_validar.py` usa tokens completos para todos os resultados, inclusive `UNDER` e `ARMED`, para que a abreviação não esconda o ramo:

- `TGL_NU_M2_TENSION__SINGLE_P_AWAITING_INDEPENDENT_CONFIRMATION`;
- `TGL_NU_M2_TENSION__SINGLE_S_AWAITING_INDEPENDENT_CONFIRMATION`;
- `TGL_NU_M2_TENSION__BOTH_NONINDEPENDENT`;
- `TGL_NU_M2_TENSION__P`;
- `TGL_NU_M2_TENSION__S`;
- `TGL_NU_M2_TENSION__S_NONINDEPENDENT`;
- `TGL_NU_M2_TENSION__BOTH`;
- `TGL_NU_M2_FALSIFIED`;
- `TGL_NU_M2_NOT_FALSIFIED_UNDERPOWERED`;
- `TGL_NU_M2_ARMED_CONSISTENT`;
- `TGL_NU_M2_MATCHED_PROSPECTIVELY`;
- `INCONCLUSIVE_SYSTEMATICS__INTEGRITY_P/S`;
- `AWAITING_SOURCE_P`.

[DECLARADO] A cobertura inclui todas as combinações da tabela e as fronteiras `rP=3`, `rS=3`, `rP=5` e `rS=5`:

- `rP=5, rS=3,5` → `SINGLE_P`, nunca `BOTH_NONINDEPENDENT`;
- `rP=5, rS=5` → `BOTH_NONINDEPENDENT`;
- `rP=3, rS<3` → `TENSION_P`;
- `rP=3, rS=3` → `BOTH_NONINDEPENDENT`;
- `rP=4,999, rS=4,999` → `BOTH_NONINDEPENDENT`;
- `rP=3, rS=5` e `rP=4,999, rS=5` → `SINGLE_S`;
- `rP=2,999, rS=2,999` → `ARMED`;
- `rP=2, rS=4` → `TENSION_S_NONINDEPENDENT`;
- `rP=2,999, rS=3` e `rP=2,999, rS=4,999` → `TENSION_S_NONINDEPENDENT`;
- `rP=2,999, rS=5` → `SINGLE_S`.

[DECLARADO] Os controles anteriores continuam: P/S ausentes, independentes em todas as faixas, ambos independentes em `[3,5)`, `MATCHED`, integridade intrínseca e a fronteira entre covariância intrínseca e cruzada. Nenhum caso usa dados observados.

## 3. Propagação e fonte JUNO inalterada

[REAL] Foram atualizados `PRE_REGISTRO_CEGO_RASCUNHO_K01.md`, `CANAIS_K01.json → neutrino_m2_juno.funcao_veredito`, `ENTREGA_K01.md`, `PERGUNTA_K01.md`, `REGISTRO_MAPA_K01.json`, `K01_validar.py` e `VALIDACAO_K01.json`.

[REAL] Os números JUNO aprovados não foram alterados: Δm²₂₁,pred = 7,237609466718292×10⁻⁵ eV²; planning = 7,388×10⁻⁵ eV²; σ_total = 0,078×10⁻⁵ eV²; D = 1,9281; 5σ pede 0,407121 %; D90 pede 0,324061 %; 0,5 % dá D = 4,0712; 0,3 % dá D = 6,7854. O poder conjunto permanece [OPEN]. A fonte primária da liberação de 207,2 dias permanece `arXiv:2609.37895v1`.

[DECLARADO] `JUNO publications` continua apenas como índice institucional, não como rol atualizado de 2026.

## 4. REV2 — preservação com tamanhos e hashes

[REAL] A versão R2 foi copiada antes das alterações para `K01\REV2\`. Estes valores pertencem à R2, não à R3.

| Arquivo REV2 | Bytes | sha256 |
|---|---:|---|
| `2026-11-13_REV2_ENTREGA_K01.md` | 29829 | `82b645713586c1da5c4511017818588df902a2678aaac2ca9d9d9cb3eb464bdf` |
| `2026-11-13_REV2_CANAIS_K01.json` | 88648 | `496f9517e860b5b25c8f1b58b00073cd9d8406b7415896a5babebac8bdae34da` |
| `2026-11-13_REV2_PRE_REGISTRO_CEGO_RASCUNHO_K01.md` | 25696 | `6bb0213f0473b961d434edb8fa8c46f8d21c2a76cadb58def820ee58fcf7b6ad` |
| `2026-11-13_REV2_REGISTRO_MAPA_K01.json` | 9740 | `423977b66c210c8dddb726a16035f4f81c0ff5853e6d9e52b802681abe6883ce` |
| `2026-11-13_REV2_PERGUNTA_K01.md` | 5860 | `61d661b43cacd538829b39a00706f5133d9a4650c3ffe59493120ecb01b13c25` |
| `2026-11-13_REV2_K01_validar.py` | 21193 | `99702d8915f713242967ede060d8f72e983c0beb55095698fff16b85efc68282` |
| `2026-11-13_REV2_VALIDACAO_K01.json` | 11793 | `b721fc7a6ed95051cb852b9e139cda41f68e9bb0bfa681c3c71786d22b8e3d32` |
| `2026-11-13_REV2_ERRATA_K01_R2.md` | 7100 | `52912e7691afd74d2dd88eaeb857a4b120fa21bea285b788f845c6bbd94bfbf0` |

[REAL] Backup local: [REV2](C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01\REV2). `VALIDACAO_K01.json` contém uma seção própria para REV2, além das seções REV0 e REV1 e dos novos hashes canônicos.

## 5. Estatuto após R3

[DERIVED] A inconsistência intermediária foi removida sem alterar planning, precisão, fonte ou poder JUNO. A conclusão de ausência de canal pronto permanece.

[DECLARADO] A conferência final pode verificar a tabela completa, os casos sintéticos com tokens completos e os hashes atualizados. `NOT_FALSIFIED ≠ CONFIRMED`; o gate permanece imóvel; nenhum teste empírico nem dado observado; somente casos sintéticos; nada foi registrado nem depositado.
