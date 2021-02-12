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

"""Validator for messages consumed from SQS."""

import sys

from voluptuous import Schema
from voluptuous import Required, Optional
from voluptuous import Any
from voluptuous import ALLOW_EXTRA

from validators import *

from common import read_control_code, cli_arguments, load_json_from_file
from common import validate_single_message, validate_multiple_messages
from common import print_report

# Schema for HTTP headers data structure
httpHeadersSchema = Schema(
        {
            Required("x-amzn-requestid"): uuidValidator,
            Required("date"): str,
            Required("content-type"): "text/xml",
            Required("content-length"): posIntInStringValidator,
         })

# Schema for response metadata data structure (sub-node in the main JSON)
responseMetadataSchema = Schema(
        {
            Required("RequestId"): uuidValidator,
            Required("HTTPStatusCode"): posIntValidator,
            Required("RetryAttempts"): posIntOrZeroValidator,
            Required("HTTPHeaders"): httpHeadersSchema,
         })

# Schema for attributes data structure
attributesSchema = Schema(
        {
            Required("SenderId"): posIntInStringValidator,
            Required("ApproximateFirstReceiveTimestamp"): posIntInStringValidator,
            Required("ApproximateReceiveCount"): posIntInStringValidator,
            Required("SentTimestamp"): posIntInStringValidator,
         })

# Schema for message data structure (sub-node in the main JSON)
messageSchema = Schema(
        {
            Required("MessageId"): uuidValidator,
            Required("ReceiptHandle"): posIntInStringValidator,
            Required("MD5OfBody"): md5Validator,
            Required("Body"): jsonInStrValidator,
            Required("Attributes"): attributesSchema,
         })

# Schema for messages consumed from SQS
schema = Schema(
        {
            Required("ResponseMetadata"): responseMetadataSchema,
            Optional("Messages"): [messageSchema],
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
