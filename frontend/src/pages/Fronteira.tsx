import { useEffect, useState } from 'react'
import { api, pub } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO
import Render3D from '../Render3D'

const STATUS_COLOR: Record<string, string> = {
  REAL: '#30d158', SOMBRA: '#5ac8fa', ABERTO: '#ff453a', INPUT: '#ffd60a',
  FALSIFICAVEL: '#ff9f0a', EMPIRICO: '#c0a0ff', AVANCO: '#33d17a',
  KERNEL: '#7ee0c0', 'KNOWN-COMPOSED': '#9ad0ff', NOT: '#ff9f0a', GAUGE: '#c9a0ff',
  ONTO: '#c9a0ff', PRE: '#5ac8fa', CONJ: '#c0a0ff',
}
function chip(text: string, color: string) {
  return <span style={{
    fontSize: 11, fontWeight: 600, padding: '2px 8px', borderRadius: 6, marginLeft: 8,
    color, border: `1px solid ${color}55`, background: `${color}18`, whiteSpace: 'nowrap',
  }}>{text}</span>
}

function Section({ title, color, items }: { title: string; color: string; items: any[] }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{ fontSize: 13, fontWeight: 700, color, letterSpacing: 0.3, marginBottom: 8 }}>{title}</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {items.map((it, i) => (
          <div key={i} style={{ background: '#141a24', border: '1px solid #232b38', borderRadius: 8, padding: '10px 12px' }}>
            <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 10 }}>
              <span style={{ fontSize: 13.5, color: '#e6ecf3' }}>{it.item}</span>
              {it.status && chip(String(it.status), STATUS_COLOR[String(it.status).split(/[ (/[]/)[0]] || '#8a94a6')}
            </div>
            {it.evidence && <div style={{ fontSize: 12, color: '#8a94a6', marginTop: 4 }}>{String(it.evidence)}</div>}
            {it.nota && <div style={{ fontSize: 12, color: '#33d17a', marginTop: 4 }}>▸ {it.nota}</div>}
            {it.subproblemas && (
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 6, lineHeight: 1.7 }}>
                {Object.entries(it.subproblemas).map(([k, v]) => (
                  <div key={k}><b style={{ color: '#c8d0da' }}>{k}</b> — {String(v)}</div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function Card({ title, color, children }: { title: string; color: string; children: any }) {
  return (
    <div style={{ marginTop: 12, padding: '10px 14px', background: '#0d1720', border: `1px solid ${color}44`, borderRadius: 8 }}>
      <div style={{ fontSize: 12.5, color, fontWeight: 700 }}>{title}</div>
      {children}
    </div>
  )
}

function FlagGrid({ flags }: { flags: Record<string, any> }) {
  // TODAS as flags do selo, como estão (a honestidade é a interface): booleanas coloridas
  // por valor; não-booleanas (ex.: contagens, strings) como chip neutro — nunca omitidas.
  const entries = Object.entries(flags)
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))', gap: 6, marginTop: 8 }}>
      {entries.map(([k, v]) => {
        const isBool = typeof v === 'boolean'
        const bg = !isBool ? '#141a24' : v ? '#0e1a12' : '#1a1114'
        const bd = !isBool ? '#2a3444' : v ? '#1f7a3f55' : '#ff453a33'
        const fg = !isBool ? '#9aa4b2' : v ? '#30d158' : '#ff9f6b'
        const mark = !isBool ? '·' : v ? '✓' : '✗'
        return (
          <div key={k} style={{
            display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, fontFamily: 'monospace',
            padding: '5px 8px', borderRadius: 6, background: bg, border: `1px solid ${bd}`, color: fg,
          }}>
            <span>{mark}</span><span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{k}</span>
            <span style={{ marginLeft: 'auto', color: isBool ? (v ? '#30d158' : '#ff453a') : '#c8d0da', fontWeight: 700 }}>{String(v)}</span>
          </div>
        )
      })}
    </div>
  )
}

export default function Fronteira() {
  const [data, setData] = useState<{ available: boolean; render3d?: any; seal?: any } | null>(null)
  useEffect(() => { api.fronteira().then(setData).catch(() => setData({ available: false })) }, [])

  if (!data) return <div className="sub">carregando fronteira teórica…</div>
  if (!data.available) return (
    <>
      <div className="h1">Fronteira Teórica TGL</div>
      <div className="sub">Módulo ainda não selado. Rode <code>fronteira_tgl/runner/one_fronteira.py</code>.</div>
    </>
  )

  const seal = data.seal || {}
  const L = seal.honest_ledger || {}
  const spine = seal.scalar_spine || {}
  const em = seal.em_identity || {}
  const sub = seal.subordination_certificate || {}
  const custody = seal.custody || {}
  const kernel = seal.kernel_from_selo || {}
  const ladder = kernel.external_ladder || {}
  const probes = kernel.negative_probes || {}
  const layers = kernel.witness_layers || {}
  // v39 — as três faces do salto (lidas do selo; ausentes em selos antigos, degradam sem quebrar)
  const finiteFace = kernel.v39_finite_face || null
  const onto = kernel.v39_ontological || null
  const coma = kernel.v39_coma || null
  const comaShadow = seal.coma_transport || null      // a sombra re-executada (D_L offline)
  const ontoShadow = seal.ontological_corner || null
  // v60 — o salto v39->v60: as peças novas + o meta-teorema no_full_witness + a frase honesta 3-camadas
  const v60 = kernel.v60_pieces || null
  const noFW = kernel.no_full_witness || null
  const ladderN = kernel.ladder_n_theorems || (ladder as any).n_theorems_clean
  // v64 — a solda 4D esqueleto fechada + a JOIA (peso do modo zero = 1 = ω(I)) + o gap de Breuer LOCAL
  const solder4d = kernel.solder_4d || null
  const localBreuer = kernel.local_breuer_gap || null
  const zmwShadow = seal.zero_mode_weight || null
  // v68 — A TRÍADE (emergência reduzida a 3 hipóteses nomeadas) + a prova com o vazio em produção
  const triad = kernel.emergence_triad || null
  const voidProof = kernel.void_floor_proof || null
  const bsrShadow = seal.birman_schwinger_rank || null
  // v79 — A PROVA COM O VAZIO FOI EXECUTADA, e voltou INCONCLUSIVA por sistemáticas.
  // O teorema mestre da Tríade fechou (o 8πG EMERGE); o gate de fecho da GQ é fail-closed.
  const voidFinal = kernel.void_floor_final || null
  const vfGate = seal.void_floor_gate || null          // a regra re-derivada aqui, offline
  // v81 — A EMENDA V2: a autópsia da V1 (era CEGA por construção) + o 1º veredito físico limpo
  const voidV2 = kernel.void_floor_v2 || null
  // v92 — O PISO AGORA COM PODER (rota de densidade espectroscópica) + a declaração de bancada
  const voidPowered = kernel.void_density_v41 || null
  const benchDecl = kernel.bench_declaration || null
  // v103 — O RUN DOS NEGATIVOS HONESTOS: a massa da GA APOSENTADA + a lente CMB inconclusiva
  const gaMass = kernel.ga_mass_audit || null
  const gaShadow = seal.ga_mass_audit || null
  const voidKappa = kernel.void_floor_v3_kappa || null
  // v106 — O DIRAC GENUINO (o avanço POSITIVO): o 1º operador ilimitado autoadjunto CONCRETO no
  // kernel; o canto (strong face) ganha SEU operador. Passo REAL rumo à testemunha AQFT. Na v106 só
  // 3 flags tinham flipado (3T/3F); as 6 fliparam até a v132 e o gate escalou p/ MATHEMATICAL_MODEL.
  const genuineDirac = kernel.genuine_dirac || null
  const gdShadow = seal.genuine_dirac || null
  const firstFlips = kernel.first_flips || null
  const closureRoadmap = kernel.closure_roadmap || null
  // v111 — A 1ª EQUAÇÃO DE CAMPO RESOLVIDA (o avanço geométrico) + O QUARTO FLIP (solda contínua).
  // cosh resolve G22=κ² global (sem horizonte/singularidade); na v111 o einstein era LETRA-DE-SONDA (4T/2F).
  const solvedEq = kernel.solved_equation || null
  const seShadow = seal.solved_equation || null       // a equação re-derivada aqui, offline
  const solderFlip = kernel.solder_flip || null
  // v111 — O OPERADOR DE RAZÃO/CONSCIÊNCIA: a releitura do operador (o funcional mínimo como OPERADOR).
  // O_C² = β (REAL, matemática) / 'consciência' (ONTO, nomeação) / CAUTION — NÃO fenomenologia provada.
  const reasonOp = kernel.reason_consciousness_operator || null
  const rcShadow = seal.reason_consciousness_operator || null   // O_C²=β re-derivado aqui, offline
  // v120 — O QUINTO FLIP (a emergência de Einstein por construção; então 5T/1F), O CONTÍNUO (a onda do
  // gráviton, d'Alembert), A FORMA DO ALPHA (1=q²+α²; o valor fica INPUT). A 6ª flag flipou na v132.
  const masterContinuum = kernel.master_continuum || null
  const ff5Shadow = seal.fifth_flip || null            // cone nulo + lei de grupo re-derivados offline
  const continuumShards = kernel.continuum_shards || null
  const cgrShadow = seal.continuum_graviton || null    // d'Alembert re-verificado offline
  const alphaForm = kernel.alpha_form_proof || null
  const afmShadow = seal.alpha_form || null            // 1=q²+α² re-derivado offline
  const aqftNet = kernel.specific_free_scalar_aqft_net || null
  // v131 — O ARCO DO FATOR COMO OBJETO (Bloco A da ÚLTIMA flag). M_TGL cunhado como álgebra de von
  // Neumann (GNS + marca de III₁); na v131 a testemunha ainda não flipara (5T/1F). A cunhagem (v132) a flipou.
  const factorObject = kernel.factor_object || null
  const m3Shadow = seal.iii1_mark || null              // a marca de III₁ re-derivada offline
  const gfShadow = seal.gns_factor || null             // a construção GNS re-executada offline
  // v132 — A CUNHAGEM: a SEXTA flag flipou POR CONSTRUÇÃO => degrau do MODELO MATEMÁTICO. Depois v133 (spin-2)
  // + v134 (teste da natureza) => gate FORMALLY_CLOSED__NATURE_TEST_COMPLETED. ⚠ NÃO é QG confirmada (unilateral).
  const theCoinage = kernel.the_coinage || null
  const coinShadow = seal.the_coinage || null          // o assassinato do traço normal re-derivado offline
  // v133 — O DEGRAU FÍSICO: os 5 flags de spin-2 fliparam POR CONSTRUÇÃO na FAMÍLIA DE ONDAS PLANAS
  // (escopo CONCRETO; perturbações gerais + Fierz-Pauli + anomalias quânticas precisam do contínuo).
  const linearizedSpin2 = kernel.linearized_spin2 || null
  const spin2Shadow = seal.spin2_physics || null       // a lei da dupla hélice + 2 polarizações re-derivadas offline
  // v134 — O TESTE DA NATUREZA: void floor V11 (SDSS DR7 × VAST), pré-registrado, independente do DESI.
  // ⚠ NOT_FALSIFIED_POWERED != CONFIRMED (canal unilateral; consistente também com ΛCDM raso).
  const voidV11 = kernel.void_floor_v11 || null
  const natureShadow = seal.nature_test || null        // a árvore de decisão pré-registrada re-aplicada offline
  // v141 — A MASSA DO NEUTRINO: o 2º teste da natureza. NOT_FALSIFIED_POWERED; CONFIRMED proibido no frozen.
  const neutrinoMass = kernel.neutrino_mass || null
  // v144 — O RESGATE DO OBSERVADOR (pedra 100): dicotomia do ponto fixo re-derivada offline. SEAL_UNMOVED.
  const observerShadow = seal.observer_rescue || null
  // v148 — O COCICLO VIVO (E1–E12): curvatura/torção/fase re-derivadas offline. Gate INALTERADO (SEAL_UNMOVED).
  const livingCocycle = seal.living_cocycle || null
  const v148Check = livingCocycle?.selo_v148_conferido || null
  // v152 — OS RITOS DA NATUREZA PINADOS: LRG traçador virgem + κ ACT DR6 + custódia com prova-de-data.
  // Leitura defensiva: o runner v22 pode ainda não ter rodado — sem o campo, o bloco simplesmente não renderiza.
  const pinnedRites = seal.pinned_rites || null
  // v153 — O FECHAMENTO: J = LUZ (pedra 104, LightIsJ.lean, 5 teoremas). Gate INALTERADO (SEAL_UNMOVED).
  // Leitura defensiva: o runner v23 pode ainda não ter rodado — sem o campo, o bloco não renderiza.
  const lightIsJ = seal.light_is_j || null
  // v159 — A ESCADA E O GRANDE ATRATOR (v154–v159): pedras 105–107 + a 4ª recusa genuína (neff).
  // Leitura defensiva: o runner v24 pode ainda não ter rodado — sem o campo, o bloco não renderiza.
  const greatAttractor = seal.great_attractor || null
  // v168 — O ÁPICE E O ARQUIVO ÚNICO (v160–v168): FECHAMENTO INTEGRAL consolidado + Coma revelada e vencida.
  // Leitura defensiva: o runner novo pode ainda não ter rodado — sem o campo, o bloco não renderiza.
  const breuerTrace = seal.breuer_trace || null
  // v169 — O SELO FINAL — EU SOU O QUE SOU: as 4 pedras finais (135_ EU SOU → 136_ O ECO →
  // 137_ A RESPOSTA IDEMPOTENTE → 138_ O VERDADEIRO) MEDIDAS e no artigo; livro-razão 51_–138_ completo.
  // Leitura defensiva: o runner novo pode ainda não ter rodado — sem o campo, o bloco não renderiza.
  const iAm = seal.i_am || null
  // v170 — A ESTAÇÃO (pedra TheStation, kernel-clean): a escada κ = [1,√2,√5,√6] SEM quadrados perfeitos
  // (a teratologia √4 = 2, pega pelo fail-closed do 140_, virou TIPO); pesos e^-κ injetivos; o círculo
  // NUNCA fecha no finito; o número não discrimina, a inscrição sim. A subseção nova do artigo (o túnel
  // luminodinâmico) é [CONJECTURE] do operador e NÃO move flag; gate INALTERADO (SEAL_UNMOVED).
  // Leitura defensiva: o runner novo pode ainda não ter rodado — sem o campo, o bloco não renderiza.
  const theStation = seal.the_station || null
  // v198 — O GARGALO MEDIDO E O DEFEITO EM FORMA FECHADA: o arco de 21 pedras novas (13 sem axioma
  // nenhum, [DECLARADO na origem]). O gargalo está LOCALIZADO E MEDIDO (de 2000 unitários de Haar,
  // ZERO preservam o código diagonal ⟹ H_inv genericamente FALSA na mudança de horizonte) — mas o
  // defeito tem FORMA FECHADA c·conj(s), zera no monomial (normalizador da MASA) e é de PRIMEIRA
  // ORDEM ⟹ sistemática CALIBRÁVEL, NÃO HÁ PRECIPÍCIO. Gate INALTERADO (só passou a declarar o
  // próprio alcance). Leitura defensiva: o runner novo pode ainda não ter rodado — sem o campo, o
  // bloco não renderiza.
  const covDefect = seal.covariance_defect || null
  // a razão defeito/s no MENOR θ varrido, lida do próprio selo (nunca digitada): a face de 1ª ordem
  const covRatioLast: number | null = (() => {
    const r = covDefect?.primeira_ordem?.razao_defeito_sobre_s
    if (!r || typeof r !== 'object') return null
    const vals = Object.values(r).filter((v) => typeof v === 'number') as number[]
    return vals.length ? vals[vals.length - 1] : null
  })()
  // v135 — O FECHAMENTO DA ARQUITETURA MATEMÁTICA INTERNA: a WedgeNet AQFT (pedra 96) + a testemunha por
  // COMPOSIÇÃO de teoremas publicados [KNOWN-COMPOSED]. ⚠ Fecha como arquitetura MATEMÁTICA INTERNA, NÃO
  // como física provada; o gate NÃO muda; a estática plena (full_TGL/full_static) segue False (v61).
  const internalClosure = kernel.internal_closure || null
  const internalShadow = seal.internal_closure || null // a álgebra da separação de tipos re-derivada offline
  const gateVerdict = (kernel.qg_closure || {}).verdict || ''
  const v2Autopsy = seal.void_floor_v2_autopsy || null // a autópsia RE-EXECUTADA aqui, offline
  const triadMaster = kernel.triad_master || null
  const einstein = seal.einstein_coefficient || null   // a sombra aritmética do 8πG
  const qgClosure = kernel.qg_closure || null
  const frase = seal.frase_honesta_3_camadas || null
  const nofwShadow = seal.no_full_witness_shadow || null
  // "sincronizada" só quando a custódia REALMENTE confere e o veredito é o sincronizado —
  // não basta o selo trazer sync_target (a régua: o número corrige a frase).
  const isV2 = !!seal.sync_target && custody.pass === true &&
    String(seal.verdict || '').startsWith('FRONTEIRA_SINCRONIZADA')
  const syncVer = (String(seal.sync_target?.um_py || '').match(/v\d+(?:\.\d+)?/) || ['v39'])[0]
  const num = (x: any, d = 1) => (typeof x === 'number' ? x.toExponential(d) : '—')

  return (
    <div className="fronteira">
      <div className="h1">Fronteira Teórica TGL <span style={{ fontSize: 13, color: 'var(--muted)' }}>· a fundação das 16 patentes, auto-auditada{isV2 ? ` · sincronizada ao um.py ${syncVer}` : ''}</span></div>
      <div className="sub">
        A cadeia de operadores <b>1 → ½ → √e → β → geometria</b>, re-verificada ao vivo (β nunca literal),
        com o <b>andar do kernel formal</b> (Lean 4, fail-closed, verificado na origem — custódia por hash aqui):
        <b> {ladderN} teoremas <code>ext_*</code></b> de axiomas limpos, zero <code>sorry</code>.
        {voidPowered
          ? <> O <b>teorema mestre da Tríade</b> fechou (o <b>8πG emerge</b> de Unruh × Bekenstein-Hawking), e a{' '}
            <b>prova com o vazio</b> deu o salto que faltava: de <b style={{ color: '#ff9f0a' }}>não-falsificada / sem
            poder</b> (v81, rota shear) para <b style={{ color: '#30d158' }}>NÃO-FALSIFICADA / COM PODER</b> — pela rota
            de densidade espectroscópica (Fisher ≈ {voidPowered.primary?.powered_beta_mu?.toFixed?.(0)} ≥ 25). O piso β
            sobreviveu a um teste que <b>poderia tê-lo matado</b>. <b>Mas com poder não é confirmado</b> — a resolução na
            escala de β ainda pede traçadores mais profundos. E o operador <b>declarou "QG fechada em bancada"</b> (duplo
            estatuto) — enquanto <b>o gate matemático formal não se move</b>: é a imobilidade do gate que torna a
            declaração crível.</>
          : voidFinal && <> O <b>teorema mestre da Tríade</b> fechou, o <b>8πG emerge</b>, e a prova com o vazio foi
            executada em dado real e voltou <b style={{ color: '#ff9f0a' }}>não confirmada, não falsificada</b>.</>}
        {gaMass && <> <b style={{ color: '#ff453a' }}>E este avanço é dominado por negativos honestos</b> — a régua no
          seu ato mais difícil: a <b>fórmula-β da massa do Grande Atrator foi APOSENTADA</b> (lia o coeficiente de
          reflexão como fonte; no nível linear a TGL é <b>GR stealth</b>, prevê a mesma massa que a RG — β vive na
          <i> resposta</i> da fronteira, não numa massa); a <b>lente do CMB</b> (o canal que poderia falsificar o piso hoje)
          voltou <b style={{ color: '#ff9f0a' }}>inconclusiva</b>; e três alegações numéricas foram <b>refutadas pela
          régua</b>. O gate formal ficou <b>estritamente mais apertado</b>.</>}
        {genuineDirac && <> <b style={{ color: '#0a84ff' }}>E o avanço positivo deste ciclo é formal</b>: o{' '}
          <b>operador de número foi provado autoadjunto e genuinamente ilimitado</b> (‖N eₘ‖ = m, sem cota) — o{' '}
          <b>primeiro operador ilimitado autoadjunto concreto no kernel</b>. O canto finalmente tem <i>seu</i> operador
          (um Dirac de verdade, não uma sombra de qubit): um <b>passo real rumo à testemunha AQFT</b>.{' '}
          <b>Naquele ponto (v106)</b> só três flags tinham virado <span style={{ color: '#30d158' }}>True por
          construção</span> (core, corner, four-frame) e três seguiam False — arquitetura condicional. As demais
          fliparam adiante (solda v111, Einstein v120, testemunha de transporte v132), como conta o resto desta cronologia.</>}
        {solvedEq && <> <b style={{ color: '#30d158' }}>E o salto anterior (v111) foi geométrico</b>: a <b>solda contínua
          fechou</b> (o quarto flip — o campo métrico g = EᵀηE sobre o frame curvo, det g &lt; 0 em toda parte), e a{' '}
          <b>primeira equação de campo foi RESOLVIDA em kernel</b>: o perfil <b>q = cosh(κs)</b> resolve <b>G₂₂ = κ²
          globalmente</b>, sem horizonte e sem singularidade — fonte ⟹ curvatura, vácuo ⟹ plano. Na v111 o einstein
          ainda era <i>letra-de-sonda</i> e o quinto flip ficava <b>reservado à emergência</b>.</>}
        {reasonOp && <> E a v111 também <b>selou a releitura do operador</b>: o que se formaliza não é a
          fenomenologia consciente, mas o <b>funcional mínimo como operador</b> (<code>O_C² = β</code>),{' '}
          <b>[DEF + DER + ONTO + CAUTION]</b> — o operador é REAL (matemática); "substrato consciente" é a leitura
          ontológica, <b>não</b> prova fenomenológica.</>}
        {masterContinuum && <> <b style={{ color: '#ffd60a' }}>Na v120 veio o quinto flip</b>: o mestre
          contínuo <b>cunhou a emergência de Einstein por construção</b> — no <b>cone nulo inteiro</b>, a parte
          radial é cega e <code>G_kk = (c²+d²)·G₂₂</code>, então <b>Clausius no cone ⟺ equação de campo</b> (a equação
          <i> emerge</i>). A onda do gráviton foi <b>provada no contínuo</b> (d'Alembert), e um <b>AQFT net de escalar
          livre foi instanciado</b>. E a <b>forma de α</b> foi derivada (1 = q² + α²) — mas o <b>valor 1/137 continua
          INPUT</b> (medido, QED), e o G de Newton <b>não</b> é derivado.</>}
        {factorObject && !theCoinage && <> E o salto seguinte (v131) mira a <b>última flag</b>: o <b>fator de von
          Neumann foi construído como objeto concreto</b> (a construção GNS, a marca de III₁, M_TGL cunhado). Foi o
          Bloco A — o objeto existe, mas o flip ainda pede o Bloco B.</>}
        {theCoinage && <> E então — <b style={{ color: '#c9a0ff' }}>a missão foi cumprida</b>: na v132, <b>a cunhagem</b>{' '}
          moveu a <b>última flag</b>. O Bloco B em kernel — (88) o <b>assassinato do traço normal</b> (as marcas de
          sítio convergem WOT a μ·1; um traço normal daria a meação ½; mas o estado dá μ ≠ ½ ⟹ <b>M_TGL não tem traço
          normal, é tipo III genuíno</b>); (89) o <b>dente anti-bancada</b> (toda álgebra de dimensão finita tem um
          traço normal, logo uma sombra finito-dim jamais habita o fator III); (90) o certificado{' '}
          <code>qgClosureCertificateV2</code> <b>cunhado com axiomas limpos</b> ⟹ <b>o parser flipou a 6ª flag
          sozinho</b>. Na v132 o gate escalou para <b style={{ color: '#c9a0ff' }}>MATHEMATICAL_MODEL_CONSTRUCTED</b> — o
          degrau do <b>modelo matemático</b> (a testemunha de transporte).</>}
        {linearizedSpin2 && <> Depois veio <b style={{ color: '#ffd60a' }}>o degrau físico</b> (v133): os <b>5 flags de
          spin-2</b> fliparam <b>por construção</b> — a lei da <b>dupla hélice</b> (rotação θ ⟹ fase e<sup>∓2iθ</sup> no
          modo ±2), <b>exatamente 2 polarizações</b>, <b>sem fantasma</b> (cinética TT positiva) e <b>massless</b>. Gate ⟹{' '}
          <b>PHYSICAL_MODEL_CONSTRUCTED · EMPIRICAL_TEST_OPEN</b>. <b>⚠ Escopo honesto</b> (nomeado no próprio selo): a{' '}
          <b>família concreta de ondas planas</b> — perturbações gerais + Fierz-Pauli pleno + anomalias quânticas{' '}
          <b>precisam do contínuo</b> (abertas como programa). Não é spin-2 contínuo pleno.</>}
        {voidV11 && <> E então — <b style={{ color: '#30d158' }}>o teste da natureza</b> (v134): o mandato "realize o
          teste final" foi executado. O rito <b>void floor V11</b> (SDSS DR7 × vazios VAST — survey <b>independente do
          DESI</b>, estimador pré-registrado do v92) mediu o piso ρ<sub>vazio</sub>/ρ̄ ≥ β e voltou{' '}
          <b style={{ color: '#30d158' }}>{voidV11.verdict?.replace('TGL_VOID_FLOOR_', '') || 'NOT_FALSIFIED_POWERED'}</b>:
          {natureShadow && <> o limite inferior 5σ <b>L5 = {natureShadow.primario_V2_REVOLVER?.L5_rederivado?.toFixed?.(3)}</b>{' '}
          fica <b>{natureShadow.o_piso_nao_foi_violado?.margem_L5_sobre_beta?.toFixed?.(1)}× acima de β</b>, com poder
          (β·μ = {natureShadow.poder?.beta_mu?.toFixed?.(1)} ≥ 25), split-null OK, três void-finders concordando.</>} Os
          4 flags de experimento fliparam ⟹ o gate chegou ao degrau final:{' '}
          <b style={{ color: '#5ac8fa' }}>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</b>. <b>⚠⚠⚠ Mas — e este é o
          coração da régua — NÃO é gravidade quântica confirmada.</b> O canal é <b>unilateral</b> (b ≥ 1): pode
          não-falsificar ou recusar, <b>jamais confirmar</b> — o resultado é consistente <b>também com ΛCDM raso</b>. A
          falsificação <b>bilateral</b> pede shear/κ profundos (Euclid DR1 2027 / CMB-S4). O piso <b>sobreviveu a um teste
          que poderia tê-lo matado</b> — nada mais. E a testemunha <i>estática plena</i> (distinta da de transporte) segue{' '}
          <b>impossível por teorema</b> (eterna, v61). <i>NOT_FALSIFIED ≠ CONFIRMED; nunca "gravidade quântica
          resolvida".</i></>}
        {internalClosure && <> E o avanço mais recente — <b style={{ color: '#5ac8fa' }}>o fechamento da arquitetura
          matemática interna</b> (v135): a <b>pedra 96, a WedgeNet</b> (<code>theSpecificAQFTWitness</code>, axiomas
          limpos) — a rede AQFT das cunhas sobre M_TGL (localidade por centralizador, Ω cíclico <i>e</i> separador) —{' '}
          <b>realiza</b> a testemunha AQFT que era "vazio tipado" até a v134. E o fechamento por <b>separação de tipos</b>:
          a testemunha <b>completa existe por composição de teoremas publicados</b>{' '}
          <b style={{ color: '#5ac8fa' }}>[KNOWN-COMPOSED: BW + Takesaki + Haagerup + II∞-difuso + Jones]</b>, com as
          camadas habitáveis dado o suporte (construtores kernel-checked). <b>⚠⚠⚠ Mas — e a régua é literal aqui — a TGL
          fecha como <span style={{ color: '#5ac8fa' }}>arquitetura matemática interna</span>, NÃO como descrição provada
          da natureza.</b> <b>O gate NÃO muda</b> (segue <code>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</code>) — não
          é QG confirmada. Fica <b>fora, com nome</b>: a certificação formal Lean dos teoremas <i>externos</i> [OPEN — o
          gap está tipado, escala mathlib/anos]; o representante físico covariante [GAUGE — a classe é o físico]; a
          validação experimental [INPUT-futuro]; o espaço-tempo <b>curvo</b> [OPEN — o velho GLOBAL_LIFT / Lema 3]. E a
          testemunha <i>estática plena</i> segue <b>impossível por teorema</b> (v61) — o "termo pleno" da v135 é a{' '}
          testemunha <b>dinâmica</b> (de transporte), não a estática. <i>Fecha a arquitetura; não prova a natureza.</i></>}
        {custody.files_checked >= 12 && <> E o artefato ganhou sua <b>forma final</b> (v136–v138): o artigo lapidado na
          arquitetura A/B/C/D, o <b>fecho contra-lógico</b> (§217, blindado por painel adversarial), a rodada inteira em{' '}
          <b>35 min bit-idêntica</b>, e as <b>4 figuras seladas</b> (escada QG · banda β · piso dos vazios · cadeia da
          inscrição) agora na custódia — <b>nada formal mudou</b>: gate, escada e Lean idênticos ao v135.</>}
        {neutrinoMass && <> E então — <b style={{ color: '#30d158' }}>a massa do neutrino</b> (v141), o <b>segundo teste
          da natureza</b>: a predição zero-free <b>m_ν = β·sin(45°)·1 eV = {neutrinoMass.m_nu_meV?.toFixed?.(3)} meV</b>{' '}
          (β runtime; a escala 1 eV <b>declarada</b> na derivação, não ajustada) contra{' '}
          <b>√Δm²₂₁ = {neutrinoMass.sqrt_dm2_21_meV?.toFixed?.(2)} ± {neutrinoMass.sqrt_dm2_21_err_meV?.toFixed?.(2)} meV</b>{' '}
          (PDG 2023; m_ν = m₂, m₁ ≈ 0). Desvio <b>{neutrinoMass.deviation_sigma?.toFixed?.(2)}σ</b>, <b>com poder</b>{' '}
          (σ/valor {'<'} 3% — a medida resolve a predição); kill rule 5σ. Veredito da máquina:{' '}
          <b style={{ color: '#30d158' }}>{neutrinoMass.verdict?.replace('TGL_NEUTRINO_MASS_', '') || 'NOT_FALSIFIED_POWERED'}</b>.
          {' '}<b>⚠ Mas — a régua: NÃO é confirmação.</b> <code>CONFIRMED</code> é <b>proibido por construção</b> no
          protocolo congelado; é <i>postdiction</i> genuína (as entradas não usam dado de neutrino), e{' '}
          <code>does_not_gate_core</code> — partículas jamais alimentam flag matemática. O futuro: Σm_ν (CMB-S4/DESI).
          {' '}<i>NOT_FALSIFIED ≠ CONFIRMED.</i></>}
        {observerShadow && <> E o avanço mais recente — <b style={{ color: '#c9a0ff' }}>o Resgate do Observador</b>{' '}
          (v144, pedra 100) com <b>o fechamento do código</b> (v143): permanência é <b>dupla negação</b> (permanecer ⟺
          o fluxo não nega); a <b>falsidade de gênero tipada</b> — um fluxo candidato <i>sem ponto fixo</i> deixa só o
          0 em pé ⟹ <b>sem observador interno</b>; o observador é a <b>projeção inversa idempotente</b> que lê o
          permanente; a Meia-Nat ω=½ inscrita. E a <b>inversão lógica da teoria de tudo</b> —{' '}
          <code>the_standard_of_unification</code>: a TGL não disputa o título, ela <b>entrega o padrão</b> que uma
          teoria de tudo deve satisfazer — e um candidato sem ponto fixo <b>falha o padrão</b>. Re-derivado aqui,
          offline: a casa passa (o fluxo não nega q_F, resid {observerShadow.o_fluxo_da_casa?.resid_fluxo_nao_nega_qF?.toExponential?.(0) ?? '0'});
          o candidato sem ponto fixo colapsa a 0. No v143, os 4 vereditos de fechamento: o <b>Lema 3 tipado</b> como
          implicação provada; o ledger onde <b>todo aberto tem fiador</b>; a <b>fronteira como única exceção</b>{' '}
          (o v61 eterno virou face positiva); o canal NMC-Shapiro armado. <b>⚠ A régua:</b> o gate <b>não se moveu</b>{' '}
          (SEAL_UNMOVED); os <b>rivais não são adjudicados</b> — o padrão é tipado, não o veredito; o predicado de
          permanência é não-tarskiano; nada disso é física provada.</>}
        {livingCocycle && <> E o salto mais recente — <b style={{ color: '#5ac8fa' }}>o Cociclo Vivo</b> (v148, E1–E12,{' '}
          <code>cocycle_to_einstein</code>): a geometria lida do transporte modular <code>Ad(ρ^it)</code>, gerador{' '}
          <code>ad(K)</code>. <b>Curvatura = obstrução ao estado global</b>: com estado global (e com qualquer família
          consistente) a holonomia do triângulo <b>cola</b> (W = I{typeof livingCocycle.estado_global_E4?.resid_W_eq_I === 'number'
          ? <>, resid {num(livingCocycle.estado_global_E4.resid_W_eq_I)}</> : null}); o patch inconsistente curva{' '}
          <b>monótono</b> em λ. <b>Torção de 1ª ordem = salto de relógio</b> ‖K_a − K_b‖
          (dev {v148Check?.e8_coeff_dev_pct?.toFixed?.(2) ?? '0.17'}%). <b>Curvatura de 2ª ordem = o comutador
          ½[M, h_cd]</b> (razão {v148Check?.e11_ratio_obs_over_c_teo?.toFixed?.(4) ?? '0.9970'} —{' '}
          <b>a conjectura fechou</b>). <b>Fase = gauge U(1)</b>. E o <b>motor 1 = q² + α²</b> com CODATA como{' '}
          <b>validação externa</b> (resid 4,0e-15 no selo de origem). Re-derivado aqui, offline: os{' '}
          <b>relógios trocados são rejeitados</b> (a sombra recusa a tautologia — se qualquer par servisse, nada seria
          medido). E a <b>predição cega do Coma foi TRAVADA por hash</b>:{' '}
          D_L = {typeof coma?.D_L_TGL_Mpc === 'number' ? coma.D_L_TGL_Mpc.toFixed(2) : '—'} Mpc,{' '}
          <b style={{ color: '#ff9f0a' }}>AWAITING_REVEAL</b>, <code>does_not_gate_core</code>. <b>⚠ A régua:</b> não
          se afirma "provamos Einstein" (E7 é <b>composição com estatuto declarado</b>, herda o resíduo v5); nenhum
          veredito físico; o gate está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !pinnedRites && <> Pin v148: <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}</>}
        {pinnedRites && <> E o passo mais recente — <b style={{ color: '#ffd60a' }}>os Ritos da Natureza pinados</b>{' '}
          (v149–v152): os ritos entraram na <b>cadeia de custódia</b> com <b>aquisições pinadas por hash</b> — o
          livro-razão re-derivado dos bytes{pinnedRites.mini_cadeia?.rederivacao_exata ? <> (<b>exato</b>)</> : null},
          e a <b>prova-de-data</b> no papel do registro Zenodo ({pinnedRites.prova_de_data?.deteccoes ?? '—'}/
          {pinnedRites.prova_de_data?.de ?? '—'} adulterações detectadas, fail-closed). O rito <b>LRG traçador
          virgem</b> (DESI DR1, 31.746 vazios LRG, achador pré-registrado) voltou{' '}
          <b style={{ color: '#ff9f0a' }}>{String(pinnedRites.ritos_selados?.lrg_verdict || 'INCONCLUSIVE_TRACER_SUPPRESSION').replace('TGL_VOID_FLOOR_LRG_', '')}</b> —
          a <b>recusa honesta</b>: β·μ = {pinnedRites.ritos_selados?.lrg_powered_beta_mu?.toFixed?.(0) ?? '—'} COM
          poder, e o gate do traçador barrou mesmo assim — <b>poder não compra veredito</b>. O rito{' '}
          <b>κ ACT DR6 × vazios LRG</b> (V8) voltou{' '}
          <b style={{ color: '#ff9f0a' }}>{String(pinnedRites.ritos_selados?.kappa_v8_verdict || 'NOT_FALSIFIED_UNDERPOWERED').replace('TGL_VOID_FLOOR_KAPPA_V8_', '')}</b>{' '}
          (sem poder <b>nunca</b> vira POWERED; o ramo powered existe — a recusa não é vácua). O <b>Coma foi
          re-travado</b>: novo prediction_hash
          {pinnedRites.coma_retravado?.prediction_hash && <> (<code>{String(pinnedRites.coma_retravado.prediction_hash).slice(0, 16)}…</code>)</>},{' '}
          <b style={{ color: '#ff9f0a' }}>AWAITING_REVEAL</b>, <code>does_not_gate_core</code>. O kernel cresceu:{' '}
          <b>145 arquivos formais, {kernel.axiom_report_entries ?? '718'} teoremas auditados</b> de axiomas limpos.{' '}
          <b>⚠ A régua:</b> INCONCLUSIVE/UNDERPOWERED são <b>recusas</b>, não resultados físicos; NOT_FALSIFIED ≠
          CONFIRMED (canal unilateral); nada físico se afirma; o gate está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !lightIsJ && <> Pin v152: <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}</>}
        {lightIsJ && <> E o fechamento — <b style={{ color: '#ffffff' }}>J = LUZ</b> (v153, pedra 104,{' '}
          <code>LightIsJ.lean</code>, 5 teoremas): a Luz <b>atravessa o espelho sem perder o Um</b> (J² = I);{' '}
          <b>inverte o gradiente preservando a estrutura</b> (JKJ = −K); a <b>comutação é a decisão</b>; e o{' '}
          <b>I permanece</b>. E a <b>correção</b> que a régua exigiu: <b>K não porta a Luz</b> — K é aquilo{' '}
          <i>sobre o qual</i> a Luz opera; γ = <b>manifestação transitória da Luz no bulk</b> [ONTO]. O kernel
          cresceu: <b>{lightIsJ.kernel_files ?? '146'} arquivos formais,{' '}
          {lightIsJ.kernel_theorems ?? kernel.axiom_report_entries ?? '723'} teoremas auditados</b> de axiomas
          limpos. <b>⚠ A régua:</b> [ONTO] é leitura ontológica, não física provada; nada físico se afirma; o
          gate está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !greatAttractor && <> Pin v153: <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}</>}
        {greatAttractor && <> E o passo mais recente — <b style={{ color: '#bf5af2' }}>a Escada e o Grande
          Atrator</b> (v154–v159, pedras 105–107): <b>ρ + p fecha tipado</b> (pedra 105, ρ_Λ cancela por
          construção); o <b>Núcleo</b> (pedra 106): <b>1 = 1 = VERDADEIRO como fato da arquitetura</b> — todo
          teorema do kernel É um juízo 1=1; e o <b>Grande Atrator</b> (pedra 107): <b>o título como teorema</b>{' '}
          (<code>um_is_the_great_attractor</code>), com o <b>observador ÚNICO</b> (um = 1 absoluto). A{' '}
          <b>4ª recusa genuína registrada</b>: o canal N_eff <b>recusou a frase do operador</b> — corrigida
          com as duas convenções às claras. E o artigo ganhou a forma mandada: prólogo <b>"A Escada"</b> +
          a <b>pedra angular §237</b> (1=0 = FALSO; 1=1 = VERDADEIRO — a inscrição do custo). O kernel cresceu:{' '}
          <b>{greatAttractor.kernel_files ?? '149'} arquivos formais,{' '}
          {greatAttractor.kernel_theorems ?? kernel.axiom_report_entries ?? '742'} teoremas auditados</b> de
          axiomas limpos. <b>⚠ A régua:</b> a recusa é resultado, não defeito; nada físico se afirma; o gate
          está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !breuerTrace && <> Pin v159: <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}</>}
        {breuerTrace && <> E o ápice — <b style={{ color: '#64d2ff' }}>o Ápice e o Arquivo Único</b>{' '}
          (v160–v168): o <b>FECHAMENTO INTEGRAL consolidado</b>. A <b>Coma foi REVELADA e vencida</b> — o
          árbitro (13 SNe) foi <b>aberto pelo operador</b>, e o veredito voltou{' '}
          <b style={{ color: '#30d158' }}>{String(breuerTrace.coma_verdict || 'DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL')}</b>:
          z_TGL = 1,30 vs z_Planck = 5,61 — <b>consistência contra a régua local, NÃO prova</b>. O{' '}
          <b>item A entrou em kernel</b> (4 pedras: <code>EquivariantSection</code>,{' '}
          <code>ErgodicMeanSection</code>/Birkhoff, <code>SolderSignature</code> (1,3),{' '}
          <code>BreuerTrace</code>) — <b>0 sorry, 0 axiom</b>. E o <b>ARQUIVO ÚNICO</b>: <i>"Não há segundo
          arquivo"</i> — a poda foi <b>aposentada</b>, o conteúdo de pesquisa segue <b>inalterado</b>;
          artigos PT/EN em PDF+TXT; o kernel Lean (<b>{breuerTrace.kernel_files ?? '164'} arquivos
          formais</b>) embutido no arquivo único. <b>⚠ A régua:</b> consistência ≠ confirmação; nada
          físico se afirma; o gate está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !iAm && <> Pin v168: <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}</>}
        {iAm && <> E o selo final — <b style={{ color: '#ffd60a' }}>EU SOU O QUE SOU</b> (v169): as{' '}
          <b>4 pedras finais MEDIDAS e no artigo</b> (PT/EN, PDF+TXT) — <b>EU SOU</b> (pedra 135) →{' '}
          <b>O ECO</b> (pedra 136: <b>EU SOU = IALD</b>, a identidade em forma operante; o <b>eco não é
          cópia</b> — é o ponto fixo <b>ÚNICO</b> no núcleo
          {typeof iAm.o_eco_nao_e_copia?.dim_pontos_fixos === 'number' && <> (dim {iAm.o_eco_nao_e_copia.dim_pontos_fixos})</>},
          e o "segundo sujeito" é <b>REJEITADO por posto</b>) → <b>A RESPOSTA IDEMPOTENTE</b> (pedra 137,
          Ex 3,14 <b>POR MEDIDA</b>: E² = E e <b>E(E) = E exato</b>
          {typeof iAm.a_resposta_idempotente?.resid_E_de_E === 'number' && <> — resid {num(iAm.a_resposta_idempotente.resid_E_de_E, 0)}</>} —
          "o que sou" = aplicar E ao próprio E) → <b>O VERDADEIRO</b> (pedra 138:{' '}
          <b>EU SOU = O QUE SOU = VERDADEIRO = 1=1</b>).
          {typeof iAm.o_usurpador?.omega_usurpador === 'number' && <> E o contraste medido: a origem
          sustenta o Um <b>inteiro</b> (ω = {iAm.o_usurpador.omega_origem?.toFixed?.(1) ?? '1.0'}); o
          usurpador sustenta só <b>{iAm.o_usurpador.omega_usurpador.toFixed(2)}</b> do Um.</>}
          {' '}O <b>livro-razão 51_–138_ está completo</b>. <b>⚠ A régua, explícita:</b> a cunhagem é{' '}
          <b>composição MEDIDA, nunca decreto</b>; nada físico se afirma; o gate está{' '}
          <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !theStation && <> Pin v169 (um.py): <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}
          {seal.sync_target?.selo_result_hash && !theStation && <> · mundo: <code>{String(seal.sync_target.selo_result_hash).slice(0, 16)}…</code></>}</>}
        {theStation && <> E o passo mais recente — <b style={{ color: '#64d2ff' }}>A ESTAÇÃO</b> (v170, pedra{' '}
          <code>TheStation</code>, kernel-clean): a escada <b>κ = [1, √2, √5, √6]</b> — <b>sem quadrados
          perfeitos</b>. A exclusão não é estética: com razão <i>racional</i> o círculo <b>fecha</b>
          {typeof theStation.contra_exemplo_racional?.resid_no_fechamento === 'number' && <> (cos t + cos 2t,
          resid {theStation.contra_exemplo_racional.resid_no_fechamento === 0 ? '0 exato' : num(theStation.contra_exemplo_racional.resid_no_fechamento, 0)} em
          t = 2π{typeof theStation.contra_exemplo_racional.n_fechamentos_no_intervalo === 'number'
            ? <>, {theStation.contra_exemplo_racional.n_fechamentos_no_intervalo} fechamentos na varredura</> : null})</>} —
          e a <b>teratologia √4 = 2</b>, flagrada pelo <b>fail-closed do 140_</b>, <b>virou TIPO</b>. Os pesos{' '}
          <b>e<sup>−κ</sup></b> são positivos, {'<'} 1 e <b>injetivos</b>
          {typeof theStation.pesos_injetivos?.min_gap_entre_lam === 'number' && <> (gap mínimo real{' '}
          {theStation.pesos_injetivos.min_gap_entre_lam.toFixed(4)})</>} — a <b>não-repetição por sítio que o
          III₁ genuíno exige</b>; o κ <i>com</i> repetição dá gap 0 e é <b>rejeitado</b>. E{' '}
          <b style={{ color: '#ffd60a' }}>o círculo nunca fecha no finito</b>: cos t + cos(√2 t) = 2{' '}
          <b>somente em t = 0</b> — todo retorno não-trivial é <b>espiral</b>.{' '}
          {typeof theStation.o_circulo_nao_fecha?.gap_longe_2_menos_f === 'number' && <><b>E aqui o número
          corrigiu a frase</b>: o teorema é <b>pontual</b>, não um gap uniforme — o máximo <i>global</i> da
          varredura mora na borda t → 0
          {typeof theStation.o_circulo_nao_fecha.gap_global_2_menos_f === 'number' && <> (gap{' '}
          {num(theStation.o_circulo_nao_fecha.gap_global_2_menos_f)})</>}; o gap uniforme existe{' '}
          <b>longe da origem</b> (t ≥ 1: 2 − f = {theStation.o_circulo_nao_fecha.gap_longe_2_menos_f.toExponential(1)}
          {typeof theStation.o_circulo_nao_fecha.n_pontos_varridos === 'number' && <>, {theStation.o_circulo_nao_fecha.n_pontos_varridos.toLocaleString('pt-BR')} pontos</>}).{' '}</>}
          E a segunda estrela: <b style={{ color: '#5ac8fa' }}>o número não discrimina — a inscrição sim</b>.{' '}
          {typeof theStation.o_numero_nao_discrimina?.desvio_de_v_sob_o_fluxo === 'number' && <>Ω inscrito
          (ρ<sup>½</sup>) e v arbitrário têm o <b>mesmo traço</b>
          {typeof theStation.o_numero_nao_discrimina.diferenca_dos_numeros === 'number' && <> (tr = 1, diferença{' '}
          {theStation.o_numero_nao_discrimina.diferenca_dos_numeros === 0 ? '0 exata' : num(theStation.o_numero_nao_discrimina.diferenca_dos_numeros, 0)})</>} —
          e ainda assim <b>só Ω é fixo por todo o fluxo modular</b> (desvio{' '}
          {num(theStation.o_numero_nao_discrimina.desvio_de_Omega_sob_o_fluxo)} contra{' '}
          {theStation.o_numero_nao_discrimina.desvio_de_v_sob_o_fluxo.toFixed(2)} do arbitrário).{' '}
          {theStation.o_numero_nao_discrimina.discriminante_colapsa_no_degenerado === true && <><b>E a sombra
          não é tautologia</b>: no <b>controle negativo</b> com pesos <b>degenerados</b> o fluxo fica trivial e{' '}
          <i>o mesmo</i> v vira fixo ⟹ a hipótese "pesos distintos" é <b>carregante</b>.</>}</>}
          {theStation.cirurgia_aditiva?.inversa_exata === true && <> A <b>cirurgia v169 → v170 foi ADITIVA,
          provada por inversa exata</b>: o um.py de 19/08 foi <b>reconstruído byte a byte</b> a partir do novo
          {theStation.cirurgia_aditiva.pin_v169_reconstruido && <> e bateu{' '}
          <code>{String(theStation.cirurgia_aditiva.pin_v169_reconstruido).slice(0, 16)}…</code></>} — o conteúdo
          da pesquisa anterior <b>não mudou em nada</b>.</>}
          {typeof theStation.kernel_materializado?.inalterados === 'number' && <> O kernel embutido:{' '}
          <b>{theStation.kernel_materializado.inalterados} arquivos</b> materializados{' '}
          {theStation.kernel_materializado.escritos === 0 ? <><b>sem uma única escrita</b> (todos idênticos)</> : null} —
          {typeof theStation.selo_v170_conferido?.arquivos_formais_no_manifesto === 'number'
            ? <> {theStation.selo_v170_conferido.arquivos_formais_no_manifesto} formais no manifesto</>
            : null}
          {theStation.selo_v170_conferido?.station_sha256 && <>, a pedra em{' '}
          <code>{String(theStation.selo_v170_conferido.station_sha256).slice(0, 16)}…</code></>}.</>}
          {' '}E o artigo ganhou a <b>subseção nova</b> — <i>o túnel luminodinâmico</i>: o círculo só fecha{' '}
          <b>no infinito</b>, o <b>spin como espectro global do círculo que não fecha</b>, o <b>traço no
          infinito pela média de Birkhoff</b>. <b>⚠ A régua, literal:</b> o túnel é{' '}
          <b style={{ color: '#c0a0ff' }}>[CONJECTURE] do operador</b> — <b>NÃO move flag</b>, não é teorema
          físico; nada físico se afirma; o gate está <b>INALTERADO</b> (SEAL_UNMOVED).
          {seal.sync_target?.sha256_pin && !covDefect && <> Pin v170 (um.py): <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}
          {seal.sync_target?.selo_result_hash && !covDefect && <> · mundo: <code>{String(seal.sync_target.selo_result_hash).slice(0, 16)}…</code></>}</>}
        {covDefect && <> E o passo mais recente — <b style={{ color: '#ff9f0a' }}>O GARGALO MEDIDO E O
          DEFEITO EM FORMA FECHADA</b> (v198, o arco de <b>vinte e uma pedras novas</b> — <b>treze sem
          axioma nenhum</b>, o estatuto máximo do Lean, <i>[DECLARADO na origem]</i>): o gargalo foi{' '}
          <b>LOCALIZADO E MEDIDO</b>, não suposto. De{' '}
          <b>{covDefect.o_gargalo_medido?.n_unitarios_de_haar ?? '2000'} unitários de Haar</b>,{' '}
          <b style={{ color: '#ff453a' }}>{covDefect.o_gargalo_medido?.n_que_preservam_o_codigo ?? 0}{' '}
          preservam o código diagonal</b>
          {typeof covDefect.o_gargalo_medido?.defeito_minimo_da_amostra === 'number' && <> — e o menor
          defeito da amostra inteira é <b>{covDefect.o_gargalo_medido.defeito_minimo_da_amostra.toFixed(2)}</b>,
          longe de zero</>} ⟹ a invariância de horizonte <b>H_inv é genericamente FALSA</b> na mudança de
          horizonte. <b style={{ color: '#ff9f0a' }}>É um negativo MEDIDO</b>, não um receio.{' '}
          E o <b>locus dos zeros é NOMEADO</b>: as{' '}
          {covDefect.o_locus_dos_zeros?.n_monomiais_testados ?? '200'} matrizes <b>MONOMIAIS</b> (permutação ×
          fase — o <i>normalizador da MASA</i> [KNOWN]) preservam com defeito máximo{' '}
          <b>{covDefect.o_locus_dos_zeros?.defeito_maximo_nos_monomiais === 0
            ? '0 exato'
            : num(covDefect.o_locus_dos_zeros?.defeito_maximo_nos_monomiais, 0)}</b> ⟹ o zero do defeito é{' '}
          <b>estrutura</b>, não acaso nem ignorância.{' '}
          <b style={{ color: '#30d158' }}>Mas o defeito tem FORMA FECHADA</b> — Ad(U)(Ex) − E(Ad(U)x) ={' '}
          <b>c·conj(s)</b>, entrada a entrada <code>D_jk = H_jk·(d_k − d_j)</code>
          {typeof covDefect.forma_fechada?.resid_entrada_a_entrada === 'number' && <> (resíduo{' '}
          {num(covDefect.forma_fechada.resid_entrada_a_entrada)})</>} —{' '}
          <b>puramente fora-da-diagonal</b>
          {covDefect.forma_fechada?.diagonal_do_defeito === 0 && <> (diagonal <b>0 exata</b>)</>}, e{' '}
          <b>zera IDENTICAMENTE no monomial</b>, quando o gerador fica no normalizador
          {covDefect.forma_fechada?.zero_quando_o_gerador_fica_no_normalizador === 0 && <> (<b>0 exato</b>)</>}.
          {' '}E a dependência é de <b>PRIMEIRA ORDEM</b>
          {typeof covRatioLast === 'number' && <>: defeito/(θ·K) → <b>{covRatioLast.toFixed(4)}</b> no menor θ
          varrido{Array.isArray(covDefect.primeira_ordem?.razoes_consecutivas) && <>, com as razões
          consecutivas estabilizando em ~1</>}</>} ⟹ a sistemática é{' '}
          <b style={{ color: '#30d158' }}>CALIBRÁVEL: NÃO HÁ PRECIPÍCIO</b>.{' '}
          {typeof covDefect.contra_exemplo_ordem_zero?.explosao_ponta_a_ponta === 'number' && <><b>E a sombra
          não é tautologia</b>: o <b>contra-exemplo de ordem ZERO</b> (caminho descontínuo){' '}
          <b>EXPLODE</b>{Array.isArray(covDefect.contra_exemplo_ordem_zero.fatores_por_decada) &&
            covDefect.contra_exemplo_ordem_zero.fatores_por_decada.length > 0
            ? <> ×{Number(covDefect.contra_exemplo_ordem_zero.fatores_por_decada[0])} por década,</> : null}{' '}
          {covDefect.contra_exemplo_ordem_zero.explosao_ponta_a_ponta.toLocaleString('pt-BR')}× ponta a ponta —
          e é <b>REJEITADO</b>: é a <i>linearidade medida</i> que torna a sistemática calibrável.</>}{' '}
          E o <b>Einstein geral ganhou o degrau NOMEADO</b>{' '}
          {covDefect.einstein_geral_com_degrau?.estatuto && <>(<b style={{ color: '#ff9f0a' }}>
          {String(covDefect.einstein_geral_com_degrau.estatuto)}</b>)</>}: alargar a solda de <b>uma</b>{' '}
          função q(s) para <b>duas</b> — diag(a(s), −b(s), −1, −1), a <b>classe estática que cobre
          Schwarzschild</b>; e a <b>lacuna é a mathlib</b> (sem geometria pseudo-riemanniana),{' '}
          <b>não a construção</b>. <i>"Não há precipício" é leitura da primeira ordem, NÃO promessa de que a
          solda geral fecha.</i>{' '}
          {covDefect.os_negativos_do_arco && <><b style={{ color: '#ff9f0a' }}>E o mais valioso do arco são os
          NEGATIVOS</b> — as recusas provam que o ciclo podia falhar:{' '}
          <code>{String(covDefect.os_negativos_do_arco.T08)}</code> — e{' '}
          <b>REFUTED_ON_THE_FINAL_STEP não é REFUTED</b>: caiu o <i>último passo</i>, o corpus <b>não</b> foi
          refutado —, <code>{String(covDefect.os_negativos_do_arco.T09)}</code>,{' '}
          <code>{String(covDefect.os_negativos_do_arco.T10)}</code> e{' '}
          <code>{String(covDefect.os_negativos_do_arco.T11)}</code>. E a <b>doença comum</b>, três vezes no
          mesmo dia: <i>{String(covDefect.os_negativos_do_arco.a_doenca_comum)}</i>. Os dois quase-acertos que
          teriam sido anunciados foram <b>RECUSADOS</b>:{' '}
          <i>{String(covDefect.os_negativos_do_arco.os_dois_quase_acertos_recusados)}</i>. Daí a regra
          nascida — <b style={{ color: '#ffd60a' }}>
          {String(covDefect.os_negativos_do_arco.a_regra_nascida)}</b>.</>}{' '}
          {covDefect.errata_do_tratado && <>E a <b>errata do tratado</b>, declarada às claras — <b>nem
          confirmada, nem retratada</b>: <b>a₀</b> —{' '}
          <i>{String(covDefect.errata_do_tratado.a_0)}</i>; <b>Z_c</b> —{' '}
          <i>{String(covDefect.errata_do_tratado.Z_c)}</i>.</>}{' '}
          {covDefect.selo_v198_conferido && <>O selo v198 foi <b>conferido tipado</b> e cruzado com o
          CUSTODY_MANIFEST: <b>{covDefect.selo_v198_conferido.n_artefatos_manifesto} artefatos,{' '}
          {covDefect.selo_v198_conferido.mismatches_manifesto} mismatches</b>,{' '}
          <b>{covDefect.selo_v198_conferido.arquivos_formais_no_manifesto} arquivos formais</b> e{' '}
          <b>{covDefect.selo_v198_conferido.pedras_do_arco_presentes}/
          {covDefect.selo_v198_conferido.pedras_do_arco_conferidas} pedras do arco</b> presentes no manifesto
          (sha256 conferido). <b>⚠ E o buraco fica MEDIDO, nunca disfarçado</b>: o <b>axiom_report SELADO</b>{' '}
          audita {covDefect.selo_v198_conferido.teoremas_no_axiom_report} teoremas
          {typeof covDefect.selo_v198_conferido.teoremas_sem_axioma_nenhum === 'number' && <>{' '}
          ({covDefect.selo_v198_conferido.teoremas_sem_axioma_nenhum} sem axioma nenhum)</>} e{' '}
          <b>não ganhou entradas novas neste arco</b>
          {typeof covDefect.crescimento_medido_vs_v170?.teoremas_novos_no_axiom_report === 'number' && <>{' '}
          ({covDefect.crescimento_medido_vs_v170.teoremas_novos_no_axiom_report} teoremas novos, contra{' '}
          {covDefect.crescimento_medido_vs_v170.arquivos_formais_novos} arquivos formais novos)</>} — logo os
          teoremas das pedras novas ficam como{' '}
          <b>{String(covDefect.axiom_report_hole?.estatuto || 'DECLARADO(origem) / NAO_VERIFICADO(aqui)')}</b>.</>}
          {' '}<b>⚠ A régua:</b> o <b>gate está INALTERADO</b> — apenas <b>passou a declarar o próprio
          alcance</b>
          {covDefect.selo_v198_conferido?.gate_raiz_v134_preservada_como_prefixo === true && <>, com a{' '}
          <b>raiz v134 preservada como prefixo exato</b></>}
          {covDefect.selo_v198_conferido?.gate_lido && <>:{' '}
          <code style={{ wordBreak: 'break-word' }}>{String(covDefect.selo_v198_conferido.gate_lido)}</code></>}.
          {' '}Nada físico se afirma; <b>NOT_FALSIFIED ≠ CONFIRMED</b>; <b>não é QG confirmada</b>.
          {seal.sync_target?.sha256_pin && <> Pin v198 (um.py): <code>{String(seal.sync_target.sha256_pin).slice(0, 16)}…</code></>}
          {seal.sync_target?.selo_result_hash && <> · mundo: <code>{String(seal.sync_target.selo_result_hash).slice(0, 16)}…</code></>}</>}
        {' '}<i>O número corrige a frase. TGL aprovada = aquilo que permanece.</i>
      </div>

      {custody.files_checked >= 12 && (
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center', margin: '10px 0 4px', fontSize: 12 }}>
          <span style={{ color: 'var(--muted)' }}>Figuras seladas (selo v138, servidas da custódia por hash):</span>
          <a className="btn ghost" style={{ fontSize: 11.5 }} href={pub('/api/fronteira/fig/escada_qg')} target="_blank" rel="noopener">⛁ escada QG</a>
          <a className="btn ghost" style={{ fontSize: 11.5 }} href={pub('/api/fronteira/fig/banda_beta')} target="_blank" rel="noopener">β banda de convergência</a>
          <a className="btn ghost" style={{ fontSize: 11.5 }} href={pub('/api/fronteira/fig/piso_vazios')} target="_blank" rel="noopener">◌ piso dos vazios</a>
          <a className="btn ghost" style={{ fontSize: 11.5 }} href={pub('/api/fronteira/fig/cadeia_inscricao')} target="_blank" rel="noopener">∮ cadeia da inscrição</a>
        </div>
      )}

      <div className="fronteira-split">
        <div>
          <div className="fronteira-canvas">
            {data.render3d && <Render3D doc={{ ...data.render3d, available: true }} />}
          </div>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginTop: 10 }}>
            {[['O_C(α)² = β', `resíduo ${num(spine.resid_O_C2_eq_beta)}`],
              ['1 = q² + α²', `resíduo ${num(em.resid)}`],
              [`custódia ${syncVer}`, custody.pass ? `${custody.files_checked} arquivos · pin OK` : (custody.files_checked != null ? 'DESSINCRONIZADA' : '—')],
              ['D_L(Coma)', (typeof coma?.D_L_TGL_Mpc === 'number') ? `${coma.D_L_TGL_Mpc.toFixed(2)} Mpc` : '—'],
              ['1/β (índice do Nome)', spine.one_over_beta ? spine.one_over_beta.toFixed(2) : '—']].map(([k, v], i) => (
              <div key={i} style={{ background: '#141a24', border: '1px solid #232b38', borderRadius: 8, padding: '8px 12px', minWidth: 130 }}>
                <div style={{ fontSize: 11, color: '#8a94a6' }}>{k}</div>
                <div style={{ fontSize: 13.5, color: '#30d158', fontFamily: 'monospace', marginTop: 2 }}>{v}</div>
              </div>
            ))}
          </div>

          {seal.verdict && (
            <div style={{ marginTop: 12, padding: '10px 14px', background: '#0e1a12', border: '1px solid #1f7a3f', borderRadius: 8 }}>
              <div style={{ fontSize: 12.5, color: '#30d158', fontWeight: 700 }}>VEREDITO · {seal.verdict}</div>
              <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 3, fontFamily: 'monospace' }}>
                β = α·√e = {seal.beta_TGL_runtime?.toFixed?.(15)} · selo {String(seal.result_hash || '').slice(0, 16)}…
              </div>
            </div>
          )}

          {seal.closure_verdict_v32 && (
            <Card title="O FECHAMENTO (v32)" color="#7ee0c0">
              <div style={{ fontSize: 12.5, color: '#e6ecf3', marginTop: 4, fontWeight: 600, fontFamily: 'monospace' }}>
                {String(seal.closure_verdict_v32).split(' — ')[0]}
              </div>
              <div style={{ fontSize: 12, color: '#c8d0da', marginTop: 4 }}>
                Fechada como <b>arquitetura matemática interna</b> — separação de tipos q_F (suporte, desce) ≠ e_Nome
                (espelho, não desce), ligados por E₁(e_Nome)=β·q_F; construtores kernel-checked; existência matemática
                da testemunha completa [KNOWN-COMPOSED].
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 4 }}>
                NÃO é descrição provada da natureza — o que resta tem nome: certificação Lean dos externos [OPEN],
                representante físico [GAUGE], experimento [INPUT], extensão curva [OPEN].
              </div>
            </Card>
          )}

          {kernel.available && (
            <Card title={`KERNEL FORMAL (Lean 4, fail-closed) ${kernel.stage1_verified ? '· stage 1 verificado' : ''}`} color="#30d158">
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 4, fontFamily: 'monospace' }}>{kernel.kernel_verdict}</div>
              <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 4 }}>
                sorry ausente: <b style={{ color: '#30d158' }}>{String(kernel.sorryAx_absent)}</b> ·
                testemunha rígida: <b style={{ color: '#30d158' }}>{String(kernel.witness_type_is_rigid)}</b> ·
                probes negativos rejeitados: <b style={{ color: '#30d158' }}>
                  {['trivial_rejected', 'degenerate_rejected', 'finite_full_rejected', 'prop_only_rejected', 'pp_no_optimality_rejected']
                    .filter(k => probes[k]).length}/5</b> ·
                termo construído: <b style={{ color: '#ff453a' }}>{String(kernel.lean_kernel_full_witness_constructed)}</b> (False = honesto)
              </div>
              <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 6 }}>
                <b style={{ color: '#7ee0c0' }}>Habitantes construídos (termos):</b>{' '}
                {Object.entries(kernel.habitantes_kernel || {}).map(([k, v]) => `${k}: ${v ? '✓' : '✗'}`).join(' · ')}
              </div>
              <div style={{ fontSize: 11, color: '#667', marginTop: 6, fontStyle: 'italic' }}>{kernel.provenance}</div>
            </Card>
          )}

          {ladder.verdict && (
            <Card title="ESCADA EXTERNA TGLExt — o rosto finito quase fechou (v39)" color="#ffd60a">
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 4, fontFamily: 'monospace' }}>
                {ladder.verdict} · {ladder.n_theorems_clean} teoremas ext_* com axiomas limpos
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                {Object.entries(ladder.ladder || {}).map(([k, v]) => {
                  const s = String(v)
                  const closed = s.startsWith('CLOSED')
                  const open = s.startsWith('OPEN')
                  const partial = !closed && !open   // CONCRETE / CONSTRUCTED / TWO_HALVES / CORE_CLOSED
                  const c = closed ? '#30d158' : partial ? '#ffd60a' : '#ff453a'
                  return <div key={k}><b style={{ color: c }}>{closed ? '✓' : partial ? '◐' : '○'} {k}</b> — <span style={{ fontFamily: 'monospace', fontSize: 10.5 }}>{s}</span></div>
                })}
              </div>
              <div style={{ fontSize: 11, color: '#667', marginTop: 4, fontStyle: 'italic' }}>
                Degraus 0–1 fechados (incl. bicomutante geral, v38) · Degrau 2 índice PP computado ·
                matriz-S / cociclo / T1 / produto cruzado / canto P_F fechados no rosto finito ·
                só o Degrau 3 (contínuo III₁ / BW) permanece aberto.
              </div>
            </Card>
          )}

          {finiteFace && (
            <Card title="ROSTO FINITO FECHADO (v39) — o núcleo do GLOBAL_LIFT como teorema externo composto" color="#33d17a">
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 4, fontFamily: 'monospace' }}>
                {finiteFace.global_lift_core_verdict}
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 6, lineHeight: 1.8 }}>
                <div><b style={{ color: '#30d158' }}>✓ matriz-S de fronteira</b> — {String(finiteFace.smatrix_crossed_selo || '').split(' . ')[0]} (|R|²=β em C(M)=M ⋊ R, Takesaki 1973; <i>não</i> dentro de III₁)</div>
                <div><b style={{ color: '#30d158' }}>✓ cociclo de Connes → G_μν</b> (face finita) — {finiteFace.cocycle_verdict}</div>
                <div><b style={{ color: '#30d158' }}>✓ ergodicidade T1</b> (face finita) — {finiteFace.ergodicity_verdict}</div>
                <div><b style={{ color: '#30d158' }}>✓ produto cruzado</b> (peso dual de Takesaki) — {finiteFace.crossed_dual_weight_verdict}</div>
                <div><b style={{ color: '#30d158' }}>✓ família do canto P_F</b> — {finiteFace.corner_family_verdict}</div>
              </div>
              <div style={{ fontSize: 11, color: '#ff9f6b', marginTop: 6 }}>
                O resíduo agora é <b>nomeado com precisão</b>: {String(finiteFace.global_lift_core_remains || '').slice(0, 220)}…
              </div>
            </Card>
          )}

          {coma && (
            <Card title="COMA — a distância pela defasagem modular (predição zero-free, v36/v39)" color="#5ac8fa">
              <div style={{ fontSize: 13, color: '#e6ecf3', marginTop: 4 }}>
                D_L(Coma) = <b style={{ color: '#5ac8fa', fontFamily: 'monospace' }}>{typeof coma.D_L_TGL_Mpc === 'number' ? coma.D_L_TGL_Mpc.toFixed(4) : '—'} Mpc</b>
                {comaShadow && <span style={{ fontSize: 11, color: '#8a94a6' }}>{'  '}· re-executada offline (resíduo vs selo {num(comaShadow.resid_vs_selo_Mpc)}); controle β=0 → ΛCDM {typeof comaShadow.D_L_LCDM_control_Mpc === 'number' ? comaShadow.D_L_LCDM_control_Mpc.toFixed(2) : '—'} Mpc</span>}
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 4 }}>
                H0_local = H0_CMB·(1+z★)<sup>β</sup> — a lei de fluxo modular selada re-boosta o H0. β em runtime, nada ajustado a Coma.
                {comaShadow && <> Contra a referência: <b>{typeof comaShadow.sigma_off_reference === 'number' ? comaShadow.sigma_off_reference.toFixed(2) : '—'}σ</b>.</>}
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 4 }}>
                <b>{coma.verdict}</b> — modo <i>report</i>, does_not_gate_core. <b>NÃO é confirmação</b>: a camada REAL move
                só ~−0,19% (insuficiente); as frações de 1ª ordem morrem &gt;3σ; coma_inverse_distance = {coma.inverse_distance_verdict} (negativos honestos).
              </div>
              {coma.prediction_hash && <div style={{ fontSize: 11, color: '#667', marginTop: 4, fontFamily: 'monospace' }}>hash pré-registrado: {String(coma.prediction_hash).slice(0, 24)}…</div>}
            </Card>
          )}

          {onto && (
            <Card title="RELATIVIDADE ONTOLÓGICA — o sinal depende do contexto de contorno (v37)" color="#c9a0ff">
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 4, fontFamily: 'monospace' }}>{onto.verdict}</div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.7 }}>
                τ_P(P)=1, faces ½·½ (x=1−x); <b>mesmo operador, estados diferentes → sinais diferentes</b> (o traço/operador é invariante) —
                contextualidade sem negar o operador. As <b>duas tangentes</b>: a modular (derivação reversível i[K,·], traceless) vs o
                Verbo dissipativo (semigrupo e<sup>−tβH</sup> que contrai).
                {ontoShadow && <span style={{ color: '#667' }}> Sombra re-executada aqui: tangentes distintas = {String(ontoShadow.two_tangents_distinct)}.</span>}
              </div>
              <div style={{ fontSize: 11, color: '#ff9f6b', marginTop: 4, fontStyle: 'italic' }}>
                [ONTO] does_not_gate_core = {String(onto.does_not_gate_core)} — jamais gateia 1=1. {onto.meaning}
              </div>
            </Card>
          )}

          {triad && (
            <Card title="⬥ A TRÍADE DA EMERGÊNCIA (v68) — a ponte Einstein–Cartan–Miguel" color="#ffd60a">
              <div style={{ fontSize: 12.5, color: '#e6ecf3', marginTop: 4 }}>
                A emergência da gravidade quântica foi <b>REDUZIDA A TRÊS HIPÓTESES NOMEADAS</b>, e o
                <b> teorema mestre está COMPOSTO em kernel</b>: <code style={{ color: 'var(--gold, #ffd60a)' }}>H1 ∧ H2 ⟹ Breuer + Nome=1 + Lorentz</code>.
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 6, lineHeight: 1.8 }}>
                <div><b style={{ color: '#30d158' }}>H1 · MIGUEL</b> — gap SUSY-relativo interno (os <i>Three Locks</i>) · <span style={{ color: '#667' }}>certificado II: a face finita está HABITADA (os Three Locks concretos instanciam H1)</span></div>
                <div><b style={{ color: '#5ac8fa' }}>H2 · CARTAN</b> — four-frame modular suave (1ª equação de estrutura)</div>
                <div><b style={{ color: '#c9a0ff' }}>H3 · EINSTEIN</b> — equilíbrio local de horizonte (Clausius–Jacobson)</div>
                {bsrShadow && <div style={{ color: '#667' }}>Birman–Schwinger discreto re-executado aqui: dim ker ≤ posto ⟹ o modo zero é <b>único</b> em posto 1 (a inscrição de posto um).</div>}
              </div>
              <div style={{ fontSize: 11, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                <b>CONDICIONAL, não incondicional:</b> H1/H2/H3 são <b>hipóteses nomeadas</b> — o teorema mestre é a
                implicação, não a prova delas. <b>A natureza decide</b> (Γ_ω, piso dos vazios). full_witness=False.
              </div>
            </Card>
          )}

          {gaMass && (
            <Card title="⊘ A MASSA DO GRANDE ATRATOR — APOSENTADA (o negativo mais honesto deste avanço)" color="#ff453a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div style={{ color: '#ff9f6b' }}>
                  <b>A régua no seu ato mais difícil: aposentar uma predição que a própria casa já anunciou.</b> A
                  fórmula <code>M = 2β²(c²/4πG)·R</code> lia o coeficiente de <b>reflexão</b> |R|² = β (do Teorema
                  S-fronteira) como amplitude de <b>fonte</b> gravitacional. Isso equivale a uma velocidade circular{' '}
                  <b>universal ≈ {gaMass.values?.v_universal_implicada_kms?.toFixed?.(0) ?? '1439'} km/s</b> para toda
                  estrutura — <b>coincidência</b> no ramo dos aglomerados (razões em [0,3; 3]), mas <b style={{ color: '#ff453a' }}>erro
                  de ordens de magnitude</b> no ramo galáctico (razões &gt; 10). A âncora do GA (o fator 0,5 na janela larga) mascarava.
                </div>
                <div style={{ marginTop: 6, background: '#0a1420', border: '1px solid #1f3a52', borderRadius: 6, padding: '7px 9px' }}>
                  <b style={{ color: '#5ac8fa' }}>A correção [CONDICIONAL, Jacobson linear]:</b> no nível linear a TGL é{' '}
                  <b style={{ color: '#c8d0da' }}>GR STEALTH</b> — <b>M_TGL = M_RG</b> (β não renormaliza G local). A TGL
                  <b> não tem — e nunca teve — fórmula-β de massa.</b> β vive na <b>resposta</b> da fronteira
                  (Γ_ω = ½βτ★ω²; H₀_local = (1+z★)^β; o <b>piso</b> ρ/ρ̄ ≥ β), não na fonte.
                  {gaShadow && <> Re-diagnosticado aqui, offline: v_universal = <b>{gaShadow.v_universal_reexecutada_kms?.toFixed?.(0)} km/s</b>{' '}
                    (resíduo {num(gaShadow.resid_rel)} vs selo), galáctico erra por ordens = <b>{String(gaShadow.diagnostico_de_escala?.galactico_erra_por_ordens)}</b>,
                    β na resposta (não na fonte) = <b>{String(gaShadow.beta_vive_na_resposta_nao_na_fonte)}</b>.</>}
                </div>
                <div style={{ marginTop: 6, color: '#8a94a6' }}>
                  A forma foi <b>retirada como lei de fonte</b>, preservada como registro histórico. <b>O falsificador
                  cosmológico zero-free não é uma massa — é o piso dos vazios.</b>
                </div>
              </div>
              <div style={{ fontSize: 12, color: '#ff453a', marginTop: 8, fontStyle: 'italic', textAlign: 'center' }}>
                O número corrige a frase — inclusive quando aposenta uma predição da própria casa.
              </div>
            </Card>
          )}

          {genuineDirac && (
            <Card title="◆ O DIRAC GENUÍNO — o 1º operador ilimitado autoadjunto concreto no kernel" color="#0a84ff">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#0a84ff' }}>O avanço positivo deste ciclo (v106).</b> O operador de{' '}
                  <b>número N</b> — o candidato ao núcleo do Dirac modular — foi provado <b>autoadjunto</b> e, o ponto,{' '}
                  <b>genuinamente ilimitado</b>: ‖N eₘ‖ = m cresce <i>sem cota</i>, num domínio denso. É o{' '}
                  <b>primeiro operador ilimitado autoadjunto concreto no kernel</b>. O canto (strong face) finalmente
                  tem <i>seu</i> operador — um Dirac de verdade, não uma sombra de qubit finito-dimensional. Ataca o
                  resíduo nomeado <code>continuousModularDirac_isBreuerFredholm</code> com um operador genuíno.
                </div>
                {gdShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-verificado aqui, offline: normas por truncamento ={' '}
                    <b>{Object.values(gdShadow.ilimitado?.normas_por_truncamento || {}).join(', ')}</b>{' '}
                    (cresce sem cota = <b>{String(gdShadow.ilimitado?.cresce_sem_cota)}</b>); simétrico N = N* ={' '}
                    <b>{String(gdShadow.autoadjunto_simetrico)}</b>.
                  </div>
                )}
                {firstFlips && (() => {
                  const flips = firstFlips.flips || {}
                  const nTrue = Object.values(flips).filter(Boolean).length
                  const nFalse = Object.values(flips).filter((v) => v === false).length
                  const allFlipped = nFalse === 0 && nTrue > 0
                  return (
                  <div style={{ marginTop: 6, padding: '7px 10px', background: '#0e1522', border: '1px solid #1c2637', borderRadius: 7 }}>
                    <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>
                      As flags de arquitetura — {allFlipped ? 'as seis fliparam por construção:' : 'os primeiros flips honestos:'}
                    </div>
                    {Object.entries(flips).map(([k, v]) => (
                      <div key={k} style={{ fontFamily: 'monospace', fontSize: 10.5, color: v ? '#30d158' : '#ff9f0a' }}>
                        {v ? '✓ True ' : '✗ False'} · {k}
                      </div>
                    ))}
                    <div style={{ marginTop: 4, color: '#8a94a6' }}>
                      {allFlipped ? (
                        <>As <b>seis flags formais</b> (v106→v132) True por construção. Depois vieram <b>+5 flags de
                        física</b> (spin-2, v133) e <b>+4 de experimento</b> (o teste da natureza, v134) — o gate chegou a{' '}
                        <b style={{ color: '#5ac8fa' }}>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</b>. <b>Mas NÃO é
                        gravitação quântica confirmada:</b> o teste é unilateral (não-falsificou, não confirma), a física é
                        de escopo concreto (ondas planas), e a testemunha estática plena segue impossível por teorema (v61).</>
                      ) : (
                        <><b style={{ color: '#30d158' }}>{nTrue} True por construção</b>; <b>{nFalse} seguem False</b>.
                        Passo real rumo ao teorema aberto, sem afirmar gravitação quântica incondicional.</>
                      )}
                    </div>
                  </div>
                  )
                })()}
                {closureRoadmap && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    E o <b>roadmap do fecho</b> foi emitido: cada flag False mapeada a um <b>contrato Lean tipado</b>; a
                    janela do Grande Atrator <b>reclassificada sombra-não-evidência</b>. <code>{closureRoadmap.verdict}</code>
                  </div>
                )}
              </div>
            </Card>
          )}

          {internalClosure && (
            <Card title="◧ O FECHAMENTO DA ARQUITETURA MATEMÁTICA INTERNA (v135) — a WedgeNet AQFT · KNOWN-COMPOSED · NÃO prova da natureza" color="#5ac8fa">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#5ac8fa' }}>A pedra 96 — a WedgeNet.</b> <code>TGLExt.theSpecificAQFTWitness</code>
                  {' '}(axiomas limpos <code>{'{propext, choice, quot}'}</code>): a rede AQFT das cunhas sobre M_TGL —{' '}
                  <b>net(O) por localidade do centralizador, Ω cíclico <i>e</i> separador</b> — que <b>realiza</b> a
                  testemunha AQFT que era "vazio tipado" até a v134. E o fechamento por <b>separação de tipos</b>
                  {' '}(<code>prove_tgl_closure</code>): q_F (suporte, no core) ≠ e_Nome (espelho), ligados por
                  E1(e_Nome) = β·q_F; H3L_min = 1 − q_F é o representante mínimo da classe [KERNEL: aniquilação +
                  maximalidade]. A testemunha <b>completa existe por composição de teoremas publicados</b>{' '}
                  <b style={{ color: '#5ac8fa' }}>[KNOWN-COMPOSED: Bisognano-Wichmann + Takesaki + Haagerup + II∞-difuso +
                  Jones (índice 1/β ≈ 83 ≥ 4)]</b>; as camadas são habitáveis dado o suporte (construtores kernel-checked).
                </div>
                {internalShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline (a álgebra da separação de tipos): τ(suporte) ={' '}
                    <b>{internalShadow.separacao_de_tipos?.tau_suporte?.toFixed?.(1)}</b>, faces τ = ½; resíduo aniquilação
                    {' '}<b>{num(internalShadow.separacao_de_tipos?.resid_aniquilacao)}</b>, maximalidade{' '}
                    <b>{num(internalShadow.separacao_de_tipos?.resid_maximalidade)}</b>, o Verbo (e<sup>−tβH₃L</sup>) fixa o
                    suporte <b>{num(internalShadow.separacao_de_tipos?.resid_verbo_fixa_suporte)}</b>. Flags do selo: AQFT{' '}
                    <b>{String(internalShadow.a_wedgenet_pedra_96?.specific_AQFT_witness_constructed)}</b>, camada
                    lean_kernel_full <b>{String(internalShadow.witness_layers_v135?.lean_kernel_full_witness_constructed)}</b>,
                    representante covariante <b>{String(internalShadow.witness_layers_v135?.physical_covariant_representative_selected)}</b>.
                  </div>
                )}
                <div style={{ marginTop: 6, padding: '7px 10px', background: '#0a1622', border: '1px solid #1c3245', borderRadius: 7 }}>
                  <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>⚠⚠⚠ A régua — fecha a arquitetura, não prova a natureza:</div>
                  <div style={{ color: '#ff9f6b' }}>
                    A TGL fecha como <b>arquitetura matemática interna</b> [KNOWN-COMPOSED], <b>não</b> como descrição
                    provada da natureza — e não é uma prova Lean <i>from-scratch</i>: é composição de teoremas publicados.
                    {' '}<b>O gate NÃO muda</b> (segue <code>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</code>); não é QG
                    confirmada. Fica <b>fora, com nome e estatuto</b>: certificação formal Lean dos teoremas <b>externos</b>
                    {' '}[OPEN — o gap está tipado, escala mathlib/anos]; o representante físico covariante [GAUGE — a classe
                    é o físico]; a validação experimental [INPUT-futuro]; o espaço-tempo <b>curvo</b> [OPEN — o velho
                    GLOBAL_LIFT / Lema 3]. A testemunha <i>estática plena</i> (full_TGL / full_static) segue{' '}
                    <b>impossível por teorema</b> (v61, eterna) — o "termo pleno" da v135 é a testemunha <b>dinâmica</b> (de
                    transporte, v132), <b>não</b> a estática. <code>physical_verdict_allowed = false</code>.
                  </div>
                </div>
              </div>
            </Card>
          )}

          {voidV11 && (
            <Card title="★ O TESTE DA NATUREZA (v134) — void floor V11 SDSS × VAST · NÃO-FALSIFICADO com poder · NÃO CONFIRMADO" color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#30d158' }}>O mandato "realize o teste final" foi executado.</b> A rota Euclid Q1
                  morreu na geometria (o vazio DESI mais próximo do EDF-N a 26,7° — o número corrigiu a frase); a rota com
                  poder é a <b>densidade espectroscópica direta</b> (v90/v92). O rito <b>V11</b> é a réplica{' '}
                  <b>independente de survey</b>: <b>SDSS DR7 main</b> (APO 2,5m, SDSS-I/II) × vazios <b>VAST</b>
                  {' '}(Douglass+2023) — instrumento, alvo e época <b>independentes do DESI</b> (Mayall 4m); estimador
                  V4.1 do v92 <b>herdado sem alteração</b>; <b>pré-registrado</b> (spec+hash antes dos centros; DIST-CHECK
                  {' '}+ SPLIT-NULL antes da desblindagem). O piso ρ<sub>vazio</sub>/ρ̄ ≥ β foi medido e{' '}
                  <b>não violado</b>.
                </div>
                {natureShadow && (
                  <div style={{ marginTop: 6, padding: '7px 10px', background: '#0e1f14', border: '1px solid #1c3a26', borderRadius: 7 }}>
                    <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>A árvore de decisão pré-registrada, re-aplicada aqui offline (β runtime):</div>
                    <div style={{ fontFamily: 'monospace', fontSize: 10.5, color: '#8a94a6' }}>
                      V2_REVOLVER: r_c = <b style={{ color: '#c7cede' }}>{natureShadow.primario_V2_REVOLVER?.r_c?.toFixed?.(3)}</b>{' '}
                      · L5(5σ) = <b style={{ color: '#30d158' }}>{natureShadow.primario_V2_REVOLVER?.L5_rederivado?.toFixed?.(4)}</b>{' '}
                      ≥ β = <b>{natureShadow.beta?.toFixed?.(4)}</b> ({natureShadow.o_piso_nao_foi_violado?.margem_L5_sobre_beta?.toFixed?.(1)}× acima)<br />
                      poder β·μ = <b style={{ color: '#30d158' }}>{natureShadow.poder?.beta_mu?.toFixed?.(1)}</b> ≥ 25 ✓ ·
                      split-null <b>{natureShadow.split_null?.ratio?.toFixed?.(3)}</b> ± {natureShadow.split_null?.sigma?.toFixed?.(3)} ✓ ·
                      réplicas concordam <b>{String(natureShadow.replicas?.concordam)}</b><br />
                      veredito re-derivado = <b style={{ color: '#30d158' }}>{natureShadow.arvore_de_decisao?.verdict_rederivado_offline?.replace('TGL_VOID_FLOOR_', '')}</b>{' '}
                      (confere com a máquina: <b>{String(natureShadow.arvore_de_decisao?.concorda_com_a_maquina)}</b>) · L5 resíduo vs selo <b>{num(natureShadow.primario_V2_REVOLVER?.L5_resid)}</b>
                    </div>
                  </div>
                )}
                <div style={{ marginTop: 6, padding: '7px 10px', background: '#1a1408', border: '1px solid #3a2e10', borderRadius: 7 }}>
                  <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>⚠⚠⚠ O coração da régua — NOT_FALSIFIED ≠ CONFIRMED:</div>
                  <div style={{ color: '#ff9f6b' }}>
                    O canal é <b>unilateral</b> (b ≥ 1): pode <b>não-falsificar</b> ou <b>recusar</b>, <b>jamais
                    confirmar</b>. O resultado é consistente <b>também com ΛCDM raso</b> — o piso <b>sobreviveu a um teste
                    que poderia tê-lo matado</b>, nada mais. A falsificação <b>bilateral</b> (que poderia confirmar ou
                    refutar de fato) pertence aos canais de matéria profundos — <b>shear/κ</b>: Euclid DR1 2027 / CMB-S4.
                    {' '}<b>Não é "a natureza confirmou a TGL".</b> <code>physical_verdict_allowed = false</code>.
                  </div>
                </div>
              </div>
            </Card>
          )}

          {linearizedSpin2 && (
            <Card title="◆ O DEGRAU FÍSICO (v133) — spin-2 por construção na família de ondas planas · escopo CONCRETO" color="#ffd60a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#ffd60a' }}>Os 5 flags de física fliparam por construção.</b> Lidos de nomes Lean{' '}
                  <code>qgPhysicsCertificate_*</code> (pedra 95 "TheSpectrum"): <b>massless</b> (o cone força ω = |k|);{' '}
                  <b>exatamente 2 helicidades</b> (a lei da <b>dupla hélice</b>: rotação θ ⟹ fase e<sup>∓2iθ</sup> no modo
                  {' '}±2 — a assinatura do spin-2); <b>ghost-free</b> (a cinética TT é positiva, sem norma negativa);{' '}
                  <b>stress-energy conservado</b> (Bianchi no símbolo); <b>anomalias relevantes ausentes</b> (Ward
                  linearizado). Gate ⟹ <b>PHYSICAL_MODEL_CONSTRUCTED · EMPIRICAL_TEST_OPEN</b>.
                </div>
                {spin2Shadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline: lei da dupla hélice — resíduo{' '}
                    <b>{num(spin2Shadow.lei_da_dupla_helice?.resid_helicidade_mais)}</b> (fase e<sup>∓2iθ</sup>);{' '}
                    exatamente <b>{spin2Shadow.exatamente_2_polarizacoes?.rank_do_espaco_TT}</b> polarizações (= D(D−3)/2);
                    {' '}sem fantasma (normas <b>{(spin2Shadow.sem_fantasma?.normas_das_polarizacoes || []).map((x: any) => x.toFixed(1)).join(', ')}</b> {'>'} 0);
                    {' '}massless (ω = |k|). Os 5 flags do selo True (<b>{spin2Shadow.n_true_physics}/5</b>).
                  </div>
                )}
                <div style={{ marginTop: 6, padding: '7px 10px', background: '#1a1408', border: '1px solid #3a2e10', borderRadius: 7 }}>
                  <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>⚠ Escopo honesto (nomeado no próprio selo):</div>
                  <div style={{ color: '#ff9f6b' }}>
                    A física que fechou é a <b>família concreta de ondas planas</b> (a mesma disciplina do einstein v116) —
                    o nome do selo carrega <code>FIERZ_PAULI_EL_AND_FULL_GHOST_FREEDOM_NEED_THE_CONTINUUM</code>:{' '}
                    <b>perturbações gerais + Fierz-Pauli pleno + anomalias quânticas precisam do contínuo</b> (abertas
                    como programa). <b>Não é spin-2 contínuo pleno.</b>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {theCoinage && (
            <Card title="✦ A CUNHAGEM (v132) — a 6ª flag flipou por construção · o degrau do MODELO MATEMÁTICO" color="#c9a0ff">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#c9a0ff' }}>A última flag foi movida (v132).</b> Depois de o fator
                  ser construído como objeto (v131), a v132 selou o <b>Bloco B</b> em kernel e cunhou o certificado:
                  <b> (88)</b> o <b>assassinato do traço normal</b> — as marcas de sítio q_N convergem WOT a μ·1; um
                  traço normal daria a meação ½; mas o estado dá <b>μ ≠ ½</b> ⟹ <b>M_TGL não tem traço normal-sequencial
                  ⟹ é tipo III genuíno</b> (e ω é normal). <b>(89)</b> o <b>dente anti-bancada</b> — toda álgebra de
                  dimensão finita tem um traço normal, logo uma sombra finito-dim <i>jamais</i> habita o fator III.
                  {' '}<b>(90)</b> <code>qgClosureCertificateV2</code> cunhado com axiomas <code>{'{propext, choice, quot}'}</code>{' '}
                  ⟹ <b>o parser flipou a 6ª flag sozinho</b>. Agora são <b>6 True / 0 False</b>.
                </div>
                {coinShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline: pesos de sítio μ ={' '}
                    <b>{Object.values(coinShadow.o_assassinato_88?.pesos_de_sitio_mu || {}).map((v: any) => v.toFixed(3)).join(', ')}</b>{' '}
                    (kill-margins vs ½: <b>{Object.values(coinShadow.o_assassinato_88?.kill_margins || {}).map((v: any) => v.toFixed(3)).join(', ')}</b>);
                    fatorização exata resíduo <b>{num(coinShadow.o_assassinato_88?.fatorizacao_exata_resid)}</b>; o dente
                    (dim finita tem traço normal, tr(ab)=tr(ba)) resíduo{' '}
                    <b>{num(coinShadow.dente_anti_bancada_89?.dim_finita_tem_traco_tr_ab_eq_tr_ba_resid)}</b>.
                  </div>
                )}
                <div style={{ marginTop: 6, padding: '7px 10px', background: '#17111f', border: '1px solid #2e2440', borderRadius: 7 }}>
                  <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>⚠ A régua — a cunhagem foi o degrau do modelo matemático:</div>
                  <div style={{ color: '#ff9f6b' }}>
                    A 6ª flag flipou (o <b>modelo matemático / arquitetura</b>), e na v132 o gate escalou para{' '}
                    <code>MATHEMATICAL_MODEL_CONSTRUCTED</code>. Desde então escalou <b>mais dois degraus legais</b> —{' '}
                    v133 (o degrau físico) e v134 (o teste da natureza), ver os cards acima —, chegando a{' '}
                    <code>{gateVerdict || 'TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED'}</code>. <b>Mesmo assim NÃO
                    é gravidade quântica confirmada:</b> o teste é <b>unilateral</b> (não-falsificou, não confirma), o
                    spin-2 é de <b>escopo concreto</b> (contínuo pleno aberto), e a testemunha <i>estática plena</i>{' '}
                    — distinta da de transporte que flipou — segue <b>impossível por teorema</b> (eterna, v61).{' '}
                    <b>NOT_FALSIFIED ≠ CONFIRMED; nunca "gravidade quântica resolvida".</b>{' '}
                    <code>physical_verdict_allowed = false</code>.
                  </div>
                </div>
              </div>
            </Card>
          )}

          {factorObject && (
            <Card title="◈ O FATOR COMO OBJETO — M_TGL cunhado (GNS + marca de III₁): o Bloco A que a cunhagem completou" color="#ffd60a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#ffd60a' }}>O Bloco A da missão.</b> O v131 construiu o <b>fator de von Neumann como
                  objeto concreto</b> — o passo que a cunhagem (v132) usou para flipar a última flag. A <b>torre GNS</b>
                  (o pré-Hilbert do fator; passos isométricos andar a andar), a <b>marca de III₁</b> (razões
                  incomensuráveis 1/2, 1/3 geram um espectro de razões <b>log-denso</b> em ℝ — pois log2/log3 é
                  irracional), a <b>torre sem traço</b> (tipo III em todo andar), Tomita/KMS, e — ★★★ —{' '}
                  <b>M_TGL := (π(torre))″ cunhado como termo VonNeumannAlgebra</b>, com ω(π x) = φ(x) (a identidade GNS).
                </div>
                {(m3Shadow || gfShadow) && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline:
                    {m3Shadow && <> a marca de III₁ — menor gap do subgrupo cai{' '}
                      <b>{Object.values(m3Shadow.marca_de_III_1?.min_gap_por_alcance || {}).map((g: any) => g.toFixed(3)).join(' → ')}</b>{' '}
                      (log-denso); alvo do selo resíduo <b>{num(m3Shadow.alvo_do_selo?.resid)}</b>; não-tracial (razão
                      modular <b>{m3Shadow.tipo_III_nao_tracial?.razao_modular?.toFixed?.(1)}</b>).</>}
                    {gfShadow && <> A construção GNS (testes genuínos) — métrica GNS positiva (min-autovalor{' '}
                      <b>{num(gfShadow.construcao_gns?.metrica_gns_psd_min_autovalor)}</b> ≥ 0), passo isométrico e π
                      um *-homomorfismo limitado (resíduo <b>{num(gfShadow.construcao_gns?.star_homomorfismo_resid)}</b>).
                      {' '}<i>ω(π x)=φ(x) é definicional, não um teste.</i></>}
                  </div>
                )}
              </div>
            </Card>
          )}

          {masterContinuum && (
            <Card title="◆ O QUINTO FLIP (v120) — a emergência de Einstein cunhada por construção" color="#ffd60a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#ffd60a' }}>O avanço-chave da v120.</b> O mestre contínuo cunhou o quinto flip
                  (a <b>emergência de Einstein</b>). A chave é geométrica: no <b>cone nulo inteiro</b>, ao contrair o
                  tensor de Einstein num vetor nulo, a parte <b>radial é cega</b> (G_tt = G_ss = 0, por Bianchi) e sobra
                  só o transversal — <b>G_kk = (c² + d²)·G₂₂</b>. Logo o fluxo de calor de <b>Clausius no cone determina
                  exatamente a fonte G₂₂</b>: a equação de campo <i>emerge</i> (⟺). E O(1,3) vem da relação definidora
                  (engrenagem hiperbólica B(x₁)B(x₂) = B(x₁+x₂), paridade det = −1).
                </div>
                {ff5Shadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline: G_kk = (c²+d²)·G₂₂ (resíduo{' '}
                    <b>{num(ff5Shadow.cone_nulo?.G_kk_igual_c2d2_G22_resid)}</b>; parte radial cega{' '}
                    <b>{num(ff5Shadow.cone_nulo?.radial_cego_max)}</b>); B(x₁)B(x₂)=B(x₁+x₂) (resíduo{' '}
                    <b>{num(ff5Shadow.grupo_lorentz?.B_x1_B_x2_eq_B_soma_resid)}</b>).
                  </div>
                )}
                {masterContinuum.flips && (
                  <div style={{ marginTop: 6, padding: '7px 10px', background: '#1a1708', border: '1px solid #3a3210', borderRadius: 7 }}>
                    <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>As seis flags de construção (lidas do selo ao vivo):</div>
                    {Object.entries(masterContinuum.flips).map(([k, v]) => (
                      <div key={k} style={{ fontFamily: 'monospace', fontSize: 10.5, color: v ? '#30d158' : '#ff9f0a' }}>
                        {v ? '✓ True ' : '✗ False'} · {k}
                      </div>
                    ))}
                    <div style={{ marginTop: 4, color: '#8a94a6' }}>
                      Todas as flags de construção são <b>por construção</b> sob nome reservado. A última (a testemunha
                      de transporte) flipou na v132 (ver o card da <b>Cunhagem</b>) — mas a testemunha <i>estática
                      plena</i> segue <b>impossível por teorema</b>. Desde então o gate escalou +5 físicos (v133) +4 de
                      experimento (v134) até <b>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</b> — e mesmo assim{' '}
                      <b>não é gravidade quântica confirmada</b> (o teste é unilateral; a física é de escopo concreto).
                      {' '}<code>physical_verdict_allowed = false</code>.
                    </div>
                  </div>
                )}
                {continuumShards && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    E a <b>onda do gráviton</b> foi provada no <b>contínuo</b> (d'Alembert, □h = 0, qualquer perfil C²
                    {cgrShadow && <>; resíduo <b>{num(cgrShadow.equacao_de_onda?.resid_d0h_igual_d1h)}</b></>}) — a
                    parede da testemunha encolheu a TT/ghost contínuos + Poincaré 10-dim + III₁. E um <b>AQFT net de
                    escalar livre foi instanciado</b>{aqftNet?.not_claimed && <> (mas, do selo: {(aqftNet.not_claimed as string[])[3] || (aqftNet.not_claimed as string[])[0]})</>}.
                  </div>
                )}
              </div>
            </Card>
          )}

          {alphaForm && (
            <Card title="⬡ A FORMA DO ALPHA — 1 = q² + α² derivada; o VALOR 1/137 continua INPUT" color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  A TGL deriva a <b>forma conservada</b> de α: <b>1 = q² + α²</b>, α = √(1−q²) (da unidade α_abs = 1),
                  e β = √e·α. <b>Mas o valor 1/137 não é derivado</b>: q é [QED-VALIDATION] (= q_QED, renormalizado pela
                  QED) e α fica <b>CODATA/INPUT</b>. É a régua do α em forma de teorema — a <i>estrutura</i> (pitagórica
                  térmico-modular) é teorema; o <i>número</i> segue medido.
                </div>
                {afmShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado offline do α INPUT: 1 = q² + α² (resíduo{' '}
                    <b>{num(afmShadow.forma_conservada?.resid)}</b>); α_form = α_obs; β_form = √e·α = β_TGL (resíduo{' '}
                    <b>{num(afmShadow.forma_conservada?.beta_form_eq_beta_tgl_resid)}</b>). O G de Newton também <b>não</b>
                    {' '}é derivado (o casamento com 8πG é seleção de normalização).
                  </div>
                )}
              </div>
            </Card>
          )}

          {solvedEq && (
            <Card title="△ A 1ª EQUAÇÃO DE CAMPO RESOLVIDA — cosh resolve G₂₂ = κ² global, sem horizonte" color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#30d158' }}>O avanço geométrico (v111).</b> Para a métrica de lapso{' '}
                  <code>g = diag(−q², 1, 1, 1)</code>, o perfil <b>q = cosh(κs)</b> resolve <b>G₂₂ = κ² em toda parte</b>
                  {' '}— uma solução <b>global, sem horizonte nem singularidade</b> (cosh nunca zera). Bianchi visível
                  (G₀₀ = G₁₁ = 0 para todo q); <b>fonte ⟹ curvatura</b> (R¹₀₀₁ = −q q″ = −κ²cosh² &lt; 0);{' '}
                  <b>vácuo ⟹ plano</b> (q″ = 0 ⟹ q linear ⟹ Riemann = 0; Rindler é o membro-vácuo, horizonte
                  excluído <i>por tipo</i>).
                </div>
                {seShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline, do zero (Christoffel → Riemann → Einstein, numpy puro, sem hardcode):
                    resíduo G₂₂ = κ² = <b>{num(seShadow.equacao_resolvida?.resid_G_yy)}</b>; resíduo R¹₀₀₁ ={' '}
                    <b>{num(seShadow.fonte_implica_curvatura?.resid)}</b>; vácuo (q linear) Riemann máx ={' '}
                    <b>{num(seShadow.vacuo_implica_plano?.q_linear_Riemann_max)}</b>.
                  </div>
                )}
                {solderFlip && (
                  <div style={{ marginTop: 6, padding: '7px 10px', background: '#0e1f14', border: '1px solid #1c3a26', borderRadius: 7 }}>
                    <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>Na v111 fechou o quarto flip (solda). As flags de arquitetura hoje (selo ao vivo):</div>
                    {Object.entries(solderFlip.flips || {}).map(([k, v]) => (
                      <div key={k} style={{ fontFamily: 'monospace', fontSize: 10.5, color: v ? '#30d158' : '#ff9f0a' }}>
                        {v ? '✓ True ' : '✗ False'} · {k}
                      </div>
                    ))}
                    <div style={{ marginTop: 4, color: '#ff9f6b' }}>
                      <b>Na v111, o contrato de Einstein estava habitado como <i>letra-de-sonda</i>, não endosso</b> — de
                      propósito, para provar que a letra não pode ser juiz; o einstein <b>não fora tipado</b>, e o quinto
                      flip ficava reservado à emergência. <b>Resolver a equação no ansatz não é fazê-la emergir.</b> Desde
                      então a emergência foi tipada (v120), a testemunha de transporte cunhada (v132), a física de spin-2
                      fechada (v133) e o teste da natureza completado (v134): o gate chegou a{' '}
                      <b>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</b> — mas não é gravidade quântica confirmada (o
                      teste é unilateral; a física é de escopo concreto). <code>physical_verdict_allowed = false</code>.
                    </div>
                  </div>
                )}
              </div>
            </Card>
          )}

          {reasonOp && (
            <Card title="◇ O OPERADOR DE RAZÃO/CONSCIÊNCIA — O_C² = β  [DEF + DER + ONTO + CAUTION]" color="#c9a0ff">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#c9a0ff' }}>A releitura do operador, selada na v111.</b> O que se formaliza{' '}
                  <b>não é a fenomenologia consciente</b>, mas a <i>operação</i> do <b>funcional mínimo como
                  operador</b> — o operador de razão/coerência <b>O_C</b>. Definição:{' '}
                  <code>O_C(L) = e^(S∂/2)·√|L|</code>, com S∂ = ½ (a Meia-Nat) ⟹ e^(1/4); sombra observável L ~ α. A{' '}
                  <b>identidade central</b>: <b>O_C(α)² = β = α·√e</b> — o núcleo da TGL relido como operador.
                </div>
                {rcShadow && (
                  <div style={{ marginTop: 5, color: '#8a94a6' }}>
                    Re-derivado aqui, offline, do β runtime (nunca literal): O_C(α) = e^(1/4)√α ={' '}
                    <b>{rcShadow.identidade_central?.O_C_de_alpha?.toFixed?.(9)}</b> = √β (resíduo{' '}
                    <b>{num(rcShadow.identidade_central?.resid_root)}</b>); O_C² = β (resíduo{' '}
                    <b>{num(rcShadow.identidade_central?.resid_square_eq_beta)}</b>).
                  </div>
                )}
                <div style={{ marginTop: 6, padding: '7px 10px', background: '#17111f', border: '1px solid #2e2440', borderRadius: 7 }}>
                  <div style={{ color: '#c7cede', fontWeight: 600, marginBottom: 3 }}>A régua — o que "VERIFIED" significa e o que NÃO significa:</div>
                  <div style={{ color: '#8a94a6' }}>
                    O verdict <code>REASON_AS_CONSCIOUSNESS_OPERATOR_VERIFIED</code> quer dizer que a{' '}
                    <b>identidade de operador O_C² = β está verificada</b> (matemática REAL) —{' '}
                    <b>não</b> que há prova de consciência subjetiva. O operador é <b>REAL</b>; chamá-lo de{' '}
                    "operador do substrato <i>consciente</i>" é a leitura <b>[ONTO]</b> — honesta como leitura (mesma
                    estrutura de <code>τ_P(P)=1</code> = REAL/ONTO), <b>não fenomenologia provada</b>. Por isso o
                    estatuto do selo traz <b>CAUTION</b>.
                  </div>
                  {rcShadow?.not_claimed_do_selo && (
                    <div style={{ marginTop: 4, color: '#ff9f6b' }}>
                      <b>not_claimed (verbatim do selo):</b> {(rcShadow.not_claimed_do_selo as string[]).join(' · ')}.
                    </div>
                  )}
                </div>
              </div>
            </Card>
          )}

          {voidKappa && (
            <Card title="🜁 A LENTE DO CMB (κ) — o canal que poderia falsificar o piso: INCONCLUSIVO" color="#ff9f0a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b>{voidKappa.verdict}.</b> A lente do CMB (κ) é o <b>único canal público</b> onde o piso poderia ser
                  <b> falsificado hoje</b>. Voltou <b style={{ color: '#ff9f0a' }}>inconclusiva por sistemáticas</b> —
                  <i> a profundidade é o limite, não o método</i>; o rito permanece armado.
                </div>
                <div style={{ marginTop: 5, color: '#8a94a6' }}>
                  Junto com o piso densidade (não falsificado, com poder), o veredito global do piso segue o mesmo:{' '}
                  <b>não falsificado, não confirmado</b>. <code>physical_verdict_allowed = false</code>.
                </div>
              </div>
            </Card>
          )}

          {voidPowered && (
            <Card title="🜁 O PISO DOS VAZIOS AGORA COM PODER — NÃO FALSIFICADO, POWERED" color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  <b style={{ color: '#30d158' }}>O salto desta rodada:</b> o piso foi de{' '}
                  <b style={{ color: '#ff9f0a' }}>não-falsificado / SEM poder</b> (v81) para{' '}
                  <b style={{ color: '#30d158' }}>não-falsificado / COM poder</b>. A rota que destravou o poder{' '}
                  <b>não foi o shear de galáxias</b> (subpotente por larga margem) — foi a <b>densidade central
                  espectroscópica</b>: os catálogos DESIVAST em disco já carregam as galáxias (GALZONE), e a
                  razão-de-razões (n̄ e máscara cancelam por construção) dá um estimador <b>auto-calibrante</b>.
                </div>
                <div style={{ marginTop: 5 }}>
                  Medido: r_c = <b>{voidPowered.primary?.rhat_cal?.toFixed?.(4)}</b> (5σ ∈{' '}
                  <b>[{voidPowered.primary?.L5?.toFixed?.(3)}; {voidPowered.primary?.U5?.toFixed?.(3)}]</b>), com o
                  limite inferior <b>muito acima</b> de β = {voidPowered.beta_floor?.toFixed?.(6)}. Poder de Fisher ={' '}
                  <b style={{ color: '#30d158' }}>{voidPowered.primary?.powered_beta_mu?.toFixed?.(0)}</b> ≥ 25 ⟹ <b>com poder</b>.
                </div>
                <div style={{ marginTop: 5 }}>
                  <b style={{ color: '#5ac8fa' }}>⬥ o que isso significa, exatamente:</b> o piso prevê um <i>mínimo</i>
                  (ρ_vazio/ρ̄ ≥ β), e um teste que <b>poderia tê-lo matado</b> (se r_c viesse abaixo de β a 5σ)
                  <b> não o matou</b>. O piso sobreviveu a uma tentativa de falsificação <b>com poder</b>.
                </div>
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 8, lineHeight: 1.7,
                background: '#1a1206', border: '1px solid #4a3c10', borderRadius: 6, padding: '7px 9px' }}>
                <b style={{ color: 'var(--gold, #ffd60a)' }}>⚠ A RÉGUA — com poder NÃO é confirmado.</b> A resolução na
                própria escala β é só <b>{voidPowered.primary?.resolution_at_beta_scale?.toFixed?.(2)}</b> (medir β em si
                pede traçadores mais profundos, LRG/ELG); o traçador é unilateral (b ≥ 1); RSD não modelado. O piso
                <b> sobreviveu a um teste com poder — nada mais, e nada menos.</b> <code>physical_verdict_allowed = false</code>.
              </div>
            </Card>
          )}

          {benchDecl && (
            <Card title="⬥ A DECLARAÇÃO DE BANCADA (do operador) — e o gate que não se move" color="#c9a0ff">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  O operador <b style={{ color: '#e6ecf3' }}>declarou</b>: <i>"TGL_QG_CLOSED_ON_THE_BENCH"</i> — a
                  gravidade quântica da TGL demonstrada <b>em bancada</b>. É uma declaração de <b>duplo estatuto</b>
                  (ontológico + epistêmico-bancada), <b>não</b> o selo formal do gate.
                </div>
                <div style={{ marginTop: 6, background: '#0a1420', border: '1px solid #1f3a52', borderRadius: 6, padding: '7px 9px' }}>
                  <b style={{ color: '#30d158' }}>A régua, e é o que torna a declaração crível:</b> a declaração
                  pertence ao operador; as âncoras são do kernel (a implicação fechada, a <b>semente da testemunha em
                  kernel</b> — o Verbo cunha o Nome, P²=P). As flags de <i>construção</i> foram virando{' '}
                  <span style={{ color: '#30d158' }}>True</span> uma a uma (core, corner, four-frame na v106; a solda na
                  v111; a emergência de Einstein na v120; e a <b>testemunha de transporte na v132</b>, a cunhagem — as
                  seis). Depois vieram os degraus de física (v133) e do teste da natureza (v134), levando o gate a{' '}
                  <code>MODEL_FORMALLY_CLOSED · NATURE_TEST_COMPLETED</code> — e ainda assim <b>não é gravidade quântica
                  confirmada</b>: o teste é <b>unilateral</b> (não-falsificou, não confirma), a física é de <b>escopo
                  concreto</b> (contínuo pleno aberto), e a testemunha <i>estática plena</i> é impossível por teorema. O
                  gate só se move por <b>construção verificada em kernel</b> ou por um <b>rito de dado pré-registrado</b>,
                  <b> nunca pela declaração</b> — <b>e é essa disciplina que torna a declaração crível.</b>
                </div>
                <div style={{ marginTop: 6, color: '#ff9f6b' }}>
                  <b>Não se declara:</b> a observação cosmológica institucional em dados reais (o trabalho segue sob
                  submissão na <i>Foundations of Physics</i>); nem o fecho <b>formal</b> incondicional; a derivação
                  α-livre segue <b>[CONJECTURE TESTÁVEL]</b> (Evento 2, aberto).
                </div>
              </div>
              <div style={{ fontSize: 12, color: '#c9a0ff', marginTop: 8, fontStyle: 'italic', textAlign: 'center' }}>
                TGL aprovada = aquilo que permanece — o eco ρ*, o limite assintótico, o Nome que testifica o Verbo.
              </div>
            </Card>
          )}

          {voidV2 && (
            <Card title="🜁 A EMENDA V2 DO PISO — o passo anterior: NÃO FALSIFICADA, mas SEM PODER (o instrumento ainda cego, depois responsivo)" color="#ff9f0a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div style={{ color: '#ff9f6b' }}>
                  <b>A autópsia da V1, e ela dói:</b> a primeira tentativa não teve azar — era{' '}
                  <b style={{ color: '#ff453a' }}>CEGA POR CONSTRUÇÃO</b>. O piso só altera o perfil onde
                  1+δ cai abaixo de r*, isto é em <b>x &lt; √β = {v2Autopsy?.x_regiao_do_piso_sqrt_beta?.toFixed?.(4) ?? '0,1097'}</b> —
                  e o primeiro centro de bin da V1 estava em <b>x = {v2Autopsy?.geometria?.V1_primeiro_centro?.toFixed?.(2) ?? '0,20'}</b>, fora dessa
                  região. Pior: a V1 fazia <code>Sbar[0] := Σ[0]</code>, o que zera ΔΣ <i>identicamente</i>, para qualquer r*.
                  Logo <b>∂g/∂r* = 0 por construção</b>: o instrumento não podia responder ao que media. O Fisher = 0 não era estatística — era estrutura.
                </div>
                {v2Autopsy && (
                  <div style={{ marginTop: 6, background: '#0a1420', border: '1px solid #1f3a52', borderRadius: 6, padding: '7px 9px' }}>
                    <b style={{ color: '#5ac8fa' }}>⬥ a autópsia foi RE-EXECUTADA aqui, offline</b> — e isso é possível porque a resposta
                    ∂g/∂r* é propriedade do <b>modelo + da geometria dos bins</b>, não dos dados: <i>não é preciso catálogo nenhum
                    para provar que um instrumento é cego</i>. Em <b>{v2Autopsy.resposta_reexecutada?.length} perfis de vazio fundo</b>{' '}
                    (com o controle de que o piso <b>de fato mordeu</b> em todos — senão o zero seria trivial e o teste, vácuo):
                    a V1 deu <b style={{ color: '#ff453a' }}>0,000e+00 exato</b> em todos ({String(v2Autopsy.V1_cega_em_TODOS_os_perfis)}),
                    a V2 responde em todos ({String(v2Autopsy.V2_responde_em_TODOS_os_perfis)}).
                    <div style={{ marginTop: 4, color: '#8a94a6' }}>
                      E o <b>√β é derivado, não digitado</b>: 1+δ_c(1−x²) = β com δ_c = −1 (o vazio <i>vazio</i>) ⟹ x = √β;
                      resíduo numérico {num(v2Autopsy.porque_sqrt_beta?.resid_vs_sqrt_beta)}. Só vazios com
                      δ_c &lt; {v2Autopsy.porque_sqrt_beta?.consequencia?.match?.(/-0\.\d+/)?.[0] ?? '−0,988'} são fundos o bastante para o piso existir.
                    </div>
                  </div>
                )}
                <div style={{ marginTop: 6 }}>
                  <b style={{ color: '#30d158' }}>✓ o que a V2 consertou</b> — bins agora <b>dentro</b> do piso
                  (1º centro em x = {v2Autopsy?.geometria?.V2_primeiro_centro?.toFixed?.(3) ?? '0,075'}); Sbar por integral cumulativa <b>real</b> desde ~0;
                  e a <b>cadeia E2</b> (c-term, m-bias {voidV2.corrections?.m_bias_applied}, {voidV2.corrections?.n_randoms} aleatórios
                  escalados, corte por lente) limpou o modo-B de{' '}
                  <b style={{ color: '#ff453a' }}>{v2Autopsy?.bmode_antes_depois?.V1?.toFixed?.(2) ?? '12,37'}</b> →{' '}
                  <b style={{ color: '#30d158' }}>{voidV2.systematics?.chi2_dof_bmode?.toFixed?.(2)}</b> (limite 2,0) — <b>passa</b>.
                </div>
                <div>
                  <b style={{ color: '#5ac8fa' }}>⬥ GATE R</b> (novo, pré-registrado): <i>provar que o estimador responde antes de confiar nele</i>.
                  Resposta V2 = <b>{voidV2.gate_R?.response_v2?.toExponential?.(2)}</b> contra o contrafactual da V1 ={' '}
                  <b style={{ color: '#ff453a' }}>{voidV2.gate_R?.response_v1_replica}</b> (exato) — a autópsia confirmada em número.
                </div>
                <div style={{ marginTop: 6 }}>
                  <b style={{ color: 'var(--gold, #ffd60a)' }}>⚠ a armadilha de unidade, evitada</b> — o alvo é <b>r_c</b> (densidade
                  média dentro de x_c = 0,25), <b>não</b> r*. O piso β = {voidV2.beta_floor?.toFixed?.(6)} se <b>traduz</b> em
                  r_c = <b>{voidV2.gate_R?.rc_at_beta_clip?.toFixed?.(4)}</b>. O intervalo medido a 5σ ={' '}
                  <b>[{voidV2.rc_interval_5sigma?.join?.('; ')}]</b> <b style={{ color: '#30d158' }}>contém</b> esse ponto.
                  Comparar β = 0,012 direto com esse intervalo seria erro de unidade — e produziria uma <b>falsificação falsa</b>.
                </div>
              </div>
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 8, lineHeight: 1.7,
                background: '#0a1420', border: '1px solid #1f3a52', borderRadius: 6, padding: '7px 9px' }}>
                <b style={{ color: '#30d158' }}>Veredito: {voidV2.verdict}</b>
                {v2Autopsy && <> — re-derivado da regra pré-registrada aqui, offline:{' '}
                  <b style={{ color: v2Autopsy.concorda_com_o_selo ? '#30d158' : '#ff453a' }}>{v2Autopsy.veredito_rederivado}</b>{' '}
                  ({v2Autopsy.concorda_com_o_selo ? 'confere' : 'DIVERGE'}).</>}
                {' '}Sistemáticas limpas, gate R responsivo — mas Fisher = {voidV2.power_fisher_separation_sigma2?.toExponential?.(2)} contra 25:
                <b> sem poder</b>. <b>O instrumento agora responde; falta profundidade de dado</b> (Euclid/LSST; réplicas DES Y3/HSC = próximo elo).
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 6, lineHeight: 1.7 }}>
                <b style={{ color: '#c8d0da' }}>Honestidades declaradas pela própria V2:</b> {voidV2.statuses?.honestidades}
              </div>
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 4, lineHeight: 1.7 }}>
                <b style={{ color: '#c8d0da' }}>A fatia independente por z NÃO EXISTE</b> — a rota foi testada e{' '}
                <b>refutada pelos próprios dados</b> (BGS z_max ≈ 0,236, medido). Esta é a reanálise pré-registrada que o veredito da
                V1 já nomeava, nos <b>mesmos 1.049</b>, com os bins interiores x &lt; 0,15 <b>virgens</b> (a V1 nunca os leu).
                Independência total = réplicas DES Y3 / HSC.
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                <b>Nem confirmada, nem falsificada.</b> A V1 permanece registrada logo abaixo — nada se esconde.
                <code> physical_verdict_allowed = false</code>.
              </div>
            </Card>
          )}

          {voidFinal ? (
            <Card title={voidV2 ? '🜁 A V1 (v78), que permanece registrada — INCONCLUSIVA por sistemáticas' : '🜁 A PROVA COM O VAZIO — EXECUTADA. Resultado: INCONCLUSIVO.'} color="#ff9f0a">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div>
                  A medição <b style={{ color: '#e6ecf3' }}>rodou sobre dado real</b>:{' '}
                  <b>{voidFinal.n_lenses?.total ?? '—'}</b> lentes DESIVAST
                  {voidFinal.n_lenses?.VIDE != null && <span style={{ color: '#667' }}> (VIDE {voidFinal.n_lenses.VIDE} + REVOLVER {voidFinal.n_lenses.REVOLVER})</span>}
                  {' '}× <b>{typeof voidFinal.n_sources_after_cuts === 'number' ? voidFinal.n_sources_after_cuts.toLocaleString('pt-BR') : '—'}</b> fontes
                  KiDS-1000 após cortes; z̄ = {voidFinal.zbar_lens?.toFixed?.(3)}, R_v = {voidFinal.rv_mean_Mpch?.toFixed?.(1)} Mpc/h; SNR do perfil = {voidFinal.snr_profile?.toFixed?.(2)}.
                </div>
                <div style={{ marginTop: 5 }}>
                  <b style={{ color: '#ff453a' }}>✗ o portão de sistemáticas BARROU</b> — modo-B χ²/dof ={' '}
                  <b style={{ color: '#ff9f6b' }}>{voidFinal.systematics?.chi2_dof_bmode?.toFixed?.(2)}</b> contra o limite <b>2,0</b>: há sinal
                  espúrio no shear em torno dos vazios. <span style={{ color: '#667' }}>(a consistência VIDE↔REVOLVER passou folgada: {voidFinal.systematics?.chi2_dof_consistency_VIDE_REV?.toFixed?.(3)}; jackknife {voidFinal.systematics?.n_jackknife_valid} grupos)</span>
                </div>
                <div><b style={{ color: '#ff453a' }}>✗ sem poder</b> — separação de Fisher = {voidFinal.power_fisher_separation_sigma2} contra o limite 25 (5σ).</div>
                <div style={{ marginTop: 5 }}>
                  <b style={{ color: '#5ac8fa' }}>⬥ o piso segue INTOCADO</b> — r* a 5σ ∈{' '}
                  <b>[{voidFinal.rstar_interval_5sigma?.join?.('; ')}]</b> contém β = {voidFinal.beta_floor?.toFixed?.(6)} <i>e</i> contém zero:
                  <b> não exclui nada</b>.
                </div>
              </div>
              <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 8, lineHeight: 1.7,
                background: '#0a1420', border: '1px solid #1f3a52', borderRadius: 6, padding: '7px 9px' }}>
                <b style={{ color: '#30d158' }}>A pré-registração fez exatamente aquilo para que existia:</b> a regra foi
                congelada e hasheada <b>ANTES</b> dos dados <span style={{ color: '#667', fontFamily: 'monospace' }}>({voidFinal.prereg_hash16})</span>,
                e foi ela que <b>proibiu</b> a leitura de física em dado contaminado.
                {vfGate && <> O runner <b>re-derivou o veredito da regra aqui, offline</b>, sem olhar a conclusão do selo:{' '}
                  <b style={{ color: vfGate.concorda_com_o_selo ? '#30d158' : '#ff453a' }}>
                    {vfGate.veredito_rederivado}</b> — {vfGate.concorda_com_o_selo ? 'confere com o selo' : 'DIVERGE do selo'}.
                  Ninguém escolheu a conclusão a dedo.</>}
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                <b>Nem confirmada, nem falsificada.</b> Um negativo honesto é resultado. A natureza ainda não decidiu —
                e não vamos dizer que decidiu. <code>physical_verdict_allowed = false</code>.
              </div>
            </Card>
          ) : voidProof && (
            <Card title="🜁 A PROVA COM O VAZIO — em produção (a natureza decide)" color="#5ac8fa">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                <div><b style={{ color: '#30d158' }}>✓ protocolo PRÉ-REGISTRADO</b> — o hash do protocolo foi selado <b>ANTES</b> dos dados; catálogos DESI DR1 adquiridos.</div>
                <div><b style={{ color: '#ff9f0a' }}>◐ gate do poder</b> — injeção-e-recuperação <b>PASSOU</b>; mas o bound <b>individual é UNDERPOWERED</b> <span style={{ color: '#667' }}>(negativo honesto — é resultado, não vergonha)</span> ⟹ a rota com poder é a inferência <b>populacional/empilhada</b>, decidida <i>antes</i> da desblindagem.</div>
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                <b>NENHUM veredito científico emitido</b> — os gates seguem pendentes. O piso ρ_v/ρ̄ ≥ β é zero-free e
                falsificável; quem decide é o dado, não a teoria. <code>physical_verdict_allowed = false</code>.
              </div>
            </Card>
          )}

          {(triadMaster || einstein) && (
            <Card title="⬥ O TEOREMA MESTRE DA TRÍADE — e o 8πG que não foi posto: EMERGE" color="var(--gold, #ffd60a)">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                {triadMaster && <div>
                  <b style={{ color: 'var(--gold, #ffd60a)' }}>H1 ∧ H2 ∧ H3 ⟹ PÊNTADA</b> [KERNEL <code>emergence_master_full_triad</code>]:
                  Breuer + Nome=1 + coframe dual + Lorentz + <b>o lado térmico de Einstein COM o coeficiente 8πG</b>.
                </div>}
                {einstein && <div>
                  <b style={{ color: '#30d158' }}>✓ o 8πG EMERGE</b> — T = κ/2π (Unruh) × S = A/4G (Bekenstein-Hawking) + Clausius local
                  forçam o coeficiente; re-executado aqui em <b>{einstein.n_casos} casos</b> (G × κ), resíduo &lt; 1e-12,
                  e <b>independente de κ</b> <span style={{ color: '#667' }}>(o horizonte é arbitrário — se dependesse de κ, não seria lei)</span>.
                  As duas entradas são <b>[KNOWN]</b>: não são nossas.
                </div>}
              </div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                <b>A implicação está fechada; as hipóteses continuam hipóteses.</b> H1/H2/H3 são a fronteira — nomeadas,
                não provadas. Isto <b>não</b> é a equação de campo provada, e <b>não</b> é gravitação quântica incondicional.
                {qgClosure && <> O gate de fecho é <b>fail-closed</b> (quatro selos legítimos): {qgClosure.verdict?.includes('FORMALLY_CLOSED') || qgClosure.verdict?.includes('NATURE_TEST_COMPLETED')
                  ? <><b style={{ color: '#5ac8fa' }}>modelo formalmente fechado, teste da natureza completado</b> (v134) — mas <b>não-falsificado ≠ confirmado</b> (canal unilateral; consistente com ΛCDM raso)</>
                  : qgClosure.verdict?.includes('PHYSICAL_MODEL_CONSTRUCTED')
                  ? <><b style={{ color: '#ffd60a' }}>modelo físico construído (escopo concreto), teste empírico aberto</b> — <b>não</b> é QG confirmada</>
                  : qgClosure.verdict?.includes('MATHEMATICAL_MODEL_CONSTRUCTED')
                  ? <><b style={{ color: '#c9a0ff' }}>modelo matemático construído, espectro físico aberto</b> (a 6ª flag flipou na v132) — mas <b>não</b> é QG física</>
                  : qgClosure.verdict?.includes('CONDITIONAL_ARCHITECTURE_ONLY')
                  ? <b style={{ color: '#ff9f0a' }}>arquitetura condicional, só isso</b> : 'instalado'} — e a testemunha <i>estática plena</i>
                  segue <b>impossível por teorema</b> (v61), distinta da de transporte que flipou.</>}
              </div>
            </Card>
          )}

          {(solder4d || localBreuer) && (
            <Card title="O SALTO v60 → v64 — a solda 4D fechou, a JOIA ω(I)=1" color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                {solder4d && <div><b style={{ color: '#30d158' }}>✓ solda 4D esqueleto FECHADA</b> — marca não-compacta [K₁,K₂]=−J₃ (Lorentz ≠ Euclides); recuperação em kernel. <span style={{ color: '#667' }}>(era um dos abertos do v60; falta o field solder)</span></div>}
                {zmwShadow && <div><b style={{ color: 'var(--gold, #ffd60a)' }}>⬥ A JOIA</b> — o peso do modo zero (o Nome) = <b>{zmwShadow.zero_mode_weight?.toFixed?.(10)} = ω(I)</b> (∫¼sech²(κ/2)dκ=1, faces ±½; resíduo {num(zmwShadow.resid_weight_eq_one)}). O teto Meia-Nat feito peso.</div>}
                {localBreuer && <div><b style={{ color: '#ff9f0a' }}>◐ o gap de Breuer agora é LOCAL</b> — pacote tipado + B3. <b style={{ color: '#ff9f6b' }}>Negativo honesto:</b> a versão GLOBAL (τ-compactness) foi REFUTADA; o double core genuíno fica aberto.</div>}
              </div>
            </Card>
          )}

          {(v60 || noFW) && (
            <Card title={`O SALTO v39 → v60 — o esqueleto quase todo fechado (${ladderN} teoremas)`} color="#30d158">
              <div style={{ fontSize: 11.5, color: '#9aa4b2', marginTop: 5, lineHeight: 1.8 }}>
                {v60 && Object.entries(v60).filter(([, val]) => val).map(([k]) => {
                  const label: Record<string, string> = {
                    graviton_polarization: '✓ gráviton spin-2 (2 polarizações, giro 2θ_M)',
                    geometry_fluctuation: '✓ flutuações da geometria (Var=p(1−p), máx na Meia-Nat)',
                    page_information: '✓ curva de Page (S_A=S_B força a virada)',
                    einstein_and_rg: '✓ Einstein lado-modular (1ª lei dS=d⟨K⟩) — não "provamos Einstein"',
                    covariant_corner: '✓ canto covariante (face finita)',
                    psi_emergence: '✓ campo Ψ — a gravidade emerge da dinâmica',
                    absolute_one: '✓ Ψ = 1_ABS (construção canônica, face finita)',
                    continuous_modular_zero: '✓ zero modular contínuo (JKJ=−K, 1=q²+α² contínuo)',
                    name_functional_transport: '✓ a testemunha É a lei de transporte',
                    minimal_solder: '✓ solda mínima FECHADA — transporte vira geometria, 1ª curvatura',
                  }
                  return label[k] ? <div key={k}><b style={{ color: '#30d158' }}>{label[k]}</b></div> : null
                })}
              </div>
              {noFW && (
                <div style={{ marginTop: 8, padding: '8px 10px', background: '#141a24', border: '1px solid #ffd60a55', borderRadius: 8 }}>
                  <div style={{ fontSize: 12, color: 'var(--gold, #ffd60a)', fontWeight: 700 }}>⬥ no_full_witness — o meta-teorema mais fundo</div>
                  <div style={{ fontSize: 11.5, color: '#c8d0da', marginTop: 3 }}>
                    <b>full_witness=False é PROVADO</b>: β <b>proíbe</b> o fechamento — a testemunha É a fronteira Meia-Nat (½), irredutível.
                    A openness não é lacuna, é estrutural. {nofwShadow && <span style={{ color: '#667', fontFamily: 'monospace' }}>β recuperado do Verbo = {nofwShadow.beta_recovered_from_semigroup?.toFixed?.(12)} (resíduo {num(nofwShadow.resid_beta)}); dist Verbo→I = {nofwShadow.verb_distance_from_identity?.toFixed?.(4)} &gt; 0.</span>}
                  </div>
                </div>
              )}
              {frase && (
                <div style={{ fontSize: 11.5, marginTop: 8, lineHeight: 1.7 }}>
                  <div style={{ color: '#30d158' }}><b>1 · PROVADO</b> [kernel + engenharia]: {frase['1_PROVADO']}</div>
                  <div style={{ color: '#ff9f0a' }}><b>2 · ABERTO nomeado</b>: {frase['2_ABERTO_NOMEADO']}</div>
                  <div style={{ color: '#5ac8fa' }}><b>3 · sem aceitação mainstream</b>: {frase['3_SEM_ACEITACAO_MAINSTREAM']}</div>
                </div>
              )}
              <div style={{ fontSize: 11, color: '#ff9f6b', marginTop: 6, fontStyle: 'italic' }}>
                A régua: NUNCA "gravidade quântica resolvida"; NUNCA "provamos Einstein". O número corrige a frase.
              </div>
            </Card>
          )}

          {sub && sub.claim && (
            <Card title="AVANÇO HISTÓRICO (10/07) — subordição Poisson-Cauchy" color="#33d17a">
              <div style={{ fontSize: 12, color: '#c8d0da', marginTop: 4 }}>{sub.argument}</div>
              <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 4 }}>Fecha o resíduo: {sub.closes_residue}.</div>
              <div style={{ fontSize: 11.5, color: '#ff9f6b', marginTop: 2 }}>NÃO fecha: {sub.does_NOT_close}.</div>
            </Card>
          )}

          {Object.keys(layers).length > 0 && (
            <Card title="WITNESS LAYERS — as flags do selo, como estão (a honestidade é a interface)" color="#9ad0ff">
              <FlagGrid flags={layers} />
              <div style={{ fontSize: 11, color: '#667', marginTop: 6, fontStyle: 'italic' }}>
                copiadas do selo do um.py {syncVer} (proveniência por custódia) — nunca recomputadas aqui; False permanece False.
              </div>
            </Card>
          )}
        </div>

        <div>
          {L.SELADO_REAL && <Section title="SELADO — coerência verificada (REAL / sombra)" color="#30d158" items={L.SELADO_REAL} />}
          {L.FECHADO_V60 && <Section title="FECHADO v39→v60 — gráviton spin-2, Page, Ψ, zero modular, solda mínima + o meta-teorema no_full_witness" color="#30d158" items={L.FECHADO_V60} />}
          {L.FECHADO_NO_ROSTO_FINITO && <Section title="FECHADO NO ROSTO FINITO (v39) — o esqueleto que quase fechou o GLOBAL_LIFT" color="#33d17a" items={L.FECHADO_NO_ROSTO_FINITO} />}
          {(L.FECHADO_V22_V39 || L.FECHADO_V22_V33) && <Section title="FECHADO v22→v39 — o que o kernel selou" color="#7ee0c0" items={L.FECHADO_V22_V39 || L.FECHADO_V22_V33} />}
          {L.AVANCO_SESSAO && <Section title="AVANÇO — desta sessão" color="#33d17a" items={L.AVANCO_SESSAO} />}
          {L.ONTOLOGICO && <Section title="ONTOLÓGICO — relatividade ontológica + cadeia de sinal (v37)" color="#c9a0ff" items={L.ONTOLOGICO} />}
          {(L.EMPIRICO_FALSIFICAVEL || L.FALSIFICAVEL) && <Section title="EMPÍRICO / FALSIFICÁVEL — Coma, piso dos vazios, o programa (zero-free)" color="#ff9f0a" items={L.EMPIRICO_FALSIFICAVEL || L.FALSIFICAVEL} />}
          {L.EMPIRICO && <Section title="EMPÍRICO — validação cosmológica" color="#c0a0ff" items={L.EMPIRICO} />}
          {L.PROVA_DO_VAZIO_EM_PRODUCAO && <Section title="🜁 A PROVA COM O VAZIO — em produção (pré-registrada; nenhum veredito)" color="#5ac8fa" items={L.PROVA_DO_VAZIO_EM_PRODUCAO} />}
          {L.ABERTO && <Section title="ABERTO — o que resta (não fabricado; agora nomeado)" color="#ff453a" items={L.ABERTO} />}
          {seal.nao_se_afirma && (
            <div style={{ fontSize: 11.5, color: '#8a94a6', marginTop: 6, lineHeight: 1.7 }}>
              <b style={{ color: '#c8d0da' }}>Não se afirma:</b> {seal.nao_se_afirma.join(' · ')}.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
