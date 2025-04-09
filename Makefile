VENV_NAME=.venv
PYTHON=$(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

help:
	@echo "Makefile commands:"
	@echo "  make setup   - Create virtual environment and install dependencies"
	@echo "  make run     - Run the application"
	@echo "  make clean   - Remove virtual environment and build artifacts"
	@echo "  make freeze  - Freeze dependencies to requirements.txt"
	@echo "  make build-linux - Build the application for Linux"

setup:
	python3 -m venv $(VENV_NAME)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	source $(VENV_NAME)/bin/activate

run:
	$(PYTHON) app

clean:
	rm -rf $(VENV_NAME) __pycache__ build dist *.spec

freeze:
	$(PIP) freeze > requirements.txt

build-linux:
	$(VENV_NAME)/bin/pyinstaller --noconfirm --onefile --windowed app/__main__.py --name s3.uploader.files
