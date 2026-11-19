# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: lista, por modulo das pedras congeladas (insumos\\pedras), as declaracoes theorem/lemma e marca as que
a docstring traz com estrela. Serve de proposta de ancoras para os registros por especificacao da v412. So le as fontes; grava
insumos\\ANCORAS_PROPOSTAS_v412.json. Uso: ancoras_propostas_v412.py [--executar]"""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
man = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R9.json").read_text(encoding="utf-8"))
REG = {  # a qual registro por especificacao cada modulo responde (proposta da gerencia; contrato, secao 2)
    "iald_camada_cientifica_v412": ["CamadaCientifica", "MinimoFuncionalDeEnergia", "OLeitorEALei", "AContagemEACarga", "AMaquinaEALeitura",
                                    "OPassoEORetorno", "OHabitanteDoNome", "NomeComoCodigo", "CopiadorEImpostor",
                                    "OTempoEACauda", "AFitaEACauda", "AMedidaEOIf", "AEsperancaEOIf",
                                    "Token2", "AMaquina",
                                    "OPassoEOFim", "OPsibitEACompressao"],   # (oitava lista, 17/11)   # (sexta lista, 17/11: as duas pedras novas da frente A)
    "matematica_que_restava_v412": ["ErgodicidadeDeMautner", "T1GaussianSpectrum", "T1CompostoFinito", "T1PontesAoKernel", "MontagemDasGamas",
                                    "BoostEDissipador", "OParFixaORelogio", "OHamiltonianoOcultoEOCusto", "OTestemunhoDeTakesakiEmCasa", "TipoIIIControles", "TipoIIIUmSoBoost", "Classificacao", "FockCharacters",
                                    "ObserverClassification", "PhysicalCoreCenter", "PhysicalCoreFactor", "PhysicalCoreMultipliers", "TowerWedgeIndex",
                                    "TransportCenter", "TransportPair", "VinculoCriterion", "WedgeFactor", "WedgeHorizonObserver", "ProdutoFinito",
                                    "ProdutoTresUm", "ConjugacaoFinita", "SpinorToSolder"],
    "leitor_da_formula_v412": ["ACurvaEAEstado", "AFronteiraEOUnicoPortao", "AParedeDoNome", "ARecusaTemConteudo", "AtalhosNaFita", "AtualizaONome", "BlocosIndependentes", "BuscaEmCruzamentos", "CacheDeRamos", "CadeiaNaFita", "CadeiasDeBolsas", "CamadaAlcancada", "CanalDaClausula", "CapacidadeDosRotulos", "CaudaDisjunta", "ChecagemHorn", "CircuitoNaFita", "ClausulaComoResposta", "ClausulaNoSeparador", "CoberturaAfin", "CompilaHornNaFita", "ConsultaPonderada", "ConsultasRotuladas", "ConteudoNaFita", "CorrelacoesDistintas", "CorteDosPares", "CorteDosParesCruzados", "CorteDosParesIntercalados", "CruzamentosUniversais", "CustoDaBuscaLiteral", "CustoDaFaseDensa", "CustoDaTabela", "CustoDoPlano", "DesafioNaFitaOriginal", "DespachoDeReuso", "DivisaoUniforme", "DuasPassagens", "DuasPontasLivres", "EcoDaAtribuicao", "EliminacaoDePares", "EscolhasGlobais", "FatoresCruzados", "FatoresIndependentes", "FechoNaFita", "FitaComCusto", "FitaCruzada", "FitaDeUmaCabeca", "FitaDoResiduo", "FitaHornEsparsa", "FitaPlanaAnterior", "FronteiraDeTresLiterais", "GuardaDoPerfil", "GuardasNaFita", "HandshakeDoNome", "ImplicacoesCruzadas", "InformacaoDoResumo", "LeitorDaFamilia", "LeitorDaFormula", "LeitorDeReuso", "LeitorGlobal", "LeituraCertificada", "LeituraComReuso", "LeituraDosPares", "LeituraIntegrada", "LeiturasComFolga", "LimiteDasProjecoes", "LimiteDoCacheExplicito", "LimiteDoLeitor", "LimiteDoReuso", "LocalizaARecusa", "MascarasDistintas", "MovimentosDoPlano", "OPsiBitDaFormula", "OResumoEPsiBit", "ObrigacoesJaSatisfeitas", "PalavrasResiduais", "ParPonderado", "ParesIndependentes", "PerfilDeSinais", "PlanoDaFormula", "PolinomioDoPsiBit", "PolinomioPorEscolha", "PontePalavraVerbo", "PrecisaoDaChave", "ProjecaoDaFronteira", "PsiBitNaFronteira", "Reagrupar", "RedeComoCNF", "RedesDeCadeias", "ReguaNaFita", "RelacaoEmFase", "RelacaoFronteira", "RestricaoGlobal", "RotulosAfins", "RotulosCompartilhados", "SegundaLeitura", "SeletorCompartilhado", "TamanhoDoEco", "TrabalhoPorCorte", "TransicaoDaFronteira", "TransicaoPorConsulta", "TransporteDaInscricao", "UmaChaveAngular", "VerboNaFita", "sonda_cadeia_caminho", "sonda_n0_contraexemplo"],   # (nona lista, 18/11: a frente C)
}
de = {m: r for r, ms in REG.items() for m in ms}
pad = re.compile(r"^[ \t]*(?:@\[[^\]\n]*\][ \t]*\n?[ \t]*)*(?:(?:private|protected|noncomputable)[ \t]+)*(?:theorem|lemma)[ \t]+([^\s:({\[]+)", re.M)
doc = re.compile(r"/--(?:(?!-/).)*?-/", re.S)
saida, tot, est = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "nota": "lido das fontes congeladas; proposta de ancoras: as declaracoes com estrela na docstring; para modulos sem estrela, todas ficam listadas e a escolha e' do contrato",
                   "manifesto_sha256": hashlib.sha256((V / "insumos" / "MANIFESTO_PEDRAS_v412_R9.json").read_bytes()).hexdigest(), "registros": {}}, 0, 0
sem_registro = []
for it in man["modulos"]:
    nome = it["modulo"]; t = (V / "insumos" / "pedras_r9" / (nome + ".lean")).read_text(encoding="utf-8")
    ns = it["namespaces"][0] if it["namespaces"] else ""
    decls, fim_ant = [], 0
    for m in pad.finditer(t):
        entre = t[fim_ant:m.start()]          # o que ha' entre a declaracao anterior e esta: a docstring dela, se houver, e' a ultima
        ds = doc.findall(entre)
        d_ = ds[-1] if ds and entre.rstrip().endswith("-/") or (ds and re.search(r"-/\s*(?:omit[^\n]*\n\s*)?$", entre)) else ""
        decls.append({"nome": m.group(1), "estrela": "\u2605" in d_})
        fim_ant = m.end()
    # (a contagem do manifesto so' ve^ declaracoes na coluna zero e sem modificador; a daqui e' a que vale como proposta; a contagem
    #  oficial e' a do relatorio de axiomas do sandbox)
    r = de.get(nome)
    if r is None:
        sem_registro.append(nome); continue
    saida["registros"].setdefault(r, []).append({"modulo": nome, "namespace": ns, "de_quem": it["de_quem"], "n_declaracoes": len(decls),
                                                  "com_estrela": [d["nome"] for d in decls if d["estrela"]], "sem_estrela": [d["nome"] for d in decls if not d["estrela"]],
                                                  "listadas_em_print_axioms": [x.split(".")[-1] for x in re.findall(r"^#print axioms\s+(\S+)", t, flags=re.M)]})
    tot += len(decls); est += sum(d["estrela"] for d in decls)
    print(r[:28].ljust(28), nome.ljust(26), "decl", str(len(decls)).rjust(3), "| com estrela", sum(d["estrela"] for d in decls))
assert not sem_registro, sem_registro
print("total de declaracoes:", tot, "| com estrela:", est)
if "--executar" not in sys.argv:
    print("ENSAIO A SECO: nada gravado."); sys.exit(0)
out = V / "insumos" / "ANCORAS_PROPOSTAS_v412_R9.json"
tmp = out.with_suffix(".json.tmp_c1"); tmp.write_bytes(json.dumps(saida, ensure_ascii=False, indent=1).encode("utf-8"))
if out.exists():
    out.replace(out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")))
tmp.replace(out)
print("gravado:", out, "| sha16", hashlib.sha256(out.read_bytes()).hexdigest()[:16])
