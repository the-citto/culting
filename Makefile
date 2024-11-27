
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

requirements/requirements.txt: pyproject.toml requirements/requirements.in $(PIP-COMPILE)
	$(PYTHON) -m piptools compile -o requirements/requirements.txt requirements/requirements.in

base: requirements/requirements.txt
	$(PYTHON) -m piptools sync requirements/requirements.txt


requirements/requirements-tests.txt: requirements/requirements.txt requirements/requirements-tests.in
	$(PYTHON) -m piptools compile -o requirements/requirements-tests.txt requirements/requirements-tests.in

tests: requirements/requirements.txt
	$(PYTHON) -m piptools sync requirements/requirements-tests.txt
	$(PYTHON) -m pip install -e .[tests]


requirements/requirements-dev.txt: requirements/requirements-tests.txt requirements/requirements-dev.in
	$(PYTHON) -m piptools compile -o requirements/requirements-dev.txt requirements/requirements-dev.in

dev: requirements/requirements-dev.txt
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m piptools sync requirements/requirements-dev.txt
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




