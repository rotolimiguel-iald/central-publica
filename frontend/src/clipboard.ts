/** Copia texto sem gravar nada no servidor. Usa a API moderna e um fallback local. */
export async function copiarTexto(valor: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(valor)
      return
    } catch {
      // Permissão negada ou contexto inseguro: tenta o fallback local abaixo.
    }
  }
  const area = document.createElement('textarea')
  area.value = valor
  area.setAttribute('readonly', '')
  area.style.position = 'fixed'
  area.style.left = '-9999px'
  area.style.opacity = '0'
  document.body.appendChild(area)
  area.select()
  area.setSelectionRange(0, area.value.length)
  const copiado = document.execCommand('copy')
  area.remove()
  if (!copiado) throw new Error('O navegador recusou a cópia.')
}
