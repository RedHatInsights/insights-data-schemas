SHELL := /bin/bash

.PHONY: default tests unit_tests coverage coverage-report code-style documentation before_commit cli_tests platform_upload_announce_messages_tests pycco 

SCHEMA_DIR=schemas
DATA_DIR=data
SOURCES:=$(shell find ${SCHEMA_DIR} -name '*.py')
DOCFILES:=$(addprefix docs/packages/, $(addsuffix .html, $(basename ${SOURCES})))

default: tests

tests: unit_tests cli_tests

unit_tests:
	pytest -v -p no:cacheprovider

coverage:
	pytest -v -p no:cacheprovider --cov schemas/

coverage-report:
	pytest -v -p no:cacheprovider --cov schemas/ --cov-report=html

code-style:
	python3 tools/run_pycodestyle.py

documentation:
	pydoc3 schemas/validators.py > docs/validators.txt

before_commit: code-style unit_tests coverage

cli_tests:	platform_upload_announce_messages_tests

platform_upload_announce_messages_tests:
	${SCHEMA_DIR}/platform_upload_announce_messages.py -i ${DATA_DIR}/platform_upload_announce/correct.json

pycco: ${DOCFILES} docs/sources.md

docs/packages/%.html: %.py
	mkdir -p $(dir $@)
	pycco -l python -d $(dir $@) $^

docs/sources.md: docs/sources.tmpl.md ${DOCFILES}
	./gen_sources_md.sh
