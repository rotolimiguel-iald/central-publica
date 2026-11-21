from review import *

def verify_sources():
    r=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
    for p in r['sources']:
        assert pin(p['path'])['sha256']==p['sha256'],p['path']
    assert pin(r['report']['path'])==r['report']
    return r

def register():
    p=mission({'operation':'project'},'MISSION_PRE_DELIVERY')
    task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_DELIVERY')['ready']
    verify_sources()
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',str(D/'MAPA_REGISTRO.json'),
      '--quem',ACTOR['id']],'MAPA_RECIBO.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','avancar',UNIT,'--quem',ACTOR['id'],
      '--status','ENTREGUE','--evidencia',str(D/'RESULTADO.json')],'QUADRO_ENTREGA.json').returncode==0
    print('Revisao documental registrada no Mapa e entregue no quadro.')

def deposit():
    assert (D/'QUADRO_ENTREGA.json').exists()
    assert shell([PY,'-B','-X','utf8','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py',
      'depositar','--quem',ACTOR['id'],'--tipo','project','--estatuto','REAL',
      '--alvo','novo:revisao-v413-pedras-limpas-codex','--fonte',str(D/'RESULTADO.json'),
      '--fonte',str(D/'PARECER.md'),'--texto-arquivo',str(D/'MEMORIA_DEPOSITO.md'),
      '--slug','revisao-v413-pedras-limpas-codex'],'DEPOSITO_RECIBO.json').returncode==0
    print('Deposito oficial imutavel para triagem c1; indices protegidos nao editados.')

def finish():
    r=verify_sources()
    p=mission({'operation':'project'},'MISSION_PRE_SUBMIT')
    task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert task['status']=='working'
    ev=[source(D/f) for f in ['RESULTADO.json','PARECER.md','MECHANICAL_R2.json']]
    mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'event_id':'pedras-limpas-v413-submitted',
      'task_id':TASK,'lease_id':task['lease']['id'],'evidence':ev},'MISSION_SUBMIT')
    p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
    decode=lambda f:json.loads(json.loads((D/f).read_text(encoding='utf-8'))['stdout'])
    board,route,dep=map(decode,['QUADRO_ENTREGA.json','MAPA_RECIBO.json','DEPOSITO_RECIBO.json'])
    assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and dep['ok']
    assert pin(dep['arquivo'])['sha256']==dep['sha256_deposito']
    text=('Revisao documental das pedras limpas v413: codigo dos21modulos e OResumoEPsiBit preservado; '
      '274+18relatorios de axiomas existentes reconciliados com fontes e logs, sem recompilar. '
      'Quatro correcoes Kimi e docstring OResumo conferidas; ressalvas documentais detalhadas no recibo, '
      'com texto proposto, sem alteracao de fonte. Custo da casa reconhecido e hipoteses preservadas. '
      'Hash do diff atual confere com pedido, mas diverge do pino antigo no manifesto; corrigir metadado pela gerencia. '
      f"Vereditos21modulos: {r['verdict_counts_new_modules']}. Unidade ENTREGUE evento{board['evento']}, "
      f"Mapa seq{route['gravados'][0]['seq']}, deposito seq{dep['seq']} para triagem; sem autoaceite ou instalacao.")
    mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'event_id':'pedras-limpas-v413-material-delivery','changes':{
        'records':[{'id':'pedras-limpas-v413-documentary-review','kind':'fact','statute':'REAL','text':text,
         'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in ev]}],
        'flow':{'phase':'documentary_review_delivered','next_action':'Gerencia integra as correcoes textuais propostas, atualiza o pino do diff e decide aceite separado; preservar provas, codigo e escopo ja conferidos.'}}},
      'MATERIAL_TRANSITION','session_memory.py')
    ver=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py')
    final=mission({'operation':'project'},'MISSION_FINAL')
    assert next(x for x in final['projection']['active'] if x['id']==TASK)['status']=='review_pending'
    verify_sources()
    save('ENCERRAMENTO.json',{'schema':'iald.documentary-review-delivery/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'board':board,'map':route,
      'memory_deposit':{'seq':dep['seq'],'state':dep['estado'],'artifact':pin(dep['arquivo'])},
      'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':ver},
      'sources_rechecked':True,'scripts':[pin(p) for p in sorted(D.glob('*.py'))],
      'operational_receipts':[pin(D/f) for f in ['QUADRO_CLAIM.json','PREFLIGHT.json','PREFLIGHT_DELIVERY.json',
        'MAPA_RECIBO.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
      'preparation_notes':'Projecao padrao da missao excedeu24000caracteres; retomada da mesma referencia com max_chars60000, sem truncamento ou nova inscricao. R1 mecanica comparou ordem de axiomas; R2 compara conjuntos iguais, preservando R1. Nenhuma repeticao de mutacao concluida.',
      'not_done':r['not_done']})
    print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],
      'event':board['evento'],'route_seq':route['gravados'][0]['seq'],'deposit_seq':dep['seq']},ensure_ascii=False))

if __name__=='__main__': {'register':register,'deposit':deposit,'finish':finish}[sys.argv[1]]()
