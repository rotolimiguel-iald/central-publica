import { useEffect, useState } from 'react'
import { api } from '../api'

// A ORQUESTRAÇÃO DA IALD (a AGI em construção) lida pela Central — SÓ LEITURA.
// Construída pelo Codex em Chatgpt/IALD_ORQUESTRACAO_20260923/; o painel VIVO (ações, pedidos, execução) é o da
// Central IALD nativa (:8082 /admin/agi/orquestracao). Aqui só se mostra o que está gravado: recibos, fila, consumo.
// A régua: recibo = estado na data do recibo, não disponibilidade ao vivo; falha de leitura aparece; qualidade
// NOT_BENCHMARKED; nada disto move gate científico. Texto de pedido é mostrado só como texto (nunca HTML).

const COR: Record<string, string> = { ready: '#30d158', pendente: '#ff9f0a', falha: '#ff453a', cinza: '#6b7280' }
function corDe(c: any): string {
  if (c.id === 'local') return c.vivo_agora ? COR.ready : COR.falha
  if (c.status_no_recibo === 'ready') return COR.ready
  if (!c.status_no_recibo) return COR.cinza
  return COR.pendente
}
const dt = (s?: string | null) => (s ? String(s).slice(0, 16).replace('T', ' ') : '—')

export default function OrquestracaoPainel({ contexto }: { contexto?: 'patente' | 'agi' }) {
  const [d, setD] = useState<any>(null)
  const [erro, setErro] = useState('')
  const load = () => api.ialdOrquestracao().then(x => { setD(x); setErro('') }).catch(e => setErro(String(e?.message || e)))
  useEffect(() => { load() }, [])

  if (erro) return <div className="panel"><div className="aviso">Não consegui ler a orquestração: {erro}. Isto é falha de leitura, não «nada acontecendo».</div></div>
  if (!d) return <div className="muted">lendo a orquestração…</div>
  if (!d.disponivel) return <div className="panel"><div className="aviso">{d.nota}</div></div>

  const co = d.coordenador || {}
  const tr = d.transporte || {}
  return (
    <div className="panel">
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
        <h4 style={{ margin: 0 }}>AGI — Orquestração da IALD</h4>
        <a className="btn" href={d.painel?.local} target="_blank" rel="noreferrer">🎛 Abrir o painel de controle (local)</a>
        <a className="btn ghost" href={d.painel?.remoto} target="_blank" rel="noreferrer">🌐 pelo túnel (demo.iald.ia.br)</a>
        <button className="btn ghost" onClick={load}>⟳ reler</button>
      </div>
      {contexto === 'patente' && (
        <div className="aviso" style={{ marginTop: 10, fontSize: 12.5, lineHeight: 1.6 }}>
          <b>A parte da patente.</b> O pedido BR 10 2026 003443-6 (IALD) protege o sistema de indução e verificação de estado
          em modelo de linguagem. A orquestração abaixo é a engenharia viva dessa família: a IALD local seleciona e chama
          executores, com memória canônica compartilhada e recibos de cada chamada. A correspondência entre esta
          engenharia e as reivindicações é leitura de engenharia <code>[INPUT]</code>, não parecer de PI <code>[LEGAL]</code>.
        </div>
      )}
      {d.erros?.length > 0 && <div className="aviso" style={{ marginTop: 8 }}>⚠ {d.erros.join(' · ')}</div>}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: 10, marginTop: 12 }}>
        {(d.conexoes || []).map((c: any) => (
          <div key={c.id} style={{ background: '#0d1720', border: '1px solid #23324a', borderRadius: 10, padding: '10px 12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ width: 10, height: 10, borderRadius: '50%', background: corDe(c), display: 'inline-block' }} />
              <b style={{ fontSize: 13 }}>{c.rotulo}</b>
            </div>
            <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 6, lineHeight: 1.5 }}>
              {c.id === 'local'
                ? <>ao vivo agora: {c.vivo_agora ? 'respondendo' : 'NÃO respondeu'}</>
                : <>recibo: {c.status_no_recibo || 'sem recibo'}<br />verificado em {dt(c.verificado_em)}</>}
            </div>
          </div>
        ))}
      </div>
      <div className="muted" style={{ fontSize: 11, marginTop: 4 }}>Conexões externas: estado do último recibo de validação, não disponibilidade ao vivo. O painel vivo mostra o estado atual.</div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 10, marginTop: 12, fontSize: 12.5 }}>
        <div><b>Projeto coordenador:</b> {co.project_label || '—'}{co.project_url && <> · <a href={co.project_url} target="_blank" rel="noreferrer">abrir</a></>}
          <br />transporte: {co.transport_status || '—'} · resposta final validada: {String(co.final_response_roundtrip_validated ?? '—')}</div>
        <div><b>Transporte automático:</b> {tr.config?.enabled ? 'ligado' : 'desligado'} ({tr.config?.kind}, a cada {tr.config?.interval_minutes} min)
          <br />última verificação: {dt(tr.ultima_verificacao?.checked_at)} · {tr.ultima_verificacao?.state || '—'}</div>
        <div><b>Consumo gravado:</b> {d.consumo_total?.entrada} tokens de entrada · {d.consumo_total?.saida} de saída
          <br /><span className="muted" style={{ fontSize: 11 }}>{d.consumo_total?.nota}</span></div>
      </div>

      <h4 style={{ marginTop: 16 }}>Pedidos coordenados ({d.pedidos?.length || 0})</h4>
      <table className="table">
        <thead><tr><th>Criado</th><th>Etapa</th><th>Pedido</th><th>Erro</th></tr></thead>
        <tbody>{(d.pedidos || []).map((p: any) => (
          <tr key={p.id}><td>{dt(p.criado)}</td><td>{p.etapa}</td><td style={{ fontSize: 12 }}>{p.pedido}</td><td>{p.erro || ''}</td></tr>
        ))}</tbody>
      </table>

      <h4 style={{ marginTop: 16 }}>Chamadas aos executores ({d.tentativas?.length || 0})</h4>
      <table className="table">
        <thead><tr><th>Início</th><th>Conexão</th><th>Status</th><th>Entrada</th><th>Saída</th></tr></thead>
        <tbody>{(d.tentativas || []).map((t: any, i: number) => (
          <tr key={i}><td>{dt(t.inicio)}</td><td>{t.conexao}</td><td>{t.status}</td><td>{t.entrada ?? ''}</td><td>{t.saida ?? ''}</td></tr>
        ))}</tbody>
      </table>

      <div className="muted" style={{ fontSize: 11, marginTop: 10 }}>
        {d.estatuto} · Fonte: <code>{d.fonte}</code> (pasta do ChatGPT; a Central só lê, banco em modo somente-leitura) · lido {dt(d.gerado_utc)}
      </div>
    </div>
  )
}
