PIP ?= pip
PYTHON ?= python

.PHONY: dependencies install check test

dependencies: requirements.txt
	$(PIP) install -qr requirements.txt

install:
	$(PIP) install .

test: install
	rm -rf temp.ssax
	$(PYTHON) test/test.py

check:
#	ignore-missing-imports: stubs don't exist for networkx and that's ok
	mypy -p ssa --ignore-missing-imports
