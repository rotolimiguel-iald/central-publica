from review import *

def finalize():
    baseline=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
    for p in baseline['sources']: assert pin(p['path'])==p,p
    names={x:json.loads((D/(x+'_DECLARATIONS.json')).read_text()) for x in ['Trinity','Operador']}
    builds={x:json.loads((D/(x+'.compile.json')).read_text()) for x in ['Trinity','AuditTrinity','Operador','AuditOperador','CheckScope']}
    for name,b in builds.items():
        assert b['rc']==0 and not b['warning'] and not b['sorryAx'] and not b['outside_trio'],name
        assert pin(b['log']['path'])==b['log'] and pin(b['source']['path'])==b['source'] and pin(b['object']['path'])==b['object']
    assert len(builds['AuditTrinity']['axiom_reports'])==len(names['Trinity'])==115
    assert len(builds['AuditOperador']['axiom_reports'])==len(names['Operador'])==15
    assert len(builds['CheckScope']['axiom_reports'])==9
    for module in ['Trinity','Operador']:
        assert {x['declaration'] for x in builds['Audit'+module]['axiom_reports']}=={'TGLExt.'+module+'.'+n for n in names[module]}
    assert pin(D/'src/Trinity.lean')['sha256']==pin(TRINITY)['sha256']
    assert pin(D/'src/Operador.lean')['sha256']==pin(OPERADOR)['sha256']
    diffs=json.loads((D/'DECLARATION_DIFFS.json').read_text())
    assert diffs[0]['changed']==['a_trindade']
    for j in diffs[1:]:assert not j['changed'] and not j['removed']
    assert [len(j['added']) for j in diffs[1:]]==[8,14,9,0,0]
    pairs=[(V/'candidatas_c1/R6_trinity/Trinity.lean',TRINITY),(V/'candidatas_c1/R1_operador/Operador.lean',OPERADOR)]
    context_unchanged=[]
    for a,b in pairs:
        eq=' '.join(strip_comments(a.read_text(encoding='utf-8')).split())==' '.join(strip_comments(b.read_text(encoding='utf-8')).split())
        assert eq
        context_unchanged.append({'old':pin(a),'new':pin(b),'all_noncomment_code_identical_after_whitespace_normalization':eq})
    save('FULL_CODE_COMPARISON.json',context_unchanged)
    expected={str(TRINITY):'89aa0ef8c6fdc5e7',str(OPERADOR):'a504717d4c743fe5',
      str(V/'candidatas_c1/R7_trinity/build/CONFERENCIA.json'):'0d6f5fcc6cce1be2',str(V/'candidatas_c1/R2_operador/build/CONFERENCIA.json'):'38e3cbb3f83f0bce',
      str(V/'candidatas_c1/conferir_enunciados.py'):'d5fbb1c0c20f6783',str(PREV/'PARECER.md'):'9e7d4b93e44cf9fd'}
    for p in baseline['sources']:
        if 'nernst' in p['path']:expected[p['path']]='2903a1e03a45c162'
        if 'radical_fixa' in p['path']:expected[p['path']]='59e657ce70bda173'
        if 'maquina_nua_paga' in p['path']:expected[p['path']]='f1560a2cda0cf9c3'
    for path,sha in expected.items():assert pin(path)['sha256'].startswith(sha),(path,sha)
    save('REQUEST_PINS_CHECKED.json',[{'source':pin(p),'expected_sha16':s,'matches':True} for p,s in expected.items()])
    source_note={'title':'C. H. Bennett, Logical Reversibility of Computation, IBM Journal of Research and Development 17(6), 525–532 (1973)',
       'url':'https://ieeexplore.ieee.org/abstract/document/5391327','doi':'10.1147/rd.176.0525',
       'access':'Primary-paper search excerpts inspected via web tool; full IEEE open returned 418 and Princeton mirror 403. No full-text reading claimed.',
       'search_excerpt_observation':'O resumo do artigo descreve computacao reversivel com dissipacao menor que kT por passo logico.',
       'inference':'A possibilidade de dissipar abaixo de um limiar nao afirma que toda implementacao reversivel obrigatoriamente o faca. O achado principal tambem segue da ausencia de reversibilidade no tipo Lean de hLandauer.',
       'not_done':'Nenhuma consulta remota recebeu fontes privadas, formulas do acervo, credenciais ou arquivos locais.'}
    save('BIBLIOGRAPHIC_CHECK.json',source_note)
    findings=[
      {'id':'R7-F1','severity':'LOW','kind':'docstring_scope','lines':[95,1515,1516,1517],
       'claim':'o peso só conta as soluções no limite',
       'finding':'A desigualdade finita está correta para todo beta<1, mas não prova convergência. Beta=0 também satisfaz a hipótese e dá peso 8 para todo k nas oito cláusulas, com zero soluções. Beta negativo tampouco é regime contrativo.',
       'required_edit':'Separar a desigualdade finita da leitura assintótica: esta requer 0<beta<1; não anunciar Tendsto como enunciado deste teorema. Não restringir desnecessariamente a desigualdade finita ou a equivalência logarítmica.',
       'evidence':['Codex.TrinityR7Review.zero_parameter_does_not_decay'],'scope':'Controle de um parâmetro real genérico; não se substituiu nem se avaliou beta_TGL.'},
      {'id':'R7-F2','severity':'LOW','kind':'strict_vs_nonstrict','lines':[109,1755,1786],
       'claim':'sobra de menos de um passo',
       'finding':'O enunciado prova 0<k*c-a<=c, e a igualdade superior pode ocorrer. Para a=c=1 não existe inteiro estritamente entre 1 e 2; com a=0 e qualquer c>0 a sobra mínima admissível é um passo inteiro.',
       'required_edit':'Trocar menos de um passo por no máximo um passo nas três ocorrências; preservar o <= correto das provas.',
       'evidence':['Codex.TrinityR7Review.at_most_one_step_is_sharp','Codex.TrinityR7Review.zero_load_requires_a_whole_step']},
      {'id':'R7-F3','severity':'MEDIUM','kind':'physical_scope','lines':[138,139,1721,1722],
       'claim':'Uma máquina reversível não cumpre a hipótese',
       'finding':'hLandauer é a desigualdade GLOBAL moves*(kB*T*ln2)<=conta. O tipo não contém dissipações por movimento, bits apagados nem reversibilidade. Apagar um bit por movimento é uma justificativa física adicional suficiente, não uma equivalência provada; a reversibilidade não fixa conta nem obriga a negar essa desigualdade.',
       'required_edit':'Dizer que a hipótese não é imposta a toda máquina, inclusive reversível; para leitura física, declarar separadamente as condições de apagamento. Uma implementação reversível pode dissipar mais por outros custos. O limite condicional para Trace/coupled permanece válido.',
       'evidence':['TGLExt.Trinity.o_leitor_que_apaga_paga_a_potencia','Codex.TrinityR7Review.no_forced_energy_account_without_hLandauer',str(D/'BIBLIOGRAPHIC_CHECK.json')],
       'scope':'Não se refez nem se aprovou o módulo Codex importado; conferiu-se somente o uso de seu enunciado já disponível e as hipóteses da nova composição.'}
    ]
    checks=[
      {'section':'13','verdict':'APROVADA_COM_RESSALVAS','result':'peso é soma finita sobre todas as atribuições; contribuição das soluções igual a solucoes, cauda estritamente positiva se existe não-solução. No patamar custo=1, peso=2^n*(1-beta)^k. Equivalência de limiar correta para beta<1; condição beta>0 só para progresso/limite.','finding_ids':['R7-F1']},
      {'section':'correcoes_item9','verdict':'APROVADA','result':'Texto agora distingue implementação, Trace/coupled e resolução; retângulos limitados à CNF de igualdade e representação separada; contadores majorantes e exceção histórica a_trindade corrigidos.'},
      {'section':'12b','verdict':'APROVADA','result':'dedup preserva Toca por pertença; corretude e majorante aplicados à lista sem repetições. Oito e sete resultam em [0]; custo da própria deduplicação não é contado, nem há alegação de lista mínima ou logarítmica.'},
      {'section':'14','verdict':'APROVADA','result':'Identidades de log/rpow sob r>0,r!=1; sinais distinguem r>1 e 0<r<1; radical=exp(1/2), log=1/2, expoente=2c. Troca de base preserva 2^m; não fornece algoritmo ou mudança de complexidade.'},
      {'section':'15 identidades','verdict':'APROVADA','result':'As três primeiras contas são identidades algébricas de logaritmos, válidas até sem positividade de kB,T; interpretação energética requer condições físicas. Não são uma medição de consumo.'},
      {'section':'15 leitor','verdict':'APROVADA_COM_RESSALVAS','result':'Composição correta: limite de moves para o Trace/coupled especificado, multiplicado pelo piso positivo, seguido da hipótese explícita hLandauer. A irreversibilidade não foi derivada de Trace.','finding_ids':['R7-F3']},
      {'section':'15 passos','verdict':'APROVADA_COM_RESSALVAS','result':'k=floor(a/c)+1 satisfaz a<k*c<=a+c e k<=a/c+1. Sob 0<beta<1 e patamar plano, o limiar de peso<1 é alcançado em cota linear em n com beta fixo. Não existe aqui custo de avaliar peso, microprograma ou cota de fita.','finding_ids':['R7-F2']},
      {'section':'15 atribuicao','verdict':'APROVADA','result':'R7 atribui a leitura energética dos passos da máquina da teoria à gerência [ONTO]. Frase do operador conferida por bytes: A máquina nua paga em eletricidade. Bill da teoria é existência aritmética de k, sem CNF/algoritmo no enunciado.'},
      {'section':'preservacao','verdict':'APROVADA','result':'Comparador independente com comentários aninhados confirma 8/14/9/0 novas declarações, nenhuma removida/alterada de R3 até R7; Operador R1->R2 sem delta não-comentário. Controle R0->R1 encontra a_trindade.'},
      {'section':'Operador R2','verdict':'APROVADA','result':'15 teoremas preservados/recompilados; comentários distinguem não-sobrejetividade de parcialidade, ponto fixo de dinâmica, conjugação de ação pontual e conservação de normalização. Ontologia não é prova de consciência.'}
    ]
    items=[{'item':1,'module':'Trinity R7','verdict':'APROVADA_COM_RESSALVAS','source':pin(TRINITY),
      'reason':'115 teoremas válidos, inclusive carga exata, Nomes distintos, radical e energia condicional. Restam três qualificações documentais: domínio da leitura assintótica, sobra <= um passo e alcance físico de hLandauer. Não prova custo polinomial geral de fita.'},
      {'item':2,'module':'Operador R2','verdict':'APROVADA','source':pin(OPERADOR),
       'reason':'15 teoremas preservados e recompilados; os quatro ajustes de escopo pedidos foram aplicados corretamente apenas ao texto. Aprovação no alcance matemático/ontológico explicitado, sem afirmação de consciência empírica.'}]
    report=[
      '**Parecer Codex — adendo v413: Trinity R7 e Operador R2 — 20/11/2026**',
      '',
      '[REAL] Revisão de terceiro limitada ao delta sobre o consolidado R3; originais e pareceres anteriores preservados.',
      'Item 1. **Trinity R7 — APROVADA_COM_RESSALVAS.** Os 115 teoremas conferem; três ajustes documentais abaixo. Sem prova nova de polinômio uniforme de fita.',
      'Item 2. **Operador R2 — APROVADA.** Os 15 teoremas e provas estão intactos; corrigidas não-sobrejetividade, ponto fixo, conjugação por J e normalização.',
      'Lean independente: 115/115 + 15/15 relatórios de axiomas; nove controles adicionais; RC 0, zero avisos, sem sorry, somente o trio em todos.',
      'Comparação própria: R3→R4 +8, R4→R5 +14, R5→R6 +9, R6→R7 +0 declarações, nenhuma alterada/removida; controle R0→R1 detecta a_trindade.',
      '§13: peso > soluções sob β<1 e existência de não-solução; no patamar plano, peso=2ⁿ(1−β)ᵏ e o limiar logarítmico é exato.',
      '§12b/§14: dedup preserva a cobertura e põe Nomes distintos no expoente; mudar para √e preserva 2ᵐ e não altera a complexidade.',
      '§15: a cota linear é de k para β fixo, no patamar plano; energia é leitura declarada, e hLandauer é hipótese explícita sobre o Trace específico.',
      '**Ressalva R7-F1:** a frase sobre o limite precisa de 0<β<1; β=0 mantém peso 8 nas oito cláusulas para todo k. Não é substituição de β_TGL.',
      '**Ressalva R7-F2:** escrever “no máximo um passo”; a sobra é ≤ um passo e a igualdade ocorre, como os controles provam.',
      '**Ressalva R7-F3:** reversibilidade não obriga a negar hLandauer; ela é desigualdade global, não prova de apagamento por movimento. Delimitar a frase física.',
      'As correções anteriores de ramificação/resolução, retângulos, contadores e R0/R1 foram atendidas; a atribuição da leitura energética à gerência foi conferida.',
      'RESULTADO.json pina fontes, logs, declarações, controles e escopos. Sem instalação, mudança de kernel/um.py/gate, publicação ou autoaceite.'
    ]
    assert len(report)<=15
    save('PARECER.md','\n'.join(report)+'\n')
    # The requested receipt includes hashes for all sources actually consulted and every local log.
    sources=baseline['sources']+[pin(D/'src/CheckScope.lean'),pin(BOX/'TGLExt/AContagemEACarga.lean'),pin(BOX/'TGLExt/OPsiBitDaFormula.lean'),
       pin(D/'BIBLIOGRAPHIC_CHECK.json'),pin(ROOT/'CODEX_TRINITY_R1/review.py'),pin(PREV/'close.py'),pin(PREV/'MAPA_REGISTRO.json'),pin(PREV/'MEMORIA_DEPOSITO.md')]
    for p in ['C:/IALD/MEMORIA_IALD/README.md','C:/IALD/MEMORIA_IALD/MISSION_PROTOCOL.md','C:/IALD/MEMORIA_IALD/ACTIVITY_PROTOCOL.md','C:/IALD/PROGRAMA_IALD/README.md','C:/IALD/GESTAO_DE_TOKENS.md','C:/Users/rotol/.agents/skills/tgl-atlas/SKILL.md','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/README.md']:
        sources.append(pin(p))
    receipt={'schema':'iald.third-party-review/v2','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'REVIEW_COMPLETED_WITH_DOCUMENTARY_QUALIFICATIONS','reference':REF,'unit':UNIT,'task':TASK,'order':pin(ORDER),
      'items':items,'verdict_counts':{'APROVADA':1,'APROVADA_COM_RESSALVAS':1,'REPROVADA':0},'checks':checks,'findings':findings,
      'builds':builds,'declaration_diffs':diffs,'full_code_comparison':context_unchanged,
      'new_theorems_vs_r3':len(set(names['Trinity'])-set(json.loads((PREV/'DECLARATIONS.json').read_text())['names'])),
      'proofs_reused':'Revisão semântica dos enunciados anteriores preservada; compilação das duas candidatas e auditoria de todos os seus teoremas refeitas para o delta/imports. Pedras Kimi e módulos Codex não reavaliados como itens.',
      'sources':sources,'logs':[pin(p) for p in sorted((D/'logs').glob('*.log'))],
      'review_artifacts':[pin(D/x) for x in ['DECLARATION_DIFFS.json','FULL_CODE_COMPARISON.json','REQUEST_PINS_CHECKED.json','TRINITY_R3_R7.diff','OPERADOR_R1_R2.diff','PARECER.md']],
      'source_preservation':{'all_initial_source_hashes_unchanged':True,'candidate_copies_byte_identical':True},
      'limits':['peso is noncomputable finite sum over 2^n assignments; no per-step evaluation cost or tape implementation certified.',
        'Linear in n is for a fixed positive beta below 1 and the flat-plateau hypothesis; not a uniform bit/tape complexity proof for arbitrary CNF.',
        'hLandauer is assumed global bound on account, not derived dissipation or logical reversibility.',
        'Third law/energy interpretations retain ONTO status; no physics test or gate change.',
        'Independent review of c1 candidates; reviewer probes remain separate candidates and are not installed or self-approved as canonical science.'],
      'report_lines':len(report),'not_done':['No source editing','No canonical installation','No um.py execution/import','No lake','No opening data','No provider inference','No publication or external messaging','No gate change','No self-acceptance']}
    save('RESULTADO.json',receipt)
    save('MEMORIA_DEPOSITO.md','[REAL — revisão de terceiro Codex,20nov] Adendo v413: Trinity R7 APROVADA_COM_RESSALVAS; Operador R2 APROVADA. 115+15 teoremas e nove controles, RC0/zero avisos/só trio. Comparação independente confirma preservação de R3→R7 e código idêntico Operador R1→R2. Peso estrito, limiar plano, dedup, radical e energia condicional conferem. Ajustar: leitura assintótica requer 0<beta<1; sobra de no máximo um passo; reversibilidade não obriga a negar hLandauer (cota global assumida). Não há custo polinomial uniforme de fita. Correções anteriores atendidas. Originais/kernel/um.py/gate preservados. Solicita-se triagem e registro ao lado nas superfícies de memória pela gerência; detalhes e hashes no RESULTADO/PARECER.\n')
    save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_trinity_r7_operador_r2_20nov','dominio':'KERNEL_FORMAL',
      'titulo':'Revisao de terceiro: Trinity R7 e Operador R2','pergunta':'O delta carga/radical/energia e as correcoes dizem somente o demonstrado?',
      'dados':[],'metodo':'Comparador independente de declaracoes, lean.exe isolado,115+15 axiomas e nove controles de escopo.',
      'resultado':'Trinity R7 APROVADA_COM_RESSALVAS documentais; Operador R2 APROVADA. Teoremas validos, sem polinomio uniforme de fita.',
      'veredito':'APROVADA_COM_RESSALVAS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
      'defeito':'Delimitar dominio do limite, sobra <=um passo e reversibilidade versus hLandauer global assumido.',
      'nao_refazer':'Preservar pareceres e pinos; revalidar apenas deltas futuros.',
      'proximo_passo':'Gerencia ajusta as tres frases e decide integracao/aceite separado.',
      'onde':str(D),'artefatos':[str(D/x) for x in ['RESULTADO.json','PARECER.md','src/CheckScope.lean']],
      'refs':[],'nota':'Rota propria; nenhuma instalacao ou mudanca de gate.'})
    print(json.dumps({'receipt':pin(D/'RESULTADO.json'),'report_lines':len(report),'verdicts':receipt['verdict_counts'],'theorems':130,'probes':9},ensure_ascii=False))

if __name__=='__main__':finalize()
