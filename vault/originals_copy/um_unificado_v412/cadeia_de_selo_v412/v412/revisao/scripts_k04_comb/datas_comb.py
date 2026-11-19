from datetime import date, timedelta
cut = date(2026,5,18)
start = date(2025,8,26)
cal = (cut-start).days
frac = 207.2/cal
print("janela civil 26/08/2025 -> 18/05/2026 =", cal, "dias; fracao viva implicita", frac)
for nome, T in (("Stouffer JUNO+SO (incremento 1806,4 d)", 1806.408), ("JUNO sozinho D90 incremento (2199,24 d)", 2199.24), ("5sigma incremento (1393,41 d)", 1393.41)):
    print(nome)
    print("   100% vivo:", cut + timedelta(days=T))
    print("   frac implicita %.3f:" % frac, cut + timedelta(days=T/frac))
    print("   frac 0,85:", cut + timedelta(days=T/0.85))
