---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Format of data read by Parquet factory from Thanos

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a selected S3 bucket. It is used to
generate different data aggregations in the CCX Internal Data Pipeline, reading
data from Kafka topics and Thanos service.

## Schema version

1 (unofficial)

## Description

Parquet factory reads several metrics from Thanos in order to combine such
metrics with messages consumed from Kafka topics and generate Parquet files.
Especially the following two metrics are read:

1. `id_version_ebs_account_internal:cluster_subscribed`
1. `subscription_labels`

## Basic format

### Data taken from metrics `id_version_ebs_account_internal:cluster_subscribed`

* `cluster_id` (string) contains UUID with cluster name
* `ebs_account` (string)

An example:

---
**NOTE**

`ClusterName` uses its canonical textual representation: the 16 octets of a
UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens). For more information
please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---
### Data taken from metrics `subscription_labels`

* `cluster_id` (string) contains UUID with cluster name
* `email_domain` (string)
* `managed` (bool)

An example:

---
**NOTE**

`ClusterName` uses its canonical textual representation: the 16 octets of a
UUID are represented as 32 hexadecimal (base-16) digits, displayed in five
groups separated by hyphens, in the form 8-4-4-4-12 for a total of 36
characters (32 hexadecimal characters and 4 hyphens). For more information
please look at
[https://en.wikipedia.org/wiki/Universally_unique_identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier).

An example of UUID:

```
3ba9b042-b8b8-4714-98e9-17915c2eeb95
```

---

## Possible enhancements

N/A

## Examples
