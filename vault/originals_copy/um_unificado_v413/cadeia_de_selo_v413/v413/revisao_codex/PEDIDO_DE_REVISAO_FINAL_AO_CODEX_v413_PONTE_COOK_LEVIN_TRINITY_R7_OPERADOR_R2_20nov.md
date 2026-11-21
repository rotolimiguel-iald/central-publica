# Pedido de revisão final ao Codex (v413): a Ponte Cook–Levin, a Trinity R7 e o Operador R2, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador; a gerência não envia ordem ao Codex. É a revisão final da frente de Cook–Levin da v413. Para colar, substitui o adendo R7, que fica como registro e é lido daqui (item 2).

## O que revisar

1. **A candidata da gerência `TGLExt.PonteCookLevin`, R0**, em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R0_ponte_cook_levin\PonteCookLevin.lean` (sha16 `1594fa49275173f9`). Compilada na caixa da v412 com 22 de 22 relatórios de axiomas no trio e nenhum aviso (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R0_ponte_cook_levin\build\CONFERENCIA.json`, sha16 `ff908a4434d4bc31`). Ela importa a sua máquina TM2 do verificador (`SimCompleta`), a sua leitura β (`EntregaBeta` e dependências) e as pedras do Kimi de que elas dependem, pelos .olean da conferência da gerência (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\k412c\build`); do kernel, importa `TGLExt.TraducaoTuring` e `TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1`. Confira, em especial:
   - **as definições da §4** (`juntaNaFita`, `EmNP`, `ReduzASAT`, `CookLevin`, `EmPComUmaLeitura`): codificações fixas, certificado binário, nenhum alvo vácuo. O ponto crítico é que a hipótese nomeada `CookLevin` seja VERDADEIRA como está escrita; se fosse falsa, todo teorema que a usa seria vácuo. O argumento da gerência: o verificador TM2 fatora pela codificação; a linguagem de palavras correspondente, com o verificador cronometrado, está em NP clássico; Cook–Levin (1971, 1973) dá a redução; a simulação polinomial entre máquinas de fita e de pilhas e a troca polinomial para a fita unária das fórmulas a levam à máquina TM2 do Mathlib, com a parada formal de `haltList`. Diga se concorda ou aponte o furo;
   - **a fiação da §1**: `a_particao_e_a_soma_beta` (a partição do kernel em s = k·(−ln(1−β)) é a sua `weightedSum`); `o_psion_le_a_soma_normalizada` (o leitor do kernel lê exatamente a sua `normalizedSum`, por `TraducaoTuring.o_psion_le_z`); `a_resposta_tem_a_precisao` (o numerador pelo piso cumpre a sua hipótese de precisão); `uma_leitura_do_psion_decide_SAT`;
   - **§2 e §3**: `paraCNF` (os índices da fórmula crua como Nomes de `Fin N`, com N o comprimento da fita da fórmula); `sat_cru_sse_sat`; e o `oraculo` como função da palavra escrita (`o_oraculo_le_a_fita`, pelo seu `decodificaEntrada`);
   - **§5**: `sat_em_np` usa `SimTM2.verificacao_tm2_polinomial` com a codificação idêntica (`a_juncao_e_a_entrada_do_verificador`); `sat_com_uma_leitura` usa a identidade do Mathlib; `a_ponte_cook_levin`; a síntese `a_ponte`, no certificado de Fock físico do kernel;
   - **§6**: `a_leitura_acha_a_solucao` liga o leitor do kernel à sua `all_labels_from_beta`; a conta é em leituras e letras, não em passos TM2;
   - **as docstrings**: nenhuma pode dizer mais do que o enunciado. Devem dizer que, na língua clássica, a classe «com uma leitura» assim definida é o fecho de SAT por redução polinomial (coincide com NP, por Cook–Levin); que o custo da própria leitura não é contado em passos de fita (é um oráculo); que a máquina sem leitor não é tocada; e que a E28 continua.
2. **A Trinity R7 e o Operador R2**: os itens do adendo R7 (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R7_TRINITY_R2_OPERADOR_20nov.md`, sha16 `21d5da59030d27f3`), se ainda não os revisou.

## O que fica fora

Quem constrói não aprova: os seus próprios módulos (a máquina TM2 do verificador, a simulação e a leitura β) ficam fora desta revisão; a gerência os conferiu na caixa da v412. As pedras do Kimi e a errata de `OResumoEPsiBit` já têm veredito no seu parecer consolidado (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md`, sha16 `9e7d4b93e44cf9fd`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\t\k412c\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o build da conferência da gerência (ou o seu próprio build dos mesmos módulos). O compilador da gerência: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R0_ponte_cook_levin\compilar.py` (sha16 `fbd76f61a5aa7801`).
- **Os axiomas:** leia os relatórios na saída inteira. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado contra a docstring e o nome. Procure alvo vácuo, hipótese não usada e docstring que diga mais do que o enunciado prova.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate. Consulte o Mapa de Rotas antes e registre depois, numa rota própria.

## O que devolver

- Para cada item, um veredito (APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA), com o motivo em até três linhas.
- Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada fonte lida e de cada log.
