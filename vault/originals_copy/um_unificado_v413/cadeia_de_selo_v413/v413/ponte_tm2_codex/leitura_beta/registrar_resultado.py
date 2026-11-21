"""Recibo reprodutível do delta local: hashes de bytes e conferência de logs."""
from pathlib import Path
import hashlib, json, os, re, subprocess, sys, time
from datetime import datetime

root = Path(__file__).resolve().parent
names = ['RelogioBeta', 'LeituraBeta', 'QuantizacaoBeta', 'Reconstrucao', 'PonteLeituraBeta', 'EntregaBeta']
lake = Path('C:/t/k411c/final/.lake')
workshop = root.parents[2] / 'v412'

def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def write_new(name, raw):
    dst = root / name
    if dst.exists():
        raise RuntimeError('Recibo existente, preservar: ' + str(dst))
    tmp = root / (name + '.tmp')
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(dst)

if sys.argv[1:] == ['replay']:
    libs = [root, root.parent / 'simulacao', root.parent, lake/'build/lib/lean',
            *(p/'.lake/build/lib/lean' for p in sorted((lake/'packages').iterdir())),
            workshop/'candidatas_c1/build', workshop/'candidatas_c1/build_sobre_limpas',
            workshop/'candidatas_kimi/build']
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(str(p) for p in libs if p.is_dir()))
    tool = Path('C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/leanchecker.exe')
    started = time.monotonic()
    result = subprocess.run([str(tool), '-v', 'EntregaBeta'], cwd=root, env=env, capture_output=True)
    log = f'leanchecker -v EntregaBeta | RC {result.returncode} | seconds {time.monotonic()-started:.3f}\n'
    log += (result.stdout + result.stderr).decode('utf8')
    write_new('REPLAY.log', log.encode('utf8'))
    print(log)
    sys.exit(result.returncode)

assert not sys.argv[1:]
modules = []
for n in names:
    src = pin(root/(n+'.lean'))
    log = (root/(n+'.log')).read_text(encoding='utf8')
    assert src['sha256'] in log and 'RC 0' in log, n
    assert all(x not in log for x in ['sorryAx', 'warning:', 'error:']), n
    text = (root/(n+'.lean')).read_text(encoding='utf8')
    assert not re.search(r'^\s*(axiom |sorry\b|unsafe\b|\[implemented_by)', text, re.M), n
    modules.append({'module': n, 'source': src, 'object': pin(root/(n+'.olean')),
                    'log': pin(root/(n+'.log')), 'rc': 0,
                    'axiom_reports': [s for s in log.splitlines() if 'depends on axioms:' in s]})
replay = (root/'REPLAY.log').read_text(encoding='utf8')
assert 'RC 0' in replay
reviews = []
for name in ['REVIEW_RECONSTRUCAO.json','REVIEW_BETA.json']:
    reviews.append({'receipt': pin(root/name), 'content': json.loads((root/name).read_text(encoding='utf8'))})
for name, digest in reviews[0]['content']['source_sha256'].items():
    assert pin(root/name)['sha256'] == digest
for item in reviews[1]['content']['sources']:
    for key in ['source', 'log', 'olean']:
        assert pin(item[key])['sha256'] == item[key+'_sha256']
origin_receipt = json.loads((workshop/'candidatas_kimi/RESULTADO_ONomeEBeta.json').read_text(encoding='utf8'))
assert pin(workshop/'candidatas_kimi/ONomeEBeta.lean')['sha256'] == origin_receipt['sha256_fonte']
data = {
    'time_local': datetime.now().astimezone().isoformat(),
    'status': 'PROVAS_LOCAIS_CONDICIONAIS_COMPILADAS_E_REVISADAS',
    'statute': 'REAL',
    'own_session_reference': str(root.parent/'SESSION_REFERENCE.json'),
    'previous_delivery': pin(root.parent/'simulacao/RESULTADO.json'),
    'antecedents': [pin(workshop/'candidatas_kimi/ONomeEBeta.lean'),
                    pin(workshop/'candidatas_kimi/RESULTADO_ONomeEBeta.json'),
                    pin(workshop/'revisao_orquestrador/psibit_leitor_direto_Codex/LeiturasComFolga.lean')],
    'modules': modules,
    'replay': pin(root/'REPLAY.log'),
    'independent_scope_reviews': reviews,
    'results': {
        'fixed_clock': 'Para c fixo, existe m natural fixado antes da fórmula com ln(2)/beta < m. k=m(n+2), afim em n.',
        'finite_gap': 'SAT implica Z>=1; nao SAT implica Z<1/4. Erro absoluto <=1/4 e limiar 1/2 bastam.',
        'finite_precision': 'Para Z/2^n, erro <=2^(-(n+2)); existe numerador j<=2^(n+2), cabendo em n+3 bits. O comparador e j>=2.',
        'reconstruction': 'Leitor correto como hipotese: ramos sequenciais preservam modelos conjuntos, sem exigir solucao unica nem enumerar mascaras.',
        'query_bound': 'Contador estrutural <=L+1 consultas; cada consulta de ramo <=3L letras; volume total com inicial <=L+3L^2.',
        'alphabet_measure': 'L e letras phi = ocorrencias de literais + terminadores; nao e ainda comprimento binario incluindo indices.'},
    'still_open': [
        'Implementar o produtor reader a partir da formula sozinha e provar a lei de erro hr.',
        'Provar custo uniforme polinomial de reader e da construcao/decodificacao das consultas em movimentos da fita.',
        'O relogio de beta e tamanho da aproximacao nao substituem essas duas provas; a soma semantica permanece definida sobre as atribuicoes.',
        'A existencia do numerador usa piso do real; nao e um algoritmo de calculo da formula.',
        'n e a dimensao declarada de Fin n. A precisao n+3 nao foi aqui convertida para numero de nomes presentes por renomeacao compacta.'
    ],
    'limits': 'Sem instalacao, mudanca do kernel canonico, execucao de um.py, abertura de dados, publicacao ou mudanca do gate. Aceite da gerencia separado.',
    'protocol_note': 'ACOM propria recuperada na revisao 2. mission_cli.project devolveu mission_not_initialized; nao foi adotada missao de outra sessao.',
    'reproduce': [pin(p) for p in sorted(root.glob('compilar*.py'))]
}
write_new('RESULTADO.json', (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf8'))
print(json.dumps(pin(root/'RESULTADO.json'), ensure_ascii=False))
