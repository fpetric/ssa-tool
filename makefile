documentation:
	$(info No prepared documentation yet)
	$(info See src/ssa.org)

bootstrap:
	sed -n '/:shebang/,/#+END_SRC/p' README.org \
	  | tail -n +2 \
	  | sed '$$ d' > tangle.el

tangle: bootstrap
	emacs --script tangle.el

install: tangle
	python setup.py install

cleaninstall:
	rm -rf ssa.egg-info
	rm -rf build
	rm -rf dist

clean:
	rm -f tangle.el temp
	find . -name '*.py'  -type f -exec rm -rf {} \;
	find . -name '*.pyc' -type f -exec rm -rf {} \;
	find . -name '*~'    -type f -exec rm -rf {} \;

check:
	$(info At least one test pops open a window with quick, discontinuous movement.)
	$(info If this kind of thing bothers you (e.g. epileptic), do not look at this test.)
	$(info At any rate, these tests are designed to be unattended.)
	$(info Press enter to confirm that you have read this message, or Ctrl-C out.)
	@read response
	$(MAKE) _check

_check:
	cd ssa && nosetests --with-doctest --verbose

emacs24:
	wget ftp://ftp.gnu.org/pub/gnu/emacs/emacs-24.3.tar.gz
	tar -zxvf emacs-24.3.tar.gz
	cd emacs-24.3 && ./configure --with-gif=no --with-xpm=no && make

installemacs24:
	cd emacs-24.3 && make install
