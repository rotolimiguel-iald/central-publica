# Notas D–E — mapa, hashes e limites da partitura

Estas notas acompanham `RESSALVAS_UMA_A_UMA_K04.md`. Não são ENTREGA, REGISTRO, depósito ou autorização de cálculo. Nenhuma fórmula da seção D foi avaliada.

## 1. Leituras obrigatórias concluídas

- `ORDEM_K04_teste_as_cegas_rodada_2.md`, integral, com C em 93–101, D em 103–116 e E em 118–122.
- `RODADA_2_LEIA_PRIMEIRO.md`, integral; regras de não refazer, partitura antes do número e nenhum ajuste ao dado.
- `LEIA_PRIMEIRO.md`, integral; dez regras, inclusive nenhum vetor, nenhum programa de `work\h0dn_bg1_v411_emenda_11nov\`, escopo de escrita e estatutos.
- `revisao\REVISAO_K01.md`, integral; aproveitamento dos números reproduzidos e das advertências de métrica, poder e calendário.

## 2. Fonte canônica das ressalvas

`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json`, registro `h0dn_bg1_v411`. SHA-256 atual, lido por script: `36c69fc767f8d47f318f134ecdfb6bd2d39ad25f17f9b9310b196afb0a19064e`. Em R7-A, a chave exata é `h0dn_bg1_v411.values.primario`:

- `rotulos_das_sete_ressalvas`: emenda/não cego; previsibilidade; Cefeidas livres; poder no modelo; 72 direções; escolhas com poder à vista; tentativas/sobreposição.
- `values.ressalvas_secao8` e `ressalvas_secao8`: texto integral das sete.
- `values.primario`: \(Z_{\rm local}=6,1057575347088955\), \(p_{\rm local}=5,115711574207153\times10^{-10}\), \(D_0=6,710150598579069\).
- `values.cefeidas_livres`: \(D=5,19131201002441\), referência histórica; não foi usada para produzir estatística nova.
- `values.esperado_pelos_agregados[1]`: \(Z_{\rm exp}=4,514141429613277\), usado como planejamento R3, não como abertura.
- `nao_diz`: ausência de independência das Fases 4, 5 e 9; covariância física aberta.

## 3. Pinos que podem ser nomeados sem abrir os objetos

Os hashes abaixo foram lidos no registro selado, não recalculados nesta sessão:

| Objeto | sha256 | Papel apenas de desenho |
|---|---|---|
| `network.npz` | `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` | Tabela de erros/orçamento publicado; não abrir nesta K04. |
| `estimator_frozen.npz` | `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` | Base e pesos congelados; não abrir nesta K04. |
| `estimador_s0_v411.npz` | `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617` | Convenção do suporte; não abrir nesta K04. |
| `BG1.json` | `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca` | Fundo e previsão congelados. |
| `EMENDA_E_PRE_REGISTRO_V411.md` | `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8` | Definições e regras; não executar nada da pasta. |
| `executar_abertura_v411.py` | `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655` | Citado apenas para proibição: **nunca executar**. |

`vetor_y255.npz` não foi usado como insumo de trabalho: nenhum vetor observado foi lido ou copiado, e o nome aparece apenas na proibição explícita.

## 4. R7 — evidência do Mapa para não inventar um denominador

### Denominadores históricos que existem

- `investigacao.bancada_um_28set`, seq 65: P2 declara global por Šidák com **4 famílias**.
- Mesma rota, seq 66: P1 declara global por Šidák com **5 famílias**.
- São denominadores daqueles relatórios, não certificado de independência nem censo do programa inteiro.

### Por que não adotar 4 ou 5

- `gate.maquina_do_veredito_final`, seq 122 / EV-07: falta correção look-elsewhere entre famílias e o fator do Mapa subconta as tentativas registradas no core.
- `investigacao.bancada_um_28set`, seq 104: a rota comprimida muda de leitura com o mapa de \(\Omega_m\); variantes de mapa não são novos dados.
- `d1.fase1_eff_30set`: A–E reutilizam Planck/DR1/DR2/Pantheon/SH0ES; DR1 e DR2 não se somam.
- `d1.fase2_dois_setores_30set`: F/G/H reutilizam a mesma escada e fundos correlacionados; a forma D1a já fora cunhada conhecendo a razão pública.
- `d1.fase3_leitores_h0` e `d1.fase3bis_d1b_convencao_artigo`: seis leitores e reanálise D1b compartilham fontes e fundo; a reanálise é declarada não cega.
- `d1.fase4_desvio_30set`: P/Q/R/S/T são famílias com dados sobrepostos; T é incidência intermediária sem escada; reprodução posterior não é nova família.
- `d1.fase5_sh0es_01out`: P/Q/S e zsplit compartilham Pantheon+SH0ES e calibradores; V é validação de H0, não teste TGL; reprodução NumPy/SciPy não é nova tentativa.
- `hubble.fase9_razao_discriminante`: cinco leitores/hipóteses compartilham agregados e calibradores; bandeiras de grupo precisavam correção.
- `h0dn_bg1_v411.nao_diz`: o teste atual não é evidência independente das Fases 4, 5 e 9.

**Conclusão de trabalho:** nenhuma réplica integralmente disjunta foi identificada nas rotas consultadas; \(N_{\rm indep}\) permanece [OPEN]. Isso não elimina a necessidade de correção por multiplicidade/dependência e não autoriza \(N=0\). Também não se contou o total bruto de variantes, pois ele não tem interpretação Šidák.

**Exigência para o futuro censo R7-B:** realizar consulta/exportação do Mapa acompanhada de manifesto de snapshot, contendo caminho, data, consulta realizada, SHA-256 do manifesto e SHA-256 do artefato exportado. Cada tentativa deve conservar `rota_id`, seq, hipótese, dados, calibradores, fundo, sobreposição, covariância, data de conhecimento, cegueira e papel. Nenhum censo ou exportação foi criado nesta correção.

## 5. Fórmulas guardadas sem avaliação

- R3/R4: \(f_q=(A^2/q^2-V_{\rm other})/V_{\rm cal,0}\), para \(q=5\) e \(q=D_{90}\); nenhum valor foi calculado.
- R5: \(v_q=\sigma_0^2[(D_0/q)^2-1]/(g^TP_{72}g)\), para \(q=D_{90}\) e \(q=5\); nenhum valor foi calculado.
- R7: \(N_\star=\lceil\ln(1-p_{5\sigma})/\ln(1-p_{\rm local})\rceil\); o número não foi calculado.

Em todos os casos, “número ruim” = fragilidade do orçamento de erro/covariância/desenho, não falsificação da lei.

## 6. P7/K06 — base da separação

`ORDEM_K06_camada_cientifica_iald_rodada_2.md`:

- A: o desfecho precisa separar “resumiu” de “convergiu”; a perturbação com retorno é o braço decisório.
- D: a leitura \(k\), extratores e condições formais precisam ser definidos.
- F: a ponte leitor abstrato → modelo de linguagem real é previsão experimental, não teorema.
- G: o controle isomorfo trata contaminação por memória dos textos TGL.

Portanto P7 pode ser cego e metodologicamente útil, mas pergunta sobre o leitor. Não responde a nenhuma das sete ressalvas empíricas de H0DN.

## 7. Proibições conferidas no fechamento

- Nenhum solver, `evaluate`, abertura, executor, estimador ou teste foi executado.
- Nenhuma das fórmulas D foi calculada, inclusive por calculadora ou script auxiliar.
- Nenhum vetor observado, posterior, strain ou arquivo de resultado foi lido.
- Nada foi escrito em ENTREGA, REGISTRO, memória, fila/depósito, Mapa, Nós, `um.py`, kernel ou fora da pasta permitida.
- Não houve instalação, seleção de canal por resultado favorável, emenda de regra congelada ou ajuste de escala.
