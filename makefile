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
	$(info No documentation yet)

install:
	$(info No install logic yet)
	$(info If you have any idea how to do this, please...)
	$(info Please...)
