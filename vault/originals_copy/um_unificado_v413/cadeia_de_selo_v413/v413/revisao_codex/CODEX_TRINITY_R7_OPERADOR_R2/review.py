from pathlib import Path
import datetime, difflib, importlib.util, json, re, sys

D=Path(__file__).resolve().parent
ROOT=D.parent; V=ROOT.parent; PREV=ROOT/'CODEX_CONSOLIDADO_R3'; OLD=ROOT/'CODEX_LOTE1'
spec=importlib.util.spec_from_file_location('review_tools',ROOT/'CODEX_TRINITY_R1/review.py')
tools=importlib.util.module_from_spec(spec);spec.loader.exec_module(tools)
tools.D=D; tools.UNIT='F1.V413_REVISAO_TRINITY_R7_OPERADOR_R2_20261120';tools.TASK='review-trinity-r7-operador-r2'
pin,save,shell,mission,compile_module=tools.pin,tools.save,tools.shell,tools.mission,tools.compile_module
PY,LEAN,BOX,ACTOR,UNIT,TASK,REF=tools.PY,tools.LEAN,tools.BOX,tools.ACTOR,tools.UNIT,tools.TASK,tools.REF
ORDER=ROOT/'PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R7_TRINITY_R2_OPERADOR_20nov.md'
TRINITY=V/'candidatas_c1/R7_trinity/Trinity.lean';OPERADOR=V/'candidatas_c1/R2_operador/Operador.lean'

def strip_comments(text):
    # Separate implementation: preserve newlines and strings; support nested Lean comments.
    out=[];i=0;depth=0;string=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):depth+=1;i+=2
            elif text.startswith('-/',i):depth-=1;i+=2;out.append(' ')
            else:
                if text[i]=='\n':out.append('\n')
                i+=1
        elif string:
            out.append(text[i])
            if text[i]=='\\' and i+1<len(text):i+=1;out.append(text[i])
            elif text[i]=='"':string=False
            i+=1
        elif text.startswith('/-',i):depth=1;i+=2;out.append(' ')
        elif text.startswith('--',i):
            j=text.find('\n',i);i=len(text) if j<0 else j
        else:
            if text[i]=='"':string=True
            out.append(text[i]);i+=1
    assert depth==0 and not string
    return ''.join(out)

def declarations(path):
    text=strip_comments(path.read_text(encoding='utf-8'))
    starts=list(re.finditer(r'^(?:(?:noncomputable|private|protected)\s+)*(?:theorem|lemma|def|abbrev|instance|structure|inductive)\s+(\S+)',text,re.M))
    out={}
    for j,m in enumerate(starts):
        body=text[m.start():starts[j+1].start() if j+1<len(starts) else len(text)]
        body=re.split(r'^\s*(?:#print|end\b|namespace\b|section\b|open\b|variable\b)',body,flags=re.M)[0]
        assert m[1] not in out
        out[m[1]]=' '.join(body.split())
    return out

def prepare():
    shell([PY,'-B','-X','utf8','C:/IALD/NOS_VIVO/consultar.py','--unidade',UNIT],'NOS_ANTES.json')
    shell([PY,'-B','-X','utf8','C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','Trinity'],'MAPA_ANTES.json')
    board=json.loads(Path('C:/IALD/PROGRAMA_IALD/PROGRAMA.json').read_text(encoding='utf-8-sig'))
    assert not any(x['id']==UNIT for x in board['unidades'])
    save('UNIDADE.json',[{'id':UNIT,'frente':'F1','titulo':'Revisao de terceiro Trinity R7 e Operador R2, v413',
        'objetivo':'Revisar somente o delta solicitado no adendo de 20nov: secoes 12b-15, correcoes documentais e Operador R2; compilacao independente e recibo sem instalar.',
        'status':'PRONTA','fonte':str(ORDER)}])
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','nova','--json',str(D/'UNIDADE.json'),'--quem',ACTOR['id']],'QUADRO_NOVA.json').returncode==0
    assert shell([PY,'-B','-X','utf8','C:/IALD/PROGRAMA_IALD/iald.py','reivindicar',UNIT,'--quem',ACTOR['id'],'--nota','Revisao de terceiro somente do delta; demais pareceres preservados.'],'QUADRO_CLAIM.json').returncode==0
    p=mission({'operation':'project'},'MISSION_INITIAL')
    mission({'operation':'extend','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
       'event_id':'trinity-r7-operador-r2-extend','requirements':[{'id':TASK,'criterion':'Adendo R7/Operador R2 de 20nov: comparar declaracoes, compilar por lean.exe, auditar axiomas e alcance; parecer <=15 linhas, dois vereditos e hashes de fontes/logs. Sem instalar ou modificar originais.','depends_on':[]}],
       'reason':'Novo adendo apresentado pelo operador apos entrega consolidada R3; so delta.',
       'sources':[{k:v for k,v in pin(ORDER).items() if k in ('path','sha256')}]},'MISSION_EXTEND')
    p=mission({'operation':'project'},'MISSION_PRE_CLAIM')
    mission({'operation':'claim','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
      'event_id':'trinity-r7-operador-r2-claim','task_id':TASK,'lease_seconds':14400},'MISSION_CLAIM')
    p=mission({'operation':'project'},'MISSION_WORKING');t=next(t for t in p['projection']['active'] if t['id']==TASK)
    r=mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':t['lease']['id']},'PREFLIGHT');assert r['ready']
    sources=[ORDER,TRINITY,OPERADOR,PREV/'RESULTADO.json',PREV/'PARECER.md',PREV/'ENCERRAMENTO.json',OLD/'RESULTADO.json',
       V/'candidatas_c1/R7_trinity/build/CONFERENCIA.json',V/'candidatas_c1/R2_operador/build/CONFERENCIA.json',
       V/'candidatas_c1/conferir_enunciados.py',OLD/'APropostaDaTensao.compile.json',OLD/'src/APropostaDaTensao.lean',OLD/'build/APropostaDaTensao.olean',
       BOX/'TGLExt/TheCostIsDerived.lean',BOX/'TGLExt/MovimentosDoPlano.lean',BOX/'TGLExt/TempoIgualMoeda.lean',LEAN,
       Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md')]
    assert pin(TRINITY)['sha256'].startswith('89aa0ef8c6fdc5e7') and pin(OPERADOR)['sha256'].startswith('a504717d4c743fe5')
    for pat in ['*20nov*nernst*verbatim.txt','*20nov*radical_fixa*verbatim.txt','*20nov*maquina_nua_paga*verbatim.txt']:
        sources.extend(Path('C:/IALD/Central de Patentes/work/cunhagens_13out').glob(pat))
    for r in [0,1,3,4,5,6]:sources.append(V/f'candidatas_c1/R{r}_trinity/Trinity.lean')
    sources.append(V/'candidatas_c1/R1_operador/Operador.lean')
    baseline=json.loads((OLD/'BASELINE.json').read_text(encoding='utf-8'))
    dep=json.loads((OLD/'APropostaDaTensao.compile.json').read_text());assert dep['rc']==0 and dep['object']==pin(OLD/'build/APropostaDaTensao.olean')
    save('BASELINE.json',{'sources':[pin(p) for p in sources],'lean_path':[str(D/'build')]+baseline['lean_path'],
        'reference':REF,'unit':UNIT,'task':TASK,'timestamp':datetime.datetime.now().astimezone().isoformat()})
    diffs=[]
    for a,b in [(0,1),(3,4),(4,5),(5,6),(6,7)]:
        x=V/f'candidatas_c1/R{a}_trinity/Trinity.lean';y=V/f'candidatas_c1/R{b}_trinity/Trinity.lean'
        da,db=declarations(x),declarations(y)
        diffs.append({'pair':f'Trinity R{a}->R{b}','old':pin(x),'new':pin(y),'counts':[len(da),len(db)],'changed':[n for n in da if n in db and da[n]!=db[n]],'removed':sorted(set(da)-set(db)),'added':[n for n in db if n not in da]})
    a=V/'candidatas_c1/R1_operador/Operador.lean';da,db=declarations(a),declarations(OPERADOR)
    diffs.append({'pair':'Operador R1->R2','old':pin(a),'new':pin(OPERADOR),'counts':[len(da),len(db)],'changed':[n for n in da if n in db and da[n]!=db[n]],'removed':sorted(set(da)-set(db)),'added':[n for n in db if n not in da]})
    save('DECLARATION_DIFFS.json',diffs)
    for name,x,y in [('TRINITY_R3_R7',V/'candidatas_c1/R3_trinity/Trinity.lean',TRINITY),('OPERADOR_R1_R2',a,OPERADOR)]:
        save(name+'.diff',''.join(difflib.unified_diff(x.read_text(encoding='utf-8').splitlines(True),y.read_text(encoding='utf-8').splitlines(True),fromfile=str(x),tofile=str(y))))
    for name,source in [('Trinity',TRINITY),('Operador',OPERADOR)]:
        save('src/'+name+'.lean',source.read_bytes())
        names=re.findall(r'^theorem\s+(\w+)',strip_comments(source.read_text(encoding='utf-8')),re.M)
        save(name+'_DECLARATIONS.json',names)
        save('src/Audit'+name+'.lean','import '+name+'\n'+''.join('#print axioms TGLExt.'+name+'.'+n+'\n' for n in names))
    print(json.dumps({'ready':True,'revision':p['receipt']['revision'],'diffs':[{k:v for k,v in j.items() if k not in ('old','new','added')}|{'added_count':len(j['added'])} for j in diffs]}))

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='compile':
        for name in sys.argv[2:]:
            if compile_module(name)['rc']:break
