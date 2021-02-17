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

"""Unit tests for ccx_ocp_results module."""

import pytest
import sys

from voluptuous import Invalid

from parquet_input_features import schema, main
from common import validate


@pytest.fixture
def validation_schema():
    """Provide standard schema to check messages."""
    return schema


# verbosity level
verbose = (True, False)

# attributes to check
attribute = (
        "path",
        "metadata",
        "report",
        )


# report attributes to check
report_attribute = (
        "metadata",
        "schema",
        "data",
        )


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
            "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",  # noqa E501
            "metadata": {
                "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "external_organization": "1234567890"
                },
            "report": [
                {
                    "metadata": {
                        "feature_id": "feature_name",
                        "component": "feature.component.identifier"
                        },
                    "schema": {
                        "version": "1.0",
                        "fields": [
                            {
                                "name": "cluster_id",
                                "type": "String"
                                },
                            {
                                "name": "value",
                                "type": "Float"
                                },
                            {
                                "name": "last_transition_time",
                                "type": "DateTime"
                                }
                            ]
                        },
                    "data": [
                        {
                            "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                            "value": 123,
                            "last_transition_time": "2021-01-20T01:03:27"
                            },
                        {
                            "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                            "value": 0,
                            "last_transition_time": "2021-01-20T01:03:29"
                            }
                        ]
                    }
                ]
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
    """Test the validation for proper message."""
    # it should not fail
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
    correct_message[attribute] = b"foobar"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with number
    correct_message[attribute] = None
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message[attribute] = False
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", report_attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_report_attributes(validation_schema, verbose, correct_message,
                                                  attribute):
    """Test the validation for improper payload."""
    correct_message["report"][0][attribute] = b"foobar"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with number
    correct_message["report"][0][attribute] = -123456
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["report"][0][attribute] = None
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", report_attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_report_attributes(validation_schema, verbose, correct_message,
                                                    attribute):
    """Test the validation for improper payload."""
    del correct_message["report"][0][attribute]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)
