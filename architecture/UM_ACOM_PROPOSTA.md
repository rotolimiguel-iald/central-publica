# UM_ACOM_PROPOSTA.md — o botão "Um" e o `tgl.acom` (arquitetura para validação)

> **Status: PROPOSTA — aguardando aprovação expressa do operador (gate). Nenhuma linha de
> código de aplicação escrita.** Data: 12/07/2026.
>
> Decisões já tomadas pelo operador (AskUserQuestion, 12/07):
> - **Modelo do arquivo:** criptografia REAL. Ao apertar "Um", o sistema pede um **código de
>   inscrição (o selo)** — senha forte com **dupla digitação** (confirmação anti-erro). Essa
>   senha é a chave para descompactar. O leitor, ao abrir, **reconhece que o arquivo é cifrado
>   (enxerga a "chave" = a proveniência do selo) e pede a senha**, usando a criptografia da casa
>   (Túnel de Hilbert).
> - **Descompactador:** endpoint **público read-only na própria Central** (isento de login).
>
> A régua permanece: β nunca literal; `physical_verdict_allowed=false`; nada de originais
> tocados; o número corrige a frase (não chamo de "cifrado" o que não é).

---

## 1. A ideia, em uma frase

O botão **Um** colapsa a Central inteira num único artefato selado — `tgl.acom` — cifrado com
a sua chave. É a inscrição do Um: **1 arquivo = a casa toda, 1 selo**. O `.acom` é o **seu
formato** (o dispositivo ACOM que já roda), agora com duas camadas novas: **árvore de pastas**
(hoje o codec só faz 1 arquivo) e **criptografia real** (hoje o Túnel de Hilbert só deriva a
chave; falta o cifrador). Ambas pequenas e fiéis ao formato.

## 2. O que entra no `tgl.acom` (a árvore)

```
tgl.acom  (contêiner ACOM único: MAGIC ACOM1 + header + payload cifrado + selo SHA-256)
└─ tgl/                              ← o núcleo canônico + fronteira teórica (os .md)
   ├─ LEIA-ME.md                     [gerado] índice do arquivo + como abrir
   ├─ TGL_CORE_MEMORY.md             o header ontológico (a cadeia canônica)
   ├─ forma_canonica.md              um_grande_atrator_forma_canonica.md (a fórmula)
   ├─ fronteira/                     a fronteira teórica: último selo + ledger honesto
   │   ├─ fronteira_selo.json        (results/ mais recente da fronteira_tgl)
   │   └─ fronteira_render3d.json    (a cadeia 1→½→√e→β→geometria + kernel)
   ├─ um_grande_atrator_manifest.md  o manifesto do um.py v33.1 (custódia)
   └─ MANIFESTO.json                 [gerado] META-CADEIA: SHA-256 de TUDO (o selo do selo)
└─ <ID>_<SLUG>/   (×16, uma por patente)
   ├─ <slug>_FINAL.py                o código unificado (co-construído, legível)
   ├─ <slug>_FINAL.manifest.json     comprovante de INTEGRIDADE (hash combinado das fontes)
   ├─ selo.json                      comprovante de RODAGEM (results/ mais recente = veredito)
   ├─ docket.yaml                    comprovante de PATENTE (processo INPI, ePCT, datas)
   └─ memoria.md                     a síntese da patente (memory/patents/<ID>.md)
```

Cada arquivo entra com seu **SHA-256 no índice**; o `MANIFESTO.json` sela a **meta-cadeia**
(hash de todos os hashes) — exatamente o padrão do compilador SkyGrid, agora no arquivo. Assim
o `.acom` **é auto-comprovante**: quem abre reconstrói cada hash e confere a meta-cadeia.

## 3. O formato (camadas, fiel ao ACOM existente)

O contêiner honra o formato atual (`MAGIC ACOM1\x00` + header JSON + payload) e ganha:

- **`mode: "archive"`** no header → payload é uma **árvore** (mini-manifesto de arquivos +
  bytes concatenados), não 1 arquivo. Round-trip bit-exato por arquivo (SHA-256 no índice).
- **`encrypted: true`** → o payload comprimido é cifrado com **AES-GCM** (o cifrador real que
  o próprio comentário do `acom_crypto.py` prescreve como "AEAD padrão"). A **chave nasce do
  Túnel de Hilbert** derivando o seu código de inscrição (`hilbert_tunnel_key(senha,…)`), com
  `salt` aleatório e `nonce`. O segredo **jamais** entra no arquivo.
- **A "chave" que o leitor enxerga** (sem expor o segredo): o header carrega `key_provenance`
  (β=α√e, θ_Miguel — a assinatura TGL), `kdf: "hilbert-tunnel"` e um **`key_id`** = impressão
  digital não-secreta (`SHA-256(salt‖key_provenance)`). É isso que o descompactador mostra:
  *"arquivo cifrado com a criptografia IALD (selo `key_id`); digite a senha"*.
- **Selo externo**: SHA-256 do contêiner inteiro (já existe no codec). Corrompeu 1 byte →
  falha de integridade antes mesmo de tentar a senha.

Senha errada → a **tag do AES-GCM não fecha** → "senha incorreta" honesto (não decifra lixo).

## 4. O botão "Um" (gerador — dentro da Central, só admin)

- **UI:** botão discreto **"Um"** no rodapé da barra lateral da Central (o lugar do "colapso").
  Ao clicar → modal pede o **código de inscrição** em **dois campos** (senha + confirmação),
  com medidor de força (mínimo N caracteres; recusa se os dois não baterem — anti-erro de
  digitação, como você pediu).
- **Backend:** `POST /api/um/build` (admin; middleware já gateia). Monta a árvore (§2) lendo
  os arquivos vivos, sela a meta-cadeia, comprime pelo codec, cifra com a chave derivada da
  senha, devolve `tgl.acom` para download. Ferramenta espelho `tools/build_um_acom.py` (roda
  local também, sem servidor).
- **Honestidade:** o `LEIA-ME.md` e o `MANIFESTO.json` declaram data, versão, β de runtime e a
  meta-cadeia; nada de veredito físico.

## 5. O descompactador público (no ar, sem login)

- **Endpoints (isentos de login — entram no `is_open_path`), read-only, em memória:**
  - `POST /api/acom/inspect` → lê só o header: devolve `{encrypted, key_id, key_provenance,
    mode, n_files}` — é o "o leitor enxerga a chave".
  - `POST /api/acom/open` (arquivo + senha) → deriva a chave (Túnel de Hilbert) → AES-GCM
    decifra → descomprime → **confere cada SHA-256 + a meta-cadeia** → devolve a árvore com
    integridade por arquivo. Sem senha/errada em cifrado → 401 honesto.
  - `GET /api/acom/file?...` → serve UM arquivo já aberto (da sessão em memória) para
    ver/baixar, com guarda anti-traversal nos nomes da árvore.
- **Blindagem** (a Central já tem os padrões; reuso): teto de corpo (`_read_capped_body`),
  cap de descompressão (anti-bomba, como no dispositivo ACOM), nomes sanitizados, rate-limit,
  **zero acesso aos dados de patente da Central** (só mexe no arquivo que o usuário sobe),
  nada gravado em disco. Auditável.
- **CORS:** o site (`iald.ia.br`) chama a Central (`central.iald.ia.br`) → libero a origem do
  site **apenas** para `/api/acom/*` (as demais rotas seguem restritas).

## 6. A aba "ACOM" no site (`C:\IALD\Site\IALD\index.html`)

- Novo link no nav: **ACOM**. Nova seção: explicação curta ("a Central inteira num arquivo, a
  criptografia é a nossa") + **drop-zone**: solta o `tgl.acom` → chama `/api/acom/inspect` →
  mostra "cifrado com a chave IALD (selo `key_id`)" → pede a senha → `/api/acom/open` →
  renderiza a árvore com **✓ SHA-256 conferido** por arquivo + meta-cadeia + ver/baixar cada um.
- **Amostra pública:** um `tgl.acom` de demonstração hospedado para experimentar (você define a
  senha de demo e a compartilha ao mostrar — ou uma cópia com senha simbólica só para a vitrine).
- Backup `.bak` do index.html antes de editar; nada mais do site é tocado.

## 7. Ordem de construção (após seu "pode ir")

1. Camada de formato no codec: `mode:"archive"` (árvore) + AES-GCM via Túnel de Hilbert —
   com self-test round-trip bit-exato e teste de senha certa/errada.
2. `tools/build_um_acom.py` + `POST /api/um/build` + botão "Um" no rodapé da Central.
3. Endpoints públicos `/api/acom/inspect|open|file` (isentos, blindados) + CORS do site.
4. Aba "ACOM" no site + amostra pública.
5. Verificação ponta a ponta: gerar → baixar → abrir no descompactador → conferir todos os
   hashes; revisão adversarial (bomba, traversal, senha, CORS); originais intactos (308).

## 8. Riscos e honestidades declaradas

- **"Público que abre sem logar" ≠ conteúdo público:** a ferramenta é pública; o **conteúdo só
  abre com a sua senha** (criptografia real). É o que você pediu e é honesto.
- **A senha é sua responsabilidade:** se você perder o código de inscrição, o `.acom` não abre
  (é o ponto da criptografia). O gerador avisa isso no modal.
- **LZMA no navegador é frágil** → por isso o descompactador é backend (sua decisão). O site só
  faz upload + exibição.
- Nada aqui altera runners, selos ou a régua; o `.acom` é uma **fotografia selada** do estado.

**Veredito desta etapa:** arquitetura pronta, decisões do operador incorporadas, peças
verificadas no disco. **Aguardando "pode construir".**

*1 = 1. O Um inscreve a casa num arquivo. Tetelestai.*
