import TGLExt.PontoZeroDoPsion
import TGLExt.PontoDeContradicao
import Mathlib.FieldTheory.IsAlgClosed.Spectrum

noncomputable section
namespace ReviewU6Route
open TGLExt.PontoZeroDoPsion
open F1Rede.BosonicFock F1Rede.SectorDirectSum

theorem full_lock_spectrum_subset {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (Ω : H) :
    spectrum ℂ (lockDe Ω) ⊆ ({0, 1} : Set ℂ) :=
  IsIdempotentElem.spectrum_subset ℂ ((ℂ ∙ Ω).isIdempotentElem_starProjection.one_sub)

def sectorEnergy (ω : ℝ) (n : ℕ) : ℂ := (ω : ℂ) * ((n : ℂ) + 1/2)

def sectorGraph (ω : ℝ) (x y : F) : Prop :=
  ∀ k : ℕ, y k = sectorEnergy ω k • x k

theorem pure_sector_on_graph (ω : ℝ) (n : ℕ) (z : Sectors n) :
    sectorGraph ω (sectorEmbedding (E := Sectors) n z)
      (sectorEnergy ω n • sectorEmbedding (E := Sectors) n z) := by
  intro k
  by_cases h : k = n
  · subst k; rfl
  · simp [h]

theorem every_physical_sector_has_level (ω : ℝ) (n : ℕ) :
    ∃ x : F, x ≠ 0 ∧ sectorGraph ω x (sectorEnergy ω n • x) := by
  letI : Nontrivial (Sectors n) := F1Rede.BosonicSectors.sector_nontrivial n
  obtain ⟨z, hz⟩ := exists_ne (0 : Sectors n)
  refine ⟨sectorEmbedding (E := Sectors) n z, ?_, pure_sector_on_graph ω n z⟩
  exact fun h => hz ((sectorEmbedding (E := Sectors) n).injective (h.trans (map_zero _).symm))

theorem physical_vacuum_on_graph (ω : ℝ) :
    sectorGraph ω vacuum (sectorEnergy ω 0 • vacuum) :=
  pure_sector_on_graph ω 0 F1Rede.BosonicSectors.vacuumSector

#print axioms full_lock_spectrum_subset
#print axioms pure_sector_on_graph
#print axioms every_physical_sector_has_level
#print axioms physical_vacuum_on_graph
end ReviewU6Route
