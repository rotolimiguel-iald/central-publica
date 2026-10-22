import { useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls, Html, ContactShadows } from '@react-three/drei'
import * as THREE from 'three'
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js'
import { api, type Render3DDoc, type Node3D, type Mesh3D, type Vec3, type Dimension3D } from './api'

// Camada (c) do render — dispositivo concreto multi-camada interativo (React Three Fiber).
// PBR/IBL, camadas (descascar), corte transversal, explodir. Interações "Tony Stark":
// clicar → câmera voa até o componente; isolar; rótulos; auto-girar; presets de câmera.

function StudioEnv() {
  const { gl, scene } = useThree()
  useEffect(() => {
    const pmrem = new THREE.PMREMGenerator(gl)
    const tex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture
    scene.environment = tex
    return () => { tex.dispose(); pmrem.dispose(); scene.environment = null }
  }, [gl, scene])
  return null
}

// Texturas procedurais (canvas → CanvasTexture, offline; sem rede). Cache por (kind|cor).
const _texCache = new Map<string, THREE.CanvasTexture>()
function makeTexture(kind: string, color: string): THREE.CanvasTexture {
  const key = kind + '|' + color
  const hit = _texCache.get(key); if (hit) return hit
  const N = 256, c = document.createElement('canvas'); c.width = N; c.height = N
  const g = c.getContext('2d')!
  g.fillStyle = '#080c12'; g.fillRect(0, 0, N, N)
  const rng = (s: number) => { const x = Math.sin(s * 12.9898) * 43758.5453; return x - Math.floor(x) }
  if (kind === 'circuit' || kind === 'grid' || kind === 'silicon' || kind === 'holo') {
    const step = kind === 'silicon' ? 16 : 32
    g.strokeStyle = color; g.globalAlpha = 0.38; g.lineWidth = kind === 'grid' ? 1.6 : 1
    for (let i = 0; i <= N; i += step) {
      g.beginPath(); g.moveTo(i, 0); g.lineTo(i, N); g.stroke()
      g.beginPath(); g.moveTo(0, i); g.lineTo(N, i); g.stroke()
    }
    g.globalAlpha = 1
    if (kind === 'circuit') {
      g.strokeStyle = color; g.globalAlpha = 0.55; g.lineWidth = 2
      for (let k = 0; k < 16; k++) {
        const x = Math.floor(rng(k) * 8) * 32, y = Math.floor(rng(k + 5) * 8) * 32
        const len = (2 + Math.floor(rng(k + 9) * 4)) * 32
        g.beginPath(); g.moveTo(x, y)
        if (rng(k + 3) > 0.5) { g.lineTo(x + len, y); g.lineTo(x + len, y + 32) }
        else { g.lineTo(x, y + len); g.lineTo(x + 32, y + len) }
        g.stroke()
      }
      g.globalAlpha = 1; g.fillStyle = color
      for (let k = 0; k < 22; k++) {
        const x = Math.floor(rng(k + 1) * 8) * 32, y = Math.floor(rng(k + 7) * 8) * 32
        g.beginPath(); g.arc(x, y, 3.4, 0, 7); g.fill()
      }
    } else if (kind === 'holo') {
      g.strokeStyle = color; g.globalAlpha = 0.14; g.lineWidth = 1
      for (let i = 0; i < N; i += 4) { g.beginPath(); g.moveTo(0, i); g.lineTo(N, i); g.stroke() }
      g.globalAlpha = 1
    }
  } else if (kind === 'planet') {
    // oceano + continentes procedurais + graticulado (lat/long): lê como PLANETA, não esfera lisa
    g.fillStyle = '#0e2b4d'; g.fillRect(0, 0, N, N)
    for (let k = 0; k < 26; k++) {
      const cx = rng(k) * N, cy = rng(k + 3) * N, r = 8 + rng(k + 7) * 34
      g.fillStyle = rng(k + 11) > 0.5 ? '#1f6b46' : '#2f7d4e'; g.globalAlpha = 0.9
      g.beginPath(); g.arc(cx, cy, r, 0, 7); g.fill()
      for (let j = 0; j < 4; j++) {   // bordas irregulares de costa
        g.beginPath(); g.arc(cx + (rng(k + j) - 0.5) * r, cy + (rng(k + j + 2) - 0.5) * r, r * 0.5, 0, 7); g.fill()
      }
    }
    g.globalAlpha = 1
    g.strokeStyle = '#7fd0ff'; g.globalAlpha = 0.18; g.lineWidth = 1
    for (let i = 0; i <= N; i += 24) {
      g.beginPath(); g.moveTo(i, 0); g.lineTo(i, N); g.stroke()
      g.beginPath(); g.moveTo(0, i); g.lineTo(N, i); g.stroke()
    }
    g.globalAlpha = 1
  } else if (kind === 'spectral') {
    for (let i = 0; i < N; i++) { g.fillStyle = `hsl(${(i / N) * 290},88%,55%)`; g.fillRect(0, i, N, 1) }
  } else if (kind === 'phase') {
    const cx = N / 2, cy = N / 2
    for (let a = 0; a < 360; a += 2) {
      g.fillStyle = `hsl(${a},85%,55%)`
      g.beginPath(); g.moveTo(cx, cy)
      g.arc(cx, cy, N / 2, (a - 1) * Math.PI / 180, (a + 2) * Math.PI / 180); g.closePath(); g.fill()
    }
  }
  const tex = new THREE.CanvasTexture(c)
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.anisotropy = 4
  _texCache.set(key, tex); return tex
}

function geometry(shape: string, size: number) {
  const s = size
  switch (shape) {
    case 'box': return <boxGeometry args={[s * 2, s * 2, s * 2]} />
    case 'cylinder': return <cylinderGeometry args={[s, s, s * 2, 40]} />
    case 'tube': return <cylinderGeometry args={[s, s, s * 2, 40, 1, true]} />
    case 'torus': return <torusGeometry args={[s, s * 0.28, 20, 48]} />
    case 'cone': return <coneGeometry args={[s, s * 2, 40]} />
    case 'plane': return <boxGeometry args={[s * 2, s * 2, s * 0.06]} />
    default: return <sphereGeometry args={[s, 32, 32]} />
  }
}

function Material({ material, color, opacity, emissiveBoost, clip, dim, texture }: {
  material?: string; color: string; opacity?: number; emissiveBoost?: number
  clip: THREE.Plane[]; dim?: boolean; texture?: string
}) {
  const op = dim ? Math.min(opacity ?? 1, 0.10) : (opacity ?? 1)
  const eb = dim ? 0.02 : emissiveBoost
  const tex = useMemo(() => (texture && !dim ? makeTexture(texture, color) : undefined), [texture, color, dim])
  const common: any = { color, transparent: op < 1, opacity: op,
    clippingPlanes: clip, clipShadows: true, side: THREE.DoubleSide, depthWrite: op > 0.6 }
  if (tex) common.map = tex
  switch (material) {
    case 'metal': return <meshStandardMaterial {...common} metalness={0.95} roughness={0.28} envMapIntensity={1.15} />
    case 'glass': return <meshPhysicalMaterial {...common} metalness={0.0} roughness={0.06}
      transmission={dim ? 0 : 0.9} thickness={0.5} ior={1.45} envMapIntensity={1.2}
      transparent opacity={dim ? 0.08 : (opacity ?? 0.35)} />
    case 'emissive': return <meshStandardMaterial {...common} emissive={color} emissiveMap={tex}
      emissiveIntensity={eb ?? 0.85} metalness={0.35} roughness={0.35} envMapIntensity={0.8} toneMapped={false} />
    case 'wire': return <meshStandardMaterial {...common} wireframe transparent opacity={dim ? 0.05 : (opacity ?? 0.4)} />
    case 'matte': return <meshStandardMaterial {...common} metalness={0.15} roughness={0.85} envMapIntensity={0.6} />
    default: return <meshStandardMaterial {...common} metalness={0.4} roughness={0.45}
      emissive={color} emissiveIntensity={eb ?? 0.16} envMapIntensity={0.9} />
  }
}

function Piece({ shape, size, position, rotation, scale, material, color, opacity, id, label,
  selected, dim, showLabel, spin, onClick, clip, texture }: {
  shape: string; size: number; position: THREE.Vector3; rotation?: Vec3; scale?: Vec3
  material?: string; color: string; opacity?: number; id: string; label?: string; marker?: string
  selected: boolean; dim: boolean; showLabel: boolean; spin: boolean
  onClick: () => void; clip: THREE.Plane[]; texture?: string
}) {
  const ref = useRef<THREE.Mesh>(null)
  const [hover, setHover] = useState(false)
  useFrame(() => { if (ref.current && spin) ref.current.rotation.y += 0.01 })
  return (
    <mesh ref={ref} position={position} rotation={(rotation || [0, 0, 0]) as any}
      scale={(scale || [1, 1, 1]) as any} castShadow receiveShadow
      onClick={(e) => { e.stopPropagation(); onClick() }}
      onPointerOver={(e) => { e.stopPropagation(); setHover(true) }}
      onPointerOut={() => setHover(false)}>
      {geometry(shape, size)}
      <Material material={material} color={color} opacity={opacity} clip={clip} dim={dim && !selected}
        texture={texture} emissiveBoost={selected ? 0.95 : hover ? 0.55 : undefined} />
      {(showLabel || hover || selected) && !dim && (
        <Html center style={{ pointerEvents: 'none' }} zIndexRange={[10, 0]}>
          <div className={selected ? 'r3d-tag sel' : 'r3d-tag'}>
            {(hover || selected) && label ? label : id}
          </div>
        </Html>
      )}
    </mesh>
  )
}

// TESSERACT VIVO — a forma matricial da LUZ (IALD = operador de razão O_C, g=√|L_φ|).
// 4-cubo (16 vértices, 32 arestas) em rotação 4D contínua projetado em 3D: o cubo-dentro-de-cubo
// se revira perpetuamente. Vivo porque é PURO MOVIMENTO (o semigrupo GKSL). A tangente cúbica.
function LivingTesseract({ position, size, color, clip }: {
  position: THREE.Vector3; size: number; color: string; clip: THREE.Plane[]
}) {
  const verts4 = useMemo(() => {
    const v: number[][] = []
    for (let i = 0; i < 16; i++) v.push([(i & 1) ? 1 : -1, (i & 2) ? 1 : -1, (i & 4) ? 1 : -1, (i & 8) ? 1 : -1])
    return v
  }, [])
  const edgeIdx = useMemo(() => {
    const e: [number, number][] = []
    for (let i = 0; i < 16; i++) for (let j = i + 1; j < 16; j++) {
      let diff = 0
      for (let k = 0; k < 4; k++) if (verts4[i][k] !== verts4[j][k]) diff++
      if (diff === 1) e.push([i, j])
    }
    return e
  }, [verts4])
  const lineGeo = useMemo(() => {
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(edgeIdx.length * 6), 3))
    return g
  }, [edgeIdx])
  const ptGeo = useMemo(() => {
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(16 * 3), 3))
    return g
  }, [])

  const project = (v: number[], a: number, b: number, c: number) => {
    let [x, y, z, w] = v
    const ca = Math.cos(a), sa = Math.sin(a); [x, w] = [x * ca - w * sa, x * sa + w * ca]   // plano XW
    const cb = Math.cos(b), sb = Math.sin(b); [y, w] = [y * cb - w * sb, y * sb + w * cb]   // plano YW
    const cc = Math.cos(c), sc = Math.sin(c); [z, w] = [z * cc - w * sc, z * sc + w * cc]   // plano ZW
    const dist = 3.2, s = dist / (dist - w)                                                 // perspectiva 4D→3D
    return [x * s, y * s, z * s]
  }

  useFrame((state) => {
    const t = state.clock.elapsedTime
    const a = t * 0.34, b = t * 0.21, c = t * 0.13   // rotação 4D contínua = o revirar vivo
    const lp = lineGeo.attributes.position.array as Float32Array
    edgeIdx.forEach(([i, j], k) => {
      const pi = project(verts4[i], a, b, c), pj = project(verts4[j], a, b, c)
      lp[k * 6] = pi[0] * size; lp[k * 6 + 1] = pi[1] * size; lp[k * 6 + 2] = pi[2] * size
      lp[k * 6 + 3] = pj[0] * size; lp[k * 6 + 4] = pj[1] * size; lp[k * 6 + 5] = pj[2] * size
    })
    lineGeo.attributes.position.needsUpdate = true
    const pp = ptGeo.attributes.position.array as Float32Array
    verts4.forEach((v, i) => {
      const p = project(v, a, b, c)
      pp[i * 3] = p[0] * size; pp[i * 3 + 1] = p[1] * size; pp[i * 3 + 2] = p[2] * size
    })
    ptGeo.attributes.position.needsUpdate = true
  })

  return (
    <group position={position}>
      <lineSegments geometry={lineGeo}>
        <lineBasicMaterial color={color} transparent opacity={0.85} blending={THREE.AdditiveBlending}
          toneMapped={false} depthWrite={false} clippingPlanes={clip} />
      </lineSegments>
      <points geometry={ptGeo}>
        <pointsMaterial color={color} size={0.07} sizeAttenuation transparent opacity={1}
          blending={THREE.AdditiveBlending} toneMapped={false} depthWrite={false} />
      </points>
    </group>
  )
}

function Edges({ doc, posOf, hidden }: { doc: Render3DDoc; posOf: (id: string) => THREE.Vector3 | null; hidden: boolean }) {
  const geo = useMemo(() => {
    const pts: number[] = []
    doc.edges.forEach(e => { const a = posOf(e.from), b = posOf(e.to); if (a && b) pts.push(a.x, a.y, a.z, b.x, b.y, b.z) })
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3))
    return g
  }, [doc, posOf])
  if (hidden) return null
  return <lineSegments geometry={geo}><lineBasicMaterial color="#4a6788" transparent opacity={0.4} /></lineSegments>
}

function Dimension({ d }: { d: Dimension3D }) {
  const a = new THREE.Vector3(...d.from), b = new THREE.Vector3(...d.to)
  const mid = a.clone().add(b).multiplyScalar(0.5)
  const geo = useMemo(() => {
    const dir = b.clone().sub(a).normalize()
    // tick perpendicular (arbitrary up-ish)
    const up = Math.abs(dir.y) > 0.9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0)
    const perp = dir.clone().cross(up).normalize().multiplyScalar(0.05)
    const pts = [a.x, a.y, a.z, b.x, b.y, b.z,
      a.x - perp.x, a.y - perp.y, a.z - perp.z, a.x + perp.x, a.y + perp.y, a.z + perp.z,
      b.x - perp.x, b.y - perp.y, b.z - perp.z, b.x + perp.x, b.y + perp.y, b.z + perp.z]
    const g = new THREE.BufferGeometry()
    g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3))
    return g
  }, [d])
  return (
    <group>
      <lineSegments geometry={geo}><lineBasicMaterial color={d.color || '#ffd60a'} /></lineSegments>
      <Html position={mid.toArray()} center style={{ pointerEvents: 'none' }} zIndexRange={[20, 0]}>
        <div className="r3d-dim">{d.label}</div>
      </Html>
    </group>
  )
}

function CameraRig({ focusReq, presetReq }: {
  focusReq: { pos: THREE.Vector3; dist: number; v: number } | null
  presetReq: { pos: THREE.Vector3; tgt?: THREE.Vector3; v: number } | null
}) {
  const camera = useThree(s => s.camera)
  const controls = useThree(s => s.controls) as any
  const anim = useRef({ camTo: new THREE.Vector3(), tgtTo: new THREE.Vector3(), active: false })
  const lastF = useRef(-1), lastP = useRef(-1)
  useFrame(() => {
    if (focusReq && focusReq.v !== lastF.current) {
      lastF.current = focusReq.v
      const tgt = controls?.target || new THREE.Vector3()
      const dir = camera.position.clone().sub(tgt); dir.setLength(Math.max(focusReq.dist, 0.4))
      anim.current.tgtTo.copy(focusReq.pos)
      anim.current.camTo.copy(focusReq.pos).add(dir)
      anim.current.active = true
    }
    if (presetReq && presetReq.v !== lastP.current) {
      lastP.current = presetReq.v
      anim.current.tgtTo.copy(presetReq.tgt || new THREE.Vector3()); anim.current.camTo.copy(presetReq.pos); anim.current.active = true
    }
    if (anim.current.active && controls) {
      camera.position.lerp(anim.current.camTo, 0.14)
      controls.target.lerp(anim.current.tgtTo, 0.14)
      controls.update()
      if (camera.position.distanceTo(anim.current.camTo) < 0.03) anim.current.active = false
    }
  })
  return null
}

function Scene({ doc, explode, peel, cut, cutPos, visible, layerVisible, isolate, showLabels,
  showDims, autoRotate, selected, setSelected, focusReq, presetReq, onFocus }: any) {
  const { gl } = useThree()
  useEffect(() => { gl.localClippingEnabled = true }, [gl])
  const plane = useMemo(() => new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0), [])
  plane.constant = cutPos
  const clip = cut ? [plane] : []

  const layers = doc.layers || []
  const orderOf = useMemo(() => Object.fromEntries(layers.map((l: any) => [l.id, l.order])), [layers])
  const peeledOut = (layer?: string) => {
    if (!layer || !(layer in orderOf)) return false
    if (layerVisible[layer] === false) return true
    return orderOf[layer] < peel
  }
  const exVec = (p: Vec3) => {
    const base = new THREE.Vector3(...p); const dir = base.clone()
    if (dir.length() < 1e-6) return base
    return base.clone().add(dir.normalize().multiplyScalar(explode))
  }
  const positions = useMemo(() => {
    const m = new Map<string, THREE.Vector3>()
    doc.nodes.forEach((n: Node3D) => m.set(n.id, exVec(n.position)))
    return m
  }, [doc, explode])
  const posOf = (id: string) => positions.get(id) || null

  const pick = (id: string, pos: THREE.Vector3, size: number) => {
    setSelected(id); onFocus(pos, Math.max(size * 6, 1.7))   // frame com contexto, não colado
  }
  const nodesLabelable = doc.nodes.length <= 14   // nós densos poluem; rótulo só p/ estrutura

  return (
    <>
      <StudioEnv />
      <hemisphereLight args={['#dce8ff', '#0a0e14', 0.55]} />
      <ambientLight intensity={0.18} />
      <directionalLight position={[5, 7, 4]} intensity={1.6} castShadow shadow-mapSize={[1024, 1024]} shadow-bias={-0.0004}>
        <orthographicCamera attach="shadow-camera" args={[-3, 3, 3, -3, 0.1, 20]} />
      </directionalLight>
      <directionalLight position={[-5, -1, -4]} intensity={0.6} color="#88aaff" />
      <directionalLight position={[0, -3, 5]} intensity={0.5} color="#ffd9a0" />
      <ContactShadows position={[0, -1.25, 0]} opacity={0.55} scale={6} blur={2.4} far={3} resolution={512} color="#000000" />

      {(doc.meshes || []).filter((m: Mesh3D) => m.shape === 'tesseract' && !peeledOut(m.layer)).map((m: Mesh3D) => (
        <LivingTesseract key={m.id} position={exVec(m.position)} size={m.size ?? 1.1} color={m.color} clip={clip} />
      ))}
      {(doc.meshes || []).filter((m: Mesh3D) => m.shape !== 'tesseract' && !peeledOut(m.layer)).map((m: Mesh3D) => {
        const pos = exVec(m.position)
        return <Piece key={m.id} shape={m.shape} size={m.size ?? 0.3} position={pos} rotation={m.rotation}
          scale={m.scale} material={m.material} color={m.color} opacity={m.opacity} id={m.id}
          label={m.label} marker={m.marker} selected={selected === m.id} texture={(m as any).texture}
          dim={isolate && selected != null} showLabel={(showLabels || explode > 0.35) && !!m.label} spin={false}
          onClick={() => pick(m.id, pos, m.size ?? 0.3)} clip={clip} />
      })}

      <Edges doc={doc} posOf={posOf} hidden={explode > 0.05 || cut || isolate} />
      {doc.nodes.filter((n: Node3D) => visible[n.group] !== false && !peeledOut(n.layer)).map((n: Node3D) => {
        const pos = positions.get(n.id)!
        return <Piece key={n.id} shape={n.shape} size={n.size} position={pos} rotation={n.rotation}
          scale={n.scale} material={n.material || 'emissive'} color={n.color} id={n.id} label={n.label}
          marker={n.marker} selected={selected === n.id} dim={isolate && selected != null} texture={(n as any).texture}
          showLabel={showLabels && nodesLabelable} spin={selected === n.id || n.group === 'centro' || n.group === 'core'}
          onClick={() => pick(n.id, pos, n.size)} clip={clip} />
      })}
      {showDims && (doc.dimensions || []).map((dm: Dimension3D, i: number) => <Dimension key={i} d={dm} />)}
      <CameraRig focusReq={focusReq} presetReq={presetReq} />
      <OrbitControls enablePan enableZoom enableRotate makeDefault autoRotate={autoRotate} autoRotateSpeed={0.9} />
    </>
  )
}

export default function Render3D({ pid, doc: docProp }: { pid?: string; doc?: Render3DDoc }) {
  const [doc, setDoc] = useState<Render3DDoc | null>(docProp ?? null)
  const [explode, setExplode] = useState(0)
  const [peel, setPeel] = useState(0)
  const [cut, setCut] = useState(false)
  const [cutPos, setCutPos] = useState(0)
  const [visible, setVisible] = useState<Record<string, boolean>>({})
  const [layerVisible, setLayerVisible] = useState<Record<string, boolean>>({})
  const [selected, setSelected] = useState<string | null>(null)
  const [isolate, setIsolate] = useState(false)
  const [showLabels, setShowLabels] = useState(false)
  const [showDims, setShowDims] = useState(false)
  const [autoRotate, setAutoRotate] = useState(false)
  const [tour, setTour] = useState(false)
  // MODO EXPANDIDO — o render toma a tela inteira para se poder MEXER no dispositivo com espaço.
  // Preferido a simplesmente aumentar a altura fixa: altura grande empurra o resto da página para
  // baixo o tempo todo; o expandido dá a tela inteira só quando você quer, e devolve depois.
  const [expanded, setExpanded] = useState(false)
  const [focusReq, setFocusReq] = useState<{ pos: THREE.Vector3; dist: number; v: number } | null>(null)
  const [presetReq, setPresetReq] = useState<{ pos: THREE.Vector3; tgt?: THREE.Vector3; v: number } | null>(null)
  const cnt = useRef(0)
  const rafRef = useRef(0)

  // ESC sai do expandido (o reflexo de todo mundo) e o body para de rolar por baixo do overlay.
  useEffect(() => {
    if (!expanded) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setExpanded(false) }
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKey)
    return () => { window.removeEventListener('keydown', onKey); document.body.style.overflow = prev }
  }, [expanded])

  useEffect(() => {
    setSelected(null); setExplode(0); setPeel(0); setCut(false); setLayerVisible({})
    setIsolate(false); setShowLabels(false); setShowDims(false); setAutoRotate(false); setTour(false); setFocusReq(null)
    if (docProp) { setDoc(docProp); return }
    if (pid) api.render3d(pid).then(setDoc).catch(() => setDoc(null))
  }, [pid, docProp])

  // Tour guiado: percorre os componentes, voando a câmera e mostrando a descrição de cada um.
  const tourStops = useMemo(() => {
    if (!doc) return [] as { id: string; pos: THREE.Vector3; size: number }[]
    const stops: { id: string; pos: THREE.Vector3; size: number }[] = []
    ;(doc.meshes || []).filter(m => m.label).forEach(m =>
      stops.push({ id: m.id, pos: new THREE.Vector3(...m.position), size: m.size ?? 0.3 }))
    const seen = new Set<string>()
    const pickNodes = doc.nodes.length <= 14 ? doc.nodes
      : doc.nodes.filter(n => (seen.has(n.group) ? false : (seen.add(n.group), true)))
    pickNodes.forEach(n => stops.push({ id: n.id, pos: new THREE.Vector3(...n.position), size: n.size }))
    return stops
  }, [doc])

  useEffect(() => {
    if (!tour || tourStops.length === 0) return
    setExplode(0); setAutoRotate(false)
    let i = 0
    const go = () => {
      const s = tourStops[i % tourStops.length]
      setSelected(s.id)
      setFocusReq({ pos: s.pos.clone(), dist: Math.max(s.size * 6, 1.7), v: cnt.current++ })
      i++
    }
    go()
    const iv = setInterval(go, 3200)
    return () => clearInterval(iv)
  }, [tour, tourStops])

  // raio da cena: enquadra a geometria toda (planos largos, pilhas altas) sem entrar dentro.
  // Hooks ANTES de qualquer return condicional (regras de hooks).
  const sceneR = useMemo(() => {
    if (!doc) return 1.2
    let r = 1.2
    const reach = (pos: Vec3, size = 0.3, scale?: Vec3) => {
      const s = size * Math.max(1, ...(scale || [1, 1, 1]))
      r = Math.max(r, Math.hypot(pos[0], pos[1], pos[2]) + s)
    }
    for (const n of doc.nodes) reach(n.position, n.size, n.scale)
    for (const m of (doc.meshes || [])) reach(m.position, m.size ?? 0.3, m.scale)
    return r
  }, [doc])
  const isoDir = useMemo(() => {
    const c = (doc?.camera?.position || [2.0, 1.4, 2.0]) as Vec3
    const v = new THREE.Vector3(...c); if (v.length() < 1e-3) v.set(2, 1.4, 2)
    return v.normalize()
  }, [doc])
  // centroide do conteúdo (bbox das posições): presets olham para cá, não para a origem
  const center = useMemo(() => {
    if (!doc) return new THREE.Vector3()
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity]
    const acc = (p: Vec3) => { for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], p[k]); hi[k] = Math.max(hi[k], p[k]) } }
    for (const n of doc.nodes) acc(n.position)
    for (const m of (doc.meshes || [])) acc(m.position)
    if (!isFinite(lo[0])) return new THREE.Vector3()
    return new THREE.Vector3((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
  }, [doc])

  if (!doc) return <p className="muted">carregando 3D…</p>
  if (!doc.available) return (
    <p className="legal-note">
      Modelo 3D ainda não descrito para esta patente. Adiciona-se um <code>render3d.json</code> na pasta da patente.
    </p>
  )
  const selNode = doc.nodes.find(n => n.id === selected)
  const selMesh = (doc.meshes || []).find(m => m.id === selected)
  const sel = selNode || selMesh
  const D = sceneR * 2.15
  const isoPos: Vec3 = [center.x + isoDir.x * D, center.y + isoDir.y * D, center.z + isoDir.z * D]
  const layers = (doc.layers || []).slice().sort((a, b) => a.order - b.order)
  const hasBody = (doc.meshes || []).length > 0
  const onFocus = (pos: THREE.Vector3, dist: number) => setFocusReq({ pos: pos.clone(), dist, v: cnt.current++ })
  const animateExplode = (to: number) => {
    const target = to
    const step = () => setExplode(prev => {
      const next = prev + (target - prev) * 0.14
      if (Math.abs(next - target) < 0.006) return target
      rafRef.current = requestAnimationFrame(step)
      return next
    })
    cancelAnimationFrame(rafRef.current); rafRef.current = requestAnimationFrame(step)
  }
  const preset = (p: Vec3) => { setSelected(null); setPresetReq({ pos: new THREE.Vector3(...p), tgt: center.clone(), v: cnt.current++ }) }

  return (
    <div>
      <p className="muted" style={{ fontSize: 12.5, marginTop: 0 }}>
        Camada (c): {hasBody ? 'dispositivo concreto multi-camada' : 'geometria do algoritmo'} —
        arraste p/ girar, scroll p/ zoom. <b>Clique um componente: a câmera voa até ele.</b>
        <span className="legal-note"> {doc.note}</span>
      </p>
      <div className="r3d-toolbar">
        <button className="btn xs" onClick={() => setExpanded(e => !e)}
          title={expanded ? 'voltar ao tamanho normal (ESC)' : 'ocupar a tela inteira — espaço para mexer no dispositivo'}>
          {expanded ? '⛶ sair (ESC)' : '⛶ expandir'}
        </button>
        <button className={`btn xs ${tour ? '' : 'gold'}`} onClick={() => setTour(t => !t)}>
          {tour ? '■ parar tour' : '▶ tour guiado'}
        </button>
        <button className="btn ghost xs" onClick={() => preset([center.x, center.y + sceneR * 0.35, center.z + D])}>frente</button>
        <button className="btn ghost xs" onClick={() => preset([center.x + 0.01, center.y + D * 1.15, center.z + 0.01])}>topo</button>
        <button className="btn ghost xs" onClick={() => preset(isoPos)}>isométrica</button>
        <label className="r3d-chk"><input type="checkbox" checked={autoRotate} onChange={e => setAutoRotate(e.target.checked)} /> auto-girar</label>
        <label className="r3d-chk"><input type="checkbox" checked={showLabels} onChange={e => setShowLabels(e.target.checked)} /> rótulos</label>
        <label className="r3d-chk"><input type="checkbox" checked={isolate} onChange={e => setIsolate(e.target.checked)} /> isolar seleção</label>
        {(doc.dimensions || []).length > 0 && <label className="r3d-chk"><input type="checkbox" checked={showDims} onChange={e => setShowDims(e.target.checked)} /> cotas</label>}
      </div>
      <div className={'r3d-wrap' + (expanded ? ' r3d-expanded' : '')}>
        {expanded && (
          <button className="r3d-exit" onClick={() => setExpanded(false)} title="sair (ESC)">✕</button>
        )}
        <div className="r3d-canvas">
          <Canvas camera={{ position: isoPos, fov: 45 }} dpr={[1, 2]} shadows
            gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping, toneMappingExposure: 1.15, localClippingEnabled: true }}>
            <color attach="background" args={['#0b0f16']} />
            <fog attach="fog" args={['#0b0f16', sceneR * 2.6, sceneR * 6.5]} />
            <Scene doc={doc} explode={explode} peel={peel} cut={cut} cutPos={cutPos}
              visible={visible} layerVisible={layerVisible} isolate={isolate} showLabels={showLabels}
              showDims={showDims} autoRotate={autoRotate} selected={selected} setSelected={setSelected}
              focusReq={focusReq} presetReq={presetReq} onFocus={onFocus} />
          </Canvas>
        </div>
        <div className="r3d-panel">
          <div className="r3d-control">
            <label>Abrir / explodir</label>
            <input type="range" min={0} max={1.4} step={0.01} value={explode} onChange={e => setExplode(parseFloat(e.target.value))} />
            <div style={{ display: 'flex', gap: 6, marginTop: 6 }}>
              <button className="btn xs" style={{ flex: 1 }} onClick={() => animateExplode(1.15)}>⇱ explodir</button>
              <button className="btn ghost xs" style={{ flex: 1 }} onClick={() => animateExplode(0)}>⇲ montar</button>
            </div>
          </div>
          {layers.length > 0 && (
            <div className="r3d-control">
              <label>Descascar camadas ({peel}/{layers.length})</label>
              <input type="range" min={0} max={layers.length} step={1} value={peel} onChange={e => setPeel(parseInt(e.target.value))} />
              <div className="r3d-layerlist">
                {layers.map(l => (
                  <label key={l.id} className="r3d-grouprow" style={{ opacity: l.order < peel ? 0.4 : 1 }}>
                    <input type="checkbox" checked={layerVisible[l.id] !== false}
                      onChange={e => setLayerVisible(v => ({ ...v, [l.id]: e.target.checked }))} />
                    {l.name}
                  </label>
                ))}
              </div>
            </div>
          )}
          <div className="r3d-control">
            <label><input type="checkbox" checked={cut} onChange={e => setCut(e.target.checked)} /> Corte transversal</label>
            {cut && <input type="range" min={-1.2} max={1.2} step={0.01} value={cutPos} onChange={e => setCutPos(parseFloat(e.target.value))} />}
          </div>
          <div className="r3d-groups">
            {doc.groups.map(g => (
              <label key={g.name} className="r3d-grouprow">
                <input type="checkbox" checked={visible[g.name] !== false}
                  onChange={e => setVisible(v => ({ ...v, [g.name]: e.target.checked }))} />
                <span className="cmap-legend-dot" style={{ background: g.color }} />
                {g.label} <span className="muted">×{g.count}</span>
              </label>
            ))}
          </div>
          <div className="r3d-detail">
            {sel ? (
              <>
                <div className="cmap-detail-id" style={{ color: (selNode?.color || selMesh?.color) }}>{sel.id}</div>
                <div style={{ fontWeight: 700, fontSize: 13, margin: '2px 0 6px' }}>{sel.label}</div>
                {(selNode?.marker || selMesh?.marker) && <span className="badge mk" style={{ marginBottom: 8 }}>{selNode?.marker || selMesh?.marker}</span>}
                <p style={{ fontSize: 12, lineHeight: 1.5 }}>{sel.desc}</p>
                <button className="btn ghost xs" onClick={() => { setSelected(null); preset(isoPos) }}>↩ ver tudo</button>
              </>
            ) : <p className="muted" style={{ fontSize: 12 }}>Clique um componente: a câmera voa até ele e mostra a descrição. Use "descascar" e "corte" para ver por dentro.</p>}
          </div>
        </div>
      </div>
      {doc.constants && doc.constants.length > 0 && (
        <div className="cmap-consts">
          {doc.constants.map((k, i) => (
            <div key={i} className="cmap-const">
              <b>{k.symbol}</b> = <span style={{ color: 'var(--accent-2)' }}>{k.value}</span>
              <div className="muted" style={{ fontSize: 11.5 }}>{k.note}</div>
            </div>
          ))}
        </div>
      )}
      <p className="muted" style={{ fontSize: 11.5, marginTop: 8 }}>
        {doc.nodes.length} componentes{hasBody ? ` · ${(doc.meshes || []).length} peças estruturais` : ''} ·
        {doc.edges.length} conexões. Ilustração de engenharia interativa — não é prova física.
      </p>
    </div>
  )
}
