# ── Central de Patentes TGL — imagem de nuvem (forma = conteúdo num só container) ──
# Estágio 1: compila o frontend (React 19 / Vite)
FROM node:20-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Estágio 2: backend Python que serve a API + o frontend compilado
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONUTF8=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# dependências primeiro (cache de camada)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

# código + dados reconstrutíveis (o .dockerignore exclui venv/node_modules/dist/data/segredos/confidenciais)
COPY . /app
# o dist recém-compilado do estágio 1
COPY --from=frontend /app/frontend/dist /app/frontend/dist

EXPOSE 8765
# na partida: reconstrói o índice (SQLite descartável) e sobe em 0.0.0.0:$PORT ($PORT vem do Render).
# a auth pela sua criptografia (CENTRAL_AUTH=crypto + CENTRAL_CRYPTO_SECRET) é o portão na nuvem.
CMD ["sh", "-c", "python -m backend.app.reindex --full || true; python tools/verify_evidence.py --all || true; exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8765}"]
