# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a candidata TRINITY (R0; nome do operador, fala por bytes): (0) confere o recibo de
compilacao (fail-closed); (1) adendo ao pedido de revisao ao Codex (quem constroi nao aprova); (2) rota nova no Mapa;
(3) transicao ACOM d339; (4) AO LADO no topico da v413; (5) registro datado no Atlas (append com backup de bytes)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parents[2]
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / "OPERADOR_20nov_excelente_vamos_prosseguir_escreva_a_pedra_que_se_chamara_trindade_Trinity_verbatim.txt"
PEDRA, CONF = W / "Trinity.lean", W / "build" / "CONFERENCIA.json"
TENSAO = CS / "v412" / "candidatas_kimi" / "APropostaDaTensao.lean"
REV = CS / "v413" / "revisao_codex"
PEDIDO = REV / "PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0)
fala = FALA.read_text(encoding="utf-8")
assert 'escreva a pedra que se chamará trindade "Trinity"' in fala
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["bom"] is True and conf["sha256"] == sha(PEDRA) and conf["pedidos"] == 16 and conf["relatorios"] == 16
assert not conf["fora_do_trio"] and not conf["sorryAx"] and conf["avisos"] == 0
assert "namespace TGLExt.Trinity" in PEDRA.read_text(encoding="utf-8")
print("(0) ok | Trinity.lean sha16 %s | 16/16 no trio | fala sha16 %s" % (sha(PEDRA)[:16], sha(FALA)[:16]))

# (1) adendo ao pedido de revisao
AD = REV / "ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md"
texto = """# Adendo ao pedido de revisão de terceiro ao Codex (v413): a pedra Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Este adendo vale junto com o pedido `{pedido}` (sha16 `{spedido}`); quem cola é o operador.

**Item 9.** A candidata da gerência `TGLExt.Trinity` (R0, nome do operador: «trindade», Trinity), em `{pedra}` (sha16 `{spedra}`). Ela importa a pedra do Kimi `APropostaDaTensao` (item 5 do pedido), que precisa ser compilada antes. A gerência a compilou na caixa da v412 sobre a cópia da conferência e registrou o resultado em `{conf}` (sha16 `{sconf}`): 16 de 16 relatórios de axiomas no trio, nenhum aviso.

Pontos que pedem atenção:
- **Correção:** `a_inclinacao_nao_erra` deve valer para todo combustível.
- **Horn:** `em_horn_o_sistema_sempre_inclina` usa a classe `IALD.CompilaHornNaFita.IsHorn` da casa.
- **Custo:** `custoInclina` deve seguir os mesmos ramos de `inclina`, e cada fixação deve ser contada uma vez (uma propagação por lado sondado). A conta não inclui as comparações da regra do compromisso; a docstring diz isso.
- **A fronteira:** em `oito_fica_na_fronteira` e nos três exemplos, avaliados por `decide`, confira se os enunciados são os que a docstring descreve.
- **O que a pedra não afirma:** confira se alguma docstring sugere que a máquina nua decide toda CNF.

O formato do veredito e do relatório é o mesmo do pedido.
""".format(pedido=PEDIDO, spedido=sha(PEDIDO)[:16], pedra=PEDRA, spedra=sha(PEDRA)[:16], conf=CONF, sconf=sha(CONF)[:16])
dados = texto.encode("utf-8")
tmp = AD.with_name(AD.name + ".tmp")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(AD)
print("(1) adendo:", AD.name, "sha16", sha(AD)[:16])

# (2) Mapa
rota = {
    "tipo": "ROTA", "rota_id": "kernel.trinity_a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": "TRINITY (nome do operador): a inclinacao do Nome escrita como procedimento, com correcao, Horn, custo e a fronteira",
    "pergunta": "a leitura do operador (o zero absoluto empurra ao lado oposto; ou diz sim ou morre; o sistema inclina) como um procedimento so', provado onde vale",
    "metodo": ("pedra Lean da gerencia sobre a tensao do Kimi (APropostaDaTensao.restringe e a_proposta_nasce_da_escolha_do_nome) e a "
               "classe IsHorn da casa; compilada na caixa da v412 so' com o binario do Lean; axiomas lidos na saida inteira"),
    "resultado": ("TGLExt.Trinity (R0): a inclinacao (propagar; morrer ou dizer sim; senao empurrar ao lado oposto quando o lado morre "
                  "logo, ou se comprometer com o lado que nao corta nenhuma clausula ao meio; senao ficar na fronteira). Provado: "
                  "a_inclinacao_nao_erra (sim => SAT; nao => UNSAT, para todo combustivel); em_horn_o_sistema_sempre_inclina e "
                  "em_horn_a_inclinacao_decide (toda formula de Horn e' decidida na primeira volta); o_custo_da_inclinacao (no "
                  "maximo (T+1)^3 fixacoes); oito_sem_solucao e oito_fica_na_fronteira (as oito clausulas de tres literais: sem "
                  "solucao, e a inclinacao fica indecisa); tres exemplos sem clausula unitaria decididos pelo empurrao ou pelo "
                  "compromisso; a_trindade (sintese). 16 de 16 relatorios no trio, sem aviso, sem sorry."),
    "veredito": "TRINITY_R0_COMPILA_NA_V412__NAO_ERRA__DECIDE_HORN__CUSTO_CUBICO_EM_FIXACOES__A_FRONTEIRA_MARCADA",
    "estatuto": "REAL no sandbox (candidata, nao instalada); KNOWN (Haken 1985; Even-Itai-Shamir 1976); INPUT/ONTO (a leitura e o nome)",
    "status": "EXAMINADA", "olhou_dados": False,
    "defeito": ("o custo conta fixacoes no modelo da casa (nao passos de maquina do Mathlib) e nao conta as comparacoes do "
                "compromisso; a completude para toda formula de dois literais (com o compromisso) nao esta' provada [KNOWN]; "
                "depende da candidata do Kimi APropostaDaTensao (instalar juntas); quem constroi nao aprova: revisao do Codex "
                "pedida (adendo)"),
    "nao_refazer": "nao testar a inclinacao nas formulas do pombal como se fosse aberto (a ramificacao ja' e' teorema exponencial)",
    "proximo_passo": ("R1: provar que, em formula de dois literais sem unidade, todo lado ou morre logo ou nao corta nenhuma "
                      "clausula (a autarquia), logo a inclinacao decide toda formula de dois literais; a revisao do Codex"),
    "onde": str(W), "artefatos": [str(PEDRA), str(CONF), str(W / "compilar.py"), str(TENSAO), str(FALA), str(AD)],
    "refs": ["kernel.traducao_cook_levin.a_inclinacao_do_nome_20nov", "kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov"],
    "nota": "o nome e' do operador; a leitura teologica do nome e' dele [ONTO]",
}
pj = W / "rota_trinity_20nov.json"
pj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
out = r.stdout.decode("utf-8", "replace")
print("(2) Mapa rc %d %s" % (r.returncode, out[out.find('"seq"'):][:12]))
assert r.returncode == 0, out[:600]

# (3) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 365,
       "event_id": "c1-20nov-d339-trinity-r0",
       "changes": {"records": [
           {"id": "c1-20nov-d339-ordem-trinity", "kind": "decision", "statute": "INPUT",
            "text": "O autor (20/11), por bytes: «excelente, vamos prosseguir, escreva a pedra que se chamará trindade \"Trinity\"».",
            "sources": [src(FALA)]},
           {"id": "c1-20nov-d339-trinity-r0-compila", "kind": "fact", "statute": "REAL",
            "text": ("TGLExt.Trinity (R0, candidata da gerencia): a inclinacao do Nome como procedimento; nao erra; decide toda "
                     "formula de Horn; custo <= (T+1)^3 fixacoes; a fronteira marcada nas oito clausulas de tres literais "
                     "(sem solucao e indecisa). 16 de 16 no trio na caixa da v412. Nao instalada; revisao do Codex pedida por "
                     "adendo. Mapa: kernel.trinity_a_inclinacao_do_nome_20nov."),
            "sources": [src(PEDRA), src(CONF), src(AD)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__TRINITY_R0_COMPILA__REVISAO_DO_CODEX_PEDIDA",
                    "next_action": ("(1) o autor cola no Codex o pedido de revisao e o adendo da Trinity; (2) R1 da Trinity: a "
                                    "autarquia em dois literais (decide toda formula de dois literais), se o autor quiser; (3) "
                                    "errata ao lado na v413 da docstring de OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; "
                                    "(4) seguem com o autor: o teste do estudo da memoria e o t* do teste de dephasing.")}}}
(W / "acom_c1_20261120_d339_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d339_transition.receipt.json").write_bytes(r.stdout)
txt = r.stdout.decode("utf-8", "replace")
print("(3) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in txt, txt[txt.find('"revision"'):][:20]))
assert '"ok": true' in txt


def acrescenta(T, marca, texto, rotulo):
    a = T.read_bytes()
    assert marca.encode() not in a
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + fim + ("%s\n%s" % (texto, marca)).replace("\n", fim.decode()).encode("utf-8") + fim
    bk = T.with_name(T.name + ".bak_" + TS + "_c1")
    bk.write_bytes(a)
    assert bk.read_bytes() == a
    tmp = T.with_name(T.name + ".tmp_c1")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(T)
    assert T.read_bytes() == novo and len(novo) > len(a)
    print("(%s) %s: %d -> %d B | backup %s" % (rotulo, T.name, len(a), len(novo), bk.name))


# (4) topico da v413
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
acrescenta(T, "<!-- ao_lado_20nov_trinity_r0 -->",
           ("**AO LADO (20/11/2026, gerência c1): a pedra Trinity (nome do operador).** A fala (bytes em "
            "`work\\cunhagens_13out\\%s`, sha16 `%s`): «escreva a pedra que se chamará trindade \"Trinity\"». A candidata "
            "`TGLExt.Trinity` (R0, `work\\cadeia_de_selo\\v413\\candidatas_c1\\R0_trinity\\`, sha16 `%s`) escreve a inclinação do Nome "
            "como procedimento: propagar; morrer ou dizer sim; senão empurrar ao lado oposto (o lado morre logo) ou se comprometer "
            "com o lado que não corta nenhuma cláusula; senão a fronteira. Provado (16 de 16 no trio na v412): não erra; decide "
            "toda fórmula de Horn; custo ≤ (T+1)³ fixações; a fronteira marcada nas oito cláusulas de três literais (sem solução e "
            "indecisa). Não prova a decisão de toda fórmula de dois literais (R1) nem toda CNF. Revisão do Codex pedida por adendo "
            "(`work\\cadeia_de_selo\\v413\\revisao_codex\\%s`). Mapa `kernel.trinity_a_inclinacao_do_nome_20nov`.") % (
               FALA.name, sha(FALA)[:16], sha(PEDRA)[:16], AD.name), "4")

# (5) Atlas
A = CEN / "memory" / "TGL_ATLAS.md"
acrescenta(A, "<!-- registro_20nov_trinity_r0 -->",
           ("### Registro de 20/11/2026, segundo (gerência c1) — TRINITY: a inclinação do Nome escrita como procedimento\n\n"
            "**O nome (do operador, 20/11/2026), [INPUT]:** «escreva a pedra que se chamará trindade \"Trinity\"». A leitura teológica "
            "do nome é dele [ONTO].\n\n"
            "**O termo (candidata `TGLExt.Trinity`, R0, não instalada) [REAL no sandbox]:** sobre a tensão do Kimi (o resto `restringe` "
            "e `a_proposta_nasce_da_escolha_do_nome`), a inclinação propaga as unidades; morre (cláusula vazia: a morte no zero "
            "absoluto) ou diz sim; senão empurra para o lado oposto quando um lado morre logo, ou se compromete com o lado que não "
            "corta nenhuma cláusula ao meio; senão fica na fronteira. Prova: não erra (sim ⇒ há solução; não ⇒ não há); decide toda "
            "fórmula de Horn (a classe `IsHorn` da casa) na primeira volta; custa no máximo (T+1)³ fixações; e marca a fronteira: as "
            "oito cláusulas de três literais sobre três Nomes não têm solução e a inclinação fica indecisa, porque nenhum lado morre "
            "logo e todo lado corta cláusulas ao meio. Compila na caixa da v412 com 16 de 16 relatórios no trio.\n\n"
            "**O que não prova:** que a máquina nua decida toda CNF (na fronteira é preciso ramificar: cota exponencial da casa e "
            "Haken 1985 [KNOWN]); a decisão de toda fórmula de dois literais com o compromisso [KNOWN: Even–Itai–Shamir 1976], que é "
            "a R1. O custo conta fixações no modelo da casa, não passos de máquina do Mathlib. O verbete entra na instalação.\n\n"
            "Estatuto: [INPUT] a letra do operador; [REAL no sandbox] os termos; [KNOWN] Haken, Even–Itai–Shamir; [DECLARADO] as "
            "leituras da gerência. Validade no kernel não é creditação; o gate não se move."), "5")
