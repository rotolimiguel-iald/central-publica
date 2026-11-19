"""Record bounded text searches and byte pins of primary local sources."""
import hashlib
import json
from pathlib import Path
import subprocess

root=Path("C:/IALD")
here=Path(__file__).resolve().parent
nos=root/"Artigo/Haja_Luz/A Ponte e o Um/Nós"
memory=root/"Central de Patentes/memory"
texts=[memory/"INVENTARIO_BANCADA_CHATGPT.md",nos/"um_absoluto.json",nos/"um_absoluto_selo.json",
       root/"MAPA_DE_ROTAS/MAPA_DE_ROTAS.json"]
gamma=here.parents[1]/"candidatas_c1/MontagemDasGamas.lean"
verb=root/"Central de Patentes/work/cunhagens_13out"
speeches=[next(verb.glob("OPERADOR_16nov_concordo_com_tudo_os_nomes_provisorios*verbatim.txt")),
          next(verb.glob("OPERADOR_16nov_o_protocolo_de_avaliacao_t6_da_iald_tem*verbatim.txt"))]
sources=[*texts,gamma,nos/"tgl_kernel/TGLExt/SitePauliObservables.lean",
         root/"TUNEL_CLAUDE_APP/ORDEM_020_ao_codex_tres_levantamentos_e_uma_construcao_para_fechar_a_v412.md",
         *speeches]
records=[]
def query(path,pattern,is_kernel=False):
    args=["rg","-n","--no-ignore","-i",pattern]
    if is_kernel: args+=["-g","*.lean","-g","!**/.lake/**"]
    args.append(str(path))
    proc=subprocess.run(args,capture_output=True,encoding="utf-8")
    if proc.returncode not in (0,1): raise RuntimeError(proc.stderr)
    lines=proc.stdout.splitlines()
    records.append({"command":args,"exit":proc.returncode,"hits":len(lines),"matches":[line[:370] for line in lines[:35]]})
names="spectral.?tripl|tripla.?espectral|tripl[ée]s?.?spectr"
query(nos/"tgl_kernel",r"^\s*(?:noncomputable\s+)?(?:structure|class|def|abbrev|inductive)\s+[^:\s(]*?(?:"+names+")",True)
query(nos/"tgl_kernel",names,True)
for path in texts: query(path,names+"|MontagemDasGamas")
for f in speeches: print(f.read_text(encoding="utf-8-sig").strip())
out={"searches":records,"source_pins":[{"path":str(f),"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"bytes":f.stat().st_size} for f in sources],
     "scope":"These lexical searches cover the canonical kernel excluding dependency/build directories, and the explicitly named documents. Zero matches do not rule out a declaration under an unrelated name."}
(here/"CONSULTAS.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print([(r["hits"],r["exit"]) for r in records])
