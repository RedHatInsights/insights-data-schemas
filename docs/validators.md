---
layout: default
---
\[[Front page](index.md)\]

# validators - Set of custom validators (predicates) used in data schemes.

## `BLAKE2Validator(value)`
Predicate that checks if the given value seems to be BLAKE2 256-bit hash.
    
## `b64IdentityValidator(identitySchema, value)`
Validate identity encoded by base64 encoding.
    
## `bytesTypeValidator(value)`
Validate value for byte array type.
    
## `emptyStringValidator(value)`
Validate value for an empty string.
    
## `floatTypeValidator(value)`
Validate value for any float.
    
## `hexaString32Validator(value)`
Validate value for string containign exactly 32 hexadecimal digits.
    
## `intInBytesValidator(value)`
Validate value for an int value stored as a string.
    
## `intInStringValidator(value)`
Validate value for an int value stored as a string.
    
## `intTypeValidator(value)`
Validate value for any integer.
    
## `isNaNValidator(value)`
Predicate that checks if the given value is NaN.
    
## `isNotNaNValidator(value)`
Predicate that checks if the given value is not NaN.
    
## `jsonInStrValidator(value)`
Validate if the value is JSON stored in string.
    
## `keyValueValidator(value)`
Validate if value conformns to a key used in Insights Results.

## `md5Validator(value)`
Predicate that checks if the given value seems to be MD5 hash.
    
## `negFloatInBytesValidator(value)`
Validate value for a negative float value stored as a string.
    
## `negFloatInStringValidator(value)`
Validate value for a negative float value stored as a string.
    
## `negFloatOrZeroInBytesValidator(value)`
Validate value for a negative float value or zero stored as a string.
    
## `negFloatOrZeroInStringValidator(value)`
Validate value for a negative float value or zero stored as a string.
    
## `negFloatOrZeroValidator(value)`
Predicate that checks if the given value is positive float or zero.
    
## `negFloatValidator(value)`
Predicate that checks if the given value is positive float.
    
## `negIntInBytesValidator(value)`
Validate value for a negative int value stored as a string.
    
## `negIntInStringValidator(value)`
Validate value for a negative int value stored as a string.
    
## `negIntOrZeroInBytesValidator(value)`
Validate value for a negative int value or zero stored as a string.
    
## `negIntOrZeroInStringValidator(value)`
Validate value for a negative int value or zero stored as a string.
    
## `negIntOrZeroValidator(value)`
Validate value for negative integers or zeroes.
    
## `negIntValidator(value)`
Validate value for negative integers.
    
## `notEmptyStringValidator(value)`
Validate value for a non-empty string.
    
## `pathToCephInBytesValidator(value)`
Check if value conforms to path to Ceph.
    
## `posFloatInBytesValidator(value)`
Validate value for a positive float value stored as a string.
    
## `posFloatInStringValidator(value)`
Validate value for a positive float value stored as a string.
    
## `posFloatOrZeroInBytesValidator(value)`
Validate value for a positive float value or zero stored as a string.
    
## `posFloatOrZeroInStringValidator(value)`
Validate value for a positive float value or zero stored as a string.
    
## `posFloatOrZeroValidator(value)`
Predicate that checks if the given value is positive float or zero.
    
## `posFloatValidator(value)`
Predicate that checks if the given value is positive float.
    
## `posIntInBytesValidator(value)`
Validate value for a positive int value stored as a string.
    
## `posIntInStringValidator(value)`
Validate value for a positive int value stored as a string.
    
## `posIntOrZeroInBytesValidator(value)`
Validate value for a positive int value or zero stored as a string.
    
## `posIntOrZeroInStringValidator(value)`
Validate value for a positive int value or zero stored as a string.
    
## `posIntOrZeroValidator(value)`
Validate value for positive integers or zeroes.
    
## `posIntValidator(value)`
Validate value for positive integers.
    
## `sha1Validator(value)`
Predicate that checks if the given value seems to be SHA1 hash.
    
## `sha224Validator(value)`
Predicate that checks if the given value seems to be SHA224 hash.
    
## `sha256Validator(value)`
Predicate that checks if the given value seems to be SHA256 hash.
    
## `sha384Validator(value)`
Predicate that checks if the given value seems to be SHA384 hash.
    
## `sha3_224Validator(value)`
Predicate that checks if the given value seems to be SHA-3 224 hash.
    
## `sha3_256Validator(value)`
Predicate that checks if the given value seems to be SHA-3 256 hash.
    
## `sha3_384Validator(value)`
Predicate that checks if the given value seems to be SHA-3 384 hash.
    
## `sha3_512Validator(value)`
Predicate that checks if the given value seems to be SHA-3 512 hash.
    
## `sha512Validator(value)`
Predicate that checks if the given value seems to be SHA512 hash.
    
## `shake128Validator(value)`
Predicate that checks if the given value seems to be SHAKE128 256-bit hash.
    
## `shake256Validator(value)`
Predicate that checks if the given value seems to be SHAKE256 256-bit hash.
    
## `stringTypeValidator(value)`
Validate value for string type.
    
## `timestampValidator(value)`
Validate value for timestamps.
    
## `timestampValidatorMs(value)`
Validate value for timestamps without ms part, but with TZ info.
    
## `urlToAWSValidator(value)`
Validate if value conformns to AWS S3 URL.
    
## `uuidInBytesValidator(value, version=4)`
Check if value conforms to UUID.
    
## `uuidValidator(value, version=4)`
Check if value conforms to UUID.
    
## `versionInBytesValidator(value)`
Check if value conforms to version.

## `ruleFQDNValidator(value)`
Validate if value contains FQDN (fully-qualified name).

## `ruleIDValidator(value)`
Validate if value contains rule ID.
