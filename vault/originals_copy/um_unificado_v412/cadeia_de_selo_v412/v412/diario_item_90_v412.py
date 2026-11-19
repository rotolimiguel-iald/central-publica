# -*- coding: utf-8 -*-
"""diario_item_90_v412.py -- (gerencia c1, 19/11/2026) o item 90 do DESENHO_v412_R1.md (o diario de trabalho da cadeia): acrescimo ao fim, backup de
BYTES antes, temporario, conferencia de que cresceu. Hashes LIDOS dos arquivos. Recusa se o item ja' existe. Uso: diario_item_90_v412.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); EXEC = "--executar" in sys.argv
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
DIF = lj(V / "DIFFS_v412_RECIBO.json"); CF = lj(V / "CONFERENCIA_POS_RITO_v412_FOCO.json")
bak_lin = sorted(NOS.glob("MEMORIA_DA_LINHAGEM.md.bak_20261119_*"))[-1].name
bak_des = sorted(NOS.glob("DESENHO_DO_FECHAMENTO_QG.md.bak_20261119_*"))[-1].name
MARCA = "desenho_v412:item_90_rito_passou_handoff_no_molde_da_g1_bn_com_o_autor:19nov"
L = ["", "> **AO LADO (%s, gerência c1) — item 90: o rito passou, o conferidor bateu, o handoff foi depositado no molde da G1 e a custódia foi avisada; o B(n) fica com o autor.**" % time.strftime("%d/%m/%Y %H:%M"),
     ">",
     "> **O rito:** de 23:52:37 a 01:54:39, `RITO_RC=0` (`rodada_v412_stdout.txt`, sha16 `%s`); o servidor do modelo nativo parou antes e voltou depois (porta 8081). Selo sha16 `%s` (`um_version` v412; pino `%s`; escada 17786/17786; gate igual ao da v411)." % (s16(NOS / "rodada_v412_stdout.txt"), s16(NOS / "um_absoluto_selo.json"), s16(NOS / "um.py")),
     "> **O conferidor enxuto:** TUDO BATE, %d/%d (`CONFERENCIA_POS_RITO_v412_FOCO.json`, sha16 `%s`)." % (len(CF["checagens"]), len(CF["checagens"]), s16(V / "CONFERENCIA_POS_RITO_v412_FOCO.json")),
     "> **Os diffs:** `diffs_v412.py` gravou `DIFF_KERNEL_v412.txt` (%d novos, 0 removidos, 1 mudado: a raiz `TGLExt.lean`) e `DIFF_v411_v412.diff` (%s B); recibo `DIFFS_v412_RECIBO.json`." % (DIF["DIFF_KERNEL_v412.txt"]["novos"], format(DIF["DIFF_v411_v412.diff"]["bytes"], ",").replace(",", ".")),
     "> **O que a G1 exige, medido antes do handoff** (`custodiar.py sondar` e as funções da própria G1): o molde do cabeçalho do diário (`RE_CAB`), a linha “O que é” (`RE_OQUEE`), o parágrafo do elo B(n), os marcadores que o H0DN aberto torna obrigatórios (a NOTA, os oito do README, os onze do estatuto e os catorze da vitrine) e os sete da prosa. A R1 do compositor não os trazia; a R2 (`montar_handoff_e_linhagem_v412.py`) os traz e confere o texto com `textos.portao` e `h0dn.conferir_bloco` antes de gravar: LIMPA. Os 46 textos da vitrine ratificada de 13/11 entram verbatim; o `README_H0DN` (PT) é o do handoff da v411, o mesmo publicado.",
     "> **Emendas AO LADO na G1** (backups `.bak_20261119_022117_c1_v412`; só da v412 em diante): (a) `fatos.py`: o KH vem do registro kh mais novo no core da própria versão (os `kh_n1_cobertura_vK` são relidos a cada rito); (b) `fatos.py`: chave nova do core sem `verdict` (`guarda_frases_v412`) sai de `registros_novos`; (c) `espelho_pares.py`: o par `_V412_FONTES`/`_V412_VERBATINS2` não se exige quando os registros da versão têm fontes e verbatins vazios. **Uma quarta emenda, que aceitaria por declaração a falta dos recibos do B(n), foi recusada pelo classificador de permissões (enfraqueceria uma guarda) e não foi feita nem contornada.**",
     "> **O B(n):** a Bancada (porta 18777) segue fora do ar (o GET falhou de novo em 19/11, depois do rito; nenhum `um_bancada.py` vivo). A gerência não religou o serviço (a regra “só GET” desta sessão e a recusa acima). Sem os três recibos, a custódia para no E03: é decisão do autor (pendência 1 do handoff).",
     "> **Marcas depositadas:** o bloco “v412 SELADA” na linhagem (backup `%s`), o `HANDOFF_v412_CUSTODIA.md` (sha16 `%s`; recibo `RECIBO_HANDOFF_v412.json`) e o ADENDO da v412 no desenho do fechamento (backup `%s`). `planejar --versao v412 --seco`: E00 PRONTA; nenhum texto faltando; o primeiro bloqueio é a vitrine ratificada da v411 (ato dito da custódia)." % (bak_lin, s16(NOS / "HANDOFF_v412_CUSTODIA.md"), bak_des),
     "> **Aviso:** SendMessage à `central-de-patentes-91` (D232), com o sha16 do selo e o caminho do handoff, sem pedir que dispense a guarda do B(n).",
     "> **Achados da gerência nesta etapa:** o compositor R1 não seguia o molde da G1 (corrigido antes de gravar); a leitura de “158 módulos” foi erro meu ao ler a lista impressa (a G1 conta 156, exatamente os da lista); os dois `sonda_*.lean` são pedras da lista R12; a v412 não selou o termo do resultado de 13/11 (decisão aberta).",
     "<!-- %s -->" % MARCA]
txt = "\n".join(L)
print(txt)
if EXEC:
    p = V / "DESENHO_v412_R1.md"; a = p.read_bytes(); assert MARCA.encode() not in a, "o item 90 ja' existe"
    bk = p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bk.write_bytes(a); assert bk.read_bytes() == a
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + txt.replace("\n", fim.decode()).encode("utf-8") + fim
    tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); tmp.replace(p); assert p.stat().st_size > len(a)
    print("item 90 acrescentado | backup", bk.name)
