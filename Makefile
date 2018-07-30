PIP ?= pip
PYTHON ?= python

install:
	$(PIP) install -r requirements.txt

test:
	$(PIP) install .
	$(PYTHON) test/test.py
#	type-check
	mypy -p ssa \
	  --ignore-missing-imports # stubs don't exist for networkx and that's ok
