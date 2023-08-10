#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2021 Pavel Tisnovsky
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

"""Unit tests for parquet_output_available_updates module."""

import pytest
import sys

from datetime import datetime

from voluptuous import Invalid

from parquet_output_available_updates import schema, main
from common import validate


@pytest.fixture
def validation_schema():
    """Provide standard schema to check messages."""
    return schema


# verbosity level
verbose = (True, False)

# attributes
attribute = (
    "cluster_id",
    "current_version",
    "release",
    "collected_at",
    "archive_path",
)


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
        "cluster_id": b"2f22800c-52fb-459e-9ba8-2bfd0602ee97",
        "current_version": b"4.8.12",
        "release": b"4.10.0-fc.4",
        "collected_at": datetime.now(),
        "archive_path":
            b"archives/compressed/00/00000000-0000-0000-0000-000000000000/202102/08/002219.tar.gz",
    }


def test_main_help():
    """Test the main function when -h parameter is given."""
    sys.argv.append("-h")
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 0


def test_main_input():
    """Test the main function when -i parameter is given."""
    sys.argv.append("-i test")
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 0


@pytest.mark.parametrize("verbose", verbose)
def test_validate_no_payload(validation_schema, verbose):
    """Test the validation for improper (no) payload."""
    # it should fail
    with pytest.raises(ValueError) as excinfo:
        validate(schema, None, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_correct_message(validation_schema, verbose, correct_message):
    """Test the validation for correct payload."""
    # it should not fail
    validate(schema, correct_message, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_cluster_id_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    del correct_message["cluster_id"]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_attributes(validation_schema, verbose, correct_message,
                                             attribute):
    """Test the validation for improper payload."""
    del correct_message[attribute]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_attributes(validation_schema, verbose, correct_message, attribute):
    """Test the validation for improper payload."""
    # check with an empty bytes
    correct_message[attribute] = b""
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # make sure the attribute type will be incorrect by changing its value
    if not isinstance(correct_message[attribute], int):
        # check with number
        correct_message[attribute] = 123456
    elif isinstance(correct_message[attribute], int):
        # check with string
        correct_message[attribute] = "invalid"

    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message[attribute] = []
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)
