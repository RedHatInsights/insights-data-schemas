# Format of the received SQS messages consumed by SQS Listener

The messages received from SQS are represented as Python data structures
provided by SQS interface (Boto client).

## Basic format

The response is represented as Python dictionary and contains two parts -
namely `ResponseMetadata` and `Messages`. `ResponseMetadata` sub-structure is
required and is represented as a Python dictionary as well. `Messages` is a
list (of items with format described below) and is optional - when no messages
are available in SQS, this attribute is missing.

---
**NOTE**

For SQS Listener only the `Messages` attribute is relevant, because
`ResponseMetatada` is ignored in the current version.

---

### `ResponseMetadata` attribute

This attribute is basically Python dictionary with following attributes:

* `RequestId` (string) UUID of request
* `HTTPStatusCode` (string) contains HTTP status code in string form. Usually "200" status code is used
* `HttpHeaders` (dictionary of string:string) metadata with HTTP headers, uses at least `content-type` and `content-length`, but more headers can be provided (`date` etc.)
* `RetryAttempts` (positive integer or zero) number of attempts made to receive the message/messages

---
**NOTE**

UUID uses its canonical textual representation: the 16 octets of a UUID are
represented as 32 hexadecimal (base-16) digits, displayed in five groups
separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters (32
hexadecimal characters and 4 hyphens)

---

### `Messages` attribute

This attribute is basically Python list and each item in this list has
following attributes:

* `MessageId` (string) message UUID
* `ReceiptHandle` (string) handle, which is basically integer stored as string
* `MD5OfBody` (string) MD5 hash of message body, string consisting of 32 hexadecimal digits
* `Body` (string) message body in JSON stored into string
* `Attributes` (dictionary) additional message attributes, these attributes are described below

---
**NOTE**

UUID uses its canonical textual representation: the 16 octets of a UUID are
represented as 32 hexadecimal (base-16) digits, displayed in five groups
separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters (32
hexadecimal characters and 4 hyphens).

---
**NOTE**

The 128-bit (16-byte) MD5 hashes (also termed message digests) are represented
as a sequence of 32 hexadecimal digits.
---

#### Structure of `Body` sub-attribute

This attribute contains string that represents JSON data in following format:

```json
{
  "Records": [
    {
      "s3": {
        "object": {
          "key": "1234567/abcd1234-1234-abcd-5678-1234abcd1234/20200609125740-1234567890abcdef1234567890abcdef",
          "size": 11805,
          "eTag": "9876543210abcdef9876543210abcdef",
          "sequencer": "00E5FD87444DFD5752"
        }
      }
    }
  ]
}
```

The most important sub-attribute is `key` that can be used to access data in S3 bucket.

#### Structure of `Attributes` sub-attribute

This is simple Python dictionary with following attributes:

* `SenderId` (string) ID of message sender
* `ApproximateFirstReceiveTimestamp` (string) time stamp when the message was first received
* `ApproximateReceiveCount` (string) how many times the message was received (usually 1)
* `SentTimestamp` (string) time stamp when the message was sent

## Examples

### Structure returned when the queue is empty

```python
{
    "ResponseMetadata": {
        "RequestId": "12345678-aaaa-bbbb-cccc-dddddddddddd",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "98765432-1111-2222-3333-1234abcd1234",
            "date": "Tue, 09 Jun 2020 12:51:50 GMT",
            "content-type": "text/xml",
            "content-length": "240",
        },
        "RetryAttempts": 0,
    }
}
```

### Structure returned when the queue contains at least one message

```python
{
    "Messages": [
        {
            "MessageId": "abcd1234-1234-abcd-5678-1234abcd1234",
            "ReceiptHandle": "123",
            "MD5OfBody": "09b5bfe7a082c6f4f24c0e81cafebabe",
            "Body": '{"Records": [{"s3": {"object": {"key": "1234567/abcd1234-1234-abcd-5678-1234abcd1234/20200609125740-1234567890abcdef1234567890abcdef","size": 11805,"eTag": "9876543210abcdef9876543210abcdef","sequencer": "00E5FD87444DFD5752"}}}]}',
            "Attributes": {
                "SenderId": "123456",
                "ApproximateFirstReceiveTimestamp": "1591707477622",
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1591707468964",
            },
        }
    ],
    "ResponseMetadata": {
        "RequestId": "12345678-aaaa-bbbb-cccc-dddddddddddd",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "98765432-1111-2222-3333-1234abcd1234",
            "date": "Tue, 09 Jun 2020 12:51:50 GMT",
            "content-type": "text/xml",
            "content-length": "22437",
        },
        "RetryAttempts": 0,
    },
}
```

