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

"""Validator for messages consumed from ccx-XXX-insights-operator-archive-rules-results topic."""


from voluptuous import Schema
from voluptuous import Required, Optional
from voluptuous import Any
from voluptuous import ALLOW_EXTRA

from validators import *

from common import cli_arguments
from common import validate_single_message, validate_multiple_messages
from common import print_report

# Schema for metadata sub-node
metadataSchema = Schema({
        Required("cluster_id"): uuidValidator,
        Required("external_organization"): posIntInStringValidator
            })

# Schema for report "details" node
reportDetailsSchema = Schema(
        {
            Optional("current"): str,
            Optional("desired"): str,
            Optional("nodes"): [dict],
            Optional("nodes_with_different_version"): [dict],
            Optional("link"): str,
            Optional("info"): dict,
            Optional("kcs"): str,
            Optional("kcs_link"): str,
            Optional("op"): dict,
            Optional("forced_versions"): [dict],
            Required("error_key"): keyValueValidator,
            Required("type"): "rule",
            }, extra=ALLOW_EXTRA)

# Schema for info "details" node
infoDetailsSchema = Schema(
        {
            Optional("current"): str,
            Optional("desired"): str,
            Optional("cluster_id"): uuidValidator,
            Optional("grafana_link"): str,
            Required("info_key"): str,
            Required("type"): "info",
            Optional("update_time"): str,
            Optional("nodes"): [dict],
            }, extra=ALLOW_EXTRA)

# Schema for "reports" node
reportsSchema = Schema(
        {
            Required("component"): ruleFQDNValidator,
            Required("details"): reportDetailsSchema,
            Required("key"): keyValueValidator,
            Required("links"): dict,
            Required("rule_id"): ruleIDValidator,
            Required("tags"): [str],
            Required("type"): "rule",
            })

# Schema for "fingerprints" node
fingerprintsSchema = Schema(
        {
            })

# Schema for content of "skips" node from the Report
skipsSchema = Schema(
        {
            Required("rule_fqdn"): ruleFQDNValidator,
            Required("reason"): keyValueValidator,
            Required("details"): str,
            Required("type"): "skip",
            })

# Schema for "info" node
infoSchema = Schema(
        {
            Required("component"): ruleFQDNValidator,
            Required("details"): infoDetailsSchema,
            Required("info_id"): str,
            Required("key"): keyValueValidator,
            Required("links"): dict,
            Required("tags"): [str],
            Required("type"): "info",
            })

# Schema for "pass" node
passSchema = Schema(
        {
            Required("pass_id"): str,
            Required("component"): ruleFQDNValidator,
            Required("type"): "pass",
            Required("key"): keyValueValidator,
            Required("details"): dict,
            Required("links"): dict,
            Required("tags"): [str],
         })

# Version+commit info
versionCommitSchema = Schema({
            Required("version"): str,
            Required("commit"): Any(str, None)
        })

# Schema for plugin_sets sub-node
pluginSetsSchema = Schema({
            Required("insights-core"): versionCommitSchema,
            Required("ccx_rules_ocp"): versionCommitSchema,
            Required("ccx_ocp_core"): versionCommitSchema,
        })

# Schema for analysis_metadata sub-node
analysisMetadataSchema = Schema({
            Required("start"): timestampValidatorOffset,
            Required("finish"): timestampValidatorOffset,
            Required("execution_context"): str,
            Required("plugin_sets"): pluginSetsSchema,
        })

# Schema for report sub-nodes
reportSchema = Schema({
        Required("system"): Schema(
            {
                Required("metadata"): dict,
                Required("hostname"): Any(None, str),
                }, extra=ALLOW_EXTRA),
        Required("reports"): [reportsSchema],
        Required("fingerprints"): [fingerprintsSchema],
        Required("skips"): [skipsSchema],
        Required("info"): [infoSchema],
        Required("pass"): [passSchema],
        Required("analysis_metadata"): analysisMetadataSchema,
        })

# Schema for messages consumed from ccx-XXX-insights-operator-archive-rules-results Kafka topic
schema = Schema({
        Required("path"): pathToCephValidator,
        Required("metadata"): metadataSchema,
        Required("report"): reportSchema,
            })


def main():
    """Entry point to this script."""
    # Parse all CLI arguments.
    args = cli_arguments()
    verbose = args.verbose
    multiple = args.multiple
    input_file = args.input

    if multiple:
        # process multiple messages stored in one input file
        report = validate_multiple_messages(schema, input_file, verbose)
    else:
        # process single message stored in one input file
        report = validate_single_message(schema, input_file, verbose)

    # print report from schema validation
    print_report(report, args.nocolors)


if __name__ == "__main__":
    main()
