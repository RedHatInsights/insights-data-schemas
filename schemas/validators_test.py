#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2020, 2011  Pavel Tisnovsky
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

"""Unit tests for validators module."""

import pytest

from voluptuous import Invalid

from validators import *


# proper positive integers
positive_int_values = (1, 2, 3, 65535, 65536, 4294967295, 4294967296,
                       18446744073709551615, 18446744073709551616)

# proper positive integers and a zero
positive_int_values_and_zero = positive_int_values + (0, )

# improper positive integers
not_positive_int_values = (0, -1, -65535)

# proper negative integers
negative_int_values = (-1, -2, -3, -65535, -65536, -4294967295, -4294967296,
                       -18446744073709551615, -18446744073709551616)

# proper negative integers and a zero
negative_int_values_and_zero = negative_int_values + (0, )

# improper negative integers
not_negative_int_values = (0, 1, 65535)

# improper integers
not_integer_type = ("", "0", "1", "-1", True, False, 3.14)

# positive float values
positive_float_values = (1.0, 3.14, 1e10, 1e100, 1e-10, 1e-100)

# not positive float values
not_positive_float_values = (0.0, -3.14, -1e10, -1e100, -1e-10, -1e-100)

# positive float values and zero
positive_float_values_and_zero = positive_float_values + (0.0, )

# negative float values
negative_float_values = (-1.0, -3.14, -1e10, -1e100, -1e-10, -1e-100)

# not negative float values
not_negative_float_values = (0.0, 1.0, 3.14, 1e10, 1e100, 1e-10, 1e-100)

# negative float values and zero
negative_float_values_and_zero = negative_float_values + (0.0, )

# improper floats
not_float_type = ("", "0", "1", "-1", True, False)

# proper string values
string_values = ("", " ", "non-empty", "ěščř")

# proper string values
non_empty_string_values = (" ", "non-empty", "ěščř")

# improper string values
not_string_type = (0, 3.14, True, False, None)

# proper positive integers stored in string
positive_int_values_in_string = ("1", "2", "3", "65535", "65536", "4294967295", "4294967296",
                                 "18446744073709551615", "18446744073709551616")

# proper positive integers and a zero stored in string
positive_int_values_and_zero_in_string = positive_int_values_in_string + ("0", )

# improper positive integers stored in string
not_positive_int_values_in_string = ("0", "-1", "-65535")

# proper negative integers stored in string
negative_int_values_in_string = ("-1", "-2", "-3", "-65535", "-65536", "-4294967295", "-4294967296",
                                 "-18446744073709551615", "-18446744073709551616")

# proper negative integers and a zero stored in string
negative_int_values_and_zero_in_string = negative_int_values_in_string + ("0", )

# improper negative integers stored in string
not_negative_int_values_in_string = ("0", "1", "65535")

# positive float values stored in string
positive_float_values_in_string = ("1.0", "3.14", "1e10", "1e100", "1e-10", "1e-100")

# not positive float values stored in string
not_positive_float_values_in_string = ("0.0", "-3.14", "-1e10", "-1e100", "-1e-10", "-1e-100")

# positive float values and zero stored in string
positive_float_values_and_zero_in_string = positive_float_values_in_string + ("0.0", )

# negative float values stored in string
negative_float_values_in_string = ("-1.0", "-3.14", "-1e10", "-1e100", "-1e-10", "-1e-100")

# not negative float values stored in string
not_negative_float_values_in_string = ("0.0", "1.0", "3.14", "1e10", "1e100", "1e-10", "1e-100")

# negative float values and zero stored in string
negative_float_values_and_zero_in_string = negative_float_values_in_string + ("0.0", )


@pytest.mark.parametrize("value", positive_int_values+negative_int_values_and_zero)
def test_intTypeValidator_correct_values(value):
    """Check if proper integer values are validated."""
    # no exception is expected
    intTypeValidator(value)


@pytest.mark.parametrize("value", positive_int_values+negative_int_values_and_zero)
def test_intTypeValidator_incorrect_values(value):
    """Check if proper integer values are validated."""
    # no exception is expected
    intTypeValidator(value)


@pytest.mark.parametrize("value", not_integer_type)
def test_posIntValidator_correct_values(value):
    """Check if inproper positive integer values are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        intTypeValidator(value)


@pytest.mark.parametrize("value", not_positive_int_values)
def test_posIntValidator_wrong_values(value):
    """Check if improper positive integer values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntValidator(value)


@pytest.mark.parametrize("value", not_integer_type)
def test_posIntValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntValidator(value)


@pytest.mark.parametrize("value", positive_int_values_and_zero)
def test_posIntOrZeroValidator_correct_values(value):
    """Check if proper positive integer or zero values are validated."""
    # no exception is expected
    posIntOrZeroValidator(value)


@pytest.mark.parametrize("value", negative_int_values)
def test_posIntOrZeroValidator_wrong_values(value):
    """Check if improper positive integer values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntOrZeroValidator(value)


@pytest.mark.parametrize("value", not_integer_type)
def test_posIntOrZeroValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntOrZeroValidator(value)


@pytest.mark.parametrize("value", negative_int_values)
def test_negIntValidator_correct_values(value):
    """Check if proper negative integer values are validated."""
    # no exception is expected
    negIntValidator(value)


@pytest.mark.parametrize("value", not_negative_int_values)
def test_negIntValidator_wrong_values(value):
    """Check if improper negative integer values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntValidator(value)


@pytest.mark.parametrize("value", not_integer_type)
def test_negIntValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntValidator(value)


@pytest.mark.parametrize("value", negative_int_values_and_zero)
def test_negIntOrZeroValidator_correct_values(value):
    """Check if proper negative integer values or zero are validated."""
    # no exception is expected
    negIntOrZeroValidator(value)


@pytest.mark.parametrize("value", positive_int_values)
def test_negIntOrZeroValidator_wrong_values(value):
    """Check if improper negative integer values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntOrZeroValidator(value)


@pytest.mark.parametrize("value", not_integer_type)
def test_negIntOrZeroValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntOrZeroValidator(value)


@pytest.mark.parametrize("value", positive_float_values+negative_float_values_and_zero)
def test_floatTypeValidator_correct_values(value):
    """Check if proper float values are validated."""
    # no exception is expected
    floatTypeValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_floatTypeValidator_incorrect_values(value):
    """Check if improper float values are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        floatTypeValidator(value)


@pytest.mark.parametrize("value", positive_float_values)
def test_posFloatValidator_correct_values(value):
    """Check if proper positive float values are validated."""
    # no exception is expected
    posFloatValidator(value)


@pytest.mark.parametrize("value", not_positive_float_values)
def test_posFloatValidator_wrong_values(value):
    """Check if improper positive float values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_PosFloatValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatValidator(value)


def test_PosFloatValidator_nan():
    """Check if NaN is not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatValidator(math.nan)


@pytest.mark.parametrize("value", positive_float_values_and_zero)
def test_posFloatOrZeroValidator_correct_values(value):
    """Check if proper positive float values are validated."""
    # no exception is expected
    posFloatOrZeroValidator(value)


@pytest.mark.parametrize("value", negative_float_values)
def test_PosFloatOrZeroValidator_wrong_values(value):
    """Check if improper positive float values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatOrZeroValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_PosFloatOrZeroValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatOrZeroValidator(value)


def test_PosFloatOrZeroValidator_nan():
    """Check if NaN is not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatOrZeroValidator(math.nan)


def test_PosFloatOrZeroValidator_nan():
    """Check if NaN is not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatOrZeroValidator(math.nan)


@pytest.mark.parametrize("value", negative_float_values)
def test_negFloatValidator_correct_values(value):
    """Check if proper negative float values are validated."""
    # no exception is expected
    negFloatValidator(value)


@pytest.mark.parametrize("value", not_negative_float_values)
def test_negFloatValidator_wrong_values(value):
    """Check if improper negative float values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_negFloatValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatValidator(value)


def test_NegFloatValidator_nan():
    """Check if NaN is not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatValidator(math.nan)


@pytest.mark.parametrize("value", negative_float_values_and_zero)
def test_negFloatOrZeroValidator_correct_values(value):
    """Check if proper negative float values are validated."""
    # no exception is expected
    negFloatOrZeroValidator(value)


@pytest.mark.parametrize("value", positive_float_values)
def test_negFloatOrZeroValidator_wrong_values(value):
    """Check if improper negative float values are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatOrZeroValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_negFloatOrZeroValidator_wrong_types(value):
    """Check if improper types are not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatOrZeroValidator(value)


def test_NegFloatOrZeroValidator_nan():
    """Check if NaN is not validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatOrZeroValidator(math.nan)


def test_isNaNValidator():
    """Check if NaN value is validated properly."""
    # exception is not expected
    isNaNValidator(math.nan)


@pytest.mark.parametrize("value", positive_float_values+negative_float_values_and_zero)
def test_isNaNValidator_wrong_values(value):
    """Check if NaN value is validated properly."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        isNaNValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_isNaNValidator_wrong_types(value):
    """Check if NaN value is validated properly."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        isNaNValidator(value)


def test_isNotNaNValidator():
    """Check if NaN value is validated properly."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        isNotNaNValidator(math.nan)


@pytest.mark.parametrize("value", positive_float_values+negative_float_values_and_zero)
def test_isNotNaNValidator_wrong_values(value):
    """Check if NaN value is validated properly."""
    # exception is not expected
    isNotNaNValidator(value)


@pytest.mark.parametrize("value", not_float_type)
def test_isNotNaNValidator_wrong_types(value):
    """Check if NaN value is validated properly."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        isNotNaNValidator(value)


@pytest.mark.parametrize("value", string_values)
def test_stringTypeValidator_correct_values(value):
    """Check if proper string values are validated."""
    # no exception is expected
    stringTypeValidator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_stringTypeValidator_incorrect_values(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        stringTypeValidator(value)


def test_emptyStringValidator_correct_value():
    """Check if proper empty string value is validated."""
    # no exception is expected
    emptyStringValidator("")


@pytest.mark.parametrize("value", non_empty_string_values)
def test_emptyStringValidator_correct_values(value):
    """Check if improper empty string values are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        emptyStringValidator(value)


@pytest.mark.parametrize("value", non_empty_string_values)
def test_notEmptyStringValidator_correct_values(value):
    """Check if proper non empty string values are validated."""
    # no exception is expected
    notEmptyStringValidator(value)


def test_notEmptyStringValidator_incorrect_value():
    """Check if improper non empty string values are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        notEmptyStringValidator("")


@pytest.mark.parametrize("value", positive_int_values_in_string + negative_int_values_in_string)
def test_intInStringValidator_correct_values(value):
    """Check the parsing and validating integers stored in string."""
    # no exception is expected
    intInStringValidator(value)


@pytest.mark.parametrize("value", positive_float_values_in_string)
def test_intInStringValidator_incorrect_values(value):
    """Check the parsing and validating integers stored in string."""
    # exception is expected
    with pytest.raises(ValueError) as excinfo:
        intInStringValidator(value)


@pytest.mark.parametrize("value", positive_int_values_in_string)
def test_posIntInStringValidator_correct_values(value):
    """Check the parsing and validating positive integers stored in string."""
    # no exception is expected
    posIntInStringValidator(value)


@pytest.mark.parametrize("value", negative_int_values_and_zero_in_string)
def test_posIntInStringValidator_incorrect_values(value):
    """Check the parsing and validating positive integers stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntInStringValidator(value)


@pytest.mark.parametrize("value", positive_int_values_and_zero_in_string)
def test_posIntOrZeroInStringValidator_correct_values(value):
    """Check the parsing and validating positive integers or a zero stored in string."""
    # no exception is expected
    posIntOrZeroInStringValidator(value)


@pytest.mark.parametrize("value", negative_int_values_in_string)
def test_posIntOrZeroInStringValidator_incorrect_values(value):
    """Check the parsing and validating positive integers or a zero stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntInStringValidator(value)


@pytest.mark.parametrize("value", negative_int_values_in_string)
def test_negIntInStringValidator_correct_values(value):
    """Check the parsing and validating negative integers stored in string."""
    # no exception is expected
    negIntInStringValidator(value)


@pytest.mark.parametrize("value", positive_int_values_and_zero_in_string)
def test_negIntInStringValidator_incorrect_values(value):
    """Check the parsing and validating negative integers stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntInStringValidator(value)


@pytest.mark.parametrize("value", negative_int_values_and_zero_in_string)
def test_negIntOrZeroInStringValidator_correct_values(value):
    """Check the parsing and validating negative integers or a zero stored in string."""
    # no exception is expected
    negIntOrZeroInStringValidator(value)


@pytest.mark.parametrize("value", positive_int_values_in_string)
def test_negIntOrZeroInStringValidator_incorrect_values(value):
    """Check the parsing and validating negative integers or a zero stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntInStringValidator(value)


@pytest.mark.parametrize("value", positive_float_values_in_string)
def test_posFloatInStringValidator_correct_values(value):
    """Check the parsing and validating positive floats stored in string."""
    # no exception is expected
    posFloatInStringValidator(value)


@pytest.mark.parametrize("value", negative_float_values_and_zero_in_string)
def test_posFloatInStringValidator_incorrect_values(value):
    """Check the parsing and validating positive floats stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatInStringValidator(value)


@pytest.mark.parametrize("value", positive_float_values_and_zero_in_string)
def test_posFloatOrZeroInStringValidator_correct_values(value):
    """Check the parsing and validating positive floats or a zero stored in string."""
    # no exception is expected
    posFloatOrZeroInStringValidator(value)


@pytest.mark.parametrize("value", negative_float_values_in_string)
def test_posFloatOrZeroInStringValidator_incorrect_values(value):
    """Check the parsing and validating positive floats or a zero stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatInStringValidator(value)


@pytest.mark.parametrize("value", negative_float_values_in_string)
def test_negFloatInStringValidator_correct_values(value):
    """Check the parsing and validating negative floats stored in string."""
    # no exception is expected
    negFloatInStringValidator(value)


@pytest.mark.parametrize("value", positive_float_values_and_zero_in_string)
def test_negFloatInStringValidator_incorrect_values(value):
    """Check the parsing and validating negative floats stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatInStringValidator(value)


@pytest.mark.parametrize("value", negative_float_values_and_zero_in_string)
def test_negFloatOrZeroInStringValidator_correct_values(value):
    """Check the parsing and validating negative floats or a zero stored in string."""
    # no exception is expected
    negFloatOrZeroInStringValidator(value)


@pytest.mark.parametrize("value", positive_float_values_in_string)
def test_negFloatOrZeroInStringValidator_incorrect_values(value):
    """Check the parsing and validating negative floats or a zero stored in string."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatInStringValidator(value)
