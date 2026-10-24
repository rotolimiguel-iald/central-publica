import { useEffect, useState } from 'react'

interface UmAcomInfo {
  chave_publica?: string
  sha256?: string
  bytes?: number
  n_arquivos?: number
  gerado_em?: string
  formato?: string
}

const BASE_PUB_UM: string = ((import.meta as any).env || {}).BASE_URL || '/'

export default function PublicAcomCard() {
  const [info, setInfo] = useState<UmAcomInfo | null>(null)
  const [erro, setErro] = useState('')

  useEffect(() => {
    let vivo = true
    fetch(BASE_PUB_UM + 'um_acom_info.json', { cache: 'no-store' })
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((dados: UmAcomInfo) => { if (vivo) setInfo(dados) })
      .catch(e => { if (vivo) setErro(e instanceof Error ? e.message : 'Falha ao ler os metadados.') })
    return () => { vivo = false }
  }, [])

  const tamanho = typeof info?.bytes === 'number'
    ? `${new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 }).format(info.bytes / 1048576)} MB`
    : null

  return (
    <section className="pc-acom" aria-labelledby="pc-acom-title">
      <div className="pc-acom-main">
        <div className="pc-eyebrow">O único download da Central</div>
        <h2 id="pc-acom-title">A Central inteira em um arquivo</h2>
        <p>O <code>um.acom</code> reúne o núcleo, os dispositivos e seus artefatos. Baixe direto ou abra no descompactador público.</p>
        {(info || erro) && (
          <dl className="pc-acom-meta">
            {typeof info?.n_arquivos === 'number' && <div><dt>Arquivos</dt><dd>{info.n_arquivos}</dd></div>}
            {tamanho && <div><dt>Tamanho</dt><dd>{tamanho}</dd></div>}
            {info?.gerado_em && <div><dt>Gerado em</dt><dd>{info.gerado_em}</dd></div>}
            {info?.sha256 && <div className="pc-acom-hash"><dt>sha256</dt><dd title={info.sha256}>{info.sha256}</dd></div>}
            {erro && <div><dt>Metadados</dt><dd>Não foi possível lê-los agora; os links continuam disponíveis.</dd></div>}
          </dl>
        )}
      </div>
      <div className="pc-acom-actions">
        <a className="pc-button pc-button-gold" href={BASE_PUB_UM + 'um.acom'} download="um.acom">↓ Baixar um.acom</a>
        <a className="pc-button pc-button-outline" href="https://iald.ia.br/#acom" target="_blank" rel="noopener">Abrir no descompactador →</a>
        {info?.chave_publica && (
          <details className="pc-acom-details">
            <summary>Chave pública e formato</summary>
            <div><span>Chave universal pública</span><code>{info.chave_publica}</code></div>
            {info.formato && <div><span>Formato</span><code>{info.formato}</code></div>}
          </details>
        )}
      </div>
    </section>
  )
}
