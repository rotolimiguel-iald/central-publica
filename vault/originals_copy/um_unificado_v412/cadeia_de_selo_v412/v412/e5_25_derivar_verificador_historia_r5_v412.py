"""R5: deriva verificar_historia_texto_v412_r5.py (o original fica intacto). Duas mudancas, cada uma com a sua causa e o seu controle no autoteste:
(1) a palavra de processo ORDEM (maiusculas) e “ordem <numero>” continuam recusadas, mas a palavra comum “ordem” (a ordem de uma lista, a ordem prometida de uma cadeia) deixa de ser recusada: no original a alternativa ORDEM
    estava sob a opcao de ignorar a caixa e recusava a palavra matematica, que a pagina R18 traz (“cadeia binaria na ordem prometida”); a atribuicao (“ordem do autor”, “ordem do operador”) segue recusada pela classe propria;
(2) um identificador do kernel (nome completo de declaracao do relatorio de axiomas, ou espaco de nome do manifesto, com pelo menos um ponto) nao e' prosa: sai do texto antes do exame, e o resultado diz quantos sairam.
    A frente C conserva os espacos de nome que os autores deram (contrato R5, secao 1), e um deles coincide com um nome de modelo; a palavra SOLTA continua recusada (o autoteste confere os dois lados)."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
EU = "e5_25_derivar_verificador_historia_r5_v412.py"
NOVO_EXAMINAR = '''_IDS_KERNEL = None
RX_IDENT = re.compile(r"[A-Za-z_\\u00C0-\\u024F][\\w'\\u00C0-\\u024F]*(?:\\.[A-Za-z_\\u00C0-\\u024F][\\w'\\u00C0-\\u024F]*)+")


def identificadores_do_kernel():
    """os identificadores que nao sao prosa: os nomes completos das declaracoes publicas dos modulos novos (kernel/FLAGS_v412.json, lidos do relatorio de axiomas) e os espacos de nome que o manifesto da'; so' nomes com pelo menos um ponto"""
    global _IDS_KERNEL
    if _IDS_KERNEL is None:
        d = Path(__file__).resolve().parent
        ids = set()
        fl = d / "kernel" / "FLAGS_v412.json"
        if fl.exists():
            ids |= set(json.loads(fl.read_bytes().decode("utf-8"))["proveniencia_publicas"])
        mp = d / "insumos" / "MANIFESTO_PEDRAS_v412_R10.json"
        if mp.exists():
            for x in json.loads(mp.read_bytes().decode("utf-8"))["modulos"]:
                ids |= set(x.get("namespaces") or [])
        _IDS_KERNEL = {i for i in ids if "." in i}
    return _IDS_KERNEL


def examinar(unidades, identificadores=None):
    ids = identificadores_do_kernel() if identificadores is None else set(identificadores)
    achados, info = [], []
    n_ids = [0]

    def _tira(m):
        if m.group(0) in ids:
            n_ids[0] += 1
            return " "
        return m.group(0)
    for onde, texto in unidades:
        sem_codigo = re.sub(r"`[^`]+`", " ", texto)   # nomes de termo entre crases nao sao prosa
        sem_codigo = RX_IDENT.sub(_tira, sem_codigo)   # identificador do kernel (nome completo de declaracao ou espaco de nome) nao e' prosa
'''
derivar("verificar_historia_texto_v412.py", "verificar_historia_texto_v412_r5.py", [
    ('def examinar(unidades):\n    achados, info = [], []\n    for onde, texto in unidades:\n        sem_codigo = re.sub(r"`[^`]+`", " ", texto)   # nomes de termo entre crases nao sao prosa\n', NOVO_EXAMINAR, 1),
    ('re.compile(r"\\b[Oo]rdem\\s+\\d+|\\bORDEM\\b|', 're.compile(r"\\b[Oo]rdem\\s+\\d+|(?-i:\\bORDEM\\b)|', 1),
    ('    return {"n_unidades_examinadas": len(unidades), "achados": achados,', '    return {"n_unidades_examinadas": len(unidades), "n_identificadores_do_kernel_fora_da_prosa": n_ids[0], "achados": achados,', 1),
    ('("ordem_revisao_parecer_decisao_errata", "conforme a ordem 027"),', '("ordem_revisao_parecer_decisao_errata", "conforme a ordem 027"), ("ordem_revisao_parecer_decisao_errata", "pela ORDEM vigente"), ("atribuicao_de_fala", "por ordem do autor"), ("nome_de_pessoa_ou_modelo", "o Codex leu a âncora Codex.Modulo.termo"),', 1),
    ('LIMPAS = ["O operador do custo de uma fórmula é a penalidade dos vínculos das cláusulas.",', 'LIMPAS = ["cadeia binária na ordem prometida", "âncora Codex.Modulo.termo (Modulo): a bandeira é verdadeira", "O operador do custo de uma fórmula é a penalidade dos vínculos das cláusulas.",', 1),
    ('        r = examinar([("plantada", tx)])', '        r = examinar([("plantada", tx)], identificadores={"Codex.Modulo.termo"})', 1),
    ('        r = examinar([("limpa", tx)])', '        r = examinar([("limpa", tx)], identificadores={"Codex.Modulo.termo"})', 1),
], EU, imports=False)
import verificar_historia_texto_v412_r5 as V
a = V.autoteste()
print("autoteste:", a["n_ok"], "/", a["n"], "OK" if a["ok"] else "FALHOU", [x for x in a["itens"] if (x["classe"] == "limpa") == x["detectou"]])
sys.exit(0 if a["ok"] else 1)
