# -*- coding: utf-8 -*-
"""custodiar.py — UMA ordem por versão: a CUSTÓDIA de uma versão selada do um.py, parametrizada por vNNN (G1 do organismo da IALD, 24/10/2026).

Regra do operador de 23/10/2026: «pode custodiar sempre que o handoff aparecer, como regra». As TRÊS MARCAS que disparam: (1) o selo do Nós com
`um_version` novo e o `um.py` batendo com o pino; (2) o bloco «vNNN SELADA» no diário; (3) HANDOFF_vNNN_CUSTODIA.md + rodada_vNNN_stdout.txt.

  vigiar     lê o Nós e diz se as três marcas de uma versão estão presentes e o que já foi custodiado (idempotente; só leitura). `--gravar` (MODO SOMBRA) também escreve
             work\\custodia_G1\\VIGIA_ULTIMO.json (versão vista, marcas, código, plano resumido, hora) e VIGIA_ULTIMO.txt (chave=valor, para o .bat); sai com os códigos abaixo.
             `tools\\custodia_g1\\vigia.bat` o roda e, se a versão do selo tem as três marcas, grava o plano em work\\custodia_G1\\PLANO_vNNN.json — nunca executa, nunca publica.
  sondar     os FATOS (esquema 2) lidos do selo, do core, do manifesto, do um.py e do cofre anterior; grava fatos_vNNN.json.
  planejar   cada passo das quatro pernas com a marca de «já aplicado» e o que FALTA; --seco = nada é escrito, nem em work\\.
  executar   roda as pernas na ordem, com gates (para na primeira falha; nunca prossegue com hash divergente). Ato para fora (commit, push, subida
             do site, Central pública, ACOM) só com --publicar. --ensaio = nada é gravado.
  auditar    os números citados nas superfícies e o rótulo do Teste da Única Palavra (L03/L04); só leitura.

Códigos de saída: 0 completo (nada a fazer E nenhuma decisão do operador aberta) · 1 pendente (pronto para custodiar ou para publicar) ·
5 G1 terminou o que lhe cabe, mas há decisões do OPERADOR abertas (listadas) · 10 WAIT (Nós em obra, trava recente) ·
20 STOP (falta insumo, âncora ou gate; passo BLOQUEADO; a lista vai impressa) · 30 falha de leitura (git, arquivo, recibo) · 40 divergência do ar/GitHub.
«Superado só pela relação» (SUPERADO_REL) conta como nada a fazer, mas vai DITO: G1 não tem artefato que o prove (versão histórica).
Nunca passa --force, --sem-guarda nem --permitir-ftp-em-claro; nunca lê credencial; nunca mata processo por nome."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

from custodia_g1 import fatos, motor, nos, util  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
from custodia_g1.util import G1Erro, FalhaLeitura  # noqa: E402


def _caminhos(a):
    sobre = {}
    for r in a.raiz or []:
        k, _, v = r.partition("=")
        if not v:
            raise SystemExit("--raiz espera NOME=CAMINHO (ex.: NOS=C:\\x)")
        sobre[k.strip().upper()] = v
    return Caminhos(sobre)


def _ctx(a, publicar=False):
    c = _caminhos(a)
    return motor.Ctx(c=c, versao=a.versao, data=getattr(a, "data", None), sessao=getattr(a, "sessao", None), ordem=getattr(a, "ordem", None),
                     coautor=getattr(a, "coautor", None), rede=bool(getattr(a, "rede", False) or publicar), publicar=publicar, ensaio=getattr(a, "ensaio", False),
                     aceitar_molde=getattr(a, "aceitar_molde", False), saida=getattr(a, "saida", None), anterior=getattr(a, "anterior", None), ator=getattr(a, "ator", None),
                     trabalho=getattr(a, "trabalho", None))


def _imprimir_plano(p):
    print("PLANO %s — %s; espelho %s" % (p["versao"], "corrente (selo do Nós)" if p["corrente"] else "HISTÓRICA (o Nós já selou outra)", p["relacao_espelho"]))
    for i in p["itens"]:
        marca = {"APLICADO": "ok  ", "SUPERADO": "sup ", "SUPERADO_REL": "rel ", "NA": "n/a ", "OPERADOR": "oper", "BLOQUEADO": "BLOQ"}.get(i["estado"], "FALT" if i["estado"] == "FALTA" else i["estado"][:4])
        print("  %-5s %s %-62s %s" % (i["id"], marca, i["passo"][:62], i["detalhe"][:110] + (" [para fora]" if i["externo"] and i["estado"] not in ("APLICADO", "SUPERADO", "SUPERADO_REL") else "")))
    print("  contagem:", ", ".join("%s %d" % (k, n) for k, n in sorted(p["contagem"].items())))
    if p["nada_a_fazer"]:
        rel = p.get("superados_por_relacao") or []
        provados = sum(n for k, n in p["contagem"].items() if k in ("APLICADO", "SUPERADO", "NA"))
        print("NADA A FAZER: todos os passos aplicados ou superados (provados no artefato: %d%s)." % (
            provados, ("; superados SÓ pela relação histórica, que G1 não prova: %d" % len(rel)) if rel else ""))
        if rel:
            print("   ressalva: os passos %s estão «rel» — a versão é histórica e a superfície é regerada a cada versão; G1 não tem artefato que os prove" % ", ".join(rel))
    else:
        print("FALTAM %d passo(s): %s" % (len(p["pendentes"]), ", ".join(p["pendentes"])))
        if p.get("falha_de_leitura"):
            print("FALHA DE LEITURA em: %s (G1 não decide por marca ilegível: código 30)" % ", ".join(p["falha_de_leitura"]))
        para = p.get("executar_para_em")
        if para:
            print("EXECUTAR PARARIA EM %s (BLOQUEADO): %s" % (para["id"], para["motivo"][:300]))
            if p.get("atras_do_bloqueio"):
                print("   atrás dele, sem rodar enquanto isso durar: %s (use --so ID para o que não depende dele; cada passo confere a sua pré-condição)" % ", ".join(p["atras_do_bloqueio"]))
        t = p.get("textos") or {}
        if t:
            print("TEXTOS (só o que os passos pendentes consomem): %s" % (", ".join(t.get("necessarios") or []) or "nenhum passo pendente precisa de prosa nova"))
            print("  parágrafos prontos no handoff:", ", ".join(t.get("paragrafos_prontos") or ["(nenhum)"]), "| marcadores opcionais presentes:", ", ".join(t.get("do_handoff") or ["(nenhum)"]))
            if t.get("faltam"):
                print("  PARAR: faltam os marcadores abaixo (sem eles a prosa sairia do MOLDE FACTUAL; passe --aceitar-molde ou peça ao autor do handoff):")
                for x in t["faltam"]:
                    print("     - %s" % x)
            for b in t.get("bloqueios") or []:
                print("  BLOQUEIO: %s" % b)
    decs = p.get("decisoes_do_operador") or []
    if decs:
        print("DECISÕES DO OPERADOR ABERTAS (%d) — G1 não as toma%s:" % (len(decs), "; nada mais falta: código %d" % util.COD_OPERADOR if p["nada_a_fazer"] and not p.get("bloqueados") else ""))
        for d in decs:
            print("   - [%s] %s" % (d["origem"], d["texto"][:360]))
            if d.get("nota"):
                print("       (%s)" % d["nota"])


def _sem_hora(d):
    return {k: x for k, x in d.items() if k != "hora"}


def gravar_vigia(pasta, saida):
    """`vigiar --gravar` (MODO SOMBRA): VIGIA_ULTIMO.json (o registro: versão vista, marcas, código, plano resumido, hora) e VIGIA_ULTIMO.txt (chave=valor, a vista que o .bat lê sem
    analisar JSON). Escrita atômica (temporário -> conferir -> substituir). O backup de BYTES do JSON anterior só quando o conteúdo MUDOU (fora a hora): o vigia roda de tempos em tempos e
    uma cópia por rodada, com o mesmo conteúdo, só encheria a pasta; o .txt é a vista derivada do JSON (regenerável). Falha de escrita é FalhaLeitura (30), nunca silêncio."""
    pasta = Path(pasta)
    try:
        pasta.mkdir(parents=True, exist_ok=True)
        alvo = pasta / "VIGIA_ULTIMO.json"
        mudou = True
        if alvo.is_file():
            try:
                mudou = _sem_hora(json.loads(alvo.read_text(encoding="utf-8"))) != _sem_hora(saida)
            except (ValueError, OSError):
                mudou = True
        util.escrever_atomico(alvo, json.dumps(saida, ensure_ascii=False, indent=1).encode("utf-8"), backup=mudou)
        linhas = ["versao=%s" % saida.get("versao"), "selo=%s" % saida.get("selo"), "marcas=%s" % saida.get("marcas"), "codigo=%s" % saida.get("codigo"),
                  "estado=%s" % str(saida.get("estado", "")).split(" \u2014 ")[0].strip(), "hora=%s" % saida.get("hora")]
        util.escrever_atomico(pasta / "VIGIA_ULTIMO.txt", ("\n".join(linhas) + "\n").encode("utf-8"), backup=False)
    except OSError as e:
        raise FalhaLeitura("não gravei o VIGIA_ULTIMO em %s: %r" % (pasta, e))
    return alvo


def cmd_vigiar(a):
    c = _caminhos(a)
    selo = nos.selo(c)
    v = a.versao or selo["um_version"]
    m = nos.marcas(c, v)
    linhas = ["Nós: selo %s %s (%s) | três marcas de %s: %s" % (selo["um_version"], selo["sha256"]["um.py"][:16], selo.get("timestamp"), v, m.estado)]
    linhas += ["   falta: %s" % x for x in m.faltam]
    if m.em_obra_versoes:
        linhas.append("Em obra no Nós (pasta em cadeia_de_selo sem selo): %s — a custódia dela espera o selo." % ", ".join(m.em_obra_versoes))
    saida = {"esquema": "custodia_vigia/1", "modo": "SOMBRA: vigiar só lê; nada é executado nem publicado", "versao": v, "selo": selo["um_version"], "marcas": m.estado,
             "faltam": m.faltam, "em_obra": m.em_obra_versoes}

    def fim(codigo, estado):
        saida["estado"] = estado
        saida["codigo"] = codigo
        saida["hora"] = util.agora_iso()
        if a.json:
            print(json.dumps(saida, ensure_ascii=False, indent=1))          # --json: SÓ o JSON (para quem agenda o vigia)
        else:
            print("\n".join(linhas))
            print("ESTADO: " + estado)
        if a.gravar:
            f = gravar_vigia(Path(a.saida) if a.saida else c.G1, saida)
            if not a.json:
                print("VIGIA_ULTIMO gravado em %s" % f)
        return codigo
    if m.estado == "EM_OBRA":
        return fim(util.COD_WAIT, "EM_OBRA (WAIT)")
    if m.estado == "INCOMPLETA":
        return fim(util.COD_STOP, "INCOMPLETA (STOP) — o handoff/stdout/diário/cadeia ainda não estão todos")
    ctx = motor.Ctx(c=c, versao=v, rede=a.rede)
    p = motor.planejar(ctx)
    n_ok = sum(1 for i in p["itens"] if i["estado"] in ("APLICADO", "SUPERADO", "SUPERADO_REL", "NA"))
    n_op = sum(1 for i in p["itens"] if i["estado"] == "OPERADOR")
    linhas.append("Plano de %s: %d de %d passos aplicados ou superados%s; pendentes: %s" % (v, n_ok, len(p["itens"]), (" (+%d do operador, à parte)" % n_op) if n_op else "",
                                                                                         ", ".join(p["pendentes"]) or "nenhum"))
    if p.get("superados_por_relacao"):
        linhas.append("Superados SÓ pela relação histórica (G1 não os prova): %s" % ", ".join(p["superados_por_relacao"]))
    for d in p.get("decisoes_do_operador") or []:
        linhas.append("DECISÃO DO OPERADOR ABERTA: [%s] %s" % (d["origem"], d["texto"][:200]))
    saida["plano"] = {"aplicados_ou_superados": n_ok, "total": len(p["itens"]), "pendentes": p["pendentes"], "pendentes_do_operador": p.get("pendentes_do_operador"),
                      "decisoes_do_operador": [dict(d, texto=str(d.get("texto", ""))[:400]) for d in (p.get("decisoes_do_operador") or [])], "bloqueados": p.get("bloqueados"),
                      "falha_de_leitura": p.get("falha_de_leitura"),
                      "superados_por_relacao": p.get("superados_por_relacao"), "provado_no_artefato": p.get("provado_no_artefato"), "completo": p.get("completo"),
                      "texto_bloqueia": p.get("texto_bloqueia")}
    cod = motor.codigo_do_plano(p)
    if cod == util.COD_LEITURA:
        return fim(cod, "FALHA DE LEITURA (%s) — G1 não decide por marca ilegível" % ", ".join(p["falha_de_leitura"]))
    if cod == util.COD_STOP:
        return fim(cod, "BLOQUEADA (STOP) — %s" % (", ".join(p.get("bloqueados") or []) or "falta fonte de texto"))
    if cod == util.COD_PENDENTE:
        return fim(cod, "PENDENTE — pronta para `custodiar.py planejar --versao %s --seco` e `executar`" % v)
    if cod == util.COD_OPERADOR:
        return fim(cod, "CUSTODIADA POR G1 (nada a fazer) — %d decisão(ões) do operador abertas" % len(p["decisoes_do_operador"]))
    return fim(cod, "CUSTODIADA (nada a fazer)")


def cmd_sondar(a):
    c = _caminhos(a)
    ctx = motor.Ctx(c=c, versao=a.versao, anterior=a.anterior, saida=a.saida, data=a.data)
    F = fatos.sondar(c, ctx.versao, anterior=a.anterior, fonte=a.fonte)
    saida = Path(a.saida) if a.saida else ctx.W
    saida.mkdir(parents=True, exist_ok=True)
    alvo = saida / ("fatos_%s.json" % ctx.versao)
    texto = json.dumps(F, ensure_ascii=False, indent=1)
    if alvo.exists():
        if alvo.read_text(encoding="utf-8") == texto:
            print("fatos idênticos ao já gravado: %s" % alvo)
        else:
            alvo = saida / ("fatos_%s.g1_%s.json" % (ctx.versao, util.carimbo()))
            alvo.write_text(texto, encoding="utf-8")
            print("já existia um fatos_%s.json DIFERENTE (nada se sobrescreve): gravei ao lado, %s" % (ctx.versao, alvo))
    else:
        alvo.write_text(texto, encoding="utf-8")
        print("fatos gravados:", alvo)
    print("%s contra %s (fonte %s) | pin16 %s | escada %s -> %s | kernel %d/%d (+%s) | bandeiras novas %d | registros novos %s" % (
        F["versao"], F["anterior"], F["fonte"], F["pin16"], F["escada_anterior"]["texto"], F["escada"]["texto"], F["kernel"]["formais"], F["kernel"]["declaracoes"],
        ",".join(F["kernel"]["modulos_novos"]) or "-", len(F["bandeiras_novas"]), ",".join(F["registros_novos"])))
    h = F["handoff"]
    print("handoff:", "cruzado com os fatos: OK" if h.get("ok") else ("DIVERGE: %s" % h.get("divergencias") if h.get("presente") else "ausente"))
    return util.COD_OK if (h.get("ok") or not h.get("presente")) else util.COD_STOP


def cmd_planejar(a):
    ctx = _ctx(a)
    m = nos.marcas(ctx.c, ctx.versao)
    if m.estado == "EM_OBRA":            # versão ainda não selada (ou um.py != pino): marcas de uma versão sem dados dariam «ok» falsos (E12, C5) — fail-closed, como o vigia
        if a.json:
            print(json.dumps({"versao": ctx.versao, "estado": "EM_OBRA", "faltam": m.faltam, "codigo": util.COD_WAIT}, ensure_ascii=False, indent=1))
        else:
            print("EM_OBRA (WAIT): %s ainda não está selada no Nós (ou o um.py não é o do selo); o plano espera o selo." % ctx.versao)
            for x in m.faltam:
                print("   falta: %s" % x)
        return util.COD_WAIT
    p = motor.planejar(ctx, so=a.so, ate=a.ate)
    if a.json:
        print(json.dumps(p, ensure_ascii=False, indent=1))
    else:
        _imprimir_plano(p)
    if not a.seco:
        alvo = Path(a.saida) if a.saida else ctx.c.RUNS
        alvo.mkdir(parents=True, exist_ok=True)
        f = alvo / ("PLANO_%s_%s.json" % (ctx.versao, util.carimbo()))
        f.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
        print("plano gravado em", f)
    return motor.codigo_do_plano(p)


def cmd_executar(a):
    ctx = _ctx(a, publicar=a.publicar)
    print("EXECUTAR %s%s%s" % (ctx.versao, " [ENSAIO: nada é gravado]" if a.ensaio else "", " [--publicar: atos para fora LIGADOS]" if a.publicar else " [sem --publicar: para antes do primeiro ato para fora]"))
    codigo, rel = motor.executar(ctx, so=a.so, ate=a.ate)
    print("código de saída:", codigo, "| recibos em" if ctx.run_dir else "| ensaio: nada foi gravado (nem recibo, nem RELATORIO.json)", ctx.run_dir or "")
    for av in ctx.avisos:
        print("aviso:", av)
    return codigo


def cmd_auditar(a):
    from custodia_g1 import espelho
    ctx = _ctx(a)
    d = espelho.auditar_numeros_citados(ctx)
    l3 = espelho.rotulo_do_teste_no_readme(ctx)
    for x in d:
        print("DEFASADO: %s cita %s = %d bytes; o real é %d" % (x["superficie"], x["arquivo"], x["citado"], x["real"]))
    for x in l3:
        print("RÓTULO:", x)
    print("%d número(s) citado(s) defasado(s); %d rótulo(s) errado(s)" % (len(d), len(l3)))
    return util.COD_OK if not (d or l3) else util.COD_STOP


def cmd_guardar_plano(a):
    """Subcomando oculto do vigia.bat: valida a saída de `planejar --versao vN --seco --json` (JSON legível, é o plano de vN, traz os itens) e a guarda em --para por escrita
    atômica; se o plano guardado já é IDÊNTICO, não toca no arquivo; se mudou, backup de BYTES antes. Saída que não é o plano NÃO sobrescreve o plano anterior (30)."""
    de, para = Path(a.de), Path(a.para)
    try:
        d = json.loads(de.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise FalhaLeitura("a saída do planejar não é um JSON legível (%s): %r" % (de, e))
    if not isinstance(d, dict) or d.get("versao") != a.versao or not isinstance(d.get("itens"), list):
        raise FalhaLeitura("a saída do planejar não é o plano de %s (versao=%r, itens=%s): o plano guardado não foi tocado" % (
            a.versao, d.get("versao") if isinstance(d, dict) else None, type(d.get("itens")).__name__ if isinstance(d, dict) else "-"))
    mudou = True
    if para.is_file():
        try:
            mudou = json.loads(para.read_text(encoding="utf-8")) != d
        except (ValueError, OSError):
            mudou = True
    if not mudou:
        print("plano de %s idêntico ao já guardado em %s: nada escrito" % (a.versao, para))
        return util.COD_OK
    try:
        para.parent.mkdir(parents=True, exist_ok=True)
        util.escrever_atomico(para, json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8"), backup=True)
    except OSError as e:
        raise FalhaLeitura("não guardei o plano em %s: %r" % (para, e))
    print("plano de %s guardado em %s (%d itens; pendentes: %s)" % (a.versao, para, len(d["itens"]), ", ".join(d.get("pendentes") or []) or "nenhum"))
    return util.COD_OK


def cmd_snapshot(a):
    from custodia_g1 import central
    c = _caminhos(a)
    nome = central.snapshot_incremental(c)
    print("snapshot concluído:", nome)
    return util.COD_OK


def main(argv=None):
    pai = argparse.ArgumentParser(add_help=False)
    pai.add_argument("--raiz", action="append", help="troca uma raiz (NOS, TB, BANC, SITE, CEN, BK, ...): NOME=CAMINHO (ensaios e replays)")
    ap = argparse.ArgumentParser(prog="custodiar.py", description=__doc__.split("\n")[0], parents=[pai])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comum(p, versao_obrigatoria=False):
        p.add_argument("--versao", required=versao_obrigatoria, help="vNNN (padrão: a do selo do Nós)")
        p.add_argument("--data", help="dd/mm/aaaa da custódia (padrão: hoje)")
        p.add_argument("--sessao", help="rótulo da sessão nos textos (padrão: a7)")
        p.add_argument("--ator", help="id honesto de quem executa (ACOM, rota)")
        p.add_argument("--ordem", help="arquivo verbatim da ordem do operador (padrão: a regra permanente de 23/10)")
        p.add_argument("--coautor", help='trailer «Co-Authored-By» dos commits (G1 não o inventa): "Nome <email>"')
        p.add_argument("--rede", action="store_true", help="marcas que dependem do ar/GitHub leem a rede (padrão: o último quadro)")
        p.add_argument("--trabalho", help="pasta de trabalho da versão (padrão: work\\custodia_vNNN_<ddmes>; ensaios usam outra para não escrever na de outra sessão)")

    p = sub.add_parser("vigiar", parents=[pai]); comum(p); p.add_argument("--json", action="store_true")
    p.add_argument("--gravar", action="store_true", help="MODO SOMBRA: grava VIGIA_ULTIMO.json e .txt (versão vista, marcas, código, plano resumido, hora); não executa nada")
    p.add_argument("--saida", help="pasta de VIGIA_ULTIMO.* (padrão: work\\custodia_G1)"); p.set_defaults(f=cmd_vigiar)
    p = sub.add_parser("sondar", parents=[pai]); comum(p, True); p.add_argument("--anterior"); p.add_argument("--saida"); p.add_argument("--fonte", choices=("nos", "cofre")); p.set_defaults(f=cmd_sondar)
    p = sub.add_parser("planejar", parents=[pai]); comum(p, True)
    p.add_argument("--seco", action="store_true", help="nada é escrito, nem em work\\"); p.add_argument("--json", action="store_true")
    p.add_argument("--so"); p.add_argument("--ate"); p.add_argument("--saida"); p.add_argument("--aceitar-molde", action="store_true"); p.set_defaults(f=cmd_planejar)
    p = sub.add_parser("executar", parents=[pai]); comum(p, True)
    p.add_argument("--publicar", action="store_true", help="liga os atos PARA FORA: commit, push, subida do site, Central pública, ACOM")
    p.add_argument("--ensaio", action="store_true", help="nada é gravado: lista o que faria")
    p.add_argument("--so"); p.add_argument("--ate"); p.add_argument("--aceitar-molde", action="store_true", help="aceita o molde factual onde o handoff não traz o marcador")
    p.set_defaults(f=cmd_executar)
    p = sub.add_parser("auditar", parents=[pai]); comum(p, True); p.set_defaults(f=cmd_auditar)
    p = sub.add_parser("_snapshot", parents=[pai]); p.set_defaults(f=cmd_snapshot)
    p = sub.add_parser("_guardar_plano", parents=[pai]); p.add_argument("--de", required=True); p.add_argument("--para", required=True); p.add_argument("--versao", required=True)
    p.set_defaults(f=cmd_guardar_plano)
    a = ap.parse_args(argv)
    if getattr(a, "trabalho", None):              # 25/10/2026: --trabalho relativo quebrou o commit do E10 — sempre absoluto
        a.trabalho = str(Path(a.trabalho).resolve())
    try:
        return a.f(a)
    except G1Erro as e:
        alvo = sys.stderr if getattr(a, "json", False) else sys.stdout          # com --json o stdout é SÓ o JSON (quem redireciona para um arquivo não grava a mensagem de erro dentro dele)
        print("%s: %s" % (type(e).__name__.upper(), e.motivo), file=alvo)
        for x in e.faltam:
            print("   - %s" % x, file=alvo)
        return e.codigo


if __name__ == "__main__":
    sys.exit(main())
