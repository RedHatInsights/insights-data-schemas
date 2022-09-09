---
layout: default
---
\[[Front page](../index.md)\] \[[External data pipeline](../external_data_pipeline.md)\]

# Format of the received Kafka records from `platform.upload.announce` topic

## Schema version

1 (unofficial)

## Description

The records (messages) received from `platform.upload.announce` that are encoded
using JSON format. It consists of an object with various attributes.

Every time a new record is sent by Kafka to the subscribed topic, the
`ccx_data_pipeline.consumer.Consumer` class will handle and process it, storing
the needed information from the record and returning the URL to the archive in
the corresponding S3 bucket.

Other relevant information about `ccx_data_pipeline` can be found on address
[https://redhatinsights.github.io/ccx-data-pipeline/](https://redhatinsights.github.io/ccx-data-pipeline/).

## Required attributes

Consumed messages is in JSON format with the following three top-level required
attributes:

* `url` (string with custom format)
* `b64_identity` (JSON encoded by BASE64 encoding)
* `timestamp` (timestamp with TZ info stored as a string)

---
**NOTE**

All required attributes are described in more details below, including the
`b64_identity` internal structure.

---

## Optional attributes

Some attributes are optional:

* `account` (unsigned integer)
* `principal` (unsigned integer)
* `size` (unsigned integer)
* `category` (string)
* `metadata` (object)
* `request_id` (string[32])
* `service` (string)

## Possible enhancements

Version (positive integer) should be included in the message so the schema
change will be possible w/o breaking other services and tools.

## Basic format

Consumed messages can contain optional attributes, but in fact only `url`,
`b64_identity`, and `timestamp` attributes are really required and used by
external data pipeline.

### Message without optional attributes

The minimal message content that is fully usable by the external data pipeline:

```json
{
  "url": "https://hostname.s3.amazonaws.com/first-part?X-Amz-Algorithm=algorithm&X-Amz-Credential=credential-info&X-Amz-Date=creation-date&X-Amz-Expires=expiration-time&X-Amz-SignedHeaders=host&X-Amz-Signature=signature",
  "b64_identity": "encoded-identity-info",
  "timestamp": "2020-01-23T16:15:59.478901889Z"
}
```

### Message with optional attributes

Message that contains all optional attributes, that are not strictly required
by the external data pipeline:

```json
{
  "account": 123456,
  "category": "test",
  "metadata": {
    "reporter": "",
    "stale_timestamp": "0001-01-01T00:00:00Z",
    "custom_metadata": {
      "ccx_metadata": {
        "gathering_time": "2022-03-02T00:01:02Z"
      }
    }
  },
  "request_id": "b44bfb83b8b0e4a7aad8b64b43879846",
  "principal": 9,
  "size": 55099,
  "url": "https://hostname.s3.amazonaws.com/first-part?X-Amz-Algorithm=algorithm&X-Amz-Credential=credential-info&X-Amz-Date=creation-date&X-Amz-Expires=expiration-time&X-Amz-SignedHeaders=host&X-Amz-Signature=signature",
  "b64_identity": "encoded-identity-info",
  "timestamp": "2020-01-23T16:15:59.478901889Z"
}
```

## `b64_identity` attribute

The attribute `b64_identity` contains another JSON encoded by BASE64 encoding.
User and organization identities are stored here along with other attributes.
That embedded JSON must contain at least `identity` object with account number
(stored as string, not an integer), auth_type and `internal` object. `internal`
object is important as it contains `org_id` (also stored as a string).

## Required attributes

* `identity` (object)

Nested JSON structure (sub-node) that contain more details about user or system
who stored data into S3 bucket. That JSON structure usually contains several
attributes, especially:

* `account_number` (integer stored in string)
* `auth_type` (type represented as a string)
* `internal` (JSON sub-node with organization ID etc.)
* `type` (object type - user, system etc.)
* `user` (optional, JSON sub-node with user-related attributes)
* `system` (optional, JSON sub-node with system-related attributes)

Please note that `account_number` and `org_id` attributes are stored as
strings, but currently its content can be represented as a positive integer.
This might change in future, but it is unlikely.

## Optional attributes

* `entitlements` (object)

Optional JSON structure with additional flags with entitlements:

```json
"first_entitlement": {
  "is_entitled": true,
  "is_trial": false
},
"second_entitlement": {
  "is_entitled": true,
  "is_trial": true
},
"third_entitlement": {
  "is_entitled": false,
  "is_trial": false
}
```

* `metadata` (object)

Optional JSON structure with additional metadata sent by Insights and,
optinally, from the archive uploader.

```json
"reporter": "ingress",
"stale_timestamp": "2022-03-02T11:53:00Z",
"custom_metadata": {
  "ccx_metadata": {
    "gathering_time": "2022-03-02T11:50:15Z"
  }
}
```

The `custom_metadata` will contain a JSON object too. In case that it contains
the `ccx_metadata` key, it will be used by the external data pipeline for
further processing.

## Examples

### Identity based on `basic-auth`

```json
{
    "identity": {
        "account_number": "1234567",
        "auth_type": "basic-auth",
        "internal": {
            "auth_time": 1400,
            "org_id": "1234567"
        },
        "type": "User",
        "user": {
            "email": "foo@bar.com",
            "first_name": "John",
            "is_active": true,
            "is_internal": false,
            "is_org_admin": true,
            "last_name": "Doe",
            "locale": "en_US",
            "username": "john_doe"
        }
}
```

### Identity based on `cert-auth` with system info

```json
{
    "identity": {
        "account_number": "1234567",
        "auth_type": "cert-auth",
        "internal": {
            "auth_time": 0,
            "org_id": "1234567"
        },
        "type": "System",
        "user": {
            "email": "foo@bar.com",
            "first_name": "John",
            "is_active": true,
            "is_internal": false,
            "is_org_admin": true,
            "last_name": "Doe",
            "locale": "en_US",
            "username": "john_doe"
        }
        "system": {
          "cn": "a259dd72-563a-17d-8e6e4-ca5f63e45824",
          "cert_type": "system"
        }
    }
}
```

### Identity based on `cert-auth` with entitlements info

```json
{
    "identity": {
        "account_number": "1234567",
        "auth_type": "cert-auth",
        "internal": {
            "auth_time": 0,
            "org_id": "1234567"
        },
        "type": "System",
        "user": {
            "email": "foo@bar.com",
            "first_name": "John",
            "is_active": true,
            "is_internal": false,
            "is_org_admin": true,
            "last_name": "Doe",
            "locale": "en_US",
            "username": "john_doe"
        }
        "system": {
          "cn": "a259dd72-563a-17d-8e6e4-ca5f63e45824",
          "cert_type": "system"
        }
    },
    "entitlements": {
        "first_entitlement": {
          "is_entitled": true,
          "is_trial": false
        },
        "second_entitlement": {
          "is_entitled": true,
          "is_trial": true
        },
        "third_entitlement": {
          "is_entitled": false,
          "is_trial": false
        }
    }
}
```

---
**NOTE**

`cn` uses its canonical textual representation: the 16 octets of a
UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---
