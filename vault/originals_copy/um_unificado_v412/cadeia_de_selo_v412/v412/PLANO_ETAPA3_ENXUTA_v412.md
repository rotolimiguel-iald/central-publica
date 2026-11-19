# Plano da Etapa 3 enxuta da v412 (gerência c1, 18/11/2026, noite)

Ordem do autor (bytes em `work\cunhagens_13out\`, arquivo que começa por `OPERADOR_18nov_nao_envie_mais_ordem_ao_codex`): ir até o fim sem outra IA; publicado quando ele acordar; nada pode depender dele. A gerência decidiu o escopo; o handoff diz tudo por extenso.

## Por que enxuta

Os scripts da cadeia v412 são cópias da v411, que não tinha módulo novo. A v412 tem 156 módulos novos, cinco registros novos e 5.478 bandeiras novas. Contei 74 scripts marcados `[A ADAPTAR v412]`: 39 na raiz, 7 em `bateria_pre_selo`, 5 em `bancada_B3_servico` e 23 em `pos_rito`. Adaptar todos de verdade não cabe numa noite com segurança. A Bancada (127.0.0.1:18777) não responde, o que impede o B(n) pré-selo.

## O que se faz

1. **Etapa 2** pelos scripts do construtor (`ETAPA_2_R7_ESTADO_v412.json`): kernel R12 a frio, âncoras, fecho do kernel, registros, candidato, recibos, portão do pilar, guarda de material privado, ensaio a seco, fecho `PREPARACAO_v412_PRONTA_R7.json`.
2. **Esperados enxutos** (`esperados_v412_foco.py` → `ESPERADOS_v412.json`), lidos dos artefatos:
   - o candidato (sha16 e bytes);
   - a origem (o `um.py` v411 selado);
   - a escada, as bandeiras novas e os 156 módulos com o sha256 do manifesto R12;
   - a raiz e o Audit antes (os do Nós) e depois (os do sandbox);
   - o pilar (chave e resultado);
   - o gate da v411;
   - as cinco palavras de veredito do contrato R11;
   - a referência do núcleo e do selo da v411 para a comparação.
3. **Instalador** (`instalar_v412.py`, adaptado pelo molde da v410): as travas de processo, origem, candidato, pilar e pedras anteriores; os 156 novos ausentes do Nós; a raiz e o Audit do Nós iguais aos da v411; os backups de bytes. A trava do recibo pré-selo do B(n) e a do pino da Bancada saem, como desvio declarado.
4. **Reversão** (`reverter_v412.py`): restaura os backups e retira os 156 módulos que o rito materializar.
5. **Rito** (`rito_v412.sh`): o corpo é genérico; muda só o cabeçalho descritivo, e a marca sai.
6. **Conferidor enxuto** (`conferir_pos_rito_v412_foco.py`), que compara o núcleo pós-rito com o núcleo selado da v411:
   - nenhum veredito herdado muda, salvo os que mudam por desenho;
   - todas as bandeiras herdadas e as novas de pé;
   - o gate igual;
   - o selo com `um_version` v412 e o `um.py` batendo com o pino;
   - os 156 módulos no Nós com o sha256 do manifesto;
   - a escada medida;
   - sem `sorry`.
7. **As três marcas e o handoff** (D232).

## O que não se faz esta noite (vai às decisões abertas do handoff)

- O B(n) pré-selo e pós-selo (a Bancada não responde).
- O serviço estático da Bancada.
- Os ensaios prévios da custódia em `pos_rito` (derivação, harnesses, prévia do X, harness do fechar).
- A varredura Fock/Omega, a purga, o relatório da preparação e o p00 completo.
- O conferidor herdado de 151 KB e o gerador de esperados herdado: seguem marcados e não rodam.
