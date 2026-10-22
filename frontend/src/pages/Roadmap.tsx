import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, type PatentClass, type PatentRow, type RunsDoc } from '../api'
import { UrgencyDot } from '../ui'

// Página /roadmap — cockpit de progresso do acervo. Por classe e patente: status do
// runner forma=conteúdo (testes/veredito), disponibilidade de render, urgência de prazo.
// Client-side: agrega /api/classes + /api/patents + /api/runs.
export default function Roadmap() {
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [patents, setPatents] = useState<PatentRow[]>([])
  const [runsDoc, setRunsDoc] = useState<RunsDoc | null>(null)
  const nav = useNavigate()

  useEffect(() => {
    api.classes().then(setClasses)
    api.patents().then(setPatents)
    api.runs().then(setRunsDoc)
  }, [])

  const runByPatent = useMemo(() => {
    const m = new Map<string, { tests: number | null; verdict: string }>()
    runsDoc?.runs.forEach(r => {
      if (!m.has(r.patent_id)) m.set(r.patent_id, { tests: r.tests_passed, verdict: r.max_verdict })
    })
    return m
  }, [runsDoc])

  const withRunner = runsDoc?.patents_with_runs ?? 0
  const total = patents.length
  const pct = total ? Math.round((withRunner / total) * 100) : 0

  return (
    <>
      <div className="h1">Roadmap · cockpit de progresso</div>
      <div className="sub">
        Cada patente termina num runner forma=conteúdo. Abaixo, o estado de todo o acervo por
        linha de pesquisa (classe). Controle interno — não substitui agente de PI.
      </div>

      <div className="grid stat-row">
        <div className="stat"><div className="n">{withRunner}/{total}</div><div className="l">com runner selado</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--accent-2)' }}>{pct}%</div><div className="l">forma = conteúdo</div></div>
        <div className="stat"><div className="n">{runsDoc?.runs_total ?? 0}</div><div className="l">execuções seladas</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--accent-2)' }}>0</div><div className="l">vereditos físicos (regra)</div></div>
      </div>

      <div className="roadmap-bar">
        <div className="roadmap-bar-fill" style={{ width: `${pct}%` }} />
      </div>

      {classes.map(c => {
        const ps = patents.filter(p => p.class_id === c.id)
        if (ps.length === 0) return null
        const done = ps.filter(p => runByPatent.has(p.id)).length
        return (
          <div className="class-block" key={c.id}>
            <div className="class-head">
              <span className="ord">{String(c.ordinal).padStart(2, '0')}</span>
              <h3>{c.name}</h3>
              <span className="muted" style={{ fontSize: 12 }}>· {done}/{ps.length} runner(s)</span>
            </div>
            <table className="table">
              <thead><tr>
                <th></th><th>Patente</th><th>Runner</th><th>Testes</th>
                <th>Veredito máximo</th><th>Render</th><th>Prazo</th>
              </tr></thead>
              <tbody>
                {ps.map(p => {
                  const run = runByPatent.get(p.id)
                  return (
                    <tr key={p.id} style={{ cursor: 'pointer' }} onClick={() => nav(`/patents/${p.id}`)}>
                      <td>{p.role === 'agregadora' ? <span style={{ color: 'var(--gold)' }}>★</span>
                        : p.role === 'raiz' ? <span style={{ color: 'var(--accent)' }}>⬢</span> : ''}</td>
                      <td>
                        <div style={{ fontWeight: 600 }}>{p.display_name}</div>
                        <div className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{p.id}</div>
                      </td>
                      <td>{run
                        ? <span className="badge mk" style={{ background: '#0e2a1a', color: '#7ce7c8', borderColor: '#1c3a42' }}>selado</span>
                        : <span className="muted">—</span>}</td>
                      <td>{run?.tests ?? '—'}</td>
                      <td className="run-verdict muted">{run ? run.verdict.split(' (')[0] : 'aguardando runner'}</td>
                      <td className="muted" style={{ fontSize: 11 }}>(a) desenho · (b) componentes</td>
                      <td><UrgencyDot level={p.next_urgency} /></td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )
      })}
      <p className="muted" style={{ fontSize: 12, marginTop: 16 }}>
        Runners são scaffolds honestos que demonstram a LÓGICA de cada invenção
        (β = <code>α·√e</code> em runtime; <code>physical_verdict_allowed=false</code> em todo o
        acervo). Promover [SIM]→[DATA] exige dado/hardware real. 1 = 1. Tetelestai.
      </p>
    </>
  )
}
