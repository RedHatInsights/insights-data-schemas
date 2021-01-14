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
positive_int_values = (1, 2, 3, 127, 128, 255, 256,
                       65535, 65536, 4294967295, 4294967296,
                       18446744073709551615, 18446744073709551616)

# proper positive integers and a zero
positive_int_values_and_zero = positive_int_values + (0, )

# improper positive integers
not_positive_int_values = (0, -1, -65535)

# proper negative integers
negative_int_values = (-1, -2, -3, -127, -128, -255, -256,
                       -65535, -65536, -4294967295, -4294967296,
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
not_string_type = (0, 3.14, True, False, None, 1+2j)

# proper positive integers stored in string
positive_int_values_in_string = ("1", "2", "3", "127", "128", "255", "256",
                                 "65535", "65536", "4294967295", "4294967296",
                                 "18446744073709551615", "18446744073709551616")

# proper positive integers and a zero stored in string
positive_int_values_and_zero_in_string = positive_int_values_in_string + ("0", )

# improper positive integers stored in string
not_positive_int_values_in_string = ("0", "-1", "-65535")

# proper negative integers stored in string
negative_int_values_in_string = ("-1", "-2", "-3", "-127", "-128", "-255", "-256",
                                 "-65535", "-65536", "-4294967295", "-4294967296",
                                 "-18446744073709551615", "-18446744073709551616")

# proper negative integers and a zero stored in string
negative_int_values_and_zero_in_string = negative_int_values_in_string + ("0", )

# improper negative integers stored in string
not_negative_int_values_in_string = ("0", "1", "127", "128", "255", "256", "65535")

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
        "11111111111111111111111111111111",
        "22222222222222222222222222222222",
        "33333333333333333333333333333333",
        "44444444444444444444444444444444",
        "55555555555555555555555555555555",
        "66666666666666666666666666666666",
        "77777777777777777777777777777777",
        "88888888888888888888888888888888",
        "99999999999999999999999999999999",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "cccccccccccccccccccccccccccccccc",
        "dddddddddddddddddddddddddddddddd",
        "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "ffffffffffffffffffffffffffffffff",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
        "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f",
        "0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F",
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
        "0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0",
        "0123456789abcdef0123456789abcde",
        "0123456789ABCDEF0123456789ABCDE",
        # longer by one character
        "000000000000000000000000000000000",
        "fffffffffffffffffffffffffffffffff",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f000",
        "0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F000",
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
        "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709",   # changed to uppercase: ""
        "B858CB282617FB0956D960215C8E84D1CCF909C6",   # changed to uppercase: " "
        "AC9231DA4082430AFE8F4D40127814C613648D8E",   # changed to uppercase: "<TAB>"
        "0BEEC7B5EA3F0FDBC95D0DD47F3C5BC275DA8A33",   # changed to uppercase: "FOO"
        "62CDB7020FF920E5AA642C3D4066950DD1F01F4D",   # changed to uppercase: "BAR"
        "BBE960A25EA311D21D40669E93DF2003BA9B90A2",   # changed to uppercase: "BAZ"
        "01B307ACBA4F54F55AAFC33BB06BBBF6CA803E9A",   # changed to uppercase: "1234567890"
        "FEAB40E1FCA77C7360CCCA1481BB8BA5F919CE3A",   # changed to uppercase: "FOO"
        "A5D5C1BBA91FDB6C669E1AE0413820885BBFC455",   # changed to uppercase: "BAR"
        "8324FEB44EDA347289CA80C2CBF964A214CCD719",   # changed to uppercase: "BAZ"
        "3A52CE780950D4D969792A2559CD519D7EE8C727",   # changed to uppercase: "."
        "5BAB61EB53176449E25C2C82F172B82CB13FFB9D",   # changed to uppercase: "?"
        "C0A0E1C81318F3D91F6B7B7B8DC12FC1220ED187",   # changed to uppercase: "ĚŠČŘŽÝÁÍÉ"
        "EDC52DFB9088C992C272F2EC05226C6B3B57F87B",   # changed to uppercase: "АБВГДЕЖЛПРСТОУ"
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

# correct SHA384 sum values
sha384sum_correct_values = (
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b",  # noqa: E501  ""
        "588016eb10045dd85834d67d187d6b97858f38c58c690320c4a64e0c2f92eebd9f1bd74de256e8268815905159449566",  # noqa: E501  " "
        "1f04ac7ef36d8652363c75ce68109badf388ea06f2696924eb413eea47578a80f30a46deb7257dcce4779f7de8eef43b",  # noqa: E501  "<Tab>"
        "98c11ffdfdd540676b1a137cb1a22b2a70350c9a44171d6b1180c6be5cbb2ee3f79d532c8a1dd9ef2e8e08e752a3babb",  # noqa: E501  "foo"
        "14919aaff0da5efeb871fe8a438061c1996e88bfe199e2796b3b5c5c65714f61183adc53d48c3a32734ca6faf7d7fda8",  # noqa: E501  "bar"
        "967004d25de4abc1bd6a7c9a216254a5ac0733e8ad96dc9f1ea0fad9619da7c32d654ec8ad8ba2f9b5728fed6633bd91",  # noqa: E501  "baz"
        "ed845f8b4f2a6d5da86a3bec90352d916d6a66e3420d720e16439adf238f129182c8c64fc4ec8c1e6506bc2b4888baf9",  # noqa: E501  "1234567890"
        "e415991986b2e2c1d65e1ea66cbdbab71da0a28f5aa51fd693ca633d1ea26499bf57a79160b7396f16882f21e0cbc631",  # noqa: E501  "FOO"
        "710d1ad91688c9876d6b39f1b49290c01926a9c2a48d0cc6cf29ac0e9af0bb1d576374545c3f06ddd91a6701288f1edb",  # noqa: E501  "BAR"
        "849b220c87377ecc35db359115602f9d03b9f94b92065c8575afd8eefc174f044d55521a15970d65bc0e0e828e460418",  # noqa: E501  "BAZ"
        "7582368259da8769965446762440c16e3ff4d09dd3bc0e9073a2b4e3d7d87d672c6de61faa09b2795d33da3264b05bcc",  # noqa: E501  "."
        "000f49a27e6d5622a6e521df9355bb938c391c9a5c1871ce528d9088e1cda2223b4afe2aafaa481321d649082db6e547",  # noqa: E501  "?"
        "9c60a389c58d3ceffbc7838bbce12710d36ee28b84b75f2cf3433db9d51b8e3cfd305a20ed426a594fbca1f6ef0c306b",  # noqa: E501  "ěščřžýáíé"
        "7e9a4a2ae3fe0b910abc297f9a6e51acd1fed6252adb713b15bb1dda92b02fa78d80a315959f8fb707c8bfe104b4c317",  # noqa: E501  "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA384 sum values
sha384sum_incorrect_values = (
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95",    # noqa: E501  shorter
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95bb",  # noqa: E501  longer
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95Z",   # noqa: E501  invalid character
        ""                                                                                                    # noqa: E501  empty (obviously)
        )

# correct SHA512 sum values
sha512sum_correct_values = (
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",  # noqa: E501  ""
        "f90ddd77e400dfe6a3fcf479b00b1ee29e7015c5bb8cd70f5f15b4886cc339275ff553fc8a053f8ddc7324f45168cffaf81f8c3ac93996f6536eef38e5e40768",  # noqa: E501  " "
        "f27b5bf8d35ea2bbbb6c0f9fef89d883415b5adbd6a84030cb1f35e6a6c026e65c60fb99f562f7eb9f77f3dec5001473441d2c5586b54d9b999cf4bd790e4c56",  # noqa: E501  "<Tab>"
        "f7fbba6e0636f890e56fbbf3283e524c6fa3204ae298382d624741d0dc6638326e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7",  # noqa: E501  "foo"
        "d82c4eb5261cb9c8aa9855edd67d1bd10482f41529858d925094d173fa662aa91ff39bc5b188615273484021dfb16fd8284cf684ccf0fc795be3aa2fc1e6c181",  # noqa: E501  "bar"
        "22b41602570746d784cef124fa6713eec180f93af02a1bfee05528e94a1b053e4136b446015161d04e9900849575bd8f95f857773868a205dbed42413cd054f1",  # noqa: E501  "baz"
        "12b03226a6d8be9c6e8cd5e55dc6c7920caaa39df14aab92d5e3ea9340d1c8a4d3d0b8e4314f1f6ef131ba4bf1ceb9186ab87c801af0d5c95b1befb8cedae2b9",  # noqa: E501  "1234567890"
        "9840f9826bba3ddfc3c4872884f51dcbe915a2d42c6a4d0d59ce564e7fe541f15b9a4271554065379709932bc99a71d85f05aacd62457fce5fd131f847de99ec",  # noqa: E501  "FOO"
        "d28acbb746e0b2b703739edc8b93602aa7d50d864e350248c520f895213207b25182c913892024a3de0b6306898911ff3b526fa8ad16c4f0565bd4bfa614ca06",  # noqa: E501  "BAR"
        "649e8d185da5490ebc0f78364f000dd31a2f2a18e8eb3d938148193b36101f2952e69bbbea78b3ebdb19c0b458ada878b1f047f0e3536136d581d6e857ae0d41",  # noqa: E501  "BAZ"
        "0b61241d7c17bcbb1baee7094d14b7c451efecc7ffcbd92598a0f13d313cc9ebc2a07e61f007baf58fbf94ff9a8695bdd5cae7ce03bbf1e94e93613a00f25f21",  # noqa: E501  "."
        "ca63c07ad35d8c9fb0c92d6146759b122d4ec5d3f67ebe2f30ddb69f9e6c9fd3bf31a5e408b08f1d4d9cd68120cced9e57f010bef3cde97653fed5470da7d1a0",  # noqa: E501  "?"
        "961933f57beedb78ae8984118bbca4919961a7ae324e554fd476de3f3e0676f1611adaebc5082cec3a8d47c9c7339d1f2c6a28fe92310b2726443da4a8ecb3bc",  # noqa: E501  "ěščřžýáíé"
        "2e3589a4eaa0187b35aa67b00c4f8744aa08f531d33816a630791de09075f1653dd2e58d439489fd2fbe3fcbf65297f552621e6137143eee2fb7993f723acc29",  # noqa: E501  "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA512 sum values
sha512sum_incorrect_values = (
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3",    # noqa: E501  shorter
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ee",  # noqa: E501  longer
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3Z",   # noqa: E501  invalid character
        ""                                                                                                                                    # noqa: E501  empty (obviously)
        )

# correct SHA-3 224 sum values
sha3_224sum_correct_values = (
        "6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7",  # ""
        "4cb5f87b01b38adc0e6f13f915668c2394cb1fb7a2795635b894dda1",  # " "
        "afb459483f686e0e3e541fa96717c1886121e6270196c924fa8a067e",  # "<Tab>"
        "f4f6779e153c391bbd29c95e72b0708e39d9166c7cea51d1f10ef58a",  # "foo"
        "cd3e5cfe8c66f5cf9ab3b7867e4d752851d4a6a54d06bf6081429ca0",  # "bar"
        "35b4a09d436c7ec1768389749757e6d924751c5b5462211257f7ec07",  # "baz"
        "9877af03f5e1919851d0ef4ce6b23f1e85a40b446d93713f4c6e6dcd",  # "1234567890"
        "3be6ce866712576f7531c8a4ecc4dc7bcd34605dacc44fb0333f9e4a",  # "FOO"
        "f68a7709193f40271900ee0af123f53f19a3f7d63b28bb972096a480",  # "BAR"
        "868f8514afd2cb4a4ea47a2b60ea4611feb13a61f1ac7b22d8974d2d",  # "BAZ"
        "175f6a68d155bbb981487655627e09ddb9b27c3a5cec04cfd626f638",  # "."
        "490c6a2682fc57b15cae3b04798dca145e9e00466e52cf9343441c2d",  # "?"
        "c770e8542bad958c42d0ed15f37eac0bff07a58c8d8489bf3cf84a5a",  # "ěščřžýáíé"
        "2b2c672f6aa173425f613722c05e8bb8a2e82e083433dcad6fe049d1",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA-3 224 sum values
sha3_224sum_incorrect_values = (
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42",    # shorter
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42ff",  # longer
        "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42Z",   # invalid character
        ""                                                            # empty (obviously)
        )

# correct SHA-3 256 sum values
sha3_256sum_correct_values = (
        "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",  # ""
        "60e893e6d54d8526e55a81f98bfac5da236bb203e84ed5967a8f527d5bf3d4a4",  # " "
        "8bf02b8b238233453488311be9b316e58ab7e1356ce948cb90dfef1af56992eb",  # "<Tab>"
        "76d3bc41c9f588f7fcd0d5bf4718f8f84b1c41b20882703100b9eb9413807c01",  # "foo"
        "cceefd7e0545bcf8b6d19f3b5750c8a3ee8350418877bc6fb12e32de28137355",  # "bar"
        "9713fc828dd6313c2975127f77e1681499b9d80c0bef9645837ed6555f24fb76",  # "baz"
        "01da8843e976913aa5c15a62d45f1c9267391dcbd0a76ad411919043f374a163",  # "1234567890"
        "841674cfd27cf225b4cb2cf79b8f6d4065cb374e17d0cf04ca160f1c8836d7ba",  # "FOO"
        "237aed288cafaada0fde7b2fcecf0c26b9638947a504ce8a20a78047e9fab294",  # "BAR"
        "3e2499206cc0d2643bbe9b301dc51e1f384f309cdb58aef05589d19cdaad7849",  # "BAZ"
        "6890427a1f51a3e7e1dfb1f57449c5f2a24a9bed6b5d82973df1d78e765ea227",  # "."
        "d827feb7bdb2df079c4d896ee5fdabad3b6258ad2049919bf822317e91d89bbf",  # "?"
        "fc5c5dc05616b236c008719e17e542977ad862d2db0c97c2ec3692ae557485ce",  # "ěščřžýáíé"
        "6a4ec5d268f3f04651e788a97a17708c428d062fb200b1de88fa0fe8cb574d94",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA-3 256 sum values
sha3_256sum_incorrect_values = (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85",    # shorter
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b8555",  # longer
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85Z",   # invalid character
        ""                                                                    # empty (obviously)
        )

# correct SHA-3 384 sum values
sha3_384sum_correct_values = (
        "0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004",  # noqa: E501  ""
        "56cd53d48102c914e48813b23c82e168faac72ea78df8f9d88b6d7c4a20c0b9d42c67c9647560cc91031a2bd559a1a2b",  # noqa: E501  " "
        "634da3ecea77f875a073de435e5cf12b3c77ab55dbd95cde81d556af64abaaa68e91c221481793ba3b378b6e137fd61c",  # noqa: E501  "<Tab>"
        "665551928d13b7d84ee02734502b018d896a0fb87eed5adb4c87ba91bbd6489410e11b0fbcc06ed7d0ebad559e5d3bb5",  # noqa: E501  "foo"
        "11cfca1618a8cfad41c77c8e4af303d6c98de7424116e87b5cd533920a17c96b4948e83a9b509a70aa6440e3a7ccc5cb",  # noqa: E501  "bar"
        "043a768f02f081a34a99c561becad6306082d726ff2c758f96cb9c6c12f60bd92d152918ee93404e1cbabee14992402e",  # noqa: E501  "baz"
        "6fdddab7d670f202629531c1a51b32ca30696d0af4dd5b0fbb5f82c0aba5e505110455f37d7ef73950c2bb0495a38f56",  # noqa: E501  "1234567890"
        "1dfd2dad0a7e71f42743680b96e122faea17559a1da31b1404efbc665fc88e64ebfd3ba1542512169f01b10808855dc2",  # noqa: E501  "FOO"
        "458952226b5919c8a366fdb2d545e919888787baca3af383e493c34e27eb212611bce0351cdd99f40ba3350abdb20207",  # noqa: E501  "BAR"
        "243e51586cbf1c3df1e138b18a6196503a01a7ca69f5bc7e520497e22c2c3ca9562033de7d1f9bc02f403cdbb33dfdd3",  # noqa: E501  "BAZ"
        "ba4729848e50f0c964d716e7d39d0bc4cb28eaa66a9c5e696de904d55317faf187d4a6964fa2f9364458b2b237cdf57d",  # noqa: E501  "."
        "ce7a9f02603364934950707f03fb9af51afedd23941ce8bb97201dfe88b61102685aee236602370813cfa4a3cfb31773",  # noqa: E501  "?"
        "45f08e3dfd537c58c5e18d169cc7b0a3ab981f5108ffb85a9436207a83d5848a9e4eb09a6b0f9b0b2af5ae599db9a062",  # noqa: E501  "ěščřžýáíé"
        "3cd09bb3353f5a5d75bfd5944943ef66a7da489614cf9ab1abe4c83146d1d3042d7cc64779b4cf2868dea8f61a7f0bc3",  # noqa: E501  "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA-3 384 sum values
sha3_384sum_incorrect_values = (
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95",    # noqa: E501  shorter
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95bb",  # noqa: E501  longer
        "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95Z",   # noqa: E501  invalid character
        ""                                                                                                    # noqa: E501  empty (obviously)
        )

# correct SHA-3 512 sum values
sha3_512sum_correct_values = (
        "a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26",  # noqa: E501  ""
        "e307daea2f0168daa1318e2faa2d67791e9d8e03692a6f7d1eb974e664fe721e81a47b4cf3d0eb19ae5d57afa19a095941cad5a5c050774ad56a8e5e21105757",  # noqa: E501  " "
        "f219f3571fe6327ffddf3cc609c111b4c7eff2e39e405594e99979bea771df45358418482f8f184b01e2acc5869334a8cbba2b7789d1a70d310f73df2a7129d9",  # noqa: E501  "<Tab>"
        "4bca2b137edc580fe50a88983ef860ebaca36c857b1f492839d6d7392452a63c82cbebc68e3b70a2a1480b4bb5d437a7cba6ecf9d89f9ff3ccd14cd6146ea7e7",  # noqa: E501  "foo"
        "03457d23880d7847fc3f58780dd58cda7237a7144ac6758e76d45cec0e06ba69440a855e913ef03790c618777f5b0ec25fc34c4b82d7538151745b120b4f8b37",  # noqa: E501  "bar"
        "8600823e9544f65105a16c30ee786b9f14b477da92cc8308b3cbec0ce4e14cf737babb8a9546b571fcd43d3b8fa355bf842e39e24d6253f578736a06fc07f6be",  # noqa: E501  "baz"
        "36dde7d288a2166a651d51ec6ded9e70e72cf6b366293d6f513c75393c57d6f33b949879b9d5e7f7c21cd8c02ede75e74fc54ea15bd043b4df008533fc68ae69",  # noqa: E501  "1234567890"
        "556c3cdb0c4ae9d908579d98eae3e717a12cf1aae816b0f7c8fdac0148fe2cde19bdd68fe2b74a2ccba81c5ab3abe554a8df928998417cea3f6b5a064d7ea4c4",  # noqa: E501  "FOO"
        "e2e63561a6c322018bbee8a5d5604fb953c6983d37f2c4b1422b2931ad444bc8ed225f6fc100a376c81b96984e255a91505b3b331877c92a5864b3a1713df0e2",  # noqa: E501  "BAR"
        "213225c1c50370a0b6776ed1da67545d58464ac52ade91db086127aa7e8e03af55d91fd71aa3350d332f480772cf581724dae30ba06df12d48470d0833b7a7e0",  # noqa: E501  "BAZ"
        "d70294740dd11b05c90c40afea3794592d551c799076eddb846de5439c56510893f878fca115786f44e7c91bb1b32051606e9b843b3c26c56e4cef1f74cd3a12",  # noqa: E501  "."
        "cfb06fe8c2bda236cb35369e82ee3043d21bbab5d70696dd79fe27ae5f8b067e314411feebc75e0b0edb01e55d4195bf15317c7cb3e5128e1d77929c530b9d24",  # noqa: E501  "?"
        "b85f17b2db3e6e5afbea97740b0bcc591aa10c34394b1d737fab275c69727f8aa09c577f5bc84d2872d586225540195d3570f7f1e3ce5297306fe007d70a4de6",  # noqa: E501  "ěščřžýáíé"
        "7c2e33b1c3c0a91fea40f121fc36900e569e7a3d32771d40503ca3b2eeb30446307d19c24ea485fbc50af9f40e2f52fdfd8e90e8ae40a1571ddd535373f8cf52",  # noqa: E501  "АБВГДЕЖЛПРСТОУ"
        )

# incorrect SHA-3 512 sum values
sha3_512sum_incorrect_values = (
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3",    # noqa: E501  shorter
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3ee",  # noqa: E501  longer
        "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3Z",   # noqa: E501  invalid character
        ""                                                                                                                                    # noqa: E501  empty (obviously)
        )

# correct MD5 sum values
md5sum_correct_values = (
        "d41d8cd98f00b204e9800998ecf8427e",  # ""
        "7215ee9c7d9dc229d2921a40e899ec5f",  # " "
        "5e732a1878be2342dbfeff5fe3ca5aa3",  # "<Tab>"
        "acbd18db4cc2f85cedef654fccc4a4d8",  # "foo"
        "37b51d194a7513e45b56f6524f2d51f2",  # "bar"
        "73feffa4b7f6bb68e44cf984c85f6e88",  # "baz"
        "e807f1fcf82d132f9bb018ca6738a19f",  # "1234567890"
        "901890a8e9c8cf6d5a1a542b229febff",  # "FOO"
        "3d75eec709b70a350e143492192a1736",  # "BAR"
        "f5aedf92178e1396cd4181962c8a9979",  # "BAZ"
        "5058f1af8388633f609cadb75a75dc9d",  # "."
        "d1457b72c3fb323a2671125aef3eab5d",  # "?"
        "b7feb6f62750ba2ea364c72d8b58a53e",  # "ěščřžýáíé"
        "b3307c094d02020507dea2960a293d90",  # "АБВГДЕЖЛПРСТОУ"
        )

# incorrect MD5 sum values
md5sum_incorrect_values = (
        "d41d8cd98f00b204e9800998ecf8427",    # shorter
        "d41d8cd98f00b204e9800998ecf8427ef",  # longer
        "d41d8cd98f00b204e9800998ecf8427Z",   # "invalid character"
        ""                                    # noqa: E501  empty (obviously)
        )

# correct UUID values
uuid_correct_values = (
        "90e1013c-a2f6-433b-af13-f7373dafa5ed",
        "74fbc0e8-2948-401f-bc6f-830ae9f73e22",
        "8089b58b-1803-40e1-9998-616c3ee91db7",
        "b584365b-9a62-4879-aec1-893d0fb5ba3b",
        "b87c7f88-87c4-4f7b-98b4-9f7fdc5ce8b1",
        "060e525a-209f-48ca-8b34-ef70f7d4d7ee",
        "dcaf8faf-cfd5-40d7-898e-25c5c904314a",
        "f695231a-f48f-4f06-a771-ba357bd672ec",
        "0293be3a-7a45-4e2d-9fa8-a64f43988257",
        "79588e77-3db9-4599-88c3-a8be8657012b",
        "c2068ad5-86cb-4871-b3ae-d31e038a8ce4",
        "07328b51-c9c8-4a7c-b575-01594078d217",
        "79a3f026-461c-4b5c-a31e-05656b4e45e6",
        "c9540851-e036-4534-a82c-020f19ea2eb5",
        "ac5c1ff4-53b4-4475-8645-01e0bca6ef56",
        "732413c4-710f-41b0-b19b-5a82e231b333",
        "dd371a0c-a640-49b3-8c6f-9e3dca257350",
        "990331cb-a29e-4475-9549-79f0c9b681c3",
        "aeb69680-e0a2-4793-ae53-fec76478efd3",
        "6b77193c-abee-4dd0-8f1f-654f667a4e9f",
        )

# incorrect UUID values
uuid_incorrect_values = (
        "90e1013c-a2f6-433b-af13-f7373dafa5e",    # shorter
        "90e1013c-a2f6-433b-af13-f7373dafa5edf",  # longer
        "90e1013c-a2f6-433b-af13-f7373dafa5eZ",   # invalid character
        "90e1013ca-2f6-433b-af13-f7373dafa5e",    # wrong structure
        "90e1013c-a2f-6433b-af13-f7373dafa5e",    # wrong structure
        "90e1013c-a2f6-433-baf13-f7373dafa5e",    # wrong structure
        "90e1013c-a2f6-43-3baf1-3f7373dafa5e",    # wrong structure
        "",  # empty
        )


# valid timestamps
valid_timestamps = (
        "2022-08-11T10:09:21Z",  # UNIX time: 1660205361
        "2004-08-20T15:53:38Z",  # UNIX time: 1093010018
        "2031-01-06T04:30:45Z",  # UNIX time: 1925436645
        "2011-08-02T13:28:26Z",  # UNIX time: 1312284506
        "1988-03-17T21:36:02Z",  # UNIX time: 574634162
        "2000-04-27T13:06:50Z",  # UNIX time: 956833610
        "2042-11-19T15:57:19Z",  # UNIX time: 2300021839
        "2013-01-09T14:42:55Z",  # UNIX time: 1357738975
        "2049-06-30T16:45:37Z",  # UNIX time: 2508680737
        "2099-01-26T15:21:12Z",  # UNIX time: 4073120472
        "1986-03-25T02:45:21Z",  # UNIX time: 512099121
        "2071-04-23T07:35:16Z",  # UNIX time: 3196996516
        "1973-07-23T14:10:16Z",  # UNIX time: 112281016
        "2018-10-17T16:08:10Z",  # UNIX time: 1539785290
        "2049-12-04T01:00:07Z",  # UNIX time: 2522188807
        "2044-02-21T03:39:34Z",  # UNIX time: 2339635174
        "2047-06-04T02:52:34Z",  # UNIX time: 2443225954
        "2104-12-18T08:43:41Z",  # UNIX time: 4259029421
        "2029-06-27T18:32:34Z",  # UNIX time: 1877272354
        "2083-06-25T19:56:38Z",  # UNIX time: 3581175398
        "2080-11-12T18:59:35Z",  # UNIX time: 3498659975
        "2046-10-02T01:00:31Z",  # UNIX time: 2422051231
        "2045-11-03T03:28:21Z",  # UNIX time: 2393288901
        "2035-07-29T01:20:52Z",  # UNIX time: 2069277652
        "1984-02-09T14:13:16Z",  # UNIX time: 445180396
        "2061-08-07T05:42:26Z",  # UNIX time: 2890615346
        "2056-01-24T00:54:51Z",  # UNIX time: 2715897291
        "1994-08-24T04:39:19Z",  # UNIX time: 777695959
        "2063-07-18T08:44:44Z",  # UNIX time: 2951970284
        "2026-03-31T09:43:43Z",  # UNIX time: 1774943023
        )

# invalid timestamps
invalid_timestamps = (
        "",                       # empty
        "2022-08-11",             # just date
        "10:09:21",               # just time
        "2022-08-11 10:09:21Z",   # no TZ separator
        "2022-08-11T10:09:21",    # no Z at the end
        "2022-08-11 10:09:21",    # no TZ separator, no Z at the end
        "99999-03-31T09:43:43Z",  # wrong year
        "2026-999-31T09:43:43Z",  # wrong month
        "2026-99-391T09:43:43Z",  # wrong day
        "2026-03-31T99:43:43Z",   # wrong hour
        "2026-03-31T09:99:43Z",   # wrong minute
        "2026-03-31T09:43:99Z",   # wrong second
        )

# valid timestamps with millisecond part
valid_timestamps_ms = (
        "1984-12-30T14:25:20.000000",  # UNIX time: 473261120
        "1996-12-16T22:31:16.000000",  # UNIX time: 850771876
        "1978-01-06T07:40:52.000000",  # UNIX time: 252916852
        "2100-11-10T08:33:25.000000",  # UNIX time: 4129515205
        "2078-04-07T09:06:33.000000",  # UNIX time: 3416544393
        "2068-06-20T18:16:09.000000",  # UNIX time: 3107438169
        "2033-02-20T22:52:28.000000",  # UNIX time: 1992549148
        "2042-10-05T21:08:33.000000",  # UNIX time: 2296152513
        "2066-08-12T15:38:23.000000",  # UNIX time: 3048849503
        "2053-04-28T06:20:58.000000",  # UNIX time: 2629430458
        "2098-03-30T10:53:09.000000",  # UNIX time: 4047011589
        "2038-08-14T07:19:02.000000",  # UNIX time: 2165375942
        "1976-11-12T08:45:42.000000",  # UNIX time: 216632742
        "2089-02-22T21:32:02.000000",  # UNIX time: 3759942722
        "2065-10-22T19:40:59.000000",  # UNIX time: 3023462459
        "2091-11-24T10:00:05.000000",  # UNIX time: 3846733205
        "2062-08-08T15:40:04.000000",  # UNIX time: 2922273604
        "2102-02-14T17:50:30.000000",  # UNIX time: 4169379030
        "2069-11-07T18:03:41.000000",  # UNIX time: 3151069421
        "1999-09-29T14:24:30.000000",  # UNIX time: 938607870
        "2043-10-03T02:57:39.000000",  # UNIX time: 2327450259
        "2042-08-03T00:26:33.000000",  # UNIX time: 2290634793
        "1995-04-15T06:48:08.000000",  # UNIX time: 797921288
        "2096-03-13T04:10:53.000000",  # UNIX time: 3982446653
        "2058-02-24T02:02:49.000000",  # UNIX time: 2781738169
        "2091-08-13T23:53:56.000000",  # UNIX time: 3837884036
        "2042-01-07T23:58:07.000000",  # UNIX time: 2272748287
        "2007-03-12T09:31:21.000000",  # UNIX time: 1173688281
        "2003-05-08T18:07:30.000000",  # UNIX time: 1052410050
        "2059-07-25T11:00:54.000000",  # UNIX time: 2826352854
        )

# invalid timestamps with millisecond part
invalid_timestamps_ms = (
        "",                             # empty
        "2022-08-11",                   # just date
        "10:09:21",                     # just time
        "10:09:21.000000",              # just time + milliseconds
        "1984-12-30 14:25:20.000000",   # no TZ separator
        "1984-12-30T14:25:20",          # no milliseconds
        "-12-30T14:25:20",              # no year
        "1984-12-30 14:25:20",          # no TZ separator, no milliseconds
        "99999-12-30T14:25:20.000000",  # wrong year
        "1984-99-30T14:25:20.000000",   # wrong month
        "1984-12-99T14:25:20.000000",   # wrong day
        "1984-12-30T99:25:20.000000",   # wrong hour
        "1984-12-30T14:99:20.000000",   # wrong minute
        "1984-12-30T14:25:99.000000",   # wrong second
        )

# valid URLs to AWS
valid_aws_urls = (
        "https://zzzzzzzzzzzzzzzzzzzzzzzz.s3.amazonaws.com/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential="
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ&X-Amz-Date=19700101T000000Z"
        "&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature="
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "https://foo.s3.amazonaws.com/upload-service-1-abcdefghijklmnop-000144/"
        "Z0ThU1Jyxc-000004?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
        "X-Amz-Credential=BAQ2GEXO117FVBVXWDMK%2F20200520%2Fus-east-1%2Fs3%2Faws4_request&",
        "http://minio:9000/insights-upload-perma/hpe.hpe2.foo.bar.com/"
        "Z0ThU1Jyxc-000004?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
        "X-Amz-Credential=BAQ2GEXO117FVBVXWDMK%2F20200520%2Fus-east-1%2Fs3%2Faws4_request&"
        "X-Amz-Date=20200520T140918Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&"
        "X-Amz-Signature=1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "https://s3.us-east-1.amazonaws.com/insights-ingress-prod/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential="
        "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ&X-Amz-Date=20201201T210535Z&"
        "X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature="
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        )


# invalid URLs to AWS
invalid_aws_urls = (
        "https://foo.s3.NOT-AMAZON.com/upload-service-1-abcdefghijklmnop-000144/"
        "Z0ThU1Jyxc-000004?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
        "X-Amz-Credential=BAQ2GEXO117FVBVXWDMK%2F20200520%2Fus-east-1%2Fs3%2Faws4_request&",
        "https://foo.s3.amazonaws.com/upload-service-1-abcdefghijklmnop-000144/",
        "https://foo.s3.NOT-AMAZON.com/upload-service-1-abcdefghijklmnop-000144/"
        "X-Amz-Credential=BAQ2GEXO117FVBVXWDMK%2F20200520%2Fus-east-1%2Fs3%2Faws4_request&",
        "https://foo.s3.NOT-AMAZON.com/upload-service-1-abcdefghijklmnop-000144/"
        "Z0ThU1Jyxc-000004?X-Amz-Algorithm=AWS4-HMAC-SHA256&"
        )

# not a proper BASE64 values
not_base64_values = (
        " ",
        "A",
        "ěščřžýáíé"
        )

# proper BASE64 values that don't contain JSONs
base64_values_not_json = (
        "Zm9v",  # "foo"
        "YmFy",  # "bar"
        "YmF6",  # "baz"
        "Rk9P",  # "FOO"
        "QkFS",  # "BAR"
        "QkFa",  # "BAZ"
        "Lg==",  # "."
        "Pw==",  # "?"
        "xJvFocSNxZnFvsO9w6HDrcOp",  # "ěščřžýáíé"
        "0JDQkdCS0JPQlNCV0JbQm9Cf0KDQodCi0J7Qow==",  # "АБВГДЕЖЛПРСТОУ"
        )

# proper BASE64 values that contain JSONs
base64_values_json = (
        "IA==",                      # " "
        "CQ==",                      # "<Tab>"
        "MTIzNDU2Nzg5MA==",          # "1234567890"
        "W10K",                      # []
        "e30K",                      # {}
        "WzEsIDIsIDNdCg==",          # [1, 2, 3]
        "eyJmb28iOjEsImJhcjoyfQo=",  # {"foo":1,"bar:2}
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


@pytest.mark.parametrize("value", not_string_type)
def test_emptyStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_notEmptyStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        notEmptyStringValidator(value)


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


@pytest.mark.parametrize("value", not_string_type)
def test_intInStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
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


@pytest.mark.parametrize("value", not_string_type)
def test_posIntInStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_posIntInOrZeroStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posIntOrZeroInStringValidator(value)


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


@pytest.mark.parametrize("value", not_string_type)
def test_negIntInStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_negIntInOrZeroStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negIntOrZeroInStringValidator(value)


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


@pytest.mark.parametrize("value", not_string_type)
def test_posFloatInStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_posFloatInOrZeroStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        posFloatOrZeroInStringValidator(value)


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


@pytest.mark.parametrize("value", not_string_type)
def test_negFloatInStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_negFloatInOrZeroStringValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        negFloatOrZeroInStringValidator(value)


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


@pytest.mark.parametrize("value", not_string_type)
def test_hexaString32Validator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_sha1ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_sha224ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
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


@pytest.mark.parametrize("value", not_string_type)
def test_sha256ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha256Validator(value)


@pytest.mark.parametrize("value", sha384sum_correct_values)
def test_sha384Validator_correct_values(value):
    """Check the parsing and validating SHA384 sums."""
    # exception is not expected
    sha384Validator(value)


@pytest.mark.parametrize("value", sha384sum_incorrect_values)
def test_sha384Validator_incorrect_values(value):
    """Check the parsing and validating SHA384 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha384Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha384ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha384Validator(value)


@pytest.mark.parametrize("value", sha512sum_correct_values)
def test_sha512Validator_correct_values(value):
    """Check the parsing and validating SHA512 sums."""
    # exception is not expected
    sha512Validator(value)


@pytest.mark.parametrize("value", sha512sum_incorrect_values)
def test_sha512Validator_incorrect_values(value):
    """Check the parsing and validating SHA512 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha512Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha512ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha512Validator(value)


@pytest.mark.parametrize("value", sha3_224sum_correct_values)
def test_sha3_224Validator_correct_values(value):
    """Check the parsing and validating SHA-3 224 sums."""
    # exception is not expected
    sha3_224Validator(value)


@pytest.mark.parametrize("value", sha3_224sum_incorrect_values)
def test_sha3_224Validator_incorrect_values(value):
    """Check the parsing and validating SHA-3 224 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_224Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha3_224ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_224Validator(value)


@pytest.mark.parametrize("value", sha3_256sum_correct_values)
def test_sha3_256Validator_correct_values(value):
    """Check the parsing and validating SHA-3 256 sums."""
    # exception is not expected
    sha3_256Validator(value)


@pytest.mark.parametrize("value", sha3_256sum_incorrect_values)
def test_sha3_256Validator_incorrect_values(value):
    """Check the parsing and validating SHA-3 256 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_256Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha3_256ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_256Validator(value)


@pytest.mark.parametrize("value", sha3_384sum_correct_values)
def test_sha3_384Validator_correct_values(value):
    """Check the parsing and validating SHA-3 384 sums."""
    # exception is not expected
    sha3_384Validator(value)


@pytest.mark.parametrize("value", sha3_384sum_incorrect_values)
def test_sha3_384Validator_incorrect_values(value):
    """Check the parsing and validating SHA-3 384 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_384Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha3_384ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_384Validator(value)


@pytest.mark.parametrize("value", sha3_512sum_correct_values)
def test_sha3_512Validator_correct_values(value):
    """Check the parsing and validating SHA-3 512 sums."""
    # exception is not expected
    sha3_512Validator(value)


@pytest.mark.parametrize("value", sha3_512sum_incorrect_values)
def test_sha3_512Validator_incorrect_values(value):
    """Check the parsing and validating SHA-3 512 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_512Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_sha3_512ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        sha3_512Validator(value)


@pytest.mark.parametrize("value", md5sum_correct_values)
def test_md5Validator_correct_values(value):
    """Check the parsing and validating MD5 sums."""
    # exception is not expected
    md5Validator(value)


@pytest.mark.parametrize("value", md5sum_incorrect_values)
def test_md5Validator_incorrect_values(value):
    """Check the parsing and validating MD5 sums."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        md5Validator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_md5ValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        md5Validator(value)


@pytest.mark.parametrize("value", uuid_correct_values)
def test_UUIDValidator_correct_values(value):
    """Check the parsing and validating UUID values."""
    # exception is not expected
    uuidValidator(value)


@pytest.mark.parametrize("value", uuid_incorrect_values)
def test_UUIDValidator_incorrect_values(value):
    """Check the parsing and validating UUID values."""
    # exception is expected
    with pytest.raises(ValueError) as excinfo:
        uuidValidator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_UUIDValidatorValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        uuidValidator(value)


@pytest.mark.parametrize("value", valid_timestamps)
def test_timestampValidator_correct_values(value):
    """Check the parsing and validating timestamps."""
    # exception is not expected
    timestampValidator(value)


@pytest.mark.parametrize("value", invalid_timestamps)
def test_timestampValidator_incorrect_values(value):
    """Check the parsing and validating timestamps."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        timestampValidator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_timestampValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        timestampValidator(value)


@pytest.mark.parametrize("value", valid_timestamps_ms)
def test_timestampMsValidator_correct_values(value):
    """Check the parsing and validating timestamps with milliseconds part."""
    # exception is not expected
    timestampValidatorMs(value)


@pytest.mark.parametrize("value", invalid_timestamps_ms)
def test_timestampMsValidator_incorrect_values(value):
    """Check the parsing and validating timestamps with milliseconds part."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        timestampValidatorMs(value)


@pytest.mark.parametrize("value", not_string_type)
def test_timestampMsValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        timestampValidatorMs(value)


@pytest.mark.parametrize("value", valid_aws_urls)
def test_urlToAWSValidator_correct_values(value):
    """Check the parsing and validating URLs to AWS with milliseconds part."""
    # exception is not expected
    urlToAWSValidator(value)


@pytest.mark.parametrize("value", invalid_aws_urls)
def test_urlToAWSValidator_incorrect_values(value):
    """Check the parsing and validating URLs to AWS with milliseconds part."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        urlToAWSValidator(value)


@pytest.mark.parametrize("value", not_string_type)
def test_urlToAWSValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        urlToAWSValidator(value)


@pytest.mark.parametrize("value", not_base64_values)
def test_b64IdentityValidator_incorrect_base64values(value):
    """Check if improper values (not base64-based) are validated."""
    schema = None  # not needed right now
    # exception is expected
    with pytest.raises(Exception) as excinfo:
        b64IdentityValidator(schema, value)


@pytest.mark.parametrize("value", base64_values_not_json)
def test_b64IdentityValidator_not_JSON(value):
    """Check if improper values (not JSON) are validated."""
    schema = None  # not needed right now
    # exception is expected
    with pytest.raises(Exception) as excinfo:
        b64IdentityValidator(schema, value)


@pytest.mark.parametrize("value", base64_values_json)
def test_b64IdentityValidator_proper_JSON(value):
    """Check if proper values are validated."""
    schema = None  # not needed right now
    # exception is expected
    with pytest.raises(Exception) as excinfo:
        b64IdentityValidator(schema, value)


@pytest.mark.parametrize("value", not_string_type)
def test_b64IdentityValidator_incorrect_types(value):
    """Check if improper values (with wrong type) are validated."""
    schema = None  # not needed right now
    # exception is expected
    with pytest.raises(Invalid) as excinfo:
        b64IdentityValidator(schema, value)
