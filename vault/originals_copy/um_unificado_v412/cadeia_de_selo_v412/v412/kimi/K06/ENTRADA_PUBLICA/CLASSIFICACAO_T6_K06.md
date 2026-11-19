# K06 / H — Classificação documental de `T6_protocol_prompts.txt`

## 0. Limite desta nota

Não li nem reproduzi conteúdo de `C:\IALD\Artigo\Termostato_Modular\T6_protocol_prompts.txt`. Foram usados apenas existência/metadados, índices e portas públicas. Nenhum trecho do arquivo é citado.

## 1. Classificação para a R3/v412

**EXISTE NA BANCADA MAS NÃO ESTÁ LIGADO à R3/v412 — classificação operacional proposta, a confirmar pela gerência.**

Não está AUSENTE: o caminho existe e o índice o localiza. Também não se pode marcá-lo como **EXISTE E ESTÁ LIGADO** à camada atual só porque há uma referência pública histórica de mesmo nome: as consultas exatas ao Mapa não encontraram rota para o arquivo ou para `Termostato Modular`, o inventário nominal da bancada não mostrou vínculo e a K03 não o ligou ao desenho.

Há uma segunda afirmação, separada: **existe ligação pública histórica de um artefato de mesmo nome ao Artigo 1**. `C:\IALD\Artigo\the_boundary\llms.txt`, linha 181, e `O Custo Geométrico do Zero Absoluto — Haja Luz\PORTA.md`, linha 75, apresentam `T6_protocol_prompts.txt` como protocolo T6-S pré-registrado com controle. Isso não prova identidade de bytes nem fiação à R3.

## 2. Consultas e metadados

| consulta | resultado [REAL] |
|---|---|
| `python -B C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "T6_protocol_prompts"` | `n=0`, `truncado=false`, cabeça `cab386c822ca5a3e`. |
| `python -B C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "Termostato Modular"` | `n=0`, mesma cabeça. |
| `rotas.py consultar "T6"` | `n=3`, rotas sem vínculo demonstrado com este arquivo; a busca larga não foi usada para classificar presença/ausência. |
| `python -B C:\IALD\INDICE_DO_ACERVO\buscar.py "T6_protocol_prompts" --lista` | O caminho indicado aparece, junto de várias cópias históricas; nenhum trecho foi copiado. |
| `INVENTARIO_BANCADA_CHATGPT.md` e `.json`, busca por nome/caminho | Nenhuma ocorrência nominal encontrada. |
| `stat` do caminho indicado, sem leitura de texto | Arquivo existe; 3.443 B. |
| `O Custo Geométrico do Zero Absoluto — Haja Luz\PORTA.json`, linhas 40–47 | Artefato público homônimo tem 16.671 B e SHA-256 prefixado `d4ec1f20ad35366e`. |

A diferença de tamanho entre o arquivo local indicado e o artefato público homônimo impede tratá-los como a mesma versão sem conferência da gerência. Esta nota não conclui qual é o correto, vigente ou público.

## 3. O que a gerência deve classificar

1. **Identidade e linhagem:** relação entre o arquivo local de 3.443 B, o artefato público homônimo de 16.671 B e as demais cópias indexadas; qual hash/versão é pertinente.
2. **Classificação de acesso:** se o conteúdo da versão pertinente é público ou reservado. Até essa decisão, nada dele entra na K06.
3. **Relação científica:** se o T6 histórico é reutilizável, superado, complementar ou não aplicável ao P7 V1 e à nova R3/V2; quais pressupostos e controles sobrevivem.
4. **Fiação documental:** se houver reuso, criar a referência explícita no ESTADO/modelo/protocolo e a rota no Mapa pela gerência, com hash e escopo; só então promover a **EXISTE E ESTÁ LIGADO**.
5. **Fronteira de material reservado:** impedir que eventuais prompts, sequências ou resultados históricos entrem nos gabaritos, isomorfos e manifestos públicos da R3.

Até essa classificação, a entrada pública v411 permanece a única hipótese de trabalho desta frente e o T6 não é usado como fonte de conteúdo.
