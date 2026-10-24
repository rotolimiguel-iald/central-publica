import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type PatentClass, type PatentRow } from '../api'
import { EpctPill, Markers } from '../ui'
import PublicAcomCard from './PublicAcomCard'
import '../public-central.css'

export default function PublicHome() {
  const [classes, setClasses] = useState<PatentClass[]>([])
  const [patents, setPatents] = useState<PatentRow[]>([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  useEffect(() => {
    let vivo = true
    Promise.all([api.classes(), api.patents()])
      .then(([cs, ps]) => {
        if (!vivo) return
        setClasses(cs)
        setPatents(ps)
      })
      .catch(e => { if (vivo) setErro(e instanceof Error ? e.message : 'Não foi possível ler a coleção.') })
      .finally(() => { if (vivo) setCarregando(false) })
    return () => { vivo = false }
  }, [])

  const byClass = (cid: string) => patents.filter(p => p.class_id === cid)

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
            <div className="pc-collection-count" aria-label={`${patents.length} pedidos em ${classes.length} linhas`}>
              <span><b>{patents.length}</b> pedidos</span>
              <span><b>{classes.length}</b> linhas</span>
            </div>
          )}
        </div>

        {carregando && <div className="pc-note" role="status">Lendo a coleção pública…</div>}
        {erro && <div className="pc-error" role="alert">Não foi possível ler toda a coleção. {erro}</div>}

        <div className="pc-class-list">
          {classes.map((c, indice) => {
            const ps = byClass(c.id)
            if (!ps.length) return null
            return (
              <details className="pc-class" key={c.id} open={indice < 2}>
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
      </section>
    </div>
  )
}
