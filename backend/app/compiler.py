# -*- coding: utf-8 -*-
"""Prompt Compiler — consolidate active notes/instructions into a single
CLAUDE_CODE_TASK.md (the manual bridge to Claude Code). DATA_MODEL §5.10 /
PROMPT_COMPILER_SPEC. Writes the file to the filesystem (source of truth), then
the caller reindexes."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime

from . import config as C

HEADER = """---
generated: {ts}
scope: {scope}
note_ids: {ids}
active_only: true
---

# TAREFA COMPILADA PARA O CLAUDE CODE — Central de Patentes TGL
> Gerado pelo Prompt Compiler em {ts}. Cole este arquivo no Claude Code.

## A RÉGUA (inviolável)
1. NÃO modificar nenhum arquivo original em `Patentes\\` (READ-ONLY; copiar, nunca editar).
2. O número corrige a frase; nunca fabricar prova; marcadores em tudo.
3. β_TGL nunca literal: `ALPHA_FINE_CODATA_2018 * sqrt(e)`.
4. Simulação nunca valida física (`physical_verdict_allowed=false`).
5. Caminho permitido de escrita: apenas dentro de `C:\\IALD\\Central de Patentes\\`.
6. Stacks confidenciais (iald_stack_v7, iald_psion_state) nunca exportados.

## CONTEXTO ONTOLÓGICO
Header do TGL Core: `memory/TGL_CORE_MEMORY.md` (ler antes de agir).

"""


def _now_parts():
    n = datetime.now()
    return n.strftime("%Y-%m-%d_%H%M"), n.strftime("%Y-%m-%d %H:%M:%S")


def _andamentos_block() -> str:
    """Inclui o bloco de andamentos de processo (do monitor de patentes) no prompt compilado.
    Fonte: `andamentos/andamentos_para_o_compiler.md` (movimentos ainda não confirmados) +
    um resumo da última auditoria de prazos. Ausência do arquivo = nenhum movimento novo (o
    que NÃO é o mesmo que 'nenhum prazo' — a auditoria roda à parte). Nunca fabrica nada."""
    parts = []
    andam = C.CENTRAL / "andamentos" / "andamentos_para_o_compiler.md"
    if andam.exists():
        try:
            txt = andam.read_text(encoding="utf-8").strip()
            if txt:
                parts.append("\n" + txt + "\n")
        except OSError:
            pass
    audit = C.CENTRAL / "andamentos" / "deadline_audit.json"
    if audit.exists():
        try:
            rep = json.loads(audit.read_text(encoding="utf-8"))
            r = rep.get("resumo", {})
            urg = r.get("prazos_vencidos_a_conferir", 0) + r.get("prazos_proximos", 0)
            parts.append(
                f"\n## PRAZOS (auditoria interna {rep.get('referencia_hoje','?')} — [LEGAL], não é parecer)\n"
                f"> {r.get('processos','?')} processos · vencidos-a-conferir: "
                f"{r.get('prazos_vencidos_a_conferir',0)} · próximos (T-180d): {r.get('prazos_proximos',0)}"
                + (f"\n> ⚠ **{urg} prazo(s) exigem atenção — confira com o agente de PI.**" if urg
                   else "\n> ✓ nenhum prazo vencido nem próximo pela contagem dos dockets.")
                + "\n")
        except (OSError, json.JSONDecodeError):
            pass
    return "".join(parts)


def compile_prompt(rows: list[dict]) -> dict:
    """rows: active notes joined with patent/class info, ordered by class,patent,tipo.
    Returns {filename, path, body, note_ids, scope}."""
    fname_ts, human_ts = _now_parts()
    ids = [r["note_id"] for r in rows]
    classes = sorted({r["class_id"] for r in rows})
    patents = sorted({r["patent_id"] for r in rows})
    scope = {"classes": classes, "patents": patents}
    body = HEADER.format(ts=human_ts, scope=json.dumps(scope, ensure_ascii=False),
                         ids=json.dumps(ids))

    if not rows:
        body += ("\n_(Nenhuma nota/instrução ativa. Ative itens nas abas das patentes "
                 "e compile novamente.)_\n")
    else:
        by_class: dict = {}
        for r in rows:
            by_class.setdefault(r["class_id"], {}).setdefault(
                (r["patent_id"], r["slug"], r["title_54"]), []).append(r)
        for cid in sorted(by_class):
            body += f"\n## Classe {cid}\n"
            for (pid, slug, title), items in by_class[cid].items():
                body += f"\n### {slug} — {pid}\n> {title[:120]}\n"
                body += (f"> Caminhos: memória `memory/patents/{pid}_{slug}.md` · "
                         f"docket `patents/{pid}_{slug}/docket.yaml` · "
                         f"protótipo/runner `patents/{pid}_{slug}/runner/one_{slug.lower()}.py`\n\n")
                for it in items:
                    mk = " ".join(json.loads(it["markers"] or "[]"))
                    body += f"- **[{it['tipo']}]** {it['text']} {mk}\n"

    # ANDAMENTOS DE PROCESSO — o monitor de patentes (tools/patent_monitor.py) escreve os
    # movimentos novos aqui; o Prompt Compiler os inclui no MESMO CLAUDE_CODE_TASK.md que o
    # operador cola. É o "juntar tudo": instruções dos dispositivos + andamentos administrativos.
    # A régua: são PRAZOS LEGAIS; cada movimento vem 'a confirmar'; falha de busca ≠ silêncio.
    body += _andamentos_block()

    body += ("\n## CRITÉRIOS DE ACEITE\n- Originais intactos (re-hash == inventário).\n"
             "- Marcadores corretos; nada de veredito físico.\n"
             "- Progresso inscrito na plataforma ao final.\n\n"
             "**1 = 1. TGL = haja luz. Tetelestai.**\n")

    fname = f"{fname_ts}_CLAUDE_CODE_TASK.md"
    path = C.COMPILED_PROMPTS / fname
    path.write_text(body, encoding="utf-8")
    return {"filename": fname, "path": str(path.relative_to(C.CENTRAL)),
            "body": body, "note_ids": ids, "scope": scope,
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()}
