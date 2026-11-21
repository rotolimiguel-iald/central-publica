from review import *
from collections import Counter

def assemble():
    p=mission({'operation':'project'},'MISSION_PRE_INTEGRATION')
    task=next(x for x in p['projection']['active'] if x['id']==TASK)
    assert mission({'operation':'check','actor':ACTOR,'expected_revision':p['receipt']['revision'],
      'projection_sha256':p['projection_sha256'],'task_id':TASK,'lease_id':task['lease']['id']},'PREFLIGHT_INTEGRATION')['ready']
    base=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
    mech=json.loads((D/'MECHANICAL_R2.json').read_text(encoding='utf-8'))
    assert mech['all_code_equal'] and mech['all_audits_pass']
    sources={}
    def add(x):
        actual=pin(x['path']);assert actual['sha256']==x['sha256'],x['path']
        key=str(Path(x['path']).resolve()).lower()
        if key not in sources:sources[key]=actual
    for x in base['sources']+mech['sources']:add(x)
    for f in ['BASELINE.json','MECHANICAL_R2.json','VERIFICADOR_HISTORIA_R2.json']:
        add(pin(D/f))
    modules=[];findings=[];delegated=[]
    for f in ['beta.json','tm2.json','kimi.json']:
        q=D/'reviews'/f;v=json.loads(q.read_text(encoding='utf-8'));add(pin(q));delegated.append(pin(q))
        for x in v.get('read_files',v.get('files_read',[])):add(x)
        for x in v.get('modules',v.get('reviews',[])):
            modules.append({k:x[k] for k in ['module','verdict','reason','findings'] if k in x})
            for item in x.get('findings',[]):
                if isinstance(item,dict):findings.append(item)
        findings.extend(v.get('findings',[]))
    modules.append({'module':'TGLExt.PonteCookLevin','verdict':'APROVADA',
      'reason':'Preserva os localizadores Lean, o fecho positivo de SAT por reducao many-one e CookLevin como hipotese nomeada. Mantem separados o custo do relogio beta e os passos TM2; a limpeza retira apenas historia.',
      'findings':[]})
    assert len(modules)==22 and len({x['module'] for x in modules})==22
    for m in modules:
        assert len(m['reason'].splitlines())<=3
    findings={f['id']:f for f in findings}
    mismatch=base['manifest_mismatches'];assert len(mismatch)==1
    mm=mismatch[0];assert mm['actual']['sha256'].startswith('9ef5b29fd30661ed')
    findings['META-DIFF-01']={'id':'META-DIFF-01','severity':'BAIXO','category':'PIN_DESATUALIZADO',
      'module':None,'path':str(I/'MANIFESTO_PEDRAS_v413.json'),
      'reason':'O manifesto pina o diff anterior, enquanto o pedido explicito pina corretamente o diff atual. Todas as21origens e21pedras conferem; diffs regenerados para a revisao.',
      'expected_in_manifest':mm['expected'],'measured':mm['actual'],
      'proposed_text':'Atualizar somente recibos.diff.sha256 (ou campo equivalente da entrada do diff) para o hash integral medido '+mm['actual']['sha256']+'; recalcular o hash do manifesto nos recibos dependentes.'}
    for f in ['diffs/PonteCookLevin.diff','diffs/OResumoEPsiBit.diff']:
        add(pin(D/f))
    for f in ['C:/IALD/MEMORIA_IALD/README.md','C:/IALD/MEMORIA_IALD/MISSION_PROTOCOL.md','C:/IALD/GESTAO_DE_TOKENS.md',
      'C:/Users/rotol/.agents/skills/tgl-atlas/SKILL.md','C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/fila/README.md',
      str(ROOT/'CODEX_TRINITY_R1/review.py'),str(ROOT/'CODEX_RELEITURA_CUSTO_KIMI/close.py'),str(ROOT/'CODEX_RELEITURA_CUSTO_KIMI/MAPA_REGISTRO.json')]:add(pin(f))
    counts=dict(Counter(x['verdict'] for x in modules if x['module']!='TGLExt.OResumoEPsiBit'))
    approved=', '.join(x['module'].removeprefix('TGLExt.') for x in sorted(modules,key=lambda x:x['module']) if x['verdict']=='APROVADA' and x['module']!='TGLExt.OResumoEPsiBit')
    remarks=', '.join(x['module'].removeprefix('TGLExt.') for x in sorted(modules,key=lambda x:x['module']) if x['verdict']=='APROVADA_COM_RESSALVAS')
    report='\n'.join([
      '# Revisao das pedras limpas v413 — Codex — 20/11/2026',
      '[REAL] Leitura documental das21pedras e da errata OResumoEPsiBit; sem recompilacao ou alteracao das fontes.',
      f"Vereditos das21pedras: {counts.get('APROVADA',0)} APROVADAS; {counts.get('APROVADA_COM_RESSALVAS',0)} APROVADAS_COM_RESSALVAS; {counts.get('REPROVADA',0)} REPROVADAS.",
      'APROVADAS: '+approved+'.',
      'APROVADAS_COM_RESSALVAS: '+remarks+'. Motivos e substituicoes exatas por modulo em RESULTADO.json.',
      '[REAL] Codigo preservado nos22pares, descontados comentarios, linhas vazias e finais de linha; verificador da casa tambem IDENTICO nos21novos.',
      '[REAL] Fontes e logs existentes reconciliados:274relatorios novos+18da errata; RC0 registrados, nenhum aviso/sorryAx/axioma fora do trio.',
      '[REAL] Quatro correcoes Kimi conferidas: custo cobrado do iterador; hipoteses _hA/_hB ociosas; alpha definido/k expoente; conjuncao final sem carga.',
      'OResumoEPsiBit — APROVADA: a docstring usa peso individual e admite fibra-universo na fronteira vazia; somente a docstring mudou.',
      'Reposicoes documentais: SimCompleta/verificacao_tm2_polinomial, fonte Tensao_Fundamental.docx e a_maquina_e_uma_leitura_decidem com escopos distintos.',
      'Precisao textual: PonteLeituraBeta recebe reader/hr; Trinity deve explicitar expoente (m ln2)/(ln sqrt(e))=2m ln2 na docstring final.',
      'Metadado: manifesto ainda pina diff58674f73..., mas pedido e arquivo coincidem em9ef5b29f...;21pares principais integros, correcao do pino proposta.',
      '[ESCOPO] Custo da casa reconhecido; sem novo requisito de construir leitor TM2. Nenhuma promocao ontologica/fisica, instalacao, publicacao ou movimento de gate.',
      '[PROXIMO] Gerencia aplica os ajustes de texto/metadado e decide integracao; per-module verdicts e SHA256 integrais em RESULTADO.json.'
    ])+'\n'
    assert len(report.splitlines())<=15
    rp=save('PARECER.md',report)
    result={'schema':'iald.pedras-limpas-documentary-review/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
      'unit':UNIT,'task':TASK,'reference':REF,'status':'APROVADA_COM_RESSALVAS_DOCUMENTAIS','report':rp,
      'verdict_counts_new_modules':counts,'modules':sorted(modules,key=lambda x:x['module']),
      'findings':list(findings.values()),'mechanical':pin(D/'MECHANICAL_R2.json'),'delegated_reviews':delegated,
      'sources':sorted(sources.values(),key=lambda x:x['path']),
      'coverage':'Leitura semantica integral dos21pares feita em3lotes mais PonteCookLevin pelo coordenador; errata OResumo por diff/docstring/enunciado. Contexto e remissoes consultados de forma dirigida; hashing de arquivo nao implica leitura integral de corpus contextual. Relatorios dos lotes discriminam cobertura.',
      'prior_review_reuse':'Pareceres anteriores mantidos; presente aceite e documental da copia limpa, nao autoaceite de ciencia nova. As quatro correcoes sanam os pontos do consolidado; pequenas ressalvas atuais nao invalidam os termos.',
      'recorded_compilation_scope':'Reconciliacao de fontes por hash, comandos #print, nomes e conjuntos de axiomas dos logs existentes; nenhum novo processo Lean nesta rodada.',
      'not_done':['editar origens/pedras limpas/manifesto alheios','compilar Lean/lake','executar/importar um.py','instalar/publicar/mover gate','autoaceitar missao','reiniciar automacoes ou chamar provedores externos']}
    result_pin=save('RESULTADO.json',result)
    save('MAPA_REGISTRO.json',{'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_pedras_limpas_20nov','dominio':'KERNEL_FORMAL',
      'titulo':'Revisao documental de terceiro das21pedras limpas v413 e errata OResumoEPsiBit',
      'pergunta':'A limpeza preserva o codigo, o alcance, os estatutos e os localizadores tecnicos?',
      'dados':[],'metodo':'Comparacao integral em lotes, verificacao mecanica22pares, hashes e reconciliacao de292relatorios existentes; sem recompilar.',
      'resultado':f'{counts}; errata aprovada. Ressalvas documentais com texto proposto e pino antigo do diff no manifesto.',
      'veredito':'APROVADA_COM_RESSALVAS_DOCUMENTAIS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
      'defeito':'Remissoes/precisao textual e pino auxiliar desatualizado; codigo preservado.',
      'nao_refazer':'Nao recompilar provas sem mudanca de codigo; nao reabrir custo ja reconhecido nem alterar fontes alheias.',
      'proximo_passo':'Gerencia integra correcoes documentais e decide aceite separado.',
      'onde':str(D),'artefatos':[str(D/'RESULTADO.json'),str(D/'PARECER.md')],'refs':[],
      'nota':'Entrega documental; sem instalacao, gate, confirmacao fisica ou autoaceite.'})
    save('MEMORIA_DEPOSITO.md',report+'\nFontes com hashes integrais no recibo RESULTADO.json; aplicar conceitos apenas pela triagem da gerencia.\n')
    print(json.dumps({'receipt':result_pin,'report':rp,'counts':counts,'findings':list(findings),'sources':len(sources)},ensure_ascii=False))

if __name__=='__main__':assemble()
