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
                        action="store", default=False, type=bool, required=False)
    parser.add_argument("-v", "--verbose", dest="verbose", help="make it verbose",
                        action="store_true", default=None)

    # Now it is time to parse flags, check the actual content of command line
    # and fill in the object named `args`.
    return parser.parse_args()


def main():
    """Entry point to this script."""
    # Parse all CLI arguments.
    args = cli_arguments()
    verbose = args.verbose
    multiple = args.multiple


if __name__ == "__main__":
    main()
