import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, PUBLICA, type PatentClass, type PatentRow } from '../api'
import { UrgencyDot, EpctPill, daysLabel } from '../ui'

// Página /patents — tabela no desktop e cartões no mobile, sempre filtrável.
export default function Patents() {
  const [patents, setPatents] = useState<PatentRow[]>([])
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [q, setQ] = useState('')
  const [cls, setCls] = useState('')
  const nav = useNavigate()   // 24/10 (cetico final): a linha da tabela volta a navegar ao clique, como antes; os links ficam para o teclado

  useEffect(() => {
    api.patents().then(setPatents)
    // 24/10 (achado do revisor): no retrato /api/classes pode faltar — a tabela segue (a classe cai para o identificador);
    // na Central do operador a falha continua como era
    api.classes().then(setClasses).catch(e => { if (!PUBLICA) throw e })
  }, [])

  const clsName = useMemo(() => Object.fromEntries(classes.map(c => [c.id, c.name])), [classes])
  const rows = patents.filter(p => {
    if (cls && p.class_id !== cls) return false
    if (!q.trim()) return true
    const s = q.toLowerCase()
    return p.display_name.toLowerCase().includes(s) || p.id.toLowerCase().includes(s)
      || p.title_54.toLowerCase().includes(s)
  })
  const prazo = (p: PatentRow) => p.next_due
    ? daysLabel(Math.round((new Date(p.next_due).getTime() - Date.now()) / 86400000))
    : '—'

  return (
    <>
      <div className="h1">Patentes · {patents.length} depositadas</div>
      <div className="sub">Lista completa filtrável. Abra um pedido para ver seus artefatos.</div>

      <div className="patent-filters" style={{ display: 'flex', gap: 8, marginBottom: 14, flexWrap: 'wrap' }}>
        <input className="txt" style={{ flex: 1, minWidth: 220 }} placeholder="buscar por nome, nº do processo ou título…"
          aria-label="Buscar por nome, número do processo ou título" value={q} onChange={e => setQ(e.target.value)} />
        <select className="txt" aria-label="Filtrar por classe" value={cls} onChange={e => setCls(e.target.value)}>
          <option value="">todas as classes</option>
          {classes.map(c => <option key={c.id} value={c.id}>{String(c.ordinal).padStart(2, '0')} · {c.name}</option>)}
        </select>
      </div>

      <div className="panel patents-table-wrap">
        <table className="table">
          <thead><tr>
            <th></th><th>Patente</th><th>Classe</th><th>Depósito</th>
            <th>{PUBLICA ? 'PCT' : 'ePCT'}</th><th>Reiv.</th><th>Protótipo</th>{!PUBLICA && <th>Prazo</th>}
          </tr></thead>
          <tbody>
            {rows.map(p => (
              <tr key={p.id} style={{ cursor: 'pointer' }} onClick={e => { if (!(e.target as HTMLElement).closest('a')) nav(`/patents/${p.id}`) }}>
                <td>{p.role === 'agregadora' ? <span style={{ color: 'var(--gold)' }}>★</span>
                  : p.role === 'raiz' ? <span style={{ color: 'var(--accent)' }}>⬢</span> : ''}</td>
                <td>
                  <Link to={`/patents/${p.id}`} style={{ fontWeight: 600 }}>{p.display_name}</Link>
                  <div className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{p.id}</div>
                </td>
                <td className="muted" style={{ fontSize: 12 }}>{clsName[p.class_id] || p.class_id}</td>
                <td className="muted" style={{ fontSize: 12 }}>{p.filing_date}</td>
                {/* 24/10 (achado do revisor): no retrato público não há epct_status (há o número PCT) nem prazo */}
                <td>{PUBLICA ? (p.epct_number || '—') : <EpctPill status={p.epct_status} />}</td>
                <td>{p.claims_total ?? '—'}</td>
                <td className="muted" style={{ fontSize: 11 }}>{p.prototype_status}</td>
                {!PUBLICA && <td><UrgencyDot level={p.next_urgency} />{' '}{prazo(p)}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="patent-mobile-list">
        {rows.map(p => (
          <Link className="patent-mobile-card" to={`/patents/${p.id}`} key={p.id}
            aria-label={`Abrir artefatos de ${p.display_name}`}>
            <span className="patent-mobile-head">
              <strong>{p.display_name}</strong>
              {p.role === 'agregadora' ? <span style={{ color: 'var(--gold)' }}>★</span>
                : p.role === 'raiz' ? <span style={{ color: 'var(--accent)' }}>⬢</span> : null}
            </span>
            <span className="patent-mobile-id">{p.id}</span>
            <span className="patent-mobile-class">{clsName[p.class_id] || p.class_id}</span>
            <span className="patent-mobile-title">{p.title_54}</span>
            <span className="patent-mobile-meta">
              {PUBLICA ? <span>{p.epct_number || '—'}</span> : <EpctPill status={p.epct_status} />}
              <span>{p.claims_total ?? '—'} reiv.</span>
              <span>{p.filing_date}</span>
              {!PUBLICA && <span><UrgencyDot level={p.next_urgency} /> {prazo(p)}</span>}
            </span>
            <span className="patent-mobile-open">Abrir artefatos →</span>
          </Link>
        ))}
      </div>
      {rows.length === 0 && <p className="muted" style={{ marginTop: 10 }}>Nenhuma patente para este filtro.</p>}
    </>
  )
}
