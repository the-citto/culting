
.PHONY: base
.PHONY: build
.PHONY: check
.PHONY: dev
.PHONY: recipes
.PHONY: tests




VENV-NAME:= .venv
BIN-DIR:= $(VENV-NAME)/bin

PIP-COMPILE:= $(BIN-DIR)/pip-compile$(EXTENSION)
PYTHON:= $(BIN-DIR)/python



#

all:
	@echo
	@echo recipes:
	@echo dev
	@echo tests
	@echo check
	@echo build
	@echo

#

requirements.txt: pyproject.toml requirements.in $(PIP-COMPILE)
	$(PYTHON) -m piptools compile -o requirements.txt requirements.in

base: requirements.txt
	$(PYTHON) -m piptools sync requirements.txt


requirements-tests.txt: requirements.txt requirements-tests.in
	$(PYTHON) -m piptools compile -o requirements-tests.txt requirements-tests.in

tests: requirements.txt
	$(PYTHON) -m piptools sync requirements-tests.txt
	$(PYTHON) -m pip install -e .[tests]


requirements-dev.txt: requirements-tests.txt requirements-dev.in
	$(PYTHON) -m piptools compile -o requirements-dev.txt requirements-dev.in

dev: requirements-dev.txt
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m piptools sync requirements-dev.txt
	$(PYTHON) -m pip install -e .[dev]


check:
	@$(BIN-DIR)/pytest || true
	@echo
	@echo ------------------------------   mypy   ------------------------------
	@$(BIN-DIR)/mypy . || true
	@echo
	@echo ------------------------------   ruff   ------------------------------
	@$(BIN-DIR)/ruff check || true
	@echo
	@echo -----------------------------   pyright   ----------------------------
	@$(BIN-DIR)/pyright || true
	@echo


$(PIP-COMPILE):
	python -m venv $(VENV-NAME)
	$(PYTHON) -m pip install --upgrade pip pip-tools

#

build: dev
	$(PYTHON) -m build $(OUTDIR)




