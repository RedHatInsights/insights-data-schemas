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

"""Unit tests for sqs_messages module."""

import pytest

from voluptuous import Invalid

from sqs_messages import schema
from common import validate


@pytest.fixture
def validation_schema():
    """Provide standard schema to check messages."""
    return schema


# verbosity level
verbose = (True, False)

# attributes to check
attribute = (
        "ResponseMetadata",
        "Messages"
        )


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
            "Messages": [
                {
                    "MessageId": "abe528f6-18a9-45a9-9871-8391ccb5c7d7",
                    "ReceiptHandle": "123",
                    "MD5OfBody": "905bbf7ea802c6043fbc0e81cafe7e5f",
                    "Body": '{"Records": [{"s3": {"object": {"key": "7307752/4e696069-edf5-44dd-9f05-fcca2d14cdf1/20200609125740-113ebefe3cdd4a62b9d0e094213bf9e9","size": 11805,"eTag": "ef140efa70e9efe79fdd71e5909713bb","sequencer": "005EDF87444DDF7525"}}}]}',  # noqa: E501
                    "Attributes": {
                        "SenderId": "321123",
                        "ApproximateFirstReceiveTimestamp": "1591707477622",
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1591707468964",
                        },
                    }
                ],
            "ResponseMetadata": {
                "RequestId": "aeb60670-75fd-5378-a1d3-5129fc68d330",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "aeb60670-75fd-5378-a1d3-5129fc68d330",
                    "date": "Tue, 09 Jun 2020 12:57:57 GMT",
                    "content-type": "text/xml",
                    "content-length": "22437",
                    },
                "RetryAttempts": 0,
                },
            }


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
def test_validate_message_without_response_metadata_attribute(validation_schema,
                                                              verbose,
                                                              correct_message):
    """Test the validation for improper payload."""
    del correct_message["ResponseMetadata"]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_response_metadata_attribute(validation_schema,
                                                            verbose,
                                                            correct_message):
    """Test the validation for improper payload."""
    # check with string not representing number
    correct_message["ResponseMetadata"] = "foobar"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with number
    correct_message["ResponseMetadata"] = 123456
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["ResponseMetadata"] = []
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["ResponseMetadata"] = {}
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
    correct_message[attribute] = -123456
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message[attribute] = None
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)
