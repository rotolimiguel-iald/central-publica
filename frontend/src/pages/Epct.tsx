import { useEffect, useState } from 'react'
import { api } from '../api'
import { useMe, isAdmin } from '../auth'

// ANEXO ePCT — conferência do protocolo internacional dos 15 dispositivos.
// A régua: prazo é [LEGAL] (o painel alerta; a conferência final é do operador com o
// agente da PI). Tiques gravados em EPCT/epct_status.json via backend (admin).

function corPrazo(dias: number | null | undefined): string {
  if (dias == null) return '#6b7280'
  if (dias < 0) return '#ff453a'
  if (dias <= 60) return '#ff453a'
  if (dias <= 120) return '#ff9f0a'
  return '#30d158'
}

function BadgePrazo({ dias, deadline }: { dias: number | null; deadline: string | null }) {
  const c = corPrazo(dias)
  const txt = dias == null ? 'sem dossiê' : dias < 0 ? `VENCIDO há ${-dias}d` : `${dias} dias`
  return (
    <span title={deadline ? `prazo fatal (prioridade 12 meses): ${deadline}` : 'prazo não extraído'}
      style={{ background: `${c}22`, color: c, border: `1px solid ${c}55`, borderRadius: 12, padding: '2px 10px', fontSize: 12, fontWeight: 600, whiteSpace: 'nowrap' }}>
      ⏳ {txt}
    </span>
  )
}

export default function Epct() {
  const me = useMe()
  const admin = isAdmin(me)
  const [s, setS] = useState<any>(null)
  const [err, setErr] = useState('')
  const [busyKey, setBusyKey] = useState('')
  const [aberto, setAberto] = useState<string | null>(null)

  const load = () => api.epctStatus().then(setS).catch(() => { setS(null); setErr('backend offline (:8765) ou status indisponível') })
  useEffect(() => { load() }, [])

  async function tick(id: string, step: string, value: boolean) {
    if (!admin) return
    setBusyKey(id + ':' + step); setErr('')
    try { setS(await api.epctTick({ id, step, value })) }
    catch (e: any) { setErr('Falha ao gravar o tique: ' + (e?.message || e)) }
    setBusyKey('')
  }

  async function gravarCampo(id: string, campo: string, atual: string | null) {
    if (!admin) return
    const v = window.prompt(campo === 'pct_number' ? 'Número PCT (ex.: PCT/BR2026/000123):' : campo === 'protocol_date' ? 'Data do protocolo (YYYY-MM-DD):' : 'Nota:', atual || '')
    if (v === null) return
    setErr('')
    try { setS(await api.epctTick({ id, step: campo, value: v })) }
    catch (e: any) { setErr('Falha ao gravar: ' + (e?.message || e)) }
  }

  const devices: any[] = s?.devices || []
  const total = s?.total ?? 0
  const done = s?.concluidos ?? 0
  const urgentes: string[] = s?.urgentes || []

  return (
    <>
      <div className="h1">🌐 ePCT <span style={{ fontSize: 12, color: '#8a94a6', fontWeight: 400 }}>· protocolo internacional · {done}/{total} concluídos</span></div>
      <div className="sub">
        Conferência do protocolo dos 15 dispositivos. Pacotes em <code>EPCT/&lt;ID&gt;/</code> (4 documentos separados — o vício de 2026 não se repete).
        Prazo é <b>[LEGAL]</b>: o painel alerta, mas a conferência final é sua com a agente da PI.
      </div>

      {err && <div className="aviso" style={{ background: '#241012', borderColor: '#5c2a2e', color: '#ffb3b8' }}>{err}</div>}
      {!s && !err && <div className="sub">carregando…</div>}

      {s && (
        <div style={{ margin: '10px 0 16px' }}>
          <div style={{ height: 10, background: '#1a2230', borderRadius: 6, overflow: 'hidden' }}>
            <div style={{ width: `${total ? (100 * done / total) : 0}%`, height: '100%', background: 'linear-gradient(90deg,#2ea8ff,#30d158)', transition: 'width .4s' }} />
          </div>
          <div style={{ fontSize: 12, color: '#8a94a6', marginTop: 4 }}>
            {done}/{total} protocolados · {urgentes.length > 0 && <span style={{ color: '#ff9f0a' }}>⚠ {urgentes.length} com prazo ≤ 60 dias</span>}
            {!admin && <span> · somente leitura (tiques exigem admin)</span>}
          </div>
        </div>
      )}

      {devices.map(d => (
        <div key={d.id} className="card" style={{ marginBottom: 10, padding: 14, border: d.concluido ? '1px solid #30d15844' : undefined }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', cursor: 'pointer' }} onClick={() => setAberto(aberto === d.id ? null : d.id)}>
            <span style={{ fontSize: 16 }}>{d.concluido ? '✅' : '⬜'}</span>
            <div style={{ flex: 1, minWidth: 220 }}>
              <div style={{ fontWeight: 600 }}>{d.title}</div>
              <div style={{ fontSize: 12, color: '#8a94a6' }}>
                {d.br_number || d.id} · depósito {d.filing_date || '?'} {d.pct_number && <span style={{ color: '#30d158' }}> · {d.pct_number}</span>}
              </div>
            </div>
            <BadgePrazo dias={d.days_left} deadline={d.priority_deadline} />
            <span style={{ fontSize: 12, color: '#8a94a6' }}>{d.n_done}/{d.n_steps}</span>
            <span style={{ color: '#8a94a6' }}>{aberto === d.id ? '▾' : '▸'}</span>
          </div>

          {aberto === d.id && (
            <div style={{ marginTop: 10, borderTop: '1px solid #1a2230', paddingTop: 10 }}>
              {!d.dossie_ok && <div className="aviso" style={{ background: '#241a10', borderColor: '#5c452a', color: '#ffd9a8' }}>Dossiê ainda não gerado (00_DOSSIE.json ausente) — a fábrica de pacotes ainda está produzindo ou falhou; confira a pasta.</div>}
              {d.steps.map((st: any) => (
                <label key={st.key} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '4px 0', cursor: admin ? 'pointer' : 'default', opacity: busyKey === d.id + ':' + st.key ? 0.5 : 1 }}>
                  <input type="checkbox" checked={st.done} disabled={!admin || busyKey !== ''}
                    onChange={e => tick(d.id, st.key, e.target.checked)} />
                  <span style={{ fontSize: 13, textDecoration: st.done ? 'line-through' : 'none', color: st.done ? '#8a94a6' : undefined }}>{st.label}</span>
                </label>
              ))}
              <div style={{ display: 'flex', gap: 8, marginTop: 8, flexWrap: 'wrap' }}>
                <button className="btn" disabled={!admin} onClick={() => gravarCampo(d.id, 'pct_number', d.pct_number)}>nº PCT{d.pct_number ? `: ${d.pct_number}` : ''}</button>
                <button className="btn" disabled={!admin} onClick={() => gravarCampo(d.id, 'protocol_date', d.protocol_date)}>data{d.protocol_date ? `: ${d.protocol_date}` : ''}</button>
                <button className="btn" disabled={!admin} onClick={() => gravarCampo(d.id, 'nota', d.nota)}>nota{d.nota ? ' ✎' : ''}</button>
              </div>
              {d.nota && <div style={{ fontSize: 12, color: '#bfe0f2', marginTop: 6 }}>🗒 {d.nota}</div>}
              <div style={{ fontSize: 11, color: '#6b7280', marginTop: 8 }}>
                pacote: {d.package_files.length ? d.package_files.join(' · ') : '(vazio)'}
              </div>
            </div>
          )}
        </div>
      ))}

      {s && devices.length === 0 && (
        <div className="aviso">Nenhuma subpasta <code>EPCT/BR*</code> encontrada ainda — a fábrica de pacotes está rodando.</div>
      )}
    </>
  )
}
