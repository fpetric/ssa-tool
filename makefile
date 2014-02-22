documentation:
	$(info No prepared documentation yet)
	$(info See src/ssa.org)

install:
	python src/setup.py

check:
	$(info At least one test pops open a window with quick, discontinuous movement.)
	$(info If this kind of thing bothers you (e.g. epileptic), do not look at this test.)
	$(info At any rate, these tests are designed to be unattended.)
	$(info Press enter to confirm that you have read this message, or Ctrl-C out.)
	@read response
	nosetests --with-doctest

clean:
	find src -name *.pyc -type f | while read NAME ; do rm "$${NAME}" ; done

cleanall: clean cleanpaper
	rm -rf src/ssa
	rm -rf src/tests
	rm -f  src/setup.py
	rm -f  src/out.log
	rm -f  src/ssa.pdf
	rm -f  src/ssa.tex
	rm -f  src/ssa.tex~
