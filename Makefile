clean:
	$(MAKE) -C src clean
	rm -rf *.pyc *.npy __pycache__ *~ pystreamvbyte.egg-info/ *.lprof build dist

build:
	$(MAKE) -C src

test: build
	python tests/unit
