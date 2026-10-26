# -*- coding: utf-8 -*-
"""Caminhos da casa (G1). Uma tabela só, com RAÍZES SUBSTITUÍVEIS para ensaios e replays (variável de ambiente
`G1_RAIZ_<NOME>` ou o argumento --raiz NOME=CAMINHO do CLI). Nada aqui lê credencial: os arquivos privados (marcadores,
termos proibidos, .env do site) são apenas NOMEADOS; quem os lê é o passo que precisa deles, só em `executar`."""
import os
from pathlib import Path

# nome -> caminho padrão (a casa, hoje)
_PADRAO = {
    "CEN": r"C:\IALD\Central de Patentes",
    "NOS": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós",
    "TB": r"C:\IALD\Artigo\the_boundary",                       # espelho (repositório git, branch main)
    "BK": r"C:\IALD\Artigo\the_boundary_BACKUPS",               # backups do espelho, fora do repositório
    "SITE": r"C:\IALD\Site\tgl\v3.0",                           # fonte do site que sobe ao ar
    "BANC": r"C:\IALD\Site\tgl\v3.0_bancada",                   # ferramentas do site (tools\, revisoes\, subidas\)
    "PUB": r"C:\IALD\Central_publica",
    "MAPA": r"C:\IALD\MAPA_DE_ROTAS",
    "ACOM": r"C:\IALD\MEMORIA_IALD",
    "NOS_VIVO": r"C:\IALD\NOS_VIVO",
    "BU": r"C:\IALD\Bancada_Um",
    "BKCEN": r"C:\IALD\Central de Patentes_BACKUPS",           # snapshots do Chatgpt\
    "APP": r"C:\IALD\projetos_pyhton\IALD",                    # o app/web server da IALD: iald_nucleo_fixo.json diz a release instalada (C21 só CONFERE)
    "MEM": str(Path.home() / ".claude" / "projects" / "c--IALD-Central-de-Patentes" / "memory"),
    "PYTHON": r"C:\Python314\python.exe",
}


class Caminhos:
    """Atributos Path para cada raiz + os derivados. `sobre` troca raízes (ensaios)."""

    def __init__(self, sobre=None):
        sobre = dict(sobre or {})
        for nome, padrao in _PADRAO.items():
            v = sobre.get(nome) or os.environ.get("G1_RAIZ_" + nome) or padrao
            setattr(self, nome, Path(v))
        self.sobre = sobre
        self._oc = Path(sobre["OC"]) if sobre.get("OC") else None
        self._atlas = Path(sobre["ATLAS"]) if sobre.get("ATLAS") else None

    # -- derivados (todos relativos às raízes acima) --
    @property
    def ESP(self):
        return self.TB / "Um (absoluto) \u2014 Grande Atrator"

    @property
    def OC(self):
        return self._oc if self._oc is not None else self.CEN / "vault" / "originals_copy"

    @property
    def ATLAS(self):
        """O Atlas da TGL (append datado, correção ao lado). Substituível só em ensaios."""
        return self._atlas if self._atlas is not None else self.CEN / "memory" / "TGL_ATLAS.md"

    @property
    def CS(self):
        return self.CEN / "work" / "cadeia_de_selo"

    @property
    def G1(self):
        return self.CEN / "work" / "custodia_G1"

    @property
    def RUNS(self):
        return self.G1 / "runs"

    @property
    def TUNEL(self):
        return self.CEN / "Chatgpt" / "TUNEL"

    @property
    def CACHE_NOS(self):
        return self.NOS.parent / "cache"

    @property
    def ROTAS_JSONL(self):
        return self.MAPA / "rotas.jsonl"

    @property
    def RAW(self):
        return "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/"

    URL_SITE = "https://teoriadagravitacaoluminodinamica.com/"

    def cofre(self, v):
        return self.OC / ("um_unificado_" + v)

    def cofre_kernel(self, v):
        return self.OC / ("tgl_kernel_" + v)

    def pasta_trabalho(self, v, data_ddmes):
        """work\\custodia_vNNN_<ddmes>\\ (a convenção da casa; ex.: custodia_v398_24out)."""
        return self.CEN / "work" / ("custodia_%s_%s" % (v, data_ddmes))

    def pastas_trabalho_existentes(self, v):
        return sorted(p for p in (self.CEN / "work").glob("custodia_%s_*" % v) if p.is_dir())

    def memoria(self, nome):
        return self.MEM / nome

    def py(self):
        return str(self.PYTHON)


def padrao():
    return Caminhos()
