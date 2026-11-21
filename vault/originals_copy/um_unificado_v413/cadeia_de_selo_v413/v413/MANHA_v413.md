# O que falta da v413 depois das duas palavras do autor (gerência c1, 21/11/2026)

Estado da noite e motivos: `PLANO_DA_NOITE_v413_20nov.md` (notas do fim). Este roteiro é só o que resta. Tudo a partir de
`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413` (`$PK`), com `PY="/c/Python314/python.exe -B -X utf8"`.

## As duas decisões que são dele

1. **O nome Trinity** (marcador privado nº 28 da guarda; 685 ocorrências a mais que a v412, no `um.py`, no `Trinity.lean` e na raiz
   do kernel). As falas em que ele nomeia a pedra (20/11, `work\cunhagens_13out\OPERADOR_20nov_excelente_vamos_prosseguir_escreva_a_pedra_que_se_chamara_trindade_Trinity_verbatim.txt`
   e `…_porque_a_pedra_trinity_refere_se_a_fronteira_dos_tres_literais_verbatim.txt`) nomeiam; não liberam o marcador.
   - **Libera:** gravar a fala dele por bytes em `work\cunhagens_13out\OPERADOR_21nov_<resumo>_verbatim.txt` e passá-la à entrega com
     `--decisao TERMO_PRIVADO_ISENTO_v413 <fala> "o nome Trinity (e trinity, TRINITY) pode ir ao público na v413"`. A custódia grava
     `TERMO_PRIVADO_ISENTO_v413.json`.
   - **Não libera:** a pedra ganha outro nome dado por ele, e a v413 é selada de novo (reverter, candidato novo, rito). Nada abaixo.
2. **O religamento da Bancada** (DIAGNÓSTICO 5.2; o treino na placa): (a) esperar o treino acabar; (b) `cpu` (`CUDA_VISIBLE_DEVICES=-1`;
   o lago ainda toma até 60% da RAM livre); (c) `normal`. Ou publicar sem o religamento, como na v412 (`BN_DISPENSADO_v413`).
   - Gravar a fala dele por bytes em `work\cunhagens_13out\OPERADOR_21nov_<resumo>_verbatim.txt`.

## Depois das duas palavras (cerca de 30 minutos)

1. Conferência A de hoje (só leitura): `cd bancada && $PY -I saude_bancada.py --saida "<SAUDE_DIR do util_bn>"`.
2. A autorização com o modo: `$PY -I bancada/montar_autorizacao_v413.py <fala do modo> <cpu|normal>` → o texto vai em
   `V413_AUTORIZACAO_OPERADOR`; mais `V413_MODO_PLACA` e `V413_FALA_MODO_PLACA` (o NOME do arquivo da fala).
3. `$PY -I bancada/recibo_religamento_v413.py` (lança com log; confere a identidade servida em `/api/contratos`).
4. `CHAIN_DE=10c sh bancada/bn_v413.sh` (10c e 11: os três recibos juntos, o pino conjunto, a entrega na pasta `bench` do 1687);
   depois `$PY -I bancada/aviso_f06_v413.py` (o aviso F0.6 ao Codex).
   - Se ele escolher publicar sem o religamento: `--bn-dispensado <fala>` no compositor e `--decisao BN_DISPENSADO_v413 <fala> "…"` na entrega.
5. `CHAIN_DE=7 sh pos_rito/cadeia_pos_rito_v413.sh` (o compositor R2: o bloco «v413 SELADA», o adendo do desenho e o handoff; a guarda do
   título com o handoff; com `CHAIN_SUPERFICIES=sim`, `atlas_indice.py v413` e `porta_memoria.py`).
6. Os blocos `core_v413_selada` e `haja_luz_v413_selada` (os dois parágrafos de abertura do handoff, verbatim); a linha do `MEMORY.md`
   em «**DD/MM: SELADA; custódia em curso**» (pela fila, `memoria.py pinar`); `grep -c v413` em cada superfície.
7. `$PY pos_rito/conferir_mds_v413.py --exigir-arvore` (os `.md` apontam a v413 e trazem as derivações novas).
8. **Por último**: `$PY pos_rito/gerar_entrega_a_custodia_v413.py --decisao TERMO_PRIVADO_ISENTO_v413 <fala> "…"` (e, se for o caso,
   `--decisao BN_DISPENSADO_v413 <fala> "…"`); depois uma linha à `central-de-patentes-91`.
