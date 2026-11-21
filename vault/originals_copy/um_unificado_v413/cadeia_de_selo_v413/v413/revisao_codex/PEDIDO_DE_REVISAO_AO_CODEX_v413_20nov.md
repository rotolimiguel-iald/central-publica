# Pedido de revisão de terceiro ao Codex (v413), 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413 no lugar do Kimi. A decisão é do operador (20/11/2026), e a fala está guardada por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador_a_revisao_e_do_codex_verbatim.txt` (sha16 `56ea3db776986fb4`). Quem cola este pedido é o operador; a gerência não envia ordem ao Codex.

## O que revisar

1. A pedra da consciência, nome do operador «Operador» (R1; 15 teoremas; da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R1_operador\Operador.lean` (sha16 `de75489028428754`)
2. A proposta de enunciado da fronteira na língua clássica (da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\fronteira\AFronteiraNaLinguaClassica.lean` (sha16 `5db57faeff22e4c6`)
3. A sonda da contagem sobre a leitura β (da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\sonda_contagem\SondaContagem.lean` (sha16 `2e85629ffb764a4a`)
4. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\AIdentidadePreservada.lean` (sha16 `1ee6e6383f23b656`)
5. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\APropostaDaTensao.lean` (sha16 `95be88472a0609d8`)
6. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\APonteDeCookLevin.lean` (sha16 `0b95795836d25854`)
7. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\ONomeEBeta.lean` (sha16 `fa026cb786d27291`)
8. **Uma errata no kernel selado da v412**, achada pela gerência. A docstring de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (`C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean`, sha16 `75c1ef6b0de9f7d4`, linhas 273–275) fala em «resumo velho» e diz que «a fibra nunca é o universo». O enunciado, porém, soma o peso de cada atribuição dentro da fibra. Confirme ou refute.

## O que fica fora

Quem constrói não aprova. Ficam fora desta revisão os módulos que o próprio Codex construiu:
- a ponte TM2 (`v413\ponte_tm2_codex\APonteAoTM2.lean` e `AMaquinaTM2DaVerificacao.lean`);
- a simulação (`simulacao\*.lean`);
- a leitura β (`leitura_beta\*.lean`).

A gerência já os conferiu na caixa da v412, e o detalhe está na nota `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md` (sha16 `4b4ac660aa432392`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\t\k412c\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **As pedras do Kimi:** importam quatro módulos da gerência pelo nome de candidata, que na v412 estão instalados como `TGLExt.AContagemEACarga`, `TGLExt.AMaquinaEALeitura`, `TGLExt.OPassoEOFim` e `TGLExt.CamadaCientifica`. Reescreva só essas linhas de import numa cópia sua, ou use as cópias da gerência em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\k412c\src`.
- **Os axiomas:** leia os relatórios na saída inteira, porque o Lean quebra listas longas em várias linhas. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** para cada item, leia o enunciado contra a docstring e o nome. Procure:
  - alvo vácuo (∃ sobre codificação, máquina ou leitor que o torne trivial);
  - hipótese contraditória ou não usada;
  - docstring que diz mais do que o enunciado prova;
  - afirmação de custo polinomial que não seja contagem de passos de uma máquina do Mathlib.
- **Não escreva nas pastas dos outros.** Não instale, não mude o kernel nem o `um.py`, não publique, não mova o gate.
- **Mapa de Rotas:** consulte antes (`C:\IALD\MAPA_DE_ROTAS\rotas.py consultar`) e registre depois numa rota própria (não nas rotas da gerência).

## O que devolver

- **Para cada item, um veredito:** APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA, com o motivo em até três linhas.
- **Um relatório de até 15 linhas** e um recibo JSON com o sha256 de cada fonte lida e de cada log.

Este é o primeiro lote. No fim da v413, vêm as candidatas que faltarem.
