---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Format of the received SQS messages consumed by SQS Listener

SQS listener service listens to notifications sent to AWS SQS (Simple Queue
Service) about new files in the S3 bucket. It sends a message with S3 path of
the file to `ccx-XXX-insights-operator-archive-new` (where `XXX` needs to be
changed to `prod` etc.) Kafka topic for every new file in S3.

As there is only one queue in SQS, we have only one SQS Listener deployed (in
production environment) that sends notifications to 3 environments: dev, qa and
prod.

## Schema version

1 (unofficial)

## Description

The messages received from SQS are represented as Python data structures
provided by SQS interface (Boto client). More information about Boto client can
be found on AWS site:
[https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html).

Common event format is described at [https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html](https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html).

## Basic format

The response is represented as a standard Python dictionary and contains two
parts - namely `ResponseMetadata` and `Messages`. `ResponseMetadata`
sub-structure is required and is represented as a Python dictionary as well.
`Messages` is represented as a list (of items with format described below) and
is optional - when no messages are available in SQS, this attribute is missing.

---
**NOTE**

For SQS Listener only the `Messages` attribute is relevant, because
`ResponseMetatada` attribute is ignored in the current version of SQS consumer
code.

---

### `ResponseMetadata` attribute

This attribute is basically a standard Python dictionary with following
attributes:

* `RequestId` (string) UUID of request
* `HTTPStatusCode` (string) contains HTTP status code in string form. Usually "200" status code is used in most situations
* `HttpHeaders` (dictionary of string:string) metadata with HTTP headers, uses at least `content-type` and `content-length`, but more headers can be provided (`date` etc.)
* `RetryAttempts` (positive integer or zero) number of attempts made to receive the message or messages

---
**NOTE**

UUID uses its canonical textual representation: the 16 octets of a UUID are
represented as 32 hexadecimal (base-16) digits, displayed in five groups
separated by hyphens, in the form 8-4-4-4-12 for a total of 36 characters (32
hexadecimal characters and 4 hyphens). For more information please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

---

### `Messages` attribute

This attribute is basically represented as a standard Python list and each item
in this list has following attributes:

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
hexadecimal characters and 4 hyphens). For more information please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---
**NOTE**

The 128-bit (16-byte) MD5 hashes (also termed message digests) are represented
as a sequence of 32 hexadecimal digits. For more information please look at
https://en.wikipedia.org/wiki/MD5
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

The most important sub-attribute is `key` that can be used to access data in S3
bucket. It is the unique identifier of an object stored in S3.

#### Structure of `Attributes` sub-attribute

This is simple Python dictionary with following attributes:

* `SenderId` (string) ID of message sender
* `ApproximateFirstReceiveTimestamp` (string) time stamp with moment when the message was first received
* `ApproximateReceiveCount` (string) how many times the message was received (usually 1)
* `SentTimestamp` (string) time stamp with moment when the message was sent

## Examples

The following examples can be used to test the actual code or validators.
Please note that `RequestId` and other sensitive information are changed
accordingly so no real info is exposed.

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

### Possible enhancements

Not possible as the structure is dictated by AWS and Boto client.
