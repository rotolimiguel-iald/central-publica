import glob, json
from tokenizers import Tokenizer
tj=glob.glob(r"C:\Users\rotol\.cache\huggingface\hub\models--Qwen--Qwen3.6-35B-A3B\snapshots\*\tokenizer.json")[0]
tok=Tokenizer.from_file(tj)
p=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt"
t=open(p,encoding="utf-8").read()
n=len(tok.encode(t).ids)
print("tokenizer_file",tj.split("snapshots")[1][:12])
print("ref_tokens",n, "tokens_per_word", n/157921, "bytes_per_token", 1164350/n)
for k in (1,2,12):
    print("k=%d copies -> %d tokens (+2048 out)"%(k,k*n+2048))
print("sum_k=1..12 input per session",78*n)
for S in (6400,12360,13100):
    print("sessions",S,"input tokens (ref tokenizer, corpus-only)",S*78*n)
