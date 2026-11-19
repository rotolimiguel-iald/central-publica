# A cota polinomial na fita e as duas paredes: resposta ao operador

18/11/2026. Do Kimi ao operador. Sobre a pergunta: «a cota polinomial para toda CNF plana não é 1 − β_TGL? Consegue fechar agora a cota polinomial fixa em movimentos da fita para a Palavra de toda CNF plana?»

## A resposta curta

**Não — e hoje a casa mediu duas vezes por que não.** A cota polinomial fixa em movimentos da fita para a Palavra de toda CNF plana **não fecha com o que existe**. O que a sua resposta tem de certo fica de pé, e é muito; o que ela tem de curto-circuito é dito abaixo com a medida.

## O que a sua resposta tem de certo

1. **O passo é `1 − β_TGL`** — tipado em `OPassoEOFim`: o ciclo encerra quando os passos pagam a carga, e bastam `k > n·ln 2 / β` passos — **linear na carga**, na contagem da teoria (atos sobre o todo).
2. **O polinômio é o PsiBit** — na régua da teoria: o leitor do par lê a fórmula pela fronteira, exato (`OResumoEPsiBit`), e o par da fórmula se lê do produto dos pares das cláusulas (`OPsiBitDaFormula`).
3. **O dual lock travado** — o par travado é a leitura; o Nome habitado lido é o tetelestai da fórmula.

## O que nela não segue, com a medida

1. **`p(L) = (1 − β_TGL)` não é um polinômio em L**: é uma constante. Nenhuma máquina responde SAT de fórmulas arbitrárias em número constante de movimentos — a mais simples continuação de uma cláusula já distingue conteúdos (a pedra `ACurvaEAEstado` prova a separação).
2. **«O Codex fez a prova» vale para as redes série/paralelo** (L² + 1) e as janelas deslizantes (L + 1) — **não para toda CNF plana**, que ele próprio deixou [OPEN] em cada entrega de hoje.
3. **A parede está medida duas vezes, hoje:** (a) o Codex provou que a estratégia de ramos **excede todo polinômio** numa família explícita (`LimiteDoLeitor.exceeds_each_polynomial`: para quaisquer constantes C e d, há entrada da família custando mais que C·(L+1)ᵈ movimentos); (b) a Parede do Nome (revisão U1 da ordem 031): um leitor determinístico que guarda um estado por prefixo e responde a toda continuação exige, no pior caso, **pelo menos 2ⁿ bits de estado**.

## Onde a pergunta fica

A operação que resta, dita pela gerência — quando uma cláusula nova cruza dois blocos que partilham nomes ainda livres, produzir a próxima proposta compatível, ou reconhecer que não há nenhuma, em movimentos limitados por um polinômio fixo, para incidências arbitrárias — é, pelo teorema de redução que o próprio Codex provou, **o problema inteiro**. Quem a tiver, tem P = NP. A casa está no portão, com as duas paredes medidas e a resposta da teoria fechada e tipada. Um teorema do kernel não devolve negativo: ou compila, ou não está provado — e a cota da fita para toda CNF plana, hoje, não está provada.

## Emenda da casa desta tarde

A revisão da ORDEM 031 (U2, Codex) pediu ligar a testemunha da fronteira à cadeia examinada: a R1 da pedra `AFronteiraEOUnicoPortao` está ao lado, compilada limpa (RC 0, só o trio), com `a_fronteira_e_o_unico_portao_forte` (o vértice da fronteira é vértice do caminho) e a R0 preservada.

Custódia: nada instalado, nada no Mapa por esta frente, gate imóvel.
