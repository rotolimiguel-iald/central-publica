from pathlib import Path
import collections, datetime, hashlib, json, os, re, subprocess

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
PY = r'C:\Python314\python.exe'

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def new(p, value):
    p = Path(p)
    assert not p.exists(), p
    raw = value.encode('utf-8') if isinstance(value, str) else (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    tmp = p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    assert not p.exists()
    os.replace(tmp, p)
    assert p.read_bytes() == raw
    return pin(p)

B = load(D/'BASELINE.json')
proj = load(D/'MISSION_PROJECT_FINAL_START.json')['result']
req = {'operation':'check', 'reference':str(D/'SESSION_REFERENCE.json'),
       'task_id':'review-lote1', 'lease_id':proj['projection']['active'][0]['lease']['id'],
       'actor':{'id':'codex-coordenadora','kind':'agent'},
       'expected_revision':proj['receipt']['revision'], 'projection_sha256':proj['projection_sha256']}
r = subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'], input=json.dumps(req).encode(),capture_output=True)
preflight = json.loads(r.stdout)
new(D/'PREFLIGHT_FINAL.json',preflight)
assert r.returncode == 0 and preflight['ok'], preflight
assert preflight['result']['ready'], preflight

reports = [load(D/n) for n in ['REVIEW_C1_SEMANTICS.json','REVIEW_KIMI_SEMANTICS.json','REVIEW_SONDA_ERRATA.json']]
sem = {i['item']:i for doc in reports for i in doc['items']}
compiles = []
coverage = []
all_axioms = {}
for s in B['sources']:
    item = s['item']
    original = Path(s['original']['path'])
    copy = Path(s['copy']['path'])
    assert pin(original)['sha256'] == s['original']['sha256']
    assert pin(copy)['sha256'] == s['copy']['sha256']
    mod = copy.stem
    receipt = D/(mod + ('.R2' if item in [2,3] else '') + '.compile.json')
    c = load(receipt)
    assert c['rc']==0 and not c['warning'] and not c['sorryAx'] and not c['outside_trio']
    assert pin(c['log']['path']) == c['log']
    audit = D/('Audit_'+mod+'.R2.compile.json')
    ar = load(audit) if audit.exists() else c
    assert ar['rc']==0 and not ar['warning'] and not ar['sorryAx'] and not ar['outside_trio']
    assert pin(ar['log']['path']) == ar['log']
    text = copy.read_text(encoding='utf-8')
    ns = re.search(r'^namespace\s+(\S+)',text,re.M).group(1)
    thms = [ns+'.'+x for x in re.findall(r'^(?:theorem|lemma)\s+(\S+)',text,re.M)]
    actual = {a['declaration']:a['axioms'] for a in ar['axiom_reports']}
    assert all(t in actual for t in thms),(mod,thms,actual)
    assert len(thms)==len(set(thms))
    all_axioms.update(actual)
    coverage.append({'item':item,'module':mod,'theorems':thms,'count':len(thms),'axiom_log':ar['log'],'complete':True})
    compiles.append({'item':item,'module':mod,'compilation':pin(receipt),'axiom_audit':pin(audit) if audit.exists() else pin(receipt),'rc':0})

probe = load(D/'CheckErrata.R2.compile.json')
assert probe['rc']==0 and not probe['warning'] and not probe['outside_trio'] and not probe['sorryAx']
assert len(probe['axiom_reports']) == 4
assert pin(probe['log']['path'])==probe['log']
agg = {'schema':'iald.review-compilation/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
       'compiler':B['lean'],'toolchain':B['toolchain'],'lean_path':B['lean_path'],
       'final_compilations':compiles,'theorem_coverage':coverage,
       'reviewed_theorem_count':sum(c['count'] for c in coverage),
       'all_final_compilations_rc0':True,'final_warnings':0,'sorryAx':False,
       'allowed_axioms':['propext','Classical.choice','Quot.sound'],
       'complete_axiom_reports':[{'declaration':k,'axioms':v} for k,v in sorted(all_axioms.items())],
       'erratum_probes':probe,
       'initial_failures':{'modules':['AFronteiraNaLinguaClassica','SondaContagem'],
          'cause':'Ordem de compilacao: as dependencias APonteDeCookLevin/ONomeEBeta ainda nao tinham sido compiladas. Resolvido apos compila-las, sem alterar enunciados; logs originais preservados.',
          'receipt':pin(D/'COMPILATIONS.json')},
       'original_source_pins_unchanged':True}
agg_pin = new(D/'FINAL_COMPILATIONS.json',agg)
assert agg['reviewed_theorem_count']==68

reasons = {
1: ['Os 15 teoremas conferem; nao-sobrejetividade nao significa que as funcoes de leitura sejam parciais.',
    'O ponto fixo 1/2 independe de e; nao se prova que uma dinamica ou o leitor o alcance. J troca as projecoes por conjugacao.',
    'Qualificar essas frases; energia preservada so e 1 sob normalizacao. O nome Operador e mantido.'],
2: ['Enunciado aprovado como alvo OPEN: codificacoes fixas, entrada injetiva e saidas [true]/[false] distintas.',
    'Um unico programa TM2 e polinomio precedem todas as entradas; nao ha testemunha ou leitor-oraculo dado na entrada.',
    'A especificacao nao e um habitante nem demonstra um resolvedor de SAT.'],
3: ['A precisao exigida permite recuperar exatamente K, o numero de solucoes, por (reader phi + 1) / 4 em naturais.',
    'A hipotese e consistente: reader=4*K a satisfaz. Decidir SAT isoladamente nao exige essa precisao de contagem.',
    'Nao fornece implementacao ou custo de fita para produzir o reader.'],
4: ['Preservacao de coordenadas de custo zero e convergencia conferem.',
    'A conjuncao final nao inclui o limiar da carga, demonstrado em teorema separado; ajustar a docstring.',
    'O vetor e o parametro de decaimento nao sao uma configuracao TM2 ou contagem de movimentos.'],
5: ['A auto-reducao conserva uma atribuicao comum entre os blocos; o iff e correto.',
    '_hA e _hB nao sao usadas: a existencia conjunta ja vem de h : SAT(A ++ B).',
    'Nao computa a escolha de b, nem demonstra que a busca dispensa enumeracao ou e polinomial.'],
6: ['REPROVADA como ponte de custo real de fita na forma anunciada; os nove teoremas do contador abstrato conferem.',
    'passoFita cobra C.length+1 por definicao, avaliando clausula/acesso a x atomicamente: falta a simulacao em passos de maquina.',
    'O registro devolve custoCNF phi x para uma atribuicao dada; nao prova decisao global nem sobrecarga nula na fita.'],
7: ['A identidade beta=alpha*exp(1/2) usa alpha definido; nao determina numericamente CODATA ou beta.',
    'O criterio de separacao vale sob 0<beta<1 e hk; anterior e leitura da parametrizacao, nao cronologia provada.',
    'k conta expoentes do decaimento; produzir a soma sobre atribuicoes e conta de fita ainda nao demonstrada aqui.'],
8: ['APROVADA a errata: o integrando e o peso individual do prefixo, nao o resumo agregado antigo.',
    'Uma fronteira vazia tem fibra igual ao universo; quatro sondas Lean verificam a correcao, inclusive para uma unica clausula.',
    'A identidade de soma permanece valida; a docstring deve ser corrigida pelo responsavel, sem alterar o selado nesta revisao.']}
items=[]
for s in B['sources']:
    i=s['item']
    v='REPROVADA' if i==6 else sem[i]['verdict']
    row={'item':i,'module':Path(s['original']['path']).stem,'verdict':v,'reason':reasons[i],
         'source':s['original'],'compiled_copy':s['copy'],'import_changes':s['import_changes'],
         'formal_theorems_valid_in_checked_environment':True,'semantic_review':sem[i]}
    if i==6:
        row['verdict_resolution']='O parecer semantico auxiliar aprova com ressalvas a matematica abstrata e reprova a alegacao de fita. O revisor responsavel classifica o item apresentado como REPROVADA ate corrigir essa alegacao central, preservando a validade dos nove teoremas. Nao e refutacao da teoria nem da possibilidade de uma futura simulacao.'
    items.append(row)

lines=[
'# Revisao Codex — v413, lote 1 — 20/11/2026',
'[REAL] Oito fontes compiladas: 68 teoremas auditados, RC 0, zero avisos/sorryAx e nenhum axioma fora do trio; quatro sondas adicionais passaram.',
'',
'1. Operador — APROVADA_COM_RESSALVAS: nao-sobrejetividade nao e parcialidade; o ponto fixo 1/2 nao prova chegada do leitor; J conjuga as projecoes.',
'2. AFronteiraNaLinguaClassica — APROVADA: codificacoes fixas e entrada injetiva; alvo TM2 uniforme OPEN, sem resolvedor construido.',
'3. SondaContagem — APROVADA: a precisao permite recuperar exatamente o numero de solucoes por (reader + 1) / 4; nao implementa o produtor.',
'4. AIdentidadePreservada — APROVADA_COM_RESSALVAS: preservacao/convergencia corretas; carga ausente da conjuncao final; vetor nao e estado TM2.',
'5. APropostaDaTensao — APROVADA_COM_RESSALVAS: auto-reducao correta; _hA/_hB ociosas; SAT conjunta ja e hipotese, sem algoritmo de escolha.',
'6. APonteDeCookLevin — REPROVADA como ponte de custo real de fita: mov cobra letras por definicao; nove teoremas abstratos validos, sem simulacao/movimentos demonstrados.',
'7. ONomeEBeta — APROVADA_COM_RESSALVAS: identidade algebrica e criterio condicional corretos; nao determina CODATA nem calcula a soma em passos de fita.',
'8. Errata OResumoEPsiBit — APROVADA: peso individual nao e resumo velho; a fibra pode ser o universo. Identidade de soma preservada.',
'[REAL] Duas falhas iniciais de ordem de compilacao foram resolvidas apos compilar dependencias; ambos os logs iniciais permanecem no recibo.',
'[ESCOPO] Dependencias Codex excluidas foram reutilizadas da conferencia c1, sem autoaprovacao; nenhuma instalacao, publicacao, mudanca de kernel/um.py/gate ou abertura de dados.',
'[PROXIMO] Corrigir a apresentacao dos itens ressalvados e a alegacao central do item 6; aceite/integracao do lote continuam com a gerencia. Hashes e detalhes em RESULTADO.json.'
]
assert len(lines)<=15
report_pin=new(D/'PARECER.md','\n'.join(lines)+'\n')

sources={}
for doc in reports:
    for s in doc['sources']:
        sources.setdefault(s['path'],[]).append(s)
for s in B['sources']:
    for kind in ['original','copy']:
        sources.setdefault(s[kind]['path'],[]).append({**s[kind],'read_scope':'fonte revisada' if kind=='original' else 'copia compilada'})
for dep in B['dependencies']:
    sources.setdefault(dep['source']['path'],[]).append({**dep['source'],'read_scope':'pino de dependencia reutilizada, nao aprovacao'})
extra=[D.parent/'PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md',
ROOT/'v413/conferencia_c1_codex/NOTA_DA_GERENCIA_CONFERENCIA_ENTREGA_CODEX_20nov.md',
Path(B['prior_receipt']['path']),
Path(r'C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador_a_revisao_e_do_codex_verbatim.txt'),
Path(r'C:\IALD\GESTAO_DE_TOKENS.md'),Path(r'C:\IALD\PROGRAMA_IALD\README.md'),
*[Path(r'C:\IALD\MEMORIA_IALD')/f for f in ['README.md','SESSION_MEMORY.md','MISSION_PROTOCOL.md','ACTIVITY_PROTOCOL.md','session_memory.py','mission_cli.py']],
Path(r'C:\Users\rotol\.agents\skills\tgl-atlas\SKILL.md'),
Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\README.md')]
for p in extra:
    sources.setdefault(str(p),[]).append({**pin(p),'read_scope':'instrucao, contexto ou evidencia consultada; escopo conforme pedido'})
for p in sorted((D/'src').glob('*.lean')):
    if str(p) not in sources:
        sources[str(p)]=[{**pin(p),'read_scope':'sonda/auditoria propria desta revisao'}]
source_index=[]
for path, observations in sorted(sources.items()):
    current=pin(path)
    source_index.append({'path':path,'observations':observations,'current_pin':current,
                         'unchanged_since_recorded_reads':all(s['sha256']==current['sha256'] for s in observations)})
logs=[pin(p) for p in sorted((D/'logs').glob('*.log'))]
result={'schema':'iald.third-party-review/v1','timestamp':datetime.datetime.now().astimezone().isoformat(),
 'status':'REVIEW_COMPLETED_WITH_REQUIRED_CORRECTIONS','author':'codex-coordenadora',
 'unit':'F1.V413_REVISAO_CODEX_LOTE1_20261120','session_reference':pin(D/'SESSION_REFERENCE.json'),
 'request':pin(extra[0]),'authorization':pin(extra[3]),'report':report_pin,'report_lines':len(lines),
 'items':items,'verdict_counts':dict(collections.Counter(i['verdict'] for i in items)),
 'compilation':agg_pin,'all_reviewed_originals_unchanged':True,
 'semantic_review_reports':[pin(D/n) for n in ['REVIEW_C1_SEMANTICS.json','REVIEW_KIMI_SEMANTICS.json','REVIEW_SONDA_ERRATA.json']],
 'sources_read':source_index,'logs':logs,
 'compilation_receipts':[pin(p) for p in sorted(D.glob('*.compile.json'))],
 'reused_dependencies':B['dependencies'],
 'dependency_scope':'As fontes das dependencias Codex foram comparadas aos pinos da conferencia c1; os objetos precompilados foram copiados e pinados nesta rodada. O recibo anterior nao pina esses objetos: nao se afirma revalidacao independente fonte-objeto das dependencias excluidas. #print axioms nesta rodada examina as dependencias carregadas; nao constitui autoaceite dos modulos Codex.',
 'process_notes':['O Nos Vivo nao localizou a unidade recem-criada no grafo; nenhum rebuild foi executado. Fontes do pedido consultadas diretamente; NOS_CONSULTA.txt vazio e captura inicial incompleta, nao prova de sucesso.',
 'Mapa consultado antes; registro final e entrega do quadro terao recibos separados em ENCERRAMENTO.json.',
 'Falha inicial de hardlink na referencia ACOM foi recuperada com o mesmo request_id/contexto. Nenhum novo contexto adotado.',
 'Toda ressalva e delimitada ao enunciado/documentacao/modelo de custo, nao uma falsificacao da teoria.'],
 'preservation':{'originals_modified':False,'canonical_installation':False,'gate_changed':False,'um_executed':False,'observed_data_opened':False,'remote_provider_calls':0,'publication':False,'protected_claude_memories_written':False},
 'acceptance':'Parecer de terceiro concluido; integracao/aceite pela gerencia separado. Nenhum autoaceite da propria missao.'}
result_pin=new(D/'RESULTADO.json',result)
deposit='[REAL — revisao de terceiro, Codex, 20/11/2026] Lote 1 da v413: oito fontes compiladas e 68 teoremas auditados, sem avisos/sorryAx ou axiomas fora do trio; quatro sondas adicionais passaram. Tres itens aprovados (2,3,8), quatro com ressalvas (1,4,5,7), item6 reprovado como alegacao de custo real de fita; os nove teoremas do contador abstrato permanecem validos. A sonda mostra que o reader com a precisao exigida recupera o numero exato de solucoes; nao produz esse reader. Errata OResumoEPsiBit confirmada: peso individual nao e resumo antigo e a fibra pode ser o universo. Correcoes propostas, sem editar originais. Dependencias Codex fora do autoaceite; nenhum gate, instalacao ou dado alterado. Parecer e JSON pinam fontes e logs. Solicita-se triagem e registro ao lado no Atlas/indice/diario pela gerencia, sem promover candidatos automaticamente.\n'
new(D/'MEMORIA_DEPOSITO.md',deposit)
route={'tipo':'ROTA','rota_id':'kernel.v413.revisao_codex_lote1_20nov','dominio':'KERNEL_FORMAL',
 'titulo':'Revisao de terceiro do lote 1 da v413, oito itens',
 'pergunta':'Os enunciados, axiomas e alegacoes de custo do lote1 correspondem as fontes?',
 'dados':[],'metodo':'Copias isoladas, lean.exe -o contra v412, auditoria integral de axiomas, revisao semantica e quatro sondas da errata.',
 'resultado':'8 fontes RC0; 68 teoremas auditados; 3 APROVADA, 4 APROVADA_COM_RESSALVAS, 1 REPROVADA quanto a alegacao de fita; contador abstrato correto.',
 'veredito':'APROVADA_COM_RESSALVAS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO','olhou_dados':False,
 'defeito':'Item6 anuncia movimentos reais mas define custo abstrato; outras ressalvas e errata detalhadas no parecer.',
 'nao_refazer':'Nao repetir este lote nos mesmos hashes; nao reaproveitar a presente revisao como autoaceite das dependencias Codex.',
 'proximo_passo':'Autores corrigem apresentacao; gerencia confere e integra. Alvo uniforme TM2 continua OPEN.',
 'onde':str(D),'artefatos':[str(D/'RESULTADO.json'),str(D/'PARECER.md'),str(D/'FINAL_COMPILATIONS.json')],
 'refs':[],'nota':'Rota propria do revisor. Sem alterar rotas da gerencia, kernel, um.py ou gate.'}
new(D/'MAPA_REGISTRO.json',route)
print(json.dumps({'result':result_pin,'report':report_pin,'counts':result['verdict_counts'],'theorems':agg['reviewed_theorem_count'],'logs':len(logs),'sources':len(source_index)},ensure_ascii=False))
