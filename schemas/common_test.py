#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2021, 2022, 2023 Pavel Tisnovsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for common module."""

import pytest
import contextlib
import io

from os import path

from voluptuous import Schema
from voluptuous import Invalid

from common import read_control_code, load_json_from_file
from common import validate_single_message
from common import try_to_validate_message
from common import try_to_validate_message_from_parquet
from common import validate_multiple_messages
from common import validate_parquet_file
from common import print_report


def test_read_control_code():
    """Test the function read_control_code."""
    # first test
    cc = read_control_code("setab 1")
    assert cc is not None
    assert cc[0] == "\x1b"

    # second test
    cc = read_control_code("sgr0")
    assert cc is not None
    assert cc[0] == "\x1b"


def path_to_json(filename):
    """Get a real path to JSON with data."""
    return path.join(path.dirname(__file__), "test_data", filename)


def test_load_json_from_file():
    """Test the function load_json_from_file."""
    path_to_payload = path_to_json("test.json")
    payload = load_json_from_file(path_to_payload, True)

    # check the loaded payload
    assert payload is not None
    assert "foo" in payload
    assert payload["foo"] == "bar"


def test_validate_single_message_empty_data():
    """Test the function validate_single_message."""
    schema = Schema({})
    path_to_payload = path_to_json("empty.json")

    # try to validate empty JSON file
    result = validate_single_message(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 1
    assert result["valid"] == 1
    assert result["invalid"] == 0
    assert result["error"] == 0


def test_validate_single_message_error_data():
    """Test the function validate_single_message."""
    schema = Schema({})
    path_to_payload = path_to_json("error.json")

    # try to validate JSON file containing errors
    result = validate_single_message(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 0
    assert result["valid"] == 0
    assert result["invalid"] == 1
    assert result["error"] == 0


def test_validate_single_message_no_data():
    """Test the function validate_single_message."""
    schema = Schema({})

    # try to validate JSON file that does not exists
    result = validate_single_message(schema, "this_does_not_exists.json", True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 0
    assert result["valid"] == 0
    assert result["invalid"] == 0
    assert result["error"] == 1


def test_try_to_validate_message_empty_data():
    """Test the function try_to_validate_message."""
    schema = Schema({})
    payload = "{}"

    # try to validate empty JSON file
    try_to_validate_message(schema, payload, 1, True)


def test_try_to_validate_message_wrong_data():
    """Test the function try_to_validate_message."""
    schema = Schema({})
    payload = "{\"foo\":\"bar\"}"

    # it should fail
    with pytest.raises(Invalid):
        try_to_validate_message(schema, payload, 1, True)


def test_try_to_validate_message_invalid_data():
    """Test the function try_to_validate_message."""
    schema = Schema({})
    payload = "{xyzzy}"

    # it should fail
    with pytest.raises(Exception):
        try_to_validate_message(schema, payload, 1, True)


def test_try_to_validate_message_from_parquet_empty_data():
    """Test the function try_to_validate_message_from_parquet."""
    schema = Schema({})
    payload = {}

    # try to validate empty message
    try_to_validate_message_from_parquet(schema, payload, 1, True)


def test_try_to_validate_message_from_parquet_wrong_data():
    """Test the function try_to_validate_message_from_parquet."""
    schema = Schema({})
    payload = {"foo": "bar"}

    # it should fail
    with pytest.raises(Invalid):
        try_to_validate_message_from_parquet(schema, payload, 1, True)


def test_validate_multiple_messages_correct_file():
    """Test the function validate_multiple_messages."""
    schema = Schema({})
    path_to_payload = path_to_json("multiple_ok.json")

    # try to validate JSON file without errors
    result = validate_multiple_messages(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 2
    assert result["valid"] == 2
    assert result["invalid"] == 0
    assert result["error"] == 0


def test_validate_multiple_messages_incorrect_file():
    """Test the function validate_multiple_messages."""
    schema = Schema({})
    path_to_payload = path_to_json("multiple_incorrect.json")

    # try to validate JSON file without errors
    result = validate_multiple_messages(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 2
    assert result["valid"] == 0
    assert result["invalid"] == 2
    assert result["error"] == 0


def test_validate_multiple_messages_correct_and_incorrect_file():
    """Test the function validate_multiple_messages."""
    schema = Schema({})
    path_to_payload = path_to_json("multiple_correct_and_incorrect.json")

    # try to validate JSON file without errors
    result = validate_multiple_messages(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 2
    assert result["valid"] == 1
    assert result["invalid"] == 1
    assert result["error"] == 0


def test_validate_multiple_messages_wrong_file():
    """Test the function validate_multiple_messages."""
    schema = Schema({})
    path_to_payload = path_to_json("error.json")

    # try to validate JSON file without errors
    result = validate_multiple_messages(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 1
    assert result["valid"] == 0
    assert result["invalid"] == 1
    assert result["error"] == 0


def test_validate_multiple_nonexistent_file():
    """Test the function validate_multiple_messages."""
    schema = Schema({})
    path_to_payload = "this_does_not_exists"

    # try to validate JSON file without errors
    result = validate_multiple_messages(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 0
    assert result["valid"] == 0
    assert result["invalid"] == 0
    assert result["error"] == 1


def test_validate_parquet_file_nonexistent_file():
    """Test the function validate_parquet_file."""
    schema = Schema({})
    path_to_payload = "this_does_not_exists"

    # try to validate Parquet file that does not exists
    result = validate_parquet_file(schema, path_to_payload, True)

    # validate result
    assert result is not None
    assert "processed" in result
    assert "valid" in result
    assert "invalid" in result
    assert "error" in result

    # validate counters
    assert result["processed"] == 0
    assert result["valid"] == 0
    assert result["invalid"] == 0
    assert result["error"] == 1


def test_print_report_in_case_of_no_error():
    """Test the function print_report."""
    result = {
            "processed": 2,
            "valid": 2,
            "invalid": 0,
            "error": 0
            }

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_report(result, True)
    output = f.getvalue()

    print(output)

    expected = """
Status:
Processed messages: 2

Valid messages:     2
Invalid messages:   0
Errors detected:    0

Summary:
[OK]: all messages have proper format
"""
    assert output == expected


def test_print_report_in_case_of_invalid_data():
    """Test the function print_report."""
    result = {
            "processed": 2,
            "valid": 1,
            "invalid": 1,
            "error": 0
            }

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_report(result, True)
    output = f.getvalue()

    print(output)

    expected = """
Status:
Processed messages: 2

Valid messages:     1
Invalid messages:   1
Errors detected:    0

Summary:
[WARN]: invalid messages detected
"""
    assert output == expected


def test_print_report_in_case_of_error():
    """Test the function print_report."""
    result = {
            "processed": 1,
            "valid": 2,
            "invalid": 3,
            "error": 4
            }

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_report(result, True)
    output = f.getvalue()

    print(output)

    expected = """
Status:
Processed messages: 1

Valid messages:     2
Invalid messages:   3
Errors detected:    4

Summary:
[FAIL]: invalid JSON(s) detected
"""
    assert output == expected


def test_print_report_use_colors():
    """Test the function print_report."""
    result = {
            "processed": 2,
            "valid": 2,
            "invalid": 0,
            "error": 0
            }

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        print_report(result, False)
    output = f.getvalue()

    print(output)

    assert "Status:" in output
    assert "Processed messages:" in output
    assert "Valid messages:" in output
    assert "Invalid messages:" in output
    assert "Errors detected:" in output
    assert "Summary:" in output
    assert "[OK]" in output
    assert "all messages have proper format" in output
