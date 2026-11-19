# -*- coding: utf-8 -*-
"""adendo_desenho_v412.py -- (gerencia c1, 19/11/2026; A REGRA DA LINHAGEM COMPLETA) o ADENDO «v412 SELADA» do DESENHO_DO_FECHAMENTO_QG.md do Nos,
no molde dos adendos da v410 e da v411: acrescimo ao fim, backup de BYTES antes, temporario, conferencia de que cresceu. Numeros LIDOS do selo, do
core, dos ESPERADOS e do conferidor. Recusa se o adendo ja' existe. Uso: adendo_desenho_v412.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
ESP = lj(V / "ESPERADOS_v412.json"); CF = lj(V / "CONFERENCIA_POS_RITO_v412_FOCO.json"); selo = lj(NOS / "um_absoluto_selo.json")
core = lj(NOS / "um_absoluto.json")["core"]
assert CF["ok"] is True and selo["um_version"] == "v412" and selo["sha256"]["um.py"] == sha(NOS / "um.py")
U16 = sha(NOS / "um.py")[:16]; A_, B_ = ESP["escada"]; NMOD = ESP["kernel"]["modulos_novos"]; NB = ESP["n_bandeiras_novas"]
KH = core["kh_n1_cobertura_v411"]["lido"]; KHC, KHT = KH["constantes_cobertas"], KH["teoremas_cobertos"]
kf = core.get("kernel_formalization") or {}; NLIG = sum(1 for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_")) and x is True)
NAPA = sum(1 for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_")) and x is False)
HOJE = time.strftime("%d/%m/%Y")
T = ["", "## ADENDO — %s · v412 SELADA (COMPLETA) `%s` — A camada científica, a matemática que restava e o leitor da fórmula: %d módulos novos no kernel, "
     "escada %d → %d, a página pública aprovada pelo autor" % (HOJE, U16, NMOD, A_, B_), "",
     "<!-- adendo_v412_selada -->",
     "- **O que a v412 diz:** P = nP é teorema da TGL nas classes do seu dicionário: o custo polinomial está demonstrado na máquina da teoria, pela lei do "
     "custo; contado letra por letra na máquina de fita, vale para classes de fórmulas e não está demonstrado para a fórmula plana arbitrária. A camada "
     "científica (o leitor que pousa e retorna tem teorema; que um modelo de linguagem seja esse leitor é hipótese nomeada) e a matemática que restava "
     "entram como pedras; o teste às cegas acima de 5σ é parede medida. %d módulos novos e %d bandeiras novas; escada %d → %d; %d declarações auditadas "
     "e %d teoremas no relatório de axiomas, 0 fora do trio. O gate é o da v411 (`%s`; %d bandeiras ligadas e %d apagadas, lidas do core). Gate intocado."
     % (NMOD, NB, A_, B_, KHC, KHT, selo["qg_closure_verdict"], NLIG, NAPA),
     "- **O que a v412 NÃO é para o caminho crítico:** não demonstra o custo polinomial na máquina de fita para a fórmula plana arbitrária; não reabre o "
     "teste H0DN × BG1; não dá a creditação, que é de quem observa de fora; não produz a geometria 3+1 do contínuo a partir do par (álgebra, estado), que "
     "segue aberta; não fixa o relógio τ★; Navier–Stokes segue condicional às duas implicações ainda não mostradas. Seguem NOMEADAS [OPEN] as do item 5 "
     "da página: H1 e H2 na natureza, a tela fundada e o horizonte causal geral, α livre, o levantamento covariante global ao contínuo III₁, a teoria "
     "interagente com o ultravioleta e a existência global, τ★ e o setor eletrônico.",
     "- **O que segue do operador:** o elo B(n) da v412, que não rodou (a Bancada fora do ar; a gerência não religou o serviço); a ratificação das "
     "decisões da gerência e das três emendas dela na G1; o termo do resultado de 13/11, não selado na v412; a pedra `AIdentidadePreservada` (v413); o "
     "depósito no Zenodo. O candidato não teve leitura de terceiro (ordem do autor de 18/11/2026). Decisões abertas: `HANDOFF_v412_CUSTODIA.md`.", ""]
txt = "\n".join(T)
print(txt)
if EXEC:
    p = NOS / "DESENHO_DO_FECHAMENTO_QG.md"; a = p.read_bytes(); assert b"adendo_v412_selada" not in a, "o adendo da v412 ja' existe"
    bk = p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bk.write_bytes(a); assert bk.read_bytes() == a
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + txt.replace("\n", fim.decode()).encode("utf-8") + fim
    tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); tmp.replace(p); assert p.stat().st_size > len(a)
    print("ADENDO v412 acrescentado | backup", bk.name, "| sha16 novo", sha(p)[:16])
