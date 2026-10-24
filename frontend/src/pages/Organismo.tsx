import { useCallback, useEffect, useMemo, useState } from 'react'
import { PUBLICA } from '../api'
import './Organismo.css'

type Estado = 'OK' | 'DEFASADO' | 'PENDENTE_OPERADOR' | 'EM_OBRA' | 'FALHA' | 'INFO'
type Filtro = 'ACAO' | 'TODOS' | Estado

interface OrganismoItem {
  superficie: string
  item: string
  esperado: unknown
  achado: unknown
  estado: Estado
}

interface OrganismoDocumento {
  medido_em: string
  selo: { versao: string; pin: string; timestamp: string }
  resumo: Partial<Record<Estado, number>>
  itens: OrganismoItem[]
}

const ESTADOS: Estado[] = ['DEFASADO', 'PENDENTE_OPERADOR', 'EM_OBRA', 'FALHA', 'OK', 'INFO']
const ACAO: Estado[] = ['DEFASADO', 'PENDENTE_OPERADOR', 'EM_OBRA', 'FALHA']
const ROTULO: Record<Estado, string> = {
  DEFASADO: 'Defasado', PENDENTE_OPERADOR: 'Com o operador', EM_OBRA: 'Em obra',
  FALHA: 'Falha', OK: 'Em dia', INFO: 'Contexto',
}
const ICONE: Record<Estado, string> = {
  DEFASADO: '↻', PENDENTE_OPERADOR: '◇', EM_OBRA: '◌', FALHA: '!', OK: '✓', INFO: 'i',
}

function texto(valor: unknown): string {
  if (valor === null || valor === undefined || valor === '') return '—'
  if (typeof valor === 'string') return valor
  return JSON.stringify(valor)
}

function validarDocumento(valor: unknown): OrganismoDocumento {
  const doc = valor as OrganismoDocumento
  if (!doc || typeof doc.medido_em !== 'string' || !doc.selo || !Array.isArray(doc.itens)) {
    throw new Error('A leitura do organismo não tem o formato esperado.')
  }
  return doc
}

async function lerOrganismo(metodo: 'GET' | 'POST'): Promise<OrganismoDocumento> {
  const resposta = await fetch('/api/organismo', {
    method: metodo,
    cache: 'no-store',
    headers: { Accept: 'application/json' },
  })
  if (!resposta.ok) throw new Error(`A medição respondeu HTTP ${resposta.status}.`)
  return validarDocumento(await resposta.json())
}

function passoDoOperador(item: OrganismoItem): string {
  const alvo = `${item.superficie} ${item.item}`.toLowerCase()
  if (alvo.includes('hsts')) return 'Revisar e autorizar a fase 2 do HSTS na hospedagem.'
  if (alvo.includes('llms.txt') || alvo.includes('sitemap.xml')) return 'Publicar a porta de leitura e conferir a resposta 200.'
  if (alvo.includes('x.php')) return 'Aplicar o bloqueio de scripts no domínio e repetir a sonda.'
  if (alvo.includes('robots.txt') || alvo.includes('claudebot') || alvo.includes('gptbot')) {
    return 'Revisar os leitores de IA permitidos no Cloudflare.'
  }
  if (alvo.includes('zenodo')) return 'Decidir se esta versão terá um novo depósito no Zenodo.'
  return 'Revisar este item e registrar a decisão ou o responsável.'
}

export default function Organismo() {
  const [doc, setDoc] = useState<OrganismoDocumento | null>(null)
  const [carregando, setCarregando] = useState(true)
  const [medindo, setMedindo] = useState(false)
  const [erro, setErro] = useState('')
  const [aviso, setAviso] = useState('')
  const [filtro, setFiltro] = useState<Filtro>('ACAO')
  const [busca, setBusca] = useState('')

  const carregar = useCallback(async () => {
    setCarregando(true)
    setErro('')
    try {
      setDoc(await lerOrganismo('GET'))
    } catch (e) {
      setErro(e instanceof Error ? e.message : 'Não foi possível ler o organismo.')
    } finally {
      setCarregando(false)
    }
  }, [])

  useEffect(() => { void carregar() }, [carregar])

  const medir = async () => {
    setMedindo(true)
    setErro('')
    setAviso('')
    try {
      setDoc(await lerOrganismo('POST'))
      setAviso('Nova medição recebida. O quadro abaixo já reflete o JSON devolvido.')
    } catch (e) {
      setErro(e instanceof Error ? e.message : 'Não foi possível medir de novo.')
    } finally {
      setMedindo(false)
    }
  }

  const itens = useMemo(() => doc?.itens ?? [], [doc])
  const contar = (estado: Estado) => doc?.resumo?.[estado] ?? itens.filter(i => i.estado === estado).length
  const filtrados = useMemo(() => {
    const termo = busca.trim().toLocaleLowerCase('pt-BR')
    return itens.filter(item => {
      const noFiltro = filtro === 'TODOS' || (filtro === 'ACAO' ? ACAO.includes(item.estado) : item.estado === filtro)
      if (!noFiltro) return false
      if (!termo) return true
      return `${item.superficie} ${item.item} ${texto(item.esperado)} ${texto(item.achado)}`
        .toLocaleLowerCase('pt-BR').includes(termo)
    })
  }, [itens, filtro, busca])

  const superficies = useMemo(() => {
    const grupos = new Map<string, OrganismoItem[]>()
    filtrados.forEach(item => grupos.set(item.superficie, [...(grupos.get(item.superficie) ?? []), item]))
    return [...grupos.entries()]
  }, [filtrados])

  const totalAcao = ACAO.reduce((soma, estado) => soma + contar(estado), 0)
  const primeiroFiltro = (proximo: Filtro) => { setFiltro(atual => atual === proximo ? 'TODOS' : proximo) }

  return (
    <div className="org-page">
      <header className="org-hero">
        <div className="org-hero-copy">
          <div className="org-kicker">Medição contra o selo corrente</div>
          <h1>Estado do organismo</h1>
          <p>O que precisa de ação aparece antes do que está em dia. Cada número abaixo vem do JSON de medição.</p>
        </div>
        {doc && (
          <div className="org-seal" aria-label={`Selo ${doc.selo.versao}`}>
            <span>Selo corrente</span>
            <strong>{doc.selo.versao}</strong>
            <code>{doc.selo.pin}</code>
            <small>{doc.selo.timestamp}</small>
          </div>
        )}
      </header>

      <div className="org-toolbar">
        <div className="org-measured">
          {doc ? <>Medido em <time>{doc.medido_em}</time> · {totalAcao} ponto(s) pedem atenção</> : 'Lendo a medição…'}
        </div>
        <div className="org-toolbar-actions">
          <button type="button" className="org-button org-button-quiet" onClick={() => void carregar()} disabled={carregando || medindo}>
            {carregando && doc ? 'Relendo…' : 'Reler JSON'}
          </button>
          {!PUBLICA && (
            <button type="button" className="org-button" onClick={() => void medir()} disabled={medindo || carregando}>
              {medindo ? 'Medindo…' : '↻ Medir de novo'}
            </button>
          )}
        </div>
      </div>

      {erro && <div className="org-alert" role="alert"><b>Leitura não concluída.</b> {erro} {doc && 'A última leitura válida permanece visível.'}</div>}
      {aviso && <div className="org-success" role="status">{aviso}</div>}

      {carregando && !doc ? (
        <div className="org-loading" role="status">Carregando o estado do organismo…</div>
      ) : doc ? (
        <>
          <section className="org-summary" aria-label="Resumo por estado">
            {ESTADOS.map(estado => (
              <button
                type="button"
                key={estado}
                className={`org-stat org-${estado.toLowerCase()} ${filtro === estado ? 'is-active' : ''}`}
                onClick={() => primeiroFiltro(estado)}
                aria-pressed={filtro === estado}
              >
                <span className="org-stat-icon" aria-hidden="true">{ICONE[estado]}</span>
                <strong>{contar(estado)}</strong>
                <span>{ROTULO[estado]}</span>
              </button>
            ))}
          </section>

          <section className="org-lanes" aria-label="O que fazer">
            {([
              ['DEFASADO', 'Sincronizar o organismo', 'Fontes e superfícies que ainda não alcançaram o selo.'],
              ['PENDENTE_OPERADOR', 'Com o operador', 'Decisões, hospedagem e atos que não pertencem à rotina automática.'],
              ['EM_OBRA', 'Em obra', 'Trabalho já em movimento nesta leitura.'],
              ['FALHA', 'Falhas de medição', 'Leituras que precisam de diagnóstico antes de qualquer conclusão.'],
            ] as [Estado, string, string][]).map(([estado, titulo, descricao]) => {
              const n = contar(estado)
              if (!n) return null
              return (
                <button type="button" className={`org-lane org-${estado.toLowerCase()}`} key={estado} onClick={() => { setFiltro(estado); setBusca('') }}>
                  <span className="org-lane-top"><span>{titulo}</span><strong>{n}</strong></span>
                  <span>{descricao}</span>
                  <span className="org-lane-link">Ver por superfície →</span>
                </button>
              )
            })}
          </section>

          <section className="org-register" aria-labelledby="org-register-title">
            <div className="org-register-head">
              <div>
                <div className="org-kicker">Quadro por superfície</div>
                <h2 id="org-register-title">O próximo passo, sem procurar no ruído</h2>
              </div>
              <label className="org-search">
                <span>Filtrar itens</span>
                <input value={busca} onChange={e => setBusca(e.target.value)} placeholder="Superfície, item, esperado ou achado" type="search" />
              </label>
            </div>
            <div className="org-filter-row" aria-label="Filtro de leitura">
              <button type="button" className={filtro === 'ACAO' ? 'is-active' : ''} onClick={() => setFiltro('ACAO')}>Pedem atenção · {totalAcao}</button>
              <button type="button" className={filtro === 'TODOS' ? 'is-active' : ''} onClick={() => setFiltro('TODOS')}>Quadro completo · {itens.length}</button>
              {(busca || filtro !== 'ACAO') && <button type="button" onClick={() => { setFiltro('ACAO'); setBusca('') }}>Limpar filtros</button>}
            </div>

            <div className="org-result-note" role="status">
              {filtrados.length} de {itens.length} item(ns) · {superficies.length} superfície(s)
            </div>

            {superficies.length ? (
              <div className="org-groups">
                {superficies.map(([superficie, registros], indice) => (
                  <details className="org-group" key={superficie} open={indice < 2 || filtro !== 'ACAO' || Boolean(busca)}>
                    <summary>
                      <span className="org-group-name">{superficie}</span>
                      <span className="org-group-count">{registros.length} item(ns)</span>
                      <span className="org-group-states">{[...new Set(registros.map(i => ROTULO[i.estado]))].join(' · ')}</span>
                    </summary>
                    <div className="org-items">
                      {registros.map((item, i) => (
                        <article className={`org-item org-${item.estado.toLowerCase()}`} key={`${item.superficie}-${item.item}-${i}`}>
                          <div className="org-item-head">
                            <span className="org-state"><span aria-hidden="true">{ICONE[item.estado]}</span> {ROTULO[item.estado]}</span>
                            <h3>{item.item}</h3>
                          </div>
                          <dl className="org-values">
                            <div><dt>Esperado</dt><dd>{texto(item.esperado)}</dd></div>
                            <div><dt>Achado</dt><dd>{texto(item.achado)}</dd></div>
                          </dl>
                          {item.estado === 'PENDENTE_OPERADOR' && <p className="org-next"><b>Passo:</b> {passoDoOperador(item)}</p>}
                        </article>
                      ))}
                    </div>
                  </details>
                ))}
              </div>
            ) : (
              <div className="org-empty">
                <strong>Nenhum item nesta vista.</strong>
                <p>Altere a busca ou volte ao quadro completo.</p>
                <button type="button" className="org-button org-button-quiet" onClick={() => { setFiltro('TODOS'); setBusca('') }}>Abrir quadro completo</button>
              </div>
            )}
          </section>
        </>
      ) : (
        <div className="org-empty" role="alert">
          <strong>O organismo ainda não pôde ser lido.</strong>
          <p>Confira a rota de leitura e tente novamente.</p>
          <button type="button" className="org-button" onClick={() => void carregar()}>Tentar de novo</button>
        </div>
      )}
    </div>
  )
}
