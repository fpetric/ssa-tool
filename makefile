paper:
	cd paper && xelatex        smp > /dev/null
	cd paper && makeglossaries smp > /dev/null
	cd paper && biber          smp > /dev/null
	cd paper && xelatex        smp > /dev/null
	cd paper && xelatex        smp > /dev/null
	cd paper && xelatex        smp > /dev/null

cleanpaper:
	cd paper && rm -f *.aux        # tex
	cd paper && rm -f *.bbl        # biber
	cd paper && rm -f *.bcf        # biber
	cd paper && rm -f *.blg        # biber
	cd paper && rm -f *.glg        # makeglossaries
	cd paper && rm -f *.glo        # makeglossaries
	cd paper && rm -f *.gls        # makeglossaries
	cd paper && rm -f *.idx        # xindy
	cd paper && rm -f *.ilg        # xindy
	cd paper && rm -f *.ind        # xindy
	cd paper && rm -f *.log        # tex
	cd paper && rm -f *.out        # tex
	cd paper && rm -f *.run.xml    # biber
	cd paper && rm -f *.toc        # tex
	cd paper && rm -f *.xdv        # tex
	cd paper && rm -f *.xdy        # xindy
	cd paper && rm -f *~           # emacs
	cd paper/sections && rm -f *.aux
	cd paper/sections && rm -f *~

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
