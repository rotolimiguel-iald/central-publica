from pathlib import Path
import hashlib,json,os,re,subprocess,sys,time
D=Path(__file__).resolve().parent
B=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
env=os.environ.copy();env['LEAN_PATH']=';'.join(B['lean_path'])
def pin(p):
 b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
for name in sys.argv[1:]:
 src=D/'src'/(name+'.lean');label=name
 if name.startswith('Audit_'):
  mod=name[6:];original=D/'src'/(mod+'.lean');txt=original.read_text(encoding='utf-8')
  ns=re.search(r'^namespace\s+(\S+)',txt,re.M).group(1)
  decls=re.findall(r'^(?:theorem|lemma)\s+(\S+)',txt,re.M)
  raw=('import '+mod+'\n\n'+'\n'.join('#print axioms '+ns+'.'+s for s in decls)+'\n').encode()
  assert not src.exists();src.write_bytes(raw)
 log=D/'logs'/(name+'.R2.log');assert not log.exists(),log
 cmd=[B['lean']['path'],'-j','2','-o',str(D/'build'/(name+'.olean')),src.name]
 start=time.monotonic();r=subprocess.run(cmd,cwd=D/'src',env=env,capture_output=True);log.write_bytes(r.stdout+r.stderr)
 txt=log.read_text(encoding='utf-8');entries=[]
 for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",txt,re.S):
  entries.append({'declaration':m.group(1),'axioms':[a.strip() for a in (m.group(2) or '').split(',') if a.strip()]})
 result={'module':name,'source':pin(src),'rc':r.returncode,'seconds':round(time.monotonic()-start,3),'command':cmd,'log':pin(log),'axiom_reports':entries,'outside_trio':sorted({a for e in entries for a in e['axioms'] if a not in {'propext','Classical.choice','Quot.sound'}}),'warning':bool(re.search(r'\bwarning:',txt)),'sorryAx':'sorryAx' in txt}
 obj=D/'build'/(name+'.olean')
 if obj.exists():result['object']=pin(obj)
 out=D/(name+'.R2.compile.json');assert not out.exists();out.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
 print(json.dumps({k:result[k] for k in ['module','rc','seconds','warning','outside_trio']},ensure_ascii=False),flush=True)
