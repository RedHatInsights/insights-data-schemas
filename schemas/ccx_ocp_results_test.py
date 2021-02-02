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

from voluptuous import Invalid

from ccx_ocp_results import schema
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
            "OrgID": 11789772,
            "ClusterName": "5d5892d3-1f74-4ccf-91af-548dfc9767aa",
            "LastChecked": "2020-04-02T09:00:05.268294Z",
            "Report": {
                "system": {
                    "metadata": {},
                    "hostname": None
                    },
                "reports": [],
                "fingerprints": [],
                "skips": [
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.check_ocs_version.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.OperatorsOcsMGOCS'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.check_pods_scc.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.PodsMGOCS'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.operator_phase_check.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.OperatorsOcsMGOCS'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.pvc_phase_check.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather_ocs.PersistentVolumeClaimsMGOCS'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.ocs.ceph_check_mon_clock_skew.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_rules_ocp.ocs.ceph_check_mon_clock_skew.get_mon_reporting_clock_skew'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.external.bug_rules.bug_1801300.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather.DeploymentsMG'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.external.bug_rules.bug_1802248.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_ocp_core.specs.must_gather.DeploymentsMG'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.external.rules.image_registry_pv_no_access.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_rules_ocp.common.conditions.image_registry.DegradedImageRegistryOperator', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPod', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPersistentVolumeClaim'] Any: ",
                        "type": "skip"
                        },
                    {
                        "rule_fqdn": "ccx_rules_ocp.external.rules.image_registry_pv_low_capacity.report",
                        "reason": "MISSING_REQUIREMENTS",
                        "details": "All: ['ccx_rules_ocp.common.conditions.image_registry.DegradedImageRegistryOperator', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPod', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPersistentVolumeClaim'] Any: ",
                        "type": "skip"
                        },
                    {
                            "rule_fqdn": "ccx_rules_ocp.external.rules.image_registry_no_volume_set_check.report",
                            "reason": "MISSING_REQUIREMENTS",
                            "details": "All: ['ccx_rules_ocp.common.conditions.image_registry.DegradedImageRegistryOperator', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPod', 'ccx_rules_ocp.common.conditions.image_registry.isImageRegistryPodEmptyDirVolume', 'ccx_rules_ocp.common.conditions.image_registry.isImageRegistryPodPersistentVolume'] Any: ",
                            "type": "skip"
                            },
                    {
                            "rule_fqdn": "ccx_rules_ocp.external.rules.image_registry_pv_not_bound.report",
                            "reason": "MISSING_REQUIREMENTS",
                            "details": "All: ['ccx_rules_ocp.common.conditions.image_registry.DegradedImageRegistryOperator', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPod', 'ccx_rules_ocp.common.conditions.image_registry.ImageRegistryPersistentVolumeClaim'] Any: ",
                            "type": "skip"
                            }
                    ],
                "info": [],
                "pass": []
            }
      }


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


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_without_org_id_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    del correct_message["OrgID"]
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)


@pytest.mark.parametrize("verbose", verbose)
def test_validate_message_wrong_org_id_attribute(validation_schema, verbose, correct_message):
    """Test the validation for improper payload."""
    # check with negative integer
    correct_message["OrgID"] = -1
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with string not representing number
    correct_message["OrgID"] = "foobar"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with string representing number
    correct_message["OrgID"] = "123456"
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)

    # check with different data type
    correct_message["OrgID"] = []
    # it should fail
    with pytest.raises(Invalid) as excinfo:
        validate(schema, correct_message, verbose)
