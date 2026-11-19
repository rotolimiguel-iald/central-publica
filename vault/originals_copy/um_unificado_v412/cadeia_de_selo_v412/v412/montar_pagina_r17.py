# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R17 = a proposta R16 com a abertura A (escolhida pelo autor) emendada pelo parecer da ordem 032
(REVISAO_032_V3_Codex.md), por trocas exatas (cada marca casa UMA vez). Confere, linha a linha da tabela do leitor da formula, que cada
termo citado e' theorem/lemma em algum dos modulos da propria linha (fontes de pedras_novas\\). Sem --executar so' ensaia. Com
--executar grava o_que_fica_claro_REV17\\O_QUE_FICA_CLARO_v412_R17.md (nao sobrescreve). A redacao final vai a' leitura de terceiro
junto com a revisao do candidato."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "o_que_fica_claro_REV16" / "O_QUE_FICA_CLARO_v412_R16_PROPOSTA_frase_A.md").read_bytes().decode("utf-8")
TROCAS = [
 # a prosa do bloco (linha 48 do parecer)
 ("Agrupar a soma lida pela fronteira não perde nada: a soma inteira é, célula a célula, o peso lido vezes o peso por ler.",
  "Agrupar a soma lida pela fronteira não perde nada: a soma inteira soma, em cada célula, os produtos do peso lido pelo peso por ler sobre as atribuições completas que caem nela; a soma simples das células da tabela dá a soma lida do prefixo."),
 ("Dois blocos só se juntam pelo mesmo conteúdo nos nomes que partilham, e a recusa de uma proposta devolve a própria cláusula violada.",
  "Dois blocos juntam-se quando há uma testemunha compatível de cada lado, as duas com os mesmos valores nos nomes que partilham, e pelo menos uma delas satisfaz a parte que lhe cabe da cláusula nova. A recusa de uma proposta devolve uma ocorrência da cláusula violada, e essa recusa se reaproveita."),
 # linha do resumo (54)
 ("`a_leitura_pela_fronteira_e_exata`: a soma lida inteira agrupa, célula a célula, o peso lido pelo peso por ler.",
  "`a_leitura_pela_fronteira_e_exata`: a soma lida inteira soma, em cada célula, os produtos do peso lido pelo peso por ler sobre as atribuições completas da célula."),
 # juncao (61)
 ("| dois blocos juntam-se pelo conteúdo dos nomes partilhados | `semantic_handshake` | `HandshakeDoNome` |",
  "| dois blocos juntam-se pelo conteúdo dos nomes partilhados | `semantic_handshake`: com os nomes comuns cobertos pelos rótulos ou pelas marcas, a fórmula com a cláusula nova é compatível se e só se há uma testemunha certificada de cada lado, as duas iguais nos rótulos, e pelo menos uma satisfaz a sua parte da cláusula. Dois ecos iguais podem falhar juntos | `HandshakeDoNome` |"),
 # recusa (62)
 ("| a recusa devolve a cláusula violada | `reuses_clause`: a recusa vale para toda atribuição que coincida nas variáveis da cláusula. `reply_bounds` e `call_bound`: para um bloco de m cláusulas, no máximo m recusas e m + 1 chamadas a um proponente exato. O custo de produzir a proposta seguinte não está cotado |",
  "| a recusa devolve a cláusula violada | `inspect_some`: a recusa devolve uma ocorrência de cláusula violada do bloco que responde. `reuses_clause`: ela vale para toda atribuição que coincida nas variáveis da cláusula. `reply_bounds` e `call_bound`: para um bloco de m cláusulas, no máximo m devoluções e m + 1 chamadas a um proponente exato, cujo tempo continua por medir |"),
 # cadeia binaria (67) e a lista da frase (14)
 ("| cadeia binária ordenada: a correlação entre as pontas cabe em quatro bits e sai das letras em exatamente L deslocamentos | `one_head`; `closed_path`, com a cláusula que liga as duas pontas. A classe é prometida: a ordenação e o reconhecimento dela em entradas arbitrárias não estão contados |",
  "| cadeia binária na ordem prometida (cada ponta nova ainda não ocorreu; as paridades dos endereços alternam): a correlação entre as pontas cabe em quatro bits e sai das letras em exatamente L deslocamentos | `one_head`: L deslocamentos em L + 1 transições. `closed_path`: os quatro valores entre as pontas em L deslocamentos, incluída a cláusula que liga as duas pontas. A ordenação e o reconhecimento da classe em entradas arbitrárias não estão contados |"),
 ("cadeias binárias ordenadas, cláusulas binárias com dois pivôs), e para a fórmula plana arbitrária", "cadeias binárias na ordem prometida, cláusulas binárias que começam por um de dois pivôs), e para a fórmula plana arbitrária"),
 # dois pivos (68)
 ("| cláusulas binárias com dois pivôs: os quatro ramos em exatamente 7L + 8T movimentos, T o número de marcas de endereço | `exact_movements`; `branch_exact` |",
  "| cláusulas binárias em que o primeiro literal é um de dois pivôs (o do endereço zero e outro) e o segundo é um nome fora dos dois: os quatro ramos em exatamente 7L + 8T movimentos, T o número de marcas de endereço | `exact_movements`: quatro passagens, com os retornos. `branch_exact`: cada ramo responde se há atribuição com aqueles dois valores. Os nomes livres podem repetir-se |"),
 # transporte (71)
 ("| o transporte da inscrição em dois bits por letra, com a reconstrução: 6L deslocamentos | `any_cnf_transport` (8L com a rebobinagem do canal). A Palavra pede leitura adicional |",
  "| o transporte da inscrição em dois bits por letra: 6L deslocamentos, somadas a transmissão e a recepção | `any_cnf_transport` (8L com a rebobinagem do canal). A reconstrução entrega a inscrição; a Palavra pede leitura adicional |"),
 # projecoes (74), registros (75), afins (76)
 ("`no_profile_update`: não há função que, do perfil de projeções do prefixo e da cláusula inteira, dê o perfil seguinte para todo prefixo e toda cláusula |",
  "`no_profile_update`: com pelo menos uma variável, não há função que, do perfil de projeções do prefixo e da cláusula inteira, dê o perfil seguinte para todo prefixo e toda cláusula |"),
 ("| limite: registros conjuntivos exatos de k pares pedem pelo menos 2 elevado a k registros | `any_exact_cube_layer` |",
  "| limite: registros conjuntivos que representem exatamente as soluções de k pares disjuntos pedem pelo menos 2 elevado a k registros | `any_exact_cube_layer` |"),
 ("| limite: cobrir exatamente a conjunção de n cláusulas de dois literais sobre pares disjuntos com k rótulos afins pede 3ⁿ ≤ k·2ⁿ |",
  "| limite: cobrir exatamente, com k rótulos afins, a conjunção de n cláusulas de dois literais positivos sobre pares disjuntos pede 3ⁿ ≤ k·2ⁿ |"),
 # chave autossuficiente (77)
 ("| limite: uma chave de b bits que responda sozinha a toda continuação que fixa w rótulos livres tem b ≥ 2 elevado a w |",
  "| limite: uma chave de b bits, exata para todo prefixo e para toda continuação que fixa os w rótulos livres, tem b ≥ 2 elevado a w |"),
 # fase densa (78)
 ("| limite: a chave em fase densa excede todo polinômio numa família | `no_fixed_dense_budget` |",
  "| limite: a chave em fase densa excede todo polinômio numa família | `charged_lower`: o percurso da cabeça até o dígito que decide. `no_fixed_dense_budget`: esse piso excede todo polinômio no comprimento da fonte |"),
 # reducao (80)
 ("| a redução: toda fórmula se embute, em no máximo 5L + 15 passos, numa instância de dois blocos com uma ponte, compatível se e só se a original é | `linear_embedding`. Logo uma regra uniforme para os indicadores dos blocos decidiria se a fórmula tem solução |",
  "| a redução: toda fórmula se embute, em no máximo 5L + 15 ações de leitura e escrita, numa instância de dois blocos com uma ponte, compatível se e só se a original é | `linear_embedding`. `genuinely_shared` e `packet_decides` ligam a ponte aos indicadores dos blocos. Quem gerasse esses indicadores uniformemente, a partir da entrada, decidiria se a fórmula tem solução; o custo dessa geração não está cotado |"),
]
for velho, novo in TROCAS:
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:70])
    t = t.replace(velho, novo)
# conferencia, linha a linha da tabela do leitor: cada termo e' theorem/lemma em algum modulo da propria linha
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("O que esta seção não diz: que o kernel decida")
bloco = t[ini:fim]; linhas = [l for l in bloco.split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    assert len(cols) == 3, l[:80]
    termos = re.findall(r"`([a-z][a-z0-9_]+)`", cols[1]); mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    if cols[2] == "—":
        assert not termos; continue
    assert termos and mods, l[:80]
    for m in mods:
        assert (V / "pedras_novas" / (m + ".lean")).exists(), "modulo sem fonte: " + m
    for x in termos:
        achou = [m for m in mods if re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), (V / "pedras_novas" / (m + ".lean")).read_text(encoding="utf-8"), flags=re.M)]
        assert achou, "termo %s nao e' theorem/lemma em %s" % (x, mods)
        n_termos += 1
for proibido in ("«", "ráculo"):
    assert proibido not in bloco
assert "P = nP" not in bloco and "Turing" not in bloco
b = t.encode("utf-8")
print("trocas:", len(TROCAS), "| linhas de conteudo da tabela:", len(linhas), "| termos conferidos:", n_termos, "| R17", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV17"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R17.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)
