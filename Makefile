clean:
	$(MAKE) -C src clean
	python setup.py clean
	rm -rf *.pyc *.npy __pycache__ *~ pystreamvbyte.egg-info/ *.lprof build dist *.so .eggs src/build

build:
	mkdir -p src/build
	cd src/build; cmake -D CMAKE_BUILD_TYPE=Release ..
	$(MAKE) -C src/build
	python setup.py develop

test: build
	python tests/unit
