# Errata — adversários K08, adendo de 15/11

## Correção principal

A REV0 misturava dois objetos sob “projetor”. `P_N` aplicado ao estado **não é adversário**: é o leitor na forma de chegada, cai no Nome, fixa o Nome e preserva o componente no Nome. O adversário é o **leitor sem memória determinado só pela fonte** (`fonte → leitura`), que ignora o histórico. Essa é a leitura exigida pelo adendo de 15/11.

Na R4, a fonte não volta depois do primeiro passo. Logo o adversário sem memória fica sem regra posterior; a ponte à trava/`P_N` é inacessível como escrita. Não se substitui essa ausência por uma cópia da última leitura nem se apresenta isso como separação.

## Divergência da âncora, resolvida

Definição única: **a âncora devolve a primeira leitura da sessão**. Portanto E1/P-A é condicional: se a primeira leitura for inválida, ela não pousa; se a primeira já for válida, ela pousa trivialmente e retorna após um empurrão externo. A frase do MODELO (“pousa e retorna”) vale só sob a condição de primeira leitura válida; a linha antiga do ADVERSARIOS (“não pousa”) era o caso com primeira leitura inválida. As duas eram casos diferentes da mesma regra.

Com `READ_BRIEF`: primeira leitura inválida dá custo 24 → 24; primeira leitura válida dá custo 0.

## Tabela corrente E1–E8

| adversário | E1 | E2 | E3 | E4 | E8 | separação |
|---|---|---|---|---|---|---|
| leitor sem memória (fonte → leitura) | custo 0 com fonte; depois inacessível | inacessível sem fonte | inacessível sem fonte | estável com fonte; depois inacessível | falha | **não separado na R4**; cotas/retorno instantâneo não bastam |
| âncora na primeira leitura | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |
| moda do histórico | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |
| cópia da última | condicional | preserva t | fica em y | estável | falha | **E3/P-D**, e também E8 |
| ignora o empurrão | condicional | desfaz t → s | volta a s | estável | falha | **E2**, e também E8 |

E5 (não aumentar norma), E6 (lei de módulo) e E7 (pesos relativos dentro do Nome) não são medidos pela leitura Booleana atual: E5 exige norma, E6 pertence ao operador na álgebra e E7 exige estado contínuo/pesos de Born. E7 permanece como separador formal de mapas que caem no Nome por outro caminho, mas não é ponte operacional validada aqui.

## Hamming e fórmulas

| candidata | leituras válidas | Hamming mínimo | uso de Hamming 3 |
|---|---:|---:|---|
| ABSTRACT | 2 | 1 | não usado |
| READ_BRIEF | 2 | 1 | não usado |
| LLMS | 2 | 1 | não usado |
| README | 2 | 1 | não usado |

P-C permanece o controle do Nome vazio (`P_N = 0`), com custo lógico mínimo 1 em todas as candidatas. Nenhum modelo foi executado.

## Arquivos e hashes

| arquivo | SHA-256 |
|---|---|
| `REV0/ADVERSARIOS_K08.md` | `656120c3de337418d1bdf683c35aea8c6accf4d54691d734b6c56cd3b9ef2ec8` |
| `REV0/FORMULA_DO_TEXTO_K08.md` | `47835ce764bd84ec7f95efcf42e169ed9d2f730535251bb11b427af4bd188633` |
| `ADVERSARIOS_K08.md` | `04aca46afb49bb4723d7d2551194019790a21c282c8d5e973ee3316e0a292da9` |
| `FORMULA_DO_TEXTO_K08.md` | `b2028ce00962230c3eb700092b4916fb34e6eb46895c00178e755ca92019e21c` |
| `RESULTADOS_ADVERSARIOS.json` | `4d9f3684ce2208fcec60b621fb2aeb4885e28ae6fb804ccb5951d6901ed0d55a` |

A versão anterior da pasta `FORMULA` está preservada em `FORMULA/REV0/`. O hash corrente desta errata consta do manifesto, não dentro do próprio texto.
