# -*- coding: utf-8 -*-
"""Os remendos de G1 nos DOIS arquivos que a Central remenda a cada versão (ambos CRLF): o runner da Fronteira e o módulo comum dos
16 dispositivos. Funções PURAS sobre o texto (LF) — testáveis em cópias —, mais o aplicador (backup de BYTES, fim de linha original,
py_compile no temporário, `os.replace`, sentinela de «já aplicado»).

Ancoragem por REGEX QUE CAPTURA A VERSÃO (ESPEC_CENTRAL §6.7 e §7.4), nunca pela prosa da versão anterior: cada troca confere a
contagem e que a versão capturada é a ESPERADA (vANT) antes de trocar.

  G1.0 (uma vez):  o runner ganha `_custodia_generica(versao, anterior)`; o módulo ganha `CAMADAS_GENERICAS` e o carregador de
                   `camada_generica.py`. Os módulos genéricos (generico/custodia_generica.py e generico/camada_generica.py) são instalados
                   em fronteira_tgl\\runner\\ e patents\\_formula_completa\\ pelo script work\\custodia_G1\\patches\\instalar_g1_0.py.
  Por versão:      o runner ganha um STUB de duas linhas por versão (o nome que o quadro procura: `_medir_vNNN_custodia`) e as onze trocas;
                   o módulo ganha a versão na tupla, o parágrafo, o sufixo do veredito, os itens de `nao_se_afirma` e a entrada de `USOS`.
As pedras artesanais anteriores FICAM como estão: são exatas para sempre."""
import os
import re
from pathlib import Path

from . import util
from .util import Parar

ARQ_RUNNER = Path("fronteira_tgl") / "runner" / "one_fronteira.py"
ARQ_FORMULA = Path("patents") / "_formula_completa" / "tgl_formula_completa.py"

CARREGADOR_RUNNER = '''def _custodia_generica(versao, anterior):
    """G1.0: a pedra genérica da custódia (custodia_generica.py, carregada por caminho); lê o cofre `versao` contra o `anterior` PELO NOME."""
    import importlib.util as _ilu
    _s = _ilu.spec_from_file_location("custodia_generica", str(HERE / "custodia_generica.py"))
    _m = _ilu.module_from_spec(_s)
    _s.loader.exec_module(_m)
    return _m.medir_custodia_generica(CUSTODY_DIR.parent, versao, anterior)


'''

CARREGADOR_FORMULA = '''CAMADAS_GENERICAS = ()


def _camadas_genericas(core, selo, cofre):
    """G1.0: camadas da custódia parametrizada (camada_generica.py, carregado por caminho); cada uma lê o FATOS_CUSTODIA.json do cofre da SUA versão."""
    import importlib.util as _ilu
    _s = _ilu.spec_from_file_location("camada_generica", str(Path(__file__).resolve().parent / "camada_generica.py"))
    _m = _ilu.module_from_spec(_s)
    _s.loader.exec_module(_m)
    return {("camada_%s_no_cofre" % _v): _m.conferir_custodia_generica(core, selo, _v, cofre.parent) for _v in CAMADAS_GENERICAS}


'''


def _um(s, rx, rot, flags=re.M):
    ms = list(re.finditer(rx, s, flags))
    if len(ms) != 1:
        raise Parar("âncora «%s» casou %d vez(es), esperado 1" % (rot, len(ms)), [rx[:120]])
    return ms[0]


def _ultimo(s, rx, rot, minimo=1, flags=re.M):
    ms = list(re.finditer(rx, s, flags))
    if len(ms) < minimo:
        raise Parar("âncora «%s» casou %d vez(es), esperado >= %d" % (rot, len(ms), minimo), [rx[:120]])
    return ms[-1], len(ms)


# =================================================================== RUNNER
def runner_g1_0(s):
    """Uma vez: o carregador. Idempotente (sentinela `def _custodia_generica`)."""
    if "def _custodia_generica" in s:
        return s, ["G1.0 já aplicado"]
    m = _um(s, r"^def shadow_the_station\(core, selo\):$", "def shadow_the_station")
    return s[:m.start()] + CARREGADOR_RUNNER + s[m.start():], ["G1.0: carregador _custodia_generica inserido"]


def runner_numeros(s):
    """vMM (runner) e vNN (pedra), lidos do próprio arquivo: cabeçalho e último comentário `# vNN (vMM): A CUSTODIA…`."""
    mm = _um(s, r'^"""FRONTEIRA TEORICA TGL v(\d+) — auto-auditoria', "cabeçalho do runner")
    ult, _ = _ultimo(s, r"^\s*# v(\d+) \(v(\d+)\): A CUSTODIA", "comentário da última pedra")
    return int(mm.group(1)), int(ult.group(1))


def runner_por_versao(s, v, ant, F, titulo_slug, sufixo_sem=None):
    """As onze trocas contadas (§6.7) do runner para a versão `v` (anterior `ant`), com os números de `F` (esquema 2). Devolve (texto, trocas)."""
    if "_medir_%s_custodia" % v in s:
        return s, ["%s já aplicado" % v]
    if "def _custodia_generica" not in s:
        raise Parar("G1.0 não instalado no runner (rode work\\custodia_G1\\patches\\instalar_g1_0.py depois que a custódia em curso terminar)")
    N, A = v[1:], ant[1:]
    mm, nn = runner_numeros(s)
    novo_mm, novo_nn = mm + 1, nn + 1
    trocas = []

    def sub(rx, rep, rot, esperado_ant=None, n=1):
        nonlocal s
        ms = list(re.finditer(rx, s, re.M))
        if len(ms) != n:
            raise Parar("âncora «%s» casou %d vez(es), esperado %d" % (rot, len(ms), n), [rx[:110]])
        if esperado_ant is not None and ms[0].group("ver") != esperado_ant:
            raise Parar("âncora «%s» capturou v%s, esperava v%s (o runner não está na versão anterior)" % (rot, ms[0].group("ver"), esperado_ant))
        s = s[:ms[0].start()] + ms[0].expand(rep) + s[ms[0].end():]
        trocas.append(rot)

    sub(r'^("""FRONTEIRA TEORICA TGL v)(\d+)( — auto-auditoria honesta do fechamento, SINCRONIZADA ao um\.py v)(\d+)(\.)$',
        r"\g<1>%d\g<3>%s\g<5>" % (novo_mm, N), "1 cabeçalho do runner")
    sub(r"^(  A custodia viva passou a ser vault/originals_copy/um_unificado_v)(\d+)(\. O RENOME v209: o selo.*)$", r"\g<1>%s\g<3>" % N, "2 docstring custódia")
    sub(r"(\()(\d+)( arquivos formais no manifesto v)(\d+)(; entre)", r"\g<1>%d\g<3>%s\g<5>" % (F["kernel"]["formais"], N), "3 docstring kernel")
    sub(r"(Fonte canonica sincronizada \(custodia\): um\.py unificado v)(\d+)( \(pin)", r"\g<1>%s\g<3>" % N, "4 docstring fonte")
    sub(r'^(CUSTODY_DIR = CENTRAL_DIR / "vault" / "originals_copy" / "um_unificado_v)(?P<ver>\d+)(")$', r"\g<1>%s\g<3>" % N, "5 CUSTODY_DIR", A)
    sub(r'(print\(f"\[fronteira v30\] CUSTODIA um\.py v)(?P<ver>\d+)(: pin)', r"\g<1>%s\g<3>" % N, "6 print custódia", A)
    stub = ('def _medir_%s_custodia():\n'
            '    """v%d (custodia %s, G1): o COFRE %s contra o COFRE %s, lidos PELO NOME (exata para sempre); expectativas congeladas em FATOS_CUSTODIA.json\n'
            '    do cofre %s (sha256 pinado no CUSTODY_MANIFEST) e a semantica revisada ao lado; DOIS CETICOS. physical_verdict_allowed=False."""\n'
            '    return _custodia_generica("%s", "%s")\n\n\n' % (v, novo_nn, v, v, ant, v, v, ant))
    m = _um(s, r"^def shadow_the_station\(core, selo\):$", "7 def shadow_the_station")
    s = s[:m.start()] + stub + s[m.start():]
    trocas.append("7 stub _medir_%s_custodia" % v)
    ult, n8 = _ultimo(s, r'^        "custodia_v(\d+)": _medir_v\1_custodia\(\),$', "8 entrada da pedra na station")
    s = s[:ult.end()] + '\n        "custodia_%s": _medir_%s_custodia(),' % (v, v) + s[ult.end():]
    trocas.append("8 entrada station (existentes: %d)" % n8)
    ult, n9 = _ultimo(s, r'^    v(\d+)_pass = station\["custodia_v(\d+)"\]\["pass"\]$', "9 vNN_pass")
    s = s[:ult.end()] + ('\n    # v%d (v%d): A CUSTODIA %s -- o cofre %s contra o %s, pelo nome (pedra generica G1); dois ceticos.\n    v%d_pass = station["custodia_%s"]["pass"]'
                         % (novo_nn, novo_mm, v, v, ant, novo_nn, v)) + s[ult.end():]
    trocas.append("9 vNN_pass (existentes: %d)" % n9)
    m = _um(s, r"(and v)(\d+)(_pass\))$", "10 all_pass")
    if int(m.group(2)) != nn:
        raise Parar("all_pass termina em v%s_pass, esperava v%d_pass" % (m.group(2), nn))
    s = s[:m.start()] + "and v%d_pass and v%d_pass)" % (nn, novo_nn) + s[m.end():]
    trocas.append("10 all_pass")
    m = _um(s, r'^        verdict = \("FRONTEIRA_SINCRONIZADA_V(\d+)"$', "11 veredito")
    if m.group(1) != A:
        raise Parar("o veredito está em V%s, esperava V%s" % (m.group(1), A))
    esc = F["escada"]["esperadas"]
    nbl = len(F["registros_novos"])
    reg = F["registro"]
    suf = sufixo_sem or "SEMANTICA_DECLARADA_SEM_REVISAO"
    seg = ("__V%s_%s__COFRE_V%s_CONTRA_O_V%s_PELO_NOME__%d_BLOCOS_NOVOS_VERIFICADOS_NENHUM_MOVE_O_GATE__%d_BANDEIRAS__ESCADA_%d_DE_%d_BANDEIRAS__KERNEL_%d_%d_NO_TRIO__%s"
           "__REGISTRO_%d_COM_OS_%d_DA_V%s_E_%d_MUDADOS_DITOS__DOIS_CETICOS__GATE_INALTERADO"
           % (N, titulo_slug, N, A, nbl, len(F["bandeiras_novas"]), esc, esc, F["kernel"]["formais"], F["kernel"]["declaracoes"], suf,
              reg["pt"], reg["anterior"], A, len(reg["mudados"])))
    nova = ('        verdict = ("FRONTEIRA_SINCRONIZADA_V%s"\n                   "%s"\n                   "__V%s"' % (N, seg, A))
    s = s[:m.start()] + nova + s[m.end():]
    trocas.append("11 veredito")
    return s, trocas


# =================================================================== MÓDULO COMUM DOS 16 DISPOSITIVOS
def formula_g1_0(s):
    if "CAMADAS_GENERICAS" in s:
        return s, ["G1.0 já aplicado"]
    trocas = []
    m = _um(s, r"^def conferir_no_cofre\(rt: dict\) -> dict:$", "def conferir_no_cofre")
    s = s[:m.start()] + CARREGADOR_FORMULA + s[m.start():]
    trocas.append("G1.0: CAMADAS_GENERICAS e o carregador")
    ult, n = _ultimo(s, r"^    v(\d+) = conferir_v\1_no_cofre\(core, selo\)\s+# camada v\1 \(item (\d+)\); fail-closed$", "chamadas das camadas", minimo=3)
    s = s[:ult.end()] + "\n    _genericas = _camadas_genericas(core, selo, cofre)     # camadas da custódia parametrizada (G1); fail-closed" + s[ult.end():]
    trocas.append("G1.0: chamada das camadas genéricas (camadas existentes: %d)" % n)
    m = _um(s, r'("camada_v(\d+)_no_cofre": v\2)\}$', "retorno de conferir_no_cofre")
    s = s[:m.start()] + m.group(1) + ", **_genericas}" + s[m.end():]
    trocas.append("G1.0: retorno inclui as camadas genéricas")
    return s, trocas


def formula_por_versao(s, v, ant, paragrafo, sufixo_veredito, nao_se_afirma, uso_chave, uso_rx):
    """Por versão (anchors 1,2,6,7,8,9 de §7.4). `paragrafo`/`nao_se_afirma`/`uso_*` vêm de textos (verbatim do core). Idempotente: a versão na tupla."""
    if re.search(r'^CAMADAS_GENERICAS = \(.*"%s".*\)$' % v, s, re.M):
        return s, ["%s já aplicado" % v]
    if "CAMADAS_GENERICAS" not in s:
        raise Parar("G1.0 não instalado no módulo dos 16 dispositivos (rode work\\custodia_G1\\patches\\instalar_g1_0.py)")
    trocas = []
    m = _um(s, r'^VERSAO_DA_CAMADA = "(v\d+)"(.*)$', "VERSAO_DA_CAMADA")
    if m.group(1) != ant:
        raise Parar("VERSAO_DA_CAMADA é %s, esperava %s" % (m.group(1), ant))
    s = s[:m.start()] + 'VERSAO_DA_CAMADA = "%s"   # (era "%s"; a camada %s é GENÉRICA — camada_generica.py lê o FATOS_CUSTODIA.json do cofre)' % (v, ant, v) + s[m.end():]
    trocas.append("1 VERSAO_DA_CAMADA")
    m = _um(s, r"^Régua: β NUNCA literal \(sempre ALPHA_FINE_CODATA_2018", "docstring: Régua")
    s = s[:m.start()] + paragrafo.rstrip("\n") + "\n\n" + s[m.start():]
    trocas.append("2 parágrafo da docstring")
    m = _um(s, r'"RECALCULADA_E_CONFERIDA_NO_COFRE__NOT_A_CONFIRMATION"\) % VERSAO_DA_CAMADA\.upper\(\),$', "sufixo do veredito")
    s = s[:m.start()] + '"%s"\n                     ' % sufixo_veredito + s[m.start():]
    trocas.append("6 sufixo do veredito")
    # a âncora de nao_se_afirma é o fim da lista, antes do `}` e do `if __name__` (ESPEC_CENTRAL §7.4, âncora 7)
    m = _um(s, r'\],\n    \}\n\n\nif __name__ == "__main__":', "fim de nao_se_afirma", flags=0)
    itens = "".join(',\n                          %s' % repr(x) for x in nao_se_afirma)
    s = s[:m.start()] + itens + s[m.start():]
    trocas.append("7 nao_se_afirma (%d itens)" % len(nao_se_afirma))
    m = _um(s, r"\n\}\n\n\ndef uso_no_dispositivo", "USOS", flags=0)
    s = s[:m.start()] + ('\n    # %s: mede se algum dispositivo cita as pedras novas; não interpreta\n    %r: %s,' % (v, uso_chave, uso_rx)) + s[m.start():]
    trocas.append("8 USOS")
    m = _um(s, r"^CAMADAS_GENERICAS = \((.*)\)$", "tupla CAMADAS_GENERICAS")
    atual = m.group(1).strip().rstrip(",").strip()      # 25/10/2026 (v401): ("v400",) + v401 dava ("v400",, "v401",)
    s = s[:m.start()] + "CAMADAS_GENERICAS = (%s\"%s\",)" % ((atual + ", ") if atual else "", v) + s[m.end():]
    trocas.append("9 CAMADAS_GENERICAS += %s" % v)
    return s, trocas


# =================================================================== aplicar em arquivo (backup de bytes, EOL, py_compile)
def aplicar_em_arquivo(caminho, f, rot, ts=None):
    """`f(texto_lf) -> (novo, trocas)`. Backup de BYTES `<arquivo>.bak_<rot>_<TS>`, respeita CRLF, py_compile no temporário, os.replace."""
    p = Path(caminho)
    s, eol, raw = util.ler_eol(p)
    novo, trocas = f(s)
    if novo == s:
        return {"estado": "ja_aplicado", "trocas": trocas}
    dados = util.para_eol(novo, eol).encode("utf-8")
    ok, msg = util.py_compile_bytes(dados, p.name)
    if not ok:
        raise Parar("SINTAXE INVÁLIDA — nada trocado em %s" % p.name, [msg])
    ts = ts or util.carimbo()
    bak = p.with_name("%s.bak_%s_%s" % (p.name, rot, ts))
    with open(util.lp(bak), "wb") as g:
        g.write(raw)
    tmp = p.with_name(p.name + ".tmp_" + rot)
    with open(util.lp(tmp), "wb") as g:
        g.write(dados)
    if os.path.getsize(util.lp(tmp)) != len(dados) or len(dados) <= len(raw):
        os.remove(util.lp(tmp))
        raise Parar("o arquivo não cresceu ou o temporário saiu errado: %s" % p.name)
    os.replace(util.lp(tmp), util.lp(p))
    return {"estado": "aplicado", "antes": len(raw), "depois": len(dados), "backup": bak.name, "trocas": trocas}
