"""Compare every independently recompiled theorem and its axioms against the authors' receipts."""
from pathlib import Path
import hashlib,json,re

here=Path(__file__).resolve().parent
base=here.parent.parent/'candidatas_c1'
def pin(path):return dict(arquivo=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
def main():
    builds=json.loads((here/'COMPILACAO.json').read_bytes())['modulos']
    checks=[]
    for rel in ['RESULTADO_CopiadorEImpostor.json','RESULTADO_MinimoFuncionalDeEnergia.json','tipo_iii/RESULTADO_GERENCIA.json','t1/RESULTADO_GERENCIA.json']:
        receipt=base/rel
        for original in json.loads(receipt.read_bytes())['modulos']:
            name=Path(original['fonte']).stem;own=builds[name]
            expected={x['nome']:sorted(x['axiomas']) for x in original['teoremas']}
            code=Path(own['copia']['arquivo']).read_text(encoding='utf-8-sig')
            declared=re.findall(r'^theorem\s+([\w.]+)',code,re.M)
            probes=re.findall(r'^#print axioms\s+([\w.]+)',code,re.M)
            assert own['por_teorema']==expected, (name,'axioms differ')
            assert sorted(n.split('.')[-1] for n in expected)==sorted(n.split('.')[-1] for n in declared)==sorted(n.split('.')[-1] for n in probes),name
            assert own['rc']==int(original['rc'])==0 and own['avisos']==original['avisos']==0
            assert own['fonte']['sha256']==own['copia']['sha256']==original['sha256']
            assert len(expected)==original['teoremas_declarados']==original['teoremas_com_axiomas_impressos']
            checks.append(dict(modulo=name,recibo_origem=pin(receipt),recibo_proprio=pin(here/'build'/(name+'.json')),
                 nomes_e_axiomas_por_teorema_identicos=True,declarados=len(declared),sem_axiomas=sum(not v for v in expected.values())))
    report=dict(status='CONFERIDO',comparacoes=checks,modulos_recompilados=len(builds),avisos_das_dependencias={n:r['avisos'] for n,r in builds.items() if r['avisos']},
        pino_compilacao=pin(here/'COMPILACAO.json'),pino_buscas=pin(here/'TEXTO_E_BUSCAS.json'))
    with (here/'CONFERENCIA_COMPILADORES.json').open('xb') as f:f.write(json.dumps(report,ensure_ascii=False,indent=2).encode())
    print('Checked', [(x['modulo'],x['declarados']) for x in checks],report['avisos_das_dependencias'])
if __name__=='__main__': main()
