# -*- coding: utf-8 -*-
"""pilar_no_stdout_v413.py -- o VIGIA DO PILAR durante o rito da v413 (chamado em laco pelo rito_v413.sh; so' le o stdout canonico que o
carimbador grava em tempo real). O um.py decide o pilar logo depois da inscricao do Um e imprime UMA de duas linhas (lidas do codigo da v412,
quantum_pillar_start_v384, que a v413 nao muda: PORTAO_DO_PILAR_v413.json):
  * "[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de <data> (chave <chave>) ..."  -> o pilar NAO roda na placa;
  * "[v384] pilar quantico: o trabalhador da GPU foi lancado (PID <n>), ... chave <chave>"        -> o pilar seria CALCULADO na placa.
Saida (uma linha e o codigo): REUSO_OK <chave> (0) se a linha do reuso apareceu com a chave do ESPERADOS; CALCULA <linha> (3) se a linha do calculo
apareceu (o rito PARA na hora: ha' treino em curso na placa); CHAVE_ERRADA <chave> (4) se o reuso veio com outra chave; AINDA_NAO (1) se nenhuma
apareceu; ERRO (2) se nao leu. Uso: python pilar_no_stdout_v413.py <rodada_v413_stdout.txt> <ESPERADOS_v413.json>"""
import json, re, sys

RE_REUSO = re.compile(r"pilar quantico: REAPROVEITADO da rodada[^\n]*\(chave ([0-9a-f]{24})\)")
RE_CALC = re.compile(r"pilar quantico: o trabalhador da GPU foi lancado[^\n]*")


def decidir(texto, chave):
    m_c = RE_CALC.search(texto)
    if m_c:
        return "CALCULA " + m_c.group(0)[:200], 3
    m_r = RE_REUSO.search(texto)
    if m_r:
        return (("REUSO_OK " + m_r.group(1)), 0) if m_r.group(1) == chave else (("CHAVE_ERRADA " + m_r.group(1)), 4)
    return "AINDA_NAO", 1


def main(argv):
    if len(argv) != 3:
        print("ERRO uso: pilar_no_stdout_v413.py <stdout> <ESPERADOS_v413.json>"); return 2
    try:
        chave = json.load(open(argv[2], encoding="utf-8"))["pilar"]["key"]
        with open(argv[1], "rb") as f:
            texto = f.read(4 * 1024 * 1024).decode("utf-8", "replace")   # a decisao sai nas primeiras linhas; 4 MiB bastam
    except Exception as e:  # noqa: BLE001
        print("ERRO %r" % (e,)); return 2
    linha, rc = decidir(texto, chave)
    print(linha)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
