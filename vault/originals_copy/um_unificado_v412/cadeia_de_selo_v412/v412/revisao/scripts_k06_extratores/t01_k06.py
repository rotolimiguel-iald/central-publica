import re
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
paras=re.split(r"\n\s*\n",t)
for q in paras:
    if "AEscala" in q and "LeitorDoFundo" in q:
        i=q.find("LeitorDoFundo"); j=q.find("AEscala")
        print("len",len(q),"| pos AEscala",j,"pos LeitorDoFundo",i)
        a=min(i,j); print("   ..."+q[max(0,a-120):a+260].replace("\n"," ")+"...")
