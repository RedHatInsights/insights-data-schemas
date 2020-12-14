#!/usr/bin/env python3

# Copyright © 2020 Pavel Tisnovsky
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

"""Validator for messages stored in platform.upload.buckit topic."""

import json
import sys
import os
from argparse import ArgumentParser


def cli_arguments():
    """Retrieve all CLI arguments."""
    # First of all, we need to specify all command line flags that are
    # recognized by this tool.
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="name of input file",
                        action="store", default=None, type=str, required=True)
    parser.add_argument("-m", "--multiple", dest="multiple",
                        help="Input file should containg more messages, each message on one line",
                        action="store_true", default=False, required=False)
    parser.add_argument("-v", "--verbose", dest="verbose", help="make it verbose",
                        action="store_true", default=None, required=False)

    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    return parser.parse_args()


def load_json_from_file(filename, verbose):
    """Load and decode JSON file."""
    if verbose:
        print("Loading original file", filename)
    with open(filename) as fin:
        return json.load(fin)


def validate(payload, verbose):
    """Try to validate the payload against known schema."""
    pass


def validate_single_message(input_file, verbose):
    """Validate single message stored in input file."""
    try:
        payload = load_json_from_file(input_file, verbose)
        valid = validate(payload, verbose)
        return {"processed": 1,
                "valid": 1 if valid else 0,
                "error": 0}
    except Exception as e:
        print(e)
        return {"processed": 1,
                "valid": 0,
                "error": 1}


def try_to_validate_message(line, processed, verbose):
    """Try to validate one message represented by string."""
    if verbose:
        print("Reading message #{}".format(processed))
    try:
        payload = json.loads(line)
        return validate(payload, verbose), False
    except Exception as e:
        print(e)
        return False, True


def validate_multiple_messages(input_file, verbose):
    """Validate multiple messages stored in input file."""
    processed = 0
    valid = 0
    error = 0

    with open(input_file, "r") as fin:
        # iterate over all lines in the message file
        for line in fin:
            processed += 1
            v, e = try_to_validate_message(line, processed, verbose)
            if v:
                valid += 1
            if e:
                error += 1

    return {"processed": processed,
            "valid": valid,
            "error": error}


def main():
    """Entry point to this script."""
    # Parse all CLI arguments.
    args = cli_arguments()
    verbose = args.verbose
    multiple = args.multiple
    input_file = args.input

    if multiple:
        report = validate_multiple_messages(input_file, verbose)
    else:
        report = validate_single_message(input_file, verbose)
    print(report)


if __name__ == "__main__":
    main()
