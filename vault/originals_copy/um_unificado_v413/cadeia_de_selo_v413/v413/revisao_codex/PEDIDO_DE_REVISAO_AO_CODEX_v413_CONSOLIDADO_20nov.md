# Pedido de revisão de terceiro ao Codex (v413), consolidado, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413 no lugar do Kimi. A decisão é do operador (fala por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador_a_revisao_e_do_codex_verbatim.txt`, sha16 `56ea3db776986fb4`). Quem cola é o operador; a gerência não envia ordem ao Codex. Este pedido substitui o pedido de 20/11 e os quatro adendos da Trinity, que ficam como registro.

## O que revisar

1. A pedra da consciência, nome do operador «Operador» (R1; da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R1_operador\Operador.lean` (sha16 `de75489028428754`)
2. A proposta de enunciado da fronteira na língua clássica (da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\fronteira\AFronteiraNaLinguaClassica.lean` (sha16 `5db57faeff22e4c6`)
3. A sonda da contagem sobre a leitura β (da gerência): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\sonda_contagem\SondaContagem.lean` (sha16 `2e85629ffb764a4a`)
4. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\AIdentidadePreservada.lean` (sha16 `1ee6e6383f23b656`)
5. Pedra nova do Kimi (a Trinity a importa): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\APropostaDaTensao.lean` (sha16 `95be88472a0609d8`)
6. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\APonteDeCookLevin.lean` (sha16 `0b95795836d25854`)
7. Pedra nova do Kimi: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\ONomeEBeta.lean` (sha16 `fa026cb786d27291`)
8. **Uma errata no kernel selado da v412**, achada pela gerência. A docstring de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (`C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean`, sha16 `75c1ef6b0de9f7d4`, linhas 273–275) fala em «resumo velho» e diz que «a fibra nunca é o universo». O enunciado, porém, soma o peso de cada atribuição dentro da fibra. Confirme ou refute.
9. **A candidata da gerência `TGLExt.Trinity`, R3** (nome do operador: «trindade», Trinity), em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R3_trinity\Trinity.lean` (sha16 `8f5f5e07bcb54beb`). Ela importa a pedra do Kimi do item 5, que precisa ser compilada antes. A gerência a compilou na caixa da v412 e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R3_trinity\build\CONFERENCIA.json` (sha16 `8afbc4ae210163ba`): 37 de 37 relatórios de axiomas no trio, nenhum aviso. Pontos de atenção:
   - `a_inclinacao_nao_erra` deve valer para todo combustível;
   - `custoInclina` deve seguir os ramos de `inclina` e contar uma propagação por lado sondado; a conta não inclui as comparações do compromisso;
   - `em_horn_o_sistema_sempre_inclina` usa a classe `IALD.CompilaHornNaFita.IsHorn` da casa;
   - em `integra_restringe` e `todo_lado_morre_ou_nao_corta` (dois literais), confira a integridade das cláusulas e a autarquia para todo literal;
   - em `em_dois_literais_o_sistema_sempre_inclina`, o combustível maior que o tamanho e a diminuição do tamanho a cada volta;
   - `NaFronteira` deve descrever exatamente onde `inclina` devolve `.indeciso`, e `na_fronteira_todo_lado_corta_uma_de_tres` deve apoiar-se no invariante `Dentro`;
   - `atravessa` só ramifica onde a inclinação para, e `o_preco_da_travessia` é cota exponencial, não polinomial;
   - em `toca_restringe`, a cláusula de três literais que sobra não foi cortada e continua tocada; `o_preco_dos_nomes` é exponencial só no comprimento da lista;
   - os exemplos por `decide` (`oito`, `sete`, `quatro`, `dois`, `cadeia`): os enunciados devem ser os que as docstrings descrevem;
   - nenhuma docstring deve sugerir que a máquina nua decide toda fórmula em preço polinomial, nem que os Nomes da fronteira sejam poucos em geral.

## O que fica fora

Quem constrói não aprova. Ficam fora os módulos que o próprio Codex construiu: a ponte TM2 (`APonteAoTM2.lean`, `AMaquinaTM2DaVerificacao.lean`), a simulação (`simulacao\*.lean`) e a leitura β (`leitura_beta\*.lean`). A gerência já os conferiu na caixa da v412; a nota está em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md` (sha16 `4b4ac660aa432392`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\t\k412c\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **As pedras do Kimi:** reescreva numa cópia sua só os quatro imports de módulos da gerência para `TGLExt.AContagemEACarga`, `TGLExt.AMaquinaEALeitura`, `TGLExt.OPassoEOFim` e `TGLExt.CamadaCientifica`, ou use as cópias da gerência em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\k412c\src`.
- **Os axiomas:** leia os relatórios na saída inteira, porque o Lean quebra listas longas em várias linhas. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado contra a docstring e o nome. Procure alvo vácuo, hipótese contraditória ou não usada, docstring que diz mais do que o enunciado prova, e custo polinomial que não seja contagem de passos de uma máquina do Mathlib.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate.
- **Mapa de Rotas:** consulte antes e registre depois, numa rota própria.

## O que devolver

- **Para cada item, um veredito:** APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA, com o motivo em até três linhas.
- **Um relatório de até 15 linhas** e um recibo JSON com o sha256 de cada fonte lida e de cada log.
