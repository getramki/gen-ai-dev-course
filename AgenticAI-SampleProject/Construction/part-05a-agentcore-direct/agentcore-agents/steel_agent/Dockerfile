FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy steel agent code
COPY main.py __init__.py ./

# Set environment variables
ENV PYTHONPATH=/app
ENV AWS_DEFAULT_REGION=us-east-1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check for AgentCore
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ping || exit 1

# Run the AgentCore-compliant agent
CMD ["python", "main.py"]