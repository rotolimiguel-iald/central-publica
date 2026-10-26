import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type PatentClass, type PatentRow } from '../api'
import { EpctPill, Markers } from '../ui'
import PublicAcomCard from './PublicAcomCard'
import '../public-central.css'

const INICIAIS = 6   // pedidos da vista inicial, antes de «Ver todos»

// Uma linha (classe) que tem pedidos; se o registro dela faltar no retrato, vale o próprio identificador.
type Linha = Pick<PatentClass, 'id' | 'ordinal' | 'name' | 'markers'>

function normalizar(valor: string): string {
  return valor.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLocaleLowerCase('pt-BR')
}

export default function PublicHome() {
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [patents, setPatents] = useState<PatentRow[]>([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState(false)
  const [busca, setBusca] = useState('')
  const [classeSelecionada, setClasseSelecionada] = useState('')
  const [mostrarTodos, setMostrarTodos] = useState(false)
  const notaRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let vivo = true
    // 24/10 (achado do revisor): no retrato /api/classes pode faltar — a página segue só com os pedidos; e a falha
    // nunca mostra o texto de parse («Unexpected token…»), só uma frase que se entende
    Promise.all([api.classes().catch(() => []), api.patents()])
      .then(([cs, ps]) => {
        if (!vivo) return
        setClasses(cs)
        setPatents(ps)
      })
      .catch(() => { if (vivo) setErro(true) })
      .finally(() => { if (vivo) setCarregando(false) })
    return () => { vivo = false }
  }, [])

  const porId = useMemo(() => new Map(classes.map(c => [c.id, c] as const)), [classes])
  // só as linhas que têm pedidos (a API lista também as vazias): é o que se conta, se filtra e se agrupa
  const linhas = useMemo<Linha[]>(() => [...new Set(patents.map(p => p.class_id))]
    .map(id => porId.get(id) ?? { id, ordinal: Number(/^CLASS_(\d+)_/.exec(id)?.[1] ?? 0), name: id, markers: [] })
    .sort((a, b) => a.ordinal - b.ordinal), [patents, porId])
  const semNomes = linhas.some(l => !porId.has(l.id))

  const filtroAtivo = Boolean(busca.trim() || classeSelecionada)
  const filtrados = useMemo(() => {
    const termo = normalizar(busca.trim())
    return patents.filter(p => {
      if (classeSelecionada && p.class_id !== classeSelecionada) return false
      if (!termo) return true
      return normalizar(`${p.display_name} ${p.id} ${p.title_54}`).includes(termo)
    })
  }, [patents, busca, classeSelecionada])
  const visiveis = mostrarTodos || filtroAtivo ? filtrados : filtrados.slice(0, INICIAIS)
  const byClass = (cid: string) => visiveis.filter(p => p.class_id === cid)
  // «Limpar» desmonta o botão clicado: o foco vai para a nota de resultados, nunca cai no body
  const limpar = () => { setBusca(''); setClasseSelecionada(''); notaRef.current?.focus() }

  return (
    <div className="pc-home">
      <section className="pc-hero" aria-labelledby="pc-title">
        <div className="pc-eyebrow">TGL · IALD · Central pública</div>
        <h1 id="pc-title">A Central aberta</h1>
        <p>Os dispositivos, o código, as execuções e os artefatos da IALD — para ler, verificar e baixar.</p>
        <div className="pc-hero-actions">
          {/* 24/10 (subida, achado do revisor): href="#…" vira rota no createHashRouter (404); rolar por script */}
          <button type="button" className="pc-button pc-button-primary"
            onClick={() => document.getElementById('colecao-publica')?.scrollIntoView({ behavior: 'smooth', block: 'start' })}>
            Explorar{patents.length > 0 ? ` os ${patents.length} pedidos` : ' os pedidos'}
          </button>
          <a className="pc-button pc-button-gold" href={(import.meta as any).env.BASE_URL + 'um.acom'} download="um.acom">↓ Baixar um.acom</a>
          <a className="pc-link" href="https://iald.ia.br/#acom" target="_blank" rel="noopener">Abrir no descompactador →</a>
        </div>
      </section>

      <PublicAcomCard />

      <section className="pc-collection" id="colecao-publica" aria-labelledby="pc-collection-title">
        <div className="pc-section-head">
          <div>
            <div className="pc-eyebrow">A coleção</div>
            <h2 id="pc-collection-title">Os pedidos e suas linhas</h2>
          </div>
          {!carregando && !erro && (
            <div className="pc-collection-count" aria-label={`${patents.length} pedidos em ${linhas.length} linhas`}>
              <span><b>{patents.length}</b> pedidos</span>
              <span><b>{linhas.length}</b> linhas</span>
            </div>
          )}
        </div>

        {carregando && <div className="pc-note" role="status">Lendo a coleção pública…</div>}
        {erro && <div className="pc-error" role="alert">Não foi possível ler a coleção agora. Recarregue a página para tentar de novo.</div>}
        {!carregando && !erro && semNomes && (
          <div className="pc-note">Os nomes das linhas não puderam ser lidos agora; os pedidos aparecem agrupados pelo identificador de cada linha.</div>
        )}

        {!carregando && !erro && (
          <>
            <div className="pc-filters" aria-label="Filtros da coleção">
              <label className="pc-search">
                <span>Buscar na coleção</span>
                <input type="search" value={busca} onChange={e => setBusca(e.target.value)}
                  placeholder="Nome, processo ou título" />
              </label>
              <label className="pc-class-filter">
                <span>Linha</span>
                <select value={classeSelecionada} onChange={e => setClasseSelecionada(e.target.value)}>
                  <option value="">Todas as linhas</option>
                  {linhas.map(c => <option key={c.id} value={c.id}>{String(c.ordinal).padStart(2, '0')} · {c.name}</option>)}
                </select>
              </label>
              {filtroAtivo && <button type="button" className="pc-clear" onClick={limpar}>Limpar filtros</button>}
            </div>
            <div className="pc-result-note" role="status" tabIndex={-1} ref={notaRef}>
              {visiveis.length} de {filtrados.length} pedido(s) nesta vista
              {filtroAtivo && filtrados.length !== patents.length ? ` · ${patents.length} no total` : ''}
            </div>
          </>
        )}

        <div className="pc-class-list">
          {linhas.map(c => {
            const ps = byClass(c.id)
            if (!ps.length) return null
            return (
              // 24/10 (achado do revisor): todo grupo com cartões na vista abre — «6 de 16» e «16 de 16» mostram o que dizem
              <details className="pc-class" key={c.id} open>
                <summary>
                  <span className="pc-class-order">{String(c.ordinal).padStart(2, '0')}</span>
                  <span className="pc-class-name">{c.name}</span>
                  <span className="pc-class-count">{ps.length} item(ns)</span>
                  <Markers items={c.markers} />
                </summary>
                <div className="pc-patent-grid">
                  {ps.map(p => (
                    <Link className="pc-patent-card" to={`/patents/${p.id}`} key={p.id}>
                      <span className="pc-patent-top">
                        <strong>{p.display_name}</strong>
                        {p.role === 'agregadora' && <span title="agregadora">★</span>}
                        {p.role === 'raiz' && <span title="raiz">⬢</span>}
                      </span>
                      <span className="pc-patent-id">{p.id}</span>
                      <span className="pc-patent-title">{p.title_54}</span>
                      <span className="pc-patent-foot">
                        {p.epct_status ? <EpctPill status={p.epct_status} /> : null}
                        <span>{p.claims_total ?? '—'} reiv.</span>
                        <span className="pc-patent-open">Abrir artefatos →</span>
                      </span>
                    </Link>
                  ))}
                </div>
              </details>
            )
          })}
        </div>

        {!carregando && !erro && !visiveis.length && (
          <div className="pc-note">
            Nenhum pedido corresponde a estes filtros.
            <button type="button" className="pc-clear" onClick={limpar}>Limpar filtros</button>
          </div>
        )}
        {/* um só botão que troca o rótulo: o elemento persiste e o foco fica nele (dois botões condicionais o perdiam para o body) */}
        {!carregando && !erro && !filtroAtivo && filtrados.length > INICIAIS && (
          <button type="button" className="pc-show-all" onClick={() => setMostrarTodos(v => !v)}>
            {mostrarTodos ? `Mostrar apenas os ${INICIAIS} primeiros` : `Ver todos os ${filtrados.length} pedidos`}
          </button>
        )}
      </section>
    </div>
  )
}
