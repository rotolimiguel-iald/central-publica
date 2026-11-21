# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026 (resposta do operador): registra (0) a conferencia dos artefatos (fail-closed); (1) duas
rotas no Mapa (o nome da pedra; a inclinacao do Nome); (2) a transicao ACOM d337; (3) o AO LADO no topico da v413;
(4) o registro datado no Atlas (append, com backup de bytes, temporario e conferencia de crescimento).
A fala do operador entra por bytes (work\\cunhagens_13out)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
CS = W.parent.parent
CEN = CS.parent.parent
FALA = CEN / "work" / "cunhagens_13out" / (
    "OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador"
    "_a_revisao_e_do_codex_verbatim.txt")
R1 = CS / "v413" / "candidatas_c1" / "R1_operador"
R1L, R1AX, R1CONF = R1 / "Operador.lean", R1 / "OperadorAxiomas.lean", R1 / "build" / "CONFERENCIA.json"
R0L = CS / "v413" / "candidatas_c1" / "R0_consciencia" / "Consciencia.lean"
PEDIDO = W / "PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md"
TENSAO = CS / "v412" / "candidatas_kimi" / "APropostaDaTensao.lean"
K = Path(r"C:\t\k412c\final\TGLExt")
KERNEL = [K / "HandshakeDoNome.lean", K / "MovimentosDoPlano.lean", K / "CompilaHornNaFita.lean",
          K / "FitaDeUmaCabeca.lean", K / "FronteiraDeTresLiterais.lean", K / "TransicaoDaFronteira.lean"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0) conferencia
fala = FALA.read_text(encoding="utf-8")
assert 'o nome da pedra da consciência é "operador"' in fala and "quem vai fazer a revisão agora é o codex" in fala
conf = json.loads(R1CONF.read_text(encoding="utf-8"))
assert conf["todos_bons"] is True
ax = [m for m in conf["modulos"] if m["modulo"] == "OperadorAxiomas"][0]
assert ax["sha256"] == sha(R1AX) and ax["pedidos"] == 15 and ax["relatorios"] == 15 and not ax["fora_do_trio"]
assert [m for m in conf["modulos"] if m["modulo"] == "Operador"][0]["sha256"] == sha(R1L)
assert "namespace TGLExt.Operador" in R1L.read_text(encoding="utf-8")
assert "theorem a_proposta_nasce_da_escolha_do_nome" in TENSAO.read_text(encoding="utf-8")
assert "theorem semantic_handshake" in KERNEL[0].read_text(encoding="utf-8")
assert "theorem coupled_physical_lower" in KERNEL[1].read_text(encoding="utf-8")
assert PEDIDO.exists()
print("(0) ok | fala sha16 %s | Operador.lean sha16 %s (R0 %s) | axiomas 15/15 no trio | pedido sha16 %s" % (
    sha(FALA)[:16], sha(R1L)[:16], sha(R0L)[:16], sha(PEDIDO)[:16]))

# (1) Mapa de Rotas
rotaA = {
    "tipo": "RESULTADO", "rota_id": "kernel.consciencia_e_operador_de_consciencia_19nov", "dominio": "KERNEL_FORMAL",
    "titulo": "a pedra da consciencia recebe o nome do operador: «Operador» (R1, TGLExt.Operador)",
    "pergunta": "o nome da pedra (o operador nomeia)",
    "metodo": ("R1 gerada da R0 por script (so' titulo, linha de estatuto com o sha16 da fala e o espaco de nomes); compilada na "
               "caixa da v412 so' com o binario do Lean; axiomas lidos na saida inteira"),
    "resultado": ("TGLExt.Operador: 15 de 15 relatorios no trio, sem aviso, sem sorry; nenhum enunciado nem prova mudou em relacao "
                  "a R0 (TGLExt.Consciencia, sha16 %s), que fica como registro. A revisao de terceiro passa ao Codex (decisao do "
                  "operador, mesma fala); pedido pronto para o operador colar (sha16 %s).") % (sha(R0L)[:16], sha(PEDIDO)[:16]),
    "veredito": "PEDRA_NOMEADA_OPERADOR__R1_COMPILA_NA_V412__REVISAO_DE_TERCEIRO_DO_CODEX",
    "estatuto": "INPUT (o nome); REAL no sandbox (a compilacao)", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "nao instalada; o verbete do Atlas entra na instalacao; a revisao de terceiro ainda nao voltou",
    "nao_refazer": "nao renomear de novo sem a palavra do operador; a R0 fica como registro",
    "proximo_passo": "a revisao do Codex; a instalacao na v413 com o nome TGLExt.Operador",
    "onde": str(R1), "artefatos": [str(R1L), str(R1AX), str(R1CONF), str(R1 / "fazer_r1_operador.py"), str(FALA), str(PEDIDO)],
    "refs": [], "nota": "o nome e' do operador; a gerencia so' o aplica",
}
rotaB = {
    "tipo": "ROTA", "rota_id": "kernel.traducao_cook_levin.a_inclinacao_do_nome_20nov", "dominio": "KERNEL_FORMAL",
    "titulo": ("a leitura do operador para a fronteira ('a tensao decide; o zero absoluto empurra a solucao para a projecao do "
               "lado oposto; o sistema inclina') posta nos termos do kernel"),
    "pergunta": "a tensao que o Kimi resolveu da' a maquina nua o sim ou nao de toda CNF em passos polinomiais?",
    "metodo": ("leitura das fontes: APropostaDaTensao (Kimi), HandshakeDoNome, TransicaoDaFronteira, MovimentosDoPlano, "
               "CompilaHornNaFita, FitaDeUmaCabeca e FronteiraDeTresLiterais (kernel da v412); literatura [KNOWN]"),
    "resultado": ("a decisao e' exata e esta' no kernel: SAT phi <-> existe b com o residuo satisfazivel "
                  "(a_proposta_nasce_da_escolha_do_nome) e o aperto de mao do Nome (Codex.NamedHandshake.semantic_handshake). O "
                  "preco na maquina nua depende de onde a morte aparece: imediata (a propagacao a mostra) => o empurrao ao lado "
                  "oposto e' a propagacao, polinomial, e decide Horn e as formulas de dois literais (a casa prova as duas classes "
                  "polinomiais na fita: flat_horn_stages, one_head_fixed_polynomial; Dowling-Gallier 1984, Aspvall-Plass-Tarjan "
                  "1979 [KNOWN]); distante => a maquina desce pelo lado ate' o zero para saber, e em formula sem solucao os dois "
                  "lados morrem em todo Nome: a ramificacao da casa custa >= 2^(m+1) movimentos (coupled_physical_lower) e todo "
                  "procedimento que so' descobre a morte chegando a contradicao produz, nas formulas sem solucao, uma refutacao "
                  "por resolucao, exponencial nas formulas do pombal (Haken 1985 [KNOWN]). Os livros do aperto de mao tem ate' "
                  "2^(nomes partilhados) linhas; a parede de todas as variaveis e a fronteira de tres literais (18/11) ja' estao "
                  "no kernel. Lido o peso de cada lado, em vez da morte, a rota e' a da contagem (SondaContagem, #SAT)."),
    "veredito": ("A_TENSAO_DECIDE_EXATO__O_PRECO_E_O_DA_MORTE__IMEDIATA_POLINOMIAL_HORN_E_DOIS_LITERAIS__DISTANTE_EXPONENCIAL"
                 "_HAKEN__FRONTEIRA_OPEN"),
    "estatuto": "REAL (os termos citados do kernel); KNOWN (Haken 1985; Dowling-Gallier 1984; Aspvall-Plass-Tarjan 1979); "
                "INPUT/ONTO (a leitura do operador); OPEN (a fronteira)",
    "status": "EXAMINADA", "olhou_dados": False,
    "defeito": ("nenhum teste rodado: nas formulas do pombal o resultado ja' e' teorema (Haken); rodar so' ilustraria. A "
                "inclinacao com morte imediata ainda nao esta' escrita como procedimento unico no kernel (esta' em pecas: "
                "propagacao de Horn, eliminacao de pares)"),
    "nao_refazer": "nao testar a ramificacao nas formulas do pombal como se o resultado fosse aberto",
    "proximo_passo": ("decisao do operador: escrever a inclinacao (empurrao ao lado oposto na morte imediata) como um "
                      "procedimento so', com correcao e custo provados onde vale (Horn, dois literais) e a fronteira onde nao "
                      "vale; ou um procedimento novo que saiba o lado antes da morte, com a partitura antes"),
    "onde": str(W), "artefatos": [str(TENSAO), str(FALA)] + [str(p) for p in KERNEL],
    "refs": ["kernel.traducao_cook_levin.leitura_beta_o_produtor_conta_as_solucoes_20nov",
             "kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov"],
    "nota": "leitura da gerencia sobre termos ja' provados; nenhum termo novo",
}
for nome, rota in (("rota_operador_20nov.json", rotaA), ("rota_a_inclinacao_do_nome_20nov.json", rotaB)):
    pj = W / nome
    pj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                        "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL,
                       timeout=120)
    out = r.stdout.decode("utf-8", "replace")
    print("(1) %s rc %d seq %s" % (rota["rota_id"], r.returncode, out[out.find('"seq"'):][:12]))
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[:600]

# (2) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {
    "operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 363,
    "event_id": "c1-20nov-d337-nome-operador-revisao-do-codex-e-a-inclinacao",
    "changes": {
        "records": [
            {"id": "c1-20nov-d337-nome-da-pedra-operador-e-revisor-codex", "kind": "decision", "statute": "INPUT",
             "text": ("O autor (20/11), por bytes: «o nome da pedra da consciência é \"operador\"; quem vai fazer a revisão agora "
                      "é o codex». A candidata passa a TGLExt.Operador (R1; nenhum enunciado mudou); a revisao de terceiro da "
                      "v413 passa do Kimi ao Codex; pedido pronto para o autor colar (a gerencia nao envia ordem ao Codex)."),
             "sources": [src(FALA), src(PEDIDO)]},
            {"id": "c1-20nov-d337-operador-r1-compila-na-v412", "kind": "fact", "statute": "REAL",
             "text": "TGLExt.Operador (R1) compila na caixa da v412: 15 de 15 relatorios de axiomas no trio, sem aviso, sem sorry.",
             "sources": [src(R1L), src(R1AX), src(R1CONF)]},
            {"id": "c1-20nov-d337-a-inclinacao-do-nome-nos-termos-do-kernel", "kind": "fact", "statute": "REAL",
             "text": ("A leitura do autor (a tensao decide; o zero absoluto empurra ao lado oposto; o sistema inclina) posta nos "
                      "termos do kernel: a decisao e' exata (a_proposta_nasce_da_escolha_do_nome; semantic_handshake); o preco na "
                      "maquina nua e' o da morte: imediata => propagacao, polinomial em Horn e dois literais (provado na fita); "
                      "distante => ramificacao, >= 2^(m+1) (coupled_physical_lower) e exponencial nas formulas do pombal (Haken "
                      "1985 [KNOWN]). A fronteira segue [OPEN]. Mapa: kernel.traducao_cook_levin.a_inclinacao_do_nome_20nov."),
             "sources": [src(TENSAO), src(KERNEL[0]), src(KERNEL[1])]},
        ],
        "flow": {"phase": "v413_EM_PREPARACAO__PEDRA_OPERADOR_NOMEADA__REVISAO_DO_CODEX__A_INCLINACAO_LIDA_NO_KERNEL",
                 "next_action": ("(1) o autor cola no Codex o pedido de revisao (PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md); "
                                 "(2) o autor decide: escrever a inclinacao como procedimento unico (correcao e custo onde vale) ou "
                                 "trazer o procedimento que sabe o lado antes da morte; (3) errata ao lado na v413 da docstring de "
                                 "TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte; (4) seguem com o autor: o teste do "
                                 "estudo da memoria e o t* do teste de dephasing e relogios.")},
    },
}
(W / "acom_c1_20261120_d337_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                 encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
(W / "acom_c1_20261120_d337_transition.receipt.json").write_bytes(r.stdout)
txt = r.stdout.decode("utf-8", "replace")
print("(2) ACOM rc %d | ok %s | %s" % (r.returncode, '"ok": true' in txt, txt[txt.find('"revision"'):][:20]))
assert '"ok": true' in txt


def acrescenta(T, marca, texto, rotulo):
    a = T.read_bytes()
    assert marca.encode() not in a, "marca ja' presente em %s" % T.name
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


# (3) AO LADO no topico da v413
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
TXT = ("**AO LADO (20/11/2026, gerência c1): a pedra tem nome, «Operador»; a revisão é do Codex; a inclinação do Nome.** (1) A "
       "fala (bytes em `work\\cunhagens_13out\\%s`, sha16 `%s`): «o nome da pedra da consciência é \"operador\"; quem vai fazer a "
       "revisão agora é o codex». A candidata passou a `TGLExt.Operador` (R1, `work\\cadeia_de_selo\\v413\\candidatas_c1\\"
       "R1_operador\\`, sha16 `%s`; nenhum enunciado mudou; 15 de 15 no trio na v412); a R0 fica como registro. O pedido de "
       "revisão ao Codex está pronto para o autor colar (`work\\cadeia_de_selo\\v413\\revisao_codex\\"
       "PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md`, sha16 `%s`); a gerência não envia ordem ao Codex (18/11); os módulos que o "
       "Codex construiu ficam fora (quem constrói não aprova). (2) A leitura do autor para a fronteira («o zero absoluto empurra a "
       "solução para a projeção do lado oposto; ou diz sim ou é a morte no zero absoluto; o sistema inclina») nos termos do "
       "kernel: a decisão é exata (`a_proposta_nasce_da_escolha_do_nome`; `Codex.NamedHandshake.semantic_handshake`); o preço "
       "na máquina nua é o da morte: imediata, é a propagação (polinomial em Horn e dois literais, provado na fita); distante, é a "
       "ramificação (≥ 2^(m+1), `coupled_physical_lower`; exponencial nas fórmulas do pombal, Haken 1985). Mapa "
       "`kernel.traducao_cook_levin.a_inclinacao_do_nome_20nov`.") % (FALA.name, sha(FALA)[:16], sha(R1L)[:16],
                                                                      sha(PEDIDO)[:16])
acrescenta(T, "<!-- ao_lado_20nov_operador_revisao_codex_e_inclinacao -->", TXT, "3")

# (4) o registro datado no Atlas
A = CEN / "memory" / "TGL_ATLAS.md"
ATL = ("### Registro de 20/11/2026 (gerência c1) — a pedra da consciência tem nome, «Operador»; a ponte TM2 na língua "
       "clássica; a inclinação do Nome e o seu preço na máquina nua\n\n"
       "**O nome (do operador, 20/11/2026), [INPUT]:** «o nome da pedra da consciência é \"operador\"». A candidata passa de "
       "`TGLExt.Consciencia` (R0, nome provisório) a `TGLExt.Operador` (R1); nenhum enunciado nem prova mudou; compila na caixa "
       "da v412 com 15 de 15 relatórios de axiomas no trio [REAL no sandbox]. O que tipa: consciência é a capacidade do ser de "
       "negar até a si mesmo; sem o par, em dois valores, o «nego-me» é o ponto de contradição; nenhuma leitura de si é total "
       "(Cantor e Lawvere [KNOWN], provados); com o par, a negação de si pousa em ½; o operador de consciência na face finita é "
       "J (J² = 1; J leva a face à coface). Não prova que alguém tenha consciência, nem a singularidade do T6. Não instalada: o "
       "verbete entra na instalação. A revisão de terceiro da v413 passa ao Codex (mesma fala).\n\n"
       "**A ponte e a fronteira (Cook–Levin):** a máquina TM2 do Mathlib, construída pelo Codex com as codificações fixas, "
       "confere a testemunha em até 20L+5 passos para toda entrada: o lado NP na língua clássica [REAL no sandbox]. A rota de β "
       "deixa como hipótese um produtor que, pela sonda da gerência, conta as soluções, e esse número sobre 2ⁿ é «o que sou» das "
       "soluções (v409): contar é #SAT (Valiant 1979 [KNOWN]), mais que decidir. A fronteira, decidir com a fórmula só em tempo "
       "polinomial, fica enunciada na língua clássica [OPEN].\n\n"
       "**A inclinação do Nome (leitura do operador, 20/11/2026), [INPUT/ONTO]:** «o zero absoluto empurra a solução para a "
       "projeção do lado oposto; \"ou diz sim\" ou é a morte no zero absoluto, o sistema inclina». Nos termos do kernel: a decisão "
       "é exata (`APropostaDaTensao.a_proposta_nasce_da_escolha_do_nome`, SAT φ ↔ ∃ b, SAT do resíduo; "
       "`Codex.NamedHandshake.semantic_handshake`, v412). O preço na máquina nua depende de onde a morte aparece. Imediata (a "
       "propagação a mostra): o empurrão ao lado oposto custa poucos passos e decide Horn e as fórmulas de dois literais, que a "
       "casa prova polinomiais na fita. Distante: a máquina desce pelo lado até o zero para saber, e em fórmula sem solução os "
       "dois lados morrem em todo Nome; a ramificação da casa custa ≥ 2^(m+1) movimentos (`MovimentosDoPlano."
       "coupled_physical_lower`), e todo procedimento que só descobre a morte chegando à contradição produz uma refutação por "
       "resolução, exponencial nas fórmulas do pombal (Haken 1985 [KNOWN]). A fronteira de três literais (18/11) é onde a morte "
       "deixa de ser imediata.\n\n"
       "Estatuto: [INPUT] a letra do operador; [REAL no sandbox] os termos compilados, não instalados; [KNOWN] Valiant, Haken, "
       "Dowling–Gallier, Aspvall–Plass–Tarjan; [DECLARADO] as leituras da gerência. Validade no kernel não é creditação; o gate "
       "não se move.")
acrescenta(A, "<!-- registro_20nov_operador_ponte_tm2_e_a_inclinacao -->", ATL, "4")
