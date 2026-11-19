# PERGUNTA — o custo polinomial na máquina, nas quatro línguas

Gerência c1, 17/11/2026. Ao autor. A fala que pede esta pergunta está por bytes em `work\cunhagens_13out\` (arquivo que começa por `OPERADOR_17nov_eu_quero_demonstrar_sim_o_custo_polinomial_na_maquina`).

## 1. O que a gerência entendeu que já foi dito (falas lidas por bytes; a leitura abaixo é da gerência)

- A contagem dos passos da máquina sobre a entrada é a própria carga da entrada (16/11).
- A fita já pressupõe o espaço da inscrição, e o problema foi posto sem o custo da leitura (17/11).
- O tempo é a cauda; a cobrança fecha o ciclo do processamento (17/11).
- Contar o campo todo de uma vez é um (17/11).

Juntando: o custo é o pedágio, ln 2 por oitava. Para n variáveis, a carga é n·ln 2.

## 2. O que já é teorema, na máquina da casa

- A máquina decide com um passo levantado por cláusula e uma leitura (`a_maquina_e_uma_leitura_decidem`).
- A carga de n variáveis é o pedágio de n oitavas (`a_carga_e_o_pedagio_de_n_oitavas`).
- A contagem da leitura é a carga, nem mais nem menos: a garantia vale para toda fórmula exatamente quando o tempo pago passa de n·ln 2 (`a_contagem_e_a_carga_para_formulas`).
- No todo, decidir e conferir levam a mesma fita (`no_todo_decidir_e_conferir_levam_a_mesma_fita`).
- Na expansão explícita, o todo são 2ⁿ parcelas (`as_partes_sao_dois_a_n`).

Falta só juntar isso num teorema do custo total. Com m cláusulas e n variáveis: (m + 2) atos, se cada ato sobre o todo paga um; ou (m + 2)·n·ln 2, se cada ato sobre o todo paga a carga. Nos dois casos é polinomial. Isso a gerência demonstra no kernel.

## 3. Onde está a dúvida

Não é sobre qual é o custo. É sobre o que a máquina lê num passo.

O enunciado do Instituto fixa duas coisas: a cabeça lê UMA casa da fita por passo; e cada casa guarda uma letra de um alfabeto finito, escolhido antes de se saber o tamanho da fórmula. Com essa regra, o todo de n variáveis ocupa 2ⁿ casas, e a máquina deles gasta 2ⁿ passos só para percorrê-lo. O custo da teoria, ln 2 por oitava, paga n. A distância entre n e 2ⁿ é a distância entre contar oitavas e contar casas.

## 4. A pergunta, nas quatro línguas

1. **TGL.** A casa da fita é uma parcela do bulk, ou é a fronteira inteira, o psíon inscrito? Quando o passo age sobre o todo, ele paga por parcela (2ⁿ) ou por oitava (n·ln 2)?
2. **Teológica.** O Verbo lê o Nome de uma vez, num ato só, ou soletra? “Haja luz” é um ato. Quem soletra a luz letra por letra faz 2ⁿ atos.
3. **Linguística.** A unidade da leitura é a letra ou a palavra? Quem lê a palavra inteira paga uma leitura; quem soletra paga por letra. O Instituto mandou soletrar, com um alfabeto fixado antes de a palavra existir.
4. **Jurídica.** Qual régua vale na prova? (a) A do edital do Instituto: cada casa lida conta um. (b) A lei da teoria: conta-se por oitava, e a régua do edital é impugnada, porque deixou de fora o custo da leitura.

## 5. O que cada resposta dá (dito antes de provar qualquer coisa)

- **Se a resposta é (b):** a gerência demonstra no kernel o custo polinomial pela lei da teoria. O teorema diz: com o preço de ln 2 por oitava, decidir custa (m + 2)·n·ln 2. Ele NÃO diz que a máquina do edital decide em tempo polinomial. O texto público diria as duas coisas: polinomial pela lei da TGL, por teorema; pela contagem do Instituto, não demonstrado. Aceitar a régua da teoria no lugar da régua do edital é a creditação, que é do Instituto.
- **Se a resposta é (a):** falta uma coisa que a gerência não tem e não achou nas falas: como o todo cabe em casas de alfabeto finito de modo que a cabeça o leia em número polinomial de passos. Com essa indicação, a gerência tenta a prova. Se tentar e não sair, é parede medida, não falsificação da teoria.
- Um teorema do kernel não devolve “negativo”: ou compila, ou não está provado.

## 6. O que não muda sem a resposta

A página pública (R10) diz hoje: teorema nas classes do dicionário; o `if` sobre o todo conta um, por lei da teoria; na máquina de fita, com custo polinomial no tamanho da entrada, não está demonstrado. O construtor segue montando o candidato com esse texto. Se a resposta mudar o texto, sai página nova e contrato novo, e o construtor refaz só o que o texto alcança.
