from pathlib import Path
import datetime, hashlib, json, os, subprocess

D=Path(__file__).resolve().parent
PY=r'C:\Python314\python.exe'
REF=str(D/'SESSION_REFERENCE.json')
ACTOR={'id':'codex-coordenadora','kind':'agent'}

def pin(p):
    p=Path(p);raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def put(name,obj):
    p=D/name;assert not p.exists(),p
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==raw
    os.replace(t,p);assert p.read_bytes()==raw

def call(script,req,name):
    req=dict(req,reference=REF)
    put(name+'.request.json',req)
    r=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/script)],input=json.dumps(req).encode(),capture_output=True)
    v=json.loads(r.stdout)
    put(name+'.json',v)
    assert r.returncode==0 and v.get('ok'),v
    return v['result']

p=call('mission_cli.py',{'operation':'project'},'MISSION_PRE_SUBMIT')
t=next(x for x in p['projection']['active'] if x['id']=='review-lote1')
assert t['status']=='working'
files=['RESULTADO.json','PARECER.md','FINAL_COMPILATIONS.json']
evidence=[{k:v for k,v in pin(D/f).items() if k in ('path','sha256')} for f in files]
submitted=call('mission_cli.py',{'operation':'submit','actor':ACTOR,
 'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
 'event_id':'lote1-review-submitted','task_id':'review-lote1','lease_id':t['lease']['id'],
 'evidence':evidence},'MISSION_SUBMIT')
p=call('mission_cli.py',{'operation':'project'},'MISSION_POST_SUBMIT')
assert next(x for x in p['projection']['active'] if x['id']=='review-lote1')['status']=='review_pending'
sources=[{'kind':'artifact','ref':q['path'],'sha256':q['sha256']} for q in evidence]
transition=call('session_memory.py',{'operation':'transition','actor':ACTOR,
 'expected_revision':p['receipt']['revision'],'event_id':'lote1-review-material-delivery',
 'changes':{'records':[{'id':'lote1-review-delivered','kind':'fact','statute':'REAL',
 'text':'Revisao de terceiro do lote1 entregue: oito fontes RC0, 68 teoremas auditados e quatro sondas; zero avisos/sorryAx/axiomas fora do trio. Parecer registra tres itens aprovados, quatro ressalvados e item6 reprovado como alegacao de custo real de fita, preservando seus teoremas abstratos. Errata confirmada; nenhum canonico alterado. Quadro ENTREGUE evento1692; mapa proprio seq2188; deposito seq764 pendente de triagem. Aceite e integracao pela gerencia separados.',
 'sources':sources}],
 'flow':{'phase':'review_delivered','next_action':'Gerencia confere o parecer, corrige as alegacoes documentais e decide integracao; nao repetir este lote nos mesmos hashes. Missao review_pending, sem autoaceite.'}}},'MATERIAL_TRANSITION')
verification=call('session_memory.py',{'operation':'verify'},'ACOM_VERIFY')
final=call('mission_cli.py',{'operation':'project'},'MISSION_FINAL')
assert next(x for x in final['projection']['active'] if x['id']=='review-lote1')['status']=='review_pending'

deposited=json.loads(json.loads((D/'DEPOSITO_RECIBO.json').read_text(encoding='utf-8'))['stdout'])
dep_pin=pin(deposited['arquivo'])
assert dep_pin['sha256']==deposited['sha256_deposito']
result=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
for item in result['items']:
    assert pin(item['source']['path'])['sha256']==item['source']['sha256']
for rec in result['logs']:
    assert pin(rec['path'])==rec
assert len((D/'PARECER.md').read_text(encoding='utf-8').splitlines())<=15
operational_sources=[Path(r'C:\IALD\MEMORIA_IALD\lib\iald_memory\store.py'),
 Path(r'C:\IALD\MAPA_DE_ROTAS\rotas.py'),Path(r'C:\IALD\PROGRAMA_IALD\iald.py'),
 Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\memoria.py')]
put('ENCERRAMENTO.json',{'schema':'iald.review-delivery-close/v1',
 'timestamp':datetime.datetime.now().astimezone().isoformat(),
 'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),
 'board':{'status':'ENTREGUE','event':1692,'receipt':pin(D/'QUADRO_ENTREGA.json')},
 'map':{'seq':2188,'route':'kernel.v413.revisao_codex_lote1_20nov','receipt':pin(D/'MAPA_RECIBO.json')},
 'memory_deposit':{'seq':764,'status':'PENDENTE','artifact':dep_pin,'receipt':pin(D/'DEPOSITO_RECIBO.json')},
 'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':'review-lote1',
         'status':'review_pending','verified':verification,'receipt':pin(D/'MISSION_FINAL.json')},
 'originals_and_logs_rechecked':True,'report_line_limit_verified':True,
 'operational_sources_consulted':[pin(p) for p in operational_sources],
 'own_scripts':[pin(p) for p in sorted(D.glob('*.py'))],
 'operational_receipts':[pin(D/f) for f in ['MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json','PREFLIGHT_FINAL.json']],
 'not_done':['No canonical install','No changes to kernel, um.py or gate','No scientific data opened','No publication','No self acceptance of mission or excluded Codex modules']})
print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'acom_revision':final['receipt']['revision'],'acom_task_status':'review_pending','board':'ENTREGUE','map_seq':2188,'deposit_seq':764},ensure_ascii=False))
