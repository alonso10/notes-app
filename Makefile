VENV_DIR = venv
REQ_FILE = requirements.txt
APP_MODULE = app.main:app
HOST = 0.0.0.0
PORT = 8000

.PHONY: help install run lint format docker-build docker-up docker-down

help:
	@echo "Comandos disponibles en este Makefile:"
	@echo "  make install       - Crea entorno virtual e instala dependencias"
	@echo "  make run           - Arranca la aplicación local (FastAPI)"
	@echo "  make lint          - Ejecuta linters (ejemplo: flake8)"
	@echo "  make format        - Formatea el código (ejemplo: black, isort)"
	@echo "  make docker-build  - Construye la imagen Docker usando docker-compose"
	@echo "  make docker-up     - Levanta los servicios con docker-compose"
	@echo "  make docker-down   - Detiene los contenedores docker-compose"

install:
	@echo ">>> Creating virtual environment and setting dependencies..."
	python -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r $(REQ_FILE)
	@echo ">>> Virtual environment created in '$(VENV_DIR)' and installing completed."

run:
	@echo ">>> Starting app with Uvicorn..."
	. $(VENV_DIR)/bin/activate && uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

lint:
	@echo ">>> Checking quality code with Ruff..."
	. $(VENV_DIR)/bin/activate && ruff check

lint-fix:
	@echo ">>> Checking quality code with Ruff..."
	. $(VENV_DIR)/bin/activate && ruff check --fix

format:
	@echo ">>> Formatting the code with Ruff"
	. $(VENV_DIR)/bin/activate && ruff format

docker-build:
	@echo ">>> Building Docker image..."
	docker-compose build

docker-up:
	@echo ">>> Raising services with docker-compose..."
	docker compose up -d --build

docker-down:
	@echo ">>> Stopping and deleting containers ..."
	docker-compose down
