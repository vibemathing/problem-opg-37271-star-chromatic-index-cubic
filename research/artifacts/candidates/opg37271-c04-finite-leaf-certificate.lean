import Std

/-!
C04, candidate_only. Intended toolchain: leanprover/lean4:v4.33.0.
Unexecuted finite certificate draft; this file is not a kernel receipt.
Vertex codes: v=0, u=1, x=2, y=3, a=4, b=5, c=6, d=7.
Colour code 0 denotes an absent edge, never an available edge colour.
-/

set_option maxHeartbeats 5000000
set_option maxRecDepth 100000

namespace OPG37271.C04

abbrev V := Fin 8
abbrev Colouring := V → V → Nat

def hColour (a b : V) : Nat :=
  match min a.val b.val, max a.val b.val with
  | 1, 2 => 1
  | 1, 3 => 2
  | 2, 4 => 3
  | 2, 5 => 4
  | 4, 5 => 1
  | 3, 6 => 5
  | 3, 7 => 6
  | 6, 7 => 2
  | _, _ => 0

def gColour (t : Fin 6) (a b : V) : Nat :=
  if (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 0)
  then t.val + 1
  else hColour a b

abbrev Distinct4 (a b c d : V) : Prop :=
  a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d

abbrev Distinct5 (a b c d e : V) : Prop :=
  Distinct4 a b c d ∧ a ≠ e ∧ b ≠ e ∧ c ≠ e ∧ d ≠ e

abbrev Adj (f : Colouring) (a b : V) : Prop := f a b ≠ 0

abbrev SimplePalette (f : Colouring) : Prop :=
  (∀ a b : V, f a b = f b a) ∧
  (∀ a : V, f a a = 0) ∧
  (∀ a b : V, f a b ≤ 6)

abbrev Subcubic (f : Colouring) : Prop :=
  ∀ o a b c d : V, Distinct4 a b c d →
    ¬ (Adj f o a ∧ Adj f o b ∧ Adj f o c ∧ Adj f o d)

abbrev Proper (f : Colouring) : Prop :=
  ∀ o a b : V, a ≠ b → Adj f o a → Adj f o b →
    f o a ≠ f o b

abbrev BadPath4 (f : Colouring) : Prop :=
  ∃ a b c d e : V, Distinct5 a b c d e ∧
    Adj f a b ∧ Adj f b c ∧ Adj f c d ∧ Adj f d e ∧
    f a b = f c d ∧ f b c = f d e

abbrev BadCycle4 (f : Colouring) : Prop :=
  ∃ a b c d : V, Distinct4 a b c d ∧
    Adj f a b ∧ Adj f b c ∧ Adj f c d ∧ Adj f d a ∧
    f a b = f c d ∧ f b c = f d a

abbrev Star (f : Colouring) : Prop :=
  Proper f ∧ ¬ BadPath4 f ∧ ¬ BadCycle4 f

-- Intended proof terms use kernel reduction through decidability.
-- Successful checking is not asserted by the existence of this source.
theorem h_simple_palette : SimplePalette hColour := by decide

theorem h_star : Star hColour := by decide

theorem h_isolated_leaf_vertex : ∀ a : V, hColour 0 a = 0 := by decide

theorem g_simple_palette : ∀ t : Fin 6, SimplePalette (gColour t) := by decide

theorem g_subcubic : ∀ t : Fin 6, Subcubic (gColour t) := by decide

theorem g_leaf : ∀ (t : Fin 6) (a : V),
    Adj (gColour t) 0 a ↔ a = 1 := by decide

theorem g_same_adjacency : ∀ (s t : Fin 6) (a b : V),
    Adj (gColour s) a b ↔ Adj (gColour t) a b := by decide

theorem g_agrees_after_vertex_deletion : ∀ (t : Fin 6) (a b : V),
    a ≠ 0 → b ≠ 0 → gColour t a b = hColour a b := by decide

theorem no_fixed_extension : ∀ t : Fin 6, ¬ Star (gColour t) := by decide

-- Positive control: recolour xa from 3 to 5, and give uv colour 3.
def repaired (a b : V) : Nat :=
  if (a = 2 ∧ b = 4) ∨ (a = 4 ∧ b = 2)
  then 5
  else gColour (2 : Fin 6) a b

theorem repaired_star : Star repaired := by decide

theorem repaired_same_graph : ∀ a b : V,
    Adj repaired a b ↔ Adj (gColour (2 : Fin 6)) a b := by decide

theorem repaired_palette : SimplePalette repaired := by decide

-- Audit requests below print dependencies only when a trusted runtime runs them.
#print axioms h_simple_palette
#print axioms h_star
#print axioms g_subcubic
#print axioms g_leaf
#print axioms g_same_adjacency
#print axioms g_agrees_after_vertex_deletion
#print axioms no_fixed_extension
#print axioms repaired_star

end OPG37271.C04
