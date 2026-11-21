# -*- coding: utf-8 -*-
"""derivar_rito_e_carimbo_v413.py -- (Etapa 3 da v413, 20/11/2026) deriva rito_v413.sh e carimbar_stdout_v413.py dos moldes selados da v412
(v412\\rito_v412.sh e v412\\carimbar_stdout_v412.py; so' lidos). Trocas por texto EXATO com contagem conferida; cada troca registrada em
etapa3\\DERIVACAO_RITO_v413.json, com o diff unificado em etapa3\\bump\\. O que muda no rito:
  (1) o CABECALHO descritivo (a v413: 21 modulos novos e um corrigido; o tempo esperado LIDO de kernel\\construir_marcas.txt e do KH_N1; o tempo-limite
      do lake build LIDO do um.py; os registros LIDOS do contrato R1; a rodada da v412 lida de v412\\rito_horarios_v412.txt);
  (2) os rotulos: v412 -> v413 e, depois, v411 -> v412 (a guarda do marcador da rodada anterior passa a ler as pastas v412 e v413);
  (3) o PORTAO DO PILAR antes de qualquer parada (portao_ambiente_pilar_v413.py: o ambiente que o um.py sonda e' o do cache; senao PARAR, codigo 19;
      ilegivel, codigo 21); nao toca a placa;
  (4) a placa NAO e' medida: sai a leitura da VRAM (nvidia-smi) e as recusas 11 e 12 (com treino em curso na placa elas sempre recusariam, e o
      pilar e' reaproveitado pelo cache, sem calculo); a parada do servidor do modelo nativo so' age se ele estava ligado (a recusa 10 fica);
  (5) o VIGIA DO PILAR durante o rito (pilar_no_stdout_v413.py em laco): se a linha de CALCULO do pilar aparecer, ou o reuso vier com outra chave,
      grava PILAR_PARADA_v413.txt e manda TERM ao proprio lancador (o caminho de sinal do molde: encerra a arvore do um.py desta rodada,
      RITO_RC=SINAL_TERM, restaura o servidor); a bandeira do vigia sai no religamento.
No carimbador so' mudam a marca de cabecalho e os rotulos (o corpo e' generico). Uso: derivar_rito_e_carimbo_v413.py [--executar]"""
import difflib, hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
E3 = Path(__file__).resolve().parent; V = E3.parent; V412 = V.parent / "v412"; EXEC = "--executar" in sys.argv; TS = time.strftime("%Y%m%d_%H%M%S")
sha = lambda b: hashlib.sha256(b).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
REG = []


def troca(t, velho, novo, n, rotulo):
    c = t.count(velho); assert c == n, ("contagem diferente", rotulo, c, n, velho[:90])
    REG.append({"troca": rotulo, "ocorrencias": c, "velho_sha16": sha(velho.encode())[:16], "novo_sha16": sha(novo.encode())[:16]}); return t.replace(velho, novo)


# ------------------------------------------------------------------ os numeros do cabecalho, LIDOS
marcas = (V / "kernel" / "construir_marcas.txt").read_text(encoding="utf-8")
ep = {k: int(v) for k, v in re.findall(r"^(epoch_inicio|epoch_build_fim|epoch_audit_fim)=(\d+)", marcas, re.M)}
n_mod_marcas = len(re.findall(r"^modulo=TGLExt\.\S+ rc=0 s=\d+", marcas, re.M)); assert re.search(r"^rc=0$", marcas, re.M), "o build do sandbox nao fechou com rc=0"
t_build, t_audit = ep["epoch_build_fim"] - ep["epoch_inicio"], ep["epoch_audit_fim"] - ep["epoch_build_fim"]
KH = lj(V / "kernel" / "KH_N1_v413.json"); assert KH["duracao_build_s"] == t_build and KH["duracao_audit_s"] == t_audit, ("as duracoes do KH_N1 diferem das marcas", KH["duracao_build_s"], t_build, KH["duracao_audit_s"], t_audit)
KN = lj(V / "kernel_modulos_novos_v413.json"); NN = KN["n"]; NC = len(KN["kernel_corrigido"]); assert n_mod_marcas == NN + NC
BU = lj(V / "BUNDLE_v413.json"); n_dep = len(BU["kernel_corrigido"][0].get("dependentes_antigos_no_kernel") or [])
FJ = lj(V / "kernel" / "FLAGS_v413.json"); NB = FJ["n_flags"]
um412 = (V / "base_v412" / "um.py").read_text(encoding="utf-8", errors="replace")
m_to = re.findall(r'run_process_checked\(\[lake, "build"\], FORMAL_DIR, (\d+)\)', um412); assert len(m_to) == 1, m_to; T_LAKE = int(m_to[0])
hor = (V412 / "rito_horarios_v412.txt").read_text(encoding="utf-8").split()
h0, h1 = [int(x[:2]) * 3600 + int(x[3:5]) * 60 + int(x[6:8]) for x in hor[:2]]; dur412 = (h1 - h0) % 86400
ctt = (V / "CONTRATO_v413_R1.md").read_text(encoding="utf-8"); s2 = re.search(r"^## 2\. .*?(?=^## 3\. )", ctt, re.M | re.S).group(0)
REGS = re.findall(r"^- `([a-z0-9_]+_v413)`", s2, re.M); assert REGS
CHAVE = lj(V412 / "ESPERADOS_v412.json")["pilar"]["key"]
CAB = [
    "#!/bin/sh",
    "# [DERIVADO v413, 20/11/2026, Etapa 3 da v413 (construtor da Etapa 3, a servico da gerencia c1)] de v412\\rito_v412.sh por etapa3\\derivar_rito_e_carimbo_v413.py: o corpo e' o do molde",
    "# (generico); mudam este cabecalho, os rotulos, o PORTAO DO PILAR antes de qualquer parada, a placa que NAO se mede e o VIGIA DO PILAR durante o rito (trocas e diff em etapa3\\DERIVACAO_RITO_v413.json).",
    "# O RITO v413 (ato da gerencia c1): roda o um.py v413 instalado no Nos (instalar_v413.py) -- %d MODULOS NOVOS de kernel e UM modulo CORRIGIDO (TGLExt/OResumoEPsiBit.lean, so' a docstring; o" % NN,
    "# um.py materializa o corpo embutido em tgl_kernel\\TGLExt: os novos, o corrigido por cima do antigo e a raiz TGLExt.lean com os imports novos), %d bandeiras novas e os registros por especificacao %s," % (NB, ", ".join(REGS)),
    "# com as palavras de veredito do contrato R1; os registros anteriores sao RECRIADOS; nenhuma chave antiga muda fora dos numeros; o gate nao se move; o teste H0DN x BG1 nao se reabre.",
    "# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (%s, a mesma da v412; _QP_REUSE_V386); TGL_RITE_CHECKPOINT DESLIGADO. HA TREINO EM CURSO NA PLACA (C:\\IALD\\TGL_IALD_NATIVE_QWEN5090):" % CHAVE,
    "# NAO TOCAR, NAO MEDIR, NAO PARAR. Por isso: (a) o PORTAO DO PILAR (portao_ambiente_pilar_v413.py, com o mesmo python do um.py) confere, ANTES de qualquer parada e sem tocar a placa, que o",
    "# ambiente que o um.py vai sondar (torch, cuda, numpy, scipy, python, nome da placa) e' o do cache; senao NAO RODO (19; ilegivel: 21) e a gerencia avisa o operador; (b) a VRAM nao e' lida e as",
    "# recusas 11/12 do molde saem (com o treino na placa elas sempre recusariam); (c) o VIGIA DO PILAR le o stdout canonico e, se o um.py anunciar o CALCULO do pilar (o autoteste do motor, que o",
    "# um.py roda na placa mesmo no reuso, pode falhar por memoria) ou o reuso com outra chave, grava PILAR_PARADA_v413.txt e manda TERM ao lancador (encerra a arvore do um.py; RITO_RC=SINAL_TERM).",
    "# O que o portao NAO decide: o autoteste do motor (E1..E8), curto, que o um.py roda na placa no reuso; esse toque e' do proprio um.py (PORTAO_DO_PILAR_v413.json) e o vigia cobre a falha dele.",
    "# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v413_stdout.txt (o carimbador grava o tempo de cada linha no pacote), trailer RITO_RC=<rc>. RODADA COMPLETA.",
    "# O SERVIDOR DO MODELO NATIVO (molde): a tarefa «IALD Llama Server» e o supervisor sao PARADOS antes SE estavam ligados (estado lido pela tarefa e pelo processo; sonda vazia conta como ligado),",
    "# VIGIADOS durante e RELIGADOS no fim se estavam ligados -- mesmo se o rito falhar ou o lancador receber TERM/HUP/INT; o marcador .servidor_parado_pelo_rito fica no pacote enquanto parado.",
    "# ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v413.pid) NO GIT BASH (o PID do MSYS), conferindo antes /proc/<pid>/cmdline com rito_v413. Codigos de recusa do molde: 6-10, 13-18; novos: 19, 21.",
    "# TEMPO ESPERADO (v413, lido de kernel\\construir_marcas.txt do build A FRIO no sandbox k413c e conferido com kernel\\KH_N1_v413.json): %d modulos (os novos e o corrigido) e o lake build em %d s, o Audit em %d s." % (n_mod_marcas, t_build, t_audit),
    "# No Nos o kernel da v412 ja' esta' compilado em .lake/build: o rito compila os novos, o corrigido e os %d dependentes antigos dele (BUNDLE_v413.json), a raiz e o Audit; o lake build do um.py tem" % n_dep,
    "# tempo-limite de %d s (lido do um.py); a rodada da v412 levou %d h %02d min (v412\\rito_horarios_v412.txt). Se o lake build estourar o tempo-limite (licao v372), a verificacao do kernel sai FAILED" % (T_LAKE, dur412 // 3600, (dur412 % 3600) // 60),
    "# com rc 0: o conferidor reprova (escada e linha do kernel) e a rodada seguinte, com o cache quente, fecha; preservar o stdout e a captura da que estourou.",
]
# ------------------------------------------------------------------ o rito
src = (V412 / "rito_v412.sh").read_bytes().decode("utf-8"); L = src.split("\n")
i_pk = next(i for i, l in enumerate(L) if l.startswith('PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412"')); assert i_pk == 23, i_pk
corpo = "\n".join(L[i_pk:])
corpo = troca(corpo, "v412", "v413", corpo.count("v412"), "rotulos v412 -> v413 (todas as ocorrencias do corpo)")
corpo = troca(corpo, "v411", "v412", 5, "rotulos v411 -> v412 (a guarda do marcador da rodada anterior: o comentario e a lista das pastas)")
assert "v411" not in corpo
# (3) o portao do pilar, depois da guarda de processo e antes de qualquer parada
ANC3 = 'n=$(echo "$v" | grep -c -E \'^[0-9]+\\s*$\'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }\n'
NOVO3 = ANC3 + ("# o PORTAO DO PILAR (v413): o ambiente que o um.py vai sondar tem de ser o do cache do pilar (senao o um.py CALCULARIA o pilar na placa, onde ha treino em curso):\n"
                "# NAO toca a placa; recusa = PARAR e avisar o operador (19); ilegivel = PARAR (21). Roda com o MESMO python do um.py, sem -I (os mesmos pacotes).\n"
                'pp_=$(python "$PK/portao_ambiente_pilar_v413.py" "$PK/ESPERADOS_v413.json" 2>&1); prc_=$?\n'
                'echo "$pp_" | tail -3\n'
                '[ "$prc_" = "0" ] || { echo "o portao do pilar recusou (rc $prc_): o ambiente da placa nao e\' o do cache, ou nao se leu -- NAO RODO; avisar o operador"; [ "$prc_" = "19" ] && exit 19; exit 21; }\n')
corpo = troca(corpo, ANC3, NOVO3, 1, "o portao do pilar antes de qualquer parada")
# (4) a placa nao e' medida; a parada so' age se o servidor estava ligado
ANC4 = ('log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"\n'
        'powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName \'IALD Llama Server\'" >> "$LOGS" 2>&1\n'
        'powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1\n'
        'sleep 5\n'
        'vivos=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d \'\\r\')\n'
        "mem=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' \\r')\n"
        'log "depois da parada: llama-server vivos = $vivos ; VRAM usada = $mem MiB"\n'
        'if [ "$vivos" != "0" ]; then\n'
        '  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); o trap restaura o estado anterior"; exit 10\n'
        'fi\n'
        'case "$mem" in \'\'|*[!0-9]*) log "a VRAM usada nao e\' legivel (\'$mem\') -- NAO RODO (fail-closed)"; exit 12;; esac\n'
        'if [ "$mem" -gt 6000 ]; then\n'
        '  log "a VRAM usada ($mem MiB) passa de 6000 MiB com o servidor parado: ha outro processo na GPU -- NAO RODO (fail-closed)"; exit 11\n'
        'fi\n')
NOVO4 = ('if [ "$ESTAVA_LIGADO" = "1" ]; then\n'
         '  log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"\n'
         '  powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName \'IALD Llama Server\'" >> "$LOGS" 2>&1\n'
         '  powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1\n'
         '  sleep 5\n'
         'else\n'
         '  log "o servidor do modelo nativo nao estava ligado: nada a parar (a parada e o religamento so\' agem se ele estava ligado)"\n'
         'fi\n'
         'vivos=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d \'\\r\')\n'
         'log "depois da parada: llama-server vivos = $vivos ; a placa NAO e\' medida (v413: ha treino em curso na placa -- nao tocar, nao medir, nao parar; o pilar e\' reaproveitado pelo cache e o vigia do pilar para o rito se o um.py anunciar o calculo)"\n'
         'if [ "$vivos" != "0" ]; then\n'
         '  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); o trap restaura o estado anterior"; exit 10\n'
         'fi\n')
corpo = troca(corpo, ANC4, NOVO4, 1, "a placa nao e' medida (sai a VRAM e as recusas 11/12); a parada so' age se o servidor estava ligado")
# (5a) o vigia do pilar: a bandeira sai no religamento
ANC5 = '  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"\n'
corpo = troca(corpo, ANC5, ANC5 + '  [ -f "$PK/.vigia_pilar_ativo" ] && rm -f "$PK/.vigia_pilar_ativo"   # (v413) o vigia do pilar sai sozinho ao ver a bandeira apagada\n', 1, "a bandeira do vigia do pilar sai no religamento")
# (5b) o vigia do pilar: depois de girar o stdout da tentativa anterior e antes de lancar o um.py
ANC6 = 'if [ -f rodada_v413_stdout.txt ]; then n=1; while [ -f "rodada_v413_stdout_tentativa$n.txt" ]; do n=$((n+1)); done; mv rodada_v413_stdout.txt "rodada_v413_stdout_tentativa$n.txt"; fi\n'
NOVO6 = ANC6 + ('# 2b. (v413) o VIGIA DO PILAR: le o stdout canonico (que o carimbador grava em tempo real) ate\' a decisao do pilar. REUSO com a chave do ESPERADOS: sai. CALCULO, ou reuso com\n'
                '# outra chave: grava PILAR_PARADA_v413.txt e manda TERM ao lancador (sinal TERM do molde: encerra a arvore do um.py desta rodada e restaura o servidor). Ha treino na placa.\n'
                '[ -f "$PK/PILAR_PARADA_v413.txt" ] && mv -f "$PK/PILAR_PARADA_v413.txt" "$PK/PILAR_PARADA_v413.txt.anterior_$(date +%Y%m%d_%H%M%S)"\n'
                'touch "$PK/.vigia_pilar_ativo"\n'
                '(\n'
                '  t0p=$(date +%s); avisou=0\n'
                '  while [ -f "$PK/.vigia_pilar_ativo" ]; do\n'
                '    kill -0 "$PAI" 2>/dev/null || break\n'
                '    if [ -f rodada_v413_stdout.txt ]; then\n'
                '      r_=$(python "$PK/pilar_no_stdout_v413.py" rodada_v413_stdout.txt "$PK/ESPERADOS_v413.json" 2>&1 | tail -1 | tr -d \'\\r\')\n'
                '      case "$r_" in\n'
                '        REUSO_OK*) echo "$(date +%H:%M:%S) VIGIA DO PILAR: $r_ (o pilar foi reaproveitado pela chave do cache; nada na placa alem do autoteste do motor)" >> "$LOGS"; break;;\n'
                '        CALCULA*|CHAVE_ERRADA*) echo "$(date +%H:%M:%S) VIGIA DO PILAR: $r_ -- o pilar NAO foi reaproveitado; ha treino em curso na placa: PARO o rito e aviso" >> "$LOGS"\n'
                '          echo "$r_ $(date \'+%Y-%m-%d %H:%M:%S\')" > "$PK/PILAR_PARADA_v413.txt"; kill -TERM "$PAI" 2>/dev/null; break;;\n'
                '      esac\n'
                '    fi\n'
                '    if [ "$avisou" = "0" ] && [ $(( $(date +%s) - t0p )) -gt 2400 ]; then echo "$(date +%H:%M:%S) VIGIA DO PILAR: AVISO -- 40 min sem a linha do pilar no stdout; sigo vigiando" >> "$LOGS"; avisou=1; fi\n'
                '    sleep 3\n'
                '  done\n'
                ') &\n')
corpo = troca(corpo, ANC6, NOVO6, 1, "o vigia do pilar durante o rito")
# o PAI do vigia do pilar e' o mesmo do vigia do servidor: conferir que ja' esta' definido antes
assert corpo.index("PAI=$$") < corpo.index("# 2b. (v413) o VIGIA DO PILAR"), "o PAI tem de estar definido antes do vigia do pilar"
assert "nvidia-smi" not in corpo and "VRAM usada" not in corpo and "exit 11" not in corpo and "exit 12" not in corpo
novo_rito = "\n".join(CAB) + "\n" + corpo
assert corpo.count("v412") == 5 and corpo.count("ESPERADOS_v413.json") == 3, ("o corpo tem de citar a v412 so' na guarda do marcador anterior (5) e o ESPERADOS da v413 tres vezes (o candidato esperado, o portao e o vigia do pilar)", corpo.count("v412"), corpo.count("ESPERADOS_v413.json"))
# ------------------------------------------------------------------ o carimbador
cs = (V412 / "carimbar_stdout_v412.py").read_bytes().decode("utf-8"); CL = cs.split("\n")
assert CL[1].startswith("# [ADAPTADO v412") and CL[2].startswith("# [ADAPTADO v411") and CL[3].startswith("# [ADAPTADO v410")
VELHO_DOC = "[copia na cadeia v412, 12/11/2026, claude-construtor-v412: o corpo e' o do carimbador da v411 (sha16 do arquivo da v411, lido pelo adaptador de 12/11: fd8d88dae063b429; a subida de 06/11 dizia o da v409); so' o rotulo da versao sobe no texto] "
c_corpo = "\n".join(CL[4:])
c_corpo = troca(c_corpo, VELHO_DOC, "[copia na cadeia v413: o corpo e' o do carimbador do molde selado (ver a marca do cabecalho); so' o rotulo da versao sobe no texto] ", 1, "o carimbador: a marca do docstring")
c_corpo = troca(c_corpo, "v412", "v413", c_corpo.count("v412"), "o carimbador: rotulos v412 -> v413")
assert "v411" not in c_corpo and "v412" not in c_corpo and "v410" not in c_corpo.split('"""', 2)[2]
c1 = "\n".join([CL[0], "# [DERIVADO v413, 20/11/2026, Etapa 3 da v413] de v412\\carimbar_stdout_v412.py por etapa3\\derivar_rito_e_carimbo_v413.py: o corpo e' generico (um tee que carimba a hora de cada linha e confere o sha256 do stdout gravado); mudam so' os rotulos"]) + "\n" + c_corpo
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("error")
    compile(c1, "carimbar_stdout_v413.py", "exec")
# ------------------------------------------------------------------ gravar (com --executar), o diff e o registro
saidas = {"rito_v413.sh": (V412 / "rito_v412.sh", novo_rito), "carimbar_stdout_v413.py": (V412 / "carimbar_stdout_v412.py", c1)}
(E3 / "bump").mkdir(exist_ok=True)
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "etapa3\\derivar_rito_e_carimbo_v413.py", "trocas": REG, "saidas": {},
       "numeros_lidos": {"modulos_nas_marcas": n_mod_marcas, "build_s": t_build, "audit_s": t_audit, "dependentes_antigos_do_corrigido": n_dep, "lake_build_timeout_s": T_LAKE,
                         "rodada_v412_s": dur412, "bandeiras_novas": NB, "registros": REGS, "chave_do_pilar": CHAVE}}
for nome, (molde, novo) in saidas.items():
    d = list(difflib.unified_diff(molde.read_text(encoding="utf-8").split("\n"), novo.split("\n"), molde.name, nome, lineterm=""))
    (E3 / "bump" / (nome + ".diff")).write_text("\n".join(d) + "\n", encoding="utf-8")
    rec["saidas"][nome] = {"molde": str(molde), "molde_sha16": sha(molde.read_bytes())[:16], "sha16": sha(novo.encode("utf-8"))[:16], "bytes": len(novo.encode("utf-8")),
                           "diff": "etapa3\\bump\\%s.diff" % nome, "linhas_trocadas": sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---"))}
    print(nome, rec["saidas"][nome])
if EXEC:
    for nome, (molde, novo) in saidas.items():
        p = V / nome; b = novo.encode("utf-8")
        if p.exists():
            bk = p.with_name(p.name + ".bak_" + TS); bk.write_bytes(p.read_bytes()); assert bk.read_bytes() == p.read_bytes()
        tmp = p.with_name(p.name + ".tmp_e3"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(p)
    pr = E3 / "DERIVACAO_RITO_v413.json"; pt = pr.with_name(pr.name + ".tmp"); pt.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8"); pt.replace(pr)
    print("gravados: rito_v413.sh, carimbar_stdout_v413.py | registro", pr)
else:
    print("(ensaio: nada gravado; --executar grava)")
