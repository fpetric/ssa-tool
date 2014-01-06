paper:
	cd doc && xelatex        smp > /dev/null
	cd doc && makeglossaries smp > /dev/null
	cd doc && biber          smp > /dev/null
	cd doc && xelatex        smp > /dev/null
	cd doc && xelatex        smp > /dev/null
	cd doc && xelatex        smp > /dev/null

cleanpaper:
	cd doc && rm -f *.aux        # tex
	cd doc && rm -f *.bbl        # biber
	cd doc && rm -f *.bcf        # biber
	cd doc && rm -f *.blg        # biber
	cd doc && rm -f *.glg        # makeglossaries
	cd doc && rm -f *.glo        # makeglossaries
	cd doc && rm -f *.gls        # makeglossaries
	cd doc && rm -f *.idx        # xindy
	cd doc && rm -f *.ilg        # xindy
	cd doc && rm -f *.ind        # xindy
	cd doc && rm -f *.log        # tex
	cd doc && rm -f *.out        # tex
	cd doc && rm -f *.run.xml    # biber
	cd doc && rm -f *.toc        # tex
	cd doc && rm -f *.xdv        # tex
	cd doc && rm -f *.xdy        # xindy
	cd doc && rm -f *~           # emacs
	cd doc/sections && rm -f *.aux
	cd doc/sections && rm -f *~

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
	read response
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
