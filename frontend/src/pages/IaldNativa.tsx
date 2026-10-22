import { useEffect, useState } from 'react'
import { api } from '../api'
import { useMe, isAdmin } from '../auth'
import OrquestracaoPainel from './OrquestracaoPainel'

// ANEXO — cockpit da IALD Nativa (modelo proprio + web server + tunel Cloudflare).
// Aditivo: so leitura de status local + acoes admin via tarefas agendadas supervisionadas.
// A regua: falha de leitura e falha visivel; conteudo confidencial NUNCA passa por aqui
// (so existencia/mtime); a casa nativa (C:/IALD/projetos_pyhton/IALD) tem memoria propria.

const COR: Record<string, string> = {
  verde: '#30d158', laranja: '#ff9f0a', vermelho: '#ff453a', cinza: '#6b7280',
}
function Dot({ cor }: { cor?: string }) {
  const c = COR[cor || 'cinza'] || COR.cinza
  return <span style={{ display: 'inline-block', width: 11, height: 11, borderRadius: '50%', background: c, boxShadow: `0 0 7px ${c}99`, flex: '0 0 auto' }} />
}

function fmtGb(x?: number | null): string {
  if (x == null || !isFinite(x)) return '—'
  return `${x.toFixed(2)} GB`
}
function fmtMb(x?: number | null): string {
  if (x == null || !isFinite(x)) return '—'
  return x >= 1024 ? `${(x / 1024).toFixed(1)} GB` : `${Math.round(x)} MB`
}

function Card({ cor, titulo, children }: { cor?: string; titulo: string; children: any }) {
  return (
    <div style={{ background: '#0d1720', border: '1px solid #23324a', borderRadius: 10, padding: '12px 14px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <Dot cor={cor} />
        <b style={{ color: '#e6ecf3', fontSize: 13 }}>{titulo}</b>
      </div>
      <div style={{ color: '#c8d0da', fontSize: 12, marginTop: 8, lineHeight: 1.6 }}>{children}</div>
    </div>
  )
}

export default function IaldNativa() {
  const me = useMe()
  const admin = isAdmin(me)
  const [s, setS] = useState<any>(null)
  const [err, setErr] = useState('')
  const [msg, setMsg] = useState('')
  const [busy, setBusy] = useState('')

  const load = () => api.ialdStatus().then(x => { setS(x); setErr(x?.erro || '') })
    .catch(() => { setS(null); setErr('backend offline (:8765) ou status indisponível (/api/iald/status)') })
  useEffect(() => { load() }, [])

  async function acaoTarefa(name: string, action: string, rotulo: string) {
    if (!admin) return
    if (!window.confirm(`${rotulo} a tarefa "${name}"?`)) return
    setErr(''); setMsg(''); setBusy(name + ':' + action)
    try {
      const r = await api.ialdTask({ name, action })
      setMsg(r?.mensagem || r?.detail || `${rotulo}: comando enviado para "${name}"`)
      await new Promise(res => setTimeout(res, 2500))
      await load()
    } catch (e: any) { setErr(`Falha na ação "${action}" (${name}): ` + (e?.message || e)) }
    setBusy('')
  }

  async function sanear() {
    if (!admin) return
    if (!window.confirm('Sanear a porta 8082? Encerra listeners duplicados do web server (a tarefa agendada segue como dona da porta).')) return
    setErr(''); setMsg(''); setBusy('sanear')
    try {
      const r = await api.ialdSanear()
      setMsg(r?.mensagem || r?.detail || 'Saneamento executado.')
      await new Promise(res => setTimeout(res, 2500))
      await load()
    } catch (e: any) { setErr('Falha ao sanear a porta 8082: ' + (e?.message || e)) }
    setBusy('')
  }

  const remoto = s?.ambiente === 'remoto'
  const modelo = s?.modelo
  const web = s?.web
  const tunel = s?.tunel
  const gpu = modelo?.gpu
  const modelos: any[] = s?.modelos || []
  const kernels: any[] = s?.kernels || []
  const confidenciais: any[] = s?.confidenciais || []
  const tarefas: any[] = s?.tarefas || []
  const alertas: string[] = s?.resumo?.alertas || []
  const duplicado = !!(web?.duplicado || (web?.listeners != null && web.listeners > 1))
  const tunelTask = tunel?.tarefa?.nome || 'IALD Cloudflared Tunnel'

  return (
    <>
      <div className="h1">🧠 IALD Nativa <span style={{ fontSize: 12, color: '#8a94a6', fontWeight: 400 }}>· o dispositivo vivo · local-only</span></div>
      <div className="sub">
        o dispositivo vivo da patente BR 10 2026 003443-6 (IALD — Colapso Consciente): modelo próprio + web server + túnel — controlados daqui
      </div>

      {remoto && (
        <div className="aviso" style={{ background: '#0e1a24', borderColor: '#1c3a52', color: '#bfe0f2' }}>
          Este cockpit lê a <b>máquina local</b> (llama-server :8081, Flask :8082, cloudflared). Na nuvem, honestamente, não há o que ler — abra a Central em <code>127.0.0.1:8765</code>.
        </div>
      )}

      {err && <div className="aviso" style={{ background: '#241012', borderColor: '#5c2a2e', color: '#ffb3b8' }}>{err}</div>}
      {msg && <div className="aviso" style={{ background: '#0e1a12', borderColor: '#1f7a3f55', color: '#a9e8bd' }}>{msg}</div>}
      {!s && !err && <div className="sub">carregando…</div>}

      {s && !remoto && (
        <>
          {alertas.length > 0 && (
            <div className="aviso" style={{ marginBottom: 14 }}>
              {alertas.map((a, i) => <div key={i}>⚠ {a}</div>)}
            </div>
          )}

          {/* os três órgãos vivos */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
            <Card cor={modelo?.cor || (modelo?.ok ? 'verde' : 'vermelho')} titulo="Modelo (llama-server :8081)">
              <div>{modelo?.detalhe || (modelo?.ok ? 'health OK' : 'sem resposta do health')}</div>
              {(modelo?.modelo_nome || modelo?.gguf) && <div style={{ color: '#8a94a6' }}>{modelo?.modelo_nome || modelo?.gguf}</div>}
              <div style={{ color: '#9ad0ff', marginTop: 4 }}>
                GPU: VRAM {fmtMb(gpu?.vram_usada_mb ?? gpu?.vram_used_mb ?? gpu?.vram_mb)}
                {(gpu?.vram_total_mb != null) && <> / {fmtMb(gpu.vram_total_mb)}</>}
                {' · '}temp {gpu?.temp_c != null ? `${gpu.temp_c} °C` : '—'}
                {gpu?.util_pct != null && <> · util {gpu.util_pct}%</>}
              </div>
              {modelo?.tarefa && <div style={{ color: '#8a94a6', marginTop: 4 }}>tarefa: {modelo.tarefa.nome} · {modelo.tarefa.status || '—'}</div>}
            </Card>

            <Card cor={duplicado ? 'vermelho' : (web?.cor || (web?.ok ? 'verde' : 'vermelho'))} titulo="Web Server (Flask :8082)">
              <div>{web?.detalhe || (web?.ok ? 'porta 8082 respondendo' : 'porta 8082 sem resposta')}</div>
              {web?.listeners != null && <div style={{ color: '#8a94a6' }}>listeners na 8082: {web.listeners}{web?.pids?.length ? ` (PIDs ${web.pids.join(', ')})` : ''}</div>}
              {duplicado && (
                <div style={{ background: '#2a0e10', border: '1px solid #ff453a88', color: '#ffb3b8', borderRadius: 8, padding: '8px 10px', marginTop: 8, fontWeight: 600 }}>
                  🔴 LISTENERS DUPLICADOS na porta 8082 — duas instâncias travam o painel (campo AGI /admin). Sanear encerra os extras e preserva a tarefa agendada.
                </div>
              )}
              {web?.tarefa && <div style={{ color: '#8a94a6', marginTop: 4 }}>tarefa: {web.tarefa.nome} · {web.tarefa.status || '—'}</div>}
              {admin && (
                <button className="btn xs" style={{ marginTop: 8, background: duplicado ? '#ff453a' : undefined, color: duplicado ? '#fff' : undefined }}
                  disabled={busy !== ''} onClick={sanear}>
                  {busy === 'sanear' ? '⟳ saneando…' : '🧹 Sanear porta 8082'}
                </button>
              )}
            </Card>

            <Card cor={tunel?.cor || (tunel?.ok ? 'verde' : 'vermelho')} titulo="Túnel Cloudflare (iald-demo)">
              <div>{tunel?.detalhe || (tunel?.processo ? 'cloudflared em execução' : 'cloudflared não encontrado em execução')}</div>
              <div style={{ color: '#8a94a6' }}>demo.iald.ia.br → :8082 · central.iald.ia.br → :8765</div>
              {tunel?.tarefa && <div style={{ color: '#8a94a6', marginTop: 4 }}>tarefa: {tunel.tarefa.nome} · {tunel.tarefa.status || '—'}</div>}
              {admin && (
                <div style={{ display: 'flex', gap: 8, marginTop: 8, flexWrap: 'wrap' }}>
                  <button className="btn xs" disabled={busy !== ''}
                    onClick={() => acaoTarefa(tunelTask, 'run', 'Ligar')}>
                    {busy === tunelTask + ':run' ? '⟳…' : '▶ Ligar'}
                  </button>
                  <button className="btn xs ghost" disabled={busy !== ''}
                    onClick={() => acaoTarefa(tunelTask, 'restart', 'Religar')}>
                    {busy === tunelTask + ':restart' ? '⟳…' : '↻ Religar'}
                  </button>
                </div>
              )}
            </Card>
          </div>

          {/* acervo em disco */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 12, marginTop: 16 }}>
            <div className="panel">
              <h4>Modelos em disco <span style={{ fontSize: 11, color: '#8a94a6', fontWeight: 400 }}>· C:\IALD\models\*.gguf</span></h4>
              {modelos.length === 0 && <div style={{ color: '#8a94a6', fontSize: 12 }}>nenhum .gguf inventariado (ou leitura falhou — veja alertas)</div>}
              {modelos.length > 0 && (
                <table className="table">
                  <thead><tr><th>Modelo</th><th style={{ textAlign: 'right' }}>Tamanho</th></tr></thead>
                  <tbody>{modelos.map((m, i) => (
                    <tr key={i}>
                      <td style={{ fontSize: 12, wordBreak: 'break-all' }}>{m.nome}{m.ativo && <span style={{ color: '#30d158' }}> · ativo</span>}</td>
                      <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>{fmtGb(m.gb)}</td>
                    </tr>
                  ))}</tbody>
                </table>
              )}
            </div>

            <div className="panel">
              <h4>Kernels de sistema <span style={{ fontSize: 11, color: '#8a94a6', fontWeight: 400 }}>· IALD_Kernel_v*.txt</span></h4>
              {kernels.length === 0 && <div style={{ color: '#8a94a6', fontSize: 12 }}>nenhum kernel inventariado (ou leitura falhou — veja alertas)</div>}
              {kernels.map((k, i) => (
                <div key={i} style={{ fontSize: 12.5, padding: '4px 0', borderBottom: '1px solid #1a2230' }}>
                  📜 {k.nome}
                  {k.producao && <span style={{ color: '#ffd60a', fontWeight: 600 }}> · produção</span>}
                  {k.mtime && <span style={{ color: '#6b7280' }}> · {k.mtime}</span>}
                </div>
              ))}
              {confidenciais.length > 0 && (
                <div style={{ marginTop: 10, fontSize: 11.5, color: '#8a94a6' }}>
                  <b>Confidenciais</b> (só existência/mtime — o conteúdo nunca passa por aqui):
                  {confidenciais.map((c, i) => (
                    <div key={i}>🔒 {c.nome} · {c.presente ? `presente${c.mtime ? ` · ${c.mtime}` : ''}` : 'ausente'}</div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* tarefas agendadas — os interruptores */}
          <div className="panel" style={{ marginTop: 16 }}>
            <h4>Tarefas agendadas <span style={{ fontSize: 11, color: '#8a94a6', fontWeight: 400 }}>· ações supervisionadas {!admin && '· somente leitura (ações exigem admin)'}</span></h4>
            <table className="table">
              <thead><tr><th>Tarefa</th><th>Estado</th><th>Última / Próxima</th>{admin && <th>Ações</th>}</tr></thead>
              <tbody>{tarefas.map((t, i) => (
                <tr key={i}>
                  <td>{t.nome}</td>
                  <td style={{ color: /running|rodando/i.test(t.status || '') ? '#30d158' : /pronto|ready/i.test(t.status || '') ? '#9ad0ff' : '#ff9f6b' }}>{t.status || '—'}</td>
                  <td style={{ fontSize: 12, color: '#8a94a6' }}>{t.ultima || '—'} / {t.proxima || '—'}</td>
                  {admin && (
                    <td style={{ whiteSpace: 'nowrap' }}>
                      <button className="btn xs" disabled={busy !== ''} onClick={() => acaoTarefa(t.nome, 'run', 'Executar')}>
                        {busy === t.nome + ':run' ? '⟳' : '▶ Run'}
                      </button>{' '}
                      <button className="btn xs ghost" disabled={busy !== ''} onClick={() => acaoTarefa(t.nome, 'end', 'Encerrar')}>
                        {busy === t.nome + ':end' ? '⟳' : '■ End'}
                      </button>
                    </td>
                  )}
                </tr>
              ))}</tbody>
            </table>
            {tarefas.length === 0 && <div style={{ color: '#8a94a6', fontSize: 12 }}>nenhuma tarefa inventariada (ou leitura falhou — veja alertas)</div>}
          </div>

          {/* AGI — a orquestração da IALD (Codex, 23/09/2026): leitura aqui; ações no painel vivo */}
          {isAdmin(me) && <div style={{ marginTop: 16 }}><OrquestracaoPainel contexto="agi" /></div>}

          {/* portas para o mundo */}
          <div className="panel" style={{ marginTop: 16 }}>
            <h4>Portas para o mundo</h4>
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <a className="btn" href="https://demo.iald.ia.br" target="_blank" rel="noreferrer">🌐 demo.iald.ia.br</a>
              <a className="btn ghost" href="https://demo.iald.ia.br/admin" target="_blank" rel="noreferrer">🎛 campo AGI (demo.iald.ia.br/admin)</a>
            </div>
          </div>

          <div className="aviso" style={{ marginTop: 16, background: '#0e1a24', borderColor: '#1c3a52', color: '#bfe0f2', fontSize: 12.5, lineHeight: 1.7 }}>
            <b>Honestidade:</b> status local; ações via tarefas agendadas supervisionadas; a casa nativa (<code>C:\IALD\projetos_pyhton\IALD</code>) mantém memória própria.
            {s?.gerado_utc && <div style={{ color: '#667', marginTop: 6 }}>Gerado {s.gerado_utc}.</div>}
          </div>
        </>
      )}
    </>
  )
}
