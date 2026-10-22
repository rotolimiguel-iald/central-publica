import { useEffect, useState } from 'react'
import { api } from '../api'
import { useMe, isAdmin, ROLE_LABEL } from '../auth'

export default function Users() {
  const me = useMe()
  const [data, setData] = useState<any>(null)
  const [name, setName] = useState('')
  const [role, setRole] = useState('viewer')
  const [email, setEmail] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [newKey, setNewKey] = useState<{ name: string; key: string } | null>(null)

  const load = () => api.users().then(setData).catch(() => setData({ enabled: false, users: [] }))
  useEffect(() => { load() }, [])
  const twofa = data?.email_2fa

  if (me && !isAdmin(me)) {
    return (
      <div className="panel">
        <h4>Usuários</h4>
        <p className="muted">Esta área é exclusiva do administrador. Seu acesso é
          <b> {ROLE_LABEL[me.role] || me.role}</b>.</p>
      </div>
    )
  }
  if (!data) return <div className="muted">carregando…</div>
  if (!data.enabled) {
    return (
      <div className="panel">
        <h4>Usuários</h4>
        <p className="muted">O controle de usuários só funciona com a autenticação por criptografia
          ligada (na nuvem). Localmente em casa a Central roda sem login.</p>
      </div>
    )
  }

  async function add(e: React.FormEvent) {
    e.preventDefault(); if (!name.trim()) return
    if (twofa && role === 'editor' && !email.includes('@')) {
      setErr('Editor precisa de e-mail (para a verificação em duas etapas).'); return
    }
    setBusy(true); setErr(''); setNewKey(null)
    try {
      const r = await api.userAdd(name.trim(), role, email.trim())
      setNewKey({ name: r.name, key: r.key })
      setName(''); setEmail('')
      await load()
    } catch (e: any) {
      setErr(String(e.message).includes('400') ? 'Nome já existe, ou editor sem e-mail válido.' : 'Falha ao criar.')
    }
    setBusy(false)
  }

  return (
    <>
      <div className="h1">Usuários & Acessos</div>
      <div className="sub">Cadastre quem pode entrar e com qual permissão. Cada pessoa recebe uma
        <b> chave própria</b> (o login pela sua criptografia). Você pode revogar quando quiser.</div>

      <div className="panel">
        <h4 style={{ marginTop: 0 }}>Cadastrar novo acesso</h4>
        <form onSubmit={add} style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
          <input className="txt" placeholder="nome (ex.: Esposa)" value={name}
            onChange={e => setName(e.target.value)} style={{ flex: '1 1 160px' }} />
          <input className="txt" type="email" value={email}
            placeholder={twofa ? 'e-mail (obrigatório p/ editor)' : 'e-mail (opcional)'}
            onChange={e => setEmail(e.target.value)} style={{ flex: '1 1 200px' }} />
          <select className="txt" value={role} onChange={e => setRole(e.target.value)}>
            <option value="viewer">somente leitura</option>
            <option value="editor">editor (pode alterar)</option>
          </select>
          <button className="btn" disabled={busy || !name.trim()}>{busy ? 'criando…' : 'Criar acesso'}</button>
        </form>
        {twofa && <p className="muted" style={{ fontSize: 11.5, marginTop: 8 }}>
          🔐 Verificação em duas etapas <b>ligada</b>: quem for <b>editor</b> recebe também um código
          por e-mail a cada login. {!data.smtp_ready && <span className="legal-note">⚠️ envio de e-mail
            ainda não configurado no servidor (CENTRAL_SMTP_*).</span>}
        </p>}
        {err && <div className="device-err" style={{ marginTop: 10 }}>{err}</div>}
        {newKey && (
          <div className="key-reveal">
            <div className="key-reveal-h">✓ Acesso criado para <b>{newKey.name}</b> — copie a chave e entregue a ela:</div>
            <div className="key-box">
              <code>{newKey.key}</code>
              <button className="btn xs" onClick={() => navigator.clipboard?.writeText(newKey.key)}>copiar</button>
            </div>
            <div className="key-note">⚠️ Esta chave só aparece <b>agora</b>. Ela usa a chave para entrar
              (mesma tela de login). Se perder, é só criar um novo acesso.</div>
          </div>
        )}
      </div>

      <div className="panel">
        <h4 style={{ marginTop: 0 }}>Acessos ativos</h4>
        <table className="table">
          <thead><tr><th>Nome</th><th>E-mail</th><th>Permissão</th><th></th></tr></thead>
          <tbody>
            {data.users.map((u: any) => (
              <tr key={u.uid}>
                <td>{u.name} {u.builtin && <span className="muted">(você · admin)</span>}</td>
                <td className="muted" style={{ fontSize: 12 }}>{u.email || '—'}</td>
                <td>
                  {u.builtin ? <b>administrador</b> : (
                    <select className="txt" value={u.role} style={{ padding: '4px 8px', fontSize: 12 }}
                      onChange={async e => { await api.userRole(u.uid, e.target.value); load() }}>
                      <option value="viewer">somente leitura</option>
                      <option value="editor">editor (pode alterar)</option>
                    </select>
                  )}
                </td>
                <td style={{ textAlign: 'right' }}>
                  {!u.builtin && (
                    <button className="btn ghost xs" style={{ color: '#ff6b6b' }}
                      onClick={async () => { if (confirm(`Revogar o acesso de ${u.name}?`)) { await api.userRemove(u.uid); load() } }}>
                      revogar
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="legal-note" style={{ marginTop: 12 }}>
          <b>somente leitura</b>: vê tudo, não altera nada. <b>editor</b>: pode alterar conteúdo
          (notas, reindexar). <b>administrador</b> (você): tudo + gerencia usuários. Todas as chaves
          entram pela sua criptografia (Túnel de Hilbert); a chave de sessão nunca é transmitida.
        </p>
      </div>
    </>
  )
}
