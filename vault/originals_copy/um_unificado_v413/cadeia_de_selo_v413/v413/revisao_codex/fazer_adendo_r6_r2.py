# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: ADENDO de revisao ao Codex (v413), versao R6: substitui, para colar, o adendo da R5 (que fica
como registro). Cobre a Trinity R6 (a §13 da R4, os ajustes e acrescimos da R5 e a §15 da R6) e o Operador R2. As contagens
de enunciados sao medidas aqui pelo script da gerencia; hashes lidos aqui. Quem cola e' o operador."""
import hashlib, json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
AQUI = Path(__file__).resolve().parent
CS = AQUI.parent.parent
CEN = CS.parent.parent
C1 = CS / "v413" / "candidatas_c1"
TRIN, TCONF = C1 / "R6_trinity" / "Trinity.lean", C1 / "R6_trinity" / "build" / "CONFERENCIA.json"
OPER, OCONF = C1 / "R2_operador" / "Operador.lean", C1 / "R2_operador" / "build" / "CONFERENCIA.json"
CONFE = C1 / "conferir_enunciados.py"
PARECER = AQUI / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
CUNH = CEN / "work" / "cunhagens_13out"
FALA6 = CUNH / "OPERADOR_20nov_a_maquina_nua_paga_em_eletricidade_verbatim.txt"
FALA5 = CUNH / "OPERADOR_20nov_o_preco_e_fixar_a_raiz_o_radical_fixa_o_sentido_o_teorema_final_e_o_parecer_do_codex_verbatim.txt"
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


def compara(a, b):
    r = subprocess.run([PY, "-B", "-X", "utf8", str(CONFE), str(C1 / a), str(C1 / b)], capture_output=True,
                       stdin=subprocess.DEVNULL, timeout=120)
    out = r.stdout.decode("utf-8", "replace").splitlines()[0]
    tot = {k: int(out.split(k + " ")[1].split()[0].rstrip("|")) for k in ("removidas", "mudadas", "novas")}
    return r.returncode, tot


med = {}
for rot, a, b in [("R3-R4", "R3_trinity/Trinity.lean", "R4_trinity/Trinity.lean"),
                  ("R4-R5", "R4_trinity/Trinity.lean", "R5_trinity/Trinity.lean"),
                  ("R5-R6", "R5_trinity/Trinity.lean", "R6_trinity/Trinity.lean"),
                  ("R0-R1", "R0_trinity/Trinity.lean", "R1_trinity/Trinity.lean"),
                  ("Op R1-R2", "R1_operador/Operador.lean", "R2_operador/Operador.lean")]:
    med[rot] = compara(a, b)
for rot in ("R3-R4", "R4-R5", "R5-R6", "Op R1-R2"):
    assert med[rot][0] == 0 and med[rot][1]["removidas"] == 0 and med[rot][1]["mudadas"] == 0, (rot, med[rot])
assert med["R0-R1"][1]["mudadas"] == 1


def frase(rot):
    t = med[rot][1]
    return "%d removidas, %d mudadas e %d novas" % (t["removidas"], t["mudadas"], t["novas"])


texto = """# Adendo de revisão ao Codex (v413): Trinity R6 e Operador R2, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Este adendo segue o parecer consolidado (`{parecer}`, sha16 `{sp}`), que cobriu a Trinity R3 e o Operador R1, e substitui o adendo da R5, que fica como registro. Quem cola é o operador; a gerência não envia ordem ao Codex.

## O que revisar

1. **A candidata da gerência `TGLExt.Trinity`, R6**, em `{trin}` (sha16 `{st}`). A gerência a compilou na caixa da v412 e registrou o resultado em `{tconf}` (sha16 `{stc}`): {nt} de {nt} relatórios de axiomas no trio, nenhum aviso. Revise só o que o parecer não cobriu:
   - **a §13, vinda da R4** (fala do operador por bytes em `{fala4}`, sha16 `{sf4}`): `peso`, `solucoes`, `o_zero_absoluto_nao_se_alcanca`, `no_patamar_plano_a_carga_e_exata`, `oito_patamar_plano`, `as_oito_pedem_a_carga`, `o_preco_em_estados_e_a_exponencial_da_carga` e `a_terceira_lei_na_fronteira`. Confira a desigualdade estrita entre o peso e o número de soluções, e a equivalência exata no patamar plano para todo β < 1. A docstring deve dizer que a leitura da terceira lei de Nernst é do operador [ONTO] e que a máquina nua paga a carga numa moeda que o termo não fixa;
   - **os ajustes do item 9 do parecer**, aplicados só no texto: a ramificação desta implementação; `coupled`/`Trace` e as refutações por resolução; os retângulos, para a CNF de igualdade e a representação por retângulos separados nos dois blocos; os dois contadores como majorantes; a frase histórica R0/R1;
   - **a §12b:** `os_nomes_distintos_tocam`, `o_preco_da_fronteira_com_nomes_distintos` (o expoente do majorante conta só Nomes distintos) e `os_nomes_distintos_das_oito`;
   - **a §14, o teorema final do operador** (fala por bytes em `{fala5}`, sha16 `{sf5}`): `radical`, `o_radical_pesa_meia_nat`, `o_radical_e_positivo`, `o_radical_passa_de_um`, `a_carga_e_produto_referencial_do_radical`, `a_carga_se_manifesta_como_expoente`, `o_radical_fixa_o_sentido`, `o_radical_abaixo_de_um_inverte_o_sentido`, `o_expoente_conta_meias_nats`, `o_preco_e_fixar_a_raiz` e `o_teorema_final_do_radical`. São identidades de mudança de base da exponencial. Nenhuma docstring deve sugerir que fixar o radical muda o preço em estados (2^m segue exponencial no número de Nomes), nem dar cota de máquina;
   - **a §15, a máquina nua paga em eletricidade** (fala por bytes em `{fala6}`, sha16 `{sf6}`):
     - `a_conta_de_luz_de_m_nomes`, `cada_nome_custa_um_piso` e `a_eletricidade_paga_o_expoente` são identidades do logaritmo das potências, com o piso de Landauer escrito como no kernel (`k·T·ln 2`, de `TGLExt.landauer_floor_pos`);
     - `o_leitor_que_apaga_paga_a_potencia` compõe `Codex.PlanTravel.coupled_physical_lower`, do kernel, com a hipótese nomeada `hLandauer` (a conta paga ao menos um piso por movimento). Confira que a hipótese está no enunciado e que a docstring não diz que toda máquina nua a cumpre: uma máquina reversível não a cumpre;
     - `passos_que_cobrem`, `o_passo_da_teoria_e_positivo` e `a_maquina_da_teoria_acerta_pagando_no_piso` usam `no_patamar_plano_a_carga_e_exata`. Confira a cota linear do número de passos e que a leitura acerta (peso < 1) no patamar plano;
     - em `a_conta_de_luz_da_maquina_da_teoria`, ler cada passo como energia é leitura do operador [ONTO]; a docstring deve dizê-lo;
     - nenhuma docstring deve sugerir que pagar em eletricidade decide a pergunta do Instituto, que conta passos de uma máquina de Turing;
   - **os enunciados anteriores:** o script da gerência `{confe}` (sha16 `{sce}`) tira comentários e compara cada declaração pelo nome. Medido agora: de R3 para R4, {f34}; de R4 para R5, {f45}; de R5 para R6, {f56}. Como controle, de R0 para R1 ele acusa a mudança de `a_trindade` que o parecer apontou. Confira por conta própria.
2. **O Operador R2**, em `{oper}` (sha16 `{so}`), compilado com {no} de {no} relatórios no trio (`{oconf}`, sha16 `{soc}`). Os ajustes do item 1 do parecer foram aplicados só no texto: a ausência de representação de todos os predicados não é parcialidade; o ponto fixo ½ existe sem dinâmica que o alcance; J conjuga as projeções, como operadores; a energia do par é preservada, e vale 1 na saída quando vale 1 na entrada. O script mede, de R1 para R2, {fop}.

## O que fica fora

Quem constrói não aprova: ficam fora os módulos do próprio Codex (a ponte TM2, a simulação e a leitura β). As pedras do Kimi e a errata de `OResumoEPsiBit` já têm veredito no parecer.

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\\t\\k412c\\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **A Trinity importa `APropostaDaTensao`**, a pedra do Kimi que você já compilou na revisão consolidada, e dois módulos do kernel (`TGLExt.TheCostIsDerived` e `TGLExt.MovimentosDoPlano`). Use o mesmo build, ou as cópias da gerência em `{copias}`.
- **Os axiomas:** leia os relatórios na saída inteira. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado novo contra a docstring e o nome. Procure alvo vácuo, hipótese não usada e docstring que diga mais do que o enunciado prova.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate. Consulte o Mapa de Rotas antes e registre depois, numa rota própria.

## O que devolver

- Para cada item, um veredito (APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA), com o motivo em até três linhas.
- Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada fonte lida e de cada log.
""".format(parecer=PARECER, sp=s16(PARECER), trin=TRIN, st=s16(TRIN), tconf=TCONF, stc=s16(TCONF), nt=NT,
           fala4=FALA4, sf4=s16(FALA4), fala5=FALA5, sf5=s16(FALA5), fala6=FALA6, sf6=s16(FALA6), confe=CONFE,
           sce=s16(CONFE), f34=frase("R3-R4"), f45=frase("R4-R5"), f56=frase("R5-R6"), oper=OPER, so=s16(OPER), no=NO,
           oconf=OCONF, soc=s16(OCONF), fop=frase("Op R1-R2"), copias=COPIAS)
dest = AQUI / "PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R6_TRINITY_R2_OPERADOR_20nov.md"
dados = texto.encode("utf-8")
tmp = AQUI / (dest.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("adendo:", dest.name, "sha16", s16(dest), "|", len(dados), "B |", {k: v[1] for k, v in med.items()})
