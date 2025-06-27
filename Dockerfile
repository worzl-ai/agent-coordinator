FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY run_dev.py .

# Create necessary directories
RUN mkdir -p logs \
    && mkdir -p /app/data/clients \
    && mkdir -p /app/credentials

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080
ENV CLIENT_DATA_DIRECTORY=/app/data/clients

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}

# Use uvicorn for production
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
