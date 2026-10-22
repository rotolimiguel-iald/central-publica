import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, type PatentClass, type PatentRow } from '../api'
import { Markers, EpctPill } from '../ui'

export default function Classes() {
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [patents, setPatents] = useState<PatentRow[]>([])
  const nav = useNavigate()
  useEffect(() => { api.classes().then(setClasses); api.patents().then(setPatents) }, [])

  return (
    <>
      <div className="h1">Classes — as 10 linhas de pesquisa</div>
      <div className="sub">Cada classe agrupa patentes de uma mesma linha; CLASS_09 é pipeline (rascunhos) e CLASS_10 é o docket transversal.</div>
      {classes.map(c => {
        const ps = patents.filter(p => p.class_id === c.id)
        return (
          <div className="panel" key={c.id} style={{ marginBottom: 14 }}>
            <div className="class-head">
              <span className="ord">{String(c.ordinal).padStart(2, '0')}</span>
              <h3>{c.name}</h3><Markers items={c.markers} />
              <span className="muted" style={{ fontSize: 12 }}>· {ps.length} patente(s)</span>
            </div>
            {c.lock_note && <div className="legal-note" style={{ fontSize: 12, marginBottom: 8 }}>TRAVA: {c.lock_note}</div>}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {ps.map(p => (
                <div key={p.id} onClick={() => nav(`/patents/${p.id}`)}
                  style={{ cursor: 'pointer', border: '1px solid var(--line)', borderRadius: 8, padding: '6px 10px', fontSize: 12 }}>
                  <b>{p.slug}</b> <EpctPill status={p.epct_status} />
                </div>
              ))}
              {ps.length === 0 && <span className="muted" style={{ fontSize: 12 }}>— sem patente depositada (classe de pipeline/transversal)</span>}
            </div>
          </div>
        )
      })}
    </>
  )
}
