
# Stage 1: Build Python dependencies
FROM python:3.14-alpine3.24 AS builder

WORKDIR /build

RUN python -m venv /opt/venv

COPY requirements.txt .

RUN /opt/venv/bin/python -m pip install \
    --no-cache-dir -r requirements.txt \
    && /opt/venv/bin/python -m pip uninstall -y pip


# Stage 2: Application runtime
FROM python:3.14-alpine3.24 AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv



# Remove pip from the system Python installation
# The application dependencies are already in /opt/venv
RUN /usr/local/bin/python -m pip uninstall -y pip \
    && addgroup -S -g 10001 kubeguard \
    && adduser -S -D -u 10001 -G kubeguard kubeguard \
    && mkdir -p /app/data \
    && chown 10001:10001 /app/data



COPY --chown=10001:10001 app/ ./app/

USER 10001:10001

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
