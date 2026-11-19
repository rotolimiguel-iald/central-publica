"""Read-only scan of the canonical Lean corpus and audit of the original/local logs."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
V412 = HERE.parents[1]
ORIGINAL = V412 / 'candidatas_c1'
MODULE = 'PsionVacuoEModoDoTratado'
KERNEL = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
CONSOLIDATION = Path('C:/IALD/Central de Patentes/work/vitrine_postura_13nov/rodada_b/consolidacao_das_falas/CONSOLIDACAO_DAS_FALAS_DO_PSION_16nov.md')
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def log_axioms(path):
    data = path.read_bytes().decode('utf-8-sig')
    found = {k: [a.strip() for a in v.split(',')] for k, v in
             re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", data)}
    assert found and all(set(ax) == ALLOWED for ax in found.values()), path
    assert not re.search(r'(?i)\b(?:warning|error|sorryAx)\b', data), path
    return found


def canonical_scan():
    cmd = ['rg', '--files', '--hidden', '--no-ignore', '-g', '*.lean']
    filenames = sorted(subprocess.check_output(cmd, cwd=KERNEL).decode('utf8').splitlines())
    patterns = {name: re.compile(pat, re.I) for name, pat in {
        'lockDe': r'\blockDe\b', 'HminMic': r'\bHminMic\b',
        'PFmic': r'\bPFmic\b', 'physicalFockCertificate': r'\bphysicalFockCertificate\b',
        'eigen_or_spectrum_lock_identifier': r'\b\w*(?:hminmic|lock)\w*(?:eigen|spectrum|spectr|autoval|níve[il])\w*|\b\w*(?:eigen|spectrum|spectr|autoval|níve[il])\w*(?:hminmic|lock)\w*',
    }.items()}
    hits = {name: {} for name in patterns}
    packages = 0
    for name in filenames:
        f = Path(name)
        packages += '.lake' in f.parts and 'packages' in f.parts
        data = (KERNEL / f).read_bytes().decode('utf-8-sig')
        for label, pattern in patterns.items():
            if pattern.search(data):
                lines = [i for i, line in enumerate(data.splitlines(), 1) if pattern.search(line)]
                hits[label][f.as_posix()] = lines
    return {'root': str(KERNEL), 'command': cmd, 'lean_files': len(filenames),
            'packages_within_root': packages, 'case_insensitive_line_hits': hits}


def main():
    copied = HERE / (MODULE + '.lean')
    source = ORIGINAL / 'REV17' / copied.name
    original_log = ORIGINAL / 'build' / (MODULE + '.log')
    measured_log = HERE / 'build' / original_log.name
    script = HERE / 'compilar_candidata.ps1'
    receipt = ORIGINAL / ('RESULTADO_' + MODULE + '.json')
    assert source.read_bytes() == copied.read_bytes()
    assert script.read_bytes() == (ORIGINAL / script.name).read_bytes()
    data = copied.read_text(encoding='utf8')
    declared = re.findall(r'^theorem (\w+)', data, re.M)
    ax = log_axioms(measured_log)
    assert [s.rsplit('.', 1)[-1] for s in ax] == declared and len(ax) == 27
    assert ax == log_axioms(original_log)
    claimed = json.loads(receipt.read_bytes())['modulos'][0]
    assert {r['nome']: r['axiomas'] for r in claimed['teoremas']} == ax
    assert claimed['sha256'] == pin(source)['sha256'] and 'RC: 0' in measured_log.read_text(encoding='utf8')
    lines = data.splitlines()
    omit = {i + 1: next(row.split()[1] for row in lines[i+1:] if row.startswith('theorem '))
            for i, row in enumerate(lines) if row.startswith('omit [CompleteSpace F] in')}
    assert len(omit) == 8
    refs = ['PontoZeroDoPsion', 'PontoDeContradicao', 'ThePsionAndTheViscosity', 'QGReaderUVLock',
            'NumberOperator', 'NumberSelfAdjoint', 'F1Fecho394/CanonicalFockModularCoreInputR1',
            'F1Fecho394/BosonicFock', 'F1Fecho394/BosonicSectors', 'F1Fecho394/SectorDirectSum']
    paths = [source, copied, script, ORIGINAL / script.name, receipt, original_log, measured_log,
             ORIGINAL / 'REV17' / 'NOTA_DA_GERENCIA_VETOR_E_MODO_R0.md', CONSOLIDATION,
             HERE / 'build' / (MODULE + '.olean'), *[KERNEL / 'TGLExt' / (r + '.lean') for r in refs]]
    sandbox = Path('C:/t/k411c/final')
    sandbox_check = {}
    for ref in refs:
        relative = Path('TGLExt') / (ref + '.lean')
        assert (KERNEL / relative).read_bytes() == (sandbox / relative).read_bytes()
        olean = sandbox / '.lake/build/lib/lean' / relative.with_suffix('.olean')
        sandbox_check[ref] = {'source_bytes_equal': True, 'object': pin(olean)}
    probe_results = {}
    for name in ['ReviewProbe', 'ReviewRoute']:
        log = HERE / 'build' / (name + '.log')
        probe_results[name] = log_axioms(log)
        paths.extend([HERE / (name + '.lean'), log])
    result = {'pins': [pin(p) for p in paths], 'theorem_axioms': ax, 'omit': omit,
              'scan': canonical_scan(), 'probe_axioms': probe_results, 'sandbox': sandbox_check}
    (HERE / 'VERIFICACAO.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
    print(len(ax), len(omit), result['scan']['lean_files'], result['scan']['packages_within_root'])


if __name__ == '__main__':
    main()
