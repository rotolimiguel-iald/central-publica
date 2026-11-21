from pathlib import Path
import importlib.util, json, datetime, sys, re, difflib

D=Path(__file__).resolve().parent
ROOT=D.parent; V=ROOT.parent; I=V/'insumos'
spec=importlib.util.spec_from_file_location('review_tools',ROOT/'CODEX_TRINITY_R1/review.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
t.D=D;t.UNIT='F1.V413_REVISAO_PEDRAS_LIMPAS_20261120';t.TASK='review-pedras-limpas-v413'
pin,save,shell=t.pin,t.save,t.shell
def mission(req,name,script='mission_cli.py'):
    if req['operation']=='project' and script=='mission_cli.py': req=dict(req,max_chars=60000)
    return t.mission(req,name,script)
PY,ACTOR,UNIT,TASK,REF=t.PY,t.ACTOR,t.UNIT,t.TASK,t.REF
ORDER=ROOT/'PEDIDO_DE_LEITURA_DAS_PEDRAS_LIMPAS_v413_20nov.md'

def source(p): return {k:v for k,v in pin(p).items() if k in ('path','sha256')}

def prepare():
    shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_ANTES.json')
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','limpeza'],'MAPA_ANTES.json')
    board=json.loads(Path('C:/IALD/PROGRAMA_IALD/PROGRAMA.json').read_text(encoding='utf-8-sig'))
    assert not any(x['id']==UNIT for x in board['unidades'])
    save('UNIDADE.json',[{'id':UNIT,'frente':'F1','titulo':'Revisao de terceiro da limpeza documental das pedras v413',
      'objetivo':'Comparar texto de21modulos e errata OResumoEPsiBit com origens, preservar codigo/localizadores/estatutos e conferir correcao das ressalvas; sem instalar.',
      'status':'PRONTA','fonte':str(ORDER)}])
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','nova','--json',str(D/'UNIDADE.json'),'--quem',ACTOR['id']],'QUADRO_NOVA.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Leitura documental de terceiro; provas ja conferidas preservadas, sem instalacao.'],'QUADRO_CLAIM.json').returncode==0
    p=mission({'operation':'project'},'MISSION_INITIAL')
    mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'pedras-limpas-v413-extend','requirements':[{'id':TASK,'criterion':'Pedido pedras limpas:21modulos e errata OResumoEPsiBit; comparar texto/codigo/localizadores/estatutos; vereditos por modulo, texto proposto se ressalva, relatorio <=15linhas e hashes. Sem recompilacao desnecessaria ou instalacao.','depends_on':[]}],
      'reason':'Pedido humano posterior de leitura das pedras na forma final do kernel.', 'sources':[source(ORDER)]},'MISSION_EXTEND')
    resume()

def resume():
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM_R2')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'pedras-limpas-v413-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING');task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT')['ready']
    m=json.loads((I/'MANIFESTO_PEDRAS_v413.json').read_text(encoding='utf-8-sig'))
    inputs=[ORDER,I/'MANIFESTO_PEDRAS_v413.json',I/'REGRAS_DA_LIMPEZA_v413.md',I/'DIFF_DA_LIMPEZA_v413.txt',
      I/'kernel_edits/ERRATA_OResumoEPsiBit.json', ROOT/'CODEX_CONSOLIDADO_R3/PARECER.md',ROOT/'CODEX_CONSOLIDADO_R3/RESULTADO.json',
      ROOT/'CODEX_PONTE_COOK_LEVIN_R0/RESULTADO.json',ROOT/'CODEX_RELEITURA_CUSTO_KIMI/RESULTADO.json',
      ROOT/'CODEX_TRINITY_R7_OPERADOR_R2/RESULTADO.json',V.parent/'v412/verificar_historia_nas_pedras.py']
    mismatch=[]; modules=[]
    for name,v in m['modulos_novos'].items():
        short=name.removeprefix('TGLExt.')
        clean=Path(v['pedra_limpa']);orig=I/'origem/TGLExt'/clean.name;prev=Path(v['fonte_revisada'])
        for path,expected in [(clean,v['sha256_pedra_limpa']),(orig,v['sha256_origem']),(prev,v['sha256_fonte_revisada'])]:
            inputs.append(path)
            if pin(path)['sha256']!=expected: mismatch.append({'path':str(path),'expected':expected,'actual':pin(path)})
        modules.append({'module':name,'clean':pin(clean),'origin':pin(orig),'reviewed_source':pin(prev),'author':v['autor_da_construcao']})
        save('diffs/'+short+'.diff',''.join(difflib.unified_diff(orig.read_text(encoding='utf-8').splitlines(True),clean.read_text(encoding='utf-8').splitlines(True),fromfile=str(orig),tofile=str(clean))))
    for k,v in m['kernel_corrigido'].items():
        for path,h in [(v['origem'],v['sha256_origem']),(v['saida'],v['sha256_saida'])]:
            inputs.append(Path(path))
            if pin(path)['sha256']!=h:mismatch.append({'path':path,'expected':h,'actual':pin(path)})
    for v in m['recibos'].values():
        path=Path(v['caminho']);inputs.append(path)
        if pin(path)['sha256']!=v['sha256']:mismatch.append({'path':str(path),'expected':v['sha256'],'actual':pin(path)})
    save('BASELINE.json',{'timestamp':datetime.datetime.now().astimezone().isoformat(),'reference':REF,'unit':UNIT,'task':TASK,
      'sources':[pin(x) for x in sorted(set(inputs))],'modules':modules,'manifest_mismatches':mismatch})
    print(json.dumps({'ready':True,'revision':p['receipt']['revision'],'modules':len(modules),'manifest_mismatches':mismatch},ensure_ascii=False))

if __name__=='__main__': {'prepare':prepare,'resume':resume}[sys.argv[1]]()
