from pathlib import Path
import datetime, difflib, hashlib, json, os, re, subprocess, sys, time

D=Path(__file__).resolve().parent
V=D.parents[1]
OLD=D.parent/'CODEX_LOTE1'
REF=str(OLD/'SESSION_REFERENCE.json')
PY='C:/Python314/python.exe'
LEAN=Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
BOX=Path('C:/t/k412c/final')
ACTOR={'id':'codex-coordenadora','kind':'agent'}
UNIT='F1.V413_REVISAO_TRINITY_R1_20261120'
TASK='review-trinity-r1'
SRC=V/'candidatas_c1/R1_trinity/Trinity.lean'

def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

def save(name,obj):
    p=D/name; p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),p
    b=obj if isinstance(obj,bytes) else ((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode() if not isinstance(obj,str) else obj.encode())
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p); assert p.read_bytes()==b
    return pin(p)

def shell(args,name):
    r=subprocess.run(args,capture_output=True)
    save(name,{'args':args,'rc':r.returncode,'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8')})
    return r

def mission(req,name,script='mission_cli.py'):
    req=dict(req,reference=REF)
    save(name+'.request.json',req)
    r=subprocess.run([PY,'-B','-X','utf8','C:/IALD/MEMORIA_IALD/'+script],input=json.dumps(req).encode(),capture_output=True)
    v=json.loads(r.stdout); save(name+'.json',v)
    assert r.returncode==0 and v.get('ok'),v
    return v['result']

def prepare():
    sources=[SRC,V/'candidatas_c1/R0_trinity/Trinity.lean',V/'candidatas_c1/R1_trinity/build/CONFERENCIA.json',
      D.parent/'ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md',D.parent/'ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md',
      D.parent/'PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md',
      OLD/'BASELINE.json',OLD/'RESULTADO.json',OLD/'ENCERRAMENTO.json',OLD/'APropostaDaTensao.compile.json',
      OLD/'src/APropostaDaTensao.lean',OLD/'build/APropostaDaTensao.olean',
      BOX/'TGLExt/CompilaHornNaFita.lean', BOX/'lean-toolchain', LEAN]
    pins=[pin(p) for p in sources]
    assert pins[0]['sha256'].startswith('97fd14f931128cf3')
    rec=json.loads((OLD/'APropostaDaTensao.compile.json').read_text())
    assert rec['rc']==0 and pin(OLD/'build/APropostaDaTensao.olean')==rec['object']
    base=json.loads((OLD/'BASELINE.json').read_text())
    assert pin(OLD/'src/APropostaDaTensao.lean')==base['sources'][4]['copy']
    lp=[str(D/'build')]+base['lean_path']
    save('BASELINE.json',{'sources':pins,'lean_path':lp,'dependency_receipt':pin(OLD/'APropostaDaTensao.compile.json'),
      'reference':REF,'unit':UNIT,'task':TASK,'timestamp':datetime.datetime.now().astimezone().isoformat()})
    shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_CONSULTA.json')
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Trinity'],'MAPA_ANTES.json')
    board=json.loads(Path('C:/IALD/PROGRAMA_IALD/PROGRAMA.json').read_text(encoding='utf-8-sig'))
    assert UNIT not in json.dumps(board)
    save('UNIDADE.json',[{'id':UNIT,'frente':'F1','titulo':'Revisao de terceiro Trinity R1, item 9 da v413',
      'objetivo':'Adendo 2 de 20nov: revisar Trinity R1; fontes, compilacao, axiomas, decisao Horn/dois literais, custo e docstrings. Sem instalacao.',
      'status':'PRONTA','fonte':str(sources[3])}])
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','nova','--json',str(D/'UNIDADE.json'),'--quem',ACTOR['id']],'QUADRO_NOVA.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Revisao independente de c1, item 9; sem alterar originais.'],'QUADRO_CLAIM.json').returncode==0
    p=mission({'operation':'project'},'MISSION_INITIAL')
    p=mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-r1-extend','requirements':[{'id':TASK,'criterion':'Revisar item 9 Trinity R1 segundo os dois adendos; compilacao, axiomas integrais, semantica e custo; parecer curto e hashes. Sem refazer lote1 ou instalar.','depends_on':[]}],
      'reason':'Adendo 2 apresentado pelo operador amplia a revisao com item 9 R1.',
      'sources':[{k:v for k,v in pin(sources[3]).items() if k in ('path','sha256')}]},'MISSION_EXTEND')
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-r1-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    ready=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'task_id':TASK,'lease_id':t['lease']['id']},'PREFLIGHT')
    assert ready['ready'],ready
    save('src/Trinity.lean',SRC.read_bytes())
    r0=sources[1].read_text(encoding='utf-8');r1=SRC.read_text(encoding='utf-8')
    save('R0_R1.diff',''.join(difflib.unified_diff(r0.splitlines(True),r1.splitlines(True),fromfile='R0/Trinity.lean',tofile='R1/Trinity.lean')))
    names=re.findall(r'^theorem\s+(\w+)',r1,re.M)
    save('DECLARATIONS.json',{'theorem_count':len(names),'names':names})
    save('src/AuditTrinity.lean','import Trinity\n'+''.join('#print axioms TGLExt.Trinity.'+x+'\n' for x in names))
    print(json.dumps({'ready':True,'theorems':len(names),'unit':UNIT,'revision':p['receipt']['revision']}))

def compile_module(name):
    base=json.loads((D/'BASELINE.json').read_text())
    env=os.environ.copy();env['LEAN_PATH']=';'.join(base['lean_path'])
    (D/'build').mkdir(exist_ok=True)
    cmd=[str(LEAN),'-j','2','-o',str(D/'build'/(name+'.olean')),name+'.lean']
    start=time.monotonic();r=subprocess.run(cmd,cwd=D/'src',env=env,capture_output=True)
    log=save('logs/'+name+'.log',r.stdout+r.stderr);txt=(r.stdout+r.stderr).decode('utf-8')
    entries=[{'declaration':m.group(1),'axioms':[a.strip() for a in (m.group(2) or '').split(',') if a.strip()]} for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",txt,re.S)]
    out={'command':cmd,'source':pin(D/'src'/(name+'.lean')),'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'log':log,'axiom_reports':entries,
      'outside_trio':sorted({a for e in entries for a in e['axioms'] if a not in {'propext','Classical.choice','Quot.sound'}}),
      'warning':bool(re.search(r'\bwarning:',txt)),'sorryAx':'sorryAx' in txt}
    if (D/'build'/(name+'.olean')).exists():out['object']=pin(D/'build'/(name+'.olean'))
    save(name+'.compile.json',out)
    print(json.dumps({k:v for k,v in out.items() if k not in ['axiom_reports','command','object','source']}) )
    if r.returncode:print(txt)
    return out

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='compile':
        for module in sys.argv[2:]:
            result=compile_module(module)
            if result['rc']:break
