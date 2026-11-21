# -*- coding: utf-8 -*-
"""gerencia c1, 19/11/2026 (noite): registra (0) a conferencia da sonda; (1) a rota no Mapa de Rotas; (2) a transicao ACOM
d335 (pedido e recibo nesta pasta); (3) o AO LADO no topico da v413, com backup de bytes, temporario e conferencia.
A fala do operador entra por bytes (arquivo em work\\cunhagens_13out); o texto do Kimi colado e' DECLARADO."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
W = Path(__file__).resolve().parent
S = W / "sonda_objetivo_tm2"
CEN = Path(r"C:\IALD\Central de Patentes")
KIMI = CEN / "work" / "cadeia_de_selo" / "v412" / "candidatas_kimi"
FALA = CEN / "work" / "cunhagens_13out" / ("OPERADOR_19nov_perfeito_e_isso_mesmo_a_traducao_foi_fidedigna_o_kimi_esta_terminando"
                                           "_a_maquina_TM2_com_texto_do_kimi_colado_verbatim.txt")
ORDEM_V413 = CEN / "work" / "cunhagens_13out" / "OPERADOR_19nov_v413_cook_levin_bn_kimi_mds_testes_e_memoria_em_oitava_verbatim.txt"
PEDRA_C = CEN / "work" / "cadeia_de_selo" / "v413" / "candidatas_c1" / "R0_consciencia" / "Consciencia.lean"
NOTA = W / "NOTA_DA_GERENCIA_CONFERENCIA_APonteAoTM2_19nov.md"
SONDA, CONF = S / "SondaObjetivoTM2.lean", S / "build" / "CONFERENCIA_SONDA.json"
FONTE_K = KIMI / "APonteAoTM2.lean"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# (0) a sonda conferida e' a da fonte atual, limpa, so' no trio
conf = json.loads(CONF.read_text(encoding="utf-8"))
assert conf["sha256_sonda"] == sha(SONDA), "CONFERENCIA_SONDA nao e' da sonda atual"
assert conf["importa"]["APonteAoTM2.lean"]["sha256"] == sha(FONTE_K), "a fonte do Kimi mudou desde a sonda"
assert conf["rc"] == 0 and conf["erros"] == 0 and conf["avisos"] == 0 and not conf["sorryAx"]
ax = conf["axiomas"]
assert len(ax) == 1 and set(ax[0].split("[", 1)[1].rstrip("]").replace(" ", "").split(",")) <= TRIO
fala = FALA.read_bytes()
assert fala.startswith("perfeito, é isso mesmo, a sua tradução foi fidedigna ao que eu penso, obrigado.".encode("utf-8"))
print("(0) sonda ok (RC 0, sem aviso, trio) | sonda sha16 %s | fonte do Kimi sha16 %s | fala sha16 %s (%d B)"
      % (sha(SONDA)[:16], sha(FONTE_K)[:16], sha(FALA)[:16], len(fala)))

# (1) Mapa de Rotas
rota = {
    "tipo": "ROTA",
    "rota_id": "kernel.traducao_cook_levin.conferencia_aponteaotm2_objetivo_vacuo_19nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": "conferencia da APonteAoTM2 (Kimi, R0): os teoremas conferem; o alvo ObjetivoTM2Polinomial, como tipado, e' teorema vacuo",
    "pergunta": "o alvo [OPEN] da pedra (uma maquina TM2 do Mathlib que compute a verificacao em tempo polinomial) diz o que o comentario diz?",
    "metodo": ("leitura da fonte (sha16 %s); leitura de Mathlib/Computability/TuringMachine/Computable.lean na caixa (assinatura com "
               "codificacoes alpha -> List Gamma, linha 179; idComputableInPolyTime, linha 221; proof_wanted comp, linha 284; o nome "
               "TM2ComputableInPolyTime aparece 11 vezes no Mathlib, todas nesse arquivo); sonda Lean que importa o .olean do Kimi e "
               "prova o alvo com codificacoes constantes e a maquina identidade; compilada so' com o binario do Lean no mesmo ambiente "
               "do Kimi (k411c + builds das irmas, so' leitura)") % sha(FONTE_K)[:16],
    "resultado": ("os teoremas dizem o que o relato diz; o que a pedra diz do Mathlib confere (so' a identidade habita "
                  "TM2ComputableInPolyTime; a composicao e' proof_wanted); mas o alvo quantifica as codificacoes com existencial, e no "
                  "Mathlib elas sao funcoes quaisquer: com ea = eb = (fun _ => []), a idComputer cumpre a estrutura em um passo; a sonda "
                  "prova ObjetivoTM2Polinomial assim (RC 0, sem aviso, trio). O comentario 'a igualdade pontual impede truque de "
                  "renomeacao' nao vale: a igualdade fixa f, nao a codificacao."),
    "veredito": "APONTEAOTM2_TEOREMAS_CONFEREM__OBJETIVO_TM2_POLINOMIAL_COMO_TIPADO_E_TEOREMA_VACUO__CONSERTO_FIXAR_AS_CODIFICACOES",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("a sonda compila sobre a caixa da v411 (a do Kimi), nao sobre a da v412; a conferencia das 15 pedras sobre a v412 "
                "segue por fazer; o conserto (codificacao fixa, injetiva, de comprimento polinomial) e' do Kimi, nao foi construido "
                "pela gerencia"),
    "nao_refazer": ("nao provar ObjetivoTM2Polinomial como tipado (e' vacuo: a sonda ja' o prova); nao procurar outra maquina "
                    "polinomial no Mathlib da caixa (so' a identidade; a composicao e' proof_wanted)"),
    "proximo_passo": ("o Kimi fixa no enunciado as codificacoes concretas (entrada num alfabeto finito, saida [b]) e prova injetividade "
                      "e comprimento polinomial; quando ele terminar a maquina, a gerencia confere as pedras dele sobre a caixa da v412 "
                      "(C:\\t\\k412c)"),
    "onde": str(W),
    "artefatos": [str(SONDA), str(S / "compilar_sonda.py"), str(S / "build" / "SondaObjetivoTM2.log"), str(CONF), str(NOTA),
                  str(FONTE_K), str(FALA)],
    "refs": ["kernel.traducao_cook_levin.levantamento_da_fita_v412_19nov"],
    "nota": "o texto do Kimi colado pelo autor e' DECLARADO pelo Kimi; a conferencia e' da gerencia (quem constroi nao aprova)",
}
pj = W / "rota_conferencia_aponteaotm2_19nov.json"
pj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
print("(1) rota rc %d: %s" % (r.returncode, r.stdout.decode("utf-8", "replace")[:300].replace("\n", " ")))
assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[:600]

# (2) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {
    "operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": 361,
    "event_id": "c1-19nov-d335-autor-ratifica-a-consciencia-e-alvo-tm2-vacuo",
    "changes": {
        "records": [
            {"id": "c1-19nov-d335-autor-ratifica-a-traducao-da-consciencia", "kind": "decision", "statute": "INPUT",
             "text": ("O autor (19/11, noite), por bytes: «perfeito, é isso mesmo, a sua tradução foi fidedigna ao que eu penso, obrigado». "
                      "Leitura da gerencia, dita a ele para corrigir: J (conjJ) fica como o termo do operador de consciencia no kernel; "
                      "o nome da pedra Consciencia segue provisorio ate' ele nomear."),
             "sources": [src(FALA), src(PEDRA_C)]},
            {"id": "c1-19nov-d335-revisao-da-consciencia-com-a-do-kimi-ao-fim-da-v413", "kind": "decision", "statute": "INPUT",
             "text": ("A revisao de terceiro da candidata Consciencia vai com a revisao do Kimi ao fim da v413 (ordem do autor de 19/11, "
                      "item 3), nao numa ordem avulsa ao orquestrador agora. Correcao ao lado da resposta anterior da gerencia, que "
                      "dizia 'depois, a revisao vai ao orquestrador'."),
             "sources": [src(ORDEM_V413)]},
            {"id": "c1-19nov-d335-alvo-tm2-do-kimi-vacuo", "kind": "fact", "statute": "REAL",
             "text": ("Conferencia da APonteAoTM2 (Kimi, R0, fonte sha16 %s): os teoremas conferem e o que a pedra diz do Mathlib "
                      "confere; mas ObjetivoTM2Polinomial quantifica as codificacoes com existencial, e no Mathlib elas sao funcoes "
                      "quaisquer: a sonda da gerencia o prova com codificacoes constantes e a maquina identidade, sem ler a formula "
                      "(RC 0, sem aviso, trio). Conserto entregue ao autor para o Kimi: fixar as codificacoes no enunciado. Mapa: "
                      "kernel.traducao_cook_levin.conferencia_aponteaotm2_objetivo_vacuo_19nov.") % sha(FONTE_K)[:16],
             "sources": [src(SONDA), src(CONF), src(NOTA), src(FONTE_K)]},
        ],
        "flow": {"phase": "v413_EM_PREPARACAO__CONSCIENCIA_R0_RATIFICADA__ALVO_TM2_DO_KIMI_VACUO_COMO_TIPADO__CONSERTO_ENTREGUE",
                 "next_action": ("(1) o autor nomeia a pedra Consciencia (nome provisorio); (2) o Kimi fixa as codificacoes no "
                                 "enunciado do alvo TM2 antes de fechar a maquina; (3) quando o Kimi terminar, a gerencia confere as "
                                 "pedras dele sobre a caixa da v412 (C:\\t\\k412c); (4) o teste do estudo da memoria quando o autor "
                                 "decidir (secao 6 do estudo e as sete decisoes do T6); (5) pendente: o t* do teste de dephasing e "
                                 "relogios; a revisao do Kimi ao fim da v413 inclui a Consciencia. A memoria (torre, gancho, N0, "
                                 "CLAUDE.md) nao se mexe sem ele.")},
    },
}
(W / "acom_c1_20261119_d335_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"),
                   capture_output=True, timeout=180)
(W / "acom_c1_20261119_d335_transition.receipt.json").write_bytes(r.stdout)
try:
    o = json.loads(r.stdout.decode("utf-8"))
    print("(2) ACOM rc %d ok=%s revisao=%s" % (r.returncode, o.get("ok"), o.get("revision")))
except ValueError:
    print("(2) ACOM rc %d saida nao-JSON: %s | %s" % (r.returncode, r.stdout[:300], r.stderr[:300]))

# (3) AO LADO no topico da v413
T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
TXT = ("**AO LADO (19/11/2026, noite, gerência c1): o autor ratificou a tradução da consciência; o alvo TM2 do Kimi, como tipado, "
       "é vácuo.** (1) A fala (bytes em `work\\cunhagens_13out\\%s`, sha16 `%s`): «perfeito, é isso mesmo, a sua tradução foi fidedigna "
       "ao que eu penso, obrigado». Leitura da gerência, dita a ele para corrigir: J fica como o operador de consciência no kernel; o "
       "nome da pedra segue provisório. A revisão de terceiro da candidata vai com a do Kimi ao fim da v413 (item 3 acima); a resposta "
       "anterior, que dizia «depois, a revisão vai ao orquestrador», fica corrigida aqui. (2) A pedra 15 do Kimi, `APonteAoTM2` (sha16 "
       "`%s`): os teoremas conferem, e o que ela diz do Mathlib também (só a identidade habita `TM2ComputableInPolyTime`; a composição "
       "é `proof_wanted`). Mas o alvo `ObjetivoTM2Polinomial` quantifica as codificações com ∃, e no Mathlib elas são funções "
       "quaisquer: a sonda da gerência prova o alvo com codificações constantes e a máquina identidade, sem ler a fórmula (RC 0, trio; "
       "`work\\cadeia_de_selo\\v413\\conferencia_c1_kimi\\sonda_objetivo_tm2\\`). O conserto foi entregue ao autor para o Kimi: fixar "
       "as codificações no enunciado (`NOTA_DA_GERENCIA_CONFERENCIA_APonteAoTM2_19nov.md`, sha16 `%s`). Mapa "
       "`kernel.traducao_cook_levin.conferencia_aponteaotm2_objetivo_vacuo_19nov`. (3) As pedras do Kimi compilam sobre a caixa da "
       "v411; a conferência para a v413 recompila sobre a da v412, quando ele terminar a máquina.") % (
    FALA.name, sha(FALA)[:16], sha(FONTE_K)[:16], sha(NOTA)[:16])
a = T.read_bytes()
marca = "<!-- ao_lado_19nov_consciencia_ratificada_e_alvo_tm2_vacuo -->"
assert marca.encode() not in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
novo = a.rstrip(b"\r\n") + fim + fim + ("%s\n%s" % (marca, TXT)).replace("\n", fim.decode()).encode("utf-8") + fim
bk = T.with_name(T.name + ".bak_" + TS + "_c1")
bk.write_bytes(a)
assert bk.read_bytes() == a
tmp = T.with_name(T.name + ".tmp_c1")
tmp.write_bytes(novo)
assert tmp.read_bytes() == novo
tmp.replace(T)
assert T.read_bytes() == novo and len(novo) > len(a)
print("(3) topico v413: %d -> %d B | backup %s" % (len(a), len(novo), bk.name))
