import { useEffect, useState } from 'react'

// Store leve do usuário logado (papel/nome). Preenchido pelo Gate após o login.
export interface Me { role: string; name: string; uid?: string }

let _me: Me | null = null
const listeners = new Set<() => void>()

export function setMe(m: Me | null) { _me = m; listeners.forEach(l => l()) }
export function getMe(): Me | null { return _me }

export function useMe(): Me | null {
  const [, force] = useState(0)
  useEffect(() => {
    const l = () => force(x => x + 1)
    listeners.add(l)
    return () => { listeners.delete(l) }
  }, [])
  return _me
}

export const isAdmin = (m?: Me | null) => (m ?? _me)?.role === 'admin'
export const canEdit = (m?: Me | null) => {
  const r = (m ?? _me)?.role
  return r === 'admin' || r === 'editor'
}
export const ROLE_LABEL: Record<string, string> = {
  admin: 'administrador', editor: 'editor', viewer: 'somente leitura',
}
