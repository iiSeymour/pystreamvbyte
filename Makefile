clean:
	$(MAKE) -C src clean
	python setup.py clean
	rm -rf *.pyc *.npy __pycache__ *~ pystreamvbyte.egg-info/ *.lprof build dist *.so .eggs

build:
	$(MAKE) -C src
	python setup.py develop

test: build
	python tests/unit
