#!/usr/bin/env python3

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

"""Generator of SHAKE-256 sum values."""

import hashlib

with open("input.txt", "r") as fin:
    for input_string in fin:
        # remove EOLN
        input_string = input_string[:-1]

        # compute hash
        shake_256_sum = hashlib.shake_256()
        shake_256_sum.update(input_string.encode("UTF-8"))

        # prepare special chars for output
        input_string = input_string.replace("\t", "<Tab>")

        # generate output
        print(f'    "{shake_256_sum.hexdigest(32)}",  # "{input_string}"')
