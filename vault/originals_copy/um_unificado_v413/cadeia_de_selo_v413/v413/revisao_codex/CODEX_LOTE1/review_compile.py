from pathlib import Path
import concurrent.futures, hashlib, json, os, re, subprocess, time

D = Path(__file__).resolve().parent
V = D.parents[1]
K = V.parent / 'v412/candidatas_kimi'
BOX = Path('C:/t/k412c/final')
G = V / 'conferencia_c1_codex/k412c'
LEAN = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def save(name,obj):
    p=D/name
    assert not p.exists(),p
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
for name in ['src','build','logs']:(D/name).mkdir(exist_ok=True)
items=[
 (1,V/'candidatas_c1/R1_operador/Operador.lean','de75489028428754'),
 (2,V/'conferencia_c1_codex/fronteira/AFronteiraNaLinguaClassica.lean','5db57faeff22e4c6'),
 (3,V/'conferencia_c1_codex/sonda_contagem/SondaContagem.lean','2e85629ffb764a4a'),
 (4,K/'AIdentidadePreservada.lean','1ee6e6383f23b656'),
 (5,K/'APropostaDaTensao.lean','95be88472a0609d8'),
 (6,K/'APonteDeCookLevin.lean','0b95795836d25854'),
 (7,K/'ONomeEBeta.lean','fa026cb786d27291'),
 (8,BOX/'TGLExt/OResumoEPsiBit.lean','75c1ef6b0de9f7d4')]
sources=[]
for i,p,short in items:
    original=pin(p);assert original['sha256'].startswith(short),(p,original)
    raw=p.read_bytes();new=raw;changes=[]
    if i in [4,5,6,7]:
        for mod in ['AContagemEACarga','AMaquinaEALeitura','OPassoEOFim','CamadaCientifica']:
            before=('import '+mod).encode();after=('import TGLExt.'+mod).encode()
            lines=new.splitlines(keepends=True)
            for no,line in enumerate(lines,1):
                if line.rstrip(b'\r\n')==before:
                    lines[no-1]=after+line[len(before):];changes.append({'line':no,'before':before.decode(),'after':after.decode()})
            new=b''.join(lines)
    dst=D/'src'/p.name;assert not dst.exists();dst.write_bytes(new)
    sources.append({'item':i,'original':original,'copy':pin(dst),'import_changes':changes})

# Reuse the already compiled, excluded Codex dependencies from the v412 box review.
# This is dependency custody, not a new semantic approval of Codex's own modules.
receipt=json.loads((G/'CONFERENCIA_K412C.json').read_text(encoding='utf-8'))
records={r['modulo']:r for r in receipt['modulos']}
deps=['APonteAoTM2','AMaquinaTM2DaVerificacao','SimBase','SimLiteral','SimExterior','SimCompleta',
      'RelogioBeta','LeituraBeta','QuantizacaoBeta','Reconstrucao','PonteLeituraBeta','EntregaBeta']
dependency_pins=[]
for name in deps:
    rec=records[name];p=Path(rec['fonte']);sp=pin(p)
    assert sp['sha256']==rec['sha256_fonte'] and rec['rc']==0,rec
    obj=G/'build'/(name+'.olean');dst=D/'build'/obj.name
    assert not dst.exists();dst.write_bytes(obj.read_bytes())
    dependency_pins.append({'module':name,'source':sp,'object_original':pin(obj),'object_copy':pin(dst),'prior_receipt':str(G/'CONFERENCIA_K412C.json'),'status':'REUSED_DEPENDENCY_NOT_REVIEWED_HERE'})
lp=[BOX/'.lake/build/lib/lean']+sorted(p for p in (BOX/'.lake/packages').glob('*/.lake/build/lib/lean') if p.is_dir())+[D/'build']
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,lp))
save('BASELINE.json',{'sources':sources,'dependencies':dependency_pins,'prior_receipt':pin(G/'CONFERENCIA_K412C.json'),'lean':pin(LEAN),'toolchain':pin(BOX/'lean-toolchain'),'lean_path':list(map(str,lp))})
def compile_one(source):
    src=Path(source['copy']['path']);name=src.stem
    cmd=[str(LEAN),'-j','2','-o',str(D/'build'/(name+'.olean')),src.name]
    start=time.monotonic();r=subprocess.run(cmd,cwd=D/'src',env=env,capture_output=True)
    out=D/'logs'/(name+'.log');out.write_bytes(r.stdout+r.stderr)
    txt=out.read_text(encoding='utf-8',errors='strict')
    entries=[]
    for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",txt,re.S):
        entries.append({'declaration':m.group(1),'axioms':[a.strip() for a in (m.group(2) or '').split(',') if a.strip()]})
    outside=sorted({a for e in entries for a in e['axioms'] if a not in {'propext','Classical.choice','Quot.sound'}})
    result={'item':source['item'],'module':name,'command':cmd,'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'log':pin(out),'axiom_reports':entries,'outside_trio':outside,'warning':bool(re.search(r'\bwarning:',txt)),'sorryAx':'sorryAx' in txt,'source_unchanged':pin(Path(source['original']['path']))==source['original']}
    obj=D/'build'/(name+'.olean')
    if obj.exists():result['object']=pin(obj)
    save(name+'.compile.json',result)
    print(json.dumps({k:result[k] for k in ['item','module','rc','seconds','warning','outside_trio']},ensure_ascii=False),flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(compile_one,sources))
save('COMPILATIONS.json',{'results':results,'all_ok':all(r['rc']==0 and not r['warning'] and not r['outside_trio'] and not r['sorryAx'] and r['source_unchanged'] for r in results)})
