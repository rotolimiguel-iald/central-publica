"""Local monitor -> internal follow-up bridge. No network, scheduling or GET writes."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re


def _load_followup(central: Path):
    path = central / 'backend' / 'app' / 'acompanhamento.py'
    spec = importlib.util.spec_from_file_location('patent_followup_storage', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    if path.stat().st_size > 64 * 1024 * 1024:
        raise ValueError('movements.jsonl excede limite de leitura')
    result = []
    for n, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            raise ValueError(f'movements.jsonl: JSON inválido na linha {n}') from None
        if not isinstance(row, dict) or not re.fullmatch(r'[0-9a-f]{16}', str(row.get('id', ''))):
            raise ValueError(f'movements.jsonl: identidade inválida na linha {n}')
        for field in ('processo', 'data', 'detectado_utc'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f'movements.jsonl: campo {field} ausente na linha {n}')
        result.append(row)
    return result


def _process_map(central: Path, storage, known: dict[str, Path]) -> dict[str, str]:
    """Read identity and related process numbers only; never legacy docket status."""
    import yaml
    mapping = {pid: pid for pid in known}
    for pid, folder in known.items():
        docket = folder / 'docket.yaml'
        storage._safe_local_path(central, docket)
        if not docket.exists():
            continue
        if docket.stat().st_size > 1024 * 1024:
            raise ValueError('Docket excede limite de leitura')
        value = yaml.safe_load(docket.read_text(encoding='utf-8-sig'))
        if not isinstance(value, dict):
            raise ValueError('Docket não é objeto: ' + pid)
        aliases = [value.get('processo')]
        additions = value.get('processos_adicionais') or []
        if not isinstance(additions, list):
            raise ValueError('Processos adicionais inválidos: ' + pid)
        aliases.extend(x.get('processo') if isinstance(x, dict) else x for x in additions)
        for number in aliases:
            if not number:
                continue
            if not isinstance(number, str) or not re.fullmatch(r'BR\d{12}-\d', number):
                raise ValueError('Número adicional inválido: ' + pid)
            if number in mapping and mapping[number] != pid:
                raise ValueError('Processo associado a mais de uma família: ' + number)
            mapping[number] = pid
    return mapping


def reconcile(central: Path) -> dict:
    """Reconcile unseen source IDs; retry repairs a prior partial materialization.

    Existing events and their later corrections are left exactly as stored.
    The monitor itself remains responsible for recording the source ledger first.
    """
    central = central.absolute()
    storage = _load_followup(central)
    known = storage.catalog(central)
    source = central / 'andamentos' / 'movements.jsonl'
    storage._safe_local_path(central, source)
    rows = _rows(source)  # strict: malformed source never becomes "no news"
    existing, errors = storage.load_events(central)
    if errors and (central / 'andamentos/acompanhamento/eventos.jsonl').exists():
        raise ValueError('Histórico integrado inválido; ponte interrompida')
    mapping = _process_map(central, storage, known)
    by_id = {e['id']: e for e in existing}
    seen_sources = {(e.get('source_id'), e['patent_id']) for e in existing if e['tipo'] == 'despacho'}
    incoming, snapshots, seen_rows = [], [], {}
    skipped = 0
    for row in rows:
        source_id = row['id']
        if source_id in seen_rows:
            if seen_rows[source_id] != row:
                raise ValueError('Origem duplicada divergente: ' + source_id)
            continue
        seen_rows[source_id] = row
        pid = mapping.get(row['processo'])
        if not pid:
            raise ValueError('Processo sem vínculo ao catálogo: ' + row['processo'])
        event_id = 'rpi-' + source_id
        if event_id in by_id and by_id[event_id]['patent_id'] != pid:
            raise ValueError('Identidade integrada vinculada a outra patente: ' + event_id)
        if event_id in by_id or (source_id, pid) in seen_sources:
            skipped += 1
            continue
        content = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8') + b'\n'
        pin = hashlib.sha256(content).hexdigest()
        snapshot = central / 'andamentos/acompanhamento/fontes/monitor' / (source_id + '_' + pin + '.json')
        event = {
            'id': event_id, 'source_id': source_id,
            'correlation_key': 'monitor:' + row['processo'] + ':' + str(row.get('codigo_despacho') or '') + ':' + row['data'],
            'patent_id': pid, 'processo': row['processo'], 'data': row['data'],
            'observado_em': row['detectado_utc'], 'tipo': 'despacho',
            'titulo': 'Movimento ' + str(row.get('codigo_despacho') or 'sem código') + ' — ' + row['processo'],
            'resumo': str(row.get('trecho') or ''), 'estatuto': 'DECLARADO', 'status': 'a_confirmar',
            'providencia': 'Conferir o documento oficial e registrar a leitura e as providências com fonte. O aviso não comprova cumprimento.',
            'fonte': {'tipo': 'Monitor existente / ' + str(row.get('fonte') or 'não informada'),
                      'referencia': 'movements.jsonl, id ' + source_id + '; retrato imutável da linha de origem'},
            'evidencias': [{'path': str(snapshot), 'sha256': pin, 'label': 'Registro original do movimento ' + source_id}],
        }
        storage.validate_event(event, known)
        incoming.append(event); snapshots.append((snapshot, content))
    # Validate all snapshot/materialization destinations before creating snapshots.
    for event, (snapshot, _) in zip(incoming, snapshots):
        storage._safe_local_path(central, snapshot)
        storage._safe_local_path(central, known[event['patent_id']] / 'andamentos' /
                                 (hashlib.sha256(event['id'].encode()).hexdigest() + '.json'))
    for snapshot, content in snapshots:
        storage._atomic_new(central, snapshot, content)
    result = storage.ingest(central, incoming)
    return {'status': 'sincronizado', 'origens_lidas': len(rows), 'origens_ja_integradas': skipped,
            'novos_eventos': result['adicionados'], 'sha256_ledger': result['sha256_ledger'],
            'cobertura': 'Somente movimentos do monitor; não consulta WIPO nem lê pareceres.'}
