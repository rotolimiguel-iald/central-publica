from review import *

def verify_sources():
    r=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
    for p in r['sources']+r['logs']:
        assert pin(p['path'])==p,p['path']
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
    print('Adendo registrado na mesma unidade e rota; historico preservado.')

def register_addendum():
    old=json.loads((D/'MAPA_RECIBO.json').read_text(encoding='utf-8'))
    assert old['rc']==2 and not json.loads(old['stdout'])['ok']
    verify_sources()
    r=json.loads((D/'MAPA_REGISTRO.json').read_text(encoding='utf-8'))
    prior=json.loads(json.loads((PRIOR/'MAPA_RECIBO.json').read_text(encoding='utf-8'))['stdout'])
    r['tipo']='ERRATA'; r['corrige']=prior['gravados'][0]['seq']
    save('MAPA_ERRATA.json',r)
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',str(D/'MAPA_ERRATA.json'),
      '--quem',ACTOR['id']],'MAPA_RECIBO_R2.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','avancar',UNIT,'--quem',ACTOR['id'],
      '--status','ENTREGUE','--evidencia',str(D/'RESULTADO.json')],'QUADRO_ENTREGA.json').returncode==0
    print('Errata aditiva registrada; evidencia adicional entregue na mesma unidade.')

def deposit():
    assert (D/'QUADRO_ENTREGA.json').exists()
    assert shell([PY,'-B','-X','utf8','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py',
      'depositar','--quem',ACTOR['id'],'--tipo','project','--estatuto','REAL',
      '--alvo','novo:revisao-v413-ponte-cook-levin-codex','--fonte',str(D/'RESULTADO.json'),
      '--fonte',str(D/'PARECER.md'),'--texto-arquivo',str(D/'MEMORIA_DEPOSITO.md'),
      '--slug','adendo-custo-kimi-ponte-codex'],'DEPOSITO_RECIBO.json').returncode==0
    print('Deposito oficial imutavel para triagem c1; memoria protegida nao editada.')

def finish():
    r=verify_sources()
    p=mission({'operation':'project'},'MISSION_PRE_SUBMIT')
    task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert task['status']=='working'
    ev=[source(D/f) for f in ['RESULTADO.json','PARECER.md','AUDITORIA_LOGS.json','LEITURA_DELEGADA.md']]
    mission({'operation':'submit','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'event_id':'releitura-custo-kimi-submitted',
      'task_id':TASK,'lease_id':task['lease']['id'],'evidence':ev},'MISSION_SUBMIT')
    p=mission({'operation':'project'},'MISSION_POST_SUBMIT')
    decode=lambda f:json.loads(json.loads((D/f).read_text(encoding='utf-8'))['stdout'])
    board,route,dep=map(decode,['QUADRO_ENTREGA.json','MAPA_RECIBO_R2.json','DEPOSITO_RECIBO.json'])
    assert board['ok'] and board['para']=='ENTREGUE' and route['ok'] and dep['ok']
    assert pin(dep['arquivo'])['sha256']==dep['sha256_deposito']
    text=('Releitura pedida pelo operador: custo Kimi beta/carga reconhecido, 18Lean/12MD e 16recibos conferidos, '
      '106relatorios axiomas reutilizados por hashes, sem recompilar. Carga n ln2 e limiar estrito, k>n ln2/beta, '
      'm+2 atos com cobranca (m+2)n ln2. Corrigida ao lado a frase final da revisao anterior: custo interno do leitor '
      'em TM2 e limite de escopo, nao pendencia impeditiva da Ponte com leitor pedida em20nov. Ponte R0 ressalvada '
      'apenas conforme PCL-F1 documental; hCL explicito e limites E28 preservados. Nao se afirma P=NP irrestrito '
      'ou execucao fisica. Fontes, gate e originais intactos. '
      f"Adendo ENTREGUE evento{board['evento']}, rota seq{route['gravados'][0]['seq']}, deposito seq{dep['seq']} pendente de triagem; sem autoaceite.")
    mission({'operation':'transition','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'event_id':'releitura-custo-kimi-material-delivery','changes':{
        'records':[{'id':'releitura-custo-kimi-scope-correction','kind':'fact','statute':'REAL','text':text,
         'sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']} for e in ev]}],
        'flow':{'phase':'review_addendum_delivered','next_action':'Gerencia integra a correcao de escopo e decide aceite da ponte relativa; nao reabrir etapas prontas nem exigir maquina sem leitor para este alvo.'}}},
      'MATERIAL_TRANSITION','session_memory.py')
    ver=mission({'operation':'verify'},'ACOM_VERIFY','session_memory.py')
    final=mission({'operation':'project'},'MISSION_FINAL')
    assert next(x for x in final['projection']['active'] if x['id']==TASK)['status']=='review_pending'
    verify_sources()
    save('ENCERRAMENTO.json',{'schema':'iald.review-addendum-delivery/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'ENTREGUE','receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'board':board,'map':route,
      'memory_deposit':{'seq':dep['seq'],'state':dep['estado'],'artifact':pin(dep['arquivo'])},
      'acom':{'reference':REF,'revision':final['receipt']['revision'],'task':TASK,'status':'review_pending','verification':ver},
      'sources_logs_rechecked':True,'scripts':[pin(p) for p in sorted(D.glob('*.py'))],
      'operational_receipts':[pin(D/f) for f in ['QUADRO_CLAIM.json','PREFLIGHT.json','PREFLIGHT_DELIVERY.json',
        'MAPA_RECIBO.json','MAPA_RECIBO_R2.json','QUADRO_ENTREGA.json','DEPOSITO_RECIBO.json','MISSION_SUBMIT.json','MATERIAL_TRANSITION.json','ACOM_VERIFY.json','MISSION_FINAL.json']],
      'preparation_notes':'Consulta NosVivo retornou unidade ausente no indice, preservada sem reconstruir grafo; fontes e mapa lidos diretamente. Erro de variavel no print final de prepare corrigido sem repetir mutacoes ja efetivadas. Registro ROTA recusado por identidade existente, sem escrita; substituido por ERRATA citando a seq anterior na mesma rota.',
      'not_done':r['not_done']})
    print(json.dumps({'delivery':pin(D/'ENCERRAMENTO.json'),'revision':final['receipt']['revision'],
      'event':board['evento'],'route_seq':route['gravados'][0]['seq'],'deposit_seq':dep['seq']},ensure_ascii=False))

if __name__=='__main__': {'register':register,'register_addendum':register_addendum,'deposit':deposit,'finish':finish}[sys.argv[1]]()
