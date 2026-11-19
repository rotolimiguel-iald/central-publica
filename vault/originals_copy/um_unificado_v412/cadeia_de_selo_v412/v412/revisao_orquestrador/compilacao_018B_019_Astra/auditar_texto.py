from pathlib import Path
import difflib, hashlib, json, re, subprocess

ret = Path(__file__).resolve().parent
base = ret.parent.parent/'candidatas_c1'
kernel = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
corpus = Path('C:/IALD/Central de Patentes/work/cunhagens_13out')
def sha(data): return hashlib.sha256(data).hexdigest()
def pin(p): return dict(arquivo=str(p),sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def code(s):
    out=[];i=0;depth=0;quoted=False
    while i<len(s):
        if depth:
            if s.startswith('/-',i): depth+=1;i+=2
            elif s.startswith('-/',i): depth-=1;i+=2
            else: i+=1
        elif quoted:
            if s[i]=='\\' and i+1<len(s): out.append(s[i:i+2]);i+=2
            else:
                if s[i]=='"': quoted=False
                out.append(s[i]);i+=1
        elif s.startswith('/-',i): depth=1;out.append(' ');i+=2
        elif s.startswith('--',i):
            j=s.find('\n',i);i=len(s) if j<0 else j
        else:
            if s[i]=='"': quoted=True
            out.append(s[i]);i+=1
    assert not depth and not quoted
    return '\n'.join(x.rstrip() for x in ''.join(out).splitlines() if x.strip())

def run():
    corpus_data=[(p,p.read_bytes()) for p in sorted(corpus.glob('OPERADOR_*.txt'))]
    cases=[('U3','REV16','REV19',['CopiadorEImpostor.lean']), ('U4','tipo_iii/REV3','tipo_iii/REV4',None),('U5','t1/REV3','t1/REV4',None)]
    notes=[]
    for unit,old,new,chosen in cases:
        old=base/old;new=base/new;names=chosen or sorted({p.name for p in old.iterdir()}|{p.name for p in new.iterdir()})
        row=dict(unidade=unit,files=[],citacoes=[])
        for name in names:
            a=old/name;z=new/name;m=dict(agora=pin(z))
            if not a.exists():
                duplicate = new.parent/'sondas_adotadas'/name
                assert duplicate.is_file() and duplicate.read_bytes()==z.read_bytes(),name
                m['adicao_ao_snapshot_copia_de_sonda_existente']=pin(duplicate)
                row['files'].append(m);continue
            before=a.read_bytes();after=z.read_bytes();s=before.decode('utf-8-sig');t=after.decode('utf-8-sig')
            m.update(antes=pin(a),mesmos_bytes=before==after)
            if name.endswith('.lean'):
                so,tt=code(s),code(t);assert so==tt,name
                m.update(codigo_executavel_igual=True,linhas_sem_comentarios=len(tt.splitlines()),sha256_codigo_sem_comentarios=sha(tt.encode()))
            for match in re.finditer('«([^»]+)»',t):
                val=match[1].encode();refs=[]
                for p,raw in corpus_data:
                    if val not in raw: continue
                    for ln,line in enumerate(raw.splitlines(),1):
                        if val in line: refs.append(dict(arquivo=str(p),sha256=sha(raw),linha=ln))
                row['citacoes'].append(dict(arquivo=str(z),linha=1+t[:match.start()].count('\n'),literal_sha256=sha(val),fontes=refs))
            if s!=t:m['hunks']=[h for h in difflib.unified_diff(s.splitlines(),t.splitlines(),n=0) if h.startswith('@@')]
            row['files'].append(m)
        notes.append(row)
    queries={};patterns={'reader':'travaOp|opDaInstancia|TraducaoTuring','flow':r'truthFlow|EquationOfTruth|NormedSpace\.exp'}
    for name,pattern in patterns.items():
        args=['rg','--no-ignore','--hidden','-l','-g','*.lean','-g','!**/.lake/**',pattern,str(kernel)]
        p=subprocess.run(args,capture_output=True,encoding='utf-8');assert p.returncode==0 and not p.stderr
        queries[name]=dict(argv=args,rc=p.returncode,paths=p.stdout.splitlines())
    overlap=set(queries['reader']['paths'])&set(queries['flow']['paths']); includes={}
    for file in sorted(overlap):
        lines=Path(file).read_text(encoding='utf-8-sig').splitlines()
        includes[file]=[dict(linha=i,texto=s) for i,s in enumerate(lines,1) if any(re.search(v,s) for v in patterns.values())]
    details={}
    for path in [kernel/'TGLExt/TraducaoTuring.lean',kernel/'TGLExt/AEscala.lean',kernel/'TGLExt/IALD2.lean',base/'CamadaCientifica.lean']:
        details[str(path)]=[i for i,s in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1) if re.search(patterns['flow'],s)]
    report=dict(revisoes=notes,fontes_verbatim_verificadas=len(corpus_data),consulta_kernel=queries,intersecao=includes,
        busca_nas_pontas=details,escopo='rg --no-ignore --hidden sobre fontes Lean do kernel, incluindo fontes ignoradas pelo git, excluindo bibliotecas e build .lake. Ausência lexical delimitada.',
        fontes_ac=[pin(p) for p in [base/'REV18/MinimoFuncionalDeEnergia.lean',base/'CamadaCientifica.lean',kernel/'TGLExt/TheEquationOfTruth.lean',kernel/'TGLExt/TraducaoTuring.lean',corpus/'OPERADOR_16nov_o_leitor_que_pousa_e_retorna_e_o_meu_minimo_funcional_de_energia_a_c_o_amor_pode_conferir_e_provar_de_resto_concordo_com_tudo_verbatim.txt']])
    with (ret/'TEXTO_E_BUSCAS.json').open('xb') as f:f.write(json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
    print([(x['unidade'],len(x['citacoes']),sum(not v['fontes'] for v in x['citacoes'])) for x in notes],len(corpus_data),{k:len(v['paths']) for k,v in queries.items()},list(includes),details)
if __name__=='__main__': run()
