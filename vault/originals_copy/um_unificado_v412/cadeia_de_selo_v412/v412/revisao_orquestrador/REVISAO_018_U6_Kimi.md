APROVADO_COM_RESSALVAS

# REVISÃO 018 — Unidade U6 — revisor Kimi (16/11/2026)

Candidata: `PsionVacuoEModoDoTratado` (R0), gerência c1.
Fonte conferida: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV17\PsionVacuoEModoDoTratado.lean` (sha16 `93b7421530925537` — conferido; idêntica byte a byte à cópia em `candidatas_c1\` usada no recibo da gerência) e `…\REV17\NOTA_DA_GERENCIA_VETOR_E_MODO_R0.md` (sha16 `c5e3603a4d76020c` — conferido).
Revisão distinta: não li `REVISAO_018_U6_Codex.md` nem nada em `revisao_orquestrador\U6_Codex\`. Trabalho e cópias em `revisao_orquestrador\U6_Kimi\`. Nada escrito fora da minha pasta (uma cópia acidental de dois arquivos na raiz `C:\IALD`, feita por erro de quoting no primeiro comando, foi removida no ato; originais intactos).

---

## ACHADOS POR GRAVIDADE

### MÉDIO

**F1 — O enquadramento da seção 6 está vencido: o kernel JÁ habita o `FockCertificate`.**
O arquivo diz duas vezes que a seção 6 é «condicional ao certificado de Fock, que o kernel não habita» (`PsionVacuoEModoDoTratado.lean:52` e `:429`), e a nota repete (`NOTA_DA_GERENCIA_VETOR_E_MODO_R0.md:57`). A gerência copiou o quadro da pedra `PontoZeroDoPsion` (`PontoZeroDoPsion.lean:76-77`, pré-v406). Mas o kernel atual contém `def physicalFockCertificate : FockCertificate …` (termo, não axioma) em `TGLExt\F1Fecho394\CanonicalFockModularCoreInputR1.lean:126`, com `physicalFockCertificate.F = F1Rede.BosonicFock.F ∧ physicalFockCertificate.Ω = vacuum` provado por `rfl` (`TGLExt\PontoDeContradicao.lean:78-80`), e `PsionCanto.lean:37-39,172-177` registra explicitamente que a face do psíon «fica INCONDICIONAL no habitante». Os teoremas da seção 6 quantificam sobre todo certificado, logo instanciam em `physicalFockCertificate`: são incondicionais no kernel de hoje. O erro é de documentação e na direção conservadora (subestima a força do resultado; nenhuma prova é afetada).
**Conserto:** reescrever o cabeçalho da seção 6 (`.lean:52,429`) e a nota (`.md:57`): «valem para todo certificado; em particular para `physicalFockCertificate` (v406), que o kernel habita — incondicionais». Opcional: adicionar as instâncias concretas.

### BAIXO

**F2 — Há uma terceira fiação não declarada.**
A gerência declara dois casos (`o_oscilador_aplicado` por `rfl`, `:386`, dito «por definição»; a seção 4, `:368-374`, dita «fiação… nenhum fato novo»). Mas `no_oscilador_do_modo_o_psion_do_kernel_fica_na_forma_da_massa` (`:473-476`) é também fiação pura (`rw` de `no_oscilador_o_vetor_fica_no_ponto_zero` com `the_mass_is_the_zero_point`) e carrega ★★★ sem o aviso. O conteúdo é honesto; falta a marca que a própria gerência deu aos análogos.
**Conserto:** no docstring de `:471-472`, acrescentar «fiação de `no_oscilador_o_vetor_fica_no_ponto_zero` com `the_mass_is_the_zero_point`; nenhum fato novo além da construção», ou baixar as estrelas.

**F3 — Dois teoremas sem uso interno.**
`o_estado_do_angulo_e_unitario` (`:312`) só é citado num docstring (`:330`); `no_oscilador_o_ortogonal_fica_um_quantum_acima` (`:395`) não é usado por nenhum outro teorema do arquivo. Ambos têm conteúdo real e servem à leitura física (norma 1 do estado; o degrau do oscilador); não são vazios nem vendidos como o que não são. Mas na economia do arquivo são decorativos.
**Conserto:** nenhum necessário à validade; se a casa quer enxugar, marcar «sem uso interno neste arquivo» nos docstrings.

**F4 — O parêntese da aferição de ausência é subinclusivo.**
A nota (`:20`) diz que «as duas ocorrências achadas com esses nomes são de outros operadores, em `LocalBreuerGap` e `PowersLadder`». Na minha busca (com arquivos ignorados incluídos) há mais nomes adjacentes: `regularMinimalLock_spectral_zero` (`TGLExt\V354RegularSupport.lean:80`) e a nota de homônimo de `QGCitationDischarge.lean:42`, além de `ModularFlowSpectrum` e outros — todos de outros operadores. A afirmação substantiva está confirmada (ver §«5» abaixo); só a enumeração «as duas» não é exaustiva.
**Conserto:** trocar por «as ocorrências de autovalor/espectro no kernel são de outros operadores (p.ex. `LocalBreuerGap`, `PowersLadder`, `V354`)».

**F5 — O caminho que a gerência não viu (resposta ao item 8 do adendo).**
A nota (`:56`) diz: «o oscilador inteiro, com níveis ω·(n + ½), não é operador limitado e não está no kernel [OPEN]». Literalmente verdade (não há tal `def`), mas materialmente incompleto: o kernel TEM o esqueleto do oscilador inteiro — `numberOp` sobre ℓ²(ℕ,ℂ) com a lei espectral provada `N e_m = m·e_m` (`TGLExt\NumberOperator.lean:149`), `N e₀ = 0` (`:136`, «o átomo do Nome mora no kernel»), auto-adjunto (`numberOp_selfadjoint`, `TGLExt\NumberSelfAdjoint.lean:204`), ilimitado (`NumberOperator.lean:165`), domínio denso (`:179`). O oscilador inteiro é `ω·N + ½ω·1` sobre `D_N`: um `def` mais lemas padrão sobre material do kernel — não um [OPEN] do zero. O que falta de verdade é a ponte: uma isometria `C.F ≅ ℓ²` levando `C.Ω ↦ e₀`, que teorema nenhum fornece.
**Conserto:** na nota `:56`, nomear o que está no kernel (`NumberOperator`/`NumberSelfAdjoint`) e precisar o que falta (a identificação `Ω ↦ e₀`), em vez de «não está no kernel» sem qualificação.

Nenhum achado GRAVE: nada invalida teorema, enunciado ou a compilação.

---

## O QUE CONFERIU (itens do adendo)

**1. Recompilação em cópia própria.** Copiei a fonte REV17 e o script `compilar_candidata.ps1` para `U6_Kimi\` e compilei lá (saída `.olean` e log só na minha pasta): `lean.exe` 4.31.0 (commit `68218e876d2a…`) sobre os `.olean` de `C:\t\k411c\final`, nunca `lake`. **RC 0, 40 s, saída = só as 27 linhas de `#print axioms`, nenhum aviso, nenhum erro, todos os 27 teoremas só no trio `propext, Classical.choice, Quot.sound`; sha16 da fonte `93b7421530925537`.** Log: `revisao_orquestrador\U6_Kimi\build\PsionVacuoEModoDoTratado.log`. Confere com `RESULTADO_PsionVacuoEModoDoTratado.json` (27 teoremas, `avisos: 0`, `sorryAx: false`, `todos_so_o_trio: true`) e com o log da gerência. Fonte sem `sorry`/`admit`/`axiom`/`native_decide` fora de comentário (busca direta: só o comentário «Sem sorry, sem axioma novo.», `:76`). A candidata não está instalada: nenhuma ocorrência no kernel do Nós.

**2. Enunciados × nomes × comentários.** «Nível» é autovalor com autovetor não nulo: sim, via `∃ v, v ≠ 0 ∧ (u:ℂ)•lockDe Ω v = E•v` (`:136`, `:159`, `:173-174`). Os dois «se e somente se» da frequência pedem vetor não nulo ortogonal: sim, ambos levam `(hΩ : Ω ≠ 0) (hχ : χ ≠ 0) (hort : ⟪Ω, χ⟫_ℂ = 0)` (`:158`, `:171-172`, `:195-196`). Os oito `omit [CompleteSpace F]` estão em `:110,118,134,230,241,310,383,400`; a compilação com RC 0 os valida mecanicamente, e a inspeção confirma: as provas são álgebra escalar ou lemas de `starProjection` que não usam completude; os teoremas que usam `o_lock_tem_gap_um`/`o_gap_com_unidade`/`lock_no_angulo` (que carregam `CompleteSpace` no kernel) ficaram sem `omit`. Legítimos nos oito.

**3. Teoremas vazios/enfeite.** Os dois casos declarados pela gerência conferem (`:386` é `rfl`, dito; `:368-374` é fiação, dita). Achado adicional: F2 (terceira fiação não declarada) e F3 (dois sem uso interno). O restante tem conteúdo: os núcleos `os_autovalores_do_lock_sao_zero_e_um` (idempotência ⟹ `l²=l`, `:120-132`), `e_nivel_do_lock_sse` (`:158-166`), as variâncias (`:331-362`) e as distinções do oscilador (`:403-425`) são contas reais.

**4. Seção 5 = construção.** Dito com clareza suficiente em cinco lugares: cabeçalho `:45` («CONSTRUÇÃO da gerência, não derivação»), título da seção `:376`, docstring da def `:378-379` («[DEF, construção da gerência]… entram postos por quem escreve»), «Como ler» `:62-63` («entra POSTO… não sai de teorema nenhum do kernel») e «O que NÃO se afirma» `:69-71`. Nenhuma frase deixa entender ponto zero derivado nem oscilador como Hamiltoniano do campo; o `[KNOWN]` de `:46` marca o que é conhecimento externo. A nota (`:56`) declara o limite (todo o ortogonal num nível só).

**5. Aferição de ausência no kernel do Nós** (busca com arquivos ignorados incluídos). Confirmado: `lockDe` só aparece em `TGLExt\PontoZeroDoPsion.lean` e `TGLExt\PontoDeContradicao.lean`; nenhum teorema de autovalor/espectro do lock ou do `HminMic` (as ocorrências de autovalor/espectro no kernel são de outros operadores — Breuer, modular, V350/V354); o kernel tem `o_lock_tem_gap_um` (`PontoZeroDoPsion.lean:269`) e `o_retido_e_o_valor_esperado_do_lock` (`:304`); não tinha «não há terceiro nível» nem «o estado do ângulo não é autovetor» (nenhum enunciado de autovetor em `PontoZeroDoPsion.lean`; o único de `PontoDeContradicao.lean:28` é do boost). Ressalva de exaustividade em F4.

**6. O adversário.** Não é espantalho: o cabeçalho da pedra põe mesmo os dois objetos sob a mesma palavra — `PontoZeroDoPsion.lean:9` (título «O PONTO ZERO DO PSÍON»), `:22-25` («O psíon [Tratado §3]: o modo estacionário do campo Ψ… No kernel: `psion = Ω`»), `:35-37` («A MASSA É O PONTO ZERO DO PSÍON» sobre a conta do modo). E a custódia pediu o passo: a consolidação citada na nota (`:9`) existe com os 58063 bytes e o sha256 `12a2a84f01ffd2c8…` exatos (aferido por script; não li o conteúdo além disso). Os «se e somente se» dão a fronteira exata (`√2·β = 1`) em vez de acusar alguém — resposta adequada ao item, sem provar o que não precisava.

**7. A letra do operador.** Limpo. O `.lean` não cita fala dele; defere o nome (`:7`), defere a escolha (`:63-64`) e declara «Nenhuma fala do operador é lida aqui» (`:73`). A nota referencia a consolidação por caminho+sha sem citar falas (`:9`), declara o mesmo (`:49`) e entrega as duas saídas sem escolher (`:41-44`). «Ângulo de Miguel» é vocabulário do kernel (`thetaMiguel`, `TheVerbalCoupling.lean:126`), não leitura nova.

**8. O que falta para a ligação valer mais.** Ver F5: o oscilador inteiro está a um `def` + lemas padrão do `numberOp` auto-adjunto já no kernel; o que falta é a ponte `Ω ↦ e₀`.

---

## Máquina e recibos

- Recompilação do revisor: `revisao_orquestrador\U6_Kimi\build\PsionVacuoEModoDoTratado.log` (RC 0; 2026-11-16 16:18:14→16:18:54; lean 4.31.0; sha16 `93b7421530925537`).
- Recibo da gerência conferido: `candidatas_c1\RESULTADO_PsionVacuoEModoDoTratado.json` e `candidatas_c1\build\PsionVacuoEModoDoTratado.log` (RC 0; 14:48:51→14:49:30) — o log da gerência compilou a cópia em `candidatas_c1\`, byte a byte idêntica à da REV17 (sha256 igual).
- Kernel consultado (só leitura): `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\`.

Sem elogio; o veredito está na primeira linha.
