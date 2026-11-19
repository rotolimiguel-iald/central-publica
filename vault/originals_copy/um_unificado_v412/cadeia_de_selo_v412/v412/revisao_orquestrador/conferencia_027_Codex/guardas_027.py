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


import ast
lines=rd(u).splitlines(keepends=True)
previous=json.loads(rd(r/'compilacao_026_Codex/CONFERENCIAS.json'))
assert sha(u)==previous['guardas']['programa']['sha256']
ranges=previous['guardas']['funcoes_e_linhas']
functions={name:''.join(lines[a-1:b]) for name,(a,b) in ranges.items()}
def literal_assignment(name):
    i=next(i for i,s in enumerate(lines) if s.startswith(name+' = '))
    j=next((j for j in range(i+1,len(lines)) if re.match(r'^[A-Za-z_@]',lines[j])),len(lines))
    node=ast.parse(''.join(lines[i:j])).body[0]
    return ast.literal_eval(node.value),[i+1,j]
verbatims,verb_range=literal_assignment('_V410_VERBATINS2')
scope={'_V410_VERBATINS2':verbatims}
for name,code in functions.items():
    tree=ast.parse(code)
    assert len(tree.body)==1 and isinstance(tree.body[0],ast.FunctionDef)
    exec(compile(tree,'guardas_extraidas_'+name,'exec'),scope)
guard=scope['_v411_guarda_frases']
d59=Path(previous['guardas']['D59']['arquivo'])
d65=Path(previous['guardas']['D65']['arquivo'])
d59lines=rd(d59).splitlines()
rx=next(s for s in d59lines if s.startswith('_RX_D59 = '))
rxscope={'re':re};exec(rx,rxscope)
a=next(i for i,s in enumerate(d59lines) if s.startswith('def ') and 'viola' in s)
b=next(i for i in range(a+1,len(d59lines)) if re.match(r'^[A-Za-z_@]',d59lines[i]))
exec('
'.join(d59lines[a:b]),rxscope)
d59func=rxscope[re.match(r'def (\w+)',d59lines[a]).group(1)]
d65node=ast.parse(next(s for s in rd(d65).splitlines() if s.startswith('FORA_D65 ='))).body[0]
forbidden=ast.literal_eval(d65node.value)
results={}
for label,pth in [('R6',oldpage),('R7',page)]:
    text=rd(pth)
    result={'source':pin(pth),'whole':guard(text),'D59_whole':d59func(text),'D65_whole':[s for s in forbidden if s.lower() in text.lower()],'lines':[]}
    for i,line in enumerate(text.splitlines(),1):
        g=guard(line);d=d59func(line);f=[s for s in forbidden if s.lower() in line.lower()]
        if g or d or f:result['lines'].append({'line':i,'text':line,'guards':g,'D59':d,'D65':f})
    results[label]=result
assert results['R6']['whole']==previous['disparos']['pagina_inteira']['guardas']
assert [q['line'] for q in results['R6']['lines']]==[3,13,15,19,50,52,79]
dump(out/'GUARDAS.json',{'program':pin(u),'functions':ranges,'verbatims_range':verb_range,'literal_verbatims_count':len(verbatims),'D59':pin(d59),'D65':pin(d65),'results':results,'method':'Somente funções textuais isoladas e dicionário literal. Sem executar ou importar um.py.'})
print(json.dumps(results['R7'],ensure_ascii=False,indent=2))
