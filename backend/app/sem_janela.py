"""Subprocesso que NAO abre janela preta na tela do operador.

POR QUE ISTO EXISTE (medido em 22/08/2026, nao suposto): este backend roda sob
`pythonw.exe`, que nao tem console nenhum -- nao e' um console escondido, e' a
AUSENCIA de console. Quando um processo sem console dispara um programa de console
(schtasks, netstat, powershell, tasklist, taskkill), o Windows e' OBRIGADO a alocar
um console novo: a janela preta nasce, fica visivel e VAI PARA PRIMEIRO PLANO,
roubando o foco do teclado de quem estiver digitando.

O estrago medido: o poll de 5 em 5 minutos do App.tsx chamava /api/backup/status,
que consultava DUAS tarefas agendadas -- duas janelas por poll, cravadas no segundo
(17:21:06 / 17:26:06 / 17:31:06 ...), ~830 janelas em 68 horas. O painel do LAR
agravou o quadro ao manter a Central aberta o tempo todo.

A cura e' `CREATE_NO_WINDOW` em TODA chamada. Para que ninguem precise lembrar disso
de novo, o modulo entra no lugar do subprocess e poe a flag sozinho:

    from . import sem_janela as _subprocess     # em vez de: import subprocess

As chamadas continuam identicas; nenhuma janela nasce.
"""

from __future__ import annotations

import os
import subprocess as _sp

CREATE_NO_WINDOW = getattr(_sp, "CREATE_NO_WINDOW", 0)

# repassados para quem faz `_subprocess.PIPE`, `_subprocess.TimeoutExpired` etc.
PIPE = _sp.PIPE
DEVNULL = _sp.DEVNULL
STDOUT = _sp.STDOUT
SubprocessError = _sp.SubprocessError
CalledProcessError = _sp.CalledProcessError
TimeoutExpired = _sp.TimeoutExpired
CompletedProcess = _sp.CompletedProcess


def _calado(kw: dict) -> dict:
    """Poe a flag -- so' no Windows, onde ela existe e onde o problema mora."""
    if os.name == "nt":
        kw["creationflags"] = kw.get("creationflags", 0) | CREATE_NO_WINDOW
    return kw


def run(*a, **kw):
    return _sp.run(*a, **_calado(kw))


def Popen(*a, **kw):                                  # noqa: N802 (assinatura do stdlib)
    return _sp.Popen(*a, **_calado(kw))


def check_output(*a, **kw):
    return _sp.check_output(*a, **_calado(kw))


def check_call(*a, **kw):
    return _sp.check_call(*a, **_calado(kw))


def call(*a, **kw):
    return _sp.call(*a, **_calado(kw))
