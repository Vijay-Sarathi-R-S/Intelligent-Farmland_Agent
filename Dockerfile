FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt || true

ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Use run.py which registers robust handlers
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "--workers", "2", "--timeout", "60"]
