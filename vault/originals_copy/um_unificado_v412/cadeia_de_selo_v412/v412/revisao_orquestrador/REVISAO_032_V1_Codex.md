FAVORÁVEL — V1. OSeparadorNoPercurso demonstra a propriedade de separador anunciada.
[REAL] No termo principal, o mesmo v pertence à lista recebida i :: p e à fronteira no corte j. A hipótese sobre o fim usa o getLast dessa própria lista. Tirar a fronteira impede a travessia do só lido ao só por ler.
Percurso.um contém um vértice. Percurso.passo acrescenta um vértice ligado ao seguinte por uma cláusula. Os construtores excluem a lista vazia e permitem repetição, como convém à afirmação sobre todo percurso.
A indução ou encontra o segundo vértice na fronteira, ou preserva o testemunho da cauda. No caso de um só vértice as hipóteses sobre os extremos são incompatíveis.
toda_cadeia_tem_percurso realiza a alcançabilidade por uma lista com os extremos corretos. a_cadeia_atravessa_a_fronteira fornece uma lista testemunha. A afirmação sobre toda lista está no primeiro teorema.
As ressalvas de minimalidade, unicidade, tamanho e custo delimitam bem o resultado. A expressão “piso da leitura” está identificada como entrada da teoria. O cabeçalho explica a diferença técnica para o lema antigo.
[REAL] As duas cópias conferem por bytes. Recompilei a REV68 por stdin com Lean 4.31.0 sobre os módulos compilados. Saída 0, sem avisos. Cada um dos três termos declara somente propext, Classical.choice e Quot.sound.
Adendo A. A leitura da gerência está correta. Cadeia φ i k vive em Prop. A irrelevância de provas torna intercambiáveis c e c′ com as mesmas pontas, inclusive no índice de NoVertice.
A primeira sonda usa o próprio h sem transporte explícito; a segunda aplica NoVertice.elo de um passo a uma cadeia arbitrária com as mesmas pontas. Logo o termo forte da R1 admite uma testemunha realizável em algum percurso entre as pontas, mas sua pertinência não identifica o percurso escolhido.
Exemplo. Com prefixo (i∨u)∧(i∨v) e sufixo (u∨k)∧(v∨k), a fronteira é {u,v}. Pode-se transportar a marca u de i–u–k ao índice da cadeia de i–v–k. Na lista [i,v,k] o vértice da fronteira é v, e u sequer aparece.
Recompilei separadamente a R1 e a sonda com o Lean 4.31.0. Ambas tiveram saída 0. A validade dos termos da R1 é compatível com a limitação do seu tipo.
Para a v412, recomendo conservar o código R0 do Kimi com os comentários emendados e incluir OSeparadorNoPercurso, com o percurso como lista. A R1 posterior ao corte fica como alternativa examinada.
