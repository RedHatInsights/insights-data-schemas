.PHONY: tests

SCHEMA_DIR=schemas
DATA_DIR=data

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
