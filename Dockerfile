FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . /app
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 56961
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import requests; print(requests.get('http://localhost:56961/health').status_code)" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "56961"]
