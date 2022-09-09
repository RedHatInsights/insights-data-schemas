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

"""Validator for messages stored in platform.upload.announce topic."""

import sys

from voluptuous import Schema
from voluptuous import Required
from voluptuous import ALLOW_EXTRA

from validators import *

from common import read_control_code, cli_arguments, load_json_from_file
from common import validate_single_message, validate_multiple_messages
from common import print_report


identitySchema = Schema(
        {
            Required("identity"): Schema(
                {
                    Required("internal"): Schema(
                        {
                            Required("org_id"): intInStringValidator,
                            "auth_time": int
                         }),
                    Required("account_number"): intInStringValidator,
                    "auth_type": str,
                    "system": Schema(
                        {"cn": uuidValidator,
                         "cert_type": str
                         }),
                    "type": str,
                }, extra=ALLOW_EXTRA)}, extra=ALLOW_EXTRA)


# Schema for messages consumed from platform.upload.announce Kafka topic
schema = Schema(
        {
            Required("account"): intInStringValidator,
            Required("category"): notEmptyStringValidator,
            Required("request_id"): hexaString32Validator,
            Required("principal"): intInStringValidator,
            Required("service"): notEmptyStringValidator,
            Required("size"): posIntValidator,
            Required("metadata"): Schema(
                {
                    Required("reporter"): str,
                    Required("stale_timestamp"): timestampValidator
                 }),
            Required("url"): urlToAWSValidator,
            Required("b64_identity"): lambda value: b64IdentityValidator(identitySchema, value),
            Required("timestamp"): timestampValidatorMs,
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
