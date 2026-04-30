NAME = a_maze_ing
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

LINTFLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# --------------------------
# DEFAULT
# --------------------------

all: install run

# --------------------------
# VENV
# --------------------------

venv:
	python3 -m venv $(VENV)

# --------------------------
# INSTALL
# --------------------------

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# --------------------------
# RUN
# --------------------------

run:
	PYTHONPATH= $(PYTHON) -m $(NAME) config.txt

debug:
	PYTHONPATH= $(PYTHON) -m pdb -m $(NAME) config.txt


# --------------------------
# CLEAN
# --------------------------

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

clean-venv: clean
	rm -rf $(VENV)

# --------------------------
# LINT
# --------------------------

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . $(LINTFLAGS)

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . $(LINTFLAGS) --strict

# --------------------------
# BUILD (IMPORTANT)
# --------------------------

build:
	$(PIP) install build
	$(PYTHON) -m build

# --------------------------
# PHONY
# --------------------------

.PHONY: all venv install run debug clean clean-venv lint lint-strict build
