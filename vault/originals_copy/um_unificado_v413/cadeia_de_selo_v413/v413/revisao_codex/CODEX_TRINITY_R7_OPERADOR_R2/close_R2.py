from review import *
import hashlib

def verify_source(s):
    now=pin(s['path'])
    if now==s:return
    c=json.loads((D/'CONCURRENCY_OBSERVATION.json').read_text(encoding='utf-8'))
    assert s==c['previous'] and now==c['observed'], (s,now)
    b=Path(s['path']).read_bytes()
    assert hashlib.sha256(b[:s['bytes']]).hexdigest()==s['sha256']
    assert hashlib.sha256(b[s['bytes']:]).hexdigest()==c['append_sha256']
    return


def register():
    p=mission({'operation':'project'},'MISSION_PRE_DELIVERY_R2')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    r=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'task_id':TASK,'lease_id':t['lease']['id']},'PREFLIGHT_DELIVERY_R2');assert r['ready']
    for s in json.loads((D/'BASELINE.json').read_text())['sources']:verify_source(s)
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',str(D/'MAPA_REGISTRO.json'),'--quem',ACTOR['id']],'MAPA_RECIBO.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',str(D/'RESULTADO.json')],'QUADRO_ENTREGA.json').returncode==0
    print('Mapa proprio registrado; unidade ENTREGUE, nao AUDITADA.')

def deposit():
    assert (D/'QUADRO_ENTREGA.json').exists()
    assert shell([PY,'-B','-X','utf8','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py','depositar',
      '--quem',ACTOR['id'],'--tipo','project','--estatuto','REAL','--alvo','novo:revisao-v413-trinity-r7-operador-r2-codex',
      '--fonte',str(D/'RESULTADO.json'),'--fonte',str(D/'PARECER.md'),'--texto-arquivo',str(D/'MEMORIA_DEPOSITO.md'),
      '--slug','revisao-v413-trinity-r7-operador-r2-codex'],'DEPOSITO_RECIBO.json').returncode==0
    print('Deposito imutavel oficial criado para triagem da gerencia.')

def finish():
    p=mission({'operation':'project'},'MISSION_PRE_SUBMIT');t=next(t for t in p['projection']['active'] if t['id']==TASK)
    assert t['status']=='working'
    evidence=[{k:v for k,v in pin(D/f).items() if k in ('path','sha256')} for f in ['RESULTADO.json','PARECER.md','AuditTrinity.compile.json','AuditOperador.compile.json','CheckScope.compile.json','CONCURRENCY_OBSERVATION.json']]
    mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-r7-operador-r2-review-submitted','task_id':TASK,'lease_id':t['lease']['id'],'evidence':evidence},'MISSION_SUBMIT')
    p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
    assert next(t for t in p['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    board=json.loads(json.loads((D/'QUADRO_ENTREGA.json').read_text())['stdout'])
    route=json.loads(json.loads((D/'MAPA_RECIBO.json').read_text())['stdout'])
    dep=json.loads(json.loads((D/'DEPOSITO_RECIBO.json').read_text())['stdout'])
    assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and dep['ok']
    assert pin(dep['arquivo'])['sha256']==dep['sha256_deposito']
    text=('Adendo v413 R7/Operador R2 revisado: Trinity R7 APROVADA_COM_RESSALVAS; Operador R2 APROVADA. '
      '115+15 teoremas e nove controles RC0/zero avisos/so trio. Correcao anterior de escopo e dedup conferem; fontes preservadas. '
      'Restam qualificacoes documentais: limite sob 0<beta<1, sobra <=um passo, hLandauer global assumido nao determinado por reversibilidade. '
      'Identidades de carga/radical e energia condicional validas; nenhuma nova cota polinomial uniforme de fita, instalacao ou alteracao de gate. '
      f"Unidade ENTREGUE evento{board['evento']}; mapa seq{route['gravados'][0]['seq']}; deposito seq{dep['seq']} pendente. Requisito review_pending sem autoaceite.")
    mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],'event_id':'trinity-r7-operador-r2-material-delivery',
      'changes':{'records':[{'id':'trinity-r7-operador-r2-delivered','kind':'fact','statute':'REAL','text':text,
      'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in evidence]}],
      'flow':{'phase':'review_delivered','next_action':'Gerencia confere parecer R7/Operador R2, ajusta tres qualificacoes documentais e decide integracao/aceite. Preservar entregas anteriores e nao refazer mesmos hashes.'}}},'MATERIAL_TRANSITION','session_memory.py')
    ver=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py');final=mission({'operation':'project'},'MISSION_FINAL')
    assert next(t for t in final['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    res=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
    for s in res['sources']+res['logs']:verify_source(s)
    closing={'schema':'iald.review-delivery-close/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'verdict_counts':res['verdict_counts'],
      'board':board,'map':route,'memory_deposit':{'seq':dep['seq'],'state':dep['estado'],'artifact':pin(dep['arquivo'])},
      'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':ver},
      'sources_and_logs_rechecked':True,'concurrent_append_observation':pin(D/'CONCURRENCY_OBSERVATION.json'),'unchanged_source_prefix_verified':True,'report_lines':len((D/'PARECER.md').read_text(encoding='utf-8').splitlines()),
      'operational_receipts':[pin(D/f) for f in ['QUADRO_NOVA.json','QUADRO_CLAIM.json','PREFLIGHT.json','PREFLIGHT_DELIVERY_R2.json','MAPA_RECIBO.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
      'scripts':[pin(p) for p in sorted(D.glob('*.py'))],
      'not_done':res['not_done']}
    save('ENCERRAMENTO.json',closing)
    print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],'status':'ENTREGUE','board_event':board['evento'],'map_seq':route['gravados'][0]['seq'],'deposit_seq':dep['seq']},ensure_ascii=False))

if __name__=='__main__':{'register':register,'deposit':deposit,'finish':finish}[sys.argv[1]]()
