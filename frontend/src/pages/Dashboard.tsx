import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, type PatentClass, type PatentRow } from '../api'
import { Markers, UrgencyDot, EpctPill, daysLabel } from '../ui'

export default function Dashboard() {
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [patents, setPatents] = useState<PatentRow[]>([])
  const nav = useNavigate()

  useEffect(() => {
    api.classes().then(setClasses)
    api.patents().then(setPatents)
  }, [])

  const byClass = (cid: string) => patents.filter(p => p.class_id === cid)
  const urgent = patents.filter(p => ['amarelo', 'laranja', 'vermelho', 'vencido'].includes(p.next_urgency || ''))

  return (
    <>
      <div className="h1">Central de Controle e Desenvolvimento de Patentes</div>
      <div className="sub">16 patentes · 10 classes (linhas de pesquisa) · forma = conteúdo. Cada patente termina num runner único que demonstra, certifica com hash e renderiza.</div>

      <div className="grid stat-row">
        <div className="stat"><div className="n">{patents.length}</div><div className="l">patentes depositadas</div></div>
        <div className="stat"><div className="n">{classes.length}</div><div className="l">classes / linhas</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--gold)' }}>{urgent.length}</div><div className="l">em prazo de atenção</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--accent-2)' }}>1</div><div className="l">ePCT vivo (ACOM)</div></div>
      </div>

      {urgent.length > 0 && (
        <div className="aviso" style={{ marginTop: 18 }}>
          ⚠ <b>{urgent.length} patentes</b> com prazo de atenção — janela de Paris do novo ePCT: alvo <b>30/11/2026</b>, fatal <b>05/12/2026</b>. Ver <a href="#/docket">Prazos / Docket</a>. Controle interno não substitui agente de PI.
        </div>
      )}

      {classes.map(c => {
        const ps = byClass(c.id)
        if (ps.length === 0) return null
        return (
          <div className="class-block" key={c.id}>
            <div className="class-head">
              <span className="ord">{String(c.ordinal).padStart(2, '0')}</span>
              <h3>{c.name}</h3>
              <Markers items={c.markers} />
              <span className="muted" style={{ fontSize: 12 }}>· {ps.length} patente(s)</span>
            </div>
            <div className="cards">
              {ps.map(p => (
                <div className="card" key={p.id} onClick={() => nav(`/patents/${p.id}`)}>
                  {p.role === 'agregadora' && <span className="star" title="agregadora">★</span>}
                  {p.role === 'raiz' && <span className="star" title="raiz" style={{ color: 'var(--accent)' }}>⬢</span>}
                  <div className="devname">{p.display_name}</div>
                  <div className="ttl">{p.title_54}</div>
                  <div className="pid">{p.id}</div>
                  <div className="foot">
                    <UrgencyDot level={p.next_urgency} />
                    <EpctPill status={p.epct_status} />
                    <span>· {p.claims_total ?? '—'} reiv.</span>
                    <span style={{ marginLeft: 'auto' }}>{p.next_due ? daysLabel(
                      Math.round((new Date(p.next_due).getTime() - Date.now()) / 86400000)) : '—'}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </>
  )
}
