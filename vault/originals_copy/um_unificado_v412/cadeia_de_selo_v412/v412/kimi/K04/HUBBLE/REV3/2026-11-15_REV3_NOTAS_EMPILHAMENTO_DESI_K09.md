# Notas K09 — empilhamento, Fase 9 V2 e DESI DR3

## 1. O que o empilhamento contém e o que já estava na V2

A Fase 9 usa cinco leitores decisórios: SH0ES, CCHP, SBF, masers e TDCOSMO. A preparação V2 (`d1.fase9.v2_c1_a_unica_palavra_23out`, seq 1353, 1354, 1360 e 1656) também pinou variantes/leitores auxiliares, incluindo sirenes; isso não cria novas evidências independentes por contagem de entradas.

| Conta do revisor | Valores | Sobreposição com a V2 | Classificação obrigatória |
|---|---|---|---|
| SN II tailored EPM + TDCOSMO‑2026 | D = 4,04; 3,36 com sistemática SN II = estatística | **1/2 linha:** TDCOSMO já está na V2; 8 das 11 lentes de 2026 vêm da amostra anterior | Não cego, não independente, não composto aberto |
| SN II + TDCOSMO‑2026 + reanálise MCP + FRB localizados + BBH–AGN estendido | D = 5,34; 4,88 com sistemática SN II = estatística | **2/5 linhas:** TDCOSMO e masers são famílias já presentes; SN II, FRB e BBH–AGN estão fora da V2 | Não cego, não independente, três entradas só-estatísticas |

A reanálise MCP usa as mesmas cinco galáxias/família de masers; não se confunde “outro modelo” com “nova testemunha”. SN II, FRB e BBH–AGN, embora fora da V2, não têm ponte específica examinada. Portanto:

1. os valores 4,04/3,36 e 5,34/4,88 não são incremento sobre o poder da V2;
2. não se somam esses D ao D/poder da V2;
3. TDCOSMO e masers não entram duas vezes;
4. a vizinhança aritmética de 5 não satisfaz cegueira, independência, covariância ou contagem de tentativas.

Para lentes isoladamente, a estimativa do revisor sob escala 1/√N só estatística é cerca de **48 lentes equivalentes para 5σ** e **79 para D90**. É forecast, não medida nem data.

## 2. Critério DESI DR3

**Decisão documental adotada: DR3 entra como fundo.** A justificativa é a continuidade da evidência: DR1/DR2 já estão em D1/CAMB e BG1 contém Planck comprimido + DESI DR2. Atualizar a liberação muda o fundo; não produz uma determinação local de um passo nem cegueira retroativa.

Um uso **testemunhal de fundo, em pergunta separada**, só seria admissível com todos os atos anteriores à leitura:

1. observável, hipótese nula e estimador declarados;
2. mapa Ωm/R fixado antes do dado, porque a rota comprimida depende dessa escolha;
3. likelihood e covariância completas, variantes e veredito congelados por hash;
4. custódia de liberação ainda não lida e abertura única;
5. regra explícita contra dupla contagem: DR3 não pode ser fundo e testemunha do mesmo composto, e DR2/DR3 não são independentes sem covariância.

**Faltam hoje:** data de liberação nomeável; pacote likelihood/covariância; mapa Ωm/R decidido; pré-registro/hash; custódia e regra de abertura; demonstração de não dupla contagem com BG1. Na ausência desses itens, DR3 é atualização de fundo **não cega**, não nova testemunha e não caminho executável para 5σ.

## 3. Parede preservada

Essas notas não alteram a conclusão: não existe hoje teste cego de natureza com poder de desenho ≥ 5σ executável no setor Hubble. Também não ampliam exclusões: a leitura intermediária segue desfavorecida e não excluída, com a lei da face pendente e poder prévio 2,33σ. `NOT_FALSIFIED` não é `CONFIRMED`.
