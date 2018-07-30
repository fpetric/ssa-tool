PIP ?= pip
PYTHON ?= python

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) ssa/core.py
