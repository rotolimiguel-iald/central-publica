import re,json
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
spec=json.load(open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\extratores\especificacao.json",encoding="utf-8"))
paras=re.split(r"\n\s*\n",t)
def cnt(tok):
    return len(re.findall(re.escape(tok),t))
for it in spec["arms"]["T"]["assertions"]:
    s,o=it["subject"],it["object"]
    # token variants: last dotted component
    s2=s.split(".")[-1]
    ns,no=cnt(s),cnt(o)
    ns2=cnt(s2)
    co=sum(1 for q in paras if (s in q or s2 in q) and o in q)
    print(it["id"],s,"|",it["relation"],"|",o,"| subj",ns,"(last",ns2,") obj",no,"| paragraphs with both",co)
