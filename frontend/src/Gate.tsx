import { useEffect, useState } from 'react'
import { api } from './api'
import { setMe } from './auth'

/** Portão de autenticação pela criptografia do operador (ACOM Crypto — Túnel de Hilbert).
 *  Se a auth está ligada e você não está autenticado, mostra o login. Senão, deixa passar. */
export default function Gate({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<'loading' | 'in' | 'login'>('loading')
  const [beta, setBeta] = useState<any>(null)

  const loadMe = async () => {
    try { const m = await api.me(); setMe({ role: m.role, name: m.name, uid: m.uid }) } catch { /* */ }
  }
  const check = () =>
    api.authStatus()
      .then(async s => {
        setBeta(s.beta)
        if (s.authenticated) { await loadMe(); setState('in') } else setState('login')
      })
      .catch(async () => { await loadMe(); setState('in') })   // backend antigo: não bloqueia

  useEffect(() => { check() }, [])

  if (state === 'loading') return <div className="gate-loading">carregando…</div>
  if (state === 'in') return <>{children}</>
  return <LoginScreen beta={beta} onIn={() => { loadMe(); setState('in') }} />
}

function LoginScreen({ beta, onIn }: { beta: any; onIn: () => void }) {
  const [secret, setSecret] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [twofa, setTwofa] = useState<{ challenge: string; email_hint: string } | null>(null)
  const [code, setCode] = useState('')

  function fail(e: any, fallback: string) {
    const msg = String(e.message || '')
    setErr(msg.includes('401') ? fallback
      : msg.includes('429') ? 'Muitas tentativas. Aguarde alguns minutos.'
      : msg.includes('503') || msg.includes('502') ? 'Falha ao enviar o e-mail do código. Tente de novo.'
      : 'Falha ao entrar. Tente de novo.')
  }

  async function enter(e: React.FormEvent) {
    e.preventDefault()
    if (!secret) return
    setBusy(true); setErr('')
    try {
      const r = await api.authLogin(secret)
      if (r.twofa_required && r.challenge) {
        setTwofa({ challenge: r.challenge, email_hint: r.email_hint || 'seu e-mail' })
        setSecret('')
      } else { onIn() }
    } catch (e: any) { fail(e, 'Segredo incorreto — acesso negado.') }
    setBusy(false)
  }

  async function submitCode(e: React.FormEvent) {
    e.preventDefault()
    if (!code || !twofa) return
    setBusy(true); setErr('')
    try { await api.auth2fa(twofa.challenge, code.trim()); onIn() }
    catch (e: any) { fail(e, 'Código inválido ou expirado.') }
    setBusy(false)
  }

  return (
    <div className="login-wrap">
      {!twofa ? (
        <form className="login-card" onSubmit={enter}>
          <div className="login-brand">CENTRAL DE PATENTES</div>
          <div className="login-sub">TGL · IALD Ltda. · forma = conteúdo</div>
          <div className="login-lock">🔒</div>
          <div className="login-scheme">
            Segurança: <b>sua própria criptografia</b> — ACOM Crypto (Túnel de Hilbert)
          </div>
          <input className="login-input" type="password" autoFocus
            placeholder="seu segredo (frase-chave)" value={secret}
            onChange={e => setSecret(e.target.value)} disabled={busy} />
          <button className="login-btn" type="submit" disabled={busy || !secret}>
            {busy ? 'verificando pelo Túnel de Hilbert…' : 'Entrar'}
          </button>
          {err && <div className="login-err">{err}</div>}
          <div className="login-note">
            Seu segredo prova quem você é pelo <b>seu</b> chaveamento — a chave de sessão
            nunca é transmitida. Funciona em qualquer dispositivo seu.
          </div>
          {beta && <div className="login-beta">β = α·√e = {beta.beta_tgl?.toFixed(9)}</div>}
        </form>
      ) : (
        <form className="login-card" onSubmit={submitCode}>
          <div className="login-brand">CENTRAL DE PATENTES</div>
          <div className="login-lock">📧</div>
          <div className="login-scheme">
            <b>Verificação em duas etapas</b> — enviamos um código para <b>{twofa.email_hint}</b>
          </div>
          <input className="login-input" type="text" autoFocus inputMode="numeric"
            placeholder="código de 6 dígitos" value={code} maxLength={6}
            onChange={e => setCode(e.target.value.replace(/\D/g, ''))} disabled={busy}
            style={{ textAlign: 'center', letterSpacing: 6, fontSize: 20 }} />
          <button className="login-btn" type="submit" disabled={busy || code.length < 6}>
            {busy ? 'verificando…' : 'Confirmar código'}
          </button>
          {err && <div className="login-err">{err}</div>}
          <button type="button" className="login-back"
            onClick={() => { setTwofa(null); setCode(''); setErr('') }}>← voltar</button>
          <div className="login-note">
            O código expira em 10 minutos. Não recebeu? Volte e entre de novo para reenviar.
          </div>
        </form>
      )}
    </div>
  )
}
