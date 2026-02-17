.PHONY: help install test clean run render-build render-local deploy

help:
@echo "AgriTech - Makefile Commands"
@echo ""
@echo "Development:"
@echo "  make install         - Install all dependencies"
@echo "  make test            - Run tests"
@echo "  make run             - Run Flask dev server"
@echo "  make clean           - Clean build artifacts"
@echo ""
@echo "Docker:"
@echo "  make docker-compose  - Run with docker-compose"
@echo ""
@echo "Render Deployment:"
@echo "  make render-build    - Build for Render"
@echo "  make render-test     - Test with Render config"
@echo "  make deploy          - Deploy to Render"

install:
pip install -r requirements.txt
pip install -r requirements-dev.txt

test:
pytest -v

run:
flask run

docker-compose:
docker-compose up --build

render-build:
pip install -r requirements.txt

clean:
findstr /S /D __pycache__ . 2>nul || echo "No pycache found"
del /S *.pyc 2>nul || echo "No pyc files"
