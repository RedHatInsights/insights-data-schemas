---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Messages produced by Multiplexor service and sent to `XXX-ols-archive-new` topic

Multiplexor Service classify every new archive by reading the related
information from `XXX-archive-new` (where `XXX` needs to be replaced by
environment, for example `prod`) Kafka topic, downloading the archive
from AWS S3 and checking its content to classify it and send the same message
to different topics according to its classification.

Information about Openshift Lightspeed generated archives are sent to
`XXX-ols-archive-new`.

## Schema version

1 (unofficial)

## Description

Messages consumed from `XXX-io-archive-new` topic (where `XXX` needs to be replaced by
environment, for example `prod`) are created by SQS listener for each new object created
in S3. These messages have very simple format consisting of just three attributes:

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

## Possible enhancements

Not needed at this moment as the schema is super simple.
