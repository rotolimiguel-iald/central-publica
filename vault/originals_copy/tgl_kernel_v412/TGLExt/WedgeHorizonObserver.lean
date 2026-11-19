import TGLExt.F1Fecho394.PhysicalFockNetRealizationR2
import TGLExt.FlagNetV31

/-! Covariant two-sided reading of the actual right-wedge boundary and its
Maxwell Weyl algebra. A transverse shear supplies a negative control. -/

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section

namespace K07.Horizon
open Filter Topology TGL.SpecificAQFT TGLExt TGLExt.ContratoQGv31
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.MaxwellLocalization
open F1Fecho.OrbitalScreen F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz
open F1Fecho.MaxwellGlobal F1Fecho.PhysicalFockNet

abbrev Point := Fin 4 → ℝ

def u (x : Point) := x 1 + x 0
def v (x : Point) := x 1 - x 0
def futureSheet : Set Point := {x | v x = 0 ∧ 0 ≤ u x}
def pastSheet : Set Point := {x | u x = 0 ∧ 0 ≤ v x}

theorem wedge_read (x : Point) : x ∈ rightWedge ↔ 0 < u x ∧ 0 < v x := by
  change |x 0| < x 1 ↔ _
  rw [abs_lt]
  unfold u v
  constructor <;> intro h <;> constructor <;> linarith [h.1, h.2]

theorem closure_rightWedge :
    closure rightWedge = {x : Point | |x 0| ≤ x 1} := by
  apply Set.Subset.antisymm
  · refine closure_minimal ?_ (isClosed_le (by fun_prop) (by fun_prop))
    intro x hx
    exact (show |x 0| < x 1 from hx).le
  · intro x hx
    change |x 0| ≤ x 1 at hx
    let d : Point := fun i => if i=1 then 1 else 0
    let p : ℝ → Point := fun t => x + t • d
    have hc : Continuous p := by dsimp [p]; fun_prop
    have ht : Tendsto (fun n : ℕ => p (1 / ((n:ℝ)+1))) atTop (𝓝 x) := by
      have h := (hc.continuousAt (x := 0)).tendsto.comp
        (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
      simpa [Function.comp_def,p] using h
    apply mem_closure_of_tendsto ht
    apply Eventually.of_forall
    intro n
    change |(p (1/((n:ℝ)+1))) 0| < (p (1/((n:ℝ)+1))) 1
    change |x 0 + (1 / ((n:ℝ)+1)) * (0:ℝ)| < x 1 + (1 / ((n:ℝ)+1)) * 1
    rw [mul_zero,add_zero,mul_one]
    exact lt_add_of_le_of_pos hx (by positivity)

theorem boundary_two_sheets : frontier rightWedge = futureSheet ∪ pastSheet := by
  have ho : IsOpen rightWedge := isOpen_lt (by fun_prop) (by fun_prop)
  rw [frontier, closure_rightWedge, ho.interior_eq]
  ext x
  change (|x 0| ≤ x 1 ∧ ¬ |x 0| < x 1) ↔
    (v x = 0 ∧ 0 ≤ u x) ∨ (u x = 0 ∧ 0 ≤ v x)
  unfold u v
  constructor
  · intro h
    have he := le_antisymm h.1 (le_of_not_gt h.2)
    rcases le_total 0 (x 0) with hp | hn
    · rw [abs_of_nonneg hp] at he
      exact Or.inl ⟨by linarith, by linarith⟩
    · rw [abs_of_nonpos hn] at he
      exact Or.inr ⟨by linarith, by linarith⟩
  · rintro (⟨he,h⟩ | ⟨he,h⟩)
    · rw [abs_of_nonneg (show 0 ≤ x 0 by linarith)]
      exact ⟨by linarith, by linarith⟩
    · rw [abs_of_nonpos (show x 0 ≤ 0 by linarith)]
      exact ⟨by linarith, by linarith⟩

theorem bifurcation (x : Point) :
    x ∈ futureSheet ∩ pastSheet ↔ x 0 = 0 ∧ x 1 = 0 := by
  change ((x 1-x 0=0 ∧ 0≤x 1+x 0) ∧ (x 1+x 0=0 ∧ 0≤x 1-x 0)) ↔ _
  constructor
  · rintro ⟨⟨h1,_⟩,h2,_⟩
    exact ⟨by linarith, by linarith⟩
  · rintro ⟨h1,h2⟩
    simp [h1,h2]

def readPoint (x : Point) : Point := ![u x,v x,x 2,x 3]

theorem readPoint_injective : Function.Injective readPoint := by
  intro x y he
  have h0 : x 1+x 0=y 1+y 0 := congrFun he 0
  have h1 : x 1-x 0=y 1-y 0 := congrFun he 1
  funext i
  fin_cases i
  · change x 0 = y 0
    linarith
  · change x 1 = y 1
    linarith
  · exact congrFun he 2
  · exact congrFun he 3

theorem boost_read (s : ℝ) (x : Point) :
    u (wedgeBoostMap s x)=Real.exp s*u x ∧
    v (wedgeBoostMap s x)=Real.exp (-s)*v x ∧
    wedgeBoostMap s x 2=x 2 ∧ wedgeBoostMap s x 3=x 3 := by
  unfold u v
  rw [wedgeBoostMap_apply0,wedgeBoostMap_apply1,←Real.cosh_add_sinh,←Real.cosh_sub_sinh]
  refine ⟨by ring, by ring, ?_, ?_⟩ <;>
    simp [wedgeBoostMap,boostMat,Matrix.mulVec,dotProduct,Fin.sum_univ_four]

def observerChart (L : generatedLorentz) (a : Point) : Point ≃ₜ Point where
  toFun x := lorentzEquiv L.val x + a
  invFun x := (lorentzEquiv L.val).symm (x - a)
  left_inv x := by simp
  right_inv x := by simp
  continuous_toFun := (lorentzEquiv L.val).toContinuousLinearEquiv.continuous.add continuous_const
  continuous_invFun := (lorentzEquiv L.val).symm.toContinuousLinearEquiv.continuous.comp
    (continuous_id.sub continuous_const)

theorem observer_region (L : generatedLorentz) (a : Point) (O : Set Point) :
    observerChart L a '' O = TGL.SpecificAQFT.translate a (lorentzEquiv L.val '' O) := by
  ext y
  constructor
  · rintro ⟨x,hx,rfl⟩
    exact ⟨lorentzEquiv L.val x,⟨x,hx,rfl⟩,rfl⟩
  · rintro ⟨_,⟨x,hx,rfl⟩,rfl⟩
    exact ⟨x,hx,rfl⟩

theorem coordinate_lorentz_region (L : generatedLorentz) (O : Set Point) :
    coordinateRegion (lorentzEquiv L.val '' O) = lorentzRegion L (coordinateRegion O) := by
  ext x
  constructor
  · rintro ⟨y,hy,he⟩
    refine ⟨spacetimeOf y,hy,?_⟩
    apply PiLp.ext
    intro i
    exact congrFun he i
  · rintro ⟨y,hy,rfl⟩
    exact ⟨fun i => y i,hy,rfl⟩

def observerUnitary (L : generatedLorentz) (a : Point) : H1 ≃ₗᵢ[ℂ] H1 :=
  (helicityUnitary L).trans (U1 a)

theorem canonical_one_particle_covariance (L : generatedLorentz) (a : Point)
    (O : Set Point) (f : H1) :
    f ∈ physicalCanonicalNet.K O ↔ observerUnitary L a f ∈
        physicalCanonicalNet.K (observerChart L a '' O) := by
  rw [observer_region]
  change f ∈ compactPhysicalNet O ↔ U1 a (helicityUnitary L f) ∈ compactPhysicalNet _
  have hL := compactLocalized_lorentz_iff L (coordinateRegion O) f
  rw [←coordinate_lorentz_region] at hL
  exact hL.trans (compactPhysicalNet_translate a (lorentzEquiv L.val '' O) (helicityUnitary L f))

theorem observer_and_wedge_algebra (L : generatedLorentz) (a : Point)
    (A : F →L[ℂ] F) :
    frontier (observerChart L a '' rightWedge) =
      (observerChart L a '' futureSheet) ∪ (observerChart L a '' pastSheet) ∧
    (A ∈ net rightWedge ↔ (gamma (observerUnitary L a)).conjStarAlgEquiv A ∈
      net (observerChart L a '' rightWedge)) := by
  refine ⟨?_, net_covariant _ _ _ (canonical_one_particle_covariance L a rightWedge) A⟩
  rw [←(observerChart L a).image_frontier, boundary_two_sheets, Set.image_union]

theorem boost_read_and_kms_action (t : ℝ) (x : Point) (A : F →L[ℂ] F) :
    u (wedgeBoostMap (2*Real.pi*t) x) = Real.exp (2*Real.pi*t) * u x ∧
    v (wedgeBoostMap (2*Real.pi*t) x) = Real.exp (-(2*Real.pi*t)) * v x ∧
    (A ∈ net rightWedge ↔ (gamma (B0 (2*Real.pi*t))).conjStarAlgEquiv A ∈ net rightWedge) := by
  have h := boost_read (2*Real.pi*t) x
  refine ⟨h.1,h.2.1,net_covariant _ _ _ ?_ A⟩
  intro f
  simpa only [FlagNet.boost_image_rightWedge] using
    physicalCanonicalNet.K_boost (2*Real.pi*t) rightWedge f

/-! The null branches and their transverse labels alone admit a smooth
one-parameter shear which fixes every boundary point but changes intervals. -/

def shear (s : ℝ) (x : Point) : Point := ![x 0,x 1,x 2+s*(u x*v x),x 3]

theorem shear_add (s t : ℝ) (x : Point) : shear (s+t) x = shear s (shear t x) := by
  funext i
  fin_cases i
  all_goals first | rfl | (simp [shear,u,v]; ring)

theorem shear_fixes_boundary (s : ℝ) (x : Point) (hx : x ∈ frontier rightWedge) :
    shear s x = x := by
  rw [boundary_two_sheets] at hx
  have h : u x * v x = 0 := hx.elim (fun z => mul_eq_zero_of_right _ z.1)
    (fun z => mul_eq_zero_of_left z.1 _)
  funext i
  fin_cases i <;> simp [shear,h]

theorem shear_refutes_interval_preservation (s : ℝ) (hs : s≠0) :
    minkowskiSq (shear s ![0,1,0,0]) ≠ minkowskiSq ![0,1,0,0] := by
  simp [minkowskiSq,shear,u,v]
  nlinarith [sq_pos_of_ne_zero hs]

/-- Independent transverse labels survive on each generator and on the bifurcation plane. -/
theorem generator_labels (r y z : ℝ) (hr : 0 ≤ r) :
    (![r,r,y,z] : Point) ∈ futureSheet ∧ (![-r,r,y,z] : Point) ∈ pastSheet ∧
    (![0,0,y,z] : Point) ∈ futureSheet ∩ pastSheet := by
  refine ⟨?_,?_,(bifurcation _).2 ⟨rfl,rfl⟩⟩
  · change r-r=0 ∧ 0≤r+r
    exact ⟨by ring, by linarith⟩
  · change r+(-r)=0 ∧ 0≤r-(-r)
    exact ⟨by ring, by linarith⟩

theorem inward_null_translations (t : ℝ) (ht : 0 ≤ t) :
    TGL.SpecificAQFT.translate (t • nullPlus) rightWedge ⊆ rightWedge ∧
    TGL.SpecificAQFT.translate ((-t) • nullMinus) rightWedge ⊆ rightWedge := by
  constructor <;> rintro _ ⟨x,hx,rfl⟩ <;>
    obtain ⟨h1,h2⟩ := (wedge_read x).1 hx <;> apply (wedge_read _).2 <;>
    simp [u,v,nullPlus,nullMinus] at * <;> constructor <;> linarith

theorem null_translations_fock (t : ℝ) (ht : 0 ≤ t) (A : F →L[ℂ] F)
    (hA : A ∈ net rightWedge) :
    (gamma (U1 (t • nullPlus))).conjStarAlgEquiv A ∈ net rightWedge ∧
    (gamma (U1 ((-t) • nullMinus))).conjStarAlgEquiv A ∈ net rightWedge := by
  have hlocal (a : Point) (h : TGL.SpecificAQFT.translate a rightWedge ⊆ rightWedge) :
      (gamma (U1 a)).conjStarAlgEquiv A ∈ net rightWedge := by
    apply net_mono _ _ h
    exact (net_covariant (U1 a) rightWedge (TGL.SpecificAQFT.translate a rightWedge)
      (physicalCanonicalNet.K_translate a rightWedge) A).1 hA
  exact ⟨hlocal _ (inward_null_translations t ht).1,
    hlocal _ (inward_null_translations t ht).2⟩

open MeasureTheory AuditF13v31 F1Rede.Canonical in
theorem modular_read_with_fiber (t : ℝ) (x : Point) (f : H1) :
    u (wedgeBoostMap (-(2*Real.pi*t)) x) = Real.exp (-(2*Real.pi*t)) * u x ∧
    v (wedgeBoostMap (-(2*Real.pi*t)) x) = Real.exp (2*Real.pi*t) * v x ∧
    ((⇑(canonicalPartialFourier (B0 (-(2 * Real.pi * t)) f)) : ℝ → TransverseFiber) =ᵐ[volume]
      fun ξ => Complex.exp (((t * canonicalSigma ξ : ℝ) : ℂ) * Complex.I) •
        (⇑(canonicalPartialFourier f) : ℝ → TransverseFiber) ξ) := by
  have hb := boost_read (-(2*Real.pi*t)) x
  exact ⟨hb.1, by simpa only [neg_neg] using hb.2.1,
    canonical_modularGroupIsBoost t f⟩

/-- A relative reading is evaluated in the observer's own affine chart. -/
def observerRead (L : generatedLorentz) (a y : Point) : Point :=
  readPoint ((observerChart L a).symm y)

theorem observerRead_covariant (L : generatedLorentz) (a x : Point) :
    observerRead L a (observerChart L a x) = readPoint x := by
  simp [observerRead]

/-- A positive-radius uniformly accelerated observer recovers rapidity from null contrast.
Its transverse labels are unrestricted. -/
theorem observer_recovers_rapidity (ρ s y z : ℝ) (hρ : 0<ρ) :
    let x : Point := wedgeBoostMap s ![0,ρ,y,z]
    u x / v x = Real.exp (2*s) ∧ Real.log (u x / v x) / 2 = s := by
  let p : Point := ![0,ρ,y,z]
  have hu : u p=ρ := by simp [p,u]
  have hv : v p=ρ := by simp [p,v]
  have h := boost_read s p
  have hratio : u (wedgeBoostMap s p) / v (wedgeBoostMap s p) = Real.exp (2*s) := by
    rw [h.1,h.2.1,hu,hv,mul_div_mul_right _ _ hρ.ne',← Real.exp_sub]
    congr 1
    ring
  change _ ∧ Real.log (u (wedgeBoostMap s p) / v (wedgeBoostMap s p)) / 2 = s
  exact ⟨hratio, by rw [hratio,Real.log_exp]; ring⟩

theorem interval_by_read (x : Point) : minkowskiSq x =
    -(u x * v x) - x 2 ^ 2 - x 3 ^ 2 := by
  unfold minkowskiSq u v
  ring

theorem boost_preserves_interval (s : ℝ) (x : Point) :
    minkowskiSq (wedgeBoostMap s x) = minkowskiSq x := by
  have h := boost_read s x
  have hp : u (wedgeBoostMap s x) * v (wedgeBoostMap s x) = u x * v x := by
    rw [h.1,h.2.1]
    calc
      _ = (Real.exp s * Real.exp (-s)) * (u x * v x) := by ring
      _ = _ := by rw [← Real.exp_add]; simp
  simp only [interval_by_read,hp,h.2.2.1,h.2.2.2]

/-- The prescribed nontrivial boost on every boundary point has an extension to the
bulk with exactly the same boundary action which fails invariance of the interval. -/
theorem same_boundary_motion_different_interval (s : ℝ) (hs : s ≠ 0) :
    (∀ x ∈ frontier rightWedge, wedgeBoostMap s (shear s x) = wedgeBoostMap s x) ∧
    minkowskiSq (wedgeBoostMap s (shear s ![0,1,0,0])) ≠ minkowskiSq ![0,1,0,0] := by
  constructor
  · intro x hx
    rw [shear_fixes_boundary s x hx]
  · rw [boost_preserves_interval]
    exact shear_refutes_interval_preservation s hs

theorem transported_light_witness (L : generatedLorentz) (a : Point) :
    ∃ f : H1, f ≠ 0 ∧ f ∈ physicalCanonicalNet.K rightWedge ∧
      observerUnitary L a f ≠ 0 ∧
      F1Fecho.FieldWeyl.W (observerUnitary L a f) ∈ net (observerChart L a '' rightWedge) := by
  obtain ⟨f,hf,hn⟩ := physical_canonical_net_nonzero
  refine ⟨f,hn,hf,?_,weyl_generator_mem _ _
    ((canonical_one_particle_covariance L a rightWedge f).1 hf)⟩
  intro hz
  apply hn
  apply (observerUnitary L a).injective
  simpa only [map_zero] using hz

end K07.Horizon
