import { useEffect, useRef } from 'react'
import OpenSeadragon from 'openseadragon'

// Deep-zoom viewer for a single image (the "Tony Stark" ampliable drawing).
// Uses OSD's { type: 'image' } tile source — no tiling pipeline needed; scroll/drag
// to zoom and pan into the technical detail.
export default function DeepZoom({ url, height = 520 }: { url: string; height?: number }) {
  const ref = useRef<HTMLDivElement>(null)
  const viewerRef = useRef<any>(null)

  useEffect(() => {
    if (!ref.current) return
    const viewer = OpenSeadragon({
      element: ref.current,
      tileSources: { type: 'image', url },
      showNavigationControl: false,
      showNavigator: true,
      navigatorPosition: 'BOTTOM_RIGHT',
      navigatorHeight: '60px',
      navigatorWidth: '90px',
      gestureSettingsMouse: { scrollToZoom: true, clickToZoom: false, dblClickToZoom: true },
      minZoomImageRatio: 0.6,
      maxZoomPixelRatio: 5,
      visibilityRatio: 1,
    })
    viewerRef.current = viewer
    return () => { viewer.destroy(); viewerRef.current = null }
  }, [url])

  return (
    <div style={{ position: 'relative' }}>
      <div ref={ref} style={{ width: '100%', height, background: '#0d141d',
        border: '1px solid var(--line)', borderRadius: 10 }} />
      <div style={{ position: 'absolute', top: 8, left: 10, fontSize: 11, color: 'var(--muted)',
        background: 'rgba(10,14,20,.7)', padding: '2px 8px', borderRadius: 6 }}>
        role/scroll para ampliar · arraste para navegar
      </div>
    </div>
  )
}
