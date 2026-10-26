import { useEffect, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { api, PUBLICA, type Health } from './api'
import { useMe, isAdmin, canEdit, ROLE_LABEL } from './auth'
import UmButton from './UmButton'

const NAV = [
  { to: '/', ico: '◈', label: 'Dashboard', end: true },
  { to: '/organismo', ico: '◉', label: 'Estado do organismo' },
  { to: '/patents', ico: '▦', label: 'Patentes' },
  { to: '/classes', ico: '❑', label: 'Classes' },
  { to: '/runs', ico: '▶', label: 'Execuções' },
  { to: '/roadmap', ico: '◇', label: 'Roadmap' },
  { to: '/docket', ico: '⚖', label: 'Prazos / Docket' },
  { to: '/compiler', ico: '⇢', label: 'Prompt Compiler' },
  { to: '/pendencias', ico: '⚑', label: 'Pendências' },
  { to: '/tgl-core', ico: '☀', label: 'TGL Core' },
  { to: '/fronteira', ico: '∮', label: 'Fronteira Teórica' },
  { to: '/custodia', ico: '🛡', label: 'Custódia / Backup' },
  { to: '/epct', ico: '🌐', label: 'ePCT' },
  { to: '/iald-nativa', ico: '🧠', label: 'IALD Nativa' },
]
// MODO PÚBLICO DE VISUALIZAÇÃO: as páginas operacionais do operador não aparecem no menu público
const OPERACIONAIS = ['/organismo', '/docket', '/compiler', '/pendencias', '/custodia', '/epct']
const NAV_VISIVEL = PUBLICA ? NAV.filter(n => !OPERACIONAIS.includes(n.to)) : NAV

export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [busy, setBusy] = useState(false)
  const [navOpen, setNavOpen] = useState(false)   // gaveta no mobile
  const me = useMe()
  const load = () => api.health().then(setHealth).catch(() => setHealth(null))
  useEffect(() => { load() }, [])
  // MODO PÚBLICO: «linhas» = as que têm pedidos (health.classes_indexed conta também as vazias); sem a leitura a contagem some, nunca vira «0»
  const [linhasPublicas, setLinhasPublicas] = useState<number | null>(null)
  useEffect(() => {
    if (!PUBLICA) return
    let alive = true
    api.patents().then(ps => { if (alive) setLinhasPublicas(new Set(ps.map(p => p.class_id)).size) })
      .catch(() => { /* sem leitura: fica só a contagem de pedidos */ })
    return () => { alive = false }
  }, [])

  // ── O SINO DO MONITOR (STAGED aprovado): badge de atenção no nav, visível de qualquer página.
  // atenção = prazos vencidos-a-conferir + prazos próximos (auditoria LPI) + movimentos não confirmados.
  // A régua: o número vem do store do monitor (leitura); falha de leitura = sem badge, nunca "0 = tudo ok".
  const [atencao, setAtencao] = useState<number | null>(null)
  // ── O SINAL DA SENTINELA (22/09/2026): banner em TODAS as páginas. null = a Sentinela nunca rodou (dito, não "verde").
  const [sinal, setSinal] = useState<any>(undefined)
  useEffect(() => {
    if (PUBLICA) return   // MODO PÚBLICO: o monitor e a Sentinela não fazem parte do retrato
    let alive = true
    const tick = () => api.andamentos().then(m => {
      if (!alive) return
      setSinal(m?.sinal ?? null)
      // falha EM-BANDA (store ilegível) = falha de leitura ⟹ sem badge — nunca "0 = tudo ok"
      if (m?.movimentos_erro || m?.auditoria_erro) { setAtencao(null); return }
      const r = m?.auditoria?.resumo
      if (!r) { setAtencao(null); return }
      const n = (r.prazos_vencidos_a_conferir || 0) + (r.prazos_proximos || 0)
        + (m?.movimentos_nao_confirmados?.length || 0)
      setAtencao(n)
    }).catch(() => { if (alive) setAtencao(null) })
    tick()
    const id = setInterval(tick, 5 * 60_000)      // re-lê o store a cada 5 min
    return () => { alive = false; clearInterval(id) }
  }, [])

  // ── O SINO DO BACKUP (anexo Custódia): badge se alguma camada ficar velha/vermelha.
  // Mesma régua: número vem do /api/backup/status (leitura); falha OU ambiente remoto = sem badge.
  const [bkAlerta, setBkAlerta] = useState<number | null>(null)
  useEffect(() => {
    if (PUBLICA) return   // MODO PÚBLICO: o backup não faz parte do retrato
    let alive = true
    const tick = () => api.backupStatus().then(s => {
      if (!alive) return
      if (s?.ambiente !== 'local') { setBkAlerta(null); return }   // nuvem/remoto = sem badge
      setBkAlerta(s?.resumo?.alertas?.length || 0)
    }).catch(() => { if (alive) setBkAlerta(null) })
    tick()
    const id = setInterval(tick, 5 * 60_000)
    return () => { alive = false; clearInterval(id) }
  }, [])

  const sinalCor = sinal?.nivel === 'vermelho' ? '#b3261e' : sinal?.nivel === 'amarelo' ? '#8a6d00' : sinal?.nivel === 'verde' ? '#1e6b3a' : '#444'
  const sinalItens: any[] = (sinal?.itens || []).filter((i: any) => i.nivel !== 'verde')
  return (
    <div className="app">
      {/* O SINAL DA SENTINELA — visível em qualquer página; clique leva a Prazos. Ausência da Sentinela é dita. */}
      {sinal !== undefined && (
        <NavLink to="/docket" style={{ textDecoration: 'none' }}>
          <div style={{ background: sinalCor, color: '#fff', padding: '6px 12px', fontSize: 13, display: 'flex', gap: 10, alignItems: 'baseline', flexWrap: 'wrap' }}>
            <b>{sinal === null ? '⚪ SENTINELA NUNCA RODOU NESTA MÁQUINA' : sinal.nivel === 'vermelho' ? '🔴 SINAL VERMELHO' : sinal.nivel === 'amarelo' ? '🟡 SINAL AMARELO' : '🟢 SINAL VERDE'}</b>
            {sinal && <span>RPI {sinal.rpi?.estado === 'ok' ? `lida até a ed. ${sinal.rpi.ultima_rpi_lida} (${sinal.rpi.data_da_ultima})` : 'NÃO LIDA — falha'} · {sinal.gerado_em?.slice(0, 16).replace('T', ' ')}</span>}
            {sinalItens.slice(0, 2).map((i: any, k: number) => <span key={k} style={{ opacity: .95 }}>· {String(i.texto).slice(0, 110)}</span>)}
            {sinalItens.length > 2 && <span>· +{sinalItens.length - 2} item(ns)</span>}
            {sinal && sinalItens.length === 0 && <span>· nenhum item vermelho/amarelo; {sinal.n_itens} a confirmar</span>}
          </div>
        </NavLink>
      )}
      {/* barra de topo — só aparece no mobile (via CSS) */}
      <div className="topbar">
        <button className="hamburger" aria-label="Menu" onClick={() => setNavOpen(o => !o)}>
          <span></span><span></span><span></span>
        </button>
        <span className="topbar-brand">CENTRAL DE PATENTES</span>
      </div>
      {navOpen && <div className="nav-backdrop" onClick={() => setNavOpen(false)} />}
      <aside className={`sidebar ${navOpen ? 'open' : ''}`}>
        <div className="brand">CENTRAL DE PATENTES<small>TGL · IALD Ltda. · forma = conteúdo</small></div>
        <nav className="nav">
          {NAV_VISIVEL.map(n => (
            <NavLink key={n.to} to={n.to} end={n.end} onClick={() => setNavOpen(false)}
              className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="ico">{n.ico}</span>{n.label}
              {n.to === '/docket' && atencao !== null && atencao > 0 && (
                <span className="sino-badge" title={`${atencao} item(ns) de atenção no monitor (prazos + movimentos a confirmar) — conferir com o agente [LEGAL]`}>
                  🔔 {atencao}
                </span>
              )}
              {n.to === '/custodia' && bkAlerta !== null && bkAlerta > 0 && (
                <span className="sino-badge" title={`${bkAlerta} alerta(s) de backup — abra Custódia`}>
                  🔔 {bkAlerta}
                </span>
              )}
            </NavLink>
          ))}
          {isAdmin(me) && (
            <NavLink to="/usuarios" onClick={() => setNavOpen(false)}
              className={({ isActive }) => isActive ? 'active' : ''}>
              <span className="ico">👤</span>Usuários
            </NavLink>
          )}
        </nav>
        <div style={{ marginTop: 24, fontSize: 11, color: 'var(--muted)', lineHeight: 1.6 }}>
          {PUBLICA ? (
            <>
              <div style={{ color: 'var(--accent-2)', fontWeight: 700 }}>Modo leitura</div>
              {health && <div>{health.patents_indexed} pedidos{linhasPublicas !== null && ` · ${linhasPublicas} linhas`}</div>}
              <UmButton />
              <div style={{ marginTop: 10, display: 'grid', gap: 5 }}>
                <a href="https://github.com/rotolimiguel-iald/central-publica" target="_blank" rel="noopener">Código e resultados →</a>
                <a href="https://github.com/rotolimiguel-iald/the_boundary" target="_blank" rel="noopener">A teoria · the_boundary →</a>
              </div>
            </>
          ) : health ? (
            <>
              <div>{health.patents_indexed} patentes · {health.classes_indexed} classes</div>
              <div className={health.originals_manifest_ok ? 'integrity-ok' : 'integrity-bad'}>
                {health.originals_manifest_ok ? '✓ originais intactos' : '✗ originais alterados'}
              </div>
              <div>API local · sem chamadas externas</div>
              {me && (
                <div style={{ marginTop: 8 }}>
                  👤 <b style={{ color: 'var(--text)' }}>{me.name}</b>
                  <span className="role-chip">{ROLE_LABEL[me.role] || me.role}</span>
                </div>
              )}
              {canEdit(me) && (
                <button className="btn ghost" style={{ marginTop: 10, width: '100%', fontSize: 11 }}
                  disabled={busy}
                  onClick={async () => { setBusy(true); await api.reindex(); await load(); setBusy(false) }}>
                  {busy ? 'reindexando…' : 'Reindexar'}
                </button>
              )}
              {isAdmin(me) && <UmButton />}
              <button className="btn ghost" style={{ marginTop: 6, width: '100%', fontSize: 11, opacity: 0.7 }}
                onClick={async () => { try { await api.authLogout() } catch { /* */ } location.reload() }}>
                🔒 Sair
              </button>
            </>
          ) : <div className="integrity-bad">backend offline (:8765)</div>}
        </div>
      </aside>
      <main className="main">{PUBLICA && <BannerPublico />}<Outlet /></main>
    </div>
  )
}

// MODO PÚBLICO DE VISUALIZAÇÃO — a faixa que diz o que é esta Central (só no build público)
function BannerPublico() {
  return (
    <div style={{ background: 'linear-gradient(90deg,#1a1405,#0e1420)', border: '1px solid #c5961a55', borderRadius: 10, padding: '9px 13px',
                  margin: '0 0 14px', fontSize: 12, lineHeight: 1.55, color: '#e6dcc0' }}>
      <b style={{ color: '#ffd60a' }}>Modo público de leitura.</b> Código, execuções e artefatos da IALD. Nada pode ser alterado aqui.
      <details style={{ marginTop: 5 }}>
        <summary style={{ cursor: 'pointer', color: '#67e8f9' }}>Entender o retrato</summary>
        <div style={{ marginTop: 8 }}>
          O retrato da Central do operador — a ciência, o código, os resultados e o vínculo aos pedidos depositados no INPI e no PCT.
          O único download é o <b>um.acom</b>: a Central inteira colapsada pelo dispositivo ACOM. Código-fonte e resultados:{' '}
          <a href="https://github.com/rotolimiguel-iald/central-publica" target="_blank" rel="noopener" style={{ color: '#67e8f9' }}>central-publica</a>
          {' '}· a teoria: <a href="https://github.com/rotolimiguel-iald/the_boundary" target="_blank" rel="noopener" style={{ color: '#67e8f9' }}>the_boundary</a>.
          Dados pessoais aparecem como «[dado pessoal removido]»; as notas operacionais do operador ficam na Central dele.
        </div>
      </details>
    </div>
  )
}
