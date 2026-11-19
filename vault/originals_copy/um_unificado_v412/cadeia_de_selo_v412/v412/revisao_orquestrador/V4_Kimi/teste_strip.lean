-- comentário de linha
def x : String := "-- não é comentário" -- fim
/- bloco /- aninhado -/ ainda bloco -/
/-- docstring com /- interno -/ fim -/
/-! módulo doc -/
theorem t : True := by trivial -- ok
def c : Char := '-'
/- multi
linha -/
def y := 1
