from pathlib import Path
import json,hashlib,re,sys,os,datetime,subprocess,uuid,math
root=Path('C:/IALD');t=root/'TUNEL_CLAUDE_APP';central=root/'Central de Patentes';v=central/'work/cadeia_de_selo/v412';c=v/'candidatas_c1';r=v/'revisao_orquestrador';nos=root/'Artigo/Haja_Luz/A Ponte e o Um/Nós';k=nos/'tgl_kernel/TGLExt';u=nos/'um.py'
def rd(p):return p.read_text(encoding='utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(arquivo=str(p),bytes=p.stat().st_size,sha256=sha(p))
orders=sorted(t.glob('ORDEM_025*.md'),key=lambda p:('ADENDO' in p.name,p.name));anchor=r/'SESSION_REFERENCE_025_Codex.json';actor={'id':'codex-coordenadora','kind':'agent'};dst=t/'RESULTADOS/025_RESULTADO.json'
def mem(**q):
 proc=subprocess.run([sys.executable,'-B','-X','utf8',str(root/'MEMORIA_IALD/session_memory.py')],input=json.dumps(q,ensure_ascii=False).encode(),capture_output=True);out=proc.stdout.decode('utf8');assert not proc.returncode,out[-2100:];j=json.loads(out);return j.get('result',j)
revpaths=[c/'REV44/OTempoEACauda.lean',c/'REV45/AFitaEACauda.lean',c/'REV46/AMedidaEOIf.lean',c/'REV47/AEsperancaEOIf.lean']; page=v/'o_que_fica_claro_REV5/O_QUE_FICA_CLARO_v412_R5.md';out=r/'compilacao_025_Codex'
def immutable(p,data):
 if p.exists():
  assert p.read_bytes()==data, str(p)
  return
 temp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp')
 with temp.open('xb') as f:
  f.write(data);f.flush();os.fsync(f.fileno())
 assert temp.read_bytes()==data
 os.rename(temp,p);assert p.read_bytes()==data
def dump(p,obj):immutable(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())

orders=sorted(t.glob('ORDEM_026*.md'),key=lambda p:('ADENDO' in p.name,p.name));anchor=r/'SESSION_REFERENCE_026_Codex.json';dst=t/'RESULTADOS/026_RESULTADO.json';page5=page;page=v/'o_que_fica_claro_REV6/O_QUE_FICA_CLARO_v412_R6.md';out=r/'compilacao_026_Codex'
olds=[next((c/f'REV{i}').glob('*.lean')) for i in (44,45,46,48,49)]
news=[next((c/f'REV{i}').glob('*.lean')) for i in range(50,56)]
prior=r/'compilacao_025_Codex'

orders=sorted(t.glob('ORDEM_027*.md'),key=lambda p:('ADENDO' in p.name,p.name));anchor=r/'SESSION_REFERENCE_027_Codex.json';dst=t/'RESULTADOS/027_RESULTADO.json';oldpage=page;page=v/'o_que_fica_claro_REV7/O_QUE_FICA_CLARO_v412_R7.md';out=r/'conferencia_027_Codex'
r3=v/'insumos/pedras_r3';r4=v/'insumos/pedras_r4';manifest=v/'insumos/MANIFESTO_PEDRAS_v412_R4.json'

import difflib
def split_lean(text):
    code=[]; comments=[]; i=0; start=0; n=len(text)
    while i<n:
        if text.startswith('/-',i):
            begin=i; depth=1; i+=2
            while i<n and depth:
                if text.startswith('/-',i): depth+=1; i+=2
                elif text.startswith('-/',i): depth-=1; i+=2
                else:i+=1
            assert depth==0
            comments.append({'line':text.count('\n',0,begin)+1,'text':text[begin:i]})
            continue
        if text.startswith('--',i):
            begin=i; end=text.find('\n',i); i=n if end<0 else end
            comments.append({'line':text.count('\n',0,begin)+1,'text':text[begin:i]})
            continue
        if text[i]=='"':
            begin=i;i+=1
            while i<n:
                if text[i]=='\\':i+=2
                elif text[i]=='"':i+=1;break
                else:i+=1
            code.append(text[begin:i]);continue
        code.append(text[i]);i+=1
    raw=''.join(code)
    canonical='\n'.join(s.rstrip() for s in raw.splitlines() if s.strip())
    return raw,canonical,comments
out.mkdir(exist_ok=True)
records=[]; diffs={}
mf=json.loads(rd(manifest)); claimed={m['modulo']:m for m in mf['modulos']}
assert len(claimed)==40
for f in sorted(r4.glob('*.lean')):
    before=r3/f.name;a=rd(before);b=rd(f)
    raw1,t1,c1=split_lean(a);raw2,t2,c2=split_lean(b)
    assert sha(f)==claimed[f.stem]['sha256']
    assert sha(before)==claimed[f.stem]['fonte_revista_sha256']
    records.append({'module':f.stem,'before':pin(before),'after':pin(f),'bytes_equal':before.read_bytes()==f.read_bytes(),'code_raw_equal':raw1==raw2,'code_layout_normalized_equal':t1==t2,'code_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in [t1,t2]],'comments_before':c1,'comments_after':c2})
    diffs[f.name]='\n'.join(difflib.unified_diff(a.splitlines(),b.splitlines(),fromfile=str(before),tofile=str(f),n=1))
dump(out/'COMPARACAO_FONTES.json',{'manifest':pin(manifest),'records':records,'page':pin(page),'previous_page':pin(oldpage)})
dump(out/'DIFFS.json',diffs)
print({'files':len(records),'changed':sum(not a['bytes_equal'] for a in records),'raw_equal':sum(a['code_raw_equal'] for a in records),'layout_equal':sum(a['code_layout_normalized_equal'] for a in records)})
