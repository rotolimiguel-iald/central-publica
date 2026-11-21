# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ADENDO de revisao ao Codex (v413), depois do parecer consolidado (que cobriu a Trinity R3 e o
Operador R1): a Trinity R5 (a §13 da R4 e o que a R5 acrescenta) e o Operador R2 (so' texto). Hashes lidos aqui.
Quem cola e' o operador; a gerencia nao envia ordem ao Codex."""
import hashlib, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
CS = AQUI.parent.parent
CEN = CS.parent.parent
C1 = CS / "v413" / "candidatas_c1"
TRIN, TCONF = C1 / "R5_trinity" / "Trinity.lean", C1 / "R5_trinity" / "build" / "CONFERENCIA.json"
OPER, OCONF = C1 / "R2_operador" / "Operador.lean", C1 / "R2_operador" / "build" / "CONFERENCIA.json"
CONFE = C1 / "conferir_enunciados.py"
PARECER = AQUI / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
CUNH = CEN / "work" / "cunhagens_13out"
FALA = CUNH / "OPERADOR_20nov_o_preco_e_fixar_a_raiz_o_radical_fixa_o_sentido_o_teorema_final_e_o_parecer_do_codex_verbatim.txt"
FALA4 = CUNH / ("OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao"
                "_e_o_zero_absoluto_verbatim.txt")
COPIAS = CS / "v413" / "conferencia_c1_codex" / "k412c" / "src"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


tc = json.loads(TCONF.read_text(encoding="utf-8"))
assert tc["bom"] is True and tc["sha256"] == sha(TRIN) and not tc["fora_do_trio"] and tc["avisos"] == 0
oc = json.loads(OCONF.read_text(encoding="utf-8"))
assert oc["todos_bons"] is True and oc["modulos"][0]["sha256"] == sha(OPER)
NT, NO = tc["relatorios"], oc["modulos"][1]["relatorios"]

texto = """# Adendo de revisão ao Codex (v413): Trinity R5 e Operador R2, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Este adendo segue o parecer consolidado (`{parecer}`, sha16 `{sp}`), que cobriu a Trinity R3 e o Operador R1. Quem cola é o operador; a gerência não envia ordem ao Codex.

## O que revisar

1. **A candidata da gerência `TGLExt.Trinity`, R5**, em `{trin}` (sha16 `{st}`). A gerência a compilou na caixa da v412 e registrou o resultado em `{tconf}` (sha16 `{stc}`): {nt} de {nt} relatórios de axiomas no trio, nenhum aviso. Revise só o que o parecer não cobriu:
   - **a §13, vinda da R4** (fala do operador por bytes em `{fala4}`, sha16 `{sf4}`): `peso`, `solucoes`, `o_zero_absoluto_nao_se_alcanca`, `no_patamar_plano_a_carga_e_exata`, `oito_patamar_plano`, `as_oito_pedem_a_carga`, `o_preco_em_estados_e_a_exponencial_da_carga` e `a_terceira_lei_na_fronteira`. Confira a desigualdade estrita entre o peso e o número de soluções, e a equivalência exata no patamar plano para todo β < 1. A docstring deve dizer que a leitura da terceira lei de Nernst é do operador [ONTO] e que a moeda em que a máquina nua paga a carga segue aberta;
   - **os ajustes do item 9 do parecer**, aplicados só no texto: a ramificação desta implementação; `coupled`/`Trace` e as refutações por resolução; os retângulos, para a CNF de igualdade e a representação por retângulos separados nos dois blocos; os dois contadores como majorantes; a frase histórica R0/R1;
   - **a §12b:** `os_nomes_distintos_tocam`, `o_preco_da_fronteira_com_nomes_distintos` (o expoente do majorante conta só Nomes distintos) e `os_nomes_distintos_das_oito`;
   - **a §14, o teorema final do operador** (fala por bytes em `{fala}`, sha16 `{sf}`): `radical`, `o_radical_pesa_meia_nat`, `o_radical_e_positivo`, `o_radical_passa_de_um`, `a_carga_e_produto_referencial_do_radical`, `a_carga_se_manifesta_como_expoente`, `o_radical_fixa_o_sentido`, `o_radical_abaixo_de_um_inverte_o_sentido`, `o_expoente_conta_meias_nats`, `o_preco_e_fixar_a_raiz` e `o_teorema_final_do_radical`. São identidades de mudança de base da exponencial. Nenhuma docstring deve sugerir que fixar o radical muda o preço em estados (2^m segue exponencial no número de Nomes), nem dar cota de máquina;
   - **os enunciados anteriores:** o script da gerência `{confe}` (sha16 `{sce}`) tira comentários e compara cada declaração pelo nome. Ele relata, de R4 para R5, 0 removidas, 0 mudadas e 14 novas; de R3 para R4, 0, 0 e 8. Como controle, de R0 para R1 ele acusa a mudança de `a_trindade` que o parecer apontou. Confira por conta própria.
2. **O Operador R2**, em `{oper}` (sha16 `{so}`), compilado com {no} de {no} relatórios no trio (`{oconf}`, sha16 `{soc}`). Os ajustes do item 1 do parecer foram aplicados só no texto: a ausência de representação de todos os predicados não é parcialidade; o ponto fixo ½ existe sem dinâmica que o alcance; J conjuga as projeções, como operadores; a energia do par é preservada, e vale 1 na saída quando vale 1 na entrada. O script relata, de R1 para R2, 0 removidas, 0 mudadas e 0 novas.

## O que fica fora

Quem constrói não aprova: ficam fora os módulos do próprio Codex (a ponte TM2, a simulação e a leitura β). As pedras do Kimi e a errata de `OResumoEPsiBit` já têm veredito no parecer.

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\\t\\k412c\\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **A Trinity importa `APropostaDaTensao`**, a pedra do Kimi que você já compilou na revisão consolidada. Use o mesmo build, ou as cópias da gerência em `{copias}`.
- **Os axiomas:** leia os relatórios na saída inteira. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado novo contra a docstring e o nome. Procure alvo vácuo, hipótese não usada e docstring que diga mais do que o enunciado prova.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate. Consulte o Mapa de Rotas antes e registre depois, numa rota própria.

## O que devolver

- Para cada item, um veredito (APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA), com o motivo em até três linhas.
- Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada fonte lida e de cada log.
""".format(parecer=PARECER, sp=s16(PARECER), trin=TRIN, st=s16(TRIN), tconf=TCONF, stc=s16(TCONF), nt=NT,
           fala4=FALA4, sf4=s16(FALA4), fala=FALA, sf=s16(FALA), confe=CONFE, sce=s16(CONFE), oper=OPER, so=s16(OPER),
           no=NO, oconf=OCONF, soc=s16(OCONF), copias=COPIAS)
dest = AQUI / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R5_TRINITY_R2_OPERADOR_20nov.md"
dados = texto.encode("utf-8")
tmp = AQUI / (dest.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("adendo:", dest.name, "sha16", s16(dest), "|", len(dados), "B")
