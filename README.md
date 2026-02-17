# Intelligent Farmland Agent (AgriTech)

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-unknown-yellow)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)
![License](https://img.shields.io/badge/license-MIT-green)
![Hackathon](https://img.shields.io/badge/hackathon-2026-orange)

Asset intelligence for farmland — combining satellite imagery, weather data, and AI to build auditable, time-anchored records of field activity and risk.

Company: https://www.verdex.com/

**AgriTech - Farmland Intelligence** is an AI-powered web application that provides vegetation analysis (NDVI), weather-driven risk metrics, and automated reports to support risk management, insurance verification, and precision agriculture.

---

## Table of contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Services](#services)
- [AI Integration](#ai-integration)
- [Dependencies](#dependencies)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting & Support](#troubleshooting--support)

---

## Overview

This system leverages satellite imagery, weather forecasting, and Google Gemini AI to analyze farmland health, detect anomalies, and produce actionable recommendations and PDF reports.

Use cases include crop health monitoring, yield prediction, insurance claim evidence, and regulatory reporting.

---

## Key Features

- **Satellite imagery analysis** — NDVI and vegetation metrics using NASA and other satellite providers.
- **Weather intelligence** — historical and forecasted weather to compute risk metrics.
- **AI-powered analysis** — Google Gemini-driven contextual insights and validation.
- **Automated reports** — PDF generation with charts and summaries for stakeholders.
- **Field management UI** — simple dashboard to register and analyze fields.
- **Resilient data fetching** — multi-API fallbacks to maximize availability.

---

## Quick Start

1. Create and activate a virtualenv (recommended):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1   # PowerShell on Windows
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Copy environment template and add keys:

```powershell
copy .env.example .env
# then edit .env and add GEMINI_API_KEY, SECRET_KEY, etc.
```

4. Run the app:

```powershell
python app.py
```

5. Open http://localhost:5000

---

## Configuration

Required environment variables (set in `.env`):

- `GEMINI_API_KEY` — Google Gemini API key (required)
- `SECRET_KEY` — Flask secret key (required)
- `NASA_API_KEY` — NASA API key (optional, improves satellite data availability)

---

## API Endpoints

- GET `/api/fields` — list all registered fields
- POST `/api/fields` — create a new field (body: name, latitude, longitude, acres, crop_type)
- POST `/api/fields/<field_id>/analyze` — run analysis for a field (returns NDVI, weather risks, AI insights)

Request example:

```json
POST /api/fields
{
  "name": "Field A",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "acres": 50,
  "crop_type": "Corn"
}
```

Response example:

```json
{
  "success": true,
  "analysis": {
    "field_id": "abc123",
    "vegetation_health": "Healthy",
    "ndvi_value": 0.8,
    "weather_risks": {},
    "ai_insights": "Crops appear healthy with good moisture levels...",
    "timestamp": "2026-02-17T10:30:00"
  }
}
```

---

## Services

- `services/satellite.py` — satellite data retrieval, NDVI calculation, API fallbacks
- `services/weather.py` — weather collection, risk scoring, forecast/historical support
- `services/analyzer.py` — combines satellite + weather, calls Gemini for contextual analysis
- `services/report_generator.py` — creates PDF reports with charts and findings

---

## AI Integration

Google Gemini is used to validate inputs, provide contextual insights (cause/effect), and generate human-readable recommendations included in reports.

---

## Dependencies

Core packages are listed in `requirements.txt`. Key packages include Flask, numpy, requests, google-generativeai, and reportlab.

---

## Testing

Run unit tests:

```powershell
python -m pytest -q
```

Or run the provided test runner:

```powershell
python test.py
```

---

## Contributing

- Fork the repo, create a branch, add tests and features, then open a pull request.
- Keep changes focused and add tests for new behaviors.

---

## License

Provided as-is for hackathon purposes. Consider adding an explicit license file for broader use (MIT recommended).

---

## Troubleshooting & Support

- If satellite or weather data is missing: check API keys, network access, and service availability.
- If AI responses are unexpected: verify `GEMINI_API_KEY` and review request payloads passed to the AI.
- For PDF generation issues: ensure `reportlab` is installed and output folders are writable.

If you'd like, I can also:

- add a `.github/workflows` CI stub, or
- generate a `requirements-dev.txt` with test & lint extras.

---

File: [README.md](README.md)

## Hackathon & Team

This project was created for the AgentX Hackathon by Team **FuTech**. Our team members:

1. Vijay Sarathi R.S
2. Sanjai S
3. Akhil T.T
4. Sreevidhya A

Good luck and thank you for reviewing our work!

> Made with ❤️ for smarter farming

docker compose up --build -d
docker compose -f docker-compose.dev.yml up --build