from review import *
import hashlib, subprocess

def strip_comments(s):
    out=[]; i=0; depth=0; mode='code'
    while i<len(s):
        a=s[i:i+2]; c=s[i]
        if mode=='line':
            if c=='\n': mode='code';out.append(c)
            i+=1;continue
        if depth:
            if a=='/-':depth+=1;i+=2
            elif a=='-/':depth-=1;i+=2
            else:
                if c=='\n':out.append(c)
                i+=1
            continue
        if mode=='string':
            out.append(c);i+=1
            if c=='\\' and i<len(s):out.append(s[i]);i+=1
            elif c=='"':mode='code'
            continue
        if a=='/-':depth=1;i+=2;continue
        if a=='--':mode='line';i+=2;continue
        if c=='"':mode='string'
        out.append(c);i+=1
    assert depth==0 and mode!='string'
    return '\n'.join(x.rstrip() for x in ''.join(out).splitlines() if x.strip())

base=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
records=[]; sources=[]
for r in base['modules']:
    a,b=Path(r['origin']['path']),Path(r['clean']['path'])
    aa,bb=a.read_text(encoding='utf-8'),b.read_text(encoding='utf-8')
    ca,cb=strip_comments(aa),strip_comments(bb)
    records.append({'module':r['module'],'code_identical':ca==cb,
        'code_sha256_origin':hashlib.sha256(ca.encode()).hexdigest(),'code_sha256_clean':hashlib.sha256(cb.encode()).hexdigest(),
        'source_pin_unchanged':pin(a)==r['origin'] and pin(b)==r['clean'],
        'comments_backticks_removed':sorted(set(re.findall(r'`([^`\n]+)`',aa))-set(re.findall(r'`([^`\n]+)`',bb)))})
    sources.extend([pin(a),pin(b)])
m=json.loads((I/'MANIFESTO_PEDRAS_v413.json').read_text(encoding='utf-8-sig'))
for r in m['kernel_corrigido'].values():
    a,b=Path(r['origem']),Path(r['saida']);aa=a.read_text(encoding='utf-8');bb=b.read_text(encoding='utf-8')
    if not (D/'diffs/OResumoEPsiBit.diff').exists():
        save('diffs/OResumoEPsiBit.diff',''.join(difflib.unified_diff(aa.splitlines(True),bb.splitlines(True),fromfile=str(a),tofile=str(b))))
    records.append({'module':'TGLExt.OResumoEPsiBit','code_identical':strip_comments(aa)==strip_comments(bb),
      'source_pin_unchanged':pin(a)['sha256']==r['sha256_origem'] and pin(b)['sha256']==r['sha256_saida']})
    sources.extend([pin(a),pin(b)])
audits=[]
for kind in ['pedras_limpas','kernel_edits']:
    receipt=I/('CONJUNTO_'+kind+'.json');v=json.loads(receipt.read_text(encoding='utf-8-sig'));sources.append(pin(receipt))
    for name,r in v['modulos'].items():
        folder=I/('auditoria_'+kind)
        files=[folder/(name+'.compile.log'),folder/('Audit_'+name+'.lean'),folder/('Audit_'+name+'.log')]
        texts=[p.read_text(encoding='utf-8') for p in files];sources.extend(pin(p) for p in files)
        entries={a:[s.strip() for s in (b or '').split(',') if s.strip()] for a,b in re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",texts[2],re.S)}
        declared=re.findall(r'^#print axioms\s+(\S+)',texts[1],re.M)
        checks={'source_hash_matches':pin(r['fonte'])['sha256']==r['sha256'],
          'reported_rc_zero':r['rc']==0 and r['rc_auditoria']==0,
          'audit_names_exact':set(entries)==set(declared)==set(r['axiomas']),
          'audit_axioms_match':{k:sorted(v) for k,v in entries.items()}=={k:sorted(v) for k,v in r['axiomas'].items()},
          'counts_match':len(entries)==r['teoremas']==r['relatorios'],
          'only_trio':all(set(x)<={'propext','Classical.choice','Quot.sound'} for x in entries.values()),
          'no_errors_or_warnings':not any(re.search(r'\b(?:error|warning):|sorryAx',s) for s in (texts[0],texts[2]))}
        audits.append({'kind':kind,'module':name,'checks':checks,'report_count':len(entries),'passed':all(checks.values())})
cmd=[PY,'-B','-X','utf8',str(V.parent/'v412/verificar_historia_nas_pedras.py'),str(I/'pedras_limpas/TGLExt'),'--contra',str(I/'origem/TGLExt'),'--detalhe']
r=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True)
save('VERIFICADOR_HISTORIA_R2.json',{'command':cmd,'rc':r.returncode,'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8')})
save('MECHANICAL_R2.json',{'erratum':'R1 comparou listas de axiomas na ordem impressa com listas ordenadas do recibo. R2 compara o mesmo conjunto por declaracao; nenhum axioma novo ou ausente. R1 preservado.',
  'method':'Leitor local de comentarios aninhados e strings; compara linhas nao vazias do codigo, preserva indentacao e conteudo, retira apenas comentarios e espaco final; LF normalizado. Nao reexecuta Lean.',
  'modules':records,'audits':audits,'sources':sources,'verifier_rc':r.returncode,
  'all_code_equal':all(x['code_identical'] for x in records),'all_audits_pass':all(x['passed'] for x in audits)})
print(json.dumps({'code_equal':[(x['module'],x['code_identical']) for x in records], 'audit_pass':all(x['passed'] for x in audits),'reports':sum(x['report_count'] for x in audits),'failed_audits':[x for x in audits if not x['passed']],'verifier_rc':r.returncode},ensure_ascii=False))
