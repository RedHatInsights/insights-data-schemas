---
layout: default
---
\[[Front page](../index.md)\] \[[Internal data pipeline](../internal_data_pipeline.md)\]

# Format of received Kafka messages from `ccx-XXX-insights-operator-archive-features` topic

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a S3 bucket. It is used to generate
different data aggregations in the CCX Internal Data Pipeline, reading data
from Kafka topics and Thanos service.

## Schema version

1 (unofficial)

## Description

## Basic format

## Possible enhancements

Version (positive integer) should be included in the generated Parquet files
into separate column.

## Examples

