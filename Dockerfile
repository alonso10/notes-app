FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && pip install --upgrade pip \
    && pip install --prefix=/install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . /app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
