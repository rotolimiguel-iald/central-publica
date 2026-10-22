import { useEffect, useState } from 'react'
import { api } from '../api'

// Duas faces da mesma memória: o header ontológico (Core) e o índice holográfico (Atlas).
// Aditivo — o Core segue sendo a face padrão, exatamente como antes.
const FACES = ['☀ TGL Core', '🗺 Atlas'] as const
type Face = typeof FACES[number]

const HEAD: Record<Face, { h1: string; sub: string }> = {
  '☀ TGL Core': {
    h1: 'TGL Core — header ontológico da Central',
    sub: 'Toda memória, runner e prompt compilado herda este arquivo. A cadeia canônica, os dois zeros, o Estado Verificado.',
  },
  '🗺 Atlas': {
    h1: '🗺 Atlas da TGL — a memória holográfica',
    sub: 'A forma canônica condensada: dicionário, pedras, ritos, dispositivos, casas, régua e leis da memória. Não substitui nenhuma fonte — indexa todas, com estatuto marcado e remissão de origem.',
  },
}

export default function TglCore() {
  const [face, setFace] = useState<Face>('☀ TGL Core')
  const [core, setCore] = useState('')
  const [atlas, setAtlas] = useState('')

  useEffect(() => { api.tglCore().then(setCore) }, [])
  useEffect(() => {
    if (face === '🗺 Atlas' && !atlas) api.tglAtlas().then(setAtlas)
  }, [face])

  const md = face === '🗺 Atlas' ? atlas : core
  return (
    <>
      <div className="h1">{HEAD[face].h1}</div>
      <div className="sub">{HEAD[face].sub}</div>
      <div className="tabs">
        {FACES.map(f => (
          <div key={f} className={`tab ${face === f ? 'active' : ''}`} onClick={() => setFace(f)}>{f}</div>
        ))}
      </div>
      <pre className="md" style={{ maxHeight: '78vh' }}>{md || 'carregando…'}</pre>
    </>
  )
}
