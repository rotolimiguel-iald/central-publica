import { useCallback, useEffect, useMemo, useRef, useState, type FormEvent } from 'react'
import { createPortal } from 'react-dom'
import {
  api, ApiError,
  type IaldAppAcao, type IaldAppComando, type IaldAppEstado, type IaldAppPedido, type IaldAppUsuario,
} from '../api'
import { useMe, isAdmin } from '../auth'

// ANEXO da patente IALD (BR102026003443-6) — aba "Usuários do app": liberar/recusar pedidos de
// acesso e bloquear/desbloquear contas do app da IALD pela internet, sem o PC receber nada de fora.
// Ligação "pull": esta tela só ENFILEIRA ordens na Central; o servidor da IALD busca as ordens,
// executa com a SUA própria lista de ações permitidas e devolve o resultado + um retrato mínimo.
// A régua desta tela:
//  - só 4 ações (liberar, recusar, bloquear, desbloquear) — nada de criar admin, senha, exportar,
//    apagar, plano ou acesso estendido;
//  - toda ordem pede a chave da Central DE NOVO (campo senha, não guardado, limpo no envio);
//  - dados mínimos (LGPD): nome, e-mail MASCARADO, usuário, situação, datas, provedor, tentativas;
//  - todo texto do servidor é dado de terceiros (o nome do pedido é digitado por quem pede):
//    só texto JSX, sem caracteres de controle/bidi, nunca HTML, href ou src;
//  - falha de leitura é falha visível — nunca "tudo ok" por omissão.

const POLL_ESTADO_MS = 15_000
const POLL_ORDEM_MS = 5_000
const MAX_ORDENS_ACOMPANHADAS = 5
const SYNC_VELHO_S = 180
const NOTA_MAX = 200
const CHAVE_MAX = 512
const ORDENS_MOSTRADAS = 20

const PEDIDO_ABERTO = new Set(['pendente', 'pending', 'aberto', 'novo'])
const STATUS_VIVO = new Set(['pendente', 'entregue'])
const ID_COMANDO = /^[A-Za-z0-9_-]{1,96}$/

const ACAO_ROTULO: Record<string, string> = {
  aprovar: 'liberar', recusar: 'recusar', bloquear: 'bloquear', desbloquear: 'desbloquear',
}
const PROVEDOR: Record<string, string> = {
  apple: 'Apple', apple_nativo: 'Apple (app)', apple_web: 'Apple (web)', google: 'Google',
  senha: 'usuário e senha',
}
const STATUS: Record<string, { rotulo: string; cor: string }> = {
  pendente: { rotulo: 'pendente — na fila', cor: '#ffd60a' },
  entregue: { rotulo: 'entregue à IALD', cor: '#35b7ff' },
  executado: { rotulo: 'executado', cor: '#30d158' },
  falhou: { rotulo: 'falhou', cor: '#ff453a' },
  expirado: { rotulo: 'expirado', cor: '#8195ab' },
  sem_resultado: { rotulo: 'sem resposta da IALD', cor: '#ff9f0a' },
  desconhecido: { rotulo: 'não encontrado', cor: '#8195ab' },
}
const DIALOGO: Record<IaldAppAcao, { titulo: string; botao: string; texto: string; perigo: boolean }> = {
  aprovar: {
    titulo: 'Liberar acesso ao app', botao: 'Liberar', perigo: false,
    texto: 'O pedido é aprovado e a pessoa passa a ter acesso ao app da IALD, com conta comum (nunca administrador).',
  },
  recusar: {
    titulo: 'Recusar pedido de acesso', botao: 'Recusar', perigo: true,
    texto: 'O pedido é recusado e a pessoa não recebe acesso.',
  },
  bloquear: {
    titulo: 'Bloquear conta', botao: 'Bloquear', perigo: true,
    texto: 'A conta perde o acesso ao app quando a IALD executar a ordem, até ser desbloqueada.',
  },
  desbloquear: {
    titulo: 'Desbloquear conta', botao: 'Desbloquear', perigo: false,
    texto: 'A conta volta a poder entrar no app.',
  },
}

// ---- higiene do texto vindo do servidor ----

/** Controle C0/C1, soft hyphen, marcas e isolantes bidi, larguras zero, separadores de
 *  linha/parágrafo, BOM, âncoras de anotação, surrogates soltos e caracteres TAG. */
function invisivel(cp: number): boolean {
  return cp <= 0x1f || (cp >= 0x7f && cp <= 0x9f) || cp === 0xad || cp === 0x061c || cp === 0x180e
    || (cp >= 0x200b && cp <= 0x200f) || (cp >= 0x2028 && cp <= 0x202e)
    || (cp >= 0x2060 && cp <= 0x206f) || cp === 0xfeff || (cp >= 0xfff9 && cp <= 0xfffb)
    || (cp >= 0xd800 && cp <= 0xdfff) || (cp >= 0xe0000 && cp <= 0xe007f)
}

function texto(v: unknown): string {
  return typeof v === 'string' ? v : typeof v === 'number' && Number.isFinite(v) ? String(v) : ''
}

/** Texto seguro para exibição: tira controle/bidi, junta espaços, corta no limite. */
function limpo(v: unknown, max = 160): string {
  let out = ''
  for (const ch of texto(v)) out += invisivel(ch.codePointAt(0) ?? 0) ? ' ' : ch
  const cps = Array.from(out.replace(/\s+/g, ' ').trim())
  return cps.length > max ? cps.slice(0, max - 1).join('') + '…' : cps.join('')
}

/** O alvo de uma ordem vai EXATAMENTE como veio (não se "conserta" um identificador).
 *  Se tiver espaço, controle ou bidi, a tela mostraria outra coisa do que a ordem atinge —
 *  então a ação fica desligada (falha fechada). */
function alvoSeguro(v: string): boolean {
  if (v.length === 0 || v.length > 128) return false
  for (const ch of v) if (invisivel(ch.codePointAt(0) ?? 0) || /\s/.test(ch)) return false
  return true
}

function de<T>(mapa: Record<string, T>, k: string): T | undefined {
  return Object.hasOwn(mapa, k) ? mapa[k] : undefined
}

/** Remascara por garantia (o servidor já manda mascarado): no máximo 2 caracteres do usuário
 *  + '***@' + domínio. Idempotente: 'ma***@gmail.com' fica igual. Sem '@' ⟹ nada. */
function mascarar(v: unknown): string {
  const s = limpo(v, 254).replace(/ /g, '')
  const at = s.lastIndexOf('@')
  if (at < 0) return ''
  const local = s.slice(0, at)
  const dominio = s.slice(at + 1) || '***'
  const base = Array.from(local.split('*')[0])
  const visivel = base.slice(0, !local.includes('*') && base.length <= 2 ? 1 : 2).join('')
  return `${visivel}***@${dominio}`
}

// ---- datas ----

const ISO_SEM_FUSO = /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$/
function paraMs(v: unknown): number | null {
  if (typeof v === 'number' && Number.isFinite(v) && v > 0) return v > 1e12 ? v : v * 1000
  if (typeof v !== 'string' || !v) return null
  // o backend roda em UTC: data ISO sem fuso é lida como UTC, não como hora local
  const n = Date.parse(ISO_SEM_FUSO.test(v) ? v.replace(' ', 'T') + 'Z' : v)
  return Number.isFinite(n) ? n : null
}
function fmtData(v: unknown): string {
  const ms = paraMs(v)
  if (ms == null) return limpo(v, 32) || '—'
  return new Date(ms).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}
function fmtIdade(s: number): string {
  if (s < 120) return `${s} s`
  if (s < 7200) return `${Math.round(s / 60)} min`
  if (s < 172800) return `${Math.round(s / 3600)} h`
  return `${Math.round(s / 86400)} dias`
}

// ---- normalização defensiva do que o servidor manda ----

function comoComando(x: unknown): IaldAppComando | null {
  if (!x || typeof x !== 'object') return null
  const o = x as Record<string, unknown>
  const c = (o.comando && typeof o.comando === 'object' ? o.comando : o) as Record<string, unknown>
  const id = texto(c.id)
  if (!ID_COMANDO.test(id)) return null
  return {
    id, acao: texto(c.acao), alvo: texto(c.alvo), status: texto(c.status).toLowerCase(),
    criado_em: texto(c.criado_em), expira_em: texto(c.expira_em), nota: texto(c.nota),
    resultado: c.resultado,
  }
}
function comoPedido(x: unknown): IaldAppPedido | null {
  if (!x || typeof x !== 'object') return null
  const o = x as Record<string, unknown>
  const id = texto(o.id)
  if (!id) return null
  return {
    id, nome: texto(o.nome), email_mascarado: mascarar(texto(o.email_mascarado) || texto(o.email)),
    provedor: texto(o.provedor), criado_em: texto(o.criado_em) || texto(o.criado),
    tentativas: typeof o.tentativas === 'number' && Number.isFinite(o.tentativas) ? o.tentativas : NaN,
    status: texto(o.status).toLowerCase(),
  }
}
function comoUsuario(x: unknown): IaldAppUsuario | null {
  if (!x || typeof x !== 'object') return null
  const o = x as Record<string, unknown>
  const username = texto(o.username)
  if (!username) return null
  const st = texto(o.status).toLowerCase()
  // Falha fechada: só "ativo"/"bloqueado" (ou admin === false explícito) admitem ação.
  // "protegido", admin true, status desconhecido ou marca ausente ⟹ conta protegida, sem botões.
  const protegido = o.admin === true || (st ? !(st === 'ativo' || st === 'bloqueado') : o.admin !== false)
  return {
    username, nome: texto(o.nome), email_mascarado: mascarar(texto(o.email_mascarado) || texto(o.email)),
    provedor: texto(o.provedor),
    bloqueado: st ? st === 'bloqueado' : o.bloqueado === true,
    protegido, criado_em: texto(o.criado_em) || texto(o.criado),
  }
}
function rank(status: string): number {
  return status === 'pendente' ? 0 : status === 'entregue' ? 1 : 2
}
function textoResultado(r: unknown): string {
  if (r == null || r === '') return ''
  if (typeof r === 'string') return limpo(r, 240)
  if (typeof r === 'number' || typeof r === 'boolean') return String(r)
  if (typeof r === 'object') {
    const o = r as Record<string, unknown>
    for (const k of ['mensagem', 'erro', 'error', 'detail', 'motivo']) {
      if (typeof o[k] === 'string') return limpo(o[k], 240)
    }
    try { return limpo(JSON.stringify(r), 240) } catch { return '' }
  }
  return ''
}

// ---- erros ----

type Fatal = { titulo: string; texto: string } | null

function msgErro(e: unknown, contexto: 'ordem' | 'leitura'): string {
  if (e instanceof ApiError) {
    const d = limpo(e.detail, 200)
    switch (e.status) {
      case 401: return d || (contexto === 'ordem'
        ? 'Chave da Central incorreta, ou a sessão expirou.' : 'Sessão expirada — entre de novo na Central.')
      case 403: return d || 'Recusado pelo servidor — só o administrador da Central (na nuvem) usa esta aba.'
      case 409: return d || 'Já existe uma ordem na fila para este alvo.'
      case 400: case 415: case 422: return d || 'Ordem inválida — recusada pelo servidor.'
      case 429: return d || 'Muitas tentativas. Aguarde alguns minutos.'
      case 503: return d || 'A ligação com a IALD não está disponível neste servidor agora.'
      default: return d ? `${d} (erro ${e.status})` : `Falha (erro ${e.status}).`
    }
  }
  return 'Falha de rede — a Central não respondeu.'
}

/** Erros que param a leitura periódica (insistir não resolve). */
function fatalDe(e: unknown): Fatal {
  if (!(e instanceof ApiError)) return null
  const d = limpo(e.detail, 200)
  if (e.status === 401) return { titulo: 'Sessão expirada', texto: 'Entre de novo na Central para continuar.' }
  if (e.status === 403) return { titulo: 'Acesso recusado', texto: d || 'Só o administrador da Central (na nuvem) usa esta aba.' }
  if (e.status === 404) return { titulo: 'Ligação ausente', texto: 'Este servidor da Central ainda não tem a ligação com o app da IALD (/api/iald-app).' }
  if (e.status === 400) return { titulo: 'Ligação desligada', texto: d || 'O servidor recusou a leitura.' }
  return null
}

// ---- estilos (mesma paleta do resto da Central) ----

const linha: React.CSSProperties = {
  display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center', justifyContent: 'space-between',
  padding: '10px 12px', border: '1px solid var(--line)', borderRadius: 10,
  background: 'var(--panel-2)', marginTop: 8,
}
const coluna: React.CSSProperties = { flex: '1 1 240px', minWidth: 0 }
const quebra: React.CSSProperties = { overflowWrap: 'anywhere' }
const acoes: React.CSSProperties = { display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }
const vermelho: React.CSSProperties = { color: '#ff6b6b' }
const okBox: React.CSSProperties = { background: '#0e1a12', borderColor: '#1f7a3f55', color: '#a9e8bd' }

function Chip({ status }: { status: string }) {
  const s = de(STATUS, status) || { rotulo: limpo(status, 24) || 'desconhecido', cor: '#8195ab' }
  return (
    <span className="pill" style={{ border: `1px solid ${s.cor}66`, color: s.cor, background: `${s.cor}14` }}>
      {s.rotulo}
    </span>
  )
}

/** A idade da última busca da IALD, medida pelo relógio do SERVIDOR (cabeçalho Date). */
function SyncBanner({ syncMs, skew, geradoEm }: { syncMs: number | null; skew: number; geradoEm: unknown }) {
  const [agora, setAgora] = useState(() => Date.now())
  useEffect(() => {
    const t = setInterval(() => setAgora(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])
  const idade = syncMs == null ? null : Math.max(0, Math.round((agora + skew - syncMs) / 1000))
  const velho = idade == null || idade > SYNC_VELHO_S
  const retrato = paraMs(geradoEm) != null ? fmtData(geradoEm) : ''
  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12.5, margin: '4px 0 12px' }}>
        <span className="dot" style={{ background: velho ? '#ff9f0a' : '#30d158' }} />
        <span>{idade == null
          ? 'A IALD ainda não sincronizou com esta Central.'
          : `IALD sincronizou há ${fmtIdade(idade)}`}</span>
        {retrato && <span className="muted">· retrato de {retrato}</span>}
      </div>
      {velho && (
        <div className="aviso">
          O servidor da IALD não está buscando ordens agora (PC desligado?). As ordens ficam na fila por 10 minutos.
        </div>
      )}
    </>
  )
}

type Alvo = { acao: IaldAppAcao; alvo: string; quem: string; email: string }

export default function IaldAppUsuarios() {
  const me = useMe()
  const admin = isAdmin(me)
  const [authOn, setAuthOn] = useState<boolean | null>(null)
  const [estado, setEstado] = useState<IaldAppEstado | null>(null)
  const [skew, setSkew] = useState(0)
  const [erro, setErro] = useState('')
  const [fatal, setFatal] = useState<Fatal>(null)
  const [msg, setMsg] = useState('')
  const [acomp, setAcomp] = useState<Record<string, IaldAppComando>>({})
  const [sumidos, setSumidos] = useState<Record<string, true>>({})
  const [dialogo, setDialogo] = useState<Alvo | null>(null)
  const [filtro, setFiltro] = useState('')
  const [rodada, setRodada] = useState(0)
  const vivo = useRef(true)
  const emCurso = useRef(false)

  useEffect(() => { vivo.current = true; return () => { vivo.current = false } }, [])

  // 1) a aba só liga com o login da nuvem; local (sem login) = desligada, falha fechada
  useEffect(() => {
    if (!admin) return
    let ok = true
    api.authStatus()
      .then(s => { if (ok) setAuthOn(!!s.enabled) })
      .catch(() => { if (ok) setErro('Não consegui ler /api/auth/status — a Central não respondeu.') })
    return () => { ok = false }
  }, [admin, rodada])

  const carregar = useCallback(async () => {
    try {
      const { body, serverMs } = await api.ialdAppEstado()
      if (!vivo.current) return
      const ok = body && typeof body === 'object' ? body : null
      setEstado(ok)
      // relógio do servidor: o campo "agora" (se houver) ou o cabeçalho Date
      const srv = paraMs(ok?.agora) ?? serverMs
      if (srv != null) setSkew(srv - Date.now())
      setErro('')
    } catch (e) {
      if (!vivo.current) return
      const f = fatalDe(e)
      if (f) setFatal(f)
      else setErro('Falha ao ler o estado: ' + msgErro(e, 'leitura'))
    }
  }, [])

  // 2) leitura periódica do estado (pausa com a aba do navegador escondida)
  useEffect(() => {
    if (!admin || authOn !== true || fatal) return
    carregar()
    const t = setInterval(() => { if (!document.hidden) carregar() }, POLL_ESTADO_MS)
    return () => clearInterval(t)
  }, [admin, authOn, fatal, carregar, rodada])

  const comandos = useMemo(() => {
    const m = new Map<string, IaldAppComando>()
    for (const x of Array.isArray(estado?.comandos) ? estado.comandos : []) {
      const c = comoComando(x)
      if (c) m.set(c.id, c)
    }
    for (const c of Object.values(acomp)) {
      const b = m.get(c.id)
      if (!b || rank(c.status) >= rank(b.status)) m.set(c.id, c)
    }
    for (const [id, c] of m) {
      if (Object.hasOwn(sumidos, id) && STATUS_VIVO.has(c.status)) {
        m.set(id, { ...c, status: 'desconhecido', resultado: 'ordem não encontrada no servidor' })
      }
    }
    return [...m.values()].sort((a, b) => (paraMs(b.criado_em) ?? 0) - (paraMs(a.criado_em) ?? 0))
  }, [estado, acomp, sumidos])

  const vivosIds = comandos.filter(c => STATUS_VIVO.has(c.status))
    .slice(0, MAX_ORDENS_ACOMPANHADAS).map(c => c.id).join(',')

  // 3) acompanhamento ao vivo das ordens não terminadas (a cada 5 s)
  useEffect(() => {
    if (!admin || fatal || !vivosIds) return
    const ids = vivosIds.split(',')
    const t = setInterval(async () => {
      if (document.hidden || emCurso.current) return
      emCurso.current = true
      let terminou = false
      try {
        for (const id of ids) {
          try {
            const { body } = await api.ialdAppComando(id)
            if (!vivo.current) return
            const c = comoComando(body)
            if (!c || c.id !== id) continue
            if (!STATUS_VIVO.has(c.status)) terminou = true
            setAcomp(a => ({ ...a, [id]: c }))
          } catch (e) {
            if (!vivo.current) return
            if (e instanceof ApiError && e.status === 404) {   // a ordem sumiu do servidor
              setSumidos(s => ({ ...s, [id]: true }))
              continue
            }
            const f = fatalDe(e)
            if (f) { setFatal(f); return }
          }
        }
        if (terminou) carregar()
      } finally { emCurso.current = false }
    }, POLL_ORDEM_MS)
    return () => clearInterval(t)
  }, [admin, fatal, vivosIds, carregar])

  const ocupadoPor = useMemo(() => {
    const m = new Map<string, string>()
    for (const c of comandos) if (STATUS_VIVO.has(c.status) && !m.has(c.alvo)) m.set(c.alvo, c.status)
    return m
  }, [comandos])

  const snap = estado?.snapshot && typeof estado.snapshot === 'object' ? estado.snapshot : null
  const falhas = useMemo(() => (Array.isArray(estado?.falhas_sync_recentes) ? estado.falhas_sync_recentes : [])
    .slice(-10).map(x => {
      if (!x || typeof x !== 'object') return limpo(x, 160)
      const o = x as Record<string, unknown>
      const vezes = typeof o.vezes === 'number' && Number.isFinite(o.vezes) && o.vezes > 1
        ? `${Math.round(o.vezes)}× (desde ${fmtData(o.primeira)})` : ''
      return [fmtData(o.ts), texto(o.status) && `erro ${limpo(o.status, 8)}`, limpo(o.motivo, 120), vezes]
        .filter(Boolean).join(' · ')
    }).filter(Boolean), [estado])
  // recusas SEM assinatura válida (qualquer um na internet): só a contagem, por motivo
  const anonimas = useMemo(() => {
    const r = estado?.recusas_sem_assinatura
    if (!r || typeof r !== 'object') return ''
    const o = r as Record<string, unknown>
    const total = typeof o.total === 'number' && Number.isFinite(o.total) ? Math.round(o.total) : 0
    if (total <= 0) return ''
    const por = o.por_motivo && typeof o.por_motivo === 'object'
      ? Object.entries(o.por_motivo as Record<string, unknown>).slice(0, 6)
        .map(([m, n]) => `${limpo(m, 60)}: ${typeof n === 'number' ? Math.round(n) : '?'}`).join('; ')
      : ''
    return `${o.no_minimo === true ? 'pelo menos ' : ''}${total} busca(s) recusada(s) sem assinatura válida `
      + `nos últimos 10 min${por ? ` (${por})` : ''} — nenhuma mudou nada; se a IALD parou de `
      + 'sincronizar, confira se o segredo dela é o mesmo desta Central'
  }, [estado])
  const omitidos = useMemo(() => {
    const s = estado?.snapshot
    const o = s && typeof s === 'object' ? (s as Record<string, unknown>).omitidos : null
    if (!o || typeof o !== 'object') return ''
    const n = (v: unknown) => (typeof v === 'number' && Number.isFinite(v) && v > 0 ? Math.round(v) : 0)
    const p = n((o as Record<string, unknown>).pedidos), u = n((o as Record<string, unknown>).usuarios)
    return p || u ? `Retrato parcial: ${p} pedido(s) e ${u} conta(s) passaram do limite e não vieram `
      + '(pendentes e bloqueadas vêm primeiro).' : ''
  }, [estado])
  const pedidos = useMemo(
    () => (Array.isArray(snap?.pedidos) ? snap.pedidos : []).map(comoPedido)
      .filter((p): p is IaldAppPedido => p !== null),
    [snap])
  const usuarios = useMemo(
    () => (Array.isArray(snap?.usuarios) ? snap.usuarios : []).map(comoUsuario)
      .filter((u): u is IaldAppUsuario => u !== null),
    [snap])
  const abertos = pedidos.filter(p => PEDIDO_ABERTO.has(p.status))
  const outros = pedidos.length - abertos.length
  const f = filtro.trim().toLowerCase()
  const contas = f
    ? usuarios.filter(u => [u.username, u.nome, u.email_mascarado].some(x => x.toLowerCase().includes(f)))
    : usuarios

  const fechar = useCallback(() => setDialogo(null), [])
  const aoEnfileirar = useCallback((c: IaldAppComando | null, a: Alvo) => {
    setDialogo(null)
    if (c) setAcomp(x => ({ ...x, [c.id]: c }))
    setMsg(`Ordem enfileirada: ${de(ACAO_ROTULO, a.acao) || a.acao} → ${limpo(a.alvo, 64)}. `
      + 'Ela vale por 10 minutos e é executada quando o servidor da IALD buscar.')
    carregar()
  }, [carregar])

  function tentarDeNovo() {
    setFatal(null); setErro(''); setRodada(r => r + 1)
  }

  function botao(acao: IaldAppAcao, alvo: string, quem: string, email: string, rotulo: string, perigo: boolean) {
    const ok = alvoSeguro(alvo)
    return (
      <button key={acao} className={perigo ? 'btn ghost xs' : 'btn xs'} style={perigo ? vermelho : undefined}
        disabled={!ok || !!fatal}
        title={ok ? undefined : 'identificador com caracteres inválidos — use o painel local da IALD'}
        onClick={() => { setMsg(''); setDialogo({ acao, alvo, quem, email }) }}>
        {rotulo}
      </button>
    )
  }

  if (!admin) {
    return (
      <div className="panel">
        <h4 style={{ marginTop: 0 }}>Usuários do app</h4>
        <p className="muted">Esta aba é exclusiva do administrador da Central.</p>
      </div>
    )
  }

  if (authOn === false) {
    return (
      <div className="panel">
        <h4 style={{ marginTop: 0 }}>Usuários do app IALD</h4>
        <p className="muted" style={{ fontSize: 13, lineHeight: 1.6 }}>
          Esta aba só funciona na Central da nuvem (central.iald.ia.br), com o login pela sua
          criptografia. Aqui, localmente, a Central roda sem login — por isso a ligação com o app
          fica <b>desligada</b> (falha fechada). No PC, use o painel da própria IALD.
        </p>
      </div>
    )
  }

  return (
    <div className="panel">
      <h4 style={{ marginTop: 0, marginBottom: 4 }}>Usuários do app IALD</h4>
      <div className="muted" style={{ fontSize: 12.5, lineHeight: 1.55, marginBottom: 10 }}>
        Libere ou recuse pedidos de acesso e bloqueie ou desbloqueie contas do app — de qualquer lugar.
        A Central só guarda a <b>ordem</b>; o servidor da IALD a busca e executa. Toda ordem pede a
        chave da Central de novo.
      </div>

      {fatal && (
        <div className="device-err" style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
          <span><b>{fatal.titulo}</b> — {fatal.texto}</span>
          <button className="btn ghost xs" onClick={tentarDeNovo}>tentar de novo</button>
        </div>
      )}
      {erro && !fatal && (
        <div className="device-err" style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
          <span>{erro}</span>
          {authOn === null && <button className="btn ghost xs" onClick={tentarDeNovo}>tentar de novo</button>}
        </div>
      )}
      {msg && <div className="aviso" style={{ ...okBox, marginTop: 10 }}>{msg}</div>}
      {!estado && !erro && !fatal && <div className="muted" style={{ marginTop: 10 }}>carregando…</div>}

      {estado && (
        <>
          <SyncBanner syncMs={paraMs(estado.ultima_sincronizacao)} skew={skew} geradoEm={snap?.gerado_em} />

          {estado.sync_configurado === false && (
            <div className="device-err" style={{ marginBottom: 12 }}>
              A ligação com a IALD ainda não está configurada neste servidor
              ({limpo(estado.sync_problema, 200) || 'falta o segredo de sincronização'}).
              Nenhuma ordem será buscada até isso ser feito.
            </div>
          )}
          {anonimas && <div className="muted" style={{ ...quebra, fontSize: 12, marginBottom: 8 }}>{anonimas}</div>}
          {omitidos && <div className="aviso" style={{ marginBottom: 12 }}>{omitidos}</div>}
          {falhas.length > 0 && (
            <details style={{ marginBottom: 12, fontSize: 12 }}>
              <summary style={{ cursor: 'pointer', color: '#ff9f0a' }}>
                {falhas.length} falha(s) recente(s) de sincronização
              </summary>
              {falhas.map((f, i) => <div key={i} className="muted" style={{ ...quebra, marginTop: 4 }}>{f}</div>)}
            </details>
          )}

          {!snap && (
            <p className="muted" style={{ fontSize: 12.5 }}>
              Ainda não há retrato da IALD nesta Central — a lista aparece depois da primeira busca do servidor da IALD.
            </p>
          )}

          {snap && (
            <>
              <h4 style={{ marginBottom: 2 }}>Pedidos de acesso ({abertos.length})</h4>
              {abertos.length === 0 && <p className="muted" style={{ fontSize: 12.5 }}>Nenhum pedido esperando.</p>}
              {abertos.map((p, i) => {
                const quem = limpo(p.nome, 80) || 'Nome não informado'
                const email = limpo(p.email_mascarado, 80) || '—'
                const ocupado = ocupadoPor.get(p.id)
                return (
                  <div key={`${p.id}#${i}`} style={linha}>
                    <div style={coluna}>
                      <div style={{ ...quebra, fontWeight: 600 }}>{quem}</div>
                      <div className="muted" style={{ fontSize: 11.5 }}>
                        {p.nome ? 'Nome informado no cadastro' : 'A pessoa pode completar o nome no app antes da liberação.'}
                      </div>
                      <div className="muted" style={{ ...quebra, fontSize: 12 }}>{email}</div>
                      <div className="muted" style={{ fontSize: 11.5, marginTop: 2 }}>
                        {de(PROVEDOR, p.provedor) || limpo(p.provedor, 24) || '—'} · pedido em {fmtData(p.criado_em)}
                        {' · '}{Number.isFinite(p.tentativas) ? `${p.tentativas} tentativa(s)` : 'tentativas: —'}
                      </div>
                    </div>
                    <div style={acoes}>
                      {ocupado ? <Chip status={ocupado} /> : <>
                        {botao('aprovar', p.id, quem, email, 'Liberar', false)}
                        {botao('recusar', p.id, quem, email, 'Recusar', true)}
                      </>}
                    </div>
                  </div>
                )
              })}
              {outros > 0 && (
                <p className="muted" style={{ fontSize: 11.5, marginTop: 6 }}>
                  {outros} pedido(s) já resolvido(s) não aparecem aqui.
                </p>
              )}

              <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', marginTop: 22 }}>
                <h4 style={{ margin: 0 }}>Contas ({usuarios.length})</h4>
                {usuarios.length > 6 && (
                  <input className="txt" placeholder="filtrar por usuário, nome ou e-mail" value={filtro}
                    onChange={e => setFiltro(e.target.value)} maxLength={80}
                    style={{ flex: '1 1 200px', maxWidth: 340, padding: '6px 10px', fontSize: 12.5 }} />
                )}
              </div>
              {contas.length === 0 && (
                <p className="muted" style={{ fontSize: 12.5 }}>{usuarios.length ? 'Nenhuma conta com esse filtro.' : 'Nenhuma conta no retrato.'}</p>
              )}
              {contas.map((u, i) => {
                const usuario = limpo(u.username, 64)
                const quem = limpo(u.nome, 80)
                const email = limpo(u.email_mascarado, 80) || '—'
                const ocupado = ocupadoPor.get(u.username)
                return (
                  <div key={`${u.username}#${i}`} style={linha}>
                    <div style={coluna}>
                      <div style={quebra}>
                        <b>{quem || 'Nome não informado'}</b>
                        <div className="muted" style={{ fontSize: 11.5 }}>
                          {quem ? 'Nome informado no cadastro' : 'A pessoa pode completar o nome ao entrar no app.'}
                        </div>
                        <div className="muted" style={{ fontSize: 11.5, marginTop: 3 }}>
                          Identificador interno: <span style={{ fontFamily: 'Cascadia Code, Consolas, monospace' }}>{usuario}</span>
                        </div>
                      </div>
                      <div className="muted" style={{ ...quebra, fontSize: 12 }}>{email}</div>
                      <div className="muted" style={{ fontSize: 11.5, marginTop: 2 }}>
                        {de(PROVEDOR, u.provedor || '') || limpo(u.provedor, 24) || 'Entrada não informada'} · conta criada em {fmtData(u.criado_em)}
                      </div>
                    </div>
                    <div style={acoes}>
                      {u.protegido
                        ? <span className="role-chip" title="conta de administrador ou protegida — não se altera por aqui">protegida</span>
                        : u.bloqueado
                          ? <span className="pill" style={{ color: '#ff6b6b', border: '1px solid #ff6b6b55' }}>bloqueada</span>
                          : <span className="pill" style={{ color: '#30d158', border: '1px solid #30d15855' }}>ativa</span>}
                      {!u.protegido && (ocupado ? <Chip status={ocupado} /> : u.bloqueado
                        ? botao('desbloquear', u.username, (quem ? quem + ' · ' : '') + usuario, email, 'Desbloquear', false)
                        : botao('bloquear', u.username, (quem ? quem + ' · ' : '') + usuario, email, 'Bloquear', true))}
                    </div>
                  </div>
                )
              })}
            </>
          )}

          <h4 style={{ marginTop: 22, marginBottom: 2 }}>Ordens recentes</h4>
          {comandos.length === 0 && <p className="muted" style={{ fontSize: 12.5 }}>Nenhuma ordem enviada.</p>}
          {comandos.slice(0, ORDENS_MOSTRADAS).map(c => {
            const res = textoResultado(c.resultado)
            return (
              <div key={c.id} style={linha}>
                <div style={coluna}>
                  <div style={quebra}>
                    <b>{de(ACAO_ROTULO, c.acao) || limpo(c.acao, 24) || '—'}</b>
                    {' → '}
                    <span style={{ fontFamily: 'Cascadia Code, Consolas, monospace', fontSize: 12 }}>{limpo(c.alvo, 64) || '—'}</span>
                  </div>
                  <div className="muted" style={{ fontSize: 11.5, marginTop: 2 }}>
                    enviada {fmtData(c.criado_em)}
                    {STATUS_VIVO.has(c.status) && c.expira_em && <> · expira {fmtData(c.expira_em)}</>}
                  </div>
                  {c.nota && <div className="muted" style={{ ...quebra, fontSize: 11.5, marginTop: 2 }}>nota: {limpo(c.nota, NOTA_MAX)}</div>}
                  {res && <div className="muted" style={{ ...quebra, fontSize: 11.5, marginTop: 2 }}>{res}</div>}
                </div>
                <div style={acoes}><Chip status={c.status} /></div>
              </div>
            )
          })}
        </>
      )}

      <p className="legal-note" style={{ marginTop: 16, lineHeight: 1.55 }}>
        Só quatro ações existem aqui: liberar, recusar, bloquear e desbloquear. Contas de administrador
        não se alteram por esta aba. Dados mostrados (LGPD): nome, e-mail mascarado, usuário, situação,
        datas, provedor e tentativas — nada além. Cada ordem vale por 10 minutos; a chave digitada vai
        só naquela ordem e não é guardada.
      </p>

      {dialogo && <ConfirmaOrdem alvo={dialogo} onCancelar={fechar} onEnfileirado={aoEnfileirar} />}
    </div>
  )
}

function ConfirmaOrdem({ alvo, onCancelar, onEnfileirado }: {
  alvo: Alvo
  onCancelar: () => void
  onEnfileirado: (c: IaldAppComando | null, a: Alvo) => void
}) {
  const [chave, setChave] = useState('')
  const [nota, setNota] = useState('')
  const [busy, setBusy] = useState(false)
  const [erro, setErro] = useState('')
  const comNota = alvo.acao === 'recusar' || alvo.acao === 'bloquear'
  const d = DIALOGO[alvo.acao]

  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape' && !busy) onCancelar() }
    window.addEventListener('keydown', k)
    return () => window.removeEventListener('keydown', k)
  }, [busy, onCancelar])

  async function enviar(e: FormEvent) {
    e.preventDefault()
    if (busy || !chave) return
    const segredo = chave
    setChave('')              // a chave sai do campo no ato do envio; nunca é guardada
    setBusy(true); setErro('')
    try {
      const n = comNota ? limpo(nota, NOTA_MAX) : ''
      const { body } = await api.ialdAppOrdem({
        acao: alvo.acao, alvo: alvo.alvo, chave: segredo, ...(n ? { nota: n } : {}),
      })
      onEnfileirado(comoComando(body), alvo)
    } catch (err) {
      setErro(msgErro(err, 'ordem'))
      setBusy(false)
    }
  }

  return createPortal(
    <div onClick={() => !busy && onCancelar()} style={{
      position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(0,0,0,0.65)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16,
    }}>
      <form role="dialog" aria-modal="true" aria-labelledby="iapp-dlg-t" onSubmit={enviar}
        onClick={e => e.stopPropagation()} autoComplete="off" style={{
          width: 'min(460px, 96vw)', maxHeight: '92vh', overflowY: 'auto', background: '#0e1420',
          border: '1px solid #232b38', borderRadius: 14, padding: 22, boxShadow: '0 20px 80px rgba(0,0,0,0.5)',
        }}>
        <div id="iapp-dlg-t" style={{ fontSize: 17, fontWeight: 800, color: d.perigo ? '#ff6b6b' : 'var(--accent)' }}>
          {d.titulo}
        </div>
        <div style={{ marginTop: 10, fontSize: 13, ...quebra }}>
          <b>{alvo.quem}</b>{alvo.email && alvo.email !== '—' && <span className="muted"> · {alvo.email}</span>}
        </div>
        <div className="muted" style={{ fontSize: 11, marginTop: 2, fontFamily: 'Cascadia Code, Consolas, monospace', ...quebra }}>
          {alvo.alvo}
        </div>
        <div style={{ fontSize: 12.5, color: '#c8d0da', marginTop: 10, lineHeight: 1.55 }}>{d.texto}</div>

        {comNota && (
          <div style={{ marginTop: 14 }}>
            <label htmlFor="iapp-nota" style={{ fontSize: 11.5, color: '#8a94a6' }}>Nota (opcional, até {NOTA_MAX} caracteres)</label>
            <input id="iapp-nota" className="txt" value={nota} maxLength={NOTA_MAX} disabled={busy}
              onChange={e => setNota(e.target.value)} placeholder="motivo, para o registro"
              style={{ width: '100%', marginTop: 4 }} />
          </div>
        )}

        <div style={{ marginTop: 14 }}>
          <label htmlFor="iapp-chave" style={{ fontSize: 11.5, color: '#8a94a6' }}>
            Redigite a chave da Central (a mesma do login) para confirmar
          </label>
          <input id="iapp-chave" name="confirmacao-central" type="password" autoComplete="off" autoFocus
            spellCheck={false} autoCapitalize="off" autoCorrect="off" maxLength={CHAVE_MAX}
            className="txt" value={chave} disabled={busy} onChange={e => setChave(e.target.value)}
            placeholder="chave da Central" style={{ width: '100%', marginTop: 4 }} />
        </div>

        <div style={{ fontSize: 11, color: '#8a94a6', marginTop: 12, lineHeight: 1.5 }}>
          A ordem fica na fila por até 10 minutos e é executada quando o servidor da IALD buscar.
          A chave não é guardada: vai só nesta ordem e o campo é limpo no envio.
        </div>

        {erro && <div className="device-err" style={{ marginTop: 10 }}>{erro}</div>}

        <div style={{ display: 'flex', gap: 8, marginTop: 16, justifyContent: 'flex-end', flexWrap: 'wrap' }}>
          <button type="button" className="btn ghost" onClick={() => !busy && onCancelar()} disabled={busy}>cancelar</button>
          <button type="submit" className={d.perigo ? 'btn ghost' : 'btn'} disabled={busy || !chave}
            style={d.perigo ? { ...vermelho, borderColor: '#ff6b6b88' } : undefined}>
            {busy ? 'enviando…' : d.botao}
          </button>
        </div>
      </form>
    </div>,
    document.body,
  )
}
