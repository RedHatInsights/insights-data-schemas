# Copyright 2021 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for ccx_ocp_results module."""


import sys
from datetime import datetime

import pytest
from voluptuous import Invalid

from parquet_output_workload_image_layers import schema, main
from common import validate


@pytest.fixture
def validation_schema():
    """Provide standard schema to check messages."""
    return schema


# verbosity level
verbose = (True, False)


# attributes to check
attribute = (
    "cluster_id",
    "image_id",
    "layer_image_id",
    "layer_image_level",
    "first_command",
    "first_arg",
    "archive_path",
    "collected_at"
)


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
        "cluster_id": b"123e4567-e89b-12d3-a456-426614174000",
        "image_id": b"sha256:49e4b3ddcd72c0b101311c2f92512a6ed88117aa5163534746a88f2c21cf29e9",
        "layer_image_id":
        b"sha256:eac1b95df832dc9f172fd1f07e7cb50c1929b118a4249ddd02c6318a677b506a",
        "layer_image_level": 2,
        "first_command": b"safdasd",
        "first_arg": b"",
        "archive_path":
        b"archives/compressed/00/00000000-0000-0000-0000-000000000000/202102/08/002219.tar.gz",
        "collected_at": datetime.now(),
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
    with pytest.raises(ValueError):
        validate(schema, None, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_correct_message(validation_schema, verbose, correct_message):
    """Test the validation for proper message."""
    # it should not fail
    validate(schema, correct_message, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_cluster_id_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    del correct_message["cluster_id"]
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_attributes(validation_schema, verbose, correct_message,
                                             attribute):
    """Test the validation for improper payload."""
    del correct_message[attribute]
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_attributes(validation_schema, verbose, correct_message,
                                           attribute):
    """Test the validation for improper payload."""
    # check with different data type
    correct_message[attribute] = None
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)

    correct_message[attribute] = False
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)
