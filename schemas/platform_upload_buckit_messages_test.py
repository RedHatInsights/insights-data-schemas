#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2020, 2021 Pavel Tisnovsky
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

"""Unit tests for platform_upload_buckit_messages module."""

import pytest

from voluptuous import Invalid

from platform_upload_buckit_messages import schema
from common import validate


@pytest.fixture
def validation_schema():
    """Provide standard schema to check messages."""
    return schema


# verbosity level
verbose = (True, False)


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
        "account": "12345678",
        "category": "test",
        "metadata": {
            "reporter": "",
            "stale_timestamp": "0001-01-01T00:00:00Z"
            },
        "request_id": "1234567890abcdef1234567890abcdef",
        "principal": "87654321",
        "service": "openshift",
        "size": 123456,
        "url": "https://hostname.s3.amazonaws.com/first-part?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=credential-info&X-Amz-Date=creation-date&X-Amz-Expires=expiration-time&X-Amz-SignedHeaders=host&X-Amz-Signature=signature",  # noqa E501
        "b64_identity": "ewogICJpZGVudGl0eSI6IHsKICAgICJpbnRlcm5hbCI6IHsKICAgICAgIm9yZ19pZCI6ICIxMjM0NTYiLAogICAgICAiYXV0aF90aW1lIjogMAogICAgfSwKICAgICJhY2NvdW50X251bWJlciI6ICI3ODkwMDAiLAogICAgImF1dGhfdHlwZSI6ICJjZXJ0LWF1dGgiLAogICAgInN5c3RlbSI6IHsKICAgICAgImNuIjogIjEyMzQ1Njc4LWFhYWEtZWVlZS1mZmZmLTAwMDAwMDAwMDAwMCIsCiAgICAgICJjZXJ0X3R5cGUiOiAic3lzdGVtIgogICAgfSwKICAgICJ0eXBlIjogIlN5c3RlbSIKICB9LAogICJlbnRpdGxlbWVudHMiOiB7CiAgICAiaW5zaWdodHMiOiB7CiAgICAgICJpc19lbnRpdGxlZCI6IHRydWUsCiAgICAgICJpc190cmlhbCI6IGZhbHNlCiAgICB9LAogICAgImZvbyI6IHsKICAgICAgImlzX2VudGl0bGVkIjogdHJ1ZSwKICAgICAgImlzX3RyaWFsIjogdHJ1ZQogICAgfSwKICAgICJiYXIiOiB7CiAgICAgICJpc19lbnRpdGxlZCI6IGZhbHNlLAogICAgICAiaXNfdHJpYWwiOiBmYWxzZQogICAgfSwKICAgICJiYXoiOiB7CiAgICAgICJpc19lbnRpdGxlZCI6IHRydWUsCiAgICAgICJpc190cmlhbCI6IHRydWUKICAgIH0KICB9Cn0K",  # noqa E501
        "timestamp": "2020-12-09T16:17:42.822020204Z"
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
def test_validate_message_without_account_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    del correct_message["account"]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_account_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    # check with string not representing number
    correct_message["account"] = "foobar"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with number
    correct_message["account"] = 123456
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["account"] = []
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)
