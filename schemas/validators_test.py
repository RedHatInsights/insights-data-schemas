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

# strings with exactly 32 hexadecimal digits
hexa32_strings = (
        "00000000000000000000000000000000",
        "ffffffffffffffffffffffffffffffff",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f",
        "0123456789abcdef0123456789abcdef",
        "0123456789ABCDEF0123456789ABCDEF",
        )


# strings that have not exactly 32 hexadecimal digits
not_hexa32_strings = (
        "",
        "0",
        # not hexa chars
        "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ",
        "0000000000000000000000000000000",
        # shorter by one character
        "fffffffffffffffffffffffffffffff",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0",
        "0123456789abcdef0123456789abcde",
        "0123456789ABCDEF0123456789ABCDE",
        # longer by one character
        "000000000000000000000000000000000",
        "fffffffffffffffffffffffffffffffff",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f000",
        "0123456789abcdef0123456789abcdeee",
        "0123456789ABCDEF0123456789ABCDEEE",
        )

# correct SHA1 sum values
sha1sum_correct_values = (
        "da39a3ee5e6b4b0d3255bfef95601890afd80709",  # ""
        "b858cb282617fb0956d960215c8e84d1ccf909c6",  # " "
        "ac9231da4082430afe8f4d40127814c613648d8e",  # "<Tab>"
        "0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33",  # "foo"
        "62cdb7020ff920e5aa642c3d4066950dd1f01f4d",  # "bar"
        "bbe960a25ea311d21d40669e93df2003ba9b90a2",  # "baz"
        "01b307acba4f54f55aafc33bb06bbbf6ca803e9a",  # "1234567890"
        "feab40e1fca77c7360ccca1481bb8ba5f919ce3a",  # "FOO"
        "a5d5c1bba91fdb6c669e1ae0413820885bbfc455",  # "BAR"
        "8324feb44eda347289ca80c2cbf964a214ccd719",  # "BAZ"
        "3a52ce780950d4d969792a2559cd519d7ee8c727",  # "."
        "5bab61eb53176449e25c2c82f172b82cb13ffb9d",  # "?"
        "c0a0e1c81318f3d91f6b7b7b8dc12fc1220ed187",  # "ěščřžýáíé"
        "edc52dfb9088c992c272f2ec05226c6b3b57f87b",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA1 sum values
sha1sum_incorrect_values = (
        "da39a3ee5e6b4b0d3255bfef95601890afd8070",    # shorter
        "b858cb282617fb0956d960215c8e84d1ccf909c6f",  # longer
        "ac9231da4082430afe8f4d40127814c613648d8Z",   # invalid character
        ""                                            # empty (obviously)
        )

# correct SHA224 sum values
sha224sum_correct_values = (
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f",  # ""
        "ca17734c016e36b898af29c1aeb142e774abf4b70bac55ec98a27ba8",  # " "
        "c0a4e868a8a338b2457376faf371e5b41a367e3c162bb0cb1a06efc8",  # "<Tab>"
        "0808f64e60d58979fcb676c96ec938270dea42445aeefcd3a4e6f8db",  # "foo"
        "07daf010de7f7f0d8d76a76eb8d1eb40182c8d1e7a3877a6686c9bf0",  # "bar"
        "1846d1bd30922b6492a1a28bc940fd00efcd2d9bfb00e34e94bf8048",  # "baz"
        "b564e8a5cf20a254eb34e1ae98c3d957c351ce854491ccbeaeb220ea",  # "1234567890"
        "9245d41684c67df13d81a3600ab1f59c155eb8667929c2798c01bb62",  # "FOO"
        "b50a9be3c2ac5c2e7b732124f5aefc5e9c44e74009e7c2c493e1ae68",  # "BAR"
        "9e502a72e805a78cdf933f99259ad4576ccf3762d5151a262f44e7df",  # "BAZ"
        "2727e5a04d8acc225b3320799348e34eff9ac515e1130101baab751a",  # "."
        "a1d9840a7d6e6f9a6c13f2b7802f1f64bb01f0fb041f698244f207a1",  # "?"
        "b9da488e288ac2e28307cda16734d1030a865e372ea837f440b429a7",  # "ěščřžýáíé"
        "987771883fcf5b44bcf91d4ac18c7b89a4a8741299eaf78fbbff3009",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA224 sum values
sha224sum_incorrect_values = (
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42",    # shorter
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42ff",  # longer
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42Z",   # invalid character
        ""                                                            # empty (obviously)
        )

# correct SHA256 sum values
sha256sum_correct_values = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # ""
        "36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068",  # " "
        "2b4c342f5433ebe591a1da77e013d1b72475562d48578dca8b84bac6651c3cb9",  # "<Tab>"
        "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",  # "foo"
        "fcde2b2edba56bf408601fb721fe9b5c338d10ee429ea04fae5511b68fbf8fb9",  # "bar"
        "baa5a0964d3320fbc0c6a922140453c8513ea24ab8fd0577034804a967248096",  # "baz"
        "c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646",  # "1234567890"
        "9520437ce8902eb379a7d8aaa98fc4c94eeb07b6684854868fa6f72bf34b0fd3",  # "FOO"
        "81f5f5515e670645c30c6340fe397157bbd2d42caa6968fd296a725ec9fac4ed",  # "BAR"
        "9773f3684f996b2775eb5b05819b54674a6de538e1193c8c0db784f74ae14e63",  # "BAZ"
        "cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8",  # "."
        "8a8de823d5ed3e12746a62ef169bcf372be0ca44f0a1236abc35df05d96928e1",  # "?"
        "a05e42c7e14de716cd501e135f3f5e49545f71069de316a1e9f7bb153f9a7356",  # "ěščřžýáíé"
        "ee3b5d221780c973eb9a43805d696b7a201dbd159900acff9988a9ee41d54125",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA256 sum values
sha256sum_incorrect_values = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85",    # shorter
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b8555",  # longer
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85Z",   # invalid character
        ""                                                                    # empty (obviously)
        )


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


@pytest.mark.parametrize("value", hexa32_strings)
def test_hexaString32Validator_correct_values(value):
    """Check the parsing and validating strings with 32 hexa characters."""
    # no exception is expected
    hexaString32Validator(value)


@pytest.mark.parametrize("value", not_hexa32_strings)
def test_hexaString32Validator_incorrect_values(value):
    """Check the parsing and validating strings with 32 hexa characters."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        hexaString32Validator(value)


@pytest.mark.parametrize("value", sha1sum_correct_values)
def test_sha1Validator_correct_values(value):
    """Check the parsing and validating SHA1 sums."""
    # exception is not expected
    sha1Validator(value)


@pytest.mark.parametrize("value", sha1sum_incorrect_values)
def test_sha1Validator_incorrect_values(value):
    """Check the parsing and validating SHA1 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha1Validator(value)


@pytest.mark.parametrize("value", sha224sum_correct_values)
def test_sha224Validator_correct_values(value):
    """Check the parsing and validating SHA224 sums."""
    # exception is not expected
    sha224Validator(value)


@pytest.mark.parametrize("value", sha224sum_incorrect_values)
def test_sha224Validator_incorrect_values(value):
    """Check the parsing and validating SHA224 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha224Validator(value)


@pytest.mark.parametrize("value", sha256sum_correct_values)
def test_sha256Validator_correct_values(value):
    """Check the parsing and validating SHA256 sums."""
    # exception is not expected
    sha256Validator(value)


@pytest.mark.parametrize("value", sha256sum_incorrect_values)
def test_sha256Validator_incorrect_values(value):
    """Check the parsing and validating SHA256 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha256Validator(value)
