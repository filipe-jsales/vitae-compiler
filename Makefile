.PHONY: install validate build build-skip-pdf ats-check test clean

DATA ?= data/example

install:
	pip install -r requirements-dev.txt

validate:
	python src/validate.py --data $(DATA)

build: validate
	python src/build.py --data $(DATA)

build-skip-pdf:
	python src/build.py --data $(DATA) --skip-pdf

ats-check:
	python src/ats_check.py --pdf output/cv-pt.pdf --data $(DATA) --lang pt
	python src/ats_check.py --pdf output/cv-en.pdf --data $(DATA) --lang en

test:
	pytest -q

clean:
	rm -rf build output
