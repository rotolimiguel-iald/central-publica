from review import *

def verified_inputs():
    res=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
    for s in res['sources']+res['logs']: assert pin(s['path'])==s, s['path']
    return res

def register():
    p=mission({'operation':'project'},'MISSION_PRE_DELIVERY')
    task=next(t for t in p['projection']['active'] if t['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_DELIVERY')['ready']
    verified_inputs()
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',str(D/'MAPA_REGISTRO.json'),
      '--quem',ACTOR['id']],'MAPA_RECIBO.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','avancar',UNIT,'--quem',ACTOR['id'],
      '--status','ENTREGUE','--evidencia',str(D/'RESULTADO.json')],'QUADRO_ENTREGA.json').returncode==0
    print('Mapa próprio registrado; quadro ENTREGUE, sem autoauditoria.')

def deposit():
    assert (D/'QUADRO_ENTREGA.json').exists()
    assert shell([PY,'-B','-X','utf8','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py',
      'depositar','--quem',ACTOR['id'],'--tipo','project','--estatuto','REAL','--alvo','novo:revisao-v413-ponte-cook-levin-codex',
      '--fonte',str(D/'RESULTADO.json'),'--fonte',str(D/'PARECER.md'),'--texto-arquivo',str(D/'MEMORIA_DEPOSITO.md'),
      '--slug','revisao-v413-ponte-cook-levin-codex'],'DEPOSITO_RECIBO.json').returncode==0
    print('Depósito imutável oficial criado para triagem c1.')

def finish():
    res=verified_inputs()
    p=mission({'operation':'project'},'MISSION_PRE_SUBMIT')
    task=next(t for t in p['projection']['active'] if t['id']==TASK)
    assert task['status']=='working'
    names=['RESULTADO.json','PARECER.md','PonteCookLevin.compile.json','CheckBridgeR2.compile.json','BIBLIOGRAPHIC_CHECK.json']
    evidence=[{k:v for k,v in pin(D/f).items() if k in ('path','sha256')} for f in names]
    mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'event_id':'ponte-cook-levin-r0-review-submitted',
      'task_id':TASK,'lease_id':task['lease']['id'],'evidence':evidence},'MISSION_SUBMIT')
    p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
    assert next(t for t in p['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    read_shell=lambda f:json.loads(json.loads((D/f).read_text(encoding='utf-8'))['stdout'])
    board,route,dep=map(read_shell,['QUADRO_ENTREGA.json','MAPA_RECIBO.json','DEPOSITO_RECIBO.json'])
    assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and dep['ok']
    assert pin(dep['arquivo'])['sha256']==dep['sha256_deposito']
    text=('PonteCookLevin R0 revisada: APROVADA_COM_RESSALVAS documentais; 22 relatorios publicos e oito controles finais '
      'RC0/zero avisos/sorry/fora do trio. Fiacao do leitor, precisao diadica, codificacao e SATcru conferidos. '
      'Controle prova EmPComUmaLeitura iff ReduzASAT sem hCL; falta explicitar o fecho many-one de SAT, nao toda P com oraculo. '
      'Concordancia matematica com traducao classica Cook-Levin (DERIVED/KNOWN), mas hCL continua hipotese sem habitante Lean nesta entrega. '
      'Trinity R7 ressalvada e Operador R2 aprovado, reutilizados por hash. Custo da leitura nao contado em TM2, sem P=NP em fita '
      'ou prova fisica de dispositivo num ato. Nenhum original/kernel/um.py/Atlas/gate alterado. '
      f"Unidade ENTREGUE evento{board['evento']}; mapa seq{route['gravados'][0]['seq']}; deposito seq{dep['seq']} pendente de triagem. Sem autoaceite.")
    mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'event_id':'ponte-cook-levin-r0-material-delivery','changes':{'records':[{'id':'ponte-cook-levin-r0-delivered',
      'kind':'fact','statute':'REAL','text':text,'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in evidence]}],
      'flow':{'phase':'review_delivered','next_action':'Gerencia confere parecer Cook-Levin R0, acrescenta qualificacao documental, decide integracao/aceite; preservar hashes e pareceres anteriores.'}}},
      'MATERIAL_TRANSITION','session_memory.py')
    ver=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py')
    final=mission({'operation':'project'},'MISSION_FINAL')
    assert next(t for t in final['projection']['active'] if t['id']==TASK)['status']=='review_pending'
    verified_inputs()
    save('ENCERRAMENTO.json',{'schema':'iald.review-delivery-close/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'verdict_counts':res['verdict_counts'],
      'board':board,'map':route,'memory_deposit':{'seq':dep['seq'],'state':dep['estado'],'artifact':pin(dep['arquivo'])},
      'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':ver},
      'sources_and_logs_rechecked':True,'report_lines':len((D/'PARECER.md').read_text(encoding='utf-8').splitlines()),
      'operational_receipts':[pin(D/f) for f in ['QUADRO_NOVA.json','QUADRO_CLAIM.json','PREFLIGHT.json','PREFLIGHT_DELIVERY.json',
        'MAPA_RECIBO.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
      'scripts':[pin(p) for p in sorted(D.glob('*.py'))],'not_done':res['not_done']})
    print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],'status':'ENTREGUE',
      'board_event':board['evento'],'map_seq':route['gravados'][0]['seq'],'deposit_seq':dep['seq']},ensure_ascii=False))

if __name__=='__main__': {'register':register,'deposit':deposit,'finish':finish}[sys.argv[1]]()
