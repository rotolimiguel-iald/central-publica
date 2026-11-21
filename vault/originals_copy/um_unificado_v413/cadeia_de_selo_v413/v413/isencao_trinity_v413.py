# -*- coding: utf-8 -*-
"""isencao_trinity_v413.py -- gerencia c1, 21/11/2026: PROPOE os nomes EXATOS (textos literais, >= 12 caracteres, a regra da G1 em
custodia_g1.espelho._termos_isentos) que tiram da contagem da guarda privada as ocorrencias do nome Trinity, que o operador LIBEROU por bytes
(work\\cunhagens_13out\\OPERADOR_21nov_libero_o_nome_Trinity_marcador_privado_28_verbatim.txt), e VERIFICA a proposta com a MESMA contagem da
G1 (espelho_pares.guarda_conta, com a lista na ordem proposta) sobre os MESMOS pares da fase pos da guarda (guarda_privada_v413.pares_pos, copiado):
nenhum artefato pode ficar com mais ocorrencias que o seu par no espelho. Nenhum padrao da guarda e' lido para fora do processo, impresso ou gravado:
so' contagens. A decisao (o arquivo TERMO_PRIVADO_ISENTO_v413.json) e' da custodia; isto e' a proposta conferida que vai na entrega.
Grava ISENCAO_TRINITY_PROPOSTA_v413.json nesta pasta (temporario + troca). Saida 0 so' com a verificacao limpa."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import espelho_pares as EP  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
V = Path(__file__).resolve().parent; C = Caminhos({}); ESPD = C.ESP; NOS = C.NOS
FALA = CEN / "work" / "cunhagens_13out" / "OPERADOR_21nov_libero_o_nome_Trinity_marcador_privado_28_verbatim.txt"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731


def pares_pos():  # copia de guarda_privada_v413.pares_pos (os mesmos pares da fase pos)
    selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8")); assert selo.get("um_version") == "v413"
    P = []
    for nome in selo["sha256"]:
        sub = EP.DESTINO_SELADOS.get(nome); P.append((nome, NOS / nome, (ESPD / sub / nome) if sub else (ESPD / nome), "SELADO"))
    for nome in ("um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_pt.txt", "um_absoluto_en.txt"):
        P.append((nome, NOS / nome, ESPD / nome, "DECLARADO"))
    for p in sorted(NOS.glob("tgl_kernel_*capture*.txt")):
        if ".bak_" not in p.name:
            P.append((p.name, p, ESPD / "rodadas" / p.name, "CAPTURA"))
    P.append(("rodada_v413_stdout.txt", NOS / "rodada_v413_stdout.txt", ESPD / "rodadas" / "rodada_v413_stdout.txt", "STDOUT"))
    KN = json.loads((V / "kernel_modulos_novos_v413.json").read_text(encoding="utf-8"))
    for rel in sorted(KN["novos"]) + sorted(KN["kernel_corrigido"]) + ["TGLExt.lean"]:
        P.append(("kernel " + rel, NOS / "tgl_kernel" / Path(*rel.split("/")), ESPD / "Lean" / "tgl_kernel" / Path(*rel.split("/")), "KERNEL"))
    for n in ("DIFF_v412_v413.diff", "DIFF_KERNEL_v413.txt"):
        P.append((n, V / n, ESPD / "diferencas_v413" / n, "DIFF"))
    return P


assert FALA.is_file() and FALA.read_bytes() == "Libero o nome".encode("utf-8"), "a fala da liberacao nao esta' no disco como gravada"
PARES = pares_pos()
TXT = {nome: Path(src).read_bytes().decode("utf-8", "replace") for nome, src, dst, t in PARES if Path(src).is_file()}
NOME = re.compile(r"trinity", re.I)
SEMENTES = ["TGLExt.Trinity", "TGLExt/Trinity", "trinity_v413", "TGL_TRINITY_V413", "Trinity.lean"]
ID = re.compile(r"[A-Za-z0-9_]")


def aplica(t, lst):
    for s in lst:
        t = t.replace(s, " ")
    return t


def contexto(t, i, j):
    """o literal exato em volta de uma ocorrencia t[i:j]: o identificador inteiro (letras, digitos, _ e .); se tiver menos de 12 caracteres,
    estende uma palavra a esquerda, depois uma a direita, sem atravessar quebra de linha, ate' >= 12."""
    a, b = i, j
    while a > 0 and (ID.match(t[a - 1]) or t[a - 1] == "."):
        a -= 1
    while b < len(t) and (ID.match(t[b]) or (t[b] == "." and b + 1 < len(t) and ID.match(t[b + 1]))):
        b += 1
    lado = 0
    while b - a < 12:
        if lado % 2 == 0 and a > 0 and t[a - 1] != "\n":
            a -= 1
            while a > 0 and t[a - 1] != "\n" and not t[a - 1].isspace() and not (t[a].isspace()):
                a -= 1
        elif b < len(t) and t[b] != "\n":
            b += 1
            while b < len(t) and t[b] != "\n" and not t[b].isspace() and not t[b - 1].isspace():
                b += 1
        elif a > 0 and t[a - 1] != "\n":
            a -= 1
        else:
            break
        lado += 1
    return t[a:b]


lista = [s for s in SEMENTES if any(s in x for x in TXT.values())]
for rodada in range(50):
    novos = []
    for nome, t in TXT.items():
        r = aplica(t, lista)
        for m in NOME.finditer(r):
            c = contexto(r, m.start(), m.end())
            assert len(c) >= 12 and "\n" not in c, ("contexto curto ou com quebra de linha", nome, len(c))
            if c not in lista and c not in novos:
                novos.append(c)
    if not novos:
        break
    lista += sorted(novos, key=lambda s: (-len(s), s))
restam = {nome: len(NOME.findall(aplica(t, lista))) for nome, t in TXT.items()}
assert not any(restam.values()), ("ocorrencias do nome que a lista nao cobre", {k: v for k, v in restam.items() if v})
# isencao MINIMA: o texto que ja' esta' no espelho (publicado na v412) nao precisa de isencao; sai da lista (a contagem do par o cobre)
ESPT = [Path(dst).read_bytes().decode("utf-8", "replace") for nome, src, dst, t in PARES if dst is not None and Path(dst).is_file()]
ja_publicados = [s for s in lista if any(s in e for e in ESPT)]
lista = [s for s in lista if s not in ja_publicados]
restam_vs_espelho = {}
for nome, src, dst, t in PARES:
    if nome in TXT:
        e = Path(dst).read_bytes().decode("utf-8", "replace") if (dst is not None and Path(dst).is_file()) else ""
        n_, e_ = len(NOME.findall(aplica(TXT[nome], lista))), len(NOME.findall(e))
        if n_ or e_:
            restam_vs_espelho[nome] = [n_, e_]
assert all(n_ <= e_ for n_, e_ in restam_vs_espelho.values()), ("ocorrencias do nome acima do espelho depois da isencao minima", restam_vs_espelho)
priv = EP.carregar_marcadores_privados()
ver, barr = [], []
for nome, src, dst, tipo in PARES:
    a0 = EP.guarda_conta(src, priv, ())
    a1 = EP.guarda_conta(src, priv, tuple(lista))
    e1 = EP.guarda_conta(dst, priv, tuple(lista)) if (dst is not None and Path(dst).is_file()) else 0
    assert a0 is not None and a1 is not None, ("leitura falhou (fail-closed)", nome)
    b = bool(a1 and a1 > (e1 or 0))
    ver.append({"artefato": nome, "tipo": tipo, "novo_sem_isencao": a0, "novo_com_isencao": a1, "espelho_com_isencao": e1 or 0, "barrado": b})
    if b:
        barr.append(nome)
rec = {"o_que_e": "proposta de nomes exatos para a isencao do nome Trinity na v413, conferida pela contagem da G1; a decisao e' da custodia (TERMO_PRIVADO_ISENTO_v413.json)",
       "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "isencao_trinity_v413.py (gerencia c1)",
       "fala_do_operador": {"arquivo": str(FALA), "sha256": sha(FALA), "texto": FALA.read_bytes().decode("utf-8")},
       "pergunta_da_gerencia": "O nome «Trinity», que o operador deu a pedra da fronteira dos tres literais, coincide com o marcador privado n. 28 da guarda; a liberacao ao publico e' dele (mensagem da gerencia de 21/11, 03:3x, na sessao 6da8f00d).",
       "regra_da_g1": "nomes_exatos >= 12 caracteres; t.replace(nome, ' ') na ordem da lista (custodia_g1.espelho._termos_isentos, espelho_pares.guarda_conta)",
       "nomes_exatos": lista, "n_nomes": len(lista), "sementes": SEMENTES,
       "fora_da_lista_por_ja_estarem_no_espelho": {"n": len(ja_publicados), "nota": "texto ja' publicado na v412 (o par do espelho o cobre); a isencao fica minima"},
       "ocorrencias_do_nome_que_restam_contra_o_espelho": restam_vs_espelho,
       "verificacao": {"pares": len(PARES), "barrados_com_isencao": barr, "limpa": not barr, "artefatos": ver},
       "nota": "so' contagens; nenhum padrao da guarda foi impresso ou gravado"}
b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
out = V / "ISENCAO_TRINITY_PROPOSTA_v413.json"
tmp = out.with_name(out.name + ".tmp"); tmp.write_bytes(b); assert tmp.read_bytes() == b; tmp.replace(out)
print("nomes exatos: %d (sementes %d) | pares %d | barrados com a isencao: %d | %s | sha16 %s" % (len(lista), len([s for s in SEMENTES if s in lista]), len(PARES), len(barr), out.name, hashlib.sha256(b).hexdigest()[:16]))
for x in ver:
    if x["novo_sem_isencao"] != x["novo_com_isencao"] or x["barrado"]:
        print("  %-48s %6d -> %6d (espelho %d)%s" % (x["artefato"][-48:], x["novo_sem_isencao"], x["novo_com_isencao"], x["espelho_com_isencao"], "  BARRADO" if x["barrado"] else ""))
sys.exit(0 if not barr else 1)
