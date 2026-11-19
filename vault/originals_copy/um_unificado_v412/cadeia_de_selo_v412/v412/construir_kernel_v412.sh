#!/bin/sh
# Constroi o kernel do SANDBOX da v412 (C:\t\k412c\final; NUNCA o do Nos). Gerado por preparar_bundle_v412.py (claude-construtor-v412) em 20261118_221312; nao editar a mao (regerar pelo preparo).
# Molde: v410\construir_kernel_v410.sh. Diferenca: os 156 modulos novos sao construidos UM A UM, na ordem topologica das dependencias (`lake build +<modulo>`), e o script PARA no
# primeiro que nao compilar (marca `parou_em=` e nao roda o resto nem o Audit); so' depois vem o `lake build` inteiro (a raiz e o TGL.Audit) e o Audit (`lake env lean TGL/Audit.lean`).
# O build e' INCREMENTAL no que e' antigo (o kernel da v411 ja compilado em .lake/build, copiado do k411c) e A FRIO nos modulos novos. Marcas em kernel/construir_marcas.txt.
K="/c/t/k412c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412/kernel"
LAKE=/c/Users/rotol/.elan/bin/lake
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log construir_marcas.txt; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
: > "$D/lake_build.log"
rb=0
for m in TGLExt.CamadaCientifica TGLExt.MinimoFuncionalDeEnergia TGLExt.OLeitorEALei TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura TGLExt.OPassoEORetorno TGLExt.OHabitanteDoNome TGLExt.NomeComoCodigo TGLExt.CopiadorEImpostor TGLExt.OTempoEACauda TGLExt.AFitaEACauda TGLExt.AMedidaEOIf TGLExt.AEsperancaEOIf TGLExt.ErgodicidadeDeMautner TGLExt.T1GaussianSpectrum TGLExt.T1CompostoFinito TGLExt.T1PontesAoKernel TGLExt.MontagemDasGamas TGLExt.BoostEDissipador TGLExt.OParFixaORelogio TGLExt.OHamiltonianoOcultoEOCusto TGLExt.OTestemunhoDeTakesakiEmCasa TGLExt.FockCharacters TGLExt.PhysicalCoreCenter TGLExt.PhysicalCoreMultipliers TGLExt.PhysicalCoreFactor TGLExt.TowerWedgeIndex TGLExt.TipoIIIUmSoBoost TGLExt.WedgeFactor TGLExt.WedgeHorizonObserver TGLExt.TransportCenter TGLExt.VinculoCriterion TGLExt.Classificacao TGLExt.TransportPair TGLExt.ObserverClassification TGLExt.TipoIIIControles TGLExt.ProdutoFinito TGLExt.ProdutoTresUm TGLExt.ConjugacaoFinita TGLExt.SpinorToSolder TGLExt.Token2 TGLExt.AMaquina TGLExt.OPassoEOFim TGLExt.OPsibitEACompressao TGLExt.AFitaEOIndice TGLExt.LeitorDaFormula TGLExt.CorrelacoesDistintas TGLExt.CorteDosPares TGLExt.CorteDosParesCruzados TGLExt.InformacaoDoResumo TGLExt.AParedeDoNome TGLExt.LeiturasComFolga TGLExt.OCustoEAIsometria TGLExt.OPolinomioFixoEBeta TGLExt.ORazaoDoColapsoEBeta TGLExt.OResumoEPsiBit TGLExt.AClausulaExemplificativa TGLExt.AFronteiraEOUnicoPortao TGLExt.DivisaoUniforme TGLExt.OPsiBitDaFormula TGLExt.ACurvaEAEstado TGLExt.CorteDosParesIntercalados TGLExt.ImplicacoesCruzadas TGLExt.EscolhasGlobais TGLExt.FitaHornEsparsa TGLExt.FechoNaFita TGLExt.OSeparadorNoPercurso TGLExt.PalavrasResiduais TGLExt.ParPonderado TGLExt.ParesIndependentes TGLExt.CruzamentosUniversais TGLExt.BuscaEmCruzamentos TGLExt.PolinomioPorEscolha TGLExt.ChecagemHorn TGLExt.CompilaHornNaFita TGLExt.GuardasNaFita TGLExt.PontePalavraVerbo TGLExt.FitaComCusto TGLExt.CadeiasDeBolsas TGLExt.ClausulaComoResposta TGLExt.FitaCruzada TGLExt.ProjecaoDaFronteira TGLExt.Reagrupar TGLExt.RedesDeCadeias TGLExt.FitaDeUmaCabeca TGLExt.RedeComoCNF TGLExt.RelacaoEmFase TGLExt.RelacaoFronteira TGLExt.CustoDaTabela TGLExt.PsiBitNaFronteira TGLExt.ConsultasRotuladas TGLExt.ConsultaPonderada TGLExt.MascarasDistintas TGLExt.RestricaoGlobal TGLExt.CaudaDisjunta TGLExt.AtalhosNaFita TGLExt.BlocosIndependentes TGLExt.FitaDoResiduo TGLExt.CircuitoNaFita TGLExt.LeitorGlobal TGLExt.AtualizaONome TGLExt.LimiteDasProjecoes TGLExt.LimiteDoCacheExplicito TGLExt.FatoresIndependentes TGLExt.ClausulaNoSeparador TGLExt.ARecusaTemConteudo TGLExt.HandshakeDoNome TGLExt.PerfilDeSinais TGLExt.CustoDaBuscaLiteral TGLExt.CacheDeRamos TGLExt.DuasPassagens TGLExt.EcoDaAtribuicao TGLExt.EliminacaoDePares TGLExt.FronteiraDeTresLiterais TGLExt.GuardaDoPerfil TGLExt.LocalizaARecusa TGLExt.ObrigacoesJaSatisfeitas TGLExt.CapacidadeDosRotulos TGLExt.PlanoDaFormula TGLExt.CustoDoPlano TGLExt.LeituraIntegrada TGLExt.LeitorDaFamilia TGLExt.LeituraDosPares TGLExt.CadeiaNaFita TGLExt.ConteudoNaFita TGLExt.MovimentosDoPlano TGLExt.LimiteDoLeitor TGLExt.PrecisaoDaChave TGLExt.CustoDaFaseDensa TGLExt.RotulosAfins TGLExt.CoberturaAfin TGLExt.RotulosCompartilhados TGLExt.FatoresCruzados TGLExt.SegundaLeitura TGLExt.LeitorDeReuso TGLExt.LeituraCertificada TGLExt.DespachoDeReuso TGLExt.CamadaAlcancada TGLExt.LimiteDoReuso TGLExt.LeituraComReuso TGLExt.ReguaNaFita TGLExt.SeletorCompartilhado TGLExt.TamanhoDoEco TGLExt.TrabalhoPorCorte TGLExt.TransicaoDaFronteira TGLExt.TransicaoPorConsulta TGLExt.TransporteDaInscricao TGLExt.CanalDaClausula TGLExt.DesafioNaFitaOriginal TGLExt.UmaChaveAngular TGLExt.DuasPontasLivres TGLExt.VerboNaFita TGLExt.FitaPlanaAnterior TGLExt.PolinomioDoPsiBit TGLExt.sonda_cadeia_caminho TGLExt.sonda_n0_contraexemplo; do
  t0=$(date +%s)
  echo "=== MODULO $m (inicio $(date '+%H:%M:%S'))" >> "$D/lake_build.log"
  $LAKE build "+$m" >> "$D/lake_build.log" 2>&1; r=$?
  echo "modulo=$m rc=$r s=$(( $(date +%s) - t0 ))" >> "$D/construir_marcas.txt"
  if [ "$r" != "0" ]; then rb=$r; echo "parou_em=$m" >> "$D/construir_marcas.txt"; break; fi
done
if [ "$rb" = "0" ]; then
  echo "=== BUILD INTEIRO (inicio $(date '+%H:%M:%S'))" >> "$D/lake_build.log"
  $LAKE build >> "$D/lake_build.log" 2>&1; rb=$?
fi
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ]; then
  $LAKE env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
else
  ra=99; echo "o Audit NAO rodou: o build parou (rc_build=$rb)" > "$D/audit.log"
fi
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
