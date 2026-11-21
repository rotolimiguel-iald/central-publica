from review import *

p=mission({'operation':'project'},'MISSION_PRE_SUBMIT')
t=next(t for t in p['projection']['active'] if t['id']==TASK)
assert t['status']=='working'
evidence=[{k:v for k,v in pin(D/f).items() if k in ('path','sha256')} for f in ['RESULTADO.json','PARECER.md','CheckTrinityR2.compile.json']]
mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
 'event_id':'trinity-r1-review-submitted','task_id':TASK,'lease_id':t['lease']['id'],'evidence':evidence},'MISSION_SUBMIT')
p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
assert next(t for t in p['projection']['active'] if t['id']==TASK)['status']=='review_pending'
board=json.loads(json.loads((D/'QUADRO_ENTREGA.json').read_text())['stdout'])
route=json.loads(json.loads((D/'MAPA_RECIBO.json').read_text())['stdout'])
deposit=json.loads(json.loads((D/'DEPOSITO_RECIBO.json').read_text())['stdout'])
assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and deposit['ok']
assert pin(deposit['arquivo'])['sha256']==deposit['sha256_deposito']
text=('Revisao de terceiro do item9 Trinity R1 entregue: APROVADA_COM_RESSALVAS documentais. '
 '60 teoremas auditados e sete verificacoes adicionais em Lean, RC0/sem avisos/so trio. Correcao geral e decisao Horn/dois literais conferidas; contador de fixacoes ligado a avaliador instrumentado, sem cota TM2. '
 'Delimitar generalizacao sobre ramificacao/resolucao; a_trindade foi ampliada. Nenhum canonico alterado; lote1 preservado. '
 f"Quadro ENTREGUE evento{board['evento']}; mapa proprio seq{route['gravados'][0]['seq']}; deposito seq{deposit['seq']} pendente de triagem. Sem autoaceite.")
mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],
 'event_id':'trinity-r1-material-delivery','changes':{'records':[{'id':'trinity-r1-delivered','kind':'fact','statute':'REAL','text':text,
 'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in evidence]}],
 'flow':{'phase':'review_delivered','next_action':'Gerencia confere os pareceres lote1/item9, delimita os comentarios e decide integracao. Nao repetir mesmos hashes. Requisitos review_pending, sem autoaceite.'}}},'MATERIAL_TRANSITION','session_memory.py')
verification=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py')
final=mission({'operation':'project'},'MISSION_FINAL')
assert next(t for t in final['projection']['active'] if t['id']==TASK)['status']=='review_pending'
base=json.loads((D/'BASELINE.json').read_text())
for s in base['sources']:assert pin(s['path'])==s,s['path']
result=json.loads((D/'RESULTADO.json').read_text())
for s in result['logs']:assert pin(s['path'])==s
assert len((D/'PARECER.md').read_text(encoding='utf-8').splitlines())<=15
closing={'schema':'iald.review-delivery-close/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
 'status':'ENTREGUE','verdict':result['verdict'],'receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),
 'board':board,'map':route,'memory_deposit':{'seq':deposit['seq'],'state':deposit['estado'],'artifact':pin(deposit['arquivo'])},
 'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':verification},
 'sources_and_logs_rechecked':True,'report_lines':12,'reviewed_theorems':60,'additional_checks':7,
 'operational_receipts':[pin(D/f) for f in ['QUADRO_CLAIM.json','PREFLIGHT.json','PREFLIGHT_DELIVERY.json','MAPA_RECIBO.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
 'scripts':[pin(p) for p in sorted(D.glob('*.py'))],
 'not_done':['No source changes','No canonical installation','No gate change','No external message/publication','No redo of first eight-item review','No self-acceptance']}
save('ENCERRAMENTO.json',closing)
print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],'status':'ENTREGUE','verdict':result['verdict'],'board_event':board['evento'],'map_seq':route['gravados'][0]['seq'],'deposit_seq':deposit['seq']},ensure_ascii=False))
