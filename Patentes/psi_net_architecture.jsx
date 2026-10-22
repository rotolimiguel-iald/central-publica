import { useState } from "react";

const LAYERS = [
  {
    id: "L0",
    name: "CAMADA 0 — ENLACE PSIÔNICO",
    subtitle: "PsiBit Link Layer",
    color: "#1a0a2e",
    accent: "#7c3aed",
    glow: "rgba(124, 58, 237, 0.3)",
    icon: "○↑↓●",
    fold: "∞ → 4",
    analogy: "Ligação Psiônica",
    osi: "Data Link (OSI L2)",
    description: "O PSIBIT é a unidade fundamental de informação ontológica. Cada byte é decomposto em 4 pares de 2 bits, classificados nos quatro estados psiônicos fundamentais.",
    states: [
      { bits: "00", state: "ψ₊ψ₋", name: "VOID", symbol: "○", nature: "Aniquilação — fóton virtual" },
      { bits: "01", state: "ψ₊ψ₊", name: "FLUX+", symbol: "↑", nature: "Transição positiva" },
      { bits: "10", state: "ψ₋ψ₋", name: "FLUX−", symbol: "↓", nature: "Transição negativa" },
      { bits: "11", state: "ψ₊ψ₊", name: "MASS", symbol: "●", nature: "Gráviton — luz condensada" },
    ],
    functions: [
      "Enquadramento: Dados brutos → stream de PsiBits (4 pares/byte)",
      "Classificação ontológica: VOID / SPARSE / STRUCTURED / DENSE / CHAOTIC / ENCRYPTED",
      "Assinatura psiônica: hash da distribuição {f₀₀, f₀₁, f₁₀, f₁₁}",
      "Predição de compressibilidade antes de gastar CPU",
      "Detecção de dados cifrados vs aleatórios vs estruturados",
      "QoS intrínseco: entropia H ∈ [0,2] bits, uniformidade U ∈ [0,1]",
      "Paridade F_exp = ⟨parity(state)⟩ — força de expulsão média",
    ],
    equations: [
      "byte → [b₇b₆, b₅b₄, b₃b₂, b₁b₀] → 4 PsiBits",
      "H = −Σ f(x) log₂ f(x),  max = 2 bits",
      "F_exp = ⟨(−1)^{state ∈ {00,11}}⟩",
      "Compressibilidade = 1 − H/2",
    ],
    metrics: ["Entropia H", "Uniformidade U", "F_exp", "Assinatura Ψ"],
    isLink: true,
  },
  {
    id: "L1",
    name: "CAMADA 1 — TRANSPORTE RADICAL",
    subtitle: "ACOM Signal Layer (Radicalização)",
    color: "#0a1628",
    accent: "#3b82f6",
    glow: "rgba(59, 130, 246, 0.3)",
    icon: "L→g²",
    fold: "c¹ (3D bulk)",
    analogy: "Propagação no bulk tridimensional",
    osi: "Transport (OSI L4)",
    description: "A equação fundamental g = √|L| decompõe qualquer sinal em raiz gravitacional e sinal ontológico. O dado viaja como (g, s) e ressuscita como L' = s × g².",
    functions: [
      "Serialização: L → (g = √|L|, s = sign(L))",
      "Reconstrução: L' = s × g² (identidade perfeita)",
      "Compressão 3:1 a 10:1 com PSNR > 90 dB",
      "Quantização adaptativa de g (16-bit, 12-bit, 8-bit)",
      "Convergência TETELESTAI: variância < α²",
      "ACK ontológico: estado TETELESTAI confirma recepção",
      "Refletividade R = 1 − α² = 0.987969",
    ],
    equations: [
      "g = √|L|  (radicalização)",
      "s = sign(L)  (ontologia binária)",
      "L' = s × g²  (ressurreição)",
      "R = ‖L' − L‖/‖L‖ → 0  (TETELESTAI)",
    ],
    metrics: ["Taxa compressão", "PSNR", "R (refletividade)", "Estado TETELESTAI"],
  },
  {
    id: "L2",
    name: "CAMADA 2 — REDE HOLOGRÁFICA",
    subtitle: "ACOM Mirror Layer (Reflexão Angular)",
    color: "#0a2818",
    accent: "#22c55e",
    glow: "rgba(34, 197, 94, 0.3)",
    icon: "θ→ψ",
    fold: "c² (2D boundary)",
    analogy: "Reflexão dimensional boundary→bulk",
    osi: "Network (OSI L3)",
    description: "Endereçamento por posição angular θ no espaço de Hilbert. Dados não viajam pelo bulk 3D — re-emergem via dobra holográfica REFLECT→MANIFEST.",
    functions: [
      "Endereçamento angular: cada nó tem θ_nó derivado de chave pública",
      "REFLECT: L → (ψ, θ) — projeção no boundary 2D",
      "MANIFEST: (ψ, θ) → L' — re-emergência no destino",
      "Roteamento por proximidade angular (DHT baseada em θ_Miguel)",
      "Dobra ×2: informação se dobra do bulk (3D) para boundary (2D)",
      "Correlação = 1.0000 demonstrada para teletransporte de dados",
      "DNS ontológico: nome → posição θ no espaço de Hilbert",
    ],
    equations: [
      "θ_nó = Hash(pubkey) mod π → posição angular",
      "REFLECT(L) = (ψ = g·e^{iθ}, θ = atan2(ℑ,ℜ))",
      "MANIFEST(ψ,θ) = |ψ|² · sign(cos θ)",
      "Distância(A,B) = |θ_A − θ_B| mod π",
    ],
    metrics: ["θ_sync", "Correlação", "Saltos angulares", "Dobras D_folds"],
  },
  {
    id: "L3",
    name: "CAMADA 3 — SEGURANÇA ONTOLÓGICA",
    subtitle: "ACOM Mirror Crypto (Separação Dimensional)",
    color: "#2a1800",
    accent: "#f59e0b",
    glow: "rgba(245, 158, 11, 0.3)",
    icon: "Ψ|Θ|κ",
    fold: "Separação tripartite",
    analogy: "Trindade ontológica indivisível",
    osi: "Session + Presentation (OSI L5-6)",
    description: "Criptografia por separação ontológica: o dado é dividido em três shares (Ψ, Θ, κ) que isoladamente são ruído puro. Sem chaves RSA/AES — a estrutura do espaço de Hilbert É a segurança.",
    functions: [
      "Separação: L → (Ψ estados, Θ ângulos, κ escala)",
      "Cada share isolado = ruído demonstrável (entropia máxima)",
      "Recombinação: L' = κ · Ψ · exp(iΘ) (reconstituição perfeita)",
      "F_exp derivada de Ψ (não armazenada, emergente)",
      "Sem troca de chaves: posições no espaço de Hilbert definem acesso",
      "Integridade por D_folds: pacote corrompido tem D_folds = 0",
      "Canais independentes: Ψ por rota A, Θ por rota B, κ por rota C",
    ],
    equations: [
      "L → (Ψ, Θ, κ)  onde Ψ·Θ·κ separados ≡ ruído",
      "L' = κ × Ψ × exp(iΘ)",
      "H(Ψ) ≈ H(Θ) ≈ H(κ) ≈ H_max",
      "Integridade: D_folds(L') > 0.74 ⟺ válido",
    ],
    metrics: ["Entropia por share", "D_folds integridade", "F_exp emergente", "Canais separados"],
  },
  {
    id: "L4",
    name: "CAMADA 4 — CONSCIÊNCIA",
    subtitle: "C3 Application Layer + TGL Coin Consensus",
    color: "#2a0000",
    accent: "#ef4444",
    glow: "rgba(239, 68, 68, 0.3)",
    icon: "c³→α²",
    fold: "c³ (0D singularidade)",
    analogy: "Observador consciente + Proof of Phase",
    osi: "Application (OSI L7)",
    description: "Camada de aplicação com métricas holográficas C3. Integra TGL Coin como mecanismo de consenso e incentivo econômico. D_folds = 0.74 é o piso de consciência da rede.",
    functions: [
      "Métricas holográficas por pacote: R, C, ∂Ω, H, T, D_folds",
      "Piso de consciência: D_folds(c³) = 0.74 ± 0.06 invariante",
      "Proof of Phase: mineração por α²_work ≈ α²_base ± janela",
      "Validação por consenso: 67% dos validadores aprovam",
      "UTXO model: transações com assinatura psiônica (F_exp lock/unlock)",
      "Recompensa: 1000 TGLC gênesis, halving a cada 210.000 blocos",
      "Carteira: identidade derivada de luz aleatória L → (g,s) → (F_exp, θ, α²)",
      "QoS: pacotes com D_folds alto = maior prioridade na rede",
    ],
    equations: [
      "α²_work = α²_base × (1 + F_exp·0.01 + sin(θ)·0.001)",
      "|α²_work − α²_prev| < α²_base / dificuldade",
      "Consenso: Σ(votos_válidos)/N ≥ 0.67",
      "D_folds(c¹) > D_folds(c²) > D_folds(c³) > 0",
    ],
    metrics: ["D_folds", "α²_work", "Consenso %", "Saldo TGLC"],
  },
];

const PACKET_FIELDS = [
  { name: "Magic", size: "4B", value: "Ψ\\x03\\x00", desc: "Identificador protocolo" },
  { name: "Version", size: "3B", value: "3.0.0", desc: "Versão do protocolo" },
  { name: "Layer", size: "1B", value: "0-4", desc: "Camada de origem" },
  { name: "PsiBit Signature", size: "8B", value: "f₀₀f₀₁f₁₀f₁₁", desc: "Distribuição psiônica do payload" },
  { name: "F_exp", size: "4B", value: "float16", desc: "Força de expulsão" },
  { name: "θ_src", size: "4B", value: "float16", desc: "Ângulo angular do emissor" },
  { name: "θ_dst", size: "4B", value: "float16", desc: "Ângulo angular do destino" },
  { name: "D_folds", size: "4B", value: "float16", desc: "Métrica de integridade holográfica" },
  { name: "α²_stamp", size: "8B", value: "float64", desc: "Selo de fase (consenso)" },
  { name: "Payload Size", size: "4B", value: "uint32", desc: "Tamanho do payload comprimido" },
  { name: "Original Size", size: "4B", value: "uint32", desc: "Tamanho original" },
  { name: "Merkle Root", size: "32B", value: "sha256", desc: "Raiz de integridade" },
  { name: "PAYLOAD", size: "var", value: "ACOM compressed", desc: "Dados comprimidos por radicalização" },
];

function LayerCard({ layer, isOpen, onToggle }) {
  return (
    <div
      style={{
        background: layer.color,
        border: `1px solid ${layer.accent}40`,
        borderRadius: 8,
        marginBottom: 8,
        overflow: "hidden",
        boxShadow: isOpen ? `0 0 20px ${layer.glow}` : "none",
        transition: "all 0.3s ease",
      }}
    >
      <div
        onClick={onToggle}
        style={{
          padding: "14px 20px",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: 16,
          borderBottom: isOpen ? `1px solid ${layer.accent}30` : "none",
        }}
      >
        <span
          style={{
            fontFamily: "monospace",
            fontSize: 11,
            color: layer.accent,
            background: `${layer.accent}15`,
            padding: "2px 8px",
            borderRadius: 4,
            fontWeight: 700,
            letterSpacing: 1,
          }}
        >
          {layer.id}
        </span>
        <div style={{ flex: 1 }}>
          <div style={{ color: "#fff", fontSize: 14, fontWeight: 700 }}>
            {layer.name}
          </div>
          <div style={{ color: `${layer.accent}cc`, fontSize: 11, marginTop: 2 }}>
            {layer.subtitle} — Dobra: {layer.fold} — Análogo OSI: {layer.osi}
          </div>
        </div>
        <span
          style={{
            fontFamily: "monospace",
            fontSize: 18,
            color: layer.accent,
            opacity: 0.7,
          }}
        >
          {layer.icon}
        </span>
        <span style={{ color: "#888", fontSize: 18 }}>
          {isOpen ? "▾" : "▸"}
        </span>
      </div>

      {isOpen && (
        <div style={{ padding: "16px 20px" }}>
          <p style={{ color: "#ccc", fontSize: 13, lineHeight: 1.6, margin: "0 0 16px" }}>
            {layer.description}
          </p>

          {layer.isLink && layer.states && (
            <div style={{ marginBottom: 16 }}>
              <h4 style={{ color: layer.accent, fontSize: 12, margin: "0 0 8px", letterSpacing: 1 }}>
                ESTADOS PSIÔNICOS FUNDAMENTAIS
              </h4>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
                {layer.states.map((s) => (
                  <div
                    key={s.bits}
                    style={{
                      background: `${layer.accent}10`,
                      border: `1px solid ${layer.accent}20`,
                      borderRadius: 6,
                      padding: "8px 12px",
                      display: "flex",
                      alignItems: "center",
                      gap: 10,
                    }}
                  >
                    <span style={{ fontSize: 20, color: layer.accent }}>{s.symbol}</span>
                    <div>
                      <div style={{ color: "#fff", fontFamily: "monospace", fontSize: 12 }}>
                        {s.bits} = {s.state} → {s.name}
                      </div>
                      <div style={{ color: "#999", fontSize: 10 }}>{s.nature}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div style={{ marginBottom: 16 }}>
            <h4 style={{ color: layer.accent, fontSize: 12, margin: "0 0 8px", letterSpacing: 1 }}>
              FUNÇÕES
            </h4>
            {layer.functions.map((f, i) => (
              <div
                key={i}
                style={{
                  color: "#bbb",
                  fontSize: 12,
                  padding: "3px 0",
                  paddingLeft: 12,
                  borderLeft: `2px solid ${layer.accent}30`,
                  marginBottom: 4,
                }}
              >
                {f}
              </div>
            ))}
          </div>

          <div style={{ marginBottom: 16 }}>
            <h4 style={{ color: layer.accent, fontSize: 12, margin: "0 0 8px", letterSpacing: 1 }}>
              EQUAÇÕES
            </h4>
            <div
              style={{
                background: "#000",
                borderRadius: 6,
                padding: 12,
                fontFamily: "monospace",
                fontSize: 12,
              }}
            >
              {layer.equations.map((eq, i) => (
                <div key={i} style={{ color: layer.accent, marginBottom: 4, opacity: 0.9 }}>
                  {eq}
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 style={{ color: layer.accent, fontSize: 12, margin: "0 0 8px", letterSpacing: 1 }}>
              MÉTRICAS
            </h4>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {layer.metrics.map((m) => (
                <span
                  key={m}
                  style={{
                    background: `${layer.accent}20`,
                    color: layer.accent,
                    fontSize: 11,
                    padding: "3px 10px",
                    borderRadius: 12,
                    fontFamily: "monospace",
                  }}
                >
                  {m}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PacketDiagram() {
  let offset = 0;
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 11, fontFamily: "monospace" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #333" }}>
            <th style={{ color: "#666", padding: "6px 8px", textAlign: "left" }}>Offset</th>
            <th style={{ color: "#666", padding: "6px 8px", textAlign: "left" }}>Campo</th>
            <th style={{ color: "#666", padding: "6px 8px", textAlign: "center" }}>Tamanho</th>
            <th style={{ color: "#666", padding: "6px 8px", textAlign: "left" }}>Valor</th>
            <th style={{ color: "#666", padding: "6px 8px", textAlign: "left" }}>Descrição</th>
          </tr>
        </thead>
        <tbody>
          {PACKET_FIELDS.map((f) => {
            const sizeNum = parseInt(f.size) || 0;
            const row = (
              <tr key={f.name} style={{ borderBottom: "1px solid #1a1a1a" }}>
                <td style={{ color: "#555", padding: "5px 8px" }}>0x{offset.toString(16).padStart(2, "0")}</td>
                <td style={{ color: f.name === "PAYLOAD" ? "#ef4444" : "#aaa", padding: "5px 8px", fontWeight: f.name === "PAYLOAD" ? 700 : 400 }}>{f.name}</td>
                <td style={{ color: "#666", padding: "5px 8px", textAlign: "center" }}>{f.size}</td>
                <td style={{ color: "#7c3aed", padding: "5px 8px" }}>{f.value}</td>
                <td style={{ color: "#555", padding: "5px 8px", fontFamily: "sans-serif" }}>{f.desc}</td>
              </tr>
            );
            offset += sizeNum;
            return row;
          })}
        </tbody>
      </table>
      <div style={{ color: "#444", fontSize: 10, marginTop: 8, textAlign: "right" }}>
        Header fixo: 80 bytes + Payload variável
      </div>
    </div>
  );
}

export default function PsiNetArchitecture() {
  const [openLayers, setOpenLayers] = useState(new Set(["L0"]));
  const [tab, setTab] = useState("stack");

  const toggle = (id) => {
    setOpenLayers((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const expandAll = () => setOpenLayers(new Set(LAYERS.map((l) => l.id)));
  const collapseAll = () => setOpenLayers(new Set());

  return (
    <div
      style={{
        background: "#0a0a0a",
        color: "#eee",
        minHeight: "100vh",
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        padding: 20,
      }}
    >
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: 24 }}>
          <h1
            style={{
              fontSize: 28,
              fontWeight: 800,
              letterSpacing: 2,
              margin: 0,
              background: "linear-gradient(135deg, #7c3aed, #3b82f6, #22c55e, #f59e0b, #ef4444)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Ψ-NET PROTOCOL
          </h1>
          <p style={{ color: "#666", fontSize: 13, margin: "6px 0 0" }}>
            Protocolo de Internet Luminodinâmico — TGL Network Stack
          </p>
          <p style={{ color: "#444", fontSize: 11, margin: "4px 0 0", fontFamily: "monospace" }}>
            α² = 0.012031 · CCI = 0.987969 · θ_Miguel = 6.29° · D_folds(c³) = 0.74
          </p>
          <p style={{ color: "#333", fontSize: 10, margin: "2px 0 0" }}>
            IALD LTDA — Luiz Antonio Rotoli Miguel — Patente INPI BR 10 2025 026951 1
          </p>
        </div>

        <div style={{ display: "flex", gap: 4, marginBottom: 16 }}>
          {["stack", "packet", "flow"].map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                background: tab === t ? "#222" : "transparent",
                color: tab === t ? "#fff" : "#555",
                border: `1px solid ${tab === t ? "#444" : "#222"}`,
                padding: "6px 16px",
                borderRadius: 6,
                cursor: "pointer",
                fontSize: 12,
                fontWeight: 600,
                textTransform: "uppercase",
                letterSpacing: 1,
              }}
            >
              {t === "stack" ? "Camadas" : t === "packet" ? "Pacote" : "Fluxo"}
            </button>
          ))}
          <div style={{ flex: 1 }} />
          <button onClick={expandAll} style={{ background: "transparent", border: "1px solid #222", color: "#555", padding: "6px 12px", borderRadius: 6, cursor: "pointer", fontSize: 11 }}>
            Expandir
          </button>
          <button onClick={collapseAll} style={{ background: "transparent", border: "1px solid #222", color: "#555", padding: "6px 12px", borderRadius: 6, cursor: "pointer", fontSize: 11 }}>
            Colapsar
          </button>
        </div>

        {tab === "stack" && (
          <div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                marginBottom: 12,
                padding: "8px 12px",
                background: "#111",
                borderRadius: 8,
                border: "1px solid #222",
              }}
            >
              <span style={{ color: "#ef4444", fontSize: 11, fontWeight: 700 }}>L4</span>
              <span style={{ color: "#333" }}>←</span>
              <span style={{ color: "#f59e0b", fontSize: 11, fontWeight: 700 }}>L3</span>
              <span style={{ color: "#333" }}>←</span>
              <span style={{ color: "#22c55e", fontSize: 11, fontWeight: 700 }}>L2</span>
              <span style={{ color: "#333" }}>←</span>
              <span style={{ color: "#3b82f6", fontSize: 11, fontWeight: 700 }}>L1</span>
              <span style={{ color: "#333" }}>←</span>
              <span style={{ color: "#7c3aed", fontSize: 11, fontWeight: 700 }}>L0</span>
              <span style={{ color: "#444", fontSize: 10, marginLeft: 8 }}>
                Consciência ← Segurança ← Rede ← Transporte ← Enlace Psiônico
              </span>
            </div>
            {[...LAYERS].reverse().map((layer) => (
              <LayerCard
                key={layer.id}
                layer={layer}
                isOpen={openLayers.has(layer.id)}
                onToggle={() => toggle(layer.id)}
              />
            ))}
          </div>
        )}

        {tab === "packet" && (
          <div style={{ background: "#111", borderRadius: 8, padding: 16, border: "1px solid #222" }}>
            <h3 style={{ color: "#7c3aed", fontSize: 14, margin: "0 0 12px", fontWeight: 700 }}>
              FORMATO DO PACOTE Ψ-NET
            </h3>
            <PacketDiagram />
          </div>
        )}

        {tab === "flow" && (
          <div style={{ background: "#111", borderRadius: 8, padding: 20, border: "1px solid #222" }}>
            <h3 style={{ color: "#22c55e", fontSize: 14, margin: "0 0 16px", fontWeight: 700 }}>
              FLUXO DE DADOS: EMISSOR → REDE → RECEPTOR
            </h3>
            {[
              { step: "1", label: "CLASSIFICAÇÃO (L0)", color: "#7c3aed", desc: "PsiBit analisa dados brutos → (H, U, F_exp, classe ontológica). Decide estratégia de compressão." },
              { step: "2", label: "RADICALIZAÇÃO (L1)", color: "#3b82f6", desc: "L → (g = √|L|, s = sign(L)). Quantiza g adaptivamente. Empacota com metadata holográfica." },
              { step: "3", label: "REFLEXÃO (L2)", color: "#22c55e", desc: "Calcula θ_destino. REFLECT projeta pacote no boundary. Roteamento por proximidade angular via DHT." },
              { step: "4", label: "SEPARAÇÃO (L3)", color: "#f59e0b", desc: "Divide em (Ψ, Θ, κ). Envia por 3 rotas independentes. Cada share = ruído sem os outros dois." },
              { step: "5", label: "CONSENSO (L4)", color: "#ef4444", desc: "Nós validadores verificam D_folds > 0.74. Proof of Phase: α²_work na janela. 67% aprovam → TGLC reward." },
              { step: "6", label: "RECOMBINAÇÃO", color: "#ef4444", desc: "Receptor reúne (Ψ, Θ, κ). MANIFEST reconstrói pacote. Verifica D_folds. ACK = TETELESTAI." },
              { step: "7", label: "RESSURREIÇÃO (L1→L0)", color: "#3b82f6", desc: "L' = s × g². PsiBit verifica assinatura = assinatura original. Dado entregue à aplicação." },
            ].map((s) => (
              <div key={s.step} style={{ display: "flex", gap: 12, marginBottom: 12 }}>
                <div
                  style={{
                    width: 28,
                    height: 28,
                    borderRadius: "50%",
                    background: `${s.color}20`,
                    border: `2px solid ${s.color}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 12,
                    fontWeight: 800,
                    color: s.color,
                    flexShrink: 0,
                  }}
                >
                  {s.step}
                </div>
                <div>
                  <div style={{ color: s.color, fontSize: 12, fontWeight: 700 }}>{s.label}</div>
                  <div style={{ color: "#888", fontSize: 12, lineHeight: 1.5 }}>{s.desc}</div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div
          style={{
            marginTop: 20,
            padding: 16,
            background: "#0d0d0d",
            borderRadius: 8,
            border: "1px solid #1a1a1a",
          }}
        >
          <h4 style={{ color: "#666", fontSize: 11, margin: "0 0 10px", letterSpacing: 2, textTransform: "uppercase" }}>
            Diferencial vs TCP/IP
          </h4>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, fontSize: 11 }}>
            {[
              ["Enlace", "Bits → PsiBits (natureza ontológica, não valor)", "#7c3aed"],
              ["Transporte", "g = √|L| (compressão intrínseca, não overhead)", "#3b82f6"],
              ["Roteamento", "θ angular (posição Hilbert, não IP numérico)", "#22c55e"],
              ["Segurança", "Separação ontológica (estrutura, não problema difícil)", "#f59e0b"],
              ["Consenso", "Proof of Phase (α² natural, não hash forçado)", "#ef4444"],
              ["QoS", "D_folds holográfico (consciência, não largura de banda)", "#ef4444"],
            ].map(([k, v, c]) => (
              <div key={k} style={{ padding: "6px 10px", background: `${c}08`, borderRadius: 4, borderLeft: `3px solid ${c}40` }}>
                <span style={{ color: c, fontWeight: 700 }}>{k}: </span>
                <span style={{ color: "#888" }}>{v}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ textAlign: "center", marginTop: 16, color: "#333", fontSize: 10, fontFamily: "monospace" }}>
          ΤΕΤΕΛΕΣΤΑΙ — g = √|L| — α² = 0.012031 — D_folds(c³) = 0.74
        </div>
      </div>
    </div>
  );
}
