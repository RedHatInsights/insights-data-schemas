---
layout: default
---
# Insights Data Schemas

## Internal data pipeline

<img src="images/internal-data-pipeline-architecture.png" alt="Internal data pipeline" usemap="#internal-pipeline">

1. [Incoming messages in `platform.upload.buckit`](platform_upload_buckit_messages.md)
1. [Incoming messages from SQS](incoming_sqs_messages.md)
1. [Messages produced by SQS listener](sqs_listener_messages.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-new` topic](insights_operator_archive_new.md)
1. [Raw data stored in S3 bucket](raw_data_S3_bucket.md)
1. [Raw data stored into Ceph bucket](raw_data_Ceph_bucket.md)
1. [Messages produced by archive-sync-service](archive_sync_service_messages.md)
1. [Messages consumed by Rules service from `ccx-XXX-insights-operator-archive-synced` topic](insights_operator_archive_synced.md)
1. [Messages consumed by Features service from `ccx-XXX-insights-operator-archive-synced` topic](insights_operator_archive_synced.md)
1. [Messages produced by Rules service](rules_service_messages.md)
1. [Messages produced by Features service](features_service_messages.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic](parquet_rules_results.md)
1. [Data consumed from Thanos](parquet_thanos.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-features` topic](parquet_features.md)
1. [Generated parquet files](parquet_output.md)

### Parquet factory

Parquet Factory is a program that can read data from several data sources,
aggregate the data received from them and generate a set of Parquet files with
the aggregated data, storing them in a S3 bucket. It is used to generate
different data aggregations in the CCX Internal Data Pipeline, reading data
from Kafka topics and Thanos service.

<img src="images/parquet-factory.png" alt="Parquet factory" usemap="#parquet-factory">
<map name="parquet-factory">
    <area shape="rect" coords="130, 34, 170, 64"   title="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-rules-results topic" href="parquet_rules_results.html">
    <area shape="rect" coords="130, 212, 170, 242" title="Messages consumed from ccx-XXX-insights-operator-archive-features topic" alt="Messages consumed from ccx-XXX-insights-operator-archive-features topic" href="parquet_features.html">
    <area shape="rect" coords="295, 83, 335, 114"  title="Data consumed from Thanos" alt="Data consumed from Thanos" href="parquet_thanos.html">
    <area shape="rect" coords="389, 165, 429, 195" title="Generated parquet files" alt="Generated parquet files" href="parquet_output.html">
</map>

1. [Messages consumed from `ccx-XXX-insights-operator-archive-rules-results` topic](parquet_rules_results.md)
1. [Messages consumed from `ccx-XXX-insights-operator-archive-features` topic](parquet_features.md)
1. [Data consumed from Thanos](parquet_thanos.md)
1. [Generated parquet files](parquet_output.md)
