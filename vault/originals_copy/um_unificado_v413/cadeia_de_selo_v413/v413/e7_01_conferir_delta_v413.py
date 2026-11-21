# -*- coding: utf-8 -*-
"""Etapa 2 da v413, bloco 1: importa o delta_v413 e confere, por leitura dos arquivos, o que ele expoe (versao, base, sandbox, bundle, modulo corrigido, bandeiras, escada, registros e palavras do contrato,
constantes do B(n) lidas do delta do B(n)); confere que o delta da v412 (o molde) e o do B(n) nao foram tocados; grava o estado do bloco 1."""
import json, os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import delta_v413 as DL

e = L.Exame("delta_v413")
e.chk("UM_VERSION v413 e base v412", DL.UM_VERSION == "v413" and DL.BASE_VERSION == "v412", 2, [DL.UM_VERSION, DL.BASE_VERSION])
base = L.D / "base_v412"
selo = L.ler_json(base / "um_absoluto_selo.json")
e.chk("a base_v412 e' a v412 selada (sha256 do um.py = selo; sha16 = o do contrato)", selo.get("um_version") == "v412" and L.sha256_arq(base / "um.py") == selo["sha256"]["um.py"] and L.sha16_arq(base / "um.py") == DL.BASE_SHA16_DA_ORDEM, 3,
      [selo.get("um_version"), L.sha16_arq(base / "um.py"), DL.BASE_SHA16_DA_ORDEM])
e.chk("o bundle: 21 modulos na ordem topologica, sufixo da raiz conferido", DL.N_BUNDLE == 21 and len(DL.ROOT_SUFFIX.splitlines()) == 21, DL.N_BUNDLE)
e.chk("o modulo corrigido: TGLExt/OResumoEPsiBit.lean, antes e depois diferentes", DL.KERNEL_CORRIGIDO["rel"] == "TGLExt/OResumoEPsiBit.lean" and DL.KERNEL_CORRIGIDO["sha256_antes"] != DL.KERNEL_CORRIGIDO["sha256_depois"], 1, DL.KERNEL_CORRIGIDO)
sb = Path(DL.SANDBOX) / "TGLExt" / "OResumoEPsiBit.lean"
e.chk("o sandbox tem o modulo corrigido com o sha256 depois", L.sha256_arq(sb) == DL.KERNEL_CORRIGIDO["sha256_depois"], 1)
e.chk("a escada 17786 -> 18498 com 712 bandeiras (lidas de FLAGS_v413.json)", DL.ESCADA_NOVA == DL.ESCADA_BASE + DL.N_FLAGS, DL.N_FLAGS, [DL.ESCADA_BASE, DL.ESCADA_NOVA, DL.N_FLAGS])
e.chk("os cinco registros e as palavras de veredito, lidos do contrato; o kh_n1_cobertura_v413 (contrato R2) antes do cunhagens_v413, com a palavra no molde do kh da v411 e os numeros do recibo KH_N1",
      len(DL.REGISTROS_SPEC_V413_CONTRATO) == 5 and DL.REGISTROS_SPEC_V413 == DL.REGISTROS_SPEC_V413_CONTRATO[:-1] + ["kh_n1_cobertura_v413", "cunhagens_v413"] and all(DL.PALAVRAS_DE_VEREDITO[n] for n in DL.REGISTROS_SPEC_V413)
      and "NONE_OUTSIDE_THE_TRIO" in DL.PALAVRAS_DE_VEREDITO["kh_n1_cobertura_v413"], 6, DL.REGISTROS_SPEC_V413)
e.chk("as constantes do B(n) vem do delta do B(n) (o sandbox curto do B(n), so' lido, e o BANCADA_PINA_HOJE); o sandbox curto da Etapa 2 e' proprio e diferente do do B(n)",
      DL.SANDBOX_CURTO_DO_BN == DL.DBN.SANDBOX_CURTO and DL.BANCADA_PINA_HOJE == DL.DBN.BANCADA_PINA_HOJE and DL.SANDBOX_CURTO == DL.SANDBOX_GUARDAS != DL.SANDBOX_CURTO_DO_BN, 3,
      {"sandbox_curto_do_bn_so_lido": DL.SANDBOX_CURTO_DO_BN, "sandbox_da_etapa_2": DL.SANDBOX_GUARDAS, "existe_o_da_etapa_2": os.path.exists(DL.SANDBOX_GUARDAS), "existe_o_do_bn": os.path.exists(DL.SANDBOX_CURTO_DO_BN),
       "bancada_pina_hoje": DL.BANCADA_PINA_HOJE})
e.chk("o delta da v412 foi carregado pelo delta do B(n) (o delta_v411 fixado)", DL.D12.D11.BANCADA_PINA_HOJE == DL.DBN.BANCADA_PINA_HOJE_FIXADA_V411, 1)
e.chk("o modo e a pagina", DL.MODO in ("contrato", "proposta") and Path(DL.PAGINA_ARQ).exists(), 1, {"modo": DL.MODO, "pagina": DL.PAGINA_ARQ})
print(json.dumps(e.resumo(), ensure_ascii=False))
for l in e.linhas:
    print(("OK   " if l["ok"] else "FALHA ") + l["checagem"])
rec = {"contrato": "DELTA_v413_CONFERIDO", "resumo": e.resumo(), "checagens": e.linhas, "delta_sha16": L.sha16_arq(L.D / "delta_v413.py"),
       "molde_delta_v412_r7_sha16": L.sha16_arq(L.V412 / "delta_v412_r7.py"), "delta_bn_v413_sha16": L.sha16_arq(L.D / "bancada" / "delta_bn_v413.py")}
L.salvar_json(L.D / "DELTA_v413_CONFERIDO.json", rec)
L.estado_bloco("1_delta", e.ok, {"delta": L.D / "delta_v413.py", "lib": L.D / "e7_lib_v413.py", "conferencia": L.D / "DELTA_v413_CONFERIDO.json", "base_um_v412": L.D / "base_um_v412.py",
                                 "conferencia_de_entrada": L.D / "CONFERENCIA_ENTRADA_ETAPA2_v413.json"},
               nota="delta_v413: bump 412->413, o bundle dos 21, o modulo corrigido (OResumoEPsiBit, substituicao do texto embutido), as bandeiras e a escada de FLAGS_v413.json, os registros e as palavras do contrato; B(n) lido do delta_bn_v413",
               proximo="e7_10/e7_11 (as ancoras), e7_12 (os cabecalhos), registros_v413.py")
sys.exit(0 if e.ok else 1)
