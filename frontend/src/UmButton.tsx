import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { api, PUBLICA } from './api'

// O botão UM — colapsa a Central inteira num tgl.acom cifrado. Pede o código de inscrição
// (o selo) em dois campos, com medidor de força e confirmação anti-erro de digitação.

// Salva o blob deixando o usuário ESCOLHER a pasta (File System Access API) quando disponível;
// senão cai no download padrão. showSaveFilePicker precisa do gesto do clique — por isso é
// chamado ANTES da geração (o handle fica reservado; a escrita acontece depois).
async function pickSaveHandle(name = 'tgl.acom'): Promise<any | null | 'cancel'> {
  const w = window as any
  if (!w.showSaveFilePicker) return null
  try {
    return await w.showSaveFilePicker({
      suggestedName: name,
      types: [{ description: 'ACOM selado (.acom)', accept: { 'application/octet-stream': ['.acom'] } }],
    })
  } catch (e: any) {
    if (e?.name === 'AbortError') return 'cancel'
    return null   // navegador negou/erro → cai no download padrão
  }
}

async function writeBlob(handle: any | null, blob: Blob, name = 'tgl.acom'): Promise<string> {
  if (handle) {
    const w = await handle.createWritable()
    await w.write(blob); await w.close()
    return handle.name || name
  }
  // fallback: download padrão (pasta de Downloads do navegador)
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = name
  document.body.appendChild(a); a.click(); a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 4000)
  return name
}

function strength(s: string): { score: number; label: string; color: string } {
  let score = 0
  if (s.length >= 8) score++
  if (s.length >= 14) score++
  if (/[a-z]/.test(s) && /[A-Z]/.test(s)) score++
  if (/\d/.test(s)) score++
  if (/[^A-Za-z0-9]/.test(s)) score++
  const labels = ['muito fraca', 'fraca', 'razoável', 'boa', 'forte', 'excelente']
  const colors = ['#ff453a', '#ff453a', '#ff9f0a', '#ffd60a', '#30d158', '#30d158']
  return { score, label: labels[score], color: colors[score] }
}

// ── MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026, ordem do operador: «a possibilidade, inclusive, de modo público, de colapsarem a
// central inteira em um.acom e baixarem na sua própria máquina, esse é o único acesso público de baixar direto na central»).
// Sem senha: o um.acom já vem colapsado pelo dispositivo ACOM (sem perdas, SHA-256 bit a bit) e selado com a chave universal
// pública, a mesma declarada no site para a oncologia.
const BASE_PUB_UM: string = ((import.meta as any).env || {}).BASE_URL || '/'
function UmPublico() {
  const [open, setOpen] = useState(false)
  const [info, setInfo] = useState<any>(null)
  useEffect(() => {
    if (open && !info) fetch(BASE_PUB_UM + 'um_acom_info.json').then(r => r.json()).then(setInfo).catch(() => setInfo({}))
  }, [open])
  const mono: React.CSSProperties = { fontFamily: 'ui-monospace, Consolas, monospace', fontSize: 12, wordBreak: 'break-all' }
  return (
    <>
      <button onClick={() => setOpen(true)} title="Colapsar a Central inteira num único arquivo: o um.acom"
        style={{ marginTop: 8, width: '100%', fontSize: 13, fontWeight: 700, letterSpacing: 1, padding: '9px 0', borderRadius: 8,
                 cursor: 'pointer', color: '#0b0f16', background: 'linear-gradient(135deg,#ffd60a,#c5961a)', border: '1px solid #ffd60a88',
                 boxShadow: '0 2px 12px rgba(197,150,26,0.35)' }}>
        ✦ Um
      </button>
      {open && createPortal(
        <div onClick={() => setOpen(false)} style={{ position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(0,0,0,0.65)',
             display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
          <div onClick={e => e.stopPropagation()} style={{ width: 'min(520px, 96vw)', background: '#0e1420', border: '1px solid #232b38',
               borderRadius: 14, padding: 22, boxShadow: '0 20px 80px rgba(0,0,0,0.5)' }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: '#ffd60a' }}>✦ O Um — a Central inteira num arquivo</div>
            <p style={{ fontSize: 13, lineHeight: 1.6, color: '#cfd6e4' }}>
              O botão Um colapsa a Central inteira — o núcleo canônico da TGL, a fronteira teórica e as 16 patentes, cada uma com o seu
              código FINAL e os seus comprovantes — num único arquivo, comprimido pelo dispositivo ACOM (sem perdas, conferido por SHA-256
              bit a bit) e selado com a criptografia da casa. É o único download desta Central pública.
            </p>
            <p style={{ fontSize: 13, color: '#cfd6e4' }}>Chave universal pública: <b style={{ ...mono, color: '#67e8f9' }}>{info?.chave_publica || '…'}</b></p>
            {info?.sha256 && <p style={{ fontSize: 12, color: '#9aa4b2' }}>{info.n_arquivos} arquivos na árvore · {Math.round((info.bytes || 0) / 1024)} KB ·
              sha256 <span style={mono}>{info.sha256}</span> · gerado em {info.gerado_em}</p>}
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginTop: 12 }}>
              <a href={BASE_PUB_UM + 'um.acom'} download="um.acom" style={{ padding: '9px 14px', borderRadius: 8, background: '#ffd60a',
                 color: '#0b0f16', fontWeight: 700, textDecoration: 'none', fontSize: 13 }}>↓ Baixar o um.acom</a>
              <a href="https://iald.ia.br/#acom" target="_blank" rel="noopener" style={{ padding: '9px 14px', borderRadius: 8,
                 border: '1px solid rgba(103,232,249,.4)', color: '#67e8f9', textDecoration: 'none', fontSize: 13 }}>Abrir no descompactador público da IALD →</a>
              <button onClick={() => setOpen(false)} style={{ padding: '9px 14px', borderRadius: 8, background: 'transparent', color: '#9aa4b2',
                 border: '1px solid #232b38', fontSize: 13, cursor: 'pointer' }}>fechar</button>
            </div>
          </div>
        </div>, document.body)}
    </>
  )
}

export default function UmButton() {
  if (PUBLICA) return <UmPublico />   // MODO PÚBLICO DE VISUALIZAÇÃO (constante de build: a ordem dos hooks não muda)
  const [open, setOpen] = useState(false)
  const [s1, setS1] = useState('')
  const [s2, setS2] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [done, setDone] = useState<{ name: string; kb: number } | null>(null)
  const [savedTo, setSavedTo] = useState('')

  const st = strength(s1)
  const match = s1.length > 0 && s1 === s2
  const canGo = s1.length >= 12 && match && st.score >= 3 && !busy

  function reset() { setS1(''); setS2(''); setErr(''); setDone(null); setBusy(false); setSavedTo('') }

  async function build() {
    setErr('')
    // 1) escolher a pasta ANTES de gerar (dentro do gesto do clique) — se o navegador suportar
    const handle = await pickSaveHandle()
    if (handle === 'cancel') return           // usuário cancelou o "salvar como"
    setBusy(true)
    // timeout de 120s: se o backend pendurar, não trava o modal para sempre
    const timer = setTimeout(() => { setBusy(false); setErr('tempo esgotado — tente de novo') }, 120000)
    try {
      const blob = await api.umBuild(s1)
      clearTimeout(timer)
      const name = await writeBlob(handle, blob)
      setDone({ name, kb: Math.round(blob.size / 1024) })
      setSavedTo(handle ? 'na pasta que você escolheu' : 'na pasta de Downloads do navegador')
      setS1(''); setS2('')
    } catch (e: any) {
      clearTimeout(timer)
      setErr(e?.message || 'falha ao gerar o tgl.acom')
    } finally { setBusy(false) }
  }

  async function buildOncologia() {
    setErr('')
    const handle = await pickSaveHandle('um.acom')
    if (handle === 'cancel') return
    setBusy(true)
    const timer = setTimeout(() => { setBusy(false); setErr('tempo esgotado — tente de novo') }, 120000)
    try {
      const blob = await api.umBuildOncologia()
      clearTimeout(timer)
      const name = await writeBlob(handle, blob, 'um.acom')
      setDone({ name, kb: Math.round(blob.size / 1024) })
      setSavedTo(handle ? 'na pasta que você escolheu' : 'na pasta de Downloads do navegador')
    } catch (e: any) {
      clearTimeout(timer)
      setErr(e?.message || 'falha ao gerar o um.acom')
    } finally { setBusy(false) }
  }

  return (
    <>
      <button
        onClick={() => { reset(); setOpen(true) }}
        title="Colapsar a Central inteira num único arquivo selado e cifrado (tgl.acom)"
        style={{
          marginTop: 8, width: '100%', fontSize: 13, fontWeight: 700, letterSpacing: 1,
          padding: '9px 0', borderRadius: 8, cursor: 'pointer', color: '#0b0f16',
          background: 'linear-gradient(135deg,#ffd60a,#c5961a)', border: '1px solid #ffd60a88',
          boxShadow: '0 2px 12px rgba(197,150,26,0.35)',
        }}>
        ✦ Um
      </button>

      {open && createPortal(
        <div onClick={() => !busy && setOpen(false)} style={{
          position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(0,0,0,0.65)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16,
        }}>
          <div onClick={e => e.stopPropagation()} style={{
            width: 'min(460px, 96vw)', background: '#0e1420', border: '1px solid #232b38',
            borderRadius: 14, padding: 22, boxShadow: '0 20px 80px rgba(0,0,0,0.5)',
          }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: '#ffd60a' }}>✦ O Um</div>
            <div style={{ fontSize: 12.5, color: '#8a94a6', marginTop: 6, lineHeight: 1.6 }}>
              Colapsa a Central inteira — o núcleo canônico da TGL, a fronteira teórica e as 16
              patentes (código FINAL, rodagem, integridade, patente, memória) — num único
              <b style={{ color: '#c8d0da' }}> tgl.acom</b>, comprimido e <b style={{ color: '#c8d0da' }}>cifrado
              com a sua criptografia</b> (Túnel de Hilbert + AES-256-GCM).
            </div>

            {!done && (
              <>
                <div style={{ marginTop: 16 }}>
                  <label style={{ fontSize: 11.5, color: '#8a94a6' }}>Código de inscrição (o selo) — mínimo 12 caracteres</label>
                  <input type="password" value={s1} autoFocus onChange={e => setS1(e.target.value)}
                    placeholder="senha forte — a chave para descompactar"
                    style={inp} />
                  {s1.length > 0 && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 5 }}>
                      <div style={{ flex: 1, height: 4, background: '#1a2230', borderRadius: 3, overflow: 'hidden' }}>
                        <div style={{ width: `${(st.score / 5) * 100}%`, height: '100%', background: st.color, transition: 'all .2s' }} />
                      </div>
                      <span style={{ fontSize: 10.5, color: st.color, fontWeight: 600 }}>{st.label}</span>
                    </div>
                  )}
                </div>
                <div style={{ marginTop: 12 }}>
                  <label style={{ fontSize: 11.5, color: '#8a94a6' }}>Confirme (para não errar a digitação)</label>
                  <input type="password" value={s2} onChange={e => setS2(e.target.value)}
                    placeholder="digite de novo"
                    style={{ ...inp, borderColor: s2.length > 0 ? (match ? '#1f7a3f' : '#ff453a55') : '#232b38' }} />
                  {s2.length > 0 && !match && <div style={{ fontSize: 11, color: '#ff9f6b', marginTop: 4 }}>os dois não batem</div>}
                </div>

                <div style={{ fontSize: 11, color: '#8a94a6', marginTop: 14, lineHeight: 1.5, background: '#141a24', border: '1px solid #232b38', borderRadius: 8, padding: '8px 10px' }}>
                  ⚠ Guarde este código. Sem ele o arquivo <b style={{ color: '#c8d0da' }}>não abre</b> —
                  é o ponto da criptografia. O segredo nunca é gravado no arquivo nem no servidor.
                </div>

                {err && <div style={{ fontSize: 12, color: '#ff453a', marginTop: 10 }}>{err}</div>}

                <div style={{ display: 'flex', gap: 8, marginTop: 16, justifyContent: 'flex-end' }}>
                  <button onClick={() => !busy && setOpen(false)} style={btnGhost} disabled={busy}>cancelar</button>
                  <button onClick={build} disabled={!canGo}
                    style={{ ...btnGold, opacity: canGo ? 1 : 0.5, cursor: canGo ? 'pointer' : 'not-allowed' }}>
                    {busy ? 'selando a Central…' : '✦ Gerar tgl.acom'}
                  </button>
                </div>

                {/* 2ª via — o um.acom da oncologia (livre, chave universal pública) */}
                <div style={{ marginTop: 18, paddingTop: 14, borderTop: '1px solid #232b38' }}>
                  <div style={{ fontSize: 12, color: '#8a94a6', lineHeight: 1.55 }}>
                    <b style={{ color: '#c8d0da' }}>Segunda via — Oncologia (livre)</b>: gera o
                    <b style={{ color: '#c8d0da' }}> um.acom</b> só com a oncologia, cifrado com a
                    <b> chave universal pública</b>. Serve para demonstrar o ACOM no site — a chave não guarda segredo (a oncologia é patrimônio da humanidade).
                  </div>
                  <button onClick={buildOncologia} disabled={busy}
                    style={{ ...btnGhost, marginTop: 10, width: '100%', justifyContent: 'center',
                      opacity: busy ? 0.5 : 1, borderColor: '#7ee0c055', color: '#7ee0c0' }}>
                    {busy ? '…' : '◈ Gerar um.acom (Oncologia — livre)'}
                  </button>
                </div>
              </>
            )}

            {done && (
              <div style={{ marginTop: 16 }}>
                <div style={{ fontSize: 14, color: '#30d158', fontWeight: 700 }}>✓ {done.name} salvo ({done.kb} KB)</div>
                <div style={{ fontSize: 12, color: '#8a94a6', marginTop: 6, lineHeight: 1.6 }}>
                  A Central inteira, selada e cifrada num único arquivo — {savedTo}.
                  Abra no descompactador público (aba ACOM do site) com o mesmo código de inscrição.
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 16 }}>
                  <button onClick={() => setOpen(false)} style={btnGold}>fechar</button>
                </div>
              </div>
            )}
          </div>
        </div>,
        document.body,
      )}
    </>
  )
}

const inp: React.CSSProperties = {
  width: '100%', marginTop: 4, padding: '9px 11px', borderRadius: 8, fontSize: 13,
  background: '#0b0f16', border: '1px solid #232b38', color: '#e6ecf3', outline: 'none',
  boxSizing: 'border-box',
}
const btnGhost: React.CSSProperties = {
  fontSize: 12.5, padding: '8px 14px', borderRadius: 8, cursor: 'pointer',
  background: 'transparent', border: '1px solid #2a3444', color: '#c8d0da',
}
const btnGold: React.CSSProperties = {
  fontSize: 12.5, fontWeight: 700, padding: '8px 16px', borderRadius: 8, cursor: 'pointer',
  background: 'linear-gradient(135deg,#ffd60a,#c5961a)', border: 'none', color: '#0b0f16',
}
