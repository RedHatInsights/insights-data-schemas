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

Parquet factory reads several metrics from Thanos in order to combine the results and
generate Parquet files on an hourly basis called `cluster_thanos_info.parquet`.
It is independent from the reading of Kafka topics and so it doesn't need Kafka at all in
order to generate the `cluster_thanos_info.parquet` files.
The following two metrics are read:

1. `id_version_ebs_account_internal:cluster_subscribed`
1. `subscription_labels`

Especially querying for the second metric is very performance heavy on Thanos, therefore
results from querying for the first metric are used as a filter in a query for the second metric
to avoid Thanos timing out the query requests.

## Basic format

### Data taken from metrics `id_version_ebs_account_internal:cluster_subscribed`

* `_id` (string) - Cluster ID, contains UUID with cluster name
* `ebs_account` (string)

An example:

```
{_id="10bc27ef-1111-4fc8-85a2-a1231dc614e9", ebs_account="6181891"}
```

---
**NOTE**

`_id/ClusterName` uses its canonical textual representation: the 16 octets of a
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

* `_id` (string) - Cluster ID, contains UUID with cluster name
* `email_domain` (string)
* `managed` (bool)

An example:

```
{_id="4976be4c-1111-460b-a4cf-e22ed1d96923", email_domain="us.ibm.com", managed="false"}
```

---
**NOTE**

`_id/ClusterName` uses its canonical textual representation: the 16 octets of a
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
`parquet-tools show cluster_thanos_info.parquet --head 4`

```
+--------------------------------------+---------------+--------------------+-----------+---------------------+
| cluster_id                           |   ebs_account | email_domain       | managed   | collected_at        |
|--------------------------------------+---------------+--------------------+-----------+---------------------|
| 07c82637-1111-46d4-b741-d2f8bb189050 |     b'123456' | bkfs.com           | False     | 2021-02-12 08:00:00 |
| 2ef7ff7e-1111-41fd-8e67-763ba7ca68b5 |    b'1234565' | us.ibm.com         | False     | 2021-02-12 08:00:00 |
| b603b714-1111-4210-a73d-47fa0d1fa2f5 |    b'1234565' | us.ibm.com         | False     | 2021-02-12 08:00:00 |
| 35028b19-1111-422a-bc4c-ec164163b86e |    b'1234567' | redhat.com         | False     | 2021-02-12 08:00:00 |
+--------------------------------------+---------------+--------------------+-----------+---------------------+
``