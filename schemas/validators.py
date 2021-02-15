#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2020, 2021  Pavel Tisnovsky
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

"""Set of custom validators (predicates) used in data schemes."""


import datetime
import string
import re
import json
import base64
import math
from uuid import UUID

from voluptuous import Schema
from voluptuous import Invalid
from voluptuous import Required


def intTypeValidator(value):
    """Validate value for any integer."""
    # check if the given value is an integer
    if type(value) is not int:
        raise Invalid("integer expected, but invalid value type {v}".format(v=value))


def posIntValidator(value):
    """Validate value for positive integers."""
    # check if the given value is integer greater than zero
    intTypeValidator(value)
    if value <= 0:
        raise Invalid("positive integer value expected, but got {v} instead".format(v=value))


def posIntOrZeroValidator(value):
    """Validate value for positive integers or zeroes."""
    # check if the given value is integer greater than or equal to zero
    intTypeValidator(value)
    if value < 0:
        raise Invalid("positive integer or 0 value expected, but got {v} instead".format(v=value))


def negIntValidator(value):
    """Validate value for negative integers."""
    # check if the given value is integer less than zero
    intTypeValidator(value)
    if value >= 0:
        raise Invalid("negative integer value expected, but got {v} instead".format(v=value))


def negIntOrZeroValidator(value):
    """Validate value for negative integers or zeroes."""
    # check if the given value is integer less than or equal zero
    intTypeValidator(value)
    if value > 0:
        raise Invalid("negative integer or 0 value expected, but got {v} instead".format(v=value))


def floatTypeValidator(value):
    """Validate value for any float."""
    # check if the given value is a float
    if type(value) is not float:
        raise Invalid("invalid value type {value}".format(value=value))


def posFloatValidator(value):
    """Predicate that checks if the given value is positive float."""
    # check if the value has the expected type
    floatTypeValidator(value)

    # check for NaN
    isNotNaNValidator(value)

    if value <= 0.0:
        raise Invalid("invalid value {value}, positive float expected".format(value=value))


def posFloatOrZeroValidator(value):
    """Predicate that checks if the given value is positive float or zero."""
    # check if the value has the expected type
    floatTypeValidator(value)

    # check for NaN
    isNotNaNValidator(value)

    if value < 0.0:
        raise Invalid("invalid value {value}, positive float or zero expected".format(value=value))


def negFloatValidator(value):
    """Predicate that checks if the given value is positive float."""
    # check if the value has the expected type
    floatTypeValidator(value)

    # check for NaN
    isNotNaNValidator(value)

    if value >= 0.0:
        raise Invalid("invalid value {value}, negative float expected".format(value=value))


def negFloatOrZeroValidator(value):
    """Predicate that checks if the given value is positive float or zero."""
    # check if the value has the expected type
    floatTypeValidator(value)

    # check for NaN
    isNotNaNValidator(value)

    if value > 0.0:
        raise Invalid("invalid value {value}, negative float or zero expected".format(value=value))


def isNaNValidator(value):
    """Predicate that checks if the given value is NaN."""
    # check if the value has the expected type
    floatTypeValidator(value)

    if not math.isnan(value):
        raise Invalid("invalid value {value}, NaN expected".format(value=value))


def isNotNaNValidator(value):
    """Predicate that checks if the given value is not NaN."""
    # check if the value has the expected type
    floatTypeValidator(value)

    if math.isnan(value):
        raise Invalid("invalid value {value}, NaN is not expected".format(value=value))


def stringTypeValidator(value):
    """Validate value for string type."""
    # check if the given value is a string
    if type(value) is not str:
        raise Invalid("string value expected, but got {t} type instead".format(t=type(value)))


def bytesTypeValidator(value):
    """Validate value for byte array type."""
    # check if the given value is a byte array
    if type(value) is not bytes:
        raise Invalid("byte array value expected, but got {t} type instead".format(t=type(value)))


def emptyStringValidator(value):
    """Validate value for an empty string."""
    stringTypeValidator(value)

    # check for non-empty string
    if value:
        raise Invalid("Empty string value expected")


def notEmptyStringValidator(value):
    """Validate value for a non-empty string."""
    stringTypeValidator(value)

    # check for empty string
    if not value:
        raise Invalid("empty string should not be used there")


def intInStringValidator(value):
    """Validate value for an int value stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = int(value)


def posIntInStringValidator(value):
    """Validate value for a positive int value stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    posIntValidator(x)


def posIntOrZeroInStringValidator(value):
    """Validate value for a positive int value or zero stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    posIntOrZeroValidator(x)


def negIntInStringValidator(value):
    """Validate value for a negative int value stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    negIntValidator(x)


def negIntOrZeroInStringValidator(value):
    """Validate value for a negative int value or zero stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    negIntOrZeroValidator(x)


def posFloatInStringValidator(value):
    """Validate value for a positive float value stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    posFloatValidator(x)


def posFloatOrZeroInStringValidator(value):
    """Validate value for a positive float value or zero stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    posFloatOrZeroValidator(x)


def negFloatInStringValidator(value):
    """Validate value for a negative float value stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    negFloatValidator(x)


def negFloatOrZeroInStringValidator(value):
    """Validate value for a negative float value or zero stored as a string."""
    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    negFloatOrZeroValidator(x)


def intInBytesValidator(value):
    """Validate value for an int value stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = int(value)


def posIntInBytesValidator(value):
    """Validate value for a positive int value stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    posIntValidator(x)


def posIntOrZeroInBytesValidator(value):
    """Validate value for a positive int value or zero stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    posIntOrZeroValidator(x)


def negIntInBytesValidator(value):
    """Validate value for a negative int value stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    negIntValidator(x)


def negIntOrZeroInBytesValidator(value):
    """Validate value for a negative int value or zero stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = int(value)
    negIntOrZeroValidator(x)


def posFloatInBytesValidator(value):
    """Validate value for a positive float value stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    posFloatValidator(x)


def posFloatOrZeroInBytesValidator(value):
    """Validate value for a positive float value or zero stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    posFloatOrZeroValidator(x)


def negFloatInBytesValidator(value):
    """Validate value for a negative float value stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    negFloatValidator(x)


def negFloatOrZeroInBytesValidator(value):
    """Validate value for a negative float value or zero stored as a string."""
    # check if the value has the expected type
    bytesTypeValidator(value)

    # use default encoding
    value = value.decode("utf-8")

    stringTypeValidator(value)

    # try to parse the string
    x = float(value)
    negFloatOrZeroValidator(x)


def hexaString32Validator(value):
    """Validate value for string containign exactly 32 hexadecimal digits."""
    stringTypeValidator(value)

    if len(value) != 32:
        raise Invalid("wrong number of digits: {}".format(len(value)))
    if not all(c in string.hexdigits for c in value):
        raise Invalid("non-hexadecimal char detected in: {}".format(value))


def timestampValidator(value):
    """Validate value for timestamps."""
    stringTypeValidator(value)

    timeformat = '%Y-%m-%dT%H:%M:%SZ'
    try:
        # try to parse the input value
        datetime.datetime.strptime(value, timeformat)
    except ValueError:
        raise Invalid("invalid datetime value {value}".format(value=value))


def timestampValidatorMs(value):
    """Validate value for timestamps without ms part, but with TZ info."""
    stringTypeValidator(value)

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


def keyValueValidator(value):
    """Validate if value conformns to a key used in Insights Results."""
    stringTypeValidator(value)

    KEY_VALUE_RE = re.compile(r"[A-Z]+([_][A-Z0-9]+)+")
    if not KEY_VALUE_RE.fullmatch(value):
        raise Invalid("wrong key value '{}'".format(value))


def ruleFQDNValidator(value):
    """Validate if value contains FQDN (fully-qualified name)."""
    stringTypeValidator(value)

    FQDN_VALUE_RE = re.compile(r"([a-z0-9_]+[.])+[a-z0-9_]+")
    if not FQDN_VALUE_RE.fullmatch(value):
        raise Invalid("wrong FQDN '{}'".format(value))


def ruleIDValidator(value):
    """Validate if value contains rule ID."""
    stringTypeValidator(value)

    FQDN_VALUE_RE = re.compile(r"[a-z0-9_]+([_][a-z0-9_]+)+\|[A-Z0-9_]+([_][A-Z0-9_]+)+")
    if not FQDN_VALUE_RE.fullmatch(value):
        raise Invalid("wrong FQDN '{}'".format(value))


def urlToAWSValidator(value):
    """Validate if value conformns to AWS S3 URL."""
    stringTypeValidator(value)

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
    stringTypeValidator(value)

    # UUID version 4 is the most common version, but it is possible to specify
    # other version as well
    UUID(value, version=version)


def md5Validator(value):
    """Predicate that checks if the given value seems to be MD5 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # MD5 hash has 32 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{32}$", value):
        raise Invalid("the value '{value}' does not seem to be MD5 hash".format(value=value))


def sha1Validator(value):
    """Predicate that checks if the given value seems to be SHA1 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-1 hash has 40 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{40}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA1 hash".format(value=value))


def sha224Validator(value):
    """Predicate that checks if the given value seems to be SHA224 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-224 hash has 56 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{56}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA224 hash".format(value=value))


def sha256Validator(value):
    """Predicate that checks if the given value seems to be SHA256 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-256 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA256 hash".format(value=value))


def sha384Validator(value):
    """Predicate that checks if the given value seems to be SHA384 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-384 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{96}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA384 hash".format(value=value))


def sha512Validator(value):
    """Predicate that checks if the given value seems to be SHA512 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-512 hash has 128 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{128}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA512 hash".format(value=value))


def sha3_224Validator(value):
    """Predicate that checks if the given value seems to be SHA-3 224 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-3 224 hash has 56 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{56}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA-3 224 hash".format(value=value))


def sha3_256Validator(value):
    """Predicate that checks if the given value seems to be SHA-3 256 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-3 256 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA-3 256 hash".format(value=value))


def sha3_384Validator(value):
    """Predicate that checks if the given value seems to be SHA-3 384 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-3 384 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{96}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA-3 384 hash".format(value=value))


def sha3_512Validator(value):
    """Predicate that checks if the given value seems to be SHA-3 512 hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHA-3 512 hash has 128 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{128}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA-3 512 hash".format(value=value))


def shake128Validator(value):
    """Predicate that checks if the given value seems to be SHAKE128 256-bit hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHAKE128 256-bit hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{v}' does not seem to be SHAKE128 256-bit hash".format(v=value))


def shake256Validator(value):
    """Predicate that checks if the given value seems to be SHAKE256 256-bit hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # SHAKE256 256-bit hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{v}' does not seem to be SHAKE256 256-bit hash".format(v=value))


def BLAKE2Validator(value):
    """Predicate that checks if the given value seems to be BLAKE2 256-bit hash."""
    # check if the value has the expected type
    stringTypeValidator(value)

    # BLAKE2 256-bit hash has 128 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{128}$", value):
        raise Invalid("the value '{v}' does not seem to be BLAKE2 256-bit hash".format(v=value))


def b64IdentityValidator(identitySchema, value):
    """Validate identity encoded by base64 encoding."""
    # input must be a string
    stringTypeValidator(value)

    # decode from BASE64 encoding
    value = base64.b64decode(value).decode('utf-8')

    # parse JSON
    identity = json.loads(value)

    # validate schema
    identitySchema(identity)


def jsonInStrValidator(value):
    """Validate if the value is JSON stored in string."""
    # input must be a string
    stringTypeValidator(value)

    # try to parse into JSON
    decoded = json.loads(value)

    assert decoded is not None
