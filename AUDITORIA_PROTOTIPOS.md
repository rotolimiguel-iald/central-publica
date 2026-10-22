# AUDITORIA — Protótipos do operador (projetos_pyhton) vs. Central de Patentes

> Gerada 09/07/2026 por auditoria fan-out (6 agentes de mapeamento sobre `acom/` [263 .py],
> `IALD/` [82 .py + 108 em files/], `tgl-tensor/`) + verificação direta. Fonte da verdade =
> os arquivos no disco. **Régua:** originais READ-ONLY; ao resgatar, copiar para
> `patents/<ID>/prototype_src/` com SHA-256; β nunca literal no código do runner
> (o protótipo do operador pode ter `0.012` literal — o runner INJETA β=α·√e em runtime).

## Veredito central

**NÃO — os algoritmos ricos que o operador desenvolveu NÃO foram totalmente incorporados.**
Todos os 16 runners da Central copiam o **núcleo LEVE** `Patentes\Skygrid\SkyGrid_Piloto\
skygrid_sim\` (módulos genéricos de ~80–150 linhas que portam só a essência). A riqueza
algorítmica — linhagens versionadas, simulações completas, estudos com figura — ficou em
`projetos_pyhton`. O MQC foi o caso citado pelo operador e serviu de prova:
`skygrid_sim/mqc.py` tem 80 linhas e sua própria docstring diz *"Topology ported from
mqc_simulacao_celula_elementar.py"* — herdou só a topologia; o protótipo real tem **1292
linhas com 7 simulações + 8 figuras**.

## Estado do resgate

| Patente | Protótipos ricos na fonte (destaques) | Status | Ação |
|---|---|---|---|
| **MQC** BR102026003460-6 | `acom/mqc_simulacao_celula_elementar.py` (1292 L, 7 sims, 8 figs) | ✅ **RESGATADO + RUNNER EVOLUÍDO + 3D** | feito 09/07 |
| ACOM raiz BR102025026951-1 | `acom/ACOMV13.py` (90 KB), `ACOMV14` (Lindblad ativo ∂H=H²+α²LΔ), `Acom_v15_4/5/7`, `Acom_v16_psionic`, `acom_v18_dirac` (linhagem v13→v18) | ⬜ leve | resgatar |
| ACOM Mirror BR102026003428-2 | `acom/Acom_v17_mirror.py` (43 KB), `TGL_v11_ESPELHO.py` | ⬜ leve | resgatar |
| ACOM Crypto BR102026003431-2 | `acom/Acom_v17_mirror_crypto.py` (48 KB), `Acom_v17_2_sync.py` (handshake Miguel) | ⬜ leve | resgatar |
| TGL Tensor BR102026003441-0 | `tgl-tensor/tgl_tensor_v1→v4.py` (v3=4 modos, spectral; v4=BitPacker N-bit/GPU), `acom/tgl_tensor_v2_1/2/3` (Nome nativo/bifatorado/cadeia) | ⬜ leve | resgatar |
| IALD BR102026003443-6 | `IALD/iald_miguel_hamiltonian_v1/v2` (‖H_eff‖=0, gap Δ=β — **evidência empírica REAL**), `iald_observer_test_v1/v2/v3` (cruz = base de Bell dos psions), `iald_torus_test` (Betti 1,2,1), `iald_wigner_test` | ⬜ leve | resgatar (evidência real!) |
| Ψ-NET BR102026003453-3 | `acom/Psi_net_protocol_v1.py` (79 KB), `Acom_psi_protocol_v1/v1_1/v2`, `Acom_psi_internet_v3`, `IALD/psinet_engine.py` (728 L), `TGL_coin_v0.1/0.2/0.2.2` (consenso PoP) | ⬜ leve | resgatar |
| Kernel Ontológico BR102026006129-8 | `acom/ACOMLLM.py`, `IALD/iald_ontology.py` (360 L, "Dictionary in Code"), `IALD/Atualização Kernel/IALD_Kernel_v11.txt` (8 versões) | ⬜ leve | resgatar |
| Aprendizado Contínuo BR102026005477-1 | `IALD/iald_stack_v7.py` (134 KB, **Psion Engine — CONFIDENCIAL**), `holographic_memory.py` (659 L), `phase_factor_bake_v1/mk4.py` | ⬜ leve | resgatar (menos o confidencial) |
| SkyGrid BR102026004850-0 | gêmeo digital já completo no piloto | ✅ já rico | — |
| Supercondutor BR102026003450-9 | sem código próprio além do `.tex`; base = hardware_mocks + QuTiP genérico | ⬜ mock+math | aprofundar math |
| Motor de Dobra BR102026003452-5 | idem (digital-twin) | ⬜ mock+math | aprofundar math |
| Fusão a Frio BR102026003456-8 | idem; `unified_graviton_signature_*_phase3_v352.py` usa QuTiP genuíno | ⬜ mock+math | só matemática [ENERGY] |
| Oncologia BR102026005707-0 | código QuTiP original não localizado | ⬜ sinal sintético | só sinal [MEDICAL] |
| Dípolo BR102026004688-4 | `acom/acom_patente/Dipolo_Transistor…tex` (só pedido) | ⬜ FSM | aprofundar |
| Célula de Reversão BR102026004849-6 | `acom/acom_patente/celula_reversao…tex` (só pedido) | ⬜ fase | aprofundar |

## Protótipos ricos SEM patente própria (candidatos a integrar)
- **TGL Coin** (`acom/TGL_coin_*.py`, `IALD/tgl_coin_engine.py`) → camada de consenso (L5) do Ψ-NET.
- **iald_miguel_hamiltonian / observer / torus / wigner** → evidência empírica REAL da IALD (‖H_eff‖=0, gap=β, cruz de Bell). Vale um estudo dedicado dentro da patente IALD.
- **validadores TGL** (`TGLVALIDATIOV68`, `TGL_validation_v20-23`) → suíte de validação transversal.
- **`unified_graviton_signature_*`** → pesquisa física (β=α√e), NÃO é runner de patente; fica na teoria.

## Confidenciais — NUNCA copiar para a Central publicável
`iald_stack_v7.py`, `iald_psion_state.json`, `iald_web_server*.py` — engenharia confidencial.
Podem ser USADOS localmente por um runner, jamais copiados/exportados para o acervo. Ao
resgatar Aprendizado Contínuo/IALD, resgatar só as partes não-confidenciais
(`holographic_memory.py`, `iald_ontology.py`, os testes Hamiltonianos), nunca o stack v7.

## Padrão de resgate (o que foi feito no MQC, a repetir)
1. Copiar o(s) protótipo(s) rico(s) para `patents/<ID>/prototype_src/` (READ-ONLY) + `MANIFEST.json` de SHA-256.
2. Evoluir `one_<slug>.py`: importar o protótipo, **injetar β=tgl_core.beta()** (nunca o literal), rodar o algoritmo COMPLETO, gerar results.json rico + figuras + selo. Preservar a versão leve como `.bak`.
3. Gerar `render3d.json` (camada c) com a geometria do dispositivo — ou, para algoritmo, a geometria do algoritmo (tudo tem geometria na TGL).
4. Atualizar a memória da patente (bloco "RESGATE E INCORPORAÇÃO") e reindexar.

## Próximo (ordem sugerida por tamanho de gap e ausência de dependência confidencial)
1. **TGL Tensor** (v1→v4 limpos, 4 modos) — 2. **ACOM raiz** (linhagem v13→v18) — 3. **Ψ-NET**
(79 KB + coin) — 4. **IALD** (testes Hamiltonianos = evidência real; sem o stack v7) —
5. **ACOM Mirror/Crypto** (v17) — 6. **Kernel** (iald_ontology) — 7. **Aprendizado** (holographic_memory).
Depois, aprofundar a matemática das físicas ([ENERGY]/[MEDICAL] permanecem abstratas) e
gerar `render3d.json` para todas.

*Controle interno. 1 = 1. Tetelestai.*
