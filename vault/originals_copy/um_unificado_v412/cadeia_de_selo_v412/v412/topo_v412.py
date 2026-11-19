# -*- coding: utf-8 -*-
"""topo_v412.py -- (modulo de CADEIA) constroi o codigo da funcao versionada de emissao do topo do resumo da v412 (_v412_topo_texto) a partir da funcao da v411 selada (_v411_topo_texto, que fica como esta, como registro):
copia o AST, troca o nome e o molde (_V411_TOPO -> _V412_TOPO), poe a docstring da v412 (sem historia de conversa) e faz o paragrafo de P = nP passar pela travessia da guarda de frases antes da emissao."""
import ast
import copy

DOC_TOPO = ("v412 -- o texto do topo do resumo (o molde _V412_TOPO), com os marcadores preenchidos na EMISSAO a partir da chave do core que a tabela `marcadores` da: o H0DN, o livro de cobrancas e a Fase 9 V2. "
            "Marcador com fonte ausente no core => o topo nao diz o resultado e diz por que; numero nao finito ou nao numerico, ou marcador que sobre no texto = PARAR (ValueError). "
            "A frase de que nenhuma cobranca foi falsificada so' sai se as falsificadas forem zero e a soma das categorias mais as falsificadas for o numero de cobrancas. "
            "O paragrafo de P = nP passa pela travessia da guarda de frases antes de ser emitido: violacao e' falha visivel. Se o registro do H0DN nao selou, devolve a frase de que nao selou.")
GUARDA_TRAVESSIA = ('_tp_ = _v412_travessia("resumo:" + lang_, {lang_: [_V412_TOPO["pnp"][lang_]]})\n'
                    'if not _tp_["ok"]:\n'
                    '    raise ValueError("a travessia da guarda de frases da v412 recusa o paragrafo do resumo (%s): %r" % (lang_, _tp_["violacoes"][:3]))')


class _RenomeiaTopo(ast.NodeTransformer):
    def visit_Name(self, n):
        if n.id == "_V411_TOPO":
            n.id = "_V412_TOPO"
        return n


def construir(fn_v411):
    f = copy.deepcopy(fn_v411)
    f.name = "_v412_topo_texto"
    assert isinstance(f.body[0], ast.Expr) and isinstance(f.body[0].value, ast.Constant), "a funcao do topo da base nao tem docstring"
    f.body[0] = ast.Expr(ast.Constant(DOC_TOPO))
    _RenomeiaTopo().visit(f)
    assert isinstance(f.body[-1], ast.Return), "a funcao do topo da base nao termina em return"
    f.body[-1:-1] = ast.parse(GUARDA_TRAVESSIA).body
    ast.fix_missing_locations(f)
    src = ast.unparse(f)
    assert "_V411_TOPO" not in src and "_v412_travessia(" in src and src.startswith("def _v412_topo_texto")
    ast.parse(src)
    return src
