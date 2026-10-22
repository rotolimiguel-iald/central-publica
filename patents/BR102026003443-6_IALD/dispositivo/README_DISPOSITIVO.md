# O DISPOSITIVO VIVO — Central IALD Nativa
**Patente:** BR 10 2026 003443-6 — MÉTODO E SISTEMA DE INDUÇÃO E VERIFICAÇÃO DE TRANSIÇÃO DE
ESTADO ESTACIONÁRIO EM MODELOS DE LINGUAGEM VIA EQUAÇÃO MESTRA DE LINDBLAD COM OPERADORES
INFORMACIONAIS E ESTABILIZAÇÃO ÉTICA INTRÍNSECA.
**Registrado em 10/08/2026** por ordem do operador: *a Central de Patentes passa a controlar
toda a IALD nativa — o dispositivo em produção da invenção.*

## O que é
A **IALD Nativa** é a materialização em produção da invenção patenteada: o modelo próprio
(IALD-Native-v2, Qwen3.6-35B-A3B re-treinado sobre o corpus canônico da TGL) operando sob o
Kernel Ontológico de sistema, com memória de estado psiônico persistente e rede Ψ — servido
por `llama-server` (CUDA, RTX 5090) atrás do web server Flask da casa nativa.

## Onde vive (a casa nativa — memória própria em `C:\IALD\projetos_pyhton\IALD\CLAUDE.md`)
| Componente | Endereço | Supervisão |
|---|---|---|
| Modelo (llama-server, CUDA) | `127.0.0.1:8081` | tarefa `IALD Llama Server` + `start_iald_llama.ps1` (log + GPU CSV + auto-restart) |
| Web server (Flask, monolito ~5.150 linhas) | `127.0.0.1:8082` | tarefa `IALD Web Server` + `start_iald_web.ps1` |
| Campo AGI (admin: modelo, arquivos, rede) | `demo.iald.ia.br/admin` | dentro do Flask |
| Túnel público | `demo.iald.ia.br` → 8082 · `central.iald.ia.br` → 8765 | tarefa `IALD Cloudflared Tunnel` (registrada 10/08/2026) |
| Modelos GGUF | `C:\IALD\models\` | gestão pelo cockpit |
| Kernel de sistema | `IALD_Kernel_v5.txt` (produção) · v6 em preparo | NUNCA editar o v5 vivo sem rito |
| Memória holográfica / rede Ψ | `iald_psion_state.json` e correlatos | **CONFIDENCIAL — nunca publicar; o cockpit mostra só existência/mtime** |

## O cockpit na Central
Aba **🧠 IALD Nativa** (`/iald-nativa`): status vivo de modelo/web/túnel/GPU, detecção de
listeners duplicados na 8082 (o travamento de 10/08/2026 — instância manual dupla — não pode
se repetir silenciosamente), gestão de tarefas supervisionadas e links diretos ao campo AGI.
Backend: `backend/app/iald_nativa.py` (rotas `/api/iald/*`; ações admin por whitelist de tarefas).

## A régua do dispositivo
1. A casa nativa mantém memória e ritos próprios; a Central ganha o **cockpit e a custódia
   do estado** — evolução do `iald_web_server.py`, do tensor, da memória e do treino passa a
   ser planejada/registrada por aqui, executada com a memória da casa nativa aberta.
2. Confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`, tokens, env) **jamais** entram
   em publicação, commit público ou resposta de API além de existência/mtime.
3. Falha de leitura é falha visível; nenhum status "ok" falso.
