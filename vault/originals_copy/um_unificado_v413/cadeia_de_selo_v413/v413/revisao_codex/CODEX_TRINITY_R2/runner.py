from pathlib import Path
import datetime, difflib, hashlib, importlib.util, json, os, re, subprocess, sys

D=Path(__file__).resolve().parent
PREV=D.parent/'CODEX_TRINITY_R1'
# Reuse the previous audit's immutable tooling, changing only its in-process targets.
spec=importlib.util.spec_from_file_location('trinity_review_tools',PREV/'review.py')
tools=importlib.util.module_from_spec(spec);spec.loader.exec_module(tools)
tools.D=D; tools.SRC=D.parents[1]/'candidatas_c1/R2_trinity/Trinity.lean'
tools.UNIT='F1.V413_REVISAO_TRINITY_R2_20261120';tools.TASK='review-trinity-r2'
pin,save,shell,mission,compile_module=tools.pin,tools.save,tools.shell,tools.mission,tools.compile_module
SRC,V,OLD,REF,PY,LEAN,BOX,ACTOR,UNIT,TASK=tools.SRC,tools.V,tools.OLD,tools.REF,tools.PY,tools.LEAN,tools.BOX,tools.ACTOR,tools.UNIT,tools.TASK

def statements(text):
    matches=list(re.finditer(r'^theorem\s+(\w+)\b',text,re.M)); result={}
    for i,m in enumerate(matches):
        chunk=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)]
        marker=re.search(r':=|^\s*\|',chunk,re.M); assert marker,m.group(1)
        result[m.group(1)]=' '.join(chunk[:marker.start()].split())
    return result

def prepare():
    sources=[SRC,V/'candidatas_c1/R1_trinity/Trinity.lean',V/'candidatas_c1/R2_trinity/build/CONFERENCIA.json',
     D.parent/'ADENDO_3_AO_PEDIDO_DE_REVISAO_TRINITY_R2_20nov.md',
     D.parent/'ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md',D.parent/'ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md',
     D.parent/'PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md',
     PREV/'RESULTADO.json',PREV/'ENCERRAMENTO.json',PREV/'review.py',PREV/'src/CheckTrinityR2.lean',
     OLD/'BASELINE.json',OLD/'APropostaDaTensao.compile.json',OLD/'src/APropostaDaTensao.lean',OLD/'build/APropostaDaTensao.olean',
     BOX/'TGLExt/CompilaHornNaFita.lean',BOX/'lean-toolchain',LEAN,
     LEAN.parents[1]/'src/lean/Init/Prelude.lean']
    pins=[pin(p) for p in sources]
    assert pins[0]['sha256'].startswith('97e78d6417e84091')
    assert pins[2]['sha256'].startswith('7962c359b1350620')
    prev=json.loads((PREV/'RESULTADO.json').read_text())
    assert pin(sources[1])==prev['source']
    dep=json.loads((OLD/'APropostaDaTensao.compile.json').read_text())
    assert dep['rc']==0 and pin(OLD/'build/APropostaDaTensao.olean')==dep['object']
    base=json.loads((OLD/'BASELINE.json').read_text())
    assert pin(OLD/'src/APropostaDaTensao.lean')==base['sources'][4]['copy']
    lp=[str(D/'build')]+base['lean_path']
    save('BASELINE.json',{'sources':pins,'lean_path':lp,'reference':REF,'unit':UNIT,'task':TASK,'timestamp':datetime.datetime.now().astimezone().isoformat()})
    shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_CONSULTA.json')
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Trinity'],'MAPA_ANTES.json')
    board=json.loads(Path('C:/IALD/PROGRAMA_IALD/PROGRAMA.json').read_text(encoding='utf-8-sig'))
    assert UNIT not in json.dumps(board)
    save('UNIDADE.json',[{'id':UNIT,'frente':'F1','titulo':'Revisao de terceiro Trinity R2, item 9 v413',
     'objetivo':'Adendo 3: revisar fronteira, sublistas e travessia completa com cota exponencial; reutilizar R1 intacta, sem instalar.',
     'status':'PRONTA','fonte':str(sources[3])}])
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','nova','--json',str(D/'UNIDADE.json'),'--quem',ACTOR['id']],'QUADRO_NOVA.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Revisao independente de c1, delta R2. Originais preservados.'],'QUADRO_CLAIM.json').returncode==0
    p=mission({'operation':'project'},'MISSION_INITIAL')
    mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
     'event_id':'trinity-r2-extend','requirements':[{'id':TASK,'criterion':'Revisar delta R2 do item9 segundo Adendo3: fronteira, Dentro, travessia, custo; compilar/axiomas completos e entregar parecer curto com hashes. Nao repetir lote1/R1 ou instalar.','depends_on':[]}],
     'reason':'Adendo3 apresentado pelo operador substitui item9 por R2.',
     'sources':[{k:v for k,v in pin(sources[3]).items() if k in ('path','sha256')}]},'MISSION_EXTEND')
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
     'event_id':'trinity-r2-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING')
    task=next(t for t in p['projection']['active'] if t['id']==TASK)
    ready=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
     'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT')
    assert ready['ready']
    save('src/Trinity.lean',SRC.read_bytes())
    a=sources[1].read_text(encoding='utf-8');b=SRC.read_text(encoding='utf-8')
    save('R1_R2.diff',''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='R1',tofile='R2')))
    sa,sb=statements(a),statements(b)
    save('STATEMENT_DIFF.json',{'old_count':len(sa),'new_count':len(sb),'changed':[n for n in sa if n in sb and sa[n]!=sb[n]],
     'added':sorted(set(sb)-set(sa)),'removed':sorted(set(sa)-set(sb)),'method':'Header before := or first equation branch, whitespace normalized. Byte diff preserved.'})
    names=list(sb)
    save('DECLARATIONS.json',{'names':names,'count':len(names)})
    save('src/AuditTrinity.lean','import Trinity\n'+''.join('#print axioms TGLExt.Trinity.'+n+'\n' for n in names))
    print(json.dumps({'ready':True,'theorems':len(names),'new':len(set(sb)-set(sa)),'changed':[n for n in sa if sa[n]!=sb.get(n)]}))

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='compile':
        for name in sys.argv[2:]:
            r=compile_module(name)
            if r['rc']:break
