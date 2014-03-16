PREBUILT_EMACS=https://dl.dropboxusercontent.com/u/17471132/emacs/emacs-24.3__Ubuntu-12.04-LTS.tgz

documentation:
	$(info No prepared documentation yet)
	$(info See src/ssa.org)
	$(info $(HOME))

bootstrap:
	sed -n '/:shebang/,/#+END_SRC/p' README.org \
	  | tail -n +2 \
	  | sed '$$ d' > tangle.el

tangle: bootstrap
	emacs --script tangle.el

install: tangle
	python setup.py install

install-clean:
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
	cd ssa && nosetests --verbose

travis-dependencies:
	make --silent _travis-emacs24-build
	make --silent _travis-emacs24-install
	emacs --version

_travis-emacs24-build:
	$(info Downloading emacs 24)
	cd $(HOME) && wget --quiet -O emacs.tgz $(PREBUILT_EMACS)
	$(info Unzipping)
	cd $(HOME) && tar -zxf emacs.tgz

_travis-emacs24-install:
	$(info Installing)
	cd $(HOME) && cd emacs && make install > /dev/null 2>&1 3>&1
