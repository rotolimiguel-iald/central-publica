import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, type PatentClass, type PatentRow } from '../api'
import { UrgencyDot, EpctPill, daysLabel } from '../ui'

// Página /patents — lista tabular de todas as patentes, filtrável e ordenável.
// Complementa o Dashboard (agrupado por classe) com uma visão densa e buscável.
export default function Patents() {
  const [patents, setPatents] = useState<PatentRow[]>([])
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [q, setQ] = useState('')
  const [cls, setCls] = useState('')
  const nav = useNavigate()

  useEffect(() => {
    api.patents().then(setPatents)
    api.classes().then(setClasses)
  }, [])

  const clsName = useMemo(() => Object.fromEntries(classes.map(c => [c.id, c.name])), [classes])
  const rows = patents.filter(p => {
    if (cls && p.class_id !== cls) return false
    if (!q.trim()) return true
    const s = q.toLowerCase()
    return p.display_name.toLowerCase().includes(s) || p.id.toLowerCase().includes(s)
      || p.title_54.toLowerCase().includes(s)
  })

  return (
    <>
      <div className="h1">Patentes · {patents.length} depositadas</div>
      <div className="sub">Lista completa filtrável. Clique para abrir a página da patente (12 abas).</div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 14, flexWrap: 'wrap' }}>
        <input className="txt" style={{ flex: 1, minWidth: 220 }} placeholder="buscar por nome, nº do processo ou título…"
          value={q} onChange={e => setQ(e.target.value)} />
        <select className="txt" value={cls} onChange={e => setCls(e.target.value)}>
          <option value="">todas as classes</option>
          {classes.map(c => <option key={c.id} value={c.id}>{String(c.ordinal).padStart(2, '0')} · {c.name}</option>)}
        </select>
      </div>

      <div className="panel">
        <table className="table">
          <thead><tr>
            <th></th><th>Patente</th><th>Classe</th><th>Depósito</th>
            <th>ePCT</th><th>Reiv.</th><th>Protótipo</th><th>Prazo</th>
          </tr></thead>
          <tbody>
            {rows.map(p => (
              <tr key={p.id} style={{ cursor: 'pointer' }} onClick={() => nav(`/patents/${p.id}`)}>
                <td>{p.role === 'agregadora' ? <span style={{ color: 'var(--gold)' }}>★</span>
                  : p.role === 'raiz' ? <span style={{ color: 'var(--accent)' }}>⬢</span> : ''}</td>
                <td>
                  <div style={{ fontWeight: 600 }}>{p.display_name}</div>
                  <div className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{p.id}</div>
                </td>
                <td className="muted" style={{ fontSize: 12 }}>{clsName[p.class_id] || p.class_id}</td>
                <td className="muted" style={{ fontSize: 12 }}>{p.filing_date}</td>
                <td><EpctPill status={p.epct_status} /></td>
                <td>{p.claims_total ?? '—'}</td>
                <td className="muted" style={{ fontSize: 11 }}>{p.prototype_status}</td>
                <td>
                  <UrgencyDot level={p.next_urgency} />{' '}
                  {p.next_due ? daysLabel(Math.round((new Date(p.next_due).getTime() - Date.now()) / 86400000)) : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && <p className="muted" style={{ marginTop: 10 }}>Nenhuma patente para este filtro.</p>}
      </div>
    </>
  )
}
