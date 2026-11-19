"""Recompile the exact frozen candidates and their local dependencies with lean.exe."""
import concurrent.futures as futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

out_root = Path(__file__).resolve().parent / 'compilacao_018B_019_Astra'
base = out_root.parent.parent / 'candidatas_c1'
sandbox = Path('C:/t/k411c/final/.lake')
lean = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
def sha(data): return hashlib.sha256(data).hexdigest()
def pin(file): return dict(arquivo=str(file), bytes=file.stat().st_size, sha256=sha(file.read_bytes()))
def put(file,data):
    with file.open('xb') as output: output.write(data)
def main():
    candidates = [('REV18/MinimoFuncionalDeEnergia.lean','e8a4932297df704d'),
        ('REV19/CopiadorEImpostor.lean','0729ab820c049e9a'),
        ('tipo_iii/REV4/TipoIIIControles.lean','0c28be72049eb776'),
        ('tipo_iii/REV4/TipoIIIUmSoBoost.lean','3e7342cb5478bc3d'),
        ('t1/REV4/T1CompostoFinito.lean','4acd9ef1ff8c7dac'),
        ('t1/REV4/T1PontesAoKernel.lean','64bbbb948ffbd734')]
    files = [(base/f, digest) for f,digest in candidates]
    files.append((base/'ErgodicidadeDeMautner.lean',None))
    for directory in ['tipo_iii/dep_codex','t1/dep_codex']:
        deps=base/directory
        manifest=json.loads((deps/'MANIFESTO_DEP_CODEX.json').read_text(encoding='utf-8-sig'))
        files.extend((deps/name,values['sha256']) for name,values in manifest['arquivos'].items())
    version=subprocess.check_output([str(lean),'--version']).decode().strip()
    assert 'version 4.31.0' in version and (sandbox/'build/lib/lean').is_dir()
    out_root.mkdir(exist_ok=False)
    sources=out_root/'fontes'; sources.mkdir()
    build=out_root/'build'; build.mkdir()
    env=dict(os.environ)
    paths=[build,sandbox/'build/lib/lean']
    paths.extend(sorted((sandbox/'packages').glob('*/.lake/build/lib/lean')))
    env['LEAN_PATH']=';'.join(map(str,paths))
    pending={}; allnames={f.stem for f,_ in files}; source_paths={}
    for f,digest in files:
        data=f.read_bytes(); assert digest is None or sha(data).startswith(digest),f
        target=sources/f.name; put(target,data); source_paths[f.stem]=f
        pending[f.stem]=set(re.findall(r'^import\s+(\w+)\s*$',data.decode('utf-8-sig'),re.M)) & allnames
    def run(name):
        f=sources/(name+'.lean'); olean=build/(name+'.olean'); log=build/(name+'.log')
        args=[str(lean),'-o',str(olean),f.name]
        start=time.monotonic()
        p=subprocess.run(args,cwd=sources,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        put(log,p.stdout); raw=p.stdout.decode('utf-8',errors='replace')
        q=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]|'([^']+)' does not depend on any axioms",raw)
        ax={name or empty: sorted(a.strip() for a in ax.split(',') if a.strip()) for name,ax,empty in q}
        entry=dict(modulo=name,rc=p.returncode,elapsed_s=time.monotonic()-start,
          avisos=len(re.findall(r'\bwarning:',raw,re.I)),erros=len(re.findall(r'\berror:',raw,re.I)),
          axiomas=sorted({a for arr in ax.values() for a in arr}),por_teorema=ax,
          consultas=len(ax),fonte=pin(source_paths[name]),copia=pin(f),log=pin(log),
          objeto=pin(olean) if olean.exists() else None,comando=args)
        put(build/(name+'.json'),json.dumps(entry,ensure_ascii=False,indent=2).encode())
        print(name,p.returncode,entry['avisos'],len(ax),round(entry['elapsed_s'],1),flush=True)
        return entry
    complete={}; tasks={}
    with futures.ThreadPoolExecutor(max_workers=5) as pool:
        while pending or tasks:
            for name in list(pending):
                if pending[name].issubset(complete):
                    tasks[pool.submit(run,name)]=name; del pending[name]
            if not tasks: raise RuntimeError('cyclic dependencies: '+str(pending))
            done,_=futures.wait(tasks,return_when=futures.FIRST_COMPLETED)
            for future in done:
                result=future.result(); name=tasks.pop(future)
                if result['rc'] or not result['objeto']: raise RuntimeError('failed:'+name)
                complete[name]=result
    put(out_root/'COMPILACAO.json',json.dumps(dict(lean=version,sandbox=str(sandbox),
       paths=[str(p) for p in paths],script=pin(Path(__file__)),modulos=complete),ensure_ascii=False,indent=2).encode())
if __name__=='__main__': main()
