# Format of the received Kafka records from `platform.upload.buckit` topic

The records (messages) received from `platform.upload.buckit` uses JSON format. It consists of an object with various attributes.

## Required attributes

There are several required attributes stored in this object:

* `account` (unsigned integer)
* `principal` (unsigned integer)
* `size` (unsigned integer)
* `url` (string with custom format)
* `b64_identity` (JSON encoded by BASE64 encoding)
* `timestamp` (timestamp with TZ info)

## Optional attributes

Some attributes are optional:

* `category` (string)
* `metadata` (object)
* `request_id` (string[32])
* `service` (string)

## Examples

### Message without optional attributes

```json5
{
  "account": 123456,
  "principal": 9,
  "size": 55099,
  "url": "https://hostname.s3.amazonaws.com/first-part?X-Amz-Algorithm=algorithm&X-Amz-Credential=credential-info&X-Amz-Date=creation-date&X-Amz-Expires=expiration-time&X-Amz-SignedHeaders=host&X-Amz-Signature=signature",
  "b64_identity": "encoded-identity-info",
  "timestamp": "2020-01-23T16:15:59.478901889Z"
}
```

### Message with optional attributes

```json5
{
  "account": 123456,
  "category": "test",
  "metadata": {
    "reporter": "",
    "stale_timestamp": "0001-01-01T00:00:00Z"
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
(stored as string, not an integer), auth_type and `internal` object.  Internal
object is important as it contains `org_id` (also stored as a string).

## Required attributes

* `identity` (object)

## Optional attributes

* `entitlements` (object)

## Examples

### Identity based on `basic-auth`

```json5
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

```json5
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

```json5
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

