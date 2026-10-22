import { useEffect, useMemo, useState } from 'react'
import { api, type ComponentsDoc, type Component } from './api'

// Camada (b) do render: mapa de componentes clicável. Layout data-driven a partir
// de components.json (posições normalizadas 0..1). SVG + overlay HTML, sem libs.
const KIND_COLOR: Record<string, string> = {
  block: '#35b7ff', 'flow-node': '#7ce7c8', state: '#ffd60a',
  share: '#c88cff', qubit: '#ff9f6a',
}

export default function ComponentMap({ pid }: { pid: string }) {
  const [doc, setDoc] = useState<ComponentsDoc | null>(null)
  const [sel, setSel] = useState<Component | null>(null)

  useEffect(() => { setSel(null); api.components(pid).then(setDoc).catch(() => setDoc(null)) }, [pid])

  const index = useMemo(() => {
    const m = new Map<string, { c: Component; kind: string }>()
    doc?.groups.forEach(g => g.components.forEach(c => m.set(c.id, { c, kind: g.kind })))
    return m
  }, [doc])

  if (!doc) return <p className="muted">carregando componentes…</p>
  if (!doc.available) return (
    <p className="legal-note">
      Mapa de componentes ainda não descrito para esta patente. Adiciona-se um
      <code> components.json</code> na pasta da patente (fonte da verdade) e ele aparece aqui.
    </p>
  )

  const W = 960, H = 620
  return (
    <div>
      <p className="muted" style={{ fontSize: 12.5, marginTop: 0 }}>
        Camada (b): diagrama de componentes clicável. Clique um bloco para ver sua descrição.
        <span className="legal-note"> {doc.note}</span>
      </p>
      <div className="cmap-wrap">
        <svg viewBox={`0 0 ${W} ${H}`} className="cmap-svg" role="img"
          aria-label="mapa de componentes">
          {/* flows */}
          {doc.flows.map((f, i) => {
            const a = index.get(f.from)?.c, b = index.get(f.to)?.c
            if (!a || !b) return null
            const x1 = a.x * W + 70, y1 = a.y * H + 20
            const x2 = b.x * W + 70, y2 = b.y * H + 20
            return (
              <g key={i}>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#2a3a4e" strokeWidth={1.5}
                  markerEnd="url(#arrow)" />
              </g>
            )
          })}
          <defs>
            <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="3"
              orient="auto" markerUnits="strokeWidth">
              <path d="M0,0 L7,3 L0,6 Z" fill="#3a5570" />
            </marker>
          </defs>
          {/* nodes */}
          {doc.groups.flatMap(g => g.components.map(c => {
            const color = KIND_COLOR[g.kind] || '#35b7ff'
            const active = sel?.id === c.id
            const x = c.x * W, y = c.y * H
            return (
              <g key={g.name + c.id} transform={`translate(${x},${y})`}
                style={{ cursor: 'pointer' }} onClick={() => setSel(c)}>
                <rect width={140} height={40} rx={9}
                  fill={active ? color : '#0d141d'} fillOpacity={active ? 0.22 : 1}
                  stroke={color} strokeWidth={active ? 2.2 : 1.3} />
                <text x={9} y={16} fill={color} fontSize={11} fontWeight={700}>{c.id}</text>
                <text x={9} y={31} fill="#dce6f2" fontSize={10}>
                  {c.label.length > 22 ? c.label.slice(0, 21) + '…' : c.label}
                </text>
              </g>
            )
          }))}
        </svg>
        <div className="cmap-detail">
          {sel ? (
            <>
              <div className="cmap-detail-id">{sel.id}</div>
              <div className="cmap-detail-label">{sel.label}</div>
              <span className="badge mk" style={{ marginBottom: 8 }}>{sel.marker}</span>
              <p style={{ fontSize: 12.5, lineHeight: 1.5 }}>{sel.desc}</p>
            </>
          ) : (
            <p className="muted" style={{ fontSize: 12.5 }}>
              Selecione um componente no diagrama.
              <br /><br />Legenda:
              {Object.entries(KIND_COLOR).filter(([k]) =>
                doc.groups.some(g => g.kind === k)).map(([k, v]) => (
                  <span key={k} style={{ display: 'block', marginTop: 6 }}>
                    <span className="cmap-legend-dot" style={{ background: v }} />
                    {doc.groups.find(g => g.kind === k)?.name}
                  </span>
                ))}
            </p>
          )}
        </div>
      </div>
      {doc.constants?.length > 0 && (
        <div className="cmap-consts">
          {doc.constants.map((k, i) => (
            <div key={i} className="cmap-const">
              <b>{k.symbol}</b> = <span style={{ color: 'var(--accent-2)' }}>{k.value}</span>
              <div className="muted" style={{ fontSize: 11.5 }}>{k.note}</div>
            </div>
          ))}
        </div>
      )}
      <p className="muted" style={{ fontSize: 11.5, marginTop: 10 }}>
        Fonte: {doc.source}. Camada (c) 3D ilustrativa — próximo ciclo. Ilustração de
        engenharia, não prova física.
      </p>
    </div>
  )
}
