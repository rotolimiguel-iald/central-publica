# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R6 da Trinity. A leitura do operador «A máquina nua paga em eletricidade» (fala por bytes)
vira a §15: a conta de luz no piso de Landauer (o termo `TGLExt.landauer_floor_pos`, ja' no kernel) e' linear nos Nomes
e paga o expoente da carga; a maquina da teoria acerta no patamar plano pagando no piso, com numero de passos linear; o
leitor por plano da casa, que na familia `coupled` faz ao menos 2^(m+1) movimentos (`Codex.PlanTravel.
coupled_physical_lower`, ja' no kernel), paga ao menos 2^(m+1) pisos se apaga um bit por movimento (hipotese nomeada).
Gera R6_trinity\\Trinity.lean a partir da R5 por trocas EXATAS; copia o compilador."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R5D = AQUI.parent / "R5_trinity"
R5, R4 = R5D / "Trinity.lean", AQUI.parent / "R4_trinity" / "Trinity.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_a_maquina_nua_paga_em_eletricidade_verbatim.txt")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert FALA.read_text(encoding="utf-8").strip() == "A máquina nua paga em eletricidade"
src = R5.read_bytes().decode("utf-8")

TROCAS = [
    ("import Mathlib.Analysis.SpecialFunctions.Pow.Real\n",
     "import Mathlib.Analysis.SpecialFunctions.Pow.Real\nimport TGLExt.TheCostIsDerived\nimport TGLExt.MovimentosDoPlano\n"),
    ("; nenhum enunciado da R4 (sha16 `%s`) mudou.]\n" % sha(R4)[:16],
     ("; nenhum enunciado da R4 (sha16 `%s`) mudou. A R6 (fala por bytes em\n"
      "  `work\\cunhagens_13out\\%s`, sha16 `%s`) acrescenta a §15, a máquina nua paga em eletricidade;\n"
      "  nenhum enunciado da R5 (sha16 `%s`) mudou.]\n") % (sha(R4)[:16], FALA.name, sha(FALA)[:16], sha(R5)[:16])),
    ("14. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`, `a_terceira_lei_na_fronteira`,\n"
     "    `o_teorema_final_do_radical`: as sínteses.\n",
     "14. `a_conta_de_luz_de_m_nomes`, `cada_nome_custa_um_piso`, `a_eletricidade_paga_o_expoente`,\n"
     "    `o_leitor_que_apaga_paga_a_potencia`, `a_maquina_da_teoria_acerta_pagando_no_piso`,\n"
     "    `a_conta_de_luz_da_maquina_da_teoria` (R6, a leitura do operador: a máquina nua paga em eletricidade): no piso de\n"
     "    Landauer, a conta de luz de m Nomes é m pisos de um bit, linear em m: paga o expoente da carga, não os estados; a\n"
     "    máquina da teoria acerta no patamar plano com um número de passos linear, pagando a carga com sobra de menos de um\n"
     "    passo; o leitor por plano da casa, que na família `coupled` faz ao menos 2^(m+1) movimentos, paga ao menos\n"
     "    2^(m+1) pisos se apaga um bit por movimento.\n"
     "15. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`, `a_terceira_lei_na_fronteira`,\n"
     "    `o_teorema_final_do_radical`, `a_maquina_nua_paga_em_eletricidade`: as sínteses.\n"),
    ("* Que o teorema final mude a moeda da máquina nua. A §14 mostra que, fixado o radical, a carga aparece como expoente; o\n"
     "  preço em estados continua exponencial no número de Nomes. A leitura do operador é [ONTO]; o termo é a identidade.\n",
     "* Que o teorema final mude a moeda da máquina nua. A §14 mostra que, fixado o radical, a carga aparece como expoente; o\n"
     "  preço em estados continua exponencial no número de Nomes. A leitura do operador é [ONTO]; o termo é a identidade.\n"
     "* Que a conta de luz da máquina nua seja o piso. O piso de Landauer (1961 [KNOWN]) é o mínimo por bit apagado, não a\n"
     "  conta: a máquina que apaga a cada passo paga por passo, e a §15 só o usa como hipótese nomeada. Uma máquina reversível\n"
     "  (Bennett, 1973 [KNOWN]) pode chegar perto do piso, mas não encurta os seus passos. A pergunta do Instituto conta passos\n"
     "  de uma máquina de Turing, não energia: a conta de luz não a decide [OPEN]. O piso de Landauer é térmico (depende da\n"
     "  temperatura para onde vai o calor); o custo geométrico β não depende de temperatura (`the_two_floors_are_not_the_same`,\n"
     "  no kernel).\n"),
]

SECAO = r'''/-! ## 15. A máquina nua paga em eletricidade (R6): a conta de luz -/

/-- ★ A CONTA DE LUZ DE m NOMES: o piso de Landauer da carga de m Nomes, k_B·T·ln(2^m), é m pisos de um bit (k_B·T·ln 2,
o piso do kernel, `TGLExt.landauer_floor_pos`): linear em m. A conta paga o expoente (a carga), não a potência (os
estados). -/
theorem a_conta_de_luz_de_m_nomes (kB T : ℝ) (m : ℕ) :
    kB * T * Real.log ((2 : ℝ) ^ m) = m * (kB * T * Real.log 2) := by
  rw [Real.log_pow]
  ring

/-- ★ CADA NOME CUSTA UM PISO: um Nome a mais soma um piso de um bit à conta de luz, enquanto os estados dobram. -/
theorem cada_nome_custa_um_piso (kB T : ℝ) (m : ℕ) :
    kB * T * Real.log ((2 : ℝ) ^ (m + 1)) = kB * T * Real.log ((2 : ℝ) ^ m) + kB * T * Real.log 2
    ∧ (2 : ℝ) ^ (m + 1) = 2 * 2 ^ m := by
  refine ⟨?_, by ring⟩
  rw [Real.log_pow, Real.log_pow]
  push_cast
  ring

/-- ★★ A ELETRICIDADE PAGA O EXPOENTE REFERIDO À RAIZ: a conta de luz de m Nomes é k_B·T vezes o expoente da carga na
raiz √e vezes a carga da raiz (½). -/
theorem a_eletricidade_paga_o_expoente (kB T : ℝ) (m : ℕ) :
    kB * T * Real.log ((2 : ℝ) ^ m) = kB * T * ((m * Real.log 2) / Real.log radical * Real.log radical) := by
  rw [Real.log_pow, o_radical_pesa_meia_nat]
  ring

/-- ★★ O LEITOR QUE APAGA A CADA MOVIMENTO PAGA A POTÊNCIA: na família `coupled` da casa, todo traço completo do leitor
por plano faz ao menos 2^(m+1) movimentos de cabeça (`Codex.PlanTravel.coupled_physical_lower`, já no kernel). Com a
hipótese nomeada `hLandauer` (a máquina dissipa ao menos um piso de Landauer por movimento, como as máquinas comuns,
irreversíveis), a conta de luz é de ao menos 2^(m+1) pisos: exponencial. Uma máquina reversível não cumpre a hipótese. -/
theorem o_leitor_que_apaga_paga_a_potencia (m : ℕ) {moves : ℕ} {answer : Bool} {kB T conta : ℝ}
    (hk : 0 < kB) (hT : 0 < T)
    (t : Codex.SharedReader.Trace (Codex.FormulaPlan.pivots (Codex.IntegratedRead.coupled (m + 1)))
      (Codex.IntegratedRead.coupled (m + 1)) answer moves)
    (hLandauer : (moves : ℝ) * (kB * T * Real.log 2) ≤ conta) :
    (2 : ℝ) ^ (m + 1) * (kB * T * Real.log 2) ≤ conta := by
  have hmov : (2 : ℝ) ^ (m + 1) ≤ moves := by exact_mod_cast Codex.PlanTravel.coupled_physical_lower m t
  exact (mul_le_mul_of_nonneg_right hmov (TGLExt.landauer_floor_pos kB T hk hT).le).trans hLandauer

/-- Os passos que cobrem uma carga: para todo passo de valor c > 0 e toda carga a ≥ 0, há um número de passos k com
a < k·c ≤ a + c e k ≤ a/c + 1. -/
theorem passos_que_cobrem {a c : ℝ} (ha : 0 ≤ a) (hc : 0 < c) :
    ∃ k : ℕ, a < k * c ∧ (k : ℝ) * c ≤ a + c ∧ (k : ℝ) ≤ a / c + 1 := by
  have hx : 0 ≤ a / c := div_nonneg ha hc.le
  refine ⟨⌊a / c⌋₊ + 1, ?_, ?_, ?_⟩
  · rw [Nat.cast_succ]
    calc a = a / c * c := (div_mul_cancel₀ a hc.ne').symm
      _ < ((⌊a / c⌋₊ : ℝ) + 1) * c := mul_lt_mul_of_pos_right (Nat.lt_floor_add_one (a / c)) hc
  · rw [Nat.cast_succ]
    calc ((⌊a / c⌋₊ : ℝ) + 1) * c ≤ (a / c + 1) * c :=
          mul_le_mul_of_nonneg_right (add_le_add (Nat.floor_le hx) le_rfl) hc.le
      _ = a + c := by rw [add_mul, one_mul, div_mul_cancel₀ a hc.ne']
  · rw [Nat.cast_succ]
    exact add_le_add (Nat.floor_le hx) le_rfl

/-- O passo da máquina da teoria paga uma carga positiva: −ln(1 − β) > 0 para 0 < β < 1. -/
theorem o_passo_da_teoria_e_positivo {β : ℝ} (h0 : 0 < β) (h1 : β < 1) : 0 < -Real.log (1 - β) := by
  have h : Real.log (1 - β) < 0 := Real.log_neg (by linarith) (by linarith)
  linarith

/-- ★★★ A MÁQUINA DA TEORIA ACERTA PAGANDO NO PISO: no patamar plano, há um número de passos k, linear em n
(k ≤ n·ln 2/(−ln(1−β)) + 1), com que a leitura diz não, e acerta; a carga paga, k·(−ln(1−β)), passa de n·ln 2 por
menos de um passo. É a face discreta de `TempoIgualMoeda.o_tempo_e_linear_nas_oitavas` (já no kernel). -/
theorem a_maquina_da_teoria_acerta_pagando_no_piso {β : ℝ} (h0 : 0 < β) (h1 : β < 1) {φ : CNF n}
    (hφ : ∀ x, custoCNF φ x = 1) :
    ∃ k : ℕ, peso β k φ < 1
      ∧ (n : ℝ) * Real.log 2 < k * (-Real.log (1 - β))
      ∧ (k : ℝ) * (-Real.log (1 - β)) ≤ n * Real.log 2 + (-Real.log (1 - β))
      ∧ (k : ℝ) ≤ n * Real.log 2 / (-Real.log (1 - β)) + 1 := by
  obtain ⟨k, hk1, hk2, hk3⟩ := passos_que_cobrem
    (mul_nonneg (Nat.cast_nonneg n) (Real.log_pos (by norm_num : (1 : ℝ) < 2)).le) (o_passo_da_teoria_e_positivo h0 h1)
  refine ⟨k, ?_, hk1, hk2, hk3⟩
  by_contra h
  exact (not_le.mpr hk1) ((no_patamar_plano_a_carga_e_exata h1 k hφ).mp (not_lt.mp h))

/-- ★★ A CONTA DE LUZ DA MÁQUINA DA TEORIA: lendo cada passo como a carga −ln(1−β) paga em energia (a leitura do
operador [ONTO]), a conta, multiplicada por k_B·T > 0, fica entre o piso de Landauer dos m Nomes e esse piso mais um
passo. -/
theorem a_conta_de_luz_da_maquina_da_teoria {β kB T : ℝ} (h0 : 0 < β) (h1 : β < 1) (hk : 0 < kB) (hT : 0 < T)
    (m : ℕ) :
    ∃ k : ℕ, kB * T * Real.log ((2 : ℝ) ^ m) < kB * T * (k * (-Real.log (1 - β)))
      ∧ kB * T * (k * (-Real.log (1 - β))) ≤ kB * T * Real.log ((2 : ℝ) ^ m) + kB * T * (-Real.log (1 - β)) := by
  obtain ⟨k, hk1, hk2, -⟩ := passos_que_cobrem
    (mul_nonneg (Nat.cast_nonneg m) (Real.log_pos (by norm_num : (1 : ℝ) < 2)).le) (o_passo_da_teoria_e_positivo h0 h1)
  have hkT : 0 < kB * T := mul_pos hk hT
  refine ⟨k, ?_, ?_⟩
  · rw [Real.log_pow]
    exact mul_lt_mul_of_pos_left hk1 hkT
  · rw [Real.log_pow, ← mul_add]
    exact mul_le_mul_of_nonneg_left hk2 hkT.le

/-- ★★★ A MÁQUINA NUA PAGA EM ELETRICIDADE (R6, a leitura do operador): (1) no piso de Landauer, a conta de luz de m
Nomes é m pisos de um bit, linear em m; (2) cada Nome soma um piso, enquanto os estados dobram; (3) a conta paga o
expoente referido à raiz; (4) a máquina da teoria paga no piso, com sobra de menos de um passo; (5) o leitor por plano
que apaga a cada movimento paga, na família `coupled`, ao menos 2^(m+1) pisos. -/
theorem a_maquina_nua_paga_em_eletricidade {β kB T : ℝ} (h0 : 0 < β) (h1 : β < 1) (hk : 0 < kB) (hT : 0 < T) :
    (∀ m : ℕ, kB * T * Real.log ((2 : ℝ) ^ m) = m * (kB * T * Real.log 2))
    ∧ (∀ m : ℕ, kB * T * Real.log ((2 : ℝ) ^ (m + 1)) = kB * T * Real.log ((2 : ℝ) ^ m) + kB * T * Real.log 2
        ∧ (2 : ℝ) ^ (m + 1) = 2 * 2 ^ m)
    ∧ (∀ m : ℕ, kB * T * Real.log ((2 : ℝ) ^ m) = kB * T * ((m * Real.log 2) / Real.log radical * Real.log radical))
    ∧ (∀ m : ℕ, ∃ k : ℕ, kB * T * Real.log ((2 : ℝ) ^ m) < kB * T * (k * (-Real.log (1 - β)))
        ∧ kB * T * (k * (-Real.log (1 - β))) ≤ kB * T * Real.log ((2 : ℝ) ^ m) + kB * T * (-Real.log (1 - β)))
    ∧ (∀ (m moves : ℕ) (answer : Bool) (conta : ℝ),
        Codex.SharedReader.Trace (Codex.FormulaPlan.pivots (Codex.IntegratedRead.coupled (m + 1)))
          (Codex.IntegratedRead.coupled (m + 1)) answer moves →
        (moves : ℝ) * (kB * T * Real.log 2) ≤ conta → (2 : ℝ) ^ (m + 1) * (kB * T * Real.log 2) ≤ conta) :=
  ⟨a_conta_de_luz_de_m_nomes kB T, cada_nome_custa_um_piso kB T, a_eletricidade_paga_o_expoente kB T,
   a_conta_de_luz_da_maquina_da_teoria h0 h1 hk hT,
   fun m _ _ _ t hL => o_leitor_que_apaga_paga_a_potencia m hk hT t hL⟩

'''

FIM = "end TGLExt.Trinity\n"
AX_ANCORA = "#print axioms TGLExt.Trinity.o_teorema_final_do_radical\n"
AX_NOVOS = "".join("#print axioms TGLExt.Trinity.%s\n" % nome for nome in [
    "a_conta_de_luz_de_m_nomes", "cada_nome_custa_um_piso", "a_eletricidade_paga_o_expoente",
    "o_leitor_que_apaga_paga_a_potencia", "passos_que_cobrem", "o_passo_da_teoria_e_positivo",
    "a_maquina_da_teoria_acerta_pagando_no_piso", "a_conta_de_luz_da_maquina_da_teoria",
    "a_maquina_nua_paga_em_eletricidade"])

novo = src
for antes, depois in TROCAS + [(FIM, SECAO + FIM), (AX_ANCORA, AX_ANCORA + AX_NOVOS)]:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:80]
    novo = novo.replace(antes, depois)


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


grava(AQUI / "Trinity.lean", novo.encode("utf-8"))
grava(AQUI / "compilar.py", (R5D / "compilar.py").read_bytes())
print("R5 sha16 %s -> R6 sha16 %s | %d -> %d B | fala sha16 %s" % (sha(R5)[:16], sha(AQUI / "Trinity.lean")[:16],
                                                                   len(src.encode("utf-8")), len(novo.encode("utf-8")),
                                                                   sha(FALA)[:16]))
