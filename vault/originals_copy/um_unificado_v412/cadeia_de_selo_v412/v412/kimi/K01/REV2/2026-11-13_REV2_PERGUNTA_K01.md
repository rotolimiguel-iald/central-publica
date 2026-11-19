# PERGUNTAS K01 — SOMENTE DECISÕES PENDENTES

[DECLARADO] Estas perguntas não bloqueiam o levantamento dos 20 canais nem os cálculos documentais já entregues. Bloqueiam apenas a transformação do rascunho de m₂ em protocolo executável e qualquer futura abertura. Nenhuma pergunta autoriza abrir dados agora.

## 1. Decisões que só o operador pode tomar

### Q1 — Como fica a regra de morte do m₂ e a segunda testemunha?

**TGL.** [DECLARADO] Deve ser mantida a exigência frozen de **duas determinações independentes ≥5σ** para `TGL_NU_M2_FALSIFIED`? A recomendação é mantê-la. Nesse caso, qual determinação S, com JUNO explicitamente excluído, será fixada antes da próxima abertura JUNO-only?

**Face ontológica [ONTO — analogia estrutural, não derivação].** [DECLARADO] O operador confirma que o objeto de morte é o pacote `β·sen45°·E0` com E0 = 1 eV e m₁≈0, isto é, a escala posta e a identificação, e não β isoladamente nem o Um axiomático? A proposta é que a escala possa cair ao lado, com o gate imóvel.

**Linguagem pura.** [DECLARADO] Quando X ∈ {P,S} alcançar ≥5σ e a outra determinação for ausente ou não alcançar 5σ, qual nome deve valer: `TGL_NU_M2_TENSION__SINGLE_X_AWAITING_INDEPENDENT_CONFIRMATION`, como proposto, ou `OPEN_RULE_GAP`? Isso inclui S independente ou não independente com r_S≥5 e r_P<5. `TENSION_BOTH` só vale com ambos em [3,5); ambos ≥5 com S não independente vão `TENSION_BOTH_NONINDEPENDENT`, nunca `FALSIFIED`. Primeiro se avalia integridade intrínseca, depois independência: covariância intrínseca indispensável a σ_X é `INVALID`; covariância condicional cruzada ausente é `NONINDEPENDENT`, não INVALID.

**Custódia/jurídica do protocolo.** [DECLARADO] Quem será o terceiro custodiante de P e S e quem revisará a independência antes da tranca pública? A equipe/versão de S precisa ser nomeada sem olhar o próximo centro ou erro; quem escreve o protocolo não o aprova.

### Q2 — O objetivo imediato é esperar o m₂ ou aceitar outro desenho?

**TGL.** [DECLARADO] O operador confirma que a meta de 5σ deve **esperar uma futura determinação m₂ com a segunda testemunha armada**, em vez de abrir ringdown D hoje com planejamento D10 = 3,93 e D14 = 4,64? A recomendação é não abrir D para essa meta e preservar sua cegueira até poder/convergência e palavra específica. Com o planning público de 29/09/2026, m₂ dá D = 1,9281 com σ publicado; 0,5 % dá D = 4,0712 e falha; somente a tabela de 0,3 % dá D = 6,7854 e cruza D90 no primário, ainda sem poder conjunto.

**Face ontológica [ONTO — analogia estrutural].** [DECLARADO] A ausência de canal que cumpra cegueira+poder+independência hoje pode ser registrada como parede honesta, e não como derrota da teoria nem como permissão para baixar o limiar? A proposta mantém o gate e a liberdade de negação intactos.

**Linguagem pura.** [DECLARADO] O documento deve permanecer chamado `PRE_REGISTRO_CEGO_RASCUNHO_K01.md`, sem o rótulo de teste agendado, até que P/S, poder e custódia estejam fechados? A proposta é sim; “rascunho” não é promessa de resultado nem autorização de execução.

**Custódia/jurídica do protocolo.** [DECLARADO] O operador deseja ratificar agora apenas o desenho e a futura guarda por hash/timestamp externo anterior à liberação/abertura/comunicação, deixando a autorização de abertura para um ato separado depois do estágio cego? A recomendação é separar esses dois atos e não usar aquisição de bytes como marco de cegueira.

## 2. O que cabe à gerência, sem pergunta ao operador

- [DECLARADO] Conferir o `CANAIS_K01.json`, as fontes, as contas de desenho e o texto contra o core; corrigir ao lado qualquer erro antes de promover o rascunho. As fontes JUNO obrigatórias são `arXiv:2511.14593v1` e `arXiv:2609.37895v1`, já públicas, não futuras.
- [DECLARADO] Fixar a implementação da regra de independência e da covariância condicional entre liberações cumulativas, a lista append-only de tentativas e o manifesto de hashes depois das respostas Q1/Q2.
- [DECLARADO] Submeter a revisão científica a pessoa distinta do redator; quem constrói não aprova.
- [DECLARADO] Depois da revisão, registrar no Mapa e depositar na fila pelos procedimentos da casa. **Nada foi registrado nem depositado por esta K01.**

## 3. Bloqueios objetivos que não são decisões discricionárias

- [DERIVED] Hoje não há segunda determinação m₂ independente com poder e calendário assegurados; um global contendo JUNO não resolve o problema, e o poder conjunto permanece [OPEN].
- [DERIVED] As determinações JUNO de 59,1 e 207,2 dias já são públicas e cumulativas; conteúdo incremental não é independência e exige covariância condicional. O planning atual dá D = 1,9281; 0,5 % falha, e só 0,3 % cruza D90 no primário.
- [DERIVED] Não foi localizada próxima liberação H0DN/escada independente com data, covariância e forecast do mesmo estimador; a precisão corrente não é dado futuro.
- [DERIVED] Ringdown D continua abaixo de 5 no planejamento; N_eff/SO, Σmν, BBN e relógios não alcançam 5σ; vazios carecem de D bilateral e de modelo de matéria.
- [DERIVED] NMC/Shapiro não tem N nem taxa de eventos; Coma e ecos não são cegos; os sistemas analógicos não têm ponte TGL derivada.

[DECLARADO] Enquanto Q1/Q2 estiverem abertas, o estado operacional segue a tabela-verdade: P ausente/incompleto → `AWAITING_SOURCE`; falha intrínseca → `INCONCLUSIVE`; covariância cruzada ausente → `NONINDEPENDENT`; para X∈{P,S}≥5 com a outra <5 ou ausente → `TENSION_SINGLE(X)` ou `OPEN_RULE_GAP`; ambos em [3,5) → `TENSION_BOTH`; ambos ≥5 com S não independente → `TENSION_BOTH_NONINDEPENDENT`, nunca FALSIFIED. Para todos os demais canais desta fase: não abrir.
