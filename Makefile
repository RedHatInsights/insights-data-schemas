.PHONY: tests

SCHEMA_DIR=schemas
DATA_DIR=data

default: tests

tests: unit_tests cli_tests

unit_tests:
	pytest -v -p no:cacheprovider

coverage:
	pytest -v -p no:cacheprovider --cov schemas/

cli_tests:	platform_upload_buckit_messages_tests

platform_upload_buckit_messages_tests:
	${SCHEMA_DIR}/platform_upload_buckit_messages.py -i ${DATA_DIR}/platform_upload_buckit/correct.json
