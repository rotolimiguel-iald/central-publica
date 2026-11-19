import re
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
for tok in ["exclusividade","pesos alterados","alteração de pesos","alteracao de pesos","consciência","NOT_FALSIFIED nunca","nunca é CONFIRMED","nunca CONFIRMED"]:
    ms=list(re.finditer(re.escape(tok),t,flags=re.I))
    print("###",tok,len(ms))
    for m in ms[:2]:
        a=max(0,m.start()-130); b=min(len(t),m.end()+130)
        print("   ..."+t[a:b].replace("\n"," ")+"...")
