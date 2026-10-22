# -*- coding: utf-8 -*-
"""ZENODO — amarrar o registro do Um: Absoluto (10.5281/zenodo.22659173) ao repositorio e ao site.

O registro publicado em 08/09/2026 nao tem NENHUM link na descricao nem 'related identifiers'. Este script:
  --dry-run  : le a metadata PUBLICA do registro (sem token) e mostra o que sera enviado;
  --apply    : com ZENODO_TOKEN no AMBIENTE (nunca em arquivo; escopo deposit:write + deposit:actions),
               faz o fluxo oficial de edicao de metadata de registro publicado:
                 POST /api/deposit/depositions/{id}/actions/edit  ->  PUT metadata  ->  POST .../actions/publish
               (edicao de metadata NAO cria versao nova nem muda o DOI).
Regua: o token e' do operador; este script o le do ambiente e nao o grava em lugar nenhum.
Uso:  set ZENODO_TOKEN=...   (na mesma janela)   ->   python tools/zenodo_update.py --apply
"""
import json
import os
import sys
import urllib.request

RID = 22659173
API = "https://zenodo.org/api"
REPO = "https://github.com/rotolimiguel-iald/the_boundary"
SITE = "https://teoriadagravitacaoluminodinamica.com/"
RAW = "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/"
A3 = "Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/"
RELATED = [
    {"identifier": REPO, "relation": "isSupplementTo", "resource_type": "software", "scheme": "url"},
    {"identifier": SITE, "relation": "isDescribedBy", "scheme": "url"},
    {"identifier": RAW + A3 + "um.py", "relation": "isIdenticalTo", "resource_type": "software", "scheme": "url"},
    {"identifier": RAW + "ESTADO_ATUAL.md", "relation": "isDescribedBy", "scheme": "url"},
    {"identifier": "10.5281/zenodo.20999495", "relation": "continues", "scheme": "doi"},
    {"identifier": "10.5281/zenodo.20564341", "relation": "continues", "scheme": "doi"},
]
PREFIXO = (
    "<p><strong>Onde ler e reproduzir · where to read and reproduce:</strong> "
    "repositório <a href=\"%s\">the_boundary</a> (GitHub) · "
    "<a href=\"%sESTADO_ATUAL.md\">ESTADO_ATUAL.md</a> (uma página: pin, gate, o que está provado, o que não está) · "
    "<a href=\"%sllms.txt\">llms.txt</a> (entrada para leitores automáticos) · "
    "<a href=\"%s%sum.py\">um.py</a> (o artefato, URL direta; sha256 e1b74a907c403538…) · "
    "<a href=\"%s%sum_absoluto_selo.json\">o selo</a> · site <a href=\"%s\">teoriadagravitacaoluminodinamica.com</a>. "
    "Rodar: <code>echo 1 | python um.py</code>.</p>\n" % (REPO, RAW, RAW, RAW, A3, RAW, A3, SITE)
)


def req(method, url, token=None, data=None):
    """Via curl (o urllib desta maquina falha o handshake TLS com zenodo.org; o curl nao). O token vai num
    arquivo de cabecalho temporario (-H @arquivo), nunca na linha de comando nem em arquivo persistente."""
    import subprocess
    import tempfile
    cmd = ["curl", "-sS", "--max-time", "180", "-X", method, "-H", "Content-Type: application/json",
           "-H", "User-Agent: central-iald-zenodo", "-w", "\n%{http_code}"]
    hdr = None
    if token:
        hdr = tempfile.NamedTemporaryFile("w", delete=False, suffix=".hdr", encoding="utf-8")
        hdr.write("Authorization: Bearer %s\n" % token)
        hdr.close()
        cmd += ["-H", "@" + hdr.name]
    body = None
    if data is not None:
        body = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
        body.write(json.dumps(data))
        body.close()
        cmd += ["--data-binary", "@" + body.name]
    cmd.append(url)
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=200).stdout.decode("utf-8", "replace")
    finally:
        for f in (hdr, body):
            if f is not None:
                try:
                    os.unlink(f.name)
                except OSError:
                    pass
    raw, _, code = out.rpartition("\n")
    status = int(code.strip() or 0)
    if status >= 400:
        raise RuntimeError("HTTP %d em %s %s: %s" % (status, method, url, raw[:300]))
    return status, (json.loads(raw) if raw.strip() else {})


def main() -> int:
    apply = "--apply" in sys.argv
    token = os.environ.get("ZENODO_TOKEN")
    if apply and not token:
        print("FAIL-CLOSED: --apply exige ZENODO_TOKEN no ambiente (nunca em arquivo).")
        return 2
    st, pub = req("GET", "%s/records/%d" % (API, RID))
    meta = pub["metadata"]
    desc = meta.get("description", "")
    ja = "the_boundary" in desc
    print("registro: %s | publicado %s | licenca %s | related hoje: %s" % (meta.get("title"), meta.get("publication_date"), (meta.get("license") or {}).get("id"), meta.get("related_identifiers")))
    print("descricao ja tem o repositorio? %s" % ja)
    nova_desc = desc if ja else PREFIXO + desc
    print("--- related_identifiers a enviar ---")
    for r in RELATED:
        print("  ", r["relation"], r["identifier"])
    print("--- prefixo da descricao ---")
    print(PREFIXO if not ja else "(mantida)")
    if not apply:
        print("\n(dry-run: nada enviado. Para aplicar: set ZENODO_TOKEN=... && python tools/zenodo_update.py --apply)")
        return 0
    dep_url = "%s/deposit/depositions/%d" % (API, RID)
    try:
        req("POST", dep_url + "/actions/edit", token)
    except RuntimeError as e:  # ja em edicao (400/409) e' aceitavel
        if "HTTP 400" not in str(e) and "HTTP 409" not in str(e):
            raise
    st, dep = req("GET", dep_url, token)
    md = dep["metadata"]
    md["related_identifiers"] = RELATED
    md["description"] = nova_desc
    st, out = req("PUT", dep_url, token, {"metadata": md})
    print("PUT metadata:", st)
    st, out = req("POST", dep_url + "/actions/publish", token)
    print("publish:", st, "| doi:", out.get("doi"))
    st, pub2 = req("GET", "%s/records/%d" % (API, RID))
    print("conferido: related agora =", len(pub2["metadata"].get("related_identifiers") or []), "| repo na descricao:", "the_boundary" in pub2["metadata"].get("description", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
