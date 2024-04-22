---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Messages produced by SQS listener

SQS listener service listens to notifications sent to AWS SQS (Simple Queue
Service) about new files in the S3 bucket. It sends a message with S3 path of
the file to `[qa|prod]-archive-new` Kafka topic for every new file in S3.

As there is only one queue in SQS, we have only one SQS Listener deployed (in
production environment) that sends notifications to 2 environments: qa and prod.

## Schema version

1 (unofficial)

## Description

Messages produced into `[qa|prod]-archive-new` topic are created by SQS listener
for each new object created in S3. These messages have very simple format
consisting of just three attributes:

* cluster ID
* path to S3 object
* message ID


## Basic format

Messages are stored in JSON format and have to contain three attributes:

* `cluster_id` (string with UUID value) cluster ID
* `path` (string) path to an object stored in AWS S3
* `sqs_message_id` (positive integer) ID of the SQS message

### `cluster_id` attribute

Attribute `cluster_id` uses its canonical textual representation: the 16 octets
of a UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens).  For more information
please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

### `path` attribute

This attribute contains path to object stored in AWS S3. It must be real path
with chunks splitted by slash character.

An example of path:

```
1234567/abcd1234-1234-abcd-5678-1234abcd1234/20200609125740-1234567890abcdef1234567890abcdef
```

### `sqs_message_id` attribute

This attribute contains a positive integer with message ID that can be used to
delete message on delivery (in SQS Listener)

An example of message ID:

```
123
```

## Attributes extraction

Messages taken from SQS has the following format:

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

Two sub-nodes are needed to construct a new message:

* `Messages[0]/ReceiptHandle`
* `Messages[0]/Body`

The first sub-node is used to create `sqs_message_id`. Second sub-node needs to
be deserialized from JSON. Deserialized form of `Body` sub-node looks like:

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

`path` is gathered from `key` sub-sub-node. `cluster_id` as also recreated from
`key` sub-node by taking the second item from path. For example if the `key`
attribute contains:

```
1234567/abcd1234-1234-abcd-5678-1234abcd1234/20200609125740-1234567890abcdef1234567890abcdef
```

`cluster_id` will be:

```
abcd1234-1234-abcd-5678-1234abcd1234
```

## Possible enhancements

Not needed at this moment as the schema is super simple.
