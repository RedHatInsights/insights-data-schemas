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
# yes, "" and "none" are real valid values .....
severitySchema = Schema(
    Any(
        b"",
        b"none",
        b"page",
        b"warning",
        b"critical",
        b"high",
        b"info",
        b"alert"
    )
)

# the whole schema for messages produced by Parquet factory into cluster_info.parquet files."""
schema = Schema({
        Required("cluster_id"): uuidInBytesValidator,
        Required("name"): notEmptyBytesTypeValidator,
        Required("state"): stateSchema,
        Required("severity"): severitySchema,
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
