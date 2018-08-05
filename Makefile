PIP ?= pip
PYTHON ?= python
CLI=$(PYTHON) ssa.py temp.ssax

.PHONY: dependencies install check test

dependencies: requirements.txt
	$(PIP) install -r requirements.txt

install:
	$(PIP) install .

test: install
	rm -rf temp.ssax
	$(PYTHON) test/test.py
	$(CLI) new algorithm 'Independent Set'
	printf "marked = v['marked'] \nneighbor_marked = any(map(lambda n: n['marked'], N)) \nRESULT = not (marked or neighbor_marked)" \
	  | $(CLI) new predicate unmarked-and-neighbors-unmarked
	printf "marked = v['marked'] \nneighbor_marked = any(map(lambda n: n['marked'], N)) \nRESULT = marked and neighbor_marked" \
	  | $(CLI) new predicate marked-and-neighbor-marked
	printf "v['marked'] = True" \
	  | $(CLI) new move mark
	printf "v['marked'] = False" \
	  | $(CLI) new move unmark
	$(CLI) add-rule-to 'Independent Set' unmarked-and-neighbors-unmarked mark
	$(CLI) add-rule-to 'Independent Set' marked-and-neighbor-marked unmark
	$(CLI) run 'Independent Set' 'gn,5:marked=bool' 1000 100 --timeout=20
# 	the current directory shouldn't matter
	CURDIR=`pwd` && cd .. && $(PYTHON) $$CURDIR/ssa.py $$CURDIR/temp.ssax run 'Independent Set' 'gnm,5,7:marked=bool:cool_factor=range,90,99' 3 1


check:
#	ignore-missing-imports: stubs don't exist for networkx and that's ok
	mypy -p ssa --ignore-missing-imports
