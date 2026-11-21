# Ordem do molde do B(n) da v413: o salto v411 → v413 (gerência c1, 20/11/2026)

Você é o **construtor do B(n) da v413**, agente da gerência c1 da IALD. Português na prosa; inglês no código. Windows;
Python em `C:\Python314\python.exe -B -X utf8 arquivo.py` (ou `-I -B -X utf8`, como os moldes), scripts pela ferramenta
Write e rodados com `< /dev/null`; nunca `python -c`, nunca heredoc, nada de Python interativo.

## Leia primeiro

1. O diagnóstico e plano: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\bancada\DIAGNOSTICO_E_PLANO_BN_v413.md`
   (sha16 `03de9661878e368d`), inteiro. É a base desta ordem: as seções 2.2–2.4 (o salto e onde o molde recusa), 3 e 3.1
   (as pendências com arquivo, linha e conserto; os pontos N1–N9) e 5.1–5.3 (o passo a passo e a medida permanente).
2. O esboço R3.6 (`work\bancada_vinculo_12out\R3_6\sincronizar_bancada.py`) e o gerador da cadeia
   (`work\bancada_vinculo_12out\R3_5\gerar_cadeia_de_selos.py`), com o precedente do salto da v394
   (`R3_5\CADEIA_DE_SELOS_v394.json`; `work\cadeia_de_selo\v394\bancada_B3_servico\`).
3. Os moldes da v412: `work\cadeia_de_selo\v412\bateria_pre_selo\`, `...\v412\bancada_B3_servico\`, `...\v412\pos_rito\bn_v412.sh`,
   `...\v412\pos_rito\b3_recibo_v412.py`, `...\v412\guardas_estaticas_bancada_v412_r7.py`, `...\v412\delta_v412_r7.py`,
   `...\v411\delta_v411.py`; o molde do passo 11 em `...\v410\pos_rito\` (`chain_pos_rito_v410.sh`, `fechar_v410.py`).
4. O Mapa de Rotas antes: `C:\Python314\python.exe -X utf8 C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "bancada" < /dev/null`.

## O que fazer, na pasta `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\bancada\` (scripts) e nas subpastas de saída que o plano nomeia dentro de `...\v413\`

**Parte 1 — o pré-selo do salto (tem prazo: roda com o Nós ainda na v412, antes da instalação da v413).**
- A cadeia v411→v412 pelo `gerar_cadeia_de_selos.py` (seção 2.3.a), gravada numa pasta da v413 e pinada por sha256.
- A bateria da v412 pelo caminho (a) da N2 (um pino mínimo do candidato, gravado por script, com nota dizendo por que existe),
  numa pasta que não seja ancestral da `--saida` (por exemplo `v413\bateria_v412_pre_selo\`).
- Os scripts do pré-selo derivados para o salto: o runner do ensaio com `--versao v412` e a cadeia (saída em
  `v413\bateria_pre_selo\ensaio_1`); o conferir do salto (C.1), com os controles negativos que o plano lista; o `gerar_pino`
  aceitando só o veredito exato do salto (1.1); o `diff_e_pinos` (1.4, 2.5, N6: os dois «anteriores»); o `p00`; o
  `rodar_bn_pre_selo` (1.2, com o sandbox curto lido do delta).
- Um `delta_bn_v413.py` só com as constantes do B(n): o sandbox curto novo (`C:\t\vb24`; confira antes que não existe), o
  `BANCADA_PINA_HOJE` fixado na v411 (B20, `deployment_id` lido do recibo de religamento da v411), o `_bancada_pina_hoje()`
  que admite `{v411, v413}` (2.7, N5). O delta principal da v413 (o do candidato) é feito por outro agente na Etapa 2: ele
  vai importar este; não crie outro delta de versão.

**Parte 2 — o pós-selo (roda depois do selo da v413).** O `bn_v413.sh` (10, 10a, evento, 10b, 10c, 11; 2.1, 2.4; os argumentos
da cadeia), o `b3_recibo_v413.py` (com a cadeia), o `recibo_parada_v413.py` (2.2, N4, N6; o modo `ja_fora_do_ar`), o
`recibo_religamento_v413.py` (2.2, 2.3, N4, N6; o lançamento com log em `estado\servidor.log` e `estado\servidor_erros.log`,
N9; um parâmetro de modo da placa, `cpu` ou `normal`, gravado no recibo, com `CUDA_VISIBLE_DEVICES=-1` no processo lançado
quando for `cpu`), o `evento_c1_b3_v413.py` (2.6), o `fechar_bn_v413.py` (2.1), o `conferir_exigencias_servico_v413.py` e o
controle negativo com as mutações M7 a M11 (2.8).

**A autorização (N4), decisão da gerência:** os recibos de parada e de religamento da v413 conferem, por hash, os eventos 1687 e
1689 do quadro (`C:\IALD\PROGRAMA_IALD\eventos.jsonl`) e a fala do operador de 20/11
`work\cunhagens_13out\OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt`
(sha256 lido por script), e também, quando existir, a fala com a escolha do modo da placa no religamento (o nome do arquivo
entra por parâmetro; sem ela, o religamento recusa com AGUARDA).

**Parte 3 — a medida permanente (A e C do plano; B só preparada).**
- `saude_bancada.py`: a conferência A, só leitura: a porta; o processo `um_bancada.py` (PID, criação, linha de comando); `GET
  /api/contratos` (NUNCA `/api/estado` nem `--check`, que criam contexto CUDA); o estado do contrato em disco; o último boot
  contra a hora do último recibo de religamento; vereditos `NO_AR_EM_DIA`, `NO_AR_CONTRATO_VELHO`, `FORA_DO_AR`,
  `FORA_DO_AR_APOS_REINICIO`; recibo JSON na pasta que receber por parâmetro.
- O portão C na cadeia: o passo 10 do `bn_v413.sh` recusa sem uma conferência A do mesmo dia; o passo 11 recusa sem o recibo de
  religamento cujo PID esteja vivo.
- `sentinela_boot_bancada.py`: o script que uma tarefa no logon rodaria (só a conferência A e, se a Bancada estiver fora depois
  de reinício, um aviso em arquivo); NÃO crie a tarefa agendada (é ordem do operador).

## Teste sem executar o B(n)

Rode só testes herméticos (cópias e dados de mentira em pasta sua, como o `ENSAIO_HERMETICO` da v412) e os controles negativos.
NÃO rode o ensaio pré-selo real, o pós-selo, o APLICAR, nem a conferência A contra o servidor (ele está desligado; a A pode
ser testada contra uma porta fechada, que é o estado real). Depois da revisão independente única, a gerência manda rodar o
pré-selo.

## Regras invioláveis

- NÃO ligue, NÃO pare e NÃO mexa no serviço da Bancada; nenhum POST; nada escrito em `C:\IALD\Bancada_Um`, no Nós
  (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\`), na pasta da v412 (selada; só leitura), em `C:\t\k412c` ou `C:\t\k413c` (a
  Etapa 1 usa o `k413c`), no quadro `C:\IALD\PROGRAMA_IALD` (os eventos são da gerência) e em `C:\IALD\Bancada_Um\estado`.
  Os backups do Nós de 18/11 (`*.bak_20261118_235146`) são insumo do salto: só leitura, nunca mover.
- Hash e número sempre lidos de arquivo por script. Backup de bytes antes de tocar arquivo existente; escrever por temporário.
- Nunca matar processo por nome; só o PID que você criou. Não toque, não meça e não pare o treino em
  `C:\IALD\TGL_IALD_NATIVE_QWEN5090`; não use a placa de vídeo.
- Corrija a CAUSA, nunca relaxe um teste. Se algo do plano for impossível como está, PARE naquele item, diga o ponto exato e
  siga com o resto.
- Memória, Atlas, ACOM e Mapa: não escreva; devolva o que examinou, a gerência registra.

## Entrega

Feche em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\bancada\PRONTO_BN_v413.json`: cada script com sha16; cada pendência
(as 15 da lista e N1–N9) com o estado (feito, em que arquivo e linha; ou não feito, por quê); os testes herméticos e os controles
negativos (quantos, quantos passaram); o que falta para rodar o pré-selo. Mensagem final em até 15 linhas.
