from pathlib import Path
import importlib.util, json, sys, datetime, re
D=Path(__file__).resolve().parent
ROOT=D.parent; V=ROOT.parent
spec=importlib.util.spec_from_file_location('prior_tools',ROOT/'CODEX_TRINITY_R1/review.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
t.D=D;t.UNIT='F1.V413_REVISAO_PONTE_COOK_LEVIN_20261120';t.TASK='review-ponte-cook-levin-r0'
pin,save,shell,mission,compile_module=t.pin,t.save,t.shell,t.mission,t.compile_module
PY,LEAN,BOX,ACTOR,UNIT,TASK,REF=t.PY,t.LEAN,t.BOX,t.ACTOR,t.UNIT,t.TASK,t.REF
ORDER=ROOT/'PEDIDO_DE_REVISAO_FINAL_AO_CODEX_v413_PONTE_COOK_LEVIN_TRINITY_R7_OPERADOR_R2_20nov.md'
SRC=V/'candidatas_c1/R0_ponte_cook_levin/PonteCookLevin.lean'
CONF=V/'conferencia_c1_codex/k412c'
PREV=ROOT/'CODEX_TRINITY_R7_OPERADOR_R2'

def prepare():
    shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_ANTES.json')
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Cook'],'MAPA_ANTES.json')
    board=json.loads(Path('C:/IALD/PROGRAMA_IALD/PROGRAMA.json').read_text(encoding='utf-8-sig'))
    assert not any(x['id']==UNIT for x in board['unidades'])
    save('UNIDADE.json',[{'id':UNIT,'frente':'F1','titulo':'Revisao final de terceiro Ponte Cook-Levin R0, v413',
       'objetivo':'Conferir fiacao, classes, hipotese CookLevin, semantica e axiomas; reutilizar Trinity R7 e Operador R2 por hashes; sem instalar.',
       'status':'PRONTA','fonte':str(ORDER)}])
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','nova','--json',str(D/'UNIDADE.json'),'--quem',ACTOR['id']],'QUADRO_NOVA.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Revisao final de terceiro da candidata c1, sem refazer os hashes ja auditados.'],'QUADRO_CLAIM.json').returncode==0
    p=mission({'operation':'project'},'MISSION_INITIAL')
    mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'ponte-cook-levin-r0-extend','requirements':[{'id':TASK,'criterion':'Pedido final v413: PonteCookLevin R0; revisar hipotese, enunciados/docstrings, compilar e auditar axiomas; reutilizar dois pareceres por hash. Relatorio <=15 linhas e recibo completo; sem instalar.','depends_on':[]}],
      'reason':'Pedido final apresentado pelo operador, com nova candidata c1.', 'sources':[{k:v for k,v in pin(ORDER).items() if k in ('path','sha256')}]},'MISSION_EXTEND')
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'ponte-cook-levin-r0-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING');task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT')['ready']
    rec=json.loads((SRC.parent/'build/CONFERENCIA.json').read_text(encoding='utf-8'))
    assert rec['bom'] and rec['sha256']==pin(SRC)['sha256'] and pin(SRC)['sha256'].startswith('1594fa49275173f9')
    for name,sha in rec['importa'].items(): assert pin(CONF/'build'/name)['sha256']==sha
    for name,prefix in [('build/CONFERENCIA.json','ff908a4434d4bc31'),('compilar.py','fbd76f61a5aa7801')]:assert pin(SRC.parent/name)['sha256'].startswith(prefix)
    prev=json.loads((PREV/'RESULTADO.json').read_text(encoding='utf-8'))
    reuse=[]
    for path in [V/'candidatas_c1/R7_trinity/Trinity.lean',V/'candidatas_c1/R2_operador/Operador.lean']:
        old=next(s for s in prev['sources'] if Path(s['path'])==path);assert pin(path)==old;reuse.append(old)
    sources=[ORDER,SRC,SRC.parent/'compilar.py',SRC.parent/'build/CONFERENCIA.json',CONF/'CONFERENCIA_K412C.json',CONF/'AXIOMAS_K412C.json',
      PREV/'RESULTADO.json',PREV/'PARECER.md',PREV/'ENCERRAMENTO.json',ROOT/'CODEX_CONSOLIDADO_R3/PARECER.md',LEAN,
      BOX/'TGLExt/TraducaoTuring.lean',BOX/'TGLExt/F1Fecho394/CanonicalFockModularCoreInputR1.lean',
      BOX/'.lake/packages/mathlib/Mathlib/Computability/TuringMachine/Computable.lean',
      BOX/'.lake/packages/mathlib/Mathlib/Computability/TuringMachine/StackTuringMachine.lean']
    sources += [Path(s['path']) for s in reuse]
    sources += sorted((CONF/'build').glob('*.olean'))+sorted((CONF/'src').glob('*.lean'))
    save('BASELINE.json',{'sources':[pin(p) for p in sources],'lean_path':[str(D/'build')]+rec['lean_path'][:-1],
      'reference':REF,'unit':UNIT,'task':TASK,'timestamp':datetime.datetime.now().astimezone().isoformat(),'reused_candidates':reuse})
    save('ATLAS_CONTEXT_PIN.json',pin('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md'))
    save('src/PonteCookLevin.lean',SRC.read_bytes())
    print(json.dumps({'ready':True,'revision':p['receipt']['revision'],'sources':len(sources),'reused_candidates':reuse}))

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='compile':
        for name in sys.argv[2:]:
            if compile_module(name)['rc']:break
