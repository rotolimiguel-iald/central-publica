from pathlib import Path
import importlib.util, json, datetime, sys, hashlib, re

D = Path(__file__).resolve().parent
ROOT = D.parent
V = ROOT.parent
K = V.parent / 'v412/candidatas_kimi'
PRIOR = ROOT / 'CODEX_PONTE_COOK_LEVIN_R0'
spec = importlib.util.spec_from_file_location('review_tools', ROOT/'CODEX_TRINITY_R1/review.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
t.D = D
t.UNIT = 'F1.V413_REVISAO_PONTE_COOK_LEVIN_20261120'
t.TASK = 'releitura-custo-kimi'
pin, save, shell, mission = t.pin, t.save, t.shell, t.mission
PY, ACTOR, UNIT, TASK, REF = t.PY, t.ACTOR, t.UNIT, t.TASK, t.REF
ORDER = ROOT/'PEDIDO_DE_REVISAO_FINAL_AO_CODEX_v413_PONTE_COOK_LEVIN_TRINITY_R7_OPERADOR_R2_20nov.md'

def source(p):
    return {k:v for k,v in pin(p).items() if k in ('path','sha256')}

def prepare():
    original = 'work/cadeia_de_selo/v413/revisao_codex/PEDIDO_DE_REVISAO_FINAL_AO_CODEX_v413_PONTE_COOK_LEVIN_TRINITY_R7_OPERADOR_R2_20nov.md. não continua não o kimi pagou esse custo e provou isso, basta revisitar toda a pasta do kimi e ler as provas que estão lá'
    if (D/'PEDIDO_ATUAL.txt').exists():
        assert (D/'PEDIDO_ATUAL.txt').read_bytes()==original.encode()
    else:
        save('PEDIDO_ATUAL.txt', original)
    if not (D/'NOS_ANTES.json').exists():
        shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT], 'NOS_ANTES.json')
    nos=json.loads((D/'NOS_ANTES.json').read_text(encoding='utf-8'))
    assert nos['rc']==0 or (nos['rc']==1 and 'unidade não está no grafo' in nos['stderr'])
    save('NOS_LIMITE.json',{'status':'INDICE_SEM_UNIDADE' if nos['rc'] else 'OK',
        'evidence':pin(D/'NOS_ANTES.json'),'action':'Nao reconstruir grafo. Conferir fontes e recibos existentes diretamente e consultar Mapa. Ausencia no indice nao e ausencia de prova.'})
    assert shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Cook'], 'MAPA_ANTES.json').returncode == 0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Adendo de releitura do custo Kimi solicitado pelo operador; preservar entrega anterior.'], 'QUADRO_CLAIM.json').returncode == 0
    p = mission({'operation':'project'}, 'MISSION_INITIAL')
    mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'event_id':'releitura-custo-kimi-extend',
        'requirements':[{'id':TASK,'criterion':'Reler provas do Kimi sobre custo e corrigir eventual imprecisao do parecer final da Ponte, com fontes e limites exatos. Preservar originais e entregar adendo, sem instalar nem mover gate.','depends_on':[]}],
        'reason':'Operador contesta conclusao e pede releitura das provas existentes.',
        'sources':[source(D/'PEDIDO_ATUAL.txt'),source(ORDER)]}, 'MISSION_EXTEND')
    p = mission({'operation':'project'}, 'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'event_id':'releitura-custo-kimi-claim',
        'task_id':TASK,'lease_seconds':10800}, 'MISSION_CLAIM')
    p = mission({'operation':'project'}, 'MISSION_WORKING')
    req = next(x for x in p['projection']['active'] if x['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],
        'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':req['lease']['id']}, 'PREFLIGHT')['ready']
    files = sorted(p for p in K.rglob('*') if p.is_file() and p.suffix in ('.lean','.md','.json') and not any(x in p.parts for x in ('build','.lake')))
    save('INVENTARIO_KIMI.json', {'root':str(K),'files':[pin(p) for p in files], 'count':len(files),
        'note':'Inventario e pinos nao substituem leitura semantica; cobertura separada no resultado.'})
    receipts=[]
    for p in sorted(K.glob('RESULTADO_*.json')):
        r=json.loads(p.read_text(encoding='utf-8-sig'))
        item={'receipt':pin(p),'declared_rc':r.get('rc'),'declared_sorry':r.get('sorry'),'bindings':[]}
        for key, hkey in [('fonte','sha256_fonte'),('log','sha256_log'),('olean','sha256_olean')]:
            if key not in r: continue
            q=Path(r[key]); v={'field':key,'path':str(q),'exists':q.exists()}
            if q.exists():
                v.update(pin(q)); v['declared_hash']=r.get(hkey)
                v['matches_declared_hash']= v['sha256']==r[hkey] if hkey in r else None
            item['bindings'].append(v)
        receipts.append(item)
    save('RECIBOS_KIMI_CONFERIDOS.json',receipts)
    extras=[ORDER,PRIOR/'RESULTADO.json',PRIOR/'PARECER.md',PRIOR/'ENCERRAMENTO.json',
        V/'candidatas_c1/R0_ponte_cook_levin/PonteCookLevin.lean',
        ROOT/'CODEX_CONSOLIDADO_R3/RESULTADO.json', ROOT/'CODEX_CONSOLIDADO_R3/PARECER.md',
        Path('C:/t/k412c/final/TGLExt/AMaquinaEALeitura.lean'),Path('C:/t/k412c/final/TGLExt/AContagemEACarga.lean'),
        Path('C:/t/k412c/final/TGLExt/OPassoEOFim.lean'),Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md')]
    save('BASELINE.json',{'timestamp':datetime.datetime.now().astimezone().isoformat(),'reference':REF,'unit':UNIT,
        'task':TASK,'sources':[pin(p) for p in extras]})
    print(json.dumps({'ready':True,'revision':json.loads((D/'MISSION_WORKING.json').read_text(encoding='utf-8'))['result']['receipt']['revision'],'candidate_files':len(files),
        'receipts':len(receipts),'broken_bindings':[{'receipt':x['receipt']['path'],'binding':b} for x in receipts for b in x['bindings'] if not b['exists'] or b.get('matches_declared_hash') is False]},ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare}[sys.argv[1]]()
