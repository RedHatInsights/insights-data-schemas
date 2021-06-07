# Copyright 2021 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Validator for messages produced by Parquet factory into alerts.parquet files."""

import sys

from voluptuous import Schema
from voluptuous import Required, Optional
from voluptuous import Any
from voluptuous import ALLOW_EXTRA

from validators import *

from common import read_control_code, cli_arguments
from common import validate_parquet_file
from common import print_report


# column with information about the state of alert
stateSchema = Schema(
    Any(
        b"pending",
        b"firing"
    )
)

# column with information about the severity of the alert
# currently not used because new values keep popping up...
severitySchema = Schema(
    Any(
        b"",
        b"none",
        b"page",
        b"warning",
        b"critical",
        b"high",
        b"info",
        b"alert",
        b"error",
        b"fatal",
        b"disaster",
        b"1",
        b"2"
    )
)

# the whole schema for messages produced by Parquet factory into alerts.parquet files."""
schema = Schema({
        Required("cluster_id"): uuidInBytesValidator,
        Required("name"): notEmptyBytesTypeValidator,
        Required("state"): stateSchema,
        Required("severity"): bytesTypeValidator,
        Required("labels"): jsonInBytesValidator,
        Required("archive_path"): pathToCephInBytesValidator,
        })


def main():
    """Entry point to this script."""
    # Parse all CLI arguments.
    args = cli_arguments()
    verbose = args.verbose
    input_file = args.input

    # validate the provided Parquet file
    report = validate_parquet_file(schema, input_file, verbose)

    # print report from schema validation
    print_report(report, args.nocolors)


if __name__ == "__main__":
    main()
