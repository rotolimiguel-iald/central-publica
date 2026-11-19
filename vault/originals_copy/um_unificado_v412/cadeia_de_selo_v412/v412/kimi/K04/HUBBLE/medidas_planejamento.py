import json
import math
from pathlib import Path

# Planejamento sobre agregados publicados. Nenhum vetor observado é lido;
# nenhum Z, razão H0_local/H0_fundo ou veredito observado é calculado.
K_MINUS_1 = 0.0838071748529643  # REVISAO_K01.md, tabela de contas, K-1
BG1_H0 = 68.53
BG1_SIGMA = 0.30
D90 = 6.281551565544601
SIGMA_BG_REL = BG1_SIGMA / BG1_H0

# Valores documentais lidos pela revisão distinta; não recalculados nesta rodada.
H0DN_CORE = {
    "fonte": "core.h0dn_bg1_v411.values",
    "primario": {"D": 6.710, "campo": "values.primario.D", "estatuto": "já lido; não cego; não independente"},
    "cefeidas_livres": {"D": 5.191, "campo": "values.cefeidas_livres.D", "estatuto": "variante já lida; não nova abertura"},
    "conta_de_bolso": {
        "baseline": {"insumo": "73,50 ± 0,81; BG1 0,30/68,53", "D": 7.067538789321352},
        "v99": {"insumo": "73,994 ± 0,697; BG1 0,30/68,53", "D": 8.068302253267012},
        "estatuto": "planejamento com erros de cabeçalho; não substitui o modelo de erros do core",
    },
}

RG = {"masers_pesce", "masers_reanalysis", "tdcosmo2025", "tdcosmo_xxv", "tdcosmo2026", "tdcosmo2026_all", "tdcosmo_approved", "tdcosmo_40_200"}
RH = {"sirens_gwtc4", "sirens_gwtc5"}
SEM_PONTE = {"sn2_vogl", "sn2_dejaeger", "sz_colago", "frb_local", "frb_pseudo", "frb_2026", "frb_126", "frb_500", "bbh_agn", "bbh_agn_extended", "bbh_agn_planck", "bbh_agn_shoes", "sn_encore"}

EMPILHAMENTO_REVISOR = {
    "estatuto": "[DERIVED pelo revisor — PLANEJAMENTO] não cego, não independente, não composto aberto; não somar à Fase 9 V2",
    "duas_linhas": {"linhas": ["sn2_vogl", "tdcosmo2026"], "D_so_stat": 4.04, "D_sn2_sistematica_igual_estatistica": 3.36, "ja_na_fase9_v2": ["TDCOSMO"], "fracao_de_linhas_ja_na_v2": "1/2"},
    "cinco_linhas": {"linhas": ["sn2_vogl", "tdcosmo2026", "masers_reanalysis", "frb_local", "bbh_agn_extended"], "D_so_stat": 5.34, "D_sn2_sistematica_igual_estatistica": 4.88, "ja_na_fase9_v2": ["TDCOSMO", "masers"], "fracao_de_linhas_ja_na_v2": "2/5", "fora_da_v2": ["SN II", "FRB", "BBH–AGN"]},
}

records = [
    dict(id="h0dn_baseline", metodo="H0DN baseline", h0=73.50, sigma=0.81, fonte="arXiv:2510.23823; DOI 10.1051/0004-6361/202557993", inclusao="H0DN baseline; não é um dos cinco leitores F9", calendario="Já público; nenhuma próxima liberação datada localizada", nota="Composto atual, não independente nem cego"),
    dict(id="h0dn_all", metodo="H0DN V99 todos os estimadores", h0=73.994, sigma=0.697, fonte="arXiv:2510.23823; DOI 10.1051/0004-6361/202557993", inclusao="H0DN V99; não F9", calendario="Já público; sem data de sucessora localizada", nota="V99: a própria fonte recomenda não usar para análise posterior"),
    dict(id="sh0es_jwst", metodo="SH0ES JWST 19 hosts", h0=73.49, sigma=0.93, fonte="arXiv:2509.01667", inclusao="H0DN e F9 R25", calendario="Já público", nota="Não independente"),
    dict(id="sh0es_trgb", metodo="SH0ES + 35 calibrações TRGB", h0=73.18, sigma=0.88, fonte="arXiv:2509.01667", inclusao="H0DN e F9 R25", calendario="Já público", nota="Não independente; TRGB compartilha calibração"),
    dict(id="cchp_trgb", metodo="CCHP TRGB HST+JWST", h0=70.39, sigma=math.sqrt(1.22**2 + 1.33**2 + 0.70**2), fonte="arXiv:2408.06153; DOI 10.3847/1538-4357/adce78", inclusao="H0DN e F9", calendario="Já público; mais JWST sem data de H0", nota="Não independente"),
    dict(id="sbf_trgb", metodo="TRGB–SBF III", h0=73.8, sigma=math.sqrt(0.7**2 + 2.3**2), fonte="arXiv:2502.15935; DOI 10.3847/1538-4357/addfd6", inclusao="H0DN e F9", calendario="GO-5989 e futura amostra sem data de H0; meta 1 % no programa", nota="Não independente; mesma âncora NGC4258"),
    dict(id="masers_pesce", metodo="MCP XIII, seis masers", h0=73.9, sigma=3.0, fonte="arXiv:2001.09213", inclusao="H0DN e F9", calendario="Já público", nota="F9 usa cinco sem NGC4258 no decisório e seis ao lado"),
    dict(id="masers_reanalysis", metodo="Reanálise MCP, cinco masers", h0=71.6, sigma=3.7, fonte="arXiv:2609.17684", inclusao="Não estava na F9; MCP entra H0DN", calendario="Já público; futura alta cadência sem data de H0", nota="σ só estatística; mesmas cinco galáxias, outro modelo"),
    dict(id="sn2_vogl", metodo="SN II tailored EPM", h0=74.9, sigma=1.9, fonte="arXiv:2411.04968; DOI 10.1051/0004-6361/202452910", inclusao="H0DN variante astrofísica; não F9", calendario="Dados dedicados futuros sem data", nota="σ só estatística; sistemática declarada comparável ou menor"),
    dict(id="sn2_dejaeger", metodo="SN II standardized candle", h0=75.4, sigma=math.sqrt(3.8**2 + 1.5**2), fonte="arXiv:2203.08974; DOI 10.1093/mnras/stac1661", inclusao="H0DN baseline empírica e variantes; não F9", calendario="Já público", nota="σ stat+sys; não é EPM de um passo"),
    dict(id="tdcosmo2025", metodo="TDCOSMO-2025", h0=71.6, sigma=3.9, fonte="arXiv:2506.03023", inclusao="F9; não é escada H0DN", calendario="Já público", nota="Usa prior Ωm Pantheon+"),
    dict(id="tdcosmo_xxv", metodo="TDCOSMO XXV J1433+6007", h0=73.2, sigma=4.8, fonte="arXiv:2604.14145; DOI 10.1103/PhysRevD.114.063509", inclusao="Nova em 2026; entra TDCOSMO-2026", calendario="Já público", nota="Uma lente; análise cega pela colaboração"),
    dict(id="tdcosmo2026", metodo="TDCOSMO-2026, 11 lentes", h0=71.1, sigma=2.4, fonte="arXiv:2610.14781v2 e 2610.14881v2", inclusao="Não estava na F9; não H0DN", calendario="Já público; ciclos 4/5 JWST prevêem 1,5 %, sem data de liberação", nota="Cega pela colaboração; oito lentes já eram da Fase 2025"),
    dict(id="tdcosmo2026_all", metodo="TDCOSMO-2026 + SLACS + SL2S", h0=71.3, sigma=2.2, fonte="arXiv:2610.14781v2", inclusao="Não estava na F9; não H0DN", calendario="Já público; 1,5 % previsto sem data", nota="Precisão 3,0 %; mesma ressalva de continuidade"),
    dict(id="sirens_gwtc4", metodo="GWTC-4.0, dark+bright", h0=76.6, sigma=13.0, fonte="arXiv:2509.04348v2", inclusao="Fase 3/F9 sirenes; não H0DN", calendario="Já público", nota="Histórico, superado por GWTC-5.0"),
    dict(id="sirens_gwtc5", metodo="GWTC-5.0, 235 dark + GW170817", h0=71.0, sigma=9.0, fonte="arXiv:2605.27227v2", inclusao="Não estava na F9; não H0DN", calendario="Já público; GWTC-6.0 sem data/previsão de σ", nota="25,7 % mais preciso que GWTC-4.0, ainda ∼11 %"),
    dict(id="sz_colago", metodo="SZ/raios X + Pantheon", h0=67.2, sigma=6.1, fonte="arXiv:2310.18711v2", inclusao="Não H0DN nem F9", calendario="Já público; sem previsão de σ/data", nota="Distância SZ direta, mas H0 usa SNe não ancoradas"),
    dict(id="frb_local", metodo="108 FRBs localizados", h0=69.40, sigma=2.14, fonte="arXiv:2410.03994; DOI 10.1051/0004-6361/202453006", inclusao="Não H0DN nem F9", calendario="∼500 localizados projeta ∼1 % estatístico, sem data", nota="σ só estatística; f_IGM domina"),
    dict(id="frb_pseudo", metodo="527 FRBs não localizados, pseudo-z", h0=68.81, sigma=0.68, fonte="arXiv:2410.03994; DOI 10.1051/0004-6361/202453006", inclusao="Não H0DN nem F9", calendario="Não confundir com 500 localizados reais", nota="Nominal apenas; pseudo-z e f_IGM impedem qualificação"),
    dict(id="frb_2026", metodo="2124 FRBs não localizados, CHIME II", h0=69.0, sigma=17.0, fonte="arXiv:2604.03769v2", inclusao="Não H0DN nem F9", calendario="Já público; degenerescência residual 9 %", nota="22 %; não melhora a linha de 2025"),
    dict(id="bbh_agn", metodo="13 BBH–AGN, Run 1 agnóstico", h0=70.50, sigma=math.sqrt(3.37**2 + 1.56**2), fonte="arXiv:2607.03672v2", inclusao="Não H0DN nem F9", calendario="Já público; amostra futura sem data", nota="4,4 % de precisão estatística publicada; D usa stat+cal em quadratura"),
    dict(id="bbh_agn_extended", metodo="13 BBH–AGN + Bom + GW170817", h0=69.71, sigma=math.sqrt(2.55**2 + 1.54**2), fonte="arXiv:2607.03672v2", inclusao="Não H0DN nem F9", calendario="Já público; amostra futura sem data", nota="3,5 % de precisão publicada; D usa stat+cal em quadratura"),
    dict(id="bbh_agn_planck", metodo="BBH–AGN, âncora Planck", h0=67.62, sigma=0.72, fonte="arXiv:2607.03672v2", inclusao="Não H0DN nem F9", calendario="Já público; âncora escolhida, não independente", nota="Nominal apenas: recupera a âncora por construção"),
    dict(id="bbh_agn_shoes", metodo="BBH–AGN, âncora SH0ES", h0=72.91, sigma=0.72, fonte="arXiv:2607.03672v2", inclusao="Não H0DN nem F9", calendario="Já público; âncora escolhida, não independente", nota="Nominal apenas: recupera a âncora por construção"),
    dict(id="sn_encore", metodo="SN Encore, MACS J0138−2155", h0=66.9, sigma=11.2, fonte="arXiv:2509.12301; DOI 10.3847/1538-4357/ae3159", inclusao="Não H0DN nem F9; fora do composto", calendario="Já público; futuras imagens podem levar a 2–3 %", nota="Incerteza dominada pelo atraso; não cruza limiares"),
    dict(id="frb_126", metodo="126 FRBs/118 após cortes, modelo VII NE2001", h0=71.36, sigma=3.94, fonte="DOI 10.3389/fspas.2026.1753671", inclusao="Não H0DN nem F9", calendario="Publicado 12/08/2026; 500 simulados projeta 1,2 %, sem data", nota="5,5 % estatística; diferenças Galácticas NE2001/YMW16"),
]

forecasts = [
    dict(id="tdcosmo_approved", metodo="TDCOSMO JWST-GO-7184/9637", sigma_rel=0.015, fonte="arXiv:2610.14881v2, §V", calendario="Ciclos 4/5 aprovados; sem data de liberação", nota="Previsão 1,5 %: cruza 5σ, não D90"),
    dict(id="tdcosmo_40_200", metodo="TDCOSMO 40 atrasos + 200 sem atrasos", sigma_rel=0.012, fonte="arXiv:2008.06157", calendario="Forecast sem data", nota="Previsão 1,2 %: cruza D90"),
    dict(id="sbf_goal", metodo="SBF Coma e Hubble flow", sigma_rel=0.01, fonte="JWST-GO-5989; arXiv:2502.15935", calendario="Meta do programa, sem data de H0", nota="Meta 1 %, não forecast de publicação"),
    dict(id="frb_500", metodo="∼500 FRBs localizados", sigma_rel=0.01, fonte="arXiv:2410.03994; DOI 10.1051/0004-6361/202453006", calendario="Sem taxa/data; exige f_IGM e sistemáticas resolvidos", nota="∼1 % estatístico apenas"),
]


PUBLICADO = {
    "h0dn_baseline": "73,50 ± 0,81",
    "h0dn_all": "73,994 ± 0,697 (0,942 %)",
    "sh0es_jwst": "73,49 ± 0,93",
    "sh0es_trgb": "73,18 ± 0,88",
    "cchp_trgb": "70,39 ± 1,22 (stat) ± 1,33 (sys) ± 0,70 (SN)",
    "sbf_trgb": "73,8 ± 0,7 (stat) ± 2,3 (sys)",
    "masers_pesce": "73,9 ± 3,0",
    "masers_reanalysis": "71,6 ± 3,7 (stat)",
    "sn2_vogl": "74,9 ± 1,9 (stat)",
    "sn2_dejaeger": "75,4 +3,8/−3,7 (stat) ± 1,5 (sys)",
    "tdcosmo2025": "71,6 +3,9/−3,3",
    "tdcosmo_xxv": "73,2 +4,8/−4,7",
    "tdcosmo2026": "71,1 +2,4/−2,3",
    "tdcosmo2026_all": "71,3 +2,2/−2,1",
    "sirens_gwtc4": "76,6 +13,0/−9,5",
    "sirens_gwtc5": "71,0 +9,0/−7,1",
    "sz_colago": "67,2 ± 6,1",
    "frb_local": "69,40 +2,14/−1,97 (stat)",
    "frb_pseudo": "68,81 ± 0,68 (stat; pseudo-z)",
    "frb_2026": "69 +17/−15",
    "bbh_agn": "70,50 +3,37/−2,89 (stat) ± 1,56 (cal); 4,4 %",
    "bbh_agn_extended": "69,71 +2,55/−2,40 (stat) ± 1,54 (cal); 3,5 %",
    "bbh_agn_planck": "67,62 ± 0,72; 1,1 %, ancorada Planck",
    "bbh_agn_shoes": "72,91 ± 0,72; 1,0 %, ancorada SH0ES",
    "sn_encore": "66,9 +11,2/−8,1",
    "frb_126": "71,36 −3,94/+3,59; 5,5 %",
}

STAT_ONLY = {"masers_reanalysis", "sn2_vogl", "frb_local", "frb_pseudo", "frb_2026", "frb_126"}
NOMINAL_ONLY = {"bbh_agn_planck", "bbh_agn_shoes"}

def finish(record):
    sigma_rel = record.get("sigma_rel")
    if sigma_rel is None:
        sigma_rel = record["sigma"] / record["h0"]
    sigma_total = math.hypot(sigma_rel, SIGMA_BG_REL)
    d = K_MINUS_1 / sigma_total
    cruza_5 = d >= 5.0
    cruza_90 = d >= D90
    if record["id"] in SEM_PONTE:
        cruza_5 = "nominal; sem ponte" if cruza_5 else "não; sem ponte qualificada"
        cruza_90 = "nominal; sem ponte" if cruza_90 else "não; sem ponte qualificada"
    elif record["id"] == "frb_pseudo" or record["id"] in NOMINAL_ONLY:
        cruza_5 = "nominal" if cruza_5 else "não"
        cruza_90 = "nominal" if cruza_90 else "não"
    elif record["id"] in STAT_ONLY:
        cruza_5 = "sim (só stat)" if cruza_5 else "não"
        cruza_90 = "sim (só stat)" if cruza_90 else "não"
    if record["id"] in RG:
        ponte = "SIM_CONDICIONAL_RG_R16" if record["id"].startswith("tdcosmo") else "SIM_CONDICIONAL_RG"
        rota_seq = "R-G seq 379,391,393,1637; R16 seq 1225-1245" if record["id"].startswith("tdcosmo") else "R-G seq 379,391,393,1637"
        qualificada = True
    elif record["id"] in RH:
        ponte = "SIM_CONDICIONAL_RH"
        rota_seq = "R-H seq 401,1638"
        qualificada = True
    elif record["id"] in SEM_PONTE:
        ponte = "NAO_EXAMINADA"
        rota_seq = "nenhuma rota de ponte específica examinada localizada"
        qualificada = False
    else:
        ponte = "NAO_NOVA_LINHA_UM_PASSO"
        rota_seq = "rede/composto já examinado; sem independência nova"
        qualificada = False
    result = dict(
        **record,
        publicado=PUBLICADO.get(record["id"], "ver fonte"),
        sigma_local_relativa=sigma_rel,
        sigma_fundo_relativa=SIGMA_BG_REL,
        D_desenho=d,
        cruza_5sigma=cruza_5,
        cruza_D90=cruza_90,
        ponte_K_H_fundo=ponte,
        ponte_rota_seq=rota_seq,
        entra_conta_poder_qualificada=qualificada,
        D_estatuto="condicional à ponte" if qualificada else "apenas aritmético/nominal; fora da conta de poder qualificada",
    )
    if record["id"] == "sn2_vogl":
        result["D_teto_so_estatistico"] = True
        result["D_com_sistematica_igual_estatistica"] = K_MINUS_1 / math.hypot(math.sqrt(2.0) * sigma_rel, SIGMA_BG_REL)
    return result

records = [finish(record) for record in records]
forecasts = [finish(record) for record in forecasts]
summary = {
    "estatuto": "[DERIVED — PLANEJAMENTO, não estatística observada] Valores publicados [KNOWN, a conferir] com identificadores na tabela.",
    "formula": "D = (K-1) / sqrt(sigma_local_relativa^2 + sigma_fundo_relativa^2); lado maior de erros assimétricos; stat+sys em quadratura apenas quando publicados.",
    "K_minus_1": K_MINUS_1,
    "BG1": {"H0": BG1_H0, "sigma": BG1_SIGMA, "sigma_relativa": SIGMA_BG_REL},
    "D90": D90,
    "sigma_local_5sigma": math.sqrt((K_MINUS_1 / 5.0) ** 2 - SIGMA_BG_REL ** 2),
    "sigma_local_D90": math.sqrt((K_MINUS_1 / D90) ** 2 - SIGMA_BG_REL ** 2),
    "h0dn_core": H0DN_CORE,
    "regra_poder_qualificada": "Linha local de um passo sem ponte K·H_fundo examinada não entra em conta de poder qualificada; D permanece apenas aritmético/nominal.",
    "empilhamento_revisor": EMPILHAMENTO_REVISOR,
    "medidas": records,
    "previsoes": forecasts,
}
out = Path(__file__).resolve().parent
with (out / "MEDIDAS_PLANEJAMENTO_K04.json").open("w", encoding="utf-8") as handle:
    json.dump(summary, handle, ensure_ascii=False, indent=2)
    handle.write("\n")

def pct(x):
    return f"{100*x:.3f} %".replace(".", ",")

def yesno(x):
    return x if isinstance(x, str) else ("sim" if x else "não")

sn2 = next(r for r in records if r["id"] == "sn2_vogl")
lines = [
    "# Medidas de planejamento — K04/Hubble, correção K09",
    "",
    "**[DERIVED — PLANEJAMENTO, não estatística observada]** Valores de literatura são **[KNOWN, a conferir]** com identificadores. Nenhum vetor observado foi lido.",
    "",
    "## D da casa, antes das contas de bolso",
    "",
    "| Recorte do core `h0dn_bg1_v411.values` | D | Uso |",
    "|---|---:|---|",
    f"| Primário | {H0DN_CORE['primario']['D']:.3f} | Já lido, não cego e não independente |",
    f"| Cefeidas livres | {H0DN_CORE['cefeidas_livres']['D']:.3f} | Variante já lida; não nova abertura |",
    "",
    "As contas de bolso usam os cabeçalhos 73,50 ± 0,81 (baseline) e 73,994 ± 0,697 (V99), BG1 = 0,30/68,53 e a fórmula abaixo; não substituem o modelo de erros do core.",
    "",
    f"BG1: {BG1_SIGMA}/{BG1_H0} = {pct(SIGMA_BG_REL)}. Limites locais: 5σ ≤ {pct(summary['sigma_local_5sigma'])}; D90 ≤ {pct(summary['sigma_local_D90'])}.",
    "D = (K−1)/√(σ_local² + σ_BG1²). Lado maior de erros assimétricos. Linha sem ponte `K·H_fundo` examinada não entra em conta de poder qualificada.",
    "",
    "| Método | H0 e σ publicados | H0DN/Fase 9 | σ local | D desenho | Ponte `K·H_fundo` | 5σ | D90 | Data/dependência |",
    "|---|---|---|---:|---:|---|---|---|---|",
]
for r in records:
    lines.append(
        f"| {r['metodo']} | {r['publicado']} [{r['fonte']}] | {r['inclusao']} | {pct(r['sigma_local_relativa'])} | {r['D_desenho']:.3f} | {r['ponte_K_H_fundo']}: {r['ponte_rota_seq']} | {yesno(r['cruza_5sigma'])} | {yesno(r['cruza_D90'])} | {r['calendario']} |"
    )
lines.extend([
    "",
    "## Previsões, não medidas atuais",
    "",
    "| Previsão | σ local | D desenho | Ponte `K·H_fundo` | 5σ | D90 | Dependência/data |",
    "|---|---:|---:|---|---|---|---|",
])
for r in forecasts:
    lines.append(
        f"| {r['metodo']} [{r['fonte']}] | {pct(r['sigma_local_relativa'])} | {r['D_desenho']:.3f} | {r['ponte_K_H_fundo']}: {r['ponte_rota_seq']} | {yesno(r['cruza_5sigma'])} | {yesno(r['cruza_D90'])} | {r['calendario']} |"
    )
lines.extend([
    "",
    "## Empilhamento do revisor — não cego e não independente",
    "",
    "| Linhas | D nominal | D com sistemática SN II = estatística | Famílias já na Fase 9 V2 |",
    "|---|---:|---:|---|",
    f"| SN II + TDCOSMO-2026 | {EMPILHAMENTO_REVISOR['duas_linhas']['D_so_stat']:.2f} | {EMPILHAMENTO_REVISOR['duas_linhas']['D_sn2_sistematica_igual_estatistica']:.2f} | TDCOSMO (1/2) |",
    f"| SN II + TDCOSMO-2026 + reanálise MCP + FRB + BBH–AGN | {EMPILHAMENTO_REVISOR['cinco_linhas']['D_so_stat']:.2f} | {EMPILHAMENTO_REVISOR['cinco_linhas']['D_sn2_sistematica_igual_estatistica']:.2f} | TDCOSMO e masers (2/5) |",
    "",
    "Esses valores não são composto aberto, não são independentes e não se somam à V2. SN II, FRB e BBH–AGN não têm ponte examinada; três entradas do segundo empilhamento são só-estatísticas.",
    "",
    "## Leitura obrigatória",
    "",
    "- O D é distância de desenho entre K e o nulo K=1 sob o modelo de erros escolhido; não é Z observado, significância nem veredito.",
    f"- SN II tailored EPM: 3,256 é teto só-estatístico; com sistemática = estatística, D = {sn2['D_com_sistematica_igual_estatistica']:.3f}. Sem ponte examinada e com presença prévia em variante H0DN, não é independente qualificada sem ressalva.",
    "- Resultados só estatísticos são tetos otimistas. O FRB de 0,68 (0,99 %) não é precisão total: `f_IGM/H0` é degenerado e a sistemática domina.",
    "- DESI DR3 entra como fundo por padrão; uso testemunhal separado exige pergunta, mapa Ωm/R, covariância, pré-registro por hash, abertura única e não dupla contagem com BG1 antes da leitura.",
    "- A lista não foi ordenada nem filtrada por D. Novos agregados públicos não são cegos para a casa.",
])
with (out / "MEDIDAS_PLANEJAMENTO_K04.md").open("w", encoding="utf-8") as handle:
    handle.write("\n".join(lines) + "\n")
print(json.dumps({k: summary[k] for k in ("sigma_fundo_relativa" if False else "D90", "sigma_local_5sigma", "sigma_local_D90")}, ensure_ascii=False, indent=2))
