"""Publish only the independent reviews, retaining the prior receipt and competing deliveries."""
from pathlib import Path
from datetime import datetime
import argparse, hashlib, json, os, tempfile

HERE=Path(__file__).resolve().parent
REVIEW=HERE.parent
TUNNEL=Path('C:/IALD/TUNEL_CLAUDE_APP')
def pin(path): return dict(arquivo=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
def json_read(path): return json.loads(path.read_bytes())
def raw_json(value): return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def atomic(target,data,original=None):
    with tempfile.NamedTemporaryFile(mode='wb',dir=target.parent,prefix='.'+target.name+'.',suffix='.tmp',delete=False) as stream:
        name=Path(stream.name);stream.write(data);stream.flush();os.fsync(stream.fileno())
    assert name.read_bytes()==data
    try:
        if original is None:
            name.rename(target)  # Windows: fails if a competing writer has created target
        else:
            if target.read_bytes()!=original: raise RuntimeError('baseline_changed; preserve competing receipt')
            now=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            backup=target.with_name(target.name+'.bak_'+now)
            with backup.open('xb') as stream: stream.write(original)
            assert backup.read_bytes()==original
            if target.read_bytes()!=original: raise RuntimeError('baseline_changed_after_backup')
            # ReplaceFileW keeps the actual displaced bytes as well, even if an independent writer races the last comparison.
            import ctypes
            race=target.with_name(target.name+'.bak_'+now+'_substituido')
            replace=ctypes.WinDLL('kernel32',use_last_error=True).ReplaceFileW
            replace.argtypes=[ctypes.c_wchar_p]*3+[ctypes.c_ulong,ctypes.c_void_p,ctypes.c_void_p]
            if not replace(str(target),str(name),str(race),0,None,None): raise ctypes.WinError(ctypes.get_last_error())
            actual=race.read_bytes()
            if actual!=original:
                # A parallel replacement did occur. Merge our additive fields onto the exact bytes we displaced, unless a matching return exists.
                concurrent=json.loads(actual)
                own=json.loads(data)['retorno_adendo_b_codex_astra']
                if not any(x.get('unidade')=='U7' for x in concurrent.get('unidades',[])):
                    apply_018(concurrent,own)
                atomic(target,raw_json(concurrent),data)
                return
        if target.read_bytes()!=data: raise RuntimeError('delivery_changed_after_publish; inspect before any new write')
    finally:
        if name.exists(): name.unlink()

def build_result(name):
    path=HERE/'build'/(name+'.json'); d=json_read(path)
    return dict(modulo=name,rc=d['rc'],avisos=d['avisos'],consultas_de_axiomas=d['consultas'],
                axiomas=d['axiomas'],fonte=d['fonte'],log=d['log'],recibo=pin(path))
def check_existing(entry):
    p=entry['parecer'];path=Path(p['arquivo']);return path.is_file() and pin(path)['sha256']==p['sha256']
def apply_018(d,detail):
    if any(item.get('unidade')=='U7' for item in d['unidades']): raise RuntimeError('U7 already present')
    if 'B' not in d['adendos']:d['adendos'].append('B')
    d['unidades'].append(detail['unidade'])
    d['compilacoes_das_candidatas'].append(dict(unidade='U7',**detail['compilacao']))
    d['arquivos'].extend(detail['arquivos']);d['retorno_adendo_b_codex_astra']=detail
def main(order):
    now=datetime.now().astimezone().isoformat();target=TUNNEL/'RESULTADOS'/(order+'_RESULTADO.json')
    if order=='018':
        raw=target.read_bytes();d=json.loads(raw)
        existing=[item for item in d['unidades'] if item['unidade']=='U7']
        if existing:
            if not all(check_existing(e) for e in existing): raise RuntimeError('existing_U7_pin_mismatch')
            print('Valid prior U7 preserved',pin(target));return
        report=REVIEW/'REVISAO_018_U7_CodexAstra.md'
        unit=dict(unidade='U7',revisor='CodexAstra',veredito='APROVADO_COM_RESSALVAS',parecer=pin(report))
        comp=build_result('MinimoFuncionalDeEnergia');assert comp['rc']==0 and comp['consultas_de_axiomas']==11
        detail=dict(hora_local=now,unidade=unit,compilacao=comp,
            ordem=pin(next(TUNNEL.glob('ORDEM_018_ADENDO_B*.md'))),
            arquivos=[pin(report),comp['recibo'],comp['log'],pin(HERE/'TEXTO_E_BUSCAS.json')],
            alcance='Identidade formal do fluxo bruto da instância. Emendas de escopo sobre normalização, mínimo e transporte da bancada descritas no parecer.',
            continuidade='Entradas anteriores, história do recebimento de outros revisores e pendências foram preservadas.')
        apply_018(d,detail);atomic(target,raw_json(d),raw)
    else:
        if target.exists():
            d=json_read(target);existing=d.get('unidades',[])
            if len(existing)<3 or not all(check_existing(x) for x in existing): raise RuntimeError('competing_019_requires_inspection')
            print('Valid prior 019 preserved',pin(target));return
        units=[]
        for unit,verdict,names in [('U3','EMENDAS_CONFEREM_COM_RESSALVAS',['CopiadorEImpostor']),('U4','EMENDAS_CONFEREM',['TipoIIIControles','TipoIIIUmSoBoost']),('U5','EMENDAS_CONFEREM_COM_RESSALVAS',['T1CompostoFinito','T1PontesAoKernel'])]:
            report=REVIEW/('REVISAO_019_'+unit+'_CodexAstra.md');assert report.read_text(encoding='utf-8').splitlines()[0]==verdict
            units.append(dict(unidade=unit,veredito=verdict,revisor='CodexAstra',parecer=pin(report),compilacoes=[build_result(n) for n in names]))
        doc=dict(ordem='019',estado='CONFERENCIA_TECNICA_ENTREGUE',hora_local=now,fonte_da_ordem=pin(next(TUNNEL.glob('ORDEM_019*.md'))),
            unidades=units,conferencia_dos_recibos=pin(HERE/'CONFERENCIA_COMPILADORES.json'),
            fontes_e_citacoes=pin(HERE/'TEXTO_E_BUSCAS.json'),compilacao_com_dependencias=pin(HERE/'COMPILACAO.json'),
            pendencias=['U3 e U5: ressalvas editoriais locais descritas nos pareceres.','Denominação e integração seguem a ordem da gerência e as decisões do operador.'])
        atomic(target,raw_json(doc))
    print('Delivered:',pin(target))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('ordem',choices=['018','019']);main(parser.parse_args().ordem)
