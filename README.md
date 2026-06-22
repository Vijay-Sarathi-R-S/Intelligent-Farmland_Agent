# Intelligent Farmland Agent

A Flask-based farmland intelligence platform that combines satellite data, weather analysis, and AI-driven insights to support crop monitoring, risk evaluation, and report generation.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.x-black)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Render](https://img.shields.io/badge/render-deploy-ready-green)

## Overview

This project helps users:

- inspect field conditions using NDVI and weather metrics,
- review AI-assisted recommendations,
- generate PDF reports for farm risk assessment,
- run the application locally or in Docker.

## Features

- Field registration and analysis API
- NDVI-based vegetation insights
- Weather-based drought/heat/flood risk scoring
- PDF report generation
- Optional AI validation using Gemini when credentials are available
- Docker and Render deployment support

## Project Structure

- [app.py](app.py) — Flask application entry point
- [run.py](run.py) — WSGI entry point for Gunicorn/Render
- [config.py](config.py) — environment configuration
- [services](services) — analysis, weather, satellite, report, and validation logic
- [templates](templates) — HTML templates
- [tests](tests) — automated tests
- [.github/workflows](.github/workflows) — CI/CD workflows

## Quick Start

### 1) Clone and install

```bash
git clone https://github.com/Vijay-Sarathi-R-S/Intelligent-Farmland_Agent.git
cd Intelligent-Farmland_Agent
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

### 2) Configure environment

Copy the sample environment file and update the values:

```bash
copy .env.example .env
```

Required variables:

- `SECRET_KEY` — Flask session secret
- `GEMINI_API_KEY` — optional but recommended for AI summaries
- `NASA_API_KEY` — optional for improved NASA-based data access

### 3) Run locally

```bash
python -m flask --app app run --host=0.0.0.0 --port=5000
```

Or use the WSGI entry point:

```bash
python run.py
```

The app will be available at http://localhost:5000.

## Docker

Build and run the container:

```bash
docker compose up --build
```

For production-style startup:

```bash
docker build -t agritech .
docker run -p 5000:5000 --env-file .env agritech
```

## Deployment

### Render

This repository includes deployment files for Render:

- [render.yaml](render.yaml)
- [Procfile](Procfile)
- [Dockerfile](Dockerfile)
- [.github/workflows/render-deploy.yml](.github/workflows/render-deploy.yml)

Set these GitHub secrets before enabling the deployment workflow:

- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`

### GitHub Actions

CI runs on every push and pull request to validate the codebase, and the deploy workflow can trigger automatically after CI succeeds on `main`.

## Testing

Run the suite locally:

```bash
python -m pytest -q
```

The tests are designed so that external API-dependent checks are skipped when credentials are not available.

## Documentation

- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [docs/RENDER_QUICKSTART.md](docs/RENDER_QUICKSTART.md)
- [docs/RENDER_FILES_SUMMARY.md](docs/RENDER_FILES_SUMMARY.md)

## License

This project is provided for educational and hackathon use. Add a formal license if you intend to distribute it publicly.

