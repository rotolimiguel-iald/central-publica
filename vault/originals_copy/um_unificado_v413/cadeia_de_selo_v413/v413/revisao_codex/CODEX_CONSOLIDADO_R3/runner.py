from pathlib import Path
import datetime, difflib, hashlib, importlib.util, json, os, re, subprocess, sys

D=Path(__file__).resolve().parent
PREV=D.parent/'CODEX_TRINITY_R1';R2=D.parent/'CODEX_TRINITY_R2';OLD=D.parent/'CODEX_LOTE1'
spec=importlib.util.spec_from_file_location('trinity_tools',PREV/'review.py')
tools=importlib.util.module_from_spec(spec);spec.loader.exec_module(tools)
tools.D=D;tools.SRC=D.parents[1]/'candidatas_c1/R3_trinity/Trinity.lean'
# Preserve the ongoing requirement and board identity; the consolidated request
# replaces its criterion explicitly through the existing amendment protocol.
tools.UNIT='F1.V413_REVISAO_TRINITY_R2_20261120';tools.TASK='review-trinity-r2'
pin,save,shell,mission,compile_module=tools.pin,tools.save,tools.shell,tools.mission,tools.compile_module
SRC,V,REF,PY,LEAN,BOX,ACTOR,UNIT,TASK=tools.SRC,tools.V,tools.REF,tools.PY,tools.LEAN,tools.BOX,tools.ACTOR,tools.UNIT,tools.TASK
ORDER=D.parent/'PEDIDO_DE_REVISAO_AO_CODEX_v413_CONSOLIDADO_20nov.md'

def statements(text):
    matches=list(re.finditer(r'^theorem\s+(\w+)\b',text,re.M));out={}
    for i,m in enumerate(matches):
        chunk=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)]
        z=re.search(r':=|^\s*\|',chunk,re.M);assert z
        out[m.group(1)]=' '.join(chunk[:z.start()].split())
    return out

def prepare():
    prev=json.loads((OLD/'RESULTADO.json').read_text(encoding='utf-8'))
    for item in prev['items']:
        assert pin(item['source']['path'])==item['source']
        assert pin(item['compiled_copy']['path'])==item['compiled_copy']
    for log in prev['logs']:assert pin(log['path'])==log
    save('REUSO_LOTE1.json',{'receipt':pin(OLD/'RESULTADO.json'),'closing':pin(OLD/'ENCERRAMENTO.json'),
        'all_eight_sources_copies_logs_identical':True,'items':[{'item':i['item'],'verdict':i['verdict'],'source':i['source']} for i in prev['items']]})
    sources=[SRC,ORDER,V/'candidatas_c1/R3_trinity/build/CONFERENCIA.json',
        V/'candidatas_c1/R2_trinity/Trinity.lean',V/'candidatas_c1/R1_trinity/Trinity.lean',
        OLD/'RESULTADO.json',OLD/'ENCERRAMENTO.json',PREV/'RESULTADO.json',PREV/'ENCERRAMENTO.json',
        OLD/'src/APropostaDaTensao.lean',OLD/'build/APropostaDaTensao.olean',OLD/'APropostaDaTensao.compile.json',
        PREV/'src/CheckTrinityR2.lean',R2/'Trinity.compile.json',R2/'AuditTrinity.compile.json',R2/'CheckR2.compile.json',R2/'src/CheckR2.lean',
        BOX/'TGLExt/CorteDosPares.lean',BOX/'TGLExt/MovimentosDoPlano.lean',LEAN,LEAN.parents[1]/'src/lean/Init/Prelude.lean',PREV/'review.py']
    pins=[pin(p) for p in sources]
    assert pins[0]['sha256'].startswith('8f5f5e07bcb54beb') and pins[2]['sha256'].startswith('8afbc4ae210163ba')
    dep=json.loads((OLD/'APropostaDaTensao.compile.json').read_text());assert dep['rc']==0 and dep['object']==pin(sources[10])
    b=json.loads((OLD/'BASELINE.json').read_text())
    save('BASELINE.json',{'sources':pins,'lean_path':[str(D/'build')]+b['lean_path'],'reference':REF,'unit':UNIT,'task':TASK,
        'superseding_request':pin(ORDER),'timestamp':datetime.datetime.now().astimezone().isoformat()})
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Trinity'],'MAPA_ANTES.json')
    p=mission({'operation':'project'},'MISSION_INITIAL')
    mission({'operation':'amend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-consolidado-r3-amend','task_id':TASK,
      'criterion':'Pedido consolidado de 20nov: revisar nove itens, reusar lote1 e R1/R2 por hashes; item9 agora Trinity R3, delta sobre fronteira e lista de Nomes. Entregar 9 vereditos, parecer <=15 linhas e JSON de fontes/logs. Sem instalar ou editar fontes.',
      'reason':'Pedido consolidado apresentado pelo operador durante a revisao R2 substitui os pedidos/adendos. Mantida identidade da tarefa e trilha, sem revisao duplicada.',
      'sources':[{k:v for k,v in pin(ORDER).items() if k in ('path','sha256')}]},'MISSION_AMEND')
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-consolidado-r3-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    r=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'task_id':TASK,'lease_id':t['lease']['id']},'PREFLIGHT');assert r['ready']
    note={'fonte':str(ORDER),'objeto_atual':'Revisao consolidada v413; item9 Trinity R3','continuidade':'Unidade/R2 mantida, escopo substituido pelo pedido consolidado. Nao refazer itens1-8.'}
    shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','anotar','--quem',ACTOR['id'],'--tipo','ESCOPO_ATUALIZADO','--unidade',UNIT,'--dados',json.dumps(note,ensure_ascii=False)],'QUADRO_ADENDO.json')
    save('src/Trinity.lean',SRC.read_bytes())
    sa=statements(sources[3].read_text(encoding='utf-8'));sb=statements(SRC.read_text(encoding='utf-8'))
    save('STATEMENT_DIFF.json',{'old_count':len(sa),'new_count':len(sb),'changed':[n for n in sa if sa[n]!=sb.get(n)],'added':sorted(set(sb)-set(sa)),'removed':sorted(set(sa)-set(sb))})
    save('R2_R3.diff',''.join(difflib.unified_diff(sources[3].read_text(encoding='utf-8').splitlines(True),SRC.read_text(encoding='utf-8').splitlines(True),fromfile='R2',tofile='R3')))
    save('DECLARATIONS.json',{'names':list(sb),'count':len(sb)})
    save('src/AuditTrinity.lean','import Trinity\n'+''.join('#print axioms TGLExt.Trinity.'+n+'\n' for n in sb))
    save('src/CheckPriorInstrumentation.lean',(PREV/'src/CheckTrinityR2.lean').read_bytes())
    probe=(R2/'src/CheckR2.lean').read_text(encoding='utf-8')
    probe=probe.replace('next l hs =>\n          obtain','next l hs =>\n          simp only [hs]\n          obtain')
    probe=probe.replace('        · split\n          · simp\n          · next l ls hls =>','        · next hs =>\n          simp only [hs]\n          split\n          · next hfl => simp [hfl]\n          · next l ls hls =>\n            simp only [hls]')
    save('src/CheckR2Final.lean',probe)
    print(json.dumps({'ready':True,'theorems':len(sb),'new':len(set(sb)-set(sa)),'reused_items':8}))

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='compile':
        for name in sys.argv[2:]:
            if compile_module(name)['rc']:break
