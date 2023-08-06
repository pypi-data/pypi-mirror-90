.RECIPEPREFIX = >
.PHONY: all clean build upload

all: dist

clean:
> git clean -xdf

build:
> python setup.py build sdist

upload:
> twine upload dist/*
