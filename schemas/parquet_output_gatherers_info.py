# Copyright 2021, 2022, 2023 Red Hat, Inc
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

import datetime

from common import cli_arguments, print_report, validate_parquet_file
from validators import (
    intTypeValidator,
    notEmptyBytesTypeValidator,
    pathToCephInBytesValidator,
    uuidInBytesValidator,
)
from voluptuous import Required, Schema

schema = Schema({
    Required("cluster_id"): uuidInBytesValidator,
    Required("name"): notEmptyBytesTypeValidator,
    Required("duration_in_ms"): intTypeValidator,
    Required("archive_path"): pathToCephInBytesValidator,
    Required("collected_at"): datetime.datetime,
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
