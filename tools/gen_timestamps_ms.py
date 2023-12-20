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

"""Generator of semi-random timestamps."""

import datetime
import random

timeformat = "%Y-%m-%dT%H:%M:%S.%f"

for _i in range(30):
    # unix time value
    unix_time = random.randint(0, 2**32-1)

    dt = datetime.datetime.fromtimestamp(unix_time)
    dt_as_string = datetime.datetime.strftime(dt, timeformat)

    # generate output
    print(f'    "{dt_as_string}",  # UNIX time: {unix_time}')
