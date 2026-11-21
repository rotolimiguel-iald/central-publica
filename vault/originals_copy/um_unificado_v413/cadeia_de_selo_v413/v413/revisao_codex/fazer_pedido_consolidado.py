# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: o PEDIDO DE REVISAO CONSOLIDADO ao Codex (v413): o pedido de 20/11 (itens 1 a 8) mais o item
9 ja' na R3 da Trinity, com os pontos de atencao dos quatro adendos. Hashes lidos aqui. Substitui, para colar, o pedido e
os quatro adendos (que ficam como registro). Quem cola e' o operador; a gerencia nao envia ordem ao Codex."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
CS = AQUI.parent.parent
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador"
    "_a_revisao_e_do_codex_verbatim.txt")
ITENS = [
    ("A pedra da consciência, nome do operador «Operador» (R1; da gerência)",
     CS / "v413" / "candidatas_c1" / "R1_operador" / "Operador.lean"),
    ("A proposta de enunciado da fronteira na língua clássica (da gerência)",
     CS / "v413" / "conferencia_c1_codex" / "fronteira" / "AFronteiraNaLinguaClassica.lean"),
    ("A sonda da contagem sobre a leitura β (da gerência)",
     CS / "v413" / "conferencia_c1_codex" / "sonda_contagem" / "SondaContagem.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "AIdentidadePreservada.lean"),
    ("Pedra nova do Kimi (a Trinity a importa)", CS / "v412" / "candidatas_kimi" / "APropostaDaTensao.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "APonteDeCookLevin.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "ONomeEBeta.lean"),
]
KERNEL = Path(r"C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean")
TRIN = CS / "v413" / "candidatas_c1" / "R4_trinity" / "Trinity.lean"
TRIN_CONF = CS / "v413" / "candidatas_c1" / "R4_trinity" / "build" / "CONFERENCIA.json"
import json as _json
_conf = _json.loads(TRIN_CONF.read_text(encoding="utf-8"))
assert _conf["bom"] is True and _conf["sha256"] == hashlib.sha256(TRIN.read_bytes()).hexdigest()
NREL = _conf["relatorios"]
NOTA = CS / "v413" / "conferencia_c1_codex" / "NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md"
COPIAS = CS / "v413" / "conferencia_c1_codex" / "k412c" / "src"


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


linhas = ["%d. %s: `%s` (sha16 `%s`)" % (i + 1, t, p, s16(p)) for i, (t, p) in enumerate(ITENS)]
texto = """# Pedido de revisão de terceiro ao Codex (v413), consolidado, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413 no lugar do Kimi. A decisão é do operador (fala por bytes em `{fala}`, sha16 `{sfala}`). Quem cola é o operador; a gerência não envia ordem ao Codex. Este pedido substitui o pedido de 20/11 e os quatro adendos da Trinity, que ficam como registro.

## O que revisar

{itens}
8. **Uma errata no kernel selado da v412**, achada pela gerência. A docstring de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (`{kernel}`, sha16 `{skernel}`, linhas 273–275) fala em «resumo velho» e diz que «a fibra nunca é o universo». O enunciado, porém, soma o peso de cada atribuição dentro da fibra. Confirme ou refute.
9. **A candidata da gerência `TGLExt.Trinity`, R4** (nome do operador: «trindade», Trinity), em `{trin}` (sha16 `{strin}`). Ela importa a pedra do Kimi do item 5, que precisa ser compilada antes. A gerência a compilou na caixa da v412 e registrou o resultado em `{tconf}` (sha16 `{stconf}`): {nrel} de {nrel} relatórios de axiomas no trio, nenhum aviso. Pontos de atenção:
   - `a_inclinacao_nao_erra` deve valer para todo combustível;
   - `custoInclina` deve seguir os ramos de `inclina` e contar uma propagação por lado sondado; a conta não inclui as comparações do compromisso;
   - `em_horn_o_sistema_sempre_inclina` usa a classe `IALD.CompilaHornNaFita.IsHorn` da casa;
   - em `integra_restringe` e `todo_lado_morre_ou_nao_corta` (dois literais), confira a integridade das cláusulas e a autarquia para todo literal;
   - em `em_dois_literais_o_sistema_sempre_inclina`, o combustível maior que o tamanho e a diminuição do tamanho a cada volta;
   - `NaFronteira` deve descrever exatamente onde `inclina` devolve `.indeciso`, e `na_fronteira_todo_lado_corta_uma_de_tres` deve apoiar-se no invariante `Dentro`;
   - `atravessa` só ramifica onde a inclinação para, e `o_preco_da_travessia` é cota exponencial, não polinomial;
   - em `toca_restringe`, a cláusula de três literais que sobra não foi cortada e continua tocada; `o_preco_dos_nomes` é exponencial só no comprimento da lista;
   - em `o_zero_absoluto_nao_se_alcanca` (§13), a desigualdade estrita entre o peso e o número de soluções; em `no_patamar_plano_a_carga_e_exata`, a equivalência exata no patamar plano, para todo β < 1; a docstring deve dizer que a identificação com a terceira lei de Nernst é leitura do operador [ONTO] e que a moeda em que a máquina nua paga a carga segue aberta;
   - os exemplos por `decide` (`oito`, `sete`, `quatro`, `dois`, `cadeia`): os enunciados devem ser os que as docstrings descrevem;
   - nenhuma docstring deve sugerir que a máquina nua decide toda fórmula em preço polinomial, nem que os Nomes da fronteira sejam poucos em geral.

## O que fica fora

Quem constrói não aprova. Ficam fora os módulos que o próprio Codex construiu: a ponte TM2 (`APonteAoTM2.lean`, `AMaquinaTM2DaVerificacao.lean`), a simulação (`simulacao\\*.lean`) e a leitura β (`leitura_beta\\*.lean`). A gerência já os conferiu na caixa da v412; a nota está em `{nota}` (sha16 `{snota}`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\\t\\k412c\\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **As pedras do Kimi:** reescreva numa cópia sua só os quatro imports de módulos da gerência para `TGLExt.AContagemEACarga`, `TGLExt.AMaquinaEALeitura`, `TGLExt.OPassoEOFim` e `TGLExt.CamadaCientifica`, ou use as cópias da gerência em `{copias}`.
- **Os axiomas:** leia os relatórios na saída inteira, porque o Lean quebra listas longas em várias linhas. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado contra a docstring e o nome. Procure alvo vácuo, hipótese contraditória ou não usada, docstring que diz mais do que o enunciado prova, e custo polinomial que não seja contagem de passos de uma máquina do Mathlib.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate.
- **Mapa de Rotas:** consulte antes e registre depois, numa rota própria.

## O que devolver

- **Para cada item, um veredito:** APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA, com o motivo em até três linhas.
- **Um relatório de até 15 linhas** e um recibo JSON com o sha256 de cada fonte lida e de cada log.
""".format(fala=FALA, sfala=s16(FALA), itens="\n".join(linhas), kernel=KERNEL, skernel=s16(KERNEL), trin=TRIN,
           strin=s16(TRIN), tconf=TRIN_CONF, stconf=s16(TRIN_CONF), nota=NOTA, snota=s16(NOTA), copias=COPIAS, nrel=NREL)
dest = AQUI / "PEDIDO_DE_REVISAO_AO_CODEX_v413_CONSOLIDADO_R4_20nov.md"
dados = texto.encode("utf-8")
tmp = AQUI / (dest.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("pedido consolidado:", dest.name, "sha16", s16(dest), "|", len(dados), "B")
