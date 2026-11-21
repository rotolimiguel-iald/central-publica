# Roteiro de execução da v413 — da instalação à entrega à custódia

> Preparado pelo construtor da Etapa 3 (agente da gerência c1), 20/11/2026. **Nada daqui rodou no Nós.** Quem executa é a gerência.
> Git Bash. `PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413"`; `PY="/c/Python314/python.exe -B -X utf8"`. Todo script lê hash e número de arquivo.
> Validade no kernel não é creditação; o gate não se move; nenhuma parada desta lista é teste da natureza.

## 0. A partitura, antes de qualquer passo que possa dar negativo

| passo | o que decide | o que não decide | o que um negativo significa |
|---|---|---|---|
| portão do pilar (no rito, antes de parar qualquer coisa) | se o ambiente de software que o `um.py` vai sondar (torch, cuda, numpy, scipy, python, nome da placa) é o do cache do pilar | se o autoteste do motor, que o próprio `um.py` roda na placa mesmo no reuso, passa com o treino ocupando a placa | parede medida: o `um.py` recalcularia o pilar na placa; PARAR e avisar o operador |
| vigia do pilar (durante o rito) | se o `um.py` anunciou o reuso com a chave do cache ou o cálculo | nada sobre a teoria | parede medida: o rito é parado na hora (`PILAR_PARADA_v413.txt`); reverter e avisar |
| conferidor pós-rito | se o rito fez o que os esperados e o contrato dizem e não perdeu nada da v412 | a natureza; a creditação | defeito de montagem ou estouro de tempo do `lake build`; reverter ou rodar de novo |
| guardas (privada, título, frases, G1) | se os artefatos e os textos podem ir à custódia | o mérito | parada antes da custódia: corrigir, ou decisão do autor |

## 1. Pré-condições (nesta ordem; nenhuma escreve no Nós)

1. **A Etapa 2 fechou**: `PREPARACAO_v413_PRONTA.json` (`fechou: true`, `candidato.caminho/sha16/bytes`), `CANDIDATO_v413.json`, `PORTAO_DO_PILAR_CANDIDATO_v413.json`, `TOPO_RATIFICADO_v413_DERIVADO.json`, `BLOCOS_TEXTO_PUBLICO_v413.json`. A revisão de terceiro do candidato e a leitura da página ao autor (contrato R1, seção 7) são atos da gerência.
2. **Os esperados**: `cd "$PK" && $PY esperados_v413_foco.py [--candidato <caminho>] < /dev/null` → `ESPERADOS_v413.json`. Recusa (saída 2) enquanto a Etapa 2 não fechar. Confere o kernel embutido no candidato (os 21 novos e o corrigido com os bytes do bundle; os 155 outros da v412 intactos), a linha `UM_VERSION = "v413"`, as três linhas da guarda do rito e as **exigências da custódia** (o par `_V413_FONTES`/`_V413_VERBATINS2` e o nome `kh_n1_cobertura_v413`; o contrato R1 não os traz — se faltarem, o instalador recusa: corrigir o candidato).
3. **A guarda privada (fase pré)**: `$PY guarda_privada_v413.py --fase pre < /dev/null` → `GUARDA_PRIVADA_v413_pre.json`. Zero termos novos, ou PARAR: a decisão é do autor (o termo sai, ou a fala dele por bytes vai na entrega).
4. **Os textos da custódia em conferência**: `$PY montar_handoff_e_linhagem_v413.py --ensaio < /dev/null`. Hoje (20/11, 22h) a prosa e a NOTA passam; os blocos da Etapa 2 reprovam em 5 pontos (ver `PRONTO_ETAPA3_v413.json`, `achados_para_a_etapa_2`): F37b da guarda herdada nos dois blocos «P = nP» (a frase traz «P = nP» e «Turing» sem «relativo ao leitor» nem negação; vem da seção 2 da página R0) e «proved» sem estatuto em três blocos EN. Sem a correção, o compositor recusa gravar o handoff.
5. **O pré-selo do B(n)** (o salto v411 → v413), com o Nós **ainda na v412**: o comando do `bancada\PRONTO_BN_v413.json` (`sh rodar_bn_pre_selo_v413.sh`, em `bancada\`). Grava `PINO_RECIBO_PRE_SELO_v413.json`. Sem ele utilizável, o instalador recusa; `--sem-pre-selo-bn "<motivo>"` instala assim mesmo (desvio gravado; o salto se perde e o B(n) da v413 vira decisão do operador).
6. **O portão do pilar, para saber antes**: `python portao_ambiente_pilar_v413.py "$PK/ESPERADOS_v413.json"` (o `python` do PATH, o mesmo do rito; não toca a placa). Em 20/11 o ensaio deu `PORTAO_PILAR_OK` (`etapa3\TESTE_ETAPA3_SEM_CANDIDATO_v413.json`).
7. Nenhum `python um.py` vivo; o treino em `C:\IALD\TGL_IALD_NATIVE_QWEN5090` não é tocado, medido nem parado.

## 2. Instalar

`cd "$PK" && $PY instalar_v413.py < /dev/null > instalar_v413_out.txt 2>&1`

- Travas (todas antes de qualquer escrita): processo; origem v412 selada; candidato do ESPERADOS; exigências da custódia; pré-selo do B(n); cache do pilar; **todo arquivo do manifesto do kernel pinado pelo selo da v412** no Nós com o sha256 pinado; raiz e Audit da v412; os 21 novos ausentes; o **corrigido** (`TGLExt/OResumoEPsiBit.lean`) presente com o sha256 antigo.
- Grava: `.bak_<ts>` no Nós de todo arquivo pinado pelo selo da v412 (14), do selo, do sidecar, dos `.txt` pt/en, da raiz, do Audit e do corrigido (21 no total, cada selado conferido contra o selo); a cópia do cache do pilar em `pilar_anterior_v412_<ts>\`; `APLICADO_AO_CANONICO_<ts>.json`; a troca do `um.py` (temporário + troca atômica).
- Reverter: passo 6.

## 3. O rito (em segundo plano)

`cd "$PK" && sh rito_v413.sh > rito_v413_lancador_out.txt 2>&1 &`

- Recusas antes do rito: as do molde (6–10, 13–18) e duas novas: **19** (o ambiente da placa não é o do cache: PARAR e avisar o operador) e **21** (o portão não leu: PARAR). A VRAM **não é lida** (o treino está na placa; o pilar é reaproveitado); o servidor do modelo nativo só é parado (e religado no fim) se estava ligado.
- Grava: `Nós\rodada_v413_stdout.txt` (o canônico, byte a byte, com o trailer `RITO_RC=<rc>`), `rodada_v413_stdout_tempos.jsonl`, `rito_horarios_v413.txt`, `rito_servidor_v413.log`, `PORTAO_AMBIENTE_PILAR_v413_<ts>.json`; o `um.py` grava o kernel, o core, o selo, os artigos, as capturas.
- Durante: o **vigia do pilar**. Se aparecer `PILAR_PARADA_v413.txt`, o rito foi parado (`RITO_RC=SINAL_TERM`): avisar o operador e reverter.
- Abortar: `kill -TERM $(cat "$PK/.rito_v413.pid")` no Git Bash, conferindo antes `/proc/<pid>/cmdline` (contém `rito_v413`).
- Tempo: no sandbox, o `lake build` dos 22 módulos levou 765 s e o Audit 265 s; no Nós compila também os 96 dependentes antigos do corrigido (tempo-limite do `lake build`: 3600 s); a rodada da v412 levou 2 h 02 min. Se o `lake build` estourar, a verificação do kernel sai FAILED com rc 0: o conferidor reprova; rodar de novo (cache quente) e guardar o stdout e a captura da tentativa.

## 4. Conferir

`$PY conferir_pos_rito_v413_foco.py < /dev/null` → `CONFERENCIA_POS_RITO_v413_FOCO.json` (35 checagens; saída 0 só com TUDO BATE). Confere: o stdout (RITO_RC=0, a escada, o kernel, o autoteste, nenhum selo retido, o pilar reaproveitado com a chave), o selo (v413, pina o disco, o mesmo gate), nada da v412 perdido (troca dita), os registros do contrato R1 com as palavras e `all_verified`, os registros novos do core como o C1 da G1 os compara, a guarda de palavra proibida do rito lida do candidato, as bandeiras, os axiomas e a cobertura KH, o kernel (os novos, **o corrigido com o sha novo**, os outros da v412 intactos, a raiz e o Audit, o manifesto). Ensaiado num Nós falso: positivo e 7 mutações (`etapa3\ENSAIO_MUNDO_FALSO_v413.json`).

## 5. O pós-rito dos textos e o handoff

`sh pos_rito/cadeia_pos_rito_v413.sh` (passos 1 a 10; retomada `CHAIN_DE=<n>`; saída 20 = aguarda o B(n)):

1. o conferidor; 2. a guarda privada (fase pós) → `GUARDA_PRIVADA_v413_pos.json`;
3. **a árvore da prova**: `pos_rito\adaptar_arvore_da_prova_v413.py --executar` põe a linha das pedras da v413 no gerador da casa (`cadeia_de_selo\arvore_da_prova.py`, backup `.bak_<ts>_p413`), depois `arvore_da_prova.py v413` grava `Nós\A_PROVA_DA_QG_TGL_arvore.md` (título «… (v413)», backup);
4. **a guarda do título** (`pos_rito\guarda_titulo_versao_v413.py v413 --sem-handoff`: a regra do E03 da G1 sobre os declarados, mais a árvore e o handoff com a versão do selo);
5. os diffs (`pos_rito\diffs_v413.py`) → `DIFF_v412_v413.diff`, `DIFF_KERNEL_v413.txt` (mudados: só a raiz e o corrigido), `DIFFS_v413_RECIBO.json` (a máquina reproduziu os dois diffs da v412 byte a byte);
6. o elo B(n): sem os três recibos nem a decisão do operador, **aguarda** (rc 20): rodar `bancada\bn_v413.sh` (10 → 10a → evento F0.6 → 10b → 10c → 11; o modo da placa no 10c é escolha do autor) e retomar com `CHAIN_DE=7`;
7. **o compositor R2** (`montar_handoff_e_linhagem_v413.py`, conferência e depois `--executar`): o bloco «v413 SELADA» no `MEMORIA_DA_LINHAGEM.md`, o adendo no `DESENHO_DO_FECHAMENTO_QG.md` e, por último, `Nós\HANDOFF_v413_CUSTODIA.md` + `RECIBO_HANDOFF_v413.json`; `BN_DISPENSADO_FALA=<fala>` só se o B(n) não fechar;
8. a guarda do título com o handoff; 9. com `CHAIN_SUPERFICIES=sim`: `atlas_indice.py v413` e `porta_memoria.py` (senão, os comandos são impressos); 10. os passos à mão (abaixo).

**Atenção ao vigia da custódia:** com as três marcas no Nós (selo, linhagem, handoff + stdout), ele espera 30 minutos pela entrega e depois começa com os padrões. Gravar a entrega logo depois do handoff.

## 6. Reverter (só se o rito falhar ou o conferidor não bater)

`$PY reverter_v413.py < /dev/null` → confere tudo antes de escrever (backups, sha256 do selo da v412, o corrigido com o sha antigo), guarda o estado falho em `tentativa_v413_rito_falhou_<ts>\`, restaura os 21 backups, põe os novos em `quarentena_bundle_<ts>\` e confere: `um.py` = v412, o conjunto selado bate com o selo, o corrigido, a raiz e o Audit. Não restaura `.aux/.log/.toc/.out`, as capturas do kernel e o `.lake`. Recibo `RECIBO_REVERSAO_v413_<ts>.json`. Ensaiado no Nós falso: devolveu cada arquivo byte a byte.

## 7. À mão, nesta ordem, e por último a entrega

1. A linha do índice no `MEMORY.md`, pela fila e com o pino, **antes do C13 da custódia**: `- [HANDOFF v413 — …](handoff-v413-custodia.md) — **DD/MM: SELADA; custódia em curso**`.
2. Os blocos `core_v413_selada` (TGL_CORE_MEMORY.md) e `haja_luz_v413_selada` (CLAUDE.md da Haja_Luz), com os dois parágrafos de abertura do handoff verbatim (molde da v412; sem hash de commit retirado).
3. `grep -c v413` em cada superfície (linhagem, desenho, Atlas, índice vivo, core, CLAUDE.md da Haja_Luz, MEMORY.md): zero é falha visível.
4. **Por último**: `$PY pos_rito/gerar_entrega_a_custodia_v413.py [--decisao <ID> <fala> "<o que decide>"] < /dev/null` → `ENTREGA_A_CUSTODIA_v413.json` (esquema do modelo da custódia; os três sha256 lidos na hora; recusa sem o handoff, com o conferidor reprovado, com a guarda do título reprovando, com termo privado novo sem `TERMO_PRIVADO_ISENTO_v413` ou com o B(n) aberto sem `BN_DISPENSADO_v413`).

## 8. Fora desta etapa

O B(n) (`bancada\`, do construtor do B(n)); a tarefa agendada pós-treino (`C:\t\k413c\run_pos_treino.py` aponta para `orquestrador\pos_treino_v413.py`, que não existe); a revisão de terceiro; a leitura ao autor; o Zenodo.
