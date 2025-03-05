
.PHONY: sync
.PHONY: build
.PHONY: check
.PHONY: recipes




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
	$(PYTHON) -m pip install --upgrade pip -q
	$(PYTHON) -m piptools compile -o requirements.txt requirements.in --no-strip-extras

sync: requirements.txt
	$(PYTHON) -m piptools sync requirements.txt



dev: sync
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




