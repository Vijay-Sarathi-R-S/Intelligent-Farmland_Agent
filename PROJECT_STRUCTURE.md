# Project Structure Overview

This document explains the current repository layout and provides a clean, understandable map of where things are and what they do. It does not change any code or paths. A safe, optional reorganization plan is included at the end, but no moves are applied by default to avoid breaking imports or deployment flows.

Repository root: Intelligent-Farmland_Agent/

- app.py
  - Likely Flask entry point for running the web application locally: `python app.py`.
- run.py
  - Alternate run script (may be used by Procfile/Render). Check Procfile for the actual entry used in production.
- config.py
  - Application configuration (loads env vars, settings).
- requirements.txt
  - Runtime Python dependencies.
- requirements-dev.txt
  - Development-only dependencies (tests, linting). If not referenced in CI, keep as a dev install helper.
- .env.example
  - Template for local environment variables. Copy to `.env` and fill secrets/keys.
- .env.render.example
  - Template for Render.com environment settings.
- .gitignore
  - Git ignore rules.
- .dockerignore
  - Docker build context ignore rules.
- .renderignore
  - Render.com build/deploy ignore rules.
- Dockerfile
  - Container build recipe (kept at root for standard `docker build .`).
- docker-compose.yml
  - Local orchestration for multi-service dev/testing.
- docker-compose.render.yml
  - Compose file tailored to Render.com or production-like configs.
- render.yaml
  - Render.com service definition and deploy settings.
- render-build.ps1
  - Build/deploy helper script for Render on Windows PowerShell.
- Procfile
  - Process type declaration for PaaS (e.g., `web: gunicorn ...` or similar).
- Makefile
  - Convenience targets for build/test/lint (optional on Windows; many targets can be run with `make <target>` in compatible shells).
- LICENSE
  - Licensing details for the repository.
- runtime.txt
  - Version pin for certain hosts (e.g., Heroku/Render).
- test.py
  - Simple test runner or utility script for invoking tests locally.
- README.md
  - Main project documentation with overview, quick start, configuration and endpoints.

Directories

- docs/
  - DEPLOYMENT.md — deployment guide and notes.
  - RENDER_FILES_SUMMARY.md — description of Render-related files and their roles.
  - RENDER_QUICKSTART.md — quick start focused on Render.com.

- services/
  - __init__.py — marks the directory as a Python package and may expose service-level APIs.
  - ai_validation.py — validation and guardrails around AI input/output.
  - analyzer.py — orchestrates the domain analysis pipeline.
  - knowledge_base.py — knowledge-base related functions or data.
  - report_generator.py — PDF or report generation routines.
  - satellite.py — satellite imagery, NDVI computations and fallbacks.
  - satellite_fixed.py — fixed/alternate satellite logic (reference or patched behavior).
  - weather.py — weather retrieval and risk evaluation.

- templates/
  - about.html — static page content.
  - index.html — main landing or dashboard.
  - login.html — authentication page.
  - splash.html — app splash/loading screen.

- tests/
  - conftest.py — pytest fixtures and shared setup.
  - test_ai_validation.py — unit tests for AI validation module.
  - test_endpoints.py — endpoint/integration tests for the Flask API.


How things fit together

- Flask application (app.py) serves routes and renders templates/ for the UI.
- Domain logic lives in services/ and is imported by views/controllers to process requests.
- External integrations:
  - Satellite/NDVI logic (services/satellite*.py)
  - Weather intelligence (services/weather.py)
  - AI/Gemini usage (via services/analyzer.py and ai_validation.py)
  - Reporting (services/report_generator.py)
- Configuration is loaded from environment variables (config.py and .env files).
- Tests verify individual services and API endpoints (tests/).
- Deployment/infra files (Dockerfile, docker-compose*, render.yaml, render-build.ps1, Procfile, runtime.txt) control how the app is built and deployed locally and in the cloud.


How to run (from README)

- Create a virtual environment and install dependencies:
  - `python -m venv venv && venv\Scripts\Activate.ps1`
  - `pip install -r requirements.txt`
- Copy .env file and fill secrets:
  - `copy .env.example .env`
- Start app:
  - `python app.py`
- Visit: http://localhost:5000


Conventions and recommendations

- Keep templates/ at root unless the Flask app explicitly sets another template_folder. Moving templates/ requires updating Flask initialization—avoid unless refactoring code as well.
- Keep services/ as-is to preserve imports like `from services.weather import ...`. Renaming/moving this package requires code updates; this document avoids such changes by design.
- Keep Dockerfile at repo root for standard Docker builds (`docker build .`).
- Render.com files (render.yaml, .renderignore, render-build.ps1) are often referenced relative to repo root; moving them may break CI/deploy.


Optional future reorganization (not applied)

For larger teams or packaging, consider the following structure. Only adopt if you can update imports, CI, and deploy references accordingly.

- src/
  - intelligent_farmland/
    - __init__.py
    - (move the contents of services/ here)
  - templates/
    - (optionally move templates under package and set Flask `template_folder`)
- deploy/
  - docker-compose.yml
  - docker-compose.render.yml
  - render.yaml
  - render-build.ps1
- infra/
  - Dockerfile (can remain at root, but infra/ is an alternative)
- tests/
  - (unchanged)
- docs/
  - (unchanged)

Migration notes if you apply the optional plan later:
- Update all imports from `services.*` to `intelligent_farmland.*` (or create a compatibility shim package named services that re-exports modules).
- If moving templates, initialize Flask app as: `Flask(__name__, template_folder="path/to/templates")`.
- Verify Procfile, render.yaml, and Docker-related contexts still point to the correct paths.


At-a-glance map (current, non-breaking)

- Application
  - app.py, run.py, config.py, templates/
- Domain/Services
  - services/ (ai_validation.py, analyzer.py, knowledge_base.py, report_generator.py, satellite.py, satellite_fixed.py, weather.py)
- Tests
  - tests/
- Docs
  - docs/ + README.md + LICENSE
- Deployment/Infra
  - Dockerfile, docker-compose.yml, docker-compose.render.yml, render.yaml, render-build.ps1, .renderignore, .dockerignore, Procfile, runtime.txt
- Dependencies/Env
  - requirements.txt, requirements-dev.txt, .env.example, .env.render.example


This file is intended to make the project clean and understandable without changing any code or paths. If you want me to apply the optional reorganization safely, I can produce an import-safe migration plan with compatibility shims and update references accordingly.
