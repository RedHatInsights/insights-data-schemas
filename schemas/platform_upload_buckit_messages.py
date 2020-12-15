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
from os import popen
from argparse import ArgumentParser


def read_control_code(operation):
    """Try to execute tput to read control code for selected operation."""
    return popen("tput " + operation, "r").readline()


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
    parser.add_argument("-n", "--no-colors", dest="nocolors", help="disable color output",
                        action="store_true", default=None)
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
    if payload is None:
        raise ValueError("Empty payload")


def validate_single_message(input_file, verbose):
    """Validate single message stored in input file."""
    processed = 0
    valid = 0
    error = 0

    try:
        payload = load_json_from_file(input_file, verbose)
        processed = 1
        validate(payload, verbose)
        valid = 1
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(e)
        error = 1

    return {"processed": processed,
            "valid": valid,
            "error": error}


def try_to_validate_message(line, processed, verbose):
    """Try to validate one message represented by string."""
    if verbose:
        print("Reading message #{}".format(processed))
    # load the payload from string
    payload = json.loads(line)
    # and try to validate it
    validate(payload, verbose)


def validate_multiple_messages(input_file, verbose):
    """Validate multiple messages stored in input file."""
    processed = 0
    valid = 0
    error = 0

    with open(input_file, "r") as fin:
        # iterate over all lines in the message file
        for line in fin:
            processed += 1
            try:
                try_to_validate_message(line, processed, verbose)
                valid += 1
            except ValueError as ve:
                print(ve)
            except Exception as e:
                print(e)
                error += 1

    return {"processed": processed,
            "valid": valid,
            "error": error}


def print_report(report, nocolors):
    """Display report about number of passes and failures."""
    # First of all, we need to setup colors to be displayed on terminal. Colors
    # are displayed by using terminal escape control codes. When color output
    # are not enabled on command line, we can simply use empty strings in
    # output instead of real color escape codes.
    red_background = green_background = magenta_background = red_foreground = \
        green_foreground = blue_foreground = no_color = ""

    # If colors are enabled by command line parameter, use control sequence
    # returned by `tput` command.
    if not nocolors:
        red_background = read_control_code("setab 1")
        green_background = read_control_code("setab 2")
        magenta_background = read_control_code("setab 5")
        red_foreground = read_control_code("setaf 1")
        blue_foreground = read_control_code("setaf 4")
        green_foreground = read_control_code("setaf 2")
        no_color = read_control_code("sgr0")

    print("\nStatus:")
    print("Processed messages: {}{}{}".format(green_foreground, report["processed"], no_color))
    print("Valid messages:     {}{}{}".format(blue_foreground, report["valid"], no_color))
    print("Errors detected:    {}{}{}".format(red_foreground, report["error"], no_color))
    print("\nSummary:")

    if report["error"] == 0:
        if report["processed"] == report["valid"]:
            print("{}[OK]{}: all messages have proper format".format(green_background, no_color))
        else:
            print("{}[WARN]{}: invalid messages detected".format(magenta_background, no_color))
    else:
        print("{}[FAIL]{}: invalid JSON(s) detected".format(red_background, no_color))


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

    print_report(report, args.nocolors)


if __name__ == "__main__":
    main()
