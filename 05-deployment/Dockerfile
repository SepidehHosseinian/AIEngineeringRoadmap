
# Stage 1: Build & Requirements
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime Environment
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

WORKDIR /app

# Install Python and necessary libs
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/

# Copy only the installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

# Healthcheck to ensure the service is responsive
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]