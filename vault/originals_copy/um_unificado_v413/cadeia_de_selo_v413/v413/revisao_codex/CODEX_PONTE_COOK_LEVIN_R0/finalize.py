from review import *
import hashlib

def artifacts():
    baseline=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
    for s in baseline['sources']: assert pin(s['path'])==s, s['path']
    comp=[json.loads((D/f).read_text(encoding='utf-8')) for f in ['PonteCookLevin.compile.json','CheckBridgeR2.compile.json']]
    for c,n in zip(comp,[22,8]):
        assert c['rc']==0 and not c['warning'] and not c['sorryAx'] and not c['outside_trio']
        assert len(c['axiom_reports'])==n
        assert pin(c['source']['path'])==c['source'] and pin(c['log']['path'])==c['log'] and pin(c['object']['path'])==c['object']
    extra=[V/'ponte_tm2_codex/APonteAoTM2.lean',V/'ponte_tm2_codex/simulacao/SimCompleta.lean']
    extra += [V/'ponte_tm2_codex/leitura_beta'/f for f in ['RelogioBeta.lean','LeituraBeta.lean','QuantizacaoBeta.lean','PonteLeituraBeta.lean','EntregaBeta.lean']]
    extra += [BOX/'TGLExt/TheKeyIsTheReader.lean',BOX/'.lake/packages/mathlib/Mathlib/Computability/StateTransition.lean',
       ROOT/'CODEX_TRINITY_R1/review.py',PREV/'close_R2.py',PREV/'MAPA_REGISTRO.json',
       ROOT/'PEDIDO_DE_REVISAO_AO_CODEX_v413_ADENDO_R7_TRINITY_R2_OPERADOR_20nov.md',
       Path('C:/IALD/MEMORIA_IALD/README.md'),Path('C:/IALD/MEMORIA_IALD/MISSION_PROTOCOL.md'),
       Path('C:/IALD/MEMORIA_IALD/ACTIVITY_PROTOCOL.md'),Path('C:/IALD/PROGRAMA_IALD/README.md'),
       Path('C:/IALD/GESTAO_DE_TOKENS.md'),Path('C:/Users/rotol/.agents/skills/tgl-atlas/SKILL.md'),
       Path('C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/README.md')]
    c1=json.loads((CONF/'CONFERENCIA_K412C.json').read_text(encoding='utf-8'))
    # Interfaces próprias consultadas, não nova autoaprovação desses módulos.
    for s in extra[:7]:
        entry=next(x for x in c1['modulos'] if Path(x['fonte'])==s)
        assert pin(s)['sha256']==entry['sha256_fonte'], s
    save('ADDITIONAL_SOURCES.json',{'sources':[pin(p) for p in extra],
      'scope':'Fontes de interface e de contexto; os módulos próprios do Codex não receberam nova revisão de mérito.'})
    atlas_previous=json.loads((D/'ATLAS_CONTEXT_PIN.json').read_text(encoding='utf-8'))
    atlas_now=pin(atlas_previous['path']);ab=Path(atlas_previous['path']).read_bytes()
    prefix_same=len(ab)>=atlas_previous['bytes'] and hashlib.sha256(ab[:atlas_previous['bytes']]).hexdigest()==atlas_previous['sha256']
    save('CONTEXT_RECHECK.json',{'atlas_before':atlas_previous,'atlas_after':atlas_now,'previous_prefix_preserved':prefix_same,
      'modified_by_this_review':False,'note':'Atlas é contexto compartilhado; não integra os pinos congelados dos objetos em revisão.'})
    bib=[
      {'author':'Stephen Cook','title':'The P versus NP Problem','url':'https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf',
       'consulted':'2026-11-20','pages':'1–5; texto extraído da fonte primária',
       'supports':'Definição de NP por verificador/certificado; redução many-one polinomial a SAT e 3-SAT; distinção de consulta a oráculo.',
       'remote_file_sha256':None,'hash_note':'Bytes remotos não foram baixados nem pinados; não apresentar hash de arquivo remoto.'},
      {'author':'Leonid Levin','title':'Universal Sequential Search Problems (1973, tradução)',
       'url':'https://www.karlin.mff.cuni.cz/~krajicek/levin.pdf','publisher_record':'https://www.mathnet.ru/eng/ppi914',
       'consulted':'2026-11-20','supports':'Universalidade por transformação eficiente e enquadramento da busca com certificado.',
       'remote_file_sha256':None},
      {'author':'E. Knill e R. Laflamme','title':'On the Power of One Bit of Quantum Information (1998)',
       'url':'https://arxiv.org/pdf/quant-ph/9802037','doi':'https://doi.org/10.1103/PhysRevLett.81.5672',
       'consulted':'2026-11-20','supports':'Estimativa aditiva de traço normalizado; repetições do estimador de variância limitada dependem de 1/epsilon². Não é leitura exata gratuita nem limite inferior universal.',
       'remote_file_sha256':None},
      {'author':'Stephen Cook','title':'The Complexity of Theorem-Proving Procedures (1971)',
       'url':'https://www.cs.utoronto.ca/~sacook/homepage/1971.pdf','consulted':'2026-11-20',
       'scope':'PDF aberto, sem texto extraído; screenshots não forneceram conteúdo visual utilizável nesta interface. Não usado como evidência de leitura integral.',
       'remote_file_sha256':None}]
    save('BIBLIOGRAPHIC_CHECK.json',bib)
    lines=SRC.read_text(encoding='utf-8').splitlines()
    line=lambda marker:next(i+1 for i,s in enumerate(lines) if marker in s)
    finding={
      'id':'PCL-F1','severity':'MEDIUM','kind':'documental_scope','blocks_theorem_validity':False,
      'path':str(SRC),'line':line('def EmPComUmaLeitura'),
      'finding':'Falta dizer expressamente que a classe definida é o fecho de SAT por redução many-one polinomial. A definição restringe o pós-processamento ao limiar positivo 2; não define toda a classe de máquinas com acesso ao oráculo.',
      'evidence':'CheckBridgeR2.one_read_iff_reduces prova EmPComUmaLeitura ↔ ReduzASAT sem usar CookLevin. O cabeçalho contém a inclusão e preserva E28, mas omite a identificação exigida pelo pedido.',
      'suggested_text':'Na língua clássica, para codificações usuais e parâmetros fixos admissíveis, esta classe é o fecho de SAT por redução polinomial many-one, portanto coincide com NP por Cook–Levin. Ela não representa toda P com acesso ao oráculo; o custo de realizar a leitura permanece externo à contagem TM2.',
      'action':'Gerência acrescenta a qualificação antes de integrar a candidata; fontes não foram alteradas pelo revisor.'}
    translation={
      'verdict':'CONCORDO_COM_A_TRADUCAO_CLASSICA','statute':'DERIVED_FROM_KNOWN_WITH_LOCAL_MODEL_ANALYSIS',
      'formal_status':'CookLevin é uma Prop e um parâmetro hCL nos teoremas. Não há habitante Lean construído nesta candidata ou revisão; o relatório de axiomas não elimina hipóteses explícitas.',
      'argument':[
        'Fixado um testemunho de EmNP, sejam p a cota do certificado e q a cota de passos TM2. O alfabeto de entrada é finito, herdado de M.tm e M.inputAlphabet; isso também foi conferido em Lean no controle np_input_alphabet_finite.',
        'Para cada palavra x, defina uma linguagem estendida: existe w binário, |w|≤p(|x|), para o qual M, iniciado em x++[sep]++map bit w, atinge a configuração haltList de [true] até q(|x|+1+|w|). A avaliação é interrompida por relógio mesmo fora da imagem de ea. O predicado de parada exata pode ser conferido em tempo polinomial.',
        'Nos x=ea(a), outputsFun garante uma saída booleana terminal no prazo; determinismo e [true]≠[false] fazem essa extensão coincidir com A(a). Se ea(a)=ea(b), as verificações para o mesmo w e a cota p coincidem, logo A(a)↔A(b). Não se precisa inverter ea, decidir sua imagem, assumir injetividade de ea ou efetividade de α.',
        'Sep e bit podem colidir sem invalidar a inclusão: constrói-se a palavra literalmente e simula-se M; o verificador clássico externo usa um enquadramento binário separado para x e w. Isso não autoriza chamar todo EmNP com enquadramento degenerado de uma apresentação equivalente de NP, nem provar a volta para esses sep/bit arbitrários.',
        'FinTM2 fornece finitos índices de pilha, rótulos e estados σ. Embora não exija todos os alfabetos internos finitos, cada programa tem AST finita e push só gera símbolos a partir de σ finito. Somados ao alfabeto finito de entrada e às pilhas inicialmente vazias, os símbolos alcançáveis formam conjunto finito. Peek/pop/load operam numa tabela finita alcançável; não há cálculo sobre números ilimitados embutido num passo.',
        'Um passo executa um trecho finito de Stmt, com tamanho constante para M; a simulação por fita tem sobrecusto polinomial. Com |w|≤p(n), o relógio q(n+1+p(n)) e a conferência da saída dão um limite polinomial para o verificador estendido.',
        'O resultado clássico aplicado a essa linguagem estendida produz uma CNF satisfazível exatamente para entradas aceitas. Escolhem-se índices consecutivos: se L ocorrências, C cláusulas e V variáveis são polinomiais em n, a fita unária tem tamanho no máximo L·V+L+C+1, ainda polinomial. Não se recodificam rótulos arbitrários exponencialmente grandes.',
        'A transformação de palavras é implementável por pilhas finitas simulando fita; a saída usa Simbolo e codificaFormula fixos. Esvaziar pilhas de trabalho, conservar a saída, restaurar initialState e emitir halt satisfaz haltList com sobrecusto polinomial. Definir g(a) como a CNF calculada sobre ea(a) dá ReduzASAT ea A. Esta é a justificação matemática da importação, não uma construção Lean já entregue.'
      ],
      'uniformity':'Máquina e polinômios são fixos por problema/verificador; c e m são fixos antes da entrada. Não se exige um único polinômio de grau universal para todos os problemas de NP.',
      'literature':bib[:2]
    }
    checks=[
      {'section':'1','status':'PASS','detail':'Identidade exponencial com 0<1−β, soma finita e cardinal 2^n; reader aplicado a travaInscrita é normalizedSum. Piso de y·2^(n+2), y∈[0,1], satisfaz a precisão diádica e a cota n+3 bits; limiar 2 decide SAT sob hm.'},
      {'section':'1/custo','status':'PASS_WITH_SCOPE','detail':'tempoPago é m(n+2)·(−log(1−β)); identidade de relógio para parâmetros fixos. O piso é noncomputable; comprimento curto da resposta não prova custo curto de produzi-la. A soma e o operador inscritos ainda são definidos sobre todas as atribuições.'},
      {'section':'2','status':'PASS','detail':'N é comprimento da palavra, positivo e superior a todo índice presente. comoNome usa min, mas indice_na_fita prova que não há colisão por clamp nos literais ocorrentes. sat_cru_sse_sat preserva o sim nas duas direções. Nome grande é cobrado em unário.'},
      {'section':'3','status':'PASS','detail':'O oráculo depende da palavra; a codificação da fórmula seguida de sep decodifica como (fórmula,[]). Controle de entrada sem fórmula recusa; controles satisfazível/insatisfazível produzem respostas distintas.'},
      {'section':'4','status':'PASS_WITH_DOCUMENTATION_FIX','detail':'Entradas são parâmetros fixos; saída [b] e codificaFormula são fixas/injetivas, sem a antiga liberdade ∃ea,eb. EmPComUmaLeitura é exatamente ReduzASAT sob hm; acrescentar a caracterização ao texto.'},
      {'section':'5','status':'PASS','detail':'A junção é defeq à entrada do verificador previamente auditado por c1. SATcru tem certificado ≤ comprimento da fórmula. A identidade somente conserva a fórmula na pilha de consulta; a decisão é do oráculo. hCL é usado na redução; o certificado physicalFockCertificate é instanciado, sem nova hipótese C arbitrária na síntese.'},
      {'section':'6','status':'PASS_WITH_SCOPE','detail':'Reconstrução correta via all_labels_from_beta, none sse ¬SAT, respostas Good e ≤letras+1 consultas. A máquina TM2 que monta a sequência de consultas e o custo da leitura não foram construídos.'},
      {'section':'documentação/E28','status':'PASS_WITH_SCOPE','detail':'Cabeçalho preserva NP⊆P com oráculo, não P^oráculo=NP^oráculo; explicita CookLevin importado, máquina nua aberta e ausência de prova física de leitura num ato. O termo physicalFockCertificate é certificado matemático do modelo, não medição de dispositivo.'}]
    report='\n'.join([
      '**Parecer Codex — Ponte Cook–Levin R0 / Trinity R7 / Operador R2 — 20/11/2026**',
      '[REAL] Item 1. **PonteCookLevin R0 — APROVADA_COM_RESSALVAS.** Fiação, precisão, codificações e teoremas conferem; falta a qualificação documental PCL-F1.',
      '[REAL] Compilação própria: RC 0, 22/22 relatórios públicos de axiomas; oito controles adicionais RC 0, zero avisos/sorry, somente o trio permitido.',
      '[REAL] O leitor do kernel iguala a soma normalizada; o piso fornece resposta de n+3 bits e o limiar decide SAT. Isso é correção matemática, não custo TM2 de produzir a leitura.',
      '[REAL] paraCNF preserva SAT; não há colisão de índices ocorrentes. A codificação da fórmula é injetiva e o alfabeto finito é consequência da máquina testemunha.',
      '[REAL] Controle próprio: EmPComUmaLeitura ↔ ReduzASAT sob hm, sem CookLevin. A classe aceita apenas o limiar positivo de uma consulta após redução.',
      '**PCL-F1:** explicitar que essa classe é o fecho many-one polinomial de SAT, igual a NP nas codificações clássicas; não é toda P com oráculo.',
      '[DERIVED/KNOWN] Concordo com a importação Cook–Levin: extensão cronometrada às palavras, alfabeto alcançável finito, índices consecutivos e limpeza para haltList preservam custo polinomial.',
      '[OPEN formal] CookLevin permanece hipótese hCL, não teorema Lean habitado nesta entrega; RESULTADO.json explicita a tradução e suas fontes primárias.',
      '[REAL] A síntese instancia o certificado de Fock existente; a reconstrução liga o leitor a soluções e ≤letras+1 consultas, sem contar movimentos da fita para realizar a leitura.',
      '[REAL] E28 e a máquina sem leitor permanecem preservadas; não se demonstrou P=NP na máquina nua nem execução física da leitura em um ato.',
      '[REAL] Item 2. **Trinity R7 — APROVADA_COM_RESSALVAS.** Mesmo hash; reutilizado o parecer anterior e suas três correções documentais, sem repetir compilação.',
      '[REAL] Item 3. **Operador R2 — APROVADA.** Mesmo hash; reutilizada a revisão anterior, sem nova compilação.',
      'O primeiro controle próprio teve apenas uma tática omega excedente; fonte/log falhos preservados e substituição R2 validada. Originais intactos.',
      'Recibo: RESULTADO.json. Sem instalação, alteração de kernel/um.py/gate, publicação ou autoaceite; integração e aceite da gerência permanecem separados.'
    ])+'\n'
    assert len(report.splitlines())<=15
    save('PARECER.md',report)
    sources=list(baseline['sources'])+ [pin(p) for p in extra]
    sources += [pin(p) for p in sorted((D/'src').glob('*.lean'))]
    sources=list({s['path']:s for s in sources}.values())
    prior=json.loads((PREV/'RESULTADO.json').read_text(encoding='utf-8'))
    result={'schema':'iald.third-party-review/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'unit':UNIT,'task':TASK,'reference':REF,'status':'APROVADA_COM_RESSALVAS',
      'verdict_counts':{'APROVADA':1,'APROVADA_COM_RESSALVAS':2,'REPROVADA':0},
      'items':[{'item':1,'candidate':pin(SRC),'verdict':'APROVADA_COM_RESSALVAS','reason':'22 teoremas públicos conferidos; oito controles. Importação clássica CookLevin justificada, sem habitante Lean. Acrescentar identificação exata da classe.'},
        {'item':2,'candidate':baseline['reused_candidates'][0],'verdict':'APROVADA_COM_RESSALVAS','reason':'Trinity R7 idêntica à revisão anterior; permanecem domínio 0<β<1 do limite, sobra ≤um passo e hLandauer global assumido.', 'reused_receipt':pin(PREV/'RESULTADO.json')},
        {'item':3,'candidate':baseline['reused_candidates'][1],'verdict':'APROVADA','reason':'Operador R2 idêntico à revisão anterior; não recompilado.', 'reused_receipt':pin(PREV/'RESULTADO.json')}],
      'compilations':comp,'checks':checks,'findings':[finding],'cook_levin_translation':translation,
      'control_failure':{'receipt':pin(D/'CheckBridge.compile.json'),'reason':'Tática omega excedente após simp já fechar unary_name_cost; nenhum erro na candidata c1. Fonte/log originais preservados; R2 remove somente essa tática.'},
      'sources':sources,'logs':[pin(p) for p in sorted((D/'logs').glob('*.log'))],
      'external_sources':bib,'prior_report':pin(PREV/'PARECER.md'),'prior_findings_preserved':prior.get('findings',[]),
      'source_scope':'Módulos próprios do Codex consultados apenas como interfaces previamente auditadas por c1; imports pinados, sem nova autoaprovação. Contextos compartilhados separados em CONTEXT_RECHECK.json.',
      'context_receipt':pin(D/'CONTEXT_RECHECK.json'),'baseline':pin(D/'BASELINE.json'),'report':pin(D/'PARECER.md'),
      'not_done':['Não instalado nem editado qualquer original de terceiros, kernel, um.py, Atlas ou Mapa alheio.',
        'Não executado/importado um.py; não usado lake; não chamado provedor; não aberto dado empírico.',
        'Nenhum habitante Lean de CookLevin construído; nenhum custo TM2 da leitura exata provado.',
        'Sem nova afirmação P=NP em fita, medição física, publicação, mudança de gate ou autoaceite.']}
    save('RESULTADO.json',result)
    save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_ponte_cook_levin_r0_20nov','dominio':'KERNEL_FORMAL',
      'titulo':'Revisao de terceiro da Ponte Cook-Levin R0','pergunta':'A fiacao e a importacao Cook-Levin preservam codificacoes, semantica e alcance?',
      'dados':[],'metodo':'Lean isolado:22 axiomas publicos e oito controles; exame das classes e traducao classica; reutilizacao R7/R2 por hash.',
      'resultado':'Ponte APROVADA_COM_RESSALVAS: identificacao documental do fecho many-one de SAT. Trinity R7 ressalvada e Operador R2 aprovado, reaproveitados.',
      'veredito':'APROVADA_COM_RESSALVAS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
      'defeito':'Falta dizer que EmPComUmaLeitura e o fecho many-one polinomial de SAT; nao toda P com oraculo.',
      'nao_refazer':'Mesmos hashes ja revisados; revalidar somente deltas futuros. CookLevin continua hipotese explicita.',
      'proximo_passo':'Gerencia acrescenta qualificacao documental e decide integracao/aceite; nao mover gate.',
      'onde':str(D),'artefatos':[str(D/f) for f in ['RESULTADO.json','PARECER.md','src/CheckBridgeR2.lean']],
      'refs':[],'nota':'Rota propria; zero instalacao e nenhuma nova cota de fita para a leitura.'})
    save('MEMORIA_DEPOSITO.md',
      '[REAL — Codex, revisão de terceiro da candidata c1] PonteCookLevin R0: APROVADA_COM_RESSALVAS. '
      '22 relatórios públicos e oito controles finais RC0/zero avisos/sorry/fora do trio. Fiação, SATcru, precisão diádica, certificado e reconstrução conferidos. '
      'Controle prova EmPComUmaLeitura ↔ ReduzASAT sem hCL; falta essa qualificação documental. '
      '[DERIVED/KNOWN] Concordância fundamentada com tradução clássica Cook–Levin; [OPEN formal] hCL continua hipótese, sem habitante Lean nesta entrega. '
      'Custo da leitura continua oráculo; não há P=NP em fita ou prova de dispositivo num ato. '
      'Trinity R7/Operador R2 preservados por hashes, com pareceres anteriores (ressalvada/aprovado). '
      'Falha mecânica do primeiro controle preservada. Nenhum original/kernel/um.py/Atlas/gate alterado; quadro/mapa/ACOM têm recibos próprios. '
      'Integração e aceite separados; depósito para triagem c1, sem escrita direta em memória protegida.\n')
    print(json.dumps({'result':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'lines':len(report.splitlines())},ensure_ascii=False))

if __name__=='__main__': artifacts()
