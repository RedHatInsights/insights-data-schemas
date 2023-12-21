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

import sys

import pytest
from common import validate
from parquet_input_rule_hits import main, schema
from voluptuous import Invalid


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
        "system",
        "reports",
        "fingerprints",
        "skips",
        "info",
        "pass",
        )


@pytest.fixture
def correct_message():
    """Provide correct message to be tested."""
    return {
            "path": "archives/compressed/aa/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/202101/20/031044.tar.gz",  # noqa E501
            "metadata": {
                "cluster_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "external_organization": "1234567890",
                },
            "report": {
                "system": {
                    "metadata": {},
                    "hostname": None,
                    },
                "reports": [
                    {
                        "rule_id": "tutorial_rule|TUTORIAL_ERROR",
                        "component": "ccx_rules_ocp.external.tutorial_rule.report",
                        "type": "rule",
                        "key": "TUTORIAL_ERROR",
                        "details": {
                            "type": "rule",
                            "error_key": "TUTORIAL_ERROR",
                            },
                        "tags": [],
                        "links": {},
                        },
                    ],
                "fingerprints": [],
                "skips": [
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.check_ocs_version.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.OperatorsOcsMGOCS'] Any: ",  # noqa E501
                        "type": "skip",
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.check_pods_scc.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.PodsMGOCS'] Any: ",
                        "type": "skip",
                        },
                    ],
                "info": [],
                "pass": [],
                "analysis_metadata": {
                    "start": "2021-02-12T09:22:40.335867+00:00",
                    "finish": "2021-02-12T09:22:41.434439+00:00",
                    "execution_context": "ccx_ocp_core.context.InsightsOperatorContext",
                    "plugin_sets": {
                        "insights-core": {
                            "version": "insights-core-3.0.202-1",
                            "commit": "placeholder",
                            },
                        "ccx_rules_ocp": {
                            "version": "ccx_rules_ocp-2021.2.3-1",
                            "commit": None,
                            },
                        "ccx_ocp_core": {
                            "version": "ccx_ocp_core-2021.2.8-1",
                            "commit": None,
                            },
                        },
                    },
                },
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
def test_validate_message_wrong_attributes(validation_schema, verbose, correct_message, attribute):
    """Test the validation for improper payload."""
    correct_message[attribute] = b"foobar"
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)

    # check with number
    correct_message[attribute] = None
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message[attribute] = False
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", report_attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_report_attributes(validation_schema, verbose, correct_message,
                                                  attribute):
    """Test the validation for improper payload."""
    correct_message["report"][attribute] = b"foobar"
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)

    # check with number
    correct_message["report"][attribute] = -123456
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["report"][attribute] = None
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("attribute", report_attribute)
@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_report_attributes(validation_schema, verbose, correct_message,
                                                    attribute):
    """Test the validation for improper payload."""
    del correct_message["report"][attribute]
    # it should fail
    with pytest.raises(Invalid):
        validate(schema, correct_message, verbose)
