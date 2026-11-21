from runner import *
from collections import Counter

base=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
for s in base['sources']:assert pin(s['path'])==s,s['path']
modules=['Trinity','AuditTrinity','CheckPriorInstrumentation','CheckTraversalVerified','CheckNames']
comp={m:json.loads((D/(m+'.compile.json')).read_text(encoding='utf-8')) for m in modules}
for r in comp.values():
    assert r['rc']==0 and not r['warning'] and not r['sorryAx'] and not r['outside_trio'],r['source']
decls=json.loads((D/'DECLARATIONS.json').read_text())['names']
assert len(decls)==87
assert sorted(e['declaration'] for e in comp['AuditTrinity']['axiom_reports'])==sorted('TGLExt.Trinity.'+n for n in decls)
assert len(comp['CheckTraversalVerified']['axiom_reports'])==8
assert len(comp['CheckNames']['axiom_reports'])==5
diff=json.loads((D/'STATEMENT_DIFF.json').read_text())
assert diff['changed']==[] and diff['removed']==[] and len(diff['added'])==8
prior=json.loads((OLD/'RESULTADO.json').read_text(encoding='utf-8'))
for i in prior['items']:
    assert pin(i['source']['path'])==i['source']
    assert pin(i['compiled_copy']['path'])==i['compiled_copy']
for s in prior['logs']:assert pin(s['path'])==s

def location(fragment):
    lines=SRC.read_text(encoding='utf-8').splitlines()
    return {'path':str(SRC),'line':next(i for i,s in enumerate(lines,1) if fragment in s)}

findings=[
 {'id':'TRINITY-DOC-UNIVERSAL','severity':'MEDIUM','inherited_from':str(PREV/'RESULTADO.json'),
  'location':location('Na fronteira, decidir pede ramificar'),
  'title':'A ramificacao deste procedimento nao e uma necessidade de todo procedimento',
  'detail':'A indecisao de inclina e o limite coupled_physical_lower nao provam que qualquer continuacao precise ramificar. O limite citado quantifica sobre a familia coupled e sua relacao Trace. Generalizar de procedimentos que chegam a contradicao para resolucao exige uma traducao com controle de custo. A R3 decide ramificando, mas isso nao demonstra a necessidade universal da escolha.',
  'correction':'Dizer que esta implementacao continua por ramificacao; delimitar coupled/Trace e as refutacoes por resolucao. Nao transferir a cota a outros metodos.'},
 {'id':'TRINITY-R3-RECTANGLES','severity':'MEDIUM','location':location('atravessar um corte de n Nomes'),
  'title':'A cobertura retangular vale para a relacao de igualdade especificada',
  'detail':'Codex.PairCut.ExactCover e definido pela avaliacao de equalCNF n em Fin.append u v, representada como existe k, left k u e right k v. exact_cover_iff prova r>=2^n para essa representacao. Nao quantifica sobre toda relacao com n variaveis partilhadas nem sobre tempo de todo algoritmo. A lista que toca clausulas de tres literais e outro objeto; nenhuma ponte na R3 identifica seu comprimento com n nessa familia/corte.',
  'correction':'Escrever: para equalCNF e a representacao por retangulos separados nos dois blocos, a cobertura exata requer 2^n retangulos. A implicacao para outra representacao ou algoritmo exige ponte propria.',
  'source':pin(BOX/'TGLExt/CorteDosPares.lean'),'explained_to_operator_before_delivery':True},
 {'id':'TRINITY-COUNT-SHORT-CIRCUIT','severity':'LOW','location':location('def custoAtravessa'),
  'also_location':location('def custoPelos'),
  'title':'Os contadores de travessia majoram a execucao com curto-circuito',
  'detail':'Bool.or e macro_inline com curto-circuito. custoAtravessa e custoPelos somam os dois filhos incondicionalmente; portanto nao sao sempre o numero exato de fixacoes no avaliador que dispensa a direita apos true. Sonda sevenLeft: 26 eventos contra contador31. Nomes [0,0] na formula vazia: 2 contra6. As sondas universais provam a mesma resposta e custo instrumentado <= contador, preservando ambas as cotas superiores.',
  'correction':'Nomear os dois contadores como majorantes por exploracao dos dois ramos, ou usar um contador que siga o curto-circuito. Dizer cota superior exponencial; nao custo necessariamente exponencial. Nenhuma cota TM2 e provada.'},
 {'id':'TRINITY-R0-R1-HISTORY','severity':'LOW','inherited_from':str(PREV/'RESULTADO.json'),
  'location':location('nenhum enunciado da R0'),
  'title':'O comentario historico sobre R0 permanece inexato',
  'detail':'A sintese a_trindade foi ampliada na R1, como medido na revisao anterior. A R2 preservou os 60 enunciados da R1 e a R3 preserva os79 da R2; essas duas afirmacoes novas estao corretas.',
  'correction':'Corrigir somente a frase historica R0/R1 conforme parecer anterior; nao reabrir lemas inalterados.'}
]
checks=[
 {'point':'frontier','verdict':'APROVADA_COM_ESCOPO','detail':'NaFronteira e a condicao local de parada sem combustivel esgotado. Sondas provam que a propagacao a fixa e inclina(k+1) fica indecisa nela; as guardas de ramificacao sobre a formula saturada implicam NaFronteira. A prova de a_inclinacao_para_so_na_fronteira segue as chamadas efetivas e usa tamanho<k para excluir esgotamento. O enunciado exporta apenas existencia de resto equissatisfativel, nao uma relacao de alcance/trace; adicionar esta relacao fortaleceria a interface sem invalidar o resultado atual. A sonda da formula vazia mostra por que existencia isolada nao caracteriza execucao.'},
 {'point':'sublist','verdict':'APROVADA','detail':'Dentro preserva sublistas por filtro e transitividade. contida=false fornece clausula residual ausente da original. Lado vivo apos propagacao suficiente nao tem clausula vazia/unitaria: comprimento>=2. Sublista propria implica comprimento original>=3. Quantificador e todo literal que ocorre no resto (l em psi.flatten), nao todo literal do universo.'},
 {'point':'complete_traversal','verdict':'APROVADA','detail':'Cada chamada recursiva fixa variavel de literal ocorrente, reduz tamanho estritamente e conserva tamanho<combustivel. Propagacao, empurrao e compromisso preservam SAT; na bifurcacao os_dois_lados e a auto-reducao correta. a_travessia_decide vale para toda CNF, sem hipotese de Horn/3CNF, com tamanho<k. Combustivel0 false nao significa UNSAT.'},
 {'point':'exponential_upper_bound','verdict':'APROVADA_COM_ESCOPO','detail':'o_preco_da_travessia prova C+B<=2^k B, B=(T+1)^2+1. Com k=T+1 da uma cota superior exponencial em tamanho. Nao e cota inferior nem tempo medido. Instrumentacao adicional prova resposta igual e eventos de fixacao <=C, mesmo com curto-circuito. Comparacoes, indices, copias e movimentos de fita nao sao cobrados.'},
 {'point':'touch_invariant','verdict':'APROVADA','detail':'Sob TresLiterais, se a clausula filtrada continua com comprimento3, a original tinha comprimento3 e a sublista de mesmo comprimento e identica. Logo ela nao contem o Nome fixado; a testemunha de Toca(i::S) pertence a S. Repeticoes de Nomes e literais nao invalidam o argumento.'},
 {'point':'names_decision','verdict':'APROVADA','detail':'Toca[] e TresLiterais eliminam clausulas de comprimento3, deixando DoisLiterais, cuja decisao R1 e reutilizada. Nos passos, ambas as restricoes preservam TresLiterais/Toca da cauda. Decisao completa para essa classe e lista admitida; lista vazia arbitraria nao basta, como mostra sete.'},
 {'point':'names_bound','verdict':'APROVADA_COM_ESCOPO','detail':'custoPelos+2<=2^S.length*((T+1)^3+2), para toda lista/CNF, sem hipotese de cobertura. A correcao da resposta usa separadamente TresLiterais e Toca. Expoente conta o comprimento da lista, inclusive repeticoes, nao necessariamente Nomes distintos nem minimo. nomesDaFronteira retorna oito copias de0 para oito e sete copias para sete; a lista [0] que serve nos exemplos e escolhida separadamente. Nao ha garantia de lista pequena nem polinomio uniforme para CNF geral.'},
 {'point':'examples','verdict':'APROVADA','detail':'Exemplos originais por decide foram recompilados com a fonte inteira. Oito/Sete permanecem fronteira sem decidir por inclinacao e recebem false/true por travessia; lista[0] os decide. Sondas adicionais cobrem combustivel0, formula vazia, curto-circuito e listas duplicadas.'}
]
item9={'item':9,'module':'Trinity R3','verdict':'APROVADA_COM_RESSALVAS',
 'reason':['87 teoremas conferem; decisao geral por atravessa e decisao de 3CNF por lista Toca com cotas superiores exponenciais de fixacoes.',
 'Contadores majoram o curto-circuito; comprimento da lista inclui repeticoes. Delimitar as frases universais sobre ramificacao/resolucao e cobertura retangular.',
 'Nao demonstra polinomio fixo em movimentos da fita; provas anteriores preservadas.'],
 'source':pin(SRC),'compiled_copy':pin(D/'src/Trinity.lean'),'formal_theorems_valid_in_checked_environment':True,
 'findings':findings,'checks':checks,'independent_lean_checks':{'new':13,'reused_instrumentation':7,'receipts':[pin(D/(m+'.compile.json')) for m in modules[2:]]}}
items=prior['items']+[item9]
lines=[
 '# Revisão consolidada Codex — v413 — 20/11/2026',
 '[REAL] Itens1–8 reutilizados após conferir hashes de fontes/cópias/logs (68 teoremas); Trinity R3:87 teoremas auditados e13 verificações novas, RC0, sem avisos, sorryAx ou axiomas fora do trio nos artefatos finais.',
 '1. Operador — APROVADA_COM_RESSALVAS: não-sobrejetividade não é parcialidade; ponto fixo1/2 não prova chegada do leitor; J conjuga projeções.',
 '2. AFronteiraNaLinguaClassica — APROVADA: alvo TM2 uniforme OPEN, entrada injetiva e codificações fixas; sem resolvedor construído.',
 '3. SondaContagem — APROVADA: precisão permite recuperar exatamente o número de soluções; não implementa nem cota o produtor.',
 '4. AIdentidadePreservada — APROVADA_COM_RESSALVAS: preservação/convergência corretas; carga ausente da conjunção final; vetor não é estado TM2.',
 '5. APropostaDaTensao — APROVADA_COM_RESSALVAS: auto-redução correta; _hA/_hB ociosas, SAT conjunta já é hipótese; não computa a escolha.',
 '6. APonteDeCookLevin — REPROVADA como ponte de custo real de fita: contador cobra letras por definição; nove teoremas abstratos válidos, sem simulação de movimentos.',
 '7. ONomeEBeta — APROVADA_COM_RESSALVAS: identidade/critério condicional corretos; não determina CODATA nem calcula a soma na fita.',
 '8. Errata OResumoEPsiBit — APROVADA: peso individual não é resumo velho; fibra pode ser universo; identidade de soma preservada.',
 '9. Trinity R3 — APROVADA_COM_RESSALVAS: fronteira/Dentro/Toca e decisões conferem; cotas superiores exponenciais de fixações, não polinômio TM2.',
 'Ajustes do item9: contadores majoram o curto-circuito (26≤31;2≤6); expoente usa lista com repetições; limitar ramificação/resolução e retângulos às famílias/representações provadas; corrigir frase histórica R0/R1.',
 '[REAL] R1→R2:19 teoremas novos; R2→R3:8; enunciados anteriores intactos nessas duas passagens. Treze sondas novas aprovadas; tentativas iniciais do revisor com erros preservadas, não usada como prova.',
 '[ESCOPO] Fontes alheias/kernel/um.py/gate preservados; sem instalação, publicação, provedor ou autoaceite. Unidade original retargetada ao consolidado por adendo, sem duplicar a revisão.',
 '[PRÓXIMO] Gerência delimita os comentários, trata a alegação do item6 e decide integração. Recibos, hashes, logs e detalhes: RESULTADO.json.'
]
assert len(lines)<=15
report=save('PARECER.md','\n'.join(lines)+'\n')
sources=base['sources']+[pin(p) for p in sorted((D/'src').glob('*.lean'))]
sources += [{'path':s['path'],'sha256':s['sha256'],'bytes':s['bytes'],'role':'Fonte/copia do lote1 conferida para reuso'} for i in prior['items'] for s in [i['source'],i['compiled_copy']]]
auxiliary=[
    D.parent/'ADENDO_3_AO_PEDIDO_DE_REVISAO_TRINITY_R2_20nov.md',
    D.parent/'ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md',
    D.parent/'ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md',
    D.parent/'PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md',
    V/'candidatas_c1/R2_trinity/build/CONFERENCIA.json',R2/'BASELINE.json',
    PREV/'finalize.py',PREV/'close.py',PREV/'PARECER.md',OLD/'PARECER.md',
    Path('C:/IALD/MEMORIA_IALD/README.md'),Path('C:/IALD/MEMORIA_IALD/MISSION_PROTOCOL.md'),
    Path('C:/IALD/MEMORIA_IALD/ACTIVITY_PROTOCOL.md'),Path('C:/IALD/MEMORIA_IALD/lib/iald_memory/mission.py'),
    Path('C:/IALD/GESTAO_DE_TOKENS.md'),Path('C:/Users/rotol/.agents/skills/tgl-atlas/SKILL.md'),
    Path('C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/README.md'),
    Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md')]
sources += [dict(pin(p),role='Fonte auxiliar consultada por trechos; pin atual, nao alegacao de prova ou leitura integral') for p in auxiliary]
logs=[pin(p) for p in sorted((D/'logs').glob('*.log'))]
logs += [pin(p) for p in sorted((R2/'logs').glob('*.log'))]
logs += prior['logs']
save('RESULTADO.json',{'schema':'iald.third-party-consolidated-review/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
 'status':'REVISAO_CONSOLIDADA_ENTREGAVEL','author':ACTOR,'request':pin(ORDER),'unit':UNIT,'session_reference':REF,
 'identity_note':'Identidade da etapa iniciada como R2 mantida; criterio alterado explicitamente para consolidado/R3 pelo pedido humano superveniente.',
 'report':report,'report_lines':len(lines),'items':items,'verdict_counts':dict(Counter(i['verdict'] for i in items)),
 'compilations':comp,'sources_read':sources,'logs':logs,'reused_lote1':pin(D/'REUSO_LOTE1.json'),
 'previous_trinity_review':pin(PREV/'RESULTADO.json'),'diff':pin(D/'STATEMENT_DIFF.json'),'byte_diff':pin(D/'R2_R3.diff'),
 'process_notes':['As tentativas CheckR2 e CheckR2Final falharam por simplificacao/aritmetica na prova instrumental do revisor; os sorryAx decorrentes de erros nao integram evidencia aprovada. Fontes/logs/recibos preservados. CheckTraversalVerified corrige a prova e revalida os oito enunciados.',
 'Revisao formal R2 ja executada foi reaproveitada; o consolidado chegou durante sua verificacao. R3 importou a mesma dependencia compilada e preserva todos os enunciados da R2.',
 'A equivalencia operacional dos avaliadores instrumentados e suas cotas e provada em Lean, nao medicao de tempo real, compilador ou fita.',
 'A relacao de igualdade citada em CorteDosPares foi lida para delimitar a referencia documental; nao se reaprova a construcao propria excluida do escopo.'],
 'preservation':{'all_source_pins_unchanged':True,'canonical_installation':False,'gate_changed':False,'um_executed':False,'data_opened':False,'external_publication':False,'remote_provider_calls':0,'protected_claude_memory_written':False},
 'acceptance':'Parecer de terceiro sobre candidatas de c1/Kimi. Integracao/aceite gerencial separados, sem autoaceite do requisito operacional.'})
save('MEMORIA_DEPOSITO.md','[REAL — revisão de terceiro Codex, consolidado v413,20nov] Nove itens:3 APROVADA,5 APROVADA_COM_RESSALVAS e item6 REPROVADA como alegação de custo real de fita (teoremas abstratos válidos). Itens1–8 reutilizados por hashes; Trinity R3 recompilada:87 teoremas,13 sondas novas e7 sondas de instrumentação reutilizadas, tudo final RC0/sem avisos/só trio. Fronteira/Dentro/Toca e decisões conferem. Cotas superiores exponenciais em fixações; não TM2. Contadores majoram curto-circuito e listas conservam repetições. Delimitar generalizações de ramificação/resolução e retângulos à família/representação provadas. Fontes originais intactas; sem instalação/kernel/um.py/gate/provedor. Solicita-se triagem e registro ao lado no Atlas/índice/diário pela gerência. Resultado/parecer contêm evidências e escopos; não promover automaticamente.\n')
save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_consolidada_trinity_r3_20nov','dominio':'KERNEL_FORMAL',
 'titulo':'Revisao consolidada v413: nove itens e Trinity R3','pergunta':'Os nove itens e o delta R3 dizem apenas o que seus teoremas e custos provam?',
 'dados':[],'metodo':'Reuso por hashes lote1; Trinity87teoremas,13sondas novas,7instrumentais reutilizadas; compilacao Lean sem lake; leitura de escopo.',
 'resultado':'3 aprovados,5 ressalvados; item6 reprovado como custo de fita. R3 decide CNF por travessia e 3CNF por lista Toca com cota superior exponencial de fixacoes.',
 'veredito':'APROVADA_COM_RESSALVAS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
 'defeito':'Alegacao de fita item6; qualificacoes documentais itens1/4/5/7/9. R3: contador maiorante, repeticoes na lista e limites de transferencia de resolucao/retangulos.',
 'nao_refazer':'Reutilizar os nove pinos e revalidar apenas deltas futuros; entrega anterior preservada.',
 'proximo_passo':'Gerencia corrige redacao e decide integracao. Nenhuma prova polinomial TM2 geral ou impossibilidade de outra via.',
 'onde':str(D),'artefatos':[str(D/'RESULTADO.json'),str(D/'PARECER.md'),str(D/'src/CheckTraversalVerified.lean'),str(D/'src/CheckNames.lean')],
 'refs':[],'nota':'Rota propria; criterio ACOM e unidade original da R2 explicitamente retargetados ao consolidado/R3, sem refazer lote1.'})
print(json.dumps({'receipt':pin(D/'RESULTADO.json'),'counts':dict(Counter(i['verdict'] for i in items)),'new_checks':13,'report_lines':len(lines)},ensure_ascii=False))
