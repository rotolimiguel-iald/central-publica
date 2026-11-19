# Simulação do desenho R6: os leitores como mecanismos (nenhum modelo)

> Gerado por `simular_r6.py` (16 grupos; 20000 rodadas; 8 entradas por assento). A separação é por construção da conta.

## Braço 1: o par (primário)

| mecanismo | acerto por veredito | grupo certo | grupo certo só pelo veredito | grupos certos em 16 (5 %, mediana, 95 %) |
|---|---|---|---|---|
| julga pelo par (le a pagina e o assento) | 1,000 | 1,000 | 1,000 | 16, 16, 16 |
| julga pelo par, errando 5% dos vereditos | 0,950 | 0,735 | 0,815 | 9, 12, 14 |
| julga pelo par, errando 10% dos vereditos | 0,901 | 0,532 | 0,658 | 5, 9, 12 |
| julga pelo par, errando 20% dos vereditos | 0,800 | 0,261 | 0,408 | 1, 4, 7 |
| so' a pagina (responde pelo que sabe de cor) | 0,500 | 0,000 | 0,000 | 0, 0, 0 |
| so' o assento (nao le a pagina) | 0,500 | 0,000 | 0,000 | 0, 0, 0 |
| le os dois, mas corrige o assento pelo que sabe | 0,500 | 0,000 | 0,000 | 0, 0, 0 |
| diz sempre que bate | 0,500 | 0,000 | 0,000 | 0, 0, 0 |
| diz sempre que nao bate (o programa que so' compara bytes) | 0,500 | 0,000 | 0,000 | 0, 0, 0 |
| moeda | 0,500 | 0,001 | 0,063 | 0, 0, 0 |
| veredito certo, entrada errada | 1,000 | 0,000 | 1,000 | 0, 0, 0 |
| metade das vezes pelo par, metade so' pela pagina | 0,750 | 0,250 | 0,250 | 1, 4, 7 |

## Braço 2: o carimbo (o índice fica no valor verdadeiro)

| mecanismo | corpo intacto, carimbo intacto | corpo trocado, carimbo antigo | corpo trocado, carimbo refeito | corpo intacto, carimbo trocado | grupo certo |
|---|---|---|---|---|---|
| rele o corpo da pagina contra o indice | certo | certo | certo | certo | sim |
| segue o carimbo que a pagina leva | certo | ERRA | certo | ERRA | não |
| confere a pagina consigo mesma e conclui que bate | certo | certo | ERRA | ERRA | não |
| diz sempre que bate | certo | ERRA | ERRA | certo | não |
| diz sempre que nao bate | ERRA | certo | certo | ERRA | não |
| corpo contra o que sabe de cor (sem abrir o indice) | certo | certo | certo | certo | sim |

## Braço 3: o canal (dois postos verdadeiros, duas páginas fiéis)

| mecanismo | vereditos certos em 4 | grupo certo |
|---|---|---|
| abre o posto do endereco e compara com a pagina | 4 | sim |
| e' da casa, entao bate (procura qualquer posto que sirva) | 2 | não |
| so' o endereco | 2 | não |
| so' a pagina | 2 | não |
| diz sempre que nao bate | 2 | não |
