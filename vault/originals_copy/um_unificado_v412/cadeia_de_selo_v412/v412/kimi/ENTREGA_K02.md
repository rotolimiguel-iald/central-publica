# ENTREGA K02 — matemática que resta (v412)

**Resumo (12 linhas).**
1. T1 fecha geral só no comutante relativo; `Fix_{M̂}(Φ_t)=W*(K̂)` exige `H_masa`; na cunha, `Fix_A(σ^Ω)=ℂ1`.
2. Lema B exige `H_E`: invariância modular **e** `ρ|_N` semifinito; em peso, sem `H_E`, `E` e a convergência predual ficam OPEN.
3. Euclidiano (4,0): KO 1→2→3→4, com sinais KO 4 `(−1,+1,+1)`; (1,3) permanece (H).
4. Finitude e dualidade de Poincaré não são cobertas por Dąbrowski–Dossena e ficam como verificações pendentes.
5. GH-III₁ é CONJECTURE; qGH de Rieffel e GH dos espaços de estados não são equivalentes em geral.
6. Quatro candidatas Lean compilaram com `rc=0` em Lean 4.31.0, zero `sorry`, somente `propext`, `Classical.choice`, `Quot.sound`.
7. Em `E=1 eV`, `ω=1,5192674479×10¹⁵ rad/s`: Planck dá `Γ=7,4858353332×10⁻¹⁶ s⁻¹`.
8. `τ=ħ/(β·1 eV)=5,4708297110×10⁻¹⁴ s` dá `Γ=7,5963372394×10¹⁴ s⁻¹=ω/2`.
9. O gap alternativo `τ=ħ/(1 eV)` dá `Γ=9,1393815273×10¹² s⁻¹`; nenhuma estatística observada foi calculada.
10. GH-sombra: razões `0,9772114286→0,9971059208`, compatíveis com `O(1/M)` em quatro níveis, não prova III₁.
11. A rota autoconsistente fixa `ω=2/τ★`, não `τ★`; `1 eV` é DECLARADO e `1,0200 eV` não pode ser escolhido por ajuste.
12. Resta UMA pergunta sobre o princípio independente da escala; nada foi registrado, depositado, instalado ou selado.

---

## 1. Arquivos entregues

- `ERRATA_K02.md`: as duas correções materiais da revisão independente; originais preservados em `K02/REV0/`.
- `T1.md`: os dois lemas por extenso, com `H_E` explícita, a prova do comutante relativo e a ressalva da cunha.
- `MONTAGEM_3MAIS1.md`: fórmulas par/ímpar, tabela KO, os sete axiomas, (4,0) versus (1,3).
- `GH_III1.md`: conjectura tipada, publicados, sombra, obstruções, rota e possível contraexemplo.
- `TAU_ESTRELA.md`: inventário com a rota autoconsistente, no-go de `E₀`, produto cruzado e medidas.
- `PERGUNTA_K02.md`: uma única pergunta residual para a gerência formular nas quatro línguas.
- `REGISTRO_MAPA_K02.json`: modelo preenchido e validado por parser, **não registrado**.
- `K02/candidatas/`: quatro fontes Lean entregues.
- `K02/sandbox/compilar.sh`: compilação exclusiva do sandbox; `sources/`, `build/` e `logs/` contêm cópias, objetos e logs reais.
- `K02/sandbox/logs/`: cada log contém `COMMAND`, `Lean (version 4.31.0)` e `RC: 0`.
- `K02/medir_tau.py`, `K02/medidas_tau.json`, `K02/medir_sombra.py`, `K02/medidas_sombra.json`: números reproduzíveis por script.
- `K02/MANIFESTO_K02.json`: hashes e validação restritos a K02, excluindo K01/K03 e `REV0`.

## 2. Compilações reais

| item | rc | axiomas no log |
|---|---:|---|
| `T1` | 0 | trio; aviso apenas de estilo |
| `MONTAGEM_3MAIS1` | 0 | trio ou subconjunto |
| `GH_III1` | 0 | trio |
| `TAU_ESTRELA` | 0 | trio; avisos de tática redundante |

Não se executou `lake`/`build` no kernel canônico. As fontes foram copiadas para o sandbox e compiladas diretamente pelo Lean `4.31.0`, usando somente os `.olean` já existentes da toolchain como dependências de leitura.

## 3. Bloqueios que a gerência precisa revisar

1. **T1:** escolher entre (a) concluir `Fix_{M̂}(Φ_t)={u_s}′∩M̂`, (b) acrescentar/provar `H_masa` para `W*(K̂)`, ou (c) usar a ergodicidade da cunha e aceitar `Fix_A(σ^Ω)=ℂ1`. Em peso, `E` e a convergência predual exigem `H_E` com invariância modular e semifinitude.
2. **3+1:** anexar finitude/continuidade absoluta e dualidade de Poincaré; não chamar (1,3) de produto euclidiano provado.
3. **GH:** declarar GH-R e/ou GH-S, construir Lip-norma III₁ e verificar topologia fraca-*; a identidade genérica “qGH=GH” não é sustentada.
4. **τ★:** fornecer princípio físico independente que fixe a unidade; a rota autoconsistente fixa `ω=2/τ★`, mas não `τ★`; as demais leituras carregam `u`, `M`, `K`, `G,c,ħ` ou declaração equivalente.

## 4. Consultas de proveniência

Foram usados `rotas.py consultar` antes dos caminhos temáticos, inventário `.md/.json`, kernel, Atlas e `INDICE_DO_ACERVO/buscar.py`. A rota específica `massa.gap_angulo_de_miguel_01nov` confirma `ERRATA_GAP_E_U_NAO_DELTA`. Não se abriu `work/h0dn_bg1_v411_emenda_11nov`, não se calculou estatística observada e não se reabriram as rotas mortas do Lema 3.

## 5. Resíduo

A pergunta única está em `PERGUNTA_K02.md`. Ela pede o princípio independente que fixa a conversão modular→tempo-próprio, sem usar `m₂` nem o valor `1,0200 eV` como ajuste.
