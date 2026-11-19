#!/usr/bin/env python3
"""Read public JUNO papers in memory and print selected source context.

This is bibliographic extraction only. It downloads no event-level data and runs
no statistical test. PDFs are parsed in memory and are never written to disk.
"""
from __future__ import annotations

import io
import sys
import urllib.request

from pypdf import PdfReader


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: python extrair_contexto_juno.py ARXIV_ID_OR_URL TERM [TERM ...]\n"
                         "       python extrair_contexto_juno.py ARXIV_ID_OR_URL --page N")
    arxiv_id, terms = sys.argv[1], sys.argv[2:]
    selected_page = int(terms[1]) if len(terms) == 2 and terms[0] == "--page" else None
    if selected_page is not None:
        terms = []
    url = arxiv_id if arxiv_id.startswith(("https://", "http://")) else f"https://arxiv.org/pdf/{arxiv_id}"
    request = urllib.request.Request(url, headers={"User-Agent": "K04-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    reader = PdfReader(io.BytesIO(payload))
    print(f"SOURCE {url}; pages={len(reader.pages)}; terms={terms}; selected_page={selected_page}")
    for page_number, page in enumerate(reader.pages, start=1):
        if selected_page is not None and page_number != selected_page:
            continue
        text = page.extract_text() or ""
        if all(term.casefold() in text.casefold() for term in terms):
            print(f"\n===== PDF PAGE {page_number} =====\n{text}")


if __name__ == "__main__":
    main()
