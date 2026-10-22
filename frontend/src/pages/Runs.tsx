import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type RunsDoc } from '../api'
import { Markers } from '../ui'

// Página /runs — ledger global de execuções forma=conteúdo. Uma linha por run,
// mais recentes primeiro. Todo run tem physical_verdict_allowed=false.
export default function Runs() {
  const [doc, setDoc] = useState<RunsDoc | null>(null)
  useEffect(() => { api.runs().then(setDoc).catch(() => setDoc(null)) }, [])
  if (!doc) return <div className="muted">carregando execuções…</div>

  return (
    <>
      <div className="h1">Execuções · Runners forma = conteúdo</div>
      <div className="sub">
        Cada patente termina num runner único que executa, certifica com SHA-256 e renderiza.
        Um run = results.json + seal.json + figuras + relatório auditável.
      </div>

      <div className="grid stat-row">
        <div className="stat"><div className="n">{doc.runs_total}</div><div className="l">execuções seladas</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--accent-2)' }}>{doc.patents_with_runs}</div><div className="l">patentes com runner real</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--muted)' }}>{doc.patents_total - doc.patents_with_runs}</div><div className="l">aguardando runner</div></div>
        <div className="stat"><div className="n" style={{ color: 'var(--accent-2)' }}>0</div><div className="l">vereditos físicos (por regra)</div></div>
      </div>

      <div className="aviso" style={{ marginTop: 18 }}>{doc.aviso}</div>

      <div className="panel" style={{ marginTop: 4 }}>
        <table className="table">
          <thead><tr>
            <th>Patente</th><th>Run</th><th>Testes</th><th>β runtime</th>
            <th>Veredito máximo</th><th>Marcadores</th><th>result_hash</th>
          </tr></thead>
          <tbody>
            {doc.runs.map(r => (
              <tr key={r.id}>
                <td>
                  <Link to={`/patents/${r.patent_id}`}>{r.display_name}</Link>
                  {r.role === 'agregadora' && <span style={{ color: 'var(--gold)' }}> ★</span>}
                  {r.role === 'raiz' && <span style={{ color: 'var(--accent)' }}> ⬢</span>}
                  <div className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{r.patent_id}</div>
                </td>
                <td className="muted" style={{ fontSize: 11 }}>{r.finished_at}</td>
                <td><b>{r.tests_passed ?? '—'}</b></td>
                <td className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{r.beta_runtime}</td>
                <td className="run-verdict">{r.max_verdict}
                  <div className="phys-false">physical_verdict_allowed: false</div>
                </td>
                <td><Markers items={r.markers} /></td>
                <td className="muted" style={{ fontSize: 10.5, fontFamily: 'monospace' }}>
                  {r.result_hash ? r.result_hash.slice(0, 12) + '…' : '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="muted" style={{ fontSize: 12, marginTop: 10 }}>
          β nunca literal: <code>ALPHA_FINE_CODATA_2018 · √e</code> em runtime
          (= 0.012031300400803142). Cada seal.json contém o SHA-256 de módulos, results e figuras.
        </p>
      </div>
    </>
  )
}
