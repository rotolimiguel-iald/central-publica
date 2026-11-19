p = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_ADENDO_NOME_COMO_CODIGO.md"
s = open(p, encoding="utf-8", newline="").read()
s = s.replace("= os 130 bytes-linhas originais + `rev_secao.lean`", "= as 130 linhas originais, byte a byte, + `rev_secao.lean`")
s = s.replace("Leitura integral dos 130 arquivos-linha do adendo", "Leitura integral das 130 linhas do adendo")
s = s.replace("(código em\n  `rev_secao.lean`, 3.º bloco; compila no trio)", "(código em\n  `rev_secao.lean`, seção «Item 3»; compila no trio)")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok", s.count("130 bytes-linhas"), s.count("3.º bloco"))
