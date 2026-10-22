import { useEffect, useState } from 'react'
import { api } from '../api'
import { useMe, isAdmin } from '../auth'

// ANEXO — cockpit do backup 3-2-1 (não altera a substância da Central). Só-leitura + botão
// admin. A régua: falha de leitura é falha visível; a senha do cofre NUNCA passa por aqui.

const COR: Record<string, string> = {
  verde: '#30d158', laranja: '#ff9f0a', vermelho: '#ff453a', cinza: '#6b7280',
}
function Dot({ cor }: { cor?: string }) {
  const c = COR[cor || 'cinza'] || COR.cinza
  return <span style={{ display: 'inline-block', width: 11, height: 11, borderRadius: '50%', background: c, boxShadow: `0 0 7px ${c}99`, flex: '0 0 auto' }} />
}
function idade(h?: number | null): string {
  if (h == null) return '—'
  if (h < 1) return 'há minutos'
  if (h < 48) return `há ${Math.round(h)}h`
  return `há ${Math.round(h / 24)} dia(s)`
}

export default function Custodia() {
  const me = useMe()
  const [s, setS] = useState<any>(null)
  const [err, setErr] = useState('')
  const [running, setRunning] = useState(false)
  const load = () => api.backupStatus().then(setS).catch(() => { setS(null); setErr('backend offline (:8765) ou status indisponível') })
  useEffect(() => { load() }, [])

  async function rodarAgora() {
    setErr(''); setRunning(true)
    try {
      await api.backupRun()
      // o run é em background; faz poll até concluir (a régua: falha é falha visível)
      for (let i = 0; i < 90; i++) {
        await new Promise(r => setTimeout(r, 3000))
        const g = await api.backupStatus(); setS(g)
        if (!g?.execucao?.running) break
      }
    } catch (e: any) { setErr('Falha ao disparar o backup: ' + (e?.message || e)) }
    setRunning(false)
  }

  const remoto = s?.ambiente === 'remoto'
  const resumo = s?.resumo
  const camadas: any[] = s?.camadas || []
  const tarefas: any[] = s?.tarefas || []
  const alertas: string[] = resumo?.alertas || []
  const ok = resumo?.ok

  return (
    <>
      <div className="h1">🛡 Custódia / Backup <span style={{ fontSize: 12, color: '#8a94a6', fontWeight: 400 }}>· 3-2-1 blindado · forma = conteúdo</span></div>
      <div className="sub">Onde suas joias estão e se estão frescas. A régua: falha de leitura é falha visível; a <b>senha do cofre nunca passa por aqui</b>.</div>

      {remoto && (
        <div className="aviso" style={{ background: '#0e1a24', borderColor: '#1c3a52', color: '#bfe0f2' }}>
          Este é o <b>backup local</b> (discos D:/Toshiba da sua máquina). Ele só é visível na Central rodando em <code>127.0.0.1:8765</code> — na nuvem, honestamente, não há o que ler.
        </div>
      )}

      {!s && !remoto && <div style={{ color: '#8a94a6', fontSize: 13, marginTop: 12 }}>{err || 'carregando…'}</div>}

      {s && !remoto && (
        <>
          {/* banner de resumo + botão admin */}
          <div style={{ background: ok ? '#0e1a12' : '#1a1206', border: `1px solid ${ok ? '#1f7a3f55' : '#4a3c10'}`, borderRadius: 10, padding: '14px 16px', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
              <div style={{ fontSize: 15, fontWeight: 700, color: ok ? '#30d158' : 'var(--gold, #ffd60a)' }}>
                {ok ? '✅ Protegido' : '⚠ Atenção'}
                <span style={{ fontSize: 12.5, color: '#9aa4b2', fontWeight: 400 }}> · {resumo?.protegido || ''}</span>
              </div>
              {isAdmin(me) && (
                <button className="btn" onClick={rodarAgora} disabled={running} style={{ marginLeft: 'auto' }}>
                  {running ? '⟳ backup rodando…' : '⟳ Rodar backup agora'}
                </button>
              )}
            </div>
            {alertas.map((a, i) => (
              <div key={i} style={{ color: '#ff9f6b', fontSize: 12.5, marginTop: 6 }}>⚠ {a}</div>
            ))}
            {err && <div style={{ color: '#ff6b6b', fontSize: 12, marginTop: 6 }}>{err}</div>}
            {s?.execucao?.running && <div style={{ color: '#9ad0ff', fontSize: 12, marginTop: 6 }}>backup em execução…</div>}
          </div>

          {/* camadas — os semáforos */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12 }}>
            {camadas.map((c) => (
              <div key={c.id} style={{ background: '#0d1720', border: '1px solid #23324a', borderRadius: 10, padding: '12px 14px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Dot cor={c.cor} />
                  <b style={{ color: '#e6ecf3', fontSize: 13 }}>{c.nome}</b>
                </div>
                <div style={{ color: '#c8d0da', fontSize: 12, marginTop: 6, lineHeight: 1.5 }}>{c.detalhe}</div>
                <div style={{ color: '#8a94a6', fontSize: 11.5, marginTop: 6 }}>
                  {(c.ultimo_utc || c.atualizado_utc) ? `último: ${idade(c.idade_horas)}` : (c.presente ? '' : 'ausente')}
                  {c.tamanho_gb != null ? ` · ${c.tamanho_gb} GB` : ''}
                  {c.livre_gb != null ? ` · ${c.livre_gb} GB livres` : ''}
                  {c.disjuntor_ok === false ? ' · 🔴 disjuntor' : ''}
                </div>
              </div>
            ))}
          </div>

          {/* backups automáticos */}
          <div className="panel" style={{ marginTop: 16 }}>
            <h4>Backups automáticos</h4>
            <table className="table">
              <thead><tr><th>Tarefa</th><th>Estado</th><th>Próxima execução</th></tr></thead>
              <tbody>{tarefas.map((t, i) => (
                <tr key={i}>
                  <td>{t.nome}</td>
                  <td style={{ color: /pronto|ready/i.test(t.status || '') ? '#30d158' : '#ff9f6b' }}>{t.status}</td>
                  <td>{t.proxima || '—'}</td>
                </tr>
              ))}</tbody>
            </table>
          </div>

          <div className="aviso" style={{ marginTop: 16, background: '#0e1a24', borderColor: '#1c3a52', color: '#bfe0f2', fontSize: 12.5, lineHeight: 1.7 }}>
            <b>As três honestidades:</b> (1) a <b>senha do cofre</b> existe só na sua cabeça — este painel mostra que ele está presente, <b>nunca</b> a senha. (2) O <b>disjuntor</b> anti-ransomware continua ativo: um backup disparado daqui <b>não propaga</b> apagamento/ataque. (3) Frescor honesto: sem dado = cinza, nunca "verde" falso.
            <div style={{ color: '#667', marginTop: 6 }}>Gerado {s?.gerado_utc}.</div>
          </div>
        </>
      )}
    </>
  )
}
