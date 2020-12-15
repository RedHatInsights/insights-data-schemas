#!/usr/bin/env python3
# vim: set fileencoding=utf-8

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

"""Set of custom validators used in data schemes."""

import datetime
import string
import re
import json
import base64
from uuid import UUID

from voluptuous import Schema
from voluptuous import Invalid
from voluptuous import Required


def posIntValidator(value):
    """Validate value for positive integers."""
    if type(value) is not int or value <= 0:
        raise Invalid("positive integer value expected, but got {v} instead".format(v=value))


def stringValidator(value):
    """Validate value for string type."""
    if type(value) is not str:
        raise Invalid("string value expected, but got {t} type instead".format(t=type(value)))


def intInStringValidator(value):
    """Validate value for an int value stored as a string."""
    stringValidator(value)
    # try to parse the string
    x = int(value)


def posIntInStringValidator(value):
    """Validate value for a positive int value stored as a string."""
    stringValidator(value)
    # try to parse the string
    x = int(value)
    posIntInStringValidator(x)


def notEmptyStringValidator(value):
    """Validate value for a non-empty string."""
    stringValidator(value)
    # check for empty string
    if not value:
        raise Invalid("empty string should not be used there")


def hexaString32Validator(value):
    """Validate value for string containign exactly 32 hexadecimal digits."""
    stringValidator(value)
    if len(value) != 32:
        raise Invalid("wrong number of digits: {}".format(len(value)))
    if not all(c in string.hexdigits for c in value):
        raise Invalid("non-hexadecimal char detected in: {}".format(value))


def timestampValidator(value):
    """Validate value for timestamps."""
    stringValidator(value)
    timeformat = '%Y-%m-%dT%H:%M:%SZ'
    try:
        # try to parse the input value
        datetime.datetime.strptime(value, timeformat)
    except ValueError:
        raise Invalid("invalid datetime value {value}".format(value=value))


def timestampValidatorMs(value):
    """Validate value for timestamps without ms part, but with TZ info."""
    stringValidator(value)
    timeformat = '%Y-%m-%dT%H:%M:%S.%f'
    try:
        # the following timestamp can't be parsed directly by Python
        # "2020-12-09T16:17:42.822020204Z"
        if len(value) >= 26:
            value = value[0:26]
        # try to parse the input value
        datetime.datetime.strptime(value, timeformat)
    except ValueError:
        raise Invalid("invalid datetime value {value}".format(value=value))


def urlToAWSValidator(value):
    """Validate if value conformns to AWS S3 URL."""
    stringValidator(value)
    # https://<hostname>/service_id/file_id?<credentials and other params>
    HTTP_RE = re.compile(
        r"^(?:https://[^/]+\.s3\.amazonaws\.com/[0-9a-zA-Z/\-]+|"
        r"https://s3\.[0-9a-zA-Z\-]+\.amazonaws\.com/[0-9a-zA-Z\-]+/[0-9a-zA-Z/\-]+|"
        r"http://minio:9000/insights-upload-perma/[0-9a-zA-Z\.\-]+/[0-9a-zA-Z\-]+)\?"
        r"X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=[^/]+$"
    )
    if not HTTP_RE.fullmatch(value):
        raise Invalid("wrong URL")


def uuidValidator(value, version=4):
    """Check if value conforms to UUID."""
    # check if the value has the expected type
    stringValidator(value)

    # UUID version 4 is the most common version, but it is possible to specify
    # other version as well
    UUID(value, version=version)


def md5Validator(value):
    """Predicate that checks if the given value seems to be MD5 hash."""
    # check if the value has the expected type
    stringValidator(value)

    # MD5 hash has 32 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{32}$", value):
        raise Invalid("the value '{value}' does not seem to be MD5 hash".format(value=value))


def sha1Validator(value):
    """Predicate that checks if the given value seems to be SHA1 hash."""
    # check if the value has the expected type
    stringValidator(value)

    # SHA-1 hash has 40 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{40}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA1 hash".format(value=value))


def sha256Validator(value):
    """Predicate that checks if the given value seems to be SHA256 hash."""
    # check if the value has the expected type
    stringValidator(value)

    # SHA-256 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA256 hash".format(value=value))


def b64IdentityValidator(identitySchema, value):
    """Validate identity encoded by base64 encoding."""
    # input must be a string
    stringValidator(value)

    # decode from BASE64 encoding
    value = base64.b64decode(value).decode('utf-8')

    # parse JSON
    identity = json.loads(value)

    # validate schema
    identitySchema(identity)
