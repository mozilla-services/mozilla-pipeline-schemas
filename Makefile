.PHONY: outdir dist default

JSON_IN_FILES = $(shell find src/schemas/ -type f -name '*.json.in')
TXT_IN_FILES = $(shell find src/schemas/ -type f -name '*.txt')
JSON_FILES = $(patsubst src/schemas/%.json.in, schemas/%.json, $(JSON_IN_FILES))
TXT_FILES = $(patsubst src/schemas/%.txt, schemas/%.txt, $(TXT_IN_FILES))

default: schemas

outdir:
	rm -rf schemas
	mkdir schemas

schemas/%.json: src/schemas/%.json.in
	mkdir -p `dirname $@`
	m4 m4/base.m4 m4/definitions.m4 m4/environment.m4 $< | python -mjson.tool > $@

schemas/%.txt: src/schemas/%.txt
	mkdir -p `dirname $@`
	cp $< $@

schemas: outdir $(JSON_FILES) $(TXT_FILES)
