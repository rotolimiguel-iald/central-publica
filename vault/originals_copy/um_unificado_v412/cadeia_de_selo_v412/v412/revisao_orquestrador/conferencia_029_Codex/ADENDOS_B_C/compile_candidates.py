
from pathlib import Path
import os,json,hashlib,subprocess,time,datetime
base=Path(__file__).resolve().parent
previous=json.loads((base.parent/'ADENDO_A/COMPILACAO_R1.json').read_text(encoding='utf-8'))
lean=Path(previous['lean']['arquivo'])
def pin(p):
 b=p.read_bytes()
 return dict(arquivo=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,b):
 if p.exists(): raise RuntimeError('Existing build output: '+str(p))
 tmp=p.with_name(p.name+'.tmp')
 tmp.write_bytes(b)
 assert tmp.read_bytes()==b
 tmp.rename(p)
build=base/'build'
env=os.environ.copy()
env['LEAN_PATH']=';'.join([str(build)]+previous['lean_path'])
for name in ['Token2','AMaquina']:
 start=time.monotonic()
 proc=subprocess.run([str(lean),'-o',str(build/(name+'.olean')),str(build/(name+'.lean'))],cwd=build,env=env,capture_output=True,timeout=240)
 stdout=base/(name+'.stdout.log')
 stderr=base/(name+'.stderr.log')
 write(stdout,proc.stdout);write(stderr,proc.stderr)
 rec={'source_copy':pin(build/(name+'.lean')),'lean':pin(lean),'lean_path':[str(build)]+previous['lean_path'],'rc':proc.returncode,'seconds':time.monotonic()-start,'stdout':pin(stdout),'stderr':pin(stderr),'dependency_rebuild':False,'full_kernel_rebuild':False}
 if (build/(name+'.olean')).exists():rec['olean']=pin(build/(name+'.olean'))
 write(base/(name+'_COMPILACAO.json'),(json.dumps(rec,ensure_ascii=False,indent=2)+'\n').encode())
 print(json.dumps({'name':name,'rc':proc.returncode,'seconds':rec['seconds']},ensure_ascii=False),flush=True)
 if proc.returncode:break
