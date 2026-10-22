import { URGENCY_COLOR } from './api'

export function Markers({ items }: { items: string[] }) {
  return (
    <span className="marker-row">
      {items.map((m, i) => <span key={i} className="badge mk">{m}</span>)}
    </span>
  )
}

export function UrgencyDot({ level }: { level: string | null | undefined }) {
  const c = URGENCY_COLOR[level || 'cinza'] || URGENCY_COLOR.cinza
  return <span className="dot" style={{ background: c }} title={level || ''} />
}

export function EpctPill({ status }: { status: string }) {
  const map: Record<string, [string, string]> = {
    VIVO_DEPOSITADO_E_PAGO: ['ePCT vivo', '#0e2a1a'],
    A_DEPOSITAR: ['ePCT a depositar', '#2a220a'],
    SOMENTE_INPI: ['somente INPI', '#22160a'],
  }
  const [label, bg] = map[status] || [status, '#1a2230']
  return <span className="pill" style={{ background: bg, color: '#e8eef6' }}>{label}</span>
}

export function daysLabel(d: number | null): string {
  if (d === null || d === undefined) return '—'
  if (d < 0) return `vencido há ${-d} d`
  return `${d} d`
}
