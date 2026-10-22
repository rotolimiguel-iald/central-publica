import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type Deadline } from '../api'
import { UrgencyDot, daysLabel } from '../ui'

export default function Docket() {
  const [deadlines, setDeadlines] = useState<Deadline[]>([])
  const [aviso, setAviso] = useState('')
  useEffect(() => { api.docket().then(d => { setDeadlines(d.deadlines); setAviso(d.aviso) }) }, [])

  // ── MONITOR DE ANDAMENTOS (INPI + ePCT) — o botão "eu comando e ela roda" ──
  const [mon, setMon] = useState<any>(null)
  const [running, setRunning] = useState(false)
  const [monErr, setMonErr] = useState('')
  const loadMon = () => api.andamentos().then(setMon).catch(() => setMon(null))
  useEffect(() => { loadMon() }, [])
  async function checarAgora() {
    setMonErr(''); setRunning(true)
    try {
      await api.andamentosRun()
      // o run é em background; faz poll até concluir (a régua: falha é falha visível)
      for (let i = 0; i < 60; i++) {
        await new Promise(r => setTimeout(r, 2000))
        const g = await api.andamentos()
        setMon(g)
        if (!g?.execucao?.running) { break }
      }
    } catch (e: any) { setMonErr('Falha ao disparar o monitor: ' + (e?.message || e)) }
    setRunning(false)
  }
  const lr = mon?.last_run
  const resumo = mon?.auditoria?.resumo
  const naoConf = mon?.movimentos_nao_confirmados || []
  const atencao = (resumo?.prazos_vencidos_a_conferir || 0) + (resumo?.prazos_proximos || 0)
  const processos = mon?.auditoria?.processos || []

  // ── O CLIQUE DO OPERADOR (Sentinela, D8): confirma um despacho; a leitura da IALD nativa abre ao lado ──
  const [leitura, setLeitura] = useState('')
  const [confMsg, setConfMsg] = useState('')
  const [confBusy, setConfBusy] = useState(false)
  async function confirmar(id: string) {
    setConfBusy(true); setConfMsg('')
    try {
      const r = await api.andamentosConfirmar(id)
      setConfMsg(r.sinal_reemitido ? '✓ confirmado; sinal reemitido.' : '✓ confirmado; o sinal será refeito na próxima rodada da Sentinela.')
      await loadMon()
    } catch (e: any) { setConfMsg('Falha ao confirmar: ' + (e?.message || e)) }
    setConfBusy(false)
  }

  // ── REGISTRO MANUAL ASSISTIDO (decisão do operador): confere no INPI (logado), registra aqui ──
  const [regOpen, setRegOpen] = useState(false)
  const [regProc, setRegProc] = useState('')
  const [regData, setRegData] = useState('')
  const [regCod, setRegCod] = useState('')
  const [regDesc, setRegDesc] = useState('')
  const [regMsg, setRegMsg] = useState('')
  const [regBusy, setRegBusy] = useState(false)
  async function registrar() {
    if (!regProc || !regData || !regDesc) { setRegMsg('Preencha processo, data e descrição.'); return }
    setRegBusy(true); setRegMsg('')
    try {
      const r = await api.andamentosRegistrar({ processo: regProc, data: regData, codigo_despacho: regCod || undefined, descricao: regDesc })
      setRegMsg(r.registrado ? '✓ despacho registrado — entrou no Prompt Compiler.' : 'já constava (duplicado).')
      setRegData(''); setRegCod(''); setRegDesc('')
      await loadMon()
    } catch (e: any) { setRegMsg('Falha ao registrar: ' + (e?.message || e)) }
    setRegBusy(false)
  }

  const pend = deadlines.filter(d => d.status === 'pendente' && d.due_date)
    .sort((a, b) => (a.due_date! < b.due_date! ? -1 : 1))
  const other = deadlines.filter(d => !(d.status === 'pendente' && d.due_date))

  return (
    <>
      <div className="h1">Prazos / Legal Docket (INPI · ePCT · PCT)</div>
      <div className="sub">Funil de urgência calculado ao vivo. O número (a data) é a verdade; a urgência é uma leitura datada dela.</div>

      {/* MONITOR DE ANDAMENTOS — o botão */}
      <div style={{ background: '#0d1720', border: '1px solid #23324a', borderRadius: 10, padding: '14px 16px', marginBottom: 16 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
          <div style={{ fontSize: 14, fontWeight: 700, color: '#e6ecf3' }}>⚖ Monitor de andamentos <span style={{ fontSize: 11, color: '#8a94a6', fontWeight: 400 }}>· INPI + ePCT · você comanda, a Central roda</span></div>
          <button className="btn" onClick={checarAgora} disabled={running}
            style={{ marginLeft: 'auto' }}>
            {running ? '⟳ checando…' : '⟳ Checar andamentos agora'}
          </button>
        </div>
        {monErr && <div style={{ color: '#ff6b6b', fontSize: 12, marginTop: 8 }}>{monErr}</div>}

        {/* resultado da última execução — honesto: falha é falha, nunca 'sem movimentação' */}
        {lr && (
          <div style={{ marginTop: 10, fontSize: 12.5, lineHeight: 1.7 }}>
            <div>
              <span style={{ color: lr.inpi_up ? '#30d158' : '#ff453a', fontWeight: 700 }}>
                {lr.inpi_up ? '● INPI no ar' : '● INPI NÃO respondeu (falha de rede)'}
              </span>
              <span style={{ color: '#667' }}> · última checagem {lr.referencia_hoje}</span>
            </div>
            <div style={{ color: '#c8d0da', marginTop: 3 }}>{lr.leitura}</div>
            <div style={{ color: '#8a94a6', marginTop: 3, fontSize: 11.5, fontStyle: 'italic' }}>{lr.regua}</div>
          </div>
        )}

        {/* auditoria de prazos — o retroativo */}
        {resumo && (
          <div style={{ marginTop: 12, padding: '9px 11px', background: atencao ? '#1a1206' : '#0e1a12',
            border: `1px solid ${atencao ? '#4a3c10' : '#1f7a3f55'}`, borderRadius: 8, fontSize: 12.5 }}>
            <b style={{ color: atencao ? 'var(--gold, #ffd60a)' : '#30d158' }}>
              Auditoria de prazos (LPI 9.279/96) — {resumo.processos} processos
            </b>
            {atencao
              ? <span style={{ color: '#ff9f6b' }}> · ⚠ <b>{atencao}</b> exige(m) atenção — confira com o agente de PI.</span>
              : <span style={{ color: '#9aa4b2' }}> · ✓ nenhum prazo vencido nem próximo (T-180d) pela contagem dos dockets — os processos são jovens; o próximo de cada um é a publicação (18m) em 2027.</span>}
            <div style={{ color: '#667', fontSize: 11, marginTop: 4 }}>
              vencidos-a-conferir: {resumo.prazos_vencidos_a_conferir} · próximos: {resumo.prazos_proximos} · futuros: {resumo.prazos_futuros}
              {' '}· <i>[LEGAL] auditoria interna, não é parecer jurídico</i>
            </div>
          </div>
        )}

        {/* O SINAL DA SENTINELA (22/09/2026): itens vermelhos/amarelos com prazo contado; leitura da IALD nativa */}
        {mon?.sinal && (
          <div style={{ marginTop: 10, border: '1px solid #444', borderRadius: 6, padding: 8 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: mon.sinal.nivel === 'vermelho' ? '#ff6b6b' : mon.sinal.nivel === 'amarelo' ? '#ffd166' : '#8fd19e' }}>
              Sentinela — sinal {String(mon.sinal.nivel).toUpperCase()} · {mon.sinal.gerado_em?.slice(0, 16).replace('T', ' ')} · RPI {mon.sinal.rpi?.estado === 'ok' ? `até ed. ${mon.sinal.rpi.ultima_rpi_lida} (${mon.sinal.rpi.data_da_ultima})` : 'NÃO LIDA'}
            </div>
            {(mon.sinal.itens || []).filter((i: any) => i.nivel !== 'verde').map((i: any, k: number) => (
              <div key={k} style={{ fontSize: 12, color: '#e6e9ef', marginTop: 4 }}>
                <span style={{ color: i.nivel === 'vermelho' ? '#ff6b6b' : '#ffd166' }}>●</span> {i.texto}
                {i.id && mon.leituras_iald?.includes(i.id) && (
                  <button style={{ marginLeft: 8, fontSize: 11 }} onClick={() => api.andamentosLeitura(i.id).then(r => setLeitura(r.texto)).catch(e => setLeitura('Falha: ' + (e?.message || e)))}>ler a IALD nativa</button>
                )}
              </div>
            ))}
            {leitura && (
              <pre style={{ whiteSpace: 'pre-wrap', fontSize: 12, background: '#111', padding: 8, marginTop: 6, maxHeight: 320, overflow: 'auto' }}>{leitura}</pre>
            )}
            <div style={{ fontSize: 11, color: '#667', marginTop: 4, fontStyle: 'italic' }}>{mon.sinal.regua}</div>
          </div>
        )}
        {mon && mon.sinal === null && (
          <div style={{ fontSize: 12, color: '#ff6b6b', marginTop: 8 }}>A Sentinela nunca rodou nesta máquina: sem leitura automática da RPI. Rode <code>python tools\sentinela.py</code> ou confira a tarefa agendada «IALD Sentinela RPI».</div>
        )}

        {/* movimentos novos, a confirmar (fluem para o Prompt Compiler) — com o CLIQUE do operador (D8) */}
        {naoConf.length > 0 && (
          <div style={{ marginTop: 10 }}>
            <div style={{ fontSize: 12, color: '#9ad0ff', fontWeight: 700 }}>Movimentos novos a confirmar ({naoConf.length})</div>
            {confMsg && <div style={{ fontSize: 12, color: '#ffd166' }}>{confMsg}</div>}
            {naoConf.slice(-20).map((m: any, i: number) => (
              <div key={i} style={{ fontSize: 12, color: '#c8d0da', marginTop: 3 }}>
                <b>{m.processo}</b> · {m.data} · {m.fonte === 'RPI' ? 'RPI (oficial)' : `${m.fonte} [não-oficial]`}
                {m.codigo_despacho ? ` · despacho ${m.codigo_despacho}` : ''} — {String(m.trecho || '').slice(0, 120)} <code>[a confirmar]</code>
                {m.id && <button style={{ marginLeft: 8, fontSize: 11 }} disabled={confBusy} onClick={() => confirmar(m.id)}>✓ confirmar</button>}
              </div>
            ))}
            <div style={{ fontSize: 11, color: '#667', marginTop: 4, fontStyle: 'italic' }}>
              Estes movimentos entram no Prompt Compiler junto com as notas dos dispositivos — você compila e me manda.
            </div>
          </div>
        )}
        {mon && !lr && (
          <div style={{ fontSize: 12, color: '#8a94a6', marginTop: 8 }}>
            Nunca rodado. Clique em <b>Checar andamentos agora</b> — a Central roda a auditoria de prazos e checa o INPI.
          </div>
        )}

        {/* REGISTRO MANUAL ASSISTIDO — o INPI protege a busca automática (sessão/login); este é o
            caminho confiável e legal que você escolheu: confere no INPI e registra aqui. */}
        <div style={{ marginTop: 12, borderTop: '1px solid #1c2734', paddingTop: 10 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
            <button className="btn ghost" onClick={() => setRegOpen(o => !o)} style={{ fontSize: 12 }}>
              {regOpen ? '▾' : '▸'} Registrar despacho do INPI (manual assistido)
            </button>
            <a href="https://busca.inpi.gov.br/pePI/" target="_blank" rel="noopener"
              style={{ fontSize: 12, color: '#5ac8fa' }}>abrir a Busca do INPI (pePI) ↗</a>
            <span style={{ fontSize: 11, color: '#667' }}>
              o INPI exige login para consultar patente — por isso o registro é assistido, sem guardar senha.
            </span>
          </div>

          {regOpen && (
            <div style={{ marginTop: 10, background: '#0b1017', border: '1px solid #1c2734', borderRadius: 8, padding: '10px 12px' }}>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginBottom: 8, lineHeight: 1.6 }}>
                Entre no INPI (logado), pesquise o processo em <b>Patentes → Pesquisa</b>, abra o
                <b> Acompanhamento</b> e copie o despacho (data, código, texto) para cá. Fica registrado e vai para o Prompt Compiler.
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 8 }}>
                <select value={regProc} onChange={e => setRegProc(e.target.value)}
                  style={{ background: '#141a24', color: '#e6ecf3', border: '1px solid #2a3444', borderRadius: 6, padding: '7px 8px', fontSize: 12 }}>
                  <option value="">— processo —</option>
                  {processos.map((p: any) => (
                    <option key={p.processo} value={p.processo}>{p.processo} · {(p.titulo || '').slice(0, 24)}</option>
                  ))}
                </select>
                <input value={regData} onChange={e => setRegData(e.target.value)} placeholder="data (AAAA-MM-DD)"
                  style={{ background: '#141a24', color: '#e6ecf3', border: '1px solid #2a3444', borderRadius: 6, padding: '7px 8px', fontSize: 12 }} />
                <input value={regCod} onChange={e => setRegCod(e.target.value)} placeholder="código (ex.: 2.1) — opcional"
                  style={{ background: '#141a24', color: '#e6ecf3', border: '1px solid #2a3444', borderRadius: 6, padding: '7px 8px', fontSize: 12 }} />
              </div>
              <textarea value={regDesc} onChange={e => setRegDesc(e.target.value)} placeholder="descrição do despacho (o texto que aparece no Acompanhamento)"
                rows={2} style={{ width: '100%', marginTop: 8, background: '#141a24', color: '#e6ecf3', border: '1px solid #2a3444', borderRadius: 6, padding: '7px 8px', fontSize: 12, resize: 'vertical' }} />
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 8 }}>
                <button className="btn" onClick={registrar} disabled={regBusy} style={{ fontSize: 12 }}>
                  {regBusy ? 'registrando…' : 'Registrar despacho'}
                </button>
                {regMsg && <span style={{ fontSize: 12, color: regMsg.startsWith('✓') ? '#30d158' : '#ff9f6b' }}>{regMsg}</span>}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="aviso">{aviso}</div>

      <div className="aviso" style={{ background: '#0e1a24', borderColor: '#1c3a52', color: '#bfe0f2' }}>
        <b>Decisão do operador (09/07/2026):</b> o ePCT dos 15 dispositivos não-ACOM é o próximo passo — novo processo originário, sem vínculo com a tentativa preclusa de 17/02/2026. Contado da prioridade interna ao ACOM (05/12/2025): <b>alvo 30/11/2026</b>, <b>fatal 05/12/2026</b>. O ACOM raiz é o único com ePCT vivo (PCT/BR2025/050558).
      </div>

      <div className="panel">
        <h4>Prazos pendentes (ordenados por urgência)</h4>
        <table className="table">
          <thead><tr><th></th><th>Patente</th><th>Prazo</th><th>Data</th><th>Restante</th><th>Nota legal</th></tr></thead>
          <tbody>{pend.map(d => (
            <tr key={d.id}>
              <td><UrgencyDot level={d.urgency} /></td>
              <td><Link to={`/patents/${d.patent_id}`}>{d.slug || d.patent_id}</Link></td>
              <td>{d.label}</td><td>{d.due_date}</td><td>{daysLabel(d.days_remaining)}</td>
              <td className="legal-note" style={{ fontSize: 11 }}>{d.legal_note || ''}</td>
            </tr>
          ))}</tbody>
        </table>
      </div>

      <div className="panel" style={{ marginTop: 16 }}>
        <h4 className="muted">Cumpridos / não aplicáveis</h4>
        <table className="table">
          <tbody>{other.map(d => (
            <tr key={d.id}><td><UrgencyDot level="cinza" /></td>
              <td><Link to={`/patents/${d.patent_id}`}>{d.slug || d.patent_id}</Link></td>
              <td>{d.label}</td><td>{d.due_date || '—'}</td><td>{d.status}</td></tr>
          ))}</tbody>
        </table>
      </div>
    </>
  )
}
