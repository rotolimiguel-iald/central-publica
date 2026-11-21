# -*- coding: utf-8 -*-
"""gerar_pronto_etapa3_v413.py -- o FECHO da Etapa 3 da v413 (construtor da Etapa 3, a servico da gerencia c1, 20/11/2026): grava
...\\cadeia_de_selo\\v413\\PRONTO_ETAPA3_v413.json com cada script e texto derivado (sha16 e bytes LIDOS do disco), o que foi ensaiado e o resultado
(lido dos recibos dos ensaios), o que depende do candidato, o que depende do B(n), os textos que o pos-rito regera, os achados para a Etapa 2 e a
gerencia, os desvios e o que nao foi tocado. Escrita por temporario; backup de bytes do anterior. Nada mais roda daqui: e' o ponto de PARADA."""
import hashlib, json, os, time
from pathlib import Path
E3 = Path(__file__).resolve().parent; V = E3.parent; P = V / "pos_rito"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).is_file() else None
ARQ = {
    "esperados_v413_foco.py": V, "instalar_v413.py": V, "reverter_v413.py": V, "rito_v413.sh": V, "carimbar_stdout_v413.py": V, "portao_ambiente_pilar_v413.py": V,
    "pilar_no_stdout_v413.py": V, "conferir_pos_rito_v413_foco.py": V, "montar_handoff_e_linhagem_v413.py": V, "guarda_privada_v413.py": V, "ROTEIRO_EXECUCAO_v413.md": V,
    "cadeia_pos_rito_v413.sh": P, "adaptar_arvore_da_prova_v413.py": P, "guarda_titulo_versao_v413.py": P, "diffs_v413.py": P, "gerar_entrega_a_custodia_v413.py": P,
    "derivar_rito_e_carimbo_v413.py": E3, "ensaio_mundo_falso_v413.py": E3, "teste_etapa3_sem_candidato_v413.py": E3, "gerar_pronto_etapa3_v413.py": E3}
scripts = {}
for n, d in ARQ.items():
    p = d / n; assert p.is_file(), ("falta", p)
    scripts[str(p.relative_to(V)).replace("/", "\\")] = {"sha16": sha(p)[:16], "bytes": p.stat().st_size}
R_M, R_T, R_G = lj(E3 / "ENSAIO_MUNDO_FALSO_v413.json"), lj(E3 / "TESTE_ETAPA3_SEM_CANDIDATO_v413.json"), lj(E3 / "ENSAIO_GUARDA_PRIVADA_v413.json")
R_A, R_H, R_D = lj(E3 / "ensaio_arvore" / "ENSAIO_ARVORE_v413.json"), lj(E3 / "ensaio_handoff" / "ENSAIO_HANDOFF_v413.json"), lj(E3 / "DERIVACAO_RITO_v413.json")
R_E = lj(E3 / "ensaio_entrega" / "ENTREGA_A_CUSTODIA_v413_ENSAIO.json")
viol_h = R_H["conferencia"] if R_H and isinstance(R_H.get("conferencia"), list) else []
so_blocos = all(str(x).startswith("TEXTO_PUBLICO_README_") for x in viol_h)
rec_sha = lambda p: sha(p)[:16] if Path(p).is_file() else None
ens = {
    "mundo_falso (esperados, instalador, simulacao do rito, conferidor, reversao)": {"recibo": "etapa3\\ENSAIO_MUNDO_FALSO_v413.json", "sha16": rec_sha(E3 / "ENSAIO_MUNDO_FALSO_v413.json"),
        "ok": bool(R_M and R_M["ok"]), "passos": len(R_M["passos"]) if R_M else 0, "passos_ok": sum(1 for x in R_M["passos"] if x["ok"]) if R_M else 0,
        "o_que": "Nos falso de copias da v412 selada (14 selados + 1920 do kernel); candidato sintetico (o um.py da v412 com os 21 novos e o corrigido do sandbox embutidos); esperados: 1 negativo + positivo; instalador: 5 negativos (recusam sem escrever) + positivo + 1 negativo depois de instalar; conferidor: positivo (35 checagens) + 7 mutacoes (cada uma reprova a checagem certa); reversao: 1 negativo (recusa sem escrever) + positivo (o Nos falso volta byte a byte); o mundo foi apagado"},
    "sem_candidato (vigia do pilar, laco do rito, portao do pilar, sh -n, diffs, guarda do titulo, esperados, compilacao)": {"recibo": "etapa3\\TESTE_ETAPA3_SEM_CANDIDATO_v413.json",
        "sha16": rec_sha(E3 / "TESTE_ETAPA3_SEM_CANDIDATO_v413.json"), "ok": bool(R_T and R_T["ok"]), "testes": len(R_T["testes"]) if R_T else 0,
        "testes_ok": sum(1 for x in R_T["testes"] if x["ok"]) if R_T else 0, "portao_do_pilar_de_hoje": (R_T or {}).get("portao_de_hoje")},
    "guarda_privada (positivo e negativo, so' contagens)": {"recibo": "etapa3\\ENSAIO_GUARDA_PRIVADA_v413.json", "sha16": rec_sha(E3 / "ENSAIO_GUARDA_PRIVADA_v413.json"), "ok": bool(R_G and R_G["ok"])},
    "arvore da prova (a linha da v413 numa copia do gerador, v412 dry)": {"recibo": "etapa3\\ensaio_arvore\\ENSAIO_ARVORE_v413.json", "sha16": rec_sha(E3 / "ensaio_arvore" / "ENSAIO_ARVORE_v413.json"),
        "ok": bool(R_A and R_A["ok"]), "gerador_sha16_antes": (R_A or {}).get("gerador_sha16_antes"), "gerador_sha16_depois_da_troca": (R_A or {}).get("gerador_sha16_depois_da_troca")},
    "compositor R2 (fatos sinteticos do Nos v412 com o rotulo v413; recibos B(n) sinteticos; os blocos REAIS da Etapa 2)": {"recibo": "etapa3\\ensaio_handoff\\ENSAIO_HANDOFF_v413.json",
        "sha16": rec_sha(E3 / "ensaio_handoff" / "ENSAIO_HANDOFF_v413.json"), "prosa_e_nota_limpas": bool(R_H) and so_blocos, "achados_nos_blocos_da_etapa_2": viol_h,
        "marcadores": len((R_H or {}).get("marcadores") or [])},
    "derivacao do rito e do carimbador (trocas contadas e diff)": {"recibo": "etapa3\\DERIVACAO_RITO_v413.json", "sha16": rec_sha(E3 / "DERIVACAO_RITO_v413.json"), "ok": bool(R_D)},
    "entrega a custodia (esquema do modelo)": {"recibo": "etapa3\\ensaio_entrega\\ENTREGA_A_CUSTODIA_v413_ENSAIO.json", "sha16": rec_sha(E3 / "ensaio_entrega" / "ENTREGA_A_CUSTODIA_v413_ENSAIO.json"), "ok": bool(R_E)},
}
pronto = {
    "contrato": "PRONTO_ETAPA3_v413", "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "agente": "construtor da Etapa 3 da v413, a servico da gerencia c1",
    "ordem": {"arquivo": "ORDEM_ETAPA_3_v413.md", "sha16": sha(V / "ORDEM_ETAPA_3_v413.md")[:16]},
    "pedido_da_custodia": {"arquivo": r"work\custodia_v413_preparo_20nov\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md",
                           "sha16": sha(Path(r"C:\IALD\Central de Patentes\work\custodia_v413_preparo_20nov\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md"))[:16]},
    "estado": "ETAPA 3 PREPARADA E ENSAIADA; NADA INSTALADO, O RITO NAO RODOU, O NOS NAO FOI TOCADO; PAROU AQUI",
    "etapa_3_fechou": all(x["ok"] for k, x in ens.items() if "ok" in x) and ens["compositor R2 (fatos sinteticos do Nos v412 com o rotulo v413; recibos B(n) sinteticos; os blocos REAIS da Etapa 2)"]["prosa_e_nota_limpas"],
    "scripts_sha16": scripts,
    "ensaios": ens,
    "depende_do_candidato": [
        "esperados_v413_foco.py: recusa (rc 2) ate' a Etapa 2 fechar (PREPARACAO_v413_PRONTA.json, CANDIDATO_v413.json, PORTAO_DO_PILAR_CANDIDATO_v413.json); le o caminho do candidato do fecho ou de --candidato",
        "instalar_v413.py: exige ESPERADOS_v413.json, TOPO_RATIFICADO_v413_DERIVADO.json e as exigencias da custodia NO candidato (_V413_FONTES, _V413_VERBATINS2, kh_n1_cobertura_v413; o contrato R1 nao os traz)",
        "rito_v413.sh: le candidato_sha16 do ESPERADOS; o portao do pilar le o ambiente do cache pelo ESPERADOS",
        "conferir_pos_rito_v413_foco.py, pos_rito\\diffs_v413.py, montar_handoff_e_linhagem_v413.py, pos_rito\\gerar_entrega_a_custodia_v413.py: depois do rito",
        "guarda_privada_v413.py --fase pre: sobre o candidato (o ensaio rodou so' sobre o um.py da v412 contra o espelho)",
        "montar_handoff_e_linhagem_v413.py: os blocos da Etapa 2 (BLOCOS_TEXTO_PUBLICO_v413.json, parametrizado por --blocos) tem de passar nas guardas (hoje: 5 achados)"],
    "depende_do_bn": [
        "ANTES da instalacao: o pre-selo do salto (bancada\\rodar_bn_pre_selo_v413.sh -> PINO_RECIBO_PRE_SELO_v413.json utilizavel, do um.py v412 do Nos); sem ele, o instalador recusa, salvo --sem-pre-selo-bn \"<motivo>\" (desvio gravado; o salto se perde)",
        "DEPOIS do selo e ANTES do compositor: bancada\\bn_v413.sh do 10 ao 11; os tres recibos (RECIBO_SINCRONIZACAO/PARADA/RELIGAMENTO_v413) em bancada_B3*\\ achados pela funcao da G1 (fatos.recibos_bn_resolvidos) e citados por sha16 no paragrafo «O elo B(n)»; sem eles, so' com decisoes\\BN_DISPENSADO_v413.json ou --bn-dispensado <fala por bytes>; a cadeia do pos-rito AGUARDA (rc 20) no passo 6",
        "a entrega (gerar_entrega_a_custodia_v413.py): estado da Bancada lido dos recibos; recusa com o B(n) aberto sem a decisao BN_DISPENSADO_v413 na lista"],
    "textos_que_o_pos_rito_regera": [
        "Nos\\A_PROVA_DA_QG_TGL_arvore.md (arvore_da_prova.py v413, com a linha das pedras da v413 posta no gerador da casa por adaptar_arvore_da_prova_v413.py --executar)",
        "cadeia_de_selo\\v413\\DIFF_v412_v413.diff, DIFF_KERNEL_v413.txt e DIFFS_v413_RECIBO.json (diffs_v413.py)",
        "Nos\\MEMORIA_DA_LINHAGEM.md (o bloco «v413 SELADA», no molde RE_CAB da G1)", "Nos\\DESENHO_DO_FECHAMENTO_QG.md (o adendo datado da v413)",
        "Nos\\HANDOFF_v413_CUSTODIA.md (por ultimo; 7 da prosa + NOTA_EN + os 46 ratificados e o README_H0DN verbatim + os blocos TEXTO_PUBLICO da Etapa 2) e RECIBO_HANDOFF_v413.json",
        "memory\\TGL_INDICE_VIVO.md e os blocos do TGL_ATLAS.md (atlas_indice.py v413) e a porta da memoria (porta_memoria.py): so' com CHAIN_SUPERFICIES=sim (ato da gerencia)",
        "a mao (gerencia): a linha do MEMORY.md pela fila; os blocos core_v413_selada e haja_luz_v413_selada; e por ultimo cadeia_de_selo\\v413\\ENTREGA_A_CUSTODIA_v413.json (gerar_entrega_a_custodia_v413.py)",
        "a guarda que recusa .md declarado com a versao de outro selo no titulo: pos_rito\\guarda_titulo_versao_v413.py (a regra do E03 da G1 sobre espelho_pares.DECLARADOS, mais a arvore e o handoff com a versao do selo), antes e depois do compositor"],
    "achados_para_a_etapa_2_e_a_gerencia": [
        "a pagina R0 (secao 2, primeira frase) e os blocos TEXTO_PUBLICO_README_PT_PNP e _EN_PNP: F37b da guarda herdada (_v412_guarda_frases -> _v409): «P = nP» e «Turing» na mesma frase sem «relativo ao leitor» nem negacao (a Etapa 2 ja' registra «a pagina pinada falha a guarda» no ETAPA_2_ESTADO_v413.json)",
        "os blocos EN ACRESCENTA, FRONTEIRA e CONSCIENCIA: «proved» sem estatuto na mesma frase (custodia_g1.textos.portao, regra 2); o PT usa «provado», que a regra nao le",
        "o contrato R1 nao traz o registro kh_n1_cobertura_v413 nem o par _V413_FONTES/_V413_VERBATINS2 que a custodia pede (pedido de 20/11, secao 2.1); o instalador recusa sem eles (corrigir no candidato antes do rito)",
        "o gerador da arvore da prova (cadeia_de_selo\\arvore_da_prova.py) nao tem linhas das versoes v393 a v412; a Etapa 3 so' acrescenta a da v413 (nao reescreve historia)",
        "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md (Etapa 2) traz a NOTA_EN da v412 verbatim (o texto diz «Status that goes with v412»): a NOTA e' da versao e o compositor a regera para a v413; os outros 33 marcadores em comum sao identicos, byte a byte, aos que o compositor le do handoff selado da v412 (conferencia cruzada no proprio compositor)",
        "a tarefa agendada pos-treino aponta para orquestrador\\pos_treino_v413.py, que nao existe (PRONTO_PARA_CANDIDATO_v413.json); fora desta etapa"],
    "desvios_e_por_que": [
        "rito_v413.sh: sai a leitura da VRAM (nvidia-smi) e as recusas 11/12 do molde: com o treino na placa elas sempre recusariam e a ordem manda nao medir; no lugar, o PORTAO DO PILAR antes de qualquer parada (19/21) e o VIGIA DO PILAR durante (para o rito na linha de calculo); a parada do servidor do modelo nativo so' age se ele estava ligado",
        "instalar_v413.py/reverter_v413.py: os backups passam a ser TODO o conjunto pinado pelo selo da v412 (14), o selo, o sidecar, os .txt pt/en, a raiz, o Audit e o corrigido (21; o molde guardava 10): a reversao devolve o selado inteiro, conferido contra o selo",
        "instalar_v413.py: as pedras anteriores sao conferidas pelo manifesto do kernel pinado pelo selo (1920 arquivos, nenhum nome digitado), no lugar da lista digitada do molde; trava nova: as exigencias da custodia no candidato; o pre-selo do B(n) volta a ser trava (o molde da v412 o tirou como desvio), com --sem-pre-selo-bn como desvio declarado e gravado",
        "montar_handoff_e_linhagem_v413.py: os textos ratificados vem dos marcadores _v412 do HANDOFF_v412_CUSTODIA.md (o VITRINE_RATIFICADA_v411.json foi retirado pela custodia em 19/11), conferidos verbatim contra o arquivo retirado; a guarda de frases herdada passa sobre a prosa nova, a NOTA e os blocos, e, dentro da NOTA, a linha do estatuto ratificada (com o termo do resultado) fica com as regras da G1 que a conhecem (h0dn.conferir_bloco), nao com a F65/F67 do programa, anterior ao termo; a prosa nova segue o metodo de 17/11 (sem historia; o v412 dizia quem aprovou e a ordem do autor)",
        "os blocos core_v413_selada/haja_luz_v413_selada e a linha do MEMORY.md ficam a mao (memoria e' ato da gerencia; os blocos dependem dos fatos da publicacao)",
        "erro meu, sem efeito: uma chamada solta de `python -` (stdin /dev/null) travou numa linha de comando da ferramenta; parada pela propria ferramenta; nada foi gravado por ela"],
    "nada_foi_tocado": "o Nos (so' lido), C:\\t\\k413c (so' lido: o sandbox), as pastas da v412 (so' lidas), os arquivos da Etapa 2 e do B(n) (so' lidos), o gerador da arvore da casa (so' lido: o ensaio foi numa copia), a memoria, o Atlas, a ACOM e o Mapa; a placa de video e o treino nao foram usados nem medidos (o portao le metadados de pacote e o nome do dispositivo pelo Windows)",
    "examinado_para_o_mapa": {"olhou_dados": False, "rotas_sugeridas": ["v413.etapa3.preparo (instalar/reverter/rito/conferidor/pos-rito/handoff/entrega)", "v413.etapa3.portao_do_pilar_sem_tocar_a_placa", "v413.etapa3.guarda_titulo_e_arvore"],
                              "nao_refazer": "os diffs reproduzem os da v412 byte a byte; o mundo falso (25 passos) e os testes sem candidato (16) ficam como regressao desta etapa"},
    "estatuto": "[REAL] medido nos ensaios desta pasta; nada instalado; o rito nao rodou; validade no kernel nao e' creditacao; o gate nao se move",
}
out = V / "PRONTO_ETAPA3_v413.json"
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
b = json.dumps(pronto, ensure_ascii=False, indent=1).encode("utf-8"); tmp = out.with_name(out.name + ".tmp"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, out)
print("PRONTO_ETAPA3_v413.json | etapa_3_fechou=%s | scripts %d | sha16 %s" % (pronto["etapa_3_fechou"], len(scripts), hashlib.sha256(b).hexdigest()[:16]))
