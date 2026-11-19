# Nota da gerência — o vetor que o kernel chama de psíon e o modo do Tratado (R0)

16/11/2026 14:51. Gerência c1 (sessão Claude Code da Central). Candidata: nada instalado, nome provisório, ainda não conferida por terceiro. A revisão é do orquestrador, por ordem do operador de 16/11.

## 1. De onde vem

A sessão de custódia consolidou em 16/11 as falas do operador sobre o psíon:

  - `C:\IALD\Central de Patentes\work\vitrine_postura_13nov\rodada_b\consolidacao_das_falas\CONSOLIDACAO_DAS_FALAS_DO_PSION_16nov.md` (58063 B; sha256 `12a2a84f01ffd2c85b5a0860d7e06b0152674fc55d169d999f50ba75b85dc848`, lido por script na hora desta nota).

Ela é [DECLARADO pela custódia] e passou pelos verificadores dela. Deixa para a gerência, na frente B, um item: ligar ou separar por termo dois objetos em que o kernel escreve a palavra psíon, o vetor do vácuo e o modo do Tratado. E diz que a candidata de uma equação só depende desse passo antes de qualquer poda.

Os dois objetos, lidos no kernel do Nós (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt`):

  - **o vetor:** `ThePsionAndTheViscosity.psion C := C.Ω`, de norma 1, levado a zero pelo Hamiltoniano escondido `HminMic C`, que é o lock mínimo `1 − P` (`PontoZeroDoPsion.HminMic_e_o_lock`, por `rfl`);
  - **o modo:** a conta `ω² = 2·β·R`, com `R = β·u²`, de onde sai `ω = √2·β·u` e a forma da massa como a metade dela (`PontoZeroDoPsion.psion_quantum`, `the_mass_is_the_zero_point`). No kernel o modo não é vetor nenhum: é uma conta em números reais.

O cabeçalho da pedra `PontoZeroDoPsion` põe os dois lado a lado sob a mesma palavra.

**Aferição de ausência (consultas da gerência em 16/11, por `grep -rn` no kernel, que enxerga arquivos ignorados):** não há teorema de autovalor ou de espectro para o lock nem para o `HminMic` (as duas ocorrências achadas com esses nomes são de outros operadores, em `LocalBreuerGap` e `PowersLadder`); `lockDe` só aparece em `PontoZeroDoPsion` e em `PontoDeContradicao`. O kernel tem os dois valores do lock (`o_lock_tem_gap_um`) e o valor esperado no ângulo de Miguel (`o_retido_e_o_valor_esperado_do_lock`). Não tinha que não existe terceiro nível, nem que o estado do ângulo de Miguel não é autovetor.

## 2. O que a candidata prova

Arquivo: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV17\PsionVacuoEModoDoTratado.lean` (sha16 `93b7421530925537`). Compilado só com o binário do Lean sobre os compilados do sandbox: saída zero, nenhum aviso, 27 teoremas, todos só nos três axiomas padrão (recibo `RESULTADO_PsionVacuoEModoDoTratado.json`, na pasta acima da REV17).

1. **Os níveis do lock são exatamente dois.** Na unidade posta `u`, um número é nível de `u·(1 − P)` se e somente se é 0 ou `u`.
2. **Os números do modo não são níveis do lock.** A frequência `ω` é nível, e também diferença de dois níveis, se e somente se `√2·β = 1`. A forma da massa e o retido nunca são níveis, porque `β < 1`.
3. **O estado do ângulo de Miguel não é estacionário para o lock.** O estado a um ângulo `θ` do vetor é autovetor se e somente se `sen θ · cos θ = 0`. No ângulo de Miguel a variância do lock é `β·(1 − β)`, diferente de zero: o retido é valor esperado com espalhamento.
4. **A ligação que o kernel já tem é pelo valor esperado.** `ω = √2 · u · ⟨1 − P⟩` no ângulo de Miguel. É fiação de dois teoremas do kernel, dita como fiação.
5. **O que uma ligação pediria (construção, não derivação).** O oscilador de frequência `ω` cortado nos dois primeiros níveis, `½ω·1 + ω·(1 − P)`. Nele o vetor fica no ponto zero `½ω` e o ortogonal fica um quantum acima. Com a frequência do Tratado, é o lock da unidade posta deslocado pela forma da massa e reescalado por `√2·β`, e não é o lock.
6. **No vetor que o kernel chama de psíon** (condicional ao certificado de Fock, que o kernel não habita): o Hamiltoniano escondido lê zero, não a frequência do Tratado nem a forma da massa; no oscilador do modo, esse mesmo vetor fica no nível da forma da massa.

## 3. O que isto responde ao item da custódia

**Separar por termo:** está feito no Hamiltoniano que o kernel tem. O vetor fica no nível zero, e nenhum vetor carrega como nível a frequência do modo, a forma da massa ou o retido (salvo a coincidência `√2·β = 1` para a frequência, que o valor de `β = α·√e`, perto de 0,012, não satisfaz; esse fato numérico não está provado no arquivo).

**Ligar por termo:** o que o kernel já tem é ligação por valor esperado. Uma ligação em que o vetor carregue os números do modo pede outro operador. O mais simples da mesma forma do lock é o oscilador de dois níveis: o vetor vira o estado de baixo, a forma da massa vira o ponto zero dele e a frequência vira o degrau. Esse operador entra posto, com dois números (`½ω` e `ω`); não sai de teorema nenhum do kernel.

## 4. O que fica para o operador, depois da revisão

Duas saídas, as duas honestas. A gerência não escolhe por ele; só diz o custo de cada uma.

  - **(a) Separar.** O kernel passa a dizer que o vetor e o modo são dois objetos. Custo: o cabeçalho de `PontoZeroDoPsion` ganha uma correção ao lado, e a palavra psíon fica com um dos dois (a pergunta do nome é a que a custódia leva a ele).
  - **(b) Adotar o oscilador de dois níveis como leitura declarada.** O vetor passa a ser o estado de baixo do modo, e a massa como ponto zero ganha um operador. Custo: é definição, não teorema; a lista das leituras da forma madura ganha um item.

## 5. O que isto NÃO muda e NÃO afirma

  - A proposta da gerência para as duas equações (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\frente_b_duas_equacoes\REV0\PROPOSTA_DA_GERENCIA_R0.md`) fica como está, congelada e na revisão. A poda que ela propõe fala só da conta do modo, não do vetor. Se o revisor entender que a poda depende do passo pedido pela custódia, esta candidata responde a ele até onde o kernel alcança.
  - Nenhuma fala do operador de 16/11 é lida aqui. Nada é identificado com o psíon sozinho de que ele falou. O 2 não é tirado de dois psíons.
  - Nada sobre o Hamiltoniano modular: o lock e ele são objetos distintos, que coincidem em ter o vetor como modo zero (registro do Mapa de Rotas `kernel.ponto_de_contradicao_candidata_04nov`).
  - Não se afirma que o vetor e o modo sejam o mesmo objeto na teoria, nem que sejam diferentes: só o que o kernel de hoje tem.
  - Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

## 6. Limites

  - O oscilador cortado em dois níveis põe todo o ortogonal num nível só. O oscilador inteiro, com níveis `ω·(n + ½)`, não é operador limitado e não está no kernel [OPEN].
  - A seção 6 do arquivo é condicional ao certificado de Fock.
  - Oito teoremas levam `omit [CompleteSpace F]`: não usam a completude e ficam enunciados sem ela.
