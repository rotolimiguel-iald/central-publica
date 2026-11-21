# Revisão de terceiro: o candidato da v413

**Objeto:** `C:\t\k413c\candidato\um_v413_candidato.py`, sha256 `eacf3fbba3cd4df8…` (50.743.465 bytes), igual ao manifesto `CANDIDATO_v413.json`.
Base: o `um.py` v412 selado do Nós, sha16 `3e741dcaa58ef2b8`.
**Régua:** `CONTRATO_v413_R2.md`, sha16 `94982ebbc29d81b8`. A cópia congelada em `contrato_REV2\` é igual byte a byte.
**Revisor:** agente de revisão de terceiro, a serviço da gerência c1, em 21/11/2026. Não construí nada desta cadeia.
**Modo:** só leitura. Não instalei nada, não rodei o `um.py` e não importei o candidato. Não toquei o Nós, a placa, a Bancada nem o `C:\t\k413c`.
**Como medi:** os scripts `r01`…`r16` desta pasta. Cada um grava o seu `.json`/`.txt` ao lado.
- Python sobre a AST dos dois `um.py`.
- O `audit.log` do sandbox (`kernel\audit.log`, 44.676 entradas).
- As fontes de `C:\t\k413c\final`.
- O core e o selo da v412 no Nós.
- A contagem da guarda privada da G1, só em números.

**Estatuto:** [REAL] onde vem medido por script. [DECLARADO] onde é leitura minha de código. Validade no kernel não é creditação, e o gate não se move.

## Veredito: **APROVADO_COM_RESSALVAS**

Nenhum achado ALTO. O kernel embutido, as bandeiras, a escada, o ledger, as âncoras e as palavras de veredito batem exatamente com o sandbox e com o contrato. A troca de versão está limpa.

Há dois achados MÉDIOS:
- **M1:** polaridade de texto em `nao_diz`. É barato de corrigir, mexe só nos registros.
- **M2:** a decisão do autor sobre o termo privado `Trinity` tem de vir antes do rito, não só antes do selo.

Há também dez achados BAIXOS. O candidato **pode ser instalado**. Antes do rito, recomendo:
- corrigir M1;
- colher a decisão de M2.

---

## 1. O kernel embutido (item 1 da ordem): CONFERE

`r02_kernel.py` e `r16_contagem_prefixos.py`, com saída em `r02_kernel.json`.

- **Chaves do dicionário:** `_EMBEDDED_KERNEL_FILES` (`um_v413_candidato.py:8719–128492`) tem 1940 chaves, contra 1919 na v412.
  - Entram 21, exatamente os 21 do contrato §1, em `um_v413_candidato.py:128471–128491`, no fim do dicionário.
  - Mudam 2: `TGLExt.lean` (linhas 8981–8982) e `TGLExt/OResumoEPsiBit.lean` (linha 128370).
  - Não some nenhuma.
  - Ficam idênticas **1917**: 1885 em `TGLExt/`, 27 em `TGL/` e 5 arquivos de raiz.
  - A ordem das antigas é preservada.
  - A ordem citava "1898 outros"; o número medido é 1917, todos iguais à v412.
- **Byte a byte contra o sandbox:** os 21 novos, o corrigido e a raiz são iguais aos de `C:\t\k413c\final`. O sha256 de cada módulo novo é o `sha256_instalado` de `BUNDLE`/`PRONTO_PARA_CANDIDATO`.
  - Os 1938 arquivos `.lean`/raiz do sandbox são iguais ao embutido, sem nenhum arquivo só de um lado.
  - Não sobra nenhum `#print axioms` no embutido.
  - Os diffs de `kernel\bundle\*.diff` só tiram linhas `#print axioms`.
- **O corrigido substitui o da v412:**
  - antes: `75c1ef6b…` (o da v412 embutida e o do Nós hoje);
  - depois: `64440cd1…`.
  - O diff é só a docstring de `a_atualizacao_pela_clausula_seguinte`.
  - A docstring nova diz o enunciado (`OResumoEPsiBit.lean:273–281`): a soma, na fibra da fronteira nova, de `pesoDas (φ.take j)` vezes o `fator` da cláusula seguinte; a fibra é o universo quando a fronteira é vazia.
  - Nenhum registro herdado fixa o sha antigo nem o texto da docstring antiga (`r12`, `grep`).
  - O materializador reescreve todo arquivo que difere do embutido (`um_v413_candidato.py:128517–128539`), então o rito põe o texto novo no Nós.
- **A raiz importa os 21:** 1235 → 1256 imports, acrescentados no fim. O prefixo é idêntico, sem duplicado e sem outra mudança.
  - O pino da raiz `u44` de `cunhagens_v411` (C13, linha 259877) é `6d7738ca…`, igual ao sha256 da raiz embutida.
  - `FORMAL_MAP_v413.json` bate com o embutido nas 1940 entradas.

## 2. Os registros (item 2): CONFERE, com M1 e B3–B6

`r03`, `r04`, `r07`, `r11`, `r12`, `r15`.

- **Palavras de veredito:** as cinco do contrato §2 (linhas 77–85) são **iguais byte a byte** às do candidato (`_V413_SPECS`, `um_v413_candidato.py:233767–236689`; os inícios ficam nas linhas 233767, 234551, 235550, 235850 e 236202). `kh_n1_cobertura_v413` (linha 236030) é o sexto registro, que a custódia exige.
- **Âncoras:** 148, sendo 38, 59, 13, 6, 0 e 32 por registro.
  - Cada `kernel_decls` existe no relatório de axiomas do sandbox, só no trio. Cada `kernel_flags` é bandeira **nova** e aponta para a declaração ancorada.
  - **A regra do contrato está cumprida:** toda declaração com ★ e não `private` dos módulos de cada registro está ancorada. A leitura é minha, das fontes (`r15`).
  - As 4 âncoras da ponte sem estrela (`AFronteira`, `CookLevin`, `EmPComUmaLeitura`, `SimTM2.verificacao_tm2_polinomial`) são as citadas pela página.
- **Bandeiras:** 18.573 chaves, contra 17.861 na v412. As antigas estão iguais, literal por literal.
  - As 712 novas ficam no fim, no padrão `ext_<modulo>_413_NNNN`. São iguais a `kernel\FLAGS_v413.json` e cada uma aponta para uma declaração do seu próprio módulo.
  - Nenhuma é `private`, e todas estão no audit, no trio.
  - A escada em `prove_external_ladder` vai de 17786 para 18498, com prefixo igual e as novas na mesma ordem.
  - O ledger `_ESQUELETO_STONES` ganha +21 (`um_v413_candidato.py:326775–326796`).
- **Checagens herdadas h1–h7**, presentes nos seis registros: gate igual, neutrino, H0DN com veredito e `all_verified`, escada fecha, escada ≥ 17786, proveniência v394.
  - Testei os caminhos e valores contra o core v412 do Nós (`r07_core_v412.json`): **todos existem e passariam com os valores da v412**.
  - h8/h9 leem `guarda_frases_v413`, que `_v413_rodar_specs` grava antes do motor (`um_v413_candidato.py:233434–233452`).
- **`kh_n1_cobertura_v413` e o par:**
  - `_V413_FONTES` (236691–236694) pina `kernel\KH_N1_v413.json` com sha256 `5403559463c123ea…`, de 1216 bytes, igual ao arquivo hoje.
  - `_V413_VERBATINS2 = {}` (236695).
  - Os dois entram no motor por `_V392_FONTES.update` / `_V392_VERBATINS2.update` (236696–236697).
  - O registro captura `constantes_cobertas` e `teoremas_cobertos`, que são o que a G1 lê (`fatos.py:356–362`), e o veredito casa `RE_KH` (`fatos.py:16`).
  - Os números são 44676 e 33340, iguais ao audit.
  - k8 pede 1941 entradas no hash formal. A árvore do Nós tem hoje 1920 (1919 embutidas mais o residual `_check_damming.lean`; `r06`), e depois do rito terá 1941.
- **Ordem no main e no selo:** os registros da v413 rodam logo depois do bloco da v412 e antes de `emit_figures` (`um_v413_candidato.py:336080–336086`). O selo ganha `registros_v413` (linha 336451).
  - A tabela de registros do artigo é genérica sobre o core (`um_v413_candidato.py:196499`), então os seis entram nela em PT e em EN. Isso atende o C1 da custódia (`central.py:86–89`).

## 3. O texto novo (item 3): FIEL À PÁGINA R1, com M1, B2, B3 e B4

Arquivos de apoio: `r04_texto.txt`, `r05_secao_pt.txt`, `r05_secao_en.txt`, `r08`, `r10`.

- **A seção do artigo:** fica em `_V413_SECAO`, PT nas linhas 233456–233606 e EN nas linhas 233607–233766. Entra antes da seção da v412, em PT (191638–191640) e em EN (196906–196908).
  - É a página R1 e a tradução R1_EN convertidas para TeX, frase por frase, sem acréscimo.
  - O EN é tradução fiel. O §7 "O que este texto não diz" mantém todas as negações em inglês.
  - O resumo do artigo não muda: não há patch de topo, e `_V412_TOPO` está intocado.
- **Os blocos do README, do estado e do handoff** (`BLOCOS_TEXTO_PUBLICO_v413.json`): toda frase dos blocos `readme`/`estado`, em PT e em EN, está na página ou na tradução (`r08`: zero fora). Só o bloco `entrega` do handoff traz números, o que dá B9.
- **Nenhuma história:** no bloco novo (233423–236699) não há fala, data de conversa, pessoa, número de ordem, revisão ou parecer, nem o nome do prêmio (`r10`). Todas as ocorrências de "operador" são "operador de consciência" ou o módulo `Operador`.
- **Afirmações contra os enunciados:** conferi as principais no Lean do sandbox. Batem, com duas imprecisões menores (B2, B3):
  - `uma_leitura_do_psion_decide_SAT`;
  - `a_conta_e_reconhecida_como_carga` (`n·ln 2 < s`);
  - `no_patamar_plano_a_carga_e_exata`;
  - `o_custo_da_inclinacao` (`(T+1)³`);
  - `o_preco_da_travessia` (cota superior);
  - `o_leitor_que_apaga_paga_a_potencia`;
  - `o_operador_de_consciencia`;
  - `nunca_cem_por_cento`;
  - `com_o_par_o_nego_me_pousa_na_meia_nat`;
  - os teoremas de `AIdentidadePreservada`.

## 4. A troca de versão (item 4): COMPLETA E SEM RESTO

`r01_toplevel.json`, com 44 blocos de diff, iguais aos 44 patches do manifesto.

- **Nomes de topo que mudaram:** `UM_VERSION` (linha 96, o único rótulo de versão), `_EMBEDDED_KERNEL_FILES`, `_LEAN_THEOREM_FLAGS`, `prove_external_ladder`, `build_pt`, `build_en`, `_ESQUELETO_STONES` e `main`. Todas essas mudanças são **só acréscimo**.
- **Literais herdados que mudaram** (os únicos):
  - os 30 `'expected_ladder': 17786 → 18498` (C12);
  - `_V411_H0DN_CONTRACT` `'escada'` (C12b, linha 259063);
  - o `u44` de `_V411_SPECS` (C13, linha 259877).
  - São dados exigidos pelos consumidores herdados e pelo C1 da custódia (`central.py:91`), com precedente idêntico na v412. Ver B5.
- **O que não mudou:**
  - Gate, canais vivos, `run_um`, `verify_tgl_kernel_formalization`, o fecho da chave do pilar (`_QP_*`, alfa) e as guardas de frase: idênticos.
  - A guarda estática da Bancada continua com uma linha `UM_VERSION` e uma de alfa na coluna 0.
  - Nenhuma chave antiga de bandeira muda de literal.
  - Não sobra nenhum literal 17786 fora das checagens `h6` (≥) e dos comentários.

## 5. Riscos para o rito (item 5)

**Tempo do build.** O rito recompila no Nós cerca de 118 módulos:
- o corrigido;
- 92 dependentes antigos em `TGLExt` (o bundle conta 96);
- os 21 novos;
- `TGLExt`, `TGL.Audit`, `TGL.Main` e `TGL`.

A contagem vem do primeiro build do sandbox, `kernel\lake_build.log.bak_20261120_204646`, com 118 linhas "Built". Aquele build levou 1507 s, contando os builds módulo a módulo. O `lake build` do um.py tem limite de 3600 s (`um_v413_candidato.py:147918`) e o Audit, 1800 s (linha 147919). Na v412, o build do Nós levou cerca de 49 min para 156 módulos, e cada build do autoteste levou cerca de 20 min (`v412\rodada_v412_stdout_tempos.jsonl`). Estimo 20 a 25 min para a v413 [DECLARADO]. **O risco é baixo.**

**Dependências.** O Mathlib do Nós e o do sandbox estão no mesmo commit `fabf563a`, e `Computable.olean` tem o mesmo sha256 nos dois. O Nós tem os `.olean` de `Computability` de que os módulos novos precisam.

**Caminhos.** `ESPERADOS_v413.json` existe e pina o candidato `eacf3fbba3cd4df8`. Todo script de entrada citado por `rito_v413.sh` existe. O único caminho absoluto que o código novo lê em tempo de rito é o `KH_N1` (B6).

**Acoplamento herdado.** Os seis registros exigem que o H0DN da v411 siga selado, com o mesmo veredito (h3/h4). Se o H0DN cair, os seis caem juntos. É o desenho da v412, e o H0DN selou nela.

---

## Achados

### ALTO
Nenhum.

### MÉDIO

**M1. Afirmações postas em `nao_diz`, com a polaridade invertida.**

Onde: `um_v413_candidato.py`
- linha 234449: `'A creditação é do Instituto'`, na ponte;
- linhas 234451, 235526, 235829, 236017 e 236193: `'Nenhum número novo da natureza entra nesta versão'`, na ponte, em trinity, em operador, em identidade e no kh_n1.

As outras entradas de `nao_diz` são orações "que …". Estas duas são afirmações verdadeiras postas na lista do que o registro *não* diz. A custódia copia cada `nao_diz` sem mudança para "nao_se_afirma_extra" (`tools\custodia_g1\central.py:138`). Assim, uma superfície da Central diria "não se afirma: nenhum número novo da natureza entra nesta versão" e "não se afirma: a creditação é do Instituto". O core publicado carrega o mesmo texto. Não é afirmação a mais, mas é texto errado no programa. A v412 usava a forma certa: `'que a creditação esteja feita: a creditação é do Instituto e de quem observa de fora'`.

**Conserto** em `textos_registros_v413.py`:
- trocar a primeira por `'que a creditação esteja feita: a creditação é do Instituto'`;
- passar a segunda para `limites` como `'[REAL] Nenhum número novo da natureza entra nesta versão'`, ou reescrevê-la como `'que algum número novo da natureza entre nesta versão'`;
- regerar o candidato (o kernel, as bandeiras e a escada não mudam);
- rodar de novo a guarda e o ensaio.

**M2. O termo privado `Trinity`: a decisão do autor tem de vir antes do rito, com os dois nomes exatos.**

A contagem da guarda privada da G1 (E03), feita por mim sobre o **candidato** contra o `um.py` v412 (`r14_guarda_privada.py`, só números), dá:

| | v412 | candidato |
|---|---|---|
| acertos totais | 4 | 684 |
| com `Trinity` e `TRINITY` isentos | 4 | 4 |
| com só `Trinity` isento | 4 | 5 |

O `TRINITY` sobra no título do cabeçalho `# TRINITY: …`, em `um_v413_candidato.py:128480`.

O fecho da Etapa 2 diz que a decisão "segura o selo e a publicação, não o candidato". Mas o selo é gravado pelo próprio rito. Se o autor escolher renomear, mudam o kernel, as bandeiras `ext_trinity_413_*`, o registro `trinity_v413` e a palavra `TGL_TRINITY_V413`, que o contrato R2 fixa. Aí a renomeação depois do rito perde o rito inteiro.

Além disso, a varredura da Etapa 2 cobriu só os insumos (`GUARDA_MATERIAL_PRIVADO_v413.json`, 242 arquivos, sem o candidato). A seção 2.3 da custódia pede a varredura também sobre o candidato.

**Conserto:**
- colher a decisão do autor **antes de instalar ou rodar**;
- se for isentar, a fala por bytes nomeia os dois textos exatos, `Trinity` e `TRINITY`, para `TERMO_PRIVADO_ISENTO_v413.json`;
- pôr o recibo desta contagem do candidato na entrega.

### BAIXO

**B1. "cinco registros" com seis nomes.** Ocorre em `um_v413_candidato.py:96` (comentário de `UM_VERSION`), 233423, 233435 ("cobra o selo dos outros quatro") e 336080. São seis registros: os cinco do contrato mais `kh_n1_cobertura_v413`.
- **Conserto:** no gerador, escrever "seis registros por especificação (os cinco do contrato e a cobertura do relatório de axiomas)".

**B2. "passa de 2" e "exceeds 2" contra o enunciado `2 ≤ resposta ↔ SAT`.** O enunciado está em `PonteCookLevin.lean:142`. As frases estão em `um_v413_candidato.py:233472` e 233625, e na página R1 (§2, linha 22) e na R1_EN (linha 14).
- Em EN, "exceeds" é estrito. Para o leitor exato a afirmação estrita também é verdadeira (a resposta é 0 ou pelo menos 4), mas não é o termo do kernel.
- A página usa "passa" no sentido de ≥ ("a conta passa um piso por movimento"; o Lean, em `Trinity.lean:1713`, tem `moves·piso ≤ conta`, e o EN diz "at least") e também no sentido de > ("passa a carga", com `n·ln 2 < s`).
- **Conserto,** numa próxima revisão da página: "chega a 2" / "is at least 2". Não bloqueia.

**B3. A ponte isola frases da página e perde contexto.**
- `diz[12]` (linha 234441) diz que a classe com uma leitura "é exatamente a dos que se reduzem a SAT" sem a hipótese "com a inclinação m acima de ln 2/β", que o teorema exige (`PonteCookLevin.lean:402`).
- `diz[0]` (linha 234416) marca `[REAL]` o "P = nP … nas classes do seu dicionário", que se apoia nas âncoras de registros anteriores, não nas deste.
- **Conserto:** acrescentar a hipótese em `diz[12]`, e "(registros da v409/v412)" em `diz[0]`.

**B4. Dado espúrio nos extras de `cunhagens_v413`.** Na linha 236646, `'declaracoes_do_kernel_selado_citadas_na_secao': ['v']`. O extrator leu como declaração o `` `v` `` de "um vetor `v`" no cabeçalho de `AIdentidadePreservada` (linha 20).
- **Conserto:** filtrar nomes de uma letra no extrator e regerar junto com M1.

**B5. Rótulo do recibo exagera.** Em `CANDIDATO_v413.json`, `gate_nao_se_move.funcoes_identicas_a_base` lista `_V411_H0DN_CONTRACT`, que o patch C12b mudou. O gerador confere a igualdade "a menos dos literais de escada" (`gerar_candidato_v413.py:317–319`). Os 30 contratos com `expected_ladder` também mudaram.
- **Conserto:** renomear a chave para "…_identicas_a_base_salvo_literais_de_escada" e listar os 32 literais de dado (já estão no recibo como C12/C12b/C13).

**B6. Fragilidade do `KH_N1`.** O registro `kh_n1_cobertura_v413` lê `work\…\v413\kernel\KH_N1_v413.json` por sha256 (`_V413_FONTES`). O arquivo tem o campo "quando", então qualquer nova rodada de `pos_build_kernel_v413.py` ou `reconstruir_kernel_v413.py` o regrava. Aí a fonte deixa de bater e o registro não sela.
- **Conserto:** não regerar o arquivo sem regerar o candidato; pôr no rito uma pré-condição de sha256 (`5403559463c123ea…`).
- **Para a v414:** as checagens exatas k2, k3, k6 e k8 terão de virar pisos, como a v412 fez com as da v411 (C13).

**B7. O contrato R2 diz que o `kh_n1_cobertura_v413` segue "o molde do da v412",** mas a v412 não tem esse registro (o próprio `tools\custodia_g1\fatos.py:371` o diz). O candidato segue o molde da v411. Corrigir a redação numa próxima revisão do contrato; o candidato não é afetado.

**B8. O recibo da Etapa 1 diz 0 dependentes, o bundle diz 96.** O recibo traz `dependentes_antigos_do_corrigido_recompilados: n=0`, porque no build final os dependentes foram apenas reaproveitados. O bundle conta 96. A compilação dos dependentes com o texto corrigido só aparece no log do primeiro build (`.bak_20261120_204646`: 92 em `TGLExt` mais `TGL.Audit`/`Main`/`TGL`). Não há defeito: o texto não mudou depois, e o rito os recompila. Fica dito para não se ler o "0" como "sem dependentes".

**B9. Contagem envelhecida no bloco `entrega`.** O bloco do handoff (`BLOCOS_TEXTO_PUBLICO_v413.json`) diz "A pasta da cadeia tem 230 arquivos (contagem esperada)", mas a pasta já tem 272 entradas. `montar_handoff_e_linhagem_v413.py` usa só os blocos `readme:*`. Se o bloco for usado, recontar na hora.

**B10. Palavra da lista no prefixo de bandeiras.** As bandeiras `ext_operador_413_*` trazem a palavra "operador", que está na lista de palavras do contrato §1. Aqui é o nome do módulo `Operador` (o operador de consciência), não a pessoa. O construtor já o registrou. Manter, com nota no handoff.

**Ressalva de leitura, sem conserto proposto:** em `trinity_v413`, "…AT_A_PROVED_EXPONENTIAL_PRICE…" quer dizer cota **superior** provada (`Trinity.lean:1282–1283`: "não é cota inferior"). O próprio veredito fecha com "A_POLYNOMIAL_CROSSING_IS_OPEN", o que desfaz a leitura de cota inferior. A palavra é a do contrato congelado.

---

## Pode ser instalado?

**Sim.** Não há defeito que faça o rito falhar, nem afirmação além do kernel.

Ordem que recomendo:
1. Corrigir M1, com B4 e B1 de carona. Só muda o texto dos registros; o gerador e o ensaio rodam de novo e o kernel não muda.
2. Colher do autor a decisão sobre `Trinity` (M2) **antes** do rito.
3. Proteger o `KH_N1` até o rito (B6).

Se M1 for aceito como está, o candidato atual (`eacf3fbba3cd4df8`) instala e roda. O custo é o texto invertido no core e no rascunho de "não se afirma" da custódia.

## Limites desta revisão

- Não rodei o `um.py`, nem a guarda de frases herdada como código. Confiei no recibo e no ensaio (`ENSAIO_RESULTADO_v413.json`, 510/510), e li os textos à mão.
- Não compilei o artigo inteiro.
- Não revi a Etapa 3 (instalar, reverter, conferidor) nem o B(n).
- **Memória ACOM:** não inscrevi referência, porque a ordem limita a escrita a esta pasta.
- **Mapa de Rotas:** consultei antes ("v413 candidato revisao": 0 rotas). O registro desta revisão fica para a gerência, com os artefatos desta pasta.
- **Desvios meus da ordem:**
  - Usei `python -c` duas vezes: uma só leitura de `r02_kernel.json` e uma chamada vazia. Nada foi gravado.
  - Um `python -I -` que eu mesmo lancei ficou preso. Encerrei-o pelo PID (75388), conferindo a linha de comando antes. Nenhum outro processo foi tocado.
