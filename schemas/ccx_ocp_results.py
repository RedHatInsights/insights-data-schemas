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

"""Validator for messages stored in ccx.ocp.results topic."""

import sys

from voluptuous import Schema
from voluptuous import Required, Optional
from voluptuous import Any
from voluptuous import ALLOW_EXTRA

from validators import *

from common import read_control_code, cli_arguments, load_json_from_file
from common import validate_single_message, validate_multiple_messages
from common import print_report

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
            Required("error_key"): keyValueValidator,
            Required("type"): "rule",
            })

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
            })

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
            })

# Schema for messages consumed from ccx.ocp.results Kafka topic
schema = Schema(
         {Required("OrgID"): posIntValidator,
          Required("ClusterName"): uuidValidator,
          Required("LastChecked"): timestampValidatorMs,
          Required("Report"): Schema(
              {
                  Required("system"): Schema(
                      {
                          Required("metadata"): dict,
                          Required("hostname"): Any(None, str),
                      }, extra=ALLOW_EXTRA),
                  Required("reports"): [reportsSchema],
                  Required("fingerprints"): [fingerprintsSchema],
                  Required("skips"): [skipsSchema],
                  Required("info"): [infoSchema],
                  Optional("pass"): [passSchema],
              })
          })


def main():
    """Entry point to this script."""
    # Parse all CLI arguments.
    args = cli_arguments()
    verbose = args.verbose
    multiple = args.multiple
    input_file = args.input

    if multiple:
        report = validate_multiple_messages(schema, input_file, verbose)
    else:
        report = validate_single_message(schema, input_file, verbose)

    print_report(report, args.nocolors)


if __name__ == "__main__":
    main()
