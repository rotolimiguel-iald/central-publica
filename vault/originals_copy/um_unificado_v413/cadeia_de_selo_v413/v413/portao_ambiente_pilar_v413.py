# -*- coding: utf-8 -*-
"""portao_ambiente_pilar_v413.py -- o PORTAO DO PILAR antes do rito da v413 (Etapa 3; chamado pelo rito_v413.sh com o MESMO `python` que roda o
um.py, sem -I, para ver os mesmos pacotes). Pergunta: o ambiente que o um.py vai sondar e' o do cache do pilar? Se for, o rito REAPROVEITA o pilar
pela chave (nao calcula na placa); se nao for, o um.py recusaria o reuso e CALCULARIA o pilar na placa, onde ha' treino em curso: PARAR e avisar.

NAO TOCA A PLACA: nao importa torch (nao cria contexto CUDA), nao chama nvidia-smi, nao mede memoria nem carga. Le:
  * do cache (o result.json conferido pelo sha256 do ESPERADOS e pelo result.json.sha256, como _qp_cached_ok do um.py): o ambiente gravado
    (torch, cuda, numpy, scipy, python, gpu);
  * do ambiente presente: python = platform.python_version() deste interpretador; numpy.__version__ e scipy.__version__ (importados: so' CPU);
    torch.__version__ e torch.version.cuda LIDOS DO ARQUIVO torch/version.py (achado por importlib.util.find_spec, que nao executa o pacote);
    o nome da placa pelo Windows (Win32_VideoController.Name, so' o nome do dispositivo; nada de carga ou memoria).
Decisao: tudo igual ao cache -> PORTAO_PILAR_OK (saida 0); algo diferente -> PORTAO_PILAR_RECUSA (saida 19); leitura falhou -> PORTAO_PILAR_ILEGIVEL
(saida 21, fail-closed). O que este portao NAO decide: o autoteste do motor (E1..E8), que o um.py roda na placa mesmo no reuso (curto); se ele falhar
por falta de memoria, o um.py calcularia o pilar -- e o vigia do pilar no rito (pilar_no_stdout_v413.py) para o rito na hora em que a linha de
calculo aparecer. Grava PORTAO_AMBIENTE_PILAR_v413_<ts>.json ao lado do ESPERADOS. Uso: python portao_ambiente_pilar_v413.py <ESPERADOS_v413.json>"""
import hashlib, importlib.util, json, os, platform, re, subprocess, sys, time

CHAVES = ("torch", "cuda", "numpy", "scipy", "python", "gpu")


def main(argv):
    if len(argv) != 2:
        print("uso: portao_ambiente_pilar_v413.py <ESPERADOS_v413.json>"); return 2
    rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "interpretador": sys.executable, "toca_a_placa": False}
    try:
        esp = json.load(open(argv[1], encoding="utf-8")); pil = esp["pilar"]
        cdir = pil["cache_dir"]; rj = os.path.join(cdir, "result.json")
        raw = open(rj, "rb").read(); h = hashlib.sha256(raw).hexdigest()
        hs = open(rj + ".sha256", encoding="ascii").read().strip()
        assert h == hs == pil["result_sha256"], "o result.json do cache nao confere (sha256)"
        cenv = json.loads(raw.decode("utf-8")).get("env") or {}
        cache = {k: cenv.get(k) for k in CHAVES}
        assert cache == pil["env_do_cache"], "o ambiente do cache difere do que o ESPERADOS leu"
        import numpy, scipy   # so' CPU
        spec = importlib.util.find_spec("torch")
        assert spec is not None and spec.origin, "torch nao achado"
        vtxt = open(os.path.join(os.path.dirname(spec.origin), "version.py"), encoding="utf-8").read()
        mv = re.search(r"^__version__\s*(?::[^=]+)?=\s*['\"]([^'\"]+)['\"]", vtxt, re.M); mc = re.search(r"^cuda\s*(?::[^=]+)?=\s*['\"]([^'\"]+)['\"]", vtxt, re.M)
        assert mv and mc, "torch/version.py sem __version__ ou cuda"
        r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                            "$ErrorActionPreference='Stop'; Get-CimInstance Win32_VideoController | ForEach-Object { $_.Name }; Write-Output 'NOMES_OK'"],
                           capture_output=True, text=True, timeout=60)
        nomes = [x.strip() for x in r.stdout.splitlines() if x.strip() and x.strip() != "NOMES_OK"]
        assert r.returncode == 0 and "NOMES_OK" in r.stdout, "a leitura do nome da placa falhou"
        agora = {"torch": mv.group(1), "cuda": mc.group(1), "numpy": numpy.__version__, "scipy": scipy.__version__, "python": platform.python_version(),
                 "gpu_nomes_do_windows": nomes, "torch_dir": os.path.dirname(spec.origin)}
    except Exception as e:  # noqa: BLE001
        rec.update({"veredito": "PORTAO_PILAR_ILEGIVEL", "erro": repr(e)})
        _grava(argv[1], rec); print("PORTAO_PILAR_ILEGIVEL %r" % (e,)); return 21
    dif = {k: {"cache": cache[k], "agora": agora[k]} for k in ("torch", "cuda", "numpy", "scipy", "python") if cache[k] != agora[k]}
    if cache["gpu"] not in nomes:
        dif["gpu"] = {"cache": cache["gpu"], "agora_nomes_do_windows": nomes}
    rec.update({"cache": cache, "agora": agora, "diferencas": dif, "veredito": "PORTAO_PILAR_OK" if not dif else "PORTAO_PILAR_RECUSA",
                "o_que_nao_decide": "o autoteste do motor (E1..E8) que o um.py roda na placa no reuso; se falhar, o vigia do pilar no rito para o rito na linha de calculo"})
    _grava(argv[1], rec)
    if dif:
        print("PORTAO_PILAR_RECUSA: o ambiente presente difere do cache do pilar em %s -- o um.py CALCULARIA o pilar na placa (ha treino em curso): PARAR e avisar o operador" % sorted(dif))
        return 19
    print("PORTAO_PILAR_OK: o ambiente presente (torch %s, cuda %s, numpy %s, scipy %s, python %s, placa %s) e' o do cache do pilar (chave %s)" % (
        agora["torch"], agora["cuda"], agora["numpy"], agora["scipy"], agora["python"], cache["gpu"], esp["pilar"]["key"]))
    return 0


def _grava(esp_path, rec):
    d = os.path.dirname(os.path.abspath(esp_path)); p = os.path.join(d, "PORTAO_AMBIENTE_PILAR_v413_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
