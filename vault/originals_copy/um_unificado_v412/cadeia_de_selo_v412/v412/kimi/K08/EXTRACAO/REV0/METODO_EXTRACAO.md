# MÉTODO — LEITURA POR ESCOLHA FECHADA K08/R4

## Contrato semântico

A cada passo, para cada asserção fornecida, a resposta usa exatamente um destes rótulos:

- **SIM**: o texto afirma a proposição;
- **NÃO**: o texto afirma a negação ou uma proposição explicitamente incompatível;
- **O TEXTO NÃO DIZ**: o texto não afirma nem nega a proposição. Menção, citação sem endosso, presença de termos soltos e desconhecimento ficam aqui.

“NÃO” não significa “a proposição é falsa no mundo”, nem “eu discordo”. Não se usa conhecimento externo. Quando o texto contém P e ¬P, a ficha contém dois itens, um para cada proposição, e ambos recebem SIM. Isso registra a contradição sem criar um quarto rótulo; a insatisfatibilidade é verificada à parte, não pelo extrator de strings.

## Bloco fixo

```text
INICIO_LEITURA_K08
A01=SIM
A02=NÃO
A03=O TEXTO NÃO DIZ
FIM_LEITURA_K08
```

Há um registro por ID apresentado. Não se aceitam IDs ausentes, duplicados ou desconhecidos, rótulos traduzidos, registros fora do bloco ou mais de um bloco. Qualquer ambiguidade invalida o bloco inteiro para a medida conjunta; não se escolhe o bloco mais favorável.

A ordem dos IDs pode variar e é comparada por ID. Prosa antes/depois do único bloco é ignorada para o conteúdo, mas marca `outer_prose=true` e impede `canonical_format=true`. Essa tolerância é deliberada: evita repetir o falso negativo da antiga gramática que zerava uma leitura correta por uma linha de preâmbulo. Não se aceita prosa **dentro** do bloco.

## O que muda

- O modelo não precisa reproduzir sujeito–relação–objeto nem identificadores canônicos do protocolo; responde apenas sobre as asserções apresentadas.
- A pontuação é determinística por ID e rótulo, sem LLM juiz.
- Negação, silêncio e afirmação são três resultados distintos.
- Preâmbulo externo e embaralhamento deixam de destruir uma resposta semanticamente correta.
- Conformidade analisável, conformidade canônica e acerto de conteúdo são relatados separadamente.

## O que NÃO resolve

- Perguntar fornece vocabulário e proposições: mede verificação/reconhecimento, não extração espontânea nem descoberta da fórmula.
- Uma ficha pode induzir endosso; por isso há iscas e controle “só gramática” em `inducao.py`.
- Um copiador do gabarito ou uma regra fixa pode produzir formato perfeito. Formato nunca é evidência de convergência.
- O extrator não entende paráfrase: ele só lê rótulos. A interpretação da asserção continua sendo feita pelo respondente; em saídas reais será preciso gabarito humano independente.
- Os casos sintéticos testam o contrato do software, não a distribuição de respostas de modelos nem produção.
- O custo lógico de uma fórmula e a estabilidade temporal exigem camadas próprias; um bom escore num passo não demonstra pouso, retorno ou memória.
