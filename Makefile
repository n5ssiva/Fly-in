# ============================================================
# Fly-in — Makefile
# Assumes: main.py at repo root, source in ./flyin package,
# map files in ./maps, tests in ./tests, uv-managed environment.
# ============================================================

MAIN := main.py
MAP  ?= maps/easy_1.txt

.PHONY: all install run debug lint lint-strict test clean fclean re

all: install

# --- Setup ---------------------------------------------------
# uv sync reads pyproject.toml + uv.lock, creates/updates .venv,
# and installs both runtime (pygame) and dev (flake8/mypy/pytest)
# dependencies. No manual "source venv/bin/activate" needed.

install:
	uv sync

# --- Execution -------------------------------------------------
# Override the map with: make run MAP=maps/hard_2.txt
# "uv run" transparently makes sure the venv is in sync before
# running, then executes inside it.

run:
	uv run $(MAIN) $(MAP)

debug:
	uv run python3 -m pdb $(MAIN) $(MAP)

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf .venv
