from review import *
import os

def replace_with_backup(path, data):
    old=path.read_bytes();stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bak=path.with_name(path.name+'.bak_'+stamp)
    with bak.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
    assert bak.read_bytes()==old
    temp=path.with_name(path.name+'.final.tmp')
    with temp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert temp.stat().st_size==len(data) and temp.read_bytes()==data
    os.replace(temp,path);assert path.read_bytes()==data
    return {'before':pin(bak),'after':pin(path)}

r=json.loads((D/'RESULTADO.json').read_text(encoding='utf-8'))
approved=', '.join(x['module'].removeprefix('TGLExt.') for x in r['modules'] if x['verdict']=='APROVADA' and x['module']!='TGLExt.OResumoEPsiBit')
remarks=', '.join(x['module'].removeprefix('TGLExt.') for x in r['modules'] if x['verdict']=='APROVADA_COM_RESSALVAS')
report='\n'.join([
 '# Revisão das pedras limpas v413 — Codex — 20/11/2026',
 '[REAL] Leitura documental das 21 pedras e da errata OResumoEPsiBit; sem recompilação ou alteração das fontes.',
 'Vereditos das 21 pedras: 16 APROVADAS; 5 APROVADAS_COM_RESSALVAS; 0 REPROVADAS.',
 'APROVADAS: '+approved+'.',
 'APROVADAS_COM_RESSALVAS: '+remarks+'. Motivos e substituições exatas por módulo em RESULTADO.json.',
 '[REAL] Código preservado nos 22 pares, descontados comentários, linhas vazias e espaços finais; finais de linha normalizados. Verificador da casa: IDENTICO nos 21 novos.',
 '[REAL] Fontes e logs existentes reconciliados: 274 relatórios novos + 18 da errata; RC 0 registrados, sem avisos, sorryAx ou axiomas fora do trio.',
 '[REAL] Quatro correções Kimi conferidas: custo cobrado do iterador; hipóteses _hA/_hB ociosas; α definido e k expoente; conjunção final sem carga.',
 'OResumoEPsiBit — APROVADA: a docstring usa peso individual e admite fibra igual ao universo na fronteira vazia; somente a docstring mudou.',
 'Remissões a repor: SimCompleta/verificacao_tm2_polinomial, fonte Tensao_Fundamental.docx e a_maquina_e_uma_leitura_decidem, distinguindo os objetos.',
 'Precisão textual: PonteLeituraBeta recebe reader/hr; a docstring final da Trinity deve explicitar o expoente (m·ln 2)/(ln √e) = 2m·ln 2.',
 'Metadado: manifesto ainda pina o diff 58674f73..., mas pedido e arquivo coincidem em 9ef5b29f...; os 21 pares principais estão íntegros.',
 '[ESCOPO] Custo da casa reconhecido; sem novo requisito de construir leitor TM2. Nenhuma promoção a confirmação física, instalação, publicação ou movimento de gate.',
 '[PRÓXIMO] Gerência aplica os ajustes de texto/metadado e decide integração. Vereditos individuais, propostas e SHA256 integrais em RESULTADO.json.'
])+'\n'
assert len(report.splitlines())<=15
changes=[replace_with_backup(D/'PARECER.md',report.encode('utf-8'))]
r['report']=pin(D/'PARECER.md')
r['verdict_counts_new_modules']['REPROVADA']=0
f=next(x for x in r['findings'] if x['id']=='META-DIFF-01')
f['json_pointer']='/recibos/DIFF_DA_LIMPEZA_v413.txt/sha256'
f['proposed_text']='Atualizar recibos["DIFF_DA_LIMPEZA_v413.txt"].sha256 para '+f['measured']['sha256']+'; recalcular o hash do manifesto nos recibos dependentes.'
changes.append(replace_with_backup(D/'RESULTADO.json',(json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode('utf-8')))
changes.append(replace_with_backup(D/'MEMORIA_DEPOSITO.md',(report+'\nRegistro documental para triagem c1, com propostas e fontes pinadas no recibo; originais preservados.\n').encode('utf-8')))
save('FINAL_STAGING.json',{'purpose':'Revisão de redação do relatório e ponteiro exato do metadado, antes da entrega; vereditos e evidências preservados.','changes':changes})
print(json.dumps({'receipt':pin(D/'RESULTADO.json'),'report':pin(D/'PARECER.md'),'report_lines':len(report.splitlines())},ensure_ascii=False))
