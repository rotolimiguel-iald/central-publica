// Thin fetch layer over the local FastAPI backend. Relative /api works both in
// dev (Vite proxy) and prod (served by FastAPI on the same origin).

export interface Health {
  status: string
  external_calls: string
  patents_indexed: number
  classes_indexed: number
  originals_manifest_ok: boolean
  last_reindex_utc: string | null
  schema_version: string
  counts: Record<string, number>
}

export interface PatentClass {
  id: string; ordinal: number; name: string; slug: string
  markers: string[]; lock_note: string | null; patent_count: number
}

export interface PatentRow {
  id: string; slug: string; display_name: string; dir_name: string; class_id: string
  role: string | null; title_54: string; filing_date: string; priority_date: string
  epct_status: string; epct_number: string | null; prototype_status: string
  claims_total: number | null; doc_count: number; markers: string[]
  alert_level: string | null; next_due: string | null; next_urgency: string | null
}

export interface Deadline {
  id: number; patent_id: string; kind: string; label: string
  due_date: string | null; status: string; legal_note: string | null
  days_remaining: number | null; urgency?: string
  slug?: string; basis?: string; role?: string | null
}

export interface Note {
  id: number; tipo: string; active: number; done: number; text: string
  markers: string[]; source_section: string; line_ref: number
}

export interface RenderItem {
  id: number; kind: string; layer: string; title: string; marker: string
}

export interface Component {
  id: string; label: string; desc: string; marker: string; x: number; y: number
}
export interface ComponentGroup { name: string; kind: string; components: Component[] }
export interface ComponentFlow { from: string; to: string }
export interface ComponentConst { symbol: string; value: string; note: string }
export interface ComponentsDoc {
  available: boolean; patent_id?: string; title?: string; source?: string; note?: string
  groups: ComponentGroup[]; flows: ComponentFlow[]; constants: ComponentConst[]
}

export type Vec3 = [number, number, number]
export interface Node3D {
  id: string; label: string; desc: string; shape: string
  position: Vec3; size: number; color: string
  group: string; marker: string
  layer?: string; rotation?: Vec3; scale?: Vec3; material?: string; texture?: string
}
// Structural body pieces (casing, shielding, chambers) — schema v2
export interface Mesh3D {
  id: string; label?: string; desc?: string; shape: string
  position: Vec3; size?: number; scale?: Vec3; rotation?: Vec3
  color: string; material?: string; opacity?: number; layer?: string; marker?: string
  texture?: string
}
export interface Layer3D { id: string; name: string; order: number; peelable?: boolean }
export interface Dimension3D { from: Vec3; to: Vec3; label: string; color?: string }
export interface Edge3D { from: string; to: string; color?: string }
export interface Group3D { name: string; color: string; label: string; count: number; explodable?: boolean }
export interface Render3DDoc {
  available: boolean; patent_id?: string; title?: string; kind?: string; note?: string
  schema?: number
  camera?: { position: Vec3 }
  nodes: Node3D[]; edges: Edge3D[]; groups: Group3D[]; constants?: ComponentConst[]
  meshes?: Mesh3D[]; layers?: Layer3D[]; dimensions?: Dimension3D[]
}

export interface RunRow {
  id: string; patent_id: string; slug: string; display_name: string; role: string | null
  finished_at: string; status: string; beta_runtime: number
  physical_verdict_allowed: number; tests_passed: number | null
  max_verdict: string; result_hash: string | null; markers: string[]
}
export interface RunsDoc {
  runs: RunRow[]; runs_total: number; patents_with_runs: number
  patents_total: number; aviso: string
}

export interface PatentDetail extends PatentRow {
  docket: any; class: any; deadlines: Deadline[]; documents: any[]
  notes: Note[]; renders: RenderItem[]; runs: any[]; pendencias: any[]
  abstract: string | null; nature: string | null; peticao: string
  claims_independent: number | null; figures_count: number | null
  jurisdiction: string; pasta_original: string
}

export interface EvolucaoEntry {
  timestamp: string; result_hash_short: string | null
  tests_passed: number | null; tests_total: number | null
  verdict: string | null; runner: string | null
  sections: string[]; has_result: boolean
}
export interface EvolucaoDoc {
  available: boolean; patent_id: string; dir_name?: string
  total: number; entries: EvolucaoEntry[]
}

export interface ClaimsDoc {
  available: boolean; patent_id: string; title_54: string
  claims_total: number | null; claims_independent: number | null
  section_title: string; markdown: string; source: string; note: string
}

export interface EvidenceElo {
  role: string; title: string; proves: string; value?: string
  resolved: boolean; detail: string; ref?: string
  indexed_sha256?: string; live_sha256?: string; result_hash?: string
  hash_match?: boolean | null; test?: string; test_passed?: boolean | null
  doc_id?: number; code_path?: string; run?: string
}
export interface EvidenceClaim {
  n: number; marker: string; independent?: boolean; statement?: string
  verdict?: string; chain: EvidenceElo[]; all_resolved?: boolean
}
export interface EvidenceDoc {
  available: boolean; verified?: boolean; patent_id?: string
  claims_fully_resolved?: number; claims_total?: number
  elos_resolved?: number; elos_total?: number; claims: EvidenceClaim[]
}

// ── MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026, ordem do operador: «possam interagir com a central (somente em modo de
// visualização), igual eu interajo»). Build com VITE_CENTRAL_PUBLICA=1: cada leitura /api/... vira o arquivo estático do retrato
// público, achado pelo mapa api/_mapa.json (gerado por script a partir da Central do operador, só por GET, com os dados pessoais
// trocados por «[dado pessoal removido]»); toda ação (POST/DELETE) é recusada. Sem servidor: ninguém altera nada. No build normal
// (a Central do operador) nada disto roda.
const ENV_PUB: any = (import.meta as any).env || {}
export const PUBLICA: boolean = ENV_PUB.VITE_CENTRAL_PUBLICA === '1'
export const AVISO_PUBLICO = 'Modo público de visualização: esta ação existe só na Central do operador. Aqui se lê; o único download é o um.acom.'
const BASE_PUB: string = ENV_PUB.BASE_URL || '/'
let MAPA: Record<string, string> = {}
export async function carregarMapa(): Promise<void> {
  if (!PUBLICA) return
  try {
    const r = await fetch(BASE_PUB + 'api/_mapa.json', { cache: 'no-cache' })
    if (r.ok) MAPA = await r.json()
  } catch { /* sem mapa: as leituras falham à vista */ }
}
/** A URL que o navegador abre: na Central do operador é a própria; no modo público, o arquivo do retrato (ou a nota de que a leitura
 *  não faz parte dele). */
export function pub(url: string): string {
  if (!PUBLICA) return url
  const m = MAPA[url]
  return m ? BASE_PUB + m : BASE_PUB + 'fora_do_retrato.html'
}
function respostaPublicaFixa(url: string): any {
  if (url.startsWith('/api/auth/status')) return { enabled: false, authenticated: true, scheme: 'publico-visualizacao', beta: null }
  if (url.startsWith('/api/auth/me')) return { authenticated: true, role: 'visitante', name: 'Visitante (modo público)' }
  if (url.startsWith('/api/users')) return { enabled: false, users: [], roles: [] }
  return undefined
}
/** No modo público, o fetch de qualquer página passa por aqui: leitura de /api vai ao retrato; ação em /api é recusada. */
export function instalarFetchPublico(): void {
  if (!PUBLICA) return
  const orig = window.fetch.bind(window)
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    const u = typeof input === 'string' ? input : (input instanceof URL ? input.pathname + input.search : input.url)
    if (u.startsWith('/api/')) {
      const met = ((init && init.method) || (typeof input !== 'string' && !(input instanceof URL) ? input.method : 'GET') || 'GET').toUpperCase()
      if (met !== 'GET') return Promise.resolve(new Response(JSON.stringify({ detail: AVISO_PUBLICO }), { status: 403, headers: { 'Content-Type': 'application/json' } }))
      const fixo = respostaPublicaFixa(u)
      if (fixo !== undefined) return Promise.resolve(new Response(JSON.stringify(fixo), { status: 200, headers: { 'Content-Type': 'application/json' } }))
      return orig(pub(u))
    }
    return orig(input as any, init)
  }
}

async function j<T>(url: string, opts?: RequestInit): Promise<T> {
  const r = await fetch(url, opts)
  if (!r.ok) throw new Error(`${r.status} ${url}`)
  return r.json()
}
async function t(url: string): Promise<string> {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`${r.status} ${url}`)
  return r.text()
}

// ---- Usuários do app IALD (aba da patente BR102026003443-6, só administrador) ----
// Modelo de ligação "pull": a Central (nuvem) guarda a fila de ordens; o servidor da IALD
// busca as ordens e devolve um retrato mínimo (nome + e-mail mascarado). Nada entra no PC.
// Todo texto vindo daqui é dado de terceiros (o nome do pedido é digitado por quem pede):
// a tela o mostra só como texto JSX, nunca como HTML, href ou src.
export type IaldAppAcao = 'aprovar' | 'recusar' | 'bloquear' | 'desbloquear'
export type IaldAppStatusComando =
  'pendente' | 'entregue' | 'executado' | 'falhou' | 'expirado' | 'sem_resultado'
// Forma NORMALIZADA que a tela usa (a tela aceita o retrato cru em duas grafias:
// email_mascarado|email, criado_em|criado, bloqueado/admin booleanos | status ativo/bloqueado/protegido).
export interface IaldAppPedido {
  id: string; nome: string; email_mascarado: string; provedor: string
  criado_em: string; tentativas: number; status: string
}
export interface IaldAppUsuario {
  username: string; nome: string; email_mascarado: string; provedor?: string
  bloqueado: boolean; protegido: boolean; criado_em: string
}
export interface IaldAppComando {
  id: string; acao: string; alvo: string; status: string
  criado_em: string; expira_em: string; nota: string; resultado: unknown
}
// Forma CRUA do GET /api/iald-app/estado — tudo que vem de lá é tratado como não confiável.
export interface IaldAppEstado {
  ultima_sincronizacao: string | number | null
  snapshot: {
    gerado_em?: string | null; pedidos?: unknown[]; usuarios?: unknown[]; omitidos?: unknown
  } | null
  comandos: unknown[]
  agora?: string
  sync_configurado?: boolean
  sync_problema?: unknown
  // só falhas de buscas com assinatura VÁLIDA (a IALD); iguais somadas em "vezes"
  falhas_sync_recentes?: unknown[]
  // recusas sem assinatura válida (qualquer um na internet): só contagem por motivo
  recusas_sem_assinatura?: unknown
}
export interface IaldAppOrdem { acao: IaldAppAcao; alvo: string; nota?: string; chave: string }

/** Erro HTTP com o `detail` do backend preservado (o j() comum o descarta). */
export class ApiError extends Error {
  status: number
  detail: string
  constructor(status: number, detail: string, url: string) {
    super(`${status} ${url}`)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

/** fetch das rotas /api/iald-app/*: mesma origem, sem cache, sem seguir redirecionamento,
 *  sempre com o cabeçalho próprio X-Central-Acao (força preflight em qualquer chamada
 *  de outra origem). Devolve também o relógio do servidor (cabeçalho Date) para medir
 *  "sincronizou há N s" sem depender do relógio do aparelho. */
async function jApp<T>(url: string, opts: { method?: string; body?: string; json?: boolean } = {}):
  Promise<{ body: T; serverMs: number | null }> {
  if (PUBLICA) throw new ApiError(403, AVISO_PUBLICO, url)   // o app IALD (dados de terceiros) não entra no modo público
  const headers: Record<string, string> = { 'X-Central-Acao': '1', Accept: 'application/json' }
  if (opts.json) headers['Content-Type'] = 'application/json'
  const r = await fetch(url, {
    method: opts.method || 'GET', body: opts.body, headers,
    credentials: 'same-origin', cache: 'no-store', redirect: 'error',
  })
  const d = Date.parse(r.headers.get('Date') || '')
  if (!r.ok) {
    let detail = ''
    try {
      const b = await r.json()
      if (typeof b?.detail === 'string') detail = b.detail
    } catch { /* corpo não-JSON: fica só o status */ }
    throw new ApiError(r.status, detail, url)
  }
  return { body: (await r.json()) as T, serverMs: Number.isFinite(d) ? d : null }
}

export const api = {
  health: () => j<Health>('/api/health'),
  integrity: () => j<any>('/api/integrity'),
  reindex: () => j<any>('/api/reindex?force=true', { method: 'POST' }),
  classes: () => j<PatentClass[]>('/api/classes'),
  patents: () => j<PatentRow[]>('/api/patents'),
  patent: (id: string) => j<PatentDetail>(`/api/patents/${encodeURIComponent(id)}`),
  patentMemory: (id: string) => t(`/api/patents/${encodeURIComponent(id)}/memory`),
  claims: (id: string) => j<ClaimsDoc>(`/api/patents/${encodeURIComponent(id)}/claims`),
  evidence: (id: string) => j<EvidenceDoc>(`/api/patents/${encodeURIComponent(id)}/evidence`),
  evolucao: (id: string) => j<EvolucaoDoc>(`/api/patents/${encodeURIComponent(id)}/evolucao`),
  components: (id: string) => j<ComponentsDoc>(`/api/patents/${encodeURIComponent(id)}/components`),
  render3d: (id: string) => j<Render3DDoc>(`/api/patents/${encodeURIComponent(id)}/render3d`),
  fronteira: () => j<{ available: boolean; render3d?: Render3DDoc; seal?: any }>('/api/fronteira'),
  andamentos: () => j<any>('/api/andamentos'),
  andamentosRun: () => j<any>('/api/andamentos/run', { method: 'POST' }),
  backupStatus: () => j<any>('/api/backup/status'),
  backupRun: () => j<any>('/api/backup/run', { method: 'POST' }),
  epctStatus: () => j<any>('/api/epct/status'),
  epctTick: (m: { id: string; step: string; value: any; extra?: Record<string, string | null> }) =>
    j<any>('/api/epct/tick', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) }),
  ialdStatus: () => j<any>('/api/iald/status'),
  // A ORQUESTRAÇÃO DA IALD (AGI em construção, feita pelo Codex) — só leitura, exige admin
  ialdOrquestracao: () => j<any>('/api/iald/orquestracao'),
  ialdTask: (m: { name: string; action: string }) =>
    j<any>('/api/iald/task', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) }),
  ialdSanear: () => j<any>('/api/iald/sanear', { method: 'POST' }),
  andamentosRegistrar: (m: { processo: string; data: string; codigo_despacho?: string; descricao: string }) =>
    j<any>('/api/andamentos/registrar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(m) }),
  // A SENTINELA (22/09/2026): confirmar um despacho (o clique do operador) e ler a leitura da IALD nativa
  andamentosConfirmar: (id: string) =>
    j<any>('/api/andamentos/confirmar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id }) }),
  andamentosLeitura: (id: string) => j<{ id: string; texto: string }>(`/api/andamentos/leitura/${encodeURIComponent(id)}`),
  code: (id: string) => j<any>(`/api/patents/${encodeURIComponent(id)}/code`),
  codeFile: (id: string, path: string) =>
    t(`/api/patents/${encodeURIComponent(id)}/code/file?path=${encodeURIComponent(path)}`),
  runs: () => j<RunsDoc>('/api/runs'),
  docket: () => j<{ aviso: string; deadlines: Deadline[] }>('/api/docket'),
  pendencias: () => j<any[]>('/api/pendencias'),
  tglCore: () => t('/api/tgl-core'),
  tglAtlas: () => t('/api/tgl-atlas'),
  docText: (docId: number) => t(`/api/documents/${docId}/text`),
  toggleNote: (id: number, active: boolean) =>
    j<any>(`/api/notes/${id}/active`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ active }),
    }),
  addNote: (patent_id: string, tipo: string, text: string) =>
    j<any>('/api/notes', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patent_id, tipo, text, active: true }),
    }),
  authStatus: () => j<{ enabled: boolean; authenticated: boolean; scheme: string; beta: any }>('/api/auth/status'),
  me: () => j<{ authenticated: boolean; role: string; name: string; uid?: string }>('/api/auth/me'),
  users: () => j<{ enabled: boolean; users: any[]; roles: string[] }>('/api/users'),
  userAdd: (name: string, role: string, email: string) =>
    j<{ uid: string; name: string; role: string; email: string; key: string }>('/api/users', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, role, email }),
    }),
  userRemove: (uid: string) => j<any>(`/api/users/${encodeURIComponent(uid)}`, { method: 'DELETE' }),
  userRole: (uid: string, role: string) =>
    j<any>(`/api/users/${encodeURIComponent(uid)}/role`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ role }),
    }),
  authLogin: (secret: string) =>
    j<{ ok: boolean; role?: string; name?: string; expires_in?: number
        twofa_required?: boolean; challenge?: string; email_hint?: string }>('/api/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secret }),
    }),
  auth2fa: (challenge: string, code: string) =>
    j<{ ok: boolean; role: string; name: string; expires_in: number }>('/api/auth/2fa', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ challenge, code }),
    }),
  authLogout: () => j<any>('/api/auth/logout', { method: 'POST' }),
  // Usuários do APP IALD (não confundir com users*, que são os acessos da própria Central).
  ialdAppEstado: () => jApp<IaldAppEstado>('/api/iald-app/estado'),
  ialdAppOrdem: (m: IaldAppOrdem) =>
    jApp<any>('/api/iald-app/comandos', { method: 'POST', json: true, body: JSON.stringify(m) }),
  ialdAppComando: (id: string) =>
    jApp<any>(`/api/iald-app/comandos/${encodeURIComponent(id)}`),
  compile: () => j<any>('/api/compile', { method: 'POST' }),
  compiledList: () => j<any[]>('/api/compiled'),
  compiledGet: (fn: string) => t(`/api/compiled/${encodeURIComponent(fn)}`),
  // O botão UM: gera o tgl.acom (blob) cifrado com o código de inscrição (header, nunca URL).
  umBuild: async (secret: string): Promise<Blob> => {
    if (PUBLICA) {   // modo público: o um.acom da Central já colapsado pelo dispositivo ACOM, com a chave universal pública
      const r0 = await fetch(BASE_PUB + 'um.acom')
      if (!r0.ok) throw new Error(`erro ${r0.status} ao baixar o um.acom`)
      return r0.blob()
    }
    const r = await fetch('/api/um/build', { method: 'POST', headers: { 'X-Inscricao': secret } })
    if (!r.ok) {
      let msg = `erro ${r.status}`
      try { msg = (await r.json()).detail || msg } catch { /* */ }
      throw new Error(msg)
    }
    return r.blob()
  },
  // A 2ª via: gera o um.acom da oncologia (livre, chave universal pública embutida no backend).
  umBuildOncologia: async (): Promise<Blob> => {
    if (PUBLICA) {   // modo público: o um.acom da oncologia que o site já publica
      const r0 = await fetch(BASE_PUB + '../um.acom')
      if (!r0.ok) throw new Error(`erro ${r0.status} ao baixar o um.acom da oncologia`)
      return r0.blob()
    }
    const r = await fetch('/api/um/build-oncologia', { method: 'POST' })
    if (!r.ok) {
      let msg = `erro ${r.status}`
      try { msg = (await r.json()).detail || msg } catch { /* */ }
      throw new Error(msg)
    }
    return r.blob()
  },
}

export const URGENCY_COLOR: Record<string, string> = {
  vencido: '#ff3b30', vermelho: '#ff453a', laranja: '#ff9f0a',
  amarelo: '#ffd60a', verde: '#30d158', cinza: '#6b7280',
}
