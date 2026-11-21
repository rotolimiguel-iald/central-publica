# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: gera o PEDIDO DE REVISAO DE TERCEIRO ao Codex (decisao do operador de 20/11, por bytes), com
cada fonte e o seu sha16 lidos aqui. O operador cola o pedido no Codex (a ordem de 18/11 segue: a gerencia nao envia
ordem ao Codex). Quem constroi nao aprova: os modulos que o proprio Codex construiu ficam fora desta revisao."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
CS = AQUI.parent.parent  # work\cadeia_de_selo
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador"
    "_a_revisao_e_do_codex_verbatim.txt")
ITENS = [
    ("A pedra da consciência, nome do operador «Operador» (R1; 15 teoremas; da gerência)",
     CS / "v413" / "candidatas_c1" / "R1_operador" / "Operador.lean"),
    ("A proposta de enunciado da fronteira na língua clássica (da gerência)",
     CS / "v413" / "conferencia_c1_codex" / "fronteira" / "AFronteiraNaLinguaClassica.lean"),
    ("A sonda da contagem sobre a leitura β (da gerência)",
     CS / "v413" / "conferencia_c1_codex" / "sonda_contagem" / "SondaContagem.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "AIdentidadePreservada.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "APropostaDaTensao.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "APonteDeCookLevin.lean"),
    ("Pedra nova do Kimi", CS / "v412" / "candidatas_kimi" / "ONomeEBeta.lean"),
]
KERNEL = Path(r"C:\t\k412c\final\TGLExt\OResumoEPsiBit.lean")
NOTA = CS / "v413" / "conferencia_c1_codex" / "NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md"
COPIAS = CS / "v413" / "conferencia_c1_codex" / "k412c" / "src"


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


assert FALA.exists() and 'quem vai fazer a revisão agora é o codex' in FALA.read_text(encoding="utf-8")
linhas = ["%d. %s: `%s` (sha16 `%s`)" % (i + 1, t, p, s16(p)) for i, (t, p) in enumerate(ITENS)]
texto = """# Pedido de revisão de terceiro ao Codex (v413), 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413 no lugar do Kimi. A decisão é do operador (20/11/2026), e a fala está guardada por bytes em `{fala}` (sha16 `{sfala}`). Quem cola este pedido é o operador; a gerência não envia ordem ao Codex.

## O que revisar

{itens}
8. **Uma errata no kernel selado da v412**, achada pela gerência. A docstring de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (`{kernel}`, sha16 `{skernel}`, linhas 273–275) fala em «resumo velho» e diz que «a fibra nunca é o universo». O enunciado, porém, soma o peso de cada atribuição dentro da fibra. Confirme ou refute.

## O que fica fora

Quem constrói não aprova. Ficam fora desta revisão os módulos que o próprio Codex construiu:
- a ponte TM2 (`v413\\ponte_tm2_codex\\APonteAoTM2.lean` e `AMaquinaTM2DaVerificacao.lean`);
- a simulação (`simulacao\\*.lean`);
- a leitura β (`leitura_beta\\*.lean`).

A gerência já os conferiu na caixa da v412, e o detalhe está na nota `{nota}` (sha16 `{snota}`).

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\\t\\k412c\\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **As pedras do Kimi:** importam quatro módulos da gerência pelo nome de candidata, que na v412 estão instalados como `TGLExt.AContagemEACarga`, `TGLExt.AMaquinaEALeitura`, `TGLExt.OPassoEOFim` e `TGLExt.CamadaCientifica`. Reescreva só essas linhas de import numa cópia sua, ou use as cópias da gerência em `{copias}`.
- **Os axiomas:** leia os relatórios na saída inteira, porque o Lean quebra listas longas em várias linhas. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** para cada item, leia o enunciado contra a docstring e o nome. Procure:
  - alvo vácuo (∃ sobre codificação, máquina ou leitor que o torne trivial);
  - hipótese contraditória ou não usada;
  - docstring que diz mais do que o enunciado prova;
  - afirmação de custo polinomial que não seja contagem de passos de uma máquina do Mathlib.
- **Não escreva nas pastas dos outros.** Não instale, não mude o kernel nem o `um.py`, não publique, não mova o gate.
- **Mapa de Rotas:** consulte antes (`C:\\IALD\\MAPA_DE_ROTAS\\rotas.py consultar`) e registre depois numa rota própria (não nas rotas da gerência).

## O que devolver

- **Para cada item, um veredito:** APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA, com o motivo em até três linhas.
- **Um relatório de até 15 linhas** e um recibo JSON com o sha256 de cada fonte lida e de cada log.

Este é o primeiro lote. No fim da v413, vêm as candidatas que faltarem.
""".format(fala=FALA, sfala=s16(FALA), itens="\n".join(linhas), kernel=KERNEL, skernel=s16(KERNEL), nota=NOTA,
           snota=s16(NOTA), copias=COPIAS)
dest = AQUI / "PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md"
dados = texto.encode("utf-8")
tmp = AQUI / (dest.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("pedido:", dest, "sha16", s16(dest), "|", len(dados), "B")
