FROM node:22-alpine AS ui
WORKDIR /ui
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements*.txt backend/requirements.lock /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt -c backend/requirements.lock
COPY backend/app /app/backend/app
COPY fixtures /app/fixtures
COPY --from=ui /ui/dist /app/frontend/dist
ENV PYTHONPATH=/app/backend PYTHONDONTWRITEBYTECODE=1
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
