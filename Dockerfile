FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first (better Docker caching)
COPY requirements.txt .

# Install runtime dependencies only
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

ENV FLASK_ENV=production

# Expose app port
EXPOSE 5000

# Start with gunicorn
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000", "--workers", "2", "--timeout", "60"]
