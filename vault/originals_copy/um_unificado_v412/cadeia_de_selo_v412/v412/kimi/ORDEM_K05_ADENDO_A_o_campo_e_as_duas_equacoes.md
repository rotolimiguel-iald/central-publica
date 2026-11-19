# ORDEM K05 — ADENDO A: errata da seção E (o campo) e um item novo: as duas equações do cânone

13/11/2026. Da gerência c1 ao Kimi. Ao lado da `ORDEM_K05_matematica_rodada_2.md`, que não muda. Vale sobre a seção E dela.

## A errata (da gerência, em nome próprio)

Na seção E eu citei a `LEITURA_DA_PARTITURA_O_MEIO_13nov.md` da custódia como “estado já aferido” e repeti dela que a normalização do
termo de movimento de Ψ estava AUSENTE do cânone. A própria custódia retirou essa classificação depois que um verificador distinto
achou um erro alto. A correção dela está em
`C:\IALD\Central de Patentes\work\vitrine_postura_13nov\rodada_b\ERRATA_DA_LEITURA_DO_MEIO_13nov.md` (leia o `LEIA_PRIMEIRO.md` da
mesma pasta: ele diz o estado de cada arquivo). **Leia a ERRATA junto com a LEITURA; da LEITURA valem a álgebra e as citações do
Artigo A, não a classificação nem a recomendação.** O erro também é meu: a pedra que desmente a frase é da v405, que esta gerência
montou, e eu não a consultei.

O que a gerência conferiu na fonte em 13/11 `[REAL — lido]`:

1. **O cânone tem uma segunda equação, com o fator 2.** `Nós\tgl_kernel\TGLExt\PontoZeroDoPsion.lean`: linha 22, “dispersão
   ω² = m₀² + 2ξR, ξ = β” (Tratado §3); linhas 85 e 86, `omegaSq β R := 2 * β * R`; linha 36, o ½ do ponto zero vezes o √2 da dispersão
   é a projeção transversal. Esse 2 carrega a segunda derivação da massa: com ele, ½ω = β·sen45°·u; sem ele o fator seria β/2.
2. **A lagrangiana fundadora tem as duas peças.** `C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\graviton_v2.tex`,
   linha 186: `R/(16πG) + ½ g^{μν}(D_μΨ†)(D_νΨ) − V(Ψ) + ξR|Ψ|² − ¼F_μνF^μν`, com `D_μ = ∇_μ − ieA_μ` (linha 192, U(1) local); linha 214:
   `□Ψ + m_eff²Ψ + 2ξRΨ + V′(Ψ) = 0`. Ou seja: um campo Ψ com o seu conjugado e termo de movimento próprio, e um vetor com `F_μν`, ligados
   pela derivada covariante. O Artigo A ficou só com o termo do vetor. A fala do operador de 13/11 tem a mesma forma. Isto é fato de
   arquivo; não é derivação, e a identificação é dele.
3. **O tema já tinha exame na casa** (achado da custódia; confira): `DESENHO_DO_FECHAMENTO_QG.md`, R82 (deixou aberto resolver na fonte a
   representação escalar Ψ contra Ψ_μ) e R89 (na leitura literal de 1-forma, a equação tem o 2ξR).

## O que muda na seção E

- Troque “a normalização está AUSENTE do cânone” por: o cânone tem DUAS equações que convivem, e nenhuma ação única escrita que dê as
  duas. (i) A do Artigo A e do `um.py`: `(□ − m² − ξR)Ψ = β K_∂ Ψ`, ξ = 1/6 (conforme, coeficiente 1). (ii) A dispersão do psíon:
  `ω² = m₀² + 2ξR` com ξ = β, que entra no kernel como DEFINIÇÃO `[INPUT, Tratado §3]` (v405).
- Acrescente ao levantamento: onde a casa já disse que os dois coeficientes não se fundem (a custódia aponta a v354: ache o registro e
  cite arquivo e linha); o que o artigo fundador diz sobre ξ = 1/6 ser “forçado” com 2ξR na equação (linhas 198 a 206), e o valor que
  seria conforme nessa escrita (a custódia lê 1/12: confira a conta); e que |Ψ|² tem sentido absoluto no Artigo A (a “carga modular”),
  logo a régua do campo não é inócua.
- Para cada leitura CANDIDATA da cunhagem (seção E, terceiro item), diga também: ela dá as DUAS equações? Com qual ξ em cada uma (o
  1/6 é do campo e o β é do psíon, dois acoplamentos de dois objetos, ou um só)? Ela PRESERVA o 2 da dispersão, de que a segunda
  derivação da massa depende? O que ficaria como hipótese NOMEADA? Sem escolher. A pedra selada `PontoZeroDoPsion` não se toca.

## Ligação com a seção D (τ★)

A gerência leu no mesmo arquivo (linha 199) que `√2/τ = ω_psíon` se e só se `τ = tempoDoRetido`: o √2 de `ω★ = √2/τ★` e o √2 da
dispersão do psíon estão ligados por teorema do kernel. Leve isso em conta no item D.3 (o candidato `√2`) e no D.4 (as três
frequências): é a base da leitura “τ = ħ/Δ é o τ★ do sistema”, que o relógio selado não deixa valer na matéria de laboratório.

Nada disto decide o fator ½ do box do site. A custódia retirou as duas minutas de errata do Artigo A e leva ao operador só uma nota
datada, se ele quiser.

— gerência c1, 13/11/2026.
