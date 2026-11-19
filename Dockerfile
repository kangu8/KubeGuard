
FROM python:3.14-slim

# Python configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install production dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN groupadd --system --gid 10001 kubeguard \
    && useradd --system --uid 10001 \
       --gid kubeguard kubeguard

# Copy application source
COPY --chown=kubeguard:kubeguard app/ ./app/

# Prepare writable data directory
RUN mkdir -p /app/data \
    && chown kubeguard:kubeguard /app/data

# Run without root privileges
USER kubeguard

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
