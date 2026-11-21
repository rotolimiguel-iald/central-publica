from runner import *

def register_delivery():
    p=mission({'operation':'project'},'MISSION_PRE_DELIVERY')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    r=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'task_id':TASK,'lease_id':t['lease']['id']},'PREFLIGHT_DELIVERY');assert r['ready']
    for s in json.loads((D/'BASELINE.json').read_text())['sources']:assert pin(s['path'])==s
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',str(D/'MAPA_REGISTRO.json'),'--quem',ACTOR['id']],'MAPA_RECIBO.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',str(D/'RESULTADO.json')],'QUADRO_ENTREGA.json').returncode==0
    print('Parecer consolidado registrado no mapa proprio e unidade ENTREGUE.')

def deposit():
    assert (D/'QUADRO_ENTREGA.json').exists()
    assert shell([PY,'-B','-X','utf8','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py','depositar',
      '--quem',ACTOR['id'],'--tipo','project','--estatuto','REAL','--alvo','novo:revisao-consolidada-v413-trinity-r3-codex',
      '--fonte',str(D/'RESULTADO.json'),'--fonte',str(D/'PARECER.md'),'--texto-arquivo',str(D/'MEMORIA_DEPOSITO.md'),
      '--slug','revisao-consolidada-v413-trinity-r3-codex'],'DEPOSITO_RECIBO.json').returncode==0
    print('Deposito imutavel criado pela operacao oficial; aguardando triagem.')

def finish():
    p=mission({'operation':'project'},'MISSION_PRE_SUBMIT')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    assert t['status']=='working'
    evidence=[{k:v for k,v in pin(D/f).items() if k in ('path','sha256')} for f in ['RESULTADO.json','PARECER.md','CheckTraversalVerified.compile.json','CheckNames.compile.json']]
    mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-consolidado-r3-review-submitted','task_id':TASK,'lease_id':t['lease']['id'],'evidence':evidence},'MISSION_SUBMIT')
    p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
    assert next(t for t in p['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    board=json.loads(json.loads((D/'QUADRO_ENTREGA.json').read_text())['stdout'])
    route=json.loads(json.loads((D/'MAPA_RECIBO.json').read_text())['stdout'])
    dep=json.loads(json.loads((D/'DEPOSITO_RECIBO.json').read_text())['stdout'])
    assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and dep['ok']
    assert pin(dep['arquivo'])['sha256']==dep['sha256_deposito']
    text=('Pedido consolidado20nov revisado: itens1-8 inalterados reutilizados por hash; item9 TrinityR3,87teoremas e13sondas novas finais RC0/zeroavisos/so trio. '
      '3APROVADA,5APROVADA_COM_RESSALVAS; item6 REPROVADA como custo real de fita, teoremas abstratos validos. R3 decide todaCNF com combustivel suficiente e3CNF por listaToca; cotas superiores exponenciais em fixacoes, naoTM2. '
      'Contadores majoram curto-circuito; lista conserva repeticoes; delimitar ramificacao/resolucao e retangulos. Nenhum original/kernel/um.py/gate alterado. '
      f"Unidade originalmente R2 retargetada explicitamente ao consolidado/R3, ENTREGUE evento{board['evento']}; mapa seq{route['gravados'][0]['seq']}; deposito seq{dep['seq']} pendente. Sem autoaceite.")
    mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],'event_id':'trinity-consolidado-r3-material-delivery',
      'changes':{'records':[{'id':'trinity-consolidado-r3-delivered','kind':'fact','statute':'REAL','text':text,
       'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in evidence]}],
       'flow':{'phase':'review_delivered','next_action':'Gerencia confere parecer consolidado9itens/R3, qualifica redacao e alegacao item6, decide integracao. Requisitos review_pending sem autoaceite. Nao repetir mesmos hashes.'}}},'MATERIAL_TRANSITION','session_memory.py')
    ver=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py')
    final=mission({'operation':'project'},'MISSION_FINAL')
    assert next(t for t in final['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    for s in json.loads((D/'BASELINE.json').read_text())['sources']:assert pin(s['path'])==s
    res=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
    for s in res['logs']:assert pin(s['path'])==s
    closing={'schema':'iald.review-delivery-close/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'verdict_counts':res['verdict_counts'],
      'board':board,'map':route,'memory_deposit':{'seq':dep['seq'],'state':dep['estado'],'artifact':pin(dep['arquivo'])},
      'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':ver},
      'identity_note':'Mesma unidade/requisito da etapaR2, com adendo formal de escopo para consolidado/R3.',
      'sources_and_logs_rechecked':True,'report_lines':len((D/'PARECER.md').read_text(encoding='utf-8').splitlines()),
      'operational_receipts':[pin(D/f) for f in ['QUADRO_ADENDO.json','PREFLIGHT.json','PREFLIGHT_DELIVERY.json','MAPA_RECIBO.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
      'scripts':[pin(p) for p in sorted(D.glob('*.py'))],
      'not_done':['No source changes','No canonical installation','No gate change','No external message/publication','No redo of first eight-item review','No self-acceptance']}
    save('ENCERRAMENTO.json',closing)
    print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],'status':'ENTREGUE','board_event':board['evento'],'map_seq':route['gravados'][0]['seq'],'deposit_seq':dep['seq']},ensure_ascii=False))

if __name__=='__main__':
    {'register':register_delivery,'deposit':deposit,'finish':finish}[sys.argv[1]]()
