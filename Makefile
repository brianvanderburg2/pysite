# Makefile for mrbavii.pysite


tarball: NAME=mrbavii-pysite-$(shell git describe --always)
tarball:
	mkdir -p output
	git archive --prefix=$(NAME)/ --format=tar HEAD | xz > output/$(NAME).tar.xz.temp
	mv output/$(NAME).tar.xz.temp output/$(NAME).tar.xz

clean:
	rm -rf output
	find -name "*.pyc" -delete
	find -name "*.pyo" -delete
	find -name __pycache__ -execdir rm -rf __pycache__ \; -prune


