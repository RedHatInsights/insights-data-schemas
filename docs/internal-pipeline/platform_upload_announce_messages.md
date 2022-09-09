---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Messages sent to AWS SQS with info about new S3 object

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

The messages sent to SQS can be represented as Python data structures provided
by SQS interface (Boto client). More information about Boto client can be found
on AWS site:
[https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html).

Common event format is described at
[https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html](https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html).

## Basic format

```JSON
{  
   "Service":"Amazon S3",
   "Event":"s3:TestEvent",
   "Time":"2021-02-01T18:00:00.000Z",
   "Bucket":"bucketname",
   "RequestId":"5582816E2AEA6FDF",
   "HostId":"8cLeGAwm098Xc5v4Zkwcom8vvZa3He3eKxszPBbw9Rr+sYdt6AnK4xpI8EXAMPLE"
}
```

---
**NOTE**

Format of such messages is not much relevant to internal data pipeline, as it
is just needed to consume data from SQS, not to produce or transform them.

---

## Possible enhancements

Not possible as the structure is dictated by AWS and Boto client.
