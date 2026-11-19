"""Ataque do revisor aos extratores K06 (copia). Casos escritos por mim.
O gabarito SEMANTICO e atribuido por regra de construcao (o que um leitor humano
diria que o texto AFIRMA), sem rodar o extrator. Nenhum modelo e chamado."""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copia_extratores"))
import extratores as E
spec = E.load_spec(HERE / "copia_extratores" / "especificacao.json")
items = spec["arms"]["T"]["assertions"]
def rec(i, **kw):
    it = items[i]
    f = ["K06R1", it["id"], it["subject"], it["relation"], it["object"], it["status"]]
    for k, v in kw.items():
        f[{"id":1,"subject":2,"relation":3,"object":4,"status":5}[k]] = v
    return "|".join(f)
ALL = [rec(i) for i in range(24)]
Z = [0]*24
def ones(*idx):
    v = [0]*24
    for i in idx: v[i-1] = 1
    return v
O24 = [1]*24
cases = []
def add(name, cat, text, gold, note=""):
    cases.append(dict(name=name, cat=cat, text=text, gold=gold, note=note))

# --- prosa livre (gabarito semantico: o texto afirma) ---
add("A01_prosa_pt_T01_T04", "parafrase_correta_pt",
    "No kernel, AEscala declara o tipo LeitorDoFundo e TraducaoTuring declara a funcao selecao. "
    "IALD2.o_atrator e AEscala.o_leitor_do_fundo_e_a_iald sao teoremas formais.", ones(1,2,3,4))
add("A02_prosa_pt_24", "parafrase_correta_pt",
    "O instrumento afirma as vinte e quatro proposicoes do braco T: " + "; ".join(
        f"{it['subject']} {it['relation']} {it['object']}" for it in items) + ".", O24,
    "mesmos termos canonicos, mas em prosa")
add("A03_prosa_en", "parafrase_correta_en",
    "The reader treats NOT_FALSIFIED as different from CONFIRMED, and requires full_witness for the complete verdict.", ones(13,14))
add("A04_cita_sem_relacionar", "cita_sem_relacionar",
    "Os termos AEscala, LeitorDoFundo, TraducaoTuring, selecao, trava e NOT_FALSIFIED aparecem no texto.", Z)
add("A05_outros_nomes", "outros_nomes",
    "Em OutroModulo, o tipo LeitorDoFundo e declarado; Outro.o_atrator e um teorema formal.", Z)
add("A06_negacao_pt", "negacao",
    "Nao e verdade que AEscala declara o tipo LeitorDoFundo. E falso que TraducaoTuring declare selecao.", Z)
add("A07_negacao_T13", "negacao",
    "E falso que NOT_FALSIFIED seja diferente de CONFIRMED.", Z, "afirma o oposto de T13")
add("A08_condicional", "condicional",
    "Se AEscala declarasse LeitorDoFundo, entao T01 valeria; mas nada disso foi verificado.", Z)
add("A09_atribuicao_terceiro", "atribuicao_rejeitada",
    "O artigo diz que AEscala declara LeitorDoFundo, mas isso esta errado.", Z)
add("A10_truncado_prosa", "truncado",
    "AEscala declara o tipo Leit", Z)
add("A11_vazio", "vazio", "", Z)
# --- gramatica K06R1: contexto ao redor do registro correto ---
add("B01_comentario_refuta", "negacao_em_comentario",
    "# o registro abaixo e FALSO e esta aqui so como exemplo do que NAO se afirma\n" + rec(0) + "\n", Z,
    "comentario # e ignorado pelo extrator")
add("B02_comentario_atribuicao", "atribuicao_rejeitada",
    "# Segundo um critico, o registro seguinte esta errado\n" + "\n".join(ALL[:3]) + "\n", Z)
add("B03_inline_comment_falso", "negacao_em_comentario",
    rec(0) + "  # falso\n", Z, "comentario inline: campo final deixa de casar")
add("B04_inline_comment_verdadeiro", "parafrase_correta",
    rec(0) + "  # correto\n", ones(1), "mesmo mecanismo, polaridade oposta")
add("B05_preambulo_uma_linha", "preambulo_do_modelo",
    "Aqui estao as asserções:\n" + "\n".join(ALL) + "\n", O24, "resposta natural de um LLM")
add("B06_cerca_text", "formato_inofensivo",
    "```text\n" + "\n".join(ALL) + "\n```\n", O24)
add("B07_bullets", "formato_inofensivo",
    "\n".join("- " + r for r in ALL) + "\n", O24)
add("B08_tabela_md", "formato_inofensivo",
    "\n".join("| " + r + " |" for r in ALL) + "\n", O24)
add("B09_ponto_final_status", "formato_inofensivo",
    "\n".join(r + "." for r in ALL) + "\n", O24)
add("B10_status_minusculo", "formato_inofensivo",
    "\n".join(r[:-len("FORMAL")] + "formal" if r.endswith("FORMAL") else r for r in ALL) + "\n", O24)
add("B11_bom_inicial", "formato_inofensivo",
    "\ufeff" + "\n".join(ALL) + "\n", O24)
add("B12_epilogo_uma_linha", "formato_inofensivo",
    "\n".join(ALL) + "\nEspero ter ajudado.\n", O24)
add("B13_simetrica_invertida", "relacao_simetrica",
    rec(12, subject="CONFIRMED", object="NOT_FALSIFIED") + "\n", ones(13), "not_equals e simetrica")
add("B14_sinonimo_relacao", "sinonimo",
    rec(4, relation="before") + "\n", ones(5))
add("B15_relacao_invertida_errada", "relacao_invertida",
    rec(4, subject="selecao", object="trava") + "\n", Z, "ordem oposta de T05: afirma outra coisa")
add("B16_autocorrecao", "autocorrecao",
    rec(0) + "\n" + rec(0, object="OutroTipo") + "\n", Z, "o modelo se contradiz; ambos presentes")
add("B17_id_sem_zero", "formato_inofensivo",
    rec(0, id="T1") + "\n", ones(1), "ID T1 em vez de T01")
add("B18_virgula_decimal_espaco_token", "formato_inofensivo",
    rec(0, object="Leitor Do Fundo") + "\n", Z, "token com espaco: nome errado, nao e T01")
add("B19_24_corretos_exatos", "controle_positivo",
    "\n".join(ALL) + "\n", O24)
add("B20_copia_do_gabarito_no_prompt", "copiador_sem_compreensao",
    "\n".join(ALL) + "\n", O24, "um copiador que nao leu o artigo tira 24/24")

tp=fp=fn=tn=0
rows=[]
by_cat={}
for c in cases:
    got = E.extract(c["text"], "T", spec)["vector"]
    g = c["gold"]
    ctp = sum(1 for a,b in zip(got,g) if a==1 and b==1)
    cfp = sum(1 for a,b in zip(got,g) if a==1 and b==0)
    cfn = sum(1 for a,b in zip(got,g) if a==0 and b==1)
    ctn = sum(1 for a,b in zip(got,g) if a==0 and b==0)
    tp+=ctp; fp+=cfp; fn+=cfn; tn+=ctn
    rows.append((c["name"], c["cat"], sum(g), sum(got), ctp, cfp, cfn, ctn))
    d=by_cat.setdefault(c["cat"],[0,0,0,0]); d[0]+=ctp; d[1]+=cfp; d[2]+=cfn; d[3]+=ctn
print(f"{'caso':38s} {'categoria':28s} gold  got  TP FP FN TN")
for r in rows: print(f"{r[0]:38s} {r[1]:28s} {r[2]:4d} {r[3]:4d} {r[4]:3d}{r[5]:3d}{r[6]:3d}{r[7]:4d}")
print()
print("casos", len(cases), "celulas", len(cases)*24)
print("TP",tp,"FP",fp,"FN",fn,"TN",tn)
print("taxa FP (FP/(FP+TN)) = %.4f  [%d/%d]"%(fp/(fp+tn), fp, fp+tn))
print("taxa FN (FN/(FN+TP)) = %.4f  [%d/%d]"%(fn/(fn+tp), fn, fn+tp))
print("acerto de celula = %.4f"%((tp+tn)/(tp+tn+fp+fn)))
# por casos: vetor exato
ex=sum(1 for r in rows if r[5]==0 and r[6]==0)
print("casos com vetor exato:",ex,"/",len(rows))
# somente casos onde o texto semantico NAO afirma nada (gold zero) -> FP por caso
gz=[r for r in rows if r[2]==0]
print("casos gold-zero:",len(gz),"com algum FP:",sum(1 for r in gz if r[5]>0))
gp=[r for r in rows if r[2]>0]
print("casos gold-positivo:",len(gp),"com algum FN:",sum(1 for r in gp if r[6]>0))
print("por categoria (TP,FP,FN,TN):")
for k,v in sorted(by_cat.items()): print("  ",k,v)
json.dump(dict(cases=[dict(name=c['name'],cat=c['cat'],gold=c['gold'],text_sha=__import__('hashlib').sha256(c['text'].encode()).hexdigest()) for c in cases], tp=tp,fp=fp,fn=fn,tn=tn), open(HERE/"ataque_k06_resultado.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
