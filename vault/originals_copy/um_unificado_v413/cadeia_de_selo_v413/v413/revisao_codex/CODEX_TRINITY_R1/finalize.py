from review import *

base=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
for source in base['sources']:
    assert pin(source['path'])==source,source['path']
compiles=[json.loads((D/(m+'.compile.json')).read_text(encoding='utf-8')) for m in ['Trinity','AuditTrinity','CheckTrinityR2']]
for r in compiles:
    assert r['rc']==0 and not r['warning'] and not r['sorryAx'] and not r['outside_trio'],r
decls=json.loads((D/'DECLARATIONS.json').read_text(encoding='utf-8'))['names']
assert sorted(r['declaration'] for r in compiles[1]['axiom_reports'])==sorted('TGLExt.Trinity.'+n for n in decls)
assert len(compiles[2]['axiom_reports'])==7
diff=json.loads((D/'STATEMENT_DIFF_R2.json').read_text(encoding='utf-8'))
assert [v['name'] for v in diff['changed']]==['a_trindade']

points=[
 {'id':'soundness','verdict':'APROVADA','lines':[469,489],'conclusion':'a_inclinacao_nao_erra vale para todo combustivel k e toda CNF: sim implica SAT; nao implica ausencia de SAT. Combustivel zero devolve indeciso; nao ha completude geral escondida.'},
 {'id':'horn','verdict':'APROVADA','lines':[496,574],'conclusion':'IsHorn e exatamente a classe da casa: no maximo uma ocorrencia positiva por clausula. Restricao e propagacao preservam essa classe. Sem vazia/unitaria, cada clausula restante tem negativo e a atribuicao toda falsa satisfaz. Decide na primeira volta com combustivel externo positivo.'},
 {'id':'integrity','verdict':'APROVADA','lines':[599,635],'conclusion':'Integra e uma inclusao extensional: cada clausula residual e membro da formula de referencia ou tem comprimento <=1. Se a variavel ocorre numa clausula original de comprimento 2, o filtro diminui seu comprimento; senao preserva a clausula. Clausulas ja curtas nao crescem.'},
 {'id':'arbitrary_literal','verdict':'APROVADA','lines':[650,677],'conclusion':'todo_lado_morre_ou_nao_corta nao exige que l ocorra. O combustivel tamanho psi cobre o tamanho da formula fixada. A propagacao termina em vazia ou sem unidades; no segundo caso a integridade elimina todos os residuos curtos, restando inclusao em psi.'},
 {'id':'two_literals','verdict':'APROVADA','lines':[688,742],'conclusion':'Para DoisLiterais (comprimento <=2), a saturacao deixa apenas clausulas de comprimento exatamente 2 quando nao conclui antes. A primeira letra ocorre; a fixacao em qualquer polaridade reduz estritamente tamanho. tamanho phi < k se conserva na chamada de k+1 para k. A decisao e completa para esta classe, inclusive formulas vazias/unitarias.'},
 {'id':'counting','verdict':'APROVADA_COM_ESCOPO','lines':[747,842],'conclusion':'A cota (T+1)^3 e para eventos de fixacao, nao passos TM2. CheckTrinityR2 prova, por tres equivalencias universais, que avaliadores pareados usam a mesma propagacao/sonda/ramificacao e devolvem exatamente (resultado,custo). Uma propagacao por lado; inclui a fixacao de compromisso/empurrao e a propagacao seguinte. A computacao de custoInclina em si, comparacoes, buscas, copias, indices e movimentos de fita nao sao cronometrados por esse contador.'},
 {'id':'examples','verdict':'APROVADA','lines':[847,920],'conclusion':'Exemplos originais e oito_fica_na_fronteira recompilados. Sonda adicional prova inclina 1 cadeia=indeciso e inclina 2 cadeia=sim; custo total=4 fixacoes. As duas voltas estavam apenas na docstring, agora conferidas separadamente. Casos CNF 0 vazia e com clausula vazia conferidos.'}
]
findings=[
 {'id':'TRINITY-R1-DOC-01','severity':'MEDIUM','location':{'path':str(SRC),'start':49,'end':51},
  'title':'O limite de uma ramificacao nao e um limite de toda continuacao',
  'detail':'oito_fica_na_fronteira estabelece somente indecisao deste procedimento em uma formula. coupled_physical_lower quantifica sobre Trace (pivots (coupled (m+1))) (coupled (m+1)) answer moves; restringe-se a essa familia e relacao de execucao. Nao prova que toda continuacao precise ramificar. A frase sobre todo procedimento que chega a contradicao produzir resolucao carece de definicao da classe e traducao com controle de custo. A auditoria nao refuta Haken nem afirma uma cota para outros sistemas de prova; delimita o que estes enunciados sustentam.',
  'suggestion':'A Trinity fica indecisa no exemplo. Se a continuacao usar o plano de ramificacao ja formalizado da casa, aplica-se, na familia coupled e sob sua relacao Trace, o limite demonstrado por coupled_physical_lower. A referencia a Haken deve ficar restrita a refutacoes por resolucao; transferi-la a outro procedimento exige uma ponte demonstrada.',
  'impact':'Correcao documental; nao invalida os 60 teoremas da R1 nem demonstra impossibilidade de uma outra continuacao polinomial.',
  'explained_to_operator_before_delivery':True},
 {'id':'TRINITY-R1-DOC-02','severity':'LOW','location':{'path':str(SRC),'start':12,'end':14},
  'title':'A sintese a_trindade teve seu enunciado ampliado',
  'detail':'R0 tem 46 teoremas; R1 tem 60. Quatorze foram acrescentados, 45 enunciados antigos permanecem iguais e a_trindade ganhou uma conjuncao de completude em DoisLiterais. O fortalecimento esta provado; apenas a frase nenhum enunciado mudou e inexata, tambem no Adendo 2.',
  'suggestion':'Os 45 lemas anteriores permanecem com os mesmos enunciados; a sintese a_trindade foi ampliada, e 14 teoremas foram acrescentados.'}
]
lines=[
 '# Parecer de terceiro — Trinity R1, item 9 — 20/11/2026',
 '1. **APROVADA_COM_RESSALVAS documentais.** As provas conferem; corrigir o alcance do comentario sobre ramificacao/resolucao e a frase sobre preservacao dos enunciados.',
 '2. [REAL] Copia identica compilada por lean.exe -o contra v412: RC 0; 60/60 teoremas auditados, sem avisos, sorryAx ou axiomas fora de propext/Classical.choice/Quot.sound.',
 '3. [REAL] Correcao para todo combustivel e CNF; completude para IsHorn da casa e clausulas com ate dois literais.',
 '4. [REAL] Integra preserva clausulas originais ou residuos de comprimento <=1; o lema de cada lado admite literal ausente; cada volta recursiva reduz tamanho.',
 '5. [REAL] Sete verificacoes adicionais em Lean: tres equivalencias de execucao/contador, duas voltas da cadeia, quatro fixacoes, casos vazios e quantificacao do literal.',
 '6. [REAL] A cota (T+1)^3 conta fixacoes no procedimento; nao e contagem de movimentos TM2 e exclui comparacoes, como declarado. Oito clausulas continuam indecisas.',
 '7. Ressalva MEDIA (linhas 49–51): indecisao nao prova necessidade universal de ramificar; o limite de coupled_physical_lower e para sua familia/Trace. A generalizacao a todo procedimento por contradicao nao foi demonstrada.',
 '8. Correcao: aplicar o limite somente ao plano/familia formalizados; restringir a referencia de resolucao ao sistema de prova correspondente, sem bloquear outras continuacoes.',
 '9. Ressalva BAIXA (linhas 12–14 e Adendo 2): 45 enunciados antigos intactos, a_trindade ampliado e 14 teoremas novos; nao e literal que nenhum enunciado mudou.',
 '10. [REAL] R0, R1, lote anterior e fontes preservados. Nenhuma instalacao, mudanca de kernel/um.py/gate, publicacao ou chamada a provedor.',
 '11. Fontes, hashes, logs, ressalvas e sondas: RESULTADO.json; aceite/integracao pela gerencia continuam separados.'
]
report=save('PARECER.md','\n'.join(lines)+'\n')
assert len(lines)<=15

extra=[Path('C:/IALD/GESTAO_DE_TOKENS.md'),Path('C:/IALD/PROGRAMA_IALD/README.md'),
 *[Path('C:/IALD/MEMORIA_IALD')/x for x in ['README.md','MISSION_PROTOCOL.md','ACTIVITY_PROTOCOL.md','session_memory.py','mission_cli.py']],
 Path('C:/Users/rotol/.agents/skills/tgl-atlas/SKILL.md'),
 Path('C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/README.md'),
 Path('C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/memoria.py'),
 BOX/'TGLExt/MovimentosDoPlano.lean',BOX/'TGLExt/PolinomioPorEscolha.lean',BOX/'TGLExt/EscolhasGlobais.lean',
 OLD/'close_review.py',OLD/'finalize_review.py',OLD/'review_compile.py',
 Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md'),Path('C:/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md')]
source_index=[dict(s,scope='Fonte do item, pedido, dependencia ou recibo previo; ver BASELINE.json') for s in base['sources']]
source_index += [dict(pin(p),scope='Fonte auxiliar consultada por trechos; indice/Atlas sao contexto, nao prova; pino medido ao concluir') for p in extra]
source_index += [dict(pin(p),scope='Sonda ou auditoria propria') for p in sorted((D/'src').glob('*.lean'))]
result={'schema':'iald.third-party-review/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
 'item':9,'candidate':'Trinity R1','verdict':'APROVADA_COM_RESSALVAS','scope':'Teoremas aprovados; duas correcoes documentais antes da integracao. Nao e prova polinomial em movimentos da fita para toda CNF.',
 'author':ACTOR,'unit':UNIT,'session_reference':REF,'source':pin(SRC),'report':report,'report_lines':len(lines),
 'main_compilation':compiles[0],'all_theorems_audit':compiles[1],'supplementary_checks':compiles[2],
 'checks':points,'findings':findings,'sources_read':source_index,'logs':[pin(p) for p in sorted((D/'logs').glob('*.log'))],
 'comparison':pin(D/'STATEMENT_DIFF_R2.json'),'byte_diff':pin(D/'R0_R1.diff'),
 'dependency':'APropostaDaTensao reutilizada da compilacao propria anterior, RC0, fonte/objeto atuais identicos aos pinos; sem repetir lote1. Dependencias seladas da caixa v412 carregadas, sem reconstrucao global.',
 'process_notes':['Nos Vivo nao localiza a unidade nova; retorno preservado em NOS_CONSULTA.json. Fontes foram abertas diretamente; nao houve reconstruir grafo.',
  'Primeira sonda CheckTrinity compilou RC0 mas teve dois avisos de argumentos simp redundantes; a fonte/log permanecem. CheckTrinityR2 remove somente esses argumentos e compila sem avisos.',
  'Inventario STATEMENT_DIFF.json perdeu cabecalhos em sintaxe de equacoes; STATEMENT_DIFF_R2.json corrige a contagem. O diff de bytes e os 60 relatorios do Lean sao preservados.',
  'Parecer entregue em arquivos locais autorizados, sem envio de mensagem externa. Ressalva explicada previamente ao operador.'],
 'preservation':{'reviewed_sources_unchanged':True,'previous_delivery_unchanged':True,'canonical_installation':False,'gate_changed':False,'um_executed':False,'data_opened':False,'external_publication':False,'remote_provider_calls':0,'protected_claude_memory_files_written':False},
 'acceptance':'Revisao de terceiro da candidata de c1. Evidencia nova do revisor nao e instalacao; requisito operacional sera submetido, sem autoaceite.'}
save('RESULTADO.json',result)
save('MEMORIA_DEPOSITO.md','[REAL — revisao de terceiro pelo Codex, item 9 v413, 20/11/2026] Trinity R1: APROVADA_COM_RESSALVAS documentais. Fonte identica compilada, 60 teoremas auditados e sete conferencias adicionais Lean, RC0/zero avisos/so trio na versao final. Correta para todo combustivel/CNF; decide Horn e ate dois literais. Equivalencias de avaliador instrumentado confirmam o contador de fixacoes; nao e cota TM2. Cadeia decide em duas voltas, quatro fixacoes. Corrigir comentario que generaliza ramificacao/resolucao a todo procedimento e frase nenhum enunciado mudou (sintese ampliada). Nao refazer lote1. Sem instalacao ou alteracao de kernel/um.py/gate. Solicita-se triagem e registro ao lado no Atlas/indice/diario pela gerencia; nao promover automaticamente candidata.\n')
save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_trinity_r1_20nov','dominio':'KERNEL_FORMAL',
 'titulo':'Revisao de terceiro Trinity R1, item 9 v413','pergunta':'As provas e descricoes da Trinity R1 correspondem ao procedimento e seu custo?',
 'dados':[],'metodo':'Copia identica, lean.exe -o/v412, 60 axiomas auditados, sete conferencias e comparacao R0/R1.',
 'resultado':'60 teoremas e 7 conferencias RC0, sem avisos/axiomas fora do trio. Horn e dois literais completos; contador segue a execucao; ressalvas documentais de escopo.',
 'veredito':'APROVADA_COM_RESSALVAS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
 'defeito':'Comentario sobre necessidade universal de ramificar/resolucao excede a prova; sintese a_trindade ampliada apesar de frase nenhum enunciado mudou.',
 'nao_refazer':'Nao repetir item9 nestes hashes; lote1 preservado. Revalidar somente alteracoes futuras.',
 'proximo_passo':'Gerencia delimita os dois comentarios e decide integracao. A cota uniforme TM2 para CNF geral continua aberta, nao refutada.',
 'onde':str(D),'artefatos':[str(D/'RESULTADO.json'),str(D/'PARECER.md'),str(D/'src/CheckTrinityR2.lean')],
 'refs':[],'nota':'Rota propria do revisor; nao altera rota c1, kernel, um.py ou gate.'})
print(json.dumps({'result':pin(D/'RESULTADO.json'),'verdict':result['verdict'],'theorems':len(decls),'supplementary':7,'report_lines':len(lines)},ensure_ascii=False))
