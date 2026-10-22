import React from 'react'
import { useEffect, useState, type ReactNode } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { api, pub, PUBLICA, type PatentDetail, type EvidenceClaim, type EvidenceElo, type EvolucaoDoc } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO
import { Markers, UrgencyDot, EpctPill, daysLabel } from '../ui'
import DeepZoom from '../DeepZoom'
import ComponentMap from '../ComponentMap'
import Render3D from '../Render3D'
import { canEdit, isAdmin, useMe } from '../auth'
import IaldAppUsuarios from './IaldAppUsuarios'
import OrquestracaoPainel from './OrquestracaoPainel'

const TABS = ['Overview', 'Dispositivo', 'Documentos', 'Código', 'Reivindicações', 'Protótipo',
  'Render 2D/3D', 'Runner', 'Execuções', 'Evolução', 'Selo/Hash', 'Prazos', 'Notas', 'Instruções']

// Aba extra SÓ da patente IALD e SÓ para o administrador: controle de acesso ao app da IALD.
const IALD_PATENTE = 'BR102026003443-6'
const ABA_APP = 'Usuários do app'
const ABA_AGI = 'AGI · Orquestração'

// dispositivos com interface funcional (software que roda de verdade)
// As patentes cujo dispositivo RODA DE VERDADE. Só entra aqui o que existe: uma patente sem
// algoritmo de software executável não ganha "dispositivo" — isso seria teatro, não invento.
const FUNCTIONAL_DEVICES: Record<string, string> = {
  'BR102025026951-1': 'acom',
  'BR102026003441-0': 'tgl_tensor',
}

export default function PatentPage() {
  const { id = '' } = useParams()
  const [p, setP] = useState<PatentDetail | null>(null)
  const [memory, setMemory] = useState('')
  const [tab, setTab] = useState('Overview')
  const nav = useNavigate()
  const me = useMe()
  const abaApp = id === IALD_PATENTE && isAdmin(me)
  const tabs = abaApp ? [...TABS, ABA_AGI, ABA_APP] : TABS

  const load = () => { api.patent(id).then(setP); api.patentMemory(id).then(setMemory) }
  useEffect(() => { load() }, [id])
  // a aba escolhida sobrevive à troca de patente; a do app não pode ficar "presa" fora da IALD
  useEffect(() => { if ((tab === ABA_APP || tab === ABA_AGI) && !abaApp) setTab('Overview') }, [tab, abaApp])
  if (!p) return <div className="muted">carregando…</div>

  const dk = p.docket || {}
  return (
    <>
      <div style={{ fontSize: 12, color: 'var(--muted)' }}>
        <Link to="/">Dashboard</Link> / {p.class?.name} /
      </div>
      <div className="h1" style={{ marginTop: 6 }}>
        {p.display_name} {p.role === 'agregadora' && <span style={{ color: 'var(--gold)' }}>★</span>}
        {p.role === 'raiz' && <span style={{ color: 'var(--accent)' }}> ⬢ raiz</span>}
      </div>
      <div className="sub"><span style={{ fontFamily: 'monospace' }}>{p.id}</span> · {p.title_54}</div>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <EpctPill status={p.epct_status} /><Markers items={p.markers} />
      </div>

      {PUBLICA && <VinculoPatentario v={(p as any).vinculo_patentario} />}
      <div className="tabs">
        {tabs.map(t => (
          <div key={t} className={`tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{t}</div>
        ))}
        {!PUBLICA && <div className="tab" style={{ marginLeft: 'auto', color: 'var(--gold)' }}
          onClick={() => nav('/compiler')}>⇢ Compilar instruções</div>}
      </div>

      {tab === 'Overview' && (
        <div className="panel">
          <div className="kv">
            <div className="k">Processo INPI</div><div>{p.id}</div>
            <div className="k">Classe</div><div>{p.class?.name}</div>
            <div className="k">Papel</div><div>{p.role || '—'}</div>
            <div className="k">Natureza</div><div>{p.nature}</div>
            {!PUBLICA && <><div className="k">Petição</div><div>{p.peticao}</div></>}
            <div className="k">Depósito INPI</div><div>{p.filing_date}</div>
            <div className="k">Prioridade</div><div>{p.priority_date}</div>
            {PUBLICA ? <><div className="k">PCT (OMPI)</div><div>{p.epct_number || '—'}</div></>
                     : <><div className="k">Situação ePCT</div><div><EpctPill status={p.epct_status} /> {p.epct_number || ''}</div></>}
            <div className="k">Reivindicações</div><div>{p.claims_total ?? '—'} ({p.claims_independent ?? '—'} independentes)</div>
            <div className="k">Documentos</div><div>{p.documents.length}</div>
            <div className="k">Protótipo</div><div>{p.prototype_status}</div>
            {!PUBLICA && <><div className="k">Pasta original</div><div className="muted">{p.pasta_original}</div></>}
          </div>
          {p.abstract && <><h4>Resumo oficial</h4><p style={{ fontSize: 13, lineHeight: 1.5 }}>{p.abstract}</p></>}
          {!PUBLICA && <details style={{ marginTop: 16 }}>
            <summary style={{ cursor: 'pointer', color: 'var(--accent)' }}>Memória técnica completa</summary>
            <pre className="md">{memory}</pre>
          </details>}
        </div>
      )}

      {tab === 'Documentos' && (
        <div className="panel">
          <table className="table">
            <thead><tr><th>Papel</th><th>Arquivo</th><th>SHA-256</th><th>Págs</th><th></th></tr></thead>
            <tbody>
              {p.documents.map(d => (
                <tr key={d.id} style={d.proof ? { background: '#151206' } : undefined}>
                  <td>{d.proof && <span title="classe PROVA — citado na Cadeia de Prova das reivindicações" style={{ marginRight: 5 }}>⭐</span>}{d.doc_role}</td>
                  <td className="muted" style={{ fontSize: 12 }}>{d.rel_path.split('\\').pop()}</td>
                  <td className="muted" style={{ fontSize: 11, fontFamily: 'monospace' }}>{d.sha256?.slice(0, 16)}…</td>
                  <td>{d.pages ?? '—'}</td>
                  <td><a href={pub(`/api/documents/${d.id}/text`)} target="_blank">texto</a> · <a href={pub(`/api/documents/${d.id}/file`)} target="_blank">PDF</a></td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="muted" style={{ fontSize: 12, marginTop: 10 }}>⭐ = <b>classe PROVA</b>: documento citado na Cadeia de Prova das reivindicações (aba Reivindicações → clique no marcador). Documentos originais em <code>Patentes\</code> são READ-ONLY. A plataforma serve o texto extraído e o PDF, nunca edita o original.</p>
        </div>
      )}

      {tab === 'Dispositivo' && (FUNCTIONAL_DEVICES[id] === 'tgl_tensor'
        ? <TensorDeviceTab pid={id} />
        : <DeviceTab pid={id} p={p} />)}

      {tab === 'Código' && <CodeTab pid={id} />}

      {tab === 'Reivindicações' && <ClaimsTab pid={id} p={p} />}

      {tab === 'Protótipo' && (
        <div className="panel">
          <h4>Protótipo — apresentação visual do dispositivo</h4>
          <p className="muted" style={{ fontSize: 12.5 }}>Status do protótipo: <b>{p.prototype_status}</b>. Abaixo, os desenhos técnicos do depósito INPI (role/scroll para ampliar). O detalhamento completo está na aba <b>Render 2D/3D</b>.</p>
          {p.id === 'BR102026004850-0' && <p className="legal-note">SkyGrid: gêmeo digital vivo em <code>Patentes\Skygrid\SkyGrid_Piloto\</code> (v1/v2/v3, 156 verificações, MODEL_CLOSES). Runner real já executado — ver aba Execuções.</p>}
          {p.renders.length > 0
            ? <div style={{ marginTop: 12 }}><DeepZoom url={pub(`/api/renders/${p.renders[0].id}`)} height={460} /></div>
            : <p className="legal-note">Sem desenhos rasterizados para esta patente ainda.</p>}
        </div>
      )}

      {tab === 'Runner' && (
        <div className="panel">
          <h4>Runner único forma = conteúdo</h4>
          <p style={{ fontSize: 13 }}>Runner: <code>patents/{p.dir_name}/runner/one_{p.slug.toLowerCase()}.py</code></p>
          <p className="muted" style={{ fontSize: 12.5 }}>Status do protótipo: <b>{p.prototype_status}</b>. O runner nasce scaffold honesto ([PILOTO]/[SIM]/[OPEN]/[DATA_REQUIRED]) e só demonstra números reais quando há protótipo/dado. <b>Simulação nunca valida física</b> (physical_verdict_allowed=false). Cada rodada gera results.json + seal.json + figuras (aba Execuções / Selo).</p>
          {p.runs.length > 0 && <p className="integrity-ok" style={{ fontSize: 12.5 }}>✓ {p.runs.length} execução(ões) real(is) registrada(s). Último veredito: {p.runs[0].max_verdict}.</p>}
        </div>
      )}

      {tab === 'Render 2D/3D' && <RenderTab p={p} />}

      {tab === 'Execuções' && (
        <div className="panel">
          {p.runs.length === 0 ? <p className="muted">Nenhuma execução registrada ainda. O runner produz results.json + seal.json a cada rodada.</p> : (
            <table className="table">
              <thead><tr><th>Run</th><th>Fim</th><th>Status</th><th>β runtime</th><th>Testes</th><th>Veredito</th></tr></thead>
              <tbody>{p.runs.map((r: any) => (
                <tr key={r.id}><td>{r.id}</td><td>{r.finished_at}</td><td>{r.status}</td>
                  <td>{r.beta_runtime}</td><td>{r.tests_passed ?? '—'}</td><td className="muted">{r.max_verdict}</td></tr>
              ))}</tbody>
            </table>
          )}
        </div>
      )}

      {tab === 'Evolução' && <EvolucaoTab pid={id} />}

      {tab === 'Selo/Hash' && (
        <div className="panel">
          <h4>Selo / Hash</h4>
          <p className="muted" style={{ fontSize: 12.5 }}>Cada run gera seal.json com SHA-256 de tudo. Os documentos de depósito têm hash imutável (aba Documentos). Integridade dos originais verificável no menu lateral (Reindexar re-hasheia Patentes\).</p>
          {p.runs.filter((r: any) => r.result_hash).map((r: any) => (
            <div key={r.id} style={{ fontFamily: 'monospace', fontSize: 11, marginTop: 8 }}>
              <div>result_hash: {r.result_hash}</div>
              <div>invariants: {r.invariants_hash}</div>
            </div>
          ))}
        </div>
      )}

      {tab === 'Prazos' && (
        <div className="panel">
          <div className="aviso">{dk.aviso || 'Controle interno. Não substitui agente de propriedade industrial.'}</div>
          <table className="table">
            <thead><tr><th></th><th>Prazo</th><th>Data</th><th>Restante</th><th>Status</th><th>Base</th></tr></thead>
            <tbody>{p.deadlines.map(d => (
              <tr key={d.id}>
                <td><UrgencyDot level={d.urgency} /></td>
                <td>{d.label}</td><td>{d.due_date || '—'}</td>
                <td>{daysLabel(d.days_remaining)}</td><td>{d.status}</td>
                <td className="muted" style={{ fontSize: 11 }}>{d.basis}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}

      {(tab === 'Notas' || tab === 'Instruções') && (
        <NotesTab p={p} onChange={load} kindsFilter={tab === 'Instruções'
          ? ['instrucao', 'tarefa', 'bloqueio', 'pergunta'] : ['nota', 'sugestao']} />
      )}

      {/* re-checa patente E papel no próprio bloco — não confia só na lista de abas */}
      {tab === ABA_APP && id === IALD_PATENTE && p.id === IALD_PATENTE && isAdmin(me) && <IaldAppUsuarios />}
      {tab === ABA_AGI && id === IALD_PATENTE && p.id === IALD_PATENTE && isAdmin(me) && <OrquestracaoPainel contexto="patente" />}
    </>
  )
}

const ROLE_LABEL: Record<string, string> = {
  final: 'CÓDIGO FINAL (auto-contido)', runner: 'runner (demonstra + sela)',
  prototype: 'protótipo resgatado', core: 'núcleo destilado', manifest: 'manifesto (hashes)', outro: 'outros',
}
const ROLE_ORDER = ['final', 'runner', 'prototype', 'core', 'manifest', 'outro']

// ---- Reivindicações: síntese fiel extraída da memória técnica (marcada [REAL]) ----
const MARKER_RE = /\[(REAL|SIM|LEGAL|OPEN|DATA|DER|PILOTO|CONJ|POSTULATE|DATA_REQUIRED|MEDICAL|ENERGY)\]/g

function fmtInline(text: string): ReactNode[] {
  // negrito **...** + chips de marcador [REAL]/[SIM]/...
  const out: ReactNode[] = []
  let key = 0
  // primeiro separa marcadores, depois negrito dentro de cada pedaço
  const pushBold = (s: string) => {
    const parts = s.split(/(\*\*[^*]+\*\*)/g)
    for (const part of parts) {
      if (!part) continue
      if (part.startsWith('**') && part.endsWith('**'))
        out.push(<strong key={key++}>{part.slice(2, -2)}</strong>)
      else out.push(<span key={key++}>{part}</span>)
    }
  }
  let last = 0
  text.replace(MARKER_RE, (m, _g, idx: number) => {
    if (idx > last) pushBold(text.slice(last, idx))
    out.push(<span key={key++} className="claim-marker">{m.slice(1, -1)}</span>)
    last = idx + m.length
    return m
  })
  if (last < text.length) pushBold(text.slice(last))
  return out
}

interface ClaimLine { indent: number; text: string; independent: boolean; num: string | null }

function parseClaims(md: string): { intro: string[]; lines: ClaimLine[] } {
  const intro: string[] = []
  const lines: ClaimLine[] = []
  for (const raw of md.split('\n')) {
    if (!raw.trim()) continue
    const bullet = raw.match(/^(\s*)-\s+(.*)$/)
    if (!bullet) { intro.push(raw.trim()); continue }
    const indent = Math.floor(bullet[1].replace(/\t/g, '  ').length / 2)
    const text = bullet[2].trim()
    const numMatch = text.match(/^\*{0,2}(\d+)\s*\(/)
    const independent = /independente/i.test(text)   // honesto: só as marcadas "(independente...)"
    lines.push({ indent, text, independent, num: numMatch ? numMatch[1] : null })
  }
  return { intro, lines }
}

function ClaimsTab({ pid, p }: { pid: string; p: PatentDetail }) {
  const [doc, setDoc] = useState<any>(null)
  const [evMap, setEvMap] = useState<Record<number, EvidenceClaim>>({})
  const [openProof, setOpenProof] = useState<number | null>(null)
  useEffect(() => {
    setDoc(null); setEvMap({}); setOpenProof(null)
    api.claims(pid).then(setDoc).catch(() => setDoc({ available: false }))
    api.evidence(pid).then(d => {
      const m: Record<number, EvidenceClaim> = {}
      if (d.available) for (const c of d.claims) m[c.n] = c
      setEvMap(m)
    }).catch(() => setEvMap({}))
  }, [pid])
  if (!doc) return <div className="panel"><p className="muted">carregando reivindicações…</p></div>

  return (
    <div className="panel">
      <div className="claim-stats">
        <div className="claim-stat"><b>{p.claims_total ?? doc.claims_total ?? '—'}</b><span>no total</span></div>
        <div className="claim-stat"><b>{p.claims_independent ?? doc.claims_independent ?? '—'}</b><span>independentes</span></div>
      </div>
      {!doc.available ? (
        <p className="muted" style={{ fontSize: 13 }}>
          Síntese fiel ainda não localizada na memória técnica desta patente. O detalhamento
          verbatim está no PDF de depósito (aba Documentos).
        </p>
      ) : (
        <>
          {doc.section_title && <div className="claim-section-title">{doc.section_title}</div>}
          {(() => {
            const { intro, lines } = parseClaims(doc.markdown)
            return (
              <>
                {intro.map((t, i) => (
                  <p key={i} className="claim-intro">{fmtInline(t)}</p>
                ))}
                <div className="claim-list">
                  {lines.map((ln, i) => {
                    const ev = ln.num ? evMap[Number(ln.num)] : undefined
                    const open = ev && openProof === Number(ln.num)
                    return (
                      <div key={i}>
                        <div
                          className={`claim-item ${ln.independent ? 'independent' : 'dependent'}`}
                          style={{ marginLeft: ln.indent * 18 }}>
                          {ln.num && <span className={`claim-num ${ln.independent ? 'ind' : ''}`}>{ln.num}</span>}
                          {/* remove o número do início mas preserva o "**" que abre o negrito do rótulo */}
                          <div className="claim-text">
                            {fmtInline(ln.num ? ln.text.replace(/^(\*{0,2})\d+\s*/, '$1') : ln.text)}
                            {ev && (
                              <button
                                className={`proof-badge ${ev.marker} ${open ? 'open' : ''}`}
                                onClick={() => setOpenProof(open ? null : Number(ln.num))}
                                title="ver a cadeia de prova desta reivindicação">
                                🔗 {ev.marker} · prova ({ev.chain.length}) {open ? '▾' : '▸'}
                              </button>
                            )}
                          </div>
                        </div>
                        {open && <ProofChain claim={ev!} pid={pid} indent={ln.indent} />}
                      </div>
                    )
                  })}
                </div>
              </>
            )
          })()}
          <p className="legal-note" style={{ marginTop: 16 }}>{doc.note}</p>
        </>
      )}
    </div>
  )
}

// ---- Cadeia de Prova: os elos que comprovam uma reivindicação ----
const ELO_ICON: Record<string, string> = {
  deposito: '📄', teste: '🧪', codigo: '💻', dispositivo: '⚙', figura: '🖼', dado: '📊', nota: '⚖',
}
const ELO_LABEL: Record<string, string> = {
  deposito: 'Depósito INPI', teste: 'Teste (runner + selo)', codigo: 'Código', dispositivo: 'Dispositivo',
  figura: 'Figura', dado: 'Dado', nota: 'Honestidade',
}

function eloLink(pid: string, e: EvidenceElo): string | null {
  if (e.doc_id != null) return pub(`/api/documents/${e.doc_id}/file`)
  if (e.code_path) return pub(`/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(e.code_path)}`)
  return null
}

function ProofChain({ claim, pid, indent }: { claim: EvidenceClaim; pid: string; indent: number }) {
  const hash = (e: EvidenceElo) => e.live_sha256 || e.indexed_sha256 || e.result_hash
  return (
    <div className="proof-chain" style={{ marginLeft: indent * 18 + 36 }}>
      <div className="proof-head">
        Cadeia de prova · reivindicação {claim.n} · <b>[{claim.marker}]</b>
        {claim.verdict && <span className="proof-verdict"> — {claim.verdict}</span>}
      </div>
      {claim.chain.map((e, i) => {
        const link = eloLink(pid, e)
        const h = hash(e)
        return (
          <div key={i} className={`proof-elo ${e.resolved ? 'ok' : 'bad'}`}>
            <div className="pe-icon">{ELO_ICON[e.role] || '•'}</div>
            <div className="pe-body">
              <div className="pe-title">
                <span className="pe-role">{ELO_LABEL[e.role] || e.role}</span>
                <span className="pe-name">{e.title}</span>
                {e.resolved ? <span className="pe-ok">✓</span> : <span className="pe-bad">✗</span>}
              </div>
              <div className="pe-proves">{e.proves}{e.value && <> — <b>{e.value}</b></>}</div>
              <div className="pe-meta">
                {e.hash_match === true && <span className="pe-verified">SHA-256 confere</span>}
                {e.test_passed && <span className="pe-verified">teste passou</span>}
                {h && <span className="pe-hash" title={h}>{h.slice(0, 20)}…</span>}
                {link && <a className="pe-open" href={link} target="_blank" rel="noreferrer">abrir ↗</a>}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// ---- Dispositivo: o dispositivo funcionando (interface real) ----
function b64utf8(b64: string): string {
  const bin = atob(b64)
  const bytes = Uint8Array.from(bin, c => c.charCodeAt(0))
  return new TextDecoder('utf-8').decode(bytes)
}
const fmtBytes = (b: number) =>
  b < 1024 ? `${b} B` : b < 1048576 ? `${(b / 1024).toFixed(1)} KB` : b < 1073741824 ? `${(b / 1048576).toFixed(2)} MB` : `${(b / 1073741824).toFixed(2)} GB`

// ── Empacotador ACOM (web): envelope autocontido MAGIC + header{files} + payloads ──
type PackItem = { path: string; file: File }
const PACK_MAGIC = new Uint8Array([0x41, 0x43, 0x4f, 0x4d, 0x55, 0x50, 0x31, 0x00]) // "ACOMUP1\0"
function buildEnvelope(items: PackItem[]): Blob {
  const header = JSON.stringify({ files: items.map(i => ({ path: i.path, len: i.file.size })) })
  const hb = new TextEncoder().encode(header)
  const lenBuf = new Uint8Array(4); new DataView(lenBuf.buffer).setUint32(0, hb.length, false) // big-endian
  return new Blob([PACK_MAGIC, lenBuf, hb, ...items.map(i => i.file)])   // Blob referencia os arquivos (não copia p/ RAM)
}
function walkEntry(entry: any, prefix: string, out: PackItem[]): Promise<void> {
  return new Promise(resolve => {
    if (entry.isFile) entry.file((f: File) => { out.push({ path: prefix + entry.name, file: f }); resolve() }, () => resolve())
    else if (entry.isDirectory) {
      const reader = entry.createReader()
      const readBatch = () => reader.readEntries(async (ents: any[]) => {
        if (!ents.length) return resolve()
        for (const e of ents) await walkEntry(e, prefix + entry.name + '/', out)
        readBatch()
      }, () => resolve())
      readBatch()
    } else resolve()
  })
}
async function itemsFromDrop(dt: DataTransfer): Promise<PackItem[]> {
  const out: PackItem[] = []
  const entries = Array.from(dt.items).map(i => (i as any).webkitGetAsEntry?.()).filter(Boolean)
  if (entries.length) { for (const ent of entries) await walkEntry(ent, '', out) }
  else for (const f of Array.from(dt.files)) out.push({ path: (f as any).webkitRelativePath || f.name, file: f })
  return out
}
function itemsFromInput(files: FileList | null): PackItem[] {
  if (!files) return []
  return Array.from(files).map(f => ({ path: (f as any).webkitRelativePath || f.name, file: f }))
}

function DropZone({ label, hint, accept, busy, onFile }:
  { label: string; hint: string; accept?: string; busy: boolean; onFile: (f: File) => void }) {
  const [over, setOver] = useState(false)
  return (
    <div className={`dropzone ${over ? 'over' : ''} ${busy ? 'busy' : ''}`}
      onDragOver={e => { e.preventDefault(); setOver(true) }}
      onDragLeave={() => setOver(false)}
      onDrop={e => { e.preventDefault(); setOver(false); if (e.dataTransfer.files[0]) onFile(e.dataTransfer.files[0]) }}
      onClick={() => !busy && (document.getElementById('dz-' + label) as HTMLInputElement)?.click()}>
      <input id={'dz-' + label} type="file" accept={accept} style={{ display: 'none' }}
        onChange={e => { if (e.target.files?.[0]) onFile(e.target.files[0]); e.target.value = '' }} />
      <div className="dz-icon">{busy ? '⏳' : '⬇'}</div>
      <div className="dz-label">{busy ? 'processando…' : label}</div>
      <div className="dz-hint">{hint}</div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════════════════════════════
//  TGL-TENSOR — a aba própria. Não reusa a do ACOM de propósito: aqui não há
//  empacotador nem bit-exato a exigir. Esta patente é compressão HOLOGRÁFICA (com perda
//  por natureza), e o que ela tem de único é o JUIZ: a integridade é o NOME.
// ═══════════════════════════════════════════════════════════════════════════════════
const NOME_COR: Record<string, string> = {
  TETELESTAI: '#30d158', PRESERVADO: '#5ac8fa', PERTURBADO: 'var(--gold, #ffd60a)', VIOLADO: '#ff453a',
}

function TensorDeviceTab({ pid }: { pid: string }) {
  const slug = FUNCTIONAL_DEVICES[pid]
  const [info, setInfo] = useState<any>(null)
  const [cRes, setCRes] = useState<any>(null)
  const [dRes, setDRes] = useState<any>(null)
  const [cBusy, setCBusy] = useState(false)
  const [dBusy, setDBusy] = useState(false)
  const [err, setErr] = useState('')

  useEffect(() => {
    fetch(`/api/device/${slug}/info`).then(r => r.json()).then(setInfo).catch(() => setInfo(null))
  }, [slug])

  async function post(path: string, file: File, headers: Record<string, string>) {
    const res = await fetch(`/api/device/${slug}/${path}`, {
      method: 'POST', headers: { 'Content-Type': 'application/octet-stream', ...headers }, body: file,
    })
    if (!res.ok) { let m = `${res.status}`; try { m = (await res.json()).detail || m } catch { /* */ } throw new Error(m) }
    const h = res.headers.get('X-Acom-Report')
    return { report: h ? JSON.parse(b64utf8(h)) : {}, blob: await res.blob() }
  }

  async function doCompress(file: File) {
    setErr(''); setCRes(null); setCBusy(true)
    try {
      const { report, blob } = await post('compress', file, { 'X-Filename': file.name })
      setCRes({ report, url: URL.createObjectURL(blob), name: (report.orig_name || file.name) + '.tglt' })
    } catch (e: any) { setErr('Falha ao comprimir: ' + e.message) }
    setCBusy(false)
  }
  async function doDecompress(file: File) {
    setErr(''); setDRes(null); setDBusy(true)
    try {
      const { report, blob } = await post('decompress', file, {})
      setDRes({ report, url: URL.createObjectURL(blob), name: report.restored_name || 'tensor.npy' })
    } catch (e: any) { setErr('Falha ao restaurar: ' + e.message) }
    setDBusy(false)
  }

  const v = cRes?.report?.nome_verificacao
  const cl = cRes?.report?.classico

  return (
    <div className="device fronteira">
      <div className="device-head">
        <div>
          <div className="device-title">TGL-Tensor <span className="device-badge">rodando ao vivo</span></div>
          <div className="device-sub">Compressão holográfica com <b>integridade por NOME</b> · patente {info?.patent_id || pid}</div>
        </div>
        {info && (
          <div className="device-beta">
            β = α·√e = <b>{info.beta.beta_tgl?.toFixed(9)}</b> · √β = <b>{info.beta.sqrt_beta_tgl?.toFixed(6)}</b>
            <div className="legal-note">os dois degraus da escada do Nome — nenhum digitado</div>
          </div>
        )}
      </div>

      {err && <div className="device-err">{err}</div>}

      <div className="device-foot" style={{ marginTop: 0, marginBottom: 14, borderTop: 'none', borderBottom: '1px solid var(--line)', paddingBottom: 12 }}>
        <b>O NOME é nativo (evolução v2.0 → v2.1).</b> O Nome de um tensor <b>emerge da projeção</b> —
        não é calculado à parte: é a projeção medindo a si mesma. A reconstrução é julgada por ele,
        numa escada cujos degraus são a própria teoria — o <b>Piso de Hilbert</b>:
        <div className="tgl-ladder">
          <span style={{ color: NOME_COR.TETELESTAI }}>δ &lt; β → <b>TETELESTAI</b> (identidade perfeita)</span>
          <span style={{ color: NOME_COR.PRESERVADO }}>δ &lt; √β → <b>PRESERVADO</b> (dentro do campo)</span>
          <span style={{ color: NOME_COR.PERTURBADO }}>δ &lt; 1 → <b>PERTURBADO</b> (na fronteira)</span>
          <span style={{ color: NOME_COR.VIOLADO }}>δ ≥ 1 → <b>VIOLADO</b> (fora do campo)</span>
        </div>
      </div>

      <div className="device-grid">
        <div className="device-col">
          <div className="device-col-title">Comprimir um tensor (<code>.npy</code>)</div>
          <DropZone label="Comprimir" accept=".npy" busy={cBusy}
            hint="arraste um array .npy — o modo (DIRECT/SPECTRAL) é escolhido pelo sinal, nada a configurar"
            onFile={doCompress} />
          {cRes && (
            <div className="device-result">
              <div className="dr-ratio"><b>{cRes.report.ratio?.toFixed(2)}×</b><span>compressão</span></div>
              <div className="dr-flow">
                <span>{fmtBytes(cRes.report.orig_size)}</span><span className="dr-arrow">→</span>
                <span className="dr-comp">{fmtBytes(cRes.report.compressed_size)}</span>
              </div>

              <div className="tgl-judges">
                <div className="tgl-judge">
                  <div className="tgl-judge-h">o juiz clássico</div>
                  <div className="tgl-judge-v">{cl?.psnr_db?.toFixed(1)} dB</div>
                  <div className="tgl-judge-s">PSNR · correlação {cl?.correlation?.toFixed(6)}</div>
                  <div className="tgl-judge-x">{cl?.veredito}</div>
                </div>
                <div className="tgl-judge tgl-judge-nome">
                  <div className="tgl-judge-h">o NOME (o juiz da casa)</div>
                  <div className="tgl-judge-v" style={{ color: NOME_COR[v?.state] || 'var(--text)' }}>{v?.state}</div>
                  <div className="tgl-judge-s">integridade {v?.integrity} · δ<sub>max</sub> {v?.delta_max?.toFixed(6)}</div>
                  <div className="tgl-judge-x">
                    {v?.delta_max != null && info && (v.delta_max < info.beta.beta_tgl
                      ? 'abaixo de β' : v.delta_max < info.beta.sqrt_beta_tgl
                        ? 'abaixo de √β' : `acima de √β (${(v.delta_max / info.beta.sqrt_beta_tgl).toFixed(2)}×)`)}
                  </div>
                </div>
              </div>

              {cRes.report.divergencia_dos_juizes && (
                <p className="dr-dec-why dr-dec-gate" style={{ borderLeft: '2px solid var(--gold)', paddingLeft: 8 }}>
                  <b>Os juízes discordam — e isso é o ponto.</b> {cRes.report.divergencia_dos_juizes}
                </p>
              )}

              <div className="dr-kv">
                <span>modo</span><b>{cRes.report.mode}</b>
                <span>escolhido por</span><b style={{ fontSize: 11 }}>AUTO — o sinal, não você</b>
                <span>backend</span><b>{cRes.report.entropy_backend}</b>
                <span>com perda</span><b style={{ color: 'var(--gold)' }}>sim (holográfica, medida)</b>
              </div>

              <details className="dr-dec-alt" style={{ marginTop: 8 }}>
                <summary>o NOME, campo a campo (original → reconstruído)</summary>
                <ul>
                  {['f_exp', 's_psi', 'sigma_norm'].map(k => (
                    <li key={k}><b>{k}</b>: {cRes.report.nome_original?.[k]?.toFixed?.(6)} → {cRes.report.nome_reconstruido?.[k]?.toFixed?.(6)}</li>
                  ))}
                  <li><b>psi_dist</b>: [{cRes.report.nome_original?.psi_dist?.map((x: number) => x.toFixed(3)).join(', ')}]
                    → [{cRes.report.nome_reconstruido?.psi_dist?.map((x: number) => x.toFixed(3)).join(', ')}]</li>
                </ul>
              </details>

              <a className="btn" href={cRes.url} download={cRes.name} style={{ textDecoration: 'none', display: 'inline-block', marginTop: 8 }}>
                ⬇ Baixar {cRes.name}
              </a>
              <p className="dr-note">{cRes.report.nota}</p>
            </div>
          )}
        </div>

        <div className="device-col">
          <div className="device-col-title">Restaurar (<code>.tglt</code> → <code>.npy</code>)</div>
          <DropZone label="Restaurar" accept=".tglt" busy={dBusy} hint="arraste um contêiner .tglt" onFile={doDecompress} />
          {dRes && (
            <div className="device-result">
              <div style={{ fontSize: 15, fontWeight: 700, color: NOME_COR[dRes.report.state] || 'var(--text)' }}>
                ⬥ {dRes.report.state}
              </div>
              <div className="dr-kv" style={{ marginTop: 8 }}>
                <span>arquivo</span><b>{dRes.report.restored_name}</b>
                <span>tamanho</span><b>{fmtBytes(dRes.report.restored_size)}</b>
                <span>integridade</span><b>{dRes.report.integrity}</b>
                <span>δ<sub>max</sub></span><b>{dRes.report.delta_max?.toFixed?.(8)}</b>
                <span>julgado por</span><b style={{ fontSize: 11 }}>{dRes.report.verified_by}</b>
              </div>
              <a className="btn" href={dRes.url} download={dRes.name} style={{ textDecoration: 'none', display: 'inline-block', marginTop: 10 }}>
                ⬇ Baixar tensor
              </a>
              <p className="dr-note">{dRes.report.nota}</p>
            </div>
          )}
        </div>
      </div>

      <div className="device-foot">
        <b>Honestidade (a régua).</b> Este dispositivo <b>não reimplementa</b> a invenção: ele carrega o
        protótipo do operador (<code>tgl_tensor_v2_1.py</code>, READ-ONLY) e o expõe — o que roda aqui é o
        algoritmo patenteado, não uma paráfrase. A compressão é <b>com perda por natureza</b> (é
        holográfica) e a perda é medida por <b>dois juízes</b>, que ficam os dois no relatório mesmo
        quando discordam: o clássico mede <b>erro de amplitude</b>; o Nome mede se a <b>estrutura</b>
        sobreviveu. Nenhum dos dois é dispensável — <i>medido nos dois sentidos</i>: um campo suave volta
        com PSNR ≈ 63 dB (“perfeito”) e o Nome o declara PERTURBADO; e um sinal constante faz a
        correlação clássica degenerar para 0,0 (variância zero ⇒ indefinida) enquanto o Nome acerta
        TETELESTAI. O <b>backend de entropia</b> (zstd) é biblioteca padrão da indústria; a camada TGL é a
        reflexão holográfica + o Nome. Simulação não valida física
        (<code>physical_verdict_allowed = false</code>).
      </div>
    </div>
  )
}

function DeviceTab({ pid, p }: { pid: string; p: PatentDetail }) {
  const slug = FUNCTIONAL_DEVICES[pid]
  const [info, setInfo] = useState<any>(null)
  const [cRes, setCRes] = useState<any>(null)     // resultado da compressão
  const [dRes, setDRes] = useState<any>(null)     // resultado da restauração
  const [cBusy, setCBusy] = useState(false)
  const [dBusy, setDBusy] = useState(false)
  const [err, setErr] = useState('')
  // Não há mais "modo": a PORTA É ÚNICA e o SINAL escolhe o codec (acom_auto).
  // O que resta é uma EXIGÊNCIA de integridade — não um interruptor de codec:
  // quando ligada, proíbe de forma dura a rota com perda (é o que o backup usa).
  const [exigirExato, setExigirExato] = useState(false)
  // ── empacotador (backup): muitos arquivos / pasta → um .acom ──
  const [pItems, setPItems] = useState<PackItem[]>([])
  const [pPass, setPPass] = useState('')
  const [pBusy, setPBusy] = useState(false)
  const [pRes, setPRes] = useState<any>(null)
  const [pOver, setPOver] = useState(false)
  const [uPass, setUPass] = useState('')
  const [uBusy, setUBusy] = useState(false)
  const [uRes, setURes] = useState<any>(null)     // { session, entries, files, encrypted, meta_chain }
  const [uSaved, setUSaved] = useState('')

  useEffect(() => {
    if (!slug) return
    setInfo(null); setCRes(null); setDRes(null); setErr('')
    fetch(`/api/device/${slug}/info`).then(r => r.json()).then(setInfo).catch(() => setInfo({ error: true }))
  }, [slug, pid])

  if (!slug) {
    return (
      <div className="panel">
        <h4>Dispositivo — {p.display_name}</h4>
        <p className="muted" style={{ fontSize: 13, lineHeight: 1.6 }}>
          Este dispositivo depende de <b>substância física</b> para operar de fato. A meta é uma
          <b> simulação visual do dispositivo em funcionamento</b> aqui (não o funcionamento real).
          O modelo 3D interativo já vive na aba <b>Render 2D/3D → (c)</b>. A interface funcional
          começou pelo <b>ACOM</b> (compressor de software, que roda de verdade); os demais chegam a seguir.
        </p>
        <p className="legal-note">Simulação nunca valida física (physical_verdict_allowed = false).</p>
      </div>
    )
  }

  async function post(path: string, file: File, headers: Record<string, string>) {
    const res = await fetch(`/api/device/${slug}/${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/octet-stream', ...headers },
      body: file,
    })
    if (!res.ok) {
      let msg = `${res.status}`
      try { msg = (await res.json()).detail || msg } catch { /* */ }
      throw new Error(msg)
    }
    const repHdr = res.headers.get('X-Acom-Report')
    const report = repHdr ? JSON.parse(b64utf8(repHdr)) : {}
    const blob = await res.blob()
    return { report, blob }
  }

  async function doCompress(file: File, fidelity: 'auto' | 'exata') {
    setErr(''); setCRes(null); setCBusy(true)
    try {
      if (info?.max_input_mb && file.size > info.max_input_mb * 1048576)
        throw new Error(`arquivo acima do limite de ${info.max_input_mb} MB`)
      const { report, blob } = await post('compress', file, { 'X-Filename': file.name, 'X-Fidelity': fidelity })
      setCRes({ report, url: URL.createObjectURL(blob), name: (report.orig_name || file.name) + '.acom' })
    } catch (e: any) { setErr('Falha ao comprimir: ' + e.message) }
    setCBusy(false)
  }

  async function doDecompress(file: File) {
    setErr(''); setDRes(null); setDBusy(true)
    try {
      const { report, blob } = await post('decompress', file, {})
      setDRes({ report, url: URL.createObjectURL(blob), name: report.restored_name || 'restaurado' })
    } catch (e: any) { setErr('Falha ao restaurar: ' + e.message) }
    setDBusy(false)
  }

  // ── EMPACOTADOR: muitos arquivos/pasta → um .acom ──
  const pTotal = pItems.reduce((s, i) => s + i.file.size, 0)
  async function addItems(items: PackItem[]) {
    if (!items.length) return
    setPRes(null); setErr('')
    setPItems(prev => {
      const seen = new Set(prev.map(i => i.path))
      return [...prev, ...items.filter(i => !seen.has(i.path))]
    })
  }
  async function doPack() {
    if (!pItems.length) return
    if (pPass && pPass.length < 8) { setErr('O código de inscrição precisa de ao menos 8 caracteres.'); return }
    setErr(''); setPRes(null); setPBusy(true)
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/octet-stream' }
      if (pPass) headers['X-Inscricao'] = pPass
      const res = await fetch(`/api/device/${slug}/pack`, { method: 'POST', headers, body: buildEnvelope(pItems) })
      if (!res.ok) { let m = `${res.status}`; try { m = (await res.json()).detail || m } catch { /* */ } throw new Error(m) }
      const rep = JSON.parse(b64utf8(res.headers.get('X-Acom-Report') || '')); const blob = await res.blob()
      setPRes({ report: rep, url: URL.createObjectURL(blob), name: 'backup.acom' })
    } catch (e: any) { setErr('Falha ao empacotar: ' + e.message) }
    setPBusy(false)
  }
  async function doUnpackArchive(file: File) {
    setErr(''); setURes(null); setUSaved(''); setUBusy(true)
    try {
      const headers: Record<string, string> = { 'Content-Type': 'application/octet-stream' }
      if (uPass) headers['X-Inscricao'] = uPass
      const res = await fetch(`/api/device/${slug}/unpack`, { method: 'POST', headers, body: file })
      if (!res.ok) { let m = `${res.status}`; try { m = (await res.json()).detail || m } catch { /* */ } throw new Error(m) }
      setURes(await res.json())
    } catch (e: any) { setErr('Falha ao abrir o backup: ' + e.message) }
    setUBusy(false)
  }
  async function saveTree() {
    if (!uRes?.session) return
    const w = window as any
    if (!w.showDirectoryPicker) { setErr('Seu navegador não permite gravar pasta — use o CLI (tools/acom_pack.py) para restaurar.'); return }
    setUBusy(true); setErr('')
    try {
      const dir = await w.showDirectoryPicker({ mode: 'readwrite' })
      let n = 0
      for (const e of uRes.entries) {
        const r = await fetch(`/api/device/${slug}/unpack-file?session=${uRes.session}&path=${encodeURIComponent(e.path)}`)
        if (!r.ok) throw new Error(`${e.path}: ${r.status}`)
        const buf = await r.arrayBuffer()
        const parts = e.path.split('/'); const fname = parts.pop() as string
        let cur = dir
        for (const part of parts) cur = await cur.getDirectoryHandle(part, { create: true })
        const fh = await cur.getFileHandle(fname, { create: true })
        const ws = await fh.createWritable(); await ws.write(buf); await ws.close(); n++
      }
      setUSaved(`${n} arquivos gravados em ${dir.name}/ — cada SHA-256 verificado.`)
    } catch (e: any) { if (e?.name !== 'AbortError') setErr('Falha ao gravar: ' + (e.message || e)) }
    setUBusy(false)
  }

  const beta = info?.beta
  return (
    <div className="panel">
      <div className="device-head">
        <div>
          <h4 style={{ margin: 0 }}>⚙ {info?.name || 'ACOM'} — {info?.title || 'Compressor Ontológico'}</h4>
          <p className="muted" style={{ fontSize: 12.5, margin: '4px 0 0' }}>
            O dispositivo <b>funcionando</b>: jogue um arquivo, ele comprime e devolve — e restaura
            bit a bit. <b>Sem perdas</b>, integridade garantida por SHA-256.
          </p>
        </div>
        {beta && (
          <div className="device-beta" title="β calculado em runtime — nunca literal">
            β = α·√e = <b>{beta.beta_tgl.toFixed(9)}</b><br />
            <span className="muted">θ_Miguel = {beta.theta_miguel_deg.toFixed(4)}°</span>
          </div>
        )}
      </div>

      {err && <div className="device-err">{err}</div>}

      {/* ═══════ BACKUP — muitos arquivos / pasta inteira → um .acom ═══════ */}
      <div style={{ marginBottom: 18, padding: '14px', border: '1px solid var(--gold)', borderRadius: 12, background: 'color-mix(in srgb, var(--gold) 6%, transparent)' }}>
        <div className="device-col-title" style={{ marginBottom: 2 }}>
          🗄 Backup — muitos arquivos ou uma <b>pasta inteira</b> → um único <b>.acom</b>
        </div>
        <p className="muted" style={{ fontSize: 12, margin: '2px 0 12px' }}>
          A máquina trabalhando: empacote vários arquivos/pastas num só contêiner, com a <b>sua criptografia</b>
          (opcional), e restaure bit a bit. Para backups <b>grandes (GBs)</b> use o CLI <code>tools/acom_pack.py</code> (streaming do disco).
        </p>
        <div className="device-grid">
          {/* EMPACOTAR */}
          <div className="device-col">
            <div className={`dropzone ${pOver ? 'over' : ''} ${pBusy ? 'busy' : ''}`}
              onDragOver={e => { e.preventDefault(); setPOver(true) }}
              onDragLeave={() => setPOver(false)}
              onDrop={async e => { e.preventDefault(); setPOver(false); addItems(await itemsFromDrop(e.dataTransfer)) }}>
              <div className="dz-icon">{pBusy ? '⏳' : '🗂'}</div>
              <div className="dz-label">Arraste arquivos ou pastas</div>
              <div className="dz-hint">ou escolha abaixo — vira um só .acom</div>
            </div>
            <div style={{ display: 'flex', gap: 8, marginTop: 8, flexWrap: 'wrap' }}>
              <button className="btn btn-ghost" type="button" onClick={() => document.getElementById('pk-files')?.click()}>+ Arquivos</button>
              <button className="btn btn-ghost" type="button" onClick={() => document.getElementById('pk-dir')?.click()}>+ Pasta</button>
              {pItems.length > 0 && <button className="btn btn-ghost" type="button" onClick={() => { setPItems([]); setPRes(null) }}>limpar</button>}
            </div>
            <input id="pk-files" type="file" multiple style={{ display: 'none' }}
              onChange={e => { addItems(itemsFromInput(e.target.files)); e.currentTarget.value = '' }} />
            <input id="pk-dir" type="file" style={{ display: 'none' }} ref={r => { if (r) (r as any).webkitdirectory = true }}
              onChange={e => { addItems(itemsFromInput(e.target.files)); e.currentTarget.value = '' }} />
            {pItems.length > 0 && (
              <div className="device-result" style={{ marginTop: 8 }}>
                <div><b>{pItems.length}</b> arquivo(s) · {fmtBytes(pTotal)} selecionado(s)</div>
                <input type="password" placeholder="código de inscrição — vazio = plano; ≥8 = cifrado" value={pPass}
                  onChange={e => setPPass(e.target.value)}
                  style={{ width: '100%', boxSizing: 'border-box', padding: '8px 10px', borderRadius: 8, border: '1px solid var(--border)', background: 'var(--bg-soft)', color: 'var(--text)', fontSize: 13, marginTop: 8 }} />
                <button className="btn btn-gold" type="button" disabled={pBusy} onClick={doPack} style={{ marginTop: 8, width: '100%' }}>
                  {pBusy ? 'empacotando…' : `⬛ Empacotar ${pItems.length} → .acom${pPass ? ' (cifrado)' : ''}`}
                </button>
              </div>
            )}
            {pRes && (
              <div className="device-result">
                <div className="dr-ratio">
                  <b>{pRes.report.total_input_bytes ? (pRes.report.total_input_bytes / pRes.report.container_bytes).toFixed(2) : '—'}×</b><span>compressão</span>
                </div>
                <div className="dr-flow">
                  <span>{pRes.report.files} arquivos · {fmtBytes(pRes.report.total_input_bytes || 0)}</span>
                  <span className="dr-arrow">→</span>
                  <span className="dr-comp">{fmtBytes(pRes.report.container_bytes)}</span>
                </div>
                <div className="dr-kv">
                  <span>cifrado</span><b>{pRes.report.encrypted ? '✓ sua chave' : 'não'}</b>
                  <span>meta-cadeia</span><b style={{ fontFamily: 'monospace', fontSize: 11 }}>{pRes.report.meta_chain?.slice(0, 16)}…</b>
                </div>
                <a className="btn btn-gold" href={pRes.url} download={pRes.name} style={{ textDecoration: 'none', display: 'inline-block', marginTop: 8 }}>⬇ Baixar backup.acom</a>
              </div>
            )}
          </div>
          {/* RESTAURAR BACKUP */}
          <div className="device-col">
            <div className={`dropzone ${uBusy ? 'busy' : ''}`}
              onDragOver={e => e.preventDefault()}
              onDrop={e => { e.preventDefault(); if (e.dataTransfer.files[0]) doUnpackArchive(e.dataTransfer.files[0]) }}
              onClick={() => !uBusy && document.getElementById('uk-file')?.click()}>
              <input id="uk-file" type="file" accept=".acom" style={{ display: 'none' }}
                onChange={e => { if (e.target.files?.[0]) doUnpackArchive(e.target.files[0]); e.currentTarget.value = '' }} />
              <div className="dz-icon">{uBusy ? '⏳' : '📦'}</div>
              <div className="dz-label">Abrir um backup .acom</div>
              <div className="dz-hint">arraste o .acom ou clique</div>
            </div>
            <input type="password" placeholder="código de inscrição (se cifrado)" value={uPass}
              onChange={e => setUPass(e.target.value)}
              style={{ width: '100%', boxSizing: 'border-box', padding: '8px 10px', borderRadius: 8, border: '1px solid var(--border)', background: 'var(--bg-soft)', color: 'var(--text)', fontSize: 13, marginTop: 8 }} />
            {uRes && (
              <div className="device-result">
                <div className="integrity-ok" style={{ fontSize: 15, fontWeight: 700 }}>✓ {uRes.files} arquivos · {fmtBytes(uRes.total_bytes)}</div>
                <div className="dr-kv" style={{ marginTop: 8 }}>
                  <span>cifrado</span><b>{uRes.encrypted ? 'sim' : 'não'}</b>
                  <span>meta-cadeia</span><b style={{ fontFamily: 'monospace', fontSize: 11 }}>{uRes.meta_chain?.slice(0, 16)}…</b>
                </div>
                <button className="btn btn-gold" type="button" disabled={uBusy} onClick={saveTree} style={{ marginTop: 8, width: '100%' }}>💾 Salvar na pasta…</button>
                {uSaved && <p className="dr-note integrity-ok">{uSaved}</p>}
                <div style={{ maxHeight: 120, overflow: 'auto', marginTop: 8, fontSize: 11, fontFamily: 'monospace', color: 'var(--text-soft)' }}>
                  {uRes.entries?.slice(0, 200).map((e: any, i: number) => <div key={i}>{e.path} · {fmtBytes(e.size || 0)}</div>)}
                  {uRes.files > 200 && <div>… (+{uRes.files - 200})</div>}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="device-col-title" style={{ marginBottom: 8, opacity: .8 }}>
        Um arquivo por vez — <b>porta única</b>: o sinal escolhe o codec
      </div>
      <div className="device-grid">
        {/* COMPRIMIR */}
        <div className="device-col">
          <div className="device-col-title">Comprimir</div>
          <DropZone label="Comprimir" busy={cBusy}
            hint="arraste um arquivo aqui ou clique — qualquer tipo, até 64 MB. Nada a configurar."
            onFile={f => doCompress(f, exigirExato ? 'exata' : 'auto')} />
          {info?.auto?.available && (
            <label className="device-toggle" title="Proíbe de forma dura a rota com perda (g=√|L|), mesmo que ela seja fiel e mais eficiente. É o que o backup usa.">
              <input type="checkbox" checked={exigirExato} onChange={e => setExigirExato(e.target.checked)} />
              <span>exigir <b>bit-exato</b> — proíbe a rota com perda ainda que ela passe o portão de fidelidade</span>
            </label>
          )}
          {cRes && (
            <div className="device-result">
              <div className="dr-ratio"><b>{cRes.report.ratio?.toFixed(2)}×</b><span>compressão</span></div>
              <div className="dr-flow">
                <span>{fmtBytes(cRes.report.orig_size)}</span>
                <span className="dr-arrow">→</span>
                <span className="dr-comp">{fmtBytes(cRes.report.compressed_size)}</span>
              </div>
              {cRes.report.signal_type && (
                <div className="dr-decision">
                  <div className="dr-dec-head">
                    <span className="dr-chip">{cRes.report.signal_type}</span>
                    <span className="dr-dec-arrow">→</span>
                    <span className={'dr-chip ' + (cRes.report.lossless ? 'dr-chip-ok' : 'dr-chip-lossy')}>
                      {cRes.report.route}
                    </span>
                    <span className="dr-dec-tag">decidido pelo sinal</span>
                  </div>
                  {cRes.report.signal_evidence && <p className="dr-dec-why">Leitura: {cRes.report.signal_evidence}</p>}
                  <p className="dr-dec-why">{cRes.report.decision_why}</p>
                  {cRes.report.decided_by && <p className="dr-dec-why dr-dec-gate">{cRes.report.decided_by}</p>}
                  {cRes.report.seal_probe && (
                    <p className="dr-dec-why">
                      <b>Sondagem do selo:</b> a amostra de {(cRes.report.seal_probe.sample_bytes / 1024).toFixed(0)} KiB
                      manteve <b>{(cRes.report.seal_probe.kept_fraction * 100).toFixed(1)}%</b> —{' '}
                      {cRes.report.seal_probe.seal_holds
                        ? <>o selo <b className="integrity-ok">se sustenta</b> (a redundância já tinha sido extraída).</>
                        : <><b style={{ color: 'var(--gold)' }}>o selo foi REJEITADO</b> (o magic mentiu sobre o conteúdo) — rota promovida ao conjunto completo.</>}
                      {' '}A etiqueta propõe; a medição dispõe.
                    </p>
                  )}
                  {cRes.report.alternatives?.length > 1 && (
                    <details className="dr-dec-alt">
                      <summary>rotas medidas e descartadas ({cRes.report.alternatives.length})</summary>
                      <ul>
                        {cRes.report.alternatives.map((a: any, i: number) => (
                          <li key={i}>
                            <b>{a.route}</b>{a.backend ? ` (${a.backend})` : ''} — {a.error ? a.error :
                              <>{fmtBytes(a.size)}, {a.ratio?.toFixed(2)}×{a.lossless === false && a.psnr_db != null
                                ? `, PSNR ${a.psnr_db} dB, ganho ${a.gain_vs_lossless?.toFixed(2)}× — portão ${a.gate_passed ? 'APROVOU' : 'REPROVOU'}` : ''}</>}
                          </li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              )}
              <div className="dr-kv">
                <span>economia</span><b>{cRes.report.saved_pct?.toFixed(1)}%</b>
                {cRes.report.mode === 'tensor' ? (
                  <>
                    <span>PSNR</span><b>{cRes.report.psnr_db ? cRes.report.psnr_db.toFixed(1) + ' dB' : '∞'}</b>
                    <span>correlação</span><b>{cRes.report.correlation?.toFixed(5)}</b>
                    <span>transformada</span><b>g=√|L|</b>
                    <span>com perda</span><b style={{ color: 'var(--gold)' }}>sim (controlada, medida)</b>
                  </>
                ) : (
                  <>
                    <span>regime</span><b>{cRes.report.regime}</b>
                    <span>backend</span><b>{cRes.report.backend?.toUpperCase()}</b>
                    <span>camada ACOM</span><b>{cRes.report.ontological_stage}</b>
                    <span>sem perdas</span><b className="integrity-ok">{cRes.report.lossless ? '✓ sim' : 'não'}</b>
                  </>
                )}
              </div>
              <div className="dr-sha">SHA-256 origem: {cRes.report.orig_sha256?.slice(0, 24)}…</div>
              <a className="btn" href={cRes.url} download={cRes.name} style={{ textDecoration: 'none', display: 'inline-block', marginTop: 6 }}>
                ⬇ Baixar {cRes.name}
              </a>
              <p className="dr-note">{cRes.report.note}</p>
            </div>
          )}
        </div>

        {/* RESTAURAR */}
        <div className="device-col">
          <div className="device-col-title">Restaurar (.acom → original)</div>
          <DropZone label="Restaurar" accept=".acom" busy={dBusy}
            hint="arraste um arquivo .acom aqui ou clique"
            onFile={doDecompress} />
          {dRes && (
            <div className="device-result">
              <div className="integrity-ok" style={{ fontSize: 15, fontWeight: 700 }}>✓ integridade verificada</div>
              <div className="dr-kv" style={{ marginTop: 8 }}>
                <span>arquivo</span><b>{dRes.report.restored_name}</b>
                <span>tamanho</span><b>{fmtBytes(dRes.report.restored_size)}</b>
                <span>regime</span><b>{dRes.report.regime}</b>
                <span>SHA-256</span><b style={{ fontFamily: 'monospace', fontSize: 11 }}>{dRes.report.orig_sha256?.slice(0, 20)}…</b>
              </div>
              <a className="btn" href={dRes.url} download={dRes.name} style={{ textDecoration: 'none', display: 'inline-block', marginTop: 10 }}>
                ⬇ Baixar original
              </a>
            </div>
          )}
        </div>
      </div>

      <div className="device-foot">
        <b>Honestidade (a régua).</b> A redução de bytes de arquivos arbitrários é feita por um
        backend de entropia real (<b>LZMA</b>, biblioteca padrão). A camada ACOM contribui com a
        classificação de <b>regime ontológico</b> (limiares TGL: β, e/2, 3e/2 sobre a entropia de
        Shannon), um estágio reversível de paleta para dados de baixa entropia, e a proveniência
        β = α·√e. O <b>algoritmo nativo e patenteado</b> (g=√|L|, com perda controlada, PSNR/correlação
        medidos — reivindicação 18) é a rota <code>graviton_reflect</code>{info && info.tensor_available
          ? <> — <b className="integrity-ok">rodando ao vivo</b></>
          : <> — indisponível neste backend (requer numpy; roda pelo runner da patente)</>}.
        {info?.auto?.available && <>
          {' '}<b>Não há modo a escolher:</b> a leitura tipa o sinal e a lei o roteia
          (<code>acom_auto</code> v{info.auto.version}) — é a cadeia de sinal da TGL
          (<i>o codificador é escolhido pela leitura, não pelo usuário</i>). Os limiares do
          <b> portão de fidelidade</b> (PSNR ≥ {info.auto.fidelity_gate.psnr_db} dB,
          correlação ≥ {info.auto.fidelity_gate.correlation}, ganho ≥ {info.auto.fidelity_gate.min_gain}×)
          são <b>[ENGENHARIA]</b>: escolhas de projeto declaradas, <b>não</b> derivadas de β — quem
          não desce da teoria fica marcado como o que é.
        </>}
      </div>
    </div>
  )
}

function CodeTab({ pid }: { pid: string }) {
  const [data, setData] = useState<any>(null)
  const [sel, setSel] = useState<string | null>(null)
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  useEffect(() => { setSel(null); setContent(''); setData(null); api.code(pid).then(setData).catch(() => setData({ available: false })) }, [pid])
  useEffect(() => {
    if (!sel) return
    setLoading(true)
    api.codeFile(pid, sel).then(c => { setContent(c); setLoading(false) }).catch(() => { setContent('(erro ao carregar)'); setLoading(false) })
  }, [pid, sel])
  if (!data) return <div className="panel"><p className="muted">carregando código…</p></div>
  if (!data.available) return <div className="panel"><p className="muted">Sem código nesta pasta ainda. Rode <code>tools/build_final_code.py</code>.</p></div>

  const files: any[] = data.files || []
  const groups = ROLE_ORDER.map(r => ({ role: r, items: files.filter(f => f.role === r) })).filter(g => g.items.length)
  const final = data.final
  const man = data.manifest
  const kb = (b: number) => `${(b / 1024).toFixed(1)} KB`

  return (
    <div className="panel">
      <p className="muted" style={{ fontSize: 12.5, marginTop: 0 }}>
        A <b>codificação</b> da patente também é documento dela. Aqui vive todo o código construído — e, no topo,
        o <b>código-fonte FINALIZADO</b>: um único arquivo auto-contido que roda standalone e demonstra a patente
        por completo, com hash de integridade. <i>forma = conteúdo.</i>
      </p>
      {final && (
        <div style={{ background: '#0e1a12', border: '1px solid #1f7a3f', borderRadius: 8, padding: '12px 14px', marginBottom: 14 }}>
          <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
            <span style={{ fontSize: 14, fontWeight: 700, color: '#30d158' }}>▣ {final.path}</span>
            <span style={{ fontSize: 11.5, color: '#8a94a6' }}>{kb(final.bytes)} · {man?.n_files ?? '?'} fontes integradas</span>
          </div>
          {man && (
            <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 5, fontFamily: 'monospace', wordBreak: 'break-all' }}>
              SHA-256 combinado: <span style={{ color: '#7ee0c0' }}>{man.combined_sha256}</span>
            </div>
          )}
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn xs" onClick={() => setSel(final.path)}>ver código final</button>
            <a className="btn ghost xs" href={pub(`/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(final.path)}`)}
              download style={{ textDecoration: 'none' }}>baixar</a>
          </div>
          <div style={{ fontSize: 11, color: '#6b7280', marginTop: 6 }}>
            Importável como módulo — entra no <b>compilador SkyGrid</b> (o dispositivo que agrega todas as demais).
          </div>
        </div>
      )}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(240px, 0.9fr) minmax(0, 2fr)', gap: 14, alignItems: 'start' }}>
        <div style={{ maxHeight: '62vh', overflow: 'auto' }}>
          {groups.map(g => (
            <div key={g.role} style={{ marginBottom: 10 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: '#8a94a6', textTransform: 'uppercase', letterSpacing: 0.4, marginBottom: 4 }}>
                {ROLE_LABEL[g.role]} <span style={{ color: '#4b5563' }}>({g.items.length})</span>
              </div>
              {g.items.map(f => (
                <div key={f.path} onClick={() => setSel(f.path)}
                  style={{ fontSize: 12, padding: '3px 8px', borderRadius: 5, cursor: 'pointer', fontFamily: 'monospace',
                    color: sel === f.path ? '#0b0f16' : '#c8d0da', background: sel === f.path ? '#7ee0c0' : 'transparent',
                    whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}
                  title={f.proof ? `${f.path} — ⭐ classe PROVA (citado na Cadeia de Prova)` : f.path}>
                  {f.proof && <span style={{ marginRight: 3 }}>⭐</span>}{f.path.replace(/^runner\//, '').replace(/^prototype_src\//, '')} <span style={{ color: sel === f.path ? '#0b0f16' : '#6b7280' }}>· {kb(f.bytes)}</span>
                </div>
              ))}
            </div>
          ))}
          <div style={{ fontSize: 11, color: '#8a94a6', marginTop: 6 }}>⭐ = classe PROVA (arquivo citado na Cadeia de Prova das reivindicações)</div>
        </div>
        <div>
          {sel ? (
            <>
              <div style={{ fontSize: 12, color: '#7ee0c0', fontFamily: 'monospace', marginBottom: 6 }}>{sel}</div>
              <pre className="md" style={{ maxHeight: '58vh', overflow: 'auto', fontSize: 11.5, lineHeight: 1.5 }}>
                {loading ? 'carregando…' : content}
              </pre>
            </>
          ) : <p className="muted" style={{ fontSize: 12.5 }}>Selecione um arquivo à esquerda, ou abra o <b>código final</b> acima.</p>}
        </div>
      </div>
    </div>
  )
}

function RenderTab({ p }: { p: PatentDetail }) {
  const [sel, setSel] = useState(0)
  const [layer, setLayer] = useState<'a' | 'b' | 'c'>(p.renders.length ? 'a' : 'b')
  const cur = p.renders[sel]
  return (
    <div className="panel">
      <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
        <button className={`btn ${layer === 'a' ? '' : 'ghost'}`} style={{ fontSize: 12 }}
          onClick={() => setLayer('a')} disabled={p.renders.length === 0}>
          (a) Desenho oficial · deep-zoom
        </button>
        <button className={`btn ${layer === 'b' ? '' : 'ghost'}`} style={{ fontSize: 12 }}
          onClick={() => setLayer('b')}>
          (b) Componentes clicáveis
        </button>
        <button className={`btn ${layer === 'c' ? '' : 'ghost'}`} style={{ fontSize: 12 }}
          onClick={() => setLayer('c')}>
          (c) Modelo 3D interativo
        </button>
      </div>

      {layer === 'a' && (p.renders.length === 0
        ? <p className="legal-note">Sem desenhos rasterizados para esta patente ainda (o ACOM raiz não tem PDF de desenhos separado). Veja a camada (b).</p>
        : <>
          <p className="muted" style={{ fontSize: 12.5, marginTop: 0 }}>
            Camada (a): desenho oficial do depósito INPI, ampliável (deep-zoom). {p.renders.length} prancha(s).
            <span className="legal-note"> Ilustração de engenharia — não é prova física.</span>
          </p>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
            {p.renders.map((r, i) => (
              <img key={r.id} src={pub(`/api/renders/${r.id}`)} alt={r.title}
                onClick={() => setSel(i)}
                style={{
                  width: 84, height: 108, objectFit: 'cover', cursor: 'pointer', background: '#fff',
                  borderRadius: 6, border: i === sel ? '2px solid var(--accent)' : '1px solid var(--line)',
                }} />
            ))}
          </div>
          <div style={{ fontSize: 13, marginBottom: 6 }}><b>{cur.title}</b> <span className="muted">· {cur.marker}</span></div>
          <DeepZoom url={pub(`/api/renders/${cur.id}`)} height={560} />
        </>)}

      {layer === 'b' && <ComponentMap pid={p.id} />}

      {layer === 'c' && <Render3D pid={p.id} />}
    </div>
  )
}

// ---- Evolução: linha do tempo vertical dos seals/results (read-only) ----
function fmtSealTs(ts: string): string {
  // "2026-07-29T10-15-14" -> "29/07/2026 10:15:14"
  const m = ts.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2})$/)
  if (!m) return ts
  return `${m[3]}/${m[2]}/${m[1]} ${m[4]}:${m[5]}:${m[6]}`
}

function EvolucaoTab({ pid }: { pid: string }) {
  const [doc, setDoc] = useState<EvolucaoDoc | null>(null)
  const [err, setErr] = useState(false)
  useEffect(() => {
    setDoc(null); setErr(false)
    api.evolucao(pid).then(setDoc).catch(() => setErr(true))
  }, [pid])
  if (err) return <div className="panel"><p className="muted">Falha ao carregar a evolução.</p></div>
  if (!doc) return <div className="panel"><p className="muted">carregando evolução…</p></div>
  if (!doc.available || doc.entries.length === 0)
    return <div className="panel"><p className="muted">Nenhuma rodada selada ainda. Cada execução do runner gera seal.json + results.json e entra aqui.</p></div>

  const entries = doc.entries // mais recente primeiro (o backend já inverte)
  return (
    <div className="panel">
      <h4 style={{ marginTop: 0 }}>Evolução do dispositivo — {doc.total} rodada(s) selada(s)</h4>
      <p className="muted" style={{ fontSize: 12.5 }}>
        Linha do tempo das rodadas do runner (seals/ + results/, <b>somente leitura</b> — os artefatos
        selados não mudam). As seções <b>amplificação/deepening</b> marcam as ondas de evolução
        (v138, v144, …); <span style={{ color: 'var(--gold)' }}>novo</span> = seção que não existia na rodada anterior.
      </p>
      <div style={{ marginTop: 14 }}>
        {entries.map((e, i) => {
          const older = entries[i + 1]
          const prevSecs = new Set(older ? older.sections : [])
          const allGreen = e.tests_passed != null && e.tests_total != null && e.tests_passed >= e.tests_total
          const isLatest = i === 0
          return (
            <div key={e.timestamp} style={{ display: 'flex', gap: 12 }}>
              {/* trilho vertical: ponto + linha */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 16 }}>
                <div style={{
                  width: isLatest ? 12 : 9, height: isLatest ? 12 : 9, borderRadius: '50%', marginTop: 4,
                  background: allGreen ? '#30d158' : (e.tests_passed != null ? 'var(--gold)' : 'var(--muted)'),
                  boxShadow: isLatest ? '0 0 6px #30d158' : 'none', flexShrink: 0,
                }} />
                {i < entries.length - 1 && <div style={{ width: 2, flex: 1, background: 'var(--line)', minHeight: 18 }} />}
              </div>
              {/* corpo do evento */}
              <div style={{ paddingBottom: 16, minWidth: 0, flex: 1 }}>
                <div style={{ display: 'flex', gap: 10, alignItems: 'baseline', flexWrap: 'wrap' }}>
                  <b style={{ fontSize: 13 }}>{fmtSealTs(e.timestamp)}</b>
                  {isLatest && <span style={{ fontSize: 10.5, color: '#30d158', border: '1px solid #1f7a3f', borderRadius: 10, padding: '1px 7px' }}>mais recente</span>}
                  {e.tests_passed != null && (
                    <span style={{ fontSize: 12, color: allGreen ? '#30d158' : 'var(--gold)' }}>
                      {e.tests_passed}{e.tests_total != null ? `/${e.tests_total}` : ''} testes verdes
                    </span>
                  )}
                  {e.result_hash_short && (
                    <span className="muted" style={{ fontFamily: 'monospace', fontSize: 11 }} title="result_hash (SHA-256, primeiros 16 hex)">
                      {e.result_hash_short}…
                    </span>
                  )}
                </div>
                {e.verdict && <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>{e.verdict}</div>}
                {e.sections.length > 0 && (
                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 6 }}>
                    {e.sections.map(s => {
                      const novo = !prevSecs.has(s)
                      return (
                        <span key={s} title={novo ? 'seção nova nesta rodada (onda de evolução)' : 'seção já presente na rodada anterior'}
                          style={{
                            fontSize: 11, fontFamily: 'monospace', borderRadius: 9, padding: '1px 8px',
                            border: novo ? '1px solid var(--gold)' : '1px solid var(--line)',
                            color: novo ? 'var(--gold)' : 'var(--muted)',
                          }}>
                          {novo ? '+ ' : ''}{s}
                        </span>
                      )
                    })}
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
      <p className="legal-note" style={{ marginTop: 4 }}>
        Simulação nunca valida física (physical_verdict_allowed = false). O selo completo de cada
        rodada está na aba Selo/Hash; os números vêm de seal.json/results.json, nunca refabricados.
      </p>
    </div>
  )
}

function NotesTab({ p, onChange, kindsFilter }: { p: PatentDetail; onChange: () => void; kindsFilter: string[] }) {
  const [tipo, setTipo] = useState(kindsFilter[0])
  const [text, setText] = useState('')
  const notes = p.notes.filter(n => kindsFilter.includes(n.tipo) && !n.text.toLowerCase().startsWith('exemplo:'))
  const examples = p.notes.filter(n => kindsFilter.includes(n.tipo) && n.text.toLowerCase().startsWith('exemplo:'))

  return (
    <div className="panel">
      {canEdit() ? (
        <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
          <select className="txt" value={tipo} onChange={e => setTipo(e.target.value)}>
            {kindsFilter.map(k => <option key={k} value={k}>{k}</option>)}
          </select>
          <input className="txt" style={{ flex: 1 }} placeholder="nova nota / instrução…" value={text}
            onChange={e => setText(e.target.value)} />
          <button className="btn" disabled={!text.trim()}
            onClick={async () => { await api.addNote(p.id, tipo, text); setText(''); onChange() }}>Adicionar</button>
        </div>
      ) : (
        <p className="muted" style={{ fontSize: 12, marginBottom: 14 }}>
          🔒 Seu acesso é somente leitura — você vê as notas, mas não pode adicionar/alterar.
        </p>
      )}
      {notes.length === 0 && <p className="muted">Nenhuma {kindsFilter.join('/')} ainda. Adicione acima; itens <b>ativos</b> entram no Prompt Compiler.</p>}
      {notes.map(n => (
        <div className="note" key={n.id}>
          <input type="checkbox" checked={!!n.active}
            onChange={async e => { await api.toggleNote(n.id, e.target.checked); onChange() }} />
          <div className="txt">
            <div>{n.text}</div>
            <div className="sec">[{n.tipo}] · {n.active ? 'ativa (entra no compilador)' : 'inativa'} {n.markers.length ? '· ' + n.markers.join(' ') : ''}</div>
          </div>
        </div>
      ))}
      {examples.length > 0 && (
        <details style={{ marginTop: 12 }}>
          <summary className="muted" style={{ cursor: 'pointer', fontSize: 12 }}>{examples.length} placeholder(s) de exemplo (nunca entram no compilador)</summary>
          {examples.map(n => <div key={n.id} className="muted" style={{ fontSize: 12, padding: '4px 0' }}>· {n.text}</div>)}
        </details>
      )}
    </div>
  )
}

// MODO PÚBLICO DE VISUALIZAÇÃO — o vínculo patentário de cada dispositivo: onde está o pedido e sob qual número
function VinculoPatentario({ v }: { v: any }) {
  if (!v) return null
  const linha = (k: string, val: any) => val ? <><div className="k">{k}</div><div>{val}</div></> : null
  return (
    <div className="panel" style={{ border: '1px solid #c5961a66', background: '#151206', marginBottom: 12 }}>
      <div style={{ fontWeight: 800, color: '#ffd60a', marginBottom: 6 }}>Vínculo patentário</div>
      <p style={{ fontSize: 13, margin: '0 0 8px' }}>Este dispositivo é objeto de <b>pedido de patente depositado</b> (não é patente concedida).</p>
      <div className="kv">
        {linha('Pedido no INPI (Brasil)', <b style={{ fontFamily: 'monospace' }}>{v.pedido_inpi}</b>)}
        {linha('Escritório', v.escritorio)}
        {linha('Depósito', v.deposito)}
        {linha('Prioridade', v.prioridade)}
        {linha('PCT (OMPI)', v.pct ? <span style={{ fontFamily: 'monospace' }}>{v.pct}{v.pct_data ? ` · ${v.pct_data}` : ''}</span> : null)}
        {(v.processos_adicionais || []).map((a: any) => (
          <React.Fragment key={a.processo}>{linha('Processo adicional', <span><span style={{ fontFamily: 'monospace' }}>{a.processo}</span> — {a.papel}{a.deposito ? ` · ${a.deposito}` : ''}</span>)}</React.Fragment>
        ))}
        {linha('Depositante (INPI)', v.depositante ? `${v.depositante}${v.tipo_de_pessoa ? ` — ${v.tipo_de_pessoa}` : ''}` : v.titular)}
        {linha('Inventor', v.inventor)}
        {linha('Requerente do PCT', v.pct_requerente)}
      </div>
    </div>
  )
}
