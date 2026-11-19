# Nota operacional — somente desenho e autotestes

Nenhum modelo deve ser chamado por estes scripts. Nenhum resultado de modelo foi lido.

Comandos já executados, apenas sobre casos sintéticos embutidos:

```bash
python -B isomorfo.py self-test --report VALIDACAO_SINTETICA_ISOMORFO.json
python -B medir_ponto_fixo_comum.py --self-test --output VALIDACAO_SINTETICA_PONTO_FIXO.json
```

A transformação do artigo público está bloqueada até existir dicionário completo, revisto por duas pessoas e com `status=CONGELADO`. O arquivo de esquema atual é propositalmente vazio e não pode ser aplicado.

Fluxo futuro, sem executar agora:

1. preparar JSON de termos extraídos somente da entrada pública e dos gabaritos;
2. `isomorfo.py init --terms termos.json --seed-id <custodiado> --version <nova> --output <dicionario>`;
3. revisar cobertura e mudar o estado para `CONGELADO` apenas após as duas revisões;
4. `isomorfo.py apply` sobre uma cópia de trabalho e sobre a especificação das asserções;
5. medir tokens/dificuldade e congelar perturbações e análise antes de qualquer saída.

O extrator mínimo de `isomorfo.py` não substitui os `E_j` validados da R3. O script de ponto fixo mede somente `V2-RET` em **12 interações**: perturbação depois de `k=8`, alteração em `k=9` e retorno estabilizado em `k=10–12` (`p=8,r=10`). Não emite veredito global e rejeita trajetórias com apenas oito estados.

A versão anterior, incluído o esquema legado, está preservada em `REV0\`; a correção ao lado está em `..\..\ERRATA_CONTAMINACAO_R3_1.md`. O léxico continua incompleto e a transformação do artigo permanece bloqueada.
