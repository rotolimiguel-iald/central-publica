"""Recompile the exact frozen candidates and their local dependencies with lean.exe."""
import concurrent.futures as futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

out_root = Path(__file__).resolve().parent / 'compilacao_022_Codex'
base = out_root.parent.parent / 'candidatas_c1'
sandbox = Path('C:/t/k411c/final/.lake')
lean = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe')
def sha(data): return hashlib.sha256(data).hexdigest()
def pin(file): return dict(arquivo=str(file), bytes=file.stat().st_size, sha256=sha(file.read_bytes()))
def put(file,data):
    with file.open('xb') as output: output.write(data)
def main():
    files = [(base / f, digest) for f, digest in [('REV22/MinimoFuncionalDeEnergia.lean', '6918426af1234025'), ('REV25/OParFixaORelogio.lean', '267019b19fb5a22c'), ('REV20/OLeitorEALei.lean', 'e8097c78307b6c18'), ('REV21/BoostEDissipador.lean', '69765f7fc002c37c'), ('REV26/AContagemEACarga.lean', 'e1f7ec03ed0fd3c1'), ('REV27/OVerdadeiroEDivisivel.lean', '3a95884796ebd053'), ('REV28/AMaquinaEALeitura.lean', '5a99c5e3e882e0c1'), ('REV29/OPassoEORetorno.lean', 'e9dbc9e43da1d80c')]]
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
