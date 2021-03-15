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
* `support` (string) - indicates level of paid cluster support

An example:

```
{_id="4976be4c-1111-460b-a4cf-e22ed1d96923", email_domain="us.ibm.com", managed="false", support="Premium"}
```

---
**NOTE**

`support` is one of None, Eval, Standard, Premium, Self-Support.

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

Thanos will be decomissioned by DataHub team probably in Q2 2021, so any possible enhancements might be a waste of time.

- The Thanos part of parquet-factory currently works by making queries to Thanos for 1 hour time windows (to generate hourly parquet files easily), however, the execution waits for ALL the queries to finish before dumping the data from memory to parquet files. For example, we want to generate data for 24 hours back, the parquet-factory queries Thanos for data for 24-23, 23-22, etc., after we have data for all of the time windows, the parquet files generation starts.

1) generate the hourly parquet files right when we receive all the data for the given hour and not wait for other queries to finish
2) (over the top) parallelize the aggregation for each hour-window - this might not even be possible with the Thanos timeouts and probably not necessary at all, because it only takes about 20s for each 1-hour window to aggegate.


## Examples
`parquet-tools show cluster_thanos_info.parquet --head 4`

```
+--------------------------------------+---------------+-------------------+-----------+--------------+---------------------+
| cluster_id                           |   ebs_account | email_domain      | managed   | support      | collected_at        |
|--------------------------------------+---------------+-------------------+-----------+--------------+---------------------|
| 12345678-ec5b-4552-9e2d-76c7bc4dee8f |    b'1234567' | us.ibm.com        | False     | None         | 2021-03-14 02:59:00 |
| 12345678-ef92-4ee2-84c9-478f99b76fdb |    b'1234500' | customer1.com     | False     | Self-Support | 2021-03-14 02:59:00 |
| 12345678-c145-4b12-850b-56a9de766d9c |    b'1234567' | us.ibm.com        | False     | None         | 2021-03-14 02:59:00 |
| 12345678-6d6f-490d-a6e2-0e01fbbb962d |    b'1234600' | customer2.com     | False     | None         | 2021-03-14 02:59:00 |
| 12345678-bde1-4e51-84e7-378030599471 |    b'1234700' | customer3.com     | False     | Premium      | 2021-03-14 02:59:00 |
| 12345678-f0c3-4b44-80d2-ed6b5fc6c95f |    b'1234567' | us.ibm.com        | False     | Eval         | 2021-03-14 02:59:00 |
| 12345678-8eb8-4d85-828d-ce940f1b9778 |    b'1234800' | us.ibm.com        | False     | Eval         | 2021-03-14 02:59:00 |
| 12345678-8169-4a66-8c17-ce3a15eb81d3 |     b'123000' | customer4.co      | False     | Premium      | 2021-03-14 02:59:00 |
+--------------------------------------+---------------+-------------------+-----------+--------------+---------------------+
```