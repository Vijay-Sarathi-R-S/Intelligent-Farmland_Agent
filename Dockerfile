FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1
# Flask production mode
ENV FLASK_ENV=production

WORKDIR /app

# Install system dependencies (minimal for Render free tier)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first (better Docker caching)
COPY requirements.txt .

# Install runtime dependencies only (no dev dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose app port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/healthz')" || exit 1

# Start with gunicorn (optimized for free tier with 1 worker)
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--worker-class", "sync", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
