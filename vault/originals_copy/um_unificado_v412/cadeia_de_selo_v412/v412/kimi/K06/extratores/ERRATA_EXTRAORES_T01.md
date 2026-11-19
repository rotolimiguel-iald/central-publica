# ERRATA EXTRAORES — T01: LeitorDoFundo pertence a TGLExt.AEscala

## 1. Erro e correção

[REAL] A versão anterior atribuía incorretamente T01 a `TraducaoTuring`. A conferência direta mostra `namespace TGLExt.AEscala` em `AEscala.lean:248` e `structure LeitorDoFundo` em `AEscala.lean:742`.

[REAL] O gabarito corrente fica:

- sujeito: `AEscala`;
- descrição: `Identifica LeitorDoFundo como tipo declarado em AEscala.`;
- tupla: `K06R1|T01|AEscala|declares_type|LeitorDoFundo|FORMAL`.

T02 não foi alterado. As taxas publicadas na versão anterior não valem para o gabarito corrigido; somente a revalidação abaixo sustenta as novas taxas.

## 2. Preservação e propagação

[REAL] Antes da correção, os 11 artefatos então existentes foram copiados integralmente para `REV0/`, inclusive código, especificação, bateria, relatório, resultados e manifesto. O manifesto preservado tem SHA-256 `7402d8d6b50034d81e7379c1acf0dc86a9e520a898d3d3c060c6dc39dc7f852a`.

[REAL] A correção foi propagada por `especificacao.json` e `gerar_casos.py` a todos os casos gerados. Também foram corrigidas seis ocorrências manuais em `casos/duplicacao.json`, incluindo a variante com espaços. `casos/casos.json`, `RELATORIO_EXTRAORES.md`, `resultados.json` e `manifesto.json` foram regenerados; não restou T01 com o sujeito antigo fora de `REV0/`.

## 3. Reservas de versão

[DECLARADO] C1–C4 da bateria são **LEGADOS, fora dos braços V2**. Isso está marcado em `especificacao.json`, no índice da bateria, no metadado `arm_scope=LEGADO_FORA_DOS_BRACOS_V2` de cada caso C1–C4 e no relatório. Esses braços servem apenas à regressão técnica do motor.

[DECLARADO] Os aliases ficam alinhados ao modelo R3: `H-TIME-HOMOG → H-HOM` e `H-LUMP → H-QUOT(k)`. A menção genérica do relatório foi atualizada para `H-QUOT(k)`; homogeneidade permanece hipótese separada.

[DECLARADO] Qualquer exemplo `p=4,r=6` é **LEGADO da R2, fora da R3 atual**. Nenhum desenho R3 foi alterado nesta correção.

## 4. Revalidação determinística

[REAL] Resultado após a correção:

- 690 casos sintéticos: 685 no contrato e 5 diagnósticos fora dele;
- acerto por asserção: 100% nas 120 asserções;
- sensibilidade e especificidade: 100% em T, C1, C2, C3, C4 e no cruzado E_TGL;
- erros próprios: 0; erros cruzados: 0; divergências E_T=E_TGL: 0;
- estado observado: `PASSA_NO_CONTRATO`;
- estado de produção: **BLOQUEADO_PARA_PRODUCAO**;
- `e` medido por braço: 0%; limite superior unilateral de 95%: 2,465540%; teto conservador de A8: 0,091028210.

[REAL] Uma segunda execução de `gerar_casos.py` e `validar.py` reproduziu bateria, relatório, resultados e manifesto byte a byte.

Hashes correntes:

- `especificacao.json`: `61ce3d394334892bf9a4efdc038141c2ed7754f594642feae9b74016b20cf0d2`;
- `casos/casos.json`: `edf71f74085663a6589c35f8aa7136e20620dad27735098cc423683d497a1dc6`;
- `casos/duplicacao.json`: `67efd282b03fc21a77b8249c9f1c05765f7e78878f74104a81f6e045aa0df9ae`;
- `RELATORIO_EXTRAORES.md`: `4fecf7b6f210dcbda1b22bb3091637e48de5e9acf1a7386ac2ef9cc66664e1d3`;
- `resultados.json`: `13460f78bbf43012616a34dd00245893ec702ff921087ae608a2aece79feba09`;
- `manifesto.json`: `4c5ddc355d3fe7183d121482c4c6289b439a4ceb73e86ba3db6d4149fec2ae17`.

## 5. Reprodução e escopo

```bat
cd /d "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\extratores"
python -B -X utf8 gerar_casos.py
python -B -X utf8 validar.py
```

Nenhum modelo foi executado, T6 não foi alterado e nenhum material reservado foi copiado. Não foram criados ENTREGA, REGISTRO ou depósito.
