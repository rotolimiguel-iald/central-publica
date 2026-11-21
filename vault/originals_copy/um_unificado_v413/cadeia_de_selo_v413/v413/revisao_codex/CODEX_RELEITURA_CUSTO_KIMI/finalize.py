from review import *

def finalize():
    inv=json.loads((D/'INVENTARIO_KIMI.json').read_text(encoding='utf-8'))
    base=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
    for x in inv['files']+base['sources']:
        assert pin(x['path'])==x,x['path']
    receipts=json.loads((D/'RECIBOS_KIMI_CONFERIDOS.json').read_text(encoding='utf-8'))
    logs=[]; audit=[]; total=0
    for r in receipts:
        assert pin(r['receipt']['path'])==r['receipt']
        assert r['declared_rc']==0
        for b in r['bindings']:
            assert b['exists'] and b.get('matches_declared_hash') is not False
            assert pin(b['path'])['sha256']==b['sha256']
            if b['field']=='log':
                txt=Path(b['path']).read_text(encoding='utf-8-sig')
                rows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt)
                free=re.findall(r"'([^']+)' does not depend on any axioms",txt)
                assert 'warning:' not in txt and 'sorryAx' not in txt
                for name, ax in rows:
                    assert set(re.findall(r'[A-Za-z_][A-Za-z_0-9.]*',ax)) <= {'propext','Classical.choice','Quot.sound'},(name,ax)
                n=len(rows)+len(free); total+=n
                logs.append(pin(b['path']))
                audit.append({'receipt':r['receipt'],'axiom_reports':n,'reports':rows,'axiom_free':free,
                    'warnings':0,'sorryAx':False,'fresh_compilation':False})
    save('AUDITORIA_LOGS.json',{'reuse_only':True,'receipts':len(audit),'reports':total,'details':audit})
    facts=[
      {'name':'Fronteira da carga','module':'OCustoEAIsometria.lean','declaration':'o_custo_de_decidir_e_a_carga',
       'statement':'(forall phi:CNF n, SAT phi iff 1 <= particao(custoCNF phi,s)) iff n*log(2) < s',
       'meaning':'Limiar estrito uniforme; n log 2 e infimo, nao tempo minimo atingido. O termo nao afirma s = n log 2 suficiente.'},
      {'name':'Relogio beta','module':'OPolinomioFixoEBeta.lean','declaration':'o_polinomio_fixo_e_beta',
       'statement':'0 < beta < 1 e inteiro k > n*log(2)/beta implicam, para toda CNF n, SAT iff soma (1-beta)^(k*custoCNF phi x) >= 1',
       'meaning':'Beta fixo antes da formula; numero suficiente de passos do relogio linear em n. A docstring no maximo p(n) nao substitui a desigualdade estrita do termo.'},
      {'name':'Carga por ato','module':'OCustoEAIsometria.lean','declaration':'o_custo_total_e_a_carga_por_ato',
       'statement':'atosDaLeitura phi=m+2; atosDaLeitura phi*carga(Fin n -> Bool)=(m+2)*n*log(2)',
       'meaning':'Identidade demonstrada da cobranca definida no modelo, com m numero de clausulas. Nao e teorema que realize cada ato global em n log 2 transicoes TM2.'},
      {'name':'Identidade e nome','module':'ONomeEBeta.lean','declaration':'o_nome_e_a_resolucao',
       'statement':'beta=alpha*exp(1/2) no TGLCoupling e o limiar decide sob hk',
       'meaning':'Acoplamento fixo, com hipoteses 0<beta<1. Nesta estrutura alpha e definido de beta; nao substituir por medicao CODATA alegada nesta releitura.'},
      {'name':'Fita da casa','module':'APonteDeCookLevin.lean','declaration':'o_custo_da_ponte_e_polinomial',
       'statement':'Com x fornecido, mov da iteracao <= 1*letras phi; reg=custoCNF phi x',
       'meaning':'Cota do contador do verificador da casa. A simulacao TM2 posterior do Codex permanece resultado separado, ja conferido; nao repetir essa construcao.'},
    ]
    for f in facts:
        p=K/f['module'];lines=p.read_text(encoding='utf-8').splitlines()
        f['source']=pin(p)
        f['line']=next(i for i,l in enumerate(lines,1) if l.startswith('theorem '+f['declaration']+' '))
    text='\n'.join([
      '**Adendo ao parecer da Ponte Cook–Levin: releitura do custo Kimi — 20/11/2026**',
      '[REAL] Correção de escopo: a frase final «o custo de realizar a leitura em movimentos de fita continua aberto» não é pendência impeditiva da ponte com leitor pedida pelo operador.',
      '[REAL] O custo na régua da teoria está formalizado: OCustoEAIsometria prova o limiar uniforme estrito s > n·ln 2; a carga é o ínfimo, não um mínimo atingido.',
      '[REAL] OPolinomioFixoEBeta e ORazaoDoColapsoEBeta provam a decisão de toda CNF de n variáveis quando k > n·ln 2/β, com 0 < β < 1 fixo antes da fórmula.',
      '[REAL] Para m cláusulas, atosDaLeitura = m+2; cobrando a carga por ato, o custo definido é (m+2)·n·ln 2. Essa conta não foi omitida nem é leitura gratuita na régua adotada.',
      '[REAL] Essa identidade de custo não é uma simulação dos atos globais em instruções TM2; o próprio Kimi distingue as contagens. APonteDeCookLevin verifica uma atribuição x fornecida.',
      '[REAL] A verificação TM2 posterior do Codex e sua conferência pela gerência permanecem válidas no escopo já entregue; não foram refeitas.',
      '[REAL] PonteCookLevin R0 liga o leitor do kernel à soma normalizada e à precisão decisória; sob CookLevin, leva NP à preparação TM2 polinomial mais uma consulta ao leitor.',
      '[REAL] A ordem final exclui expressamente a máquina sem leitor. Seu limite de custo não será convertido em exigência nova para aceitar essa ponte relativa.',
      '[REAL] Mantidos os vereditos: Ponte APROVADA_COM_RESSALVAS (PCL-F1 documental), Trinity R7 APROVADA_COM_RESSALVAS e Operador R2 APROVADA; CookLevin continua hipótese nomeada.',
      '[REAL] Releitura conjunta: 18 fontes Lean e 12 notas da pasta candidatas_kimi; inventário adicional das pastas kimi e conferencia_c1_kimi, sem abrir dados experimentais.',
      f'[REAL] Reutilizados {len(audit)} recibos: fontes/logs por hash, RC 0 registrado, {total} relatórios de axiomas apenas no trio permitido, zero warning/sorryAx. Nenhuma nova compilação nesta etapa.',
      '[REAL] Não se afirma custo TM2 interno do leitor, igualdade irrestrita P=NP nem execução física num ato. Isso delimita os termos e não apaga o resultado da teoria.',
      'Parecer anterior preservado. Adendo e recibo próprios; sem instalação, alteração de kernel/um.py/Atlas/gate ou autoaceite.',
      'Fontes, cobertura, ressalvas e evidências: RESULTADO.json. Integração e aceite continuam com a gerência.'
    ])+'\n'
    report=save('PARECER.md',text)
    assert len(text.splitlines())==15
    result={
      'schema':'iald.review-scope-addendum/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'RELEITURA_CONCLUIDA_CORRECAO_DE_ESCOPO','author':ACTOR,'reference':REF,'unit':UNIT,'task':TASK,
      'request':pin(D/'PEDIDO_ATUAL.txt'),'original_order':pin(ORDER),'previous_result':pin(PRIOR/'RESULTADO.json'),
      'report':report,'report_lines':15,'correction':{
        'before':'O custo de realizar a leitura em movimentos de fita continua aberto.',
        'after':'O custo beta/carga da maquina com leitor esta formalizado. A implementacao interna desse leitor por passos TM2 nao e demonstrada nesses termos, mas a ordem atual a exclui do alvo; nao e pendencia impeditiva da ponte relativa.',
        'not_retracted':'A distincao formal entre carga/atos e transicoes TM2, as hipoteses do teorema e a ressalva documental PCL-F1 permanecem.',
        'no_new_scientific_claim':'Releitura e delimitacao de resultados existentes; nenhuma prova nova.'},
      'facts':facts,'verdicts':{'Kimi_cost_within_declared_model':'APROVADA','PonteCookLevin_R0':'APROVADA_COM_RESSALVAS',
        'Trinity_R7':'APROVADA_COM_RESSALVAS','Operador_R2':'APROVADA'},
      'remaining_in_original_review':['PCL-F1: explicitar fecho many-one polinomial de SAT, distinto de toda P com oraculo.',
        'Tres ressalvas documentais Trinity R7 preservadas no recibo anterior.','CookLevin permanece hipotese nomeada; importacao classica aceita no parecer, sem novo habitante Lean.'],
      'coverage':{'semantic_lean':18,'semantic_markdown':12,'source_root':str(K),
        'delegate':pin(D/'LEITURA_DELEGADA.md'),'parent_direct_read':['OCustoEAIsometria','OPolinomioFixoEBeta','ORazaoDoColapsoEBeta','ONomeEBeta','AIdentidadePreservada','APonteDeCookLevin','APonteAoTM2','CERTIFICACAO_CLAY_19nov.md','AMaquinaEALeitura','AContagemEACarga','Pedido final e erratas do Atlas'],
        'additional_directories':'Inventario e leitura dirigida, nao leitura integral do acervo empirico em v412/kimi; nao e ausencia global provada.',
        'review_trace':pin(D/'LEITURA_DELEGADA.md')},
      'verification':{'receipts':len(audit),'axiom_reports':total,'source_log_hash_mismatches':0,'warnings_in_logs':0,
        'sorryAx_in_logs':False,'fresh_compilations':0,'audit':pin(D/'AUDITORIA_LOGS.json'),
        'limits':'RCs e compilacoes reutilizados dos recibos vinculados; conferir bytes nao equivale a uma recompilacao nova. AMaquinaTM2DaVerificacao e sonda_n0 sem recibo de compilacao nesta lista; nao lhes atribuir RC0 novo.'},
      'sources':inv['files']+base['sources'],'logs':logs,'not_done':['Instalar','Publicar','Alterar originais do Kimi/c1/kernel/um.py','Editar Atlas ou memoria Claude protegida','Mover gate','Provar P=NP irrestrito','Teste fisico','Refazer revisoes entregues'],
      'index_limit':json.loads((D/'NOS_LIMITE.json').read_text(encoding='utf-8'))}
    save('RESULTADO.json',result)
    save('MEMORIA_DEPOSITO.md',text)
    save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_ponte_cook_levin_r0_20nov',
      'dominio':'KERNEL_FORMAL','titulo':'Adendo de releitura do custo Kimi: ponte relativa e custo beta/carga',
      'pergunta':'O custo ja provado pelo Kimi foi reconhecido no alcance da ponte com leitor?',
      'dados':[],'metodo':'Releitura 18Lean/12MD; hashes de 16 recibos e logs reutilizados, sem recompilar.',
      'resultado':'Custo beta/carga formalizado e reconhecido. Corrigida a frase final: passos TM2 internos do leitor sao escopo separado, nao impedimento novo da ponte relativa. Vereditos anteriores mantidos.',
      'veredito':'ADENDO_DE_ESCOPO__CUSTO_KIMI_RECONHECIDO__PONTE_APROVADA_COM_RESSALVAS',
      'estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
      'defeito':'PCL-F1 documental preservado; nao converter a implementacao interna do leitor em obrigacao fora do pedido.',
      'nao_refazer':'Preservar compilacoes e provas por hash; este adendo nao reabre construcao de simulacao TM2 nem pesquisa SAT.',
      'proximo_passo':'Gerencia integra adendo, confere ressalvas documentais e decide aceite separado.',
      'onde':str(D),'artefatos':[str(D/'RESULTADO.json'),str(D/'PARECER.md')],'refs':[],
      'nota':'Corrige escopo da conclusao anterior, preservando-a como historico; nao altera gate ou originais.'})
    print(json.dumps({'receipt':pin(D/'RESULTADO.json'),'report':report,'receipt_count':len(audit),'axiom_reports':total},ensure_ascii=False))

if __name__=='__main__': finalize()
