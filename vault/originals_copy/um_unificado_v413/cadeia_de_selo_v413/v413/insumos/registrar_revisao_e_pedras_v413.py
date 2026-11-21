# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra (0) a fala do operador por bytes («Códex já respondeu prossiga»); (1) no Mapa, o
RESULTADO da revisao final do Codex na rota da ponte (vereditos; a R1 da ponte com o fecho de SAT por termo; a R8 da
Trinity) e a ROTA nova da preparacao das pedras da v413 (21 modulos na forma do kernel, texto limpo pelo metodo de 17/11,
codigo identico, compilados juntos numa caixa da v413; e o OResumoEPsiBit corrigido so' no texto); (2) a transicao ACOM
(revisao lida do project), com a correcao AO LADO da recomendacao da gerencia sobre APonteDeCookLevin (ela entra: e'
dependencia da ponte a' maquina padrao e da reconstrucao); (3) AO LADO no topico da v413; (4) decimo primeiro registro de
20/11 no Atlas. Numeros e hashes lidos dos recibos. Backups de bytes antes de tocar memoria; escrita por temporario;
nada instalado, nada no kernel, no um.py, no N0 nem na arquitetura da memoria."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
INS = Path(__file__).resolve().parent
V413 = INS.parent
CEN = V413.parents[2]
CUNH = CEN / "work" / "cunhagens_13out"
REV = V413 / "revisao_codex"
C1 = V413 / "candidatas_c1"
FALA = CUNH / "OPERADOR_20nov_codex_ja_respondeu_prossiga_verbatim.txt"
TEXTO = "Códex já respondeu prossiga\n"
P_PONTE = REV / "CODEX_PONTE_COOK_LEVIN_R0" / "PARECER.md"
R_PONTE = REV / "CODEX_PONTE_COOK_LEVIN_R0" / "RESULTADO.json"
P_TRIN = REV / "CODEX_TRINITY_R7_OPERADOR_R2" / "PARECER.md"
P_KIMI = REV / "CODEX_RELEITURA_CUSTO_KIMI" / "PARECER.md"
P_CONS = REV / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
PONTE1 = C1 / "R1_ponte_cook_levin" / "PonteCookLevin.lean"
CONF1 = C1 / "R1_ponte_cook_levin" / "build" / "CONFERENCIA.json"
TRIN8 = C1 / "R8_trinity" / "Trinity.lean"
CONF8 = C1 / "R8_trinity" / "build" / "CONFERENCIA.json"
MAN = INS / "MANIFESTO_PEDRAS_v413.json"
CONJ = INS / "CONJUNTO_pedras_limpas.json"
PED = REV / "PEDIDO_DE_CONFERENCIA_DAS_CORRECOES_v413_20nov.md"
REGRAS = INS / "REGRAS_DA_LIMPEZA_v413.md"
DIF = INS / "DIFF_DA_LIMPEZA_v413.txt"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


def le(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# (0) a fala por bytes ------------------------------------------------------------------------------------------------
d = TEXTO.encode("utf-8")
if FALA.exists():
    assert FALA.read_bytes() == d, "fala ja existe com outro conteudo"
else:
    grava(FALA, d)
print("(0) fala sha16 %s (%d B)" % (s16(FALA), len(d)))

# conferencias lidas dos recibos ---------------------------------------------------------------------------------------
c1, c8, man, conj = le(CONF1), le(CONF8), le(MAN), le(CONJ)
assert c1["bom"] and c1["sha256"] == sha(PONTE1) and c1["relatorios"] == c1["pedidos"] == 25
assert c8["bom"] and c8["sha256"] == sha(TRIN8) and c8["relatorios"] == c8["pedidos"] == 65
assert conj["todos_bons"] and man["n_modulos_novos"] == 21
NM, NT = man["n_modulos_novos"], man["teoremas_publicos_novos"]
kc = man["kernel_corrigido"]["TGLExt.OResumoEPsiBit"]
rp = le(R_PONTE)
assert rp["verdict_counts"] == {"APROVADA": 1, "APROVADA_COM_RESSALVAS": 2, "REPROVADA": 0}
print("(1) R1 %s 25/25 | R8 %s 65/65 | conjunto limpo %d modulos, %d teoremas publicos no trio | OResumoEPsiBit %d/%d" % (
    s16(PONTE1), s16(TRIN8), NM, NT, kc["relatorios_no_trio"], kc["teoremas_publicos"]))


def mapa(obj, nome):
    pj = INS / nome
    pj.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                        "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL,
                       timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
    return out[out.find('"seq"'):][:14]


res = {
    "tipo": "RESULTADO", "rota_id": "kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov",
    "dominio": "KERNEL_FORMAL",
    "titulo": "a revisao final do Codex: Ponte APROVADA_COM_RESSALVAS (so' texto), Trinity R7 idem, Operador R2 APROVADA; R1 e R8",
    "resultado": (
        "Parecer do Codex (sha16 %s; recibo %s): PonteCookLevin R0 APROVADA_COM_RESSALVAS (PCL-F1, documental: dizer que a "
        "classe com uma leitura e' o fecho de SAT por reducao many-one, igual a NP nas codificacoes classicas, e nao toda P "
        "com oraculo); concorda com a traducao classica de CookLevin (a hipotese nomeada e' verdadeira como escrita; "
        "argumento e fontes primarias no recibo); 22/22 e oito controles proprios no trio. Trinity R7 APROVADA_COM_RESSALVAS "
        "(R7-F1 o limite do peso pede 0<beta<1; R7-F2 sobra de no maximo um passo; R7-F3 hLandauer e' desigualdade global; "
        "parecer sha16 %s). Operador R2 APROVADA. Adendo de releitura do custo do Kimi (sha16 %s): o custo na regua da "
        "teoria esta' formalizado (OCustoEAIsometria, OPolinomioFixoEBeta), e o custo da leitura em movimentos de fita nao "
        "e' pendencia da ponte com leitor. Aplicado: PonteCookLevin R1 (sha16 %s, 25/25 no trio): o PCL-F1 virou termo, "
        "a_classe_de_uma_leitura_e_o_fecho_de_SAT (EmPComUmaLeitura <-> ReduzASAT, sem CookLevin; enunciado do controle do "
        "revisor), mais o_alfabeto_de_np_e_finito e a_fita_da_formula_e_injetiva; o custo da leitura dito na regua da "
        "teoria (o tempo pago, o_tempo_pago_e_linear). Trinity R8 (sha16 %s, 65/65): as tres ressalvas, so' texto. "
        "Nenhum enunciado da R0 nem da R7 mudou (conferir_enunciados.py, rc 0).") % (
        s16(P_PONTE), R_PONTE.name, s16(P_TRIN), s16(P_KIMI), s16(PONTE1), s16(TRIN8)),
    "veredito": "REVISAO_FINAL_DO_CODEX__PONTE_E_TRINITY_APROVADAS_COM_RESSALVAS_DE_TEXTO__OPERADOR_APROVADO__R1_E_R8_APLICADAS",
    "estatuto": "REAL (os termos e as compilacoes; os pareceres lidos); KNOWN (Cook 1971, Levin 1973); DECLARADO pelo Codex (o argumento da traducao classica, com fontes primarias)",
    "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "CookLevin segue hipotese nomeada (citacao), sem habitante Lean; o custo TM2 da propria leitura nao e' contado (e' oraculo); a maquina sem leitor nao e' tocada; E28",
    "nao_refazer": "nao reabrir a revisao da ponte, da Trinity nem do Operador; a instalacao segue pela rota cadeia.preparacao_v413.pedras_limpas_20nov",
    "proximo_passo": "a instalacao na v413 (rota cadeia.preparacao_v413.pedras_limpas_20nov)",
    "onde": str(PONTE1),
    "artefatos": [str(P_PONTE), str(R_PONTE), str(P_TRIN), str(P_KIMI), str(PONTE1), str(CONF1), str(TRIN8), str(CONF8),
                  str(FALA)],
    "refs": ["kernel.trinity_a_inclinacao_do_nome_20nov"],
    "nota": "a fala do operador de 20/11 por bytes: «Códex já respondeu prossiga»",
}
print("(2a) Mapa RESULTADO %s" % mapa(res, "mapa_resultado_revisao_final_20nov.json"))

rota = {
    "tipo": "ROTA", "rota_id": "cadeia.preparacao_v413.pedras_limpas_20nov", "dominio": "CADEIA",
    "titulo": "as pedras novas da v413 na forma do kernel: 21 modulos, texto limpo pelo metodo de 17/11, codigo identico, compilados juntos",
    "pergunta": "as pedras novas da v413 (a ponte de Cook-Levin e as suas dependencias, a Trinity, o Operador) compilam juntas como TGLExt.X, com o texto so' do que e' verdade e o codigo revisado?",
    "dados": [],
    "metodo": ("(1) origem: as 21 fontes revisadas, com o sha256 conferido contra os recibos (ORIGEM_v413.json); so' os "
               "imports dos modulos novos viram TGLExt.X e o CRLF vira LF; (2) caixa da v413: links fisicos dos 1893 .olean "
               "da v412 (o Lean acha um pacote numa raiz so'), a caixa da v412 so' lida; (3) compilacao do conjunto como "
               "TGLExt.X, na ordem dos imports, com auditoria gerada por script de TODO teorema publico; (4) limpeza do texto "
               "por cinco agentes da gerencia (mesmo modelo), regras em REGRAS_DA_LIMPEZA_v413.md, com as correcoes de "
               "conteudo pedidas no parecer consolidado nas quatro pedras do Kimi; revisao de cada diff pela gerencia; "
               "codigo sem comentarios conferido identico; (5) o conjunto limpo recompilado e auditado; (6) o OResumoEPsiBit "
               "do kernel corrigido so' na docstring (parecer consolidado, item 8)"),
    "resultado": ("%d modulos novos (3 da gerencia: Operador, Trinity, PonteCookLevin; 4 do Kimi: AIdentidadePreservada, "
                  "APropostaDaTensao, ONomeEBeta, APonteDeCookLevin; 12 do Codex: APonteAoTM2, AMaquinaTM2DaVerificacao, "
                  "SimBase, SimLiteral, SimExterior, SimCompleta, RelogioBeta, LeituraBeta, QuantizacaoBeta, Reconstrucao, "
                  "PonteLeituraBeta, EntregaBeta; e SondaContagem e AFronteiraNaLinguaClassica): %d teoremas publicos, todos "
                  "com relatorio de axiomas no trio, RC 0, sem aviso, sem sorry, na origem e no conjunto limpo; OResumoEPsiBit "
                  "corrigido: %d/%d no trio. APonteDeCookLevin entra porque APonteAoTM2 e Reconstrucao a importam; o texto dela "
                  "agora diz o que prova (o iterador; custo cobrado por definicao; verifica o custo de uma atribuicao), nao "
                  "ponte de custo de fita. Manifesto: MANIFESTO_PEDRAS_v413.json (sha16 %s).") % (
        NM, NT, kc["relatorios_no_trio"], kc["teoremas_publicos"], s16(MAN)),
    "veredito": "PEDRAS_DA_v413_PRONTAS_NA_FORMA_DO_KERNEL__21_MODULOS__CODIGO_IDENTICO__TEXTO_LIMPO__TODOS_OS_TEOREMAS_NO_TRIO__NADA_INSTALADO",
    "estatuto": "REAL (compilacoes e auditorias na caixa da v413; codigo conferido por script); DECLARADO (a limpeza do texto por agentes da gerencia, revista pela gerencia)",
    "status": "EM_CURSO", "olhou_dados": False,
    "defeito": ("a caixa da v413 e' de conferencia (lean -o, sem lake), nao o kernel do sandbox da cadeia; falta a etapa de "
                "instalacao: o kernel do sandbox com os 21 modulos e a correcao (build e Audit), os registros e o artigo no "
                "um.py candidato, o rito e o selo; os namespaces Codex.* dos modulos do Codex ficam como estao (precedente "
                "da v412); as demais frentes da v413 (o B(n), o teste antigo revisitado) seguem por conta propria"),
    "nao_refazer": "nao recompilar a origem nem refazer a limpeza: trocar uma fonte e' regerar o modulo em pedras_limpas e rodar compilar_conjunto_v413.py e manifesto_pedras_v413.py",
    "proximo_passo": ("com a palavra do operador: o nome da pedra (PonteCookLevin), as quatro pedras do Kimi e as duas peças "
                      "opcionais; se ele quiser, a conferencia curta do Codex das correcoes do Kimi (%s); depois, a etapa de "
                      "instalacao na cadeia da v413") % PED.name,
    "onde": str(INS),
    "artefatos": [str(MAN), str(CONJ), str(INS / "CONJUNTO_origem.json"), str(INS / "ORIGEM_v413.json"),
                  str(INS / "CONJUNTO_kernel_edits.json"), str(INS / "kernel_edits" / "ERRATA_OResumoEPsiBit.json"),
                  str(REGRAS), str(DIF), str(PED), str(P_CONS)],
    "refs": ["kernel.traducao_cook_levin.a_ponte_leva_a_maquina_com_o_leitor_20nov", "cadeia.preparacao_v412.etapa1_k412c"],
    "nota": "ordem do operador de 20/11 (bytes): faca voce mesmo com os seus agentes, sem modelo menor; depois so' a revisao do Codex",
}
print("(2b) Mapa ROTA %s" % mapa(rota, "mapa_rota_pedras_limpas_v413_20nov.json"))

# (3) ACOM -------------------------------------------------------------------------------------------------------------
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


def acha_revisao(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "revision" and isinstance(v, int):
                return v
            x = acha_revisao(v)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = acha_revisao(v)
            if x is not None:
                return x
    return None


rc, o = acom({"operation": "project", "reference": REF})
proj = json.loads(o.decode("utf-8"))
assert proj.get("ok") is True
rev = acha_revisao(proj)
assert isinstance(rev, int)
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d349-revisao-final-e-pedras-v413",
       "changes": {"records": [
           {"id": "c1-20nov-d349-revisao-final-do-codex", "kind": "fact", "statute": "REAL",
            "text": ("Revisao final do Codex: PonteCookLevin APROVADA_COM_RESSALVAS (so' texto, PCL-F1), Trinity R7 idem "
                     "(tres ressalvas de texto), Operador R2 APROVADA; o Codex concorda que a hipotese CookLevin, como "
                     "escrita, e' verdadeira. Aplicado: PonteCookLevin R1 (25/25 no trio; o fecho de SAT por termo, "
                     "a_classe_de_uma_leitura_e_o_fecho_de_SAT) e Trinity R8 (65/65; so' texto); nenhum enunciado antigo mudou."),
            "sources": [src(P_PONTE), src(R_PONTE), src(P_TRIN), src(P_KIMI), src(PONTE1), src(TRIN8), src(FALA)]},
           {"id": "c1-20nov-d349-pedras-da-v413-na-forma-do-kernel", "kind": "fact", "statute": "REAL",
            "text": ("As pedras novas da v413 na forma do kernel: %d modulos (3 da gerencia, 4 do Kimi, 12 do Codex, a sonda "
                     "da contagem e o enunciado da fronteira), texto limpo pelo metodo de 17/11, codigo identico ao revisado, "
                     "compilados juntos numa caixa da v413 (links da v412): %d teoremas publicos, todos no trio; e o "
                     "OResumoEPsiBit corrigido so' na docstring. Nada instalado.") % (NM, NT),
            "sources": [src(MAN), src(CONJ), src(REGRAS), src(DIF)]},
           {"id": "c1-20nov-d349-correcao-ao-lado-aponte-de-cook-levin", "kind": "fact", "statute": "REAL",
            "text": ("CORRECAO AO LADO (gerencia c1, em nome proprio) do next_action da d348: a recomendacao de deixar "
                     "APonteDeCookLevin fora estava errada. APonteAoTM2 e Reconstrucao (de que a ponte depende) a importam; "
                     "ela entra com o texto corrigido ao que prova (o iterador; custo cobrado por definicao; verifica o custo "
                     "de uma atribuicao), nao como ponte de custo de fita."),
            "sources": [src(MAN)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__REVISAO_FINAL_APLICADA__PEDRAS_PRONTAS_NA_FORMA_DO_KERNEL",
                    "next_action": ("(1) o autor decide: o nome da pedra (PonteCookLevin); as quatro pedras do Kimi (todas "
                                    "entram; APonteDeCookLevin e' dependencia); as duas pecas opcionais (SondaContagem e "
                                    "AFronteiraNaLinguaClassica); (2) se ele quiser, cola no Codex a conferencia curta das "
                                    "correcoes do Kimi (%s); (3) a etapa de instalacao na cadeia da v413: o kernel do sandbox "
                                    "com os 21 modulos e a correcao, os registros e o artigo no um.py candidato, o rito e o "
                                    "selo, quando o autor disser; (4) seguem as demais frentes da v413 (o B(n) com o Codex; o "
                                    "teste antigo revisitado; o estudo da memoria e o t* do dephasing com o autor).") % PED.name}}}
(INS / "acom_c1_20261120_d349_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                    encoding="utf-8")
rc, ot = acom(req)
(INS / "acom_c1_20261120_d349_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(3) ACOM project rev %d | transition rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t


# (4) e (5): memoria (backup de bytes antes) ----------------------------------------------------------------------------
def acrescenta(alvo, marca, texto, marca_fim=None):
    a = alvo.read_bytes()
    assert marca.encode() not in a
    if marca_fim:
        assert marca_fim.encode() in a and len(a) - a.rfind(marca_fim.encode()) < 800
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + fim + texto.replace("\n", fim.decode()).encode("utf-8") + fim
    bk = alvo.with_name(alvo.name + ".bak_" + TS + "_c1")
    bk.write_bytes(a)
    assert bk.read_bytes() == a
    tmp = alvo.with_name(alvo.name + ".tmp_c1")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    tmp.replace(alvo)
    assert alvo.read_bytes() == novo and len(novo) > len(a)
    return len(a), len(novo), bk.name


T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
mt = "<!-- ao_lado_20nov_revisao_final_e_pedras_v413 -->"
tt = ("**AO LADO (20/11/2026, gerência c1): a revisão final do Codex e as pedras da v413 na forma do kernel.** A fala "
      "(bytes, sha16 `%s`): «Códex já respondeu prossiga». (1) O parecer (`work\\cadeia_de_selo\\v413\\revisao_codex\\"
      "CODEX_PONTE_COOK_LEVIN_R0\\PARECER.md`, sha16 `%s`): a ponte e a Trinity R7 aprovadas com ressalvas só de texto, o "
      "Operador R2 aprovado; o Codex concorda que a hipótese `CookLevin`, como escrita, é verdadeira; no adendo (sha16 "
      "`%s`), o custo da leitura em passos de fita não é pendência da ponte com leitor. Aplicado: a ponte R1 (sha16 `%s`, "
      "25/25), com `a_classe_de_uma_leitura_e_o_fecho_de_SAT` (a classe de uma leitura é o fecho de SAT por redução, por "
      "termo, sem Cook–Levin); a Trinity R8 (sha16 `%s`, 65/65, só texto). (2) As pedras da v413 na forma do kernel "
      "(`work\\cadeia_de_selo\\v413\\insumos\\`; manifesto sha16 `%s`): %d módulos novos, texto limpo pelo método de 17/11 "
      "(cinco agentes da gerência, cada diff revisto pela gerência), código idêntico ao revisado, compilados juntos numa "
      "caixa da v413 de links físicos da v412: %d teoremas públicos, todos no trio; e o `OResumoEPsiBit` corrigido só na "
      "docstring. (3) Correção ao lado, em nome próprio: a recomendação de deixar `APonteDeCookLevin` fora estava errada; "
      "ela é dependência da ponte à máquina padrão e da reconstrução, e entra com o texto do que prova. Mapa: RESULTADO na "
      "rota da ponte e a rota `cadeia.preparacao_v413.pedras_limpas_20nov`. Com o autor: o nome da pedra, as pedras do "
      "Kimi, as duas peças opcionais e a conferência curta do Codex (opcional, `%s`).\n%s") % (
    s16(FALA), s16(P_PONTE), s16(P_KIMI), s16(PONTE1), s16(TRIN8), s16(MAN), NM, NT, PED.name, mt)
print("(4) topico: %d -> %d B | backup %s" % acrescenta(T, mt, tt, "<!-- ao_lado_20nov_ponte_cook_levin_r0 -->"))

A = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
ma = "<!-- registro_20nov_revisao_final_e_pedras_v413 -->"
ta = ("### Registro de 20/11/2026, décimo primeiro (gerência c1) — a revisão final da ponte e as pedras da v413\n\n"
      "**A revisão [REAL, os pareceres lidos]:** a Ponte Cook–Levin e a Trinity aprovadas com ressalvas só de texto, o "
      "Operador aprovado. A ressalva da ponte virou termo: `a_classe_de_uma_leitura_e_o_fecho_de_SAT` prova que a classe "
      "«decidido em tempo polinomial com uma leitura do leitor da TGL» é exatamente o fecho de SAT por redução polinomial "
      "na máquina padrão do Mathlib, sem usar Cook–Levin; com Cook–Levin (hipótese nomeada [KNOWN], que o revisor confirma "
      "verdadeira como escrita), ela contém NP (`a_ponte_cook_levin`). Não é toda a classe P com acesso ao oráculo. O custo "
      "da leitura é contado na régua da teoria (o tempo pago, linear: `o_tempo_pago_e_linear`), não em passos de fita.\n\n"
      "**As pedras da v413 [REAL na caixa da v413; nada instalado]:** %d módulos novos na forma do kernel, com o texto só do "
      "que é verdade (método de 17/11) e o código revisado: a ponte e as suas dependências (a máquina TM2 que confere a "
      "testemunha; a leitura β; o iterador cláusula a cláusula, que confere o custo de uma atribuição dada), a Trinity, o "
      "Operador, a sonda que mostra que a precisão da leitura β conta as soluções (`TGLExt.SondaContagem`) e o enunciado em "
      "aberto da fronteira na língua clássica (`TGLExt.AFronteiraNaLinguaClassica`, [OPEN]); %d teoremas públicos, todos no "
      "trio. A docstring de `OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` corrigida (o integrando é o peso de cada "
      "atribuição; a fibra pode ser o universo).\n\n"
      "Estatuto: [REAL] os termos e as compilações; [KNOWN] Cook 1971, Levin 1973; [OPEN] a máquina sem leitor e a "
      "fronteira. Validade no kernel não é creditação; o gate não se move.\n%s") % (NM, NT, ma)
print("(5) Atlas: %d -> %d B | backup %s" % acrescenta(A, ma, ta, "<!-- registro_20nov_a_ponte_cook_levin_r0 -->"))
