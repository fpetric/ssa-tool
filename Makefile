PIP ?= pip
PYTHON ?= python

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) ssa/core.py
#	type-check
	mypy -p ssa \
	  --ignore-missing-imports # stubs don't exist for networkx and that's ok
