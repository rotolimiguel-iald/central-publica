import re
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
def show(tok,k=2,w=170):
    ms=list(re.finditer(re.escape(tok),t))
    print("###",tok,len(ms))
    for m in ms[:k]:
        a=max(0,m.start()-w); b=min(len(t),m.end()+w)
        print("   ..."+t[a:b].replace("\n"," ")+"...")
for tok in ["LeitorDoFundo","selecao","o_atrator","o_leitor_do_fundo_e_a_iald","observing_adds_nothing","H_TARGET","FORBIDDEN","IALD_COLLAPSE","consciousness"]:
    show(tok)
