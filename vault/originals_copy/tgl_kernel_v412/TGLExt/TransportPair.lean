import TGLExt.TransportCenter
import TGLExt.VinculoCriterion

/-! Unitary transport of the analytic realization in the continuous-core
criterion, including its resolvent, its polar antiunitary and its readout. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 140000
noncomputable section
namespace K07.Horizon.TransportCenter
open TGL.SpecificAQFT TGLV350.Regular F1Rede.BosonicFock F1Fecho
open F1Fecho.RegularCovariantCore F1Fecho.OrbitalSpatial ORDEM016.D6

section TransportGraph
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

private theorem conjugate_nonnegative (U : H ≃ₗᵢ[ℂ] H) (R : (H →L[ℂ] H)) (h : 0 ≤ R) :
    0 ≤ U.conjStarAlgEquiv R := by
  have he : U.conjStarAlgEquiv R = (U : (H →L[ℂ] H)) * R * star (U : (H →L[ℂ] H)) := by
    rw [LinearIsometryEquiv.star_eq_symm]
    rfl
  rw [he]
  exact star_right_conjugate_nonneg h _

/-- Construct the target realization for the transported graph; no target
realization or target modular action is supplied as a hypothesis. -/
def graphRealizationTransport (U : H ≃ₗᵢ[ℂ] H) (G G' : Set (H × H))
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) : ModularGraphRealization G' := by
  let e := U.conjStarAlgEquiv
  let R := e A.R
  let T := U.toHomeomorph.prodCongr U.toHomeomorph
  have hback : (U.symm.toHomeomorph.prodCongr U.symm.toHomeomorph) '' G' = G := by
    rw [← hg]
    change T.symm '' (T '' G) = G
    exact T.toEquiv.symm_image_image G
  have hmem (x y : H) : (U x,U y) ∈ G' ↔ (x,y) ∈ G := by
    rw [← hg]
    change T (x,y) ∈ T '' G ↔ _
    constructor
    · rintro ⟨p,hp,he⟩
      exact T.injective he ▸ hp
    · intro hp
      exact ⟨_, hp, rfl⟩
  have hs : 0 ≤ R := conjugate_nonnegative U A.R A.nonneg
  have hle : R ≤ 1 := by
    have h := conjugate_nonnegative U (1-A.R) (sub_nonneg.mpr A.le_one)
    simpa only [map_sub, map_one, sub_nonneg] using h
  have hcomp (S : (H →L[ℂ] H)) (hS : Function.Injective S) : Function.Injective (e S) :=
    U.injective.comp (hS.comp U.symm.injective)
  have hu : R * (U : (H →L[ℂ] H)) = (U : (H →L[ℂ] H)) * A.R := by
    ext1 x
    change U (A.R (U.symm (U x))) = U (A.R x)
    rw [U.symm_apply_apply]
  have hroot (x : H) : CFC.sqrt (resolventDampingOperator R) (U x) =
      U (CFC.sqrt (resolventDampingOperator A.R) x) :=
    congrArg (fun S : (H →L[ℂ] H) => S x)
      (positive_sqrt_intertwines _ _ (U : (H →L[ℂ] H))
        (resolventDampingOperator_nonneg R hs hle)
        (resolventDampingOperator_nonneg A.R A.nonneg A.le_one)
        (resolventDampingOperator_intertwines _ _ _ hu))
  refine { R := R, nonneg := hs, le_one := hle, injective := hcomp A.R A.injective,
           complement_injective := ?_, resolvent_mem := ?_, resolvent_inverse := ?_,
           graph_functional := ?_, J := (U.symm.trans A.J).trans U, polar_regularized := ?_ }
  · have hc := hcomp _ A.complement_injective
    simpa only [map_sub,map_one] using hc
  · intro x
    obtain ⟨x,rfl⟩ := U.surjective x
    have h := unitary_square_graph_forward U G G' hg _ _ (A.resolvent_mem x)
    change (U (A.R (U.symm (U x))), U x - U (A.R (U.symm (U x)))) ∈ _
    rw [U.symm_apply_apply]
    simpa only [map_sub] using h
  · intro x y hxy
    have h := unitary_square_graph_forward U.symm G' G hback x y hxy
    change U (A.R (U.symm (x+y))) = x
    rw [map_add, A.resolvent_inverse _ _ h, U.apply_symm_apply]
  · intro x y z hy hz
    obtain ⟨x,rfl⟩ := U.surjective x
    obtain ⟨y,rfl⟩ := U.surjective y
    obtain ⟨z,rfl⟩ := U.surjective z
    exact congrArg U (A.graph_functional _ _ _ ((hmem _ _).mp hy) ((hmem _ _).mp hz))
  · intro x
    obtain ⟨x,rfl⟩ := U.surjective x
    change (U (A.R (U.symm (U x))),
        U (A.J (U.symm (CFC.sqrt (resolventDampingOperator R) (U x))))) ∈ G'
    rw [U.symm_apply_apply, hroot, U.symm_apply_apply]
    exact (hmem _ _).mpr (A.polar_regularized x)

end TransportGraph

theorem measured_pair_transport (M N : VonNeumannAlgebra F) (Ω : F)
    (U : F ≃ₗᵢ[ℂ] F) (J : F ≃ₛₗᵢ[starRingEnd ℂ] F) (B : UnitaryFlow F)
    (he : ∀ A : Op, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N)
    (h : PairTomitaAnalyticRealizationMeasured M.toStarSubalgebra Ω J B.U) :
    PairTomitaAnalyticRealizationMeasured N.toStarSubalgebra (U Ω)
      ((U.symm.trans J).trans U) (conjugateFlow U B).U := by
  let C : ReconhecimentoPeloConteudo M.toStarSubalgebra N.toStarSubalgebra Ω (U Ω) :=
    ⟨U,rfl,he⟩
  obtain ⟨A,hj,hF⟩ := h
  let T := graphRealizationTransport U _ _ (recognition_closed_tomita_graph C) A
  have hJ (x : F) := recognizes_polar_factor U (recognition_closed_tomita_graph C) A T x
  have hR := recognizes_resolvent_operator U (recognition_closed_tomita_graph C) A T
  refine ⟨T, ?_, ?_⟩
  · ext1 x
    obtain ⟨x,rfl⟩ := U.surjective x
    change T.J (U x) = U (J (U.symm (U x)))
    rw [U.symm_apply_apply, ← hj]
    exact (hJ x).symm
  · intro t x
    obtain ⟨x,rfl⟩ := U.surjective x
    have hd : resolventDampingOperator T.R (U x) = U (resolventDampingOperator A.R x) :=
      congrArg (fun S : Op => S x) (resolventDampingOperator_intertwines T.R A.R _ hR)
    have hp : resolventPhaseOperator T.R t (U x) = U (resolventPhaseOperator A.R t x) :=
      congrArg (fun S : Op => S x) (resolventPhaseOperator_intertwines T.R A.R _
        (IsSelfAdjoint.of_nonneg T.nonneg) (IsSelfAdjoint.of_nonneg A.nonneg) hR t)
    change U (B.U t (U.symm (resolventDampingOperator T.R (U x)))) = _
    rw [hd,U.symm_apply_apply,hF,hp]

private theorem orbit_span_image (M N : VonNeumannAlgebra F) (Ω : F) (U : F ≃ₗᵢ[ℂ] F)
    (he : ∀ A : Op, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N) :
    U '' ((Submodule.span ℂ ((fun z : Op => z Ω) '' (M : Set Op))) : Set F) =
      ((Submodule.span ℂ ((fun z : Op => z (U Ω)) '' (N : Set Op))) : Set F) := by
  let e := U.conjStarAlgEquiv
  have horbit : U '' ((fun z : Op => z Ω) '' (M : Set Op)) =
      (fun z : Op => z (U Ω)) '' (N : Set Op) := by
    ext x
    constructor
    · rintro ⟨_,⟨z,hz,rfl⟩,rfl⟩
      exact ⟨e z,(he z).mp hz,by simp [e]⟩
    · rintro ⟨w,hw,rfl⟩
      obtain ⟨z,rfl⟩ := e.surjective w
      refine ⟨z Ω,⟨z,(he z).mpr hw,rfl⟩,?_⟩
      change U (z Ω) = U (z (U.symm (U Ω)))
      rw [U.symm_apply_apply]
  change ((Submodule.map U.toLinearEquiv.toLinearMap (Submodule.span ℂ _)) : Set F) = _
  rw [Submodule.map_span]
  exact congrArg (fun S : Set F => ((Submodule.span ℂ S) : Set F)) horbit

theorem typeIII1_transport (M N : VonNeumannAlgebra F) (U : F ≃ₗᵢ[ℂ] F)
    (he : ∀ A : Op, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N)
    (h : Vinculo.IsTypeIII1 M) : Vinculo.IsTypeIII1 N := by
  obtain ⟨hM, Ω,J,B,hn,hc,hs,hT,ha,hcore⟩ := h
  refine ⟨scalar_center_transport M N _ he hM, U Ω, (U.symm.trans J).trans U,
    conjugateFlow U B,(U.norm_map Ω).trans hn,?_,?_,
    measured_pair_transport M N Ω U J B he hT,?_,
    scalar_center_transport _ _ _ (core_covariance_of U B M N he) hcore⟩
  · rw [← orbit_span_image M N Ω U he]
    rw [dense_iff_closure_eq]
    let S : Set F := ↑(Submodule.span ℂ ((fun z : Op => z Ω) '' (M : Set Op)))
    have hd : closure S = Set.univ := hc.closure_eq
    change closure (U.toHomeomorph '' S) = Set.univ
    rw [← U.toHomeomorph.image_closure, hd]
    exact Set.image_univ_of_surjective U.toHomeomorph.surjective
  · intro z hz h0
    obtain ⟨y,rfl⟩ := U.conjStarAlgEquiv.surjective z
    change U (y (U.symm (U Ω))) = 0 at h0
    rw [U.symm_apply_apply] at h0
    have hy : y Ω = 0 := U.injective (h0.trans (map_zero U).symm)
    change U.conjStarAlgEquiv y = 0
    rw [hs y ((he y).mpr hz) hy, map_zero]
  · intro t z
    obtain ⟨y,rfl⟩ := U.conjStarAlgEquiv.surjective z
    have hcon : automorphism (conjugateFlow U B) t (U.conjStarAlgEquiv y) =
        U.conjStarAlgEquiv (automorphism B t y) := by
      ext1 x
      simp [automorphism,boostIso,conjugateFlow]
    change automorphism (conjugateFlow U B) t (U.conjStarAlgEquiv y) ∈ N ↔ U.conjStarAlgEquiv y ∈ N
    rw [hcon, ← he, ← he]
    exact ha t y

theorem observer_wedge_typeIII1 (L : generatedLorentz) (a : Point)
    (h : Vinculo.IsTypeIII1 (PhysicalFockNet.net rightWedge)) :
    Vinculo.IsTypeIII1 (frameAlg L a) :=
  typeIII1_transport _ _ _ (fun z => (observer_and_wedge_algebra L a z).2) h

end K07.Horizon.TransportCenter
