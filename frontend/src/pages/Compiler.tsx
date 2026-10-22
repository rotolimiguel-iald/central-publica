import { useEffect, useState } from 'react'
import { api, pub } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO

export default function Compiler() {
  const [list, setList] = useState<any[]>([])
  const [preview, setPreview] = useState('')
  const [busy, setBusy] = useState(false)
  const [last, setLast] = useState<any>(null)

  const refresh = () => api.compiledList().then(setList)
  useEffect(() => { refresh() }, [])

  return (
    <>
      <div className="h1">Prompt Compiler — a ponte manual com o Claude Code</div>
      <div className="sub">Consolida todas as notas/instruções marcadas como <b>ativas</b> (nas abas das patentes) num único arquivo. Cole o resultado no Claude Code.</div>

      <div className="panel">
        <button className="btn gold" disabled={busy} onClick={async () => {
          setBusy(true)
          const r = await api.compile()
          setLast(r); setPreview(r.body_preview); await refresh(); setBusy(false)
        }}>{busy ? 'compilando…' : '⇢ COMPILAR INSTRUÇÕES ATIVAS'}</button>
        {last && (
          <p style={{ marginTop: 12, fontSize: 13 }}>
            Gerado <b>{last.filename}</b> · {last.note_count} instrução(ões) ativa(s) ·
            <span className="muted" style={{ fontFamily: 'monospace' }}> sha {last.sha256?.slice(0, 12)}…</span>
          </p>
        )}
        {last?.note_count === 0 && <p className="legal-note">Nenhuma instrução ativa no momento — ative itens nas abas Notas/Instruções das patentes e compile de novo.</p>}
      </div>

      {preview && <div className="panel" style={{ marginTop: 16 }}>
        <h4>Prévia</h4><pre className="md">{preview}…</pre>
      </div>}

      <div className="panel" style={{ marginTop: 16 }}>
        <h4>Prompts compilados</h4>
        {list.length === 0 ? <p className="muted">Nenhum ainda.</p> : (
          <table className="table"><tbody>{list.map(f => (
            <tr key={f.filename}>
              <td><a href={pub(`/api/compiled/${f.filename}`)} target="_blank">{f.filename}</a></td>
              <td className="muted">{f.size} bytes</td>
            </tr>
          ))}</tbody></table>
        )}
      </div>
    </>
  )
}
