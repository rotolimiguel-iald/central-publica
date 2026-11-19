import re, hashlib, glob
from tokenizers import Tokenizer
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
# 1) numeros e constantes com historia no artigo (contagem)
pats={"alpha (letra)":r"α","beta (letra)":r"β","sqrt(e) 'sqrt e' ou √e":r"√e|sqrt\(e\)|\sqrt\{e\}","0,0120":r"0,0120","0,01203":r"0,01203","8,507":r"8,507","1089":r"1089","1/137 ou 137,0":r"1/137|137,0","meia-nat/1/2 nat":r"meia-nat|Meia-Nat|½ nat|1/2 nat","45 graus":r"45°|45 graus|π/4","meV":r"meV","CODATA":r"CODATA","Planck":r"Planck","TGL":r"TGL"}
for k,v in pats.items():
    print(f"{k:28s} {len(re.findall(v,t))}")
# 2) o que o isomorfo.py faria: so troca fontes LISTADAS. Simulo (so em memoria) a troca de
#    identificadores TOTALMENTE em maiusculas com sublinhado + alpha/beta por X+20hex, para medir tokens.
tj=glob.glob(r"C:\Users\rotol\.cache\huggingface\hub\models--Qwen--Qwen3.6-35B-A3B\snapshots\*\tokenizer.json")[0]
tok=Tokenizer.from_file(tj)
base=len(tok.encode(t).ids)
ids=re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b")
mp={}
def f(m):
    s=m.group(0)
    if s not in mp: mp[s]="X"+hashlib.sha256(("sim|"+s).encode()).hexdigest()[:20]
    return mp[s]
t2=ids.sub(f,t)
t2=t2.replace("α","Xa1b2c3d4e5f60718293a").replace("β","Xb1c2d3e4f5061728394a")
n2=len(tok.encode(t2).ids)
print("fontes distintas (ALLCAPS_snake):",len(mp), "ocorrencias trocadas:",len(ids.findall(t)))
print("tokens antes",base,"depois (so essas classes)",n2,"razao",n2/base)
# numeros: o script nao os toca
nums=re.findall(r"\d+[,.]\d+",t)
print("tokens numericos tipo decimal no artigo:",len(nums))
