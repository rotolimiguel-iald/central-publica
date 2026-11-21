# Conferência da gerência c1: APonteAoTM2 (R0), 19/11/2026

**Fonte conferida:** `work\cadeia_de_selo\v412\candidatas_kimi\APonteAoTM2.lean`, sha16 `82ab2c6c6c05a3c9`; o `.olean` importado pela sonda, sha16 `ac64d0b7c65108f2`.

## O que confere

- Os teoremas dizem o que o relato diz:
  - `a_verificacao_na_fita_e_a_da_casa`: a verificação na fita é `decide (custoCNF φ x = 0)`;
  - `a_fita_tem_as_letras`;
  - `a_verificacao_e_recursiva_primitiva` (`Primrec₂`) e `a_verificacao_e_computavel` (`Computable₂`);
  - os auxiliares.
- O que a pedra diz do Mathlib confere na caixa, em `Mathlib/Computability/TuringMachine/Computable.lean`:
  - a única máquina que habita `TM2ComputableInPolyTime` é `idComputableInPolyTime` (o nome aparece 11 vezes no Mathlib, todas nesse arquivo);
  - `TM2ComputableInPolyTime.comp` é `proof_wanted` (linha 284).

## O defeito: o alvo `[OPEN]` não é aberto

`ObjetivoTM2Polinomial` quantifica as codificações `ea` e `eb` com `∃`. Nesta versão do Mathlib, `TM2ComputableInPolyTime ea eb f` recebe codificações que são funções quaisquer (`α → List αΓ`, linha 179): não se exige que sejam injetivas nem que leiam a entrada. Com `ea` e `eb` constantes (`[]`), a máquina identidade do Mathlib cumpre a estrutura em um passo, sem ler a fórmula.

- **A sonda prova o alvo assim:** `work\cadeia_de_selo\v413\conferencia_c1_kimi\sonda_objetivo_tm2\SondaObjetivoTM2.lean`, teorema `o_alvo_fecha_sem_ler_a_formula`.
- **Compilação:** RC 0, sem aviso, axiomas `[propext, Classical.choice, Quot.sound]`.
- **Ambiente:** o mesmo da pedra (a caixa `C:\t\k411c` e o build da oficina, só leitura).

O comentário «a igualdade pontual com `verificaNaFita` impede truque de renomeação» não vale: a igualdade fixa `f`, não a codificação.

## O conserto, antes de fechar a máquina

1. Definir na pedra:
   - a codificação concreta da entrada: a fórmula e a testemunha num alfabeto finito (dígitos do índice, polaridade, separadores);
   - a da saída: `fun b => [b]`.
2. Enunciar o alvo com as duas fixas, sem `∃`: `Nonempty (Turing.TM2ComputableInPolyTime codificaEntrada codificaSaida (fun p => verificaNaFita p.1 p.2))`.
3. Provar duas coisas da codificação da entrada:
   - que é injetiva;
   - que o seu comprimento é polinomial em `letras φ` e no número de bits. Assim, «polinômio do comprimento da entrada» quer dizer polinômio do tamanho da fórmula.

Se a máquina em construção já lê a codificação natural, o conserto é só de enunciado.

## O que a máquina decide, e o que não decide

Com a codificação fixa, a máquina prova que conferir o certificado é polinomial no modelo padrão: SAT em NP na língua clássica (Cook 1971 `[KNOWN]`), ligado à verificação da casa. Ela não decide a pergunta do Instituto, que é decidir toda CNF plana em tempo polinomial na máquina nua; as paredes de 18/11 seguem de pé, como o relato diz.

## A caixa

As pedras da oficina compilam sobre a caixa da v411 (`C:\t\k411c`, em `compilar_kimi_com_irmas.ps1`). A conferência para a v413 recompila todas sobre a caixa da v412 (`C:\t\k412c`).
