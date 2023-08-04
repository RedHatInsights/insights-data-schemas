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

"""Validator for messages consumed from ccx-XXX-insights-operator-archive-features topic."""


from voluptuous import Schema
from voluptuous import Required, Optional
from voluptuous import Any
from voluptuous import ALLOW_EXTRA

from validators import uuidValidator, posIntInStringValidator, posFloatInStringValidator
from validators import pathToCephValidator, timestampValidatorNoZ

from common import cli_arguments
from common import validate_single_message, validate_multiple_messages
from common import print_report

# Schema for metadata sub-node
metadataSchema = Schema({
        Required("cluster_id"): uuidValidator,
        Required("external_organization"): posIntInStringValidator
            })

# Schema for metadata sub-node in report sub-node
reportMetadataSchema = Schema({
        Required("feature_id"): str,  # TODO: more strict checking possible?
        Required("component"): str,   # TODO: more strict checking possible?
            })

# Schema for all schema fields
schemaFieldValidator = Schema({
        Required("name"): str,   # TODO: more strict checking possible?
        Required("type"): str,   # TODO: more strict checking possible?
            })

# Schema for schema sub-node
schemaSchema = Schema({
        Required("version"): posFloatInStringValidator,
        Required("fields"): [schemaFieldValidator],
            })

# Schema for data items
dataSchema = Schema({
        Required("cluster_id"): uuidValidator,
        Optional("value"): Any(int, float, str),
        Optional("last_transition_time"): timestampValidatorNoZ,
        Optional("path"): pathToCephValidator,
            }, extra=ALLOW_EXTRA)

# Schema for report sub-nodes
reportSchema = Schema({
        Required("metadata"): reportMetadataSchema,
        Required("schema"): schemaSchema,
        Required("data"): [dataSchema],
            })

# Schema for messages consumed from ccx-XXX-insights-operator-archive-features Kafka topic
schema = Schema({
        Required("path"): pathToCephValidator,
        Required("metadata"): metadataSchema,
        Required("report"): [reportSchema],
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
